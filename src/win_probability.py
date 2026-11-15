"""
Win Probability, Leverage Index, and WPA Module.
Implements machine-learning win probability models with grouped cross-validation.
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import GroupKFold
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, log_loss, roc_auc_score
from xgboost import XGBClassifier
from typing import Dict, Tuple, Any

def train_and_evaluate_wp_models(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Performs 5-fold match-grouped cross-validation on Innings 2 chases
    comparing Logistic Regression and XGBoost.
    """
    chase = df[(df['innings'] == 2) & df['win_team_id'].notna() & (df['win_team_id'] > 0)].copy()
    chase['batting_team_won'] = (chase['win_team_id'] == chase['batting_team_id']).astype(int)
    
    features = [
        'pre_legal_balls_completed', 'pre_legal_balls_remaining',
        'pre_current_score', 'pre_wickets_lost', 'pre_wickets_remaining',
        'crr_pre', 'target', 'runs_needed_pre', 'rrr_pre', 'knock_out'
    ]
    
    X = chase[features].fillna(0)
    y = chase['batting_team_won']
    groups = chase['match_id']
    
    gkf = GroupKFold(n_splits=5)
    
    results = {
        'logistic_regression': {'log_loss': [], 'brier': [], 'auc': []},
        'xgboost': {'log_loss': [], 'brier': [], 'auc': []}
    }
    
    for tr_idx, val_idx in gkf.split(X, y, groups):
        X_tr, y_tr = X.iloc[tr_idx], y.iloc[tr_idx]
        X_val, y_val = X.iloc[val_idx], y.iloc[val_idx]
        
        # Logistic Regression
        lr = LogisticRegression(max_iter=1000)
        lr.fit(X_tr, y_tr)
        p_lr = np.clip(lr.predict_proba(X_val)[:, 1], 1e-6, 1 - 1e-6)
        results['logistic_regression']['log_loss'].append(log_loss(y_val, p_lr))
        results['logistic_regression']['brier'].append(brier_score_loss(y_val, p_lr))
        results['logistic_regression']['auc'].append(roc_auc_score(y_val, p_lr))
        
        # XGBoost
        xgb = XGBClassifier(n_estimators=80, max_depth=4, learning_rate=0.08, random_state=42, eval_metric='logloss')
        xgb.fit(X_tr, y_tr)
        p_xgb = np.clip(xgb.predict_proba(X_val)[:, 1], 1e-6, 1 - 1e-6)
        results['xgboost']['log_loss'].append(log_loss(y_val, p_xgb))
        results['xgboost']['brier'].append(brier_score_loss(y_val, p_xgb))
        results['xgboost']['auc'].append(roc_auc_score(y_val, p_xgb))
        
    summary = {
        'lr_mean_log_loss': float(np.mean(results['logistic_regression']['log_loss'])),
        'lr_mean_brier': float(np.mean(results['logistic_regression']['brier'])),
        'lr_mean_auc': float(np.mean(results['logistic_regression']['auc'])),
        'xgb_mean_log_loss': float(np.mean(results['xgboost']['log_loss'])),
        'xgb_mean_brier': float(np.mean(results['xgboost']['brier'])),
        'xgb_mean_auc': float(np.mean(results['xgboost']['auc']))
    }
    return summary

def compute_win_probability_and_wpa(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fits production Win Probability models and calculates pre/post WP, WPA, and Leverage Index.
    """
    df = df.copy()
    
    # --- 1. Innings 2 Chase Model ---
    chase_mask = (df['innings'] >= 2) & df['win_team_id'].notna() & (df['win_team_id'] > 0)
    chase_df = df[chase_mask].copy()
    chase_df['batting_team_won'] = (chase_df['win_team_id'] == chase_df['batting_team_id']).astype(int)
    
    features_chase_pre = [
        'pre_legal_balls_completed', 'pre_legal_balls_remaining',
        'pre_current_score', 'pre_wickets_lost', 'pre_wickets_remaining',
        'crr_pre', 'target', 'runs_needed_pre', 'rrr_pre', 'knock_out'
    ]
    features_chase_post = [
        'post_legal_balls_completed', 'post_legal_balls_remaining',
        'post_current_score', 'post_wickets_lost', 'post_wickets_remaining',
        'crr_post', 'target', 'runs_needed_post', 'rrr_post', 'knock_out'
    ]
    
    X_chase_pre = chase_df[features_chase_pre].fillna(0)
    y_chase = chase_df['batting_team_won']
    
    # Train robust Logistic Regression model for well-calibrated monotonic win probability
    lr_chase = LogisticRegression(max_iter=1000)
    lr_chase.fit(X_chase_pre, y_chase)
    
    # Predict pre and post WP for all chase deliveries
    all_chase_mask = (df['innings'] >= 2)
    X_all_chase_pre = df.loc[all_chase_mask, features_chase_pre].fillna(0)
    X_all_chase_post = df.loc[all_chase_mask, features_chase_post].fillna(0)
    X_all_chase_post.columns = features_chase_pre  # align column names
    
    wp_pre_chase = lr_chase.predict_proba(X_all_chase_pre)[:, 1]
    wp_post_chase = lr_chase.predict_proba(X_all_chase_post)[:, 1]
    
    # If target is reached on delivery (post_current_score >= target), WP is 1.0
    target_reached = df.loc[all_chase_mask, 'post_current_score'] >= df.loc[all_chase_mask, 'target']
    wp_post_chase = np.where(target_reached, 1.0, wp_post_chase)
    
    # If all out (post_wickets_lost >= 10) and target not reached, WP is 0.0
    all_out = (df.loc[all_chase_mask, 'post_wickets_lost'] >= 10) & (~target_reached)
    wp_post_chase = np.where(all_out, 0.0, wp_post_chase)
    
    df.loc[all_chase_mask, 'wp_pre'] = wp_pre_chase
    df.loc[all_chase_mask, 'wp_post'] = wp_post_chase
    
    # --- 2. Innings 1 Setting Target Model ---
    inn1_mask = (df['innings'] == 1) & df['win_team_id'].notna() & (df['win_team_id'] > 0)
    inn1_df = df[inn1_mask].copy()
    inn1_df['batting_team_won'] = (inn1_df['win_team_id'] == inn1_df['batting_team_id']).astype(int)
    
    features_inn1_pre = [
        'pre_legal_balls_completed', 'pre_legal_balls_remaining',
        'pre_current_score', 'pre_wickets_lost', 'pre_wickets_remaining',
        'crr_pre', 'projected_final_score', 'knock_out'
    ]
    features_inn1_post = [
        'post_legal_balls_completed', 'post_legal_balls_remaining',
        'post_current_score', 'post_wickets_lost', 'post_wickets_remaining',
        'crr_post', 'projected_final_score', 'knock_out'
    ]
    
    X_inn1_pre = inn1_df[features_inn1_pre].fillna(0)
    y_inn1 = inn1_df['batting_team_won']
    
    lr_inn1 = LogisticRegression(max_iter=1000)
    lr_inn1.fit(X_inn1_pre, y_inn1)
    
    all_inn1_mask = (df['innings'] == 1)
    X_all_inn1_pre = df.loc[all_inn1_mask, features_inn1_pre].fillna(0)
    X_all_inn1_post = df.loc[all_inn1_mask, features_inn1_post].fillna(0)
    X_all_inn1_post.columns = features_inn1_pre
    
    df.loc[all_inn1_mask, 'wp_pre'] = lr_inn1.predict_proba(X_all_inn1_pre)[:, 1]
    df.loc[all_inn1_mask, 'wp_post'] = lr_inn1.predict_proba(X_all_inn1_post)[:, 1]
    
    # --- 3. Compute Win Probability Added (WPA) ---
    df['wpa_bat'] = df['wp_post'] - df['wp_pre']
    df['wpa_bowl'] = -df['wpa_bat']
    
    # --- 4. Compute Leverage Index (LI) ---
    # In Innings 2, simulate outcome swing: WP if wicket falls vs WP if 6 is hit
    X_sim_wkt = X_all_chase_pre.copy()
    X_sim_wkt['pre_legal_balls_completed'] += 1
    X_sim_wkt['pre_legal_balls_remaining'] = np.maximum(0, X_sim_wkt['pre_legal_balls_remaining'] - 1)
    X_sim_wkt['pre_wickets_lost'] += 1
    X_sim_wkt['pre_wickets_remaining'] = np.maximum(0, X_sim_wkt['pre_wickets_remaining'] - 1)
    X_sim_wkt['crr_pre'] = (X_sim_wkt['pre_current_score'] / np.maximum(1, X_sim_wkt['pre_legal_balls_completed'])) * 6.0
    X_sim_wkt['rrr_pre'] = np.where(
        X_sim_wkt['pre_legal_balls_remaining'] > 0,
        (X_sim_wkt['runs_needed_pre'] / X_sim_wkt['pre_legal_balls_remaining']) * 6.0,
        np.where(X_sim_wkt['runs_needed_pre'] == 0, 0.0, 36.0)
    )
    
    X_sim_six = X_all_chase_pre.copy()
    X_sim_six['pre_legal_balls_completed'] += 1
    X_sim_six['pre_legal_balls_remaining'] = np.maximum(0, X_sim_six['pre_legal_balls_remaining'] - 1)
    X_sim_six['pre_current_score'] += 6
    X_sim_six['runs_needed_pre'] = np.maximum(0, X_sim_six['runs_needed_pre'] - 6)
    X_sim_six['crr_pre'] = (X_sim_six['pre_current_score'] / np.maximum(1, X_sim_six['pre_legal_balls_completed'])) * 6.0
    X_sim_six['rrr_pre'] = np.where(
        X_sim_six['pre_legal_balls_remaining'] > 0,
        (X_sim_six['runs_needed_pre'] / X_sim_six['pre_legal_balls_remaining']) * 6.0,
        np.where(X_sim_six['runs_needed_pre'] == 0, 0.0, 36.0)
    )
    
    wp_sim_wkt = lr_chase.predict_proba(X_sim_wkt)[:, 1]
    wp_sim_six = lr_chase.predict_proba(X_sim_six)[:, 1]
    
    swing_chase = np.abs(wp_sim_six - wp_sim_wkt)
    mean_swing = np.mean(swing_chase[swing_chase > 0])
    li_chase = swing_chase / max(1e-4, mean_swing)
    
    df['leverage_index'] = 1.0  # default baseline
    df.loc[all_chase_mask, 'leverage_index'] = li_chase
    
    return df

if __name__ == '__main__':
    from data_loader import load_all_datasets
    from match_state import reconstruct_match_state
    from feature_engineering import generate_features
    data = load_all_datasets()
    recon = reconstruct_match_state(data['ball_by_ball'], data['matches'], data['competitions'])
    feats = generate_features(recon)
    eval_res = train_and_evaluate_wp_models(feats)
    print("Cross-Validation Win Probability Models Evaluation:")
    for k, v in eval_res.items():
        print(f" - {k}: {v:.4f}")
    df_wp = compute_win_probability_and_wpa(feats)
    print("WP and WPA computed successfully:")
    print(df_wp[['innings', 'overid', 'runs', 'is_wicket', 'wp_pre', 'wp_post', 'wpa_bat', 'leverage_index']].head(10))
