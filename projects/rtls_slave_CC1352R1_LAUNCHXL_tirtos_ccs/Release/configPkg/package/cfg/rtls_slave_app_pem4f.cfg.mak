# invoke SourceDir generated makefile for rtls_slave_app.pem4f
rtls_slave_app.pem4f: .libraries,rtls_slave_app.pem4f
.libraries,rtls_slave_app.pem4f: package/cfg/rtls_slave_app_pem4f.xdl
	$(MAKE) -f C:\Users\user\Documents\workspace\ti_aoa_workspace\rtls_slave_CC1352R1_LAUNCHXL_tirtos_ccs/src/makefile.libs

clean::
	$(MAKE) -f C:\Users\user\Documents\workspace\ti_aoa_workspace\rtls_slave_CC1352R1_LAUNCHXL_tirtos_ccs/src/makefile.libs clean

