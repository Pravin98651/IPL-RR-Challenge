"""
Data Integration Module.
Enriches ball-by-ball deliveries with match, competition, and team context.
"""
import pandas as pd
from typing import Dict, Optional

def integrate_match_context(bbb: pd.DataFrame, matches: pd.DataFrame, comps: pd.DataFrame) -> pd.DataFrame:
    # Select key match metadata
    match_cols = [
        'match_id', 'comp_id', 'match_number', 'match_date', 'stage',
        'venue_id', 'venue_country', 'home_team_id', 'home_team',
        'away_team_id', 'away_team', 'toss_win_team_id', 'toss_opted',
        'first_inn_revised_overs', 'second_inn_revised_overs',
        'revised_target', 'knock_out', 'win_team_id', 'result'
    ]
    m_sub = matches[match_cols].copy()
    
    # Merge competition details
    comp_cols = ['comp_id', 'comp_name', 'match_format', 'season']
    c_sub = comps[comp_cols].copy()
    m_enriched = m_sub.merge(c_sub, on='comp_id', how='left')
    
    # Merge with deliveries
    merged = bbb.merge(m_enriched, on='match_id', how='left')
    return merged

if __name__ == '__main__':
    from data_loader import load_ball_by_ball, load_matches, load_competitions
    bbb = load_ball_by_ball(nrows=1000)
    matches = load_matches()
    comps = load_competitions()
    enriched = integrate_match_context(bbb, matches, comps)
    print("Enriched sample shape:", enriched.shape)
    print("Columns:", enriched.columns.tolist())
