# SupeRR Selector Season 2: Pressure Performance Analytics (Audited)

A data-driven cricket analytics system designed to identify and rank the **Most Reliable Players Under Pressure** across historical IPL and T20 International data from 2022 to 2026.

---

## Official Final Deliverables

### 1. Top 10 Batters Under Pressure
| Rank | Batter Name | Pressure Balls | Runs | Strike Rate | Normal SR | Delta (&Delta;SR) | Runs Above Exp / Ball | Pressure Rating |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | **Heinrich Klaasen** | 122 | 249 | 204.10 | 163.24 | **+40.86** | **+0.611** | **76.97** |
| **2** | **Ashutosh Sharma** | 125 | 242 | 193.60 | 150.90 | **+42.70** | **+0.422** | **70.63** |
| **3** | **Shashank Singh** | 107 | 215 | 200.93 | 152.32 | **+48.62** | **+0.414** | **68.98** |
| **4** | **Shreyas Iyer** | 169 | 324 | 191.72 | 149.29 | **+42.42** | **+0.430** | **68.00** |
| **5** | **Tim David** | 300 | 584 | 194.67 | 172.14 | **+22.53** | **+0.467** | **66.44** |
| **6** | **Dinesh Karthik** | 129 | 253 | 196.12 | 160.00 | **+36.12** | **+0.368** | **66.35** |
| **7** | **Rashid Khan** | 179 | 329 | 183.80 | 140.85 | **+42.95** | **+0.344** | **66.31** |
| **8** | **Suryakumar Yadav** | 254 | 484 | 190.55 | 163.98 | **+26.57** | **+0.413** | **66.30** |
| **9** | **Mahendra Singh Dhoni** | 127 | 230 | 181.10 | 137.80 | **+43.30** | **+0.226** | **66.12** |
| **10** | **Rovman Powell** | 181 | 322 | 177.90 | 142.67 | **+35.23** | **+0.310** | **63.26** |

### 2. Top 10 Bowlers Under Pressure
| Rank | Bowler Name | Pressure Balls | Wickets | Pressure Econ | Normal Econ | Delta (&Delta;Econ) | Runs Prevented / Ball | Pressure Rating |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | **Sunil Narine** | 130 | 10 | 6.09 | 6.94 | **+0.84** | **+0.343** | **77.83** |
| **2** | **Krunal Pandya** | 130 | 11 | 6.42 | 7.98 | **+1.56** | **+0.227** | **74.73** |
| **3** | **Rashid Khan** | 183 | 19 | 7.67 | 7.42 | **-0.26** | **+0.181** | **71.52** |
| **4** | **Matheesha Pathirana** | 206 | 21 | 8.83 | 8.86 | **+0.03** | **+0.350** | **69.35** |
| **5** | **Mustafizur Rahman** | 222 | 23 | 8.16 | 7.75 | **-0.42** | **+0.232** | **66.38** |
| **6** | **Yuzvendra Chahal** | 247 | 26 | 8.87 | 8.59 | **-0.28** | **-0.026** | **65.03** |
| **7** | **Maheesh Theekshana** | 161 | 11 | 7.49 | 7.79 | **+0.30** | **+0.177** | **64.60** |
| **8** | **Varun Chakravarthy** | 199 | 16 | 7.84 | 8.03 | **+0.19** | **+0.088** | **62.46** |
| **9** | **Jason Holder** | 227 | 22 | 9.36 | 8.95 | **-0.40** | **+0.095** | **62.21** |
| **10** | **Ravichandran Ashwin** | 128 | 10 | 8.39 | 7.81 | **-0.58** | **+0.040** | **61.61** |

---

## Submission Artifacts

- **Rankings Files**: `top_10_batters.csv`, `top_10_bowlers.csv`
- **Methodology Reports**: `methodology_report.md`, `methodology_report.pdf`
- **Quality & Audit Reports**: `data_quality_report.md`, `outputs/data_audit/schema_report.md`
- **Feature Store**: `outputs/features/delivery_features.parquet`
- **Score Data**: `all_batter_scores.csv`, `all_bowler_scores.csv`, `pressure_analysis.csv`
- **Visualizations**: 12 publication-grade figures in `outputs/visualizations/`
- **Automated Tests**: 25 unit tests in `tests/`

---

## Reproduction Guide

```bash
# Install dependencies
pip install -r requirements.txt

# Execute unit tests
python -m unittest discover tests

# Run master pipeline
python src/run_pipeline.py

# Run validation experiments
python src/experiments.py

# Generate visualizations
python src/visualization.py

# Compile PDF report
python src/generate_pdf_report.py
```

# IPL-RR-Challenge
