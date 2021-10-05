#!/usr/bin/env python3
import sys
import argparse
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
import re

BLOCK_FIELDS = [
    'GEOCODE',
    'STATE',
    'COUNTY',
    'TRACT',
    'BLOCK',
    #'NAME',
    'AREALAND',
    'P0010001',
    'P0020002',
    'P0020006',
    'P0020013',
    'P0020008',
    'P0020015',
    'P0030001',
    'geometry',
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

CVAP_VARIABLES = [
    'cvap_1_est',
    'cvap_3_est',
    'cvap_4_est',
    'cvap_5_est',
    'cvap_8_est',
    'cvap_9_est',
    'cvap_10_est',
    'cvap_13_est',
    'cvap_1_moe',
    'cvap_3_moe',
    'cvap_4_moe',
    'cvap_5_moe',
    'cvap_8_moe',
    'cvap_9_moe',
    'cvap_10_moe',
    'cvap_13_moe',
]

VOTES_DEM_P16 = 'US President 2016 - DEM'
VOTES_REP_P16 = 'US President 2016 - REP'
VOTES_OTHER_P16 = 'US President 2016 - Other'
VOTES_DEM_P20 = 'US President 2020 - DEM'
VOTES_REP_P20 = 'US President 2020 - REP'
VOTES_OTHER_P20 = 'US President 2020 - Other'
VOTES_DEM_S16 = 'US Senate 2016 - DEM'
VOTES_REP_S16 = 'US Senate 2016 - REP'
VOTES_OTHER_S16 = 'US Senate 2016 - Other'
VOTES_DEM_S18 = 'US Senate 2018 - DEM'
VOTES_REP_S18 = 'US Senate 2018 - REP'
VOTES_OTHER_S18 = 'US Senate 2018 - Other'
VOTES_DEM_S20 = 'US Senate 2020 - DEM'
VOTES_REP_S20 = 'US Senate 2020 - REP'
VOTES_OTHER_S20 = 'US Senate 2020 - Other'

VOTE_COLUMNS = (
    VOTES_DEM_P16,
    VOTES_REP_P16,
    VOTES_OTHER_P16,
    VOTES_DEM_P20,
    VOTES_REP_P20,
    VOTES_OTHER_P20,
    VOTES_DEM_S16,
    VOTES_REP_S16,
    VOTES_OTHER_S16,
    VOTES_DEM_S18,
    VOTES_REP_S18,
    VOTES_OTHER_S18,
    VOTES_DEM_S20,
    VOTES_REP_S20,
    VOTES_OTHER_S20,
)

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

def sum_over_vote_columns(df1):
    ''' http://thomas-cokelaer.info/blog/2014/01/pandas-dataframe-grouping-column-by-name/
    '''
    if len(list(df1.columns)) == len(set(df1.columns)):
        # Do nothing if all column names are unique
        return df1
    
    df2 = df1.transpose()
    df3 = df2.reset_index()
    df4 = df3.groupby("index").sum()
    df5 = df4.transpose()
    df6 = geopandas.GeoDataFrame(
        pandas.concat([
            # All columns except geometry are integer vote counts
            df5[c] if c == 'geometry' else df5[c].astype(int)
            for c in df5
        ], axis=1),
        geometry='geometry',
        crs=df1.crs,
    )
    
    return df6

@memoize
def load_votes(votes_source):
    ''' Return dataframe with vote columns and geometry only
    '''
    vote_pattern = re.compile(
        r'''
        ^
        (?P<type>G|P|S|R|C) # General, Primary, Special, Runoff, reCount
        (?P<core>
            (?P<yo>
                (?P<year>16|18|20|21)
                (?P<office>PRE|USS) # PRE = President, USS = U.S. Senate
            )
            (?P<party>D|R|[A-Z]) # D = Democrat, R = Republican, etc.
        )
        ''',
        re.I | re.VERBOSE,
    )

    column_mapping = {
        '16PRED': VOTES_DEM_P16, '16PRER': VOTES_REP_P16, '16PRE': VOTES_OTHER_P16,
        '20PRED': VOTES_DEM_P20, '20PRER': VOTES_REP_P20, '20PRE': VOTES_OTHER_P20,
        '16USSD': VOTES_DEM_S16, '16USSR': VOTES_REP_S16, '16USS': VOTES_OTHER_S16,
        '18USSD': VOTES_DEM_S18, '18USSR': VOTES_REP_S18, '18USS': VOTES_OTHER_S18,
        '20USSD': VOTES_DEM_S20, '20USSR': VOTES_REP_S20, '20USS': VOTES_OTHER_S20,
        '21USSD': VOTES_DEM_S20, '21USSR': VOTES_REP_S20, '21USS': VOTES_OTHER_S20,
    }

    df = geopandas.read_file(votes_source).to_crs(epsg=4326)
    
    df2 = df[[
        column for column in df.columns
        if vote_pattern.match(column)
        or column == 'geometry'
    ]]
    
    if 'ga_2020' in votes_source:
        df3 = geopandas.GeoDataFrame(
            pandas.concat((
                df2.geometry,
                # Trump/Biden recounts
                df2.C20PRERTRU,
                df2.C20PREDBID,
                df2.C20PRELJOR,
                # Ossoff general
                df2.G20USSRPER,
                df2.G20USSDOSS,
                df2.G20USSLHAZ,
            ), axis=1),
            geometry='geometry',
            crs=df2.crs,
        )
    elif 'la_2016' in votes_source:
        df3 = geopandas.GeoDataFrame(
            pandas.concat((
                df2.geometry,
                # Trump/Biden recounts
                df2.G16PRERTRU,
                df2.G16PREDCLI,
                df2.G16PRELJOH,
                df2.G16PREGSTE,
                df2.G16PREOMCM,
                df2.G16PRECCAS,
                df2.G16PREOOTH,
                # Senate runoff + zeros for 3rd party
                df2.R16USSRKEN,
                df2.R16USSDCAM,
                pandas.Series(name='R16USSxxxx', data=[0] * len(df2)),
            ), axis=1),
            geometry='geometry',
            crs=df2.crs,
        )
    else:
        df3 = df2

    df4 = df3.rename(columns={
        column: column_mapping.get(
            vote_pattern.match(column).group('core').upper(),
            column_mapping[vote_pattern.match(column).group('yo').upper()]
        )
        for column in df3.columns
        if vote_pattern.match(column)
    })
    
    df5 = sum_over_vote_columns(df4)
    print_df(df5, votes_source)

    return df5

@memoize
def load_blocks(blocks_source):
    zf = zipfile.ZipFile(blocks_source)
    fs = [
        io.TextIOWrapper(zf.open(name), encoding='Latin-1')
        for name in sorted(zf.namelist())
    ]
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
            'P0030001': int(row[240+1]), # Total population 18 years and over
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
def load_blockgroups(bgs_source, cvap_source, acs_year):
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
    
    df3 = load_cvap(cvap_source)
    print_df(df3, 'df3')

    df4 = df3[df3.geoid.str.slice(7, 9) == df2.iloc[0].STATEFP]
    df4.geoid = df4.geoid.str.slice(7, 19)

    print_df(df4, 'df4')
    
    df5 = df2
    
    for lnnumber in (1, 3, 4, 5, 8, 9, 10, 13):
        df4_partial = df4[df4.lnnumber == lnnumber][[
            'geoid', 'cvap_est', 'cvap_moe'
        ]].rename(columns={
            'geoid': 'GEOID',
            'cvap_est': f'cvap_{lnnumber}_est',
            'cvap_moe': f'cvap_{lnnumber}_moe',
        })
        df5 = df5.merge(df4_partial, how='left', on='GEOID')

        assert len(df4_partial) == len(df5)
        assert df4_partial[f'cvap_{lnnumber}_est'].sum() == df5[f'cvap_{lnnumber}_est'].sum()

    print_df(df5, 'df5')
    
    return get_acs(df5, acs_year)

@memoize
def load_cvap(cvap_source):
    zf = zipfile.ZipFile(cvap_source)
    file = io.TextIOWrapper(zf.open('BlockGr.csv'), encoding='Latin-1')
    rows = csv.DictReader(file, dialect='excel')
    
    df = pandas.DataFrame(rows).convert_dtypes()
    
    df2 = df[[
        'geoid',
        'lnnumber', # Check documentation for line number meanings
        'cvap_est',
        'cvap_moe',
    ]]
    
    df2.lnnumber = df2.lnnumber.astype(int)
    df2.cvap_est = df2.cvap_est.astype(int)
    df2.cvap_moe = df2.cvap_moe.astype(int)
    
    return df2

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
        ] + ACS_VARIABLES + CVAP_VARIABLES]
    
    print(df_bgs3)
    
    return df_bgs3

def join_blocks_blockgroups(df_blocks, df_bgs):
    
    input_population = df_blocks['P0010001'].sum()
    
    df_blocks2 = geopandas.sjoin(df_blocks, df_bgs.to_crs(df_blocks.crs), op='within')
    
    # Sum P0030001 (VAP) for each block group
    df_bg3 = df_blocks2[['GEOID', 'P0030001']]\
        .groupby('GEOID', as_index=False).P0030001.sum()\
        .rename(columns={'P0030001': 'P0030001_bg'})
    
    # Join land area data to any block with matching block group GEOID
    df_blocks4 = df_blocks2.merge(df_bg3, on='GEOID', how='right')
    
    # Scale survey data by land area block/group fraction
    for variable in (ACS_VARIABLES + CVAP_VARIABLES):
        if variable.startswith('B19013'):
            # Do not scale household income
            continue
        df_blocks4[variable] *= (df_blocks4.P0030001 / df_blocks4.P0030001_bg)
    
    # Select just a few columns
    df_blocks5 = df_blocks4[BLOCK_FIELDS + ACS_VARIABLES + CVAP_VARIABLES]
    
    output_population = df_blocks5['P0010001'].sum()
    assert round(output_population) == round(input_population), \
        '{} people unnaccounted for'.format(abs(input_population - output_population))
    
    return df_blocks5

def print_df(df, name):
    print('- ' * 20, name, 'at line', inspect.currentframe().f_back.f_lineno, '\n', df)

def get_unmatched_votes(df_votes, df_joined, VOTES_DEM, VOTES_REP):
    ''' Get partial df_votes where no block matches but votes exist
    '''
    matched_vote_indexes = set(df_joined.index_votes.dropna())
    df_votes_matched = df_votes.iloc[list(matched_vote_indexes),:]

    df_votes_matched_with_votes = df_votes_matched[
        (df_votes_matched[VOTES_DEM] > 0) | (df_votes_matched[VOTES_REP] > 0)
    ]

    missing_vote_indexes = set(df_votes.index) - matched_vote_indexes
    df_votes_unmatched = df_votes.iloc[list(missing_vote_indexes),:]

    df_votes_unmatched_with_votes = df_votes_unmatched[
        (df_votes_unmatched[VOTES_DEM] > 0) | (df_votes_unmatched[VOTES_REP] > 0)
    ]

    return df_votes_matched, df_votes_unmatched_with_votes

def get_unmatched_blocks(df_blocks):
    ''' Get partial df_blocks where no df_votes index has been matched
    '''
    unmatched_block_flags = df_blocks.index_votes.isna()
    df_blocks_unmatched = df_blocks[unmatched_block_flags]
    
    return df_blocks_unmatched

def get_unique_blocks(df_blocks):
    ''' Get partial df_blocks with unique df_votes
    '''
    unique_block_flags = ~df_blocks.index.duplicated()
    df_blocks_unique = df_blocks[unique_block_flags]
    
    return df_blocks_unique

def get_first_good_index(df_votes_matched, bad_index, bad_row):
    ''' Select nearby voting precincts by overlapping envelopes
    '''
    bad_envelope = bad_row.geometry.envelope
    df_votes_nearby = df_votes_matched[df_votes_matched.overlaps(bad_envelope)]
    df_votes_unions = df_votes_nearby.envelope.union(bad_envelope)
    df_votes_intersections = df_votes_nearby.envelope.intersection(bad_envelope)
    df_votes_IoUs = df_votes_intersections.area / df_votes_unions.area

    try:
        (good_index, ) = df_votes_IoUs[df_votes_IoUs == df_votes_IoUs.max()].index.tolist()
    except ValueError:
        return None
    else:
        return good_index

def join_blocks_votes(df_blocks, df_votes, VOTES_DEM, VOTES_REP):
    ''' Return df_blocks[BLOCK_FIELDS + votes + precinct] for a single race
    '''
    assert df_blocks.crs == 5070, f'Should not see {df_blocks.crs} df_blocks.crs'
    assert df_votes.crs == 5070, f'Should not see {df_votes.crs} df_votes.crs'
    
    input_votes = df_votes[VOTES_DEM].sum() + df_votes[VOTES_REP].sum()
    input_people = df_blocks.P0010001.sum()
    
    # Progressively buffer voting precincts by larger amounts to intersect
    for r in [100, 1e3, 1e4, 1e5, 1e6]:
        starting_votes = df_votes[VOTES_DEM].sum() + df_votes[VOTES_REP].sum()

        df_blocks2 = geopandas.sjoin(
            df_blocks,
            df_votes[['geometry', VOTES_DEM, VOTES_REP]],
            op='within', how='left', rsuffix='votes')
        #print_df(df_blocks2, 'df_blocks2')
    
        # Note any missing precincts and their vote counts
        df_votes_matched, df_votes_unmatched \
            = get_unmatched_votes(df_votes, df_blocks2, VOTES_DEM, VOTES_REP)
        #print_df(df_votes_matched, 'df_votes_matched')
        #print_df(df_votes_unmatched, 'df_votes_unmatched')
        
        # If everything matched, break out of this loop
        if df_votes_unmatched.empty:
            break
        print_df(df_votes_unmatched, f'df_votes_unmatched, r={r}')
        
        # Buffer unmatched precincts so they'll match
        df_votes_unmatched.geometry = df_votes_unmatched.geometry.buffer(r, 2)
        
        for (bad_index, bad_row) in df_votes_unmatched.iterrows():
            good_index = get_first_good_index(df_votes_matched, bad_index, bad_row)
            if good_index is not None:
                move_votes(df_votes, good_index, bad_index, VOTES_DEM, VOTES_REP)
        
        ending_votes = df_votes[VOTES_DEM].sum() + df_votes[VOTES_REP].sum()
        assert round(starting_votes) == round(ending_votes), \
            '{} votes unnaccounted for'.format(abs(ending_votes - starting_votes))

    print('* ' * 40, VOTES_DEM)

    # Progressively buffer census blocks by larger amounts to intersect
    for r in [100, 1e3, 1e4, 1e5, 1e6]:
        starting_people = df_blocks.P0010001.sum()

        # Join precinct votes to any land block spatially contained within
        df_blocks2 = geopandas.sjoin(
            df_blocks,
            df_votes[['geometry', VOTES_DEM, VOTES_REP]],
            op='intersects', how='left', rsuffix='votes')
        #print_df(df_blocks2, 'df_blocks2')
    
        # Note any unmatched blocks
        df_blocks2_unmatched = get_unmatched_blocks(df_blocks2)
        #print_df(df_blocks2_unmatched, 'df_blocks2_unmatched')
        
        # Stop if no unmatched blocks are found
        if df_blocks2_unmatched.empty:
            break
        print_df(df_blocks2_unmatched, f'df_blocks2_unmatched, r={r}')
        
        # Buffer unmatched blocks so they'll match
        geom_index = df_blocks.columns.get_loc('geometry')
        for (bad_index, bad_row) in df_blocks2_unmatched.iterrows():
            df_blocks.iat[bad_index, geom_index] = bad_row.geometry.buffer(r, 2)
        
        ending_people = df_blocks.P0010001.sum()
        assert round(starting_people) == round(ending_people), \
            '{} people unnaccounted for'.format(abs(ending_people - starting_people))

    print('*' * 80, VOTES_DEM)

    # Note any duplicate blocks
    df_blocks3 = get_unique_blocks(df_blocks2)
    #print_df(df_blocks3, 'df_blocks3')

    # Sum land area for each voting precinct
    df_blocks3_area_sums = df_blocks3\
        .groupby('index_votes', as_index=False).AREALAND.sum()\
        .rename(columns={'AREALAND': 'AREALAND_precinct'})
    #print_df(df_blocks3_area_sums, 'df_blocks3_area_sums')
    
    # Join complete blocks with votes to precinct-summed land area
    df_blocks4 = df_blocks3.merge(df_blocks3_area_sums, on='index_votes', how='left')
    
    # Scale presidential votes by land area block/precinct fraction
    df_blocks4[VOTES_DEM] *= (df_blocks4.AREALAND / df_blocks4.AREALAND_precinct)
    df_blocks4[VOTES_REP] *= (df_blocks4.AREALAND / df_blocks4.AREALAND_precinct)
    #print_df(df_blocks4, 'df_blocks4')

    # Select just a few columns
    df_blocks5 = df_blocks4[BLOCK_FIELDS + ['index_votes'] + [
        column for column in df_blocks4.columns
        if column in VOTE_COLUMNS
    ]]
    if VOTES_DEM in (VOTES_DEM_P20, VOTES_DEM_S20):
        df_blocks6 = df_blocks5.rename(columns={'index_votes': 'index_votes2020'})
    elif VOTES_DEM in (VOTES_DEM_S18, ):
        df_blocks6 = df_blocks5.rename(columns={'index_votes': 'index_votes2018'})
    elif VOTES_DEM in (VOTES_DEM_P16, VOTES_DEM_S16):
        df_blocks6 = df_blocks5.rename(columns={'index_votes': 'index_votes2016'})
    
    output_votes = df_blocks6[VOTES_DEM].sum() + df_blocks6[VOTES_REP].sum()
    output_people = df_blocks6.P0010001.sum()

    assert round(input_votes) == round(output_votes), \
        '{} votes unnaccounted for'.format(abs(output_votes - input_votes))
    assert round(input_people) == round(output_people), \
        '{} people unnaccounted for'.format(abs(output_people - input_people))
    
    return df_blocks6
    
def main(output_dest, votes_sources, blocks_source, bgs_source, cvap_source):
    df_bgs = load_blockgroups(bgs_source, cvap_source, '2019').to_crs(5070)
    df_blocks = load_blocks(blocks_source).to_crs(5070)
    print_df(df_blocks, 'df_blocks')

    df_blocksV, df_blocks_original_geometry = df_blocks, df_blocks.geometry.copy()
    for votes_source in reversed(votes_sources):
        df_votes = load_votes(votes_source).to_crs(5070)
        print_df(df_votes, votes_source)
        
        if VOTES_DEM_P20 in df_votes.columns:
            df_blocksV = join_blocks_votes(df_blocksV, df_votes, VOTES_DEM_P20, VOTES_REP_P20)
        if VOTES_DEM_S20 in df_votes.columns:
            df_blocksV = join_blocks_votes(df_blocksV, df_votes, VOTES_DEM_S20, VOTES_REP_S20)
        if VOTES_DEM_S18 in df_votes.columns:
            df_blocksV = join_blocks_votes(df_blocksV, df_votes, VOTES_DEM_S18, VOTES_REP_S18)
        if VOTES_DEM_P16 in df_votes.columns:
            df_blocksV = join_blocks_votes(df_blocksV, df_votes, VOTES_DEM_P16, VOTES_REP_P16)
        if VOTES_DEM_S16 in df_votes.columns:
            df_blocksV = join_blocks_votes(df_blocksV, df_votes, VOTES_DEM_S16, VOTES_REP_S16)
        
    # Note vote counts to compare later
    df_blocksV_votecounts = {
        column: df_blocksV[column].sum()
        for column in VOTE_COLUMNS
        if column in df_blocksV.columns
    }

    # Restore original geometries so that later merge() works by value
    df_blocks.geometry = df_blocks_original_geometry
    df_blocksV.geometry = df_blocks_original_geometry

    print_df(df_blocksV, 'df_blocksV')
    print_df(df_bgs, 'df_bgs')
    
    df_blocksB = join_blocks_blockgroups(df_blocks, df_bgs)
    print_df(df_blocksB, 'df_blocksB')
    
    df_blocks2 = df_blocksV.merge(df_blocksB, how='inner', on=BLOCK_FIELDS)
    print_df(df_blocks2, 'df_blocks2')
    for (column, expected_count) in df_blocksV_votecounts.items():
        assert round(df_blocks2[column].sum()) == round(expected_count), \
            f'Expected same {column} votes at 2'
    
    # Final output column mapping
    df_blocks3 = df_blocks2[[
        column for column in (
            'GEOCODE',
            'geometry',
            'index_votes2016',
            'index_votes2018',
            'index_votes2020',
        )
        if column in df_blocks2.columns
    ]].rename(
        columns={
            'GEOCODE': 'GEOID20',
            'index_votes2020': 'precinct2020',
            'index_votes2018': 'precinct2018',
            'index_votes2016': 'precinct2016',
        }
    )
    
    if VOTES_DEM_P20 in df_blocks2.columns:
        df_blocks3[VOTES_DEM_P20] = df_blocks2[VOTES_DEM_P20].round(5)
        df_blocks3[VOTES_REP_P20] = df_blocks2[VOTES_REP_P20].round(5)
    if VOTES_DEM_P16 in df_blocks2.columns:
        df_blocks3[VOTES_DEM_P16] = df_blocks2[VOTES_DEM_P16].round(5)
        df_blocks3[VOTES_REP_P16] = df_blocks2[VOTES_REP_P16].round(5)
    if VOTES_DEM_S20 in df_blocks2.columns:
        df_blocks3[VOTES_DEM_S20] = df_blocks2[VOTES_DEM_S20].round(5)
        df_blocks3[VOTES_REP_S20] = df_blocks2[VOTES_REP_S20].round(5)
    if VOTES_DEM_S18 in df_blocks2.columns:
        df_blocks3[VOTES_DEM_S18] = df_blocks2[VOTES_DEM_S18].round(5)
        df_blocks3[VOTES_REP_S18] = df_blocks2[VOTES_REP_S18].round(5)
    if VOTES_DEM_S16 in df_blocks2.columns:
        df_blocks3[VOTES_DEM_S16] = df_blocks2[VOTES_DEM_S16].round(5)
        df_blocks3[VOTES_REP_S16] = df_blocks2[VOTES_REP_S16].round(5)

    for (column, expected_count) in df_blocksV_votecounts.items():
        assert round(df_blocks3[column].sum()) == round(expected_count), \
            f'Expected same {column} votes at 3'

    df_blocks3['Population 2020'] = df_blocks2['P0010001'].round(5)
    #df_blocks3['Population 2019'] = df_blocks2['B01001_001E'].round(5)
    #df_blocks3['Population 2019, Margin'] = df_blocks2['B01001_001M'].round(5)
    df_blocks3['Black Population 2019'] = df_blocks2['B02009_001E'].round(5)
    df_blocks3['Black Population 2019, Margin'] = df_blocks2['B02009_001M'].round(5)
    df_blocks3['Black Population 2020'] = (df_blocks2['P0020006'] + df_blocks2['P0020013']).round(5)
    df_blocks3['Hispanic Population 2019'] = df_blocks2['B03002_012E'].round(5)
    df_blocks3['Hispanic Population 2019, Margin'] = df_blocks2['B03002_012M'].round(5)
    df_blocks3['Hispanic Population 2020'] = df_blocks2['P0020002'].round(5)
    df_blocks3['Asian Population 2020'] = (df_blocks2['P0020008'] + df_blocks2['P0020015']).round(5)
    df_blocks3['High School or GED 2019'] = (df_blocks2['B15003_017E'] + df_blocks2['B15003_018E']).round(5)
    df_blocks3['High School or GED 2019, Margin'] = (df_blocks2['B15003_017M'] + df_blocks2['B15003_018M']).round(5)
    #df_blocks3['Household Income 2019'] = df_blocks2['B19013_001E'].round(5)
    #df_blocks3['Household Income 2019, Margin'] = df_blocks2['B19013_001M'].round(5)
    df_blocks3['Citizen Voting-Age Population 2019'] = df_blocks2['cvap_1_est'].round(5)
    df_blocks3['Citizen Voting-Age Population 2019, Margin'] = df_blocks2['cvap_1_moe'].round(5)
    df_blocks3['Black Citizen Voting-Age Population 2019'] = (df_blocks2['cvap_5_est'] + df_blocks2['cvap_10_est']).round(5)
    df_blocks3['Black Citizen Voting-Age Population 2019, Margin'] = (df_blocks2['cvap_5_moe'] + df_blocks2['cvap_10_moe']).round(5)
    df_blocks3['Asian Citizen Voting-Age Population 2019'] = (df_blocks2['cvap_4_est'] + df_blocks2['cvap_9_est']).round(5)
    df_blocks3['Asian Citizen Voting-Age Population 2019, Margin'] = (df_blocks2['cvap_4_moe'] + df_blocks2['cvap_9_moe']).round(5)
    df_blocks3['American Indian or Alaska Native Citizen Voting-Age Population 2019'] = (df_blocks2['cvap_3_est'] + df_blocks2['cvap_8_est']).round(5)
    df_blocks3['American Indian or Alaska Native Citizen Voting-Age Population 2019, Margin'] = (df_blocks2['cvap_3_moe'] + df_blocks2['cvap_8_moe']).round(5)
    df_blocks3['Hispanic Citizen Voting-Age Population 2019'] = df_blocks2['cvap_13_est'].round(5)
    df_blocks3['Hispanic Citizen Voting-Age Population 2019, Margin'] = df_blocks2['cvap_13_moe'].round(5)
    df_blocks3['Voting-Age Population 2020'] = df_blocks2['P0030001'].round(5)
    
    print_df(df_blocks3, 'df_blocks3')
    print(df_blocks3.columns)
    print(df_blocks3[[c for c in df_blocks3.columns if c in VOTE_COLUMNS]].astype(int).sum())
    
    df_blocks3.to_crs(4326).to_file(output_dest, driver='GeoJSON')

parser = argparse.ArgumentParser()
parser.add_argument('output_dest')
parser.add_argument('votes_sources', nargs='*')
parser.add_argument('blocks_source')
parser.add_argument('bgs_source')
parser.add_argument('cvap_source')

if __name__ == '__main__':
    args = parser.parse_args()
    exit(main(
        args.output_dest,
        args.votes_sources,
        args.blocks_source,
        args.bgs_source,
        args.cvap_source,
    ))
