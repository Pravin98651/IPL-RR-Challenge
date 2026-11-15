# Unique Values and Cardinality Report

## Key Identifiers and Cardinalities

| Entity | Identifier Column | Source Table | Unique Count | Range / Min-Max |
| :--- | :--- | :--- | :--- | :--- |
| Matches | `match_id` | matches.csv | 883 | 13511 to 55561 |
| Matches with Deliveries | `match_id` | ball_by_ball.csv | 867 | 13511 to 55561 |
| Competitions | `comp_id` | competitions.csv | 141 | 1331 to 3787 |
| Teams | `team_id` | teams.csv | 38 | 1 to 4444 |
| Players (Roster) | `player_id` | mapping.csv | 1,217 | 8 to 71727 |
| Batters Active | `striker_id` | ball_by_ball.csv | 888 | 8 to 71727 |
| Bowlers Active | `bowler_id` | ball_by_ball.csv | 647 | 23 to 71727 |
| Venues | `venue_id` | matches.csv | 98 | 1 to 3692 |

## Categorical Distributions

### Match Formats
| match_format   |   count |
|:---------------|--------:|
| T20I           |     134 |
| T20            |       7 |

### Match Stages
| stage      |   count |
|:-----------|--------:|
| League     |     620 |
| Others     |     226 |
| Final      |      12 |
| Qualifier  |      10 |
| Super 4    |       6 |
| Eliminator |       5 |
| Semi Final |       4 |

### Knockout vs League Matches
| knock_out          |   count |
|:-------------------|--------:|
| League/Group Stage |     852 |
| Knockout/Playoff   |      31 |

### Toss Decision
| toss_opted   |   count |
|:-------------|--------:|
| Fielding     |     639 |
| Batting      |     229 |
| nan          |      15 |

### Ball Extras Type Distribution
| extras_type   |   count |
|:--------------|--------:|
| nan           |  189167 |
| wide          |    7714 |
| legbyes       |    2748 |
| Overstep      |     576 |
| byes          |     529 |
| other         |     264 |
| Penalty       |       1 |

### Dismissal Types Breakdown
| dismissal_type        |   count |
|:----------------------|--------:|
| nan                   |  190118 |
| Caught                |    7557 |
| Bowled                |    1775 |
| LBW                   |     709 |
| RunOut                |     600 |
| Stump                 |     214 |
| Hit Wicket            |      17 |
| Retire Out            |       6 |
| Obstracting the field |       2 |
| Obstructing the field |       1 |

### Bowling Styles (Pace vs Spin)
| pace_or_spin   |   count |
|:---------------|--------:|
| Pace           |  123886 |
| Spin           |   77113 |

### Batting Hand Stance
| batting_type   |   count |
|:---------------|--------:|
| RHB            |  131006 |
| LHB            |   69993 |