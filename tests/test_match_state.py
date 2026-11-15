"""
Unit Tests for Match State Reconstruction.
"""
import unittest
import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))
from match_state import reconstruct_match_state

class TestMatchState(unittest.TestCase):
    def setUp(self):
        # Create minimal synthetic match
        self.deliveries = pd.DataFrame({
            'match_id': [1, 1, 1, 1, 1, 1, 1],
            'innings': [1, 1, 1, 1, 1, 1, 1],
            'overid': [1, 1, 1, 1, 1, 1, 1],
            'over_ball_num': [1, 2, 3, 4, 5, 6, 7],
            'innings_ball_num': [1, 2, 3, 4, 5, 6, 7],
            'batting_team_id': [10, 10, 10, 10, 10, 10, 10],
            'bowling_team_id': [20, 20, 20, 20, 20, 20, 20],
            'striker_id': [101, 101, 101, 101, 101, 101, 101],
            'striker_name': ['Batter A'] * 7,
            'non_striker_id': [102] * 7,
            'non_striker_name': ['Batter B'] * 7,
            'bowler_id': [201] * 7,
            'bowler_name': ['Bowler A'] * 7,
            'batting_type': ['RHB'] * 7,
            'bowling_type': ['Right-arm fast'] * 7,
            'batting_order': [1] * 7,
            'runs': [0, 4, 0, 0, 6, 1, 0],
            'is_four': [False, True, False, False, False, False, False],
            'is_six': [False, False, False, False, True, False, False],
            'is_wicket': [False, False, False, False, False, False, True],
            'dismissal_type_id': [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 1.0],
            'dismissal_type': [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 'Bowled'],
            'dismissed_player_id': [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 101.0],
            'extras_type': [np.nan, np.nan, 'wide', np.nan, np.nan, np.nan, np.nan],
            'extras1_runs': [0, 0, 1, 0, 0, 0, 0],
            'extras_2_runs': [0, 0, 0, 0, 0, 0, 0],
            'pace_or_spin': ['Pace'] * 7,
            'bowl_speed': [140] * 7,
            'stroke': ['Defensive'] * 7,
            'delivery_style': ['Outswing'] * 7,
            'over_or_around': ['Over'] * 7,
            'on_or_off': ['Off-side'] * 7,
            'delivery_ist_time': ['2024-01-01 19:30:00 UTC'] * 7
        })
        
        self.matches = pd.DataFrame([{
            'match_id': 1, 'comp_id': 100, 'match_number': 1, 'match_date': '2024-01-01',
            'stage': 'League', 'venue_id': 1, 'venue_country': 'India',
            'home_team_id': 10, 'home_team': 'Team A', 'away_team_id': 20, 'away_team': 'Team B',
            'home_team_captain_id': 101, 'away_team_captain_id': 201, 'toss_win_team_id': 10,
            'toss_opted': 'Batting', 'man_of_the_match': 101,
            'first_inn_revised_overs': np.nan, 'second_inn_revised_overs': np.nan,
            'revised_target': np.nan, 'knock_out': 0, 'win_team_id': 10, 'result': 'Team A Won'
        }])
        
        self.comps = pd.DataFrame([{
            'comp_id': 100, 'comp_name': 'IPL 2024', 'match_format': 'T20', 'season': 2024
        }])

    def test_cumulative_score_and_legal_balls(self):
        res = reconstruct_match_state(self.deliveries, self.matches, self.comps)
        
        # Delivery 3 is a wide, so legal balls shouldn't increase on ball 3
        # Ball 1: 0 runs -> score 0
        # Ball 2: 4 runs -> score 4
        # Ball 3: wide (1 run) -> score 5
        # Ball 4: 0 runs -> score 5
        # Ball 5: 6 runs -> score 11
        # Ball 6: 1 run -> score 12
        # Ball 7: 0 runs (wicket) -> score 12
        self.assertEqual(res.loc[0, 'pre_current_score'], 0)
        self.assertEqual(res.loc[1, 'pre_current_score'], 0)
        self.assertEqual(res.loc[2, 'pre_current_score'], 4)
        self.assertEqual(res.loc[3, 'pre_current_score'], 5)
        self.assertEqual(res.loc[6, 'post_current_score'], 12)
        
        # Check legal balls: ball 3 is wide, so legal balls completed before ball 4 is 2 (balls 1 and 2)
        self.assertEqual(res.loc[2, 'is_legal'], False)
        self.assertEqual(res.loc[3, 'pre_legal_balls_completed'], 2)
        self.assertEqual(res.loc[6, 'post_legal_balls_completed'], 6)
        
        # Check wicket attribution
        self.assertEqual(res.loc[6, 'is_bowler_wicket'], True)
        self.assertEqual(res.loc[6, 'post_wickets_lost'], 1)

if __name__ == '__main__':
    unittest.main()
