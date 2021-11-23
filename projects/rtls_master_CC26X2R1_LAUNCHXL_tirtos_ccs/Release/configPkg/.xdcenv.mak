#
_XDCBUILDCOUNT = 
ifneq (,$(findstring path,$(_USEXDCENV_)))
override XDCPATH = C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source;C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/kernel/tirtos/packages
override XDCROOT = C:/ti/ccs1030/xdctools_3_62_00_08_core
override XDCBUILDCFG = ./config.bld
endif
ifneq (,$(findstring args,$(_USEXDCENV_)))
override XDCARGS = 
override XDCTARGETS = 
endif
#
ifeq (0,1)
PKGPATH = C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/source;C:/ti/simplelink_cc13x2_26x2_sdk_4_40_00_44/kernel/tirtos/packages;C:/ti/ccs1030/xdctools_3_62_00_08_core/packages;..
HOSTOS = Windows
endif
