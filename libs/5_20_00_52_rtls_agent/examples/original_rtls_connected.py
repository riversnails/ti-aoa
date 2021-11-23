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
    RtlsUtilScanResponderNotFoundException, RtlsUtilScanNoResultsException


class RtlsConnectedExample():
    def __init__(self, coordinator_comport, passive_comports, responder_bd_addrs, scan_time, connection_interval,
                 continues_connection_info, angle_of_arrival, angle_of_arrival_params, data_collection_duration,
                 data_collection_iteration, post_analyze_func=None, timeout=30): #생성자에 값을 넣어서 들어옴 
        self.headers = ['pkt', 'sample_idx', 'rssi', 'ant_array', 'channel', 'i', 'q', 'slot_duration', 'sample_rate',
                        'filtering']

        self.coordinator_comport = coordinator_comport # coordinator com 포트 설정 
        self.passive_comports = passive_comports
        self.responder_bd_addrs = responder_bd_addrs # 둘 다 없어도 상관없음 

        self.devices = [{"com_port": coordinator_comport, "baud_rate": 460800, "name": "Coordinator"}] # coordinator는 일단은 하나
        for index, passive_comport in enumerate(passive_comports):
            self.devices.append({"com_port": passive_comport, "baud_rate": 460800, "name": f"Passive {index}"})

        self.scan_time = scan_time # scan_time 초단위다.
        self.connection_interval = connection_interval # 연결 간격이라는데 아마 초당 데이터 전송주기 같다.
        self.all_conn_handles = []

        self.enable_continues_connection_info = continues_connection_info

        self.enable_angle_of_arrival = angle_of_arrival # aoa 설정 
        self.angle_of_arrival_params = angle_of_arrival_params

        self.data_collection_duration = data_collection_duration
        self._data_collection_iteration = data_collection_iteration
        self._current_iteration = -1
        self.csv_files = []

        self.post_analyze_func = post_analyze_func

        self.timeout = timeout # default 변수

        self._data_collection_in_process = threading.Event()
        self._data_collection_in_process.clear()

        self._continues_connection_info_thread = None
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
        example_parameters += f"Passive comports                        : {self.passive_comports}\n"
        example_parameters += f"Responder BD Address                    : {self.responder_bd_addrs}\n"
        example_parameters += f"Scan time                               : {self.scan_time} Sec\n"
        example_parameters += f"Connection Interval                     : {self.connection_interval} mSec\n"
        example_parameters += f"Enable Continues Connection Interval    : {'Yes' if self.enable_continues_connection_info else 'No'}\n"
        example_parameters += f"Enable Angle Of Arrival (AoA)           : {'Yes' if self.enable_angle_of_arrival else 'No'}\n"
        example_parameters += f"    AoA Enable Filter                   : {'Yes' if self.angle_of_arrival_params.get('enable_filter', True) else 'No'}\n"
        example_parameters += f"    AoA Slot Duration                   : {self.angle_of_arrival_params.get('slot_duration', 2)}\n"
        example_parameters += f"    AoA Sample Rate                     : {self.angle_of_arrival_params.get('sample_rate', 1)}\n"
        example_parameters += f"    AoA Sample Size                     : {self.angle_of_arrival_params.get('sample_size', 1)}\n"
        example_parameters += f"    AoA CTE Length                      : {self.angle_of_arrival_params.get('cte_length', 20)}\n"
        example_parameters += f"    AoA CTE Interval                    : {self.angle_of_arrival_params.get('cte_interval', 2)}\n"
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

    def _get_logging_file_path(self): # 로그를 저장할 파일위치(파일이름)를 반환하는 함수 
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

    def initialize(self, debug=False): # 1번째로 호출되는 함수 이니셜라이징 하는 함수다.
        try:
            self.logging_file = self._get_logging_file_path() # 로그를 저장할 파일위치(파일이름)를 저장하는 변수

            self.rtls_util = RtlsUtil(self.logging_file,
                                      RtlsUtilLoggingLevel.DEBUG if debug else RtlsUtilLoggingLevel.INFO) # RTLSNode 의 클래스 첫번째는 로깅할 파일, 두번째는 로깅수
            self.rtls_util.timeout = self.timeout # 클래스 선언시 생성자에서 기본적으로 30 이라는 값을 넣기에 다시 대입한다.

            self.rtls_util.add_user_log(self._get_example_parameters()) # 위의 로그들 _get_example_parameters() 의 함수안에 있는 값들을 로그파일 안에도 기록해야 하니 그냥 프린트가 아닌 사용자 지정 로그함수를 사용하여 출력한다.

            ## Setup devices
            self.coordinator_node, self.passive_nodes, self.all_nodes = self.rtls_util.set_devices(self.devices) # 기본적으로 등록해줬던 기기들을 rtls_util 클래스안에 설정해주는 작업이다. (대입은 필요없는데 디버깅한다고 사용한듯?)
            # print(f"Coordinator : {self.coordinator_node} \nPassives : {self.passive_nodes} \nAll : {self.all_nodes}") # 요거 찍는다고 대입했었는듯

            self.rtls_util.reset_devices() # 설정되어있던 노드들을 리셋시킨다
            print("Devices Reset")

            return True

        except RtlsUtilCoordinatorNotFoundException:
            print('No one of given devices identified as RTLS Coordinator')
            return False

    def scan_and_connect(self):
        self.all_conn_handles = []

        try:
            print(f"Start scan for {self.scan_time} sec")
            scan_results = self.rtls_util.scan(self.scan_time) # 스캔타임은  __init__ 즉 생성할때 설정된 값으로 기본으로 10초가 설정되어있다. 받은 값들을 리턴한다. 
            suitable_responders = [scan_result for scan_result in scan_results if scan_result['periodicAdvInt'] == 0]
            print("Scan Results: \n\t{}".format(
                '\n\t'.join([str(suitable_responders) for suitable_responders in suitable_responders])))

            ## Code below demonstrates how to connect to multiple responders
            if not self.responder_bd_addrs:
                # Sort Scan Results by RSSI and take only 8 first responders
                self.responder_bd_addrs = sorted(suitable_responders, key=lambda s: s['rssi'], reverse=True)[:8] # 주소를 기준으로 정렬시키는 것 같다.

            for responder_bd_addr in self.responder_bd_addrs:
                try:
                    if type(responder_bd_addr) == dict:
                        responder_bd_addr = responder_bd_addr['addr']

                    print(f"\nTrying connect to {responder_bd_addr}")
                    conn_handle = self.rtls_util.ble_connect(responder_bd_addr, self.connection_interval) # 만약 스캔된 주소가 있으면 연결한다.
                    if conn_handle is not None:
                        self.all_conn_handles.append(conn_handle)
                        print(f"Connected to {responder_bd_addr} with connection handle {conn_handle}")
                    else:
                        print(f"Failed to connect to {responder_bd_addr}")
                except RtlsUtilTimeoutException:
                    print(f"Failed to connect to {responder_bd_addr}")
                    continue

            return len(self.all_conn_handles) > 0

        except RtlsUtilEmbeddedFailToStopScanException:
            return False
        except RtlsUtilScanResponderNotFoundException:
            return False
        except RtlsUtilScanNoResultsException:
            return False
        except RtlsUtilException:
            return False

    def disconnect(self):
        for conn_handle in self.all_conn_handles:
            self.rtls_util.ble_disconnect(conn_handle=conn_handle)
            print(f"Coordinator disconnected from responder with conn handle {conn_handle}")

    # Thread for Continuous Connection Info  monitoring
    # Should not be called by user's application.
    # Please use functions start_continues_connection_info and stop_continues_connection_info instead.
    def _continues_connection_info_result(self):
        while self._data_collection_in_process.is_set():
            data_time = datetime.datetime.now().strftime("[%m:%d:%Y %H:%M:%S:%f] :")

            try:
                cci_data = self.rtls_util.conn_info_queue.get_nowait()
                print(f"{data_time} {json.dumps(cci_data)}")
            except queue.Empty:
                pass

    def start_continues_connection_info(self):
        self._continues_connection_info_thread = None

        if self.enable_continues_connection_info:
            self._continues_connection_info_thread = threading.Thread(target=self._continues_connection_info_result)
            self._continues_connection_info_thread.daemon = True

            self._continues_connection_info(True)

    def stop_continues_connection_info(self):
        if self.enable_continues_connection_info:
            self._continues_connection_info(False)

        self._continues_connection_info_thread = None
        self.rtls_util._empty_queue(self.rtls_util.conn_info_queue)

    def _continues_connection_info(self, enable): # cci 관리 함수
        if enable:
            self.rtls_util.cci_start() # cci를 시작시키면 서로 동기화가 되어있는지 확인하고 coodinator와 responder가 이벤트를 주고 받는다.
            print("Continues Connection Information Started\n")
        else:
            self.rtls_util.cci_stop()
            print("\nContinues Connection Information Stopped")

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
                aoa_data = self.rtls_util.aoa_results_queue.get_nowait()
                # print(f"{data_time} {json.dumps(aoa_data)}")

                if 'type' in aoa_data and aoa_data['type'] == "RTLS_CMD_AOA_RESULT_RAW":
                    if TABLE is None:
                        TABLE = pd.DataFrame(columns=self.headers)

                    identifier = aoa_data["identifier"]
                    connHandle = aoa_data['payload']['connHandle']
                    channel = int(aoa_data['payload']['channel'])
                    offset = int(aoa_data['payload']['offset'])
                    rssi = aoa_data['payload']['rssi']
                    antenna = 1
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
                                                                    with_date=False) # csv 파일 이름 설정
                        current_csv_files.add(csv_file_name)

                        if os.path.isfile(csv_file_name):
                            df_by_channel.to_csv(csv_file_name, mode='a', index=False, header=False)
                        else:
                            df_by_channel.to_csv(csv_file_name, index=False)
                        #print(f"{data_time} Added new set of IQ into {csv_file_name}") # 저장할 cvs파일 이름 출력

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
            print(f"Rename \"{os.path.basename(current_csv_file)}\" into \"{os.path.basename(new_csv_file)}\"")

            if self.post_analyze_func:
                print(f"\nExecuting post analyze script on {new_csv_file}")
                output = self.post_analyze_func(new_csv_file)
                self.rtls_util.add_user_log(output) # 여기로 받은 값들을 로그로 보낸다.

            self.csv_files.append(new_csv_file)

    def start_angle_of_arrival(self):
        self._angle_of_arrival_thread = None

        if self.enable_angle_of_arrival:
            self._angle_of_arrival_thread = threading.Thread(target=self._angle_of_arrival_result) # thread를 돌려서 원활히 돌아가게 만든거같은
            self._angle_of_arrival_thread.daemon = True

            self._angle_of_arrival(True)

    def stop_angle_of_arrival(self):
        if self.enable_angle_of_arrival:
            self._angle_of_arrival(False)

        self._angle_of_arrival_thread = None
        self.rtls_util._empty_queue(self.rtls_util.aoa_results_queue)

    def _angle_of_arrival(self, enable): # aoa 관리 하는 함수 bool 형으로 관리한다.
        if enable:
            aoa_params = {
                "aoa_run_mode": "AOA_MODE_RAW",
                "aoa_cc26x2": {
                    "aoa_slot_durations": self.angle_of_arrival_params.get('slot_duration', 1),
                    "aoa_sample_rate": self.angle_of_arrival_params.get('sample_rate', 1),
                    "aoa_sample_size": self.angle_of_arrival_params.get('sample_size', 1),
                    "aoa_sampling_control": int(
                        '0x10' if self.angle_of_arrival_params.get('enable_filter', True) else '0x11', 16),
                    "aoa_sampling_enable": 1,
                    "aoa_pattern_len": 3,
                    "aoa_ant_pattern": [0, 1, 2]
                }
            }
            print(aoa_params)
            self.rtls_util.aoa_set_params(aoa_params)
            print("AOA Params Set")

            self.rtls_util.aoa_start(cte_length=self.angle_of_arrival_params.get('cte_length', 20),
                                     cte_interval=self.angle_of_arrival_params.get('cte_interval', 2))
            print("AOA Started\n")
        else:
            self.rtls_util.aoa_stop()
            print("\nAOA Stopped")

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
        # print("Done done!")


def post_analyze_of_IQ_data(csv_file):
    print(f"Analyzing file : {csv_file}")
    # Place here you code for IQ data post-analyze algorithms
    return "Return here output of your post-analyze algorithm"


def main():
    
    example = RtlsConnectedExample(
        coordinator_comport="COM7",  # "/dev/cu.usbmodemL1100KKT1",
        passive_comports=[],  # ['COM19']
        responder_bd_addrs=[],  # ['80:6F:B0:1E:39:02', '80:6F:B0:1E:38:C3']
        scan_time=10,
        connection_interval=100,
        continues_connection_info=False,
        angle_of_arrival=True,
        angle_of_arrival_params={
            'enable_filter': True,
            'slot_duration': 2,
            'sample_rate': 1,
            'sample_size': 1,
            'cte_length': 20,
            'cte_interval': 2
        },
        data_collection_duration=10,
        data_collection_iteration=1,
        post_analyze_func=post_analyze_of_IQ_data
    )

    try:

        # Perform initialization of RTLS Util, setup devices and reset them
        # Parameters used: coordinator_comport, passive_comports
        if example.initialize():

            # Perform Scan and Connect with required responders
            # Parameters used: responder_bd_addrs, scan_time, connection_interval
            if example.scan_and_connect():

                # Execute next action in loop
                # Parameters used: data_collection_iteration
                for example.current_iteration in range(example.data_collection_iteration): # 무한대로 돌리는거같은데 중간에 확인해서 스탑하는 것 같다.
                    # Start RSSI vs Channel report (if enabled)
                    # Parameters used: continues_connection_info
                    example.start_continues_connection_info()

                    # Start Angle of Arrival report (if enabled)
                    # Parameters used: angle_of_arrival, angle_of_arrival_params
                    example.start_angle_of_arrival()

                    # Example start all inner threads for result collecting and sleep for data_collection_duration
                    # Parameters used: data_collection_duration
                    example.sleep() # 슬립을 호출 할 시 만들어 둔 모든 thread를 data_collection_duration 동안 실행시킨다.

                    # Stop RSSI vs Channel report (if enabled)
                    # Parameters used: continues_connection_info
                    example.stop_continues_connection_info()

                    # Stop Angle of Arrival report (if enabled) and analyze collected data using post_analyze_func
                    # Parameters used: angle_of_arrival, post_analyze_func
                    example.stop_angle_of_arrival()

                # Disconnect from all connected responders
                example.disconnect()

                
        # Close all open inner threads of RTLS Util
        example.done()

    except KeyboardInterrupt: # 자꾸 안꺼지니까 except넣음 
        example.stop_angle_of_arrival()
        example.disconnect()
        example.done()


if __name__ == '__main__':
    main()




