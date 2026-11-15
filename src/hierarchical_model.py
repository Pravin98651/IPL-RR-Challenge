"""
SupeRR Selector Season 2 — Hierarchical Model Module
Answers: "Is player-specific clutch response statistically real and persistent?"

Steps:
1. Frequentist Mixed Model Prototype (statsmodels MixedLM) — M0, M1, M2
2. Empirical Bayes Hierarchical Model (closed-form Lindley-Smith EB)
3. Permutation test for clutch heterogeneity (500 permutations)
4. Rank by PressureLevel vs Clutch (dual rankings, Kendall tau)
5. Walk-forward validation of rankings (train 2022-2024, test 2025+2026)

Outputs saved to outputs/hierarchical/
"""

import os
import sys
import warnings
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import kendalltau

warnings.filterwarnings('ignore')

# ─── Setup ───────────────────────────────────────────────────────────────────

WORK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(WORK_DIR)
sys.path.insert(0, os.path.join(WORK_DIR, 'src'))

OUT_DIR = os.path.join(WORK_DIR, 'outputs', 'hierarchical')
os.makedirs(OUT_DIR, exist_ok=True)

TRAIN_SEASONS = {'2022', '2022/23', '2023', '2023/24', '2024', '2024/25'}
TEST_SEASONS  = {'2025', '2026'}


# ─── Data Loading ─────────────────────────────────────────────────────────────

def load_data():
    print("Loading delivery features parquet...")
    df = pd.read_parquet('outputs/features/delivery_features.parquet')
    ipl_mask  = df['comp_name'].str.contains('IPL', case=False, na=False)
    t20i_mask = df['match_format'] == 'T20I'
    dfo = df[ipl_mask | t20i_mask].copy()
    print(f"  Official scope (IPL + T20I): {len(dfo):,} rows")
    return dfo


# ─── Step 1: Frequentist Mixed Model (MixedLM) ───────────────────────────────

def step1_mixed_models(df_official: pd.DataFrame) -> pd.DataFrame:
    """
    Fit M0, M1, M2 on batter pressure deliveries.
    Returns model_comparison DataFrame.
    """
    print("\n=== STEP 1: Frequentist Mixed Models ===")
    try:
        import statsmodels.api as sm
        from statsmodels.regression.mixed_linear_model import MixedLM
    except ImportError:
        print("  statsmodels not available; skipping frequentist step.")
        return pd.DataFrame()

    # Filter: batter balls in high-pressure situations
    bat_press = df_official[
        (df_official['is_batter_ball'] == True) &
        (df_official['is_high_pressure'] == True)
    ].copy()
    bat_press = bat_press.dropna(subset=['runs_above_expectation', 'pressure_index_hybrid', 'striker_id'])
    print(f"  Batter pressure deliveries: {len(bat_press):,} rows, "
          f"{bat_press['striker_id'].nunique()} players")

    # Train/test split by season
    train_mask = bat_press['season'].isin(TRAIN_SEASONS)
    test_mask  = bat_press['season'].isin(TEST_SEASONS)
    train_df   = bat_press[train_mask].copy()
    test_df    = bat_press[test_mask].copy()
    print(f"  Train: {len(train_df):,}  Test: {len(test_df):,}")

    y_col = 'runs_above_expectation'
    results = []

    # ── M0: Grand mean only ──────────────────────────────────────────────────
    print("  Fitting M0 (grand mean)...")
    grand_mean = float(train_df[y_col].mean())
    grand_var  = float(train_df[y_col].var())
    n_train    = len(train_df)
    # Log-likelihood of normal with estimated mu, sigma
    sigma_m0   = float(train_df[y_col].std())
    loglik_m0  = float(np.sum(stats.norm.logpdf(train_df[y_col].values, loc=grand_mean, scale=max(sigma_m0, 1e-6))))
    k_m0       = 2  # mu, sigma
    aic_m0     = -2 * loglik_m0 + 2 * k_m0
    bic_m0     = -2 * loglik_m0 + k_m0 * np.log(n_train)
    # Held-out log-loss
    test_logloss_m0 = -float(np.mean(stats.norm.logpdf(test_df[y_col].values, loc=grand_mean, scale=max(sigma_m0, 1e-6))))
    results.append({'model': 'M0', 'description': 'Grand mean only',
                    'AIC': aic_m0, 'BIC': bic_m0, 'loglik': loglik_m0,
                    'held_out_logloss': test_logloss_m0, 'converged': True})
    print(f"    M0  loglik={loglik_m0:.2f}  AIC={aic_m0:.2f}  BIC={bic_m0:.2f}  test_logloss={test_logloss_m0:.4f}")

    # ── M1: Random intercepts ─────────────────────────────────────────────────
    print("  Fitting M1 (random intercepts)...")
    m1_converged = False
    try:
        # Subset to players with enough obs in training
        player_counts_train = train_df.groupby('striker_id').size()
        valid_players_m1 = player_counts_train[player_counts_train >= 5].index
        train_m1 = train_df[train_df['striker_id'].isin(valid_players_m1)].copy()

        m1 = MixedLM.from_formula(
            f'{y_col} ~ 1',
            data=train_m1,
            groups='striker_id'
        )
        m1_fit = m1.fit(method='lbfgs', maxiter=200)
        loglik_m1 = float(m1_fit.llf)
        aic_m1    = float(m1_fit.aic)
        bic_m1    = float(m1_fit.bic)
        m1_converged = True

        # Held-out log-loss using player random effects
        # For test: use grand mean + player RE if available
        player_re_m1 = m1_fit.random_effects  # dict: player_id -> DataFrame
        sigma_resid_m1 = float(np.sqrt(m1_fit.scale))
        pred_means_test = []
        for _, row in test_df.iterrows():
            pid = row['striker_id']
            if pid in player_re_m1:
                re_val = float(player_re_m1[pid].iloc[0])
            else:
                re_val = 0.0
            pred_means_test.append(float(m1_fit.fe_params['Intercept']) + re_val)
        pred_means_test = np.array(pred_means_test)
        test_logloss_m1 = -float(np.mean(stats.norm.logpdf(
            test_df[y_col].values, loc=pred_means_test, scale=max(sigma_resid_m1, 1e-6))))

        results.append({'model': 'M1', 'description': 'Random intercepts only',
                        'AIC': aic_m1, 'BIC': bic_m1, 'loglik': loglik_m1,
                        'held_out_logloss': test_logloss_m1, 'converged': True})
        print(f"    M1  loglik={loglik_m1:.2f}  AIC={aic_m1:.2f}  BIC={bic_m1:.2f}  test_logloss={test_logloss_m1:.4f}")
    except Exception as e:
        print(f"    M1 failed: {e}")
        results.append({'model': 'M1', 'description': 'Random intercepts only',
                        'AIC': np.nan, 'BIC': np.nan, 'loglik': np.nan,
                        'held_out_logloss': np.nan, 'converged': False})

    # ── M2: Random slopes (approximation via player-specific OLS + EB pooling) ─
    print("  Fitting M2 (random slopes — OLS approximation + EB pooling)...")
    m2_method = "OLS+EB"
    try:
        # Try full MixedLM with random slopes first
        player_counts_train = train_df.groupby('striker_id').size()
        valid_players_m2 = player_counts_train[player_counts_train >= 20].index
        train_m2 = train_df[train_df['striker_id'].isin(valid_players_m2)].copy()

        exog_re = sm.add_constant(train_m2[['pressure_index_hybrid']])
        m2 = MixedLM(
            endog=train_m2[y_col].values,
            exog=sm.add_constant(train_m2[['pressure_index_hybrid']]).values,
            groups=train_m2['striker_id'].values,
            exog_re=exog_re.values
        )
        m2_fit = m2.fit(method='lbfgs', maxiter=300)
        loglik_m2 = float(m2_fit.llf)
        aic_m2    = float(m2_fit.aic)
        bic_m2    = float(m2_fit.bic)
        m2_method = "MixedLM"

        # Held-out log-loss
        sigma_resid_m2 = float(np.sqrt(m2_fit.scale))
        player_re_m2 = m2_fit.random_effects
        fe_params = m2_fit.fe_params
        pred_means_test_m2 = []
        for _, row in test_df.iterrows():
            pid = row['striker_id']
            pi  = float(row['pressure_index_hybrid'])
            if pid in player_re_m2:
                re = player_re_m2[pid]
                re_intercept = float(re.iloc[0]) if len(re) > 0 else 0.0
                re_slope     = float(re.iloc[1]) if len(re) > 1 else 0.0
            else:
                re_intercept = 0.0
                re_slope     = 0.0
            pred = float(fe_params['Intercept']) + float(fe_params.get('pressure_index_hybrid', 0)) * pi + re_intercept + re_slope * pi
            pred_means_test_m2.append(pred)
        pred_means_test_m2 = np.array(pred_means_test_m2)
        test_logloss_m2 = -float(np.mean(stats.norm.logpdf(
            test_df[y_col].values, loc=pred_means_test_m2, scale=max(sigma_resid_m2, 1e-6))))

        results.append({'model': 'M2', 'description': 'Random slopes (MixedLM)',
                        'AIC': aic_m2, 'BIC': bic_m2, 'loglik': loglik_m2,
                        'held_out_logloss': test_logloss_m2, 'converged': True})
        print(f"    M2  loglik={loglik_m2:.2f}  AIC={aic_m2:.2f}  BIC={bic_m2:.2f}  test_logloss={test_logloss_m2:.4f}  [MixedLM]")

    except Exception as e:
        print(f"    M2 MixedLM failed ({e}); falling back to player-OLS + EB approximation")
        m2_method = "OLS+EB"
        try:
            # Fallback: per-player OLS with >=30 obs, then pool via EB
            player_counts_train = train_df.groupby('striker_id').size()
            valid_players_m2 = player_counts_train[player_counts_train >= 30].index
            train_m2 = train_df[train_df['striker_id'].isin(valid_players_m2)].copy()

            player_slopes = {}
            player_intercepts = {}
            player_sigma2s = {}
            for pid, grp in train_m2.groupby('striker_id'):
                x = grp['pressure_index_hybrid'].values
                y = grp[y_col].values
                X_p = np.column_stack([np.ones(len(x)), x])
                try:
                    b, res, _, _ = np.linalg.lstsq(X_p, y, rcond=None)
                    yhat = X_p @ b
                    s2 = float(np.var(y - yhat, ddof=2)) if len(y) > 2 else 1.0
                    player_slopes[pid]      = float(b[1])
                    player_intercepts[pid]  = float(b[0])
                    player_sigma2s[pid]     = max(s2, 1e-6)
                except Exception:
                    pass

            slopes_arr = np.array(list(player_slopes.values()))
            intercepts_arr = np.array(list(player_intercepts.values()))
            # Grand mean slope
            mu_slope_grand = float(np.mean(slopes_arr))
            mu_int_grand   = float(np.mean(intercepts_arr))
            sigma2_between_slopes = max(float(np.var(slopes_arr, ddof=1)), 1e-6)
            sigma2_between_int    = max(float(np.var(intercepts_arr, ddof=1)), 1e-6)

            # Empirical Bayes shrinkage of slopes
            eb_slopes     = {}
            eb_intercepts = {}
            for pid in player_slopes:
                n_i   = len(train_m2[train_m2['striker_id'] == pid])
                s2_i  = player_sigma2s[pid]
                # Shrinkage weight: B = s2_between / (s2_between + s2_within/n_i)
                B_slope = sigma2_between_slopes / (sigma2_between_slopes + s2_i / n_i)
                B_int   = sigma2_between_int   / (sigma2_between_int   + s2_i / n_i)
                eb_slopes[pid]     = mu_slope_grand + B_slope * (player_slopes[pid]     - mu_slope_grand)
                eb_intercepts[pid] = mu_int_grand   + B_int   * (player_intercepts[pid] - mu_int_grand)

            # Approximate log-likelihood on training set
            pred_train_m2 = []
            resid_sq = []
            for _, row in train_m2.iterrows():
                pid = row['striker_id']
                pi  = float(row['pressure_index_hybrid'])
                pred = eb_intercepts.get(pid, mu_int_grand) + eb_slopes.get(pid, mu_slope_grand) * pi
                pred_train_m2.append(pred)
                resid_sq.append((float(row[y_col]) - pred) ** 2)
            sigma_resid_m2 = max(float(np.sqrt(np.mean(resid_sq))), 1e-6)
            loglik_m2 = float(np.sum(stats.norm.logpdf(
                train_m2[y_col].values,
                loc=np.array(pred_train_m2),
                scale=sigma_resid_m2
            )))
            k_m2  = 2 + 2 * len(valid_players_m2)  # rough param count
            n_m2  = len(train_m2)
            aic_m2 = -2 * loglik_m2 + 2 * k_m2
            bic_m2 = -2 * loglik_m2 + k_m2 * np.log(n_m2)

            # Held-out log-loss
            pred_test_m2 = []
            for _, row in test_df.iterrows():
                pid = row['striker_id']
                pi  = float(row['pressure_index_hybrid'])
                pred = eb_intercepts.get(pid, mu_int_grand) + eb_slopes.get(pid, mu_slope_grand) * pi
                pred_test_m2.append(pred)
            test_logloss_m2 = -float(np.mean(stats.norm.logpdf(
                test_df[y_col].values, loc=np.array(pred_test_m2), scale=sigma_resid_m2)))

            results.append({'model': 'M2', 'description': 'Random slopes (OLS+EB approx)',
                            'AIC': aic_m2, 'BIC': bic_m2, 'loglik': loglik_m2,
                            'held_out_logloss': test_logloss_m2, 'converged': True})
            print(f"    M2  loglik={loglik_m2:.2f}  AIC={aic_m2:.2f}  BIC={bic_m2:.2f}  test_logloss={test_logloss_m2:.4f}  [OLS+EB]")
        except Exception as e2:
            print(f"    M2 OLS+EB fallback also failed: {e2}")
            results.append({'model': 'M2', 'description': 'Random slopes (failed)',
                            'AIC': np.nan, 'BIC': np.nan, 'loglik': np.nan,
                            'held_out_logloss': np.nan, 'converged': False})

    mc_df = pd.DataFrame(results)
    mc_path = os.path.join(OUT_DIR, 'model_comparison.csv')
    mc_df.to_csv(mc_path, index=False)
    print(f"  Saved: {mc_path}")
    return mc_df


# ─── Step 2: Empirical Bayes Hierarchical Model ───────────────────────────────

def step2_empirical_bayes(df_official: pd.DataFrame) -> pd.DataFrame:
    """
    Fit RAE_ij = mu + u_i + beta_i * PI_ij + e_ij per batter.
    Uses closed-form Lindley-Smith EB (adapted BayesianHierarchicalEngine).
    Returns batter_posteriors DataFrame.
    """
    print("\n=== STEP 2: Empirical Bayes Hierarchical Model ===")
    from cie.hierarchical_bayes import BayesianHierarchicalEngine

    bat_df = df_official[df_official['is_batter_ball'] == True].copy()
    bat_df = bat_df.dropna(subset=['runs_above_expectation', 'pressure_index_hybrid', 'striker_id'])

    MIN_BALLS   = 50
    MIN_MATCHES = 8

    player_summary = bat_df.groupby('striker_id').agg(
        total_balls=('runs', 'count'),
        total_matches=('match_id', 'nunique'),
        striker_name=('striker_name', 'first')
    ).reset_index()
    eligible_ids = player_summary[
        (player_summary['total_balls']   >= MIN_BALLS) &
        (player_summary['total_matches'] >= MIN_MATCHES)
    ]['striker_id'].unique()
    print(f"  Eligible players (>={MIN_BALLS} balls, >={MIN_MATCHES} matches): {len(eligible_ids)}")

    eligible_df = bat_df[bat_df['striker_id'].isin(eligible_ids)].copy()

    # Design matrix: [intercept, pressure_index_hybrid]
    X = np.column_stack([
        np.ones(len(eligible_df)),
        eligible_df['pressure_index_hybrid'].values
    ])
    y    = eligible_df['runs_above_expectation'].values
    pids = eligible_df['striker_id'].values

    engine = BayesianHierarchicalEngine()
    posteriors = engine.fit_hierarchical_random_slopes(
        pids, X, y, ['intercept', 'clutch_slope']
    )

    # Merge player names
    posteriors = posteriors.merge(
        player_summary[['striker_id', 'striker_name', 'total_balls', 'total_matches']],
        left_on='player_id', right_on='striker_id', how='left'
    )

    # Rename for readability
    posteriors = posteriors.rename(columns={
        'post_mean_intercept':          'u_i',
        'post_se_intercept':            'u_i_se',
        'post_ci95_low_intercept':      'u_i_ci95_low',
        'post_ci95_high_intercept':     'u_i_ci95_high',
        'post_mean_clutch_slope':       'beta_i',
        'post_se_clutch_slope':         'beta_i_se',
        'post_ci95_low_clutch_slope':   'beta_i_ci95_low',
        'post_ci95_high_clutch_slope':  'beta_i_ci95_high',
    })

    # Key scientific finding: sigma_beta
    sigma_beta = float(np.std(posteriors['beta_i'], ddof=1))
    print(f"  sigma_beta (SD of clutch slopes across players): {sigma_beta:.6f}")

    # Save
    post_path = os.path.join(OUT_DIR, 'batter_posteriors.csv')
    posteriors.to_csv(post_path, index=False)
    print(f"  Saved: {post_path} ({len(posteriors)} players)")
    return posteriors, sigma_beta


# ─── Step 3: Permutation Test for Clutch Heterogeneity ───────────────────────

def step3_permutation_test(df_official: pd.DataFrame, observed_sigma_beta: float,
                            n_perms: int = 500) -> pd.DataFrame:
    """
    Permutation test: shuffle PI within (player, match), recompute OLS slopes,
    compute permuted SD of slopes. p = fraction of permuted SDs >= observed.
    """
    print(f"\n=== STEP 3: Permutation Test ({n_perms} permutations) ===")

    bat_df = df_official[
        (df_official['is_batter_ball'] == True) &
        (df_official['is_high_pressure'] == True)
    ].copy()
    bat_df = bat_df.dropna(subset=['runs_above_expectation', 'pressure_index_hybrid', 'striker_id'])

    # Eligible players: >=50 pressure balls
    player_counts = bat_df.groupby('striker_id').size()
    eligible_ids  = player_counts[player_counts >= 50].index
    bat_eligible  = bat_df[bat_df['striker_id'].isin(eligible_ids)].copy().reset_index(drop=True)
    print(f"  Players >=50 pressure balls: {len(eligible_ids)}")
    print(f"  Total pressure deliveries for permutation: {len(bat_eligible):,}")

    def compute_slope_sd(data: pd.DataFrame) -> float:
        slopes = []
        for pid, grp in data.groupby('striker_id'):
            x = grp['pressure_index_hybrid'].values
            y = grp['runs_above_expectation'].values
            if len(x) < 2 or np.std(x) < 1e-10:
                continue
            X_p = np.column_stack([np.ones(len(x)), x])
            try:
                b, _, _, _ = np.linalg.lstsq(X_p, y, rcond=None)
                slopes.append(float(b[1]))
            except Exception:
                pass
        return float(np.std(slopes, ddof=1)) if len(slopes) >= 2 else 0.0

    # Observed (using raw OLS, not EB, for direct comparison with permutations)
    observed_sd = compute_slope_sd(bat_eligible)
    print(f"  Observed SD of OLS clutch slopes: {observed_sd:.6f}")

    rng = np.random.default_rng(42)
    permuted_sds = []

    for perm_i in range(n_perms):
        perm_df = bat_eligible.copy()
        # Shuffle PI within each (player, match) group
        for (pid, mid), grp in bat_eligible.groupby(['striker_id', 'match_id']):
            idx = grp.index
            shuffled_pi = rng.permutation(grp['pressure_index_hybrid'].values)
            perm_df.loc[idx, 'pressure_index_hybrid'] = shuffled_pi
        perm_sd = compute_slope_sd(perm_df)
        permuted_sds.append(perm_sd)
        if (perm_i + 1) % 100 == 0:
            print(f"    Permutation {perm_i+1}/{n_perms}  perm_sd={perm_sd:.5f}")

    permuted_sds = np.array(permuted_sds)
    p_value      = float(np.mean(permuted_sds >= observed_sd))
    pct95_null   = float(np.percentile(permuted_sds, 95))

    print(f"  Observed sigma_beta (OLS): {observed_sd:.6f}")
    print(f"  95th pct of null:          {pct95_null:.6f}")
    print(f"  Permutation p-value:       {p_value:.4f}")

    perm_df_out = pd.DataFrame({
        'statistic': ['observed_sigma_beta', 'pct95_null', 'mean_null', 'p_value', 'n_perms', 'n_eligible_players'],
        'value':     [observed_sd, pct95_null, float(np.mean(permuted_sds)), p_value, n_perms, len(eligible_ids)]
    })
    perm_path = os.path.join(OUT_DIR, 'permutation_test.csv')
    perm_df_out.to_csv(perm_path, index=False)
    print(f"  Saved: {perm_path}")
    return perm_df_out, observed_sd, p_value


# ─── Step 4: PressureLevel vs Clutch Rankings ─────────────────────────────────

def step4_dual_rankings(df_official: pd.DataFrame,
                         posteriors: pd.DataFrame) -> pd.DataFrame:
    """
    PressureLevel: shrunk RAE in high-pressure states.
    Clutch:        shrunk beta_i (marginal pressure response slope).
    Both: IPL+T20I, >=100 pressure balls, >=12 matches.
    """
    print("\n=== STEP 4: PressureLevel vs Clutch Rankings ===")

    bat_df = df_official[df_official['is_batter_ball'] == True].copy()
    press_df = bat_df[bat_df['is_high_pressure'] == True].copy()

    # Eligibility: >=100 pressure balls, >=12 matches
    player_summary = press_df.groupby('striker_id').agg(
        pressure_balls=('runs', 'count'),
        pressure_matches=('match_id', 'nunique'),
        striker_name=('striker_name', 'first'),
        mean_press_rae=('runs_above_expectation', 'mean')
    ).reset_index()
    eligible = player_summary[
        (player_summary['pressure_balls']   >= 100) &
        (player_summary['pressure_matches'] >= 12)
    ].copy()
    print(f"  Eligible (>=100 pressure balls, >=12 matches): {len(eligible)} players")

    if len(eligible) == 0:
        # Relax thresholds
        eligible = player_summary[
            (player_summary['pressure_balls']   >= 50) &
            (player_summary['pressure_matches'] >= 8)
        ].copy()
        print(f"  Relaxed (>=50 pressure balls, >=8 matches): {len(eligible)} players")

    # ── PressureLevel: Shrunk RAE via James-Stein ──
    grand_mean_rae = float(press_df['runs_above_expectation'].mean())
    sigma_e2 = float(press_df['runs_above_expectation'].var())

    # Variance of player means (between-player)
    player_means = press_df.groupby('striker_id')['runs_above_expectation'].mean()
    sigma_u2 = max(float(player_means.var() - sigma_e2 / press_df.groupby('striker_id').size().mean()), 1e-6)

    pressure_level_scores = {}
    for _, row in eligible.iterrows():
        pid  = row['striker_id']
        n_i  = row['pressure_balls']
        mu_i = row['mean_press_rae']
        # Shrinkage: k* = sigma_e2 / sigma_u2
        k_opt = sigma_e2 / sigma_u2
        alpha_i = n_i / (n_i + k_opt)
        shrunk_rae = grand_mean_rae + alpha_i * (mu_i - grand_mean_rae)
        pressure_level_scores[pid] = shrunk_rae

    eligible['pressure_level_score'] = eligible['striker_id'].map(pressure_level_scores)

    # ── Clutch: Shrunk beta_i from posteriors ──
    beta_map = posteriors.set_index('player_id')['beta_i'].to_dict()
    eligible['clutch_score'] = eligible['striker_id'].map(beta_map)
    eligible = eligible.dropna(subset=['clutch_score']).copy()
    print(f"  Players with both scores: {len(eligible)}")

    # Rankings
    eligible['pressurelevel_rank'] = eligible['pressure_level_score'].rank(ascending=False).astype(int)
    eligible['clutch_rank']        = eligible['clutch_score'].rank(ascending=False).astype(int)
    eligible = eligible.sort_values('pressurelevel_rank')

    # Top-10 overlap
    top10_pl = set(eligible.nsmallest(10, 'pressurelevel_rank')['striker_id'])
    top10_cl = set(eligible.nsmallest(10, 'clutch_rank')['striker_id'])
    overlap   = len(top10_pl & top10_cl)
    print(f"  Top-10 overlap (PressureLevel ∩ Clutch): {overlap}/10")

    # Kendall tau between the two rankings (all eligible players)
    tau_val, tau_p = kendalltau(eligible['pressurelevel_rank'], eligible['clutch_rank'])
    print(f"  Kendall tau (PressureLevel vs Clutch ranks): {tau_val:.4f}  p={tau_p:.4f}")

    # Save
    out = eligible[['striker_id', 'striker_name', 'pressure_balls', 'pressure_matches',
                    'mean_press_rae', 'pressure_level_score', 'pressurelevel_rank',
                    'clutch_score', 'clutch_rank']].copy()
    out['top10_pressurelevel'] = out['striker_id'].isin(top10_pl)
    out['top10_clutch']        = out['striker_id'].isin(top10_cl)
    out['kendall_tau']         = tau_val

    rank_path = os.path.join(OUT_DIR, 'pressurelevel_vs_clutch_rankings.csv')
    out.to_csv(rank_path, index=False)
    print(f"  Saved: {rank_path}")
    return out, overlap, tau_val


# ─── Step 5: Walk-Forward Validation ─────────────────────────────────────────

def step5_walkforward(df_official: pd.DataFrame,
                       rankings_df: pd.DataFrame) -> pd.DataFrame:
    """
    Train 2022-2024, test 2025+2026.
    Report Kendall tau between train ranks and test RAE, Precision@10.
    """
    print("\n=== STEP 5: Walk-Forward Validation ===")

    bat_df = df_official[df_official['is_batter_ball'] == True].copy()

    train_bat = bat_df[bat_df['season'].isin(TRAIN_SEASONS)].copy()
    test_bat  = bat_df[bat_df['season'].isin(TEST_SEASONS)].copy()

    press_train = train_bat[train_bat['is_high_pressure'] == True]
    press_test  = test_bat[test_bat['is_high_pressure'] == True]

    print(f"  Train pressure deliveries: {len(press_train):,}")
    print(f"  Test  pressure deliveries: {len(press_test):,}")

    # Test-period: compute mean pressure RAE per player
    test_rae = press_test.groupby('striker_id').agg(
        test_press_rae=('runs_above_expectation', 'mean'),
        test_press_balls=('runs', 'count')
    ).reset_index()

    # Train-period: compute both rankings
    train_psum = press_train.groupby('striker_id').agg(
        train_press_balls=('runs', 'count'),
        train_press_matches=('match_id', 'nunique'),
        train_press_rae=('runs_above_expectation', 'mean'),
        striker_name=('striker_name', 'first')
    ).reset_index()

    # Grand mean & shrinkage for train PressureLevel
    grand_mean_tr = float(press_train['runs_above_expectation'].mean())
    sigma_e2_tr   = float(press_train['runs_above_expectation'].var())
    player_means_tr = press_train.groupby('striker_id')['runs_above_expectation'].mean()
    sigma_u2_tr   = max(float(player_means_tr.var() - sigma_e2_tr / max(press_train.groupby('striker_id').size().mean(), 1)), 1e-6)
    k_opt_tr      = sigma_e2_tr / sigma_u2_tr

    train_psum['pl_score'] = train_psum.apply(
        lambda r: grand_mean_tr + (r['train_press_balls'] / (r['train_press_balls'] + k_opt_tr)) * (r['train_press_rae'] - grand_mean_tr),
        axis=1
    )

    # Train clutch slope per player (OLS) for walk-forward validation
    # Use all deliveries for clutch slope
    train_all_bat = train_bat.dropna(subset=['runs_above_expectation', 'pressure_index_hybrid', 'striker_id'])
    clutch_slopes_tr = {}
    for pid, grp in train_all_bat.groupby('striker_id'):
        if len(grp) < 30:
            continue
        x = grp['pressure_index_hybrid'].values
        y = grp['runs_above_expectation'].values
        X_p = np.column_stack([np.ones(len(x)), x])
        try:
            b, _, _, _ = np.linalg.lstsq(X_p, y, rcond=None)
            clutch_slopes_tr[pid] = float(b[1])
        except Exception:
            pass

    # EB shrinkage of clutch slopes
    if len(clutch_slopes_tr) >= 5:
        slopes_arr_tr = np.array(list(clutch_slopes_tr.values()))
        mu_slope_tr   = float(np.mean(slopes_arr_tr))
        sigma2_b_tr   = max(float(np.var(slopes_arr_tr, ddof=1)), 1e-6)
        sigma2_w_tr   = float(press_train['runs_above_expectation'].var())
        eb_clutch_tr  = {}
        for pid, raw_slope in clutch_slopes_tr.items():
            n_i = len(train_all_bat[train_all_bat['striker_id'] == pid])
            B   = sigma2_b_tr / (sigma2_b_tr + sigma2_w_tr / n_i)
            eb_clutch_tr[pid] = mu_slope_tr + B * (raw_slope - mu_slope_tr)
    else:
        eb_clutch_tr = {pid: s for pid, s in clutch_slopes_tr.items()}

    train_psum['clutch_score'] = train_psum['striker_id'].map(eb_clutch_tr)

    # Eligibility filter (use same thresholds as step 4; relax if needed)
    eligible_tr = train_psum[
        (train_psum['train_press_balls']   >= 50) &
        (train_psum['train_press_matches'] >= 8)
    ].dropna(subset=['clutch_score']).copy()
    print(f"  Train eligible players: {len(eligible_tr)}")

    eligible_tr['pl_rank']     = eligible_tr['pl_score'].rank(ascending=False).astype(int)
    eligible_tr['clutch_rank'] = eligible_tr['clutch_score'].rank(ascending=False).astype(int)

    # Merge with test RAE
    merged = eligible_tr.merge(test_rae, on='striker_id', how='inner')
    print(f"  Players with both train rank and test RAE: {len(merged)}")

    validation_rows = []

    if len(merged) >= 5:
        merged['test_rae_rank'] = merged['test_press_rae'].rank(ascending=False).astype(int)

        tau_pl, p_pl     = kendalltau(merged['pl_rank'],     merged['test_press_rae'])
        tau_cl, p_cl     = kendalltau(merged['clutch_rank'], merged['test_press_rae'])

        # Precision@10: how many train top-10 appear in test top-10?
        train_top10_pl = set(eligible_tr.nsmallest(10, 'pl_rank')['striker_id'])
        train_top10_cl = set(eligible_tr.nsmallest(10, 'clutch_rank')['striker_id'])
        test_top10_ids = set(merged.nsmallest(10, 'pl_rank')['striker_id']) \
                         if len(merged) >= 10 else set(merged['striker_id'])

        # Test top-10 by actual performance
        test_top10_actual = set(merged.nsmallest(10, 'test_rae_rank')['striker_id']) \
                            if len(merged) >= 10 else set(merged['striker_id'])

        prec10_pl = len(train_top10_pl & test_top10_actual)
        prec10_cl = len(train_top10_cl & test_top10_actual)

        print(f"  PressureLevel — Kendall tau: {tau_pl:.4f}  p={p_pl:.4f}  Precision@10: {prec10_pl}/10")
        print(f"  Clutch        — Kendall tau: {tau_cl:.4f}  p={p_cl:.4f}  Precision@10: {prec10_cl}/10")

        validation_rows = [
            {'method': 'PressureLevel', 'kendall_tau': tau_pl, 'tau_pvalue': p_pl, 'precision_at_10': prec10_pl},
            {'method': 'Clutch',        'kendall_tau': tau_cl, 'tau_pvalue': p_cl, 'precision_at_10': prec10_cl},
        ]
    else:
        print("  Insufficient overlap for walk-forward validation.")
        validation_rows = [
            {'method': 'PressureLevel', 'kendall_tau': np.nan, 'tau_pvalue': np.nan, 'precision_at_10': np.nan},
            {'method': 'Clutch',        'kendall_tau': np.nan, 'tau_pvalue': np.nan, 'precision_at_10': np.nan},
        ]

    wf_df = pd.DataFrame(validation_rows)
    wf_path = os.path.join(OUT_DIR, 'walkforward_validation.csv')
    wf_df.to_csv(wf_path, index=False)
    print(f"  Saved: {wf_path}")
    return wf_df


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("SupeRR Selector Season 2 — Hierarchical Model")
    print("=" * 70)

    df_official = load_data()

    # Step 1
    mc_df = step1_mixed_models(df_official)

    # Step 2
    posteriors, sigma_beta_eb = step2_empirical_bayes(df_official)

    # Step 3
    perm_df, observed_sd, p_value = step3_permutation_test(df_official, sigma_beta_eb, n_perms=500)

    # Step 4
    rankings_df, top10_overlap, tau_ranks = step4_dual_rankings(df_official, posteriors)

    # Step 5
    wf_df = step5_walkforward(df_official, rankings_df)

    # ── Summary ──────────────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("KEY FINDINGS SUMMARY")
    print("=" * 70)
    print(f"  sigma_beta (EB posterior SD of clutch slopes):  {sigma_beta_eb:.6f}")
    print(f"  sigma_beta (OLS observed SD of clutch slopes):  {observed_sd:.6f}")
    print(f"  Permutation p-value (clutch heterogeneity):     {p_value:.4f}")
    print(f"  Top-10 overlap (PressureLevel ∩ Clutch):        {top10_overlap}/10")
    print(f"  Kendall tau (PressureLevel vs Clutch ranking):  {tau_ranks:.4f}")
    for _, row in wf_df.iterrows():
        print(f"  Walk-forward [{row['method']:14s}]: tau={row['kendall_tau']:.4f}  P@10={row['precision_at_10']}")
    print("=" * 70)
    print("All outputs saved to outputs/hierarchical/")


if __name__ == '__main__':
    main()
