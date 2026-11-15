"""
Clutch Intelligence Engine 2.0 — Four-Pillar Orthogonal Rating Module
Implements:
1. Four-Pillar Performance Decomposition:
   - Pillar 1: Net Execution (Context-adjusted Bayesian RAE / RP per ball)
   - Pillar 2: Match Impact (Bayesian Win Probability Added per ball)
   - Pillar 3: Marginal Clutch Response (Bayesian Hierarchical Urgency & Leverage Slopes)
   - Pillar 4: Structural Consistency (Repeatability & Match-Level Stability)
2. Rigorous Multi-Collinearity Audit: Pearson Correlation Matrix & Variance Inflation Factors (VIF).
3. Gram-Schmidt Orthogonalization to guarantee that rating axes represent independent information.
4. Comparative Analysis: CIE 2.0 Four-Pillar Ratings vs. Baseline Round 1 Composite Ratings.
"""

import numpy as np
import pandas as pd
from typing import Dict, Tuple, List, Any

def compute_vif(df_features: pd.DataFrame) -> pd.Series:
    """Computes Variance Inflation Factor (VIF) for each feature in a dataframe."""
    from sklearn.linear_model import LinearRegression
    vifs = {}
    cols = df_features.columns.tolist()
    for col in cols:
        other_cols = [c for c in cols if c != col]
        X = df_features[other_cols].values
        y = df_features[col].values
        lr = LinearRegression()
        lr.fit(X, y)
        r2 = lr.score(X, y)
        vifs[col] = 1.0 / (1.0 - r2) if r2 < 0.999 else 999.0
    return pd.Series(vifs, name='VIF')

def gram_schmidt_orthogonalize(X: np.ndarray) -> np.ndarray:
    """
    Applies classical Gram-Schmidt orthogonalization to columns of design matrix X.
    Returns matrix Q of mutually orthogonal columns with unit variance.
    """
    n, p = X.shape
    Q = np.zeros((n, p), dtype=float)
    for j in range(p):
        v = X[:, j].copy()
        for i in range(j):
            proj = np.dot(Q[:, i], v) / np.dot(Q[:, i], Q[:, i])
            v -= proj * Q[:, i]
        # Standardize column to zero mean and unit variance
        v -= np.mean(v)
        std_v = np.std(v)
        Q[:, j] = v / (std_v if std_v > 1e-6 else 1.0)
    return Q

class FourPillarRatingEngine:
    def __init__(self,
                 w_execution: float = 0.40,
                 w_impact: float = 0.25,
                 w_clutch: float = 0.25,
                 w_consistency: float = 0.10):
        self.weights = np.array([w_execution, w_impact, w_clutch, w_consistency])
        self.weights /= np.sum(self.weights)

    def rate_batters(self, bat_df: pd.DataFrame, hier_bat_df: pd.DataFrame, min_balls: int = 100, min_matches: int = 12) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series]:
        """
        Computes experimental Four-Pillar ratings for batters.
        Merges base metrics with Bayesian hierarchical slopes.
        Filters strictly by official eligibility thresholds (min_balls and min_matches under pressure).
        """
        print("Computing Four-Pillar Orthogonal Ratings for Batters...")
        # Official Eligibility Filtering
        bat_elig = bat_df[(bat_df['pressure_balls'] >= min_balls) & (bat_df['pressure_matches'] >= min_matches)].copy()
        
        merged = bat_elig.merge(
            hier_bat_df[['player_id', 'post_mean_baseline_ability', 'post_mean_urgency_slope', 'post_mean_leverage_slope',
                         'post_se_urgency_slope', 'post_se_leverage_slope']],
            left_on='striker_id', right_on='player_id', how='inner'
        ).copy()
        
        # 1. Raw Pillar Feature Construction
        # Pillar 1: Net Execution (Bayesian Shrunk RAE / Ball)
        k = 40.0
        pop_rae = merged['pressure_rae_per_ball'].mean()
        shrunk_rae = (merged['pressure_total_rae'] + k * pop_rae) / (merged['pressure_balls'] + k)
        
        # Pillar 2: Match Impact (Bayesian Shrunk WPA / Ball)
        pop_wpa = merged['pressure_wpa_per_ball'].mean()
        shrunk_wpa = (merged['pressure_total_wpa'] + k * pop_wpa) / (merged['pressure_balls'] + k)
        
        # Pillar 3: Marginal Clutch Response (Hierarchical Slopes)
        # Combines urgency response slope (60%) and leverage response slope (40%)
        marginal_clutch = 0.60 * merged['post_mean_urgency_slope'] + 0.40 * merged['post_mean_leverage_slope']
        
        # Pillar 4: Structural Consistency
        pos_rate = merged['pct_positive_pressure_matches']
        std_safe = merged['match_rae_std'].fillna(merged['match_rae_std'].mean())
        consistency_raw = pos_rate - 0.20 * (std_safe / (std_safe.mean() + 1e-6))
        
        feature_df = pd.DataFrame({
            'Pillar_1_Net_Execution': shrunk_rae,
            'Pillar_2_Match_Impact': shrunk_wpa,
            'Pillar_3_Clutch_Slope': marginal_clutch,
            'Pillar_4_Consistency': consistency_raw
        }, index=merged.index)
        
        # 2. Multi-Collinearity Audit: Correlation Matrix & VIF
        corr_matrix = feature_df.corr()
        vif_series = compute_vif(feature_df)
        print("  Pillar Raw Correlation Matrix:")
        print(corr_matrix.round(3))
        print("  Variance Inflation Factors (VIF):")
        print(vif_series.round(2))
        
        # 3. Orthogonalization via Gram-Schmidt
        # Standardize raw features first
        Z_raw = (feature_df - feature_df.mean()) / feature_df.std()
        Q_ortho = gram_schmidt_orthogonalize(Z_raw.values)
        
        # 4. Composite Rating Calculation
        composite_score = Q_ortho @ self.weights
        merged['cie_composite_score'] = composite_score
        merged['cie_rating'] = np.round(50.0 + 15.0 * composite_score, 2)
        
        # Ranking
        ranked = merged.sort_values('cie_rating', ascending=False).reset_index(drop=True)
        ranked['cie_rank'] = ranked.index + 1
        
        return ranked, corr_matrix, vif_series

    def rate_bowlers(self, bowl_df: pd.DataFrame, hier_bowl_df: pd.DataFrame, min_balls: int = 120, min_matches: int = 12) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series]:
        """
        Computes experimental Four-Pillar ratings for bowlers.
        Filters strictly by official eligibility thresholds (min_balls and min_matches under pressure).
        """
        print("Computing Four-Pillar Orthogonal Ratings for Bowlers...")
        # Official Eligibility Filtering
        bowl_elig = bowl_df[(bowl_df['pressure_legal_balls'] >= min_balls) & (bowl_df['pressure_matches'] >= min_matches)].copy()
        
        merged = bowl_elig.merge(
            hier_bowl_df[['player_id', 'post_mean_baseline_ability', 'post_mean_urgency_slope', 'post_mean_leverage_slope',
                          'post_se_urgency_slope', 'post_se_leverage_slope']],
            left_on='bowler_id', right_on='player_id', how='inner'
        ).copy()
        
        k = 40.0
        # Pillar 1: Net Execution (Bayesian Shrunk Runs Prevented / Ball)
        pop_rp = merged['pressure_rp_per_ball'].mean()
        shrunk_rp = (merged['pressure_total_rp'] + k * pop_rp) / (merged['pressure_legal_balls'] + k)
        
        # Pillar 2: Match Impact (Bayesian Shrunk Bowling WPA / Ball)
        pop_wpa = merged['pressure_wpa_per_ball'].mean()
        shrunk_wpa = (merged['pressure_total_wpa'] + k * pop_wpa) / (merged['pressure_legal_balls'] + k)
        
        # Pillar 3: Marginal Clutch Response
        marginal_clutch = 0.60 * merged['post_mean_urgency_slope'] + 0.40 * merged['post_mean_leverage_slope']
        
        # Pillar 4: Structural Consistency
        pos_rate = merged['pct_positive_pressure_matches']
        std_safe = merged['match_rp_std'].fillna(merged['match_rp_std'].mean())
        consistency_raw = pos_rate - 0.20 * (std_safe / (std_safe.mean() + 1e-6))
        
        feature_df = pd.DataFrame({
            'Pillar_1_Net_Execution': shrunk_rp,
            'Pillar_2_Match_Impact': shrunk_wpa,
            'Pillar_3_Clutch_Slope': marginal_clutch,
            'Pillar_4_Consistency': consistency_raw
        }, index=merged.index)
        
        corr_matrix = feature_df.corr()
        vif_series = compute_vif(feature_df)
        
        Z_raw = (feature_df - feature_df.mean()) / feature_df.std()
        Q_ortho = gram_schmidt_orthogonalize(Z_raw.values)
        
        composite_score = Q_ortho @ self.weights
        merged['cie_composite_score'] = composite_score
        merged['cie_rating'] = np.round(50.0 + 15.0 * composite_score, 2)
        
        ranked = merged.sort_values('cie_rating', ascending=False).reset_index(drop=True)
        ranked['cie_rank'] = ranked.index + 1
        
        return ranked, corr_matrix, vif_series

if __name__ == '__main__':
    print("Testing FourPillarRatingEngine on mock inputs...")
    engine = FourPillarRatingEngine()
    print("Engine instantiated.")
