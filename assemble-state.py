#!/usr/bin/env python3
import urllib.parse
import collections
import hashlib
import pickle
import os
import requests
import pandas
import geopandas
import shapely.geometry

ACS_VARIABLES = [
    'B01001_001E', 'B02009_001E', 'B03002_012E', 'B15003_017E',
    'B15003_018E', 'B19013_001E', 'B29001_001E', 'B01001_001M',
    'B02009_001M', 'B03002_012M', 'B15003_017M', 'B15003_018M',
    'B19013_001M', 'B29001_001M'
]

def memoize(func):
    def new_func(*args, **kwargs):
        filename = 'memoized/{}-{}.pickle'.format(
            func.__name__,
            hashlib.md5(pickle.dumps((args, kwargs))).hexdigest()
        )
        
        if os.path.exists(filename):
            print(f'Found memoized data in {filename}')
            with open(filename, 'rb') as file:
                return pickle.load(file)
        
        response = func(*args, **kwargs)
        
        with open(filename, 'wb') as file:
            print(f'Wrote memoized data to {filename}')
            pickle.dump(response, file)
        
        return response
    
    return new_func

@memoize
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

@memoize
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
    
    return get_sf1(df3)

@memoize
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
    
    return get_acs(df2)

@memoize
def get_state_counties(state_fips):
    print('state_fips:', state_fips)
    
    query = urllib.parse.urlencode({
        'get': 'NAME', # 'P001001,NAME,GEO_ID',
        'for': 'county:*',
        'in': f'state:{state_fips}'
    })
    
    print(query)
    
    got = requests.get(f'https://api.census.gov/data/2010/dec/sf1?{query}')
    head, tail = got.json()[0], got.json()[1:]
    rows = [collections.OrderedDict(zip(head, row)) for row in tail]
    
    return [row['county'] for row in rows]

@memoize
def get_county_acs(state_fips, county_fips):

    query = urllib.parse.urlencode([
        ('get', ','.join(ACS_VARIABLES + ['NAME'])),
        ('for', 'block group:*'),
        ('in', f'state:{state_fips}'),
        ('in', f'county:{county_fips}'),
        ('in', 'tract:*'),
    ])
    
    print(query)
    
    got = requests.get(f'https://api.census.gov/data/2018/acs/acs5?{query}')
    head, tail = got.json()[0], got.json()[1:]
    data = {
        key: [row[i] for row in tail]
        for (i, key) in enumerate(head)
    }
    
    df_acs = pandas.DataFrame(data)
    
    for variable in ACS_VARIABLES:
        df_acs[variable] = df_acs[variable].astype(int)
    
    return df_acs

def get_acs(df_bgs):

    (state_fips, ) = df_bgs.STATEFP.unique()
    
    print('state_fips:', state_fips)
    
    query = urllib.parse.urlencode({
        'get': 'NAME', # 'P001001,NAME,GEO_ID',
        'for': 'county:*',
        'in': f'state:{state_fips}'
    })
    
    print(query)
    
    got = requests.get(f'https://api.census.gov/data/2010/dec/sf1?{query}')
    head, tail = got.json()[0], got.json()[1:]
    rows = [collections.OrderedDict(zip(head, row)) for row in tail]
    
    df_acs = pandas.concat([
        get_county_acs(state_fips, row['county'])
        for row in rows
    ])
    
    print(df_acs)
    
    df_bgs2 = df_bgs.merge(df_acs, how='left',
        left_on=('STATEFP', 'COUNTYFP', 'TRACTCE', 'BLKGRPCE'),
        right_on=('state', 'county', 'tract', 'block group'),
        )
    
    df_bgs3 = df_bgs2[[
        'GEOID',
        'NAMELSAD',
        'ALAND',
        'AWATER',
        'STATEFP',
        'COUNTYFP',
        'TRACTCE',
        'BLKGRPCE',
        ] + ACS_VARIABLES]
    
    print(df_bgs3)
    
    return df_bgs3

@memoize
def get_county_sf1(state_fips, county_fips):

    query = urllib.parse.urlencode([
        ('get', ','.join(['P001001', 'NAME'])),
        ('for', 'block:*'),
        ('in', f'state:{state_fips}'),
        ('in', f'county:{county_fips}'),
        ('in', 'tract:*'),
    ])
    
    print(query)
    
    got = requests.get(f'https://api.census.gov/data/2010/dec/sf1?{query}')
    head, tail = got.json()[0], got.json()[1:]
    data = {
        key: [row[i] for row in tail]
        for (i, key) in enumerate(head)
    }
    
    df_sf1 = pandas.DataFrame(data)
    df_sf1.P001001 = df_sf1.P001001.astype(int)
    
    return df_sf1

def get_sf1(df_blocks):

    (state_fips, ) = df_blocks.STATEFP.unique()
    
    print('state_fips:', state_fips)
    
    counties = get_state_counties(state_fips)
    
    df_sf1 = pandas.concat([
        get_county_sf1(state_fips, county_fips)
        for county_fips in counties
    ])
    
    print(df_blocks)
    print(df_sf1)
    
    df_blocks2 = df_blocks.merge(df_sf1, how='left',
        left_on=('STATEFP', 'COUNTYFP', 'TRACTCE', 'BLOCKCE'),
        right_on=('state', 'county', 'tract', 'block'),
        )
    
    df_blocks3 = df_blocks2[[
        'GEOID',
        'ALAND',
        'AWATER',
        'STATEFP',
        'COUNTYFP',
        'TRACTCE',
        'BLOCKCE',
        'P001001',
        ]]
    
    print(df_blocks3)
    
    return df_blocks3

def join_blocks_blockgroups(df_blocks, df_bgs):
    
    input_population = df_bgs['B01001_001E'].sum() \
                     + df_bgs['B01001_001E'].sum()
    
    # Note shorter block group GEOID for later matching
    df_blocks['GEOID_block'] = df_blocks.GEOID.str.slice(0, 12)
    
    # Sum ALAND for each block group
    df_blocks2 = df_blocks[['GEOID_block', 'ALAND']]\
        .groupby('GEOID_block', as_index=False).ALAND.sum()\
        .rename(columns={'ALAND': 'ALAND_bg'})
    
    # Join survey data to any block with matching GEOID prefix
    df_blocks3 = df_blocks2.merge(df_blocks, on='GEOID_block', how='left')
    
    # Join complete blocks with survey data to block-group-summed ALAND
    df_blocks4 = df_blocks3.merge(df_bgs[ACS_VARIABLES + ['GEOID']],
        left_on='GEOID_block', right_on='GEOID', how='left', suffixes=('', '_y'))
    
    # Scale survey data by land area block/group fraction
    for variable in ACS_VARIABLES:
        df_blocks4[variable] *= (df_blocks4.ALAND / df_blocks4.ALAND_bg)
    
    # Select just a few columns
    df_blocks5 = df_blocks4[[
        'STATEFP', 'COUNTYFP', 'TRACTCE', 'BLOCKCE',
        'NAME', 'GEOID', 'ALAND', 'AWATER',
        'geometry',
        ] + ACS_VARIABLES]
    
    output_population = df_blocks5['B01001_001E'].sum() \
                      + df_blocks5['B01001_001E'].sum()
    
    assert round(input_population / output_population, 7) == 1, \
        '{} population unnaccounted for'.format(abs(output_population - input_population))
    
    return df_blocks5

def join_blocks_votes(df_blocks, df_votes):

    input_votes = df_votes['US President 2016 - DEM'].sum() \
                + df_votes['US President 2016 - REP'].sum()

    # Join precinct votes to any block spatially contained within
    df_blocks2 = geopandas.sjoin(df_blocks,
        df_votes[['geometry', 'US President 2016 - DEM', 'US President 2016 - REP']],
        op='within', how='left', rsuffix='votes')
    
    # Sum ALAND for each voting precinct
    df_blocks3 = df_blocks2\
        .groupby('index_votes', as_index=False).ALAND.sum()\
        .rename(columns={'ALAND': 'ALAND_precinct'})
    
    # Join complete blocks with votes to precinct-summed ALAND
    df_blocks4 = df_blocks3.merge(df_blocks2, on='index_votes', how='left')
    
    # Scale presidential votes by land area block/precinct fraction
    df_blocks4['US President 2016 - DEM'] *= (df_blocks4.ALAND / df_blocks4.ALAND_precinct)
    df_blocks4['US President 2016 - REP'] *= (df_blocks4.ALAND / df_blocks4.ALAND_precinct)
    
    # Select just a few columns
    df_blocks5 = df_blocks4[[
        'STATEFP', 'COUNTYFP', 'TRACTCE',
        'BLOCKCE', 'NAME', 'GEOID', 'ALAND', 'AWATER',
        'US President 2016 - DEM', 'US President 2016 - REP',
        'geometry',
        ]]
    
    output_votes = df_blocks5['US President 2016 - DEM'].sum() \
                 + df_blocks5['US President 2016 - REP'].sum()
    
    assert round(input_votes / output_votes, 7) == 1, \
        '{} votes unnaccounted for'.format(abs(output_votes - input_votes))

    return df_blocks5

def main(votes_source, blocks_source, bgs_source):
    df_bgs = load_blockgroups(bgs_source)
    df_blocks = load_blocks(blocks_source)
    df_votes = load_votes(votes_source)
    
    print(df_bgs)
    print(df_blocks)
    
    df_blocks2 = join_blocks_blockgroups(df_blocks, df_bgs)
    
    print(df_blocks2)
    return
    
    df_blocks3 = join_blocks_votes(df_blocks2, df_votes)
    
    print(df_blocks3)

if __name__ == '__main__':
    exit(main(
        '/vsizip/ri_2016.zip',
        '/vsizip/tl_2019_44_tabblock10.zip',
        '/vsizip/tl_2019_44_bg.zip',
    ))
