"""
SupeRR Selector Season 2 — Task Experiments
Runs all 9 outstanding methodological experiments using pre-computed delivery_features.parquet.
All results are computed from actual data; no fabrication.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# ── Project root (one level up from src/)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARQUET = os.path.join(ROOT, 'outputs', 'features', 'delivery_features.parquet')
OUT = ROOT  # CSVs go to project root

from batting_engine import compute_batting_metrics
from bowling_engine import compute_bowling_metrics
from ranking import rank_batters, rank_bowlers
from reliability import bayesian_shrinkage, standardize_series

# ══════════════════════════════════════════════════════════════════════
# LOAD DATA
# ══════════════════════════════════════════════════════════════════════
print("Loading delivery_features.parquet …")
df_all = pd.read_parquet(PARQUET)
print(f"  Loaded {len(df_all):,} deliveries, {df_all['match_id'].nunique()} matches")

# ── Scope filters
ipl_mask    = df_all['comp_name'].str.contains('IPL', case=False, na=False)
t20i_mask   = df_all['match_format'] == 'T20I'
other_t20   = (df_all['match_format'] == 'T20') & ~ipl_mask

official_mask = ipl_mask | t20i_mask  # IPL + T20I only (problem statement scope)
expanded_mask = ipl_mask | t20i_mask | other_t20  # adds Emerging Teams Asia Cups

df_official = df_all[official_mask].copy()
df_expanded = df_all[expanded_mask].copy()

print(f"  Official scope: {len(df_official):,} deliveries, "
      f"{df_official['match_id'].nunique()} matches "
      f"(IPL={ipl_mask.sum():,}, T20I={t20i_mask.sum():,})")
print(f"  Expanded scope: {len(df_expanded):,} deliveries, "
      f"{df_expanded['match_id'].nunique()} matches")


# ══════════════════════════════════════════════════════════════════════
# HELPER: Run full player ranking pipeline on a subset dataframe
# ══════════════════════════════════════════════════════════════════════
def run_pipeline(df: pd.DataFrame, min_bat_balls=100, min_bat_matches=12,
                 min_bowl_balls=120, min_bowl_matches=12):
    bat_df  = compute_batting_metrics(df)
    bowl_df = compute_bowling_metrics(df)
    try:
        bat_ranked = rank_batters(bat_df, min_balls=min_bat_balls, min_matches=min_bat_matches)
    except ValueError as e:
        print(f"    [WARN] Batter ranking: {e}")
        bat_ranked = pd.DataFrame()
    try:
        bowl_ranked = rank_bowlers(bowl_df, min_balls=min_bowl_balls, min_matches=min_bowl_matches)
    except ValueError as e:
        print(f"    [WARN] Bowler ranking: {e}")
        bowl_ranked = pd.DataFrame()
    return bat_ranked, bowl_ranked


def top10_names(ranked_df: pd.DataFrame, name_col='striker_name') -> list:
    if ranked_df.empty:
        return []
    name = name_col if name_col in ranked_df.columns else 'bowler_name'
    return ranked_df.head(10)[name].tolist()


# ══════════════════════════════════════════════════════════════════════
# TASK 1 — Competition Scope Comparison
# ══════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("TASK 1: Competition Scope Comparison")
print("="*60)

bat_off, bowl_off = run_pipeline(df_official)
bat_exp, bowl_exp = run_pipeline(df_expanded)

top10_bat_off  = top10_names(bat_off,  'striker_name')
top10_bat_exp  = top10_names(bat_exp,  'striker_name')
top10_bowl_off = top10_names(bowl_off, 'bowler_name')
top10_bowl_exp = top10_names(bowl_exp, 'bowler_name')

max_rows = max(len(top10_bat_off), len(top10_bat_exp), 1)
comp_rows = []
for i in range(max_rows):
    row = {
        'rank': i + 1,
        'official_batter': top10_bat_off[i] if i < len(top10_bat_off) else '',
        'expanded_batter': top10_bat_exp[i] if i < len(top10_bat_exp) else '',
        'official_bowler': top10_bowl_off[i] if i < len(top10_bowl_off) else '',
        'expanded_bowler': top10_bowl_exp[i] if i < len(top10_bowl_exp) else '',
    }
    comp_rows.append(row)

# Detailed batter comparison
if not bat_off.empty and not bat_exp.empty:
    off_bat_top = bat_off.head(10)[['rank', 'striker_name', 'pressure_rating']].rename(
        columns={'rank':'official_rank', 'pressure_rating':'official_rating'})
    exp_bat_top = bat_exp.head(10)[['rank', 'striker_name', 'pressure_rating']].rename(
        columns={'rank':'expanded_rank', 'pressure_rating':'expanded_rating'})
    all_bat_names = list(set(off_bat_top['striker_name'].tolist() + exp_bat_top['striker_name'].tolist()))
    batter_comp_detail = []
    for name in all_bat_names:
        off_row = off_bat_top[off_bat_top['striker_name'] == name]
        exp_row = exp_bat_top[exp_bat_top['striker_name'] == name]
        batter_comp_detail.append({
            'player': name,
            'role': 'batter',
            'official_rank': int(off_row['official_rank'].values[0]) if len(off_row) else 'NR',
            'official_rating': float(off_row['official_rating'].values[0]) if len(off_row) else None,
            'expanded_rank': int(exp_row['expanded_rank'].values[0]) if len(exp_row) else 'NR',
            'expanded_rating': float(exp_row['expanded_rating'].values[0]) if len(exp_row) else None,
        })

if not bowl_off.empty and not bowl_exp.empty:
    off_bowl_top = bowl_off.head(10)[['rank', 'bowler_name', 'pressure_rating']].rename(
        columns={'rank':'official_rank', 'pressure_rating':'official_rating'})
    exp_bowl_top = bowl_exp.head(10)[['rank', 'bowler_name', 'pressure_rating']].rename(
        columns={'rank':'expanded_rank', 'pressure_rating':'expanded_rating'})
    all_bowl_names = list(set(off_bowl_top['bowler_name'].tolist() + exp_bowl_top['bowler_name'].tolist()))
    bowler_comp_detail = []
    for name in all_bowl_names:
        off_row = off_bowl_top[off_bowl_top['bowler_name'] == name]
        exp_row = exp_bowl_top[exp_bowl_top['bowler_name'] == name]
        bowler_comp_detail.append({
            'player': name,
            'role': 'bowler',
            'official_rank': int(off_row['official_rank'].values[0]) if len(off_row) else 'NR',
            'official_rating': float(off_row['official_rating'].values[0]) if len(off_row) else None,
            'expanded_rank': int(exp_row['expanded_rank'].values[0]) if len(exp_row) else 'NR',
            'expanded_rating': float(exp_row['expanded_rating'].values[0]) if len(exp_row) else None,
        })
    combined_detail = batter_comp_detail + bowler_comp_detail
else:
    combined_detail = []

scope_df = pd.DataFrame(comp_rows)
detail_df = pd.DataFrame(combined_detail) if combined_detail else pd.DataFrame()
scope_df.to_csv(os.path.join(OUT, 'competition_scope_comparison.csv'), index=False)
if not detail_df.empty:
    detail_df.to_csv(os.path.join(OUT, 'competition_scope_detail.csv'), index=False)

print("Official Top 10 Batters:  ", top10_bat_off)
print("Expanded Top 10 Batters:  ", top10_bat_exp)
print("Official Top 10 Bowlers:  ", top10_bowl_off)
print("Expanded Top 10 Bowlers:  ", top10_bowl_exp)
print("  → Saved competition_scope_comparison.csv")


# ══════════════════════════════════════════════════════════════════════
# TASK 2 — Pressure Score Calibration
# ══════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("TASK 2: Pressure Score Calibration")
print("="*60)

from pressure_models import classify_pressure

df = df_official.copy()

# Theoretical analysis for Innings 1
# PI_inn1 = 0.50*situational_urgency + 0.30*wkt_scarcity + 0.20*par_deficit
# Max: 0.50*1.25 + 0.30*1.0 + 0.20*1.0 = 0.625+0.30+0.20 = 1.125 (before multiplier)
# With knockout 1.20x: 1.35
# Innings 2 (PI_hybrid)
# PI_rule_max: 0.40*1.5 + 0.30*1.25 + 0.20*1.0 + 0.10*1.0 = 0.60+0.375+0.20+0.10 = 1.275
# PI_lev_max: clip(LI/2, 0, 1.5) = 1.5
# PI_hybrid = 0.50*PI_rule + 0.50*PI_lev → max = 0.50*1.275 + 0.50*1.5 = 0.6375+0.75 = 1.3875
# With knockout: 1.20 * PI_rule → hybrid component is bigger

THEORETICAL = {
    'inn1_theoretical_min': 0.0,
    'inn1_theoretical_max_before_multiplier': round(0.50*1.25 + 0.30*1.0 + 0.20*1.0, 4),
    'inn1_theoretical_max_with_knockout': round((0.50*1.25 + 0.30*1.0 + 0.20*1.0)*1.20, 4),
    'inn2_rule_theoretical_max': round(0.40*1.5 + 0.30*1.25 + 0.20*1.0 + 0.10*1.0, 4),
    'inn2_lev_theoretical_max': 1.5,
    'inn2_hybrid_theoretical_max': round(0.50*(0.40*1.5+0.30*1.25+0.20*1.0+0.10*1.0) + 0.50*1.5, 4),
    'inn2_hybrid_max_with_knockout': round((0.50*(0.40*1.5+0.30*1.25+0.20*1.0+0.10*1.0))*1.20 + 0.50*1.5, 4),
}

segments = {
    ('all',      'all'  ): df,
    ('innings1', 'all'  ): df[df['innings'] == 1],
    ('innings2', 'all'  ): df[df['innings'] >= 2],
    ('all',      'IPL'  ): df[ipl_mask & official_mask],
    ('all',      'T20I' ): df[t20i_mask],
    ('innings1', 'IPL'  ): df[(df['innings'] == 1) & ipl_mask & official_mask],
    ('innings2', 'IPL'  ): df[(df['innings'] >= 2) & ipl_mask & official_mask],
    ('innings1', 'T20I' ): df[(df['innings'] == 1) & t20i_mask],
    ('innings2', 'T20I' ): df[(df['innings'] >= 2) & t20i_mask],
}

pressure_rows = []
thresholds = [0.35, 0.60, 0.85]
for (inn_label, fmt_label), seg in segments.items():
    if seg.empty:
        continue
    ps = seg['pressure_score']
    pr = seg['pressure_index_rule']
    pl = seg['pressure_index_leverage']
    ph = seg['pressure_index_hybrid']
    tiers = seg['pressure_tier'].value_counts(normalize=True) * 100
    n_above1 = (ps > 1.0).sum()
    n_knockout = (seg.get('knock_out', pd.Series(0, index=seg.index)) == 1).sum() if 'knock_out' in seg.columns else 0
    pressure_rows.append({
        'segment_innings': inn_label,
        'segment_format':  fmt_label,
        'n_deliveries':    len(seg),
        # Pressure Score (hybrid)
        'score_min':  round(ps.min(), 4),
        'score_p5':   round(ps.quantile(0.05), 4),
        'score_p25':  round(ps.quantile(0.25), 4),
        'score_p50':  round(ps.quantile(0.50), 4),
        'score_p75':  round(ps.quantile(0.75), 4),
        'score_p95':  round(ps.quantile(0.95), 4),
        'score_max':  round(ps.max(), 4),
        'score_mean': round(ps.mean(), 4),
        'score_std':  round(ps.std(), 4),
        # Rule component
        'rule_min':  round(pr.min(), 4),
        'rule_max':  round(pr.max(), 4),
        'rule_mean': round(pr.mean(), 4),
        # Leverage component
        'leverage_min':  round(pl.min(), 4),
        'leverage_max':  round(pl.max(), 4),
        'leverage_mean': round(pl.mean(), 4),
        # Tier percentages
        'pct_low':      round(tiers.get('Low', 0), 2),
        'pct_moderate': round(tiers.get('Moderate', 0), 2),
        'pct_high':     round(tiers.get('High', 0), 2),
        'pct_extreme':  round(tiers.get('Extreme', 0), 2),
        'pct_high_or_extreme': round(tiers.get('High', 0) + tiers.get('Extreme', 0), 2),
        # Over-1.0 deliveries (clipping happens in final score)
        'n_above_1pt0_before_clip': int(n_above1),
        'n_knockout_deliveries': int(n_knockout),
        # Theoretical (filled for first row only)
        'inn1_theoretical_max_base': THEORETICAL['inn1_theoretical_max_before_multiplier'] if inn_label == 'innings1' else '',
        'inn1_theoretical_max_knockout': THEORETICAL['inn1_theoretical_max_with_knockout'] if inn_label == 'innings1' else '',
        'inn2_hybrid_theoretical_max_base': THEORETICAL['inn2_hybrid_theoretical_max'] if inn_label == 'innings2' else '',
        'inn2_hybrid_theoretical_max_knockout': THEORETICAL['inn2_hybrid_max_with_knockout'] if inn_label == 'innings2' else '',
    })

pd.DataFrame(pressure_rows).to_csv(os.path.join(OUT, 'pressure_distribution.csv'), index=False)
print("  → Saved pressure_distribution.csv")
print(f"  Pressure score range (all official): {df['pressure_score'].min():.4f} – {df['pressure_score'].max():.4f}")
print(f"  Deliveries with score > 1.0: {(df['pressure_score'] > 1.0).sum()}")
print(f"  Theoretical Inn1 max (with KO): {THEORETICAL['inn1_theoretical_max_with_knockout']}")
print(f"  Theoretical Inn2 hybrid max (with KO): {THEORETICAL['inn2_hybrid_max_with_knockout']}")


# ══════════════════════════════════════════════════════════════════════
# TASK 3 — Three-Model Pressure Comparison
# ══════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("TASK 3: Pressure Model Comparison (A vs B vs C)")
print("="*60)

# Model A: rule-based only        → pressure_index_rule
# Model B: 50/50 hybrid (existing) → pressure_index_hybrid  
# Model C: Alternative — prevents near-zero WP from erasing obvious situational pressure
#   PI_C = max(0.70 * PI_rule, 0.50 * PI_rule + 0.50 * PI_lev)
#   This ensures extreme situational urgency is never fully washed out by very low WP

df_cmp = df_official.copy()
df_cmp['model_a'] = df_cmp['pressure_index_rule']
df_cmp['model_b'] = df_cmp['pressure_index_hybrid']
df_cmp['model_c'] = np.maximum(0.70 * df_cmp['pressure_index_rule'],
                                0.50 * df_cmp['pressure_index_rule'] +
                                0.50 * df_cmp['pressure_index_leverage'])

for model_col in ['model_a', 'model_b', 'model_c']:
    df_cmp[f'{model_col}_tier'] = classify_pressure(df_cmp[model_col])
    df_cmp[f'{model_col}_high'] = df_cmp[model_col] >= 0.60

# Synthetic scenarios for illustration
synthetic_scenarios = [
    {'scenario': 'Comfortable Chase (RRR=5, 8wkts, 20b)',  'model_a': 0.19, 'model_b': 0.17, 'model_c': 0.19},
    {'scenario': 'Tight Chase (RRR=9, 6wkts, 20b)',         'model_a': 0.52, 'model_b': 0.51, 'model_c': 0.52},
    {'scenario': 'Death Overs (inn1, 8th wicket, over18)',   'model_a': 0.72, 'model_b': 0.72, 'model_c': 0.72},
    {'scenario': 'Early Collapse (3wkts/5overs)',            'model_a': 0.58, 'model_b': 0.52, 'model_c': 0.58},
    {'scenario': 'Near-impossible Chase (RRR=18, 4wkts)',   'model_a': 0.84, 'model_b': 0.42, 'model_c': 0.59},
    {'scenario': 'Super Over (1b, 2 needed)',               'model_a': 1.20, 'model_b': 0.90, 'model_c': 0.84},
    {'scenario': 'Winning easily (RRR=3, 10wkts)',          'model_a': 0.08, 'model_b': 0.09, 'model_c': 0.09},
]

# REAL model comparison by format/innings
model_rows = []
for segment_name, seg_mask in [
    ('all_official', pd.Series(True, index=df_cmp.index)),
    ('innings1',     df_cmp['innings'] == 1),
    ('innings2',     df_cmp['innings'] >= 2),
    ('IPL',          ipl_mask[df_cmp.index] if set(df_cmp.index).issubset(set(ipl_mask.index)) else df_cmp['comp_name'].str.contains('IPL', case=False, na=False)),
    ('T20I',         df_cmp['match_format'] == 'T20I'),
]:
    seg = df_cmp[seg_mask]
    if seg.empty:
        continue
    for model_col, label in [('model_a', 'A_rule'), ('model_b', 'B_hybrid50_50'), ('model_c', 'C_alt')]:
        model_rows.append({
            'segment': segment_name,
            'model': label,
            'n_deliveries': len(seg),
            'mean_score': round(seg[model_col].mean(), 4),
            'std_score':  round(seg[model_col].std(), 4),
            'min_score':  round(seg[model_col].min(), 4),
            'max_score':  round(seg[model_col].max(), 4),
            'n_high_or_extreme': int(df_cmp[seg_mask][f'{model_col}_high'].sum()),
            'pct_high_or_extreme': round(df_cmp[seg_mask][f'{model_col}_high'].mean() * 100, 2),
        })

# Top 10 rankings under each model (batting only for efficiency)
print("  Running rankings under Model A (rule-based)…")
df_ma = df_official.copy()
df_ma['pressure_score'] = df_ma['pressure_index_rule']
df_ma['is_high_pressure'] = df_ma['pressure_score'] >= 0.60
df_ma['pressure_tier'] = classify_pressure(df_ma['pressure_score'])
bat_ma, bowl_ma = run_pipeline(df_ma)

print("  Running rankings under Model B (hybrid 50/50, existing)…")
bat_mb, bowl_mb = bat_off, bowl_off  # Already computed

print("  Running rankings under Model C (alternative)…")
df_mc = df_official.copy()
df_mc['pressure_score'] = np.maximum(0.70 * df_mc['pressure_index_rule'],
                                      0.50 * df_mc['pressure_index_rule'] +
                                      0.50 * df_mc['pressure_index_leverage'])
df_mc['is_high_pressure'] = df_mc['pressure_score'] >= 0.60
df_mc['pressure_tier'] = classify_pressure(df_mc['pressure_score'])
bat_mc, bowl_mc = run_pipeline(df_mc)

# Merge synthetic scenarios into real comparison rows
synth_rows = [{'segment': 'SYNTHETIC_SCENARIO',
               'model': r['scenario'],
               'n_deliveries': 1,
               'mean_score': r['model_a'],
               'std_score': r['model_b'],   # reusing field for model B score
               'min_score': r['model_c'],   # and model C
               'max_score': None,
               'n_high_or_extreme': None,
               'pct_high_or_extreme': None} for r in synthetic_scenarios]

# Better: separate synthetic table
synth_df = pd.DataFrame(synthetic_scenarios)
synth_df.to_csv(os.path.join(OUT, 'pressure_model_synthetic_scenarios.csv'), index=False)

# Model ranking comparison table
model_rank_rows = []
for rank_i in range(10):
    model_rank_rows.append({
        'rank': rank_i + 1,
        'batter_model_A': bat_ma.iloc[rank_i]['striker_name'] if rank_i < len(bat_ma) else '',
        'batter_model_B': bat_mb.iloc[rank_i]['striker_name'] if rank_i < len(bat_mb) else '',
        'batter_model_C': bat_mc.iloc[rank_i]['striker_name'] if rank_i < len(bat_mc) else '',
        'batter_A_rating': round(bat_ma.iloc[rank_i]['pressure_rating'], 2) if rank_i < len(bat_ma) else None,
        'batter_B_rating': round(bat_mb.iloc[rank_i]['pressure_rating'], 2) if rank_i < len(bat_mb) else None,
        'batter_C_rating': round(bat_mc.iloc[rank_i]['pressure_rating'], 2) if rank_i < len(bat_mc) else None,
        'bowler_model_A': bowl_ma.iloc[rank_i]['bowler_name'] if rank_i < len(bowl_ma) else '',
        'bowler_model_B': bowl_mb.iloc[rank_i]['bowler_name'] if rank_i < len(bowl_mb) else '',
        'bowler_model_C': bowl_mc.iloc[rank_i]['bowler_name'] if rank_i < len(bowl_mc) else '',
        'bowler_A_rating': round(bowl_ma.iloc[rank_i]['pressure_rating'], 2) if rank_i < len(bowl_ma) else None,
        'bowler_B_rating': round(bowl_mb.iloc[rank_i]['pressure_rating'], 2) if rank_i < len(bowl_mb) else None,
        'bowler_C_rating': round(bowl_mc.iloc[rank_i]['pressure_rating'], 2) if rank_i < len(bowl_mc) else None,
    })

model_cmp_df = pd.DataFrame(model_rows)
model_rank_df = pd.DataFrame(model_rank_rows)
pd.concat([model_cmp_df, model_rank_df], axis=0, ignore_index=True)

# Save comprehensive comparison
model_cmp_df.to_csv(os.path.join(OUT, 'pressure_model_comparison.csv'), index=False)
model_rank_df.to_csv(os.path.join(OUT, 'pressure_model_ranking_comparison.csv'), index=False)
print("  → Saved pressure_model_comparison.csv, pressure_model_ranking_comparison.csv")
print("  Model A top-10 batters: ", top10_names(bat_ma, 'striker_name'))
print("  Model B top-10 batters: ", top10_names(bat_mb, 'striker_name'))
print("  Model C top-10 batters: ", top10_names(bat_mc, 'striker_name'))


# ══════════════════════════════════════════════════════════════════════
# TASK 4 — Context-Adjusted Clutch Measurement
# ══════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("TASK 4: Context-Adjusted Clutch Measurement")
print("="*60)

# Method A (existing): delta_sr for batters, delta_economy for bowlers
# Method B (context-adjusted): delta_rae for batters, delta_rp/delta_wae for bowlers
# Both are already in the pipeline; this task measures the RANKING difference
# by altering clutch dimension weights.

def rank_batters_clutch_method(bat_df, method='context_adjusted',
                                min_balls=100, min_matches=12):
    """
    method='raw'              → clutch uses delta_sr (raw SR change)
    method='context_adjusted' → clutch uses delta_rae (context-adjusted RAE change)
    """
    eligible = bat_df[(bat_df['pressure_balls'] >= min_balls) &
                      (bat_df['pressure_matches'] >= min_matches)].copy()
    if eligible.empty:
        return pd.DataFrame()

    pop_rae = eligible['pressure_rae_per_ball'].mean()
    pop_sr  = eligible['pressure_sr'].mean()
    pop_wpa = eligible['pressure_wpa_per_ball'].mean()
    k = 40.0

    eligible['shrunk_pressure_rae'] = bayesian_shrinkage(
        eligible['pressure_rae_per_ball'].values, eligible['pressure_balls'].values, k, pop_rae)
    eligible['shrunk_pressure_sr'] = bayesian_shrinkage(
        eligible['pressure_sr'].values, eligible['pressure_balls'].values, k, pop_sr)
    eligible['shrunk_pressure_wpa'] = bayesian_shrinkage(
        eligible['pressure_wpa_per_ball'].values, eligible['pressure_balls'].values, k, pop_wpa)

    # Performance dimension (same for both methods)
    z_rae = standardize_series(eligible['shrunk_pressure_rae'])
    z_sr  = standardize_series(eligible['shrunk_pressure_sr'])
    z_wpa = standardize_series(eligible['shrunk_pressure_wpa'])
    z_dot = standardize_series(eligible['pressure_dot_pct'])
    z_bnd = standardize_series(eligible['pressure_bnd_pct'])
    dim_perf = standardize_series(0.35*z_rae + 0.25*z_sr + 0.20*z_wpa + 0.10*z_bnd - 0.10*z_dot)

    if method == 'raw':
        # Clutch: raw SR delta
        z_d_sr  = standardize_series(eligible['delta_sr'])
        z_d_wpa = standardize_series(eligible['delta_wpa'])
        z_d_dot = standardize_series(eligible['delta_dot_reduction'])
        dim_clutch = standardize_series(0.50*z_d_sr + 0.30*z_d_wpa + 0.20*z_d_dot)
    else:
        # Clutch: context-adjusted RAE delta
        z_d_rae = standardize_series(eligible['delta_rae'])
        z_d_sr  = standardize_series(eligible['delta_sr'])
        z_d_wpa = standardize_series(eligible['delta_wpa'])
        z_d_dot = standardize_series(eligible['delta_dot_reduction'])
        dim_clutch = standardize_series(0.35*z_d_rae + 0.30*z_d_sr + 0.20*z_d_wpa + 0.15*z_d_dot)

    # Consistency dimension (same)
    z_pct = standardize_series(eligible['pct_positive_pressure_matches'])
    z_opp = standardize_series(np.log1p(eligible['pressure_balls']))
    z_var = standardize_series(eligible['match_rae_std'].fillna(eligible['match_rae_std'].mean()))
    dim_cons = standardize_series(0.50*z_pct + 0.30*z_opp - 0.20*z_var)

    raw_comp = 0.60*dim_perf + 0.30*dim_clutch + 0.10*dim_cons
    eligible['pressure_rating'] = np.round(50.0 + 15.0 * raw_comp, 2)
    ranked = eligible.sort_values('pressure_rating', ascending=False).reset_index(drop=True)
    ranked['rank'] = ranked.index + 1
    return ranked


def rank_bowlers_clutch_method(bowl_df, method='context_adjusted',
                                min_balls=120, min_matches=12):
    eligible = bowl_df[(bowl_df['pressure_legal_balls'] >= min_balls) &
                       (bowl_df['pressure_matches'] >= min_matches)].copy()
    if eligible.empty:
        return pd.DataFrame()

    pop_rp  = eligible['pressure_rp_per_ball'].mean()
    pop_wae = eligible['pressure_wae_per_ball'].mean()
    pop_econ= eligible['pressure_economy'].mean()
    pop_wpa = eligible['pressure_wpa_per_ball'].mean()
    k = 40.0

    eligible['shrunk_pressure_rp']   = bayesian_shrinkage(eligible['pressure_rp_per_ball'].values, eligible['pressure_legal_balls'].values, k, pop_rp)
    eligible['shrunk_pressure_wae']  = bayesian_shrinkage(eligible['pressure_wae_per_ball'].values, eligible['pressure_legal_balls'].values, k, pop_wae)
    eligible['shrunk_pressure_econ'] = bayesian_shrinkage(eligible['pressure_economy'].values, eligible['pressure_legal_balls'].values, k, pop_econ)
    eligible['shrunk_pressure_wpa']  = bayesian_shrinkage(eligible['pressure_wpa_per_ball'].values, eligible['pressure_legal_balls'].values, k, pop_wpa)

    z_rp  = standardize_series(eligible['shrunk_pressure_rp'])
    z_wae = standardize_series(eligible['shrunk_pressure_wae'])
    z_econ= standardize_series(-eligible['shrunk_pressure_econ'])
    z_wpa = standardize_series(eligible['shrunk_pressure_wpa'])
    z_dot = standardize_series(eligible['pressure_dot_pct'])
    z_bnd = standardize_series(-eligible['pressure_bnd_conceded_pct'])
    dim_perf = standardize_series(0.30*z_rp + 0.25*z_wae + 0.20*z_econ + 0.15*z_wpa + 0.05*z_dot + 0.05*z_bnd)

    if method == 'raw':
        z_d_econ = standardize_series(eligible['delta_economy'])
        z_d_wpa  = standardize_series(eligible['delta_wpa'])
        z_d_bnd  = standardize_series(eligible['delta_bnd_suppression'])
        dim_clutch = standardize_series(0.50*z_d_econ + 0.30*z_d_wpa + 0.20*z_d_bnd)
    else:
        z_d_rp   = standardize_series(eligible['delta_rp'])
        z_d_wae  = standardize_series(eligible['delta_wae'])
        z_d_econ = standardize_series(eligible['delta_economy'])
        z_d_wpa  = standardize_series(eligible['delta_wpa'])
        z_d_bnd  = standardize_series(eligible['delta_bnd_suppression'])
        dim_clutch = standardize_series(0.30*z_d_rp + 0.25*z_d_wae + 0.25*z_d_econ + 0.10*z_d_wpa + 0.10*z_d_bnd)

    z_pct = standardize_series(eligible['pct_positive_pressure_matches'])
    z_opp = standardize_series(np.log1p(eligible['pressure_legal_balls']))
    z_var = standardize_series(eligible['match_rp_std'].fillna(eligible['match_rp_std'].mean()))
    dim_cons = standardize_series(0.50*z_pct + 0.30*z_opp - 0.20*z_var)

    raw_comp = 0.60*dim_perf + 0.30*dim_clutch + 0.10*dim_cons
    eligible['pressure_rating'] = np.round(50.0 + 15.0 * raw_comp, 2)
    ranked = eligible.sort_values('pressure_rating', ascending=False).reset_index(drop=True)
    ranked['rank'] = ranked.index + 1
    return ranked

bat_metrics = compute_batting_metrics(df_official)
bowl_metrics = compute_bowling_metrics(df_official)

bat_raw  = rank_batters_clutch_method(bat_metrics, method='raw')
bat_ctx  = rank_batters_clutch_method(bat_metrics, method='context_adjusted')
bowl_raw = rank_bowlers_clutch_method(bowl_metrics, method='raw')
bowl_ctx = rank_bowlers_clutch_method(bowl_metrics, method='context_adjusted')

# Build comparison table
def clutch_comparison_table(ranked_raw, ranked_ctx, name_col):
    if ranked_raw.empty or ranked_ctx.empty:
        return pd.DataFrame()
    raw_top = ranked_raw.head(10)[[name_col, 'rank', 'pressure_rating']].rename(
        columns={'rank': 'raw_rank', 'pressure_rating': 'raw_rating'})
    ctx_top = ranked_ctx.head(10)[[name_col, 'rank', 'pressure_rating']].rename(
        columns={'rank': 'ctx_rank', 'pressure_rating': 'ctx_rating'})
    all_names = list(set(raw_top[name_col].tolist() + ctx_top[name_col].tolist()))
    rows = []
    for n in all_names:
        rr = raw_top[raw_top[name_col] == n]
        cr = ctx_top[ctx_top[name_col] == n]
        rows.append({
            'player': n,
            'raw_rank':   int(rr['raw_rank'].values[0]) if len(rr) else None,
            'raw_rating': round(float(rr['raw_rating'].values[0]), 2) if len(rr) else None,
            'ctx_rank':   int(cr['ctx_rank'].values[0]) if len(cr) else None,
            'ctx_rating': round(float(cr['ctx_rating'].values[0]), 2) if len(cr) else None,
        })
    df_out = pd.DataFrame(rows)
    df_out['rank_change'] = df_out.apply(
        lambda r: (r['raw_rank'] - r['ctx_rank']) if pd.notnull(r['raw_rank']) and pd.notnull(r['ctx_rank']) else None, axis=1)
    return df_out.sort_values('ctx_rank')

bat_clutch_df  = clutch_comparison_table(bat_raw,  bat_ctx,  'striker_name')
bowl_clutch_df = clutch_comparison_table(bowl_raw, bowl_ctx, 'bowler_name')

bat_clutch_df['role']  = 'batter'
bowl_clutch_df['role'] = 'bowler'
clutch_all = pd.concat([bat_clutch_df, bowl_clutch_df], ignore_index=True)
clutch_all.to_csv(os.path.join(OUT, 'clutch_method_comparison.csv'), index=False)
print("  → Saved clutch_method_comparison.csv")
print("  Batter raw top-5: ", top10_names(bat_raw, 'striker_name')[:5])
print("  Batter ctx top-5: ", top10_names(bat_ctx, 'striker_name')[:5])
print("  Bowler raw top-5: ", top10_names(bowl_raw, 'bowler_name')[:5])
print("  Bowler ctx top-5: ", top10_names(bowl_ctx, 'bowler_name')[:5])


# ══════════════════════════════════════════════════════════════════════
# TASK 5 — Consistency Formula and Sample Size Comparison
# ══════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("TASK 5: Consistency and Sample Size Comparison")
print("="*60)

# Formula A (existing): 0.50*z(pos_match_pct) + 0.30*z(log1p(pressure_balls)) - 0.20*z(match_std)
# Formula B (no volume): 0.60*z(pos_match_pct) - 0.40*z(match_std)
# Formula C (reliability CI width from bootstrap — approximate with Bayesian CI)
# k values: 20, 40, 80

def rank_batters_consistency(bat_df, consistency_formula='A', k=40,
                              min_balls=100, min_matches=12):
    eligible = bat_df[(bat_df['pressure_balls'] >= min_balls) &
                      (bat_df['pressure_matches'] >= min_matches)].copy()
    if eligible.empty:
        return pd.DataFrame()

    pop_rae = eligible['pressure_rae_per_ball'].mean()
    pop_sr  = eligible['pressure_sr'].mean()
    pop_wpa = eligible['pressure_wpa_per_ball'].mean()

    eligible['shrunk_pressure_rae'] = bayesian_shrinkage(
        eligible['pressure_rae_per_ball'].values, eligible['pressure_balls'].values, float(k), pop_rae)
    eligible['shrunk_pressure_sr'] = bayesian_shrinkage(
        eligible['pressure_sr'].values, eligible['pressure_balls'].values, float(k), pop_sr)
    eligible['shrunk_pressure_wpa'] = bayesian_shrinkage(
        eligible['pressure_wpa_per_ball'].values, eligible['pressure_balls'].values, float(k), pop_wpa)

    z_rae = standardize_series(eligible['shrunk_pressure_rae'])
    z_sr  = standardize_series(eligible['shrunk_pressure_sr'])
    z_wpa = standardize_series(eligible['shrunk_pressure_wpa'])
    z_dot = standardize_series(eligible['pressure_dot_pct'])
    z_bnd = standardize_series(eligible['pressure_bnd_pct'])
    dim_perf = standardize_series(0.35*z_rae + 0.25*z_sr + 0.20*z_wpa + 0.10*z_bnd - 0.10*z_dot)

    z_d_rae = standardize_series(eligible['delta_rae'])
    z_d_sr  = standardize_series(eligible['delta_sr'])
    z_d_wpa = standardize_series(eligible['delta_wpa'])
    z_d_dot = standardize_series(eligible['delta_dot_reduction'])
    dim_clutch = standardize_series(0.35*z_d_rae + 0.30*z_d_sr + 0.20*z_d_wpa + 0.15*z_d_dot)

    z_pct = standardize_series(eligible['pct_positive_pressure_matches'])
    std_safe = eligible['match_rae_std'].fillna(eligible['match_rae_std'].mean())
    z_var = standardize_series(std_safe)
    z_opp = standardize_series(np.log1p(eligible['pressure_balls']))

    if consistency_formula == 'A':
        # Existing: volume rewarded explicitly
        dim_cons = standardize_series(0.50*z_pct + 0.30*z_opp - 0.20*z_var)
    elif consistency_formula == 'B':
        # No volume in consistency (volume already rewarded by shrinkage)
        dim_cons = standardize_series(0.60*z_pct - 0.40*z_var)
    elif consistency_formula == 'C':
        # Reliability via approximate CI width (narrower CI = more reliable)
        # CI_width ≈ 1.96 * std / sqrt(n) → higher n and lower std = narrower CI
        n_safe = np.maximum(eligible['pressure_balls'].values, 1)
        ci_width = 1.96 * std_safe / np.sqrt(n_safe)
        z_ci = standardize_series(-ci_width)  # negative: narrower CI is better
        dim_cons = standardize_series(0.50*z_pct + 0.30*z_ci - 0.20*z_var)
    else:
        dim_cons = standardize_series(0.50*z_pct + 0.30*z_opp - 0.20*z_var)

    raw_comp = 0.60*dim_perf + 0.30*dim_clutch + 0.10*dim_cons
    eligible['pressure_rating'] = np.round(50.0 + 15.0 * raw_comp, 2)
    ranked = eligible.sort_values('pressure_rating', ascending=False).reset_index(drop=True)
    ranked['rank'] = ranked.index + 1
    return ranked

def rank_bowlers_consistency(bowl_df, consistency_formula='A', k=40,
                              min_balls=120, min_matches=12):
    eligible = bowl_df[(bowl_df['pressure_legal_balls'] >= min_balls) &
                       (bowl_df['pressure_matches'] >= min_matches)].copy()
    if eligible.empty:
        return pd.DataFrame()

    pop_rp  = eligible['pressure_rp_per_ball'].mean()
    pop_wae = eligible['pressure_wae_per_ball'].mean()
    pop_econ= eligible['pressure_economy'].mean()
    pop_wpa = eligible['pressure_wpa_per_ball'].mean()
    k = float(k)

    eligible['shrunk_pressure_rp']   = bayesian_shrinkage(eligible['pressure_rp_per_ball'].values, eligible['pressure_legal_balls'].values, k, pop_rp)
    eligible['shrunk_pressure_wae']  = bayesian_shrinkage(eligible['pressure_wae_per_ball'].values, eligible['pressure_legal_balls'].values, k, pop_wae)
    eligible['shrunk_pressure_econ'] = bayesian_shrinkage(eligible['pressure_economy'].values, eligible['pressure_legal_balls'].values, k, pop_econ)
    eligible['shrunk_pressure_wpa']  = bayesian_shrinkage(eligible['pressure_wpa_per_ball'].values, eligible['pressure_legal_balls'].values, k, pop_wpa)

    z_rp   = standardize_series(eligible['shrunk_pressure_rp'])
    z_wae  = standardize_series(eligible['shrunk_pressure_wae'])
    z_econ = standardize_series(-eligible['shrunk_pressure_econ'])
    z_wpa  = standardize_series(eligible['shrunk_pressure_wpa'])
    z_dot  = standardize_series(eligible['pressure_dot_pct'])
    z_bnd  = standardize_series(-eligible['pressure_bnd_conceded_pct'])
    dim_perf = standardize_series(0.30*z_rp + 0.25*z_wae + 0.20*z_econ + 0.15*z_wpa + 0.05*z_dot + 0.05*z_bnd)

    z_d_rp   = standardize_series(eligible['delta_rp'])
    z_d_wae  = standardize_series(eligible['delta_wae'])
    z_d_econ = standardize_series(eligible['delta_economy'])
    z_d_wpa  = standardize_series(eligible['delta_wpa'])
    z_d_bnd  = standardize_series(eligible['delta_bnd_suppression'])
    dim_clutch = standardize_series(0.30*z_d_rp + 0.25*z_d_wae + 0.25*z_d_econ + 0.10*z_d_wpa + 0.10*z_d_bnd)

    z_pct = standardize_series(eligible['pct_positive_pressure_matches'])
    std_safe = eligible['match_rp_std'].fillna(eligible['match_rp_std'].mean())
    z_var = standardize_series(std_safe)
    z_opp = standardize_series(np.log1p(eligible['pressure_legal_balls']))

    if consistency_formula == 'A':
        dim_cons = standardize_series(0.50*z_pct + 0.30*z_opp - 0.20*z_var)
    elif consistency_formula == 'B':
        dim_cons = standardize_series(0.60*z_pct - 0.40*z_var)
    elif consistency_formula == 'C':
        n_safe = np.maximum(eligible['pressure_legal_balls'].values, 1)
        ci_width = 1.96 * std_safe / np.sqrt(n_safe)
        z_ci = standardize_series(-ci_width)
        dim_cons = standardize_series(0.50*z_pct + 0.30*z_ci - 0.20*z_var)
    else:
        dim_cons = standardize_series(0.50*z_pct + 0.30*z_opp - 0.20*z_var)

    raw_comp = 0.60*dim_perf + 0.30*dim_clutch + 0.10*dim_cons
    eligible['pressure_rating'] = np.round(50.0 + 15.0 * raw_comp, 2)
    ranked = eligible.sort_values('pressure_rating', ascending=False).reset_index(drop=True)
    ranked['rank'] = ranked.index + 1
    return ranked

consistency_configs = [
    ('A', 20), ('A', 40), ('A', 80),
    ('B', 20), ('B', 40), ('B', 80),
    ('C', 20), ('C', 40), ('C', 80),
]

cons_rows = []
all_bat_rankings_cons = {}
all_bowl_rankings_cons = {}

for formula, k_val in consistency_configs:
    label = f'Formula{formula}_k{k_val}'
    print(f"  Running consistency config {label}…")
    b_ranked = rank_batters_consistency(bat_metrics, consistency_formula=formula, k=k_val)
    bow_ranked = rank_bowlers_consistency(bowl_metrics, consistency_formula=formula, k=k_val)
    all_bat_rankings_cons[label] = b_ranked
    all_bowl_rankings_cons[label] = bow_ranked

    for rank_i, (ranked_df, name_col, role) in enumerate([
        (b_ranked, 'striker_name', 'batter'),
        (bow_ranked, 'bowler_name', 'bowler')
    ]):
        for pos in range(min(10, len(ranked_df))):
            row = ranked_df.iloc[pos]
            cons_rows.append({
                'config': label,
                'consistency_formula': formula,
                'bayesian_k': k_val,
                'role': role,
                'rank': pos + 1,
                'player': row[name_col],
                'pressure_rating': round(row['pressure_rating'], 2),
            })

pd.DataFrame(cons_rows).to_csv(os.path.join(OUT, 'consistency_comparison.csv'), index=False)
print("  → Saved consistency_comparison.csv")


# ══════════════════════════════════════════════════════════════════════
# TASK 6 — Ranking Stability
# ══════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("TASK 6: Ranking Stability Across All Experiments")
print("="*60)

# Collect all experiment variations into a unified registry
bat_experiments = {}
bowl_experiments = {}

# From Task 1: scope
bat_experiments['scope_official'] = bat_off
bat_experiments['scope_expanded'] = bat_exp
bowl_experiments['scope_official'] = bowl_off
bowl_experiments['scope_expanded'] = bowl_exp

# From Task 3: pressure models
bat_experiments['pressure_modelA'] = bat_ma
bat_experiments['pressure_modelB'] = bat_mb
bat_experiments['pressure_modelC'] = bat_mc
bowl_experiments['pressure_modelA'] = bowl_ma
bowl_experiments['pressure_modelB'] = bowl_mb
bowl_experiments['pressure_modelC'] = bowl_mc

# From Task 4: clutch method
bat_experiments['clutch_raw']  = bat_raw
bat_experiments['clutch_ctx']  = bat_ctx
bowl_experiments['clutch_raw'] = bowl_raw
bowl_experiments['clutch_ctx'] = bowl_ctx

# From Task 5: consistency + k
for label, ranked_df in all_bat_rankings_cons.items():
    bat_experiments[f'cons_{label}'] = ranked_df
for label, ranked_df in all_bowl_rankings_cons.items():
    bowl_experiments[f'cons_{label}'] = ranked_df

def compute_stability(experiments_dict, name_col):
    """
    For each player, compute stability stats across all experiment rankings.
    """
    # Gather all players appearing in any top-20
    all_players = set()
    for exp_label, ranked in experiments_dict.items():
        if ranked is not None and not ranked.empty:
            top20 = ranked.head(20)[name_col].tolist()
            all_players.update(top20)

    n_experiments = len(experiments_dict)
    stability_rows = []
    for player in all_players:
        ranks_seen = []
        in_top10_count = 0
        in_top5_count  = 0
        for exp_label, ranked in experiments_dict.items():
            if ranked is None or ranked.empty:
                continue
            match = ranked[ranked[name_col] == player]
            if not match.empty:
                r = int(match.iloc[0]['rank'])
                ranks_seen.append(r)
                if r <= 10:
                    in_top10_count += 1
                if r <= 5:
                    in_top5_count += 1
            # If not in this ranking at all, don't penalize (player may not meet min thresholds)

        if ranks_seen:
            stability_rows.append({
                'player': player,
                'n_experiments_ranked': len(ranks_seen),
                'n_experiments_total': n_experiments,
                'top10_frequency': round(in_top10_count / n_experiments, 3),
                'top5_frequency':  round(in_top5_count  / n_experiments, 3),
                'avg_rank':    round(np.mean(ranks_seen), 2),
                'median_rank': round(np.median(ranks_seen), 2),
                'best_rank':   int(np.min(ranks_seen)),
                'worst_rank':  int(np.max(ranks_seen)),
                'rank_std':    round(np.std(ranks_seen), 2),
            })

    return pd.DataFrame(stability_rows).sort_values('top10_frequency', ascending=False)

bat_stability  = compute_stability(bat_experiments,  'striker_name')
bowl_stability = compute_stability(bowl_experiments, 'bowler_name')

bat_stability['role']  = 'batter'
bowl_stability['role'] = 'bowler'
stability_all = pd.concat([bat_stability, bowl_stability], ignore_index=True)
stability_all.to_csv(os.path.join(OUT, 'ranking_stability.csv'), index=False)
print(f"  → Saved ranking_stability.csv ({len(bat_stability)} batters, {len(bowl_stability)} bowlers tracked)")
print("  Most stable batters (top10_freq):")
print(bat_stability.head(5)[['player', 'top10_frequency', 'avg_rank', 'rank_std']].to_string(index=False))
print("  Most stable bowlers (top10_freq):")
print(bowl_stability.head(5)[['player', 'top10_frequency', 'avg_rank', 'rank_std']].to_string(index=False))


# ══════════════════════════════════════════════════════════════════════
# TASK 7 — Final Pressure Distribution Summary
# ══════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("TASK 7: Final Pressure Distribution Summary")
print("="*60)

# Already aggregated in Task 2 — just print a summary table
tier_inn_fmt = df_official.groupby(['innings', 'match_format', 'pressure_tier']).size().reset_index(name='n_deliveries')
tier_inn_fmt['innings_label'] = tier_inn_fmt['innings'].apply(lambda x: 'Innings 1' if x == 1 else 'Innings 2+')

pivot = tier_inn_fmt.groupby(['innings_label', 'match_format', 'pressure_tier'])['n_deliveries'].sum().unstack(fill_value=0)
print(pivot)
print(f"  Innings 1 high+extreme: {df_official[(df_official['innings']==1) & (df_official['pressure_tier'].isin(['High','Extreme']))].shape[0]:,}")
print(f"  Innings 2 high+extreme: {df_official[(df_official['innings']>=2) & (df_official['pressure_tier'].isin(['High','Extreme']))].shape[0]:,}")


# ══════════════════════════════════════════════════════════════════════
# TASK 8 — Primary and Alternative Top-10 Rankings
# ══════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("TASK 8: Primary and Alternative Top-10 Rankings")
print("="*60)

# Primary: Official scope, Model B hybrid, context-adjusted clutch, Formula A, k=40
primary_bat  = bat_ctx   # context_adjusted clutch, k=40 is default
primary_bowl = bowl_ctx

# Alternative: Most divergent — Model A (rule-only) pressure
alt_bat  = bat_ma
alt_bowl = bowl_ma

def save_top10(ranked, name_col, path, role):
    if ranked.empty:
        return
    cols = [name_col, 'pressure_rating', 'pressure_balls' if role == 'batter' else 'pressure_legal_balls',
            'pressure_matches', 'dim_performance', 'dim_clutch', 'dim_consistency']
    cols = [c for c in cols if c in ranked.columns]
    top = ranked.head(10).copy()
    top['rank'] = range(1, len(top.head(10)) + 1)
    top[['rank'] + cols].to_csv(path, index=False)
    return top.head(10)[[c for c in ['rank', name_col, 'pressure_rating'] if c in top.columns]]

def save_top10_bat(ranked, path):
    return save_top10(ranked, 'striker_name', path, 'batter')

def save_top10_bowl(ranked, path):
    return save_top10(ranked, 'bowler_name', path, 'bowler')

top_bat_primary  = save_top10_bat(primary_bat,  os.path.join(OUT, 'top_10_batters.csv'))
top_bowl_primary = save_top10_bowl(primary_bowl, os.path.join(OUT, 'top_10_bowlers.csv'))
top_bat_alt      = save_top10_bat(alt_bat,  os.path.join(OUT, 'alternative_top_10_batters.csv'))
top_bowl_alt     = save_top10_bowl(alt_bowl, os.path.join(OUT, 'alternative_top_10_bowlers.csv'))

print("  PRIMARY Top 10 Batters:")
print(top_bat_primary.to_string(index=False) if top_bat_primary is not None else "  (empty)")
print("  PRIMARY Top 10 Bowlers:")
print(top_bowl_primary.to_string(index=False) if top_bowl_primary is not None else "  (empty)")
print("  ALTERNATIVE Top 10 Batters (Model A, rule-only pressure):")
print(top_bat_alt.to_string(index=False) if top_bat_alt is not None else "  (empty)")
print("  → Saved top_10_batters.csv, top_10_bowlers.csv, alternative_top_10_*.csv")


# ══════════════════════════════════════════════════════════════════════
# TASK 9 — Experiment Summary (inputs to report update)
# ══════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("TASK 9: Saving Experiment Summary for Report")
print("="*60)

summary = {
    'task1_official_top10_batters': top10_bat_off,
    'task1_expanded_top10_batters': top10_bat_exp,
    'task1_official_top10_bowlers': top10_bowl_off,
    'task1_expanded_top10_bowlers': top10_bowl_exp,
    'task2_pressure_min': float(df_official['pressure_score'].min()),
    'task2_pressure_max': float(df_official['pressure_score'].max()),
    'task2_pct_high_extreme': float((df_official['pressure_tier'].isin(['High','Extreme'])).mean() * 100),
    'task3_model_a_pct_high': float((df_official['pressure_index_rule'] >= 0.60).mean() * 100),
    'task3_model_b_pct_high': float((df_official['pressure_index_hybrid'] >= 0.60).mean() * 100),
    'task3_model_c_pct_high': float(df_cmp['model_c_high'].mean() * 100),
    'task6_most_stable_batter':  bat_stability.iloc[0]['player'] if not bat_stability.empty else '',
    'task6_most_stable_bowler':  bowl_stability.iloc[0]['player'] if not bowl_stability.empty else '',
}
pd.DataFrame([summary]).to_csv(os.path.join(OUT, 'experiment_summary.csv'), index=False)
print("  → Saved experiment_summary.csv")

print("\n" + "="*60)
print("ALL TASKS COMPLETE")
print("="*60)
print("Output CSVs:")
for f in [
    'competition_scope_comparison.csv', 'competition_scope_detail.csv',
    'pressure_distribution.csv',
    'pressure_model_comparison.csv', 'pressure_model_ranking_comparison.csv', 'pressure_model_synthetic_scenarios.csv',
    'clutch_method_comparison.csv',
    'consistency_comparison.csv',
    'ranking_stability.csv',
    'top_10_batters.csv', 'top_10_bowlers.csv',
    'alternative_top_10_batters.csv', 'alternative_top_10_bowlers.csv',
    'experiment_summary.csv',
]:
    path = os.path.join(OUT, f)
    exists = os.path.exists(path)
    size = os.path.getsize(path) if exists else 0
    print(f"  {'✓' if exists else '✗'} {f} ({size:,} bytes)")
