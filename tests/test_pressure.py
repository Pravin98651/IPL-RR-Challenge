"""
Unit Tests for Pressure Models and Classification.
"""
import unittest
import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))
from pressure_models import compute_rule_based_pressure, classify_pressure

class TestPressureModels(unittest.TestCase):
    def test_chase_pressure_scaling(self):
        # High RRR and wickets down should yield high pressure
        df = pd.DataFrame({
            'innings': [2, 2],
            'rrr_pre': [6.0, 14.0],
            'pre_wickets_lost': [1, 6],
            'pre_legal_balls_completed': [20, 100],
            'runs_needed_pre': [120, 35],
            'par_deficit': [0, 0],
            'knock_out': [0, 0]
        })
        pi = compute_rule_based_pressure(df)
        self.assertLess(pi.iloc[0], pi.iloc[1])
        self.assertGreater(pi.iloc[1], 0.60)
        
    def test_pressure_classification_tiers(self):
        scores = pd.Series([0.20, 0.45, 0.70, 0.95])
        tiers = classify_pressure(scores)
        self.assertEqual(tiers.iloc[0], 'Low')
        self.assertEqual(tiers.iloc[1], 'Moderate')
        self.assertEqual(tiers.iloc[2], 'High')
        self.assertEqual(tiers.iloc[3], 'Extreme')

if __name__ == '__main__':
    unittest.main()
