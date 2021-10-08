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

    df2a = geopandas.read_file('test/ga_2020.gpkg')
    print(df2a.sum())
    
    df2b = assemble.load_votes('test/ga_2020.gpkg')
    assert df2b['US President 2020 - REP'].sum() == 17359
    assert df2b['US President 2020 - DEM'].sum() == 5468
    assert df2b['US Senate 2020 - REP'].sum() == 15556 + 15461
    assert df2b['US Senate 2020 - DEM'].sum() == 4863 + 4953
    assert df2b['US President 2020 - Other'].sum() == 325
    assert df2b['US Senate 2020 - Other'].sum() == 0

    df3a = geopandas.read_file('test/ca_2020.gpkg')
    print(df3a.sum())
    
    df3b = assemble.load_votes('test/ca_2020.gpkg')
    assert df3b['US President 2020 - REP'].sum() == 496
    assert df3b['US President 2020 - DEM'].sum() == 4869
    assert df3b['US President 2020 - Other'].sum() == 45 + 42 + 9 + 29

    df4a = geopandas.read_file('test/la_2016.gpkg')
    print(df4a.sum())
    
    df4b = assemble.load_votes('test/la_2016.gpkg')
    assert df4b['US President 2016 - REP'].sum() == 4003
    assert df4b['US President 2016 - DEM'].sum() == 492
    assert df4b['US Senate 2016 - REP'].sum() == 1816
    assert df4b['US Senate 2016 - DEM'].sum() == 303
    assert df4b['US President 2016 - Other'].sum() == 46 + 17 + 11 + 11 + 13
    assert df4b['US Senate 2016 - Other'].sum() == 0
