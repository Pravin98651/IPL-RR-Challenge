import pandas as pd
import numpy as np

df = pd.read_parquet('outputs/features/delivery_features.parquet')
ipl_mask = df['comp_name'].str.contains('IPL', case=False, na=False)
t20i_mask = df['match_format'] == 'T20I'
df_official = df[ipl_mask | t20i_mask].copy()

press_bat = df_official[(df_official['is_high_pressure']) & (df_official['is_batter_ball'])].copy()
match_bat = press_bat.groupby(['match_id', 'striker_id', 'striker_name']).agg(
    n_balls=('runs_above_expectation', 'count'),
    total_rae=('runs_above_expectation', 'sum')
).reset_index()

# Baseline eligible
player_tot = match_bat.groupby(['striker_id', 'striker_name']).agg(
    tot_balls=('n_balls', 'sum'),
    tot_matches=('match_id', 'count'),
    tot_rae=('total_rae', 'sum')
).reset_index()
baseline_elig = player_tot[(player_tot['tot_balls'] >= 100) & (player_tot['tot_matches'] >= 12)].copy()
candidate_ids = set(baseline_elig['striker_id'])

by_match = {m: g for m, g in match_bat.groupby('match_id')}
match_strata = df_official.groupby('match_id').first()[['comp_name', 'season']].copy()
match_strata['is_ipl'] = match_strata['comp_name'].str.contains('IPL', na=False)

ipl_matches = match_strata[match_strata['is_ipl']].index.values
t20i_matches = match_strata[~match_strata['is_ipl']].index.values

rng = np.random.default_rng(0)
qual_counts = {pid: 0 for pid in candidate_ids}

for i in range(100):
    b_ipl = rng.choice(ipl_matches, size=len(ipl_matches), replace=True)
    b_t20i = rng.choice(t20i_matches, size=len(t20i_matches), replace=True)
    b_matches = np.concatenate([b_ipl, b_t20i])
    boot_df = pd.concat([by_match[m] for m in b_matches if m in by_match], ignore_index=True)
    p_agg = boot_df.groupby('striker_id').agg(
        n_balls=('n_balls', 'sum'),
        n_matches=('match_id', 'count')
    )
    for pid in candidate_ids:
        if pid in p_agg.index:
            r = p_agg.loc[pid]
            if r['n_balls'] >= 100 and r['n_matches'] >= 12:
                qual_counts[pid] += 1

print('Fraction of replicates meeting criteria for candidates:')
for pid, c in sorted(qual_counts.items(), key=lambda x: x[1])[:10]:
    name = baseline_elig[baseline_elig['striker_id']==pid]['striker_name'].iloc[0]
    orig_b = baseline_elig[baseline_elig['striker_id']==pid]['tot_balls'].iloc[0]
    print(f'  {name} (orig balls={orig_b}): {c}/100 replicates')
