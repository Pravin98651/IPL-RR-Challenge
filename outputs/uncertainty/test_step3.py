import os
import sys
import time
import numpy as np
import pandas as pd
from scipy import stats

ROOT = r"c:\Users\pravi\Downloads\6af458274c1e8_data_pack\Data Pack"
PARQUET = os.path.join(ROOT, "outputs", "features", "delivery_features.parquet")
OUT_DIR = os.path.join(ROOT, "outputs", "uncertainty")

# Load data
df_all = pd.read_parquet(PARQUET)
ipl_mask = df_all['comp_name'].str.contains('IPL', case=False, na=False)
t20i_mask = df_all['match_format'] == 'T20I'
df = df_all[ipl_mask | t20i_mask].copy()

# Pre-aggregate match-level batting
press_bat = df[(df['is_high_pressure'] == True) & (df['is_batter_ball'] == True)].copy()
match_bat = press_bat.groupby(['match_id', 'striker_id', 'striker_name']).agg(
    n_balls=('runs_above_expectation', 'count'),
    total_rae=('runs_above_expectation', 'sum')
).reset_index()

bat_tot = match_bat.groupby(['striker_id', 'striker_name']).agg(
    tot_balls=('n_balls', 'sum'),
    tot_matches=('match_id', 'count'),
    tot_rae=('total_rae', 'sum')
).reset_index()
baseline_elig_bat = bat_tot[(bat_tot['tot_balls'] >= 100) & (bat_tot['tot_matches'] >= 12)].copy()
candidate_bat_ids = baseline_elig_bat['striker_id'].values
candidate_bat_names = dict(zip(baseline_elig_bat['striker_id'], baseline_elig_bat['striker_name']))

# Pre-aggregate match-level bowling
press_bowl = df[(df['is_high_pressure'] == True) & (df['is_legal'] == True)].copy()
match_bowl = press_bowl.groupby(['match_id', 'bowler_id', 'bowler_name']).agg(
    n_balls=('runs_prevented', 'count'),
    total_rp=('runs_prevented', 'sum')
).reset_index()

bowl_tot = match_bowl.groupby(['bowler_id', 'bowler_name']).agg(
    tot_balls=('n_balls', 'sum'),
    tot_matches=('match_id', 'count'),
    tot_rp=('total_rp', 'sum')
).reset_index()
baseline_elig_bowl = bowl_tot[(bowl_tot['tot_balls'] >= 100) & (bowl_tot['tot_matches'] >= 12)].copy()
candidate_bowl_ids = baseline_elig_bowl['bowler_id'].values
candidate_bowl_names = dict(zip(baseline_elig_bowl['bowler_id'], baseline_elig_bowl['bowler_name']))

# Matches strata
match_strata = df.groupby('match_id').first()[['comp_name', 'season']].copy()
match_strata['is_ipl'] = match_strata['comp_name'].str.contains('IPL', na=False)

ipl_matches = match_strata[match_strata['is_ipl']].index.values
t20i_matches = match_strata[~match_strata['is_ipl']].index.values

by_match_bat = {m: g for m, g in match_bat.groupby('match_id')}
by_match_bowl = {m: g for m, g in match_bowl.groupby('match_id')}

k_star_bat = 2212.0
k_star_bowl = 2000.0

print(f"Starting 1000 bootstrap iterations for Batters (k*={k_star_bat})...")
t0 = time.time()
rng = np.random.default_rng(0)

all_bat_ranks = []
all_bat_ratings = []

for i in range(1000):
    b_ipl = rng.choice(ipl_matches, size=len(ipl_matches), replace=True)
    b_t20i = rng.choice(t20i_matches, size=len(t20i_matches), replace=True)
    b_matches = np.concatenate([b_ipl, b_t20i])
    
    boot_df = pd.concat([by_match_bat[m] for m in b_matches if m in by_match_bat], ignore_index=True)
    p_agg = boot_df.groupby('striker_id').agg(
        n_balls=('n_balls', 'sum'),
        total_rae=('total_rae', 'sum')
    )
    pop_mean_rae = p_agg['total_rae'].sum() / p_agg['n_balls'].sum()
    
    rep_ratings = {}
    for pid in candidate_bat_ids:
        if pid in p_agg.index:
            nb = p_agg.loc[pid, 'n_balls']
            tr = p_agg.loc[pid, 'total_rae']
        else:
            nb = 0
            tr = 0.0
        shrunk = (tr + k_star_bat * pop_mean_rae) / (nb + k_star_bat)
        rep_ratings[candidate_bat_names[pid]] = shrunk
        
    s_series = pd.Series(rep_ratings)
    s_ranks = s_series.rank(ascending=False, method='min')
    all_bat_ratings.append(rep_ratings)
    all_bat_ranks.append(s_ranks.to_dict())

print(f"Batting 1000 iterations completed in {time.time() - t0:.2f}s")

# Bowling bootstrap
print(f"Starting 1000 bootstrap iterations for Bowlers (k*={k_star_bowl})...")
t0 = time.time()
rng_bowl = np.random.default_rng(0)

all_bowl_ranks = []
all_bowl_ratings = []

for i in range(1000):
    b_ipl = rng_bowl.choice(ipl_matches, size=len(ipl_matches), replace=True)
    b_t20i = rng_bowl.choice(t20i_matches, size=len(t20i_matches), replace=True)
    b_matches = np.concatenate([b_ipl, b_t20i])
    
    boot_df = pd.concat([by_match_bowl[m] for m in b_matches if m in by_match_bowl], ignore_index=True)
    p_agg = boot_df.groupby('bowler_id').agg(
        n_balls=('n_balls', 'sum'),
        total_rp=('total_rp', 'sum')
    )
    pop_mean_rp = p_agg['total_rp'].sum() / p_agg['n_balls'].sum()
    
    rep_ratings = {}
    for pid in candidate_bowl_ids:
        if pid in p_agg.index:
            nb = p_agg.loc[pid, 'n_balls']
            tr = p_agg.loc[pid, 'total_rp']
        else:
            nb = 0
            tr = 0.0
        shrunk = (tr + k_star_bowl * pop_mean_rp) / (nb + k_star_bowl)
        rep_ratings[candidate_bowl_names[pid]] = shrunk
        
    s_series = pd.Series(rep_ratings)
    s_ranks = s_series.rank(ascending=False, method='min')
    all_bowl_ratings.append(rep_ratings)
    all_bowl_ranks.append(s_ranks.to_dict())

print(f"Bowling 1000 iterations completed in {time.time() - t0:.2f}s")

df_bat_ranks = pd.DataFrame(all_bat_ranks)
df_bat_ratings = pd.DataFrame(all_bat_ratings)

df_bowl_ranks = pd.DataFrame(all_bowl_ranks)
df_bowl_ratings = pd.DataFrame(all_bowl_ratings)

# Print Klaasen & Narine metrics
print(f"\nHeinrich Klaasen:")
print(f"  Mean rank: {df_bat_ranks['Heinrich Klaasen'].mean():.2f}")
print(f"  90% CI: [{np.percentile(df_bat_ranks['Heinrich Klaasen'], 5):.1f}, {np.percentile(df_bat_ranks['Heinrich Klaasen'], 95):.1f}]")
print(f"  P(top 10): {(df_bat_ranks['Heinrich Klaasen'] <= 10).mean():.3f}")

print(f"\nSunil Narine:")
print(f"  Mean rank: {df_bowl_ranks['Sunil Narine'].mean():.2f}")
print(f"  90% CI: [{np.percentile(df_bowl_ranks['Sunil Narine'], 5):.1f}, {np.percentile(df_bowl_ranks['Sunil Narine'], 95):.1f}]")
print(f"  P(top 10): {(df_bowl_ranks['Sunil Narine'] <= 10).mean():.3f}")
