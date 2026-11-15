"""
Independent Batting Rating Engine.
Evaluates pressure performance, normal baseline, clutch delta, and match-level consistency.
"""
import pandas as pd
import numpy as np

def compute_batting_metrics(df: pd.DataFrame) -> pd.DataFrame:
    # Filter deliveries where batter faced the ball (exclude wides)
    bat_df = df[df['is_batter_ball']].copy()
    
    # 1. Match-level aggregation for consistency tracking
    match_bat = bat_df[bat_df['is_high_pressure']].groupby(['striker_id', 'match_id']).agg(
        match_pressure_runs=('runs', 'sum'),
        match_pressure_balls=('runs', 'count'),
        match_pressure_rae=('runs_above_expectation', 'sum'),
        match_pressure_wpa=('wpa_bat', 'sum')
    ).reset_index()
    
    match_bat['is_positive_match'] = match_bat['match_pressure_rae'] > 0
    consistency = match_bat.groupby('striker_id').agg(
        pressure_matches=('match_id', 'nunique'),
        positive_pressure_matches=('is_positive_match', 'sum'),
        match_rae_std=('match_pressure_rae', 'std')
    ).reset_index()
    consistency['pct_positive_pressure_matches'] = (
        consistency['positive_pressure_matches'] / consistency['pressure_matches']
    )
    
    # 2. Overall player pressure stats
    total_matches = bat_df.groupby('striker_id')['match_id'].nunique().rename('total_matches')
    
    press_df = bat_df[bat_df['is_high_pressure']]
    press_stats = press_df.groupby(['striker_id', 'striker_name']).agg(
        pressure_balls=('runs', 'count'),
        pressure_runs=('runs', 'sum'),
        pressure_fours=('is_four', 'sum'),
        pressure_sixes=('is_six', 'sum'),
        pressure_dots=('runs', lambda x: (x == 0).sum()),
        pressure_dismissals=('is_wicket', 'sum'),
        pressure_total_rae=('runs_above_expectation', 'sum'),
        pressure_total_wpa=('wpa_bat', 'sum'),
        ipl_pressure_balls=('match_format', lambda x: (x == 'T20').sum()),
        t20i_pressure_balls=('match_format', lambda x: (x == 'T20I').sum()),
        inn1_pressure_balls=('innings', lambda x: (x == 1).sum()),
        inn2_pressure_balls=('innings', lambda x: (x >= 2).sum())
    ).reset_index()
    
    press_stats['pressure_sr'] = (press_stats['pressure_runs'] / press_stats['pressure_balls']) * 100.0
    press_stats['pressure_rae_per_ball'] = press_stats['pressure_total_rae'] / press_stats['pressure_balls']
    press_stats['pressure_wpa_per_ball'] = press_stats['pressure_total_wpa'] / press_stats['pressure_balls']
    press_stats['pressure_dot_pct'] = press_stats['pressure_dots'] / press_stats['pressure_balls']
    press_stats['pressure_bnd_pct'] = (press_stats['pressure_fours'] + press_stats['pressure_sixes']) / press_stats['pressure_balls']
    press_stats['pressure_dismissal_rate'] = press_stats['pressure_dismissals'] / press_stats['pressure_balls']
    
    # 3. Overall player normal stats (non-pressure baseline)
    norm_df = bat_df[~bat_df['is_high_pressure']]
    norm_stats = norm_df.groupby('striker_id').agg(
        normal_balls=('runs', 'count'),
        normal_runs=('runs', 'sum'),
        normal_fours=('is_four', 'sum'),
        normal_sixes=('is_six', 'sum'),
        normal_dots=('runs', lambda x: (x == 0).sum()),
        normal_dismissals=('is_wicket', 'sum'),
        normal_total_rae=('runs_above_expectation', 'sum'),
        normal_total_wpa=('wpa_bat', 'sum')
    ).reset_index()
    
    norm_stats['normal_sr'] = (norm_stats['normal_runs'] / np.maximum(1, norm_stats['normal_balls'])) * 100.0
    norm_stats['normal_rae_per_ball'] = norm_stats['normal_total_rae'] / np.maximum(1, norm_stats['normal_balls'])
    norm_stats['normal_wpa_per_ball'] = norm_stats['normal_total_wpa'] / np.maximum(1, norm_stats['normal_balls'])
    norm_stats['normal_dot_pct'] = norm_stats['normal_dots'] / np.maximum(1, norm_stats['normal_balls'])
    norm_stats['normal_bnd_pct'] = (norm_stats['normal_fours'] + norm_stats['normal_sixes']) / np.maximum(1, norm_stats['normal_balls'])
    norm_stats['normal_dismissal_rate'] = norm_stats['normal_dismissals'] / np.maximum(1, norm_stats['normal_balls'])
    
    # Merge pressure, normal, and consistency
    merged = press_stats.merge(norm_stats, on='striker_id', how='left')
    merged = merged.merge(consistency, on='striker_id', how='left')
    merged = merged.merge(total_matches, on='striker_id', how='left')
    
    # 4. Clutch Improvement / Deltas
    merged['delta_sr'] = merged['pressure_sr'] - merged['normal_sr']
    merged['delta_rae'] = merged['pressure_rae_per_ball'] - merged['normal_rae_per_ball']
    merged['delta_wpa'] = merged['pressure_wpa_per_ball'] - merged['normal_wpa_per_ball']
    merged['delta_bnd'] = merged['pressure_bnd_pct'] - merged['normal_bnd_pct']
    # Lower dot pct under pressure is an improvement (negative dot delta is good)
    merged['delta_dot_reduction'] = merged['normal_dot_pct'] - merged['pressure_dot_pct']
    
    return merged

if __name__ == '__main__':
    print("Batting engine defined.")
