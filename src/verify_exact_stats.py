import sys
sys.path.append('src')
import pandas as pd

df = pd.read_parquet('outputs/features/delivery_features.parquet')
ipl_mask = df['comp_name'].str.contains('IPL', case=False, na=False)
t20i_mask = df['match_format'] == 'T20I'
df_off = df[ipl_mask | t20i_mask].copy()

from batting_engine import compute_batting_metrics
from bowling_engine import compute_bowling_metrics

top_bat = pd.read_csv('top_10_batters.csv')
bat_metrics = compute_batting_metrics(df_off)
bat_ranked = top_bat[['rank', 'striker_name', 'pressure_rating']].merge(bat_metrics, on='striker_name').sort_values('rank')

print("--- TOP 10 BATTERS (OFFICIAL SCOPE) ---")
for _, r in bat_ranked.iterrows():
    pct = r['pct_positive_pressure_matches'] * 100.0
    print(f"{r['rank']:2d} | {r['striker_name']:22s} | balls={r['pressure_balls']:3d} | runs={r['pressure_runs']:3d} | p_sr={r['pressure_sr']:6.2f} | n_sr={r['normal_sr']:6.2f} | d_sr={r['delta_sr']:+6.2f} | rae={r['pressure_rae_per_ball']:+.3f} | pos={r['positive_pressure_matches']:2d}/{r['pressure_matches']:2d} ({pct:4.1f}%) | rating={r['pressure_rating']:5.2f}")

top_bowl = pd.read_csv('top_10_bowlers.csv')
bowl_metrics = compute_bowling_metrics(df_off)
bowl_ranked = top_bowl[['rank', 'bowler_name', 'pressure_rating']].merge(bowl_metrics, on='bowler_name').sort_values('rank')

print("\n--- TOP 10 BOWLERS (OFFICIAL SCOPE) ---")
for _, r in bowl_ranked.iterrows():
    pct = r['pct_positive_pressure_matches'] * 100.0
    print(f"{r['rank']:2d} | {r['bowler_name']:22s} | balls={r['pressure_legal_balls']:3d} | wkts={r['pressure_wickets']:2d} | p_econ={r['pressure_economy']:5.2f} | n_econ={r['normal_economy']:5.2f} | d_econ={r['delta_economy']:+5.2f} | rp={r['pressure_rp_per_ball']:+.3f} | pos={r['positive_pressure_matches']:2d}/{r['pressure_matches']:2d} ({pct:4.1f}%) | rating={r['pressure_rating']:5.2f}")
