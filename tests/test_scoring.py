"""
Unit Tests for Scoring and Contextual Calculations.
"""
import unittest
import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

class TestScoringCalculations(unittest.TestCase):
    def test_bowler_conceded_runs_rules(self):
        # In cricket: wides & oversteps charged to bowler; byes & legbyes NOT charged
        runs = pd.Series([0, 0, 0, 4])
        extras1 = pd.Series([1, 1, 1, 0])
        extras_type = pd.Series(['wide', 'legbyes', 'Overstep', np.nan])
        
        illegal_types = ['wide', 'Overstep', 'other']
        is_illegal = extras_type.isin(illegal_types)
        bowler_conceded = runs + np.where(is_illegal, extras1, 0)
        
        self.assertEqual(bowler_conceded.iloc[0], 1) # wide charged
        self.assertEqual(bowler_conceded.iloc[1], 0) # legbye not charged
        self.assertEqual(bowler_conceded.iloc[2], 1) # overstep charged
        self.assertEqual(bowler_conceded.iloc[3], 4) # regular boundary charged

    def test_bowler_credited_dismissals(self):
        is_wkt = pd.Series([True, True, True, True, True])
        dismissal = pd.Series(['Caught', 'Bowled', 'RunOut', 'LBW', 'Retire Out'])
        bowler_dismissals = ['Caught', 'Bowled', 'LBW', 'Stump', 'Hit Wicket']
        is_bowler_wkt = is_wkt & dismissal.isin(bowler_dismissals)
        
        self.assertTrue(is_bowler_wkt.iloc[0])
        self.assertTrue(is_bowler_wkt.iloc[1])
        self.assertFalse(is_bowler_wkt.iloc[2]) # RunOut NOT credited
        self.assertTrue(is_bowler_wkt.iloc[3])
        self.assertFalse(is_bowler_wkt.iloc[4]) # Retire Out NOT credited

if __name__ == '__main__':
    unittest.main()
