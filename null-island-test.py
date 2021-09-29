#!/usr/bin/env python3
import io
import sys
import csv
import zipfile
import geopandas

assemble = __import__('assemble-state')

if __name__ == '__main__':
    df_blocks = geopandas.read_file('null-island-blocks.geojson')
    df_votes1 = geopandas.read_file('null-island-precincts-normal.geojson')
    
    assemble.print_df(df_blocks, 'df_blocks')
    assemble.print_df(df_votes1, 'df_votes1')
    
    joined1 = assemble.join_blocks_votes(
        df_blocks, df_votes1, 'US President 2020 - DEM', 'US President 2020 - REP',
    )

    assemble.print_df(joined1, 'joined1')
    geocodes1 = sorted(list(joined1.GEOCODE))
    
    assert set(geocodes1) == {'0200', '0300', '0500', '0800', '1000', '1200'}, \
        f"Should not have {', '.join(geocodes1)} GEOCODE column"
    assert joined1['US President 2020 - REP'].sum() == 160, \
        f"Should not have {joined1['US President 2020 - REP'].sum()} republican votes"
    assert joined1['US President 2020 - DEM'].sum() == 171, \
        f"Should not have {joined1['US President 2020 - DEM'].sum()} democratic votes"
    assert joined1['P0010001'].sum() == 63, \
        f"Should not have {joined1['P0010001'].sum()} total population"

    df_votes2 = geopandas.read_file('null-island-precincts-weird.geojson')
    
    assemble.print_df(df_votes2, 'df_votes2')
    
    joined2 = assemble.join_blocks_votes(
        df_blocks, df_votes2, 'US President 2020 - DEM', 'US President 2020 - REP',
    )

    assemble.print_df(joined2, 'joined2')
    geocodes2 = sorted(list(joined2.GEOCODE))
    
    assert set(geocodes2) == {'0200', '0300', '0500', '0800', '1000', '1200'}, \
        f"Should not have {', '.join(geocodes2)} GEOCODE column"
    assert joined2['US President 2020 - REP'].sum() == 160, \
        f"Should not have {joined2['US President 2020 - REP'].sum()} republican votes"
    assert joined2['US President 2020 - DEM'].sum() == 171, \
        f"Should not have {joined2['US President 2020 - DEM'].sum()} democratic votes"
    assert joined2['P0010001'].sum() == 63, \
        f"Should not have {joined2['P0010001'].sum()} total population"
