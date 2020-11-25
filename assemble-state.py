#!/usr/bin/env python3
import geopandas
import shapely.geometry

def load_votes(votes_source):
    df = geopandas.read_file(votes_source).to_crs(epsg=4326)
    
    df2 = df.rename(columns={
        'G16PREDCLI': 'US President 2016 - DEM',
        'G16PRERTRU': 'US President 2016 - REP',
    })
    
    df3 = df2[[
        'STATEFP',
        'COUNTYFP',
        'NAME',
        'US President 2016 - DEM',
        'US President 2016 - REP',
        'geometry'
        ]]
    
    print(df3)
    
    return df3

def load_blocks(blocks_source):
    df = geopandas.read_file(blocks_source).to_crs(epsg=4326)
    
    df2 = df.rename(columns={
        'GEOID10': 'GEOID',
        'NAME10': 'NAME',
        'ALAND10': 'ALAND',
        'AWATER10': 'AWATER',
        'INTPTLAT10': 'INTPTLAT',
        'INTPTLON10': 'INTPTLON',
        'STATEFP10': 'STATEFP',
        'COUNTYFP10': 'COUNTYFP',
        'TRACTCE10': 'TRACTCE',
        'BLOCKCE10': 'BLOCKCE',
    })
    
    # Replace upstream polygon geometry with internal points
    df2.geometry = [
        shapely.geometry.Point(float(row['INTPTLON']), float(row['INTPTLAT']))
        for (index, row) in df2.iterrows()
    ]
    
    df3 = df2[[
        'STATEFP',
        'COUNTYFP',
        'TRACTCE',
        'BLOCKCE',
        'NAME',
        'GEOID',
        'ALAND',
        'AWATER',
        'geometry',
        ]]
    
    print(df3)
    
    return df3

def load_blockgroups(bgs_source):
    df = geopandas.read_file(bgs_source)
    
    df2 = df[[
        'GEOID',
        'NAMELSAD',
        'ALAND',
        'AWATER',
        'STATEFP',
        'COUNTYFP',
        'TRACTCE',
        'BLKGRPCE',
        ]]
    
    print(df2)
    
    return df2

def main(votes_source, blocks_source, bgs_source):
    df_bgs = load_blockgroups(bgs_source)
    df_blocks = load_blocks(blocks_source)
    df_votes = load_votes(votes_source)

if __name__ == '__main__':
    exit(main(
        '/vsizip/ri_2016.zip',
        '/vsizip/tl_2019_44_tabblock10.zip',
        '/vsizip/tl_2019_44_bg.zip',
    ))
