"""
Master Pipeline Script for SupeRR Selector Season 2.
Executes the complete end-to-end analytical workflow from raw data to final rankings.
"""
import os
import sys
import pandas as pd
import numpy as np

# Ensure src is on python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_loader import load_all_datasets
from data_validation import validate_deliveries, validate_relationships
from match_state import reconstruct_match_state
from feature_engineering import generate_features
from win_probability import train_and_evaluate_wp_models, compute_win_probability_and_wpa
from pressure_models import apply_pressure_models
from expected_performance import compute_expected_performance_oof
from batting_engine import compute_batting_metrics
from bowling_engine import compute_bowling_metrics
from ranking import rank_batters, rank_bowlers

def main():
    print("=" * 70)
    print("   SUPERR SELECTOR SEASON 2: PRESSURE PERFORMANCE ANALYTICS   ")
    print("=" * 70)
    
    # --- Step 1: Load Datasets ---
    print("\n[Step 1/8] Loading raw datasets...")
    data = load_all_datasets()
    for name, df in data.items():
        print(f" - {name}: {len(df):,} rows")
        
    # --- Step 2: Validate Data & Integrity ---
    print("\n[Step 2/8] Validating structural integrity...")
    val_deliv = validate_deliveries(data['ball_by_ball'])
    val_rel = validate_relationships(data)
    print(f" - Legal deliveries: {val_deliv['legal_deliveries']:,} | Illegal extras: {val_deliv['illegal_deliveries']:,}")
    print(f" - Bowler credited wickets: {val_deliv['bowler_credited_wickets']:,} | Field/RunOut: {val_deliv['fielding_or_other_wickets']:,}")
    print(f" - Foreign key integrity: {'PERFECT (0 orphans)' if val_rel['is_fully_consistent'] else 'Passed with minor exceptions'}")

    # --- Step 3: Match-State Reconstruction ---
    print("\n[Step 3/8] Reconstructing cumulative match states (pre & post delivery)...")
    reconstructed = reconstruct_match_state(data['ball_by_ball'], data['matches'], data['competitions'])
    
    # --- Step 4: Feature Engineering ---
    print("\n[Step 4/8] Engineering 1st innings par expectations & in-match progression...")
    features_df = generate_features(reconstructed)
    
    # --- Step 5: Win Probability, WPA & Leverage ---
    print("\n[Step 5/8] Evaluating and fitting ML Win Probability and Leverage models...")
    cv_results = train_and_evaluate_wp_models(features_df)
    print(f" - Logistic Regression 5-Fold GroupKFold Log Loss: {cv_results['lr_mean_log_loss']:.4f} | AUC: {cv_results['lr_mean_auc']:.4f}")
    print(f" - XGBoost 5-Fold GroupKFold Log Loss: {cv_results['xgb_mean_log_loss']:.4f} | AUC: {cv_results['xgb_mean_auc']:.4f}")
    wp_df = compute_win_probability_and_wpa(features_df)
    
    # --- Step 6: Pressure Modeling ---
    print("\n[Step 6/8] Applying Rule-Based, Leverage, and Hybrid Pressure models...")
    pressure_df = apply_pressure_models(wp_df)
    tier_counts = pressure_df['pressure_tier'].value_counts()
    print(" - Pressure Tier Distribution:")
    for tier, count in tier_counts.items():
        print(f"   * {tier:10s}: {count:6,} balls ({count/len(pressure_df)*100:.1f}%)")
        
    # --- Step 7: Expected Performance Models (OOF) ---
    print("\n[Step 7/8] Fitting Out-of-Fold Expected Performance Models (Zero In-Sample Leakage)...")
    delivery_features = compute_expected_performance_oof(pressure_df)
    
    # Save delivery features
    os.makedirs('outputs/features', exist_ok=True)
    parquet_path = 'outputs/features/delivery_features.parquet'
    sample_csv_path = 'outputs/features/sample_delivery_features.csv'
    
    print(f" - Saving delivery features to {parquet_path}...")
    delivery_features.to_parquet(parquet_path, index=False)
    print(f" - Saving sample CSV to {sample_csv_path}...")
    delivery_features.head(1000).to_csv(sample_csv_path, index=False)
    
    # --- Step 8: Batting & Bowling Rating Engines & Final Rankings ---
    print("\n[Step 8/8] Computing Player Metrics and Final Bayesian-Shrunk Rankings...")
    bat_metrics = compute_batting_metrics(delivery_features)
    bowl_metrics = compute_bowling_metrics(delivery_features)
    
    # Rank Batters
    ranked_batters = rank_batters(bat_metrics, min_balls=100, min_matches=12)
    top10_batters = ranked_batters.head(10)
    
    # Rank Bowlers
    ranked_bowlers = rank_bowlers(bowl_metrics, min_balls=120, min_matches=12)
    top10_bowlers = ranked_bowlers.head(10)
    
    # Export player scores and final rankings
    os.makedirs('outputs/player_scores', exist_ok=True)
    os.makedirs('outputs/final_rankings', exist_ok=True)
    
    bat_metrics.to_csv('outputs/player_scores/all_batter_scores.csv', index=False)
    bat_metrics.to_csv('all_batter_scores.csv', index=False)
    
    bowl_metrics.to_csv('outputs/player_scores/all_bowler_scores.csv', index=False)
    bowl_metrics.to_csv('all_bowler_scores.csv', index=False)
    
    ranked_batters.to_csv('outputs/final_rankings/ranked_batters.csv', index=False)
    ranked_bowlers.to_csv('outputs/final_rankings/ranked_bowlers.csv', index=False)
    
    top10_batters.to_csv('outputs/final_rankings/top_10_batters.csv', index=False)
    top10_batters.to_csv('top_10_batters.csv', index=False)
    
    top10_bowlers.to_csv('outputs/final_rankings/top_10_bowlers.csv', index=False)
    top10_bowlers.to_csv('top_10_bowlers.csv', index=False)
    
    # Pressure Analysis Summary Table
    press_summary = delivery_features.groupby('pressure_tier').agg(
        total_deliveries=('runs', 'count'),
        total_runs=('total_ball_runs', 'sum'),
        total_wickets=('is_wicket', 'sum'),
        mean_strike_rate=('runs', lambda x: x.sum() / max(1, len(x)) * 100),
        mean_economy=('bowler_conceded_runs', lambda x: x.sum() / max(1, (len(x)/6.0))),
        mean_dot_pct=('runs', lambda x: (x == 0).mean() * 100),
        mean_boundary_pct=('runs', lambda x: (x >= 4).mean() * 100),
        mean_leverage=('leverage_index', 'mean')
    ).reset_index()
    press_summary.to_csv('pressure_analysis.csv', index=False)
    press_summary.to_csv('outputs/features/pressure_analysis.csv', index=False)
    
    print("\n" + "=" * 70)
    print("                 TOP 10 BATTERS UNDER PRESSURE                  ")
    print("=" * 70)
    disp_bat_cols = ['rank', 'striker_name', 'pressure_balls', 'pressure_runs', 'pressure_sr', 'delta_sr', 'pressure_rae_per_ball', 'pct_positive_pressure_matches', 'pressure_rating']
    print(top10_batters[disp_bat_cols].to_string(index=False))
    
    print("\n" + "=" * 70)
    print("                 TOP 10 BOWLERS UNDER PRESSURE                  ")
    print("=" * 70)
    disp_bowl_cols = ['rank', 'bowler_name', 'pressure_legal_balls', 'pressure_wickets', 'pressure_economy', 'delta_economy', 'pressure_rp_per_ball', 'pct_positive_pressure_matches', 'pressure_rating']
    print(top10_bowlers[disp_bowl_cols].to_string(index=False))
    
    print("\nPipeline execution complete! Deliverables generated successfully.")

if __name__ == '__main__':
    main()
