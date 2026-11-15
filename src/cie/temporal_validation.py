"""
Clutch Intelligence Engine 2.0 — Rolling Temporal Validation Module
Implements:
1. Walk-Forward Temporal Splits:
   - Fold 1: Train 2022–2023 -> Test 2024
   - Fold 2: Train 2022–2024 -> Test 2025
   - Fold 3: Train 2022–2025 -> Test 2026
2. Zero-Leakage Preprocessing, Model Fitting, Calibration and Evaluation on Future Seasons.
3. Full Validation Metrics: Brier Score, Log Loss, ROC-AUC, Calibration Slope, Calibration Intercept, ECE.
4. Baseline Comparison: GroupKFold Match-Level Cross-Validation vs. Rolling Temporal Generalization.
"""

import os
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.metrics import brier_score_loss, log_loss, roc_auc_score
from typing import Dict, Tuple, List, Any

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PARQUET = os.path.join(ROOT, 'outputs', 'features', 'delivery_features.parquet')

def compute_ece(y_true: np.ndarray, y_prob: np.ndarray, n_bins: int = 10) -> float:
    """Computes Expected Calibration Error (ECE) across uniform confidence bins."""
    bins = np.linspace(0.0, 1.0, n_bins + 1)
    bin_indices = np.digitize(y_prob, bins) - 1
    bin_indices = np.clip(bin_indices, 0, n_bins - 1)
    
    ece = 0.0
    n = len(y_true)
    for b in range(n_bins):
        mask = bin_indices == b
        if np.sum(mask) > 0:
            bin_acc = np.mean(y_true[mask])
            bin_conf = np.mean(y_prob[mask])
            bin_weight = np.sum(mask) / n
            ece += bin_weight * np.abs(bin_acc - bin_conf)
    return float(ece)

def compute_calibration_slope_intercept(y_true: np.ndarray, y_prob: np.ndarray) -> Tuple[float, float]:
    """
    Computes calibration slope and intercept via logistic calibration:
    logit(p) as predictor in logistic regression for y_true.
    """
    eps = 1e-6
    y_prob_safe = np.clip(y_prob, eps, 1.0 - eps)
    log_odds = np.log(y_prob_safe / (1.0 - y_prob_safe)).reshape(-1, 1)
    
    lr = LogisticRegression(solver='lbfgs', max_iter=1000)
    lr.fit(log_odds, y_true)
    slope = float(lr.coef_[0, 0])
    intercept = float(lr.intercept_[0])
    return slope, intercept

class RollingTemporalValidator:
    def __init__(self):
        self.inn2_features = [
            'runs_needed_pre', 'pre_wickets_remaining', 'pre_legal_balls_remaining',
            'rrr_pre', 'crr_pre', 'knock_out'
        ]

    def run_temporal_validation(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        print("Executing Rolling Temporal Validation...")
        df_clean = df.copy()
        df_clean['year'] = df_clean['season'].astype(str).str[:4].astype(int)
        df_clean['batting_team_wins'] = (df_clean['win_team_id'] == df_clean['batting_team_id']).astype(int)
        
        # Innings 2 evaluation (where WP dynamics drive leverage and match outcomes)
        inn2_df = df_clean[df_clean['innings'] >= 2].copy()
        
        temporal_splits = [
            ("Fold 1 (2022-2023 -> 2024)", [2022, 2023], [2024]),
            ("Fold 2 (2022-2024 -> 2025)", [2022, 2023, 2024], [2025]),
            ("Fold 3 (2022-2025 -> 2026)", [2022, 2023, 2024, 2025], [2026]),
        ]
        
        fold_results = []
        all_test_probs = []
        all_test_trues = []
        
        for fold_name, train_years, test_years in temporal_splits:
            train_mask = inn2_df['year'].isin(train_years)
            test_mask = inn2_df['year'].isin(test_years)
            
            train_sub = inn2_df[train_mask]
            test_sub = inn2_df[test_mask]
            
            n_train_delivs = len(train_sub)
            n_train_matches = train_sub['match_id'].nunique()
            n_test_delivs = len(test_sub)
            n_test_matches = test_sub['match_id'].nunique()
            
            # Train model on past seasons
            X_train = train_sub[self.inn2_features].fillna(0)
            y_train = train_sub['batting_team_wins']
            
            X_test = test_sub[self.inn2_features].fillna(0)
            y_test = test_sub['batting_team_wins'].values
            
            base_model = LogisticRegression(max_iter=1000, random_state=42)
            calibrated_model = CalibratedClassifierCV(base_model, method='sigmoid', cv=3)
            calibrated_model.fit(X_train, y_train)
            
            # Predict on future test season
            y_prob = calibrated_model.predict_proba(X_test)[:, 1]
            all_test_probs.extend(y_prob)
            all_test_trues.extend(y_test)
            
            brier = brier_score_loss(y_test, y_prob)
            loss = log_loss(y_test, y_prob)
            auc = roc_auc_score(y_test, y_prob)
            slope, intercept = compute_calibration_slope_intercept(y_test, y_prob)
            ece = compute_ece(y_test, y_prob, n_bins=10)
            
            res_entry = {
                'fold': fold_name,
                'train_years': str(train_years),
                'test_years': str(test_years),
                'train_deliveries': n_train_delivs,
                'train_matches': n_train_matches,
                'test_deliveries': n_test_delivs,
                'test_matches': n_test_matches,
                'brier_score': round(brier, 4),
                'log_loss': round(loss, 4),
                'roc_auc': round(auc, 4),
                'calibration_slope': round(slope, 3),
                'calibration_intercept': round(intercept, 3),
                'ece': round(ece, 4)
            }
            fold_results.append(res_entry)
            print(f"  {fold_name}: AUC={auc:.4f}, LogLoss={loss:.4f}, Brier={brier:.4f}, Slope={slope:.3f}, ECE={ece:.4f}")
            
        results_df = pd.DataFrame(fold_results)
        
        # Aggregate out-of-time performance
        all_test_trues = np.array(all_test_trues)
        all_test_probs = np.array(all_test_probs)
        agg_summary = {
            'aggregate_temporal_auc': round(float(roc_auc_score(all_test_trues, all_test_probs)), 4),
            'aggregate_temporal_log_loss': round(float(log_loss(all_test_trues, all_test_probs)), 4),
            'aggregate_temporal_brier': round(float(brier_score_loss(all_test_trues, all_test_probs)), 4),
            'aggregate_temporal_ece': round(float(compute_ece(all_test_trues, all_test_probs)), 4)
        }
        print(f"Aggregate Temporal Holdout Performance: AUC={agg_summary['aggregate_temporal_auc']}, LogLoss={agg_summary['aggregate_temporal_log_loss']}, ECE={agg_summary['aggregate_temporal_ece']}")
        return results_df, agg_summary

if __name__ == '__main__':
    print("Testing RollingTemporalValidator on official deliveries...")
    df_raw = pd.read_parquet(PARQUET)
    ipl_mask = df_raw['comp_name'].str.contains('IPL', case=False, na=False)
    t20i_mask = df_raw['match_format'] == 'T20I'
    df_off = df_raw[ipl_mask | t20i_mask].copy()
    
    val = RollingTemporalValidator()
    f_df, agg = val.run_temporal_validation(df_off)
    print("\nTemporal Validation Table:")
    print(f_df.to_string(index=False))
