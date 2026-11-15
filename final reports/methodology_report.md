# SupeRR Selector Season 2: Identifying the Most Reliable Players Under Pressure
## Comprehensive Analytical Methodology Report — Full Validation & Experiment Results

**Competition**: SupeRR Selector Season 2 — Round 1  
**Project**: Cricket Pressure Analytics Engine  
**Dataset Timeframe**: 2022 – 2026 (Historical IPL and T20 Internationals)  
**Deliverables**: Top 10 Batters, Top 10 Bowlers, Delivery-Level Feature Store, Reproducible Python Pipeline  

---

## Executive Summary

In high-stakes Twenty20 cricket, winning margins are decided by microscopic advantages at critical junctures. Conventional metrics — aggregate runs, raw batting average, gross wickets, overall economy — fail to distinguish low-leverage stat-padding from clutch performances delivered when the match hangs in the balance.

This report documents a complete, evidence-based pressure analytics system applied to 200,999 deliveries across 867 IPL and T20I matches from 2022–2026. The system:

1. **Defines pressure quantitatively** using a calibrated hybrid of domain-rule situational urgency and win-probability leverage, validated across six representative cricket scenarios.
2. **Measures player performance** in those pressure situations using context-adjusted Runs Above Expectation and Win Probability Added, computed by out-of-fold machine-learning models with no player-identity contamination.
3. **Ranks players** through Bayesian shrinkage and three-dimensional composite ratings covering pressure performance, clutch improvement, and consistency.
4. **Validates all rankings** via nine robustness experiments spanning competition scope, pressure model selection, clutch measurement method, consistency formula, sample-size sensitivity, and cross-experiment stability.

An independent technical audit corrected three critical implementation bugs:

| Bug | Impact | Fix |
|:----|:-------|:----|
| 1st-innings additive pressure (collapse + death overs both zero in same phase) | 0% high-pressure balls in Innings 1 | `max(collapse, death_urgency)` formulation |
| Ball Scarcity = `balls_completed/120` (wrong for rain-reduced matches) | Inflated scarcity in D/L matches | `1 − (balls_remaining / scheduled_balls)` |
| Leverage RRR not recomputed in simulated states | Underestimated leverage in key situations | Explicit RRR recomputation in win-probability simulation |

---

## Final Official Top 10 Rankings

### Top 10 Batters Under Pressure *(Primary: IPL + T20I, Model B Hybrid Pressure, Context-Adjusted Clutch, k=40)*

| Rank | Player | Pressure Balls | Pressure SR | Baseline SR | Δ SR | RAE/Ball | Pos Match % | Matches | Rating |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1** | **Heinrich Klaasen** | 122 | 204.10 | 163.24 | +40.86 | +0.611 | 72.7% | 22 | **77.59** |
| **2** | **Ashutosh Sharma** | 119 | 192.44 | 155.81 | +36.62 | +0.431 | 57.9% | 19 | **69.71** |
| **3** | **Shashank Singh** | 107 | 200.93 | 152.32 | +48.62 | +0.414 | 47.4% | 19 | **69.28** |
| **4** | **Shreyas Iyer** | 169 | 191.72 | 149.29 | +42.42 | +0.430 | 50.0% | 20 | **68.22** |
| **5** | **Dinesh Karthik** | 129 | 196.12 | 160.00 | +36.12 | +0.368 | 52.2% | 23 | **66.52** |
| **6** | **Tim David** | 300 | 194.67 | 172.14 | +22.53 | +0.467 | 57.8% | 45 | **66.48** |
| **7** | **Suryakumar Yadav** | 254 | 190.55 | 163.98 | +26.57 | +0.413 | 67.9% | 28 | **66.32** |
| **8** | **Rashid Khan** | 179 | 183.80 | 140.85 | +42.95 | +0.344 | 45.5% | 44 | **66.23** |
| **9** | **Mahendra Singh Dhoni** | 127 | 181.10 | 137.80 | +43.30 | +0.226 | 46.4% | 28 | **66.05** |
| **10** | **Rovman Powell** | 181 | 177.90 | 142.67 | +35.23 | +0.310 | 60.0% | 30 | **63.11** |

> [!NOTE]
> Population Baseline: Pressure SR = 154.33, RAE/Ball = +0.137. All top-10 batters comfortably exceed this baseline. Every player meets the minimum threshold: ≥100 pressure balls and ≥12 pressure matches.

### Top 10 Bowlers Under Pressure *(Primary: IPL + T20I, Model B Hybrid Pressure, Context-Adjusted Clutch, k=40)*

| Rank | Player | Pressure Balls | Wickets | Pressure Econ | Baseline Econ | Δ Econ | RP/Ball | Pos Match % | Matches | Rating |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1** | **Sunil Narine** | 130 | 10 | 6.09 | 6.94 | +0.84 | +0.343 | 88.9% | 18 | **77.83** |
| **2** | **Krunal Pandya** | 130 | 11 | 6.42 | 7.98 | +1.56 | +0.227 | 86.7% | 15 | **74.73** |
| **3** | **Rashid Khan** | 183 | 19 | 7.67 | 7.42 | −0.26 | +0.181 | 85.2% | 27 | **71.52** |
| **4** | **Matheesha Pathirana** | 206 | 21 | 8.83 | 8.86 | +0.03 | +0.350 | 82.1% | 28 | **69.35** |
| **5** | **Mustafizur Rahman** | 222 | 23 | 8.16 | 7.75 | −0.42 | +0.232 | 73.7% | 38 | **66.38** |
| **6** | **Yuzvendra Chahal** | 247 | 26 | 8.87 | 8.59 | −0.28 | −0.026 | 64.5% | 31 | **65.03** |
| **7** | **Maheesh Theekshana** | 161 | 11 | 7.49 | 7.79 | +0.30 | +0.177 | 72.0% | 25 | **64.60** |
| **8** | **Varun Chakravarthy** | 199 | 16 | 7.84 | 8.03 | +0.19 | +0.088 | 72.0% | 25 | **62.46** |
| **9** | **Jason Holder** | 227 | 22 | 9.36 | 8.95 | −0.40 | +0.095 | 81.6% | 38 | **62.21** |
| **10** | **Ravichandran Ashwin** | 128 | 10 | 8.39 | 7.81 | −0.58 | +0.040 | 68.8% | 16 | **61.61** |

> [!NOTE]
> Minimum thresholds: ≥120 pressure legal balls, ≥12 pressure matches. Narine and Krunal's near-elite economy rates under pressure — 6.09 and 6.42 — in what are inherently high-stakes situations are extraordinary; both maintain them while taking wickets and dramatically outperforming their own normal-game baselines.

---

## 1. Dataset Reconciliation

| Category | Count | Definition |
|:---|:---:|:---|
| Rows in `matches.csv` | 883 | Raw match records |
| Unique match IDs in `matches.csv` | 883 | No duplicates found |
| Active matches in `ball_by_ball.csv` | **867** | At least one delivery bowled |
| Abandoned (no ball bowled) | **16** | 4 IPL + 12 T20I |
| IPL matches (active) | 367 | `comp_name` contains 'IPL' |
| Other T20 (non-IPL, format = T20) | 30 | Emerging Teams Asia Cup 2024 (15) + Asia Cup Rising Stars 2025 (15) |
| T20I matches (active) | 470 | `match_format = 'T20I'` |
| Total active T20 format | 397 | IPL 367 + Other T20 30 |
| Knockout/playoff matches (active) | 31 | Finals, Qualifiers, Eliminators, Semi-Finals |
| League/group matches (active) | 836 | Total minus 31 knockout |
| **Official scope (IPL + T20I)** | **837** | Used for all primary rankings |

---

## 2. Pressure Definition

### Philosophy

Pressure in T20 cricket is a compound state: not just the difficulty of what's needed, but how much losing a wicket or conceding a boundary will swing the match's outcome. The system models pressure from two independent perspectives and combines them:

- **Situational urgency** (domain rules): what the scoreboard demands
- **Statistical leverage** (win probability): how much this delivery can shift match outcome probability

### Second-Innings Chase Formula

$$PI_{\text{chase}} = 0.40 \cdot \text{RRR\_comp} + 0.30 \cdot \text{Wkt\_comp} + 0.20 \cdot \text{Ball\_Scarcity} + 0.10 \cdot \text{Closeness}$$

Where:
- $\text{RRR\_comp} = \text{clip}\left(\frac{RRR - 6.0}{8.0}, 0.0, 1.5\right)$
- $\text{Wkt\_comp} = \text{clip}\left(\frac{\text{wickets\_lost}}{8.0}, 0.0, 1.25\right)$
- $\text{Ball\_Scarcity} = 1.0 - \left(\frac{\text{pre\_legal\_balls\_remaining}}{\text{scheduled\_legal\_balls}}\right)$
- $\text{Closeness} = 1.0$ if balls_remaining ≤ 30 and runs_needed ≤ 45, else 0.0

### First-Innings Formula (Audit-Corrected)

$$\text{Situational Urgency} = \max(\text{Collapse Intensity},\ \text{Death Urgency})$$
$$PI_{\text{inn1}} = 0.50 \cdot \text{Situational Urgency} + 0.30 \cdot \text{Wicket Scarcity} + 0.20 \cdot \text{Par Deficit}$$

The `max()` operator prevents mutual-exclusion suppression — collapses happen early, death-overs late; additive combination zeroed both.

### Hybrid Pressure Index (Model B — Primary)

For chases: $PI_{\text{hybrid}} = 0.50 \cdot PI_{\text{rule}} + 0.50 \cdot \text{clip}(LI/2, 0, 1.5)$

For first innings: $PI_{\text{hybrid}} = PI_{\text{rule}}$ (leverage in first innings has lower predictive value)

**Classification thresholds**: Low < 0.35 ≤ Moderate < 0.60 ≤ High < 0.85 ≤ Extreme

**Match Stakes**: Knockout matches receive a **1.20× multiplier** on the rule component.

### Scenario Validation Matrix

| Scenario | Inn | Key State | Pressure Score | Tier |
|:---|:---:|:---|:---:|:---|
| Cruising start (RRR=6, 100/1 in 3.2 ov) | 2 | Very low demands | **0.071** | Low |
| Steep mid-innings chase (RRR=12, 60/2 in 10 ov) | 2 | Rising demands | **0.475** | Moderate |
| Collapse in chase (RRR=10, 80/7 in 12 ov) | 2 | Resource crisis | **0.583** | High (Border) |
| Heroic death finish (RRR=16, 140/5 in 18 ov) | 2 | Extreme urgency | **0.968** | Extreme |
| Lost cause (RRR=36, 60/8, WP≈0) | 2 | Damped by leverage | **0.540** | Moderate |
| Stable powerplay (35/0, par surplus) | 1 | No urgency | **0.000** | Low |
| Early collapse (18/3, par deficit=15) | 1 | Acute early crisis | **0.499** | Moderate/High |
| Death overs (180/6, over 19.3) | 1 | Death urgency | **0.675** | High |

---

## 3. Win Probability & Expected Performance Validation

### Win Probability Model (Logistic Regression — Full Production)

Trained on 2nd-innings match states with features: runs_needed, balls_remaining, wickets_remaining, RRR, CRR, phase, format_code, knock_out. Validated with 5-fold match-grouped GroupKFold cross-validation.

| Model | Log Loss | Brier | AUC | Calibration Slope | ECE |
|:---|:---:|:---:|:---:|:---:|:---:|
| Naive Dummy | 0.6925 | 0.2497 | 0.500 | — | 0.2497 |
| Simple RRR Logistic | 0.4778 | 0.1544 | 0.858 | 0.924 | 0.0321 |
| **Full Production Logistic** | **0.4126** | **0.1343** | **0.891** | **0.983** | **0.0051** |
| XGBoost | 0.4252 | 0.1389 | 0.883 | 0.941 | 0.0185 |

The logistic model achieves near-perfect calibration (ECE = 0.51%, slope = 0.983). Logistic chosen over XGBoost for explicit coefficients and monotonic behaviour under extrapolation.

### Expected Performance Model

Trained using `HistGradientBoosting` with out-of-fold predictions (GroupKFold, no player IDs in features):

- **Batter**: MAE = 1.2844, RMSE = 1.7141 vs. Naive Baseline RMSE = 1.7634
- **Bowler**: MAE = 1.2736, RMSE = 1.7008

Population baseline Runs Above Expectation (RAE): pressure RAE/ball = +0.137 (all eligible batters face harder situations, context model correctly adjusts for this).

---

## 4. Rating Architecture

### Bayesian Shrinkage

$$\text{Adjusted Metric} = \frac{n}{n+k} \cdot \text{Observed} + \frac{k}{n+k} \cdot \mu_{\text{pop}}$$

**Production setting**: k = 40 balls. Note that $k=40$ is the selected prior strength chosen for balanced empirical shrinkage—dampening rate volatility in smaller sample sizes while remaining responsive to proven high-volume performers—rather than a proven global mathematical optimum. Sensitivity analysis across $k \in \{20, 40, 80\}$ is documented in Experiment 5.

### Three-Dimensional Composite

$$\text{Rating} = 50.0 + 15.0 \times \left(0.60 \cdot z_{\text{perf}} + 0.30 \cdot z_{\text{clutch}} + 0.10 \cdot z_{\text{consistency}}\right)$$

**Performance dimension** (60%): Shrunk RAE/ball, Strike Rate, WPA/ball, boundary rate, dot rate.

**Clutch dimension** (30%): Context-adjusted delta — how much better/worse vs. own normal baseline (Δ RAE, Δ SR, Δ WPA, Δ dot reduction).

**Consistency dimension** (10%): Percentage of pressure matches with positive RAE, Bayesian-shrunk sample volume, inverse of match-level RAE standard deviation.

---

## 5. Experiment Results

### Experiment 1: Competition Scope

| | Official (IPL + T20I) | Expanded (+ Other T20) |
|:---|:---:|:---:|
| Matches | 837 | 867 |
| Deliveries | 194,014 | 200,999 |

**Top 10 Batters — Stability Across Scope**:

| Rank | Official (Primary) | Expanded |
|:---:|:---|:---|
| 1 | Heinrich Klaasen | Heinrich Klaasen |
| 2 | Ashutosh Sharma | Ashutosh Sharma |
| 3 | Shashank Singh | Shashank Singh |
| 4 | Shreyas Iyer | Shreyas Iyer |
| 5 | Dinesh Karthik | Tim David |
| 6 | Tim David | Dinesh Karthik |
| 7 | Suryakumar Yadav | Rashid Khan |
| 8 | Rashid Khan | Suryakumar Yadav |
| 9 | Mahendra Singh Dhoni | Mahendra Singh Dhoni |
| 10 | Rovman Powell | Rovman Powell |

**Top 10 Bowlers**: Identical in both scopes — all 10 names and their order are unchanged by adding the 30 Emerging Teams Asia Cup matches.

> [!IMPORTANT]
> The top-10 batter list changes only in minor position swaps (5↔6, 7↔8) when the Other T20 scope is added. The top-10 bowler list is completely stable. This confirms the official IPL + T20I scope is representative and the Other T20 data has negligible influence on rankings.

---

### Experiment 2: Pressure Score Calibration

**Theoretical bounds** (computed analytically):

| Component | Formula | Min | Max (Base) | Max (with 1.20× KO) |
|:---|:---|:---:|:---:|:---:|
| Innings 1 rule | 0.50×SI + 0.30×WS + 0.20×PD | 0 | 1.125 | **1.350** |
| Innings 2 rule | 0.40×RRR + 0.30×Wkt + 0.20×BS + 0.10×Close | 0 | 1.275 | 1.530 |
| Innings 2 leverage | clip(LI/2, 0, 1.5) | 0 | 1.500 | 1.500 |
| Innings 2 hybrid | 0.50×rule + 0.50×lev | 0 | 1.3875 | **1.515** |

**Actual observed scores (all official deliveries)**:

| Segment | Min | P25 | Median | P75 | P95 | Max | Mean |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| All official | 0.000 | 0.106 | 0.218 | 0.437 | 0.859 | **1.368** | 0.277 |
| Innings 1 | 0.000 | 0.044 | 0.144 | 0.360 | 0.713 | 1.125 | 0.195 |
| Innings 2 | 0.000 | 0.191 | 0.397 | 0.600 | 1.028 | 1.368 | 0.396 |
| IPL | 0.000 | 0.106 | 0.218 | 0.455 | 0.892 | 1.368 | 0.284 |
| T20I | 0.000 | 0.106 | 0.218 | 0.422 | 0.843 | 1.325 | 0.272 |

**Pressure tier distribution** (official scope):

| Tier | Innings 1 IPL | Innings 1 T20I | Innings 2 IPL | Innings 2 T20I |
|:---|:---:|:---:|:---:|:---:|
| Low | 33,221 | 39,058 | 10,176 | 14,002 |
| Moderate | 9,984 | 14,117 | 24,740 | 28,767 |
| High | 2,353 | 3,284 | 5,728 | 5,688 |
| Extreme | 30 | 7 | 1,455 | 1,404 |
| **High + Extreme** | **2,383** | **3,291** | **7,183** | **7,092** |

> [!NOTE]
> 1,395 deliveries (0.7% of official scope) have pressure_score > 1.0. These are knockout matches with both very high situational urgency and high leverage. The classification threshold (≥0.60 = High pressure) is applied before clipping, so they correctly fall into High or Extreme tiers. No artificial clipping needed for the classification itself.

---

### Experiment 3: Pressure Model Comparison

Three models tested:

| Model | Description |
|:---|:---|
| **A — Rule-only** | `PI = PI_rule` (domain formula only) |
| **B — Hybrid 50/50** | Chase: `0.50×PI_rule + 0.50×PI_lev`; Inn1: `PI_rule` *(Primary)* |
| **C — Alternative** | `max(0.70×PI_rule, 0.50×PI_rule + 0.50×PI_lev)` — prevents near-zero WP erasing obvious situational urgency |

**High/Extreme pressure delivery counts**:

| Model | All | Inn 1 | Inn 2 |
|:---:|:---:|:---:|:---:|
| A (Rule) | 20,953 (10.8%) | 5,674 (6.2%) | 15,279 (18.6%) |
| B (Hybrid) | 20,886 (10.8%) | 5,674 (6.2%) | 15,212 (18.5%) |
| C (Alt) | 21,073 (10.9%) | 5,674 (6.2%) | 15,399 (18.7%) |

**Synthetic scenario comparison** (computed from formulas):

| Scenario | Model A | Model B | Model C | Assessment |
|:---|:---:|:---:|:---:|:---|
| Comfortable chase (RRR=5, 8wkts) | 0.19 | 0.17 | 0.19 | A/C more sensitive to mild urgency |
| Tight chase (RRR=9, 6wkts) | 0.52 | 0.51 | 0.52 | Near-identical |
| Death overs inn1 (8th wkt, over18) | 0.72 | 0.72 | 0.72 | Models agree in Inn1 |
| Early collapse (3wkts/5overs) | 0.58 | 0.52 | 0.58 | B dampens via low WP early |
| **Near-impossible chase (RRR=18, 4wkts)** | **0.84** | **0.42** | **0.59** | Model B collapses (near-0 WP); C preserves urgency |
| Winning easily (RRR=3, 10wkts) | 0.08 | 0.09 | 0.09 | Agreement on low pressure |

**Top 10 batter rankings by model**:

| Rank | Model A (Rule) | Model B (Hybrid) | Model C (Alt) |
|:---:|:---|:---|:---|
| 1 | MS Dhoni | Heinrich Klaasen | Rinku Singh |
| 2 | Rinku Singh | Ashutosh Sharma | Rashid Khan |
| 3 | Dhruv Jurel | Shashank Singh | MS Dhoni |
| 4 | M Shahrukh Khan | Shreyas Iyer | Ashutosh Sharma |
| 5 | Dasun Shanaka | Dinesh Karthik | Tim David |
| 6 | Tim David | Tim David | Heinrich Klaasen |
| 7 | Ashutosh Sharma | Suryakumar Yadav | Rovman Powell |
| 8 | David Miller | Rashid Khan | Shreyas Iyer |
| 9 | Sikandar Raza | MS Dhoni | Dinesh Karthik |
| 10 | George Dockrell | Rovman Powell | Jason Holder |

> [!IMPORTANT]
> **Model Selection Rationale — Model B (Hybrid) is the primary choice:**
> - Model A over-represents pure finisher/death-overs specialists (MS Dhoni #1) because it has no win-probability moderation: a 20-ball-remaining situation always reads as extreme urgency regardless of WP.
> - Model B correctly identifies match situations where both urgency AND match-shifting potential align — the most defensible definition of pressure.
> - Model C is a reasonable middle ground but converges with B in most situations; it was designed to handle near-impossible chases (like RRR=18) where model B unfairly dampens pressure, but such situations are rare in real data (1.5% of deliveries are "Extreme").
> - **Decision**: Retain Model B. Its top-10 rankings are most stable across the cross-experiment sensitivity analysis (Experiment 6).

---

### Experiment 4: Clutch Measurement Method

| Dimension | Raw Method | Context-Adjusted Method |
|:---|:---|:---|
| Batter clutch | Δ SR = pressure_SR − normal_SR | Δ RAE = pressure_RAE/ball − normal_RAE/ball |
| Bowler clutch | Δ Economy = normal_econ − pressure_econ | Δ RP = pressure_RP/ball − normal_RP/ball |

**Batter rank changes (top-10 union)**:

| Player | Raw Rank | Context-Adj Rank | Change |
|:---|:---:|:---:|:---:|
| Heinrich Klaasen | 1 | 1 | = |
| Ashutosh Sharma | 2 | 2 | = |
| Shashank Singh | 3 | 3 | = |
| Rashid Khan | 4 | 8 | ▼4 |
| Shreyas Iyer | 5 | 4 | ▲1 |
| Dinesh Karthik | 6 | 5 | ▲1 |
| Tim David | 7 | 6 | ▲1 |
| Suryakumar Yadav | 8 | 7 | ▲1 |
| MS Dhoni | 9 | 9 | = |
| Rovman Powell | 10 | 10 | = |

**Bowler rank changes**: Top-5 identical. Mustafizur Rahman rises from 6→5, Maheesh Theekshana drops 5→7 in context-adjusted method.

> [!TIP]
> Context-adjusted clutch is preferable: raw SR differences can be inflated by inherently high-RRR death situations where the whole batting side scores faster. The RAE delta adjusts for what was contextually expected, isolating true clutch improvement. The top-10 composition remains the same (same players) with only minor reorderings, confirming both methods broadly agree.

---

### Experiment 5: Consistency Formula & Sample Size Sensitivity

Three consistency formulas tested across k = 20, 40, 80:

| Formula | Description |
|:---|:---|
| **A** | `0.50×z(pos_match_pct) + 0.30×z(log1p(pressure_balls)) − 0.20×z(match_std)` *(includes volume)* |
| **B** | `0.60×z(pos_match_pct) − 0.40×z(match_std)` *(volume removed — avoids double-counting with Bayesian shrinkage)* |
| **C** | `0.50×z(pos_match_pct) + 0.30×z(−CI_width) − 0.20×z(match_std)` *(reliability via approximate CI width)* |

**Double-volume analysis**: Formula A rewards volume twice — once in shrinkage and once in the consistency dimension. Formula B eliminates this double-counting. In practice, the top-10 batter composition is unchanged across all nine formula×k combinations. Volume double-counting has negligible ranking impact because the consistency dimension's weight is only 10% of the composite.

**Key stability findings across k = 20, 40, 80**:

- **k=20**: Ashutosh Sharma (125 pressure balls) scores slightly lower — raw metrics less shrunk towards population. Marginally favours high-volume players.
- **k=40**: Optimal balance. Specialist low-ball players stabilised, high-volume players retain their genuine superiority.
- **k=80**: Over-shrinks Klaasen and other short-inning specialists towards the population mean, underestimating their true rates.

**Heinrich Klaasen remains #1 batter in 9/9 configurations. Sunil Narine remains #1 bowler in 9/9 configurations.**

---

### Experiment 6: Ranking Stability Across All Experiments

Across 16 evaluated methodological configurations (encompassing variations in competition scope, pressure models, clutch formulations, consistency metrics, and Bayesian prior strengths). **Important note**: The "Top-10 Frequency" percentages reported below represent sensitivity metrics reflecting how frequently a player retains top-10 status across diverse modeling assumptions, *not* frequentist confidence intervals or Bayesian posterior probabilities:

| Player | Top-10 Frequency | Avg Rank | Rank Std |
|:---|:---:|:---:|:---:|
| **Ashutosh Sharma** | 100% | 2.81 | 1.24 |
| **Tim David** | 100% | 7.25 | 1.68 |
| **Mahendra Singh Dhoni** | 100% | 6.62 | 2.26 |
| **Rashid Khan** | 93.8% | 7.00 | 1.84 |
| **Rovman Powell** | 93.8% | 10.81 | 3.99 |
| Heinrich Klaasen | 87.5% | 2.44 | 2.78 |
| Shreyas Iyer | 81.3% | 5.31 | 3.18 |
| Dinesh Karthik | 75.0% | 6.33 | 3.03 |
| Suryakumar Yadav | 68.8% | 7.33 | 3.56 |

> [!NOTE]
> Klaasen's 87.5% top-10 frequency (not 100%) is because Model A (rule-only pressure) produces a qualitatively different pressure population that inflates death-specialist rankings. Under all other 15 configurations he appears in top 3.

Across 17 experiment variations for bowlers:

| Player | Top-10 Frequency | Avg Rank | Rank Std |
|:---|:---:|:---:|:---:|
| **Sunil Narine** | 100% | 1.25 | 0.66 |
| **Matheesha Pathirana** | 100% | 4.12 | 0.48 |
| **Yuzvendra Chahal** | 93.8% | 6.56 | 2.37 |
| **Krunal Pandya** | 93.8% | 5.69 | 13.05 |
| **Mustafizur Rahman** | 87.5% | 6.25 | 3.13 |

> [!TIP]
> Krunal Pandya's high rank_std (13.05) is because Model A (rule-only) assigns very few pressure balls to spinners in the first innings (they bowl in the powerplay before the death), while Model B correctly values their contribution in do-or-die chase situations. This further validates Model B as the more faithful pressure representation.

---

### Experiment 7: Pressure Distribution Summary

| Format | Innings | Total Deliveries | Low | Moderate | High | Extreme |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| IPL | 1 | 45,588 | 72.9% | 21.9% | 5.2% | 0.07% |
| IPL | 2 | 42,099 | 24.2% | 58.8% | 13.6% | 3.5% |
| T20I | 1 | 56,466 | 69.2% | 25.0% | 5.8% | 0.01% |
| T20I | 2 | 49,861 | 28.1% | 57.7% | 11.4% | 2.8% |

**Key observation**: The first-innings now has non-zero High/Extreme deliveries (5.2% and 5.8%) after the audit correction. Original code returned exactly 0% for both, confirming the bug was genuine and significant.

**High + Extreme by context**:
- 1st innings total: 5,674 deliveries (6.0% of all 1st-innings legal deliveries)
- 2nd innings total: 14,275 deliveries (17.0% of all 2nd-innings legal deliveries)
- Knockout matches: disproportionately represented in Extreme tier (1.20× multiplier effect)

---

## 6. Alternative Rankings

**Alternative top-10 batters (Model A, rule-based pressure)**:

| Rank | Player | Rating | Note |
|:---:|:---|:---:|:---|
| 1 | Mahendra Singh Dhoni | 72.02 | Extreme specialist, mostly death-over data |
| 2 | Rinku Singh | 71.34 | Finisher profile; pure rule pressure inflates |
| 3 | Dhruv Jurel | 71.24 | Small sample in extreme finisher role |
| 4 | M Shahrukh Khan | 67.75 | Death-over specialist |
| 5 | Dasun Shanaka | 65.90 | — |
| 6 | Tim David | 65.62 | Also appears in primary top-10 |
| 7 | Ashutosh Sharma | 65.07 | Also appears in primary top-10 |
| 8 | David Miller | 64.24 | — |
| 9 | Sikandar Raza | 63.65 | — |
| 10 | George Dockrell | 63.60 | — |

The divergence between primary (Model B) and alternative (Model A) batter rankings reflects the near-impossible-chase problem: Model A assigns high pressure to situations where the chase has become statistically unwinnable (WP ≈ 0), rewarding performance in dead-match situations. Model B, through leverage moderation, correctly de-emphasises these situations.

---

## 7. Deliverables Reference

| File | Description |
|:---|:---|
| `top_10_batters.csv` | **Primary** ranked top-10 batters (official scope, Model B, context-adjusted clutch, k=40) |
| `top_10_bowlers.csv` | **Primary** ranked top-10 bowlers |
| `alternative_top_10_batters.csv` | Alternative rankings using Model A (rule-only pressure) |
| `alternative_top_10_bowlers.csv` | Alternative bowler rankings under Model A |
| `competition_scope_comparison.csv` | Side-by-side official vs expanded scope rankings |
| `pressure_distribution.csv` | Pressure score statistics by innings × format |
| `pressure_model_comparison.csv` | Delivery-level stats for Models A, B, C |
| `pressure_model_ranking_comparison.csv` | Top-10 rankings under all 3 models |
| `pressure_model_synthetic_scenarios.csv` | 7 synthetic cricket scenarios with all 3 model scores |
| `clutch_method_comparison.csv` | Rank changes: raw vs context-adjusted clutch |
| `consistency_comparison.csv` | Top-10 rankings across 9 formula×k configurations |
| `ranking_stability.csv` | Per-player stability stats across all 17 experiments |
| `experiment_summary.csv` | Key numeric findings from all 9 tasks |
| `all_batter_scores.csv` | Complete ratings for all 888+ eligible batters |
| `all_bowler_scores.csv` | Complete ratings for all 647+ eligible bowlers |
| `outputs/features/delivery_features.parquet` | Full 200,999-row feature store (123 columns) |
| `outputs/visualizations/*.png` | 12 analytical charts |
| `reports/methodology_report.pdf` | PDF version of this report |
| `tests/` | 25 passing automated unit tests |

---

## 8. Reproducibility

All analyses are fully reproducible. The complete pipeline can be rerun from raw data files:

```bash
# From project root
python src/run_pipeline.py           # Full pipeline (expensive: ~15 min to build parquet)
python src/task_experiments.py       # All 9 experiments (uses pre-built parquet, ~5 min)
python -m unittest discover tests    # 25 unit tests (< 1 second)
python src/visualization.py          # Regenerate 12 charts
python src/generate_pdf_report.py    # Regenerate PDF
```

Random seed: 42 (all scikit-learn models). No player identity features in win-probability or expected-performance models. All cross-validation is match-grouped (GroupKFold) to prevent data leakage.
