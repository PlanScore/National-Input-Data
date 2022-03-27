#!/usr/bin/env python3
import sys
import geopandas
import pandas

path_geojson, path_parquet = sys.argv[1:]

df_geojson = geopandas.read_file(path_geojson).to_crs(4326)
df_geojson['Point'] = df_geojson.geometry.astype(str)
del df_geojson['geometry']

df_parquet = pandas.DataFrame(df_geojson)

print(df_parquet)

df_parquet.to_parquet(path_parquet)
