"""
Unit Tests for Bayesian Shrinkage and Player Ratings.
"""
import unittest
import numpy as np
import pandas as pd
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))
from reliability import bayesian_shrinkage
from ranking import rank_batters

class TestPlayerRatings(unittest.TestCase):
    def test_bayesian_shrinkage(self):
        # Player with 10 balls vs player with 200 balls
        obs = np.array([2.0, 2.0]) # high performance
        n = np.array([10.0, 200.0]) # sample size
        k = 40.0
        baseline = 0.0
        
        shrunk = bayesian_shrinkage(obs, n, k, baseline)
        
        # Player with small sample (10) should be pulled much closer to 0 than player with 200 balls
        self.assertLess(shrunk[0], shrunk[1])
        self.assertAlmostEqual(shrunk[0], (10 / 50) * 2.0, places=4)
        self.assertAlmostEqual(shrunk[1], (200 / 240) * 2.0, places=4)

    def test_no_duplicate_players_in_ranking(self):
        top_bat = pd.read_csv('outputs/final_rankings/top_10_batters.csv')
        self.assertEqual(len(top_bat), 10)
        self.assertEqual(top_bat['striker_id'].nunique(), 10)
        
        top_bowl = pd.read_csv('outputs/final_rankings/top_10_bowlers.csv')
        self.assertEqual(len(top_bowl), 10)
        self.assertEqual(top_bowl['bowler_id'].nunique(), 10)

if __name__ == '__main__':
    unittest.main()
