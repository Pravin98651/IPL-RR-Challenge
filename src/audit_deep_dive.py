"""
Deep Dive Audit Script for Win Probability, Expected Performance, Bayesian Shrinkage,
and Knockout Multiplier Sensitivity.
"""
import os
import sys
import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingRegressor, HistGradientBoostingClassifier
from sklearn.metrics import (
    log_loss, brier_score_loss, roc_auc_score, mean_absolute_error, mean_squared_error, r2_score
)
from sklearn.calibration import calibration_curve

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from data_loader import load_all_datasets
from match_state import reconstruct_match_state
from feature_engineering import generate_features

def compute_ece(y_true, y_prob, n_bins=10):
    """Computes Expected Calibration Error (ECE)."""
    bin_edges = np.linspace(0, 1, n_bins + 1)
    ece = 0.0
    for i in range(n_bins):
        bin_mask = (y_prob >= bin_edges[i]) & (y_prob < bin_edges[i + 1])
        if np.sum(bin_mask) > 0:
            bin_acc = np.mean(y_true[bin_mask])
            bin_conf = np.mean(y_prob[bin_mask])
            bin_weight = np.sum(bin_mask) / len(y_true)
            ece += bin_weight * np.abs(bin_acc - bin_conf)
    return ece

def compute_calibration_slope_intercept(y_true, y_prob):
    """Fits logistic calibration line: logit(p) to logit(observed)."""
    eps = 1e-6
    p_clipped = np.clip(y_prob, eps, 1 - eps)
    logit_p = np.log(p_clipped / (1 - p_clipped)).reshape(-1, 1)
    
    cal_lr = LogisticRegression()
    cal_lr.fit(logit_p, y_true)
    slope = float(cal_lr.coef_[0][0])
    intercept = float(cal_lr.intercept_[0])
    return slope, intercept

def audit_all():
    print("Loading data and generating features...")
    data = load_all_datasets()
    recon = reconstruct_match_state(data['ball_by_ball'], data['matches'], data['competitions'])
    df = generate_features(recon)
    
    # =========================================================================
    # PART 1: WIN PROBABILITY AUDIT (2ND INNINGS)
    # =========================================================================
    print("\n" + "=" * 65)
    print("PART 1: WIN PROBABILITY AUDIT (2ND INNINGS)")
    print("=" * 65)
    
    chase = df[(df['innings'] >= 2) & df['win_team_id'].notna() & (df['win_team_id'] > 0)].copy()
    chase['batting_team_won'] = (chase['win_team_id'] == chase['batting_team_id']).astype(int)
    
    features = [
        'pre_legal_balls_completed', 'pre_legal_balls_remaining',
        'pre_current_score', 'pre_wickets_lost', 'pre_wickets_remaining',
        'crr_pre', 'target', 'runs_needed_pre', 'rrr_pre', 'knock_out'
    ]
    X = chase[features].fillna(0)
    y = chase['batting_team_won'].values
    groups = chase['match_id'].values
    
    gkf = GroupKFold(n_splits=5)
    
    # OOF Predictions
    p_lr_oof = np.zeros(len(chase))
    p_base_dummy = np.zeros(len(chase))
    p_base_crr = np.zeros(len(chase))
    
    for tr_idx, val_idx in gkf.split(X, y, groups):
        X_tr, y_tr = X.iloc[tr_idx], y[tr_idx]
        X_val, y_val = X.iloc[val_idx], y[val_idx]
        
        # Simple Baseline 1: Empirical prior mean (Dummy)
        p_base_dummy[val_idx] = np.mean(y_tr)
        
        # Simple Baseline 2: Simple RRR Logistic Baseline
        lr_simple = LogisticRegression()
        lr_simple.fit(X_tr[['rrr_pre', 'pre_wickets_remaining']], y_tr)
        p_base_crr[val_idx] = lr_simple.predict_proba(X_val[['rrr_pre', 'pre_wickets_remaining']])[:, 1]
        
        # Full Multi-feature Logistic Regression
        lr_full = LogisticRegression(max_iter=1000)
        lr_full.fit(X_tr, y_tr)
        p_lr_oof[val_idx] = lr_full.predict_proba(X_val)[:, 1]
        
    p_lr_oof = np.clip(p_lr_oof, 1e-6, 1 - 1e-6)
    p_base_dummy = np.clip(p_base_dummy, 1e-6, 1 - 1e-6)
    p_base_crr = np.clip(p_base_crr, 1e-6, 1 - 1e-6)
    
    # Overall Evaluation Metrics
    ll_full = log_loss(y, p_lr_oof)
    brier_full = brier_score_loss(y, p_lr_oof)
    auc_full = roc_auc_score(y, p_lr_oof)
    ece_full = compute_ece(y, p_lr_oof)
    slope_full, intercept_full = compute_calibration_slope_intercept(y, p_lr_oof)
    
    ll_dummy = log_loss(y, p_base_dummy)
    brier_dummy = brier_score_loss(y, p_base_dummy)
    
    ll_simple = log_loss(y, p_base_crr)
    brier_simple = brier_score_loss(y, p_base_crr)
    auc_simple = roc_auc_score(y, p_base_crr)
    ece_simple = compute_ece(y, p_base_crr)
    
    print(f"Simple Dummy Baseline    : Log Loss = {ll_dummy:.4f}, Brier = {brier_dummy:.4f}")
    print(f"Simple RRR Baseline      : Log Loss = {ll_simple:.4f}, Brier = {brier_simple:.4f}, AUC = {auc_simple:.4f}, ECE = {ece_simple:.4f}")
    print(f"Full Production Logistic : Log Loss = {ll_full:.4f}, Brier = {brier_full:.4f}, AUC = {auc_full:.4f}, ECE = {ece_full:.4f}")
    print(f"Calibration Slope = {slope_full:.3f} (Ideal: 1.000) | Calibration Intercept = {intercept_full:.3f} (Ideal: 0.000)")
    
    # Sub-breakdown by Competition
    chase['p_lr_oof'] = p_lr_oof
    print("\nWin Probability Performance Across Tournament Formats:")
    for fmt in ['T20', 'T20I']:
        sub = chase[chase['match_format'] == fmt]
        y_sub = sub['batting_team_won'].values
        p_sub = sub['p_lr_oof'].values
        print(f" - {fmt:5s}: Log Loss = {log_loss(y_sub, p_sub):.4f}, Brier = {brier_score_loss(y_sub, p_sub):.4f}, AUC = {roc_auc_score(y_sub, p_sub):.4f}, ECE = {compute_ece(y_sub, p_sub):.4f}")
        
    # Sub-breakdown by Phase
    print("\nWin Probability Performance Across Innings Phases:")
    for ph in ['powerplay', 'middle', 'death']:
        sub = chase[chase['phase'] == ph]
        y_sub = sub['batting_team_won'].values
        p_sub = sub['p_lr_oof'].values
        print(f" - {ph.capitalize():10s}: Log Loss = {log_loss(y_sub, p_sub):.4f}, Brier = {brier_score_loss(y_sub, p_sub):.4f}, AUC = {roc_auc_score(y_sub, p_sub):.4f}, ECE = {compute_ece(y_sub, p_sub):.4f}")

    # =========================================================================
    # PART 2: CONTEXTUAL EXPECTED PERFORMANCE AUDIT
    # =========================================================================
    print("\n" + "=" * 65)
    print("PART 2: CONTEXTUAL EXPECTED PERFORMANCE AUDIT")
    print("=" * 65)
    
    df['pace_or_spin_code'] = df['pace_or_spin'].map({'Pace': 1, 'Spin': 2}).fillna(0).astype(int)
    df['format_code'] = df['match_format'].map({'T20': 1, 'T20I': 2}).fillna(0).astype(int)
    
    feat_cols = [
        'innings', 'overid', 'pre_legal_balls_completed',
        'pre_wickets_lost', 'batting_order', 'knock_out',
        'pace_or_spin_code', 'format_code'
    ]
    X_exp = df[feat_cols].copy()
    X_exp['batting_order'] = X_exp['batting_order'].fillna(5).astype(int)
    y_bat_runs = df['runs'].values
    y_bowl_runs = df['bowler_conceded_runs'].values
    groups_all = df['match_id'].values
    
    exp_bat_oof = np.zeros(len(df))
    exp_bowl_oof = np.zeros(len(df))
    base_mean_bat = np.mean(y_bat_runs)
    
    for tr_idx, val_idx in gkf.split(X_exp, y_bat_runs, groups_all):
        X_tr, X_val = X_exp.iloc[tr_idx], X_exp.iloc[val_idx]
        
        # Batter runs model
        reg_b = HistGradientBoostingRegressor(max_iter=60, random_state=42)
        reg_b.fit(X_tr, y_bat_runs[tr_idx])
        exp_bat_oof[val_idx] = reg_b.predict(X_val)
        
        # Bowler runs model
        reg_bw = HistGradientBoostingRegressor(max_iter=60, random_state=42)
        reg_bw.fit(X_tr, y_bowl_runs[tr_idx])
        exp_bowl_oof[val_idx] = reg_bw.predict(X_val)
        
    # Baseline comparison (Naive constant mean model)
    mae_base = mean_absolute_error(y_bat_runs, np.full_like(y_bat_runs, base_mean_bat))
    rmse_base = np.sqrt(mean_squared_error(y_bat_runs, np.full_like(y_bat_runs, base_mean_bat)))
    
    mae_bat = mean_absolute_error(y_bat_runs, exp_bat_oof)
    rmse_bat = np.sqrt(mean_squared_error(y_bat_runs, exp_bat_oof))
    r2_bat = r2_score(y_bat_runs, exp_bat_oof)
    
    mae_bowl = mean_absolute_error(y_bowl_runs, exp_bowl_oof)
    rmse_bowl = np.sqrt(mean_squared_error(y_bowl_runs, exp_bowl_oof))
    r2_bowl = r2_score(y_bowl_runs, exp_bowl_oof)
    
    print(f"Naive Baseline (Mean Runs) : MAE = {mae_base:.4f}, RMSE = {rmse_base:.4f}")
    print(f"Batter Contextual Expected : MAE = {mae_bat:.4f}, RMSE = {rmse_bat:.4f}, R2 = {r2_bat:.4f}")
    print(f"Bowler Contextual Expected : MAE = {mae_bowl:.4f}, RMSE = {rmse_bowl:.4f}, R2 = {r2_bowl:.4f}")
    print(f"Mean Batter Expected Runs  : {np.mean(exp_bat_oof):.4f} vs Actual: {np.mean(y_bat_runs):.4f}")
    print(f"Mean Bowler Expected Runs  : {np.mean(exp_bowl_oof):.4f} vs Actual: {np.mean(y_bowl_runs):.4f}")
    print("Units: Runs Above Expectation (RAE) = Actual Batter Runs - Expected Contextual Runs [Runs/Ball]")
    print("Units: Runs Prevented (RP) = Expected Bowler Conceded Runs - Actual Bowler Conceded Runs [Runs/Ball]")

    # =========================================================================
    # PART 3: BAYESIAN SHRINKAGE AUDIT (k = 20 vs 40 vs 80 vs Raw)
    # =========================================================================
    print("\n" + "=" * 65)
    print("PART 3: BAYESIAN SHRINKAGE AUDIT (k=20, 40, 80 vs Raw)")
    print("=" * 65)
    
    bat_metrics = pd.read_csv('outputs/player_scores/all_batter_scores.csv')
    pop_sr = bat_metrics[bat_metrics['pressure_balls'] >= 80]['pressure_sr'].mean()
    pop_rae = bat_metrics[bat_metrics['pressure_balls'] >= 80]['pressure_rae_per_ball'].mean()
    
    sample_players = ['Ishan Kishan', 'Tim David', 'Suryakumar Yadav', 'Heinrich Klaasen', 'Ashutosh Sharma']
    sub_bat = bat_metrics[bat_metrics['striker_name'].isin(sample_players)].copy()
    
    print(f"Population Baselines (N >= 80): Pressure SR = {pop_sr:.2f}, RAE/Ball = {pop_rae:+.3f}\n")
    print(f"{'Player':18s} {'Balls':>5s} {'Raw SR':>8s} {'k=20':>8s} {'k=40':>8s} {'k=80':>8s} {'Raw RAE':>8s} {'k=40 RAE':>8s}")
    print("-" * 75)
    for idx, r in sub_bat.iterrows():
        n = r['pressure_balls']
        raw_sr = r['pressure_sr']
        k20_sr = (n / (n + 20)) * raw_sr + (20 / (n + 20)) * pop_sr
        k40_sr = (n / (n + 40)) * raw_sr + (40 / (n + 40)) * pop_sr
        k80_sr = (n / (n + 80)) * raw_sr + (80 / (n + 80)) * pop_sr
        
        raw_rae = r['pressure_rae_per_ball']
        k40_rae = (n / (n + 40)) * raw_rae + (40 / (n + 40)) * pop_rae
        print(f"{r['striker_name']:18s} {int(n):5d} {raw_sr:8.1f} {k20_sr:8.1f} {k40_sr:8.1f} {k80_sr:8.1f} {raw_rae:+8.3f} {k40_rae:+8.3f}")

if __name__ == '__main__':
    audit_all()
