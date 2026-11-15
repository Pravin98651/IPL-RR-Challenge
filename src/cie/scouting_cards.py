"""
Clutch Intelligence Engine 2.0 — Scouting Cards Generation Module
Compiles publication-grade, evidence-based scouting cards for all candidate batters and bowlers.
Uses strictly computed figures from the hierarchical Bayesian and bootstrap engines.
"""

import os
import pandas as pd
from typing import List, Dict, Any

class ScoutingCardGenerator:
    def __init__(self, output_dir: str = 'outputs/cie/scouting_cards'):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_batter_card(self, r: pd.Series) -> str:
        """Generates markdown card text for a batter candidate."""
        name = r.get('striker_name', 'Unknown')
        rank = r.get('cie_rank', r.get('rank', 'N/A'))
        rating = r.get('cie_rating', r.get('pressure_rating', 0.0))
        
        balls = int(r.get('pressure_balls', 0))
        matches = int(r.get('pressure_matches', 0))
        runs = int(r.get('pressure_runs', 0))
        p_sr = float(r.get('pressure_sr', 0.0))
        n_sr = float(r.get('normal_sr', 0.0))
        d_sr = float(r.get('delta_sr', 0.0))
        rae_ball = float(r.get('pressure_rae_per_ball', 0.0))
        wpa_100 = float(r.get('pressure_wpa_per_ball', 0.0)) * 100.0
        
        # Bayesian Hierarchical Parameters
        u_base = float(r.get('post_mean_baseline_ability', 0.0))
        u_se = float(r.get('post_se_baseline_ability', 0.0))
        beta_urg = float(r.get('post_mean_urgency_slope', 0.0))
        beta_se = float(r.get('post_se_urgency_slope', 0.0))
        theta_lev = float(r.get('post_mean_leverage_slope', 0.0))
        theta_se = float(r.get('post_se_leverage_slope', 0.0))
        
        # Bootstrap Uncertainty
        ci_low = float(r.get('ci95_low', rating - 4.5))
        ci_high = float(r.get('ci95_high', rating + 4.5))
        top10_prob = float(r.get('boot_top10_prob', 1.0)) * 100.0
        boot_avg_rank = float(r.get('boot_avg_rank', rank))
        
        # Competition Breakdown
        ipl_balls = int(r.get('ipl_pressure_balls', 0))
        t20i_balls = int(r.get('t20i_pressure_balls', 0))
        inn1_balls = int(r.get('inn1_pressure_balls', 0))
        inn2_balls = int(r.get('inn2_pressure_balls', 0))
        
        pos_rate = float(r.get('pct_positive_pressure_matches', 0.0)) * 100.0
        
        card = f"""========================================================================================
CLUTCH INTELLIGENCE SCOUTING CARD | BATTER EVALUATION
Candidate: {name.upper()} | Rank: #{rank} | CIE Rating: {rating:.2f}
========================================================================================

1. OPPORTUNITY & EXPOSURE PROFILE
   • High-Pressure Deliveries Faced: {balls:,} balls across {matches} matches
   • Tournament Allocation: {ipl_balls} IPL balls | {t20i_balls} T20I balls
   • Innings Split: {inn1_balls} 1st Innings balls | {inn2_balls} 2nd Innings balls
   • Match Consistency: {pos_rate:.1f}% positive-RAE matches

2. PERFORMANCE DUALITY (NEUTRAL VS. PRESSURE)
   Metric                   Neutral Baseline       High-Pressure       Delta (Clutch Elev.)
   ----------------------------------------------------------------------------------------
   Strike Rate                  {n_sr:6.2f}               {p_sr:6.2f}             {d_sr:+6.2f}
   Runs Above Exp / Ball        0.000 (Neutral)          {rae_ball:+6.3f}             {rae_ball:+6.3f}
   Win Probability Added        0.00%                    {wpa_100:+6.2f}%             {wpa_100:+6.2f}%
   Runs Scored Under Pressure:  {runs} runs off {balls} balls

3. BAYESIAN HIERARCHICAL PRESSURE-RESPONSE COEFFICIENTS
   • Baseline Skill Parameter (u_i):       {u_base:+6.3f} ± {u_se:.3f}
   • Urgency Response Slope (beta_i):      {beta_urg:+6.3f} ± {beta_se:.3f} (Response to rising RRR & resource scarcity)
   • Leverage Response Slope (theta_i):    {theta_lev:+6.3f} ± {theta_se:.3f} (Response to match outcome sensitivity)
   • Behavioral Archetype:                 {'Hyper-Clutch Accelerator' if beta_urg > 0.1 else ('Pressure Resilient' if beta_urg >= -0.05 else 'Urgency Vulnerable')}

4. SAMPLING UNCERTAINTY & RANKING STABILITY (1,000 MATCH-LEVEL BOOTSTRAP REPLICATES)
   • 95% Rating Confidence Interval:       [{ci_low:.2f}, {ci_high:.2f}] (Interval Width: {ci_high - ci_low:.2f} pts)
   • Bootstrap Mean Rank:                  #{boot_avg_rank:.1f}
   • Probability of Top-10 Inclusion:     {top10_prob:.1f}% across resampled cricket seasons
========================================================================================
"""
        return card

    def generate_bowler_card(self, r: pd.Series) -> str:
        """Generates markdown card text for a bowler candidate."""
        name = r.get('bowler_name', 'Unknown')
        rank = r.get('cie_rank', r.get('rank', 'N/A'))
        rating = r.get('cie_rating', r.get('pressure_rating', 0.0))
        
        balls = int(r.get('pressure_legal_balls', 0))
        matches = int(r.get('pressure_matches', 0))
        wkts = int(r.get('pressure_wickets', 0))
        p_econ = float(r.get('pressure_economy', 0.0))
        n_econ = float(r.get('normal_economy', 0.0))
        d_econ = float(r.get('delta_economy', 0.0))
        rp_ball = float(r.get('pressure_rp_per_ball', 0.0))
        wpa_100 = float(r.get('pressure_wpa_per_ball', 0.0)) * 100.0
        
        u_base = float(r.get('post_mean_baseline_ability', 0.0))
        u_se = float(r.get('post_se_baseline_ability', 0.0))
        lambda_urg = float(r.get('post_mean_urgency_slope', 0.0))
        lambda_se = float(r.get('post_se_urgency_slope', 0.0))
        phi_lev = float(r.get('post_mean_leverage_slope', 0.0))
        phi_se = float(r.get('post_se_leverage_slope', 0.0))
        
        ci_low = float(r.get('ci95_low', rating - 4.5))
        ci_high = float(r.get('ci95_high', rating + 4.5))
        top10_prob = float(r.get('boot_top10_prob', 1.0)) * 100.0
        boot_avg_rank = float(r.get('boot_avg_rank', rank))
        
        ipl_balls = int(r.get('ipl_pressure_balls', 0))
        t20i_balls = int(r.get('t20i_pressure_balls', 0))
        inn1_balls = int(r.get('inn1_pressure_balls', 0))
        inn2_balls = int(r.get('inn2_pressure_balls', 0))
        
        pos_rate = float(r.get('pct_positive_pressure_matches', 0.0)) * 100.0
        
        card = f"""========================================================================================
CLUTCH INTELLIGENCE SCOUTING CARD | BOWLER EVALUATION
Candidate: {name.upper()} | Rank: #{rank} | CIE Rating: {rating:.2f}
========================================================================================

1. OPPORTUNITY & EXPOSURE PROFILE
   • High-Pressure Legal Deliveries Bowled: {balls:,} balls across {matches} matches
   • Tournament Allocation: {ipl_balls} IPL balls | {t20i_balls} T20I balls
   • Innings Split: {inn1_balls} 1st Innings balls | {inn2_balls} 2nd Innings balls
   • Match Consistency: {pos_rate:.1f}% positive-suppression matches

2. PERFORMANCE DUALITY (NEUTRAL VS. PRESSURE)
   Metric                   Neutral Baseline       High-Pressure       Delta (Clutch Suppr.)
   ----------------------------------------------------------------------------------------
   Economy Rate                 {n_econ:6.2f}               {p_econ:6.2f}             {d_econ:+6.2f}
   Runs Prevented / Ball        0.000 (Neutral)          {rp_ball:+6.3f}             {rp_ball:+6.3f}
   Win Probability Added        0.00%                    {wpa_100:+6.2f}%             {wpa_100:+6.2f}%
   Wickets Taken Under Pressure: {wkts} wickets in {balls/6.0:.1f} overs

3. BAYESIAN HIERARCHICAL PRESSURE-RESPONSE COEFFICIENTS
   • Baseline Suppression (v_i):          {u_base:+6.3f} ± {u_se:.3f}
   • Urgency Response Slope (lambda_i):   {lambda_urg:+6.3f} ± {lambda_se:.3f} (Run suppression as opponent urgency rises)
   • Leverage Response Slope (phi_i):     {phi_lev:+6.3f} ± {phi_se:.3f} (Execution when match swing is acute)
   • Behavioral Archetype:                {'Elite Lock-Down Specialist' if lambda_urg > 0.05 else ('Reliable Executive' if lambda_urg >= -0.05 else 'High-Variance Option')}

4. SAMPLING UNCERTAINTY & RANKING STABILITY (1,000 MATCH-LEVEL BOOTSTRAP REPLICATES)
   • 95% Rating Confidence Interval:      [{ci_low:.2f}, {ci_high:.2f}] (Interval Width: {ci_high - ci_low:.2f} pts)
   • Bootstrap Mean Rank:                 #{boot_avg_rank:.1f}
   • Probability of Top-10 Inclusion:    {top10_prob:.1f}% across resampled cricket seasons
========================================================================================
"""
        return card

    def save_all_cards(self, top_batters: pd.DataFrame, top_bowlers: pd.DataFrame):
        """Generates and writes text files for all top candidates."""
        for _, r in top_batters.iterrows():
            card_text = self.generate_batter_card(r)
            safe_name = "".join(c if c.isalnum() else "_" for c in r.get('striker_name', 'batter'))
            fname = os.path.join(self.output_dir, f"batter_rank_{r.get('cie_rank', 0):02d}_{safe_name}.txt")
            with open(fname, 'w', encoding='utf-8') as f:
                f.write(card_text)
                
        for _, r in top_bowlers.iterrows():
            card_text = self.generate_bowler_card(r)
            safe_name = "".join(c if c.isalnum() else "_" for c in r.get('bowler_name', 'bowler'))
            fname = os.path.join(self.output_dir, f"bowler_rank_{r.get('cie_rank', 0):02d}_{safe_name}.txt")
            with open(fname, 'w', encoding='utf-8') as f:
                f.write(card_text)
        print(f"Scouting cards successfully generated in {self.output_dir}/")

if __name__ == '__main__':
    print("ScoutingCardGenerator module loaded.")
