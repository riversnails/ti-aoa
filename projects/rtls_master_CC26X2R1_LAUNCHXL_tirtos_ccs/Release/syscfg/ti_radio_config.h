/*
 *  ======== ti_radio_config.h ========
 *  Configured RadioConfig module definitions
 *
 *  DO NOT EDIT - This file is generated for the CC2652R1FRGZ
 *  by the SysConfig tool.
 *
 *  Radio Config module version : 1.8
 *  SmartRF Studio data version : 2.20.0
 */
#ifndef _TI_RADIO_CONFIG_H_
#define _TI_RADIO_CONFIG_H_

#include <ti/devices/DeviceFamily.h>
#include DeviceFamily_constructPath(driverlib/rf_mailbox.h)
#include DeviceFamily_constructPath(driverlib/rf_common_cmd.h)
#include DeviceFamily_constructPath(driverlib/rf_ble_cmd.h)
#include <ti/drivers/rf/RF.h>

// *********************************************************************************
//   RF Frontend configuration
// *********************************************************************************
// RF design based on: LAUNCHXL-CC26X2R1 (CC2642EM-7ID)
#define LAUNCHXL_CC26X2R1

// RF frontend configuration
#define FRONTEND_24G_DIFF_RF
#define FRONTEND_24G_INT_BIAS

// Supported frequency bands
#define SUPPORT_FREQBAND_2400

// TX power table size definitions
#define TXPOWERTABLE_2400_PA5_SIZE 16 // 2400 MHz, 5 dBm

// TX power tables
extern RF_TxPowerTable_Entry txPowerTable_2400_pa5[]; // 2400 MHz, 5 dBm



//*********************************************************************************
//  RF Setting:   BLE, 1 Mbps, LE 1M
//
//  PHY:          bt5le1m
//  Setting file: setting_bt5_le_1m.json
//*********************************************************************************

#define BLE_STACK_OVERRIDES_OFFSET 17

// PA table usage
#define RF_BLE_TX_POWER_TABLE_SIZE TXPOWERTABLE_2400_PA5_SIZE

#define RF_BLE_txPowerTable txPowerTable_2400_pa5

// TI-RTOS RF Mode object
extern RF_Mode RF_modeBle;

// RF Core API overrides
extern uint32_t pOverrides_bleCommon[];
extern uint32_t pOverrides_ble1Mbps[];
extern uint32_t pOverrides_ble2Mbps[];
extern uint32_t pOverrides_bleCoded[];

#endif // _TI_RADIO_CONFIG_H_
