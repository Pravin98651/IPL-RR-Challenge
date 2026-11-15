"""
Feature Engineering Module for SupeRR Selector.
Computes contextual features, par expectations, and player in-match progression.
"""
import pandas as pd
import numpy as np

def add_first_innings_par_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes 1st innings par expectations and collapse indicators.
    Uses empirical baseline lookup derived from historical 1st innings totals.
    """
    df = df.copy()
    
    # 1st Innings historical empirical average final score by (balls_bin, wickets_lost)
    # Average 1st innings score in dataset is ~168 for T20I and ~178 for IPL
    # We construct a smooth expected remaining runs function:
    # E[remaining runs] = (remaining_balls / 6.0) * base_rr * wicket_resource_factor
    balls_rem = df['pre_legal_balls_remaining']
    wkts_rem = df['pre_wickets_remaining']
    
    # Wicket resource factor (Cobb-Douglas / Duckworth-Lewis style decay)
    # Resources scale with wickets remaining: w / 10 ^ 0.65
    resource_factor = np.power(np.clip(wkts_rem / 10.0, 0.05, 1.0), 0.65)
    
    # Format baseline run rate: ~8.8 for IPL (T20), ~8.0 for T20I
    base_format_rr = np.where(df['match_format'] == 'T20', 8.8, 8.0)
    
    # Expected runs in remaining overs
    expected_remaining_runs = (balls_rem / 6.0) * base_format_rr * resource_factor
    df['projected_final_score'] = df['pre_current_score'] + expected_remaining_runs
    
    # Expected par score at current ball
    expected_completed_runs = ((120 - balls_rem) / 6.0) * base_format_rr * resource_factor
    df['par_score_at_ball'] = expected_completed_runs
    df['par_deficit'] = np.where(df['innings'] == 1, df['par_score_at_ball'] - df['pre_current_score'], 0.0)
    
    # Collapse indicators (Innings 1)
    df['is_early_collapse'] = (df['innings'] == 1) & (df['pre_legal_balls_completed'] <= 36) & (df['pre_wickets_lost'] >= 3)
    df['is_mid_collapse'] = (df['innings'] == 1) & (df['pre_legal_balls_completed'] <= 60) & (df['pre_wickets_lost'] >= 4)
    df['is_collapse_active'] = df['is_early_collapse'] | df['is_mid_collapse']
    
    return df

def add_player_in_match_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes striker and bowler in-match cumulative performance before each delivery.
    """
    df = df.copy()
    
    # Sort chronologically
    df = df.sort_values(['match_id', 'innings', 'innings_ball_num']).reset_index(drop=True)
    
    # Striker match runs before delivery
    df['striker_match_runs_post'] = df.groupby(['match_id', 'striker_id'])['runs'].cumsum()
    df['striker_match_runs_pre'] = df['striker_match_runs_post'] - df['runs']
    
    # Striker balls faced before delivery
    df['striker_balls_faced_post'] = df.groupby(['match_id', 'striker_id'])['is_batter_ball'].cumsum()
    df['striker_balls_faced_pre'] = df['striker_balls_faced_post'] - df['is_batter_ball'].astype(int)
    
    # Bowler legal balls bowled before delivery
    df['bowler_legal_balls_post'] = df.groupby(['match_id', 'bowler_id'])['is_legal'].cumsum()
    df['bowler_legal_balls_pre'] = df['bowler_legal_balls_post'] - df['is_legal'].astype(int)
    
    # Bowler runs conceded before delivery
    df['bowler_runs_conceded_post'] = df.groupby(['match_id', 'bowler_id'])['bowler_conceded_runs'].cumsum()
    df['bowler_runs_conceded_pre'] = df['bowler_runs_conceded_post'] - df['bowler_conceded_runs']
    
    # Bowler wickets before delivery
    df['bowler_wickets_post'] = df.groupby(['match_id', 'bowler_id'])['is_bowler_wicket'].cumsum()
    df['bowler_wickets_pre'] = df['bowler_wickets_post'] - df['is_bowler_wicket'].astype(int)
    
    return df

def generate_features(reconstructed_df: pd.DataFrame) -> pd.DataFrame:
    print("Engineering 1st innings par features...")
    df = add_first_innings_par_features(reconstructed_df)
    print("Engineering player in-match progression features...")
    df = add_player_in_match_features(df)
    return df

if __name__ == '__main__':
    from data_loader import load_ball_by_ball, load_matches, load_competitions
    from match_state import reconstruct_match_state
    bbb = load_ball_by_ball(nrows=2000)
    matches = load_matches()
    comps = load_competitions()
    recon = reconstruct_match_state(bbb, matches, comps)
    feat_df = generate_features(recon)
    print("Features engineered successfully. Columns count:", len(feat_df.columns))
    print(feat_df[['match_id', 'innings', 'overid', 'projected_final_score', 'is_collapse_active', 'striker_match_runs_pre']].head())
