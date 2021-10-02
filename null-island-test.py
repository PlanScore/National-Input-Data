#!/usr/bin/env python3
import io
import sys
import csv
import zipfile
import geopandas

assemble = __import__('assemble-state')

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

def get_matched_unique_blocks(df_blocks):
    ''' Get partial df_blocks with unique matching df_votes
    '''
    matched_block_flags = ~df_blocks.index_votes.isna()
    df_blocks_matched = df_blocks[matched_block_flags]
    unique_block_flags = ~df_blocks_matched.index.duplicated()
    df_blocks_matched_unique = df_blocks_matched[unique_block_flags]
    
    return df_blocks_matched_unique

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
    input_votes = df_votes[VOTES_DEM].sum() + df_votes[VOTES_REP].sum()
    input_people = df_blocks.P0010001.sum()
    
    # Progressively move votes from unmatched voting precincts
    while True:
        starting_votes = df_votes[VOTES_DEM].sum() + df_votes[VOTES_REP].sum()

        df_blocks2 = geopandas.sjoin(
            df_blocks,
            df_votes[['geometry', VOTES_DEM, VOTES_REP]],
            op='within', how='left', rsuffix='votes')
        #assemble.print_df(df_blocks2, 'df_blocks2')
    
        # Note any missing precincts and their vote counts
        df_votes_matched, df_votes_unmatched \
            = get_unmatched_votes(df_votes, df_blocks2, VOTES_DEM, VOTES_REP)
        #assemble.print_df(df_votes_matched, 'df_votes_matched')
        #assemble.print_df(df_votes_unmatched, 'df_votes_unmatched')
        
        # If everything matched, break out of this loop
        if df_votes_unmatched.empty:
            break
        assemble.print_df(df_votes_unmatched, 'df_votes_unmatched')
        
        # Reproject to a CONUS Albers equal-area
        df_votes_matched_5070 = df_votes_matched.to_crs(5070)
        df_votes_unmatched_5070 = df_votes_unmatched.to_crs(5070)
        
        for (bad_index, bad_row) in df_votes_unmatched_5070.iterrows():
            good_index = get_first_good_index(df_votes_matched_5070, bad_index, bad_row)
            if good_index is not None:
                assemble.move_votes(df_votes, good_index, bad_index, VOTES_DEM, VOTES_REP)
        
        ending_votes = df_votes[VOTES_DEM].sum() + df_votes[VOTES_REP].sum()
        assert round(starting_votes) == round(ending_votes), \
            '{} votes unnaccounted for'.format(abs(ending_votes - starting_votes))

    print('* ' * 40)

    # Progressively buffer census blocks by larger amounts to intersect
    for r in [1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1e0, 1e1, 1e2]:
        starting_people = df_blocks.P0010001.sum()

        # Join precinct votes to any land block spatially contained within
        df_blocks2 = geopandas.sjoin(
            df_blocks,
            df_votes[['geometry', VOTES_DEM, VOTES_REP]],
            op='intersects', how='left', rsuffix='votes')
        #assemble.print_df(df_blocks2, 'df_blocks2')
    
        # Note any unmatched blocks
        df_blocks2_unmatched = get_unmatched_blocks(df_blocks2)
        #assemble.print_df(df_blocks2_unmatched, 'df_blocks2_unmatched')
        
        # Stop if no unmatched blocks are found
        if df_blocks2_unmatched.empty:
            break
        assemble.print_df(df_blocks2_unmatched, f'df_blocks2_unmatched, r={r:.5f}')
        
        # Buffer unmatched blocks so they'll match
        geom_index = df_blocks.columns.get_loc('geometry')
        for (bad_index, bad_row) in df_blocks2_unmatched.iterrows():
            df_blocks.iat[bad_index, geom_index] = bad_row.geometry.centroid.buffer(r, 2)
        
        ending_people = df_blocks.P0010001.sum()
        assert round(starting_people) == round(ending_people), \
            '{} people unnaccounted for'.format(abs(ending_people - starting_people))

    print('*' * 80)

    # Un-buffer blocks now that they are all matched
    df_blocks2.geometry = df_blocks2.geometry.centroid

    # Note any duplicate blocks
    df_blocks3 = get_unique_blocks(df_blocks2)
    #assemble.print_df(df_blocks3, 'df_blocks3')

    # Sum land area for each voting precinct
    df_blocks3_area_sums = df_blocks3\
        .groupby('index_votes', as_index=False).AREALAND.sum()\
        .rename(columns={'AREALAND': 'AREALAND_precinct'})
    #assemble.print_df(df_blocks3_area_sums, 'df_blocks3_area_sums')
    
    # Join complete blocks with votes to precinct-summed land area
    df_blocks4 = df_blocks3.merge(df_blocks3_area_sums, on='index_votes', how='left')
    
    # Scale presidential votes by land area block/precinct fraction
    df_blocks4[VOTES_DEM] *= (df_blocks4.AREALAND / df_blocks4.AREALAND_precinct)
    df_blocks4[VOTES_REP] *= (df_blocks4.AREALAND / df_blocks4.AREALAND_precinct)
    #assemble.print_df(df_blocks4, 'df_blocks4')

    output_votes = df_blocks4[VOTES_DEM].sum() + df_votes[VOTES_REP].sum()
    output_people = df_blocks4.P0010001.sum()

    assert round(input_votes) == round(output_votes), \
        '{} votes unnaccounted for'.format(abs(output_votes - input_votes))
    assert round(input_people) == round(output_people), \
        '{} people unnaccounted for'.format(abs(output_people - input_people))
    
    return df_blocks4
    

if __name__ == '__main__':
    df_blocks1 = geopandas.read_file('null-island-blocks.geojson')
    df_votes1 = geopandas.read_file('null-island-precincts-normal.geojson')
    
    assemble.print_df(df_blocks1, 'df_blocks1')
    assemble.print_df(df_votes1, 'df_votes1')
    
    joined1 = join_blocks_votes(
        df_blocks1, df_votes1, 'US President 2020 - DEM', 'US President 2020 - REP',
    )

    assemble.print_df(joined1, 'joined1')
    geocodes = sorted(list(df_blocks1.GEOCODE))
    geocodes1 = sorted(list(joined1.GEOCODE))
    
    assert geocodes1 == geocodes, f"Should not have {', '.join(geocodes1)} GEOCODE column"
    assert joined1['US President 2020 - REP'].sum() == 160, \
        f"Should not have {joined1['US President 2020 - REP'].sum()} republican votes"
    assert joined1['US President 2020 - DEM'].sum() == 171, \
        f"Should not have {joined1['US President 2020 - DEM'].sum()} democratic votes"
    assert joined1['P0010001'].sum() == 63, \
        f"Should not have {joined1['P0010001'].sum()} total population"

    df_votes2 = geopandas.read_file('null-island-precincts-weird.geojson')
    
    assemble.print_df(df_votes2, 'df_votes2')
    
    joined2 = join_blocks_votes(
        df_blocks1, df_votes2, 'US President 2020 - DEM', 'US President 2020 - REP',
    )

    assemble.print_df(joined2, 'joined2')
    joined2b = joined2.merge(
        df_votes2[['Name']],
        how='left',
        left_on=joined2.index_votes,
        right_on=df_votes2.index,
        suffixes=('_block', '_precinct'),
    )
    assemble.print_df(joined2b, 'joined2b')
    print(joined2b.columns)
    joined2b.to_csv('/tmp/joined-NULL.csv')
    geocodes2 = sorted(list(joined2.GEOCODE))
    
    assert geocodes2 == geocodes, f"Should not have {', '.join(geocodes2)} GEOCODE column"
    assert joined2['US President 2020 - REP'].sum() == 160, \
        f"Should not have {joined2['US President 2020 - REP'].sum()} republican votes"
    assert joined2['US President 2020 - DEM'].sum() == 171, \
        f"Should not have {joined2['US President 2020 - DEM'].sum()} democratic votes"
    assert joined2['P0010001'].sum() == 63, \
        f"Should not have {joined2['P0010001'].sum()} total population"
    
    #exit()
    print('/' * 80)
    
    df_blocks2 = assemble.load_blocks('Census/or2020.pl.zip')
    df_votes3 = geopandas.read_file('/vsizip/VEST/or_2020.zip').to_crs(df_blocks2.crs)
    
    assemble.print_df(df_blocks2, 'df_blocks2')
    assemble.print_df(df_votes3, 'df_votes3')

    joined3 = join_blocks_votes(
        df_blocks2, df_votes3, 'G20PREDBID', 'G20PRERTRU',
    )

    assemble.print_df(joined3, 'joined3')
    joined3b = joined3.merge(
        df_votes3[['STATE', 'COUNTY', 'PRECINCT', 'NAME']],
        how='left',
        left_on=joined3.index_votes,
        right_on=df_votes3.index,
        suffixes=('_block', '_precinct'),
    )
    assemble.print_df(joined3b, 'joined3b')
    print(joined3b.columns)
    joined3b.to_csv('/tmp/joined-OR.csv')
