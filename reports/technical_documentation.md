# SupeRR Selector Season 2: Technical System Documentation (Audited)
## Architecture, Mathematical Formulations, and API Reference

### 1. Overview and Design Principles

The Pressure Performance Analytics platform is built upon a modular, layered architecture adhering to the following design constraints:
- **Strict Temporal Causality**: Feature engineering strictly guarantees that all variables representing pre-delivery match state use only information recorded before that delivery.
- **Bi-Innings Asymmetry & Calibrated 1st Innings Pressure**: Chasing pressure (Innings 2) and target-setting pressure (Innings 1) utilize specialized mathematical formulations to avoid meaningless Required Run Rate computations in Innings 1, while accurately capturing early top-order collapses and death-over scoring demands.
- **Out-of-Fold Evaluation**: Contextual expected performance metrics are trained using 5-fold match-level grouped cross-validation (`GroupKFold` by `match_id`), completely eliminating in-sample bias.
- **Empirical Bayes Shrinkage**: All rate metrics (RAE/ball, Strike Rate, Runs Prevented/ball, Economy) are shrunk toward empirical population priors with prior strength $k=40$ balls.

---

### 2. Codebase Organization

```
project/
├── data/                               # Staged source CSV datasets
│   ├── ball_by_ball.csv
│   ├── competition_team_player_mapping.csv
│   ├── competitions.csv
│   ├── matches.csv
│   ├── playing_eleven.csv
│   └── teams.csv
├── src/                                # Reusable analytical modules
│   ├── data_loader.py                  # Dataset ingestion and type parsing
│   ├── data_validation.py              # Domain rules and integrity verification
│   ├── data_integration.py             # Match and competition metadata integration
│   ├── match_state.py                  # Cumulative match-state reconstruction
│   ├── feature_engineering.py          # 1st innings par score and player progressions
│   ├── win_probability.py              # ML Win Probability, WPA, and Leverage Index
│   ├── pressure_models.py              # Rule-based, leverage, and hybrid pressure models
│   ├── expected_performance.py         # Out-of-fold contextual expectation models
│   ├── batting_engine.py               # Independent batting rating engine
│   ├── bowling_engine.py               # Independent bowling rating engine
│   ├── reliability.py                  # Empirical Bayes shrinkage and uncertainty
│   ├── ranking.py                      # Multi-dimensional composite scoring
│   ├── experiments.py                  # Stage 9 validation experiments suite
│   ├── visualization.py                # Publication-quality figure generator
│   ├── generate_pdf_report.py          # PDF methodology report generator
│   └── run_pipeline.py                 # Master end-to-end execution pipeline
├── outputs/
│   ├── data_audit/                     # Schema reports, dictionaries, ER diagrams
│   ├── features/                       # Parquet delivery feature store
│   ├── models/                         # Experimentation logs and CSVs
│   ├── player_scores/                  # Full batter and bowler score tables
│   ├── final_rankings/                 # Official Top 10 lists and ranked tables
│   └── visualizations/                 # 12 analytical publication PNG charts
├── reports/
│   ├── methodology_report.md           # Full Markdown methodology document
│   ├── methodology_report.pdf          # Professional 3-page styled PDF document
│   └── technical_documentation.md      # This technical reference
├── tests/                              # Unit testing suite
│   ├── test_match_state.py             # Match state reconstruction tests
│   ├── test_scoring.py                 # Cricket scoring and dismissal attribution tests
│   ├── test_pressure.py                # Pressure formulas and threshold tests
│   ├── test_player_ratings.py          # Shrinkage and ranking property tests
│   └── test_comprehensive_audit.py     # 18 expanded domain edge case tests
├── requirements.txt                    # Project dependency specification
└── README.md                           # Quickstart guide
```

---

### 3. Mathematical Specifications

#### 3.1 Cumulative Match-State Progression
For a delivery $t$ in match $m$ and innings $i$:
$$\text{post\_current\_score}_t = \sum_{k=1}^t \text{total\_ball\_runs}_k$$
$$\text{pre\_current\_score}_t = \text{post\_current\_score}_t - \text{total\_ball\_runs}_t$$
$$\text{pre\_wickets\_lost}_t = \sum_{k=1}^{t-1} \mathbb{I}(\text{is\_wicket}_k = \text{True})$$
$$\text{pre\_legal\_balls\_completed}_t = \sum_{k=1}^{t-1} \mathbb{I}(\text{extras\_type}_k \notin \{\text{wide, Overstep, other}\})$$

#### 3.2 Second Innings Required Run Rate
$$\text{runs\_needed}_t = \max(0, \text{target} - \text{pre\_current\_score}_t)$$
$$\text{RRR}_t = \frac{\text{runs\_needed}_t}{\max(1, \text{scheduled\_legal\_balls} - \text{pre\_legal\_balls\_completed}_t)} \times 6.0$$

#### 3.3 Hybrid Pressure Model ($PI$)
For chases ($i \ge 2$):
$$PI_{\text{chase}} = 0.40 \cdot \text{clip}\left(\frac{\text{RRR} - 6.0}{8.0}, 0, 1.5\right) + 0.30 \cdot \text{clip}\left(\frac{\text{wickets\_lost}}{8.0}, 0, 1.25\right) + 0.20 \cdot \text{Ball\_Scarcity} + 0.10 \cdot \mathbb{I}(\text{death close})$$
Where $\text{Ball\_Scarcity} = 1.0 - \left(\frac{\text{pre\_legal\_balls\_remaining}}{\text{scheduled\_legal\_balls}}\right)$.
$$PI_{\text{hybrid}} = 0.50 \cdot PI_{\text{chase}} + 0.50 \cdot \text{clip}\left(\frac{\text{Leverage Index}}{2.0}, 0, 1.5\right)$$
For Innings 1:
$$PI_{\text{inn1}} = 0.50 \cdot \max(\text{Collapse Intensity}, \text{Death Urgency}) + 0.30 \cdot \text{Wicket Scarcity} + 0.20 \cdot \text{Par Deficit}$$
Knockout multiplier: $\times 1.20$ if `knock_out == 1`.

#### 3.4 Contextual Expected Performance
Using `HistGradientBoosting` models:
$$\text{RAE}_t = \text{runs}_t - \hat{y}_{\text{bat\_runs}}(\mathbf{x}_t^{\text{pre}})$$
$$\text{RP}_t = \hat{y}_{\text{bowl\_runs}}(\mathbf{x}_t^{\text{pre}}) - \text{bowler\_conceded\_runs}_t$$
$$\text{WAE}_t = \mathbb{I}(\text{is\_bowler\_wicket}_t) - \hat{P}(\text{is\_bowler\_wicket}_t \mid \mathbf{x}_t^{\text{pre}})$$

#### 3.5 Empirical Bayes Shrinkage
$$\text{Shrunk Score}_p = \frac{n_p}{n_p + k} \cdot \bar{X}_p + \frac{k}{n_p + k} \cdot \mu_{\text{pop}}, \quad k = 40.0$$

#### 3.6 Final Composite Rating
$$\text{Composite Score}_p = 0.60 \cdot z(S_{\text{perf}}) + 0.30 \cdot z(S_{\text{clutch}}) + 0.10 \cdot z(S_{\text{cons}})$$
$$\text{Pressure Rating}_p = 50.0 + 15.0 \cdot \text{Composite Score}_p$$

---

### 4. Running the Complete System

```bash
# Verify unit tests (25 tests)
python -m unittest discover tests

# Run master end-to-end pipeline
python src/run_pipeline.py

# Run all 8 robustness experiments
python src/experiments.py

# Generate all 12 analytical visualizations
python src/visualization.py

# Compile styled PDF report
python src/generate_pdf_report.py
```
