#!/usr/bin/env python3
import geopandas

assemble = __import__('assemble-state')

if __name__ == '__main__':
    df1a = geopandas.read_file('test/ga_2016.gpkg')
    df1b = assemble.load_votes('test/ga_2016.gpkg')
    assert df1b['US President 2016 - REP'].sum() == 2660
    assert df1b['US President 2016 - DEM'].sum() == 4265
    assert df1b['US Senate 2016 - REP'].sum() == 3276
    assert df1b['US Senate 2016 - DEM'].sum() == 3433
    assert df1b['US President 2016 - Other'].sum() == 243
    assert df1b['US Senate 2016 - Other'].sum() == 221

    df2a = geopandas.read_file('test/ga_2020.gpkg')
    df2b = assemble.load_votes('test/ga_2020.gpkg')
    assert df2b['US President 2020 - REP'].sum() == 17359
    assert df2b['US President 2020 - DEM'].sum() == 5468
    assert df2b['US Senate 2020 - REP'].sum() == 17223
    assert df2b['US Senate 2020 - DEM'].sum() == 5216
    assert df2b['US President 2020 - Other'].sum() == 325
    assert df2b['US Senate 2020 - Other'].sum() == 531

    df3a = geopandas.read_file('test/ca_2020.gpkg')
    df3b = assemble.load_votes('test/ca_2020.gpkg')
    assert df3b['US President 2020 - REP'].sum() == 496
    assert df3b['US President 2020 - DEM'].sum() == 4869
    assert df3b['US President 2020 - Other'].sum() == 45 + 42 + 9 + 29

    df4a = geopandas.read_file('test/la_2016.gpkg')
    df4b = assemble.load_votes('test/la_2016.gpkg')
    assert df4b['US President 2016 - REP'].sum() == 4003
    assert df4b['US President 2016 - DEM'].sum() == 492
    assert df4b['US Senate 2016 - REP'].sum() == 1816
    assert df4b['US Senate 2016 - DEM'].sum() == 303
    assert df4b['US President 2016 - Other'].sum() == 46 + 17 + 11 + 11 + 13
    assert df4b['US Senate 2016 - Other'].sum() == 0

    df5a = geopandas.read_file('test/la_2020.gpkg')
    df5b = assemble.load_votes('test/la_2020.gpkg')
    assert df5b['US President 2020 - REP'].sum() == 5936
    assert df5b['US President 2020 - DEM'].sum() == 1453
    assert df5b['US Senate 2020 - REP'].sum() == 5654 + 143
    assert df5b['US Senate 2020 - DEM'].sum() == 406 + 84 + 587 + 90 + 16
    assert df5b['US President 2020 - Other'].sum() == 64 + 17 + 36
    assert df5b['US Senate 2020 - Other'].sum() == 19 + 33 + 68 + 84 + 20 + 14 + 22 + 23

    df6a = geopandas.read_file('test/ar_2020.gpkg')
    print(df6a.sum())
    df6b = assemble.load_votes('test/ar_2020.gpkg')
    assert df6b['US President 2020 - REP'].sum() == 2034
    assert df6b['US President 2020 - DEM'].sum() == 536
    assert df6b['US Senate 2020 - REP'].sum() == 2062
    assert df6b['US Senate 2020 - DEM'].sum() == 544
    assert df6b['US President 2020 - Other'].sum() == 26 + 4 + 9 + 3 + 4 + 0 + 14 + 9 + 6 + 2 + 1
    assert df6b['US Senate 2020 - Other'].sum() == 0
