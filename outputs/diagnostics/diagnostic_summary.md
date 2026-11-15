# SupeRR Selector Season 2: P0 Diagnostic Suite Report

This document reports empirical findings from the 6 diagnostic evaluations performed on the official scope (IPL + T20I: 194,014 deliveries; 87,687 IPL deliveries, 106,327 T20I deliveries).

---

## 1. Diagnostic Findings Summary

1. **Optimal Empirical Bayes Shrinkage ($k^* \approx 2212$ vs current $k = 40$)**:
   - At current $k = 40$, a player with 120 balls receives only **25.0%** shrinkage toward the population mean (75.0% weight retained on observed sample).
   - Across all 40 eligible batters, current $k=40$ produces an average shrinkage of **20.2%** (mean observed weight = 0.798).
   - With empirically estimated noise variance $\sigma_e^2 = 3.195$ and true talent variance $\sigma_u^2 = 0.00144$, the theoretical optimal shrinkage strength is $k^* \approx 2212$.
   - At $k^* = 2212$, a batter with 120 balls receives **94.8%** shrinkage (optimal: 95%), and the average shrinkage across eligible batters is **92.9%**.
   - **Rank Reshuffling**: Comparing $k=40$ against $k=2212$ yields Kendall $\tau = 0.9103$ and Spearman $\rho = 0.9859$. Crucially, high-sample veterans rise to the very top: **Tim David** (300 balls) moves from #2 to #1 and **Suryakumar Yadav** (254 balls) moves from #4 to #2, whereas small-sample outlier **Heinrich Klaasen** (122 balls) drops from #1 to #3.

### Shrinkage Sensitivity Table (`outputs/diagnostics/shrinkage_sensitivity.csv`)
| $k$ | Mean Weight on Observed ($w$) | Mean Shrinkage ($1-w$) | Shrinkage at $n=120$ | Kendall $\tau$ vs $k=40$ | Spearman $\rho$ vs $k=40$ | Top-10 Overlap |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 20 | 0.887 | 11.3% | 14.3% | 0.9923 | 0.9994 | 10 / 10 |
| 40 | 0.798 | 20.2% | 25.0% | 1.0000 | 1.0000 | 10 / 10 |
| 80 | 0.666 | 33.4% | 40.0% | 0.9872 | 0.9989 | 10 / 10 |
| 150 | 0.519 | 48.1% | 55.6% | 0.9744 | 0.9974 | 10 / 10 |
| 500 | 0.249 | 75.1% | 80.6% | 0.9256 | 0.9893 | 10 / 10 |
| 1000 | 0.144 | 85.6% | 89.3% | 0.9179 | 0.9878 | 10 / 10 |
| 2212 | 0.071 | 92.9% | 94.8% | 0.9103 | 0.9859 | 10 / 10 |

---

## 2. Split-Half Reliability (`outputs/diagnostics/split_half_reliability.csv`)

Evaluated by partitioning matches into odd and even match chronological indices per player, filtering to players with $\ge 30$ balls in each half, with 200 player-bootstrap resamples:

| Discipline | Eligible Players ($n$) | Pearson Correlation ($r$) | Spearman-Brown Reliability ($r_{SB}$) | 95% Bootstrap Confidence Interval |
|:---|:---:|:---:|:---:|:---:|
| **Batting** | 68 | **0.084** | **0.155** | [-0.3007, 0.4758] |
| **Bowling** | 89 | **0.1567** | **0.2709** | [-0.124, 0.5036] |

- **Scientific Reality**: The split-half reliability of batting pressure RAE is **$r_{SB} = 0.155$** ($r = 0.084$), with a 95% CI spanning zero ([-0.30, 0.48]). Bowling is similarly noisy ($r_{SB} = 0.271$, 95% CI [-0.12, 0.50]).
- Over 84% of the observed between-player variation in pressure RAE per ball in sample sizes of 60–150 deliveries is stochastic noise rather than stable, repeatable talent.

---

## 3. Pressure Dose-Response Analysis (`outputs/diagnostics/pressure_dose_response.csv`)

| Pressure Decile | All Innings RAE/ball | All Innings Dismissal Rate | Innings 1 RAE/ball | Innings 1 Dismissal Rate | Innings 2 RAE/ball | Innings 2 Boundary Rate |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Decile 1 (Low) | +0.0777 | 4.65% | +0.0774 | 4.64% | +0.1387 | 25.98% |
| Decile 2 | +0.0527 | 4.69% | +0.0317 | 4.52% | +0.1197 | 21.32% |
| Decile 3 | +0.0487 | 4.92% | +0.0644 | 4.87% | +0.0083 | 19.28% |
| Decile 4 | +0.0531 | 4.94% | +0.0595 | 5.03% | +0.0416 | 19.64% |
| Decile 5 | +0.0591 | 4.93% | +0.0507 | 5.04% | +0.0688 | 19.34% |
| Decile 6 | +0.0582 | 4.79% | +0.0395 | 4.90% | +0.0729 | 18.73% |
| Decile 7 | +0.0566 | 5.47% | +0.0207 | 5.45% | +0.0750 | 19.01% |
| Decile 8 | +0.0512 | 5.72% | +0.0653 | 6.54% | +0.0474 | 18.91% |
| Decile 9 | +0.0559 | 6.94% | +0.0623 | 8.34% | +0.0539 | 16.90% |
| Decile 10 (High) | +0.0888 | 8.98% | +0.1159 | 12.73% | +0.0784 | 18.76% |

- **Dismissal Dose-Response**: Strongly positive and monotonic (Spearman $\rho = 0.9152$, $p = 0.0002$ across all innings; $\rho = 0.9515$, $p < 0.0001$ in Innings 1). Wickets climb from 4.65% in decile 1 to 8.98% overall (and 12.73% in Innings 1 extreme pressure).
- **RAE Dose-Response**: Batter run production relative to expectations does **not** exhibit a clear monotonic trend with pressure (Spearman $\rho = 0.2000$, $p = 0.58$ overall; $\rho = -0.1636$, $p = 0.65$ in Innings 2).
- **Chasing Boundary Suppression**: In Innings 2, boundary rate drops monotonically as pressure escalates (Spearman $\rho = -0.8667$, $p = 0.0012$), falling from 26.0% in decile 1 to under 18.8% under high pressure.

---

## 4. Multicollinearity & Redundancy Check (`batting_redundancy_vif.csv` & `bowling_redundancy_vif.csv`)

### Batting Features
- `pressure_sr`: **VIF = 21.43** (Severe redundancy with RAE and boundary percentage)
- `pressure_rae_per_ball`: **VIF = 9.62**
- `pressure_bnd_pct`: **VIF = 8.53**
- `pressure_wpa_per_ball`: **VIF = 1.42** (Independent signal)
- `pressure_dot_pct`: **VIF = 1.39** (Independent signal)

### Bowling Features
- `pressure_economy`: **VIF = 43.43** (Extremely high collinearity with boundary conceded %)
- `pressure_bnd_conceded_pct`: **VIF = 30.26**
- `pressure_rp_per_ball`: **VIF = 7.30**
- `pressure_dot_pct`: **VIF = 4.94**
- `pressure_wpa_per_ball`: **VIF = 2.29**

Including both Strike Rate / Economy alongside RAE / Runs Prevented creates massive double-counting.

---

## 5. Dismissal Cost Impact (`outputs/diagnostics/dismissal_impact.csv`)

Adjusted RAE formulation: $\text{adjusted\_rae} = \text{pressure\_rae\_per\_ball} - 10.0 \times \text{dismissal\_rate\_per\_ball}$.
Across all 40 eligible batters:
- **32** of 40 batters shifted by $\ge 3$ rank positions.
- **16** of 40 batters experienced massive rank shifts of $\ge 10$ positions.

### Major Rank Shifts
| Player | Pressure Balls | Pressure Dismissal Rate | Normal Dismissal Rate | Dismissal Delta | Original Rank | Adjusted Rank | Shift |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Shashank Singh** | 107 | 3.74% | 4.42% | -0.68% | #7 | **#1** | **+6** |
| **Hardik Pandya** | 238 | 3.36% | 4.80% | -1.44% | #36 | **#6** | **+30** |
| **Dhruv Jurel** | 184 | 4.35% | 5.37% | -1.03% | #29 | **#7** | **+22** |
| **Rahul Tewatia** | 205 | 4.88% | 6.90% | -2.02% | #26 | **#10** | **+16** |
| **Heinrich Klaasen** | 122 | 8.20% | 3.78% | +4.41% | #1 | **#5** | **-4** |
| **Ashutosh Sharma** | 119 | 9.24% | 4.19% | +5.06% | #5 | **#19** | **-14** |
| **Andre Russell** | 145 | 11.03% | 4.93% | +6.10% | #13 | **#34** | **-21** |
| **Rashid Khan** | 179 | 11.73% | 7.62% | +4.11% | #10 | **#36** | **-26** |

High boundary hitters with excessive dismissal rates under pressure suffer severe penalties when wickets are appropriately costed.

---

## 6. Innings Asymmetry (`outputs/diagnostics/innings_asymmetry.csv`)

- **Innings High-Pressure Incidence**:
  - Innings 1 balls classified as high-pressure: **5.56%**
  - Innings 2 balls classified as high-pressure: **15.52%** (nearly 3x higher!)
  - Total high-pressure volume share: **Innings 1 = 28.44%** vs **Innings 2 = 71.56%**.
- **Cross-Innings Consistency**:
  - Evaluated on all 62 batters with $\ge 20$ pressure deliveries in each innings.
  - Pearson correlation between Innings 1 RAE and Innings 2 RAE across players: **$r = 0.0011$** ($p = 0.9934$).
  - Performance under pressure in setting a total (Innings 1) has **zero statistical correlation** with performance under pressure in a chase (Innings 2).

---

## 7. Bowler Baseline Anomaly Verification (`outputs/diagnostics/bowler_economy_anomaly.csv`)

- **5 of the Top 10 Bowlers** have a worse economy rate under pressure than in neutral situations:
  - **Rashid Khan**: Normal Economy 7.42 $\rightarrow$ Pressure Economy 7.67 ($\Delta = -0.26$)
  - **Mustafizur Rahman**: Normal Economy 7.75 $\rightarrow$ Pressure Economy 8.16 ($\Delta = -0.42$)
  - **Yuzvendra Chahal**: Normal Economy 8.59 $\rightarrow$ Pressure Economy 8.87 ($\Delta = -0.28$)
  - **Jason Holder**: Normal Economy 8.95 $\rightarrow$ Pressure Economy 9.36 ($\Delta = -0.40$)
  - **Ravichandran Ashwin**: Normal Economy 7.81 $\rightarrow$ Pressure Economy 8.39 ($\Delta = -0.58$)
- These bowlers were elevated to the top 10 purely by cumulative WPA and raw wickets rather than defensive run suppression under pressure.

---
*Report generated automatically by `src/diagnostics.py`.*
