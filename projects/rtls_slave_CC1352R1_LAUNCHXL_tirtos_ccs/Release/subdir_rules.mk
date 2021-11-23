################################################################################
# Automatically-generated file. Do not edit!
################################################################################

SHELL = cmd.exe

# Each subdirectory must supply rules for building sources it contributes
build-1946901521: ../rtls_slave.syscfg
	@echo 'Building file: "$<"'
	@echo 'Invoking: SysConfig'
	"C:/ti/sysconfig_1.7.0/sysconfig_cli.bat" -s "C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/.metadata/product.json" -o "syscfg" "C:/Users/user/Documents/workspace/ti_aoa_workspace/rtls_slave_CC1352R1_LAUNCHXL_tirtos_ccs/rtls_slave.syscfg" --compiler ccs
	@echo 'Finished building: "$<"'
	@echo ' '

syscfg/ti_devices_config.c: build-1946901521 ../rtls_slave.syscfg
syscfg/ti_radio_config.c: build-1946901521
syscfg/ti_radio_config.h: build-1946901521
syscfg/ti_drivers_config.c: build-1946901521
syscfg/ti_drivers_config.h: build-1946901521
syscfg/ti_utils_build_linker.cmd.genlibs: build-1946901521
syscfg/syscfg_c.rov.xs: build-1946901521
syscfg/ti_utils_runtime_model.gv: build-1946901521
syscfg/ti_utils_runtime_Makefile: build-1946901521
syscfg/: build-1946901521

syscfg/%.obj: ./syscfg/%.c $(GEN_OPTS) | $(GEN_FILES) $(GEN_MISC_FILES)
	@echo 'Building file: "$<"'
	@echo 'Invoking: Arm Compiler'
	"C:/ti/ccs1030/ccs/tools/compiler/ti-cgt-arm_20.2.5.LTS/bin/armcl" --cmd_file="C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/examples/rtos/CC1352R1_LAUNCHXL/ble5stack/rtls_slave/Tools/Defines/rtls_slave_app.opt" --cmd_file="C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/ble5stack/config/build_components.opt" --cmd_file="C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/ble5stack/config/factory_config.opt" --cmd_file="C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/examples/rtos/CC1352R1_LAUNCHXL/ble5stack/rtls_slave/build_config.opt"  -mv7M4 --code_state=16 --float_support=FPv4SPD16 -me -O4 --opt_for_speed=0 --include_path="C:/Users/user/Documents/workspace/ti_aoa_workspace/rtls_slave_CC1352R1_LAUNCHXL_tirtos_ccs" --include_path="C:/Users/user/Documents/workspace/ti_aoa_workspace/rtls_slave_CC1352R1_LAUNCHXL_tirtos_ccs/Release" --include_path="C:/Users/user/Documents/workspace/ti_aoa_workspace/rtls_slave_CC1352R1_LAUNCHXL_tirtos_ccs/Application" --include_path="C:/Users/user/Documents/workspace/ti_aoa_workspace/rtls_slave_CC1352R1_LAUNCHXL_tirtos_ccs/RTLSCtrl" --include_path="C:/Users/user/Documents/workspace/ti_aoa_workspace/rtls_slave_CC1352R1_LAUNCHXL_tirtos_ccs/Drivers/AOA" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/ble5stack/npi/src/unified/inc" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/ble5stack/npi/src/unified" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/kernel/tirtos/packages" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/ble5stack/controller/cc26xx/inc" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/ble5stack/inc" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/ble5stack/rom" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/ble5stack/common/cc26xx" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/ble5stack/icall/inc" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/ble5stack/hal/src/target/_common" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/ble5stack/hal/src/target/_common/cc26xx" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/ble5stack/hal/src/inc" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/ble5stack/heapmgr" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/ble5stack/profiles/dev_info" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/ble5stack/profiles/simple_profile" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/ble5stack/icall/src/inc" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/ble5stack/osal/src/inc" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/ble5stack/services/src/saddr" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/ble5stack/services/src/sdata" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/common/nv" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/common/cc26xx" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/devices/cc13x2_cc26x2" --include_path="C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/posix/ccs" --include_path="C:/ti/ccs1030/ccs/tools/compiler/ti-cgt-arm_20.2.5.LTS/include" --define=DeviceFamily_CC13X2 --define=FLASH_ROM_BUILD --define=NVOCMP_NWSAMEITEM=1 -g --c99 --gcc --diag_warning=225 --diag_warning=255 --diag_wrap=off --display_error_number --gen_func_subsections=on --abi=eabi --preproc_with_compile --preproc_dependency="syscfg/$(basename $(<F)).d_raw" --include_path="C:/Users/user/Documents/workspace/ti_aoa_workspace/rtls_slave_CC1352R1_LAUNCHXL_tirtos_ccs/Release/syscfg" --obj_directory="syscfg" $(GEN_OPTS__FLAG) "$<"
	@echo 'Finished building: "$<"'
	@echo ' '

build-413762913:
	@$(MAKE) --no-print-directory -Onone -f subdir_rules.mk build-413762913-inproc

build-413762913-inproc: ../rtls_slave_app.cfg
	@echo 'Building file: "$<"'
	@echo 'Invoking: XDCtools'
	"C:/ti/ccs1030/xdctools_3_62_00_08_core/xs" --xdcpath="C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source;C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/kernel/tirtos/packages;" xdc.tools.configuro -o configPkg -t ti.targets.arm.elf.M4F -p ti.platforms.simplelink:CC2642R1F -r release -c "C:/ti/ccs1030/ccs/tools/compiler/ti-cgt-arm_20.2.5.LTS" --compileOptions "-mv7M4 --code_state=16 --float_support=FPv4SPD16 -me -O4 --opt_for_speed=0 --include_path=\"C:/Users/user/Documents/workspace/ti_aoa_workspace/rtls_slave_CC1352R1_LAUNCHXL_tirtos_ccs\" --include_path=\"C:/Users/user/Documents/workspace/ti_aoa_workspace/rtls_slave_CC1352R1_LAUNCHXL_tirtos_ccs/Release\" --include_path=\"C:/Users/user/Documents/workspace/ti_aoa_workspace/rtls_slave_CC1352R1_LAUNCHXL_tirtos_ccs/Application\" --include_path=\"C:/Users/user/Documents/workspace/ti_aoa_workspace/rtls_slave_CC1352R1_LAUNCHXL_tirtos_ccs/RTLSCtrl\" --include_path=\"C:/Users/user/Documents/workspace/ti_aoa_workspace/rtls_slave_CC1352R1_LAUNCHXL_tirtos_ccs/Drivers/AOA\" --include_path=\"C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/ble5stack/npi/src/unified/inc\" --include_path=\"C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/ble5stack/npi/src/unified\" --include_path=\"C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source\" --include_path=\"C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/kernel/tirtos/packages\" --include_path=\"C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/ble5stack/controller/cc26xx/inc\" --include_path=\"C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/ble5stack/inc\" --include_path=\"C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/ble5stack/rom\" --include_path=\"C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/ble5stack/common/cc26xx\" --include_path=\"C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/ble5stack/icall/inc\" --include_path=\"C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/ble5stack/hal/src/target/_common\" --include_path=\"C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/ble5stack/hal/src/target/_common/cc26xx\" --include_path=\"C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/ble5stack/hal/src/inc\" --include_path=\"C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/ble5stack/heapmgr\" --include_path=\"C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/ble5stack/profiles/dev_info\" --include_path=\"C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/ble5stack/profiles/simple_profile\" --include_path=\"C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/ble5stack/icall/src/inc\" --include_path=\"C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/ble5stack/osal/src/inc\" --include_path=\"C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/ble5stack/services/src/saddr\" --include_path=\"C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/ble5stack/services/src/sdata\" --include_path=\"C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/common/nv\" --include_path=\"C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/common/cc26xx\" --include_path=\"C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/devices/cc13x2_cc26x2\" --include_path=\"C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source/ti/posix/ccs\" --include_path=\"C:/ti/ccs1030/ccs/tools/compiler/ti-cgt-arm_20.2.5.LTS/include\" --define=DeviceFamily_CC13X2 --define=FLASH_ROM_BUILD --define=NVOCMP_NWSAMEITEM=1 -g --c99 --gcc --diag_warning=225 --diag_warning=255 --diag_wrap=off --display_error_number --gen_func_subsections=on --abi=eabi  " "$<"
	@echo 'Finished building: "$<"'
	@echo ' '

configPkg/linker.cmd: build-413762913 ../rtls_slave_app.cfg
configPkg/compiler.opt: build-413762913
configPkg/: build-413762913


