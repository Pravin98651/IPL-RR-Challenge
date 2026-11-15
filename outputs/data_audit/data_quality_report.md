# Data Quality and Integrity Audit Report (Audited & Reconciled)

## 1. Executive Summary & Match Count Reconciliation

A rigorous reconciliation of match records across `matches.csv`, `competitions.csv`, and `ball_by_ball.csv` resolved previous count discrepancies:

| Category | Rows in `matches.csv` | Active in `ball_by_ball.csv` | Excluded (Abandoned) | Notes / Reconciliation |
| :--- | :---: | :---: | :---: | :--- |
| **IPL Matches** | **371** | **367** | **4** | 5 seasons (2022: 74, 2023: 74, 2024: 71, 2025: 74, 2026: 74). 4 matches abandoned due to rain. |
| **Other T20 Matches** | **30** | **30** | **0** | Emerging Teams Asia Cup 2024 (15), Asia Cup Rising Stars 2025 (15). Format = T20. |
| **Total T20 Matches** | **401** | **397** | **4** | Total matches with match_format == 'T20'. |
| **T20 International (T20I)** | **482** | **470** | **12** | Bilaterals, Tri-series, Asia Cups. 12 matches abandoned without a ball bowled. |
| **Total Matches** | **883** | **867** | **16** | **Exact match count = 867 active matches.** |
| **Knockout Matches** | **31** | **31** | **0** | Finals (12), Qualifiers (10), Eliminators (5), Semi-Finals (4). All 31 completed! |
| **League / Group Matches** | **852** | **836** | **16** | League (613 active), Others (217 active), Super 4 (6 active). |

---

## 2. Summary of Delivery-Level Audit Checks

| Audit Check | Scope | Result | Details | Action / Resolution |
| :--- | :--- | :--- | :--- | :--- |
| **Duplicate Deliveries** | `ball_by_ball.csv` | Passed | 0 duplicate rows across 200,999 records | None required |
| **Match ID Integrity** | `ball_by_ball -> matches` | Passed | All 867 match IDs exist in matches.csv | 16 abandoned matches in matches.csv have 0 balls |
| **Competition FK** | `matches -> competitions` | Passed | All 883 matches have valid comp_id | None required |
| **Team ID Consistency** | `bbb / matches -> teams` | Passed | 38 teams, strict 1-to-1 bijection | None required |
| **Player Roster Coverage** | `bbb -> mapping` | Passed | 100% of 958 players in bbb exist in mapping | Perfect coverage |
| **Playing XI Coverage** | `bbb -> playing_eleven` | Minor Anomaly | 2 players (Syed Haider, Basil Hameed) in 3 matches missing from playing XI | Fallback to mapping.csv names/teams |
| **Wicket vs Dismissal** | `ball_by_ball.csv` | Subtle Anomaly | 12 records have dismissed_player_id with is_wicket=False | Rely strictly on is_wicket=True |
| **Bowler Dismissal Attribution** | `ball_by_ball.csv` | Domain Rule | 609 run-outs and retire-outs present in wickets | Bowlers only credited for Caught, Bowled, LBW, Stumped, Hit Wicket |
| **Legal Delivery Counting** | `ball_by_ball.csv` | Domain Rule | 8,554 illegal balls (7,714 wides, 576 oversteps, 264 other) | Legal balls separated from balls faced and overs bowled |
| **Batter Run Attribution** | `ball_by_ball.csv` | Verified | runs = batter off bat; extras1 + extras2 = extras | Total ball runs = runs + extras1 + extras2 |
| **Bowler Conceded Runs** | `ball_by_ball.csv` | Domain Rule | byes and legbyes must not be charged to bowler | Bowler runs = runs + wides + noballs |
| **DLS / Revised Targets** | `matches.csv` | Documented | 23 rain-affected matches with revised_target | Chase target logic accurately incorporates revised_target |

---

## 3. Delivery Ordering & Over Legality Verification

- Completed overs contain exactly 6 legal deliveries.
- Illegal deliveries (wides, oversteps, other no-balls) correctly increment the over delivery count without advancing the over legal ball counter.
- Batter balls faced correctly counts deliveries where `extras_type != 'wide'`.
- Bowler overs bowled correctly counts `legal_balls / 6.0`.
