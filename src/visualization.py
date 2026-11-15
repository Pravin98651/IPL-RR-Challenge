"""
Visualization Module for SupeRR Selector Season 2.
Generates publication-quality figures supporting the analysis and methodology report.
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300

os.makedirs('outputs/visualizations', exist_ok=True)

def generate_all_visualizations():
    print("Generating 12 publication-quality analytical visualizations...")
    df = pd.read_parquet('outputs/features/delivery_features.parquet')
    top_bat = pd.read_csv('outputs/final_rankings/top_10_batters.csv')
    top_bowl = pd.read_csv('outputs/final_rankings/top_10_bowlers.csv')
    all_bat = pd.read_csv('outputs/player_scores/all_batter_scores.csv')
    all_bowl = pd.read_csv('outputs/player_scores/all_bowler_scores.csv')
    
    # -------------------------------------------------------------
    # 1. Pressure Score Distribution
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df['pressure_score'], bins=50, kde=True, color='#1E88E5', ax=ax, edgecolor='white', alpha=0.7)
    ax.axvline(0.60, color='#D81B60', linestyle='--', linewidth=2, label='High Pressure Threshold (0.60)')
    ax.axvline(0.85, color='#8E24AA', linestyle=':', linewidth=2, label='Extreme Pressure Threshold (0.85)')
    ax.set_title('Distribution of Delivery-Level Pressure Scores (N = 200,999 Deliveries)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Hybrid Pressure Score', fontsize=10)
    ax.set_ylabel('Delivery Count', fontsize=10)
    ax.legend(frameon=True)
    plt.tight_layout()
    plt.savefig('outputs/visualizations/01_pressure_score_distribution.png')
    plt.close()
    print(" - Saved 01_pressure_score_distribution.png")

    # -------------------------------------------------------------
    # 2. Distribution of Pressure Situations (Tiers)
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 5))
    tier_counts = df['pressure_tier'].value_counts()[['Low', 'Moderate', 'High', 'Extreme']]
    colors = ['#4CAF50', '#FFC107', '#FF9800', '#F44336']
    bars = ax.bar(tier_counts.index, tier_counts.values, color=colors, edgecolor='black', alpha=0.85)
    for bar in bars:
        h = bar.get_height()
        ax.annotate(f'{h:,}\n({h/len(df)*100:.1f}%)',
                    xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 4), textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, fontweight='bold')
    ax.set_title('Match Deliveries by Pressure Tier Classification', fontsize=12, fontweight='bold')
    ax.set_xlabel('Pressure Tier', fontsize=10)
    ax.set_ylabel('Total Deliveries', fontsize=10)
    ax.set_ylim(0, max(tier_counts.values) * 1.18)
    plt.tight_layout()
    plt.savefig('outputs/visualizations/02_pressure_tier_distribution.png')
    plt.close()
    print(" - Saved 02_pressure_tier_distribution.png")

    # -------------------------------------------------------------
    # 3. Required Run Rate vs Pressure Score
    # -------------------------------------------------------------
    chase = df[df['innings'] >= 2].dropna(subset=['rrr_pre'])
    chase_sample = chase.sample(min(10000, len(chase)), random_state=42)
    fig, ax = plt.subplots(figsize=(8, 5))
    scatter = ax.scatter(chase_sample['rrr_pre'], chase_sample['pressure_score'],
                         c=chase_sample['pre_wickets_lost'], cmap='viridis', alpha=0.4, s=15)
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Wickets Lost Prior to Delivery', fontsize=9)
    ax.axhline(0.60, color='#D81B60', linestyle='--', label='High Pressure Cutoff')
    ax.set_xlim(0, 24)
    ax.set_ylim(0, 1.4)
    ax.set_title('Required Run Rate vs Pressure Score (Chasing Innings)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Required Run Rate (RRR)', fontsize=10)
    ax.set_ylabel('Calculated Pressure Score', fontsize=10)
    ax.legend(loc='lower right', frameon=True)
    plt.tight_layout()
    plt.savefig('outputs/visualizations/03_rrr_vs_pressure_score.png')
    plt.close()
    print(" - Saved 03_rrr_vs_pressure_score.png")

    # -------------------------------------------------------------
    # 4. Win Probability vs Match Situation
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 5))
    balls_bins = np.linspace(0, 120, 13)
    chase_binned = chase.copy()
    chase_binned['ball_bin'] = pd.cut(chase_binned['pre_legal_balls_completed'], bins=balls_bins)
    wp_trend = chase_binned.groupby(['ball_bin', 'pre_wickets_lost'], observed=False)['wp_pre'].mean().unstack()
    for col in [0, 2, 4, 6, 8]:
        if col in wp_trend.columns:
            ax.plot(range(len(wp_trend)), wp_trend[col], marker='o', label=f'{col} Wickets Lost', linewidth=2)
    ax.set_xticks(range(len(wp_trend)))
    ax.set_xticklabels([f'{int(b.left)}-{int(b.right)}' for b in wp_trend.index], rotation=45, ha='right', fontsize=8)
    ax.set_title('Expected Win Probability Evolution by Balls Completed & Wickets Lost', fontsize=12, fontweight='bold')
    ax.set_xlabel('Legal Balls Completed in Innings', fontsize=10)
    ax.set_ylabel('Average Win Probability (Batting Team)', fontsize=10)
    ax.legend(title='Wickets Down', frameon=True)
    plt.tight_layout()
    plt.savefig('outputs/visualizations/04_win_probability_vs_match_situation.png')
    plt.close()
    print(" - Saved 04_win_probability_vs_match_situation.png")

    # -------------------------------------------------------------
    # 5. Pressure vs Normal Performance (Scatter)
    # -------------------------------------------------------------
    elig_bat = all_bat[all_bat['pressure_balls'] >= 80].copy()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))
    
    # Batters: Normal SR vs Pressure SR
    ax1.scatter(elig_bat['normal_sr'], elig_bat['pressure_sr'], color='#1E88E5', alpha=0.7, edgecolors='black')
    lims1 = [100, 210]
    ax1.plot(lims1, lims1, 'r--', label='Equal Performance (Delta = 0)')
    # Highlight top 3
    for idx, r in top_bat.head(5).iterrows():
        ax1.annotate(r['striker_name'], (r['normal_sr'], r['pressure_sr']), fontsize=8, fontweight='bold',
                     xytext=(5, 2), textcoords='offset points', color='#D81B60')
    ax1.set_title('Batters: Normal SR vs Pressure SR', fontsize=11, fontweight='bold')
    ax1.set_xlabel('Normal Situation Strike Rate', fontsize=10)
    ax1.set_ylabel('High Pressure Strike Rate', fontsize=10)
    ax1.legend(frameon=True)
    
    # Bowlers: Normal Economy vs Pressure Economy
    elig_bowl = all_bowl[all_bowl['pressure_legal_balls'] >= 90].copy()
    ax2.scatter(elig_bowl['normal_economy'], elig_bowl['pressure_economy'], color='#43A047', alpha=0.7, edgecolors='black')
    lims2 = [5, 12]
    ax2.plot(lims2, lims2, 'r--', label='Equal Economy (Delta = 0)')
    for idx, r in top_bowl.head(5).iterrows():
        ax2.annotate(r['bowler_name'], (r['normal_economy'], r['pressure_economy']), fontsize=8, fontweight='bold',
                     xytext=(5, 2), textcoords='offset points', color='#004D40')
    ax2.set_title('Bowlers: Normal Economy vs Pressure Economy', fontsize=11, fontweight='bold')
    ax2.set_xlabel('Normal Situation Economy Rate', fontsize=10)
    ax2.set_ylabel('High Pressure Economy Rate', fontsize=10)
    ax2.legend(frameon=True)
    
    plt.tight_layout()
    plt.savefig('outputs/visualizations/05_pressure_vs_normal_performance.png')
    plt.close()
    print(" - Saved 05_pressure_vs_normal_performance.png")

    # -------------------------------------------------------------
    # 6. Batter Clutch Performance Comparison (Top 10)
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 5.5))
    x = np.arange(len(top_bat))
    width = 0.35
    ax.bar(x - width/2, top_bat['normal_sr'], width, label='Normal SR', color='#90CAF9', edgecolor='black')
    ax.bar(x + width/2, top_bat['pressure_sr'], width, label='Pressure SR', color='#1E88E5', edgecolor='black')
    ax.set_xticks(x)
    ax.set_xticklabels(top_bat['striker_name'], rotation=35, ha='right', fontsize=9, fontweight='bold')
    ax.set_title('Top 10 Batters: Baseline Strike Rate vs High-Pressure Strike Rate', fontsize=12, fontweight='bold')
    ax.set_ylabel('Strike Rate', fontsize=10)
    ax.legend(frameon=True)
    plt.tight_layout()
    plt.savefig('outputs/visualizations/06_batter_clutch_comparison.png')
    plt.close()
    print(" - Saved 06_batter_clutch_comparison.png")

    # -------------------------------------------------------------
    # 7. Bowler Clutch Performance Comparison (Top 10)
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 5.5))
    x = np.arange(len(top_bowl))
    ax.bar(x - width/2, top_bowl['normal_economy'], width, label='Normal Economy', color='#A5D6A7', edgecolor='black')
    ax.bar(x + width/2, top_bowl['pressure_economy'], width, label='Pressure Economy', color='#2E7D32', edgecolor='black')
    ax.set_xticks(x)
    ax.set_xticklabels(top_bowl['bowler_name'], rotation=35, ha='right', fontsize=9, fontweight='bold')
    ax.set_title('Top 10 Bowlers: Baseline Economy vs High-Pressure Economy', fontsize=12, fontweight='bold')
    ax.set_ylabel('Economy Rate (Runs/Over)', fontsize=10)
    ax.legend(frameon=True)
    plt.tight_layout()
    plt.savefig('outputs/visualizations/07_bowler_clutch_comparison.png')
    plt.close()
    print(" - Saved 07_bowler_clutch_comparison.png")

    # -------------------------------------------------------------
    # 8. Sample Size Distribution
    # -------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    sns.histplot(all_bat['pressure_balls'], bins=40, color='#3949AB', ax=ax1, edgecolor='white')
    ax1.axvline(100, color='red', linestyle='--', label='Batting Cutoff (100 balls)')
    ax1.set_title('Batters: Pressure Balls Faced Sample Sizes', fontsize=11, fontweight='bold')
    ax1.set_xlabel('Pressure Balls Faced', fontsize=10)
    ax1.legend()
    
    sns.histplot(all_bowl['pressure_legal_balls'], bins=40, color='#00897B', ax=ax2, edgecolor='white')
    ax2.axvline(120, color='red', linestyle='--', label='Bowling Cutoff (120 balls)')
    ax2.set_title('Bowlers: Pressure Legal Deliveries Sample Sizes', fontsize=11, fontweight='bold')
    ax2.set_xlabel('Pressure Deliveries Bowled', fontsize=10)
    ax2.legend()
    plt.tight_layout()
    plt.savefig('outputs/visualizations/08_sample_size_distribution.png')
    plt.close()
    print(" - Saved 08_sample_size_distribution.png")

    # -------------------------------------------------------------
    # 9. Top 10 Batters Ranking (Horizontal Bar Chart)
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(9, 5.5))
    y_pos = np.arange(len(top_bat))[::-1]
    bars = ax.barh(y_pos, top_bat['pressure_rating'], color='#1565C0', edgecolor='black', alpha=0.85)
    ax.set_yticks(y_pos)
    ax.set_yticklabels([f"#{r['rank']} {r['striker_name']}" for idx, r in top_bat.iterrows()], fontsize=9, fontweight='bold')
    for bar in bars:
        w = bar.get_width()
        ax.annotate(f"{w:.2f}",
                    xy=(w, bar.get_y() + bar.get_height() / 2),
                    xytext=(5, 0), textcoords="offset points",
                    ha='left', va='center', fontsize=9, fontweight='bold')
    ax.set_xlim(0, 85)
    ax.set_title('Official Top 10 Batters Under Pressure (SupeRR Selector S2)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Composite Pressure Performance Rating (Scaled Index)', fontsize=10)
    plt.tight_layout()
    plt.savefig('outputs/visualizations/09_top_10_batters_ranking.png')
    plt.close()
    print(" - Saved 09_top_10_batters_ranking.png")

    # -------------------------------------------------------------
    # 10. Top 10 Bowlers Ranking (Horizontal Bar Chart)
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(9, 5.5))
    y_pos = np.arange(len(top_bowl))[::-1]
    bars = ax.barh(y_pos, top_bowl['pressure_rating'], color='#2E7D32', edgecolor='black', alpha=0.85)
    ax.set_yticks(y_pos)
    ax.set_yticklabels([f"#{r['rank']} {r['bowler_name']}" for idx, r in top_bowl.iterrows()], fontsize=9, fontweight='bold')
    for bar in bars:
        w = bar.get_width()
        ax.annotate(f"{w:.2f}",
                    xy=(w, bar.get_y() + bar.get_height() / 2),
                    xytext=(5, 0), textcoords="offset points",
                    ha='left', va='center', fontsize=9, fontweight='bold')
    ax.set_xlim(0, 95)
    ax.set_title('Official Top 10 Bowlers Under Pressure (SupeRR Selector S2)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Composite Pressure Performance Rating (Scaled Index)', fontsize=10)
    plt.tight_layout()
    plt.savefig('outputs/visualizations/10_top_10_bowlers_ranking.png')
    plt.close()
    print(" - Saved 10_top_10_bowlers_ranking.png")

    # -------------------------------------------------------------
    # 11. Competition-wise Performance Comparison (IPL vs T20I)
    # -------------------------------------------------------------
    comp_df = df.groupby(['match_format', 'pressure_tier'], observed=False).size().unstack(fill_value=0)
    comp_pct = comp_df.div(comp_df.sum(axis=1), axis=0) * 100
    fig, ax = plt.subplots(figsize=(8, 5))
    comp_pct[['Low', 'Moderate', 'High', 'Extreme']].plot(kind='bar', stacked=True,
                                                           color=['#4CAF50', '#FFC107', '#FF9800', '#F44336'],
                                                           ax=ax, edgecolor='black', alpha=0.85)
    ax.set_title('Pressure Tier Proportion by Tournament Format (IPL vs T20I)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Match Format', fontsize=10)
    ax.set_ylabel('Percentage of Deliveries (%)', fontsize=10)
    ax.set_xticklabels(['IPL (T20)', 'T20 Internationals (T20I)'], rotation=0, fontsize=10)
    ax.legend(title='Pressure Tier', frameon=True)
    plt.tight_layout()
    plt.savefig('outputs/visualizations/11_competition_comparison.png')
    plt.close()
    print(" - Saved 11_competition_comparison.png")

    # -------------------------------------------------------------
    # 12. Ranking Stability Under Different Model Weights
    # -------------------------------------------------------------
    exp7 = pd.read_csv('outputs/models/exp7_weight_sensitivity.csv')
    fig, ax = plt.subplots(figsize=(10, 5.5))
    import ast
    configs = exp7['config'].tolist()
    # Track top 5 batters across configs
    tracked_batters = ['Ishan Kishan', 'Rovman Powell', 'Shreyas Iyer', 'Tim David', 'David Miller']
    for bname in tracked_batters:
        ranks = []
        for idx, r in exp7.iterrows():
            top10 = ast.literal_eval(r['top_10'])
            rank = top10.index(bname) + 1 if bname in top10 else 11
            ranks.append(rank)
        ax.plot(configs, ranks, marker='o', label=bname, linewidth=2.5)
    ax.invert_yaxis()
    ax.set_title('Top Batter Rank Stability Across 5 Weight Configurations', fontsize=12, fontweight='bold')
    ax.set_ylabel('Rank Position (1 = Best)', fontsize=10)
    ax.set_xlabel('Weight Configuration Scenario', fontsize=10)
    ax.set_xticklabels(configs, rotation=25, ha='right', fontsize=9)
    ax.legend(title='Player', frameon=True)
    plt.tight_layout()
    plt.savefig('outputs/visualizations/12_ranking_stability_weights.png')
    plt.close()
    print(" - Saved 12_ranking_stability_weights.png")
    
    print("All 12 analytical visualizations successfully created and saved to outputs/visualizations/!")

if __name__ == '__main__':
    generate_all_visualizations()
