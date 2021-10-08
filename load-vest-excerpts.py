#!/usr/bin/env python3
import geopandas

assemble = __import__('assemble-state')

if __name__ == '__main__':
    df1a = geopandas.read_file('test/ga_2016.gpkg')
    print(df1a.sum())
    
    df1b = assemble.load_votes('test/ga_2016.gpkg')
    assert df1b['US President 2016 - REP'].sum() == 2660
    assert df1b['US President 2016 - DEM'].sum() == 4265
    assert df1b['US Senate 2016 - REP'].sum() == 3276
    assert df1b['US Senate 2016 - DEM'].sum() == 3433
    assert df1b['US President 2016 - Other'].sum() == 243
    assert df1b['US Senate 2016 - Other'].sum() == 221
