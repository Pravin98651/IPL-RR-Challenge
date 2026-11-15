"""
Data Loader Module for SupeRR Selector Cricket Analytics.
Provides robust, reproducible loading of raw datasets.
"""
import os
import pandas as pd
from typing import Dict, Optional

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

def get_data_path(filename: str, custom_dir: Optional[str] = None) -> str:
    directory = custom_dir if custom_dir else DATA_DIR
    path = os.path.join(directory, filename)
    if not os.path.exists(path):
        # Fallback to root directory
        root_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), filename)
        if os.path.exists(root_path):
            return root_path
        raise FileNotFoundError(f"Dataset file '{filename}' not found in {directory} or root.")
    return path

def load_competitions(data_dir: Optional[str] = None) -> pd.DataFrame:
    path = get_data_path('competitions.csv', data_dir)
    df = pd.read_csv(path)
    df['comp_id'] = df['comp_id'].astype(int)
    return df

def load_teams(data_dir: Optional[str] = None) -> pd.DataFrame:
    path = get_data_path('teams.csv', data_dir)
    df = pd.read_csv(path)
    df['comp_id'] = df['comp_id'].astype(int)
    df['team_id'] = df['team_id'].astype(int)
    return df

def load_matches(data_dir: Optional[str] = None) -> pd.DataFrame:
    path = get_data_path('matches.csv', data_dir)
    df = pd.read_csv(path)
    df['match_id'] = df['match_id'].astype(int)
    df['comp_id'] = df['comp_id'].astype(int)
    df['match_date'] = pd.to_datetime(df['match_date'], errors='coerce')
    df['knock_out'] = df['knock_out'].fillna(0).astype(int)
    return df

def load_playing_eleven(data_dir: Optional[str] = None) -> pd.DataFrame:
    path = get_data_path('playing_eleven.csv', data_dir)
    df = pd.read_csv(path)
    df['match_id'] = df['match_id'].astype(int)
    df['team_id'] = df['team_id'].astype(int)
    df['player_id'] = df['player_id'].astype(int)
    return df

def load_competition_team_player_mapping(data_dir: Optional[str] = None) -> pd.DataFrame:
    path = get_data_path('competition_team_player_mapping.csv', data_dir)
    df = pd.read_csv(path)
    df['comp_id'] = df['comp_id'].astype(int)
    df['team_id'] = df['team_id'].astype(int)
    df['player_id'] = df['player_id'].astype(int)
    return df

def load_ball_by_ball(data_dir: Optional[str] = None, nrows: Optional[int] = None) -> pd.DataFrame:
    path = get_data_path('ball_by_ball.csv', data_dir)
    dtypes = {
        'match_id': 'int64',
        'innings': 'int32',
        'overid': 'int32',
        'over_ball_num': 'int32',
        'innings_ball_num': 'int32',
        'batting_team_id': 'int64',
        'bowling_team_id': 'int64',
        'striker_id': 'int64',
        'non_striker_id': 'int64',
        'bowler_id': 'int64',
        'runs': 'int32',
        'is_four': 'bool',
        'is_six': 'bool',
        'is_wicket': 'bool',
        'extras1_runs': 'int32',
        'extras_2_runs': 'int32'
    }
    df = pd.read_csv(path, dtype=dtypes, nrows=nrows)
    return df

def load_all_datasets(data_dir: Optional[str] = None) -> Dict[str, pd.DataFrame]:
    return {
        'competitions': load_competitions(data_dir),
        'teams': load_teams(data_dir),
        'matches': load_matches(data_dir),
        'playing_eleven': load_playing_eleven(data_dir),
        'mapping': load_competition_team_player_mapping(data_dir),
        'ball_by_ball': load_ball_by_ball(data_dir)
    }

if __name__ == '__main__':
    data = load_all_datasets()
    print("All datasets loaded successfully:")
    for k, v in data.items():
        print(f" - {k}: {len(v):,} rows")
