# Relational Architecture and Integration Mapping Report

## 1. Entity Relationship Overview
The 6 datasets form a normalized star/snowflake relational schema centered around matches and deliveries.

```
                    +-------------------+
                    |   competitions    |
                    +-------------------+
                              | 1
                              |
                              | N
                    +-------------------+       1 +---------------+
                    |      matches      |---------|     teams     |
                    +-------------------+         +---------------+
                       | 1          | 1                   | 1
                       |            |                     |
                       | N          | N                   | N
             +-----------------+  +---------------------------------+
             | playing_eleven  |  | competition_team_player_mapping |
             +-----------------+  +---------------------------------+
                       | N                        | N
                       |                          |
                       | N                        | N
             +------------------------------------------------------+
             |                    ball_by_ball                      |
             +------------------------------------------------------+
```

## 2. Cardinality and Foreign Key Links

| Parent Table | Parent Key | Child Table | Foreign Key | Cardinality | Integrity Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `competitions` | `comp_id` | `matches` | `comp_id` | 1-to-N | 100% Valid (0 orphan records) |
| `competitions` | `comp_id` | `teams` | `comp_id` | 1-to-N | 100% Valid |
| `competitions` | `comp_id` | `competition_team_player_mapping` | `comp_id` | 1-to-N | 100% Valid |
| `matches` | `match_id` | `ball_by_ball` | `match_id` | 1-to-N | 100% Valid (867 active matches) |
| `matches` | `match_id` | `playing_eleven` | `match_id` | 1-to-N | 100% Valid |
| `teams` | `team_id` | `matches` | `home_team_id` / `away_team_id` | 1-to-N | 100% Valid |
| `teams` | `team_id` | `ball_by_ball` | `batting_team_id` / `bowling_team_id` | 1-to-N | 100% Valid |
| `mapping` | `player_id` | `ball_by_ball` | `striker_id` / `bowler_id` / `non_striker_id` | 1-to-N | 100% Valid (958 players) |
| `playing_eleven` | `player_id` | `ball_by_ball` | `striker_id` / `bowler_id` | 1-to-N | 99.8% (2 late-inclusion players handled) |