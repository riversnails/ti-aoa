import os
import sys
import time
import json
import queue
import threading
import datetime

## Uncomment line below for local debug of packages
# sys.path.append(r"../unpi")
# sys.path.append(r"../rtls")
# sys.path.append(r"../rtls_util")

from rtls_util import RtlsUtil, RtlsUtilLoggingLevel, RtlsUtilException, RtlsUtilTimeoutException, \
    RtlsUtilNodesNotIdentifiedException, RtlsUtilScanNoResultsException


## User function to proces
def results_parsing(q):
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


## Main Function
def main():
    ## Predefined parameters
    slave_bd_addr = None  # "80:6F:B0:1E:38:C3" # "54:6C:0E:83:45:D8"
    scan_time_sec = 15
    connect_interval_mSec = 100

    ## Continuous Connection Info Demo Enable / Disable
    cci = True
    ## Angle of Arival Demo Enable / Disable
    aoa = False

    ## Update connection interval on the fly Demo Enable / Disable
    update_conn_interval = False
    new_connect_interval_mSec = 80

    ## Taking python file and replacing extension from py into log for output logs + adding data time stamp to file
    data_time = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
    logging_file_path = os.path.join(os.path.curdir, os.path.basename(__file__).replace('.py', '_log'))
    if not os.path.isdir(logging_file_path):
        os.makedirs(logging_file_path)
    logging_file = os.path.join(logging_file_path, f"{data_time}_{os.path.basename(__file__).replace('.py', '.log')}")

    ## Initialize RTLS Util instance
    rtlsUtil = RtlsUtil(logging_file, RtlsUtilLoggingLevel.INFO)
    ## Update general time out for all action at RTLS Util [Default timeout : 30 sec]
    rtlsUtil.timeout = 30

    all_nodes = []
    try:
        devices = [
            {"com_port": "COM8", "baud_rate": 460800, "name": "CC26x2 Master"},
            {"com_port": "COM9", "baud_rate": 460800, "name": "CC26x2 Passive"},
        ]
        ## Setup devices
        master_node, passive_nodes, all_nodes = rtlsUtil.set_devices(devices)
        print(f"Master : {master_node} \nPassives : {passive_nodes} \nAll : {all_nodes}")

        ## Reset devices for initial state of devices
        rtlsUtil.reset_devices()
        print("Devices Reset")

        ## Code below demonstrates two option of scan and connect
        ## 1. Then user know which slave to connect
        ## 2. Then user doesn't mind witch slave to use
        if slave_bd_addr is not None:
            print(f"Start scan of {slave_bd_addr} for {scan_time_sec} sec")
            scan_results = rtlsUtil.scan(scan_time_sec, slave_bd_addr)
            print(f"Scan Results: {scan_results}")

            rtlsUtil.ble_connect(slave_bd_addr, connect_interval_mSec)
            print("Connection Success")
        else:
            print(f"Start scan for {scan_time_sec} sec")
            scan_results = rtlsUtil.scan(scan_time_sec)
            print(f"Scan Results: {scan_results}")

            rtlsUtil.ble_connect(scan_results[0], connect_interval_mSec)
            print("Connection Success")

        ## Start continues connection info feature
        if cci:
            ## Setup thread to pull out received data from devices on screen
            th_cci_parsing = threading.Thread(target=results_parsing, args=(rtlsUtil.conn_info_queue,))
            th_cci_parsing.setDaemon(True)
            th_cci_parsing.start()
            print("CCI Callback Set")

            rtlsUtil.cci_start()
            print("CCI Started")

        ## Start angle of arrival feature
        if aoa:
            if rtlsUtil.is_aoa_supported(all_nodes):
                aoa_params = {
                    "aoa_run_mode": "AOA_MODE_ANGLE",  ## AOA_MODE_ANGLE, AOA_MODE_PAIR_ANGLES, AOA_MODE_RAW
                    "aoa_cc26x2": {
                        "aoa_slot_durations": 1,
                        "aoa_sample_rate": 1,
                        "aoa_sample_size": 1,
                        "aoa_sampling_control": int('0x10', 16),
                        ## bit 0   - 0x00 - default filtering, 0x01 - RAW_RF no filtering,
                        ## bit 4,5 - default: 0x10 - ONLY_ANT_1, optional: 0x20 - ONLY_ANT_2
                        "aoa_sampling_enable": 1,
                        "aoa_pattern_len": 3,
                        "aoa_ant_pattern": [0, 1, 2]
                    }
                }
                rtlsUtil.aoa_set_params(aoa_params)
                print("AOA Params Set")

                ## Setup thread to pull out received data from devices on screen
                th_aoa_results_parsing = threading.Thread(target=results_parsing, args=(rtlsUtil.aoa_results_queue,))
                th_aoa_results_parsing.setDaemon(True)
                th_aoa_results_parsing.start()
                print("AOA Callback Set")

                rtlsUtil.aoa_start(cte_length=20, cte_interval=1)
                print("AOA Started")
            else:
                print("=== Warning ! One of the devices does not support AoA functionality ===")

        ## Update connection interval after connection is set
        if update_conn_interval:
            time.sleep(2)
            print("Sleep for 2 sec before update connection interval")

            rtlsUtil.set_connection_interval(new_connect_interval_mSec)
            print(f"Update Connection Interval into : {new_connect_interval_mSec} mSec")

        ## Sleep code to see in the screen receives data from devices
        timeout_sec = 15
        print("Going to sleep for {} sec".format(timeout_sec))
        timeout = time.time() + timeout_sec
        while timeout >= time.time():
            time.sleep(0.01)

        if cci:
            rtlsUtil.conn_info_queue.put("STOP")
            print("Try to stop CCI result parsing thread")

            rtlsUtil.cci_stop()
            print("CCI Stopped")

        if aoa and rtlsUtil.is_aoa_supported(all_nodes):
            rtlsUtil.aoa_results_queue.put("STOP")
            print("Try to stop AOA result parsing thread")

            rtlsUtil.aoa_stop()
            print("AOA Stopped")

        if rtlsUtil.ble_connected:
            rtlsUtil.ble_disconnect()
            print("Master Disconnected")

    except RtlsUtilNodesNotIdentifiedException as ex:
        print(f"=== ERROR: {ex} ===")
        print(ex.not_indentified_nodes)
    except RtlsUtilTimeoutException as ex:
        print(f"=== ERROR: {ex} ===")
    except RtlsUtilException as ex:
        print(f"=== ERROR: {ex} ===")
    finally:
        rtlsUtil.done()
        print("Done")


if __name__ == '__main__':
    main()
