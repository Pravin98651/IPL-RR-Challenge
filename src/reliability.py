"""
Statistical Reliability, Bayesian Shrinkage, and Uncertainty Module.
Shrinks small-sample rate metrics toward population priors and calculates bootstrap intervals.
"""
import pandas as pd
import numpy as np
from typing import Tuple, List, Dict

def bayesian_shrinkage(observed_scores: np.ndarray,
                       sample_sizes: np.ndarray,
                       prior_strength: float,
                       baseline_score: float) -> np.ndarray:
    """
    Applies empirical Bayes shrinkage:
    Adjusted = [n / (n + k)] * Observed + [k / (n + k)] * Baseline
    """
    weight = sample_sizes / (sample_sizes + prior_strength)
    adjusted = weight * observed_scores + (1.0 - weight) * baseline_score
    return adjusted

def standardize_series(s: pd.Series) -> pd.Series:
    """
    Z-score standardization with safe variance handling.
    """
    std = s.std()
    if pd.isna(std) or std == 0:
        return s - s.mean()
    return (s - s.mean()) / std

def bootstrap_player_uncertainty(player_id: int,
                                match_df: pd.DataFrame,
                                n_bootstrap: int = 500,
                                metric_col: str = 'match_pressure_rae') -> Dict[str, float]:
    """
    Computes bootstrap confidence intervals for a player's match-level metric.
    """
    p_matches = match_df[match_df.iloc[:, 0] == player_id][metric_col].values
    if len(p_matches) < 3:
        return {'mean': np.mean(p_matches) if len(p_matches) > 0 else 0.0,
                'ci_lower': 0.0, 'ci_upper': 0.0, 'ci_width': 0.0}
        
    boot_means = []
    for _ in range(n_bootstrap):
        sample = np.random.choice(p_matches, size=len(p_matches), replace=True)
        boot_means.append(np.mean(sample))
        
    ci_low = float(np.percentile(boot_means, 2.5))
    ci_high = float(np.percentile(boot_means, 97.5))
    return {
        'mean': float(np.mean(boot_means)),
        'ci_lower': ci_low,
        'ci_upper': ci_high,
        'ci_width': ci_high - ci_low
    }

if __name__ == '__main__':
    print("Reliability module defined.")
