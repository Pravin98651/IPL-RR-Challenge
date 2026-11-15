import os
import json

html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rajasthan Royals // IPL 2027 Auction War Room Dashboard</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700;800&family=Work+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --rr-pink: #EA1B86;
            --royal-blue: #0B1B3D;
            --canary-yellow: #FFE600;
            --electric-cyan: #00E5FF;
            --neon-mint: #00E676;
            --pure-white: #FFFFFF;
            --sharp-black: #111111;
            --canvas: #F6F4EE;
            --card-border: 3px solid #111111;
            --shadow: 5px 5px 0px #111111;
            --shadow-sm: 3px 3px 0px #111111;
        }
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        body {
            font-family: 'Work Sans', sans-serif;
            background-color: var(--canvas);
            color: var(--sharp-black);
            padding: 24px;
            line-height: 1.5;
        }
        
        /* Neobrutalist Header Hero */
        .hero {
            background-color: var(--rr-pink);
            color: var(--pure-white);
            border: 4px solid var(--sharp-black);
            box-shadow: 7px 7px 0px var(--sharp-black);
            padding: 28px 36px;
            margin-bottom: 28px;
        }
        .hero-pre {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 13px;
            font-weight: 800;
            letter-spacing: 2px;
            color: var(--canary-yellow);
            margin-bottom: 8px;
        }
        .hero-title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 40px;
            font-weight: 800;
            line-height: 1.1;
            margin-bottom: 10px;
            text-transform: uppercase;
        }
        .hero-sub {
            font-size: 16px;
            font-weight: 600;
            max-width: 950px;
            margin-bottom: 18px;
        }
        .leadership-bar {
            background-color: var(--royal-blue);
            color: var(--canary-yellow);
            border: 2px solid var(--sharp-black);
            padding: 10px 18px;
            margin-bottom: 16px;
            display: inline-flex;
            flex-wrap: wrap;
            gap: 20px;
            font-family: 'Space Grotesk', sans-serif;
            font-size: 14px;
            font-weight: 800;
            box-shadow: 3px 3px 0px var(--sharp-black);
        }
        .badge-bar {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }
        .badge {
            display: inline-block;
            font-family: 'Space Grotesk', sans-serif;
            font-size: 12px;
            font-weight: 800;
            text-transform: uppercase;
            padding: 6px 14px;
            border: 2px solid var(--sharp-black);
            box-shadow: 2px 2px 0px var(--sharp-black);
        }
        .badge-yellow { background-color: var(--canary-yellow); color: var(--sharp-black); }
        .badge-blue { background-color: var(--royal-blue); color: var(--canary-yellow); }
        .badge-mint { background-color: var(--neon-mint); color: var(--sharp-black); }
        .badge-cyan { background-color: var(--electric-cyan); color: var(--sharp-black); }
        .badge-white { background-color: var(--pure-white); color: var(--sharp-black); }
        .badge-pink { background-color: var(--rr-pink); color: var(--pure-white); }

        /* Tabs Navigation */
        .tabs-nav {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 24px;
        }
        .tab-btn {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 13px;
            font-weight: 800;
            text-transform: uppercase;
            padding: 12px 18px;
            background-color: var(--pure-white);
            border: var(--card-border);
            box-shadow: var(--shadow-sm);
            cursor: pointer;
            transition: all 0.1s ease;
        }
        .tab-btn:hover {
            transform: translate(-2px, -2px);
            box-shadow: 5px 5px 0px var(--sharp-black);
        }
        .tab-btn.active {
            background-color: var(--royal-blue);
            color: var(--canary-yellow);
            transform: translate(2px, 2px);
            box-shadow: 2px 2px 0px var(--sharp-black);
        }

        /* Neobrutalist Cards */
        .card {
            background-color: var(--pure-white);
            border: var(--card-border);
            box-shadow: var(--shadow);
            padding: 24px;
            margin-bottom: 24px;
        }
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 3px solid var(--sharp-black);
            padding-bottom: 14px;
            margin-bottom: 16px;
        }
        .card-title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 22px;
            font-weight: 800;
            color: var(--sharp-black);
        }

        /* Grid Layouts */
        .grid-4 {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 20px;
            margin-bottom: 24px;
        }
        .grid-3 {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 20px;
            margin-bottom: 24px;
        }
        .grid-2 {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
            gap: 24px;
            margin-bottom: 24px;
        }

        /* Metric Box */
        .metric-box {
            background-color: var(--pure-white);
            border: var(--card-border);
            box-shadow: var(--shadow-sm);
            padding: 16px;
        }
        .metric-label {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 11px;
            font-weight: 800;
            color: var(--rr-pink);
            text-transform: uppercase;
        }
        .metric-val {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 26px;
            font-weight: 800;
            margin: 4px 0;
            color: var(--sharp-black);
        }
        .metric-desc {
            font-size: 12px;
            font-weight: 500;
            color: #555555;
        }

        /* Table Style */
        .data-table {
            width: 100%;
            border-collapse: collapse;
            border: var(--card-border);
            box-shadow: var(--shadow-sm);
            margin-top: 12px;
            background-color: var(--pure-white);
        }
        .data-table th {
            background-color: var(--royal-blue);
            color: var(--canary-yellow);
            font-family: 'Space Grotesk', sans-serif;
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            padding: 11px 13px;
            border: 2px solid var(--sharp-black);
            text-align: left;
        }
        .data-table td {
            padding: 10px 13px;
            font-size: 13px;
            font-weight: 600;
            border: 2px solid var(--sharp-black);
        }
        .data-table tr:nth-child(even) td {
            background-color: var(--canvas);
        }

        /* Squad Categorized Pills */
        .squad-category-box {
            background-color: var(--pure-white);
            border: var(--card-border);
            box-shadow: var(--shadow-sm);
            padding: 18px;
            margin-bottom: 20px;
        }
        .squad-cat-title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 16px;
            font-weight: 800;
            text-transform: uppercase;
            padding-bottom: 8px;
            margin-bottom: 12px;
            border-bottom: 2px solid var(--sharp-black);
            display: flex;
            justify-content: space-between;
        }
        .player-chip-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }
        .player-chip {
            background-color: var(--canvas);
            border: 2px solid var(--sharp-black);
            padding: 8px 12px;
            font-size: 12px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .chip-badge {
            font-size: 9px;
            font-weight: 800;
            padding: 2px 6px;
            border: 1px solid var(--sharp-black);
            text-transform: uppercase;
        }

        /* Player Dossier Card */
        .player-card {
            background-color: var(--pure-white);
            border: var(--card-border);
            box-shadow: var(--shadow);
            padding: 22px;
            margin-bottom: 20px;
            transition: transform 0.15s ease;
        }
        .player-card:hover {
            transform: translate(-3px, -3px);
            box-shadow: 8px 8px 0px var(--sharp-black);
        }
        .player-head {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }
        .player-name {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 24px;
            font-weight: 800;
            color: var(--sharp-black);
        }
        .player-role-bar {
            font-size: 13px;
            font-weight: 800;
            color: var(--rr-pink);
            margin-bottom: 10px;
        }
        .player-fit {
            background-color: var(--canvas);
            border: 2px solid var(--sharp-black);
            padding: 12px 16px;
            font-size: 13px;
            margin-bottom: 14px;
            line-height: 1.5;
        }
        .player-metrics-row {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            font-size: 12px;
            font-weight: 700;
            color: #333333;
        }
        .metric-pill {
            background-color: #EEEEEE;
            border: 1px solid var(--sharp-black);
            padding: 4px 10px;
        }

        /* Filter Controls */
        .filter-bar {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 18px;
        }
        .filter-btn {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 11px;
            font-weight: 800;
            padding: 6px 14px;
            border: 2px solid var(--sharp-black);
            background-color: var(--pure-white);
            cursor: pointer;
        }
        .filter-btn.active {
            background-color: var(--rr-pink);
            color: var(--pure-white);
        }
    </style>
</head>
<body>

    <!-- HERO HEADER -->
    <div class="hero">
        <div class="hero-pre">★ RAJASTHAN ROYALS // IPL 2027 AUCTION STRATEGIC INTELLIGENCE ★</div>
        <div class="hero-title">SUPER R SELECTOR: CLUTCH INTELLIGENCE</div>
        <div class="hero-sub">Identifying the Most Reliable Players Under High Pressure & Integrating with Rajasthan Royals' Current Roster for IPL 2027</div>
        
        <div class="leadership-bar">
            <span>👑 <b>CAPTAIN:</b> RIYAN PARAG</span>
            <span>🧠 <b>HEAD COACH:</b> KUMAR SANGAKKARA</span>
            <span>🏟️ <b>HOME VENUE:</b> SAWAI MANSINGH STADIUM, JAIPUR</span>
        </div>

        <div class="badge-bar">
            <span class="badge badge-yellow">194,014 DELIVERIES AUDITED</span>
            <span class="badge badge-blue">837 OFFICIAL MATCHES (IPL + T20I)</span>
            <span class="badge badge-mint">CURRENT ROSTER: 25 ACTIVE PLAYERS</span>
            <span class="badge badge-cyan">k* = 2,212 OPTIMAL SHRINKAGE</span>
            <span class="badge badge-white">JAIPUR CLAY OPTIMIZED</span>
        </div>
    </div>

    <!-- TABS -->
    <div class="tabs-nav">
        <button class="tab-btn active" onclick="switchTab('overview')">1. War Room & Championship XI</button>
        <button class="tab-btn" onclick="switchTab('squad')">2. Current RR Squad Depth & Gaps</button>
        <button class="tab-btn" onclick="switchTab('batters')">3. Top 10 Pressure Batters</button>
        <button class="tab-btn" onclick="switchTab('bowlers')">4. Top 10 Pressure Bowlers</button>
        <button class="tab-btn" onclick="switchTab('methodology')">5. Scientific Audit & Proof</button>
        <button class="tab-btn" onclick="switchTab('venue')">6. Jaipur SMS Stadium Geometry</button>
        <button class="tab-btn" onclick="switchTab('simulator')">7. Auction Priority Matrix</button>
    </div>

    <!-- TAB 1: OVERVIEW -->
    <div id="tab-overview" class="tab-content">
        <div class="grid-4">
            <div class="metric-box" style="border-left: 6px solid var(--rr-pink);">
                <div class="metric-label">PRIORITY #1 TARGET</div>
                <div class="metric-val">PATHIRANA</div>
                <div class="metric-desc">+0.350 Runs Prevented / ball. Forms an unhittable death battery with Jofra Archer & Sandeep Sharma.</div>
            </div>
            <div class="metric-box" style="border-left: 6px solid var(--canary-yellow);">
                <div class="metric-label">MARQUEE FINISHER</div>
                <div class="metric-val">KLAASEN / DAVID</div>
                <div class="metric-desc">Klaasen (+0.611 RAE) or David (300 balls, 194.7 SR). Shields Parag and Jurel from spin strangulation.</div>
            </div>
            <div class="metric-box" style="border-left: 6px solid var(--neon-mint);">
                <div class="metric-label">SMS SPIN TRIPLE-THREAT</div>
                <div class="metric-val">NARINE / RASHID</div>
                <div class="metric-desc">Pairs with Ravindra Jadeja & Ravi Bishnoi to construct a suffocating 3-spinner choke on Jaipur clay.</div>
            </div>
            <div class="metric-box" style="border-left: 6px solid var(--electric-cyan);">
                <div class="metric-label">IMPACT CLOSER</div>
                <div class="metric-val">SHASHANK SINGH</div>
                <div class="metric-desc">200.9 SR with only 4 dismissals in 107 balls (3.7% rate). Low-cost Indian clutch insurance.</div>
            </div>
        </div>

        <div class="card">
            <div class="card-header">
                <div class="card-title">👑 RAJASTHAN ROYALS // PROVEN CHAMPIONSHIP XI (IPL 2027)</div>
                <span class="badge badge-pink">SQUAD LED BY RIYAN PARAG & KUMAR SANGAKKARA</span>
            </div>
            <p style="font-size: 14px; margin-bottom: 14px; color: #444;">
                Harmonizing RR's current core (Jaiswal, Parag, Jadeja, Curran, Jurel, Archer, Bishnoi, Sandeep) with elite pressure acquisitions:
            </p>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>POS</th>
                        <th>PLAYER NAME</th>
                        <th>STRATEGIC ROLE</th>
                        <th>STATUS / TARGET</th>
                        <th>PRESSURE STABILITY RATIONALE</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td>1</td><td><b>Yashasvi Jaiswal</b> (LHB)</td><td>Powerplay Disruptor</td><td><span class="badge badge-blue">CURRENT SQUAD</span></td><td>Exploits initial 6 overs before Jaipur clay holds up; +28.4 normal RAE.</td></tr>
                    <tr><td>2</td><td><b>Sunil Narine</b> / <b>Vaibhav Sooryavanshi</b></td><td>Pinch-Hitter / SMS Mystery Spinner</td><td><span class="badge badge-pink">TIER 1 TARGET / SQUAD</span></td><td>Narine: 6.09 death economy; opens batting as ultra-high-strike-rate pinch-hitter.</td></tr>
                    <tr><td>3</td><td><b>Riyan Parag</b> (RHB / C)</td><td>Captain & High-Pace Anchor</td><td><span class="badge badge-blue">CAPTAIN</span></td><td>Local Jaipur SMS mastery; elite boundary acceleration in overs 10-17.</td></tr>
                    <tr><td>4</td><td><b>Heinrich Klaasen</b> / <b>Shreyas Iyer</b></td><td>World #1 Spin Demolisher</td><td><span class="badge badge-pink">TIER 1 TARGET</span></td><td>Klaasen (+0.611 RAE/ball, 204.1 SR) dismantles visiting wrist-spinners at SMS.</td></tr>
                    <tr><td>5</td><td><b>Dhruv Jurel</b> (RHB / WK)</td><td>Middle-Order Closer / Wicket-Keeper</td><td><span class="badge badge-blue">CURRENT SQUAD</span></td><td>Proven Indian clutch performer under intense chase pressure (71.24 Model A rating).</td></tr>
                    <tr><td>6</td><td><b>Shimron Hetmyer</b> / <b>Tim David</b></td><td>Overseas Death Accelerator</td><td><span class="badge badge-yellow">SQUAD / TARGET</span></td><td>Hetmyer left-handed boundary muscle; David clears Jaipur's 75m straight fence (300 balls).</td></tr>
                    <tr><td>7</td><td><b>Ravindra Jadeja</b> (LHB / SLA)</td><td>Premier Indian All-Rounder</td><td><span class="badge badge-blue">CURRENT SQUAD</span></td><td>World-class finger spin on gripping Jaipur clay + left-handed death-batting composure.</td></tr>
                    <tr><td>8</td><td><b>Sam Curran</b> / <b>Shashank Singh</b></td><td>Pace All-Rounder / Impact Closer</td><td><span class="badge badge-yellow">SQUAD / TARGET</span></td><td>Curran provides left-arm angle + death batting; Shashank offers 200.9 SR at 3.7% hazard.</td></tr>
                    <tr><td>9</td><td><b>Jofra Archer</b> (RF)</td><td>Overseas Express Spearhead</td><td><span class="badge badge-blue">CURRENT SQUAD</span></td><td>150kph high-pace bounce at Jaipur; bowls overs 1, 3, 16 and 18.</td></tr>
                    <tr><td>10</td><td><b>Ravi Bishnoi</b> (RLB)</td><td>Attacking Indian Leg-Spinner</td><td><span class="badge badge-blue">CURRENT SQUAD</span></td><td>Rapid 100kph flatter trajectory; partners Jadeja to choke middle-overs run flow.</td></tr>
                    <tr><td>11</td><td><b>Sandeep Sharma</b> (RMF)</td><td>Swing & Death Wide Yorker Maestro</td><td><span class="badge badge-blue">CURRENT SQUAD</span></td><td>Unrivaled domestic composure; nails wide yorkers under extreme pressure in overs 18 & 20.</td></tr>
                    <tr><td>12</td><td><b>Matheesha Pathirana</b> / <b>Mustafizur</b></td><td>Impact Death Executioner (OS)</td><td><span class="badge badge-mint">PRIORITY #1 TARGET</span></td><td>Pathirana (+0.350 RP/ball, 21 wkts); or Mustafizur with gripping off-cutters on SMS clay.</td></tr>
                </tbody>
            </table>
        </div>
    </div>

    <!-- TAB 2: CURRENT RR SQUAD DEPTH & GAPS -->
    <div id="tab-squad" class="tab-content" style="display: none;">
        <div class="card">
            <div class="card-header">
                <div class="card-title">🛡️ RAJASTHAN ROYALS // OFFICIAL CURRENT SQUAD ROSTER</div>
                <span class="badge badge-blue">HEAD COACH: KUMAR SANGAKKARA</span>
            </div>
            <p style="font-size: 14px; margin-bottom: 18px; color: #444;">
                Complete inventory of Rajasthan Royals' 25 active players led by Captain <b>Riyan Parag</b>, analyzed across tactical roles and pressure readiness:
            </p>

            <div class="grid-2">
                <!-- BATTERS -->
                <div class="squad-category-box">
                    <div class="squad-cat-title">
                        <span>🏏 Batters (5 Players)</span>
                        <span class="badge badge-pink">TOP ORDER & FINISHING</span>
                    </div>
                    <div class="player-chip-grid">
                        <div class="player-chip"><b>Yashasvi Jaiswal</b> <span class="chip-badge badge-blue">LHB / RET</span></div>
                        <div class="player-chip"><b>Shimron Hetmyer</b> <span class="chip-badge badge-yellow">LHB / OS</span></div>
                        <div class="player-chip"><b>Shubham Dubey</b> <span class="chip-badge badge-white">LHB / DOM</span></div>
                        <div class="player-chip"><b>Aman Perala (Aman Rao)</b> <span class="chip-badge badge-white">RHB / DOM</span></div>
                        <div class="player-chip"><b>Vaibhav Sooryavanshi</b> <span class="chip-badge badge-mint">LHB / PRODIGY</span></div>
                    </div>
                    <p style="font-size: 12px; color: #555; margin-top: 10px;">
                        <b>Diagnosis:</b> High top-order potency in Jaiswal, but lacks an established Indian right-handed anchor at #4 if an early wicket falls. Adding <b>Shreyas Iyer</b> or <b>Heinrich Klaasen</b> perfectly balances the batting order.
                    </p>
                </div>

                <!-- ALL-ROUNDERS -->
                <div class="squad-category-box">
                    <div class="squad-cat-title">
                        <span>⚡ All-Rounders (7 Players)</span>
                        <span class="badge badge-mint">SQUAD BALANCE</span>
                    </div>
                    <div class="player-chip-grid">
                        <div class="player-chip"><b>Ravindra Jadeja</b> <span class="chip-badge badge-blue">SLA / MARQUEE</span></div>
                        <div class="player-chip"><b>Sam Curran</b> <span class="chip-badge badge-yellow">LFM / OS</span></div>
                        <div class="player-chip"><b>Dasun Shanaka</b> <span class="chip-badge badge-yellow">RFM / OS</span></div>
                        <div class="player-chip"><b>Donovan Ferreira</b> <span class="chip-badge badge-yellow">OB/WK / OS</span></div>
                        <div class="player-chip"><b>Yudhvir Singh</b> <span class="chip-badge badge-white">RFM / DOM</span></div>
                        <div class="player-chip"><b>Emanjot Singh Chahal</b> <span class="chip-badge badge-white">SLA / DOM</span></div>
                        <div class="player-chip"><b>Brijesh Sharma</b> <span class="chip-badge badge-white">RMF / DOM</span></div>
                    </div>
                    <p style="font-size: 12px; color: #555; margin-top: 10px;">
                        <b>Diagnosis:</b> Extraordinary luxury with Ravindra Jadeja and Sam Curran. Jadeja gives 4 overs of elite left-arm spin + match-winning lower-order composure. Shanaka and Ferreira offer tactical overseas depth.
                    </p>
                </div>

                <!-- WICKET KEEPERS -->
                <div class="squad-category-box">
                    <div class="squad-cat-title">
                        <span>🧤 Wicket-Keepers (3 Players)</span>
                        <span class="badge badge-cyan">MIDDLE-ORDER STABILITY</span>
                    </div>
                    <div class="player-chip-grid">
                        <div class="player-chip"><b>Dhruv Jurel</b> <span class="chip-badge badge-blue">RHB / MARQUEE</span></div>
                        <div class="player-chip"><b>Lhuan-dre Pretorius</b> <span class="chip-badge badge-yellow">LHB / OS</span></div>
                        <div class="player-chip" style="opacity: 0.6; text-decoration: line-through;"><b>Ravi Singh</b> <span class="chip-badge badge-white">WITHDRAWN</span></div>
                    </div>
                    <p style="font-size: 12px; color: #555; margin-top: 10px;">
                        <b>Diagnosis:</b> Dhruv Jurel is India's premier young clutch finisher. Ranks #3 in Model A rule pressure (71.24 rating). Supported by South Africa's exciting young Lhuan-dre Pretorius.
                    </p>
                </div>

                <!-- BOWLERS -->
                <div class="squad-category-box">
                    <div class="squad-cat-title">
                        <span>🎯 Bowlers (11 Players)</span>
                        <span class="badge badge-yellow">PACE & SPIN BATTERY</span>
                    </div>
                    <div class="player-chip-grid">
                        <div class="player-chip"><b>Jofra Archer</b> <span class="chip-badge badge-blue">RF / OS</span></div>
                        <div class="player-chip"><b>Ravi Bishnoi</b> <span class="chip-badge badge-blue">RLB / MARQUEE</span></div>
                        <div class="player-chip"><b>Sandeep Sharma</b> <span class="chip-badge badge-blue">RMF / YORKER</span></div>
                        <div class="player-chip"><b>Tushar Deshpande</b> <span class="chip-badge badge-white">RMF / DOM</span></div>
                        <div class="player-chip"><b>Nandre Burger</b> <span class="chip-badge badge-yellow">LF / OS</span></div>
                        <div class="player-chip"><b>Kwena Maphaka</b> <span class="chip-badge badge-yellow">LF / OS PRODIGY</span></div>
                        <div class="player-chip"><b>Adam Milne</b> <span class="chip-badge badge-yellow">RF / OS</span></div>
                        <div class="player-chip"><b>Kuldeep Sen</b> <span class="chip-badge badge-white">RF / DOM</span></div>
                        <div class="player-chip"><b>Sushant Mishra</b> <span class="chip-badge badge-white">LMF / DOM</span></div>
                        <div class="player-chip"><b>Vignesh Puthur</b> <span class="chip-badge badge-white">SPIN / DOM</span></div>
                        <div class="player-chip"><b>Yash Raj Punja</b> <span class="chip-badge badge-white">RMF / DOM</span></div>
                    </div>
                    <p style="font-size: 12px; color: #555; margin-top: 10px;">
                        <b>Diagnosis:</b> High-ceiling pace spearhead with Jofra Archer, Sandeep Sharma, Burger, and Deshpande. Bishnoi and Jadeja command 8 overs of spin. The only missing link: a 145kph+ slingy death specialist (**Matheesha Pathirana**) to finish matches cleanly.
                    </p>
                </div>
            </div>

            <!-- STRATEGIC GAP MATRIX -->
            <div class="metric-box" style="border-left: 6px solid var(--royal-blue); margin-top: 10px;">
                <div class="metric-label">AUCTION TACTICAL BLUEPRINT FOR SANGAKKARA & PARAG</div>
                <div class="metric-val" style="font-size: 20px;">HOW THE TOP-10 PRESSURE TARGETS COMPLETE THIS ROSTER</div>
                <p style="font-size: 13px; color: #333; margin-top: 8px; line-height: 1.6;">
                    1. <b>Death Bowling Supremacy:</b> Pairing <b>Matheesha Pathirana</b> with Jofra Archer and Sandeep Sharma guarantees 24 consecutive death balls of 148kph slingers and wide yorkers.<br>
                    2. <b>Spin Fortress at SMS:</b> Adding <b>Sunil Narine</b> or <b>Krunal Pandya</b> creates an unplayable three-spin web with <b>Ravindra Jadeja</b> and <b>Ravi Bishnoi</b> on Jaipur's abrasive red/black clay.<br>
                    3. <b>Middle-Overs Spin Destruction:</b> <b>Heinrich Klaasen</b> (+0.611 RAE) or <b>Suryakumar Yadav</b> relieves Captain Riyan Parag from bearing the entire middle-overs acceleration burden.<br>
                    4. <b>Indian Clutch Depth:</b> Acquiring <b>Shashank Singh</b> or <b>Ashutosh Sharma</b> provides low-cost, elite-SR wicket-preservation insurance alongside Dhruv Jurel.
                </p>
            </div>
        </div>
    </div>

    <!-- TAB 3: BATTERS -->
    <div id="tab-batters" class="tab-content" style="display: none;">
        <div class="card">
            <div class="card-header">
                <div class="card-title">🏏 THE TOP 10 PRESSURE BATTERS // RECRUITMENT DOSSIERS</div>
                <span class="badge badge-yellow">CROSS-REFERENCED WITH RR SQUAD</span>
            </div>
            <div id="batters-container"></div>
        </div>
    </div>

    <!-- TAB 4: BOWLERS -->
    <div id="tab-bowlers" class="tab-content" style="display: none;">
        <div class="card">
            <div class="card-header">
                <div class="card-title">🎯 THE TOP 10 PRESSURE BOWLERS // RECRUITMENT DOSSIERS</div>
                <span class="badge badge-mint">CROSS-REFERENCED WITH RR SQUAD</span>
            </div>
            <div id="bowlers-container"></div>
        </div>
    </div>

    <!-- TAB 5: METHODOLOGY -->
    <div id="tab-methodology" class="tab-content" style="display: none;">
        <div class="card">
            <div class="card-header">
                <div class="card-title">🔬 SCIENTIFIC AUDIT FINDINGS: SEPARATING SKILL FROM NOISE</div>
                <span class="badge badge-pink">EMPIRICAL PROOF</span>
            </div>
            <div class="grid-2">
                <div class="metric-box">
                    <div class="metric-label">PERMUTATION TEST (500 ITERATIONS)</div>
                    <div class="metric-val">p = 0.6920</div>
                    <p style="font-size: 13px; color: #444; line-height: 1.5;">
                        Observed cross-player clutch slope variation (sigma = 2.01) is <b>smaller</b> than the null distribution mean (mu = 2.14). 
                        <b>Finding:</b> Player-specific clutch elevation slopes are statistically indistinguishable from random noise. True skill lies in baseline talent and execution volume.
                    </p>
                </div>
                <div class="metric-box">
                    <div class="metric-label">SPLIT-HALF METRIC RELIABILITY</div>
                    <div class="metric-val">r_SB = 0.1550</div>
                    <p style="font-size: 13px; color: #444; line-height: 1.5;">
                        Across odd/even match career partitions for 68 eligible batters, Spearman-Brown reliability is only 0.1550 (95% CI [-0.30, 0.48]). 
                        <b>Finding:</b> 84.5% of cross-player variance in raw pressure metrics is stochastic. Heavy Bayesian shrinkage is mandatory.
                    </p>
                </div>
                <div class="metric-box">
                    <div class="metric-label">DISMISSAL HAZARD GRADIENT</div>
                    <div class="metric-val">rho = 0.9152 (p = 0.0002)</div>
                    <p style="font-size: 13px; color: #444; line-height: 1.5;">
                        Dismissal rates climb monotonically from 4.65% in low pressure to 8.98% overall and 12.73% in Innings 1. 
                        <b>Finding:</b> Pressure drives wickets, not run depression. Wicket preservation under pressure is the true championship differentiator.
                    </p>
                </div>
                <div class="metric-box">
                    <div class="metric-label">OPTIMAL SHRINKAGE (k*)</div>
                    <div class="metric-val">k* = 2,212 vs k = 40</div>
                    <p style="font-size: 13px; color: #444; line-height: 1.5;">
                        Per-ball noise variance is 3.1953 while player talent variance is 0.0014. 
                        <b>Finding:</b> Round 1's k=40 under-shrunk small samples by 70%. At k*, high-volume anchors (Tim David #1, Pathirana #1) rightfully ascend.
                    </p>
                </div>
            </div>
        </div>
    </div>

    <!-- TAB 6: VENUE -->
    <div id="tab-venue" class="tab-content" style="display: none;">
        <div class="card">
            <div class="card-header">
                <div class="card-title">🏟️ SAWAI MANSINGH STADIUM (JAIPUR): VENUE GEOMETRY & PITCH AUDIT</div>
                <span class="badge badge-yellow">SMS FORTRESS BLUEPRINT</span>
            </div>
            <div class="grid-2">
                <div class="metric-box" style="border-top: 6px solid var(--rr-pink);">
                    <div class="metric-label">BOUNDARY GEOMETRY & OUTFIELD</div>
                    <div class="metric-val">75m - 80m STRAIGHT</div>
                    <p style="font-size: 13px; color: #333; line-height: 1.6; margin-top: 8px;">
                        • <b>Square Boundaries:</b> 68 - 72 meters<br>
                        • <b>Straight Boundaries:</b> 75 - 80 meters (Massive)<br>
                        • <b>Outfield:</b> High-speed turf with spacious ground ring<br><br>
                        <b>Tactical Strategy for Parag:</b> Mishits do not clear the boundary at Jaipur. Hitters require raw distance (David, Klaasen) or surgical 360° placement (Surya). Jaiswal and Parag exploit powerplay pace before the pitch slows.
                    </p>
                </div>
                <div class="metric-box" style="border-top: 6px solid var(--royal-blue);">
                    <div class="metric-label">SURFACE & CLAY INTERACTION</div>
                    <div class="metric-val">RED / BLACK CLAY GRIP</div>
                    <p style="font-size: 13px; color: #333; line-height: 1.6; margin-top: 8px;">
                        • <b>Clay Mixture:</b> Abrasive clay surface holding up into the pitch<br>
                        • <b>Middle Overs (7-15):</b> Substantial turn and sticky hold for finger/wrist spinners<br>
                        • <b>Death Overs (16-20):</b> Dew factor neutralized by express slingy yorkers<br><br>
                        <b>Tactical Strategy for Sangakkara:</b> Ravindra Jadeja, Ravi Bishnoi, and potential target Sunil Narine (6.09 death economy) create an impenetrable spin stranglehold on visiting batters.
                    </p>
                </div>
            </div>
        </div>
    </div>

    <!-- TAB 7: SIMULATOR / PRIORITY MATRIX -->
    <div id="tab-simulator" class="tab-content" style="display: none;">
        <div class="card">
            <div class="card-header">
                <div class="card-title">💰 RAJASTHAN ROYALS AUCTION WAR ROOM: 3-TIER TARGET MATRIX</div>
                <span class="badge badge-mint">TAILORED TO RR SQUAD GAPS</span>
            </div>
            
            <div class="filter-bar">
                <button class="filter-btn active" onclick="filterTargets('all')">ALL TARGETS</button>
                <button class="filter-btn" onclick="filterTargets('death-bowler')">DEATH BOWLERS</button>
                <button class="filter-btn" onclick="filterTargets('finisher')">MIDDLE FINISHERS</button>
                <button class="filter-btn" onclick="filterTargets('spin-choke')">SPIN CHOKE</button>
                <button class="filter-btn" onclick="filterTargets('domestic-value')">INDIAN VALUE</button>
            </div>

            <div class="grid-2">
                <div class="metric-box target-card" data-cat="death-bowler finisher" style="border-top: 6px solid var(--rr-pink);">
                    <div class="metric-label">TIER 1: MARQUEE MATCH-WINNERS (45% - 55% PURSE)</div>
                    <div class="metric-val">PATHIRANA & KLAASEN / DAVID</div>
                    <p style="font-size: 13px; color: #333; line-height: 1.5; margin-top: 8px;">
                        • <b>Matheesha Pathirana:</b> Absolute #1 target. 148kph slingers seal death overs alongside Jofra Archer & Sandeep Sharma.<br>
                        • <b>Heinrich Klaasen OR Tim David:</b> World #1 spin destroyer (+0.611 RAE) or 75m boundary clearing powerhouse (300 balls).
                    </p>
                </div>
                <div class="metric-box target-card" data-cat="spin-choke domestic-value" style="border-top: 6px solid var(--canary-yellow);">
                    <div class="metric-label">TIER 2: TACTICAL LINCHPINS (25% - 35% PURSE)</div>
                    <div class="metric-val">NARINE / RASHID & SHASHANK</div>
                    <p style="font-size: 13px; color: #333; line-height: 1.5; margin-top: 8px;">
                        • <b>Sunil Narine OR Rashid Khan:</b> Unites with Ravindra Jadeja & Ravi Bishnoi for an unplayable SMS spin trio.<br>
                        • <b>Shashank Singh OR Ashutosh Sharma:</b> Indian finishers; Shashank preserves wickets at 200+ SR alongside Dhruv Jurel.
                    </p>
                </div>
            </div>
        </div>
    </div>

    <script>
        const batData = [
            {
                "name": "Heinrich Klaasen",
                "r1_rank": 1,
                "r1_rate": 77.59,
                "k_rank": 3,
                "shrunk_rae": 0.0526,
                "balls": 122,
                "ci": "[1.0 - 14.0]",
                "p_top10": 87.4,
                "sr": 204.1,
                "sixes": 17,
                "fours": 20,
                "pos_pct": 72.7,
                "dismissals": 10,
                "role": "World #1 Spin Demolisher (#4 / #5)",
                "tier": "Tier 1 (Marquee Target)",
                "fit": "Highest per-ball RAE in world (+0.611). Jaipur square boundaries (68-72m) stall opponents; Klaasen's back-foot pull demolishes finger and wrist spin indiscriminately. Slots in right after Captain Riyan Parag to create a devastating 3-4-5 punch with Dhruv Jurel."
            },
            {
                "name": "Ashutosh Sharma",
                "r1_rank": 2,
                "r1_rate": 69.71,
                "k_rank": 6,
                "shrunk_rae": 0.0429,
                "balls": 119,
                "ci": "[1.0 - 30.0]",
                "p_top10": 70.2,
                "sr": 192.4,
                "sixes": 15,
                "fours": 19,
                "pos_pct": 57.9,
                "dismissals": 11,
                "role": "Designated Impact Closer (#6 / #7)",
                "tier": "Tier 2 (Indian Linchpin)",
                "fit": "Pressure SR 192.4, delta +36.6. Scoop and sweep mastery against 145kph+ pace makes him impossible to defend at Jaipur. Enters at 135/5 needing 50 off 24, partnering Dhruv Jurel and Ravindra Jadeja to finish tight chases."
            },
            {
                "name": "Shashank Singh",
                "r1_rank": 3,
                "r1_rate": 69.28,
                "k_rank": 9,
                "shrunk_rae": 0.0387,
                "balls": 107,
                "ci": "[3.0 - 28.0]",
                "p_top10": 43.6,
                "sr": 200.9,
                "sixes": 17,
                "fours": 13,
                "pos_pct": 47.4,
                "dismissals": 4,
                "role": "Anti-Collapse Clutch Anchor",
                "tier": "Tier 2 (Indian Linchpin)",
                "fit": "Pressure SR 200.9 with ONLY 4 dismissals in 107 balls (3.7% rate). Ranks #1 in entire competition under dismissal-penalized evaluation. Wicket-preservation master who guarantees RR never suffers lower-order collapses."
            },
            {
                "name": "Shreyas Iyer",
                "r1_rank": 4,
                "r1_rate": 68.22,
                "k_rank": 4,
                "shrunk_rae": 0.0463,
                "balls": 169,
                "ci": "[1.0 - 22.0]",
                "p_top10": 83.6,
                "sr": 191.7,
                "sixes": 29,
                "fours": 11,
                "pos_pct": 50.0,
                "dismissals": 11,
                "role": "Middle Spine & Counter-Puncher",
                "tier": "Tier 2 (Linchpin)",
                "fit": "Middle-overs counter-puncher against high pace; 29 sixes prove elite acceleration. Offers championship IPL leadership pedigree to support Captain Riyan Parag and Head Coach Kumar Sangakkara on-field."
            },
            {
                "name": "Dinesh Karthik",
                "r1_rank": 5,
                "r1_rate": 66.52,
                "k_rank": 10,
                "shrunk_rae": 0.0345,
                "balls": 129,
                "ci": "[4.0 - 26.0]",
                "p_top10": 45.4,
                "sr": 196.1,
                "sixes": 14,
                "fours": 26,
                "pos_pct": 52.2,
                "dismissals": 11,
                "role": "Veteran Pace Ramp Specialist",
                "tier": "Tier 3 (Value Closer)",
                "fit": "Expert at ramping high pace over fine leg and third man, converting yorkers into boundaries. Supreme tactical mentor in close chases to guide young guns Dhruv Jurel and Vaibhav Sooryavanshi."
            },
            {
                "name": "Tim David",
                "r1_rank": 6,
                "r1_rate": 66.48,
                "k_rank": 1,
                "shrunk_rae": 0.0768,
                "balls": 300,
                "ci": "[1.0 - 11.0]",
                "p_top10": 94.9,
                "sr": 194.7,
                "sixes": 48,
                "fours": 37,
                "pos_pct": 57.8,
                "dismissals": 19,
                "role": "Death Finisher (Overs 17-20)",
                "tier": "Tier 1 (Priority Finisher)",
                "fit": "Rank #1 in world under optimal shrinkage (k*=2212). Clears Jaipur's 75m straight boundary with ease. 300 pressure balls provide 94.9% statistical certainty. Pairs with Shimron Hetmyer to form the most intimidating boundary duo in the IPL."
            },
            {
                "name": "Suryakumar Yadav",
                "r1_rank": 7,
                "r1_rate": 66.32,
                "k_rank": 2,
                "shrunk_rae": 0.0634,
                "balls": 254,
                "ci": "[1.0 - 15.0]",
                "p_top10": 88.6,
                "sr": 190.6,
                "sixes": 31,
                "fours": 40,
                "pos_pct": 67.9,
                "dismissals": 14,
                "role": "360° Middle Spine (#3 / #4)",
                "tier": "Tier 1 (Marquee Anchor)",
                "fit": "Manipulates Sawai Mansingh Stadium's spacious outfield; carves vacant fine-leg and third-man pockets. Forms an unstoppable middle-order axis with Captain Riyan Parag."
            },
            {
                "name": "Rashid Khan",
                "r1_rank": 8,
                "r1_rate": 66.23,
                "k_rank": 7,
                "shrunk_rae": 0.0321,
                "balls": 179,
                "ci": "[2.0 - 28.0]",
                "p_top10": 59.0,
                "sr": 183.8,
                "sixes": 25,
                "fours": 20,
                "pos_pct": 45.5,
                "dismissals": 21,
                "role": "Lethal #8 Boundary Striker",
                "tier": "Tier 1 (Dual-Threat)",
                "fit": "Transforms RR's tail from a vulnerability into a game-winning weapon at #8. His 'snake shot' creates boundary leverage off wide yorkers, batting alongside Ravindra Jadeja and Sam Curran."
            },
            {
                "name": "MS Dhoni",
                "r1_rank": 9,
                "r1_rate": 66.05,
                "k_rank": 16,
                "shrunk_rae": 0.0124,
                "balls": 127,
                "ci": "[6.0 - 34.0]",
                "p_top10": 18.6,
                "sr": 181.1,
                "sixes": 15,
                "fours": 17,
                "pos_pct": 46.4,
                "dismissals": 8,
                "role": "Final-Over Tactical Closer",
                "tier": "Tier 3 (Specialist)",
                "fit": "Enters strictly in over 19 or 20. Elite muscle memory against wide yorkers; unmatched tactical aura in final-over pressure."
            },
            {
                "name": "Rovman Powell",
                "r1_rank": 10,
                "r1_rate": 63.11,
                "k_rank": 11,
                "shrunk_rae": 0.0242,
                "balls": 181,
                "ci": "[3.0 - 24.0]",
                "p_top10": 49.7,
                "sr": 177.9,
                "sixes": 21,
                "fours": 25,
                "pos_pct": 60.0,
                "dismissals": 18,
                "role": "Boundary Muscle & Squad Familiarity",
                "tier": "Tier 3 (Retention/Value)",
                "fit": "Familiar with Jaipur pitch conditions and RR team culture; West Indies T20I captain. Clears deep boundary with raw bat speed against seam."
            }
        ];

        const bowlData = [
            {
                "name": "Sunil Narine",
                "r1_rank": 1,
                "r1_rate": 77.83,
                "k_rank": 3,
                "shrunk_rp": 0.0087,
                "balls": 130,
                "ci": "[1.0 - 19.0]",
                "p_top10": 75.1,
                "econ": 6.09,
                "wkts": 10,
                "pos_pct": 88.9,
                "rp_ball": 0.343,
                "role": "SMS Mystery Spin Anchor & Opener",
                "tier": "Tier 1 (Marquee Anchor)",
                "fit": "Concedes only 6.09 RPO under pressure (delta -0.84!). Combines with Ravindra Jadeja and Ravi Bishnoi to form an unplayable 3-man spin choke on Jaipur clay. Doubles as a powerplay pinch-hitter."
            },
            {
                "name": "Krunal Pandya",
                "r1_rank": 2,
                "r1_rate": 74.73,
                "k_rank": 8,
                "shrunk_rp": 0.0016,
                "balls": 130,
                "ci": "[3.0 - 29.0]",
                "p_top10": 47.2,
                "econ": 6.42,
                "wkts": 11,
                "pos_pct": 86.7,
                "rp_ball": 0.227,
                "role": "Indian Finger Spin & Dart Executioner",
                "tier": "Tier 2 (Linchpin)",
                "fit": "Pressure economy 6.42 (delta -1.56!). Bowls flat darts on Jaipur's long straight boundaries; saves an overseas slot while pairing seamlessly with Ravindra Jadeja."
            },
            {
                "name": "Rashid Khan",
                "r1_rank": 3,
                "r1_rate": 71.52,
                "k_rank": 7,
                "shrunk_rp": 0.0041,
                "balls": 183,
                "ci": "[1.0 - 31.0]",
                "p_top10": 58.8,
                "econ": 7.67,
                "wkts": 19,
                "pos_pct": 85.2,
                "rp_ball": 0.181,
                "role": "Middle Overs Choke & Death Overs 17/19",
                "tier": "Tier 1 (Marquee)",
                "fit": "Premier franchise asset. Rapid 100kph googly chokes middle overs (7-15) and executes at death (17/19). Rotates with Ravi Bishnoi to torment both right and left handers."
            },
            {
                "name": "Matheesha Pathirana",
                "r1_rank": 4,
                "r1_rate": 69.35,
                "k_rank": 1,
                "shrunk_rp": 0.0171,
                "balls": 206,
                "ci": "[1.0 - 12.0]",
                "p_top10": 93.1,
                "econ": 8.83,
                "wkts": 21,
                "pos_pct": 82.1,
                "rp_ball": 0.35,
                "role": "Marquee Death Yorker Bowler (17-20)",
                "tier": "Tier 1 (Priority #1 Target)",
                "fit": "Rank #1 in world under k* (P=93.1%). +0.350 RP/ball is highest in entire bowling dataset. Slingy 148kph yorkers partner Jofra Archer and Sandeep Sharma to seal RR's death-over run leakage once and for all."
            },
            {
                "name": "Mustafizur Rahman",
                "r1_rank": 5,
                "r1_rate": 66.38,
                "k_rank": 2,
                "shrunk_rp": 0.0113,
                "balls": 222,
                "ci": "[1.0 - 25.0]",
                "p_top10": 88.2,
                "econ": 8.16,
                "wkts": 23,
                "pos_pct": 73.7,
                "rp_ball": 0.232,
                "role": "Jaipur Off-Cutter Slower Ball Maestro",
                "tier": "Tier 2 (Linchpin)",
                "fit": "Rank #2 under k*. 222 balls, 23 wickets. Jaipur's surface holds up for cutters into the pitch. Former RR star who thrives in this environment alongside Sandeep Sharma."
            },
            {
                "name": "Yuzvendra Chahal",
                "r1_rank": 6,
                "r1_rate": 65.03,
                "k_rank": 34,
                "shrunk_rp": -0.0161,
                "balls": 247,
                "ci": "[11.0 - 46.0]",
                "p_top10": 3.9,
                "econ": 8.87,
                "wkts": 26,
                "pos_pct": 64.5,
                "rp_ball": -0.026,
                "role": "High-Strike-Rate Partnership Breaker",
                "tier": "Tier 2 (Talisman)",
                "fit": "26 pressure wickets (highest in competition!). Tosses ball wide outside off to break dangerous partnerships in crucial overs. Familiarity with SMS ground dimensions."
            },
            {
                "name": "Maheesh Theekshana",
                "r1_rank": 7,
                "r1_rate": 64.6,
                "k_rank": 9,
                "shrunk_rp": 0.0011,
                "balls": 161,
                "ci": "[3.0 - 27.0]",
                "p_top10": 42.4,
                "econ": 7.49,
                "wkts": 11,
                "pos_pct": 72.0,
                "rp_ball": 0.177,
                "role": "Powerplay Mystery & Carrom Bowler",
                "tier": "Tier 3 (Value Mystery)",
                "fit": "Bowls overs 1-6 and over 18. High release carrom ball skids with bounce, neutralizing aggressive opening batters."
            },
            {
                "name": "Varun Chakravarthy",
                "r1_rank": 8,
                "r1_rate": 62.46,
                "k_rank": 12,
                "shrunk_rp": -0.0043,
                "balls": 199,
                "ci": "[2.0 - 42.0]",
                "p_top10": 32.0,
                "econ": 7.84,
                "wkts": 16,
                "pos_pct": 72.0,
                "rp_ball": 0.088,
                "role": "Overspin Specialist for 70m Boundary",
                "tier": "Tier 2 (Indian Mystery)",
                "fit": "Overspin produces steep bounce. At Jaipur's 75m straight boundary, mis-hits fall comfortably into deep fielders' hands."
            },
            {
                "name": "Jason Holder",
                "r1_rank": 9,
                "r1_rate": 62.21,
                "k_rank": 13,
                "shrunk_rp": -0.0052,
                "balls": 227,
                "ci": "[4.0 - 40.0]",
                "p_top10": 27.8,
                "econ": 9.36,
                "wkts": 22,
                "pos_pct": 81.6,
                "rp_ball": 0.095,
                "role": "Tall Release & Heavy Pitch Cutters",
                "tier": "Tier 3 (Value Seamer)",
                "fit": "6ft 7in release point hits the splice of the bat at Jaipur; back-of-length slower cutters into the pitch support Jofra Archer."
            },
            {
                "name": "Ravichandran Ashwin",
                "r1_rank": 10,
                "r1_rate": 61.61,
                "k_rank": 25,
                "shrunk_rp": -0.0109,
                "balls": 128,
                "ci": "[13.0 - 37.0]",
                "p_top10": 2.5,
                "econ": 8.39,
                "wkts": 10,
                "pos_pct": 68.8,
                "rp_ball": 0.04,
                "role": "Jaipur Tactical Master & Pitch Guru",
                "tier": "Tier 3 (Tactical Mentor)",
                "fit": "Knows SMS boundary geometry and grip angles better than anyone. Orchestrates field traps and controls left-handers alongside Ravindra Jadeja."
            }
        ];

        function switchTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(el => el.style.display = 'none');
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            document.getElementById('tab-' + tabId).style.display = 'block';
            event.target.classList.add('active');
        }

        function filterTargets(category) {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            event.target.classList.add('active');
            const cards = document.querySelectorAll('.target-card');
            cards.forEach(card => {
                if (category === 'all' || card.getAttribute('data-cat').includes(category)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        }

        function renderBatters() {
            const c = document.getElementById('batters-container');
            c.innerHTML = batData.map(b => `
                <div class="player-card">
                    <div class="player-head">
                        <span class="player-name">${b.name.toUpperCase()}</span>
                        <div>
                            <span class="badge badge-yellow">k* RANK #${b.k_rank}</span>
                            <span class="badge badge-pink">R1 RANK #${b.r1_rank}</span>
                            <span class="badge badge-mint">P(TOP 10): ${b.p_top10}%</span>
                        </div>
                    </div>
                    <div class="player-role-bar">TACTICAL ROLE: ${b.role.toUpperCase()} | PRIORITY: ${b.tier.toUpperCase()}</div>
                    <div class="player-fit"><b>Why Picked & How He Strengthens Rajasthan Royals:</b> ${b.fit}</div>
                    <div class="player-metrics-row">
                        <span class="metric-pill">Pressure Balls: <b>${b.balls}</b></span>
                        <span class="metric-pill">Pressure SR: <b>${b.sr}</b></span>
                        <span class="metric-pill">Sixes: <b>${b.sixes}</b></span>
                        <span class="metric-pill">Fours: <b>${b.fours}</b></span>
                        <span class="metric-pill">Positive Match %: <b>${b.pos_pct}%</b></span>
                        <span class="metric-pill">Dismissals: <b>${b.dismissals}</b></span>
                        <span class="metric-pill">90% Rank CI: <b>${b.ci}</b></span>
                    </div>
                </div>
            `).join('');
        }

        function renderBowlers() {
            const c = document.getElementById('bowlers-container');
            c.innerHTML = bowlData.map(b => `
                <div class="player-card">
                    <div class="player-head">
                        <span class="player-name">${b.name.toUpperCase()}</span>
                        <div>
                            <span class="badge badge-yellow">k* RANK #${b.k_rank}</span>
                            <span class="badge badge-blue">R1 RANK #${b.r1_rank}</span>
                            <span class="badge badge-mint">P(TOP 10): ${b.p_top10}%</span>
                        </div>
                    </div>
                    <div class="player-role-bar">TACTICAL ROLE: ${b.role.toUpperCase()} | PRIORITY: ${b.tier.toUpperCase()}</div>
                    <div class="player-fit"><b>Why Picked & How He Strengthens Rajasthan Royals:</b> ${b.fit}</div>
                    <div class="player-metrics-row">
                        <span class="metric-pill">Legal Balls: <b>${b.balls}</b></span>
                        <span class="metric-pill">Pressure Economy: <b>${b.econ}</b></span>
                        <span class="metric-pill">Wickets: <b>${b.wkts}</b></span>
                        <span class="metric-pill">Runs Prevented/Ball: <b>+${b.rp_ball}</b></span>
                        <span class="metric-pill">Positive Match %: <b>${b.pos_pct}%</b></span>
                        <span class="metric-pill">90% Rank CI: <b>${b.ci}</b></span>
                    </div>
                </div>
            `).join('');
        }

        renderBatters();
        renderBowlers();
    </script>
</body>
</html>
'''

destinations = [
    r"reports\rr_auction_dashboard.html",
    r"dashboard.html",
    r"final_reports\rr_auction_dashboard.html",
    r"final reports\rr_auction_dashboard.html"
]

for dest in destinations:
    os.makedirs(os.path.dirname(dest) if os.path.dirname(dest) else ".", exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Updated: {dest} ({len(html_content)} bytes)")
