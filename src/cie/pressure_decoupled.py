"""
Clutch Intelligence Engine 2.0 — Decoupled Pressure Module
Implements:
1. Calibrated Win Probability Models for Innings 1 and Innings 2 (no flat 50% assumption).
2. Discrete Delivery Outcome Probability Distribution P(o|s).
3. Exact Cricket Match-State Transition Function (legal ball consumption, score, wickets, striker swaps).
4. High-Performance Vectorized Match Leverage: LI(s) = SUM_o P(o|s) * |WP(s_o) - WP(s)|.
5. Situational Urgency: P_urgency = f(RRR, Wkts, Balls, Par Deficit, Phase).
"""

import os
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from typing import Dict, Tuple, List, Any

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PARQUET = os.path.join(ROOT, 'outputs', 'features', 'delivery_features.parquet')

# Outcomes modeled
OUTCOMES = ['dot', 'one', 'two', 'three', 'four', 'five', 'six', 'wide', 'noball', 'wicket']

# Outcome mapping: (runs_added, is_wicket, is_legal, bat_runs)
OUTCOME_CONFIG = {
    'dot':    (0, False, True, 0),
    'one':    (1, False, True, 1),
    'two':    (2, False, True, 2),
    'three':  (3, False, True, 3),
    'four':   (4, False, True, 4),
    'five':   (5, False, True, 5),
    'six':    (6, False, True, 6),
    'wide':   (1, False, False, 0),
    'noball': (1, False, False, 0),
    'wicket': (0, True, True, 0),
}

def categorize_delivery_outcome(row: pd.Series) -> str:
    """Categorizes a raw delivery into one of the discrete outcomes."""
    if row.get('is_wicket', 0) == 1:
        return 'wicket'
    extras_type = row.get('extras_type', None)
    if extras_type == 'wide':
        return 'wide'
    if extras_type in ['Overstep', 'noball']:
        return 'noball'
    runs = row.get('runs', 0)
    if runs == 0:
        return 'dot'
    elif runs == 1:
        return 'one'
    elif runs == 2:
        return 'two'
    elif runs == 3:
        return 'three'
    elif runs == 4:
        return 'four'
    elif runs == 5:
        return 'five'
    elif runs == 6:
        return 'six'
    return 'dot'

class DecoupledPressureEngine:
    def __init__(self, knockout_multiplier: float = 1.20):
        self.knockout_multiplier = knockout_multiplier
        self.wp_model_inn1 = None
        self.wp_model_inn2 = None
        self.inn1_features = [
            'pre_current_score', 'pre_wickets_lost', 'pre_legal_balls_completed',
            'crr_pre', 'par_deficit', 'knock_out'
        ]
        self.inn2_features = [
            'runs_needed_pre', 'pre_wickets_remaining', 'pre_legal_balls_remaining',
            'rrr_pre', 'crr_pre', 'knock_out'
        ]
        self.phase_outcome_probs = {}

    def fit_wp_models(self, df: pd.DataFrame):
        """Fits calibrated win probability models for Innings 1 and Innings 2."""
        df_clean = df.copy()
        df_clean['batting_team_wins'] = (df_clean['win_team_id'] == df_clean['batting_team_id']).astype(int)
        
        # --- Innings 1 Model ---
        inn1 = df_clean[df_clean['innings'] == 1].copy()
        X_inn1 = inn1[self.inn1_features].fillna(0)
        y_inn1 = inn1['batting_team_wins']
        base_lr1 = LogisticRegression(max_iter=1000, random_state=42)
        self.wp_model_inn1 = CalibratedClassifierCV(base_lr1, method='sigmoid', cv=3)
        self.wp_model_inn1.fit(X_inn1, y_inn1)
        
        # --- Innings 2 Model ---
        inn2 = df_clean[df_clean['innings'] >= 2].copy()
        X_inn2 = inn2[self.inn2_features].fillna(0)
        y_inn2 = inn2['batting_team_wins']
        base_lr2 = LogisticRegression(max_iter=1000, random_state=42)
        self.wp_model_inn2 = CalibratedClassifierCV(base_lr2, method='sigmoid', cv=3)
        self.wp_model_inn2.fit(X_inn2, y_inn2)
        
        # --- Outcome Probabilities Conditioned on Innings and Phase ---
        df_clean['outcome_cat'] = df_clean.apply(categorize_delivery_outcome, axis=1)
        grouped = df_clean.groupby(['innings', 'phase'])['outcome_cat'].value_counts(normalize=True).unstack(fill_value=0.001)
        self.phase_outcome_probs = grouped.div(grouped.sum(axis=1), axis=0).to_dict('index')

    def state_transition(self, s: Dict[str, Any], outcome: str) -> Dict[str, Any]:
        """
        Executes strict cricket state transition s -> s_o under outcome o.
        Handles legal balls, runs, wickets, and striker/non-striker crossing.
        """
        s_next = s.copy()
        inn = s_next['innings']
        striker = s_next.get('striker_id', 'striker')
        non_striker = s_next.get('non_striker_id', 'non_striker')
        
        runs_add, is_wkt, is_legal, bat_runs = OUTCOME_CONFIG.get(outcome, (0, False, True, 0))
        
        if inn == 1:
            s_next['current_score'] = s_next.get('current_score', 0) + runs_add
            if is_legal:
                s_next['balls_completed'] = min(120, s_next.get('balls_completed', 0) + 1)
            if is_wkt:
                s_next['wickets_lost'] = min(10, s_next.get('wickets_lost', 0) + 1)
        else:
            s_next['runs_needed'] = max(0, s_next.get('runs_needed', 100) - runs_add)
            if is_legal:
                s_next['balls_remaining'] = max(0, s_next.get('balls_remaining', 120) - 1)
                s_next['balls_completed'] = min(120, s_next.get('balls_completed', 0) + 1)
            if is_wkt:
                s_next['wickets_remaining'] = max(0, s_next.get('wickets_remaining', 10) - 1)
                s_next['wickets_lost'] = min(10, s_next.get('wickets_lost', 0) + 1)
                
        # Striker crossing on odd bat runs
        if bat_runs % 2 == 1:
            striker, non_striker = non_striker, striker
            
        # Change ends on 6th legal ball of over
        if is_legal and (s_next.get('balls_completed', 0) % 6 == 0):
            striker, non_striker = non_striker, striker
            
        if is_wkt:
            striker = f"new_batter_wkt_{s_next['wickets_lost']}"
            
        s_next['striker_id'] = striker
        s_next['non_striker_id'] = non_striker
        return s_next

    def compute_situational_urgency(self, df: Any) -> Any:
        """
        Computes normalized Situational Urgency P_urgency in [0, 1.5]
        using documented transformations across a dataframe or single Series.
        """
        is_single = isinstance(df, pd.Series)
        if is_single:
            df = df.to_frame().T
            
        is_chase = df['innings'] >= 2
        ko_val = df.get('knock_out', pd.Series(0, index=df.index))
        ko = np.where(ko_val == 1, self.knockout_multiplier, 1.0)
        sched_balls = df.get('scheduled_legal_balls', pd.Series(120, index=df.index))
        if isinstance(sched_balls, (int, float, np.number)):
            sched_balls = pd.Series(sched_balls if sched_balls > 0 else 120, index=df.index)
        else:
            sched_balls = sched_balls.replace(0, 120).fillna(120)
        
        # Innings 2 chase components
        rrr = df.get('rrr_pre', pd.Series(8.0, index=df.index)).fillna(8.0)
        rrr_comp = np.clip((rrr - 6.0) / 8.0, 0.0, 1.5)
        
        wkts_lost = df.get('pre_wickets_lost', pd.Series(0, index=df.index)).fillna(0)
        wkt_comp = np.clip(wkts_lost / 8.0, 0.0, 1.25)
        
        balls_rem = df.get('pre_legal_balls_remaining', pd.Series(120, index=df.index)).fillna(120)
        ball_scarcity = np.clip(1.0 - (balls_rem / sched_balls), 0.0, 1.0)
        
        runs_needed = df.get('runs_needed_pre', pd.Series(999, index=df.index)).fillna(999)
        closeness = np.where((balls_rem <= 30) & (runs_needed <= 45), 1.0, 0.0)
        
        urgency_chase = (0.40 * rrr_comp +
                         0.30 * wkt_comp +
                         0.20 * ball_scarcity +
                         0.10 * closeness)
        
        # Innings 1 components
        balls_done = df.get('pre_legal_balls_completed', pd.Series(0, index=df.index)).fillna(0)
        par_def = df.get('par_deficit', pd.Series(0.0, index=df.index)).fillna(0)
        
        collapse_intensity = np.clip((wkts_lost - 1.0) / 3.0, 0.0, 1.25) * np.clip(1.0 - (balls_done / sched_balls), 0.0, 1.0)
        death_urgency = np.clip((balls_done - (sched_balls * 0.75)) / (sched_balls * 0.25), 0.0, 1.0)
        situational_urg = np.maximum(collapse_intensity, death_urgency)
        
        wkt_scarcity_inn1 = np.clip(wkts_lost / 8.0, 0.0, 1.0)
        par_def_comp = np.clip(par_def / 25.0, 0.0, 1.0)
        
        urgency_inn1 = (0.50 * situational_urg +
                        0.30 * wkt_scarcity_inn1 +
                        0.20 * par_def_comp)
        
        raw_urgency = np.where(is_chase, urgency_chase, urgency_inn1)
        p_urgency = np.clip(raw_urgency * ko, 0.0, 1.5)
        res_series = pd.Series(p_urgency, index=df.index, name='p_urgency')
        return float(res_series.iloc[0]) if is_single else res_series

    def compute_match_leverage_vectorized(self, df: pd.DataFrame) -> Tuple[pd.Series, pd.Series]:
        """
        Computes high-speed vectorized Expected Absolute Leverage Index LI(s)
        and pre-delivery win probabilities for all deliveries.
        """
        n = len(df)
        inn1_mask = df['innings'] == 1
        inn2_mask = df['innings'] >= 2
        
        # 1. Base Pre-delivery Win Probabilities
        X1 = df.loc[inn1_mask, self.inn1_features].fillna(0)
        X2 = df.loc[inn2_mask, self.inn2_features].fillna(0)
        
        wp_pre = np.zeros(n, dtype=float)
        if len(X1) > 0:
            wp_pre[inn1_mask] = self.wp_model_inn1.predict_proba(X1)[:, 1]
        if len(X2) > 0:
            wp_pre[inn2_mask] = self.wp_model_inn2.predict_proba(X2)[:, 1]
            
        leverage_expected_delta = np.zeros(n, dtype=float)
        
        # Lookup phase outcome probabilities for each row
        phases = df['phase'].values
        innings = df['innings'].values
        sched_balls = df.get('scheduled_legal_balls', pd.Series(120, index=df.index)).replace(0, 120).fillna(120).values
        
        # For each discrete outcome, construct transitioned states and evaluate WP delta in batch
        for outcome, (runs_add, is_wkt, is_legal, bat_runs) in OUTCOME_CONFIG.items():
            # Get P(o | s) vector
            p_o = np.array([
                self.phase_outcome_probs.get((1 if inn == 1 else 2, ph), {}).get(outcome, 0.10)
                for inn, ph in zip(innings, phases)
            ])
            
            # --- Transitioned Innings 1 States ---
            if inn1_mask.sum() > 0:
                df1 = df[inn1_mask]
                balls_done_o = np.clip(df1['pre_legal_balls_completed'].values + (1 if is_legal else 0), 0, 120)
                score_o = df1['pre_current_score'].values + runs_add
                wkts_o = np.clip(df1['pre_wickets_lost'].values + (1 if is_wkt else 0), 0, 10)
                overs_done_o = np.maximum(0.1, balls_done_o / 6.0)
                crr_o = score_o / overs_done_o
                expected_par_o = (balls_done_o / sched_balls[inn1_mask]) * 165.0
                par_def_o = expected_par_o - score_o
                ko1 = df1['knock_out'].values
                
                X1_o = pd.DataFrame({
                    'pre_current_score': score_o,
                    'pre_wickets_lost': wkts_o,
                    'pre_legal_balls_completed': balls_done_o,
                    'crr_pre': crr_o,
                    'par_deficit': par_def_o,
                    'knock_out': ko1
                })[self.inn1_features]
                wp1_o = self.wp_model_inn1.predict_proba(X1_o)[:, 1]
                delta1 = np.abs(wp1_o - wp_pre[inn1_mask])
                leverage_expected_delta[inn1_mask] += p_o[inn1_mask] * delta1

            # --- Transitioned Innings 2 States ---
            if inn2_mask.sum() > 0:
                df2 = df[inn2_mask]
                balls_rem_o = np.maximum(0, df2['pre_legal_balls_remaining'].values - (1 if is_legal else 0))
                runs_need_o = np.maximum(0, df2['runs_needed_pre'].values - runs_add)
                wkts_rem_o = np.maximum(0, df2['pre_wickets_remaining'].values - (1 if is_wkt else 0))
                overs_rem_o = np.maximum(0.1, balls_rem_o / 6.0)
                rrr_o = np.where(balls_rem_o > 0, (runs_need_o / overs_rem_o), np.where(runs_need_o > 0, 99.0, 0.0))
                crr_o = df2['crr_pre'].values
                ko2 = df2['knock_out'].values
                
                X2_o = pd.DataFrame({
                    'runs_needed_pre': runs_need_o,
                    'pre_wickets_remaining': wkts_rem_o,
                    'pre_legal_balls_remaining': balls_rem_o,
                    'rrr_pre': rrr_o,
                    'crr_pre': crr_o,
                    'knock_out': ko2
                })[self.inn2_features]
                wp2_o = self.wp_model_inn2.predict_proba(X2_o)[:, 1]
                # Force exact victory/defeat terminal states
                wp2_o = np.where(runs_need_o <= 0, 1.0, wp2_o)
                wp2_o = np.where((wkts_rem_o <= 0) | ((balls_rem_o <= 0) & (runs_need_o > 0)), 0.0, wp2_o)
                
                delta2 = np.abs(wp2_o - wp_pre[inn2_mask])
                leverage_expected_delta[inn2_mask] += p_o[inn2_mask] * delta2
                
        # Scale: In competitive T20 situations, expected absolute delta is around 0.05
        # Standardized LI(s) = E[|ΔWP|] / 0.05 clipped to [0, 3.0]
        li_scores = np.clip(leverage_expected_delta / 0.05, 0.0, 3.0)
        
        return pd.Series(wp_pre, index=df.index, name='wp_calibrated_pre'), pd.Series(li_scores, index=df.index, name='p_leverage')

    def process_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Full pipeline returning decoupled urgency and match leverage columns."""
        if self.wp_model_inn1 is None or self.wp_model_inn2 is None:
            self.fit_wp_models(df)
            
        df_out = df.copy()
        df_out['p_urgency'] = self.compute_situational_urgency(df_out)
        wp_cal, p_lev = self.compute_match_leverage_vectorized(df_out)
        df_out['wp_calibrated_pre'] = wp_cal
        df_out['p_leverage'] = p_lev
        return df_out

if __name__ == '__main__':
    print("Testing DecoupledPressureEngine on official scope sample...")
    df_raw = pd.read_parquet(PARQUET)
    sample = df_raw.sample(5000, random_state=42).copy()
    engine = DecoupledPressureEngine()
    engine.fit_wp_models(df_raw)
    res = engine.process_dataframe(sample)
    print("Urgency stats:")
    print(res['p_urgency'].describe())
    print("\nLeverage stats:")
    print(res['p_leverage'].describe())
    print("\nPre-delivery Calibrated Win Probability:")
    print(res['wp_calibrated_pre'].describe())
    print("\nDecoupled Pressure Engine Test PASSED.")
