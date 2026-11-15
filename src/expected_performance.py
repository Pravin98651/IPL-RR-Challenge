"""
Context-Adjusted Expected Performance Module.
Estimates neutral baseline expectations using out-of-fold match-grouped cross-validation.
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import GroupKFold
from sklearn.ensemble import HistGradientBoostingRegressor, HistGradientBoostingClassifier
from typing import Dict, Any

def compute_expected_performance_oof(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fits expected performance models using 5-fold GroupKFold by match_id
    to guarantee zero in-sample leakage.
    """
    df = df.copy()
    
    # Feature matrix (strictly pre-delivery, neutral context, NO player IDs)
    df['pace_or_spin_code'] = df['pace_or_spin'].map({'Pace': 1, 'Spin': 2}).fillna(0).astype(int)
    df['format_code'] = df['match_format'].map({'T20': 1, 'T20I': 2}).fillna(0).astype(int)
    
    feature_cols = [
        'innings', 'overid', 'pre_legal_balls_completed',
        'pre_wickets_lost', 'batting_order', 'knock_out',
        'pace_or_spin_code', 'format_code'
    ]
    
    X = df[feature_cols].copy()
    X['batting_order'] = X['batting_order'].fillna(5).astype(int)
    
    y_bat_runs = df['runs'].values
    y_bat_dot = (df['runs'] == 0).astype(int).values
    y_bat_bnd = (df['runs'] >= 4).astype(int).values
    y_bat_out = df['is_wicket'].astype(int).values
    
    y_bowl_runs = df['bowler_conceded_runs'].values
    y_bowl_wkt = df['is_bowler_wicket'].astype(int).values
    y_bowl_dot = (df['bowler_conceded_runs'] == 0).astype(int).values
    y_bowl_bnd = (df['bowler_conceded_runs'] >= 4).astype(int).values
    
    # Output arrays
    exp_bat_runs = np.zeros(len(df))
    exp_bat_dot = np.zeros(len(df))
    exp_bat_bnd = np.zeros(len(df))
    exp_bat_out = np.zeros(len(df))
    
    exp_bowl_runs = np.zeros(len(df))
    exp_bowl_wkt = np.zeros(len(df))
    exp_bowl_dot = np.zeros(len(df))
    exp_bowl_bnd = np.zeros(len(df))
    
    groups = df['match_id']
    gkf = GroupKFold(n_splits=5)
    
    print("Computing out-of-fold expected performance models across 5 match folds...")
    fold = 1
    for tr_idx, val_idx in gkf.split(X, y_bat_runs, groups):
        X_tr, X_val = X.iloc[tr_idx], X.iloc[val_idx]
        
        # 1. Batter Expected Runs
        reg_bat = HistGradientBoostingRegressor(max_iter=60, random_state=42)
        reg_bat.fit(X_tr, y_bat_runs[tr_idx])
        exp_bat_runs[val_idx] = reg_bat.predict(X_val)
        
        # 2. Batter Expected Dot
        clf_bat_dot = HistGradientBoostingClassifier(max_iter=40, random_state=42)
        clf_bat_dot.fit(X_tr, y_bat_dot[tr_idx])
        exp_bat_dot[val_idx] = clf_bat_dot.predict_proba(X_val)[:, 1]
        
        # 3. Batter Expected Boundary
        clf_bat_bnd = HistGradientBoostingClassifier(max_iter=40, random_state=42)
        clf_bat_bnd.fit(X_tr, y_bat_bnd[tr_idx])
        exp_bat_bnd[val_idx] = clf_bat_bnd.predict_proba(X_val)[:, 1]
        
        # 4. Batter Expected Dismissal
        clf_bat_out = HistGradientBoostingClassifier(max_iter=40, random_state=42)
        clf_bat_out.fit(X_tr, y_bat_out[tr_idx])
        exp_bat_out[val_idx] = clf_bat_out.predict_proba(X_val)[:, 1]
        
        # 5. Bowler Expected Runs Conceded
        reg_bowl = HistGradientBoostingRegressor(max_iter=60, random_state=42)
        reg_bowl.fit(X_tr, y_bowl_runs[tr_idx])
        exp_bowl_runs[val_idx] = reg_bowl.predict(X_val)
        
        # 6. Bowler Expected Wickets
        clf_bowl_wkt = HistGradientBoostingClassifier(max_iter=40, random_state=42)
        clf_bowl_wkt.fit(X_tr, y_bowl_wkt[tr_idx])
        exp_bowl_wkt[val_idx] = clf_bowl_wkt.predict_proba(X_val)[:, 1]
        
        # 7. Bowler Expected Dot Conceded
        clf_bowl_dot = HistGradientBoostingClassifier(max_iter=40, random_state=42)
        clf_bowl_dot.fit(X_tr, y_bowl_dot[tr_idx])
        exp_bowl_dot[val_idx] = clf_bowl_dot.predict_proba(X_val)[:, 1]
        
        # 8. Bowler Expected Boundary Conceded
        clf_bowl_bnd = HistGradientBoostingClassifier(max_iter=40, random_state=42)
        clf_bowl_bnd.fit(X_tr, y_bowl_bnd[tr_idx])
        exp_bowl_bnd[val_idx] = clf_bowl_bnd.predict_proba(X_val)[:, 1]
        
        fold += 1
        
    df['exp_batter_runs'] = exp_bat_runs
    df['exp_batter_dot_prob'] = exp_bat_dot
    df['exp_batter_bnd_prob'] = exp_bat_bnd
    df['exp_batter_out_prob'] = exp_bat_out
    
    df['exp_bowler_runs'] = exp_bowl_runs
    df['exp_bowler_wkt_prob'] = exp_bowl_wkt
    df['exp_bowler_dot_prob'] = exp_bowl_dot
    df['exp_bowler_bnd_prob'] = exp_bowl_bnd
    
    # Context-adjusted value added metrics
    df['runs_above_expectation'] = df['runs'] - df['exp_batter_runs']
    df['runs_prevented'] = df['exp_bowler_runs'] - df['bowler_conceded_runs']
    df['wickets_above_expectation'] = df['is_bowler_wicket'].astype(float) - df['exp_bowler_wkt_prob']
    
    return df

if __name__ == '__main__':
    from data_loader import load_all_datasets
    from match_state import reconstruct_match_state
    from feature_engineering import generate_features
    from win_probability import compute_win_probability_and_wpa
    from pressure_models import apply_pressure_models
    data = load_all_datasets()
    recon = reconstruct_match_state(data['ball_by_ball'], data['matches'], data['competitions'])
    feats = generate_features(recon)
    df_wp = compute_win_probability_and_wpa(feats)
    df_press = apply_pressure_models(df_wp)
    df_exp = compute_expected_performance_oof(df_press)
    print("Expected performance calculated. Mean RAE:", df_exp['runs_above_expectation'].mean())
    print("Mean Runs Prevented:", df_exp['runs_prevented'].mean())
    print("Mean Wickets Above Expectation:", df_exp['wickets_above_expectation'].mean())
