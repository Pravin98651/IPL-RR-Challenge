# Dataset Schema and Structure Report

## 1. Executive Summary
The dataset comprises six relational CSV files capturing ball-by-ball T20 and T20I matches from 2022 to 2026.

| Table Name | File Name | Rows | Columns | Memory Usage (MB) | Candidate Primary Key |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `ball_by_ball` | `ball_by_ball.csv` | 200,999 | 33 | 165.28 MB | `match_id + innings + innings_ball_num` |
| `matches` | `matches.csv` | 883 | 22 | 0.46 MB | `match_id` |
| `competitions` | `competitions.csv` | 141 | 4 | 0.03 MB | `comp_id` |
| `competition_team_player_mapping` | `competition_team_player_mapping.csv` | 6,413 | 6 | 1.39 MB | `comp_id + team_id + player_id` |
| `playing_eleven` | `playing_eleven.csv` | 28,381 | 9 | 3.21 MB | `match_id + team_id + player_id` |
| `teams` | `teams.csv` | 353 | 3 | 0.03 MB | `comp_id + team_id` |

## 2. Table-by-Table Detailed Schema

### `ball_by_ball`
- **Total Rows**: 200,999
- **Total Columns**: 33
- **Candidate Primary Key**: `match_id + innings + innings_ball_num`

| Column | Data Type | Non-Null Count | Null Count | Unique Values | Sample Value |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `match_id` | int64 | 200,999 | 0 | 867 | 13511 |
| `innings` | int64 | 200,999 | 0 | 4 | 1 |
| `overid` | int64 | 200,999 | 0 | 20 | 1 |
| `over_ball_num` | int64 | 200,999 | 0 | 13 | 1 |
| `innings_ball_num` | int64 | 200,999 | 0 | 136 | 1 |
| `batting_team_id` | int64 | 200,999 | 0 | 38 | 22 |
| `bowling_team_id` | int64 | 200,999 | 0 | 38 | 28 |
| `striker_id` | int64 | 200,999 | 0 | 888 | 1187 |
| `striker_name` | object | 200,999 | 0 | 885 | Jason Roy |
| `non_striker_id` | int64 | 200,999 | 0 | 867 | 6273 |
| `non_striker_name` | object | 200,999 | 0 | 864 | Tom Banton |
| `bowler_id` | int64 | 200,999 | 0 | 647 | 1772 |
| `bowler_name` | object | 200,999 | 0 | 646 | Sheldon Cottrell |
| `batting_type` | object | 200,999 | 0 | 2 | RHB |
| `bowling_type` | object | 200,999 | 0 | 12 | Left-arm fast-medium |
| `batting_order` | int64 | 200,999 | 0 | 13 | 1 |
| `runs` | int64 | 200,999 | 0 | 7 | 0 |
| `is_four` | bool | 200,999 | 0 | 2 | False |
| `is_six` | bool | 200,999 | 0 | 2 | False |
| `is_wicket` | bool | 200,999 | 0 | 2 | False |
| `dismissal_type_id` | float64 | 10,881 | 190,118 | 8 | 1.0 |
| `dismissal_type` | object | 10,881 | 190,118 | 9 | Bowled |
| `dismissed_player_id` | float64 | 10,892 | 190,107 | 814 | 1187.0 |
| `extras_type` | object | 11,832 | 189,167 | 6 | wide |
| `extras1_runs` | int64 | 200,999 | 0 | 6 | 0 |
| `extras_2_runs` | int64 | 200,999 | 0 | 3 | 0 |
| `pace_or_spin` | object | 200,999 | 0 | 2 | Pace |
| `bowl_speed` | float64 | 200,999 | 0 | 1,033 | 0.0 |
| `stroke` | object | 194,841 | 6,158 | 30 | Cover Drive |
| `delivery_style` | object | 200,608 | 391 | 34 | Inswing |
| `over_or_around` | object | 200,592 | 407 | 2 | Over |
| `on_or_off` | object | 200,999 | 0 | 2 | Off-side |
| `delivery_ist_time` | object | 200,999 | 0 | 200,826 | 2022-01-23 00:00:00 UTC |

### `matches`
- **Total Rows**: 883
- **Total Columns**: 22
- **Candidate Primary Key**: `match_id`

| Column | Data Type | Non-Null Count | Null Count | Unique Values | Sample Value |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `match_id` | int64 | 883 | 0 | 883 | 13511 |
| `comp_id` | int64 | 883 | 0 | 138 | 1331 |
| `match_number` | int64 | 883 | 0 | 75 | 1 |
| `match_date` | object | 883 | 0 | 686 | 2022-01-22 |
| `stage` | object | 883 | 0 | 7 | League |
| `venue_id` | int64 | 883 | 0 | 98 | 54 |
| `venue_country` | object | 883 | 0 | 17 | West Indies |
| `home_team_id` | int64 | 883 | 0 | 36 | 28 |
| `home_team` | object | 883 | 0 | 36 | West Indies |
| `away_team_id` | int64 | 883 | 0 | 36 | 22 |
| `away_team` | object | 883 | 0 | 36 | England |
| `home_team_captain_id` | float64 | 839 | 44 | 89 | 494.0 |
| `away_team_captain_id` | float64 | 838 | 45 | 98 | 478.0 |
| `toss_win_team_id` | float64 | 868 | 15 | 37 | 28.0 |
| `toss_opted` | object | 868 | 15 | 2 | Fielding |
| `man_of_the_match` | int64 | 883 | 0 | 293 | 0 |
| `first_inn_revised_overs` | float64 | 25 | 858 | 13 | 114.0 |
| `second_inn_revised_overs` | float64 | 25 | 858 | 12 | 114.0 |
| `revised_target` | float64 | 23 | 860 | 23 | 143.0 |
| `knock_out` | int64 | 883 | 0 | 2 | 0 |
| `win_team_id` | float64 | 842 | 41 | 36 | 28.0 |
| `result` | object | 883 | 0 | 670 | West Indies Won by 9 Wickets |

### `competitions`
- **Total Rows**: 141
- **Total Columns**: 4
- **Candidate Primary Key**: `comp_id`

| Column | Data Type | Non-Null Count | Null Count | Unique Values | Sample Value |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `comp_id` | int64 | 141 | 0 | 141 | 3395 |
| `comp_name` | object | 141 | 0 | 141 | South Africa in New Zealand T20I Series 2026 |
| `match_format` | object | 141 | 0 | 2 | T20I |
| `season` | object | 141 | 0 | 8 | 2026 |

### `competition_team_player_mapping`
- **Total Rows**: 6,413
- **Total Columns**: 6
- **Candidate Primary Key**: `comp_id + team_id + player_id`

| Column | Data Type | Non-Null Count | Null Count | Unique Values | Sample Value |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `comp_id` | int64 | 6,413 | 0 | 140 | 1331 |
| `comp_name` | object | 6,413 | 0 | 140 | England in West Indies T20I Series 2022 |
| `team_id` | int64 | 6,413 | 0 | 38 | 22 |
| `team_name` | object | 6,413 | 0 | 38 | England |
| `player_id` | int64 | 6,413 | 0 | 1,217 | 478 |
| `player_name` | object | 6,413 | 0 | 1,210 | Eoin Morgan |

### `playing_eleven`
- **Total Rows**: 28,381
- **Total Columns**: 9
- **Candidate Primary Key**: `match_id + team_id + player_id`

| Column | Data Type | Non-Null Count | Null Count | Unique Values | Sample Value |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `match_id` | int64 | 28,381 | 0 | 880 | 13511 |
| `team_id` | int64 | 28,381 | 0 | 38 | 22 |
| `player_id` | int64 | 28,381 | 0 | 1,082 | 1187 |
| `batting_order` | float64 | 19,703 | 8,678 | 13 | 1.0 |
| `is_played` | bool | 28,381 | 0 | 2 | True |
| `is_captain` | object | 19,714 | 8,667 | 2 | False |
| `is_wk` | object | 19,714 | 8,667 | 2 | False |
| `is_impact` | int64 | 28,381 | 0 | 2 | 0 |
| `is_impact_off` | int64 | 28,381 | 0 | 2 | 0 |

### `teams`
- **Total Rows**: 353
- **Total Columns**: 3
- **Candidate Primary Key**: `comp_id + team_id`

| Column | Data Type | Non-Null Count | Null Count | Unique Values | Sample Value |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `comp_id` | int64 | 353 | 0 | 141 | 1331 |
| `team_id` | int64 | 353 | 0 | 38 | 22 |
| `team_name` | object | 353 | 0 | 38 | England |
