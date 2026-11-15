"""
Player Ranking and Composite Rating Engine.
Implements Bayesian shrinkage, sub-dimension standardization, and sensitivity analysis.
"""
import pandas as pd
import numpy as np
from reliability import bayesian_shrinkage, standardize_series
from typing import Dict, Tuple

def rank_batters(bat_df: pd.DataFrame,
                 min_balls: int = 100,
                 min_matches: int = 12,
                 w_perf: float = 0.60,
                 w_clutch: float = 0.30,
                 w_cons: float = 0.10) -> pd.DataFrame:
    """
    Ranks batters under pressure using Bayesian-shrunk contextual metrics.
    """
    eligible = bat_df[(bat_df['pressure_balls'] >= min_balls) &
                      (bat_df['pressure_matches'] >= min_matches)].copy()
    
    if len(eligible) == 0:
        raise ValueError(f"No batters meet criteria (min_balls={min_balls}, min_matches={min_matches}).")
        
    # Population baselines for empirical Bayes shrinkage
    pop_rae = eligible['pressure_rae_per_ball'].mean()
    pop_sr = eligible['pressure_sr'].mean()
    pop_wpa = eligible['pressure_wpa_per_ball'].mean()
    
    # Bayesian shrinkage (prior strength k = 40 balls)
    k = 40.0
    eligible['shrunk_pressure_rae'] = bayesian_shrinkage(
        eligible['pressure_rae_per_ball'].values,
        eligible['pressure_balls'].values,
        k, pop_rae
    )
    eligible['shrunk_pressure_sr'] = bayesian_shrinkage(
        eligible['pressure_sr'].values,
        eligible['pressure_balls'].values,
        k, pop_sr
    )
    eligible['shrunk_pressure_wpa'] = bayesian_shrinkage(
        eligible['pressure_wpa_per_ball'].values,
        eligible['pressure_balls'].values,
        k, pop_wpa
    )
    
    # 1. Pressure Performance Dimension
    z_rae = standardize_series(eligible['shrunk_pressure_rae'])
    z_sr = standardize_series(eligible['shrunk_pressure_sr'])
    z_wpa = standardize_series(eligible['shrunk_pressure_wpa'])
    z_dot = standardize_series(eligible['pressure_dot_pct'])
    z_bnd = standardize_series(eligible['pressure_bnd_pct'])
    
    dim_performance = (0.35 * z_rae + 0.25 * z_sr + 0.20 * z_wpa + 0.10 * z_bnd - 0.10 * z_dot)
    eligible['dim_performance'] = standardize_series(dim_performance)
    
    # 2. Clutch Improvement Dimension (Delta vs normal)
    z_d_rae = standardize_series(eligible['delta_rae'])
    z_d_sr = standardize_series(eligible['delta_sr'])
    z_d_wpa = standardize_series(eligible['delta_wpa'])
    z_d_dot = standardize_series(eligible['delta_dot_reduction'])
    
    dim_clutch = (0.35 * z_d_rae + 0.30 * z_d_sr + 0.20 * z_d_wpa + 0.15 * z_d_dot)
    eligible['dim_clutch'] = standardize_series(dim_clutch)
    
    # 3. Consistency Dimension
    z_pct_pos = standardize_series(eligible['pct_positive_pressure_matches'])
    z_opps = standardize_series(np.log1p(eligible['pressure_balls']))
    std_safe = eligible['match_rae_std'].fillna(eligible['match_rae_std'].mean())
    z_var = standardize_series(std_safe)
    
    dim_consistency = (0.50 * z_pct_pos + 0.30 * z_opps - 0.20 * z_var)
    eligible['dim_consistency'] = standardize_series(dim_consistency)
    
    # Final Composite Rating
    raw_composite = (w_perf * eligible['dim_performance'] +
                     w_clutch * eligible['dim_clutch'] +
                     w_cons * eligible['dim_consistency'])
    
    # Scale to 0 - 100 rating
    min_c = raw_composite.min()
    max_c = raw_composite.max()
    eligible['pressure_rating'] = np.round(50.0 + 15.0 * raw_composite, 2)
    # Scaled 0 to 100
    eligible['normalized_rating_100'] = np.round(100.0 * (raw_composite - min_c) / (max_c - min_c), 2)
    
    ranked = eligible.sort_values('pressure_rating', ascending=False).reset_index(drop=True)
    ranked['rank'] = ranked.index + 1
    return ranked

def rank_bowlers(bowl_df: pd.DataFrame,
                 min_balls: int = 120,
                 min_matches: int = 12,
                 w_perf: float = 0.60,
                 w_clutch: float = 0.30,
                 w_cons: float = 0.10) -> pd.DataFrame:
    """
    Ranks bowlers under pressure using Bayesian-shrunk contextual metrics.
    """
    eligible = bowl_df[(bowl_df['pressure_legal_balls'] >= min_balls) &
                      (bowl_df['pressure_matches'] >= min_matches)].copy()
    
    if len(eligible) == 0:
        raise ValueError(f"No bowlers meet criteria (min_balls={min_balls}, min_matches={min_matches}).")
        
    pop_rp = eligible['pressure_rp_per_ball'].mean()
    pop_wae = eligible['pressure_wae_per_ball'].mean()
    pop_econ = eligible['pressure_economy'].mean()
    pop_wpa = eligible['pressure_wpa_per_ball'].mean()
    
    k = 40.0
    eligible['shrunk_pressure_rp'] = bayesian_shrinkage(
        eligible['pressure_rp_per_ball'].values,
        eligible['pressure_legal_balls'].values,
        k, pop_rp
    )
    eligible['shrunk_pressure_wae'] = bayesian_shrinkage(
        eligible['pressure_wae_per_ball'].values,
        eligible['pressure_legal_balls'].values,
        k, pop_wae
    )
    eligible['shrunk_pressure_econ'] = bayesian_shrinkage(
        eligible['pressure_economy'].values,
        eligible['pressure_legal_balls'].values,
        k, pop_econ
    )
    eligible['shrunk_pressure_wpa'] = bayesian_shrinkage(
        eligible['pressure_wpa_per_ball'].values,
        eligible['pressure_legal_balls'].values,
        k, pop_wpa
    )
    
    # 1. Pressure Performance Dimension
    z_rp = standardize_series(eligible['shrunk_pressure_rp'])
    z_wae = standardize_series(eligible['shrunk_pressure_wae'])
    z_econ = standardize_series(-eligible['shrunk_pressure_econ']) # negative economy is good
    z_wpa = standardize_series(eligible['shrunk_pressure_wpa'])
    z_dot = standardize_series(eligible['pressure_dot_pct'])
    z_bnd_sup = standardize_series(-eligible['pressure_bnd_conceded_pct'])
    
    dim_performance = (0.30 * z_rp + 0.25 * z_wae + 0.20 * z_econ + 0.15 * z_wpa + 0.05 * z_dot + 0.05 * z_bnd_sup)
    eligible['dim_performance'] = standardize_series(dim_performance)
    
    # 2. Clutch Improvement Dimension (Delta vs normal)
    z_d_rp = standardize_series(eligible['delta_rp'])
    z_d_wae = standardize_series(eligible['delta_wae'])
    z_d_econ = standardize_series(eligible['delta_economy'])
    z_d_wpa = standardize_series(eligible['delta_wpa'])
    z_d_bnd = standardize_series(eligible['delta_bnd_suppression'])
    
    dim_clutch = (0.30 * z_d_rp + 0.25 * z_d_wae + 0.25 * z_d_econ + 0.10 * z_d_wpa + 0.10 * z_d_bnd)
    eligible['dim_clutch'] = standardize_series(dim_clutch)
    
    # 3. Consistency Dimension
    z_pct_pos = standardize_series(eligible['pct_positive_pressure_matches'])
    z_opps = standardize_series(np.log1p(eligible['pressure_legal_balls']))
    std_safe = eligible['match_rp_std'].fillna(eligible['match_rp_std'].mean())
    z_var = standardize_series(std_safe)
    
    dim_consistency = (0.50 * z_pct_pos + 0.30 * z_opps - 0.20 * z_var)
    eligible['dim_consistency'] = standardize_series(dim_consistency)
    
    # Final Composite Rating
    raw_composite = (w_perf * eligible['dim_performance'] +
                     w_clutch * eligible['dim_clutch'] +
                     w_cons * eligible['dim_consistency'])
    
    min_c = raw_composite.min()
    max_c = raw_composite.max()
    eligible['pressure_rating'] = np.round(50.0 + 15.0 * raw_composite, 2)
    eligible['normalized_rating_100'] = np.round(100.0 * (raw_composite - min_c) / (max_c - min_c), 2)
    
    ranked = eligible.sort_values('pressure_rating', ascending=False).reset_index(drop=True)
    ranked['rank'] = ranked.index + 1
    return ranked

if __name__ == '__main__':
    print("Ranking module defined.")
