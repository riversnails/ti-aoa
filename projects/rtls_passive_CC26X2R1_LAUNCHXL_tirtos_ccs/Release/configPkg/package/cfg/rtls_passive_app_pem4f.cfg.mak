# invoke SourceDir generated makefile for rtls_passive_app.pem4f
rtls_passive_app.pem4f: .libraries,rtls_passive_app.pem4f
.libraries,rtls_passive_app.pem4f: package/cfg/rtls_passive_app_pem4f.xdl
	$(MAKE) -f C:\Users\user\Documents\workspace\ti_aoa_workspace\rtls_passive_CC26X2R1_LAUNCHXL_tirtos_ccs/src/makefile.libs

clean::
	$(MAKE) -f C:\Users\user\Documents\workspace\ti_aoa_workspace\rtls_passive_CC26X2R1_LAUNCHXL_tirtos_ccs/src/makefile.libs clean

