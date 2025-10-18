#!/usr/bin/env python3
import argparse

import geopandas
import pandas

def main(rpvnearme_url, vtd_url):
    rpv_df1 = pandas.read_csv(rpvnearme_url, dtype={'GEOID': 'object'})
    rpv_df2 = rpv_df1[['GEOID'] + [c for c in rpv_df1.columns if '.pre_20_' in c]]
    print(rpv_df2)
    
    vtd_df = geopandas.read_file(vtd_url)[['GEOID20', 'geometry']]
    print(vtd_df)
    
    df = vtd_df.merge(rpv_df2, how='inner', left_on='GEOID20', right_on='GEOID')
    print(df)
    
    df.to_file('/tmp/df.gpkg')

parser = argparse.ArgumentParser()
parser.add_argument('rpvnearme_url')
parser.add_argument('vtd_url')

if __name__ == '__main__':
    args = parser.parse_args()
    exit(main(args.rpvnearme_url, args.vtd_url))
