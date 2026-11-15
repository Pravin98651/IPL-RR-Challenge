"""
Corrected & Calibrated Pressure Detection and Modeling Module.
Implements:
1. Accurate Ball Scarcity: 1 - (Legal Balls Remaining / Scheduled Legal Balls)
2. Calibrated 1st Innings Pressure: max(Collapse, Death Urgency) + Wicket Scarcity + Par Deficit
3. Dynamic Leverage Index from Win Probability models
4. Hybrid Pressure Index balancing domain rules and statistical leverage
"""
import pandas as pd
import numpy as np
from typing import Dict, Any

def compute_rule_based_pressure(df: pd.DataFrame, knockout_multiplier: float = 1.20) -> pd.Series:
    """
    Computes Model A: Domain Rule-Based Pressure Index.
    """
    # Scheduled balls safety check
    if 'scheduled_legal_balls' in df.columns:
        sched_balls = df['scheduled_legal_balls'].replace(0, 120).fillna(120)
    else:
        sched_balls = pd.Series(120, index=df.index)
        
    if 'pre_legal_balls_remaining' in df.columns:
        balls_rem = df['pre_legal_balls_remaining'].fillna(120)
    elif 'pre_legal_balls_completed' in df.columns:
        balls_rem = np.maximum(0, sched_balls - df['pre_legal_balls_completed'])
    else:
        balls_rem = pd.Series(120, index=df.index)
    
    # Accurate Ball Scarcity: 1 - (Legal Balls Remaining / Scheduled Legal Balls)
    ball_scarcity = np.clip(1.0 - (balls_rem / sched_balls), 0.0, 1.0)
    
    # --- Innings 2 (Chase) ---
    rrr = df['rrr_pre'].fillna(0)
    rrr_comp = np.clip((rrr - 6.0) / 8.0, 0.0, 1.5)
    
    wkts_lost = df['pre_wickets_lost']
    wkt_comp = np.clip(wkts_lost / 8.0, 0.0, 1.25)
    
    # Closeness factor in death overs (overs >= 15 and runs needed <= 45)
    runs_needed = df['runs_needed_pre'].fillna(999)
    closeness_comp = np.where((balls_rem <= 30) & (runs_needed <= 45), 1.0, 0.0)
    
    pi_chase = (0.40 * rrr_comp +
                0.30 * wkt_comp +
                0.20 * ball_scarcity +
                0.10 * closeness_comp)
    
    # --- Innings 1 (Setting Total) ---
    # Calibrated formulation: Collapse and Death are phase-specific, so take their maximum
    collapse_intensity = np.clip((wkts_lost - 1.0) / 3.0, 0.0, 1.25) * np.clip(1.0 - (df['pre_legal_balls_completed'] / sched_balls), 0.0, 1.0)
    death_urgency = np.clip((df['pre_legal_balls_completed'] - (sched_balls * 0.75)) / (sched_balls * 0.25), 0.0, 1.0)
    situational_urgency = np.maximum(collapse_intensity, death_urgency)
    
    wkt_scarcity = np.clip(wkts_lost / 8.0, 0.0, 1.0)
    par_deficit = np.clip(df['par_deficit'].fillna(0) / 25.0, 0.0, 1.0)
    
    pi_inn1 = (0.50 * situational_urgency +
               0.30 * wkt_scarcity +
               0.20 * par_deficit)
    
    is_chase = df['innings'] >= 2
    raw_pi = np.where(is_chase, pi_chase, pi_inn1)
    
    # Match Stakes Multiplier (Knockout matches)
    knockout_mult = np.where(df['knock_out'] == 1, knockout_multiplier, 1.0)
    pi_rule = raw_pi * knockout_mult
    
    return pd.Series(pi_rule, index=df.index, name='pressure_index_rule')

def compute_leverage_pressure(df: pd.DataFrame) -> pd.Series:
    """
    Computes Model B: Win-Probability Leverage Pressure Index.
    """
    li = df['leverage_index'].fillna(1.0)
    pi_lev = np.clip(li / 2.0, 0.0, 1.5)
    return pd.Series(pi_lev, index=df.index, name='pressure_index_leverage')

def compute_hybrid_pressure(df: pd.DataFrame, knockout_multiplier: float = 1.20) -> pd.Series:
    """
    Computes Model C: Hybrid Pressure Index.
    Balances rule-based situational demand and win-probability leverage in chases;
    uses calibrated collapse, death-urgency, and par deficit in 1st innings.
    """
    pi_rule = compute_rule_based_pressure(df, knockout_multiplier)
    pi_lev = compute_leverage_pressure(df)
    
    is_chase = df['innings'] >= 2
    # In chase: 50% rule + 50% leverage
    pi_hybrid_chase = 0.50 * pi_rule + 0.50 * pi_lev
    # In 1st innings: calibrated rule
    pi_hybrid_inn1 = pi_rule
    
    pi_hybrid = np.where(is_chase, pi_hybrid_chase, pi_hybrid_inn1)
    return pd.Series(pi_hybrid, index=df.index, name='pressure_index_hybrid')

def classify_pressure(pi: pd.Series) -> pd.Series:
    """
    Categorizes continuous pressure score into Low, Moderate, High, Extreme.
    """
    conditions = [
        pi < 0.35,
        (pi >= 0.35) & (pi < 0.60),
        (pi >= 0.60) & (pi < 0.85),
        pi >= 0.85
    ]
    labels = ['Low', 'Moderate', 'High', 'Extreme']
    return pd.Series(np.select(conditions, labels, default='Moderate'), index=pi.index, name='pressure_tier')

def apply_pressure_models(df: pd.DataFrame, knockout_multiplier: float = 1.20) -> pd.DataFrame:
    df = df.copy()
    df['pressure_index_rule'] = compute_rule_based_pressure(df, knockout_multiplier)
    df['pressure_index_leverage'] = compute_leverage_pressure(df)
    df['pressure_index_hybrid'] = compute_hybrid_pressure(df, knockout_multiplier)
    
    df['pressure_score'] = df['pressure_index_hybrid']
    df['pressure_tier'] = classify_pressure(df['pressure_score'])
    df['is_high_pressure'] = df['pressure_score'] >= 0.60
    
    return df
