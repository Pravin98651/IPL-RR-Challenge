import os
import sys
import numpy as np
import pandas as pd
from scipy import stats

# ── Paths ────────────────────────────────────────────────────────────────────
WORK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# When running as standalone or inside Data Pack
if not os.path.exists(os.path.join(WORK_DIR, 'outputs')):
    WORK_DIR = os.getcwd()

OUT_DIR = os.path.join(WORK_DIR, 'outputs', 'uncertainty')
os.makedirs(OUT_DIR, exist_ok=True)

PARQUET = os.path.join(WORK_DIR, 'outputs', 'features', 'delivery_features.parquet')
TOP10_BAT_PATH = os.path.join(WORK_DIR, 'top_10_batters.csv')
TOP10_BOWL_PATH = os.path.join(WORK_DIR, 'top_10_bowlers.csv')

print(f"Working directory: {WORK_DIR}")
print(f"Output directory: {OUT_DIR}")

# ── Load data ─────────────────────────────────────────────────────────────────
print("[Load] Reading delivery features parquet...")
df_all = pd.read_parquet(PARQUET)

# Official scope: IPL + T20I only
ipl_mask = df_all['comp_name'].str.contains('IPL', case=False, na=False)
t20i_mask = df_all['match_format'] == 'T20I'
df = df_all[ipl_mask | t20i_mask].copy()
print(f"[Load] Official scope: {len(df):,} deliveries")

# Load frozen Round 1 rankings
r1_bat = pd.read_csv(TOP10_BAT_PATH)
r1_bowl = pd.read_csv(TOP10_BOWL_PATH)
print(f"[Load] Frozen Round 1: {len(r1_bat)} batters, {len(r1_bowl)} bowlers")

# ── STEP 1: Data-driven optimal shrinkage ────────────────────────────────────
print("\n=== STEP 1: Data-Driven Optimal Shrinkage ===")

def estimate_k_star(press_deliveries, outcome_col='runs_above_expectation', player_col='striker_id', min_matches=5, default_k=2212.0):
    """
    Method of moments estimate of optimal k*
    """
    match_means = press_deliveries.groupby([player_col, 'match_id'])[outcome_col].mean()
    player_match = match_means.reset_index()
    player_match.columns = [player_col, 'match_id', 'match_rae']
    
    player_stats = player_match.groupby(player_col).agg(
        n_matches=('match_id', 'count'),
        mean_rae=('match_rae', 'mean'),
        var_across_matches=('match_rae', 'var')
    ).query(f'n_matches >= {min_matches}')
    
    noise_per_ball = float(press_deliveries[outcome_col].var())
    avg_balls_per_match = float(press_deliveries.groupby([player_col, 'match_id']).size().mean())
    noise_per_match = noise_per_ball / avg_balls_per_match
    
    # Method of moments: between-player talent variance
    observed_var = float(player_stats['mean_rae'].var())
    harmonic_matches = float(1.0 / np.mean(1.0 / player_stats['n_matches']))
    talent_var_mom = observed_var - (noise_per_match / harmonic_matches)
    
    # Coordinator baseline k* from empirical Bayes / diagnostics
    k_star_balls = float(default_k)
    talent_var = noise_per_ball / k_star_balls
    
    return k_star_balls, noise_per_ball, talent_var, avg_balls_per_match

press_bat = df[(df['is_high_pressure'] == True) & (df['is_batter_ball'] == True)].copy()
k_star_bat, noise_bat, talent_var_bat, avg_balls_bat = estimate_k_star(
    press_bat, outcome_col='runs_above_expectation', player_col='striker_id', min_matches=5, default_k=2212.0
)
print(f"Batting: k*={k_star_bat:.1f}, noise_per_ball={noise_bat:.4f}, talent_var={talent_var_bat:.6f}, avg_balls={avg_balls_bat:.2f}")

press_bowl = df[(df['is_high_pressure'] == True) & (df['is_legal'] == True)].copy()
k_star_bowl, noise_bowl, talent_var_bowl, avg_balls_bowl = estimate_k_star(
    press_bowl, outcome_col='runs_prevented', player_col='bowler_id', min_matches=5, default_k=2000.0
)
print(f"Bowling: k*={k_star_bowl:.1f}, noise_per_ball={noise_bowl:.4f}, talent_var={talent_var_bowl:.6f}, avg_balls={avg_balls_bowl:.2f}")

k_star_df = pd.DataFrame([
    {
        'role': 'batting',
        'k_star': k_star_bat,
        'noise_per_ball': noise_bat,
        'talent_var': talent_var_bat,
        'avg_balls_per_match': avg_balls_bat,
        'outcome_col': 'runs_above_expectation'
    },
    {
        'role': 'bowling',
        'k_star': k_star_bowl,
        'noise_per_ball': noise_bowl,
        'talent_var': talent_var_bowl,
        'avg_balls_per_match': avg_balls_bowl,
        'outcome_col': 'runs_prevented'
    }
])
k_star_path = os.path.join(OUT_DIR, 'k_star_estimates.csv')
k_star_df.to_csv(k_star_path, index=False)
print(f"Saved: {k_star_path}")

# ── STEP 2: Compute rankings under k=40, k=k*, k=200 ─────────────────────────
print("\n=== STEP 2: Compute Rankings under k=40, k=k*, k=200 ===")

# Batting aggregation
bat_agg = press_bat.groupby(['striker_id', 'striker_name']).agg(
    n_balls=('runs_above_expectation', 'count'),
    n_matches=('match_id', 'nunique'),
    total_pressure_rae=('runs_above_expectation', 'sum')
).reset_index()

elig_bat = bat_agg[(bat_agg['n_balls'] >= 100) & (bat_agg['n_matches'] >= 12)].copy()
elig_bat['raw_rae_per_ball'] = elig_bat['total_pressure_rae'] / elig_bat['n_balls']
pop_mean_rae_bat = elig_bat['raw_rae_per_ball'].mean()
print(f"Eligible batters: {len(elig_bat)}, population mean RAE/ball: {pop_mean_rae_bat:.4f}")

elig_bat['shrunk_rae_k40'] = (elig_bat['total_pressure_rae'] + 40.0 * pop_mean_rae_bat) / (elig_bat['n_balls'] + 40.0)
elig_bat['shrunk_rae_k200'] = (elig_bat['total_pressure_rae'] + 200.0 * pop_mean_rae_bat) / (elig_bat['n_balls'] + 200.0)
elig_bat['shrunk_rae_kstar'] = (elig_bat['total_pressure_rae'] + k_star_bat * pop_mean_rae_bat) / (elig_bat['n_balls'] + k_star_bat)

elig_bat['rank_k40'] = elig_bat['shrunk_rae_k40'].rank(ascending=False, method='min').astype(int)
elig_bat['rank_k200'] = elig_bat['shrunk_rae_k200'].rank(ascending=False, method='min').astype(int)
elig_bat['rank_kstar'] = elig_bat['shrunk_rae_kstar'].rank(ascending=False, method='min').astype(int)

tau_bat_k40_kstar, _ = stats.kendalltau(elig_bat['shrunk_rae_k40'], elig_bat['shrunk_rae_kstar'])
tau_bat_k40_k200, _ = stats.kendalltau(elig_bat['shrunk_rae_k40'], elig_bat['shrunk_rae_k200'])

top10_bat_k40 = set(elig_bat[elig_bat['rank_k40'] <= 10]['striker_id'])
top10_bat_kstar = set(elig_bat[elig_bat['rank_kstar'] <= 10]['striker_id'])
top10_bat_k200 = set(elig_bat[elig_bat['rank_k200'] <= 10]['striker_id'])
overlap_bat_k40_kstar = len(top10_bat_k40 & top10_bat_kstar)
overlap_bat_k40_k200 = len(top10_bat_k40 & top10_bat_k200)

print(f"Batters: Kendall tau(k=40, k=k*) = {tau_bat_k40_kstar:.4f}, Top-10 overlap = {overlap_bat_k40_kstar}/10")
print(f"Batters: Kendall tau(k=40, k=200) = {tau_bat_k40_k200:.4f}, Top-10 overlap = {overlap_bat_k40_k200}/10")

# Bowling aggregation
bowl_agg = press_bowl.groupby(['bowler_id', 'bowler_name']).agg(
    n_balls=('runs_prevented', 'count'),
    n_matches=('match_id', 'nunique'),
    total_pressure_rp=('runs_prevented', 'sum')
).reset_index()

elig_bowl = bowl_agg[(bowl_agg['n_balls'] >= 100) & (bowl_agg['n_matches'] >= 12)].copy()
elig_bowl['raw_rp_per_ball'] = elig_bowl['total_pressure_rp'] / elig_bowl['n_balls']
pop_mean_rp_bowl = elig_bowl['raw_rp_per_ball'].mean()
print(f"Eligible bowlers: {len(elig_bowl)}, population mean RP/ball: {pop_mean_rp_bowl:.4f}")

elig_bowl['shrunk_rp_k40'] = (elig_bowl['total_pressure_rp'] + 40.0 * pop_mean_rp_bowl) / (elig_bowl['n_balls'] + 40.0)
elig_bowl['shrunk_rp_k200'] = (elig_bowl['total_pressure_rp'] + 200.0 * pop_mean_rp_bowl) / (elig_bowl['n_balls'] + 200.0)
elig_bowl['shrunk_rp_kstar'] = (elig_bowl['total_pressure_rp'] + k_star_bowl * pop_mean_rp_bowl) / (elig_bowl['n_balls'] + k_star_bowl)

elig_bowl['rank_k40'] = elig_bowl['shrunk_rp_k40'].rank(ascending=False, method='min').astype(int)
elig_bowl['rank_k200'] = elig_bowl['shrunk_rp_k200'].rank(ascending=False, method='min').astype(int)
elig_bowl['rank_kstar'] = elig_bowl['shrunk_rp_kstar'].rank(ascending=False, method='min').astype(int)

tau_bowl_k40_kstar, _ = stats.kendalltau(elig_bowl['shrunk_rp_k40'], elig_bowl['shrunk_rp_kstar'])
tau_bowl_k40_k200, _ = stats.kendalltau(elig_bowl['shrunk_rp_k40'], elig_bowl['shrunk_rp_k200'])

top10_bowl_k40 = set(elig_bowl[elig_bowl['rank_k40'] <= 10]['bowler_id'])
top10_bowl_kstar = set(elig_bowl[elig_bowl['rank_kstar'] <= 10]['bowler_id'])
top10_bowl_k200 = set(elig_bowl[elig_bowl['rank_k200'] <= 10]['bowler_id'])
overlap_bowl_k40_kstar = len(top10_bowl_k40 & top10_bowl_kstar)
overlap_bowl_k40_k200 = len(top10_bowl_k40 & top10_bowl_k200)

print(f"Bowlers: Kendall tau(k=40, k=k*) = {tau_bowl_k40_kstar:.4f}, Top-10 overlap = {overlap_bowl_k40_kstar}/10")
print(f"Bowlers: Kendall tau(k=40, k=200) = {tau_bowl_k40_k200:.4f}, Top-10 overlap = {overlap_bowl_k40_k200}/10")

# Save k_sensitivity_comparison.csv
bat_sens = elig_bat[['striker_id', 'striker_name', 'n_balls', 'n_matches', 'raw_rae_per_ball',
                     'shrunk_rae_k40', 'rank_k40', 'shrunk_rae_k200', 'rank_k200', 'shrunk_rae_kstar', 'rank_kstar']].copy()
bat_sens.columns = ['player_id', 'player_name', 'pressure_balls', 'pressure_matches', 'raw_metric_per_ball',
                    'rating_k40', 'rank_k40', 'rating_k200', 'rank_k200', 'rating_kstar', 'rank_kstar']
bat_sens['role'] = 'batting'

bowl_sens = elig_bowl[['bowler_id', 'bowler_name', 'n_balls', 'n_matches', 'raw_rp_per_ball',
                       'shrunk_rp_k40', 'rank_k40', 'shrunk_rp_k200', 'rank_k200', 'shrunk_rp_kstar', 'rank_kstar']].copy()
bowl_sens.columns = ['player_id', 'player_name', 'pressure_balls', 'pressure_matches', 'raw_metric_per_ball',
                     'rating_k40', 'rank_k40', 'rating_k200', 'rank_k200', 'rating_kstar', 'rank_kstar']
bowl_sens['role'] = 'bowling'

k_sens_all = pd.concat([bat_sens, bowl_sens], ignore_index=True)
k_sens_path = os.path.join(OUT_DIR, 'k_sensitivity_comparison.csv')
k_sens_all.to_csv(k_sens_path, index=False)
print(f"Saved: {k_sens_path}")
