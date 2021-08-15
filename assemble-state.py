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
import csv
import io
import zipfile

BLOCK_FIELDS = [
    'GEOCODE', 'STATE', 'COUNTY', 'TRACT', 'BLOCK', #'NAME',
    'AREALAND', 'AREAWATER', 'P0010001', 'P0020002', 'P0020006',
    'P0020013', 'P0020008', 'P0020015', 'geometry',
]

ACS_VARIABLES = [
    'B01001_001E',
    'B02009_001E',
    'B03002_012E',
    'B15003_017E',
    'B15003_018E',
    #'B19013_001E',
    'B29001_001E',
    'B01001_001M',
    'B02009_001M',
    'B03002_012M',
    'B15003_017M',
    'B15003_018M',
    #'B19013_001M',
    'B29001_001M',
]

VOTES_DEM16 = 'US President 2016 - DEM'
VOTES_REP16 = 'US President 2016 - REP'
VOTES_DEM20 = 'US President 2020 - DEM'
VOTES_REP20 = 'US President 2020 - REP'

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

def move_votes(df, good_index, bad_index, VOTES_DEM, VOTES_REP):
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
        'G16PREDCLI': VOTES_DEM16,
        'G16PRERTRU': VOTES_REP16,
        'G20PREDBID': VOTES_DEM20,
        'G20PRERTRU': VOTES_REP20,
        'G16PREDCli': VOTES_DEM16,
        'G16PRERTru': VOTES_REP16,
        'G20PREDBid': VOTES_DEM20,
        'G20PRERTru': VOTES_REP20,
    })
    
    assert VOTES_DEM20 in df2.columns or VOTES_DEM16 in df2.columns
    assert VOTES_REP20 in df2.columns or VOTES_REP16 in df2.columns
    
    if VOTES_DEM20 in df2.columns:
        df3 = df2[[
            #'STATEFP',
            #'COUNTYFP',
            #'NAME',
            VOTES_DEM20,
            VOTES_REP20,
            'geometry'
            ]]
    else:
        df3 = df2[[
            #'STATEFP',
            #'COUNTYFP',
            #'NAME',
            VOTES_DEM16,
            VOTES_REP16,
            'geometry'
            ]]
    
    print(df3)
    
    return df3

@memoize
def load_blocks(blocks_source):
    zf = zipfile.ZipFile(blocks_source)
    fs = [io.TextIOWrapper(zf.open(name)) for name in zf.namelist()]
    pls = [csv.reader(file, delimiter='|') for file in fs]
    rows = (plgeo+pl1[5:]+pl2[5:]+pl3[5:] for (pl1, pl2, pl3, plgeo) in zip(*pls))
    blocks = [
        {
            'STATE': row[12],
            'COUNTY': row[14],
            'TRACT': row[32],
            'BLOCK': row[34],
            'NAME': row[87],
            #'GEOID': row[8],
            'GEOCODE': row[9],
            'AREALAND': int(row[84]),
            'AREAWATER': int(row[85]),
            'geometry': shapely.geometry.Point(float(row[93]), float(row[92])),
            'P0010001': int(row[96+1]), # Total Population
            'P0020002': int(row[167+2]), # Hispanic or Latino
            'P0020006': int(row[167+6]), # Non-Hispanic Black
            'P0020013': int(row[167+13]), # Non-Hispanic Black + White
            'P0020008': int(row[167+8]), # Non-Hispanic Asian
            'P0020015': int(row[167+15]), # Non-Hispanic Asian + White
        }
        for row in rows if row[2] == '750'
    ]
    
    df = geopandas.GeoDataFrame(
        blocks,
        crs='EPSG:4326',
        geometry='geometry',
    )
    
    return df

@memoize
def load_blockgroups(bgs_source, acs_year):
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
        'geometry',
        ]]
    
    print(df2)
    
    return get_acs(df2, acs_year)

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
def get_county_acs(state_fips, county_fips, api_path):

    query = urllib.parse.urlencode([
        ('get', ','.join(ACS_VARIABLES + ['NAME'])),
        ('for', 'block group:*'),
        ('in', f'state:{state_fips}'),
        ('in', f'county:{county_fips}'),
        ('in', 'tract:*'),
    ])
    
    print(f'https://api.census.gov/data/{api_path}?{query}')
    
    got = requests.get(f'https://api.census.gov/data/{api_path}?{query}')
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

def get_acs(df_bgs, acs_year):

    (state_fips, ) = df_bgs.STATEFP.unique()
    
    print('state_fips:', state_fips)
    
    counties = get_state_counties(state_fips, f'{acs_year}/acs/acs5')
    
    df_acs = pandas.concat([
        get_county_acs(state_fips, county_fips, f'{acs_year}/acs/acs5')
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
        'geometry',
        ] + ACS_VARIABLES]
    
    print(df_bgs3)
    
    return df_bgs3

@memoize
def get_county_sf1(state_fips, county_fips, api_path):

    query = urllib.parse.urlencode([
        ('get', ','.join(['P001001', 'NAME'])),
        ('for', 'block:*'),
        ('in', f'state:{state_fips}'),
        ('in', f'county:{county_fips}'),
        ('in', 'tract:*'),
    ])
    
    print(f'https://api.census.gov/data/{api_path}?{query}')
    
    got = requests.get(f'https://api.census.gov/data/{api_path}?{query}')
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
        get_county_sf1(state_fips, county_fips, '2010/dec/sf1')
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
    
    #print_df(df_blocks[['GEOCODE', 'geometry']], 'df_blocks')
    #print_df(df_bgs[['GEOID', 'geometry']], 'df_bgs')
    
    df_sjoined = geopandas.sjoin(df_blocks, df_bgs.to_crs(df_blocks.crs), op='within')
    
    #print_df(df_sjoined[['GEOCODE', 'GEOID', 'geometry', 'ALAND', 'AREALAND']], 'df_sjoined')
    #print(df_sjoined.columns)
    
    #df_mismatched = df_sjoined[df_sjoined.GEOID != df_sjoined.GEOCODE.str.slice(0, 12)]
    #print_df(df_mismatched[['GEOCODE', 'GEOID', 'geometry', 'ALAND', 'AREALAND']], 'df_mismatched')
    
    # Sum AREALAND for each block group
    df_bg2 = df_sjoined[['GEOID', 'AREALAND']]\
        .groupby('GEOID', as_index=False).AREALAND.sum()\
        .rename(columns={'AREALAND': 'AREALAND_bg'})
    
    #print_df(df_bg2, 'df_bg2')
    
    # Join land area data to any block with matching block group GEOID
    df_blocks2 = df_sjoined.merge(df_bg2, on='GEOID', how='right')
    
    #print_df(df_blocks2, 'df_blocks2')
    #print(df_blocks2.columns)

    # Scale survey data by land area block/group fraction
    for variable in ACS_VARIABLES:
        if variable.startswith('B19013'):
            # Do not scale household income
            continue
        df_blocks2[variable] *= (df_blocks2.AREALAND / df_blocks2.AREALAND_bg)
    
    #print_df(df_blocks2, 'df_blocks2')
    
    # Select just a few columns
    df_blocks3 = df_blocks2[BLOCK_FIELDS + ACS_VARIABLES]
    
    output_population = df_blocks3['B01001_001E'].sum()
    missing_population = abs(1 - input_population / output_population)
    
    assert missing_population < .0002, \
        '{} ({:.5f}%, more than 0.02%) population unnaccounted for'.format(
            abs(output_population - input_population),
            100 * missing_population,
        )
    
    return df_blocks3

def print_df(df, name):
    print('- ' * 20, name, 'at line', inspect.currentframe().f_back.f_lineno, '\n', df)

def join_blocks_votes(df_blocks, df_votes, VOTES_DEM, VOTES_REP):

    input_votes = df_votes[VOTES_DEM].sum() + df_votes[VOTES_REP].sum()
    stop_moving = False
    
    while True:
        starting_votes = df_votes[VOTES_DEM].sum() + df_votes[VOTES_REP].sum()
    
        # Join precinct votes to any land block spatially contained within
        df_blocks2 = geopandas.sjoin(
            df_blocks[df_blocks.AREALAND > 0],
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
        if not len(df_missing2) or stop_moving:
            print('*' * 80)
            break
        
        # Otherwise for each unmatched precinct, move vote counts to a neighbor
        df_matched = df_votes.iloc[
            [df_votes.index.get_loc(i) for i in matched_indexes]
        ].to_crs(epsg=5070)

        print('=' * 80)
        missing_vote_count = df_missing2[VOTES_DEM].sum() + df_missing2[VOTES_REP].sum()
        print('Missing votes:', missing_vote_count)
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
        
            try:
                (good_index, ) = df_IoUs[df_IoUs == df_IoUs.max()].index.tolist()
            except ValueError:
                # Skip this unmatchable precinct for now
                continue
            else:
                move_votes(df_votes, good_index, bad_index, VOTES_DEM, VOTES_REP)
        
        ending_votes = df_votes[VOTES_DEM].sum() + df_votes[VOTES_REP].sum()
        assert starting_votes == ending_votes, \
            '{} votes unnaccounted for'.format(abs(ending_votes - starting_votes))
    
        if missing_vote_count < 5:
            # Stop altogether if missing count is low enough
            stop_moving = True

    # Sum ALAND for each voting precinct
    df_blocks3 = df_blocks2\
        .groupby('index_votes', as_index=False).AREALAND.sum()\
        .rename(columns={'AREALAND': 'AREALAND_precinct'})
    
    # Join complete blocks with votes to precinct-summed AREALAND
    df_blocks4 = df_blocks3.merge(df_blocks2, on='index_votes', how='left')
    
    # Scale presidential votes by land area block/precinct fraction
    df_blocks4[VOTES_DEM] *= (df_blocks4.AREALAND / df_blocks4.AREALAND_precinct)
    df_blocks4[VOTES_REP] *= (df_blocks4.AREALAND / df_blocks4.AREALAND_precinct)
    
    # Select just a few columns
    df_blocks5 = df_blocks4[BLOCK_FIELDS + [VOTES_DEM, VOTES_REP]]
    
    output_votes = df_blocks5[VOTES_DEM].sum() + df_blocks5[VOTES_REP].sum()
    
    # Complain if five or more votes are unaccounted for
    assert (abs(output_votes - input_votes) < 5), \
        '{} votes unnaccounted for'.format(abs(output_votes - input_votes))

    return df_blocks5

def main(output_dest, votes_source, blocks_source, bgs_source):
    df_bgs = load_blockgroups(bgs_source, '2019')
    df_blocks = load_blocks(blocks_source)
    df_votes = load_votes(votes_source)
    
    print_df(df_blocks, 'df_blocks')
    print_df(df_votes, 'df_votes')
    if VOTES_DEM20 in df_votes.columns:
        df_blocksV = join_blocks_votes(df_blocks, df_votes, VOTES_DEM20, VOTES_REP20)
    else:
        df_blocksV = join_blocks_votes(df_blocks, df_votes, VOTES_DEM16, VOTES_REP16)
    
    print_df(df_blocksV, 'df_blocksV')
    print_df(df_bgs, 'df_bgs')
    
    df_blocksB = join_blocks_blockgroups(df_blocks, df_bgs)
    print_df(df_blocksB, 'df_blocksB')
    
    df_blocks2 = df_blocksV.merge(df_blocksB, how='inner', on=BLOCK_FIELDS)
    print_df(df_blocks2, 'df_blocks2')
    print(df_blocks2.columns)
    
    # Final output column mapping
    df_blocks3 = df_blocks2[df_blocks2.AREALAND > 0].rename(
        columns={'GEOCODE': 'GEOID20'}
    )[[
        'GEOID20',
        'geometry',
    ]]
    
    if VOTES_DEM20 in df_blocks2.columns:
        df_blocks3[VOTES_DEM20] = df_blocks2[VOTES_DEM20].round(5)
        df_blocks3[VOTES_REP20] = df_blocks2[VOTES_REP20].round(5)
    else:
        df_blocks3[VOTES_DEM16] = df_blocks2[VOTES_DEM16].round(5)
        df_blocks3[VOTES_REP16] = df_blocks2[VOTES_REP16].round(5)
    df_blocks3['Population 2020'] = df_blocks2['P0010001'].round(5)
    df_blocks3['Population 2019'] = df_blocks2['B01001_001E'].round(5)
    df_blocks3['Population 2019, Margin'] = df_blocks2['B01001_001M'].round(5)
    #df_blocks3['Black Population 2019'] = df_blocks2['B02009_001E'].round(5)
    #df_blocks3['Black Population 2019, Margin'] = df_blocks2['B02009_001M'].round(5)
    df_blocks3['Black Population 2020'] = (df_blocks2['P0020006'] + df_blocks2['P0020013']).round(5)
    #df_blocks3['Hispanic Population 2019'] = df_blocks2['B03002_012E'].round(5)
    #df_blocks3['Hispanic Population 2019, Margin'] = df_blocks2['B03002_012M'].round(5)
    df_blocks3['Hispanic Population 2020'] = df_blocks2['P0020002'].round(5)
    df_blocks3['Asian Population 2020'] = (df_blocks2['P0020008'] + df_blocks2['P0020015']).round(5)
    df_blocks3['High School or GED 2019'] = (df_blocks2['B15003_017E'] + df_blocks2['B15003_018E']).round(5)
    df_blocks3['High School or GED 2019, Margin'] = (df_blocks2['B15003_017M'] + df_blocks2['B15003_018M']).round(5)
    #df_blocks3['Household Income 2019'] = df_blocks2['B19013_001E'].round(5)
    #df_blocks3['Household Income 2019, Margin'] = df_blocks2['B19013_001M'].round(5)
    df_blocks3['Citizen Voting-Age Population 2019'] = df_blocks2['B29001_001E'].round(5)
    df_blocks3['Citizen Voting-Age Population 2019, Margin'] = df_blocks2['B29001_001M'].round(5)
    
    print_df(df_blocks3, 'df_blocks3')
    print(df_blocks3.columns)
    
    df_blocks3.to_file(output_dest, driver='GeoJSON')

if __name__ == '__main__':
    output_dest, votes_source, blocks_source, bgs_source = sys.argv[1:]
    exit(main(output_dest, votes_source, blocks_source, bgs_source))
