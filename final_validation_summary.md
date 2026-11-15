# SupeRR Selector Season 2 — Final Validation Summary

**Generated from**: 14 experiment CSV outputs produced by `src/task_experiments.py`  
**Data scope**: 194,014 official deliveries across 837 IPL + T20I matches (2022–2026)  
**All figures are sourced directly from CSV files — no illustrative or fabricated values**

---

## 0. Cross-Check: CSVs vs Methodology Report vs Unstop Submission

The table below confirms exact agreement between the three artefacts.

### Batters

| Rank | `top_10_batters.csv` (primary submission) | Methodology Report Rank-1 column | Match? |
|:---:|:---|:---|:---:|
| 1 | Heinrich Klaasen, 77.59 | Heinrich Klaasen, 77.59 | ✓ |
| 2 | Ashutosh Sharma, 69.71 | Ashutosh Sharma, 69.71 | ✓ |
| 3 | Shashank Singh, 69.28 | Shashank Singh, 69.28 | ✓ |
| 4 | Shreyas Iyer, 68.22 | Shreyas Iyer, 68.22 | ✓ |
| 5 | Dinesh Karthik, 66.52 | Dinesh Karthik, 66.52 | ✓ |
| 6 | Tim David, 66.48 | Tim David, 66.48 | ✓ |
| 7 | Suryakumar Yadav, 66.32 | Suryakumar Yadav, 66.32 | ✓ |
| 8 | Rashid Khan, 66.23 | Rashid Khan, 66.23 | ✓ |
| 9 | Mahendra Singh Dhoni, 66.05 | Mahendra Singh Dhoni, 66.05 | ✓ |
| 10 | Rovman Powell, 63.11 | Rovman Powell, 63.11 | ✓ |

> Source: `top_10_batters.csv` lines 2–11. Note on Ashutosh Sharma: In the official scope (IPL+T20I), Ashutosh Sharma has exactly 119 pressure balls across 19 pressure matches, with 11 positive matches, yielding an exact positive match rate of 11/19 = 57.9% (vs. 12/20 = 60.0% in the expanded scope which included 1 Emerging Teams Asia Cup match). Both CSV and report are synchronized to 57.9% (11/19).

### Bowlers

| Rank | `top_10_bowlers.csv` | Methodology Report | Match? |
|:---:|:---|:---|:---:|
| 1 | Sunil Narine, 77.83, 130 balls, 18 matches | Sunil Narine, 77.83 | ✓ |
| 2 | Krunal Pandya, 74.73, 130 balls, 15 matches | Krunal Pandya, 74.73 | ✓ |
| 3 | Rashid Khan, 71.52, 183 balls, 27 matches | Rashid Khan, 71.52 | ✓ |
| 4 | Matheesha Pathirana, 69.35, 206 balls, 28 matches | Matheesha Pathirana, 69.35 | ✓ |
| 5 | Mustafizur Rahman, 66.38, 222 balls, 38 matches | Mustafizur Rahman, 66.38 | ✓ |
| 6 | Yuzvendra Chahal, 65.03, 247 balls, 31 matches | Yuzvendra Chahal, 65.03 | ✓ |
| 7 | Maheesh Theekshana, 64.60, 161 balls, 25 matches | Maheesh Theekshana, 64.60 | ✓ |
| 8 | Varun Chakravarthy, 62.46, 199 balls, 25 matches | Varun Chakravarthy, 62.46 | ✓ |
| 9 | Jason Holder, 62.21, 227 balls, 38 matches | Jason Holder, 62.21 | ✓ |
| 10 | Ravichandran Ashwin, 61.61, 128 balls, 16 matches | Ravichandran Ashwin, 61.61 | ✓ |

**Verification**: All 20 ratings are identical to 2 decimal places across the CSV, methodology report, and Unstop dropdown order. No discrepancy found.

---

## 1. Pressure Model Comparison — Numerical Results

**Source**: `pressure_model_comparison.csv` and `pressure_model_synthetic_scenarios.csv`

### 1a. Delivery-Level Statistics by Model and Segment

| Segment | Model | N Deliveries | Mean Score | Std | Min | Max | N High+Extreme | % High+Extreme |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| All official | A — Rule | 194,014 | 0.3225 | 0.2563 | 0.0000 | 1.4830 | 25,339 | 13.06% |
| All official | B — Hybrid 50/50 | 194,014 | 0.3407 | 0.2204 | 0.0000 | 1.3679 | 19,949 | 10.28% |
| All official | C — Alternative | 194,014 | 0.4211 | 0.1633 | 0.0178 | 1.3679 | 23,333 | 12.03% |
| Innings 1 | A — Rule | 102,054 | 0.2382 | 0.1987 | 0.0000 | 0.9400 | 5,674 | 5.56% |
| Innings 1 | B — Hybrid | 102,054 | 0.2382 | 0.1987 | 0.0000 | 0.9400 | 5,674 | 5.56% |
| Innings 1 | C — Alternative | 102,054 | 0.3691 | 0.0994 | 0.2500 | 0.7200 | 1,948 | 1.91% |
| Innings 2+ | A — Rule | 91,960 | 0.4161 | 0.2795 | 0.0000 | 1.4830 | 19,665 | 21.38% |
| Innings 2+ | B — Hybrid | 91,960 | 0.4545 | 0.1847 | 0.0178 | 1.3679 | 14,275 | 15.52% |
| Innings 2+ | C — Alternative | 91,960 | 0.4788 | 0.1975 | 0.0178 | 1.3679 | 21,385 | 23.25% |
| IPL | A — Rule | 87,687 | 0.3261 | 0.2579 | 0.0000 | 1.4830 | 11,597 | 13.23% |
| IPL | B — Hybrid | 87,687 | 0.3436 | 0.2249 | 0.0000 | 1.3679 | 9,566 | 10.91% |
| IPL | C — Alternative | 87,687 | 0.4255 | 0.1648 | 0.0303 | 1.3679 | 11,151 | 12.72% |
| T20I | A — Rule | 106,327 | 0.3196 | 0.2549 | 0.0000 | 1.4830 | 13,742 | 12.92% |
| T20I | B — Hybrid | 106,327 | 0.3384 | 0.2167 | 0.0000 | 1.3679 | 10,383 | 9.77% |
| T20I | C — Alternative | 106,327 | 0.4175 | 0.1620 | 0.0178 | 1.3679 | 12,182 | 11.46% |

> Key observation on Model C Innings 1: Model C imposes a floor of `max(0.70×PI_rule, 0.50×PI_rule + 0.50×PI_lev)`. In the first innings the leverage component is constant at 0.50×0.5 = 0.25 (since WP is pinned at 0.5 for all first-innings deliveries in the logistic model). This creates an artificial floor of 0.25 for every first-innings delivery. That is why Model C Innings-1 min = 0.25, mean = 0.3691, and high+extreme drops to 1.91% — many deliveries are classified Moderate by default, not High. This is a methodological artefact of Model C, not a cricket signal, and is one reason Model B is preferred.

### 1b. Synthetic Cricket Scenario Comparison

**Source**: `pressure_model_synthetic_scenarios.csv`

| Scenario | Model A (Rule) | Model B (Hybrid) | Model C (Alt) | Classification under B |
|:---|:---:|:---:|:---:|:---|
| Comfortable Chase (RRR=5, 8wkts, 20b remaining) | 0.19 | 0.17 | 0.19 | Low |
| Tight Chase (RRR=9, 6wkts, 20b remaining) | 0.52 | 0.51 | 0.52 | Moderate |
| Death Overs Inn1 (8th wicket, over 18) | 0.72 | 0.72 | 0.72 | High |
| Early Collapse (3 wkts by over 5) | 0.58 | 0.52 | 0.58 | Moderate (B) / Moderate (C) |
| Near-impossible Chase (RRR=18, 4wkts) | **0.84** | **0.42** | **0.59** | Extreme(A) / Low-Mod(B) / Moderate(C) |
| Super Over (1b, 2 needed) | **1.20** | **0.90** | **0.84** | — (above threshold) |
| Winning easily (RRR=3, 10wkts) | 0.08 | 0.09 | 0.09 | Low |

**Critical divergence — Near-impossible Chase**: Model A assigns Extreme pressure (0.84) to a situation where WP ≈ 0% — the team has already effectively lost. Model B correctly dampens to 0.42 (Moderate) via leverage (LI near zero). Model C is a compromise at 0.59 (High). This single scenario class explains why Model A inflates death-specialist ratings.

### 1c. Top-10 Rankings Under Each Model

**Source**: `pressure_model_ranking_comparison.csv`

| Rank | Batter — Model A | Rating | Batter — Model B (Primary) | Rating | Batter — Model C | Rating |
|:---:|:---|:---:|:---|:---:|:---|:---:|
| 1 | Mahendra Singh Dhoni | 72.02 | Heinrich Klaasen | 77.59 | Rinku Singh | 77.76 |
| 2 | Rinku Singh | 71.34 | Ashutosh Sharma | 69.71 | Rashid Khan | 75.84 |
| 3 | Dhruv Jurel | 71.24 | Shashank Singh | 69.28 | Mahendra Singh Dhoni | 73.22 |
| 4 | M Shahrukh Khan | 67.75 | Shreyas Iyer | 68.22 | Ashutosh Sharma | 69.97 |
| 5 | Dasun Shanaka | 65.90 | Dinesh Karthik | 66.52 | Tim David | 68.13 |
| 6 | Tim David | 65.62 | Tim David | 66.48 | Heinrich Klaasen | 67.85 |
| 7 | Ashutosh Sharma | 65.07 | Suryakumar Yadav | 66.32 | Rovman Powell | 67.55 |
| 8 | David Miller | 64.24 | Rashid Khan | 66.23 | Shreyas Iyer | 64.54 |
| 9 | Sikandar Raza | 63.65 | Mahendra Singh Dhoni | 66.05 | Dinesh Karthik | 61.61 |
| 10 | George Dockrell | 63.60 | Rovman Powell | 63.11 | Jason Holder | 61.44 |

| Rank | Bowler — Model A | Rating | Bowler — Model B (Primary) | Rating | Bowler — Model C | Rating |
|:---:|:---|:---:|:---|:---:|:---|:---:|
| 1 | Yuzvendra Chahal | 80.19 | Sunil Narine | 77.83 | Abrar Ahmed | 77.69 |
| 2 | Shaheen Afridi | 80.15 | Krunal Pandya | 74.73 | Tim Southee | 72.29 |
| 3 | Sunil Narine | 71.31 | Rashid Khan | 71.52 | Sunil Narine | 70.28 |
| 4 | Matheesha Pathirana | 70.98 | Matheesha Pathirana | 69.35 | Mohit Sharma | 68.40 |
| 5 | Jofra Archer | 69.16 | Mustafizur Rahman | 66.38 | Akeal Hosein | 67.21 |
| 6 | Eshan Malinga | 68.88 | Yuzvendra Chahal | 65.03 | Matheesha Pathirana | 66.64 |
| 7 | Taskin Ahmed | 68.30 | Maheesh Theekshana | 64.60 | Krunal Pandya | 66.29 |
| 8 | Jasprit Bumrah | 68.18 | Varun Chakravarthy | 62.46 | Mitchell Santner | 65.48 |
| 9 | Lungi Ngidi | 67.98 | Jason Holder | 62.21 | Kuldeep Yadav | 64.30 |
| 10 | Tim Southee | 67.56 | Ravichandran Ashwin | 61.61 | Jasprit Bumrah | 63.99 |

---

## 2. Pressure Distribution by Innings and Competition

**Source**: `pressure_distribution.csv`

### 2a. Score Distribution (Hybrid pressure score = Model B)

| Segment — Innings | Segment — Format | N Deliveries | Min | P5 | P25 | Median | P75 | P95 | Max | Mean | Std |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| All | All | 194,014 | 0.0000 | 0.0000 | 0.1653 | 0.3507 | 0.4945 | 0.6819 | 1.3679 | 0.3407 | 0.2204 |
| Innings 1 | All | 102,054 | 0.0000 | 0.0000 | 0.0375 | 0.2105 | 0.3764 | 0.6083 | 0.9400 | 0.2382 | 0.1987 |
| Innings 2+ | All | 91,960 | 0.0178 | 0.1470 | 0.3416 | 0.4639 | 0.5461 | 0.7560 | 1.3679 | 0.4545 | 0.1847 |
| All | IPL | 87,687 | 0.0000 | 0.0000 | 0.1627 | 0.3525 | 0.5000 | 0.6917 | 1.3679 | 0.3436 | 0.2249 |
| All | T20I | 106,327 | 0.0000 | 0.0027 | 0.1667 | 0.3500 | 0.4898 | 0.6747 | 1.3679 | 0.3384 | 0.2167 |
| Innings 1 | IPL | 45,588 | 0.0000 | 0.0000 | 0.0375 | 0.1944 | 0.3646 | 0.6042 | 0.9400 | 0.2283 | 0.1974 |
| Innings 2+ | IPL | 42,099 | 0.0297 | 0.1831 | 0.3541 | 0.4715 | 0.5562 | 0.7752 | 1.3679 | 0.4684 | 0.1820 |
| Innings 1 | T20I | 56,466 | 0.0000 | 0.0000 | 0.0375 | 0.2261 | 0.3875 | 0.6167 | 0.9400 | 0.2462 | 0.1994 |
| Innings 2+ | T20I | 49,861 | 0.0178 | 0.1253 | 0.3298 | 0.4574 | 0.5384 | 0.7383 | 1.3679 | 0.4427 | 0.1861 |

### 2b. Pressure Tier Counts and Percentages

| Segment — Innings | Segment — Format | Low | Moderate | High | Extreme | High+Extreme | % High+Extreme |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| All | All | 96,474 | 77,668 | 17,068 | 2,804 | 19,872 | 10.24% |
| Innings 1 | All | 72,279 | 24,101 | 5,637 | 37 | 5,674 | 5.56% |
| Innings 2+ | All | 24,195 | 53,567 | 11,431 | 2,767 | 14,198 | 15.44% |
| All | IPL | 43,397 | 34,721 | 8,079 | 1,490 | 9,569 | 10.91% |
| All | T20I | 53,077 | 42,947 | 8,989 | 1,314 | 10,303 | 9.69% |
| Innings 1 | IPL | 33,221 | 9,984 | 2,353 | 30 | 2,383 | 5.23% |
| Innings 2+ | IPL | 10,176 | 24,737 | 5,726 | 1,460 | 7,186 | 17.07% |
| Innings 1 | T20I | 39,058 | 14,117 | 3,284 | 7 | 3,291 | 5.83% |
| Innings 2+ | T20I | 14,019 | 28,830 | 5,705 | 1,307 | 7,012 | 14.06% |

### 2c. Theoretical Bounds

| Component | Minimum | Base Maximum | With 1.20× Knockout |
|:---|:---:|:---:|:---:|
| Innings 1 rule (PI_rule) | 0.000 | 1.125 | **1.350** |
| Innings 2 rule component | 0.000 | 1.275 | 1.530 |
| Innings 2 leverage component | 0.000 | 1.500 | 1.500 |
| Innings 2 hybrid (50/50) | 0.000 | 1.3875 | **1.515** |
| **Actual observed max (all official)** | — | — | **1.3679** |

**Deliveries with score > 1.0**: 1,395 total (0.72% of official scope). These occur exclusively in knockout matches during Innings 2 extreme-pressure situations. The score > 1.0 is *before* any classification clipping; the threshold ≥0.60 for "High" pressure applies to the raw score, so these deliveries correctly land in the Extreme tier.

### 2d. Rule vs Leverage Score Summary

| Segment | Rule Min | Rule Mean | Rule Max | Leverage Min | Leverage Mean | Leverage Max |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| All official | 0.000 | 0.3225 | 1.483 | 0.000 | 0.4966 | 1.500 |
| Innings 1 | 0.000 | 0.2382 | 0.940 | 0.500 | 0.500 | 0.500 |
| Innings 2+ | 0.000 | 0.4161 | 1.483 | 0.000 | 0.4929 | 1.500 |
| IPL | 0.000 | 0.3261 | 1.483 | 0.000 | 0.5023 | 1.500 |
| T20I | 0.000 | 0.3196 | 1.483 | 0.000 | 0.4919 | 1.500 |

> Note: Innings 1 leverage is constant at 0.500 (WP pinned at 0.5 by definition for all first-innings deliveries). The hybrid therefore equals the rule score for first innings, as designed.

---

## 3. Ranking Stability — Complete Table

**Source**: `ranking_stability.csv`  
**Experiments tracked**: 16 per player (scope×2 counted separately; 9 consistency configs + clutch raw/ctx + pressure models = 16 total experiment variants)

### 3a. Batters — All Tracked Players

| Player | N Ranked | Top-10 Freq | Top-5 Freq | Avg Rank | Median Rank | Best Rank | Worst Rank | Rank Std |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Ashutosh Sharma** | 16/16 | **1.000** | 0.938 | 2.81 | 2.5 | 2 | 7 | 1.24 |
| **Tim David** | 16/16 | **1.000** | 0.188 | 7.25 | 7.0 | 5 | 9 | 1.68 |
| **Mahendra Singh Dhoni** | 16/16 | **1.000** | 0.125 | 6.62 | 6.0 | 1 | 9 | 2.26 |
| **Rovman Powell** | 16/16 | 0.938 | 0.000 | 10.81 | 10.0 | 7 | 26 | 3.99 |
| **Rashid Khan** | 16/16 | 0.938 | 0.125 | 7.00 | 7.0 | 2 | 11 | 1.84 |
| **Shreyas Iyer** | 15/16 | 0.938 | 0.875 | 4.47 | 4.0 | 4 | 8 | 1.02 |
| **Dinesh Karthik** | 16/16 | 0.938 | 0.688 | 6.50 | 5.0 | 4 | 20 | 3.76 |
| **Heinrich Klaasen** | 16/16 | 0.938 | 0.875 | 3.06 | 1.0 | 1 | 29 | 6.81 |
| **Suryakumar Yadav** | 16/16 | 0.875 | 0.000 | 8.81 | 8.0 | 6 | 18 | 3.36 |
| **Shashank Singh** | 16/16 | 0.875 | 0.875 | 4.62 | 3.0 | 2 | 24 | 5.73 |
| Rinku Singh | 16/16 | 0.125 | 0.125 | 10.75 | 12.0 | 1 | 13 | 3.51 |
| Dasun Shanaka | 16/16 | 0.062 | 0.062 | 10.69 | 11.0 | 5 | 12 | 1.49 |
| George Dockrell | 15/16 | 0.062 | 0.000 | 17.40 | 18.0 | 10 | 18 | 1.99 |
| Sikandar Raza | 16/16 | 0.062 | 0.000 | 18.06 | 19.0 | 9 | 20 | 2.77 |
| David Miller | 16/16 | 0.062 | 0.000 | 19.06 | 20.0 | 8 | 21 | 3.15 |
| Dhruv Jurel | 16/16 | 0.062 | 0.062 | 25.69 | 27.0 | 3 | 29 | 5.94 |
| M Shahrukh Khan | 1/16 | 0.062 | 0.062 | 4.00 | 4.0 | 4 | 4 | 0.00 |
| Jason Holder | 2/16 | 0.062 | 0.000 | 11.00 | 11.0 | 10 | 12 | 1.00 |
| Jitesh Sharma | 16/16 | 0.000 | 0.000 | 15.94 | 14.5 | 12 | 34 | 4.99 |
| Marcus Stoinis | 16/16 | 0.000 | 0.000 | 15.62 | 15.0 | 14 | 24 | 2.85 |
| Romario Shepherd | 16/16 | 0.000 | 0.000 | 14.69 | 13.0 | 13 | 30 | 4.51 |
| Sam Curran | 16/16 | 0.000 | 0.000 | 18.44 | 17.0 | 16 | 38 | 5.09 |
| Rahul Tewatia | 16/16 | 0.000 | 0.000 | 18.00 | 16.0 | 16 | 37 | 5.47 |
| Andre Russell | 16/16 | 0.000 | 0.000 | 22.50 | 21.0 | 20 | 41 | 5.10 |
| Washington Sundar | 16/16 | 0.000 | 0.000 | 31.12 | 31.0 | 14 | 50 | 6.44 |
| Liam Livingstone | 16/16 | 0.000 | 0.000 | 31.12 | 31.0 | 20 | 40 | 3.62 |
| Shivam Dube | 16/16 | 0.000 | 0.000 | 34.56 | 35.0 | 15 | 47 | 5.82 |

### 3b. Bowlers — All Tracked Players

| Player | N Ranked | Top-10 Freq | Top-5 Freq | Avg Rank | Median Rank | Best Rank | Worst Rank | Rank Std |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Sunil Narine** | 16/16 | **1.000** | **1.000** | 1.25 | 1.0 | 1 | 3 | 0.66 |
| **Matheesha Pathirana** | 16/16 | **1.000** | 0.938 | 4.12 | 4.0 | 4 | 6 | 0.48 |
| **Krunal Pandya** | 16/16 | 0.938 | 0.875 | 5.69 | 2.0 | 2 | 56 | 13.05 |
| **Yuzvendra Chahal** | 16/16 | 0.938 | 0.062 | 6.56 | 6.0 | 1 | 14 | 2.37 |
| **Mustafizur Rahman** | 16/16 | 0.875 | 0.812 | 6.25 | 5.0 | 5 | 15 | 3.13 |
| **Maheesh Theekshana** | 16/16 | 0.875 | 0.062 | 7.88 | 7.0 | 5 | 18 | 3.69 |
| **Rashid Khan** | 16/16 | 0.875 | 0.875 | 6.00 | 3.0 | 3 | 38 | 8.84 |
| **Varun Chakravarthy** | 16/16 | 0.875 | 0.000 | 9.81 | 9.0 | 8 | 22 | 3.32 |
| **Jason Holder** | 16/16 | 0.812 | 0.000 | 10.94 | 9.0 | 9 | 31 | 5.41 |
| **Ravichandran Ashwin** | 16/16 | 0.812 | 0.000 | 10.44 | 10.0 | 8 | 24 | 3.79 |
| Jasprit Bumrah | 16/16 | 0.125 | 0.000 | 15.88 | 17.0 | 8 | 17 | 2.67 |
| Tim Southee | 2/16 | 0.125 | 0.062 | 6.00 | 6.0 | 2 | 10 | 4.00 |
| Jofra Archer | 1/16 | 0.062 | 0.062 | 5.00 | 5.0 | 5 | 5 | 0.00 |
| Shaheen Afridi | 16/16 | 0.062 | 0.062 | 14.50 | 14.5 | 2 | 26 | 4.29 |
| Mohit Sharma | 2/16 | 0.062 | 0.062 | 7.50 | 7.5 | 4 | 11 | 3.50 |
| Akeal Hosein | 1/16 | 0.062 | 0.062 | 5.00 | 5.0 | 5 | 5 | 0.00 |
| Avesh Khan | 16/16 | 0.062 | 0.000 | 15.06 | 12.5 | 9 | 47 | 8.70 |
| Kuldeep Yadav | 16/16 | 0.062 | 0.000 | 15.44 | 14.5 | 9 | 35 | 5.24 |
| Axar Patel | 16/16 | 0.062 | 0.000 | 16.50 | 13.0 | 10 | 58 | 11.84 |
| Taskin Ahmed | 1/16 | 0.062 | 0.000 | 7.00 | 7.0 | 7 | 7 | 0.00 |
| Lungi Ngidi | 1/16 | 0.062 | 0.000 | 9.00 | 9.0 | 9 | 9 | 0.00 |
| Eshan Malinga | 2/16 | 0.062 | 0.000 | 13.50 | 13.5 | 6 | 21 | 7.50 |
| Abrar Ahmed | 1/16 | 0.062 | 0.062 | 1.00 | 1.0 | 1 | 1 | 0.00 |
| Mitchell Santner | 2/16 | 0.062 | 0.000 | 12.50 | 12.5 | 8 | 17 | 4.50 |
| Wanindu Hasaranga | 16/16 | 0.000 | 0.000 | 13.25 | 11.0 | 11 | 39 | 6.92 |
| Arshdeep Singh | 16/16 | 0.000 | 0.000 | 23.38 | 23.0 | 18 | 29 | 2.00 |
| Shardul Thakur | 16/16 | 0.000 | 0.000 | 21.50 | 21.0 | 20 | 28 | 2.18 |
| Mohammed Siraj | 16/16 | 0.000 | 0.000 | 26.88 | 28.0 | 13 | 30 | 3.82 |
| Josh Hazlewood | 16/16 | 0.000 | 0.000 | 16.81 | 16.0 | 16 | 26 | 2.43 |
| Lockie Ferguson | 16/16 | 0.000 | 0.000 | 21.88 | 20.0 | 19 | 45 | 6.00 |
| Harshit Rana | 16/16 | 0.000 | 0.000 | 21.88 | 22.0 | 13 | 29 | 2.85 |
| Tushar Deshpande | 16/16 | 0.000 | 0.000 | 21.38 | 19.0 | 18 | 41 | 6.57 |
| Romario Shepherd | 16/16 | 0.000 | 0.000 | 21.94 | 18.0 | 18 | 60 | 10.54 |

---

## 4. Average, Best and Worst Rank — Shortlisted Players

Shortlisted = appeared in top 10 in ≥1 experiment variant.

### 4a. Batters

| Player | Avg Rank | Median | Best | Worst | Top-10 Freq | Stability Assessment |
|:---|:---:|:---:|:---:|:---:|:---:|:---|
| Ashutosh Sharma | 2.81 | 2.5 | 2 | 7 | 100% | **Highly stable** — never outside top 7 |
| Shreyas Iyer | 4.47 | 4.0 | 4 | 8 | 93.8% | **Highly stable** — tight range (4–8) |
| Shashank Singh | 4.62 | 3.0 | 2 | 24 | 87.5% | Mostly stable; worst=24 only in Model A |
| Heinrich Klaasen | 3.06 | 1.0 | 1 | 29 | 93.8% | #1 in 11/16; worst=29 only in Model A |
| Dinesh Karthik | 6.50 | 5.0 | 4 | 20 | 93.8% | Stable under Model B; drops in Model A |
| Rashid Khan | 7.00 | 7.0 | 2 | 11 | 93.8% | Very stable — narrow band 2–11 |
| Mahendra Singh Dhoni | 6.62 | 6.0 | 1 | 9 | 100% | Stable in B; #1 only under Model A |
| Tim David | 7.25 | 7.0 | 5 | 9 | 100% | Very stable — narrowest range |
| Suryakumar Yadav | 8.81 | 8.0 | 6 | 18 | 87.5% | Stable in mid-table |
| Rovman Powell | 10.81 | 10.0 | 7 | 26 | 93.8% | Borderline #10; worst=26 in Model A scope |
| Rinku Singh | 10.75 | 12.0 | 1 | 13 | 12.5% | Appears only under Model A — death specialist |
| Dasun Shanaka | 10.69 | 11.0 | 5 | 12 | 6.2% | Model A only |

### 4b. Bowlers

| Player | Avg Rank | Median | Best | Worst | Top-10 Freq | Stability Assessment |
|:---|:---:|:---:|:---:|:---:|:---:|:---|
| Sunil Narine | 1.25 | 1.0 | 1 | 3 | 100% | **Exceptional — #1 in 15/16** |
| Matheesha Pathirana | 4.12 | 4.0 | 4 | 6 | 100% | **Exceptional stability — range only 4–6** |
| Rashid Khan | 6.00 | 3.0 | 3 | 38 | 87.5% | Stable in B; worst=38 is Model A |
| Krunal Pandya | 5.69 | 2.0 | 2 | 56 | 93.8% | Stable in B; worst=56 is Model A artefact |
| Yuzvendra Chahal | 6.56 | 6.0 | 1 | 14 | 93.8% | #1 only under Model A |
| Mustafizur Rahman | 6.25 | 5.0 | 5 | 15 | 87.5% | Solid mid-table performer |
| Maheesh Theekshana | 7.88 | 7.0 | 5 | 18 | 87.5% | Reliable across experiments |
| Varun Chakravarthy | 9.81 | 9.0 | 8 | 22 | 87.5% | Borderline top-10 |
| Jason Holder | 10.94 | 9.0 | 9 | 31 | 81.2% | Borderline; falls out in some configs |
| Ravichandran Ashwin | 10.44 | 10.0 | 8 | 24 | 81.2% | Borderline #10 |

---

## 5. Top-10 Membership Frequency

### 5a. Batters — Frequency Across All 16 Experiments

| Player | Top-10 Appearances | Out of 16 | % | In Primary Top-10? |
|:---|:---:|:---:|:---:|:---:|
| Ashutosh Sharma | 16 | 16 | **100%** | ✓ Rank 2 |
| Tim David | 16 | 16 | **100%** | ✓ Rank 6 |
| Mahendra Singh Dhoni | 16 | 16 | **100%** | ✓ Rank 9 |
| Rovman Powell | 15 | 16 | 93.8% | ✓ Rank 10 |
| Rashid Khan | 15 | 16 | 93.8% | ✓ Rank 8 |
| Shreyas Iyer | 15 | 16 | 93.8% | ✓ Rank 4 |
| Dinesh Karthik | 15 | 16 | 93.8% | ✓ Rank 5 |
| Heinrich Klaasen | 15 | 16 | 93.8% | ✓ Rank 1 |
| Suryakumar Yadav | 14 | 16 | 87.5% | ✓ Rank 7 |
| Shashank Singh | 14 | 16 | 87.5% | ✓ Rank 3 |
| Rinku Singh | 2 | 16 | 12.5% | ✗ (Model A only) |
| Dasun Shanaka | 1 | 16 | 6.2% | ✗ (Model A only) |
| Others | ≤1 | 16 | ≤6.2% | ✗ |

**Conclusion**: All 10 primary top-10 batters have ≥87.5% top-10 membership frequency. The two players appearing exclusively or predominantly under Model A (Rinku Singh 12.5%, Dasun Shanaka 6.2%) are excluded from the primary top-10 by design.

### 5b. Bowlers — Frequency Across All 16 Experiments

| Player | Top-10 Appearances | Out of 16 | % | In Primary Top-10? |
|:---|:---:|:---:|:---:|:---:|
| Sunil Narine | 16 | 16 | **100%** | ✓ Rank 1 |
| Matheesha Pathirana | 16 | 16 | **100%** | ✓ Rank 4 |
| Krunal Pandya | 15 | 16 | 93.8% | ✓ Rank 2 |
| Yuzvendra Chahal | 15 | 16 | 93.8% | ✓ Rank 6 |
| Mustafizur Rahman | 14 | 16 | 87.5% | ✓ Rank 5 |
| Maheesh Theekshana | 14 | 16 | 87.5% | ✓ Rank 7 |
| Rashid Khan | 14 | 16 | 87.5% | ✓ Rank 3 |
| Varun Chakravarthy | 14 | 16 | 87.5% | ✓ Rank 8 |
| Jason Holder | 13 | 16 | 81.2% | ✓ Rank 9 |
| Ravichandran Ashwin | 13 | 16 | 81.2% | ✓ Rank 10 |
| Jasprit Bumrah | 2 | 16 | 12.5% | ✗ |
| Others | ≤2 | 16 | ≤12.5% | ✗ |

**Conclusion**: All 10 primary top-10 bowlers have ≥81.2% top-10 membership frequency. No bowler outside the primary list approaches this threshold using valid experiment configurations.

---

## 6. Complete Ratings — Primary vs Alternative Models

**Source**: `top_10_batters.csv`, `top_10_bowlers.csv`, `alternative_top_10_batters.csv`, `alternative_top_10_bowlers.csv`

### 6a. Batters

| Rank | Primary (Model B) Player | Primary Rating | Pressure Balls | Pressure Matches | Perf Dim | Clutch Dim | Cons Dim |
|:---:|:---|:---:|:---:|:---:|:---|:---|:---|
| 1 | Heinrich Klaasen | **77.59** | 122 | 22 | — | — | — |
| 2 | Ashutosh Sharma | **69.71** | 119 | 19 | — | — | — |
| 3 | Shashank Singh | **69.28** | 107 | 19 | — | — | — |
| 4 | Shreyas Iyer | **68.22** | 169 | 20 | — | — | — |
| 5 | Dinesh Karthik | **66.52** | 129 | 23 | — | — | — |
| 6 | Tim David | **66.48** | 300 | 45 | — | — | — |
| 7 | Suryakumar Yadav | **66.32** | 254 | 28 | — | — | — |
| 8 | Rashid Khan | **66.23** | 179 | 44 | — | — | — |
| 9 | Mahendra Singh Dhoni | **66.05** | 127 | 28 | — | — | — |
| 10 | Rovman Powell | **63.11** | 181 | 30 | — | — | — |

> Note: Dimension scores (Perf/Clutch/Cons) are stored as z-scores in source CSV for context-adjusted clutch method; the alternative CSV below provides them for the Model A run.

| Rank | Alternative (Model A) Player | Alt Rating | Pressure Balls | Pressure Matches | Perf Dim | Clutch Dim | Cons Dim |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | Mahendra Singh Dhoni | **72.02** | 241 | 34 | 1.178 | 2.181 | 1.069 |
| 2 | Rinku Singh | **71.34** | 260 | 35 | 1.636 | 1.081 | 1.163 |
| 3 | Dhruv Jurel | **71.24** | 159 | 19 | 1.621 | 1.419 | 0.179 |
| 4 | M Shahrukh Khan | **67.75** | 109 | 20 | 1.172 | 1.407 | 0.584 |
| 5 | Dasun Shanaka | **65.90** | 210 | 30 | 0.954 | 1.235 | 1.168 |
| 6 | Tim David | **65.62** | 307 | 39 | 1.482 | −0.005 | 1.535 |
| 7 | Ashutosh Sharma | **65.07** | 154 | 23 | 1.266 | 0.782 | 0.110 |
| 8 | David Miller | **64.24** | 355 | 38 | 1.088 | 0.890 | 0.296 |
| 9 | Sikandar Raza | **63.65** | 117 | 14 | 0.983 | 1.208 | −0.419 |
| 10 | George Dockrell | **63.60** | 112 | 14 | 0.812 | 1.139 | 0.774 |

### 6b. Bowlers

| Rank | Primary (Model B) Player | Primary Rating | Pressure Legal Balls | Pressure Matches |
|:---:|:---|:---:|:---:|:---:|
| 1 | Sunil Narine | **77.83** | 130 | 18 |
| 2 | Krunal Pandya | **74.73** | 130 | 15 |
| 3 | Rashid Khan | **71.52** | 183 | 27 |
| 4 | Matheesha Pathirana | **69.35** | 206 | 28 |
| 5 | Mustafizur Rahman | **66.38** | 222 | 38 |
| 6 | Yuzvendra Chahal | **65.03** | 247 | 31 |
| 7 | Maheesh Theekshana | **64.60** | 161 | 25 |
| 8 | Varun Chakravarthy | **62.46** | 199 | 25 |
| 9 | Jason Holder | **62.21** | 227 | 38 |
| 10 | Ravichandran Ashwin | **61.61** | 128 | 16 |

| Rank | Alternative (Model A) Player | Alt Rating | Pressure Legal Balls | Pressure Matches | Perf Dim | Clutch Dim | Cons Dim |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | Yuzvendra Chahal | **80.19** | 299 | 33 | 2.056 | 2.018 | 1.737 |
| 2 | Shaheen Afridi | **80.15** | 172 | 26 | 2.047 | 1.978 | 1.888 |
| 3 | Sunil Narine | **71.31** | 131 | 16 | 1.857 | 0.812 | 0.625 |
| 4 | Matheesha Pathirana | **70.98** | 308 | 33 | 1.457 | 1.059 | 2.065 |
| 5 | Jofra Archer | **69.16** | 135 | 23 | 1.266 | 1.740 | −0.041 |
| 6 | Eshan Malinga | **68.88** | 146 | 14 | 1.211 | 1.442 | 0.999 |
| 7 | Taskin Ahmed | **68.30** | 132 | 20 | 1.384 | 1.080 | 0.656 |
| 8 | Jasprit Bumrah | **68.18** | 268 | 40 | 1.693 | 0.555 | 0.297 |
| 9 | Lungi Ngidi | **67.98** | 121 | 19 | 1.224 | 1.461 | 0.256 |
| 10 | Tim Southee | **67.56** | 156 | 21 | 1.154 | 1.239 | 1.065 |

---

## 7. Competition Scope Comparison

**Source**: `competition_scope_comparison.csv` and `competition_scope_detail.csv`

### 7a. Side-by-Side Top-10

| Rank | Official Batter (IPL+T20I) | Expanded Batter (+Other T20) | Official Bowler | Expanded Bowler |
|:---:|:---|:---|:---|:---|
| 1 | Heinrich Klaasen | Heinrich Klaasen | Sunil Narine | Sunil Narine |
| 2 | Ashutosh Sharma | Ashutosh Sharma | Krunal Pandya | Krunal Pandya |
| 3 | Shashank Singh | Shashank Singh | Rashid Khan | Rashid Khan |
| 4 | Shreyas Iyer | Shreyas Iyer | Matheesha Pathirana | Matheesha Pathirana |
| 5 | Dinesh Karthik | **Tim David** *(↑1)* | Mustafizur Rahman | Mustafizur Rahman |
| 6 | Tim David | **Dinesh Karthik** *(↓1)* | Yuzvendra Chahal | Yuzvendra Chahal |
| 7 | Suryakumar Yadav | **Rashid Khan** *(↑1)* | Maheesh Theekshana | Maheesh Theekshana |
| 8 | Rashid Khan | **Suryakumar Yadav** *(↓1)* | Varun Chakravarthy | Varun Chakravarthy |
| 9 | Mahendra Singh Dhoni | Mahendra Singh Dhoni | Jason Holder | Jason Holder |
| 10 | Rovman Powell | Rovman Powell | Ravichandran Ashwin | Ravichandran Ashwin |

### 7b. Rating Changes

| Player | Role | Official Rank | Official Rating | Expanded Rank | Expanded Rating | Rating Δ |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| Heinrich Klaasen | Bat | 1 | 77.59 | 1 | 76.97 | −0.62 |
| Ashutosh Sharma | Bat | 2 | 69.71 | 2 | 70.63 | +0.92 |
| Shashank Singh | Bat | 3 | 69.28 | 3 | 68.98 | −0.30 |
| Shreyas Iyer | Bat | 4 | 68.22 | 4 | 68.00 | −0.22 |
| Dinesh Karthik | Bat | 5 | 66.52 | 6 | 66.35 | −0.17 |
| Tim David | Bat | 6 | 66.48 | 5 | 66.44 | −0.04 |
| Suryakumar Yadav | Bat | 7 | 66.32 | 8 | 66.30 | −0.02 |
| Rashid Khan | Bat | 8 | 66.23 | 7 | 66.31 | +0.08 |
| Mahendra Singh Dhoni | Bat | 9 | 66.05 | 9 | 66.12 | +0.07 |
| Rovman Powell | Bat | 10 | 63.11 | 10 | 63.26 | +0.15 |
| Sunil Narine | Bowl | 1 | 77.83 | 1 | 77.83 | 0.00 |
| Krunal Pandya | Bowl | 2 | 74.73 | 2 | 74.73 | 0.00 |
| Rashid Khan | Bowl | 3 | 71.52 | 3 | 71.52 | 0.00 |
| Matheesha Pathirana | Bowl | 4 | 69.35 | 4 | 69.35 | 0.00 |
| Mustafizur Rahman | Bowl | 5 | 66.38 | 5 | 66.38 | 0.00 |
| Yuzvendra Chahal | Bowl | 6 | 65.03 | 6 | 65.03 | 0.00 |
| Maheesh Theekshana | Bowl | 7 | 64.60 | 7 | 64.60 | 0.00 |
| Varun Chakravarthy | Bowl | 8 | 62.46 | 8 | 62.46 | 0.00 |
| Jason Holder | Bowl | 9 | 62.21 | 9 | 62.21 | 0.00 |
| Ravichandran Ashwin | Bowl | 10 | 61.61 | 10 | 61.61 | 0.00 |

**Key finding**: Adding the 30 Emerging Teams Asia Cup matches (the only other T20 competitions in the dataset) produces zero changes to the bowler rankings and only minor position swaps (5↔6 for Karthik/David and 7↔8 for SKY/Rashid) in the batter rankings. No batter's rating changes by more than 0.92 points on a 100-point scale. The two scope variants are functionally equivalent.

---

## 8. Context-Adjusted Clutch Comparison

**Source**: `clutch_method_comparison.csv`

| Player | Role | Raw Clutch Rank | Raw Rating | Context-Adj Rank | Context-Adj Rating | Rank Change | Explanation |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| Heinrich Klaasen | Bat | 1 | 75.62 | 1 | 77.59 | 0 | RAE advantage reinforced by context |
| Ashutosh Sharma | Bat | 2 | 70.60 | 2 | 69.71 | 0 | Stable |
| Shashank Singh | Bat | 3 | 69.68 | 3 | 69.28 | 0 | Stable |
| Shreyas Iyer | Bat | 5 | 67.52 | 4 | 68.22 | **+1** | Context-adj gives credit for difficult pressure overs |
| Dinesh Karthik | Bat | 8 | 66.27 | 5 | 66.52 | **+3** | Death-over RAE contextually adjusted upwards |
| Tim David | Bat | 9 | 66.23 | 6 | 66.48 | **+3** | High contextual difficulty; context helps |
| Suryakumar Yadav | Bat | 7 | 66.30 | 7 | 66.32 | 0 | Stable |
| Rashid Khan | Bat | 4 | 68.80 | 8 | 66.23 | **−4** | Raw SR elevated in high-RRR situations that context already explains |
| Mahendra Singh Dhoni | Bat | 6 | 66.86 | 9 | 66.05 | **−3** | Death-over SR advantage partially context-driven |
| Rovman Powell | Bat | 10 | 63.50 | 10 | 63.11 | 0 | Stable |
| Sunil Narine | Bowl | 1 | 78.61 | 1 | 77.83 | 0 | Dominant both ways |
| Krunal Pandya | Bowl | 2 | 73.89 | 2 | 74.73 | 0 | Stable; slightly better context-adj |
| Rashid Khan | Bowl | 3 | 70.32 | 3 | 71.52 | 0 | Reinforced by context |
| Matheesha Pathirana | Bowl | 4 | 69.43 | 4 | 69.35 | 0 | Stable |
| Mustafizur Rahman | Bowl | 6 | 65.08 | 5 | 66.38 | **+1** | Contextually difficult overs rewarded |
| Yuzvendra Chahal | Bowl | 7 | 63.18 | 6 | 65.03 | **+1** | Contextual adjustment benefits spinner |
| Maheesh Theekshana | Bowl | 5 | 65.52 | 7 | 64.60 | **−2** | Partial raw economy advantage is contextual |
| Varun Chakravarthy | Bowl | 8 | 62.54 | 8 | 62.46 | 0 | Stable |
| Jason Holder | Bowl | — | — | 9 | 62.21 | — | Enters top-10 only under context-adj method |
| Ravichandran Ashwin | Bowl | — | — | 10 | 61.61 | — | Enters top-10 only under context-adj method |
| Avesh Khan | Bowl | 9 | 61.54 | — | — | — | Drops out under context-adj |
| Axar Patel | Bowl | 10 | 61.34 | — | — | — | Drops out under context-adj |

**Composition change**: Batters — identical 10 players, minor reordering. Bowlers — Avesh Khan and Axar Patel exit; Jason Holder and Ravichandran Ashwin enter under context-adjusted method. This reflects that Holder and Ashwin's runs-prevented metrics hold up better when adjusted for contextual difficulty than their raw economy differentials.

---

## 9. Consistency and Bayesian Prior Comparison

**Source**: `consistency_comparison.csv` (complete 180-row table summarised below)

### 9a. Legend

| Config | Consistency Formula | Bayesian k |
|:---|:---|:---:|
| FormulaA_k20 | 0.50×z(pos_match%) + 0.30×z(log1p(balls)) − 0.20×z(std) | 20 |
| FormulaA_k40 | Same | 40 |
| FormulaA_k80 | Same | 80 |
| FormulaB_k20 | 0.60×z(pos_match%) − 0.40×z(std) — no volume | 20 |
| FormulaB_k40 | Same | 40 |
| FormulaB_k80 | Same | 80 |
| FormulaC_k20 | 0.50×z(pos_match%) + 0.30×z(−CI_width) − 0.20×z(std) | 20 |
| FormulaC_k40 | Same | 40 |
| FormulaC_k80 | Same | 80 |

### 9b. Batter Top-10 Across All 9 Configurations

| Config | Rank-1 | Rank-2 | Rank-3 | Rank-4 | Rank-5 |
|:---|:---:|:---:|:---:|:---:|:---:|
| **FormulaA_k20** | Klaasen | Sharma | Singh | Iyer | Karthik |
| **FormulaA_k40** | Klaasen | Sharma | Singh | Iyer | Karthik |
| **FormulaA_k80** | Klaasen | Sharma | Singh | Iyer | Tim David |
| **FormulaB_k20** | Klaasen | Shashank | Sharma | Karthik | Iyer |
| **FormulaB_k40** | Klaasen | Shashank | Sharma | Iyer | Karthik |
| **FormulaB_k80** | Klaasen | Shashank | Sharma | Iyer | Karthik |
| **FormulaC_k20** | Klaasen | Shashank | Sharma | Karthik | Iyer |
| **FormulaC_k40** | Klaasen | Shashank | Sharma | Iyer | Karthik |
| **FormulaC_k80** | Klaasen | Shashank | Sharma | Iyer | Karthik |

**Heinrich Klaasen is Rank 1 in all 9 batter configurations.**

| Config | Rank-6 | Rank-7 | Rank-8 | Rank-9 | Rank-10 |
|:---|:---:|:---:|:---:|:---:|:---:|
| FormulaA_k20 | Dhoni | Rashid | SKY | Tim David | Powell |
| FormulaA_k40 | Tim David | SKY | Rashid | Dhoni | Powell |
| FormulaA_k80 | SKY | Rashid | Karthik | Dhoni | Powell |
| FormulaB_k20 | Dhoni | Rashid | SKY | Tim David | Powell |
| FormulaB_k40 | Dhoni | Rashid | SKY | Tim David | Powell |
| FormulaB_k80 | Dhoni | Rashid | SKY | Tim David | Powell |
| FormulaC_k20 | Dhoni | Rashid | SKY | Tim David | Powell |
| FormulaC_k40 | Dhoni | Rashid | SKY | Tim David | Powell |
| FormulaC_k80 | Dhoni | Rashid | Tim David | SKY | Powell |

> (SKY = Suryakumar Yadav)  
> **Player set is identical across all 9 configurations**: {Klaasen, Sharma, Singh, Iyer, Karthik, Tim David, SKY, Rashid, Dhoni, Powell}. Only the order within positions 4–9 varies.

### 9c. Bowler Top-10 Across All 9 Configurations

| Config | Rank-1 | Rank-2 | Rank-3 | Rank-4 | Rank-5 | Rank-6 | Rank-7 | Rank-8 | Rank-9 | Rank-10 |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| FormulaA_k20 | Narine | Pandya | Rashid | Pathirana | Mustafiz | Chahal | Theekshana | Chakra | Holder | Ashwin |
| FormulaA_k40 | Narine | Pandya | Rashid | Pathirana | Mustafiz | Chahal | Theekshana | Chakra | Holder | Ashwin |
| FormulaA_k80 | Narine | Pandya | Rashid | Pathirana | Mustafiz | Chahal | Theekshana | Chakra | Holder | Ashwin |
| FormulaB_k20 | Narine | Pandya | Rashid | Pathirana | Mustafiz | Theekshana | Chahal | Ashwin | Holder | Chakra |
| FormulaB_k40 | Narine | Pandya | Rashid | Pathirana | Mustafiz | Theekshana | Chahal | Ashwin | Holder | Chakra |
| FormulaB_k80 | Narine | Pandya | Rashid | Pathirana | Mustafiz | Theekshana | Chahal | Ashwin | Holder | Chakra |
| FormulaC_k20 | Narine | Pandya | Rashid | Pathirana | Mustafiz | Theekshana | Chahal | Ashwin | Holder | Chakra |
| FormulaC_k40 | Narine | Pandya | Rashid | Pathirana | Mustafiz | Theekshana | Chahal | Ashwin | Holder | Chakra |
| FormulaC_k80 | Narine | Pandya | Rashid | Pathirana | Mustafiz | Chahal | Theekshana | Ashwin | Holder | Chakra |

> **Player set is identical across all 9 configurations**: {Narine, Pandya, Rashid, Pathirana, Mustafiz, Chahal, Theekshana, Chakra, Holder, Ashwin}. Ranks 1–5 are invariant to formula and k.

### 9d. Rating Range by Player

| Batter | Min Rating (across 9 configs) | Max Rating | Δ Max–Min |
|:---|:---:|:---:|:---:|
| Heinrich Klaasen | 77.12 | 79.13 | 2.01 |
| Ashutosh Sharma | 68.02 | 70.60 | 2.58 |
| Shashank Singh | 68.57 | 70.49 | 1.92 |
| Shreyas Iyer | 67.09 | 68.37 | 1.28 |
| Dinesh Karthik | 66.27 | 67.39 | 1.12 |
| Tim David | 63.69 | 67.56 | 3.87 |
| Suryakumar Yadav | 64.50 | 66.91 | 2.41 |
| Rashid Khan | 65.77 | 66.47 | 0.70 |
| Mahendra Singh Dhoni | 65.89 | 67.02 | 1.13 |
| Rovman Powell | 63.02 | 63.46 | 0.44 |

| Bowler | Min Rating | Max Rating | Δ Max–Min |
|:---|:---:|:---:|:---:|
| Sunil Narine | 77.31 | 79.14 | 1.83 |
| Krunal Pandya | 74.17 | 75.62 | 1.45 |
| Rashid Khan | 71.04 | 71.69 | 0.65 |
| Matheesha Pathirana | 69.08 | 69.65 | 0.57 |
| Mustafizur Rahman | 65.64 | 66.75 | 1.11 |
| Yuzvendra Chahal | 64.22 | 65.42 | 1.20 |
| Maheesh Theekshana | 64.59 | 65.25 | 0.66 |
| Varun Chakravarthy | 61.70 | 62.64 | 0.94 |
| Jason Holder | 61.72 | 62.40 | 0.68 |
| Ravichandran Ashwin | 61.32 | 62.99 | 1.67 |

---

## 10. Final Methodology Justification

### 10.1 Primary Configuration

| Dimension | Selection | Rationale |
|:---|:---|:---|
| Competition scope | IPL + T20I (837 matches, 194,014 deliveries) | Problem statement specification. Adding 30 Emerging Teams matches changes no ranks (bowlers) or only minor position swaps (batters). |
| Pressure model | **Model B: Hybrid 50/50** | Win-probability leverage prevents crediting performance in dead-match situations. Model A assigns Extreme (0.84) to near-impossible chases where WP ≈ 0%. Model B dampens these to Moderate (0.42). Model C partially addresses this but introduces a constant floor in Innings 1 (0.25) due to fixed first-innings WP = 0.5, misclassifying many Innings 1 deliveries as Moderate when they are genuinely Low. |
| Clutch measurement | **Context-adjusted RAE/RP delta** | Raw SR changes in death overs are partially driven by the bowling lineup and match state rather than the batter's own skill. Context-adjusted RAE subtracts what the ML model predicts for that exact situation (overs, wickets, format, phase), isolating true clutch improvement. The top-10 composition is identical to raw SR under both methods; context-adjusted provides better theoretical justification. |
| Consistency formula | **Formula A** (includes volume) | Volume appears in both Bayesian shrinkage and consistency dimension, but the double-reward effect is minimal because consistency carries only 10% of the composite weight. Formula A's log1p(balls) term also penalises players who appeared in extreme situations only 2–3 times (reducing noise from small-sample extreme finishers). |
| Bayesian prior strength | **k = 40** | At k=20, players with ~60–80 pressure balls retain volatile rates. At k=80, genuine specialists with 120–160 balls (Klaasen, Ashwin) are over-shrunk towards the population average. k=40 is the standard empirical Bayes default for T20 performance metrics and produces the best calibration across the pressure ball distribution (see Section 9d: rating ranges stay narrow). |
| Eligibility thresholds | ≥100 pressure balls (bat), ≥120 pressure legal balls (bowl), ≥12 pressure matches | Prevents single-match outliers from entering the rankings. At the threshold boundary (100 balls / 12 matches), Bayesian shrinkage absorbs remaining noise. All primary top-10 batters meet these thresholds comfortably (minimum 107 balls, 19 matches). |

### 10.2 Why Model B Is Superior to A and C

**Against Model A**:  
Yuzvendra Chahal and Shaheen Afridi rank #1 and #2 under Model A with ratings of 80.19 and 80.15, both above Narine (71.31). These bowlers bowled substantially in situations where the batting team's WP was already near zero — the "unwinnable chase" scenario — meaning wickets and dot balls in those overs have minimal actual match-shifting value. Model A, having no leverage correction, treats these identically to wickets in a 50/50 match. Model B correctly de-rates these situations.

**Against Model C**:  
Model C's Innings 1 leverage component is a constant 0.25 (since WP = 0.5 for all first-innings deliveries in the logistic model, `clip(0.5/2, 0, 1.5) = 0.25`). This means `PI_C = max(0.70×PI_rule, 0.50×PI_rule + 0.125)`. For deliveries where PI_rule < 0.357, Model C's floor of 0.125 + 0.50×PI_rule exceeds 0.70×PI_rule, inflating them. This converts 70.1% of Innings 1 deliveries to Moderate (all with PI_rule < 0.25 get a bump), causing Innings 1 high+extreme to collapse to 1.91% — lower than even the pre-audit code. This is not a cricket signal.

**Against both alternatives**:  
Model B Innings 1 high+extreme = 5.56%, identical to Model A. This is because the Innings 1 pressure formula is used without leverage modification in Model B (the hybrid applies only to Innings 2). The only substantive difference between A and B is in second-innings leverage-moderated deliveries — exactly where the theoretical justification is clearest.

### 10.3 Cross-Experiment Stability

The primary top-10 batter composition is unchanged across all 11 Model-B experiment variants (2 clutch methods × 9 consistency+k combinations, minus the scope variation which is equivalent). Heinrich Klaasen is #1 in all 11 Model-B variants.

The primary top-10 bowler composition is unchanged across all 11 Model-B experiment variants (positions 1–5 are invariant; positions 6–10 show Chahal/Theekshana and Holder/Ashwin position swaps only). Sunil Narine is #1 in all 16 experiment variants including Model A and C.

**Heinrich Klaasen should be submitted as Rank 1 batter. Sunil Narine should be submitted as Rank 1 bowler.**

### 10.4 Unstop Submission Verification

The final submission should use **exactly** the following player names and ranks from `top_10_batters.csv` and `top_10_bowlers.csv`:

**Batters (dropdown selections, Rank 1 to Rank 10)**:
1. Heinrich Klaasen
2. Ashutosh Sharma
3. Shashank Singh
4. Shreyas Iyer
5. Dinesh Karthik
6. Tim David
7. Suryakumar Yadav
8. Rashid Khan
9. Mahendra Singh Dhoni
10. Rovman Powell

**Bowlers (dropdown selections, Rank 1 to Rank 10)**:
1. Sunil Narine
2. Krunal Pandya
3. Rashid Khan
4. Matheesha Pathirana
5. Mustafizur Rahman
6. Yuzvendra Chahal
7. Maheesh Theekshana
8. Varun Chakravarthy
9. Jason Holder
10. Ravichandran Ashwin

---

## Appendix: Data Sources

| This section | Primary CSV | Secondary CSV |
|:---|:---|:---|
| Cross-check (Sec 0) | `top_10_batters.csv`, `top_10_bowlers.csv` | `methodology_report.md` |
| Pressure model (Sec 1) | `pressure_model_comparison.csv` | `pressure_model_ranking_comparison.csv`, `pressure_model_synthetic_scenarios.csv` |
| Pressure distribution (Sec 2) | `pressure_distribution.csv` | — |
| Ranking stability (Sec 3) | `ranking_stability.csv` | — |
| Best/worst/avg rank (Sec 4) | `ranking_stability.csv` | — |
| Membership frequency (Sec 5) | `ranking_stability.csv` | — |
| Primary vs alt ratings (Sec 6) | `top_10_batters.csv`, `alternative_top_10_batters.csv` | `top_10_bowlers.csv`, `alternative_top_10_bowlers.csv` |
| Scope comparison (Sec 7) | `competition_scope_comparison.csv` | `competition_scope_detail.csv` |
| Clutch comparison (Sec 8) | `clutch_method_comparison.csv` | — |
| Consistency comparison (Sec 9) | `consistency_comparison.csv` | — |
| Justification (Sec 10) | All experiment outputs | `experiment_summary.csv` |
