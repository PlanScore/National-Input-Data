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

all: assembled-state-DE.geojson \
     assembled-state-FL.geojson \
     assembled-state-GA.geojson \
     assembled-state-IL.geojson \
     assembled-state-MD.geojson \
     assembled-state-ME.geojson \
     assembled-state-MA.geojson \
     assembled-state-MI.geojson \
     assembled-state-MT.geojson \
     assembled-state-ND.geojson \
     assembled-state-NC.geojson \
     assembled-state-NH.geojson \
     assembled-state-RI.geojson \
     assembled-state-SD.geojson \
     assembled-state-TN.geojson \
     assembled-state-TX.geojson \
     assembled-state-VT.geojson \
     assembled-state-WI.geojson \
     assembled-state-WY.geojson

assembled-state-DE.geojson: de_2016.zip tl_2019_10_tabblock10.zip tl_2019_10_bg.zip
	./assemble-state.py $@ \
		/vsizip/de_2016.zip /vsizip/tl_2019_10_tabblock10.zip /vsizip/tl_2019_10_bg.zip

assembled-state-FL.geojson: fl_2016.zip tl_2019_12_tabblock10.zip tl_2019_12_bg.zip
	./assemble-state.py $@ \
		/vsizip/fl_2016.zip /vsizip/tl_2019_12_tabblock10.zip /vsizip/tl_2019_12_bg.zip

assembled-state-GA.geojson: ga_2016.zip tl_2019_13_tabblock10.zip tl_2019_13_bg.zip
	./assemble-state.py $@ \
		/vsizip/ga_2016.zip /vsizip/tl_2019_13_tabblock10.zip /vsizip/tl_2019_13_bg.zip

assembled-state-IL.geojson: il_2016.zip tl_2019_17_tabblock10.zip tl_2019_17_bg.zip
	./assemble-state.py $@ \
		/vsizip/il_2016.zip /vsizip/tl_2019_17_tabblock10.zip /vsizip/tl_2019_17_bg.zip

assembled-state-MD.geojson: md_2016.zip tl_2019_24_tabblock10.zip tl_2019_24_bg.zip
	./assemble-state.py $@ \
		/vsizip/md_2016.zip /vsizip/tl_2019_24_tabblock10.zip /vsizip/tl_2019_24_bg.zip

assembled-state-ME.geojson: me_2016.zip tl_2019_23_tabblock10.zip tl_2019_23_bg.zip
	./assemble-state.py $@ \
		/vsizip/me_2016.zip /vsizip/tl_2019_23_tabblock10.zip /vsizip/tl_2019_23_bg.zip

assembled-state-MA.geojson: ma_2016.zip tl_2019_25_tabblock10.zip tl_2019_25_bg.zip
	./assemble-state.py $@ \
		/vsizip/ma_2016.zip /vsizip/tl_2019_25_tabblock10.zip /vsizip/tl_2019_25_bg.zip

assembled-state-MI.geojson: mi_2016.zip tl_2019_26_tabblock10.zip tl_2019_26_bg.zip
	./assemble-state.py $@ \
		/vsizip/mi_2016.zip /vsizip/tl_2019_26_tabblock10.zip /vsizip/tl_2019_26_bg.zip

assembled-state-MT.geojson: mt_2016.zip tl_2019_30_tabblock10.zip tl_2019_30_bg.zip
	./assemble-state.py $@ \
		/vsizip/mt_2016.zip /vsizip/tl_2019_30_tabblock10.zip /vsizip/tl_2019_30_bg.zip

assembled-state-NC.geojson: nc_2016.zip tl_2019_37_tabblock10.zip tl_2019_37_bg.zip
	./assemble-state.py $@ \
		/vsizip/nc_2016.zip /vsizip/tl_2019_37_tabblock10.zip /vsizip/tl_2019_37_bg.zip

assembled-state-ND.geojson: nd_2016.zip tl_2019_38_tabblock10.zip tl_2019_38_bg.zip
	./assemble-state.py $@ \
		/vsizip/nd_2016.zip /vsizip/tl_2019_38_tabblock10.zip /vsizip/tl_2019_38_bg.zip

assembled-state-NH.geojson: nh_2016.zip tl_2019_33_tabblock10.zip tl_2019_33_bg.zip
	./assemble-state.py $@ \
		/vsizip/nh_2016.zip /vsizip/tl_2019_33_tabblock10.zip /vsizip/tl_2019_33_bg.zip

assembled-state-RI.geojson: ri_2016.zip tl_2019_44_tabblock10.zip tl_2019_44_bg.zip
	./assemble-state.py $@ \
		/vsizip/ri_2016.zip /vsizip/tl_2019_44_tabblock10.zip /vsizip/tl_2019_44_bg.zip

assembled-state-SD.geojson: sd_2016.zip tl_2011_46_tabblock.zip tl_2011_46_bg.zip
	./assemble-state.py $@ \
		/vsizip/sd_2016.zip /vsizip/tl_2011_46_tabblock.zip /vsizip/tl_2011_46_bg.zip

assembled-state-TN.geojson: tn_2016.zip tl_2019_47_tabblock10.zip tl_2019_47_bg.zip
	./assemble-state.py $@ \
		/vsizip/tn_2016.zip /vsizip/tl_2019_47_tabblock10.zip /vsizip/tl_2019_47_bg.zip

assembled-state-TX.geojson: tx_2016.zip tl_2019_48_tabblock10.zip tl_2019_48_bg.zip
	./assemble-state.py $@ \
		/vsizip/tx_2016.zip /vsizip/tl_2019_48_tabblock10.zip /vsizip/tl_2019_48_bg.zip

assembled-state-VT.geojson: vt_2016.zip tl_2019_50_tabblock10.zip tl_2019_50_bg.zip
	./assemble-state.py $@ \
		/vsizip/vt_2016.zip /vsizip/tl_2019_50_tabblock10.zip /vsizip/tl_2019_50_bg.zip

assembled-state-WI.geojson: wi_2016.zip tl_2019_55_tabblock10.zip tl_2019_55_bg.zip
	./assemble-state.py $@ \
		/vsizip/wi_2016.zip /vsizip/tl_2019_55_tabblock10.zip /vsizip/tl_2019_55_bg.zip

assembled-state-WY.geojson: wy_2016.zip tl_2019_56_tabblock10.zip tl_2019_56_bg.zip
	./assemble-state.py $@ \
		/vsizip/wy_2016.zip /vsizip/tl_2019_56_tabblock10.zip /vsizip/tl_2019_56_bg.zip

tl_2019_%_bg.zip:
	curl -OL https://www2.census.gov/geo/tiger/TIGER2019/BG/tl_2019_$*_bg.zip

tl_2019_%_tabblock10.zip:
	curl -OL https://www2.census.gov/geo/tiger/TIGER2019/TABBLOCK/tl_2019_$*_tabblock10.zip

tl_2011_%_bg.zip:
	curl -OL https://www2.census.gov/geo/tiger/TIGER2011/BG/tl_2011_$*_bg.zip

tl_2011_%_tabblock.zip:
	curl -OL https://www2.census.gov/geo/tiger/TIGER2011/TABBLOCK/tl_2011_$*_tabblock.zip
