################################################################################
# Automatically-generated file. Do not edit!
################################################################################

SHELL = cmd.exe

# Each subdirectory must supply rules for building sources it contributes
NPI/U_NPI/npi_task.obj: C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/ble5stack/npi/src/unified/npi_task.c $(GEN_OPTS) | $(GEN_FILES) $(GEN_MISC_FILES)
	@echo 'Building file: "$<"'
	@echo 'Invoking: Arm Compiler'
	"C:/ti/ccs1030/ccs/tools/compiler/ti-cgt-arm_20.2.4.LTS/bin/armcl" --cmd_file="C:/Users/user/Documents/workspace/ti_aoa_workspace/v5_rtls_passive_CC26X2R1_LAUNCHXL_tirtos_ccs/Tools/Defines/rtls_passive_app.opt" --cmd_file="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/ble5stack/config/build_components.opt" --cmd_file="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/ble5stack/config/factory_config.opt" --cmd_file="C:/Users/user/Documents/workspace/ti_aoa_workspace/v5_rtls_passive_CC26X2R1_LAUNCHXL_tirtos_ccs/build_config.opt"  -mv7M4 --code_state=16 --float_support=FPv4SPD16 -me -O4 --opt_for_speed=0 --include_path="C:/Users/user/Documents/workspace/ti_aoa_workspace/v5_rtls_passive_CC26X2R1_LAUNCHXL_tirtos_ccs" --include_path="C:/Users/user/Documents/workspace/ti_aoa_workspace/v5_rtls_passive_CC26X2R1_LAUNCHXL_tirtos_ccs/Release" --include_path="C:/Users/user/Documents/workspace/ti_aoa_workspace/v5_rtls_passive_CC26X2R1_LAUNCHXL_tirtos_ccs/Application" --include_path="C:/Users/user/Documents/workspace/ti_aoa_workspace/v5_rtls_passive_CC26X2R1_LAUNCHXL_tirtos_ccs/RTLSCtrl" --include_path="C:/Users/user/Documents/workspace/ti_aoa_workspace/v5_rtls_passive_CC26X2R1_LAUNCHXL_tirtos_ccs/Drivers/AOA" --include_path="C:/Users/user/Documents/workspace/ti_aoa_workspace/v5_rtls_passive_CC26X2R1_LAUNCHXL_tirtos_ccs/HAL/Common" --include_path="C:/Users/user/Documents/workspace/ti_aoa_workspace/v5_rtls_passive_CC26X2R1_LAUNCHXL_tirtos_ccs/HAL/Include" --include_path="C:/Users/user/Documents/workspace/ti_aoa_workspace/v5_rtls_passive_CC26X2R1_LAUNCHXL_tirtos_ccs/Drivers/TRNG" --include_path="C:/Users/user/Documents/workspace/ti_aoa_workspace/v5_rtls_passive_CC26X2R1_LAUNCHXL_tirtos_ccs/Startup" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/ble5stack/npi/src/unified/inc" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/ble5stack/npi/src/unified" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/common/nv/" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/ble5stack/boards" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/kernel/tirtos/packages" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/ble5stack/controller/cc26xx/inc" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/ble5stack/inc" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/ble5stack/rom" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/ble5stack/common/cc26xx" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/ble5stack/icall/inc" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/ble5stack/hal/src/target/_common" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/ble5stack/hal/src/target/_common/cc26xx" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/ble5stack/hal/src/inc" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/ble5stack/heapmgr" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/ble5stack/profiles/dev_info" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/ble5stack/profiles/simple_profile" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/ble5stack/icall/src/inc" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/ble5stack/osal/src/inc" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/ble5stack/services/src/saddr" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/ble5stack/services/src/sdata" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/common/nv" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/common/cc26xx" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/devices/cc13x2_cc26x2" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/posix/ccs" --include_path="C:/ti/ccs1030/ccs/tools/compiler/ti-cgt-arm_20.2.4.LTS/include" --define=DeviceFamily_CC26X2 --define=FLASH_ROM_BUILD --define=NVOCMP_NWSAMEITEM=1 -g --c99 --gcc --diag_warning=225 --diag_warning=255 --diag_wrap=off --display_error_number --gen_func_subsections=on --abi=eabi --preproc_with_compile --preproc_dependency="NPI/U_NPI/$(basename $(<F)).d_raw" --include_path="C:/Users/user/Documents/workspace/ti_aoa_workspace/v5_rtls_passive_CC26X2R1_LAUNCHXL_tirtos_ccs/Release/syscfg" --obj_directory="NPI/U_NPI" $(GEN_OPTS__FLAG) "$<"
	@echo 'Finished building: "$<"'
	@echo ' '

NPI/U_NPI/npi_util.obj: C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/ble5stack/npi/src/unified/npi_util.c $(GEN_OPTS) | $(GEN_FILES) $(GEN_MISC_FILES)
	@echo 'Building file: "$<"'
	@echo 'Invoking: Arm Compiler'
	"C:/ti/ccs1030/ccs/tools/compiler/ti-cgt-arm_20.2.4.LTS/bin/armcl" --cmd_file="C:/Users/user/Documents/workspace/ti_aoa_workspace/v5_rtls_passive_CC26X2R1_LAUNCHXL_tirtos_ccs/Tools/Defines/rtls_passive_app.opt" --cmd_file="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/ble5stack/config/build_components.opt" --cmd_file="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/ble5stack/config/factory_config.opt" --cmd_file="C:/Users/user/Documents/workspace/ti_aoa_workspace/v5_rtls_passive_CC26X2R1_LAUNCHXL_tirtos_ccs/build_config.opt"  -mv7M4 --code_state=16 --float_support=FPv4SPD16 -me -O4 --opt_for_speed=0 --include_path="C:/Users/user/Documents/workspace/ti_aoa_workspace/v5_rtls_passive_CC26X2R1_LAUNCHXL_tirtos_ccs" --include_path="C:/Users/user/Documents/workspace/ti_aoa_workspace/v5_rtls_passive_CC26X2R1_LAUNCHXL_tirtos_ccs/Release" --include_path="C:/Users/user/Documents/workspace/ti_aoa_workspace/v5_rtls_passive_CC26X2R1_LAUNCHXL_tirtos_ccs/Application" --include_path="C:/Users/user/Documents/workspace/ti_aoa_workspace/v5_rtls_passive_CC26X2R1_LAUNCHXL_tirtos_ccs/RTLSCtrl" --include_path="C:/Users/user/Documents/workspace/ti_aoa_workspace/v5_rtls_passive_CC26X2R1_LAUNCHXL_tirtos_ccs/Drivers/AOA" --include_path="C:/Users/user/Documents/workspace/ti_aoa_workspace/v5_rtls_passive_CC26X2R1_LAUNCHXL_tirtos_ccs/HAL/Common" --include_path="C:/Users/user/Documents/workspace/ti_aoa_workspace/v5_rtls_passive_CC26X2R1_LAUNCHXL_tirtos_ccs/HAL/Include" --include_path="C:/Users/user/Documents/workspace/ti_aoa_workspace/v5_rtls_passive_CC26X2R1_LAUNCHXL_tirtos_ccs/Drivers/TRNG" --include_path="C:/Users/user/Documents/workspace/ti_aoa_workspace/v5_rtls_passive_CC26X2R1_LAUNCHXL_tirtos_ccs/Startup" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/ble5stack/npi/src/unified/inc" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/ble5stack/npi/src/unified" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/common/nv/" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/ble5stack/boards" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/kernel/tirtos/packages" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/ble5stack/controller/cc26xx/inc" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/ble5stack/inc" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/ble5stack/rom" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/ble5stack/common/cc26xx" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/ble5stack/icall/inc" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/ble5stack/hal/src/target/_common" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/ble5stack/hal/src/target/_common/cc26xx" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/ble5stack/hal/src/inc" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/ble5stack/heapmgr" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/ble5stack/profiles/dev_info" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/ble5stack/profiles/simple_profile" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/ble5stack/icall/src/inc" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/ble5stack/osal/src/inc" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/ble5stack/services/src/saddr" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/ble5stack/services/src/sdata" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/common/nv" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/common/cc26xx" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/devices/cc13x2_cc26x2" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_5_20_00_52/source/ti/posix/ccs" --include_path="C:/ti/ccs1030/ccs/tools/compiler/ti-cgt-arm_20.2.4.LTS/include" --define=DeviceFamily_CC26X2 --define=FLASH_ROM_BUILD --define=NVOCMP_NWSAMEITEM=1 -g --c99 --gcc --diag_warning=225 --diag_warning=255 --diag_wrap=off --display_error_number --gen_func_subsections=on --abi=eabi --preproc_with_compile --preproc_dependency="NPI/U_NPI/$(basename $(<F)).d_raw" --include_path="C:/Users/user/Documents/workspace/ti_aoa_workspace/v5_rtls_passive_CC26X2R1_LAUNCHXL_tirtos_ccs/Release/syscfg" --obj_directory="NPI/U_NPI" $(GEN_OPTS__FLAG) "$<"
	@echo 'Finished building: "$<"'
	@echo ' '


