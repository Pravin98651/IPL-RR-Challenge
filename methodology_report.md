# SupeRR Selector Season 2: Identifying the Most Reliable Players Under Pressure
## Comprehensive Analytical Methodology Report & Independent Technical Audit

**Competition**: SupeRR Selector Season 2 — Round 1  
**Project**: Cricket Pressure Analytics Engine  
**Dataset Timeframe**: 2022 – 2026 (Historical IPL and T20 Internationals)  
**Deliverables**: Top 10 Batters, Top 10 Bowlers, Delivery-Level Feature Store, Reproducible Python Pipeline  

---

## Executive Summary & Audit Overview

In high-stakes Twenty20 cricket, winning margins are often decided by microscopic advantages in critical junctures. Conventional cricket metrics—such as aggregate runs, raw batting average, gross wickets, and overall economy rate—fail to distinguish between low-leverage stat-padding and clutch performances delivered when the match hangs in the balance.

Following an independent technical audit of the initial analytics system, several critical domain and mathematical enhancements were implemented:
1. **Dataset-Count Reconciliation**: Resolved discrepancies between match records in `matches.csv` (883 rows) and `ball_by_ball.csv` (867 active matches), explicitly accounting for 16 abandoned matches and non-IPL T20 tournaments.
2. **First-Innings Pressure Calibration**: Rectified a temporal mutual-exclusivity flaw where 1st innings pressure scores were structurally suppressed (0% high pressure balls). The calibrated formulation appropriately elevates acute early collapses and death-over boundary demands, creating fair representation across both innings.
3. **Ball Scarcity Formulation**: Corrected ball scarcity to $1 - (\text{Legal Balls Remaining} / \text{Scheduled Legal Balls})$, properly handling rain-reduced matches.
4. **Dynamic Leverage Simulation**: Corrected Required Run Rate recomputation in simulated states, allowing the logistic win-probability model's primary driver to be fully reflected in pre-delivery leverage.
5. **Empirical Calibration & Validation**: Validated the win-probability model using 5-fold match-grouped cross-validation, demonstrating exceptional calibration ($\text{ECE} = 0.0051$, slope $= 0.983$, intercept $= 0.001$).
6. **Multi-Scale Bayesian Shrinkage**: Evaluated shrinkage priors ($k=20, 40, 80$) to stabilize rate metrics without unfairly penalizing high-volume regulars.

### Final Official Top 10 Rankings

#### Top 10 Batters Under Pressure
*Selected in rank order for the Unstop submission dropdowns:*

| Rank | Player Name | Pressure Balls | Runs | Pressure SR | Baseline SR | Clutch Delta ($\Delta$SR) | Runs Above Exp / Ball | Pos Match % | Pressure Matches | Rating |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | **Heinrich Klaasen** | 122 | 249 | 204.10 | 163.24 | **+40.86** | **+0.611** | 72.7% | 22 | **76.97** |
| **2** | **Ashutosh Sharma** | 125 | 242 | 193.60 | 150.90 | **+42.70** | **+0.422** | 60.0% | 20 | **70.63** |
| **3** | **Shashank Singh** | 107 | 215 | 200.93 | 152.32 | **+48.62** | **+0.414** | 47.4% | 19 | **68.98** |
| **4** | **Shreyas Iyer** | 169 | 324 | 191.72 | 149.29 | **+42.42** | **+0.430** | 50.0% | 20 | **68.00** |
| **5** | **Tim David** | 300 | 584 | 194.67 | 172.14 | **+22.53** | **+0.467** | 57.8% | 45 | **66.44** |
| **6** | **Dinesh Karthik** | 129 | 253 | 196.12 | 160.00 | **+36.12** | **+0.368** | 52.2% | 23 | **66.35** |
| **7** | **Rashid Khan** | 179 | 329 | 183.80 | 140.85 | **+42.95** | **+0.344** | 45.5% | 44 | **66.31** |
| **8** | **Suryakumar Yadav** | 254 | 484 | 190.55 | 163.98 | **+26.57** | **+0.413** | 67.9% | 28 | **66.30** |
| **9** | **Mahendra Singh Dhoni**| 127 | 230 | 181.10 | 137.80 | **+43.30** | **+0.226** | 46.4% | 28 | **66.12** |
| **10** | **Rovman Powell** | 181 | 322 | 177.90 | 142.67 | **+35.23** | **+0.310** | 60.0% | 30 | **63.26** |

#### Top 10 Bowlers Under Pressure
*Selected in rank order for the Unstop submission dropdowns:*

| Rank | Player Name | Pressure Balls | Wickets | Pressure Econ | Baseline Econ | Clutch Delta ($\Delta$Econ) | Runs Prevented / Ball | Pos Match % | Pressure Matches | Rating |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | **Sunil Narine** | 130 | 10 | 6.09 | 6.94 | **+0.84** | **+0.343** | 88.9% | 18 | **77.83** |
| **2** | **Krunal Pandya** | 130 | 11 | 6.42 | 7.98 | **+1.56** | **+0.227** | 86.7% | 15 | **74.73** |
| **3** | **Rashid Khan** | 183 | 19 | 7.67 | 7.42 | **-0.26** | **+0.181** | 85.2% | 27 | **71.52** |
| **4** | **Matheesha Pathirana** | 206 | 21 | 8.83 | 8.86 | **+0.03** | **+0.350** | 82.1% | 28 | **69.35** |
| **5** | **Mustafizur Rahman** | 222 | 23 | 8.16 | 7.75 | **-0.42** | **+0.232** | 73.7% | 19 | **66.38** |
| **6** | **Yuzvendra Chahal** | 247 | 26 | 8.87 | 8.59 | **-0.28** | **-0.026** | 64.5% | 31 | **65.03** |
| **7** | **Maheesh Theekshana** | 161 | 11 | 7.49 | 7.79 | **+0.30** | **+0.177** | 72.0% | 25 | **64.60** |
| **8** | **Varun Chakravarthy** | 199 | 16 | 7.84 | 8.03 | **+0.19** | **+0.088** | 72.0% | 25 | **62.46** |
| **9** | **Jason Holder** | 227 | 22 | 9.36 | 8.95 | **-0.40** | **+0.095** | 81.6% | 38 | **62.21** |
| **10** | **Ravichandran Ashwin** | 128 | 10 | 8.39 | 7.81 | **-0.58** | **+0.040** | 68.8% | 16 | **61.61** |

---

## 1. Dataset Reconciliation & Data Quality Findings

### Match Count Reconciliation Table
To resolve previous reconciliation discrepancies, the table below documents the exact accounting across `matches.csv`, `competitions.csv`, and `ball_by_ball.csv`:

| Competition / Stage Category | Rows in `matches.csv` | Active in `ball_by_ball.csv` | Excluded (Abandoned) | Stage Breakdown in Active Deliveries |
| :--- | :---: | :---: | :---: | :--- |
| **Indian Premier League (IPL)** | **371** | **367** | **4** | 2022: 74, 2023: 74, 2024: 71 (3 aband.), 2025: 74 (1 aband.), 2026: 74 |
| **Other T20 Competitions** | **30** | **30** | **0** | Emerging Teams Asia Cup 2024 (15), Asia Cup Rising Stars 2025 (15) |
| **Total T20 Format Matches** | **401** | **397** | **4** | Format code = `T20` |
| **T20 Internationals (T20I)** | **482** | **470** | **12** | Bilaterals, Tri-series, Asia Cups (Format code = `T20I`) |
| **Total Across All Competitions** | **883** | **867** | **16** | **Exact match count = 867** |
| **Knockout / Playoff Matches** | **31** | **31** | **0** | Finals (12), Qualifiers (10), Eliminators (5), Semi-Finals (4) |
| **League / Group Matches** | **852** | **836** | **16** | League (613 active, 7 aband.), Others (217 active, 9 aband.), Super 4 (6) |

*Finding*: Exactly 16 matches recorded in `matches.csv` were abandoned without a ball bowled (e.g. wet outfield/continuous rain). All 31 knockout matches were completed.

---

## 2. Quantitative Pressure Definition & Calibration

### Second-Innings Chase Pressure Formula
For chases ($i \ge 2$), pressure reflects resource scarcity and statistical leverage:
$$PI_{\text{chase}} = 0.40 \cdot \text{RRR\_comp} + 0.30 \cdot \text{Wkt\_comp} + 0.20 \cdot \text{Ball\_Scarcity} + 0.10 \cdot \text{Closeness}$$
Where:
- $\text{RRR\_comp} = \text{clip}\left(\frac{RRR - 6.0}{8.0}, 0.0, 1.5\right)$
- $\text{Wkt\_comp} = \text{clip}\left(\frac{\text{wickets\_lost}}{8.0}, 0.0, 1.25\right)$
- $\text{Ball\_Scarcity} = 1.0 - \left(\frac{\text{pre\_legal\_balls\_remaining}}{\text{scheduled\_legal\_balls}}\right)$ *(Corrected to handle reduced-overs matches)*
- $\text{Closeness} = 1.0$ if $\text{pre\_legal\_balls\_remaining} \le 30$ and $\text{runs\_needed} \le 45$, else $0.0$.

### Calibrated First-Innings Pressure Formula
The audit revealed that an additive formula ($0.40 \cdot \text{collapse} + 0.40 \cdot \text{death}$) produced 0% high-pressure balls because collapses (early) and death overs (late) are temporally mutually exclusive. The corrected formulation models situational urgency:
$$\text{Situational Urgency} = \max(\text{Collapse Intensity}, \text{Death Urgency})$$
Where:
- $\text{Collapse Intensity} = \text{clip}\left(\frac{\text{wickets\_lost} - 1.0}{3.0}, 0.0, 1.25\right) \cdot \left(1.0 - \frac{\text{balls\_completed}}{\text{scheduled\_balls}}\right)$
- $\text{Death Urgency} = \text{clip}\left(\frac{\text{balls\_completed} - 0.75 \cdot \text{scheduled\_balls}}{0.25 \cdot \text{scheduled\_balls}}, 0.0, 1.0\right)$
- $\text{Wicket Scarcity} = \text{clip}\left(\frac{\text{wickets\_lost}}{8.0}, 0.0, 1.0\right)$
- $\text{Par Deficit} = \text{clip}\left(\frac{\text{par\_deficit}}{25.0}, 0.0, 1.0\right)$
$$PI_{\text{inn1}} = 0.50 \cdot \text{Situational Urgency} + 0.30 \cdot \text{Wicket Scarcity} + 0.20 \cdot \text{Par Deficit}$$

Match Stakes Multiplier: Knockout matches (`knock_out == 1`) receive a **1.20$\times$ stake amplifier**.

### Scenario Test Matrix (Verification of Cricket Logic)
The table below validates the pressure model across representative scenarios:

| Scenario Description | Innings | Key State Variables | Component Breakdowns | Pressure Score ($PI$) | Classification |
| :--- | :---: | :--- | :--- | :---: | :--- |
| **1. Cruising Start** | 2 | RRR=6.0, 100/1 in 3.2 ov (100 req off 100) | RRR: 0.00, Wkt: 0.12, Ball: 0.17 | **0.071** | Low Pressure |
| **2. Steep Chase Mid-Innings** | 2 | RRR=12.0, 60/2 in 10.0 ov (120 req off 60) | RRR: 0.75, Wkt: 0.25, Ball: 0.50 | **0.475** | Moderate Pressure |
| **3. Collapse in Chase** | 2 | RRR=10.0, 80/7 in 12.0 ov (80 req off 48) | RRR: 0.50, Wkt: 0.88, Ball: 0.60 | **0.583** | High Pressure (Border) |
| **4. Heroic Death Finish** | 2 | RRR=16.0, 140/5 in 18.0 ov (32 req off 12) | RRR: 1.25, Wkt: 0.62, Ball: 0.90, Close: 1.0 | **0.968** | Extreme Pressure |
| **5. Comfortable Death Chase** | 2 | RRR=5.0, 150/3 in 17.0 ov (15 req off 18) | RRR: 0.00, Wkt: 0.38, Ball: 0.85, Close: 1.0 | **0.382** | Moderate Pressure |
| **6. Lost Cause / Dead Rubber** | 2 | RRR=36.0, 60/8 in 18.0 ov (72 req off 12) | RRR: 1.50, Wkt: 1.00, Ball: 0.90, Leverage $\approx 0$ | **0.540** | Moderate (Damped by Leverage) |
| **A. Stable 1st Inn Powerplay** | 1 | 35/0 after 4.0 overs, Par deficit = -5 | Sit: 0.00, Wkt: 0.00, Deficit: 0.00 | **0.000** | Low Pressure |
| **B. Early Batting Collapse** | 1 | 18/3 after 4.0 overs, Par deficit = +15 | Sit: 0.53, Wkt: 0.38, Deficit: 0.60 | **0.499** | Moderate/High Building |
| **C. Acute Mid Collapse** | 1 | 75/5 after 12.0 overs, Par deficit = +20 | Sit: 0.50, Wkt: 0.62, Deficit: 0.80 | **0.598** | High Pressure Threshold |
| **D. High-Scoring Death Overs** | 1 | 165/3 after 18.0 overs, Par deficit = -10 | Sit: 0.60, Wkt: 0.38, Deficit: 0.00 | **0.412** | Moderate Pressure |
| **E. Acute Death Overs** | 1 | 180/6 after 19.3 overs, Par deficit = 0 | Sit: 0.90, Wkt: 0.75, Deficit: 0.00 | **0.675** | High Pressure |

---

## 3. Win Probability & Expected Performance Validation

### Win Probability Cross-Validation
Evaluated under **5-fold match-grouped cross-validation (`GroupKFold` by `match_id`)**:

| Model | Log Loss | Brier Score | ROC-AUC | Calibration Slope | Calibration Intercept | Expected Calibration Error (ECE) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Naive Dummy Baseline** | 0.6925 | 0.2497 | 0.5000 | N/A | N/A | 0.2497 |
| **Simple RRR Logistic** | 0.4778 | 0.1544 | 0.8578 | 0.924 | +0.042 | 0.0321 |
| **Full Production Logistic**| **0.4126** | **0.1343** | **0.8908** | **0.983** | **+0.001** | **0.0051** |
| **XGBoost Classifier** | 0.4252 | 0.1389 | 0.8832 | 0.941 | -0.021 | 0.0185 |

*Audit Conclusion*: The Logistic Regression model exhibits near-perfect calibration (slope 0.983 vs 1.000 ideal; intercept 0.001 vs 0.000 ideal; ECE = 0.51%). It dominates both baselines and outperforms XGBoost in out-of-fold generalization.

### Out-of-Fold Contextual Expectation Validation
Trained using `HistGradientBoosting` on pre-delivery context (zero player IDs, zero in-sample contamination):
- **Batter Expected Runs**: $\text{MAE} = 1.2844$, $\text{RMSE} = 1.7141$ (vs. Naive Baseline $\text{RMSE} = 1.7634$). Mean Predicted: 1.3402 vs. Actual: 1.3411 runs/ball.
- **Bowler Expected Concessions**: $\text{MAE} = 1.2736$, $\text{RMSE} = 1.7008$. Mean Predicted: 1.3901 vs. Actual: 1.3913 runs/ball.

---

## 4. Bayesian Shrinkage & Metric Construction

To balance sample sizes without double-penalizing high-volume players:
$$\text{Adjusted Score} = \frac{n}{n + k} \cdot \text{Observed} + \frac{k}{n + k} \cdot \mu_{\text{pop}}$$
Empirical evaluation across prior strengths ($k=20, 40, 80$):
- At $k=20$: Low shrinkage; micro-sample hitters with 60–70 balls retain volatile ratings.
- At $k=40$: Optimal empirical trade-off. Shorter-sample specialists (e.g. Ashutosh Sharma, 125 balls) are stabilized while proven superstars (Tim David, 300 balls; Suryakumar Yadav, 254 balls) retain their genuine rate superiority.
- At $k=80$: Over-shrinkage; dampens high-leverage outliers excessively.

### Final Composite Rating
$$\text{Composite Score} = 0.60 \cdot z(S_{\text{perf}}) + 0.30 \cdot z(S_{\text{clutch}}) + 0.10 \cdot z(S_{\text{cons}})$$
$$\text{Pressure Rating} = 50.0 + 15.0 \cdot \text{Composite Score}$$

---

## 5. Robustness & Sensitivity Audit

1. **Knockout Multiplier Audit**:
   - At 1.00 (no multiplier): Heinrich Klaasen (#1), Ashutosh Sharma (#2), Shashank Singh (#3).
   - At 1.10: Same top 3; Shreyas Iyer rises to #4 due to high playoff volume.
   - At 1.20 (production): Robust ordering; rewards proven knockout match-winners while preserving league data fidelity.
   - At 1.30: Over-weights the 31 knockout games relative to 836 regular matches. **Recommendation: Retain 1.20$\times$**.
2. **Weight Configuration Robustness**:
   Across 5 weighting configurations (Baseline 60/30/10, High Consistency 50/30/20, High Performance 70/20/10, High Clutch 40/50/10, Pure Pressure 80/10/10), Heinrich Klaasen remains **Rank 1** across all 5 configurations, with Ashutosh Sharma, Shashank Singh, Shreyas Iyer, and Tim David consistently in the top tier.
3. **Tournament Fairness**:
   Contextual expectation models include tournament format (`format_code`), standardizing baseline run rates (~8.8 in IPL vs ~8.0 in T20I) without distorting pooled rankings.

---

## 6. Updated Deliverables Reference

- `top_10_batters.csv`: Final ranked batters with opportunity and competition breakdowns.
- `top_10_bowlers.csv`: Final ranked bowlers with opportunity and competition breakdowns.
- `all_batter_scores.csv` & `all_bowler_scores.csv`: Complete ratings across all 888 batters and 647 bowlers.
- `pressure_analysis.csv`: Delivery-level pressure distribution.
- `methodology_report.pdf`: Generated 3-page styled PDF document.
- `outputs/visualizations/*.png`: 12 high-resolution analytical figures.
- `tests/test_comprehensive_audit.py`: 25 passing automated unit tests.
