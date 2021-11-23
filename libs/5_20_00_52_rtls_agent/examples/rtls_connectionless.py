import os
import queue
import sys
import threading
import time
import datetime
import json
import shutil
import subprocess

import pandas as pd

## Uncomment line below for local debug of packages
# sys.path.append(r"../unpi")
# sys.path.append(r"../rtls")
# sys.path.append(r"../rtls_util")

from rtls_util import RtlsUtil, RtlsUtilLoggingLevel, RtlsUtilException, RtlsUtilTimeoutException, \
    RtlsUtilCoordinatorNotFoundException, RtlsUtilEmbeddedFailToStopScanException, \
    RtlsUtilScanResponderNotFoundException, RtlsUtilScanNoResultsException, RtlsUtilFailToConnectException


class RtlsConnectionlessExample(object):
    dummy_responder = {'addr': 'FF:FF:FF:FF:FF:FF',
                       'addrType': 0,
                       'rssi': 0,
                       'advSID': 0,
                       'periodicAdvInt': 0
                       }

    USE_GIVEN_ADDRESS_AND_REPORT_ENABLE = 0
    USE_LIST_AND_REPORT_ENABLE = 1
    USE_GIVEN_ADDRESS_AND_REPORT_DISABLE = 2
    USE_LIST_AND_REPORT_DISABLE = 3

    def __init__(self, coordinator_comport, responder_bd_addrs, scan_time, sync_params, use_advertiser_list,
                 start_periodic_advertise_report_on_sync, periodic_advertise_report, angle_of_arrival,
                 angle_of_arrival_params, data_collection_duration, data_collection_iteration, post_analyze_func=None,
                 timeout=30):
        self.headers = ['pkt', 'sample_idx', 'rssi', 'ant_array', 'channel', 'i', 'q', 'slot_duration', 'sample_rate',
                        'filtering']

        self.coordinator_comport = coordinator_comport
        self.responder_bd_addrs = responder_bd_addrs

        self.devices = [{"com_port": coordinator_comport, "baud_rate": 460800, "name": "Coordinator"}]

        self.scan_time = scan_time
        self.sync_params = sync_params
        self.use_advertiser_list = use_advertiser_list
        self.start_periodic_advertise_report_on_sync = start_periodic_advertise_report_on_sync

        self.all_sync_responders = []

        self.enable_periodic_advertise_report = periodic_advertise_report

        self.enable_angle_of_arrival = angle_of_arrival
        self.angle_of_arrival_params = angle_of_arrival_params

        self.data_collection_duration = data_collection_duration
        self._data_collection_iteration = data_collection_iteration
        self._current_iteration = -1
        self.csv_files = []

        self.post_analyze_func = post_analyze_func

        self.timeout = timeout

        self._data_collection_in_process = threading.Event()
        self._data_collection_in_process.clear()

        self._periodic_advertise_report_thread = None
        self._angle_of_arrival_thread = None

    @property
    def data_collection_iteration(self):
        return self._data_collection_iteration

    @property
    def current_iteration(self):
        return self._current_iteration

    @current_iteration.setter
    def current_iteration(self, valuw):
        print(f"\n {'=' * 10} Starting Loop {valuw + 1} {'=' * 10}")
        self._current_iteration = valuw

    def _get_example_parameters(self):
        example_parameters = "\n"
        example_parameters += "Example Input Parameters\n"
        example_parameters += "----------------------------------------------------------------------\n"
        example_parameters += f"Coordinator comport                     : {self.coordinator_comport}\n"
        example_parameters += f"Responder BD Address                    : {self.responder_bd_addrs}\n"
        example_parameters += f"Scan time                               : {self.scan_time} Sec\n"
        example_parameters += f"Sync Params                             : \n"
        example_parameters += f"    Sync Skip                           : {self.sync_params.get('sync_skip', 0)}\n"
        example_parameters += f"Use Advertiser List                     : {'Yes' if self.use_advertiser_list else 'No'}\n"
        example_parameters += f"Start Periodic Advertise Report on Sync : {'Yes' if self.start_periodic_advertise_report_on_sync else 'No'}\n"
        example_parameters += f"Enable Periodic Advertise Report        : {'Yes' if self.enable_periodic_advertise_report else 'No'}\n"
        example_parameters += f"Enable Angle Of Arrival (AoA)           : {'Yes' if self.enable_angle_of_arrival else 'No'}\n"
        example_parameters += f"    AoA Enable Filter                   : {'Yes' if self.angle_of_arrival_params.get('enable_filter', True) else 'No'}\n"
        example_parameters += f"    AoA Slot Duration                   : {self.angle_of_arrival_params.get('slot_duration', 2)}\n"
        example_parameters += f"    AoA Sample Rate                     : {self.angle_of_arrival_params.get('sample_rate', 1)}\n"
        example_parameters += f"    AoA Sample Size                     : {self.angle_of_arrival_params.get('sample_size', 1)}\n"
        example_parameters += f"Data Collection Duration                : {self.data_collection_duration}\n"
        example_parameters += f"Data Collection iteration               : {self.data_collection_iteration}\n"
        example_parameters += f"Provide Post Analyze Function           : {'Yes' if self.post_analyze_func else 'No'}\n"
        example_parameters += f"Example Log Dir                         : {os.path.dirname(self.logging_file)}\n"
        example_parameters += f"Example Log File Name                   : {os.path.basename(self.logging_file)}\n"
        example_parameters += "----------------------------------------------------------------------\n"
        example_parameters += "\n"

        return example_parameters

    def _get_date_time(self):
        return datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

    def _get_logging_file_path(self):
        data_time = self._get_date_time()
        logging_file_path = os.path.join(os.path.curdir, os.path.basename(__file__).replace('.py', '_log'))

        if not os.path.isdir(logging_file_path):
            os.makedirs(logging_file_path)

        logging_file = os.path.join(logging_file_path,
                                    f"{data_time}_{os.path.basename(__file__).replace('.py', '.log')}")

        return os.path.abspath(logging_file)

    def _get_csv_file_name_for(self, identifier, conn_handle, loop_count, with_date=True):
        data_time = self._get_date_time()
        logging_file_path = self._get_logging_file_path()
        logging_file_dir = os.path.dirname(logging_file_path)

        identifier = identifier.lower().replace(":", "")
        if with_date:
            filename = os.path.join(logging_file_dir,
                                    f"{data_time}_rtls_raw_iq_samples_{identifier}_{conn_handle}_loop{loop_count}.csv")
        else:
            filename = os.path.join(logging_file_dir,
                                    f"rtls_raw_iq_samples_{identifier}_{conn_handle}_loop{loop_count}.csv")

        return filename

    def initialize(self, debug=False):
        try:
            self.logging_file = self._get_logging_file_path()

            self.rtls_util = RtlsUtil(self.logging_file,
                                      RtlsUtilLoggingLevel.DEBUG if debug else RtlsUtilLoggingLevel.INFO)
            self.rtls_util.timeout = self.timeout

            self.rtls_util.add_user_log(self._get_example_parameters())

            ## Setup devices
            self.coordinator_node, self.passive_nodes, self.all_nodes = self.rtls_util.set_devices(self.devices)
            # print(f"Coordinator : {self.coordinator_node} \nPassives : {self.passive_nodes} \nAll : {self.all_nodes}")

            self.rtls_util.reset_devices()
            print("Devices Reset")

            return True

        except RtlsUtilCoordinatorNotFoundException:
            print('No one of given devices identified as RTLS Coordinator')
            return False

    def scan_and_sync(self, sync_retry=5):
        self.all_sync_responders = []

        try:
            print(f"Start scan for {self.scan_time} sec")
            scan_results = self.rtls_util.scan(self.scan_time)

            scan_results_for_cl_aoa = [scan_result for scan_result in scan_results if scan_result['periodicAdvInt'] > 0]
            p_scan_results_for_cl_aoa = '\n\t\t' + '\n\t\t'.join([str(r) for r in scan_results_for_cl_aoa])
            print(f"Scan results:{p_scan_results_for_cl_aoa}")

            # Checking if all required responder found by coordinator and creating sync list
            if self.responder_bd_addrs:
                scan_results_for_cl_aoa_bdaddr = [scan_result['addr'] for scan_result in scan_results_for_cl_aoa]
                if not all([s in scan_results_for_cl_aoa_bdaddr for s in self.responder_bd_addrs]):
                    raise RtlsUtilException("One or more Responders in required list not found by Coordinator")

                responders_sync_with = [responder for responder in scan_results_for_cl_aoa if
                                        responder['addr'] in self.responder_bd_addrs]
            else:
                responders_sync_with = scan_results_for_cl_aoa

            # sync_skip : The maximum number of periodic advertising events that can be skipped after a successful receive
            # (Range: 0x0000 to 0x01F3)
            sync_skip = self.sync_params.get('sync_skip', 0)

            # sync_cte_type : Clear All Bits(0) - Sync All
            # sync_cte_type : Set Bit 0(1) - Do not sync to packets with an AoA CTE
            # sync_cte_type : Set Bit 1(2) - Do not sync to packets with an AoD CTE with 1 us slots
            # sync_cte_type : Set Bit 2(4) - Do not sync to packets with an AoD CTE with 2 us slots
            # sync_cte_type : Set Bit 4(16) - Do not sync to packets without a CTE
            sync_cte_type = 0

            p_responders_sync_with = '\n\t\t' + '\n\t\t'.join([str(r) for r in responders_sync_with])
            print(f"Example will try sync with:{p_responders_sync_with}")
            if self.use_advertiser_list:
                print("Using advertisers list to create sync")
                # Add all devices to periodic advertiser listen
                for responder in responders_sync_with:
                    self.rtls_util.padv_add_device_to_periodic_adv_list(responder)
                    print(f"\t\tResponder {responder['addr']} has been added to advertisers list")


                max_periodic_adv_interval = max([responder['periodicAdvInt'] for responder in responders_sync_with])
                sync_timeout = int(max_periodic_adv_interval * 1.25) * (sync_skip if sync_skip > 0 else 1)

                for attempt in range(len(responders_sync_with)):
                    print(
                        f"Starting attempt #{attempt + 1} to make sure that all required responder successfully connected")

                    # responder information has no meaning when using advertiser list to create sync
                    self.rtls_util.padv_create_sync(self.dummy_responder,
                                                    self.USE_LIST_AND_REPORT_ENABLE if self.start_periodic_advertise_report_on_sync else self.USE_LIST_AND_REPORT_DISABLE,
                                                    sync_skip,
                                                    sync_timeout,
                                                    sync_cte_type)

                    # Scan again for sync established event - reports will be enabled automatically
                    self.rtls_util.scan(self.scan_time)

                    self.all_sync_responders = [responder for responder in responders_sync_with if
                                                self.rtls_util.padv_get_sync_handle_by_responder(responder) >= 0]

                    if len(self.all_sync_responders) == len(responders_sync_with):
                        break
                else:
                    raise RtlsUtilFailToConnectException(
                        f"After {len(responders_sync_with)} attempts not all required responders successfully connected")
            else:
                for responder in responders_sync_with:
                    
                    sync_timeout = int(responder['periodicAdvInt'] * 1.25) * (sync_skip if sync_skip > 0 else 1)

                    self.rtls_util.padv_create_sync(responder,
                                                    self.USE_GIVEN_ADDRESS_AND_REPORT_ENABLE if self.start_periodic_advertise_report_on_sync else self.USE_GIVEN_ADDRESS_AND_REPORT_DISABLE,
                                                    sync_skip,
                                                    sync_timeout,
                                                    sync_cte_type)

                    for attempt in range(sync_retry):
                        print(f"Starting attempt #{attempt + 1} to sync with {responder['addr']}")

                        self.rtls_util.scan(self.scan_time)

                        sync_handle = self.rtls_util.padv_get_sync_handle_by_responder(responder)
                        if sync_handle >= 0:
                            print(f"Sync with: {responder['addr']} succeed with handle: {sync_handle}")
                            self.all_sync_responders.append(responder)
                            break

                        if self.rtls_util.sync_failed_to_be_est:
                            raise RtlsUtilFailToConnectException(
                                f"Sync faild to be established for responder: {responder['addr']} SID: {responder['advSID']}")

            print("All required responders successfully connected !")
            return len(self.all_sync_responders) > 0

        except RtlsUtilEmbeddedFailToStopScanException:
            return False
        except RtlsUtilScanResponderNotFoundException:
            print("Required responder didn't found in scan list")
            return False
        except RtlsUtilScanNoResultsException:
            return False
        except RtlsUtilException:
            return False

    def disconnect(self):
        for responder in self.all_sync_responders:
            sync_handle = self.rtls_util.padv_get_sync_handle_by_responder(responder)
            self.rtls_util.padv_terminate_sync(sync_handle)
            print(f"Coordinator terminated sync from responder with sync handle {sync_handle}")

    # Thread for Periodic Advertise Report monitoring
    # Should not be called by user's application.
    # Please use functions start_periodic_advertise_report and stop_periodic_advertise_report instead.
    def _periodic_advertise_report_result(self):
        while self._data_collection_in_process.is_set():
            data_time = datetime.datetime.now().strftime("[%m:%d:%Y %H:%M:%S:%f] :")

            try:
                padv_data = self.rtls_util.padv_event_queue.get_nowait()
                print(f"{data_time} {json.dumps(padv_data)}")
            except queue.Empty:
                pass

    def start_periodic_advertise_report(self):
        self._continues_connection_info_thread = threading.Thread(target=self._periodic_advertise_report_result)
        self._continues_connection_info_thread.daemon = True

        if self.enable_periodic_advertise_report:
            self._periodic_advertise_report(True)

    def stop_periodic_advertise_report(self):
        if self.enable_periodic_advertise_report or self.start_periodic_advertise_report_on_sync:
            self._periodic_advertise_report(False)

        self._continues_connection_info_thread = None
        self.rtls_util._empty_queue(self.rtls_util.padv_event_queue)

    def _periodic_advertise_report(self, enable):
        for responder in self.all_sync_responders:
            sync_handle = self.rtls_util.padv_get_sync_handle_by_responder(responder)

            if sync_handle == -1:
                print(f"Responder {responder['addr']} probably disconnected in a process, "
                      f"skip periodic advertise report {'enabling' if enable else 'disabling'}.")
                continue

            if enable:
                self.rtls_util.padv_periodic_receive_enable(sync_handle)
                print(f"Periodic report enabled for {responder['addr']}")
            else:
                self.rtls_util.padv_periodic_receive_disable(sync_handle)
                print(f"Periodic report disabled for {responder['addr']}")

    # Thread for AoA sampling collection and storage
    # Should not be called by user's application.
    # Please use functions start_angle_of_arrival and stop_angle_of_arrival instead.
    def _angle_of_arrival_result(self):
        TABLE = None
        pkt_count = 0
        current_csv_files = set()

        while self._data_collection_in_process.is_set():
            data_time = datetime.datetime.now().strftime("[%m:%d:%Y %H:%M:%S:%f] :")

            try:
                aoa_data = self.rtls_util.cl_aoa_results_queue.get_nowait()
                # print(f"{data_time} {json.dumps(aoa_data)}")

                if 'type' in aoa_data and aoa_data['type'] == "RTLS_CMD_CL_AOA_RESULT_RAW":
                    if TABLE is None:
                        TABLE = pd.DataFrame(columns=self.headers)

                    identifier = aoa_data["identifier"]
                    connHandle = aoa_data['payload']['syncHandle']
                    channel = int(aoa_data['payload']['channel'])
                    offset = int(aoa_data['payload']['offset'])
                    rssi = aoa_data['payload']['rssi']
                    antenna = 6
                    samplesLength = aoa_data['payload']["samplesLength"]

                    df_by_channel = TABLE.loc[TABLE['channel'] == channel]

                    for indx, sample in enumerate(aoa_data['payload']['samples']):
                        sample_idx = offset + indx
                        if sample_idx in list(df_by_channel['sample_idx']):
                            TABLE = TABLE.drop(
                                TABLE[(TABLE['channel'] == channel) & (
                                        TABLE['sample_idx'] == sample_idx)].index.values
                            )

                        sample_i = sample['i']
                        sample_q = sample['q']

                        row = {
                            'pkt': 0,
                            'sample_idx': sample_idx,
                            'rssi': rssi,
                            'ant_array': antenna,
                            'channel': channel,
                            'i': sample_i,
                            'q': sample_q,
                            'slot_duration': self.angle_of_arrival_params.get('slot_duration', 2),
                            'sample_rate': self.angle_of_arrival_params.get('sample_rate', 1),
                            'filtering': int(not self.angle_of_arrival_params.get('enable_filter', True))
                        }
                        TABLE = TABLE.append(row, ignore_index=True)

                    df_by_channel = TABLE.loc[TABLE['channel'] == channel]

                    if len(df_by_channel) == samplesLength:
                        df_by_channel = df_by_channel.sort_values(by=['sample_idx'])
                        df_by_channel.loc[:, "pkt"] = df_by_channel.loc[:, "pkt"].replace(to_replace=0,
                                                                                          value=pkt_count)

                        csv_file_name = self._get_csv_file_name_for(identifier, connHandle, self.current_iteration + 1,
                                                                    with_date=False)
                        current_csv_files.add(csv_file_name)

                        if os.path.isfile(csv_file_name):
                            df_by_channel.to_csv(csv_file_name, mode='a', index=False, header=False)
                        else:
                            df_by_channel.to_csv(csv_file_name, index=False)
                        print(f"{data_time} Added new set of IQ into {csv_file_name}")

                        pkt_count += 1
                        TABLE = TABLE.loc[TABLE['channel'] != channel]
            except queue.Empty:
                pass

        for current_csv_file in list(current_csv_files):
            current_csv_file_dirname = os.path.dirname(current_csv_file)
            current_csv_file_basename = os.path.basename(current_csv_file)
            dt = self._get_date_time()

            new_csv_file = os.path.join(current_csv_file_dirname, f"{dt}_{current_csv_file_basename}")
            os.rename(current_csv_file, new_csv_file)
            print(f"Rename {os.path.basename(current_csv_file)} into {os.path.basename(new_csv_file)}")

            if self.post_analyze_func:
                print(f"\nExecuting post analyze script on {new_csv_file}")
                output = self.post_analyze_func(new_csv_file)
                self.rtls_util.add_user_log(output)

            self.csv_files.append(new_csv_file)

    def start_angle_of_arrival(self):
        self._angle_of_arrival_thread = None

        if self.enable_angle_of_arrival:
            self._angle_of_arrival_thread = threading.Thread(target=self._angle_of_arrival_result)
            self._angle_of_arrival_thread.daemon = True

            self._angle_of_arrival(True)

    def stop_angle_of_arrival(self):
        if self.enable_angle_of_arrival:
            self._angle_of_arrival(False)

        self._angle_of_arrival_thread = None
        self.rtls_util._empty_queue(self.rtls_util.cl_aoa_results_queue)

    def _angle_of_arrival(self, enable):
        aoa_params = {
            "cl_aoa_role": "AOA_COORDINATOR",
            "cl_aoa_result_mode": "AOA_MODE_RAW",
            "cl_aoa_slot_durations": self.angle_of_arrival_params.get('slot_duration', 2),
            "cl_aoa_sample_rate": self.angle_of_arrival_params.get('sample_rate', 1),
            "cl_aoa_sample_size": self.angle_of_arrival_params.get('sample_size', 1),
            "cl_aoa_sampling_control": int(
                '0x10' if self.angle_of_arrival_params.get('enable_filter', True) else '0x11',
                16),
            "max_sample_cte": 1,
            "cl_aoa_pattern_len": 36,
            "cl_aoa_ant_pattern": [0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 6, 7,
                                   8, 9, 10, 11, 6, 7, 8, 9, 10, 11]
        }

        for responder in self.all_sync_responders:
            if enable:
                self.rtls_util.cl_aoa_start(aoa_params, responder)
                print(f"Connectionless AOA started for {responder['addr']}\n")
            else:
                self.rtls_util.cl_aoa_stop(aoa_params, responder)
                print(f"\nConnectionless AOA stoped for {responder['addr']}")

    def sleep(self):
        self._data_collection_in_process.set()

        if self._continues_connection_info_thread:
            self._continues_connection_info_thread.start()

        if self._angle_of_arrival_thread:
            self._angle_of_arrival_thread.start()

        print(f"\nExample will now wait for result for {self.data_collection_duration} sec\n")
        timeout = time.time() + self.data_collection_duration
        while timeout >= time.time():
            time.sleep(0.1)

        self._data_collection_in_process.clear()

        if self._continues_connection_info_thread:
            self._continues_connection_info_thread.join()

        if self._angle_of_arrival_thread:
            self._angle_of_arrival_thread.join()

    def done(self):
        self.rtls_util.done()


def post_analyze_of_IQ_data(csv_file):
    print(f"Analyzing file : {csv_file}")
    # Place here you code for IQ data post-analyze algorithms
    return "Return here output of your post-analyze algorithm"


def main():
    example = RtlsConnectionlessExample(
        coordinator_comport="COM8",
        responder_bd_addrs=[],  # ['80:6F:B0:1E:39:02', '80:6F:B0:1E:38:C3']
        scan_time=10,
        sync_params={
            'sync_skip': 0
        },
        use_advertiser_list=True,
        start_periodic_advertise_report_on_sync=False,
        periodic_advertise_report=False,
        angle_of_arrival=True,
        angle_of_arrival_params={
            'enable_filter': True,
            'slot_duration': 2,
            'sample_rate': 1,
            'sample_size': 1,
        },
        data_collection_duration=30,
        data_collection_iteration=1,
        post_analyze_func=post_analyze_of_IQ_data
    )

    # Perform initialization of RTLS Util, setup devices and reset them
    # Parameters used: coordinator_comport, passive_comports
    if example.initialize():

        # Perform Scan and Sync with required responders
        # Parameters used: responder_bd_addrs, scan_time, sync_params, use_advertiser_list, start_periodic_advertise_report_on_sync
        if example.scan_and_sync():

            # Execute next action in loop
            # Parameters used: data_collection_iteration
            for example.current_iteration in range(example.data_collection_iteration):
                # Start RSSI vs Channel, TX Power amd Data report (if enabled)
                # Parameters used: periodic_advertise_report
                example.start_periodic_advertise_report()

                # Start Angle of Arrival report (if enabled)
                # Parameters used: angle_of_arrival, angle_of_arrival_params
                example.start_angle_of_arrival()

                # Example start all inner threads for result collecting and sleep for data_collection_duration
                # Parameters used: data_collection_duration
                example.sleep()

                # Stop RSSI vs Channel, TX Power amd Data report (if enabled)
                # Parameters used: continues_connection_info
                example.stop_periodic_advertise_report()

                # Stop Angle of Arrival report (if enabled) and analyze collected data using post_analyze_func
                # Parameters used: angle_of_arrival, post_analyze_func
                example.stop_angle_of_arrival()

            # Disconnect from all synced responders
            example.disconnect()

    # Close all open inner threads of RTLS Util
    example.done()


if __name__ == '__main__':
    main()
