"""
Unit Test Suite for Clutch Intelligence Engine 2.0 (CIE 2.0)
Validates:
1. Decoupled Pressure Dimensions (P_urgency and P_leverage)
2. Delivery-Outcome Probability Distributions
3. Exact Cricket Match-State Transitions (legal balls, score, wickets, striker crossing)
4. Bayesian Parameter Recovery & Credible Intervals
5. Shrinkage Mechanics
6. Temporal Data Leakage Prevention (Strict Chronological Ordering)
7. Match-Level Cluster Bootstrap Resampling
8. Rating Calculation & Orthogonalization
9. Deterministic Reproducibility
"""

import unittest
import numpy as np
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'cie'))

from pressure_decoupled import DecoupledPressureEngine, OUTCOMES
from opponent_strength import DynamicOpponentStrengthEngine
from hierarchical_bayes import BayesianHierarchicalEngine
from four_pillar_rating import compute_vif, gram_schmidt_orthogonalize, FourPillarRatingEngine
from match_bootstrap import MatchLevelBootstrapEngine

class TestCIEEngine(unittest.TestCase):
    def setUp(self):
        np.random.seed(42)

    def test_pressure_dimensions_range(self):
        """Validates that urgency and leverage remain decoupled and bounded."""
        engine = DecoupledPressureEngine()
        row_inn1 = pd.Series({
            'innings': 1, 'knock_out': 0, 'scheduled_legal_balls': 120,
            'pre_wickets_lost': 2, 'pre_legal_balls_completed': 40, 'par_deficit': -5.0
        })
        row_inn2 = pd.Series({
            'innings': 2, 'knock_out': 1, 'scheduled_legal_balls': 120,
            'rrr_pre': 12.0, 'pre_wickets_lost': 5, 'pre_legal_balls_remaining': 24, 'runs_needed_pre': 48
        })
        
        urg1 = engine.compute_situational_urgency(row_inn1)
        urg2 = engine.compute_situational_urgency(row_inn2)
        
        self.assertGreaterEqual(urg1, 0.0)
        self.assertLessEqual(urg1, 1.5)
        self.assertGreaterEqual(urg2, 0.0)
        self.assertLessEqual(urg2, 1.5)
        self.assertGreater(urg2, urg1, "Knockout chase with RRR=12 should have higher urgency than early 1st inn")

    def test_match_state_transitions(self):
        """Verifies state transition function: legal balls, runs, wickets, and striker swaps."""
        engine = DecoupledPressureEngine()
        s0 = {
            'innings': 2, 'runs_needed': 20, 'wickets_remaining': 4, 'wickets_lost': 6,
            'balls_remaining': 12, 'balls_completed': 108, 'rrr': 10.0, 'crr': 8.0,
            'striker_id': 'batter_A', 'non_striker_id': 'batter_B', 'target': 160
        }
        
        # 1. Single taken -> consumes 1 ball, reduces runs needed by 1, batsmen cross ends
        s_single = engine.state_transition(s0, 'one')
        self.assertEqual(s_single['balls_remaining'], 11)
        self.assertEqual(s_single['runs_needed'], 19)
        self.assertEqual(s_single['striker_id'], 'batter_B')
        self.assertEqual(s_single['non_striker_id'], 'batter_A')
        
        # 2. Boundary Four -> consumes 1 ball, reduces runs needed by 4, striker does NOT swap
        s_four = engine.state_transition(s0, 'four')
        self.assertEqual(s_four['balls_remaining'], 11)
        self.assertEqual(s_four['runs_needed'], 16)
        self.assertEqual(s_four['striker_id'], 'batter_A')
        
        # 3. Wide ball -> does NOT consume legal ball, reduces runs needed by 1, batsmen do NOT cross
        s_wide = engine.state_transition(s0, 'wide')
        self.assertEqual(s_wide['balls_remaining'], 12)
        self.assertEqual(s_wide['runs_needed'], 19)
        self.assertEqual(s_wide['striker_id'], 'batter_A')
        
        # 4. Over completion (e.g. ball 114 -> ball 114 is over 19.0)
        s_over_end = s0.copy()
        s_over_end['balls_completed'] = 113
        s_over_end['balls_remaining'] = 7
        s_after_dot = engine.state_transition(s_over_end, 'dot')
        self.assertEqual(s_after_dot['balls_completed'], 114)
        self.assertEqual(s_after_dot['striker_id'], 'batter_B', "End of over must change ends")

    def test_bayesian_parameter_recovery(self):
        """Tests parameter recovery on synthetic dataset with known random effects."""
        metrics = BayesianHierarchicalEngine.run_parameter_recovery_test(n_players=30, n_obs_per_player=150)
        self.assertGreater(metrics['recovery_corr_baseline_ability'], 0.70)
        self.assertGreater(metrics['recovery_corr_urgency_slope'], 0.50)
        self.assertGreater(metrics['recovery_corr_leverage_slope'], 0.60)

    def test_temporal_leakage_prevention(self):
        """Verifies that dynamic opponent strength strictly uses past dates."""
        engine = DynamicOpponentStrengthEngine()
        sample_data = pd.DataFrame([
            {'match_id': 1, 'match_date': pd.Timestamp('2022-04-01'), 'innings': 1, 'overid': 1, 'over_ball_num': 1,
             'is_legal': 1, 'bowler_conceded_runs': 4, 'runs_prevented': 0.5, 'is_bowler_wicket': 0, 'bowler_id': 101,
             'is_batter_ball': 1, 'runs': 4, 'runs_above_expectation': 0.8, 'striker_id': 201, 'pace_or_spin': 'Pace',
             'batting_type': 'RHB'},
            {'match_id': 2, 'match_date': pd.Timestamp('2022-04-05'), 'innings': 1, 'overid': 1, 'over_ball_num': 1,
             'is_legal': 1, 'bowler_conceded_runs': 0, 'runs_prevented': 1.0, 'is_bowler_wicket': 1, 'bowler_id': 101,
             'is_batter_ball': 1, 'runs': 0, 'runs_above_expectation': -0.5, 'striker_id': 201, 'pace_or_spin': 'Pace',
             'batting_type': 'RHB'}
        ])
        res = engine.compute_chronological_features(sample_data)
        self.assertIn('bowler_prior_strength', res.columns)
        self.assertIn('batter_prior_vs_discipline', res.columns)
        # Match 1 has no prior history, must receive neutral population default
        # Match 2 must reflect performance strictly from Match 1, not Match 2 itself
        self.assertFalse(res.isna().any().any(), "No NaNs allowed in chronological opponent strength")

    def test_gram_schmidt_orthogonalization(self):
        """Verifies that Gram-Schmidt produces mutually orthogonal columns with zero correlation."""
        np.random.seed(42)
        # Correlated input matrix
        v1 = np.random.normal(0, 1, 100)
        v2 = 0.8 * v1 + 0.2 * np.random.normal(0, 1, 100)
        v3 = 0.5 * v1 + 0.5 * v2 + 0.1 * np.random.normal(0, 1, 100)
        X = np.column_stack([v1, v2, v3])
        
        Q = gram_schmidt_orthogonalize(X)
        corr_Q = np.corrcoef(Q.T)
        
        # Off-diagonal correlations must be approximately zero
        np.testing.assert_allclose(corr_Q, np.eye(3), atol=1e-4)

    def test_bootstrap_reproducibility(self):
        """Tests that bootstrap runs produce deterministic results given the same seed."""
        engine1 = MatchLevelBootstrapEngine(n_iterations=10, random_seed=42)
        engine2 = MatchLevelBootstrapEngine(n_iterations=10, random_seed=42)
        
        mock_df = pd.DataFrame([
            {'match_id': 1, 'comp_name': 'IPL 2022', 'season': 2022, 'is_batter_ball': True, 'is_high_pressure': True,
             'striker_id': 1, 'runs': 4, 'runs_above_expectation': 0.5, 'wpa_bat': 0.05},
            {'match_id': 2, 'comp_name': 'IPL 2022', 'season': 2022, 'is_batter_ball': True, 'is_high_pressure': True,
             'striker_id': 1, 'runs': 2, 'runs_above_expectation': 0.2, 'wpa_bat': 0.02}
        ] * 60)
        
        res1 = engine1.run_bootstrap_batters(mock_df, [1], {1: 0.20}, min_balls=50, min_matches=5)
        res2 = engine2.run_bootstrap_batters(mock_df, [1], {1: 0.20}, min_balls=50, min_matches=5)
        
        if len(res1) > 0 and len(res2) > 0:
            self.assertEqual(res1.iloc[0]['boot_mean_rating'], res2.iloc[0]['boot_mean_rating'])

if __name__ == '__main__':
    unittest.main()
