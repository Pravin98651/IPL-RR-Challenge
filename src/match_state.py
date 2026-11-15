"""
Match State Reconstruction Module.
Reconstructs cumulative match situation immediately BEFORE and AFTER every delivery.
"""
import pandas as pd
import numpy as np

def reconstruct_match_state(deliveries: pd.DataFrame, matches: pd.DataFrame, comps: pd.DataFrame) -> pd.DataFrame:
    df = deliveries.copy()
    
    # 1. Total ball runs and bowler conceded runs
    df['total_ball_runs'] = df['runs'] + df['extras1_runs'] + df['extras_2_runs']
    
    illegal_types = ['wide', 'Overstep', 'other']
    df['is_illegal'] = df['extras_type'].isin(illegal_types)
    df['is_legal'] = ~df['is_illegal']
    df['is_batter_ball'] = (df['extras_type'] != 'wide')
    
    # Bowler credited wickets
    bowler_dismissals = ['Caught', 'Bowled', 'LBW', 'Stump', 'Hit Wicket']
    df['is_bowler_wicket'] = df['is_wicket'] & df['dismissal_type'].isin(bowler_dismissals)
    
    # Bowler conceded runs (batter runs + wide/noball extras, excluding byes/legbyes/penalty)
    df['bowler_conceded_runs'] = df['runs'] + np.where(df['is_illegal'], df['extras1_runs'] + df['extras_2_runs'], 0)
    
    # 2. Sort chronologically
    df = df.sort_values(['match_id', 'innings', 'innings_ball_num']).reset_index(drop=True)
    
    # 3. Match level metadata merge
    m_cols = [
        'match_id', 'comp_id', 'match_number', 'match_date', 'stage',
        'venue_id', 'venue_country', 'home_team_id', 'home_team',
        'away_team_id', 'away_team', 'toss_win_team_id', 'toss_opted',
        'first_inn_revised_overs', 'second_inn_revised_overs',
        'revised_target', 'knock_out', 'win_team_id', 'result'
    ]
    df = df.merge(matches[m_cols], on='match_id', how='left')
    
    # Competition metadata
    c_cols = ['comp_id', 'comp_name', 'match_format', 'season']
    df = df.merge(comps[c_cols], on='comp_id', how='left')
    
    # 4. Groupby match_id and innings to compute cumulative progressions
    grouped = df.groupby(['match_id', 'innings'])
    
    df['post_current_score'] = grouped['total_ball_runs'].cumsum()
    df['pre_current_score'] = df['post_current_score'] - df['total_ball_runs']
    
    df['post_wickets_lost'] = grouped['is_wicket'].cumsum()
    df['pre_wickets_lost'] = df['post_wickets_lost'] - df['is_wicket'].astype(int)
    df['pre_wickets_remaining'] = np.clip(10 - df['pre_wickets_lost'], 0, 10)
    df['post_wickets_remaining'] = np.clip(10 - df['post_wickets_lost'], 0, 10)
    
    df['post_legal_balls_completed'] = grouped['is_legal'].cumsum()
    df['pre_legal_balls_completed'] = df['post_legal_balls_completed'] - df['is_legal'].astype(int)
    
    # 5. Scheduled overs and balls
    is_inn1 = df['innings'] == 1
    rev_overs = np.where(is_inn1, df['first_inn_revised_overs'], df['second_inn_revised_overs'])
    df['scheduled_overs'] = np.where(pd.notna(rev_overs) & (rev_overs > 0), rev_overs, 20.0)
    df['scheduled_legal_balls'] = (df['scheduled_overs'] * 6).astype(int)
    
    df['pre_legal_balls_remaining'] = np.maximum(0, df['scheduled_legal_balls'] - df['pre_legal_balls_completed'])
    df['post_legal_balls_remaining'] = np.maximum(0, df['scheduled_legal_balls'] - df['post_legal_balls_completed'])
    
    # 6. Current Run Rate (CRR)
    df['crr_pre'] = np.where(df['pre_legal_balls_completed'] > 0,
                             (df['pre_current_score'] / df['pre_legal_balls_completed']) * 6.0,
                             0.0)
    df['crr_post'] = np.where(df['post_legal_balls_completed'] > 0,
                              (df['post_current_score'] / df['post_legal_balls_completed']) * 6.0,
                              0.0)
    
    # 7. Innings Phases
    # Powerplay: balls 0 to 36; Middle: 37 to 90; Death: 91+
    pp_cutoff = np.round(df['scheduled_overs'] * (6.0 / 20.0) * 6).astype(int)
    mid_cutoff = np.round(df['scheduled_overs'] * (15.0 / 20.0) * 6).astype(int)
    
    df['phase'] = 'middle'
    df.loc[df['pre_legal_balls_completed'] < pp_cutoff, 'phase'] = 'powerplay'
    df.loc[df['pre_legal_balls_completed'] >= mid_cutoff, 'phase'] = 'death'
    
    # 8. Target and Chase Features (Innings 2)
    # Compute Innings 1 total score per match
    inn1_totals = df[df['innings'] == 1].groupby('match_id')['total_ball_runs'].sum().rename('inn1_total')
    df = df.merge(inn1_totals, on='match_id', how='left')
    df['calculated_target'] = df['inn1_total'] + 1
    
    df['target'] = np.where(df['revised_target'].notna() & (df['revised_target'] > 0),
                            df['revised_target'],
                            df['calculated_target'])
    
    # For innings 2 (and super overs 3/4)
    is_chase = df['innings'] >= 2
    df['runs_needed_pre'] = np.where(is_chase, np.maximum(0, df['target'] - df['pre_current_score']), np.nan)
    df['runs_needed_post'] = np.where(is_chase, np.maximum(0, df['target'] - df['post_current_score']), np.nan)
    
    # Required Run Rate
    df['rrr_pre'] = np.where(is_chase & (df['pre_legal_balls_remaining'] > 0),
                             (df['runs_needed_pre'] / df['pre_legal_balls_remaining']) * 6.0,
                             np.where(is_chase & (df['runs_needed_pre'] == 0), 0.0, np.nan))
    
    df['rrr_post'] = np.where(is_chase & (df['post_legal_balls_remaining'] > 0),
                              (df['runs_needed_post'] / df['post_legal_balls_remaining']) * 6.0,
                              np.where(is_chase & (df['runs_needed_post'] == 0), 0.0, np.nan))
    
    df['rrr_crr_diff_pre'] = np.where(is_chase, df['rrr_pre'] - df['crr_pre'], np.nan)
    
    return df

if __name__ == '__main__':
    from data_loader import load_ball_by_ball, load_matches, load_competitions
    bbb = load_ball_by_ball(nrows=5000)
    matches = load_matches()
    comps = load_competitions()
    reconstructed = reconstruct_match_state(bbb, matches, comps)
    print("Reconstructed state sample:")
    print(reconstructed[['match_id', 'innings', 'overid', 'pre_current_score', 'pre_wickets_lost', 'pre_legal_balls_remaining', 'phase', 'target', 'rrr_pre']].head(10))
