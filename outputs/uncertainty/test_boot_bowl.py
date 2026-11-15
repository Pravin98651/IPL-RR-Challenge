import pandas as pd
import numpy as np

df = pd.read_parquet('outputs/features/delivery_features.parquet')
ipl_mask = df['comp_name'].str.contains('IPL', case=False, na=False)
t20i_mask = df['match_format'] == 'T20I'
df_official = df[ipl_mask | t20i_mask].copy()

# Bowling
press_bowl = df_official[(df_official['is_high_pressure']) & (df_official['is_legal'])].copy()
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

by_match_bowl = {m: g for m, g in match_bowl.groupby('match_id')}
match_strata = df_official.groupby('match_id').first()[['comp_name', 'season']].copy()
match_strata['is_ipl'] = match_strata['comp_name'].str.contains('IPL', na=False)

ipl_matches = match_strata[match_strata['is_ipl']].index.values
t20i_matches = match_strata[~match_strata['is_ipl']].index.values

def run_test_boot_bowl(k_val, n_boot=200):
    rng = np.random.default_rng(0)
    all_ranks = []
    all_ratings = []
    for i in range(n_boot):
        b_ipl = rng.choice(ipl_matches, size=len(ipl_matches), replace=True)
        b_t20i = rng.choice(t20i_matches, size=len(t20i_matches), replace=True)
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
            shrunk = (tr + k_val * pop_mean_rp) / (nb + k_val)
            rep_ratings[pid] = shrunk
            
        s_series = pd.Series(rep_ratings)
        s_ranks = s_series.rank(ascending=False, method='min')
        all_ratings.append(rep_ratings)
        all_ranks.append(s_ranks.to_dict())
        
    df_ranks = pd.DataFrame(all_ranks)
    df_ratings = pd.DataFrame(all_ratings)
    summary = []
    for pid in candidate_bowl_ids:
        r_series = df_ranks[pid]
        rt_series = df_ratings[pid]
        summary.append({
            'bowler_id': pid,
            'bowler_name': candidate_bowl_names[pid],
            'mean_rank': r_series.mean(),
            'p5_rank': np.percentile(r_series, 5),
            'p95_rank': np.percentile(r_series, 95),
            'p_top10': (r_series <= 10).mean(),
            'rating_mean': rt_series.mean(),
            'ci95_low': np.percentile(rt_series, 2.5),
            'ci95_high': np.percentile(rt_series, 97.5)
        })
    return pd.DataFrame(summary).sort_values('mean_rank')

print('Running bowler test with k=40...')
res_40 = run_test_boot_bowl(40.0, 200)
print(res_40[['bowler_name', 'mean_rank', 'p5_rank', 'p95_rank', 'p_top10']].head(10))

print('\nRunning bowler test with k=2000...')
res_2000 = run_test_boot_bowl(2000.0, 200)
print(res_2000[['bowler_name', 'mean_rank', 'p5_rank', 'p95_rank', 'p_top10']].head(10))
