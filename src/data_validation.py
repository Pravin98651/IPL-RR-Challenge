"""
Data Validation Module for Cricket Analytics.
Validates structural integrity, domain constraints, and foreign key relations.
"""
import pandas as pd
from typing import Dict, Any, List

def validate_deliveries(bbb: pd.DataFrame) -> Dict[str, Any]:
    issues: List[str] = []
    
    # Check invalid runs
    invalid_runs = bbb[~bbb['runs'].isin([0, 1, 2, 3, 4, 5, 6, 7])]
    if len(invalid_runs) > 0:
        issues.append(f"Found {len(invalid_runs)} deliveries with non-standard batter runs.")
        
    # Check legal balls
    illegal_types = ['wide', 'Overstep', 'other']
    illegal_mask = bbb['extras_type'].isin(illegal_types)
    legal_count = (~illegal_mask).sum()
    illegal_count = illegal_mask.sum()
    
    # Check bowler wickets
    bowler_dismissals = ['Caught', 'Bowled', 'LBW', 'Stump', 'Hit Wicket']
    bowler_wkts = (bbb['is_wicket'] & bbb['dismissal_type'].isin(bowler_dismissals)).sum()
    non_bowler_wkts = (bbb['is_wicket'] & ~bbb['dismissal_type'].isin(bowler_dismissals)).sum()
    
    return {
        'total_deliveries': len(bbb),
        'legal_deliveries': int(legal_count),
        'illegal_deliveries': int(illegal_count),
        'total_wickets': int(bbb['is_wicket'].sum()),
        'bowler_credited_wickets': int(bowler_wkts),
        'fielding_or_other_wickets': int(non_bowler_wkts),
        'issues': issues
    }

def validate_relationships(data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    bbb = data['ball_by_ball']
    matches = data['matches']
    comps = data['competitions']
    mapping = data['mapping']
    
    orphan_matches = set(bbb['match_id']) - set(matches['match_id'])
    orphan_comps = set(matches['comp_id']) - set(comps['comp_id'])
    orphan_players = (set(bbb['striker_id']) | set(bbb['bowler_id'])) - set(mapping['player_id'])
    
    return {
        'orphan_match_count': len(orphan_matches),
        'orphan_comp_count': len(orphan_comps),
        'orphan_player_count': len(orphan_players),
        'is_fully_consistent': (len(orphan_matches) == 0 and len(orphan_comps) == 0 and len(orphan_players) == 0)
    }

if __name__ == '__main__':
    from data_loader import load_all_datasets
    data = load_all_datasets()
    deliv_check = validate_deliveries(data['ball_by_ball'])
    rel_check = validate_relationships(data)
    print("Deliveries Validation:", deliv_check)
    print("Relationships Validation:", rel_check)
