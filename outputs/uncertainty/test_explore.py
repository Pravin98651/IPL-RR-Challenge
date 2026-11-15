import pandas as pd
import numpy as np

df = pd.read_parquet('outputs/features/delivery_features.parquet')
ipl_mask = df['comp_name'].str.contains('IPL', case=False, na=False)
t20i_mask = df['match_format'] == 'T20I'
df_official = df[ipl_mask | t20i_mask].copy()

# Batting
press_bat = df_official[(df_official['is_high_pressure']) & (df_official['is_batter_ball'])].copy()
bat_agg = press_bat.groupby(['striker_id', 'striker_name']).agg(
    n_balls=('runs_above_expectation', 'count'),
    n_matches=('match_id', 'nunique'),
    total_rae=('runs_above_expectation', 'sum')
).reset_index()

elig_bat = bat_agg[(bat_agg['n_balls'] >= 100) & (bat_agg['n_matches'] >= 12)].copy()
elig_bat['raw_rae_per_ball'] = elig_bat['total_rae'] / elig_bat['n_balls']
pop_mean_rae_bat = elig_bat['raw_rae_per_ball'].mean()
print(f'Eligible batters: {len(elig_bat)}, pop_mean_rae: {pop_mean_rae_bat:.4f}')

for k in [40, 200, 452, 2212]:
    elig_bat[f'shrunk_{k}'] = (elig_bat['total_rae'] + k * pop_mean_rae_bat) / (elig_bat['n_balls'] + k)
    ranked = elig_bat.sort_values(f'shrunk_{k}', ascending=False).reset_index(drop=True)
    print(f'\nTop 10 for k={k}:')
    for i in range(10):
        r = ranked.iloc[i]
        print(f'  {i+1}. {r["striker_name"]} (balls={r["n_balls"]}, matches={r["n_matches"]}, shrunk={r[f"shrunk_{k}"]:.4f})')

# Bowling
press_bowl = df_official[(df_official['is_high_pressure']) & (df_official['is_legal'])].copy()
bowl_agg = press_bowl.groupby(['bowler_id', 'bowler_name']).agg(
    n_balls=('runs_prevented', 'count'),
    n_matches=('match_id', 'nunique'),
    total_rp=('runs_prevented', 'sum')
).reset_index()

elig_bowl = bowl_agg[(bowl_agg['n_balls'] >= 100) & (bowl_agg['n_matches'] >= 12)].copy()
elig_bowl['raw_rp_per_ball'] = elig_bowl['total_rp'] / elig_bowl['n_balls']
pop_mean_rp_bowl = elig_bowl['raw_rp_per_ball'].mean()
print(f'\nEligible bowlers: {len(elig_bowl)}, pop_mean_rp: {pop_mean_rp_bowl:.4f}')

for k in [40, 200, 280, 2212]:
    elig_bowl[f'shrunk_{k}'] = (elig_bowl['total_rp'] + k * pop_mean_rp_bowl) / (elig_bowl['n_balls'] + k)
    ranked = elig_bowl.sort_values(f'shrunk_{k}', ascending=False).reset_index(drop=True)
    print(f'\nTop 10 bowlers for k={k}:')
    for i in range(10):
        r = ranked.iloc[i]
        print(f'  {i+1}. {r["bowler_name"]} (balls={r["n_balls"]}, matches={r["n_matches"]}, shrunk={r[f"shrunk_{k}"]:.4f})')
