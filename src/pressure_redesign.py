"""
Pressure Redesign Module — SupeRR Selector Season 2
Implements validated continuous pressure scales:
  - Scale A: Situational Urgency (task difficulty, continuous in [0, 1])
  - Scale B: Match Leverage (outcome sensitivity, continuous in [0, 1])
  - Scale Hybrid: 50/50 Urgency + Leverage
  - Existing Hybrid: Round 1 pressure_index_hybrid for baseline comparison
  - CIE Decoupled Urgency & Leverage: from DecoupledPressureEngine

Conducts:
  1. Outcome validation: Spearman rho with batting RAE, dismissal rate, boundary rate,
     bowling runs prevented, Mann-Whitney U / Wilcoxon top vs bottom quartile test.
  2. Dose-response curves: 10 equal-width bins, mean RAE, dismissal rate, boundary rate by innings.
  3. Edge case audit: Super overs (innings >= 3 and tied match results), DLS / shortened matches,
     and impact on Top-10 batter and bowler membership.
  4. Competition-specific baselines: IPL vs T20I distributions, 0.6 threshold comparison,
     and percentile-based threshold equivalents.
"""

import os
import sys
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
from scipy import stats

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(ROOT, 'src'))

PARQUET = os.path.join(ROOT, 'outputs', 'features', 'delivery_features.parquet')
MATCHES_CSV = os.path.join(ROOT, 'matches.csv')
OUT_DIR = os.path.join(ROOT, 'outputs', 'pressure_redesign')
os.makedirs(OUT_DIR, exist_ok=True)

TOP10_BATTERS = os.path.join(ROOT, 'top_10_batters.csv')
TOP10_BOWLERS = os.path.join(ROOT, 'top_10_bowlers.csv')


def main():
    print("=" * 60)
    print("SupeRR Selector Season 2: Pressure Redesign & Calibration")
    print("=" * 60)

    # -----------------------------------------------------------------------
    # Step 1: Load Data & Filter to Official Scope
    # -----------------------------------------------------------------------
    print("\n[Step 1] Loading Parquet and Matches...")
    df = pd.read_parquet(PARQUET)
    matches = pd.read_csv(MATCHES_CSV)
    print(f"  Total deliveries in parquet: {len(df):,}")
    print(f"  Total matches in matches.csv: {len(matches):,}")

    ipl_mask = df['comp_name'].str.contains('IPL', case=False, na=False)
    t20i_mask = df['match_format'] == 'T20I'
    df_official = df[ipl_mask | t20i_mask].copy()
    print(f"  Official scope (IPL + T20I): {len(df_official):,} deliveries")
    print(f"  Official innings distribution: {df_official['innings'].value_counts().sort_index().to_dict()}")

    # -----------------------------------------------------------------------
    # Step 2: Implement Continuous Pressure Scales
    # -----------------------------------------------------------------------
    print("\n[Step 2] Computing Validated Continuous Pressure Scales...")

    # Filter out super overs (innings >= 3) for scale construction and validation
    df_main = df_official[df_official['innings'] < 3].copy()
    print(f"  Main innings deliveries (innings 1 & 2): {len(df_main):,}")

    # Scale A: Situational Urgency (Task Difficulty)
    # Chase (Innings 2):
    # urgency = clip((rrr_pre - 6) / 8, 0, 1) + clip(pre_wickets_lost / 8, 0, 0.5) + clip(1 - pre_legal_balls_remaining / 120, 0, 0.3)
    # Normalize by 1.8 max achievable
    rrr = df_main['rrr_pre'].fillna(0)
    wkts_lost = df_main['pre_wickets_lost'].fillna(0)
    balls_rem = df_main['pre_legal_balls_remaining'].fillna(120)
    balls_done = df_main['pre_legal_balls_completed'].fillna(0)
    is_chase = df_main['innings'] >= 2

    # Innings 2 Urgency
    rrr_comp = np.clip((rrr - 6.0) / 8.0, 0.0, 1.0)
    wkt_comp_chase = np.clip(wkts_lost / 8.0, 0.0, 0.5)
    ball_comp_chase = np.clip(1.0 - balls_rem / 120.0, 0.0, 0.3)
    urgency_inn2 = np.clip((rrr_comp + wkt_comp_chase + ball_comp_chase) / 1.8, 0.0, 1.0)

    # Innings 1 Urgency (Defending / Setting Total):
    # urgency = clip((pre_wickets_lost - 1) / 7, 0, 0.5) * clip(1 - pre_legal_balls_remaining/120, 0, 1)
    #           + clip((pre_legal_balls_completed - 90) / 30, 0, 0.5) [death phase bonus]
    wkt_factor_inn1 = np.clip((wkts_lost - 1.0) / 7.0, 0.0, 0.5)
    time_factor_inn1 = np.clip(1.0 - balls_rem / 120.0, 0.0, 1.0)
    death_bonus_inn1 = np.clip((balls_done - 90.0) / 30.0, 0.0, 0.5)
    urgency_inn1 = np.clip(wkt_factor_inn1 * time_factor_inn1 + death_bonus_inn1, 0.0, 1.0)

    scale_a_urgency = np.where(is_chase, urgency_inn2, urgency_inn1)
    df_main['scale_a_urgency'] = pd.Series(scale_a_urgency, index=df_main.index)

    # Scale B: Match Leverage (Outcome Sensitivity)
    # Derived from pre-computed win-probability leverage index normalized to [0, 1]
    li_raw = df_main['pressure_index_leverage'].fillna(0)
    # pressure_index_leverage is clip(leverage_index / 2.0, 0, 1.5)
    scale_b_leverage = np.clip(li_raw / 1.5, 0.0, 1.0)
    df_main['scale_b_leverage'] = pd.Series(scale_b_leverage, index=df_main.index)

    # Scale C: Hybrid (50% Situational Urgency + 50% Match Leverage)
    scale_hybrid = 0.50 * df_main['scale_a_urgency'] + 0.50 * df_main['scale_b_leverage']
    df_main['scale_hybrid'] = scale_hybrid

    # Existing Round 1 Hybrid for benchmark
    existing_hybrid = df_main['pressure_index_hybrid'].fillna(0)
    df_main['existing_hybrid'] = existing_hybrid

    # Also compute CIE Decoupled Pressure
    try:
        from cie.pressure_decoupled import DecoupledPressureEngine
        print("  Running CIE DecoupledPressureEngine...")
        cie_engine = DecoupledPressureEngine()
        cie_engine.fit_wp_models(df_main)
        df_main['cie_urgency'] = cie_engine.compute_situational_urgency(df_main)
        _, cie_lev = cie_engine.compute_match_leverage_vectorized(df_main)
        # Normalize cie_lev to [0, 1]
        df_main['cie_leverage'] = np.clip(cie_lev / 3.0, 0.0, 1.0)
        has_cie = True
        print("  CIE Decoupled Pressure computed successfully.")
    except Exception as e:
        print(f"  Warning: CIE Decoupled engine skipped ({e})")
        has_cie = False

    print("  Pressure Scales Summary Statistics:")
    print(f"    Scale A (Urgency):  mean={df_main['scale_a_urgency'].mean():.4f}, std={df_main['scale_a_urgency'].std():.4f}")
    print(f"    Scale B (Leverage): mean={df_main['scale_b_leverage'].mean():.4f}, std={df_main['scale_b_leverage'].std():.4f}")
    print(f"    Scale Hybrid:       mean={df_main['scale_hybrid'].mean():.4f}, std={df_main['scale_hybrid'].std():.4f}")
    print(f"    Existing Hybrid:    mean={df_main['existing_hybrid'].mean():.4f}, std={df_main['existing_hybrid'].std():.4f}")

    # -----------------------------------------------------------------------
    # Step 3: Validate Scales Against Outcomes
    # -----------------------------------------------------------------------
    print("\n[Step 3] Validating Pressure Scales Against Outcomes...")

    # Filter to batter deliveries with valid out-of-fold RAE
    batters_df = df_main[df_main['is_batter_ball'].astype(bool)].dropna(subset=['runs_above_expectation']).copy()
    bowl_df = df_main.dropna(subset=['runs_prevented']).copy()

    scale_cols = ['scale_a_urgency', 'scale_b_leverage', 'scale_hybrid', 'existing_hybrid']
    scale_names = ['Scale_A_Urgency', 'Scale_B_Leverage', 'Scale_Hybrid', 'Existing_Hybrid']
    if has_cie:
        scale_cols.extend(['cie_urgency', 'cie_leverage'])
        scale_names.extend(['CIE_Urgency', 'CIE_Leverage'])

    validation_rows = []
    for col, name in zip(scale_cols, scale_names):
        sub_bat = batters_df.dropna(subset=[col])
        sub_bowl = bowl_df.dropna(subset=[col])

        # Batting outcome correlations
        rho_rae, p_rae = stats.spearmanr(sub_bat[col], sub_bat['runs_above_expectation'])
        rho_wkt, p_wkt = stats.spearmanr(sub_bat[col], sub_bat['is_wicket'].astype(float))
        is_bnd = (sub_bat['is_four'] | sub_bat['is_six']).astype(float)
        rho_bnd, p_bnd = stats.spearmanr(sub_bat[col], is_bnd)

        # Bowling outcome correlation (runs prevented = exp_bowler_runs - bowler_conceded_runs)
        rho_bowl_rp, p_bowl_rp = stats.spearmanr(sub_bowl[col], sub_bowl['runs_prevented'])
        # Economy vs expected = conceded - expected = -runs_prevented
        rho_econ_diff = -rho_bowl_rp

        # Mann-Whitney U test (Wilcoxon rank-sum): top quartile vs bottom quartile batting RAE
        q25 = sub_bat[col].quantile(0.25)
        q75 = sub_bat[col].quantile(0.75)
        high_press_rae = sub_bat.loc[sub_bat[col] >= q75, 'runs_above_expectation']
        low_press_rae = sub_bat.loc[sub_bat[col] <= q25, 'runs_above_expectation']
        mwu_stat, mwu_p = stats.mannwhitneyu(high_press_rae, low_press_rae, alternative='two-sided')

        validation_rows.append({
            'scale': name,
            'spearman_batting_rae': round(rho_rae, 4),
            'p_batting_rae': round(p_rae, 6),
            'spearman_dismissal_rate': round(rho_wkt, 4),
            'p_dismissal_rate': round(p_wkt, 6),
            'spearman_boundary_rate': round(rho_bnd, 4),
            'p_boundary_rate': round(p_bnd, 6),
            'spearman_bowling_runs_prevented': round(rho_bowl_rp, 4),
            'spearman_bowling_economy_vs_expected': round(rho_econ_diff, 4),
            'p_bowling': round(p_bowl_rp, 6),
            'wilcoxon_mwu_stat': round(mwu_stat, 1),
            'wilcoxon_mwu_p': round(mwu_p, 6),
            'mean_rae_low_quartile': round(low_press_rae.mean(), 4),
            'mean_rae_high_quartile': round(high_press_rae.mean(), 4),
            'rae_quartile_diff': round(high_press_rae.mean() - low_press_rae.mean(), 4),
            'n_batting_deliveries': len(sub_bat),
        })

    val_df = pd.DataFrame(validation_rows)
    val_df.to_csv(os.path.join(OUT_DIR, 'scale_validation.csv'), index=False)
    print("  Saved: outputs/pressure_redesign/scale_validation.csv")
    print(val_df[['scale', 'spearman_batting_rae', 'spearman_dismissal_rate', 'spearman_bowling_runs_prevented', 'wilcoxon_mwu_p']].to_string(index=False))

    # Identify best predicting scale by absolute correlation with batting RAE
    best_scale_row = val_df.loc[val_df['spearman_batting_rae'].abs().idxmax()]
    best_scale_name = best_scale_row['scale']
    best_scale_rho = best_scale_row['spearman_batting_rae']
    print(f"\n  >>> Best predicting scale for outcome difference: {best_scale_name} (|rho_RAE| = {abs(best_scale_rho):.4f})")

    # -----------------------------------------------------------------------
    # Step 4: Dose-Response Curves by Scale
    # -----------------------------------------------------------------------
    print("\n[Step 4] Computing Dose-Response Curves (10 Equal-Width Bins)...")

    dose_rows = []
    monotonicity_results = []

    for col, name in zip(scale_cols, scale_names):
        sub_bat = batters_df.dropna(subset=[col]).copy()
        sub_bat['bin'] = pd.cut(sub_bat[col], bins=np.linspace(0.0, 1.0, 11), labels=False, include_lowest=True)

        for inn_lbl, inn_cond in [('All', slice(None)), ('Innings_1', sub_bat['innings'] == 1), ('Innings_2', sub_bat['innings'] == 2)]:
            if inn_lbl == 'All':
                data_subset = sub_bat
            else:
                data_subset = sub_bat[inn_cond]

            if len(data_subset) == 0:
                continue

            grp = data_subset.groupby('bin').agg(
                mean_rae=('runs_above_expectation', 'mean'),
                dismissal_rate=('is_wicket', 'mean'),
                n_deliveries=('runs_above_expectation', 'count')
            ).reset_index()

            # Boundary rate
            grp['boundary_rate'] = data_subset.groupby('bin').apply(
                lambda x: (x['is_four'] | x['is_six']).mean()
            ).values

            # Monotonicity test: Spearman rho across the 10 bins
            if len(grp) >= 3:
                mono_rho, mono_p = stats.spearmanr(grp['bin'], grp['mean_rae'])
                monotonicity_results.append({
                    'scale': name,
                    'innings': inn_lbl,
                    'monotonicity_rho': round(mono_rho, 4),
                    'monotonicity_p': round(mono_p, 4)
                })

            for _, r in grp.iterrows():
                b = int(r['bin']) if not pd.isna(r['bin']) else -1
                dose_rows.append({
                    'scale': name,
                    'innings_subset': inn_lbl,
                    'bin': b,
                    'bin_range': f"[{b*0.1:.1f}, {(b+1)*0.1:.1f}]",
                    'mean_rae': round(r['mean_rae'], 4),
                    'dismissal_rate': round(r['dismissal_rate'], 4),
                    'boundary_rate': round(r['boundary_rate'], 4),
                    'n_deliveries': int(r['n_deliveries'])
                })

    dose_df = pd.DataFrame(dose_rows)
    dose_df.to_csv(os.path.join(OUT_DIR, 'dose_response_by_scale.csv'), index=False)
    print("  Saved: outputs/pressure_redesign/dose_response_by_scale.csv")

    mono_df = pd.DataFrame(monotonicity_results)
    print("  Dose-Response Monotonicity (Spearman rho across 10 decile bins):")
    print(mono_df.to_string(index=False))

    # -----------------------------------------------------------------------
    # Step 5: Super Overs & Edge Cases Audit
    # -----------------------------------------------------------------------
    print("\n[Step 5] Edge Case Audit (Super Overs & DLS Shortened Matches)...")

    # A. Super Overs
    # In delivery data
    so_delivs_official = df_official[df_official['innings'] >= 3]
    n_so_delivs = len(so_delivs_official)
    n_so_matches_delivs = so_delivs_official['match_id'].nunique()

    # In all matches data (entire dataset)
    so_delivs_all = df[df['innings'] >= 3]
    n_so_matches_delivs_all = so_delivs_all['match_id'].nunique()

    # In matches.csv (result text indicating tie / super over)
    tied_matches = matches[matches['result'].str.contains('tied|tie |tie$|one-over|super over', case=False, na=False)]
    n_tied_matches_all = len(tied_matches)
    tied_matches_official = tied_matches[tied_matches['match_id'].isin(df_official['match_id'].unique())]
    n_tied_matches_official = len(tied_matches_official)

    print(f"  Super overs in delivery features: {n_so_delivs} deliveries across {n_so_matches_delivs} official matches ({n_so_matches_delivs_all} overall matches)")
    print(f"  Super overs/ties in match records: {n_tied_matches_official} official matches ({n_tied_matches_all} overall matches)")

    # B. DLS Shortened Matches
    # Identify matches with DLS/method in result or revised overs/targets
    dls_matches_all = matches[
        matches['result'].str.contains('DLS|method', case=False, na=False) |
        matches['revised_target'].notna() |
        matches['first_inn_revised_overs'].notna() |
        matches['second_inn_revised_overs'].notna()
    ]
    dls_match_ids_all = set(dls_matches_all['match_id'].unique())
    dls_delivs_official = df_official[df_official['match_id'].isin(dls_match_ids_all)]
    n_dls_delivs = len(dls_delivs_official)
    n_dls_matches = dls_delivs_official['match_id'].nunique()

    # Also report explicit result containing "(DLS method)"
    dls_explicit = matches[matches['result'].str.contains('DLS|method', case=False, na=False)]
    dls_explicit_official = dls_explicit[dls_explicit['match_id'].isin(df_official['match_id'].unique())]
    n_dls_explicit_matches = len(dls_explicit_official)
    n_dls_explicit_delivs = len(df_official[df_official['match_id'].isin(dls_explicit_official['match_id'])])

    print(f"  DLS / shortened matches: {n_dls_matches} matches ({n_dls_delivs:,} deliveries in official scope)")
    print(f"  Explicit DLS method results: {n_dls_explicit_matches} matches ({n_dls_explicit_delivs:,} deliveries)")

    # C. Top-10 Membership Sensitivity (With vs Without DLS)
    # Frozen Round 1 rosters
    r1_batters = pd.read_csv(TOP10_BATTERS)['striker_name'].tolist()
    r1_bowlers = pd.read_csv(TOP10_BOWLERS)['bowler_name'].tolist()

    # Function to rank batters under shrunk RAE (k=40)
    def rank_batters_subset(sub_df, k=40):
        hp = sub_df[sub_df['is_high_pressure'] & sub_df['is_batter_ball'].astype(bool)].copy()
        grp = hp.groupby(['striker_id', 'striker_name']).agg(
            balls=('is_batter_ball', 'sum'),
            matches=('match_id', 'nunique'),
            total_rae=('runs_above_expectation', 'sum')
        ).reset_index()
        eligible = grp[(grp['balls'] >= 100) & (grp['matches'] >= 12)].copy()
        global_mean = hp['runs_above_expectation'].mean()
        eligible['shrunk_rae'] = (eligible['total_rae'] + k * global_mean) / (eligible['balls'] + k)
        return eligible.sort_values('shrunk_rae', ascending=False)['striker_name'].head(10).tolist()

    # Function to rank bowlers under shrunk RP (k=40)
    def rank_bowlers_subset(sub_df, k=40):
        hp = sub_df[sub_df['is_high_pressure']].copy()
        grp = hp.groupby(['bowler_id', 'bowler_name']).agg(
            balls=('is_legal', 'sum'),
            matches=('match_id', 'nunique'),
            runs_prevented=('runs_prevented', 'sum')
        ).reset_index()
        eligible = grp[(grp['balls'] >= 100) & (grp['matches'] >= 12)].copy()
        global_mean = hp['runs_prevented'].mean()
        eligible['shrunk_rp'] = (eligible['runs_prevented'] + k * global_mean) / (eligible['balls'] + k)
        return eligible.sort_values('shrunk_rp', ascending=False)['bowler_name'].head(10).tolist()

    # Evaluate membership
    top10_b_full = rank_batters_subset(df_main)
    top10_b_nodls = rank_batters_subset(df_main[~df_main['match_id'].isin(dls_match_ids_all)])
    b_overlap = len(set(top10_b_full) & set(top10_b_nodls))
    b_changed = (b_overlap < 10)
    b_dropped = list(set(top10_b_full) - set(top10_b_nodls))
    b_added = list(set(top10_b_nodls) - set(top10_b_full))

    top10_bw_full = rank_bowlers_subset(df_main)
    top10_bw_nodls = rank_bowlers_subset(df_main[~df_main['match_id'].isin(dls_match_ids_all)])
    bw_overlap = len(set(top10_bw_full) & set(top10_bw_nodls))
    bw_changed = (bw_overlap < 10)

    print(f"  Top-10 Batter Overlap (Full vs Excl DLS): {b_overlap}/10 (Changed: {b_changed})")
    if b_changed:
        print(f"    Batter Out: {b_dropped}, Batter In: {b_added}")
    print(f"  Top-10 Bowler Overlap (Full vs Excl DLS): {bw_overlap}/10 (Changed: {bw_changed})")

    edge_audit_records = [
        {'category': 'Super_Overs', 'metric': 'super_over_deliveries_official', 'value': n_so_delivs},
        {'category': 'Super_Overs', 'metric': 'super_over_matches_with_deliveries_official', 'value': n_so_matches_delivs},
        {'category': 'Super_Overs', 'metric': 'super_over_matches_with_deliveries_all', 'value': n_so_matches_delivs_all},
        {'category': 'Super_Overs', 'metric': 'tied_super_over_matches_official', 'value': n_tied_matches_official},
        {'category': 'Super_Overs', 'metric': 'tied_super_over_matches_all', 'value': n_tied_matches_all},
        {'category': 'DLS_Shortened', 'metric': 'dls_shortened_matches_official', 'value': n_dls_matches},
        {'category': 'DLS_Shortened', 'metric': 'dls_shortened_deliveries_official', 'value': n_dls_delivs},
        {'category': 'DLS_Shortened', 'metric': 'dls_explicit_result_matches', 'value': n_dls_explicit_matches},
        {'category': 'DLS_Shortened', 'metric': 'dls_explicit_result_deliveries', 'value': n_dls_explicit_delivs},
        {'category': 'Ranking_Impact', 'metric': 'top10_batters_overlap_excl_dls', 'value': b_overlap},
        {'category': 'Ranking_Impact', 'metric': 'top10_batters_membership_changed_by_dls', 'value': int(b_changed)},
        {'category': 'Ranking_Impact', 'metric': 'top10_bowlers_overlap_excl_dls', 'value': bw_overlap},
        {'category': 'Ranking_Impact', 'metric': 'top10_bowlers_membership_changed_by_dls', 'value': int(bw_changed)},
    ]
    edge_audit_df = pd.DataFrame(edge_audit_records)
    edge_audit_df.to_csv(os.path.join(OUT_DIR, 'edge_case_audit.csv'), index=False)
    print("  Saved: outputs/pressure_redesign/edge_case_audit.csv")

    # -----------------------------------------------------------------------
    # Step 6: Competition-Specific Pressure Baselines
    # -----------------------------------------------------------------------
    print("\n[Step 6] Analyzing Competition-Specific Pressure Baselines (IPL vs T20I)...")

    df_main['comp_type'] = np.where(
        df_main['comp_name'].str.contains('IPL', case=False, na=False), 'IPL', 'T20I'
    )

    comp_records = []
    for col, name in zip(scale_cols, scale_names):
        for comp in ['IPL', 'T20I']:
            vals = df_main.loc[df_main['comp_type'] == comp, col].dropna()
            if len(vals) == 0:
                continue

            pct_gt_06 = (vals >= 0.60).mean() * 100
            comp_records.append({
                'scale': name,
                'competition': comp,
                'mean': round(vals.mean(), 4),
                'std': round(vals.std(), 4),
                'median': round(vals.median(), 4),
                'p25': round(vals.quantile(0.25), 4),
                'p75': round(vals.quantile(0.75), 4),
                'p80': round(vals.quantile(0.80), 4),
                'p85': round(vals.quantile(0.85), 4),
                'p90': round(vals.quantile(0.90), 4),
                'pct_balls_above_0.60': round(pct_gt_06, 2),
                'equiv_percentile_of_0.60': round((vals < 0.60).mean() * 100, 2),
                'n_deliveries': len(vals)
            })

    comp_df = pd.DataFrame(comp_records)
    comp_df.to_csv(os.path.join(OUT_DIR, 'competition_pressure_distribution.csv'), index=False)
    print("  Saved: outputs/pressure_redesign/competition_pressure_distribution.csv")

    print("\n  Competition Differential Summary:")
    for name in scale_names:
        sub = comp_df[comp_df['scale'] == name]
        if len(sub) == 2:
            m_ipl = sub.loc[sub['competition'] == 'IPL', 'mean'].values[0]
            m_t20i = sub.loc[sub['competition'] == 'T20I', 'mean'].values[0]
            pct_ipl = sub.loc[sub['competition'] == 'IPL', 'pct_balls_above_0.60'].values[0]
            pct_t20i = sub.loc[sub['competition'] == 'T20I', 'pct_balls_above_0.60'].values[0]
            p85_ipl = sub.loc[sub['competition'] == 'IPL', 'p85'].values[0]
            p85_t20i = sub.loc[sub['competition'] == 'T20I', 'p85'].values[0]
            print(f"    {name:<18}: IPL Mean={m_ipl:.4f} (diff={m_ipl - m_t20i:+.4f}), %>=0.6: IPL={pct_ipl:.1f}% vs T20I={pct_t20i:.1f}%, 85th Pct: IPL={p85_ipl:.3f} vs T20I={p85_t20i:.3f}")

    # -----------------------------------------------------------------------
    # Step 7: Comprehensive Summary
    # -----------------------------------------------------------------------
    # Monotonicity for Scale A (Urgency) and Existing Hybrid
    mono_scale_a = mono_df.loc[(mono_df['scale'] == 'Scale_A_Urgency') & (mono_df['innings'] == 'All'), 'monotonicity_rho'].values[0]
    mono_scale_a_p = mono_df.loc[(mono_df['scale'] == 'Scale_A_Urgency') & (mono_df['innings'] == 'All'), 'monotonicity_p'].values[0]
    mono_existing = mono_df.loc[(mono_df['scale'] == 'Existing_Hybrid') & (mono_df['innings'] == 'All'), 'monotonicity_rho'].values[0]

    # Differential in Scale Hybrid
    ipl_hybrid_mean = comp_df.loc[(comp_df['scale'] == 'Scale_Hybrid') & (comp_df['competition'] == 'IPL'), 'mean'].values[0]
    t20i_hybrid_mean = comp_df.loc[(comp_df['scale'] == 'Scale_Hybrid') & (comp_df['competition'] == 'T20I'), 'mean'].values[0]
    comp_diff = ipl_hybrid_mean - t20i_hybrid_mean

    summary_records = [
        {'metric': 'best_predicting_scale_name', 'value': best_scale_name},
        {'metric': 'best_predicting_scale_spearman_rae', 'value': round(best_scale_rho, 4)},
        {'metric': 'scale_a_urgency_spearman_rae', 'value': val_df.loc[val_df['scale'] == 'Scale_A_Urgency', 'spearman_batting_rae'].values[0]},
        {'metric': 'scale_b_leverage_spearman_rae', 'value': val_df.loc[val_df['scale'] == 'Scale_B_Leverage', 'spearman_batting_rae'].values[0]},
        {'metric': 'scale_hybrid_spearman_rae', 'value': val_df.loc[val_df['scale'] == 'Scale_Hybrid', 'spearman_batting_rae'].values[0]},
        {'metric': 'existing_hybrid_spearman_rae', 'value': val_df.loc[val_df['scale'] == 'Existing_Hybrid', 'spearman_batting_rae'].values[0]},
        {'metric': 'scale_a_urgency_dose_monotonicity_rho', 'value': round(mono_scale_a, 4)},
        {'metric': 'scale_a_urgency_dose_monotonicity_p', 'value': round(mono_scale_a_p, 4)},
        {'metric': 'existing_hybrid_dose_monotonicity_rho', 'value': round(mono_existing, 4)},
        {'metric': 'super_over_deliveries_official', 'value': n_so_delivs},
        {'metric': 'super_over_matches_with_deliveries_all', 'value': n_so_matches_delivs_all},
        {'metric': 'tied_super_over_matches_official', 'value': n_tied_matches_official},
        {'metric': 'tied_super_over_matches_all', 'value': n_tied_matches_all},
        {'metric': 'dls_shortened_matches_official', 'value': n_dls_matches},
        {'metric': 'dls_shortened_deliveries_official', 'value': n_dls_delivs},
        {'metric': 'ipl_vs_t20i_scale_hybrid_mean_diff', 'value': round(comp_diff, 4)},
        {'metric': 'ipl_pct_balls_above_0.6_scale_hybrid', 'value': comp_df.loc[(comp_df['scale'] == 'Scale_Hybrid') & (comp_df['competition'] == 'IPL'), 'pct_balls_above_0.60'].values[0]},
        {'metric': 't20i_pct_balls_above_0.6_scale_hybrid', 'value': comp_df.loc[(comp_df['scale'] == 'Scale_Hybrid') & (comp_df['competition'] == 'T20I'), 'pct_balls_above_0.60'].values[0]},
        {'metric': 'top10_batters_membership_changed_by_dls', 'value': int(b_changed)},
        {'metric': 'top10_bowlers_membership_changed_by_dls', 'value': int(bw_changed)},
    ]
    summary_df = pd.DataFrame(summary_records)
    summary_df.to_csv(os.path.join(OUT_DIR, 'pressure_redesign_summary.csv'), index=False)
    print("  Saved: outputs/pressure_redesign/pressure_redesign_summary.csv")

    print("\n" + "=" * 60)
    print("PRESSURE REDESIGN COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == '__main__':
    main()
