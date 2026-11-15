"""
Rajasthan Royals IPL 2027 Auction Dashboard (Streamlit App)
SupeRR Selector Season 2 — Pressure Performance Analytics
Run with: streamlit run src/app_dashboard.py
"""

import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Rajasthan Royals // IPL 2027 Auction Dashboard",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Neobrutalism CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Work+Sans:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Work Sans', sans-serif;
    }
    
    .stApp {
        background-color: #F8F6F0;
    }
    
    /* Neobrutalism Cards */
    .neo-card {
        background-color: #FFFFFF;
        border: 3px solid #111111;
        box-shadow: 5px 5px 0px #111111;
        border-radius: 0px;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    .neo-hero {
        background-color: #EA1B86;
        color: #FFFFFF;
        border: 4px solid #111111;
        box-shadow: 6px 6px 0px #111111;
        padding: 24px;
        margin-bottom: 24px;
    }
    
    .neo-badge {
        display: inline-block;
        padding: 4px 12px;
        font-weight: 800;
        font-size: 12px;
        border: 2px solid #111111;
        box-shadow: 2px 2px 0px #111111;
        margin-right: 8px;
        margin-bottom: 8px;
        text-transform: uppercase;
    }
    
    .badge-pink { background-color: #EA1B86; color: white; }
    .badge-yellow { background-color: #FFE600; color: #111111; }
    .badge-blue { background-color: #0B1B3D; color: #FFE600; }
    .badge-mint { background-color: #00E676; color: #111111; }
    .badge-cyan { background-color: #00E5FF; color: #111111; }
    
    /* Neobrutalism Table */
    table {
        border-collapse: collapse !important;
        width: 100% !important;
        border: 3px solid #111111 !important;
        box-shadow: 4px 4px 0px #111111 !important;
    }
    th {
        background-color: #0B1B3D !important;
        color: #FFE600 !important;
        font-weight: 800 !important;
        border: 2px solid #111111 !important;
        padding: 12px !important;
        text-transform: uppercase !important;
    }
    td {
        border: 2px solid #111111 !important;
        padding: 10px !important;
        background-color: #FFFFFF !important;
        color: #111111 !important;
        font-weight: 600 !important;
    }
    tr:nth-child(even) td {
        background-color: #F8F6F0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Top Hero Bar
st.markdown("""
<div class="neo-hero">
    <div style="font-size: 13px; font-weight: 800; letter-spacing: 1.5px; color: #FFE600; margin-bottom: 6px;">
        ★ RAJASTHAN ROYALS // IPL 2027 AUCTION MASTER WAR ROOM ★
    </div>
    <div style="font-size: 38px; font-weight: 800; line-height: 1.1; margin-bottom: 10px;">
        SUPER R SELECTOR: CLUTCH INTELLIGENCE
    </div>
    <div style="font-size: 16px; font-weight: 600; color: #FFFFFF;">
        Identifying the Most Reliable T20 Players Under Pressure & Optimizing Rajasthan Royals for Sawai Mansingh Stadium
    </div>
    <div style="margin-top: 14px;">
        <span class="neo-badge badge-yellow">194,014 DELIVERIES</span>
        <span class="neo-badge badge-blue">837 OFFICIAL MATCHES</span>
        <span class="neo-badge badge-mint">k* = 2,212 OPTIMAL SHRINKAGE</span>
        <span class="neo-badge badge-cyan">1,000 CLUSTER BOOTSTRAP</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar Navigation
sidebar = st.sidebar
sidebar.markdown("""
<div style="padding: 10px; background-color: #0B1B3D; color: #FFE600; border: 3px solid #111111; box-shadow: 4px 4px 0px #111111; margin-bottom: 20px; font-weight: 800;">
    👑 RR WAR ROOM NAVIGATION
</div>
""", unsafe_allow_html=True)

page = sidebar.radio(
    "Select Strategic Module:",
    ["1. Executive Overview & War Room",
     "2. Top 10 Pressure Batters",
     "3. Top 10 Pressure Bowlers",
     "4. Scientific Methodology & Audit",
     "5. Sawai Mansingh Stadium Dynamics",
     "6. Auction Purse & Roster Simulator"]
)

# Load data
@st.cache_data
def load_data():
    bat = pd.read_csv('outputs/uncertainty/round1_batters_uncertainty_comparison.csv')
    bowl = pd.read_csv('outputs/uncertainty/round1_bowlers_uncertainty_comparison.csv')
    return bat, bowl

bat_df, bowl_df = load_data()

# BATTER RR TACTICAL FIT DICT
bat_rr_fit = {
    'Heinrich Klaasen': {'role': 'Jaipur Spin Demolisher (#4/#5)', 'priority': 'Tier 1 (Marquee)', 'desc': 'Sawai Mansingh Stadium square boundaries (68-72m) cause middle-overs stalls against spin. Klaasen boasts +0.611 RAE/ball and 204.1 pressure SR. Demolishes wrist and finger spin without losing momentum.'},
    'Tim David': {'role': 'Death Finisher (Overs 17-20)', 'priority': 'Tier 1 (Marquee)', 'desc': 'Rank #1 in world under optimal shrinkage (k*=2212). Faced 300 pressure balls (most in dataset) with 48 sixes and 94.9% bootstrap Top-10 probability. Clears Jaipur 75m straight boundary at will.'},
    'Suryakumar Yadav': {'role': '360° Middle Spine (#3/#4)', 'priority': 'Tier 1 (Marquee)', 'desc': 'Rank #2 under k*, 254 pressure balls, +0.413 RAE/ball. Manipulates Jaipur boundary geometry by carving vacant fine-leg and third-man pockets with surgical ease.'},
    'Shreyas Iyer': {'role': 'Tactical Captain / Middle Spine', 'priority': 'Tier 2 (Linchpin)', 'desc': 'Rank #4 under k* (P=83.6%). Middle-overs counter-puncher against high pace; 29 sixes prove elite acceleration when RRR escalates.'},
    'Ashutosh Sharma': {'role': 'Designated Impact Closer (#7)', 'priority': 'Tier 2 (Linchpin)', 'desc': 'Pressure SR 192.4 with +0.431 RAE/ball. Elite scoop and sweep mastery. Ideal domestic Impact Player weapon to enter at 135/5 needing 50 off 24.'},
    'Shashank Singh': {'role': 'Anti-Collapse Clutch Anchor', 'priority': 'Tier 2 (Linchpin)', 'desc': 'Pressure SR 200.9 (delta +48.6!) with only 4 dismissals in 107 balls (3.7% rate). Ranks #1 in dataset when penalizing dismissal cost.'},
    'Dinesh Karthik': {'role': 'Veteran Pace Ramp Specialist', 'priority': 'Tier 3 (Value)', 'desc': 'Pressure SR 196.1, 26 fours, 14 sixes. Ramps 145kph+ pace over keeper to exploit short third at Jaipur.'},
    'Rashid Khan': {'role': 'Lethal #8 Boundary Striker', 'priority': 'Tier 2 (Dual Threat)', 'desc': 'Only player in world ranked Top 10 in both Batting (#8) and Bowling (#3). Pressure SR 183.8, 25 sixes; turns RR tail into a boundary engine.'},
    'Mahendra Singh Dhoni': {'role': 'Final-Over Tactical Closer', 'priority': 'Tier 3 (Specialist)', 'desc': 'Pressure SR 181.1, delta +43.3. Enters strictly in over 19/20 to punish execution mistakes against raw pace.'},
    'Rovman Powell': {'role': 'Incumbent RR Boundary Muscle', 'priority': 'Tier 3 (Retention/Value)', 'desc': 'Faced 181 pressure balls with 60% positive match rate and 21 sixes. Proven asset familiar with RR franchise culture.'}
}

bowl_rr_fit = {
    'Sunil Narine': {'role': 'SMS Mystery Spin Anchor & Pinch Hitter', 'priority': 'Tier 1 (Marquee)', 'desc': 'Pressure economy 6.09 (delta -0.84!), +0.343 RP/ball, 88.9% positive matches. Grips on Jaipur clay; doubles as powerplay pinch-hitter.'},
    'Matheesha Pathirana': {'role': 'Marquee Death Yorker Specialist (17-20)', 'priority': 'Tier 1 (Priority #1)', 'desc': 'Rank #1 in world under k* (P=93.1%), +0.350 RP/ball (highest in bowling dataset), 21 pressure wickets. Slingy 148kph toe-crushers seal RR death leakage.'},
    'Mustafizur Rahman': {'role': 'Jaipur Off-Cutter Slower Ball Maestro', 'priority': 'Tier 2 (Linchpin)', 'desc': 'Rank #2 under k* (P=88.2%), 222 legal balls, 23 wickets, +0.232 RP/ball. Off-cutters hold up on Sawai Mansingh Stadium surface.'},
    'Rashid Khan': {'role': 'Middle Overs Choke & Death Overs 17/19', 'priority': 'Tier 1 (Marquee)', 'desc': '183 legal balls, 19 wickets, 85.2% positive matches. Premier dual-threat franchise asset in world cricket.'},
    'Krunal Pandya': {'role': 'Indian Finger Spin & Dart Executioner', 'priority': 'Tier 2 (Linchpin)', 'desc': 'Pressure economy 6.42 (delta -1.56!), 86.7% positive matches. Bowls flat darts on Jaipur long boundaries; frees overseas slot.'},
    'Maheesh Theekshana': {'role': 'Powerplay Mystery & Carrom Bowler', 'priority': 'Tier 3 (Value)', 'desc': 'Pressure economy 7.49, +0.177 RP/ball. Bowls overs 1-6 and 18 with disguised carrom ball.'},
    'Varun Chakravarthy': {'role': 'Overspin Specialist for 70m Boundary', 'priority': 'Tier 2 (Linchpin)', 'desc': '199 legal balls, 16 wickets, 72% positive matches. Overspin generates steep bounce; miscues get caught on 70m boundary line.'},
    'Jason Holder': {'role': 'Tall Release & Heavy Pitch Cutters', 'priority': 'Tier 3 (Value)', 'desc': '227 balls, 22 wickets, 81.6% positive matches. 6ft 7in release point hits bat splice at Jaipur; handy lower-order hitting.'},
    'Ravichandran Ashwin': {'role': 'Jaipur Tactical Master & Pitch Guru', 'priority': 'Tier 3 (Tactical)', 'desc': 'Understands SMS boundary geometry and grip angles better than any active cricketer. Orchestrates in-game match-up traps.'},
    'Yuzvendra Chahal': {'role': 'High-Strike-Rate Partnership Breaker', 'priority': 'Tier 2 (Talisman)', 'desc': '247 pressure balls (most among spinners), 26 pressure wickets (highest in dataset!). Breaks dangerous partnerships in high-stakes overs.'}
}

if page == "1. Executive Overview & War Room":
    st.markdown("### 🏛️ RAJASTHAN ROYALS // IPL 2027 AUCTION STRATEGIC WAR ROOM")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="neo-card" style="border-top: 6px solid #EA1B86;">
            <div style="font-size: 11px; font-weight: 800; color: #EA1B86;">PRIMARY ACQUISITION GOAL</div>
            <div style="font-size: 24px; font-weight: 800; margin: 4px 0;">SEAL DEATH OVERS</div>
            <div style="font-size: 12px; color: #6E6E6E;">Overs 17-20 run leakage cost RR in past playoffs. Target: Matheesha Pathirana (+0.350 RP/ball).</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="neo-card" style="border-top: 6px solid #FFE600;">
            <div style="font-size: 11px; font-weight: 800; color: #111;">FINISHER CERTAINTY</div>
            <div style="font-size: 24px; font-weight: 800; margin: 4px 0;">TIM DAVID / KLAASEN</div>
            <div style="font-size: 12px; color: #6E6E6E;">David: 300 balls, P=94.9%. Klaasen: +0.611 RAE/ball. Demolishes middle-overs spin stall.</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="neo-card" style="border-top: 6px solid #00E676;">
            <div style="font-size: 11px; font-weight: 800; color: #00E676;">JAIPUR FORTRESS</div>
            <div style="font-size: 24px; font-weight: 800; margin: 4px 0;">SUNIL NARINE</div>
            <div style="font-size: 12px; color: #6E6E6E;">Econ 6.09 under pressure. Red/black clay grip makes Sawai Mansingh Stadium unbreachable.</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="neo-card" style="border-top: 6px solid #00E5FF;">
            <div style="font-size: 11px; font-weight: 800; color: #00E5FF;">VALUE CLOSER</div>
            <div style="font-size: 24px; font-weight: 800; margin: 4px 0;">SHASHANK / ASHUTOSH</div>
            <div style="font-size: 12px; color: #6E6E6E;">Shashank: 3.7% dismissal rate, 200.9 SR. High-impact domestic closers save auction purse.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### ⚔️ PROVEN CHAMPIONSHIP XI (PRESSURE-OPTIMIZED FOR IPL 2027)")
    
    xi_data = [
        {"Pos": "1", "Player": "Yashasvi Jaiswal (LHB)", "Role": "Anchor / Powerplay Exploder", "Status": "Retained"},
        {"Pos": "2", "Player": "Sunil Narine (LHB / OB)", "Role": "Powerplay Pinch-Hitter & Mystery Spin Anchor", "Status": "Target Tier 1"},
        {"Pos": "3", "Player": "Sanju Samson (C/WK)", "Role": "Captain & 360° Counter-Puncher", "Status": "Retained"},
        {"Pos": "4", "Player": "Suryakumar Yadav / Shreyas Iyer", "Role": "Middle-Overs Field Manipulator & Spin Spine", "Status": "Target Tier 1/2"},
        {"Pos": "5", "Player": "Heinrich Klaasen / Tim David (OS)", "Role": "Elite Spin Demolisher & Death Boundary Striker", "Status": "Target Tier 1"},
        {"Pos": "6", "Player": "Riyan Parag (RHB / Utility)", "Role": "Pace Accelerator & Seam Backup", "Status": "Retained"},
        {"Pos": "7", "Player": "Shashank Singh / Ashutosh Sharma", "Role": "Impact Closer (High Wicket Preservation)", "Status": "Target Tier 2"},
        {"Pos": "8", "Player": "Rashid Khan / Krunal Pandya", "Role": "Lethal Lower-Order Boundary Striker & Phase Choke", "Status": "Target Tier 1/2"},
        {"Pos": "9", "Player": "Sandeep Sharma", "Role": "Swing & Wide Yorker Execution", "Status": "Retained"},
        {"Pos": "10", "Player": "Matheesha Pathirana (OS)", "Role": "Marquee 148kph Death Yorker Bowler (Overs 17-20)", "Status": "Target Priority #1"},
        {"Pos": "11", "Player": "Avesh Khan / Kuldeep Sen", "Role": "High Pace Hard-Length Seamer", "Status": "Retained"},
        {"12", "Mustafizur Rahman (OS Impact)", "Jaipur Gripping Clay Off-Cutter Slower Ball Specialist", "Target Tier 3"}
    ]
    st.table(pd.DataFrame(xi_data))

elif page == "2. Top 10 Pressure Batters":
    st.markdown("### 🏏 TOP 10 PRESSURE BATTERS // RAJASTHAN ROYALS RECRUITMENT DOSSIER")
    
    sort_by = st.selectbox("Sort Batters By:", ["Optimal Shrinkage Rank (k*)", "Round 1 Competition Rank", "Bootstrap Inclusion Probability P(Top 10)"])
    
    disp_df = bat_df.copy()
    if sort_by == "Optimal Shrinkage Rank (k*)":
        disp_df = disp_df.sort_values('kstar_rank')
    elif sort_by == "Round 1 Competition Rank":
        disp_df = disp_df.sort_values('round1_rank')
    else:
        disp_df = disp_df.sort_values('p_top10', ascending=False)
        
    for _, r in disp_df.iterrows():
        name = r['striker_name']
        fit = bat_rr_fit.get(name, {'role': 'Specialist', 'priority': 'Tier 2', 'desc': ''})
        p_top = r['p_top10'] * 100.0
        
        st.markdown(f"""
        <div class="neo-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 22px; font-weight: 800; color: #111;">{name.upper()}</span>
                <div>
                    <span class="neo-badge badge-yellow">k* RANK #{int(r['kstar_rank'])}</span>
                    <span class="neo-badge badge-pink">R1 RANK #{int(r['round1_rank'])}</span>
                    <span class="neo-badge badge-mint">P(TOP 10): {p_top:.1f}%</span>
                </div>
            </div>
            <div style="font-size: 13px; font-weight: 800; color: #0B1B3D; margin-bottom: 6px;">
                ROLE: {fit['role']} | PRIORITY: {fit['priority']}
            </div>
            <div style="font-size: 13px; color: #111; line-height: 1.5; margin-bottom: 12px; background-color: #F8F6F0; padding: 10px; border: 2px solid #111;">
                <b>RR Tactical Fit:</b> {fit['desc']}
            </div>
            <div style="font-size: 12px; font-weight: 600; color: #6E6E6E;">
                <b>Metrics:</b> Round 1 Rating: <b>{r['round1_rating']:.2f}</b> | Shrunk RAE: <b>{r['kstar_rating']:+.4f}</b> | Mean Bootstrap Rank: <b>#{r['mean_boot_rank']:.1f}</b> | 90% Rank CI: <b>{r['rank_ci90']}</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

elif page == "3. Top 10 Pressure Bowlers":
    st.markdown("### 🎯 TOP 10 PRESSURE BOWLERS // RAJASTHAN ROYALS RECRUITMENT DOSSIER")
    
    sort_by_b = st.selectbox("Sort Bowlers By:", ["Optimal Shrinkage Rank (k*)", "Round 1 Competition Rank", "Bootstrap Inclusion Probability P(Top 10)"])
    
    disp_bowl = bowl_df.copy()
    if sort_by_b == "Optimal Shrinkage Rank (k*)":
        disp_bowl = disp_bowl.sort_values('kstar_rank')
    elif sort_by_b == "Round 1 Competition Rank":
        disp_bowl = disp_bowl.sort_values('round1_rank')
    else:
        disp_bowl = disp_bowl.sort_values('p_top10', ascending=False)
        
    for _, r in disp_bowl.iterrows():
        name = r['bowler_name']
        fit = bowl_rr_fit.get(name, {'role': 'Specialist', 'priority': 'Tier 2', 'desc': ''})
        p_top = r['p_top10'] * 100.0
        
        st.markdown(f"""
        <div class="neo-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 22px; font-weight: 800; color: #111;">{name.upper()}</span>
                <div>
                    <span class="neo-badge badge-yellow">k* RANK #{int(r['kstar_rank'])}</span>
                    <span class="neo-badge badge-blue">R1 RANK #{int(r['round1_rank'])}</span>
                    <span class="neo-badge badge-mint">P(TOP 10): {p_top:.1f}%</span>
                </div>
            </div>
            <div style="font-size: 13px; font-weight: 800; color: #EA1B86; margin-bottom: 6px;">
                ROLE: {fit['role']} | PRIORITY: {fit['priority']}
            </div>
            <div style="font-size: 13px; color: #111; line-height: 1.5; margin-bottom: 12px; background-color: #F8F6F0; padding: 10px; border: 2px solid #111;">
                <b>RR Tactical Fit:</b> {fit['desc']}
            </div>
            <div style="font-size: 12px; font-weight: 600; color: #6E6E6E;">
                <b>Metrics:</b> Round 1 Rating: <b>{r['round1_rating']:.2f}</b> | Shrunk RP: <b>{r['kstar_rating']:+.4f}</b> | Mean Bootstrap Rank: <b>#{r['mean_boot_rank']:.1f}</b> | 90% Rank CI: <b>{r['rank_ci90']}</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

elif page == "4. Scientific Methodology & Audit":
    st.markdown("### 🔬 MATHEMATICAL ARCHITECTURE & INDEPENDENT AUDIT")
    
    st.markdown("""
    <div class="neo-card">
        <div style="font-size: 18px; font-weight: 800; margin-bottom: 10px;">★ THE ESTIMAND DISCOVERY: CLUTCH SLOPE IS NOISE (p = 0.6920)</div>
        <p style="font-size: 14px; color: #111; line-height: 1.6;">
            A rigorous 500-iteration permutation test shuffled delivery pressure indices within player-match groups. 
            The observed cross-player variation in clutch response slopes (<b>sigma_beta = 2.0147</b>) was <b>smaller</b> than the null distribution mean (<b>mu_null = 2.1427</b>), yielding <b>p = 0.6920</b>.
            Split-half reliability across career halves is only <b>r_SB = 0.1550</b> (84.5% stochastic noise).
            <br><br>
            <b>Scientific Conclusion:</b> "Clutch elevation" is largely a narrative myth. Players who succeed under pressure do so because of:
            <br>
            1) <b>Astronomical Baseline Skill (u_i)</b>: Klaasen (+0.611 RAE) and Surya (+0.413 RAE) are elite everywhere.
            <br>
            2) <b>Dismissal Hazard Survival</b>: Dismissals surge from 4.6% to 12.7% under pressure. Shashank Singh (3.7% dismissal rate) preserves wickets.
            <br>
            3) <b>Volume Durability (n > 200 balls)</b>: Tim David (300 balls, P=94.9%) and Pathirana (206 balls, P=93.1%) provide bulletproof statistical confidence.
        </p>
    </div>
    """, unsafe_allow_html=True)

elif page == "5. Sawai Mansingh Stadium Dynamics":
    st.markdown("### 🏟️ SAWAI MANSINGH STADIUM (JAIPUR) VENUE PROFILE")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="neo-card">
            <div style="font-size: 16px; font-weight: 800; color: #EA1B86; margin-bottom: 8px;">BOUNDARY GEOMETRY</div>
            <p style="font-size: 13px; color: #111; line-height: 1.5;">
                • <b>Square Boundaries:</b> 68 - 72 meters<br>
                • <b>Straight Boundaries:</b> 75 - 80 meters (Massive)<br>
                • <b>Outfield:</b> High-speed turf, spacious outfield ring<br><br>
                <b>Tactical Implication:</b> Mistimed aerial hits do not clear the ropes at Jaipur. Batters must possess true clearing power (David, Klaasen) or surgical 360° placement (Surya).
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="neo-card">
            <div style="font-size: 16px; font-weight: 800; color: #0B1B3D; margin-bottom: 8px;">PITCH & CLAY BEHAVIOR</div>
            <p style="font-size: 13px; color: #111; line-height: 1.5;">
                • <b>Soil Mixture:</b> Red and black clay mixture with abrasive surface grip<br>
                • <b>Middle Overs (7-15):</b> Substantial turn and sticky hold into the pitch<br>
                • <b>Death Overs:</b> Dew can affect grip; requires express slingy yorkers<br><br>
                <b>Tactical Implication:</b> Sunil Narine (6.09 econ) and Mustafizur Rahman (off-cutters) are tailor-made for this surface, creating an impenetrable Jaipur fortress.
            </p>
        </div>
        """, unsafe_allow_html=True)

elif page == "6. Auction Purse & Roster Simulator":
    st.markdown("### 💰 RAJASTHAN ROYALS AUCTION SIMULATOR")
    
    st.markdown("Build your ideal pressure-tested recruitment package for Rajasthan Royals:")
    
    bat_sel = st.multiselect("Select Target Batters:", bat_df['striker_name'].tolist(), default=['Heinrich Klaasen', 'Tim David', 'Ashutosh Sharma'])
    bowl_sel = st.multiselect("Select Target Bowlers:", bowl_df['bowler_name'].tolist(), default=['Matheesha Pathirana', 'Sunil Narine', 'Mustafizur Rahman'])
    
    st.markdown(f"**Selected Recruitment Targets ({len(bat_sel) + len(bowl_sel)} Players):**")
    
    total_balls = 0
    sub_bat = bat_df[bat_df['striker_name'].isin(bat_sel)]
    sub_bowl = bowl_df[bowl_df['bowler_name'].isin(bowl_sel)]
    
    st.markdown("#### Selected Batters:")
    st.dataframe(sub_bat[['striker_name', 'round1_rank', 'kstar_rank', 'p_top10', 'rank_ci90']])
    
    st.markdown("#### Selected Bowlers:")
    st.dataframe(sub_bowl[['bowler_name', 'round1_rank', 'kstar_rank', 'p_top10', 'rank_ci90']])
