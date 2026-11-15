"""
Independent Bowling Rating Engine.
Evaluates pressure bowling performance, normal baseline, clutch delta, and match-level consistency.
"""
import pandas as pd
import numpy as np

def compute_bowling_metrics(df: pd.DataFrame) -> pd.DataFrame:
    # 1. Match-level aggregation for consistency tracking
    # Bowler legal deliveries and runs under pressure
    press_balls = df[df['is_high_pressure']].copy()
    match_bowl = press_balls.groupby(['bowler_id', 'match_id']).agg(
        match_pressure_legal_balls=('is_legal', 'sum'),
        match_pressure_runs=('bowler_conceded_runs', 'sum'),
        match_pressure_wickets=('is_bowler_wicket', 'sum'),
        match_pressure_rp=('runs_prevented', 'sum'),
        match_pressure_wae=('wickets_above_expectation', 'sum'),
        match_pressure_wpa=('wpa_bowl', 'sum')
    ).reset_index()
    
    match_bowl['is_positive_match'] = (match_bowl['match_pressure_rp'] > 0) | (match_bowl['match_pressure_wickets'] > 0)
    consistency = match_bowl.groupby('bowler_id').agg(
        pressure_matches=('match_id', 'nunique'),
        positive_pressure_matches=('is_positive_match', 'sum'),
        match_rp_std=('match_pressure_rp', 'std')
    ).reset_index()
    consistency['pct_positive_pressure_matches'] = (
        consistency['positive_pressure_matches'] / consistency['pressure_matches']
    )
    
    # 2. Overall player pressure stats
    total_matches = df.groupby('bowler_id')['match_id'].nunique().rename('total_matches')
    
    press_stats = press_balls.groupby(['bowler_id', 'bowler_name']).agg(
        pressure_total_balls=('runs', 'count'),
        pressure_legal_balls=('is_legal', 'sum'),
        pressure_runs_conceded=('bowler_conceded_runs', 'sum'),
        pressure_wickets=('is_bowler_wicket', 'sum'),
        pressure_dots=('bowler_conceded_runs', lambda x: (x == 0).sum()),
        pressure_bnd_conceded=('bowler_conceded_runs', lambda x: (x >= 4).sum()),
        pressure_total_rp=('runs_prevented', 'sum'),
        pressure_total_wae=('wickets_above_expectation', 'sum'),
        pressure_total_wpa=('wpa_bowl', 'sum'),
        ipl_pressure_balls=('match_format', lambda x: (x == 'T20').sum()),
        t20i_pressure_balls=('match_format', lambda x: (x == 'T20I').sum()),
        inn1_pressure_balls=('innings', lambda x: (x == 1).sum()),
        inn2_pressure_balls=('innings', lambda x: (x >= 2).sum())
    ).reset_index()
    
    press_stats['pressure_overs'] = press_stats['pressure_legal_balls'] / 6.0
    press_stats['pressure_economy'] = np.where(
        press_stats['pressure_overs'] > 0,
        press_stats['pressure_runs_conceded'] / press_stats['pressure_overs'],
        0.0
    )
    press_stats['pressure_rp_per_ball'] = press_stats['pressure_total_rp'] / np.maximum(1, press_stats['pressure_legal_balls'])
    press_stats['pressure_wae_per_ball'] = press_stats['pressure_total_wae'] / np.maximum(1, press_stats['pressure_legal_balls'])
    press_stats['pressure_wpa_per_ball'] = press_stats['pressure_total_wpa'] / np.maximum(1, press_stats['pressure_legal_balls'])
    press_stats['pressure_dot_pct'] = press_stats['pressure_dots'] / np.maximum(1, press_stats['pressure_total_balls'])
    press_stats['pressure_bnd_conceded_pct'] = press_stats['pressure_bnd_conceded'] / np.maximum(1, press_stats['pressure_total_balls'])
    press_stats['pressure_bowling_strike_rate'] = np.where(
        press_stats['pressure_wickets'] > 0,
        press_stats['pressure_legal_balls'] / press_stats['pressure_wickets'],
        np.nan
    )
    
    # 3. Overall player normal stats (non-pressure baseline)
    norm_balls = df[~df['is_high_pressure']]
    norm_stats = norm_balls.groupby('bowler_id').agg(
        normal_total_balls=('runs', 'count'),
        normal_legal_balls=('is_legal', 'sum'),
        normal_runs_conceded=('bowler_conceded_runs', 'sum'),
        normal_wickets=('is_bowler_wicket', 'sum'),
        normal_dots=('bowler_conceded_runs', lambda x: (x == 0).sum()),
        normal_bnd_conceded=('bowler_conceded_runs', lambda x: (x >= 4).sum()),
        normal_total_rp=('runs_prevented', 'sum'),
        normal_total_wae=('wickets_above_expectation', 'sum'),
        normal_total_wpa=('wpa_bowl', 'sum')
    ).reset_index()
    
    norm_stats['normal_overs'] = norm_stats['normal_legal_balls'] / 6.0
    norm_stats['normal_economy'] = np.where(
        norm_stats['normal_overs'] > 0,
        norm_stats['normal_runs_conceded'] / norm_stats['normal_overs'],
        0.0
    )
    norm_stats['normal_rp_per_ball'] = norm_stats['normal_total_rp'] / np.maximum(1, norm_stats['normal_legal_balls'])
    norm_stats['normal_wae_per_ball'] = norm_stats['normal_total_wae'] / np.maximum(1, norm_stats['normal_legal_balls'])
    norm_stats['normal_wpa_per_ball'] = norm_stats['normal_total_wpa'] / np.maximum(1, norm_stats['normal_legal_balls'])
    norm_stats['normal_dot_pct'] = norm_stats['normal_dots'] / np.maximum(1, norm_stats['normal_total_balls'])
    norm_stats['normal_bnd_conceded_pct'] = norm_stats['normal_bnd_conceded'] / np.maximum(1, norm_stats['normal_total_balls'])
    
    # Merge pressure, normal, and consistency
    merged = press_stats.merge(norm_stats, on='bowler_id', how='left')
    merged = merged.merge(consistency, on='bowler_id', how='left')
    merged = merged.merge(total_matches, on='bowler_id', how='left')
    
    # 4. Clutch Improvement / Deltas
    # For economy: lower economy under pressure is better, so normal_econ - pressure_econ is positive when bowler improves!
    merged['delta_economy'] = merged['normal_economy'] - merged['pressure_economy']
    merged['delta_rp'] = merged['pressure_rp_per_ball'] - merged['normal_rp_per_ball']
    merged['delta_wae'] = merged['pressure_wae_per_ball'] - merged['normal_wae_per_ball']
    merged['delta_wpa'] = merged['pressure_wpa_per_ball'] - merged['normal_wpa_per_ball']
    merged['delta_dot'] = merged['pressure_dot_pct'] - merged['normal_dot_pct']
    # For boundary conceded: lower under pressure is better
    merged['delta_bnd_suppression'] = merged['normal_bnd_conceded_pct'] - merged['pressure_bnd_conceded_pct']
    
    return merged

if __name__ == '__main__':
    print("Bowling engine defined.")
