/*
 *  ======== ti_radio_config.c ========
 *  Configured RadioConfig module definitions
 *
 *  DO NOT EDIT - This file is generated for the CC1352R1F3RGZ
 *  by the SysConfig tool.
 *
 *  Radio Config module version : 1.8
 *  SmartRF Studio data version : 2.20.0
 */

#include <ti/devices/DeviceFamily.h>
#include DeviceFamily_constructPath(driverlib/rf_mailbox.h)
#include DeviceFamily_constructPath(driverlib/rf_common_cmd.h)
#include DeviceFamily_constructPath(driverlib/rf_ble_cmd.h)
#include <ti/drivers/rf/RF.h>
#include DeviceFamily_constructPath(rf_patches/rf_patch_cpe_bt5.h)
#include "ti_radio_config.h"

// Custom overrides
#include <ti/ble5stack/icall/inc/ble_overrides.h>


// *********************************************************************************
//   RF Frontend configuration
// *********************************************************************************
// RF design based on: LPSTK-CC1352R1 (CC1352EM-XD7793-XD24)

// TX Power tables
// The RF_TxPowerTable_DEFAULT_PA_ENTRY and RF_TxPowerTable_HIGH_PA_ENTRY macros are defined in RF.h.
// The following arguments are required:
// RF_TxPowerTable_DEFAULT_PA_ENTRY(bias, gain, boost, coefficient)
// RF_TxPowerTable_HIGH_PA_ENTRY(bias, ibboost, boost, coefficient, ldoTrim)
// See the Technical Reference Manual for further details about the "txPower" Command field.
// The PA settings require the CCFG_FORCE_VDDR_HH = 0 unless stated otherwise.

// 868 MHz, 13 dBm
RF_TxPowerTable_Entry txPowerTable_868_pa13[TXPOWERTABLE_868_PA13_SIZE] =
{
    {-20, RF_TxPowerTable_DEFAULT_PA_ENTRY(0, 3, 0, 2) },
    {-15, RF_TxPowerTable_DEFAULT_PA_ENTRY(1, 3, 0, 3) },
    {-10, RF_TxPowerTable_DEFAULT_PA_ENTRY(2, 3, 0, 5) },
    {-5, RF_TxPowerTable_DEFAULT_PA_ENTRY(4, 3, 0, 5) },
    {0, RF_TxPowerTable_DEFAULT_PA_ENTRY(8, 3, 0, 8) },
    {1, RF_TxPowerTable_DEFAULT_PA_ENTRY(9, 3, 0, 9) },
    {2, RF_TxPowerTable_DEFAULT_PA_ENTRY(10, 3, 0, 9) },
    {3, RF_TxPowerTable_DEFAULT_PA_ENTRY(11, 3, 0, 10) },
    {4, RF_TxPowerTable_DEFAULT_PA_ENTRY(13, 3, 0, 11) },
    {5, RF_TxPowerTable_DEFAULT_PA_ENTRY(14, 3, 0, 14) },
    {6, RF_TxPowerTable_DEFAULT_PA_ENTRY(17, 3, 0, 16) },
    {7, RF_TxPowerTable_DEFAULT_PA_ENTRY(20, 3, 0, 19) },
    {8, RF_TxPowerTable_DEFAULT_PA_ENTRY(24, 3, 0, 22) },
    {9, RF_TxPowerTable_DEFAULT_PA_ENTRY(28, 3, 0, 31) },
    {10, RF_TxPowerTable_DEFAULT_PA_ENTRY(18, 2, 0, 31) },
    {11, RF_TxPowerTable_DEFAULT_PA_ENTRY(26, 2, 0, 51) },
    {12, RF_TxPowerTable_DEFAULT_PA_ENTRY(16, 0, 0, 82) },
    // The original PA value (12.5 dBm) has been rounded to an integer value.
    {13, RF_TxPowerTable_DEFAULT_PA_ENTRY(36, 0, 0, 89) },
    // This setting requires CCFG_FORCE_VDDR_HH = 1.
    {14, RF_TxPowerTable_DEFAULT_PA_ENTRY(63, 0, 1, 0) },
    RF_TxPowerTable_TERMINATION_ENTRY
};


// 2400 MHz, 5 dBm
RF_TxPowerTable_Entry txPowerTable_2400_pa5[TXPOWERTABLE_2400_PA5_SIZE] =
{
    {-20, RF_TxPowerTable_DEFAULT_PA_ENTRY(6, 3, 0, 2) },
    {-18, RF_TxPowerTable_DEFAULT_PA_ENTRY(8, 3, 0, 3) },
    {-15, RF_TxPowerTable_DEFAULT_PA_ENTRY(10, 3, 0, 3) },
    {-12, RF_TxPowerTable_DEFAULT_PA_ENTRY(12, 3, 0, 5) },
    {-10, RF_TxPowerTable_DEFAULT_PA_ENTRY(15, 3, 0, 5) },
    {-9, RF_TxPowerTable_DEFAULT_PA_ENTRY(16, 3, 0, 5) },
    {-6, RF_TxPowerTable_DEFAULT_PA_ENTRY(20, 3, 0, 8) },
    {-5, RF_TxPowerTable_DEFAULT_PA_ENTRY(22, 3, 0, 9) },
    {-3, RF_TxPowerTable_DEFAULT_PA_ENTRY(19, 2, 0, 12) },
    {0, RF_TxPowerTable_DEFAULT_PA_ENTRY(19, 1, 0, 20) },
    {1, RF_TxPowerTable_DEFAULT_PA_ENTRY(22, 1, 0, 20) },
    {2, RF_TxPowerTable_DEFAULT_PA_ENTRY(25, 1, 0, 25) },
    {3, RF_TxPowerTable_DEFAULT_PA_ENTRY(29, 1, 0, 28) },
    {4, RF_TxPowerTable_DEFAULT_PA_ENTRY(35, 1, 0, 39) },
    {5, RF_TxPowerTable_DEFAULT_PA_ENTRY(23, 0, 0, 57) },
    RF_TxPowerTable_TERMINATION_ENTRY
};



//*********************************************************************************
//  RF Setting:   BLE, 1 Mbps, LE 1M
//
//  PHY:          bt5le1m
//  Setting file: setting_bt5_le_1m.json
//*********************************************************************************

// PARAMETER SUMMARY
// NB! Setting RF parameters in this design has no effect as no RF commands are selected.

// TI-RTOS RF Mode Object
RF_Mode RF_modeBle =
{
    .rfMode = RF_MODE_AUTO,
    .cpePatchFxn = &rf_patch_cpe_bt5,
    .mcePatchFxn = 0,
    .rfePatchFxn = 0
};

// Overrides for CMD_BLE5_RADIO_SETUP
uint32_t pOverrides_bleCommon[] =
{
    // override_ble5_setup_override_common.json
    // DC/DC regulator: In Tx, use DCDCCTL5[3:0]=0x3 (DITHER_EN=0 and IPEAK=3).
    (uint32_t)0x00F388D3,
    // Bluetooth 5: Set pilot tone length to 20 us Common
    HW_REG_OVERRIDE(0x6024,0x2E20),
    // Bluetooth 5: Compensate for reduced pilot tone length
    (uint32_t)0x01280263,
    // Bluetooth 5: Default to no CTE. 
    HW_REG_OVERRIDE(0x5328,0x0000),
    // Synth: Increase mid code calibration time to 5 us
    (uint32_t)0x00058683,
    // Synth: Increase mid code calibration time to 5 us
    HW32_ARRAY_OVERRIDE(0x4004,1),
    // Synth: Increase mid code calibration time to 5 us
    (uint32_t)0x38183C30,
    // Bluetooth 5: Move synth start code
    HW_REG_OVERRIDE(0x4064,0x3C),
    // Bluetooth 5: Set DTX gain -5% for 1 Mbps
    (uint32_t)0x00E787E3,
    // Bluetooth 5: Set DTX threshold 1 Mbps
    (uint32_t)0x00950803,
    // Bluetooth 5: Set DTX gain -2.5% for 2 Mbps
    (uint32_t)0x00F487F3,
    // Bluetooth 5: Set DTX threshold 2 Mbps
    (uint32_t)0x012A0823,
    // Bluetooth 5: Set synth fine code calibration interval
    HW32_ARRAY_OVERRIDE(0x4020,1),
    // Bluetooth 5: Set synth fine code calibration interval
    (uint32_t)0x41005F00,
    // Bluetooth 5: Adapt to synth fine code calibration interval
    (uint32_t)0xC0040141,
    // Bluetooth 5: Adapt to synth fine code calibration interval
    (uint32_t)0x0007DD44,
    // Bluetooth 5: Set enhanced TX shape
    (uint32_t)0x000D8C73,
    // ti/ble5stack/icall/inc/ble_overrides.h
    BLE_STACK_OVERRIDES(),
    (uint32_t)0xFFFFFFFF
};

// Overrides for CMD_BLE5_RADIO_SETUP
uint32_t pOverrides_ble1Mbps[] =
{
    // override_ble5_setup_override_1mbps.json
    // Bluetooth 5: Set pilot tone length to 20 us
    HW_REG_OVERRIDE(0x5320,0x03C0),
    // Bluetooth 5: Compensate syncTimeadjust
    (uint32_t)0x015302A3,
    (uint32_t)0xFFFFFFFF
};

// Overrides for CMD_BLE5_RADIO_SETUP
uint32_t pOverrides_ble2Mbps[] =
{
    // override_ble5_setup_override_2mbps.json
    // Bluetooth 5: Set pilot tone length to 20 us
    HW_REG_OVERRIDE(0x5320,0x03C0),
    // Bluetooth 5: Compensate syncTimeAdjust
    (uint32_t)0x00F102A3,
    // Bluetooth 5: increase low gain AGC delay for 2 Mbps
    HW_REG_OVERRIDE(0x60A4,0x7D00),
    (uint32_t)0xFFFFFFFF
};

// Overrides for CMD_BLE5_RADIO_SETUP
uint32_t pOverrides_bleCoded[] =
{
    // override_ble5_setup_override_coded.json
    // Bluetooth 5: Set pilot tone length to 20 us
    HW_REG_OVERRIDE(0x5320,0x03C0),
    // Bluetooth 5: Compensate syncTimeadjust
    (uint32_t)0x07A902A3,
    // Rx: Set AGC reference level to 0x1B (default: 0x2E)
    HW_REG_OVERRIDE(0x609C,0x001B),
    (uint32_t)0xFFFFFFFF
};




