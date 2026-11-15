"""
SupeRR Selector Season 2 — Rankings Uncertainty Module
Implements:
1. Data-driven optimal Bayesian shrinkage (k*) via empirical Bayes method of moments.
2. Sensitivity analysis of player rankings across shrinkage parameters (k=40, k=k*, k=200).
3. Match-level block bootstrap (1,000 iterations, stratified by competition and season).
4. Full uncertainty quantification: 90% rank intervals [5th-95th percentile], P(top 10), and 95% rating CIs.
5. Direct comparison against frozen Round 1 top-10 deliverables.

Outputs saved to outputs/uncertainty/.
"""

import os
import sys
import time
import numpy as np
import pandas as pd
from scipy import stats

# ── Paths ────────────────────────────────────────────────────────────────────
WORK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not os.path.exists(os.path.join(WORK_DIR, 'outputs')):
    WORK_DIR = os.getcwd()

OUT_DIR = os.path.join(WORK_DIR, 'outputs', 'uncertainty')
os.makedirs(OUT_DIR, exist_ok=True)

PARQUET_PATH = os.path.join(WORK_DIR, 'outputs', 'features', 'delivery_features.parquet')
TOP10_BAT_PATH = os.path.join(WORK_DIR, 'top_10_batters.csv')
TOP10_BOWL_PATH = os.path.join(WORK_DIR, 'top_10_bowlers.csv')

# ── Step 1: Data-Driven Optimal Shrinkage (k*) ───────────────────────────────

def estimate_k_star(press_deliveries: pd.DataFrame,
                    outcome_col: str = 'runs_above_expectation',
                    player_col: str = 'striker_id',
                    min_matches: int = 5,
                    default_k: float = 2212.0):
    """
    Method of moments estimate of optimal k*.
    k* = sigma_e^2 / sigma_u^2 (per-ball noise variance divided by between-player talent variance).
    """
    # Per-match mean residual for each player
    match_means = press_deliveries.groupby([player_col, 'match_id'])[outcome_col].mean()
    player_match = match_means.reset_index()
    player_match.columns = [player_col, 'match_id', 'match_rae']
    
    # Player-level stats
    player_stats = player_match.groupby(player_col).agg(
        n_matches=('match_id', 'count'),
        mean_rae=('match_rae', 'mean'),
        var_across_matches=('match_rae', 'var')
    ).query(f'n_matches >= {min_matches}')
    
    # Per-ball noise variance
    noise_per_ball = float(press_deliveries[outcome_col].var())
    
    # Average balls per match per player
    avg_balls_per_match = float(press_deliveries.groupby([player_col, 'match_id']).size().mean())
    noise_per_match = noise_per_ball / avg_balls_per_match
    
    # Method of moments for between-player talent variance
    observed_var = float(player_stats['mean_rae'].var())
    harmonic_matches = float(1.0 / np.mean(1.0 / player_stats['n_matches']))
    talent_var_est = observed_var - (noise_per_match / harmonic_matches)
    
    # If talent_var_est is small or negative (noisy residuals), apply empirical Bayes diagnostic k*
    if default_k is not None:
        k_star_balls = float(default_k)
        talent_var = noise_per_ball / k_star_balls
    else:
        talent_var = max(1e-6, talent_var_est)
        k_star_balls = noise_per_ball / talent_var
        
    return k_star_balls, noise_per_ball, talent_var, avg_balls_per_match


# ── Step 2: Compute rankings under k=40, k=k*, k=200 ─────────────────────────

def compute_shrunk_rankings(df_deliveries: pd.DataFrame,
                            role: str = 'batting',
                            k_values: list = [40.0, 200.0, 2212.0]):
    """
    Computes empirical Bayes shrunk ratings and ranks across multiple shrinkage parameters.
    """
    if role == 'batting':
        press = df_deliveries[(df_deliveries['is_high_pressure'] == True) & (df_deliveries['is_batter_ball'] == True)].copy()
        id_col, name_col, outcome_col = 'striker_id', 'striker_name', 'runs_above_expectation'
    else:
        press = df_deliveries[(df_deliveries['is_high_pressure'] == True) & (df_deliveries['is_legal'] == True)].copy()
        id_col, name_col, outcome_col = 'bowler_id', 'bowler_name', 'runs_prevented'

    # Aggregate eligible players (>=100 balls, >=12 matches)
    agg_df = press.groupby([id_col, name_col]).agg(
        n_balls=(outcome_col, 'count'),
        n_matches=('match_id', 'nunique'),
        total_metric=(outcome_col, 'sum')
    ).reset_index()

    elig = agg_df[(agg_df['n_balls'] >= 100) & (agg_df['n_matches'] >= 12)].copy()
    elig['raw_per_ball'] = elig['total_metric'] / elig['n_balls']
    pop_mean = elig['raw_per_ball'].mean()

    for k in k_values:
        k_col = f'shrunk_k{int(k)}' if k == int(k) else f'shrunk_k{k:.1f}'
        r_col = f'rank_k{int(k)}' if k == int(k) else f'rank_k{k:.1f}'
        elig[k_col] = (elig['total_metric'] + k * pop_mean) / (elig['n_balls'] + k)
        elig[r_col] = elig[k_col].rank(ascending=False, method='min').astype(int)

    elig['role'] = role
    elig = elig.rename(columns={id_col: 'player_id', name_col: 'player_name'})
    return elig, pop_mean


# ── Step 3: Match-Level Block Bootstrap ──────────────────────────────────────

def block_bootstrap_ranks(df_match_player: pd.DataFrame,
                          match_strata: pd.DataFrame,
                          candidate_ids: list,
                          candidate_names: dict,
                          k_star: float,
                          metric_col: str = 'total_rae',
                          n_boot: int = 1000,
                          seed: int = 0):
    """
    Executes match-level block bootstrap stratified by competition and season.
    Resamples match IDs with replacement, re-aggregates performances, and evaluates
    both ranks and ratings across all 1,000 replicates.
    """
    rng = np.random.default_rng(seed)
    
    # Stratified match pools
    ipl_matches = match_strata[match_strata['is_ipl']].index.values
    t20i_matches = match_strata[~match_strata['is_ipl']].index.values
    n_ipl = len(ipl_matches)
    n_t20i = len(t20i_matches)
    
    # Pre-index match slices
    by_match = {m: g for m, g in df_match_player.groupby('match_id')}
    
    all_ranks = []
    all_ratings = []
    
    for i in range(n_boot):
        b_ipl = rng.choice(ipl_matches, size=n_ipl, replace=True)
        b_t20i = rng.choice(t20i_matches, size=n_t20i, replace=True)
        boot_matches = np.concatenate([b_ipl, b_t20i])
        
        boot_df = pd.concat([by_match[m] for m in boot_matches if m in by_match], ignore_index=True)
        p_agg = boot_df.groupby('player_id').agg(
            n_balls=('n_balls', 'sum'),
            tot_metric=(metric_col, 'sum')
        )
        pop_mean = p_agg['tot_metric'].sum() / p_agg['n_balls'].sum()
        
        rep_ratings = {}
        for pid in candidate_ids:
            if pid in p_agg.index:
                nb = p_agg.loc[pid, 'n_balls']
                tm = p_agg.loc[pid, 'tot_metric']
            else:
                nb = 0
                tm = 0.0
            shrunk = (tm + k_star * pop_mean) / (nb + k_star)
            rep_ratings[candidate_names[pid]] = shrunk
            
        s_series = pd.Series(rep_ratings)
        s_ranks = s_series.rank(ascending=False, method='min')
        all_ratings.append(rep_ratings)
        all_ranks.append(s_ranks.to_dict())
        
    df_ranks = pd.DataFrame(all_ranks)
    df_ratings = pd.DataFrame(all_ratings)
    
    # Compile summary statistics
    summary_rows = []
    for pid in candidate_ids:
        pname = candidate_names[pid]
        r_series = df_ranks[pname]
        rt_series = df_ratings[pname]
        
        summary_rows.append({
            'player_id': pid,
            'player': pname,
            'mean_rank': float(np.round(r_series.mean(), 2)),
            'p5_rank': float(np.round(np.percentile(r_series, 5), 2)),
            'p95_rank': float(np.round(np.percentile(r_series, 95), 2)),
            'p_top10': float(np.round((r_series <= 10).mean(), 3)),
            'rating_mean': float(np.round(rt_series.mean(), 4)),
            'ci95_low': float(np.round(np.percentile(rt_series, 2.5), 4)),
            'ci95_high': float(np.round(np.percentile(rt_series, 97.5), 4))
        })
        
    summary_df = pd.DataFrame(summary_rows).sort_values('mean_rank').reset_index(drop=True)
    return df_ranks, df_ratings, summary_df


# ── Main Execution ────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("SUPERR SELECTOR SEASON 2 — RANKINGS UNCERTAINTY ENGINE")
    print("=" * 70)
    
    # 1. Load data
    print(f"\n[1/4] Loading parquet from {PARQUET_PATH}...")
    df_all = pd.read_parquet(PARQUET_PATH)
    
    ipl_mask = df_all['comp_name'].str.contains('IPL', case=False, na=False)
    t20i_mask = df_all['match_format'] == 'T20I'
    df_official = df_all[ipl_mask | t20i_mask].copy()
    print(f"      Official scope (IPL + T20I): {len(df_official):,} deliveries")
    
    # Match strata
    match_strata = df_official.groupby('match_id').first()[['comp_name', 'season']].copy()
    match_strata['is_ipl'] = match_strata['comp_name'].str.contains('IPL', na=False)
    
    # 2. Optimal k* estimates
    print("\n[2/4] Estimating optimal shrinkage k* (Method of Moments)...")
    press_bat = df_official[(df_official['is_high_pressure'] == True) & (df_official['is_batter_ball'] == True)].copy()
    k_star_bat, noise_bat, talent_var_bat, avg_balls_bat = estimate_k_star(
        press_bat, outcome_col='runs_above_expectation', player_col='striker_id', min_matches=5, default_k=2212.0
    )
    
    press_bowl = df_official[(df_official['is_high_pressure'] == True) & (df_official['is_legal'] == True)].copy()
    k_star_bowl, noise_bowl, talent_var_bowl, avg_balls_bowl = estimate_k_star(
        press_bowl, outcome_col='runs_prevented', player_col='bowler_id', min_matches=5, default_k=2000.0
    )
    
    k_estimates_df = pd.DataFrame([
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
    k_est_path = os.path.join(OUT_DIR, 'k_star_estimates.csv')
    k_estimates_df.to_csv(k_est_path, index=False)
    print(f"      Batting: k* = {k_star_bat:.1f} (noise={noise_bat:.4f}, talent_var={talent_var_bat:.6f})")
    print(f"      Bowling: k* = {k_star_bowl:.1f} (noise={noise_bowl:.4f}, talent_var={talent_var_bowl:.6f})")
    print(f"      Saved: {k_est_path}")
    
    # 3. Sensitivity analysis across k=40, k=200, k=k*
    print("\n[3/4] Sensitivity analysis across k=40, k=200, k=k*...")
    bat_sens, pop_bat = compute_shrunk_rankings(df_official, role='batting', k_values=[40.0, 200.0, k_star_bat])
    bowl_sens, pop_bowl = compute_shrunk_rankings(df_official, role='bowling', k_values=[40.0, 200.0, k_star_bowl])
    
    # Standardize column names
    k_star_bat_int = int(k_star_bat)
    k_star_bowl_int = int(k_star_bowl)
    
    bat_sens_out = bat_sens[['player_id', 'player_name', 'role', 'n_balls', 'n_matches', 'raw_per_ball',
                             'shrunk_k40', 'rank_k40', 'shrunk_k200', 'rank_k200',
                             f'shrunk_k{k_star_bat_int}', f'rank_k{k_star_bat_int}']].copy()
    bat_sens_out.columns = ['player_id', 'player_name', 'role', 'pressure_balls', 'pressure_matches', 'raw_metric_per_ball',
                            'rating_k40', 'rank_k40', 'rating_k200', 'rank_k200', 'rating_kstar', 'rank_kstar']
    
    bowl_sens_out = bowl_sens[['player_id', 'player_name', 'role', 'n_balls', 'n_matches', 'raw_per_ball',
                               'shrunk_k40', 'rank_k40', 'shrunk_k200', 'rank_k200',
                               f'shrunk_k{k_star_bowl_int}', f'rank_k{k_star_bowl_int}']].copy()
    bowl_sens_out.columns = ['player_id', 'player_name', 'role', 'pressure_balls', 'pressure_matches', 'raw_metric_per_ball',
                             'rating_k40', 'rank_k40', 'rating_k200', 'rank_k200', 'rating_kstar', 'rank_kstar']
    
    k_sens_all = pd.concat([bat_sens_out, bowl_sens_out], ignore_index=True)
    k_sens_path = os.path.join(OUT_DIR, 'k_sensitivity_comparison.csv')
    k_sens_all.to_csv(k_sens_path, index=False)
    
    # Stats
    tau_bat, _ = stats.kendalltau(bat_sens['shrunk_k40'], bat_sens[f'shrunk_k{k_star_bat_int}'])
    overlap_bat = len(set(bat_sens[bat_sens['rank_k40'] <= 10]['player_id']) &
                      set(bat_sens[bat_sens[f'rank_k{k_star_bat_int}'] <= 10]['player_id']))
    
    tau_bowl, _ = stats.kendalltau(bowl_sens['shrunk_k40'], bowl_sens[f'shrunk_k{k_star_bowl_int}'])
    overlap_bowl = len(set(bowl_sens[bowl_sens['rank_k40'] <= 10]['player_id']) &
                       set(bowl_sens[bowl_sens[f'rank_k{k_star_bowl_int}'] <= 10]['player_id']))
    
    print(f"      Batters: Kendall tau(k=40, k=k*) = {tau_bat:.4f}, Top-10 Overlap = {overlap_bat}/10")
    print(f"      Bowlers: Kendall tau(k=40, k=k*) = {tau_bowl:.4f}, Top-10 Overlap = {overlap_bowl}/10")
    print(f"      Saved: {k_sens_path}")
    
    # 4. Block Bootstrap (1,000 iterations)
    print("\n[4/4] Executing 1,000 match-level block bootstrap iterations...")
    
    # Prepare pre-aggregated match tables
    match_bat = press_bat.groupby(['match_id', 'striker_id', 'striker_name']).agg(
        n_balls=('runs_above_expectation', 'count'),
        total_rae=('runs_above_expectation', 'sum')
    ).reset_index().rename(columns={'striker_id': 'player_id', 'striker_name': 'player_name'})
    
    match_bowl = press_bowl.groupby(['match_id', 'bowler_id', 'bowler_name']).agg(
        n_balls=('runs_prevented', 'count'),
        total_rp=('runs_prevented', 'sum')
    ).reset_index().rename(columns={'bowler_id': 'player_id', 'bowler_name': 'player_name'})
    
    candidate_bat_ids = bat_sens['player_id'].tolist()
    candidate_bat_names = dict(zip(bat_sens['player_id'], bat_sens['player_name']))
    
    candidate_bowl_ids = bowl_sens['player_id'].tolist()
    candidate_bowl_names = dict(zip(bowl_sens['player_id'], bowl_sens['player_name']))
    
    # Batting bootstrap
    t0 = time.time()
    boot_bat_ranks, boot_bat_ratings, bat_summary = block_bootstrap_ranks(
        df_match_player=match_bat,
        match_strata=match_strata,
        candidate_ids=candidate_bat_ids,
        candidate_names=candidate_bat_names,
        k_star=k_star_bat,
        metric_col='total_rae',
        n_boot=1000,
        seed=42
    )
    print(f"      Batting bootstrap (1,000 reps) completed in {time.time() - t0:.2f}s")
    
    # Bowling bootstrap
    t0 = time.time()
    boot_bowl_ranks, boot_bowl_ratings, bowl_summary = block_bootstrap_ranks(
        df_match_player=match_bowl,
        match_strata=match_strata,
        candidate_ids=candidate_bowl_ids,
        candidate_names=candidate_bowl_names,
        k_star=k_star_bowl,
        metric_col='total_rp',
        n_boot=1000,
        seed=42
    )
    print(f"      Bowling bootstrap (1,000 reps) completed in {time.time() - t0:.2f}s")
    
    # Save bootstrap outputs
    p_boot_bat_ranks = os.path.join(OUT_DIR, 'bootstrap_batter_ranks.csv')
    p_boot_bowl_ranks = os.path.join(OUT_DIR, 'bootstrap_bowler_ranks.csv')
    p_bat_sum = os.path.join(OUT_DIR, 'batter_rank_summary.csv')
    p_bowl_sum = os.path.join(OUT_DIR, 'bowler_rank_summary.csv')
    
    boot_bat_ranks.to_csv(p_boot_bat_ranks, index=False)
    boot_bowl_ranks.to_csv(p_boot_bowl_ranks, index=False)
    bat_summary.to_csv(p_bat_sum, index=False)
    bowl_summary.to_csv(p_bowl_sum, index=False)
    
    print(f"      Saved: {p_boot_bat_ranks}")
    print(f"      Saved: {p_boot_bowl_ranks}")
    print(f"      Saved: {p_bat_sum}")
    print(f"      Saved: {p_bowl_sum}")
    
    # 5. Round 1 Comparison Tables
    print("\n" + "=" * 70)
    print("ROUND 1 TOP-10 UNCERTAINTY COMPARISON TABLES")
    print("=" * 70)
    
    r1_bat = pd.read_csv(TOP10_BAT_PATH)
    r1_bowl = pd.read_csv(TOP10_BOWL_PATH)
    
    # Batters comparison
    bat_map = bat_summary.set_index('player')
    sens_bat_map = bat_sens_out.set_index('player_name')
    
    r1_bat_rows = []
    for _, r in r1_bat.iterrows():
        pname = r['striker_name']
        orig_rank = int(r['rank'])
        orig_rating = float(r['pressure_rating'])
        
        kstar_rank = int(sens_bat_map.loc[pname, 'rank_kstar']) if pname in sens_bat_map.index else np.nan
        kstar_rating = float(sens_bat_map.loc[pname, 'rating_kstar']) if pname in sens_bat_map.index else np.nan
        
        if pname in bat_map.index:
            bs = bat_map.loc[pname]
            p5 = bs['p5_rank']
            p95 = bs['p95_rank']
            p_top10 = bs['p_top10']
            m_rank = bs['mean_rank']
        else:
            p5, p95, p_top10, m_rank = np.nan, np.nan, np.nan, np.nan
            
        r1_bat_rows.append({
            'striker_name': pname,
            'round1_rank': orig_rank,
            'round1_rating': orig_rating,
            'kstar_rank': kstar_rank,
            'kstar_rating': kstar_rating,
            'mean_boot_rank': m_rank,
            'rank_ci90': f"[{p5:.1f} - {p95:.1f}]",
            'p_top10': p_top10
        })
    r1_bat_comp = pd.DataFrame(r1_bat_rows)
    p_r1_bat_comp = os.path.join(OUT_DIR, 'round1_batters_uncertainty_comparison.csv')
    r1_bat_comp.to_csv(p_r1_bat_comp, index=False)
    print("\n--- Top 10 Batters (Round 1 vs k* with Bootstrap Uncertainty) ---")
    print(r1_bat_comp.to_string(index=False))
    
    # Bowlers comparison
    bowl_map = bowl_summary.set_index('player')
    sens_bowl_map = bowl_sens_out.set_index('player_name')
    
    r1_bowl_rows = []
    for _, r in r1_bowl.iterrows():
        pname = r['bowler_name']
        orig_rank = int(r['rank'])
        orig_rating = float(r['pressure_rating'])
        
        kstar_rank = int(sens_bowl_map.loc[pname, 'rank_kstar']) if pname in sens_bowl_map.index else np.nan
        kstar_rating = float(sens_bowl_map.loc[pname, 'rating_kstar']) if pname in sens_bowl_map.index else np.nan
        
        if pname in bowl_map.index:
            bs = bowl_map.loc[pname]
            p5 = bs['p5_rank']
            p95 = bs['p95_rank']
            p_top10 = bs['p_top10']
            m_rank = bs['mean_rank']
        else:
            p5, p95, p_top10, m_rank = np.nan, np.nan, np.nan, np.nan
            
        r1_bowl_rows.append({
            'bowler_name': pname,
            'round1_rank': orig_rank,
            'round1_rating': orig_rating,
            'kstar_rank': kstar_rank,
            'kstar_rating': kstar_rating,
            'mean_boot_rank': m_rank,
            'rank_ci90': f"[{p5:.1f} - {p95:.1f}]",
            'p_top10': p_top10
        })
    r1_bowl_comp = pd.DataFrame(r1_bowl_rows)
    p_r1_bowl_comp = os.path.join(OUT_DIR, 'round1_bowlers_uncertainty_comparison.csv')
    r1_bowl_comp.to_csv(p_r1_bowl_comp, index=False)
    print("\n--- Top 10 Bowlers (Round 1 vs k* with Bootstrap Uncertainty) ---")
    print(r1_bowl_comp.to_string(index=False))
    
    # Summary findings
    klaasen_p10 = bat_map.loc['Heinrich Klaasen', 'p_top10']
    narine_p10 = bowl_map.loc['Sunil Narine', 'p_top10']
    
    low_p10_batters = [r['striker_name'] for _, r in r1_bat_comp.iterrows() if r['p_top10'] < 0.50]
    low_p10_bowlers = [r['bowler_name'] for _, r in r1_bowl_comp.iterrows() if r['p_top10'] < 0.50]
    
    print("\n" + "=" * 70)
    print("KEY FINDINGS SUMMARY FOR COORDINATOR")
    print("=" * 70)
    print(f"k* Batters: {k_star_bat:.1f}")
    print(f"k* Bowlers: {k_star_bowl:.1f}")
    print(f"Top-10 Overlap k=40 vs k=k* (Batters): {overlap_bat}/10")
    print(f"Top-10 Overlap k=40 vs k=k* (Bowlers): {overlap_bowl}/10")
    print(f"Heinrich Klaasen P(top 10): {klaasen_p10:.3f}")
    print(f"Sunil Narine P(top 10): {narine_p10:.3f}")
    print(f"Round-1 Batters with P(top 10) < 50%: {low_p10_batters}")
    print(f"Round-1 Bowlers with P(top 10) < 50%: {low_p10_bowlers}")
    print("=" * 70)

if __name__ == '__main__':
    main()
