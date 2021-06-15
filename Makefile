# 
# For high-priority states, here's a tentative list:
# 	• FL (risk of Rep gerrymander)
# 	• GA (risk of Rep gerrymander)
# 	• IL (risk of Dem gerrymander)
# 	• IN (risk of Rep gerrymander)
# 	• MD (risk of Dem gerrymander)
# 	• MA (risk of Dem gerrymander)
# 	• MI (new controversial commission)
# 	• MO (risk of Rep gerrymander)
# 	• NY (risk of Dem gerrymander)
# 	• NC (risk of Rep gerrymander)
# 	• OH (new redistricting process)
# 	• TN (risk of Rep gerrymander)
# 	• TX (risk of Rep gerrymander)
# 	• WI (risk of Rep gerrymander)
# 

all: assembled-state-TX.geojson \
     assembled-state-CA.geojson \
     assembled-state-FL.geojson \
     assembled-state-AK.geojson \
     assembled-state-AL.geojson \
     assembled-state-AR.geojson \
     assembled-state-AZ.geojson \
     assembled-state-CO.geojson \
     assembled-state-DC.geojson \
     assembled-state-DE.geojson \
     assembled-state-GA.geojson \
     assembled-state-HI.geojson \
     assembled-state-IA.geojson \
     assembled-state-ID.geojson \
     assembled-state-IL.geojson \
     assembled-state-IN.geojson \
     assembled-state-KS.geojson \
     assembled-state-KY.geojson \
     assembled-state-LA.geojson \
     assembled-state-MA.geojson \
     assembled-state-MD.geojson \
     assembled-state-ME.geojson \
     assembled-state-MI.geojson \
     assembled-state-MN.geojson \
     assembled-state-MO.geojson \
     assembled-state-MT.geojson \
     assembled-state-NC.geojson \
     assembled-state-ND.geojson \
     assembled-state-NE.geojson \
     assembled-state-NH.geojson \
     assembled-state-NJ.geojson \
     assembled-state-NM.geojson \
     assembled-state-NV.geojson \
     assembled-state-OH.geojson \
     assembled-state-OK.geojson \
     assembled-state-OR.geojson \
     assembled-state-RI.geojson \
     assembled-state-SC.geojson \
     assembled-state-SD.geojson \
     assembled-state-TN.geojson \
     assembled-state-UT.geojson \
     assembled-state-VT.geojson \
     assembled-state-WA.geojson \
     assembled-state-WI.geojson \
     assembled-state-WY.geojson

Nation.gpkg: all
	ogr2ogr -f GPKG -nln blocks_AK -nlt Point -overwrite $@ assembled-state-AK.geojson
	ogr2ogr -f GPKG -nln blocks_AL -nlt Point -overwrite $@ assembled-state-AL.geojson
	ogr2ogr -f GPKG -nln blocks_AR -nlt Point -overwrite $@ assembled-state-AR.geojson
	ogr2ogr -f GPKG -nln blocks_AZ -nlt Point -overwrite $@ assembled-state-AZ.geojson
	ogr2ogr -f GPKG -nln blocks_CA -nlt Point -overwrite $@ assembled-state-CA.geojson
	ogr2ogr -f GPKG -nln blocks_CO -nlt Point -overwrite $@ assembled-state-CO.geojson
	ogr2ogr -f GPKG -nln blocks_DC -nlt Point -overwrite $@ assembled-state-DC.geojson
	ogr2ogr -f GPKG -nln blocks_DE -nlt Point -overwrite $@ assembled-state-DE.geojson
	ogr2ogr -f GPKG -nln blocks_FL -nlt Point -overwrite $@ assembled-state-FL.geojson
	ogr2ogr -f GPKG -nln blocks_GA -nlt Point -overwrite $@ assembled-state-GA.geojson
	ogr2ogr -f GPKG -nln blocks_HI -nlt Point -overwrite $@ assembled-state-HI.geojson
	ogr2ogr -f GPKG -nln blocks_IA -nlt Point -overwrite $@ assembled-state-IA.geojson
	ogr2ogr -f GPKG -nln blocks_ID -nlt Point -overwrite $@ assembled-state-ID.geojson
	ogr2ogr -f GPKG -nln blocks_IL -nlt Point -overwrite $@ assembled-state-IL.geojson
	ogr2ogr -f GPKG -nln blocks_IN -nlt Point -overwrite $@ assembled-state-IN.geojson
	ogr2ogr -f GPKG -nln blocks_KS -nlt Point -overwrite $@ assembled-state-KS.geojson
	ogr2ogr -f GPKG -nln blocks_KY -nlt Point -overwrite $@ assembled-state-KY.geojson
	ogr2ogr -f GPKG -nln blocks_LA -nlt Point -overwrite $@ assembled-state-LA.geojson
	ogr2ogr -f GPKG -nln blocks_MA -nlt Point -overwrite $@ assembled-state-MA.geojson
	ogr2ogr -f GPKG -nln blocks_MD -nlt Point -overwrite $@ assembled-state-MD.geojson
	ogr2ogr -f GPKG -nln blocks_ME -nlt Point -overwrite $@ assembled-state-ME.geojson
	ogr2ogr -f GPKG -nln blocks_MI -nlt Point -overwrite $@ assembled-state-MI.geojson
	ogr2ogr -f GPKG -nln blocks_MN -nlt Point -overwrite $@ assembled-state-MN.geojson
	ogr2ogr -f GPKG -nln blocks_MO -nlt Point -overwrite $@ assembled-state-MO.geojson
	ogr2ogr -f GPKG -nln blocks_MT -nlt Point -overwrite $@ assembled-state-MT.geojson
	ogr2ogr -f GPKG -nln blocks_NC -nlt Point -overwrite $@ assembled-state-NC.geojson
	ogr2ogr -f GPKG -nln blocks_ND -nlt Point -overwrite $@ assembled-state-ND.geojson
	ogr2ogr -f GPKG -nln blocks_NE -nlt Point -overwrite $@ assembled-state-NE.geojson
	ogr2ogr -f GPKG -nln blocks_NH -nlt Point -overwrite $@ assembled-state-NH.geojson
	ogr2ogr -f GPKG -nln blocks_NJ -nlt Point -overwrite $@ assembled-state-NJ.geojson
	ogr2ogr -f GPKG -nln blocks_NM -nlt Point -overwrite $@ assembled-state-NM.geojson
	ogr2ogr -f GPKG -nln blocks_NV -nlt Point -overwrite $@ assembled-state-NV.geojson
	ogr2ogr -f GPKG -nln blocks_OH -nlt Point -overwrite $@ assembled-state-OH.geojson
	ogr2ogr -f GPKG -nln blocks_OK -nlt Point -overwrite $@ assembled-state-OK.geojson
	ogr2ogr -f GPKG -nln blocks_RI -nlt Point -overwrite $@ assembled-state-RI.geojson
	ogr2ogr -f GPKG -nln blocks_SC -nlt Point -overwrite $@ assembled-state-SC.geojson
	ogr2ogr -f GPKG -nln blocks_SD -nlt Point -overwrite $@ assembled-state-SD.geojson
	ogr2ogr -f GPKG -nln blocks_TN -nlt Point -overwrite $@ assembled-state-TN.geojson
	ogr2ogr -f GPKG -nln blocks_UT -nlt Point -overwrite $@ assembled-state-UT.geojson
	ogr2ogr -f GPKG -nln blocks_TX -nlt Point -overwrite $@ assembled-state-TX.geojson
	ogr2ogr -f GPKG -nln blocks_VT -nlt Point -overwrite $@ assembled-state-VT.geojson
	ogr2ogr -f GPKG -nln blocks_WA -nlt Point -overwrite $@ assembled-state-WA.geojson
	ogr2ogr -f GPKG -nln blocks_WI -nlt Point -overwrite $@ assembled-state-WI.geojson
	ogr2ogr -f GPKG -nln blocks_WY -nlt Point -overwrite $@ assembled-state-WY.geojson
	ogr2ogr -f GPKG -nln votes_AK -nlt MultiPolygon -overwrite $@ /vsizip/VEST/ak_2020.zip
	ogr2ogr -f GPKG -nln votes_AL -nlt MultiPolygon -overwrite $@ /vsizip/VEST/al_2020.zip
	ogr2ogr -f GPKG -nln votes_AR -nlt MultiPolygon -overwrite $@ /vsizip/VEST/ar_2016.zip
	ogr2ogr -f GPKG -nln votes_AZ -nlt MultiPolygon -overwrite $@ /vsizip/VEST/az_2020.zip
	ogr2ogr -f GPKG -nln votes_CA -nlt MultiPolygon -overwrite $@ /vsizip/VEST/ca_2016.zip
	ogr2ogr -f GPKG -nln votes_CO -nlt MultiPolygon -overwrite $@ /vsizip/VEST/co_2016.zip
	ogr2ogr -f GPKG -nln votes_DC -nlt MultiPolygon -overwrite $@ /vsizip/VEST/dc_2020.zip
	ogr2ogr -f GPKG -nln votes_DE -nlt MultiPolygon -overwrite $@ /vsizip/VEST/de_2020.zip
	ogr2ogr -f GPKG -nln votes_FL -nlt MultiPolygon -overwrite $@ /vsizip/VEST/fl_2016.zip
	ogr2ogr -f GPKG -nln votes_GA -nlt MultiPolygon -overwrite $@ /vsizip/VEST/ga_2020.zip
	ogr2ogr -f GPKG -nln votes_HI -nlt MultiPolygon -overwrite $@ /vsizip/VEST/hi_2020.zip
	ogr2ogr -f GPKG -nln votes_IA -nlt MultiPolygon -overwrite $@ /vsizip/VEST/ia_2020.zip
	ogr2ogr -f GPKG -nln votes_ID -nlt MultiPolygon -overwrite $@ /vsizip/VEST/id_2020.zip
	ogr2ogr -f GPKG -nln votes_IL -nlt MultiPolygon -overwrite $@ /vsizip/VEST/il_2020.zip
	ogr2ogr -f GPKG -nln votes_IN -nlt MultiPolygon -overwrite $@ /vsizip/VEST/in_2016.zip
	ogr2ogr -f GPKG -nln votes_KS -nlt MultiPolygon -overwrite $@ /vsizip/VEST/ks_2020.zip
	ogr2ogr -f GPKG -nln votes_KY -nlt MultiPolygon -overwrite $@ /vsizip/VEST/ky_2016.zip
	ogr2ogr -f GPKG -nln votes_LA -nlt MultiPolygon -overwrite $@ /vsizip/VEST/la_2020.zip
	ogr2ogr -f GPKG -nln votes_MA -nlt MultiPolygon -overwrite $@ /vsizip/VEST/ma_2016.zip
	ogr2ogr -f GPKG -nln votes_MD -nlt MultiPolygon -overwrite $@ /vsizip/VEST/md_2016.zip
	ogr2ogr -f GPKG -nln votes_ME -nlt MultiPolygon -overwrite $@ /vsizip/VEST/me_2016.zip
	ogr2ogr -f GPKG -nln votes_MI -nlt MultiPolygon -overwrite $@ /vsizip/VEST/mi_2016.zip
	ogr2ogr -f GPKG -nln votes_MN -nlt MultiPolygon -overwrite $@ /vsizip/VEST/mn_2020.zip
	ogr2ogr -f GPKG -nln votes_MO -nlt MultiPolygon -overwrite $@ /vsizip/VEST/mo_2016.zip
	ogr2ogr -f GPKG -nln votes_MT -nlt MultiPolygon -overwrite $@ /vsizip/VEST/mt_2020.zip
	ogr2ogr -f GPKG -nln votes_NC -nlt MultiPolygon -overwrite $@ /vsizip/VEST/nc_2016.zip
	ogr2ogr -f GPKG -nln votes_ND -nlt MultiPolygon -overwrite $@ /vsizip/VEST/nd_2016.zip
	ogr2ogr -f GPKG -nln votes_NE -nlt MultiPolygon -overwrite $@ /vsizip/VEST/ne_2016.zip
	ogr2ogr -f GPKG -nln votes_NH -nlt MultiPolygon -overwrite $@ /vsizip/VEST/nh_2020.zip
	ogr2ogr -f GPKG -nln votes_NJ -nlt MultiPolygon -overwrite $@ /vsizip/VEST/nj_2016.zip
	ogr2ogr -f GPKG -nln votes_NM -nlt MultiPolygon -overwrite $@ /vsizip/VEST/nm_2016.zip
	ogr2ogr -f GPKG -nln votes_NV -nlt MultiPolygon -overwrite $@ /vsizip/VEST/nv_2016.zip
	ogr2ogr -f GPKG -nln votes_OH -nlt MultiPolygon -overwrite $@ /vsizip/VEST/oh_2020.zip
	ogr2ogr -f GPKG -nln votes_OK -nlt MultiPolygon -overwrite $@ /vsizip/VEST/ok_2020.zip
	ogr2ogr -f GPKG -nln votes_OR -nlt MultiPolygon -overwrite $@ /vsizip/VEST/or_2016.zip
	ogr2ogr -f GPKG -nln votes_RI -nlt MultiPolygon -overwrite $@ /vsizip/VEST/ri_2020.zip
	ogr2ogr -f GPKG -nln votes_SC -nlt MultiPolygon -overwrite $@ /vsizip/VEST/sc_2020.zip
	ogr2ogr -f GPKG -nln votes_SD -nlt MultiPolygon -overwrite $@ /vsizip/VEST/sd_2016.zip
	ogr2ogr -f GPKG -nln votes_TN -nlt MultiPolygon -overwrite $@ /vsizip/VEST/tn_2016.zip
	ogr2ogr -f GPKG -nln votes_UT -nlt MultiPolygon -overwrite $@ /vsizip/VEST/ut_2016.zip
	ogr2ogr -f GPKG -nln votes_TX -nlt MultiPolygon -overwrite $@ /vsizip/VEST/tx_2016.zip
	ogr2ogr -f GPKG -nln votes_VT -nlt MultiPolygon -overwrite $@ /vsizip/VEST/vt_2016.zip
	ogr2ogr -f GPKG -nln votes_WA -nlt MultiPolygon -overwrite $@ /vsizip/VEST/wa_2016.zip
	ogr2ogr -f GPKG -nln votes_WI -nlt MultiPolygon -overwrite $@ /vsizip/VEST/wi_2020.zip
	ogr2ogr -f GPKG -nln votes_WY -nlt MultiPolygon -overwrite $@ /vsizip/VEST/wy_2020.zip

assembled-state-AK.geojson: VEST/ak_2020.zip Census/tl_2011_02_tabblock.zip Census/tl_2011_02_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/ak_2020.zip /vsizip/Census/tl_2011_02_tabblock.zip /vsizip/Census/tl_2011_02_bg.zip

assembled-state-AL.geojson: VEST/al_2020.zip Census/tl_2011_01_tabblock.zip Census/tl_2011_01_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/al_2020.zip /vsizip/Census/tl_2011_01_tabblock.zip /vsizip/Census/tl_2011_01_bg.zip

assembled-state-AR.geojson: VEST/ar_2016.zip Census/tl_2011_05_tabblock.zip Census/tl_2011_05_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/ar_2016.zip /vsizip/Census/tl_2011_05_tabblock.zip /vsizip/Census/tl_2011_05_bg.zip

assembled-state-AZ.geojson: VEST/az_2020.zip Census/tl_2011_04_tabblock.zip Census/tl_2011_04_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/az_2020.zip /vsizip/Census/tl_2011_04_tabblock.zip /vsizip/Census/tl_2011_04_bg.zip

assembled-state-CA.geojson: VEST/ca_2016.zip Census/tl_2019_06_tabblock10.zip Census/tl_2019_06_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/ca_2016.zip /vsizip/Census/tl_2019_06_tabblock10.zip /vsizip/Census/tl_2019_06_bg.zip

assembled-state-CO.geojson: VEST/co_2016.zip Census/tl_2019_08_tabblock10.zip Census/tl_2019_08_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/co_2016.zip /vsizip/Census/tl_2019_08_tabblock10.zip /vsizip/Census/tl_2019_08_bg.zip

assembled-state-DC.geojson: VEST/dc_2020.zip Census/tl_2019_11_tabblock10.zip Census/tl_2019_11_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/dc_2020.zip /vsizip/Census/tl_2019_11_tabblock10.zip /vsizip/Census/tl_2019_11_bg.zip

assembled-state-DE.geojson: VEST/de_2020.zip Census/tl_2019_10_tabblock10.zip Census/tl_2019_10_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/de_2020.zip /vsizip/Census/tl_2019_10_tabblock10.zip /vsizip/Census/tl_2019_10_bg.zip

assembled-state-FL.geojson: VEST/fl_2016.zip Census/tl_2019_12_tabblock10.zip Census/tl_2019_12_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/fl_2016.zip /vsizip/Census/tl_2019_12_tabblock10.zip /vsizip/Census/tl_2019_12_bg.zip

assembled-state-GA.geojson: VEST/ga_2020.zip Census/tl_2019_13_tabblock10.zip Census/tl_2019_13_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/ga_2020.zip /vsizip/Census/tl_2019_13_tabblock10.zip /vsizip/Census/tl_2019_13_bg.zip

assembled-state-HI.geojson: VEST/hi_2020.zip Census/tl_2019_15_tabblock10.zip Census/tl_2019_15_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/hi_2020.zip /vsizip/Census/tl_2019_15_tabblock10.zip /vsizip/Census/tl_2019_15_bg.zip

assembled-state-IA.geojson: VEST/ia_2020.zip Census/tl_2019_19_tabblock10.zip Census/tl_2019_19_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/ia_2020.zip /vsizip/Census/tl_2019_19_tabblock10.zip /vsizip/Census/tl_2019_19_bg.zip

assembled-state-ID.geojson: VEST/id_2020.zip Census/tl_2019_16_tabblock10.zip Census/tl_2019_16_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/id_2020.zip /vsizip/Census/tl_2019_16_tabblock10.zip /vsizip/Census/tl_2019_16_bg.zip

assembled-state-IL.geojson: VEST/il_2020.zip Census/tl_2019_17_tabblock10.zip Census/tl_2019_17_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/il_2020.zip /vsizip/Census/tl_2019_17_tabblock10.zip /vsizip/Census/tl_2019_17_bg.zip

assembled-state-IN.geojson: VEST/in_2016.zip Census/tl_2019_18_tabblock10.zip Census/tl_2019_18_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/in_2016.zip /vsizip/Census/tl_2019_18_tabblock10.zip /vsizip/Census/tl_2019_18_bg.zip

assembled-state-KS.geojson: VEST/ks_2020.zip Census/tl_2019_20_tabblock10.zip Census/tl_2019_20_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/ks_2020.zip /vsizip/Census/tl_2019_20_tabblock10.zip /vsizip/Census/tl_2019_20_bg.zip

assembled-state-KY.geojson: VEST/ky_2016.zip Census/tl_2019_21_tabblock10.zip Census/tl_2019_21_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/ky_2016.zip /vsizip/Census/tl_2019_21_tabblock10.zip /vsizip/Census/tl_2019_21_bg.zip

assembled-state-LA.geojson: VEST/la_2020.zip Census/tl_2019_22_tabblock10.zip Census/tl_2019_22_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/la_2020.zip /vsizip/Census/tl_2019_22_tabblock10.zip /vsizip/Census/tl_2019_22_bg.zip

assembled-state-MD.geojson: VEST/md_2016.zip Census/tl_2019_24_tabblock10.zip Census/tl_2019_24_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/md_2016.zip /vsizip/Census/tl_2019_24_tabblock10.zip /vsizip/Census/tl_2019_24_bg.zip

assembled-state-ME.geojson: VEST/me_2016.zip Census/tl_2019_23_tabblock10.zip Census/tl_2019_23_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/me_2016.zip /vsizip/Census/tl_2019_23_tabblock10.zip /vsizip/Census/tl_2019_23_bg.zip

assembled-state-MA.geojson: VEST/ma_2016.zip Census/tl_2019_25_tabblock10.zip Census/tl_2019_25_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/ma_2016.zip /vsizip/Census/tl_2019_25_tabblock10.zip /vsizip/Census/tl_2019_25_bg.zip

assembled-state-MI.geojson: VEST/mi_2016.zip Census/tl_2019_26_tabblock10.zip Census/tl_2019_26_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/mi_2016.zip /vsizip/Census/tl_2019_26_tabblock10.zip /vsizip/Census/tl_2019_26_bg.zip

assembled-state-MN.geojson: VEST/mn_2020.zip Census/tl_2019_27_tabblock10.zip Census/tl_2019_27_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/mn_2020.zip /vsizip/Census/tl_2019_27_tabblock10.zip /vsizip/Census/tl_2019_27_bg.zip

assembled-state-MO.geojson: VEST/mo_2016.zip Census/tl_2019_29_tabblock10.zip Census/tl_2019_29_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/mo_2016.zip /vsizip/Census/tl_2019_29_tabblock10.zip /vsizip/Census/tl_2019_29_bg.zip

assembled-state-MT.geojson: VEST/mt_2020.zip Census/tl_2019_30_tabblock10.zip Census/tl_2019_30_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/mt_2020.zip /vsizip/Census/tl_2019_30_tabblock10.zip /vsizip/Census/tl_2019_30_bg.zip

assembled-state-NC.geojson: VEST/nc_2016.zip Census/tl_2019_37_tabblock10.zip Census/tl_2019_37_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/nc_2016.zip /vsizip/Census/tl_2019_37_tabblock10.zip /vsizip/Census/tl_2019_37_bg.zip

assembled-state-ND.geojson: VEST/nd_2016.zip Census/tl_2019_38_tabblock10.zip Census/tl_2019_38_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/nd_2016.zip /vsizip/Census/tl_2019_38_tabblock10.zip /vsizip/Census/tl_2019_38_bg.zip

assembled-state-NE.geojson: VEST/ne_2016.zip Census/tl_2019_31_tabblock10.zip Census/tl_2019_31_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/ne_2016.zip /vsizip/Census/tl_2019_31_tabblock10.zip /vsizip/Census/tl_2019_31_bg.zip

assembled-state-NH.geojson: VEST/nh_2020.zip Census/tl_2019_33_tabblock10.zip Census/tl_2019_33_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/nh_2020.zip /vsizip/Census/tl_2019_33_tabblock10.zip /vsizip/Census/tl_2019_33_bg.zip

assembled-state-NJ.geojson: VEST/nj_2016.zip Census/tl_2019_34_tabblock10.zip Census/tl_2019_34_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/nj_2016.zip /vsizip/Census/tl_2019_34_tabblock10.zip /vsizip/Census/tl_2019_34_bg.zip

assembled-state-NM.geojson: VEST/nm_2016.zip Census/tl_2019_35_tabblock10.zip Census/tl_2019_35_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/nm_2016.zip /vsizip/Census/tl_2019_35_tabblock10.zip /vsizip/Census/tl_2019_35_bg.zip

assembled-state-NV.geojson: VEST/nv_2016.zip Census/tl_2019_32_tabblock10.zip Census/tl_2019_32_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/nv_2016.zip /vsizip/Census/tl_2019_32_tabblock10.zip /vsizip/Census/tl_2019_32_bg.zip

assembled-state-OH.geojson: VEST/oh_2020.zip Census/tl_2019_39_tabblock10.zip Census/tl_2019_39_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/oh_2020.zip /vsizip/Census/tl_2019_39_tabblock10.zip /vsizip/Census/tl_2019_39_bg.zip

assembled-state-OK.geojson: VEST/ok_2020.zip Census/tl_2019_40_tabblock10.zip Census/tl_2019_40_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/ok_2020.zip /vsizip/Census/tl_2019_40_tabblock10.zip /vsizip/Census/tl_2019_40_bg.zip

assembled-state-OR.geojson: VEST/or_2016.zip Census/tl_2019_41_tabblock10.zip Census/tl_2019_41_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/or_2016.zip /vsizip/Census/tl_2019_41_tabblock10.zip /vsizip/Census/tl_2019_41_bg.zip

assembled-state-RI.geojson: VEST/ri_2020.zip Census/tl_2019_44_tabblock10.zip Census/tl_2019_44_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/ri_2020.zip /vsizip/Census/tl_2019_44_tabblock10.zip /vsizip/Census/tl_2019_44_bg.zip

assembled-state-SC.geojson: VEST/sc_2020.zip Census/tl_2011_45_tabblock.zip Census/tl_2011_45_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/sc_2020.zip /vsizip/Census/tl_2011_45_tabblock.zip /vsizip/Census/tl_2011_45_bg.zip

assembled-state-SD.geojson: VEST/sd_2016.zip Census/tl_2011_46_tabblock.zip Census/tl_2011_46_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/sd_2016.zip /vsizip/Census/tl_2011_46_tabblock.zip /vsizip/Census/tl_2011_46_bg.zip

assembled-state-TN.geojson: VEST/tn_2016.zip Census/tl_2019_47_tabblock10.zip Census/tl_2019_47_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/tn_2016.zip /vsizip/Census/tl_2019_47_tabblock10.zip /vsizip/Census/tl_2019_47_bg.zip

assembled-state-UT.geojson: VEST/ut_2016.zip Census/tl_2019_49_tabblock10.zip Census/tl_2019_49_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/ut_2016.zip /vsizip/Census/tl_2019_49_tabblock10.zip /vsizip/Census/tl_2019_49_bg.zip

assembled-state-TX.geojson: VEST/tx_2016.zip Census/tl_2019_48_tabblock10.zip Census/tl_2019_48_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/tx_2016.zip /vsizip/Census/tl_2019_48_tabblock10.zip /vsizip/Census/tl_2019_48_bg.zip

assembled-state-VT.geojson: VEST/vt_2016.zip Census/tl_2019_50_tabblock10.zip Census/tl_2019_50_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/vt_2016.zip /vsizip/Census/tl_2019_50_tabblock10.zip /vsizip/Census/tl_2019_50_bg.zip

assembled-state-WA.geojson: VEST/wa_2016.zip Census/tl_2019_53_tabblock10.zip Census/tl_2019_53_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/wa_2016.zip /vsizip/Census/tl_2019_53_tabblock10.zip /vsizip/Census/tl_2019_53_bg.zip

assembled-state-WI.geojson: VEST/wi_2020.zip Census/tl_2019_55_tabblock10.zip Census/tl_2019_55_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/wi_2020.zip /vsizip/Census/tl_2019_55_tabblock10.zip /vsizip/Census/tl_2019_55_bg.zip

assembled-state-WY.geojson: VEST/wy_2020.zip Census/tl_2019_56_tabblock10.zip Census/tl_2019_56_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/wy_2020.zip /vsizip/Census/tl_2019_56_tabblock10.zip /vsizip/Census/tl_2019_56_bg.zip

Census/tl_2019_%_bg.zip:
	curl -L https://www2.census.gov/geo/tiger/TIGER2019/BG/tl_2019_$*_bg.zip -o $@

Census/tl_2019_%_tabblock10.zip:
	curl -L https://www2.census.gov/geo/tiger/TIGER2019/TABBLOCK/tl_2019_$*_tabblock10.zip -o $@

Census/tl_2011_%_bg.zip:
	curl -L https://www2.census.gov/geo/tiger/TIGER2011/BG/tl_2011_$*_bg.zip -o $@

Census/tl_2011_%_tabblock.zip:
	curl -L https://www2.census.gov/geo/tiger/TIGER2011/TABBLOCK/tl_2011_$*_tabblock.zip -o $@

.PHONY: all
.SECONDARY:
