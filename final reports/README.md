# SupeRR Selector Season 2: Final Submission Directory & Reports

This directory consolidates the complete set of official deliverables, analytical methodology reports, experimental verification CSVs, and Rajasthan Royals IPL 2027 Auction strategic blueprints.

---

## 1. Official Primary Top 10 Rankings (Unstop Submission)

### Top 10 Batters Under Pressure
*(Scope: IPL + T20I, Model B Hybrid Pressure, Context-Adjusted Clutch, Bayesian Shrinkage $k=40$)*

| Rank | Player Name | Pressure Balls | Pressure SR | Baseline SR | $\Delta$ SR | RAE / Ball | Positive Match % | Matches | Pressure Rating |
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

### Top 10 Bowlers Under Pressure
*(Scope: IPL + T20I, Model B Hybrid Pressure, Context-Adjusted Clutch, Bayesian Shrinkage $k=40$)*

| Rank | Player Name | Pressure Balls | Wickets | Pressure Econ | Baseline Econ | $\Delta$ Econ | RP / Ball | Positive Match % | Matches | Pressure Rating |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1** | **Sunil Narine** | 130 | 10 | 6.09 | 6.94 | +0.84 | +0.343 | 88.9% | 18 | **77.83** |
| **2** | **Krunal Pandya** | 130 | 11 | 6.42 | 7.98 | +1.56 | +0.227 | 86.7% | 15 | **74.73** |
| **3** | **Rashid Khan** | 183 | 19 | 7.67 | 7.42 | -0.26 | +0.181 | 85.2% | 27 | **71.52** |
| **4** | **Matheesha Pathirana** | 206 | 21 | 8.83 | 8.86 | +0.03 | +0.350 | 82.1% | 28 | **69.35** |
| **5** | **Mustafizur Rahman** | 222 | 23 | 8.16 | 7.75 | -0.42 | +0.232 | 73.7% | 38 | **66.38** |
| **6** | **Yuzvendra Chahal** | 247 | 26 | 8.87 | 8.59 | -0.28 | -0.026 | 64.5% | 31 | **65.03** |
| **7** | **Maheesh Theekshana** | 161 | 11 | 7.49 | 7.79 | +0.30 | +0.177 | 72.0% | 25 | **64.60** |
| **8** | **Varun Chakravarthy** | 199 | 16 | 7.84 | 8.03 | +0.19 | +0.088 | 72.0% | 25 | **62.46** |
| **9** | **Jason Holder** | 227 | 22 | 9.36 | 8.95 | -0.40 | +0.095 | 81.6% | 38 | **62.21** |
| **10** | **Ravichandran Ashwin** | 128 | 10 | 8.39 | 7.81 | -0.58 | +0.040 | 68.8% | 16 | **61.61** |

---

## 2. Directory Manifest & Deliverables

| Deliverable File | Type | Description |
|:---|:---|:---|
| `top_10_batters.csv` | CSV | Primary official Top 10 Batters ranking for Unstop dropdowns |
| `top_10_bowlers.csv` | CSV | Primary official Top 10 Bowlers ranking for Unstop dropdowns |
| `methodology_report.pdf` | PDF | Publication-grade 6-page submission PDF report with all embedded high-res figures |
| `methodology_report.md` | Markdown | Complete source text for the official Round 1 methodology report |
| `final_validation_summary.md` | Markdown | Consolidated audit and validation summary across all 14 experiment CSVs |
| `rajasthan_royals_ipl2027_report.pdf` | PDF | Executive intelligence brief for RR IPL 2027 Mega-Auction strategy |
| `rajasthan_royals_ipl2027_auction_blueprint.pptx` | PPTX | 14-slide Neobrutalism presentation deck evaluating all 20 players for RR |
| `rajasthan_royals_ipl2027_auction_strategy_report.md` | Markdown | Detailed strategic dossier mapping pressure players to RR squad roles |
| `rr_auction_dashboard.html` | HTML | Interactive, standalone data dashboard with charts, filters, and player cards |
| `competition_scope_comparison.csv` | CSV | Official (IPL+T20I) vs Expanded scope ranking sensitivity |
| `pressure_distribution.csv` | CSV | Delivery-level score distributions by innings and competition |
| `pressure_model_comparison.csv` | CSV | Delivery counts and tier stats for Models A, B, and C |
| `pressure_model_ranking_comparison.csv` | CSV | Top-10 rankings under rule-based, hybrid, and alternative pressure |
| `pressure_model_synthetic_scenarios.csv` | CSV | Scores for 7 archetypal cricket game states |
| `clutch_method_comparison.csv` | CSV | Raw delta vs Context-adjusted clutch rankings |
| `consistency_comparison.csv` | CSV | Top-10 rankings across 9 formula $\times$ prior strength configurations |
| `ranking_stability.csv` | CSV | Per-player cross-model stability metrics across 16 experiment variants |
| `experiment_summary.csv` | CSV | Quantitative metrics summarizing all 9 robustness tasks |
| `alternative_top_10_batters.csv` | CSV | Benchmark rankings under Model A (pure situational urgency) |
| `alternative_top_10_bowlers.csv` | CSV | Benchmark bowler rankings under Model A |
