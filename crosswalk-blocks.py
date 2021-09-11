#!/usr/bin/env python3
import io
import sys
import csv
import zipfile
import geopandas

assemble = __import__('assemble-state')

if __name__ == '__main__':
    blocks_path, precincts_source, output_path = sys.argv[1:]

    blocks = assemble.load_blocks(blocks_path)
    precincts = geopandas.read_file(precincts_source)
    
    joined1 = geopandas.sjoin(blocks, precincts.to_crs(blocks.crs), op='within', lsuffix='block', rsuffix='precinct')
    
    print(joined1.columns)
    
    joined2 = joined1[[
        column for column in joined1.columns
        if column not in ('geometry',)
        and not column.startswith('G20')
    ]]
    
    print(joined2)
    
    joined2.to_csv(output_path)

