"""
Clutch Intelligence Engine 2.0 — Bayesian Hierarchical Player Modelling Module
Implements:
1. Batting Hierarchical Model: RAE_ij = alpha + u_i + beta_i * Urgency_ij + theta_i * Leverage_ij + eps_ij
2. Bowling Hierarchical Model: RP_ij = alpha_b + v_i + lambda_i * Urgency_ij + phi_i * Leverage_ij + eps_ij
3. Partial Pooling with Closed-Form Empirical Bayes Posterior Means and Exact Credible Intervals.
4. Synthetic Parameter Recovery Suite verifying that true player-specific effects are recovered.
5. Non-Double-Counting Context Principle: Operates directly on out-of-fold residuals (RAE and RP).
"""

import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, Tuple, List, Any

class BayesianHierarchicalEngine:
    def __init__(self, prior_weight: float = 40.0):
        self.prior_weight = prior_weight
        self.batter_posteriors = None
        self.bowler_posteriors = None

    def fit_hierarchical_random_slopes(
        self,
        player_ids: np.ndarray,
        X_mat: np.ndarray,
        y_vec: np.ndarray,
        feature_names: List[str]
    ) -> pd.DataFrame:
        """
        Fits Lindley-Smith / Henderson closed-form Empirical Bayes random intercepts and slopes.
        Yields exact posterior means and posterior covariance (credible intervals) per player.
        """
        unique_players, inverse_indices, counts = np.unique(player_ids, return_inverse=True, return_counts=True)
        n_players = len(unique_players)
        p = X_mat.shape[1] # [Intercept, Urgency, Leverage]
        
        # 1. Grand Fixed Effect (Population Mean)
        # OLS on all data
        XtX_grand = X_mat.T @ X_mat
        Xty_grand = X_mat.T @ y_vec
        mu_hat = np.linalg.solve(XtX_grand + 1e-6 * np.eye(p), Xty_grand)
        
        # Estimate global residual variance sigma^2
        residuals = y_vec - X_mat @ mu_hat
        sigma2_hat = float(np.var(residuals, ddof=p))
        
        # 2. Estimate Population Covariance Matrix of Random Effects (Sigma)
        # Using empirical variance of individual unpooled OLS estimates
        unpooled_betas = []
        valid_counts = []
        for i, pid in enumerate(unique_players):
            idx = np.where(inverse_indices == i)[0]
            if len(idx) >= max(p + 2, 10):
                Xi = X_mat[idx]
                yi = y_vec[idx]
                try:
                    b_ols = np.linalg.solve(Xi.T @ Xi + 1e-4 * np.eye(p), Xi.T @ yi)
                    unpooled_betas.append(b_ols)
                    valid_counts.append(len(idx))
                except np.linalg.LinAlgError:
                    pass
                    
        if len(unpooled_betas) >= 5:
            Sigma_hat = np.cov(np.array(unpooled_betas).T)
            # Add small regularization to ensure positive definiteness
            Sigma_hat += 1e-4 * np.eye(p)
        else:
            Sigma_hat = np.diag([0.15**2, 0.25**2, 0.20**2])
            
        Sigma_inv = np.linalg.inv(Sigma_hat)
        
        # 3. Compute Posterior Mean and Posterior Variance per Player
        results = []
        for i, pid in enumerate(unique_players):
            idx = np.where(inverse_indices == i)[0]
            Xi = X_mat[idx]
            yi = y_vec[idx]
            n_i = len(idx)
            
            XtX_i = Xi.T @ Xi
            Xty_i = Xi.T @ yi
            
            # Posterior covariance: V_i = (XtX_i / sigma2 + Sigma_inv)^(-1)
            prec_i = (XtX_i / sigma2_hat) + Sigma_inv
            post_cov_i = np.linalg.inv(prec_i)
            
            # Posterior mean: beta_hat_i = V_i @ (Xty_i / sigma2 + Sigma_inv @ mu_hat)
            post_mean_i = post_cov_i @ ((Xty_i / sigma2_hat) + (Sigma_inv @ mu_hat))
            post_se_i = np.sqrt(np.clip(np.diag(post_cov_i), 1e-6, None))
            
            res_dict = {
                'player_id': pid,
                'sample_deliveries': n_i
            }
            for k, fname in enumerate(feature_names):
                m_val = float(post_mean_i[k])
                se_val = float(post_se_i[k])
                res_dict[f'post_mean_{fname}'] = m_val
                res_dict[f'post_se_{fname}'] = se_val
                res_dict[f'post_ci95_low_{fname}'] = m_val - 1.96 * se_val
                res_dict[f'post_ci95_high_{fname}'] = m_val + 1.96 * se_val
                
            results.append(res_dict)
            
        return pd.DataFrame(results)

    def fit_batters(self, df: pd.DataFrame, min_balls: int = 100, min_matches: int = 12) -> pd.DataFrame:
        """
        Fits Bayesian hierarchical model for batters on context-adjusted RAE.
        RAE_ij = alpha + u_i + beta_i * Urgency + theta_i * Leverage + eps_ij
        """
        print("Fitting Bayesian Hierarchical Model for Batters...")
        # Only faced deliveries
        bat_df = df[df['is_batter_ball']].copy()
        
        # Eligible check
        player_summary = bat_df.groupby('striker_id').agg(
            total_balls=('runs', 'count'),
            total_matches=('match_id', 'nunique'),
            striker_name=('striker_name', 'first')
        ).reset_index()
        eligible_ids = player_summary[
            (player_summary['total_balls'] >= min_balls) &
            (player_summary['total_matches'] >= min_matches)
        ]['striker_id'].unique()
        
        eligible_df = bat_df[bat_df['striker_id'].isin(eligible_ids)].copy()
        print(f"  Eligible batters modeled: {len(eligible_ids)} across {len(eligible_df):,} deliveries")
        
        # Design matrix: [Intercept, p_urgency, p_leverage]
        X = np.column_stack([
            np.ones(len(eligible_df)),
            eligible_df['p_urgency'].values,
            eligible_df['p_leverage'].values
        ])
        y = eligible_df['runs_above_expectation'].values
        pids = eligible_df['striker_id'].values
        
        posteriors = self.fit_hierarchical_random_slopes(
            pids, X, y, ['baseline_ability', 'urgency_slope', 'leverage_slope']
        )
        posteriors = posteriors.merge(player_summary[['striker_id', 'striker_name', 'total_matches']], left_on='player_id', right_on='striker_id')
        self.batter_posteriors = posteriors
        return posteriors

    def fit_bowlers(self, df: pd.DataFrame, min_balls: int = 120, min_matches: int = 12) -> pd.DataFrame:
        """
        Fits Bayesian hierarchical model for bowlers on context-adjusted Runs Prevented (RP).
        RP_ij = alpha_b + v_i + lambda_i * Urgency + phi_i * Leverage + eps_ij
        """
        print("Fitting Bayesian Hierarchical Model for Bowlers...")
        bowl_df = df[df['is_legal']].copy()
        
        player_summary = bowl_df.groupby('bowler_id').agg(
            total_balls=('is_legal', 'sum'),
            total_matches=('match_id', 'nunique'),
            bowler_name=('bowler_name', 'first')
        ).reset_index()
        eligible_ids = player_summary[
            (player_summary['total_balls'] >= min_balls) &
            (player_summary['total_matches'] >= min_matches)
        ]['bowler_id'].unique()
        
        eligible_df = bowl_df[bowl_df['bowler_id'].isin(eligible_ids)].copy()
        print(f"  Eligible bowlers modeled: {len(eligible_ids)} across {len(eligible_df):,} deliveries")
        
        X = np.column_stack([
            np.ones(len(eligible_df)),
            eligible_df['p_urgency'].values,
            eligible_df['p_leverage'].values
        ])
        y = eligible_df['runs_prevented'].values
        pids = eligible_df['bowler_id'].values
        
        posteriors = self.fit_hierarchical_random_slopes(
            pids, X, y, ['baseline_ability', 'urgency_slope', 'leverage_slope']
        )
        posteriors = posteriors.merge(player_summary[['bowler_id', 'bowler_name', 'total_matches']], left_on='player_id', right_on='bowler_id')
        self.bowler_posteriors = posteriors
        return posteriors

    @staticmethod
    def run_parameter_recovery_test(n_players: int = 40, n_obs_per_player: int = 200) -> Dict[str, float]:
        """
        Synthetic validation test: Generates ground-truth player effects, fits the model,
        and verifies that true parameters are recovered with high correlation.
        """
        print("Executing Synthetic Parameter Recovery Test...")
        np.random.seed(42)
        true_mu = np.array([0.05, 0.25, 0.18]) # alpha, beta, theta
        true_sigma_diag = np.array([0.25, 0.35, 0.30])
        Sigma_true = np.diag(true_sigma_diag**2)
        sigma2_true = 0.50
        
        true_betas = np.random.multivariate_normal(true_mu, Sigma_true, n_players)
        
        all_X = []
        all_y = []
        pids = []
        for i in range(n_players):
            Xi = np.column_stack([
                np.ones(n_obs_per_player),
                np.random.uniform(0.1, 0.9, n_obs_per_player),
                np.random.uniform(0.1, 0.9, n_obs_per_player)
            ])
            yi = Xi @ true_betas[i] + np.random.normal(0, np.sqrt(sigma2_true), n_obs_per_player)
            all_X.append(Xi)
            all_y.append(yi)
            pids.extend([i] * n_obs_per_player)
            
        X_mat = np.vstack(all_X)
        y_vec = np.concatenate(all_y)
        pid_arr = np.array(pids)
        
        engine = BayesianHierarchicalEngine()
        res_df = engine.fit_hierarchical_random_slopes(
            pid_arr, X_mat, y_vec, ['baseline', 'urgency', 'leverage']
        )
        
        est_u = res_df['post_mean_baseline'].values
        est_beta = res_df['post_mean_urgency'].values
        est_theta = res_df['post_mean_leverage'].values
        
        corr_u = float(np.corrcoef(true_betas[:, 0], est_u)[0, 1])
        corr_beta = float(np.corrcoef(true_betas[:, 1], est_beta)[0, 1])
        corr_theta = float(np.corrcoef(true_betas[:, 2], est_theta)[0, 1])
        
        metrics = {
            'recovery_corr_baseline_ability': corr_u,
            'recovery_r2_baseline_ability': corr_u**2,
            'recovery_corr_urgency_slope': corr_beta,
            'recovery_r2_urgency_slope': corr_beta**2,
            'recovery_corr_leverage_slope': corr_theta,
            'recovery_r2_leverage_slope': corr_theta**2,
        }
        print(f"  Parameter Recovery: Baseline Ability Corr={metrics['recovery_corr_baseline_ability']:.4f} (R2={metrics['recovery_r2_baseline_ability']:.4f})")
        print(f"  Parameter Recovery: Urgency Slope Corr={metrics['recovery_corr_urgency_slope']:.4f} (R2={metrics['recovery_r2_urgency_slope']:.4f})")
        print(f"  Parameter Recovery: Leverage Slope Corr={metrics['recovery_corr_leverage_slope']:.4f} (R2={metrics['recovery_r2_leverage_slope']:.4f})")
        return metrics

if __name__ == '__main__':
    print("Testing BayesianHierarchicalEngine...")
    test_metrics = BayesianHierarchicalEngine.run_parameter_recovery_test()
    assert test_metrics['recovery_corr_baseline_ability'] > 0.70, "Baseline ability recovery failed"
    assert test_metrics['recovery_corr_urgency_slope'] > 0.60, "Urgency slope recovery failed"
    assert test_metrics['recovery_corr_leverage_slope'] > 0.70, "Leverage slope recovery failed"
    print("All parameter recovery thresholds met. Bayesian Hierarchical Engine verified.")
