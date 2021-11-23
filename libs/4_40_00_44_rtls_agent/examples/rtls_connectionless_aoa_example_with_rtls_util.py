import os
import sys
import time
import json
import queue
import threading
import datetime
import subprocess
import shutil
import traceback

import pandas as pd
# Uncomment line below for local debug of packages
# sys.path.append(r"../unpi")
# sys.path.append(r"../rtls")
# sys.path.append(r"../rtls_util")

from rtls_util import RtlsUtil, RtlsUtilLoggingLevel, RtlsUtilException, RtlsUtilTimeoutException, \
    RtlsUtilNodesNotIdentifiedException, RtlsUtilScanNoResultsException, RtlsUtilMasterNotFoundException

headers = ['pkt', 'sample_idx', 'rssi', 'ant_array', 'channel', 'i', 'q']
TABLE = None
POST_ANALYZE_FILE_LIST = set()
data_saved = False

# Options constants:
#   Clear Bit 0 - Use the advSID, advAddrType, and advAddress parameters to determine which advertiser to listen to.
#   Set Bit 0   - Use the Periodic Advertiser List to determine which advertiser to listen to.
#   Clear Bit 1 - Reporting initially enabled.
#   Set Bit 1   - Reporting initially disabled.

USE_GIVEN_ADDRESS_AND_REPORT_ENABLE = 0
USE_LIST_AND_REPORT_ENABLE = 1
USE_GIVEN_ADDRESS_AND_REPORT_DISABLE = 2
USE_LIST_AND_REPORT_DISABLE = 3

# Dummy slave to send when using periodic advertise list for sync
dummy_slave = {'addr': 'FF:FF:FF:FF:FF:FF',
               'addrType': 0,
               'rssi': 0,
               'advSID': 0,
               'periodicAdvInt': 0
               }


def get_date_time():
    return datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")


def get_csv_file_name_for(identifier, sync_handle, with_date=True):
    data_time = get_date_time()
    logging_file_path = os.path.join(os.path.curdir, os.path.basename(__file__).replace('.py', '_log'))

    if not os.path.isdir(logging_file_path):
        os.makedirs(logging_file_path)

    identifier = identifier.lower().replace(":", "")
    if with_date:
        filename = os.path.join(logging_file_path, f"{data_time}_rtls_raw_iq_samples_{identifier}_{sync_handle}.csv")
    else:
        filename = os.path.join(logging_file_path, f"rtls_raw_iq_samples_{identifier}_{sync_handle}.csv")

    return filename


# User function to proces
def results_parsing_cl_aoa(q):
    global TABLE, POST_ANALYZE_FILE_LIST
    pkt_count = 0

    while True:
        try:
            data = q.get(block=True, timeout=0.5)
            if isinstance(data, dict):
                data_time = datetime.datetime.now().strftime("[%m:%d:%Y %H:%M:%S:%f] :")

                if 'type' in data and data['type'] == 'RTLS_CMD_CL_AOA_RESULT_RAW':
                    # print(f"{data_time} {json.dumps(data)}")

                    if TABLE is None:
                        TABLE = pd.DataFrame(columns=headers)

                    identifier = data["identifier"]
                    syncHandle = data['payload']['syncHandle']
                    channel = int(data['payload']['channel'])
                    offset = int(data['payload']['offset'])
                    rssi = data['payload']['rssi']
                    antenna = data['payload']['antenna']
                    samplesLength = data['payload']["samplesLength"]

                    for indx, sample in enumerate(data['payload']['samples']):
                        sample_idx = offset + indx
                        sample_i = sample['i']
                        sample_q = sample['q']

                        row = {
                            'pkt': 0,
                            'sample_idx': sample_idx,
                            'rssi': rssi,
                            'ant_array': antenna,
                            'channel': channel,
                            'i': sample_i,
                            'q': sample_q
                        }
                        TABLE = TABLE.append(row, ignore_index=True)

                    df_by_channel = TABLE.loc[TABLE['channel'] == channel]

                    if len(df_by_channel) == samplesLength:
                        df_by_channel = df_by_channel.sort_values(by=['sample_idx'])
                        df_by_channel.loc[:, "pkt"] = df_by_channel.loc[:, "pkt"].replace(to_replace=0, value=pkt_count)

                        csv_file_name = get_csv_file_name_for(identifier, syncHandle, with_date=False)
                        POST_ANALYZE_FILE_LIST.add(csv_file_name)

                        if os.path.isfile(csv_file_name):
                            df_by_channel.to_csv(csv_file_name, mode='a', index=False, header=False)
                        else:
                            df_by_channel.to_csv(csv_file_name, index=False)
                        print(f"{data_time} Added new set of IQ into {csv_file_name}")

                        pkt_count += 1
                        TABLE = TABLE.loc[TABLE['channel'] != channel]
                else:
                    print(f"{data_time} {json.dumps(data)}")

            elif isinstance(data, str) and data == "STOP":
                print("STOP Command Received")
                for entry in list(POST_ANALYZE_FILE_LIST)[:]:
                    date_time = get_date_time()
                    file_name = os.path.basename(entry)
                    dir_name = os.path.dirname(entry)
                    new_entry = os.path.abspath(os.path.join(dir_name, f"{date_time}_{file_name}"))
                    os.rename(entry, new_entry)
                    POST_ANALYZE_FILE_LIST.remove(entry)
                    POST_ANALYZE_FILE_LIST.add(new_entry)

                break
            else:
                pass
        except queue.Empty:
            continue


def results_parsing_padv_events(q):
    while True:
        try:
            data = q.get(block=True, timeout=0.5)
            if isinstance(data, dict):
                data_time = datetime.datetime.now().strftime("[%m:%d:%Y %H:%M:%S:%f] :")
                print(f"{data_time} {json.dumps(data)}")
            elif isinstance(data, str) and data == "STOP":
                print("STOP Command Received")
                break
            else:
                pass
        except queue.Empty:
            continue


def filter_scan_results(scan_results, slave_address=None):
    print("Filtering scan results for periodic advertisers")
    ret_slave_list = []
    for res in scan_results:
        if slave_address is None:
            if res['periodicAdvInt'] != 0:
                ret_slave_list.append(res)
        else:
            if res['periodicAdvInt'] != 0 and res['addr'] == slave_address:
                ret_slave_list.append(res)

    if ret_slave_list:
        return ret_slave_list
    else:
        raise Exception("Slave list is empty. Non of the slaves match to definition")


def aoa_post_analyze(selected_ant=16):
    global POST_ANALYZE_FILE_LIST
    aoa_exe_path = os.path.abspath("../rtls_ui/aoa/aoa.exe")
    support_files_ant1 = os.path.abspath("../rtls_ui/aoa/support_files/Ant1")
    support_files_ant2 = os.path.abspath("../rtls_ui/aoa/support_files/Ant2")

    # First, Check if cl_aoa_sampling_control configured to raw RF mode
    if selected_ant & 0x01:
        if os.path.isfile(aoa_exe_path):
            if len(POST_ANALYZE_FILE_LIST) > 0:
                for fp in POST_ANALYZE_FILE_LIST:
                    dir_name = os.path.splitext(fp)[0]
                    if selected_ant >= 32:
                        shutil.copytree(support_files_ant2, dir_name)
                    else:
                        shutil.copytree(support_files_ant1, dir_name)

                    shutil.copy2(fp, dir_name)
                    csv_file = os.path.join(dir_name, os.path.basename(fp))

                    print("----------------------------------------------------------------------------\n")
                    print(f"Analyzing file : {fp}")

                    print("\nAlgorithm : Algo1")
                    output = subprocess.check_output(
                        f'{aoa_exe_path} --pct_file {csv_file} --algo algo1 --search_speed fast').decode()
                    output = output.replace('\r\n', '\r\n\t\t')
                    print(output)

                    print("\nAlgorithm : Algo2")
                    output = subprocess.check_output(
                        f'{aoa_exe_path} --pct_file {csv_file} --algo algo2 --search_speed fast').decode()
                    output = output.replace('\r\n', '\r\n\t\t')
                    print(output)

                    print("----------------------------------------------------------------------------\n")
    else:
        print("Cannot calculate angle if not configured to raw RF mode")


def scan_for_sync_est(scan_time_sec, rtlsUtil, slave=None, retry=5):

    num_of_try = 0

    while num_of_try < retry:
        rtlsUtil.scan(scan_time_sec, slave['addr'], slave['advSID'])
        sync_handle = rtlsUtil.padv_get_sync_handle_by_slave(slave)
        if sync_handle != -1:
            print(f"Sync with: {slave['addr']} succeed with handle: {sync_handle}")
            return True
        else:
            if rtlsUtil.sync_failed_to_be_est:
                print(f"Sync faild to be established for slave: {slave['addr']} SID: {slave['advSID']} ")
                rtlsUtil.sync_failed_to_be_est = False
                return False
            else:
                num_of_try += 1
                print(f"did not get sync established event. retry no. {num_of_try}")

    return False


# Main Function
def main():
    global POST_ANALYZE_FILE_LIST
    # Predefined parameters
    slave_bd_addr_list = None # ["80:6F:B0:EE:B9:2C", "80:6F:B0:EE:A8:A8", "80:6F:B0:EE:9A:BC"] # Up to 40 slaves to sync.
    scan_time_sec = 10                                                                          # If BD address is unknown, set None.
    num_of_scan_retry = 5   # Number of scan retry in case sync established event didn't occurred
    # Sync parameters
    sync_skip = 0         # The maximum number of periodic advertising events that can be skipped after a successful receive (Range: 0x0000 to 0x01F3)
    sync_cte_type = 0     # Clear All Bits(0) - Sync All
                          # Set Bit 0(1) - Do not sync to packets with an AoA CTE
                          # Set Bit 1(2) - Do not sync to packets with an AoD CTE with 1 us slots
                          # Set Bit 2(4) - Do not sync to packets with an AoD CTE with 2 us slots
                          # Set Bit 4(16) - Do not sync to packets without a CTE

    # Flag to determine whether to sync a device from advertisers list or according to bd address and adv SID
    use_adv_list = True
    # Flag to enable periodic advertise reports to be printed
    padv_report = False
    th_padv_parsing = None
    # Flag to enable connectionless aoa reports to be printed and parsed
    cl_aoa = True
    th_cl_aoa_parsing = None

    # Replacing python file extension from py to log for output logs + adding data time stamp to file
    data_time = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
    logging_file_path = os.path.join(os.path.curdir, os.path.basename(__file__).replace('.py', '_log'))
    if not os.path.isdir(logging_file_path):
        os.makedirs(logging_file_path)
    logging_file = os.path.join(logging_file_path, f"{data_time}_{os.path.basename(__file__).replace('.py', '.log')}")

    # Initialize RTLS Util instance
    rtlsUtil = RtlsUtil(logging_file, RtlsUtilLoggingLevel.INFO)
    # Update general time out for all action at RTLS Util [Default timeout : 10 sec]
    rtlsUtil.timeout = 10

    all_nodes = []
    try:
        devices = [
            {"com_port": "COM7", "baud_rate": 460800, "name": "CC26x2 Master"}
        ]
        # Setup devices
        master_node, passive_nodes, all_nodes = rtlsUtil.set_devices(devices)
        print(f"Master : {master_node} \nPassives : {passive_nodes} \nAll : {all_nodes}")

        # Reset devices for initial state of devices
        rtlsUtil.reset_devices()
        print("Devices Reset")

        if padv_report:
            ## Setup thread to pull out received data from devices on screen
            th_padv_parsing = threading.Thread(target=results_parsing_padv_events, args=(rtlsUtil.padv_event_queue,))
            th_padv_parsing.setDaemon(True)
            th_padv_parsing.start()
            print("Periodic Advertise Callback Set")

        if cl_aoa:
            cl_aoa_params = {
                "cl_aoa_role": "AOA_MASTER",  # AOA_MASTER - currently only master role supported
                "cl_aoa_result_mode": "AOA_MODE_RAW",  # AOA_MODE_ANGLE, AOA_MODE_PAIR_ANGLES, AOA_MODE_RAW
                "cl_aoa_slot_durations": 1,
                "cl_aoa_sample_rate": 1,  # 1Mhz (BT5.1 spec), 2Mhz, 3Mhz or 4Mhz - this enables oversampling
                "cl_aoa_sample_size": 1,  # 8 bit sample (as defined by BT5.1 spec), 16 bit sample (higher accuracy)
                "cl_aoa_sampling_control": int('0x11', 16),
                # bit 0   - 0x00 - default filtering, 0x01 - RAW_RF no filtering (use this mode for post process angle calculation),
                # bit 4,5 - default: 0x10 - ONLY_ANT_1, optional: 0x20 - ONLY_ANT_2
                "max_sample_cte": 1,
                "cl_aoa_pattern_len": 3,
                "cl_aoa_ant_pattern": [0, 1, 2]
            }

            # Setup thread to pull out received data from devices on screen
            th_cl_aoa_parsing = threading.Thread(target=results_parsing_cl_aoa, args=(rtlsUtil.cl_aoa_results_queue,))
            th_cl_aoa_parsing.setDaemon(True)
            th_cl_aoa_parsing.start()
            print("Connectionless AOA Callback Set")

        # Code below demonstrates two different ways to sync with periodic advertiser for connectionless AOA
        # 1. Then user knows slave bd address and advertise SID
        # 2. Then user doesn't mind which slave to use. flow will be as follow:
        #      a. Scan for periodic advertisers
        #      b. Filter scan results for periodic interval different then 0
        #      c. Create sync
        if slave_bd_addr_list is not None:
            # Option 1
            sync_slave_list = []
            for slave_bd_addr in slave_bd_addr_list:
                # Scan and filter for desired slave
                scan_results = rtlsUtil.scan(scan_time_sec)
                print(f"Scan results found: {scan_results}")

                # Filter scan results for advertisers with periodic interval > 0
                slave_list = filter_scan_results(scan_results, slave_bd_addr)
                slave = slave_list[0]

                # Synchronization timeout for the periodic advertising train Range: 0x000A to 0x4000 Time = N*10 ms Time Range
                # For this example, the timeout value set to be 10 times bigger then the periodic advertise interval.
                sync_timeout = int((slave['periodicAdvInt'] * 1.25) * 10)

                # time out must satisfy the timeout condition. other wise sync might be lost.
                if sync_skip != 0:
                    timeout_condition = sync_timeout >= sync_skip * slave['periodicAdvInt']
                else:
                    timeout_condition = sync_timeout >= slave['periodicAdvInt']

                if timeout_condition:
                    rtlsUtil.padv_create_sync(slave,
                                              USE_GIVEN_ADDRESS_AND_REPORT_DISABLE,
                                              sync_skip,
                                              sync_timeout,
                                              sync_cte_type)

                    # Scan again for sync established event. scan again if not sync established event occurred
                    sync_est_status = scan_for_sync_est(scan_time_sec, rtlsUtil, slave, num_of_scan_retry)
                    if sync_est_status:
                        print(f"Sync established with: {slave}")
                        sync_slave_list.append(slave)
                    else:
                        print(f"Failed to establish sync with: {slave}")

                    if padv_report:
                        # Enable periodic advertise reports and sleep for 5 seconds
                        rtlsUtil.padv_periodic_receive_enable(rtlsUtil.padv_get_sync_handle_by_slave(slave))
                        print("Periodic report enabled")
                        time.sleep(5)

                    if cl_aoa:
                        rtlsUtil.cl_aoa_start(cl_aoa_params, slave)
                        print("Connectionless AOA started")

                        ## Sleep code to see in the screen receives data from devices
                        timeout_sec = 15
                        print("Going to sleep for {} sec".format(timeout_sec))
                        timeout = time.time() + timeout_sec
                        while timeout >= time.time():
                            time.sleep(0.01)

                        rtlsUtil.cl_aoa_stop(cl_aoa_params, slave)
                        print("Connectionless AOA stopped")

                else:
                    raise Exception("Timeout condition does not satisfied")

            for s_slave in sync_slave_list:
                sync_handle = rtlsUtil.padv_get_sync_handle_by_slave(s_slave)
                rtlsUtil.padv_terminate_sync(sync_handle)
                print(f"Sync terminated for sync handle: {sync_handle}")

        else:
            # Option 2

            # Scan and filter for relevant slaves that supports periodic advertise
            scan_results = rtlsUtil.scan(scan_time_sec)
            print(f"Scan results found: {scan_results}")
            slave_list = filter_scan_results(scan_results)
            slave = slave_list[0]

            # Synchronization timeout for the periodic advertising train Range: 0x000A to 0x4000 Time = N*10 ms Time Range
            # For this example, the timeout value set to be 10 times bigger then the periodic advertise interval.
            sync_timeout = int(slave_list[0]['periodicAdvInt'] * 1.25 * 10)

            # time out must satisfy the timeout condition. other wise sync might be lost.
            if sync_skip != 0:
                timeout_condition = sync_timeout >= sync_skip * slave['periodicAdvInt']
            else:
                timeout_condition = sync_timeout >= slave['periodicAdvInt']

            if timeout_condition:
                if use_adv_list:
                    print("Using advertisers list to create sync")
                    # Add all devices to periodic advertiser list
                    for slave in slave_list:
                        rtlsUtil.padv_add_device_to_periodic_adv_list(slave)
                        print(f"slave {slave} has been added to advertisers list")

                    # Slave information has no meaning when using advertiser list to create sync
                    rtlsUtil.padv_create_sync(dummy_slave,
                                              USE_LIST_AND_REPORT_ENABLE,
                                              sync_skip,
                                              sync_timeout,
                                              sync_cte_type)

                    # Scan again for sync established event - reports will be enabled automatically
                    rtlsUtil.scan(scan_time_sec)
                    time.sleep(3)

                    # find sync handle 0 to perform connectionless aoa
                    synced_slave = None
                    for slave in slave_list:
                        if rtlsUtil.padv_get_sync_handle_by_slave(slave) == 0:
                            synced_slave = slave
                            print(f"Sync created with first slave on advertisers list: {synced_slave}. "
                                  f"Periodic advertise report enabled automatically")
                    # If non of the slaves got synced, raise an exception
                    if synced_slave is None:
                        raise Exception("No slave from periodic advertise list got synced")

                    if cl_aoa:

                        rtlsUtil.cl_aoa_start(cl_aoa_params, synced_slave)
                        print("Connectionless AOA started")
                        time.sleep(5)
                        rtlsUtil.cl_aoa_stop(cl_aoa_params, synced_slave)
                        print("Connectionless AOA stopped")

                    sync_handle = rtlsUtil.padv_get_sync_handle_by_slave(synced_slave)
                    rtlsUtil.padv_terminate_sync(sync_handle)
                    print(f"Sync terminated for sync handle: {sync_handle}")
                else:

                    # Create sync with first slave from slave list
                    rtlsUtil.padv_create_sync(slave_list[0],
                                              USE_GIVEN_ADDRESS_AND_REPORT_ENABLE,
                                              sync_skip,
                                              sync_timeout,
                                              sync_cte_type)

                    # Scan again for sync established event - reports will be enabled automatically
                    sync_est_status = scan_for_sync_est(scan_time_sec, rtlsUtil, slave_list[0], num_of_scan_retry)
                    if sync_est_status:
                        print(f"Sync established with: {slave}. Periodic advertise reports enabled automatically")
                    else:
                        print(f"Failed to establish sync with: {slave}")
                    time.sleep(3)

                    if cl_aoa:
                        rtlsUtil.cl_aoa_start(cl_aoa_params, slave_list[0])
                        print("Connectionless AOA started")

                        ## Sleep code to see in the screen receives data from devices
                        timeout_sec = 15
                        print("Going to sleep for {} sec".format(timeout_sec))
                        timeout = time.time() + timeout_sec
                        while timeout >= time.time():
                            time.sleep(0.01)

                        rtlsUtil.cl_aoa_stop(cl_aoa_params, slave_list[0])
                        print("Connectionless AOA stopped")

                    sync_handle = rtlsUtil.padv_get_sync_handle_by_slave(slave_list[0])
                    rtlsUtil.padv_terminate_sync(sync_handle)
                    print(f"Sync terminated for sync handle: {sync_handle}")
            else:
                raise Exception("Timeout condition does not satisfied for all slaves")

    except RtlsUtilMasterNotFoundException as ex:
        print(f"=== ERROR: {ex} ===")
        sys.exit(1)
    except RtlsUtilNodesNotIdentifiedException as ex:
        print(f"=== ERROR: {ex} ===")
        print(ex.not_indentified_nodes)
        sys.exit(1)
    except RtlsUtilTimeoutException as ex:
        print(f"=== ERROR: {ex} ===")
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_traceback, file=sys.stdout)
        sys.exit(1)
    except RtlsUtilException as ex:
        print(f"=== ERROR: {ex} ===")
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_traceback, file=sys.stdout)
        sys.exit(1)
    except Exception as ex:
        print(f"=== ERROR: {ex} ===")
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_traceback, file=sys.stdout)
        sys.exit(1)
    finally:

        if padv_report:
            rtlsUtil.padv_event_queue.put("STOP")
            print("Try to stop Periodic Advertise event parsing thread")
            if th_padv_parsing:
                th_padv_parsing.join()

        if cl_aoa:
            rtlsUtil.cl_aoa_results_queue.put("STOP")
            print("Try to stop Connectionless AOA results parsing thread")
            if th_cl_aoa_parsing:
                th_cl_aoa_parsing.join()

        rtlsUtil.done()
        print("Done")

        # Flag to check if any data csv has been saved successfully
        data_saved = True if POST_ANALYZE_FILE_LIST else False

        if cl_aoa and data_saved:
            print("Executing analyze on results")
            if cl_aoa_params:
                aoa_post_analyze(cl_aoa_params['cl_aoa_sampling_control'])
            else:
                aoa_post_analyze()


if __name__ == '__main__':
    main()
