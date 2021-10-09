#!/usr/bin/env python3
import io
import sys
import csv
import zipfile
import geopandas

assemble = __import__('assemble-state')

if __name__ == '__main__':
    df_blocks1 = geopandas.read_file('test/null-island-blocks.geojson')
    df_votes1 = geopandas.read_file('test/null-island-precincts-normal.geojson')
    
    assemble.print_df(df_blocks1, 'df_blocks1')
    assemble.print_df(df_votes1, 'df_votes1')
    
    joined1 = assemble.join_blocks_votes(
        df_blocks1.to_crs(5070),
        df_votes1.to_crs(5070),
        'US President 2020 - DEM',
        'US President 2020 - REP',
    ).to_crs(4326)

    assemble.print_df(joined1, 'joined1')
    geocodes = sorted(list(df_blocks1.GEOCODE))
    geocodes1 = sorted(list(joined1.GEOCODE))
    
    assert geocodes1 == geocodes, f"Should not have {', '.join(geocodes1)} GEOCODE column"
    assert round(joined1['US President 2020 - REP'].sum()) == 160, \
        f"Should not have {joined1['US President 2020 - REP'].sum()} republican votes"
    assert round(joined1['US President 2020 - DEM'].sum()) == 171, \
        f"Should not have {joined1['US President 2020 - DEM'].sum()} democratic votes"
    assert round(joined1['P0010001'].sum()) == 63, \
        f"Should not have {joined1['P0010001'].sum()} total population"

    df_votes2 = geopandas.read_file('test/null-island-precincts-weird.geojson')
    
    assemble.print_df(df_votes2, 'df_votes2')
    
    joined2 = assemble.join_blocks_votes(
        df_blocks1.to_crs(5070),
        df_votes2.to_crs(5070),
        'US President 2020 - DEM',
        'US President 2020 - REP',
    ).to_crs(4326)

    assemble.print_df(joined2, 'joined2')
    joined2b = joined2.merge(
        df_votes2[['Name']],
        how='left',
        left_on=joined2.index_votes2020,
        right_on=df_votes2.index,
        suffixes=('_block', '_precinct'),
    )
    assemble.print_df(joined2b, 'joined2b')
    print(joined2b.columns)
    joined2b.to_csv('/tmp/joined-NULL.csv')
    geocodes2 = sorted(list(joined2.GEOCODE))
    
    assert geocodes2 == geocodes, f"Should not have {', '.join(geocodes2)} GEOCODE column"
    assert round(joined2['US President 2020 - REP'].sum()) == 160, \
        f"Should not have {joined2['US President 2020 - REP'].sum()} republican votes"
    assert round(joined2['US President 2020 - DEM'].sum()) == 171, \
        f"Should not have {joined2['US President 2020 - DEM'].sum()} democratic votes"
    assert round(joined2['P0010001'].sum()) == 63, \
        f"Should not have {joined2['P0010001'].sum()} total population"
    
    exit()
    print('/' * 80)
    
    df_blocks2 = assemble.load_blocks('Census/or2020.pl.zip')
    df_votes3 = geopandas.read_file('/vsizip/VEST/or_2020.zip').to_crs(df_blocks2.crs)
    
    assemble.print_df(df_blocks2, 'df_blocks2')
    assemble.print_df(df_votes3, 'df_votes3')

    joined3 = assemble.join_blocks_votes(
        df_blocks2.to_crs(5070),
        df_votes3.to_crs(5070),
        'G20PREDBID',
        'G20PRERTRU',
    ).to_crs(4326)

    assemble.print_df(joined3, 'joined3')
    joined3b = joined3.merge(
        df_votes3[['STATE', 'COUNTY', 'PRECINCT', 'NAME']],
        how='left',
        left_on=joined3.index_votes2020,
        right_on=df_votes3.index,
        suffixes=('_block', '_precinct'),
    )
    assemble.print_df(joined3b, 'joined3b')
    print(joined3b.columns)
    joined3b.to_csv('/tmp/joined-OR.csv')
