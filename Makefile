# Skip assembled-state-SD.geojson due to county name changes
all: assembled-state-DE.geojson \
     assembled-state-ME.geojson \
     assembled-state-MA.geojson \
     assembled-state-MT.geojson \
     assembled-state-ND.geojson \
     assembled-state-NH.geojson \
     assembled-state-RI.geojson \
     assembled-state-VT.geojson \
     assembled-state-WY.geojson

assembled-state-DE.geojson: de_2016.zip tl_2019_10_tabblock10.zip tl_2019_10_bg.zip
	./assemble-state.py $@ \
		/vsizip/de_2016.zip /vsizip/tl_2019_10_tabblock10.zip /vsizip/tl_2019_10_bg.zip

assembled-state-ME.geojson: me_2016.zip tl_2019_23_tabblock10.zip tl_2019_23_bg.zip
	./assemble-state.py $@ \
		/vsizip/me_2016.zip /vsizip/tl_2019_23_tabblock10.zip /vsizip/tl_2019_23_bg.zip

assembled-state-MA.geojson: ma_2016.zip tl_2019_25_tabblock10.zip tl_2019_25_bg.zip
	./assemble-state.py $@ \
		/vsizip/ma_2016.zip /vsizip/tl_2019_25_tabblock10.zip /vsizip/tl_2019_25_bg.zip

assembled-state-MT.geojson: mt_2016.zip tl_2019_30_tabblock10.zip tl_2019_30_bg.zip
	./assemble-state.py $@ \
		/vsizip/mt_2016.zip /vsizip/tl_2019_30_tabblock10.zip /vsizip/tl_2019_30_bg.zip

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

assembled-state-VT.geojson: vt_2016.zip tl_2019_50_tabblock10.zip tl_2019_50_bg.zip
	./assemble-state.py $@ \
		/vsizip/vt_2016.zip /vsizip/tl_2019_50_tabblock10.zip /vsizip/tl_2019_50_bg.zip

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
