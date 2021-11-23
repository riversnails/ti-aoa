# invoke SourceDir generated makefile for rtls_coordinator_app.pem4f
rtls_coordinator_app.pem4f: .libraries,rtls_coordinator_app.pem4f
.libraries,rtls_coordinator_app.pem4f: package/cfg/rtls_coordinator_app_pem4f.xdl
	$(MAKE) -f C:\Users\user\Documents\workspace\ti_aoa_workspace\v5_rtls_coordinator_CC26X2R1_LAUNCHXL_tirtos_ccs/src/makefile.libs

clean::
	$(MAKE) -f C:\Users\user\Documents\workspace\ti_aoa_workspace\v5_rtls_coordinator_CC26X2R1_LAUNCHXL_tirtos_ccs/src/makefile.libs clean

