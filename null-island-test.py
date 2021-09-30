#!/usr/bin/env python3
import io
import sys
import csv
import zipfile
import geopandas

assemble = __import__('assemble-state')

def join_blocks_votes(df_blocks, df_votes, VOTES_DEM, VOTES_REP):
    ''' Return df_blocks[BLOCK_FIELDS + votes + precinct] for a single race
    '''
    input_votes = df_votes[VOTES_DEM].sum() + df_votes[VOTES_REP].sum()
    input_people = df_blocks.P0010001.sum()
    stop_moving = False
    print('input_votes:', input_votes)
    print('input_people:', input_people)
    
    while True:
        starting_votes = df_votes[VOTES_DEM].sum() + df_votes[VOTES_REP].sum()
        starting_people = df_blocks.P0010001.sum() + df_blocks.P0010001.sum()
    
        # Join precinct votes to any land block spatially contained within
        df_blocks2 = geopandas.sjoin(
            df_blocks,
            df_votes[['geometry', VOTES_DEM, VOTES_REP]],
            op='within', how='left', rsuffix='votes')
    
        assemble.print_df(df_blocks2, 'df_blocks2')

        # Note any missing precincts and their vote counts
        matched_vote_indexes = set(df_blocks2.index_votes.dropna())
        missing_vote_indexes = set(df_votes.index) - matched_vote_indexes
        df_votes_unmatched = df_votes.iloc[list(missing_vote_indexes),:]
        assemble.print_df(df_votes_unmatched, 'df_votes_unmatched')
        
        # Note any unmatched blocks and their vote counts
        unmatched_block_flags = df_blocks2.index_votes.isna()
        df_blocks2_unmatched = df_blocks2[unmatched_block_flags]
        assemble.print_df(df_blocks2_unmatched, 'df_blocks2_unmatched')
    
        # Note any duplicate blocks
        matched_block_flags = ~df_blocks2.index_votes.isna()
        df_blocks2_matched = df_blocks2[matched_block_flags]
        unique_block_flags = ~df_blocks2_matched.index.duplicated()
        df_blocks2_matched_unique = df_blocks2_matched[unique_block_flags]
        assemble.print_df(df_blocks2_matched_unique, 'df_blocks2_matched_unique')
        
        raise NotImplementedError()
    

if __name__ == '__main__':
    df_blocks = geopandas.read_file('null-island-blocks.geojson')
    df_votes1 = geopandas.read_file('null-island-precincts-normal.geojson')
    
    assemble.print_df(df_blocks, 'df_blocks')
    assemble.print_df(df_votes1, 'df_votes1')
    
    joined1 = assemble.join_blocks_votes(
        df_blocks, df_votes1, 'US President 2020 - DEM', 'US President 2020 - REP',
    )

    assemble.print_df(joined1, 'joined1')
    geocodes = sorted(list(df_blocks.GEOCODE))
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
        df_blocks, df_votes2, 'US President 2020 - DEM', 'US President 2020 - REP',
    )

    assemble.print_df(joined2, 'joined2')
    geocodes2 = sorted(list(joined2.GEOCODE))
    
    assert geocodes2 == geocodes, f"Should not have {', '.join(geocodes2)} GEOCODE column"
    assert joined2['US President 2020 - REP'].sum() == 160, \
        f"Should not have {joined2['US President 2020 - REP'].sum()} republican votes"
    assert joined2['US President 2020 - DEM'].sum() == 171, \
        f"Should not have {joined2['US President 2020 - DEM'].sum()} democratic votes"
    assert joined2['P0010001'].sum() == 63, \
        f"Should not have {joined2['P0010001'].sum()} total population"
