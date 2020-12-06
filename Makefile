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
     assembled-state-FL.geojson \
     assembled-state-DE.geojson \
     assembled-state-GA.geojson \
     assembled-state-IL.geojson \
     assembled-state-MA.geojson \
     assembled-state-MD.geojson \
     assembled-state-ME.geojson \
     assembled-state-MI.geojson \
     assembled-state-MT.geojson \
     assembled-state-NC.geojson \
     assembled-state-ND.geojson \
     assembled-state-NH.geojson \
     assembled-state-RI.geojson \
     assembled-state-SD.geojson \
     assembled-state-TN.geojson \
     assembled-state-VT.geojson \
     assembled-state-WI.geojson \
     assembled-state-WY.geojson

Nation.gpkg: all
	ogr2ogr -f GPKG -nln blocks_DE -nlt Point -overwrite $@ assembled-state-DE.geojson
	ogr2ogr -f GPKG -nln blocks_FL -nlt Point -overwrite $@ assembled-state-FL.geojson
	ogr2ogr -f GPKG -nln blocks_GA -nlt Point -overwrite $@ assembled-state-GA.geojson
	ogr2ogr -f GPKG -nln blocks_IL -nlt Point -overwrite $@ assembled-state-IL.geojson
	ogr2ogr -f GPKG -nln blocks_MA -nlt Point -overwrite $@ assembled-state-MA.geojson
	ogr2ogr -f GPKG -nln blocks_MD -nlt Point -overwrite $@ assembled-state-MD.geojson
	ogr2ogr -f GPKG -nln blocks_ME -nlt Point -overwrite $@ assembled-state-ME.geojson
	ogr2ogr -f GPKG -nln blocks_MI -nlt Point -overwrite $@ assembled-state-MI.geojson
	ogr2ogr -f GPKG -nln blocks_MT -nlt Point -overwrite $@ assembled-state-MT.geojson
	ogr2ogr -f GPKG -nln blocks_NC -nlt Point -overwrite $@ assembled-state-NC.geojson
	ogr2ogr -f GPKG -nln blocks_ND -nlt Point -overwrite $@ assembled-state-ND.geojson
	ogr2ogr -f GPKG -nln blocks_NH -nlt Point -overwrite $@ assembled-state-NH.geojson
	ogr2ogr -f GPKG -nln blocks_RI -nlt Point -overwrite $@ assembled-state-RI.geojson
	ogr2ogr -f GPKG -nln blocks_SD -nlt Point -overwrite $@ assembled-state-SD.geojson
	ogr2ogr -f GPKG -nln blocks_TN -nlt Point -overwrite $@ assembled-state-TN.geojson
	ogr2ogr -f GPKG -nln blocks_TX -nlt Point -overwrite $@ assembled-state-TX.geojson
	ogr2ogr -f GPKG -nln blocks_VT -nlt Point -overwrite $@ assembled-state-VT.geojson
	ogr2ogr -f GPKG -nln blocks_WI -nlt Point -overwrite $@ assembled-state-WI.geojson
	ogr2ogr -f GPKG -nln blocks_WY -nlt Point -overwrite $@ assembled-state-WY.geojson
	ogr2ogr -f GPKG -nln votes_DE -nlt MultiPolygon -overwrite $@ /vsizip/VEST/de_2016.zip
	ogr2ogr -f GPKG -nln votes_FL -nlt MultiPolygon -overwrite $@ /vsizip/VEST/fl_2016.zip
	ogr2ogr -f GPKG -nln votes_GA -nlt MultiPolygon -overwrite $@ /vsizip/VEST/ga_2016.zip
	ogr2ogr -f GPKG -nln votes_IL -nlt MultiPolygon -overwrite $@ /vsizip/VEST/il_2016.zip
	ogr2ogr -f GPKG -nln votes_MA -nlt MultiPolygon -overwrite $@ /vsizip/VEST/ma_2016.zip
	ogr2ogr -f GPKG -nln votes_MD -nlt MultiPolygon -overwrite $@ /vsizip/VEST/md_2016.zip
	ogr2ogr -f GPKG -nln votes_ME -nlt MultiPolygon -overwrite $@ /vsizip/VEST/me_2016.zip
	ogr2ogr -f GPKG -nln votes_MI -nlt MultiPolygon -overwrite $@ /vsizip/VEST/mi_2016.zip
	ogr2ogr -f GPKG -nln votes_MT -nlt MultiPolygon -overwrite $@ /vsizip/VEST/mt_2016.zip
	ogr2ogr -f GPKG -nln votes_NC -nlt MultiPolygon -overwrite $@ /vsizip/VEST/nc_2016.zip
	ogr2ogr -f GPKG -nln votes_ND -nlt MultiPolygon -overwrite $@ /vsizip/VEST/nd_2016.zip
	ogr2ogr -f GPKG -nln votes_NH -nlt MultiPolygon -overwrite $@ /vsizip/VEST/nh_2016.zip
	ogr2ogr -f GPKG -nln votes_RI -nlt MultiPolygon -overwrite $@ /vsizip/VEST/ri_2016.zip
	ogr2ogr -f GPKG -nln votes_SD -nlt MultiPolygon -overwrite $@ /vsizip/VEST/sd_2016.zip
	ogr2ogr -f GPKG -nln votes_TN -nlt MultiPolygon -overwrite $@ /vsizip/VEST/tn_2016.zip
	ogr2ogr -f GPKG -nln votes_TX -nlt MultiPolygon -overwrite $@ /vsizip/VEST/tx_2016.zip
	ogr2ogr -f GPKG -nln votes_VT -nlt MultiPolygon -overwrite $@ /vsizip/VEST/vt_2016.zip
	ogr2ogr -f GPKG -nln votes_WI -nlt MultiPolygon -overwrite $@ /vsizip/VEST/wi_2016.zip
	ogr2ogr -f GPKG -nln votes_WY -nlt MultiPolygon -overwrite $@ /vsizip/VEST/wy_2016.zip

assembled-state-DE.geojson: VEST/de_2016.zip Census/tl_2019_10_tabblock10.zip Census/tl_2019_10_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/de_2016.zip /vsizip/Census/tl_2019_10_tabblock10.zip /vsizip/Census/tl_2019_10_bg.zip

assembled-state-FL.geojson: VEST/fl_2016.zip Census/tl_2019_12_tabblock10.zip Census/tl_2019_12_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/fl_2016.zip /vsizip/Census/tl_2019_12_tabblock10.zip /vsizip/Census/tl_2019_12_bg.zip

assembled-state-GA.geojson: VEST/ga_2016.zip Census/tl_2019_13_tabblock10.zip Census/tl_2019_13_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/ga_2016.zip /vsizip/Census/tl_2019_13_tabblock10.zip /vsizip/Census/tl_2019_13_bg.zip

assembled-state-IL.geojson: VEST/il_2016.zip Census/tl_2019_17_tabblock10.zip Census/tl_2019_17_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/il_2016.zip /vsizip/Census/tl_2019_17_tabblock10.zip /vsizip/Census/tl_2019_17_bg.zip

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

assembled-state-MT.geojson: VEST/mt_2016.zip Census/tl_2019_30_tabblock10.zip Census/tl_2019_30_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/mt_2016.zip /vsizip/Census/tl_2019_30_tabblock10.zip /vsizip/Census/tl_2019_30_bg.zip

assembled-state-NC.geojson: VEST/nc_2016.zip Census/tl_2019_37_tabblock10.zip Census/tl_2019_37_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/nc_2016.zip /vsizip/Census/tl_2019_37_tabblock10.zip /vsizip/Census/tl_2019_37_bg.zip

assembled-state-ND.geojson: VEST/nd_2016.zip Census/tl_2019_38_tabblock10.zip Census/tl_2019_38_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/nd_2016.zip /vsizip/Census/tl_2019_38_tabblock10.zip /vsizip/Census/tl_2019_38_bg.zip

assembled-state-NH.geojson: VEST/nh_2016.zip Census/tl_2019_33_tabblock10.zip Census/tl_2019_33_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/nh_2016.zip /vsizip/Census/tl_2019_33_tabblock10.zip /vsizip/Census/tl_2019_33_bg.zip

assembled-state-RI.geojson: VEST/ri_2016.zip Census/tl_2019_44_tabblock10.zip Census/tl_2019_44_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/ri_2016.zip /vsizip/Census/tl_2019_44_tabblock10.zip /vsizip/Census/tl_2019_44_bg.zip

assembled-state-SD.geojson: VEST/sd_2016.zip Census/tl_2011_46_tabblock.zip Census/tl_2011_46_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/sd_2016.zip /vsizip/Census/tl_2011_46_tabblock.zip /vsizip/Census/tl_2011_46_bg.zip

assembled-state-TN.geojson: VEST/tn_2016.zip Census/tl_2019_47_tabblock10.zip Census/tl_2019_47_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/tn_2016.zip /vsizip/Census/tl_2019_47_tabblock10.zip /vsizip/Census/tl_2019_47_bg.zip

assembled-state-TX.geojson: VEST/tx_2016.zip Census/tl_2019_48_tabblock10.zip Census/tl_2019_48_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/tx_2016.zip /vsizip/Census/tl_2019_48_tabblock10.zip /vsizip/Census/tl_2019_48_bg.zip

assembled-state-VT.geojson: VEST/vt_2016.zip Census/tl_2019_50_tabblock10.zip Census/tl_2019_50_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/vt_2016.zip /vsizip/Census/tl_2019_50_tabblock10.zip /vsizip/Census/tl_2019_50_bg.zip

assembled-state-WI.geojson: VEST/wi_2016.zip Census/tl_2019_55_tabblock10.zip Census/tl_2019_55_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/wi_2016.zip /vsizip/Census/tl_2019_55_tabblock10.zip /vsizip/Census/tl_2019_55_bg.zip

assembled-state-WY.geojson: VEST/wy_2016.zip Census/tl_2019_56_tabblock10.zip Census/tl_2019_56_bg.zip
	./assemble-state.py $@ \
		/vsizip/VEST/wy_2016.zip /vsizip/Census/tl_2019_56_tabblock10.zip /vsizip/Census/tl_2019_56_bg.zip

Census/tl_2019_%_bg.zip:
	curl -L https://www2.census.gov/geo/tiger/TIGER2019/BG/tl_2019_$*_bg.zip -o $@

Census/tl_2019_%_tabblock10.zip:
	curl -L https://www2.census.gov/geo/tiger/TIGER2019/TABBLOCK/tl_2019_$*_tabblock10.zip -o $@

Census/tl_2011_%_bg.zip:
	curl -L https://www2.census.gov/geo/tiger/TIGER2011/BG/tl_2011_$*_bg.zip -o $@

Census/tl_2011_%_tabblock.zip:
	curl -L https://www2.census.gov/geo/tiger/TIGER2011/TABBLOCK/tl_2011_$*_tabblock.zip -o $@

.PHONY: all