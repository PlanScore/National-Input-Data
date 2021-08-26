#!/usr/bin/env python3
import io
import csv
import zipfile
import geopandas

assemble = __import__('assemble-state')

if __name__ == '__main__':
    blocks = assemble.load_blocks('Census/ri2020.pl.zip')
    precincts = geopandas.read_file('/vsizip/VEST/ri_2020.zip').to_crs(epsg=4326)
    
    joined1 = geopandas.sjoin(blocks, precincts.to_crs(blocks.crs), op='within', lsuffix='block', rsuffix='precinct')
    
    print(joined1.columns)
    
    joined2 = joined1[[
        column for column in joined1.columns
        if column not in ('geometry',)
    ]]
    
    print(joined2)
    
    joined2.to_csv('/tmp/ri2020-blocks-votes.csv')

