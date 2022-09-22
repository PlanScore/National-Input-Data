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

all: assembled-state-TX.parquet \
     assembled-state-CA.parquet \
     assembled-state-FL.parquet \
     assembled-state-AK.parquet \
     assembled-state-AL.parquet \
     assembled-state-AR.parquet \
     assembled-state-AZ.parquet \
     assembled-state-CO.parquet \
     assembled-state-CT.parquet \
     assembled-state-DC.parquet \
     assembled-state-DE.parquet \
     assembled-state-GA.parquet \
     assembled-state-HI.parquet \
     assembled-state-IA.parquet \
     assembled-state-ID.parquet \
     assembled-state-IL.parquet \
     assembled-state-IN.parquet \
     assembled-state-KS.parquet \
     assembled-state-KY.parquet \
     assembled-state-LA.parquet \
     assembled-state-MA.parquet \
     assembled-state-MD.parquet \
     assembled-state-ME.parquet \
     assembled-state-MI.parquet \
     assembled-state-MN.parquet \
     assembled-state-MO.parquet \
     assembled-state-MS.parquet \
     assembled-state-MT.parquet \
     assembled-state-NC.parquet \
     assembled-state-ND.parquet \
     assembled-state-NE.parquet \
     assembled-state-NH.parquet \
     assembled-state-NJ.parquet \
     assembled-state-NM.parquet \
     assembled-state-NV.parquet \
     assembled-state-NY.parquet \
     assembled-state-OH.parquet \
     assembled-state-OK.parquet \
     assembled-state-OR.parquet \
     assembled-state-PA.parquet \
     assembled-state-RI.parquet \
     assembled-state-SC.parquet \
     assembled-state-SD.parquet \
     assembled-state-TN.parquet \
     assembled-state-UT.parquet \
     assembled-state-VA.parquet \
     assembled-state-VT.parquet \
     assembled-state-WA.parquet \
     assembled-state-WI.parquet \
     assembled-state-WV.parquet \
     assembled-state-WY.parquet

assembled-state-AK.parquet: VEST/ak_2020.zip Census/ak2020.pl.zip Census/tl_2019_02_bg.zip Census/tl_2019_02_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_AK_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/ak_2020.zip /vsizip/VEST/ak_2018.zip /vsizip/VEST/ak_2016.zip \
		Census/ak2020.pl.zip /vsizip/Census/tl_2019_02_bg.zip /vsizip/Census/tl_2019_02_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_AK_2020_VD_tabblock.centroid.json

assembled-state-AL.parquet: VEST/al_2020.zip VEST/al_2018.zip VEST/al_2016.zip Census/al2020.pl.zip Census/tl_2011_01_bg.zip Census/tl_2011_01_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_AL_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/al_2020.zip /vsizip/VEST/al_2018.zip /vsizip/VEST/al_2016.zip \
		Census/al2020.pl.zip /vsizip/Census/tl_2011_01_bg.zip /vsizip/Census/tl_2011_01_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_AL_2020_VD_tabblock.centroid.json

assembled-state-AR.parquet: VEST/ar_2020.zip VEST/ar_2018.zip VEST/ar_2016.zip Census/ar2020.pl.zip Census/tl_2011_05_bg.zip Census/tl_2011_05_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_AR_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/ar_2020.zip /vsizip/VEST/ar_2018.zip /vsizip/VEST/ar_2016.zip \
		Census/ar2020.pl.zip /vsizip/Census/tl_2011_05_bg.zip /vsizip/Census/tl_2011_05_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_AR_2020_VD_tabblock.centroid.json

assembled-state-AZ.parquet: VEST/az_2020.zip VEST/az_2018.zip VEST/az_2016.zip Census/az2020.pl.zip Census/tl_2019_04_bg.zip Census/tl_2019_04_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_AZ_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/az_2020.zip /vsizip/VEST/az_2018.zip /vsizip/VEST/az_2016.zip \
		Census/az2020.pl.zip /vsizip/Census/tl_2019_04_bg.zip /vsizip/Census/tl_2019_04_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_AZ_2020_VD_tabblock.centroid.json

assembled-state-CA.parquet: VEST/ca_2020.zip Census/ca2020.pl.zip Census/tl_2019_06_bg.zip Census/tl_2019_06_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_CA_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/ca_2020.zip \
		Census/ca2020.pl.zip /vsizip/Census/tl_2019_06_bg.zip /vsizip/Census/tl_2019_06_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_CA_2020_VD_tabblock.centroid.json

assembled-state-CO.parquet: VEST/co_2020.zip VEST/co_2018.zip VEST/co_2016.zip Census/co2020.pl.zip Census/tl_2019_08_bg.zip Census/tl_2019_08_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_CO_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/co_2020.zip /vsizip/VEST/co_2018.zip /vsizip/VEST/co_2016.zip \
		Census/co2020.pl.zip /vsizip/Census/tl_2019_08_bg.zip /vsizip/Census/tl_2019_08_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_CO_2020_VD_tabblock.centroid.json

assembled-state-CT.parquet: VEST/ct_2020.zip VEST/ct_2018.zip VEST/ct_2016.zip Census/ct2020.pl.zip Census/tl_2019_09_bg.zip Census/tl_2019_09_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_CT_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/ct_2020.zip /vsizip/VEST/ct_2018.zip /vsizip/VEST/ct_2016.zip \
		Census/ct2020.pl.zip /vsizip/Census/tl_2019_09_bg.zip /vsizip/Census/tl_2019_09_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_CT_2020_VD_tabblock.centroid.json

assembled-state-DC.parquet: VEST/dc_2020.zip Census/dc2020.pl.zip Census/tl_2019_11_bg.zip Census/tl_2019_11_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_DC_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/dc_2020.zip \
		Census/dc2020.pl.zip /vsizip/Census/tl_2019_11_bg.zip /vsizip/Census/tl_2019_11_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_DC_2020_VD_tabblock.centroid.json

assembled-state-DE.parquet: VEST/de_2020.zip VEST/de_2018.zip VEST/de_2016.zip Census/de2020.pl.zip Census/tl_2019_10_bg.zip Census/tl_2019_10_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_DE_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/de_2020.zip /vsizip/VEST/de_2018.zip /vsizip/VEST/de_2016.zip \
		Census/de2020.pl.zip /vsizip/Census/tl_2019_10_bg.zip /vsizip/Census/tl_2019_10_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_DE_2020_VD_tabblock.centroid.json

assembled-state-FL.parquet: VEST/fl_2020.zip VEST/fl_2018.zip VEST/fl_2016.zip Census/fl2020.pl.zip Census/tl_2019_12_bg.zip Census/tl_2019_12_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_FL_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/fl_2020.zip /vsizip/VEST/fl_2018.zip /vsizip/VEST/fl_2016.zip \
		Census/fl2020.pl.zip /vsizip/Census/tl_2019_12_bg.zip /vsizip/Census/tl_2019_12_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_FL_2020_VD_tabblock.centroid.json

assembled-state-GA.parquet: VEST/ga_2020.zip VEST/ga_2018.zip VEST/ga_2016.zip Census/ga2020.pl.zip Census/tl_2019_13_bg.zip Census/tl_2019_13_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_GA_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/ga_2020.zip /vsizip/VEST/ga_2018.zip /vsizip/VEST/ga_2016.zip \
		Census/ga2020.pl.zip /vsizip/Census/tl_2019_13_bg.zip /vsizip/Census/tl_2019_13_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_GA_2020_VD_tabblock.centroid.json

assembled-state-HI.parquet: VEST/hi_2020.zip VEST/hi_2018.zip VEST/hi_2016.zip Census/hi2020.pl.zip Census/tl_2019_15_bg.zip Census/tl_2019_15_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_HI_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/hi_2020.zip /vsizip/VEST/hi_2018.zip /vsizip/VEST/hi_2016.zip \
		Census/hi2020.pl.zip /vsizip/Census/tl_2019_15_bg.zip /vsizip/Census/tl_2019_15_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_HI_2020_VD_tabblock.centroid.json

assembled-state-IA.parquet: VEST/ia_2020.zip VEST/ia_2018.zip VEST/ia_2016.zip Census/ia2020.pl.zip Census/tl_2019_19_bg.zip Census/tl_2019_19_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_IA_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/ia_2020.zip /vsizip/VEST/ia_2018.zip /vsizip/VEST/ia_2016.zip \
		Census/ia2020.pl.zip /vsizip/Census/tl_2019_19_bg.zip /vsizip/Census/tl_2019_19_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_IA_2020_VD_tabblock.centroid.json

assembled-state-ID.parquet: VEST/id_2020.zip VEST/id_2018.zip VEST/id_2016.zip Census/id2020.pl.zip Census/tl_2019_16_bg.zip Census/tl_2019_16_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_ID_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/id_2020.zip /vsizip/VEST/id_2018.zip /vsizip/VEST/id_2016.zip \
		Census/id2020.pl.zip /vsizip/Census/tl_2019_16_bg.zip /vsizip/Census/tl_2019_16_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_ID_2020_VD_tabblock.centroid.json

assembled-state-IL.parquet: VEST/il_2020.zip VEST/il_2018.zip VEST/il_2016.zip Census/il2020.pl.zip Census/tl_2019_17_bg.zip Census/tl_2019_17_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_IL_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/il_2020.zip /vsizip/VEST/il_2018.zip /vsizip/VEST/il_2016.zip \
		Census/il2020.pl.zip /vsizip/Census/tl_2019_17_bg.zip /vsizip/Census/tl_2019_17_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_IL_2020_VD_tabblock.centroid.json

assembled-state-IN.parquet: VEST/in_2020.zip VEST/in_2018.zip VEST/in_2016.zip Census/in2020.pl.zip Census/tl_2019_18_bg.zip Census/tl_2019_18_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_IN_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/in_2020.zip /vsizip/VEST/in_2018.zip /vsizip/VEST/in_2016.zip \
		Census/in2020.pl.zip /vsizip/Census/tl_2019_18_bg.zip /vsizip/Census/tl_2019_18_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_IN_2020_VD_tabblock.centroid.json

assembled-state-KS.parquet: VEST/ks_2020.zip VEST/ks_2018.zip VEST/ks_2016.zip Census/ks2020.pl.zip Census/tl_2019_20_bg.zip Census/tl_2019_20_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_KS_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/ks_2020.zip /vsizip/VEST/ks_2018.zip /vsizip/VEST/ks_2016.zip \
		Census/ks2020.pl.zip /vsizip/Census/tl_2019_20_bg.zip /vsizip/Census/tl_2019_20_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_KS_2020_VD_tabblock.centroid.json

assembled-state-KY.parquet: VEST/ky_2020.zip VEST/ky_2016.zip Census/ky2020.pl.zip Census/tl_2019_21_bg.zip Census/tl_2019_21_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_KY_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/ky_2020.zip /vsizip/VEST/ky_2016.zip \
		Census/ky2020.pl.zip /vsizip/Census/tl_2019_21_bg.zip /vsizip/Census/tl_2019_21_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_KY_2020_VD_tabblock.centroid.json

assembled-state-LA.parquet: VEST/la_2020.zip VEST/la_2018.zip VEST/la_2016.zip Census/la2020.pl.zip Census/tl_2019_22_bg.zip Census/tl_2019_22_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_LA_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/la_2020.zip /vsizip/VEST/la_2018.zip /vsizip/VEST/la_2016.zip \
		Census/la2020.pl.zip /vsizip/Census/tl_2019_22_bg.zip /vsizip/Census/tl_2019_22_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_LA_2020_VD_tabblock.centroid.json

assembled-state-MD.parquet: VEST/md_2020.zip VEST/md_2018.zip VEST/md_2016.zip Census/md2020.pl.zip Census/tl_2019_24_bg.zip Census/tl_2019_24_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_MD_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/md_2020.zip /vsizip/VEST/md_2018.zip /vsizip/VEST/md_2016.zip \
		Census/md2020.pl.zip /vsizip/Census/tl_2019_24_bg.zip /vsizip/Census/tl_2019_24_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_MD_2020_VD_tabblock.centroid.json

assembled-state-ME.parquet: VEST/me_2020.zip VEST/me_2018.zip VEST/me_2016.zip Census/me2020.pl.zip Census/tl_2019_23_bg.zip Census/tl_2019_23_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_ME_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/me_2020.zip /vsizip/VEST/me_2018.zip /vsizip/VEST/me_2016.zip \
		Census/me2020.pl.zip /vsizip/Census/tl_2019_23_bg.zip /vsizip/Census/tl_2019_23_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_ME_2020_VD_tabblock.centroid.json

assembled-state-MA.parquet: VEST/ma_2020.zip VEST/ma_2018.zip VEST/ma_2016.zip Census/ma2020.pl.zip Census/tl_2019_25_bg.zip Census/tl_2019_25_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_MA_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/ma_2020.zip /vsizip/VEST/ma_2018.zip /vsizip/VEST/ma_2016.zip \
		Census/ma2020.pl.zip /vsizip/Census/tl_2019_25_bg.zip /vsizip/Census/tl_2019_25_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_MA_2020_VD_tabblock.centroid.json

assembled-state-MI.parquet: VEST/mi_2020.zip VEST/mi_2018.zip VEST/mi_2016.zip Census/mi2020.pl.zip Census/tl_2019_26_bg.zip Census/tl_2019_26_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_MI_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/mi_2020.zip /vsizip/VEST/mi_2018.zip /vsizip/VEST/mi_2016.zip \
		Census/mi2020.pl.zip /vsizip/Census/tl_2019_26_bg.zip /vsizip/Census/tl_2019_26_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_MI_2020_VD_tabblock.centroid.json

assembled-state-MN.parquet: VEST/mn_2020.zip VEST/mn_2018.zip VEST/mn_2016.zip Census/mn2020.pl.zip Census/tl_2019_27_bg.zip Census/tl_2019_27_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_MN_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/mn_2020.zip /vsizip/VEST/mn_2018.zip /vsizip/VEST/mn_2016.zip \
		Census/mn2020.pl.zip /vsizip/Census/tl_2019_27_bg.zip /vsizip/Census/tl_2019_27_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_MN_2020_VD_tabblock.centroid.json

assembled-state-MO.parquet: VEST/mo_2020.zip VEST/mo_2018.zip VEST/mo_2016.zip Census/mo2020.pl.zip Census/tl_2019_29_bg.zip Census/tl_2019_29_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_MO_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/mo_2020.zip /vsizip/VEST/mo_2018.zip /vsizip/VEST/mo_2016.zip \
		Census/mo2020.pl.zip /vsizip/Census/tl_2019_29_bg.zip /vsizip/Census/tl_2019_29_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_MO_2020_VD_tabblock.centroid.json

assembled-state-MS.parquet: VEST/ms_2020.zip VEST/ms_2018.zip VEST/ms_2016.zip Census/ms2020.pl.zip Census/tl_2019_28_bg.zip Census/tl_2019_28_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_MS_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/ms_2020.zip /vsizip/VEST/ms_2018.zip /vsizip/VEST/ms_2016.zip \
		Census/ms2020.pl.zip /vsizip/Census/tl_2019_28_bg.zip /vsizip/Census/tl_2019_28_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_MS_2020_VD_tabblock.centroid.json

assembled-state-MT.parquet: VEST/mt_2020.zip VEST/mt_2018.zip VEST/mt_2016.zip Census/mt2020.pl.zip Census/tl_2019_30_bg.zip Census/tl_2019_30_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_MT_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/mt_2020.zip /vsizip/VEST/mt_2018.zip /vsizip/VEST/mt_2016.zip \
		Census/mt2020.pl.zip /vsizip/Census/tl_2019_30_bg.zip /vsizip/Census/tl_2019_30_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_MT_2020_VD_tabblock.centroid.json

assembled-state-NC.parquet: VEST/nc_2020.zip VEST/nc_2018.zip VEST/nc_2016.zip Census/nc2020.pl.zip Census/tl_2019_37_bg.zip Census/tl_2019_37_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_NC_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/nc_2020.zip /vsizip/VEST/nc_2018.zip /vsizip/VEST/nc_2016.zip \
		Census/nc2020.pl.zip /vsizip/Census/tl_2019_37_bg.zip /vsizip/Census/tl_2019_37_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_NC_2020_VD_tabblock.centroid.json

assembled-state-ND.parquet: VEST/nd_2020.zip VEST/nd_2018.zip VEST/nd_2016.zip Census/nd2020.pl.zip Census/tl_2019_38_bg.zip Census/tl_2019_38_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_ND_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/nd_2020.zip /vsizip/VEST/nd_2018.zip /vsizip/VEST/nd_2016.zip \
		Census/nd2020.pl.zip /vsizip/Census/tl_2019_38_bg.zip /vsizip/Census/tl_2019_38_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_ND_2020_VD_tabblock.centroid.json

assembled-state-NE.parquet: VEST/ne_2020.zip VEST/ne_2018.zip VEST/ne_2016.zip Census/ne2020.pl.zip Census/tl_2019_31_bg.zip Census/tl_2019_31_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_NE_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/ne_2020.zip /vsizip/VEST/ne_2018.zip /vsizip/VEST/ne_2016.zip \
		Census/ne2020.pl.zip /vsizip/Census/tl_2019_31_bg.zip /vsizip/Census/tl_2019_31_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_NE_2020_VD_tabblock.centroid.json

assembled-state-NH.parquet: VEST/nh_2020.zip VEST/nh_2018.zip VEST/nh_2016.zip Census/nh2020.pl.zip Census/tl_2019_33_bg.zip Census/tl_2019_33_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_NH_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/nh_2020.zip /vsizip/VEST/nh_2018.zip /vsizip/VEST/nh_2016.zip \
		Census/nh2020.pl.zip /vsizip/Census/tl_2019_33_bg.zip /vsizip/Census/tl_2019_33_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_NH_2020_VD_tabblock.centroid.json

assembled-state-NJ.parquet: VEST/nj_2020.zip VEST/nj_2018.zip VEST/nj_2016.zip Census/nj2020.pl.zip Census/tl_2019_34_bg.zip Census/tl_2019_34_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_NJ_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/nj_2020.zip /vsizip/VEST/nj_2018.zip /vsizip/VEST/nj_2016.zip \
		Census/nj2020.pl.zip /vsizip/Census/tl_2019_34_bg.zip /vsizip/Census/tl_2019_34_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_NJ_2020_VD_tabblock.centroid.json

assembled-state-NM.parquet: VEST/nm_2020.zip VEST/nm_2018.zip VEST/nm_2016.zip Census/nm2020.pl.zip Census/tl_2019_35_bg.zip Census/tl_2019_35_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_NM_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/nm_2020.zip /vsizip/VEST/nm_2018.zip /vsizip/VEST/nm_2016.zip \
		Census/nm2020.pl.zip /vsizip/Census/tl_2019_35_bg.zip /vsizip/Census/tl_2019_35_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_NM_2020_VD_tabblock.centroid.json

assembled-state-NV.parquet: VEST/nv_2020.zip VEST/nv_2018.zip VEST/nv_2016.zip Census/nv2020.pl.zip Census/tl_2019_32_bg.zip Census/tl_2019_32_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_NV_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/nv_2020.zip /vsizip/VEST/nv_2018.zip /vsizip/VEST/nv_2016.zip \
		Census/nv2020.pl.zip /vsizip/Census/tl_2019_32_bg.zip /vsizip/Census/tl_2019_32_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_NV_2020_VD_tabblock.centroid.json

assembled-state-NY.parquet: VEST/ny_2020.zip VEST/ny_2018.zip VEST/ny_2016.zip Census/ny2020.pl.zip Census/tl_2019_36_bg.zip Census/tl_2019_36_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_NY_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/ny_2020.zip /vsizip/VEST/ny_2018.zip /vsizip/VEST/ny_2016.zip \
		Census/ny2020.pl.zip /vsizip/Census/tl_2019_36_bg.zip /vsizip/Census/tl_2019_36_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_NY_2020_VD_tabblock.centroid.json

assembled-state-OH.parquet: VEST/oh_2020.zip VEST/oh_2018.zip VEST/oh_2016.zip Census/oh2020.pl.zip Census/tl_2019_39_bg.zip Census/tl_2019_39_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_OH_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/oh_2020.zip /vsizip/VEST/oh_2018.zip /vsizip/VEST/oh_2016.zip \
		Census/oh2020.pl.zip /vsizip/Census/tl_2019_39_bg.zip /vsizip/Census/tl_2019_39_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_OH_2020_VD_tabblock.centroid.json

assembled-state-OK.parquet: VEST/ok_2020.zip VEST/ok_2018.zip VEST/ok_2016.zip Census/ok2020.pl.zip Census/tl_2019_40_bg.zip Census/tl_2019_40_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_OK_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/ok_2020.zip /vsizip/VEST/ok_2018.zip /vsizip/VEST/ok_2016.zip \
		Census/ok2020.pl.zip /vsizip/Census/tl_2019_40_bg.zip /vsizip/Census/tl_2019_40_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_OK_2020_VD_tabblock.centroid.json

assembled-state-OR.parquet: VEST/or_2020.zip VEST/or_2018.zip VEST/or_2016.zip Census/or2020.pl.zip Census/tl_2019_41_bg.zip Census/tl_2019_41_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_OR_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/or_2020.zip /vsizip/VEST/or_2018.zip /vsizip/VEST/or_2016.zip \
		Census/or2020.pl.zip /vsizip/Census/tl_2019_41_bg.zip /vsizip/Census/tl_2019_41_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_OR_2020_VD_tabblock.centroid.json

assembled-state-PA.parquet: VEST/pa_2020.zip VEST/pa_2018.zip VEST/pa_2016.zip Census/pa2020.pl.zip Census/tl_2019_42_bg.zip Census/tl_2019_42_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_PA_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/pa_2020.zip /vsizip/VEST/pa_2018.zip /vsizip/VEST/pa_2016.zip \
		Census/pa2020.pl.zip /vsizip/Census/tl_2019_42_bg.zip /vsizip/Census/tl_2019_42_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_PA_2020_VD_tabblock.centroid.json

assembled-state-RI.parquet: VEST/ri_2020.zip VEST/ri_2018.zip VEST/ri_2016.zip Census/ri2020.pl.zip Census/tl_2019_44_bg.zip Census/tl_2019_44_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_RI_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/ri_2020.zip /vsizip/VEST/ri_2018.zip /vsizip/VEST/ri_2016.zip \
		Census/ri2020.pl.zip /vsizip/Census/tl_2019_44_bg.zip /vsizip/Census/tl_2019_44_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_RI_2020_VD_tabblock.centroid.json

assembled-state-SC.parquet: VEST/sc_2020.zip VEST/sc_2018.zip VEST/sc_2016.zip Census/sc2020.pl.zip Census/tl_2011_45_bg.zip Census/tl_2011_45_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_SC_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/sc_2020.zip /vsizip/VEST/sc_2018.zip /vsizip/VEST/sc_2016.zip \
		Census/sc2020.pl.zip /vsizip/Census/tl_2011_45_bg.zip /vsizip/Census/tl_2011_45_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_SC_2020_VD_tabblock.centroid.json

assembled-state-SD.parquet: VEST/sd_2020.zip VEST/sd_2018.zip VEST/sd_2016.zip Census/sd2020.pl.zip Census/tl_2019_46_bg.zip Census/tl_2019_46_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_SD_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/sd_2020.zip /vsizip/VEST/sd_2018.zip /vsizip/VEST/sd_2016.zip \
		Census/sd2020.pl.zip /vsizip/Census/tl_2019_46_bg.zip /vsizip/Census/tl_2019_46_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_SD_2020_VD_tabblock.centroid.json

assembled-state-TN.parquet: VEST/tn_2020.zip Census/tn2020.pl.zip Census/tl_2019_47_bg.zip Census/tl_2019_47_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_TN_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/tn_2020.zip \
		Census/tn2020.pl.zip /vsizip/Census/tl_2019_47_bg.zip /vsizip/Census/tl_2019_47_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_TN_2020_VD_tabblock.centroid.json

assembled-state-UT.parquet: VEST/ut_2020.zip VEST/ut_2018.zip VEST/ut_2016.zip Census/ut2020.pl.zip Census/tl_2019_49_bg.zip Census/tl_2019_49_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_UT_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/ut_2020.zip /vsizip/VEST/ut_2018.zip /vsizip/VEST/ut_2016.zip \
		Census/ut2020.pl.zip /vsizip/Census/tl_2019_49_bg.zip /vsizip/Census/tl_2019_49_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_UT_2020_VD_tabblock.centroid.json

assembled-state-VA.parquet: VEST/va_2020.zip VEST/va_2018.zip VEST/va_2016.zip Census/va2020.pl.zip Census/tl_2019_51_bg.zip Census/tl_2019_51_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_VA_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/va_2020.zip /vsizip/VEST/va_2018.zip /vsizip/VEST/va_2016.zip \
		Census/va2020.pl.zip /vsizip/Census/tl_2019_51_bg.zip /vsizip/Census/tl_2019_51_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_VA_2020_VD_tabblock.centroid.json

assembled-state-TX.parquet: VEST/tx_2020.zip VEST/tx_2018.zip VEST/tx_2016.zip Census/tx2020.pl.zip Census/tl_2019_48_bg.zip Census/tl_2019_48_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_TX_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/tx_2020.zip /vsizip/VEST/tx_2018.zip /vsizip/VEST/tx_2016.zip \
		Census/tx2020.pl.zip /vsizip/Census/tl_2019_48_bg.zip /vsizip/Census/tl_2019_48_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_TX_2020_VD_tabblock.centroid.json

assembled-state-VT.parquet: VEST/vt_2020.zip VEST/vt_2018.zip VEST/vt_2016.zip Census/vt2020.pl.zip Census/tl_2019_50_bg.zip Census/tl_2019_50_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_VT_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/vt_2020.zip /vsizip/VEST/vt_2018.zip /vsizip/VEST/vt_2016.zip \
		Census/vt2020.pl.zip /vsizip/Census/tl_2019_50_bg.zip /vsizip/Census/tl_2019_50_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_VT_2020_VD_tabblock.centroid.json

assembled-state-WA.parquet: VEST/wa_2020.zip VEST/wa_2018.zip VEST/wa_2016.zip Census/wa2020.pl.zip Census/tl_2019_53_bg.zip Census/tl_2019_53_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_WA_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/wa_2020.zip /vsizip/VEST/wa_2018.zip /vsizip/VEST/wa_2016.zip \
		Census/wa2020.pl.zip /vsizip/Census/tl_2019_53_bg.zip /vsizip/Census/tl_2019_53_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_WA_2020_VD_tabblock.centroid.json

assembled-state-WI.parquet: VEST/wi_2020.zip VEST/wi_2018.zip VEST/wi_2016.zip Census/wi2020.pl.zip Census/tl_2019_55_bg.zip Census/tl_2019_55_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_WI_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/wi_2020.zip /vsizip/VEST/wi_2018.zip /vsizip/VEST/wi_2016.zip \
		Census/wi2020.pl.zip /vsizip/Census/tl_2019_55_bg.zip /vsizip/Census/tl_2019_55_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_WI_2020_VD_tabblock.centroid.json

assembled-state-WV.parquet: VEST/wv_2020.zip VEST/wv_2018.zip VEST/wv_2016.zip Census/wv2020.pl.zip Census/tl_2019_54_bg.zip Census/tl_2019_54_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_WV_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/wv_2020.zip /vsizip/VEST/wv_2018.zip /vsizip/VEST/wv_2016.zip \
		Census/wv2020.pl.zip /vsizip/Census/tl_2019_54_bg.zip /vsizip/Census/tl_2019_54_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_WV_2020_VD_tabblock.centroid.json

assembled-state-WY.parquet: VEST/wy_2020.zip VEST/wy_2018.zip VEST/wy_2016.zip Census/wy2020.pl.zip Census/tl_2019_56_bg.zip Census/tl_2019_56_tract.zip Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_WY_2020_VD_tabblock.centroid.json
	./assemble-state.py $@ \
		/vsizip/VEST/wy_2020.zip /vsizip/VEST/wy_2018.zip /vsizip/VEST/wy_2016.zip \
		Census/wy2020.pl.zip /vsizip/Census/tl_2019_56_bg.zip /vsizip/Census/tl_2019_56_tract.zip \
		Census/CVAP_2015-2019_ACS_csv_files.zip Census/DRA_WY_2020_VD_tabblock.centroid.json

# Linked from https://www.census.gov/programs-surveys/decennial-census/about/voting-rights/cvap.2019.html
Census/CVAP_2015-2019_ACS_csv_files.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/rdo/datasets/2019/2019-cvap/CVAP_2015-2019_ACS_csv_files.zip -o $@

Census/tl_2019_%_tract.zip:
	curl -L https://www2.census.gov/geo/tiger/TIGER2019/TRACT/tl_2019_$*_tract.zip -o $@

Census/tl_2019_%_bg.zip:
	curl -L https://www2.census.gov/geo/tiger/TIGER2019/BG/tl_2019_$*_bg.zip -o $@

Census/tl_2011_%_tract.zip:
	curl -L https://www2.census.gov/geo/tiger/TIGER2011/TRACT/tl_2011_$*_tract.zip -o $@

Census/tl_2011_%_bg.zip:
	curl -L https://www2.census.gov/geo/tiger/TIGER2011/BG/tl_2011_$*_bg.zip -o $@

Census/DRA_%_2020_VD_tabblock.centroid.json:
	curl -L https://dra-us-west-datafiles.s3.us-west-2.amazonaws.com/_$*_2020_VD_tabblock.centroid.json -o $@ --compressed

Census/dc2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/District_of_Columbia/dc2020.pl.zip -o $@

Census/al2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/Alabama/al2020.pl.zip -o $@

Census/ak2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/Alaska/ak2020.pl.zip -o $@

Census/az2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/Arizona/az2020.pl.zip -o $@

Census/ar2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/Arkansas/ar2020.pl.zip -o $@

Census/ca2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/California/ca2020.pl.zip -o $@

Census/co2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/Colorado/co2020.pl.zip -o $@

Census/ct2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/Connecticut/ct2020.pl.zip -o $@

Census/de2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/Delaware/de2020.pl.zip -o $@

Census/fl2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/Florida/fl2020.pl.zip -o $@

Census/ga2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/Georgia/ga2020.pl.zip -o $@

Census/hi2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/Hawaii/hi2020.pl.zip -o $@

Census/id2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/Idaho/id2020.pl.zip -o $@

Census/il2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/Illinois/il2020.pl.zip -o $@

Census/in2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/Indiana/in2020.pl.zip -o $@

Census/ia2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/Iowa/ia2020.pl.zip -o $@

Census/ks2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/Kansas/ks2020.pl.zip -o $@

Census/ky2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/Kentucky/ky2020.pl.zip -o $@

Census/la2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/Louisiana/la2020.pl.zip -o $@

Census/me2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/Maine/me2020.pl.zip -o $@

Census/md2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/Maryland/md2020.pl.zip -o $@

Census/ma2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/Massachusetts/ma2020.pl.zip -o $@

Census/mi2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/Michigan/mi2020.pl.zip -o $@

Census/mn2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/Minnesota/mn2020.pl.zip -o $@

Census/ms2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/Mississippi/ms2020.pl.zip -o $@

Census/mo2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/Missouri/mo2020.pl.zip -o $@

Census/mt2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/Montana/mt2020.pl.zip -o $@

Census/ne2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/Nebraska/ne2020.pl.zip -o $@

Census/nv2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/Nevada/nv2020.pl.zip -o $@

Census/nh2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/New_Hampshire/nh2020.pl.zip -o $@

Census/nj2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/New_Jersey/nj2020.pl.zip -o $@

Census/nm2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/New_Mexico/nm2020.pl.zip -o $@

Census/ny2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/New_York/ny2020.pl.zip -o $@

Census/nc2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/North_Carolina/nc2020.pl.zip -o $@

Census/nd2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/North_Dakota/nd2020.pl.zip -o $@

Census/oh2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/Ohio/oh2020.pl.zip -o $@

Census/ok2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/Oklahoma/ok2020.pl.zip -o $@

Census/or2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/Oregon/or2020.pl.zip -o $@

Census/pa2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/Pennsylvania/pa2020.pl.zip -o $@

Census/ri2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/Rhode_Island/ri2020.pl.zip -o $@

Census/sc2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/South_Carolina/sc2020.pl.zip -o $@

Census/sd2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/South_Dakota/sd2020.pl.zip -o $@

Census/tn2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/Tennessee/tn2020.pl.zip -o $@

Census/tx2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/Texas/tx2020.pl.zip -o $@

Census/ut2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/Utah/ut2020.pl.zip -o $@

Census/vt2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/Vermont/vt2020.pl.zip -o $@

Census/va2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/Virginia/va2020.pl.zip -o $@

Census/wa2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/Washington/wa2020.pl.zip -o $@

Census/wv2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/West_Virginia/wv2020.pl.zip -o $@

Census/wi2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/Wisconsin/wi2020.pl.zip -o $@

Census/wy2020.pl.zip:
	curl -L https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/Wyoming/wy2020.pl.zip -o $@

.PHONY: all
.SECONDARY:
