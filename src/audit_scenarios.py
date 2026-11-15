"""
Audit Scenarios Script.
Tests 2nd innings and 1st innings pressure models across manually specified cricket situations.
"""
import numpy as np
import pandas as pd

def run_scenarios():
    print("=" * 65)
    print("AUDIT: SECOND-INNINGS PRESSURE SCENARIO EVALUATION")
    print("=" * 65)
    
    scenarios = [
        {'name': '1. Low RRR, many wickets, many balls (Cruising start)', 'rrr': 6.0, 'wkts_lost': 1, 'balls_rem': 100, 'sched_balls': 120, 'runs_needed': 100},
        {'name': '2. High RRR, many wickets remaining (Steep chase mid)', 'rrr': 12.0, 'wkts_lost': 2, 'balls_rem': 60, 'sched_balls': 120, 'runs_needed': 120},
        {'name': '3. Low wickets remaining & many runs required (Collapse chase)', 'rrr': 10.0, 'wkts_lost': 7, 'balls_rem': 48, 'sched_balls': 120, 'runs_needed': 80},
        {'name': '4. Very high RRR with few balls remaining (Heroic finish)', 'rrr': 16.0, 'wkts_lost': 5, 'balls_rem': 12, 'sched_balls': 120, 'runs_needed': 32},
        {'name': '5. Comfortable chase during death overs (Cruising home)', 'rrr': 5.0, 'wkts_lost': 3, 'balls_rem': 18, 'sched_balls': 120, 'runs_needed': 15},
        {'name': '6. Difficult chase during middle overs (Building pressure)', 'rrr': 11.0, 'wkts_lost': 4, 'balls_rem': 54, 'sched_balls': 120, 'runs_needed': 99},
        {'name': '7. Hopeless chase / Lost cause (Dead rubber)', 'rrr': 36.0, 'wkts_lost': 8, 'balls_rem': 12, 'sched_balls': 120, 'runs_needed': 72}
    ]

    for sc in scenarios:
        rrr_comp = np.clip((sc['rrr'] - 6.0) / 8.0, 0.0, 1.5)
        wkt_comp = np.clip(sc['wkts_lost'] / 8.0, 0.0, 1.25)
        ball_scarcity = 1.0 - (sc['balls_rem'] / sc['sched_balls'])
        closeness_comp = 1.0 if (sc['balls_rem'] <= 30 and sc['runs_needed'] <= 45) else 0.0
        
        pi_rule = (0.40 * rrr_comp + 0.30 * wkt_comp + 0.20 * ball_scarcity + 0.10 * closeness_comp)
        
        print(f"Scenario: {sc['name']}")
        print(f"   Inputs: RRR={sc['rrr']:.1f}, Wkts Lost={sc['wkts_lost']}, Balls Rem={sc['balls_rem']}, Runs Needed={sc['runs_needed']}")
        print(f"   Components: RRR_comp={rrr_comp:.2f}, Wkt_comp={wkt_comp:.2f}, Ball_Scarcity={ball_scarcity:.2f}, Closeness={closeness_comp:.1f}")
        print(f"   --> Rule-Based Pressure Index: {pi_rule:.3f}")
        print()

    print("=" * 65)
    print("AUDIT: CALIBRATED FIRST-INNINGS PRESSURE SCENARIO EVALUATION")
    print("=" * 65)
    
    inn1_scenarios_cal = [
        {'name': 'A. Stable Powerplay (35/0 after 4 overs)', 'wkts_lost': 0, 'balls_comp': 24, 'score': 35, 'par_def': -5},
        {'name': 'B. Early Batting Collapse (18/3 after 4 overs)', 'wkts_lost': 3, 'balls_comp': 24, 'score': 18, 'par_def': 15},
        {'name': 'C. Strong Middle-Over Scoring (110/1 after 12 overs)', 'wkts_lost': 1, 'balls_comp': 72, 'score': 110, 'par_def': -15},
        {'name': 'D. Middle-Over Collapse (75/5 after 12 overs)', 'wkts_lost': 5, 'balls_comp': 72, 'score': 75, 'par_def': 20},
        {'name': 'E. Low Expected Final Score (105/6 after 16 overs)', 'wkts_lost': 6, 'balls_comp': 96, 'score': 105, 'par_def': 25},
        {'name': 'F. High-Scoring Death Overs (165/3 after 18 overs)', 'wkts_lost': 3, 'balls_comp': 108, 'score': 165, 'par_def': -10},
        {'name': 'G. Acute Death Overs (180/6 after 19.3 overs)', 'wkts_lost': 6, 'balls_comp': 117, 'score': 180, 'par_def': 0}
    ]

    for sc in inn1_scenarios_cal:
        collapse_intensity = np.clip((sc['wkts_lost'] - 1.0) / 3.0, 0.0, 1.25) * np.clip(1.0 - (sc['balls_comp'] / 120.0), 0.0, 1.0)
        death_urgency = np.clip((sc['balls_comp'] - 90.0) / 30.0, 0.0, 1.0)
        situational_urgency = max(collapse_intensity, death_urgency)
        
        wkt_scarcity = np.clip(sc['wkts_lost'] / 8.0, 0.0, 1.0)
        par_deficit = np.clip(sc['par_def'] / 25.0, 0.0, 1.0)
        
        pi_cal = 0.50 * situational_urgency + 0.30 * wkt_scarcity + 0.20 * par_deficit
        
        print(f"Scenario: {sc['name']}")
        print(f"   Inputs: Wkts Lost={sc['wkts_lost']}, Balls Comp={sc['balls_comp']}, Score={sc['score']}, Par Deficit={sc['par_def']}")
        print(f"   Components: Sit_Urgency={situational_urgency:.2f}, Wkt_Scarcity={wkt_scarcity:.2f}, Deficit={par_deficit:.2f}")
        print(f"   --> Calibrated Innings 1 Pressure: {pi_cal:.3f}")
        print()

if __name__ == '__main__':
    run_scenarios()
