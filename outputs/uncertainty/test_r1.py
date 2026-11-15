import pandas as pd
import numpy as np
from scipy import stats

df = pd.read_parquet('outputs/features/delivery_features.parquet')
ipl_mask = df['comp_name'].str.contains('IPL', case=False, na=False)
t20i_mask = df['match_format'] == 'T20I'
df_official = df[ipl_mask | t20i_mask].copy()

# Frozen round 1 top 10
top10_bat_r1 = pd.read_csv('top_10_batters.csv')
top10_bowl_r1 = pd.read_csv('top_10_bowlers.csv')
print('Round 1 top 10 batters:')
print(top10_bat_r1[['rank', 'striker_name', 'pressure_rating']])
print('\nRound 1 top 10 bowlers:')
print(top10_bowl_r1[['rank', 'bowler_name', 'pressure_rating']])
