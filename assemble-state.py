#!/usr/bin/env python3
import sys
import urllib.parse
import collections
import hashlib
import pickle
import inspect
import os
import requests
import pandas
import geopandas
import shapely.geometry

BLOCK_FIELDS = [
    'GEOID', 'STATEFP', 'COUNTYFP', 'TRACTCE', 'BLOCKCE', #'NAME',
    'ALAND', 'AWATER', 'P001001', 'geometry'
]

ACS_VARIABLES = [
    'B01001_001E', 'B02009_001E', 'B03002_012E', 'B15003_017E',
    'B15003_018E', 'B19013_001E', 'B29001_001E', 'B01001_001M',
    'B02009_001M', 'B03002_012M', 'B15003_017M', 'B15003_018M',
    'B19013_001M', 'B29001_001M'
]

VOTES_DEM = 'US President 2016 - DEM'
VOTES_REP = 'US President 2016 - REP'

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

def move_votes(df, good_index, bad_index):
    print('Move votes from', bad_index, 'to', good_index)

    dem_votes = df.columns.get_loc(VOTES_DEM)
    rep_votes = df.columns.get_loc(VOTES_REP)

    good_row = df.index.get_loc(good_index)
    bad_row = df.index.get_loc(bad_index)

    df.iat[good_row, dem_votes] += df.iat[bad_row, dem_votes]
    df.iat[good_row, rep_votes] += df.iat[bad_row, rep_votes]
    df.iat[bad_row, dem_votes] -= df.iat[bad_row, dem_votes]
    df.iat[bad_row, rep_votes] -= df.iat[bad_row, rep_votes]

@memoize
def load_votes(votes_source):
    df = geopandas.read_file(votes_source).to_crs(epsg=4326)
    
    df2 = df.rename(columns={
        'G16PREDCLI': VOTES_DEM,
        'G16PRERTRU': VOTES_REP,
        'G16PREDCli': VOTES_DEM,
        'G16PRERTru': VOTES_REP,
    })
    
    assert VOTES_DEM in df2.columns
    assert VOTES_REP in df2.columns
    
    df3 = df2[[
        #'STATEFP',
        #'COUNTYFP',
        #'NAME',
        VOTES_DEM,
        VOTES_REP,
        'geometry'
        ]]
    
    print(df3)
    
    return df3

@memoize
def load_blocks(blocks_source):
    df = geopandas.read_file(blocks_source).to_crs(epsg=4326)
    
    print('df.columns:', df.columns)
    
    if 'GEOID10' not in df.columns:
        # Older block files include certain field names without the "10" suffix
        df2 = df.rename(columns={
            'STATEFP': 'STATEFP_bad',
            'COUNTYFP': 'COUNTYFP_bad',
            #'GEOID10': 'GEOID',
            #'NAME10': 'NAME',
            #'ALAND10': 'ALAND',
            #'AWATER10': 'AWATER',
            #'INTPTLAT10': 'INTPTLAT',
            #'INTPTLON10': 'INTPTLON',
            'STATEFP10': 'STATEFP',
            'COUNTYFP10': 'COUNTYFP',
            'TRACTCE10': 'TRACTCE',
            'BLOCKCE10': 'BLOCKCE',
        })
    else:
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
    
    print('df2.columns:', df2.columns)
    
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
def get_state_counties(state_fips, api_path):
    print('state_fips:', state_fips)
    
    query = urllib.parse.urlencode({
        'get': 'NAME', # 'P001001,NAME,GEO_ID',
        'for': 'county:*',
        'in': f'state:{state_fips}'
    })
    
    print(f'https://api.census.gov/data/{api_path}?{query}')
    
    got = requests.get(f'https://api.census.gov/data/{api_path}?{query}')
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
    
    print(f'https://api.census.gov/data/2018/acs/acs5?{query}')
    
    got = requests.get(f'https://api.census.gov/data/2018/acs/acs5?{query}')
    head, tail = got.json()[0], got.json()[1:]
    data = {
        key: [row[i] for row in tail]
        for (i, key) in enumerate(head)
    }
    
    df_acs = pandas.DataFrame(data)
    
    if (state_fips, county_fips) == ('46', '102'):
        # In 2015, Shannon County, SD (FIPS 46113) was renamed to
        # Oglala Lakota County (FIPS 46101). We use the old FIPS code
        # to match cleanly with 2010 census blocks.
        df_acs.county = ['113' for _ in range(len(df_acs))]
        print(df_acs.columns)
        #raise NotImplementedError()
    
    for variable in ACS_VARIABLES:
        df_acs[variable] = df_acs[variable].astype(int)
    
    return df_acs

def get_acs(df_bgs):

    (state_fips, ) = df_bgs.STATEFP.unique()
    
    print('state_fips:', state_fips)
    
    counties = get_state_counties(state_fips, '2018/acs/acs5')
    
    df_acs = pandas.concat([
        get_county_acs(state_fips, county_fips)
        for county_fips in sorted(counties)
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
    
    print(f'https://api.census.gov/data/2010/dec/sf1?{query}')
    
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
    
    counties = get_state_counties(state_fips, '2010/dec/sf1')
    
    df_sf1 = pandas.concat([
        get_county_sf1(state_fips, county_fips)
        for county_fips in sorted(counties)
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
        'geometry',
        ]]
    
    print(df_blocks3)
    
    return df_blocks3

def join_blocks_blockgroups(df_blocks, df_bgs):
    
    input_population = df_bgs['B01001_001E'].sum()
    
    # Note shorter block group GEOID for later matching
    df_blocks['GEOID_block'] = df_blocks.GEOID.str.slice(0, 12)
    
    # Sum ALAND for each block group
    df_blocks2 = df_blocks[['GEOID_block', 'ALAND']]\
        .groupby('GEOID_block', as_index=False).ALAND.sum()\
        .rename(columns={'ALAND': 'ALAND_bg'})
    
    # Join survey data to any block with matching GEOID prefix
    df_blocks3 = df_blocks.merge(df_blocks2, on='GEOID_block', how='right')
    
    # Join complete blocks with survey data to block-group-summed ALAND
    df_blocks4 = df_blocks3.merge(df_bgs[ACS_VARIABLES + ['GEOID']],
        left_on='GEOID_block', right_on='GEOID', how='left', suffixes=('', '_y'))
    
    # Scale survey data by land area block/group fraction
    for variable in ACS_VARIABLES:
        if variable.startswith('B19013'):
            # Do not scale household income
            continue
        df_blocks4[variable] *= (df_blocks4.ALAND / df_blocks4.ALAND_bg)
    
    # Select just a few columns
    df_blocks5 = df_blocks4[BLOCK_FIELDS + ACS_VARIABLES]
    
    output_population = df_blocks5['B01001_001E'].sum()
    
    assert round(input_population / output_population, 7) == 1, \
        '{} population unnaccounted for'.format(abs(output_population - input_population))
    
    return df_blocks5

def print_df(df, name):
    print('- ' * 20, name, 'at line', inspect.currentframe().f_back.f_lineno, '\n', df)

def join_blocks_votes(df_blocks, df_votes):

    input_votes = df_votes[VOTES_DEM].sum() + df_votes[VOTES_REP].sum()
    
    while True:
        # Join precinct votes to any block spatially contained within
        df_blocks2 = geopandas.sjoin(df_blocks,
            df_votes[['geometry', VOTES_DEM, VOTES_REP]],
            op='within', how='left', rsuffix='votes')
    
        # Note any missing precincts and their vote counts
        matched_indexes = set(df_blocks2.index_votes.dropna())
        missing_indexes = set(df_votes.index) - matched_indexes
        df_missing = df_votes.iloc[[df_votes.index.get_loc(i) for i in missing_indexes]]
        df_missing2 = df_missing[
            (df_missing[VOTES_DEM] > 0) | (df_missing[VOTES_REP] > 0)
        ].to_crs(epsg=5070)
    
        # If everything matched, break out of this loop
        if not len(df_missing2):
            print('*' * 80)
            break
        
        # Otherwise for each unmatched precinct, move vote counts to a neighbor
        df_matched = df_votes.iloc[
            [df_votes.index.get_loc(i) for i in matched_indexes]
        ].to_crs(epsg=5070)

        print('=' * 80)
        print('Missing votes:', df_missing2[VOTES_DEM].sum() + df_missing2[VOTES_REP].sum())
        print_df(df_missing2, 'df_missing2')
        print(df_missing2.index)
    
        for (bad_index, bad_row) in df_missing2.iterrows():
            # Select nearby voting precincts by overlapping envelopes, then move
            # votes from missing precincts to the highest-overlap matched one
            bad_envelope = bad_row.geometry.envelope
            df_nearby = df_matched[df_matched.overlaps(bad_envelope)]
            df_unions = df_nearby.envelope.union(bad_envelope)
            df_intersections = df_nearby.envelope.intersection(bad_envelope)
            df_IoUs = df_intersections.area / df_unions.area
        
            (good_index, ) = df_IoUs[df_IoUs == df_IoUs.max()].index.tolist()
            move_votes(df_votes, good_index, bad_index)
    
    # Sum ALAND for each voting precinct
    df_blocks3 = df_blocks2\
        .groupby('index_votes', as_index=False).ALAND.sum()\
        .rename(columns={'ALAND': 'ALAND_precinct'})
    
    # Join complete blocks with votes to precinct-summed ALAND
    df_blocks4 = df_blocks3.merge(df_blocks2, on='index_votes', how='left')
    
    # Scale presidential votes by land area block/precinct fraction
    df_blocks4[VOTES_DEM] *= (df_blocks4.ALAND / df_blocks4.ALAND_precinct)
    df_blocks4[VOTES_REP] *= (df_blocks4.ALAND / df_blocks4.ALAND_precinct)
    
    # Select just a few columns
    df_blocks5 = df_blocks4[BLOCK_FIELDS + [VOTES_DEM, VOTES_REP]]
    
    output_votes = df_blocks5[VOTES_DEM].sum() + df_blocks5[VOTES_REP].sum()
    
    # Complain if five or more votes are unaccounted for
    assert (abs(output_votes - input_votes) < 5), \
        '{} votes unnaccounted for'.format(abs(output_votes - input_votes))

    return df_blocks5

def main(output_dest, votes_source, blocks_source, bgs_source):
    df_bgs = load_blockgroups(bgs_source)
    df_blocks = load_blocks(blocks_source)
    df_votes = load_votes(votes_source)
    
    print_df(df_blocks, 'df_blocks')
    print_df(df_votes, 'df_votes')
    df_blocksV = join_blocks_votes(df_blocks, df_votes)
    
    print_df(df_blocksV, 'df_blocksV')
    print_df(df_bgs, 'df_bgs')
    
    df_blocksB = join_blocks_blockgroups(df_blocks, df_bgs)
    print_df(df_blocksB, 'df_blocksB')
    
    df_blocks2 = df_blocksV.merge(df_blocksB, how='inner', on=BLOCK_FIELDS)
    print_df(df_blocks2, 'df_blocks2')
    print(df_blocks2.columns)
    
    # Final output column mapping
    df_blocks3 = df_blocks2[df_blocks2.ALAND > 0][[
        'GEOID',
        'geometry',
    ]]
    
    df_blocks3[VOTES_DEM] = df_blocks2[VOTES_DEM].round(5)
    df_blocks3[VOTES_REP] = df_blocks2[VOTES_REP].round(5)
    df_blocks3['Population 2010'] = df_blocks2['P001001'].round(5)
    df_blocks3['Population 2018'] = df_blocks2['B01001_001E'].round(5)
    df_blocks3['Population 2018, Margin'] = df_blocks2['B01001_001M'].round(5)
    df_blocks3['Black Population 2018'] = df_blocks2['B02009_001E'].round(5)
    df_blocks3['Black Population 2018, Margin'] = df_blocks2['B02009_001M'].round(5)
    df_blocks3['Hispanic Population 2018'] = df_blocks2['B03002_012E'].round(5)
    df_blocks3['Hispanic Population 2018, Margin'] = df_blocks2['B03002_012M'].round(5)
    df_blocks3['High School or GED 2018'] = (df_blocks2['B15003_017E'] + df_blocks2['B15003_018E']).round(5)
    df_blocks3['High School or GED 2018, Margin'] = (df_blocks2['B15003_017M'] + df_blocks2['B15003_018M']).round(5)
    df_blocks3['Household Income 2018'] = df_blocks2['B19013_001E'].round(5)
    df_blocks3['Household Income 2018, Margin'] = df_blocks2['B19013_001M'].round(5)
    df_blocks3['Citizen Voting-Age Population 2018'] = df_blocks2['B29001_001E'].round(5)
    df_blocks3['Citizen Voting-Age Population 2018, Margin'] = df_blocks2['B29001_001M'].round(5)
    
    print_df(df_blocks3, 'df_blocks3')
    print(df_blocks3.columns)
    
    df_blocks3.to_file(output_dest, driver='GeoJSON')

if __name__ == '__main__':
    output_dest, votes_source, blocks_source, bgs_source = sys.argv[1:]
    exit(main(output_dest, votes_source, blocks_source, bgs_source))
