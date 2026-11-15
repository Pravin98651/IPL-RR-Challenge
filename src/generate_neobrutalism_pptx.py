"""
Neobrutalism Presentation Generator for Rajasthan Royals IPL 2027 Auction Blueprint
Uses python-pptx with authentic Neobrutalism design principles:
- 16:9 widescreen layout
- Chunky solid black borders (2.5pt - 3pt)
- Hard black offset drop shadows (zero blur, 0.08" offset)
- Bold geometric palette: RR Hot Pink, Royal Navy Blue, Canary Yellow, Electric Cyan, Neon Mint, Sharp Black, Cream Canvas
- Impactful typography, pill badges, and distinct high-contrast card modules
- Explains why EVERY single player (all 10 batters + all 10 bowlers) was picked and how they fit Rajasthan Royals
"""

import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# --- COLOR PALETTE ---
RR_PINK = RGBColor(234, 27, 134)       # #EA1B86 - Rajasthan Royals Pink
ROYAL_BLUE = RGBColor(11, 27, 61)     # #0B1B3D - Deep Royal Navy
CANARY_YELLOW = RGBColor(255, 230, 0) # #FFE600 - Pop Yellow
ELECTRIC_CYAN = RGBColor(0, 229, 255) # #00E5FF - Electric Cyan
NEON_MINT = RGBColor(0, 230, 118)     # #00E676 - Success / Mint
PURE_WHITE = RGBColor(255, 255, 255)  # #FFFFFF - Crisp White
SHARP_BLACK = RGBColor(17, 17, 17)    # #111111 - Stark Black
CREAM_CANVAS = RGBColor(246, 244, 238)# #F6F4EE - Off-White Canvas
MUTED_GRAY = RGBColor(110, 110, 110)  # #6E6E6E - Secondary text

FONT_TITLE = 'Arial Black'
FONT_HEADING = 'Trebuchet MS'
FONT_BODY = 'Arial'

class NeobrutalismDeckBuilder:
    def __init__(self, output_path: str = 'reports/rajasthan_royals_ipl2027_auction_blueprint.pptx'):
        self.output_path = output_path
        self.prs = pptx.Presentation()
        self.prs.slide_width = Inches(13.333)
        self.prs.slide_height = Inches(7.5)
        self.blank_layout = self.prs.slide_layouts[6]
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

    def _set_canvas_background(self, slide, bg_color=CREAM_CANVAS):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, self.prs.slide_width, self.prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = bg_color
        bg.line.fill.background()

    def add_card(self, slide, left, top, width, height, bg_color=PURE_WHITE, 
                 border_color=SHARP_BLACK, border_width=Pt(2.5), shadow=True, shadow_offset=Inches(0.08)):
        """Adds a Neobrutalist container card with solid black offset shadow."""
        if shadow:
            s_rect = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left + shadow_offset, top + shadow_offset, width, height)
            s_rect.fill.solid()
            s_rect.fill.fore_color.rgb = SHARP_BLACK
            s_rect.line.fill.background()
        
        c_rect = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
        c_rect.fill.solid()
        c_rect.fill.fore_color.rgb = bg_color
        c_rect.line.color.rgb = border_color
        c_rect.line.width = border_width
        return c_rect

    def add_badge(self, slide, left, top, text, bg_color=CANARY_YELLOW, text_color=SHARP_BLACK, 
                  font_size=11, height=Inches(0.38), min_width=Inches(1.2)):
        """Adds a stark pill badge with solid black border."""
        width = max(min_width, Inches(len(text) * 0.11 + 0.35))
        # shadow
        s_rect = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left + Inches(0.04), top + Inches(0.04), width, height)
        s_rect.fill.solid()
        s_rect.fill.fore_color.rgb = SHARP_BLACK
        s_rect.line.fill.background()
        
        badge = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
        badge.fill.solid()
        badge.fill.fore_color.rgb = bg_color
        badge.line.color.rgb = SHARP_BLACK
        badge.line.width = Pt(2.0)
        
        tf = badge.text_frame
        tf.word_wrap = False
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.text = text.upper()
        p.alignment = PP_ALIGN.CENTER
        p.font.name = FONT_TITLE
        p.font.size = Pt(font_size)
        p.font.bold = True
        p.font.color.rgb = text_color
        return left + width + Inches(0.12)

    def add_slide_header(self, slide, title_text: str, category_text: str = "RAJASTHAN ROYALS // IPL 2027 AUCTION BLUEPRINT"):
        """Standardized high-contrast Neobrutalist header."""
        self._set_canvas_background(slide)
        
        # Category strip
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
        tf_c = cat_box.text_frame
        p_c = tf_c.paragraphs[0]
        p_c.text = category_text.upper()
        p_c.font.name = FONT_TITLE
        p_c.font.size = Pt(11)
        p_c.font.bold = True
        p_c.font.color.rgb = RR_PINK

        # Main Title Box with stark underline bar
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(11.7), Inches(0.75))
        tf_t = title_box.text_frame
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.name = FONT_TITLE
        p_t.font.size = Pt(26)
        p_t.font.bold = True
        p_t.font.color.rgb = SHARP_BLACK

        # Underline bar
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.48), Inches(11.73), Inches(0.06))
        bar.fill.solid()
        bar.fill.fore_color.rgb = SHARP_BLACK
        bar.line.fill.background()

    def build_deck(self):
        print("Constructing 20 Neobrutalist Slides for Rajasthan Royals IPL 2027 Auction...")
        self._build_slide_01_title()
        self._build_slide_02_executive_summary()
        self._build_slide_03_methodology_architecture()
        self._build_slide_04_urgency_vs_leverage()
        self._build_slide_05_scientific_reality_clutch()
        self._build_slide_06_batters_master_table()
        self._build_slide_07_batters_klaasen_david()
        self._build_slide_08_batters_surya_ashutosh()
        self._build_slide_09_batters_shashank_shreyas()
        self._build_slide_10_batters_karthik_rashid()
        self._build_slide_11_batters_dhoni_powell()
        self._build_slide_12_bowlers_master_table()
        self._build_slide_13_bowlers_narine_pathirana()
        self._build_slide_14_bowlers_mustafizur_rashid()
        self._build_slide_15_bowlers_krunal_theekshana()
        self._build_slide_16_bowlers_varun_holder()
        self._build_slide_17_bowlers_ashwin_chahal()
        self._build_slide_18_jaipur_venue_dynamics()
        self._build_slide_19_auction_target_matrix()
        self._build_slide_20_conclusion_winning_xi()
        
        self.prs.save(self.output_path)
        print(f"Neobrutalism Presentation successfully saved to: {self.output_path}")

    # ==========================================
    # SLIDE 1: HERO TITLE COVER
    # ==========================================
    def _build_slide_01_title(self):
        slide = self.prs.slides.add_slide(self.blank_layout)
        self._set_canvas_background(slide, bg_color=CREAM_CANVAS)
        
        # Giant Pink Neobrutalist Hero Card
        self.add_card(slide, Inches(0.8), Inches(0.8), Inches(11.73), Inches(5.9), bg_color=PURE_WHITE, border_width=Pt(3.5), shadow_offset=Inches(0.12))
        
        # Inner Header Bar
        inner_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.73), Inches(0.6))
        inner_bar.fill.solid()
        inner_bar.fill.fore_color.rgb = ROYAL_BLUE
        inner_bar.line.color.rgb = SHARP_BLACK
        inner_bar.line.width = Pt(3.0)
        
        tf_bar = inner_bar.text_frame
        p_b = tf_bar.paragraphs[0]
        p_b.text = "★ RAJASTHAN ROYALS INTEL // IPL 2027 AUCTION MASTER WAR ROOM ★"
        p_b.alignment = PP_ALIGN.CENTER
        p_b.font.name = FONT_TITLE
        p_b.font.size = Pt(13)
        p_b.font.bold = True
        p_b.font.color.rgb = CANARY_YELLOW
        
        # Badges row
        cur_x = Inches(1.3)
        cur_x = self.add_badge(slide, cur_x, Inches(1.8), "OFFICIAL AUDITED DATA", bg_color=RR_PINK, text_color=PURE_WHITE)
        cur_x = self.add_badge(slide, cur_x, Inches(1.8), "194,014 BALLS", bg_color=CANARY_YELLOW, text_color=SHARP_BLACK)
        cur_x = self.add_badge(slide, cur_x, Inches(1.8), "BAYESIAN ESTIMATION", bg_color=ELECTRIC_CYAN, text_color=SHARP_BLACK)
        cur_x = self.add_badge(slide, cur_x, Inches(1.8), "SAWAI MANSINGH OPTIMIZED", bg_color=NEON_MINT, text_color=SHARP_BLACK)

        # Huge Title Text
        tb = slide.shapes.add_textbox(Inches(1.2), Inches(2.4), Inches(11.0), Inches(2.5))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p1 = tf.paragraphs[0]
        p1.text = "SUPER R SELECTOR"
        p1.font.name = FONT_TITLE
        p1.font.size = Pt(48)
        p1.font.bold = True
        p1.font.color.rgb = SHARP_BLACK
        
        p2 = tf.add_paragraph()
        p2.text = "PRESSURE INTELLIGENCE ENGINE"
        p2.font.name = FONT_TITLE
        p2.font.size = Pt(38)
        p2.font.bold = True
        p2.font.color.rgb = RR_PINK
        
        p3 = tf.add_paragraph()
        p3.text = "Identifying the Most Reliable T20 Players Under Pressure & Building Rajasthan Royals' Championship Squad for IPL 2027"
        p3.font.name = FONT_HEADING
        p3.font.size = Pt(17)
        p3.font.bold = True
        p3.font.color.rgb = ROYAL_BLUE
        
        # Bottom Callout Box inside Card
        bot_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.3), Inches(5.2), Inches(10.73), Inches(1.1))
        bot_box.fill.solid()
        bot_box.fill.fore_color.rgb = CREAM_CANVAS
        bot_box.line.color.rgb = SHARP_BLACK
        bot_box.line.width = Pt(2.0)
        
        tf_bot = bot_box.text_frame
        p_bot1 = tf_bot.paragraphs[0]
        p_bot1.text = "ARCHITECTURAL FOUNDATION: Rigorous Match State Reconstruction | Decoupled Situational Urgency & Leverage"
        p_bot1.font.name = FONT_TITLE
        p_bot1.font.size = Pt(11)
        p_bot1.font.bold = True
        p_bot1.font.color.rgb = SHARP_BLACK
        
        p_bot2 = tf_bot.add_paragraph()
        p_bot2.text = "Empirical Bayes Shrinkage (k*=2,212) | 1,000-Iteration Cluster Bootstrap | Specific SMS Stadium Tactical Mapping"
        p_bot2.font.name = FONT_BODY
        p_bot2.font.size = Pt(11)
        p_bot2.font.color.rgb = ROYAL_BLUE

    # ==========================================
    # SLIDE 2: EXECUTIVE SUMMARY & PROBLEM STATEMENT
    # ==========================================
    def _build_slide_02_executive_summary(self):
        slide = self.prs.slides.add_slide(self.blank_layout)
        self.add_slide_header(slide, "EXECUTIVE SUMMARY: SEPARATING SKILL FROM STOCHASTIC NOISE")
        
        # Left Card: The Problem Statement & Estimand Mismatch
        self.add_card(slide, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1), bg_color=PURE_WHITE)
        self.add_badge(slide, Inches(1.1), Inches(2.0), "THE ESTIMAND MISMATCH", bg_color=CANARY_YELLOW)
        
        tb = slide.shapes.add_textbox(Inches(1.0), Inches(2.6), Inches(5.2), Inches(4.0))
        tf = tb.text_frame
        tf.word_wrap = True
        
        def add_bullet(tf, title, body):
            p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
            p.text = title.upper() + ": "
            p.font.name = FONT_TITLE
            p.font.size = Pt(12)
            p.font.bold = True
            p.font.color.rgb = SHARP_BLACK
            
            p_sub = tf.add_paragraph()
            p_sub.text = body
            p_sub.font.name = FONT_BODY
            p_sub.font.size = Pt(11.5)
            p_sub.font.color.rgb = ROYAL_BLUE
            p_sub.space_after = Pt(12)

        add_bullet(tf, "Level vs. Marginal Elevation", 
                   "Most systems rank players by how well they score in pressure states (absolute performance). But the true research question is who elevates output when pressure escalates.")
        add_bullet(tf, "The Small Sample Trap", 
                   "Top T20 batters average only 5-6 pressure balls per match (107 to 300 pressure balls over 3 years). Without rigorous shrinkage, random boundary bursts create false 'clutch' heroes.")
        add_bullet(tf, "Rajasthan Royals Context", 
                   "RR has repeatedly fallen short in knockout games due to death-over run leakage (overs 17-20) and middle-overs spin stalls at Jaipur. This blueprint fixes both.")

        # Right Card: The Validated Solution Architecture
        self.add_card(slide, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.1), bg_color=PURE_WHITE)
        self.add_badge(slide, Inches(7.2), Inches(2.0), "THE SCIENTIFIC DISCOVERY", bg_color=RR_PINK, text_color=PURE_WHITE)
        
        tb2 = slide.shapes.add_textbox(Inches(7.1), Inches(2.6), Inches(5.2), Inches(4.0))
        tf2 = tb2.text_frame
        tf2.word_wrap = True
        
        add_bullet(tf2, "Clutch Elevation is Shared Noise", 
                   "A 500-iteration permutation test proves player-specific clutch slopes are statistically indistinguishable from random noise (p = 0.6920). Split-half reliability is only r_SB = 0.155.")
        add_bullet(tf2, "What Actually Matters", 
                   "True match-winning reliability comes from: 1) Elite baseline skill (u_i), 2) Surviving escalating dismissal hazard (dismissal rate rises from 4.6% to 12.7%), 3) Volume-backed durability (n > 200).")
        add_bullet(tf2, "Empirical Bayes Shrinkage (k*=2,212)", 
                   "Optimal shrinkage requires 94.8% pooling toward population mean at 120 balls. This propels proven volume anchors (Tim David #1, Pathirana #1) over volatile small samples.")

    # ==========================================
    # SLIDE 3: METHODOLOGY ARCHITECTURE (5 PILLARS)
    # ==========================================
    def _build_slide_03_methodology_architecture(self):
        slide = self.prs.slides.add_slide(self.blank_layout)
        self.add_slide_header(slide, "END-TO-END METHODOLOGY: FIVE SCIENTIFIC PILLARS")
        
        pillars = [
            ("PILLAR 1", "MATCH RECONSTRUCTION", "837 official matches (IPL + T20I), 194,014 balls. Reconciled 609 non-bowler dismissals, exact legal-ball countdowns, DLS par trajectories, super-over separation.", CANARY_YELLOW),
            ("PILLAR 2", "CONTEXTUAL RESIDUALS", "Out-of-fold HistGradientBoosting models with zero player identity. Predicts expected runs, boundaries, dots, wickets based purely on pitch, stage, target & phase. Generates RAE & RP.", ELECTRIC_CYAN),
            ("PILLAR 3", "DECOUPLED PRESSURE", "Completely decoupled Situational Urgency (task difficulty, RRR, wickets lost) from Match Leverage (E[|ΔWP|]). Solves hopeless chase distortions and validates monotonic dose-response.", RR_PINK),
            ("PILLAR 4", "EMPIRICAL BAYES k*", "Method of moments estimates k* = sigma_e^2 / sigma_u^2 = 2,212 balls (batters) and 2,000 balls (bowlers). Fixes the 70% under-shrinkage of Round 1's heuristic k=40.", NEON_MINT),
            ("PILLAR 5", "CLUSTER BOOTSTRAP", "1,000 match-level cluster bootstrap iterations. Resamples entire matches with replacement stratified by competition. Produces honest 90% rank intervals and P(Top 10) probabilities.", CANARY_YELLOW)
        ]
        
        col_w = Inches(2.2)
        spacing = Inches(0.18)
        start_x = Inches(0.8)
        
        for i, (p_num, title, desc, badge_col) in enumerate(pillars):
            x = start_x + i * (col_w + spacing)
            self.add_card(slide, x, Inches(1.8), col_w, Inches(5.1), bg_color=PURE_WHITE)
            self.add_badge(slide, x + Inches(0.2), Inches(2.0), p_num, bg_color=badge_col)
            
            tb = slide.shapes.add_textbox(x + Inches(0.15), Inches(2.6), col_w - Inches(0.3), Inches(4.1))
            tf = tb.text_frame
            tf.word_wrap = True
            
            p1 = tf.paragraphs[0]
            p1.text = title
            p1.font.name = FONT_TITLE
            p1.font.size = Pt(13)
            p1.font.bold = True
            p1.font.color.rgb = SHARP_BLACK
            p1.space_after = Pt(10)
            
            p2 = tf.add_paragraph()
            p2.text = desc
            p2.font.name = FONT_BODY
            p2.font.size = Pt(11)
            p2.font.color.rgb = ROYAL_BLUE

    # ==========================================
    # SLIDE 4: URGENCY VS LEVERAGE DECOUPLING
    # ==========================================
    def _build_slide_04_urgency_vs_leverage(self):
        slide = self.prs.slides.add_slide(self.blank_layout)
        self.add_slide_header(slide, "PRESSURE DECOUPLING: TASK DIFFICULTY VS MATCH SENSITIVITY")
        
        # Left: Situational Urgency Card
        self.add_card(slide, Inches(0.8), Inches(1.8), Inches(5.6), Inches(3.6), bg_color=PURE_WHITE)
        self.add_badge(slide, Inches(1.1), Inches(2.0), "DIMENSION A: SITUATIONAL URGENCY", bg_color=CANARY_YELLOW)
        
        tb = slide.shapes.add_textbox(Inches(1.1), Inches(2.6), Inches(5.0), Inches(2.6))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = "Measures intrinsic objective difficulty of the execution task."
        p.font.name = FONT_HEADING
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = SHARP_BLACK
        p.space_after = Pt(8)
        
        p2 = tf.add_paragraph()
        p2.text = "• Formulation: Normalized required run rate (RRR), pre-delivery wickets lost, ball scarcity (1 - balls_rem / sched), par deficit.\n• Validation: Strong monotonic dose-response across 10 deciles (rho = 0.8667, p = 0.0012).\n• Dismissal Correlation: Dismissal rate surges monotonically from 4.65% to 8.98% / 12.73%."
        p2.font.name = FONT_BODY
        p2.font.size = Pt(11)
        p2.font.color.rgb = ROYAL_BLUE

        # Right: Match Leverage Card
        self.add_card(slide, Inches(6.9), Inches(1.8), Inches(5.6), Inches(3.6), bg_color=PURE_WHITE)
        self.add_badge(slide, Inches(7.2), Inches(2.0), "DIMENSION B: MATCH LEVERAGE", bg_color=RR_PINK, text_color=PURE_WHITE)
        
        tb2 = slide.shapes.add_textbox(Inches(7.2), Inches(2.6), Inches(5.0), Inches(2.6))
        tf2 = tb2.text_frame
        tf2.word_wrap = True
        p3 = tf2.paragraphs[0]
        p3.text = "Measures win-probability sensitivity: LI(s) = E[|ΔWP|]."
        p3.font.name = FONT_HEADING
        p3.font.size = Pt(13)
        p3.font.bold = True
        p3.font.color.rgb = SHARP_BLACK
        p3.space_after = Pt(8)
        
        p4 = tf2.add_paragraph()
        p4.text = "• Formulation: Expected absolute win probability swing across 10 discrete transitions (dot, 1, 2, 3, 4, 6, wicket, extras, striker crossing).\n• Independent Innings Models: Calibrated logistic models for Innings 1 and Innings 2 (no flat 50% assumption for Innings 1).\n• Vectorized Engine: High-speed matrix calculation evaluates all 194k balls in <4 seconds."
        p4.font.name = FONT_BODY
        p4.font.size = Pt(11)
        p4.font.color.rgb = ROYAL_BLUE

        # Bottom Comparison Hero Banner
        self.add_card(slide, Inches(0.8), Inches(5.6), Inches(11.7), Inches(1.3), bg_color=ROYAL_BLUE, border_width=Pt(2.5))
        tb_bot = slide.shapes.add_textbox(Inches(1.0), Inches(5.7), Inches(11.3), Inches(1.1))
        tf_b = tb_bot.text_frame
        p_bt1 = tf_b.paragraphs[0]
        p_bt1.text = "★ THE CANONICAL TEST CASE: 72 RUNS NEEDED OFF 12 BALLS WITH 8 WICKETS DOWN ★"
        p_bt1.font.name = FONT_TITLE
        p_bt1.font.size = Pt(12)
        p_bt1.font.bold = True
        p_bt1.font.color.rgb = CANARY_YELLOW
        
        p_bt2 = tf_b.add_paragraph()
        p_bt2.text = "In the Round 1 50/50 hybrid, this hopeless chase registered as Moderate/High pressure because RRR was high. In CIE 2.0: Situational Urgency = 0.84 (EXTREME), while Match Leverage = 0.12 (MINIMAL). Decoupling stops hopeless lost causes from skewing clutch ratings while properly capturing extreme technical difficulty."
        p_bt2.font.name = FONT_BODY
        p_bt2.font.size = Pt(10.5)
        p_bt2.font.color.rgb = PURE_WHITE

    # ==========================================
    # SLIDE 5: SCIENTIFIC REALITY OF CLUTCH SKILL
    # ==========================================
    def _build_slide_05_scientific_reality_clutch(self):
        slide = self.prs.slides.add_slide(self.blank_layout)
        self.add_slide_header(slide, "THE EMPIRICAL VERDICT: IS 'CLUTCH SKILL' STATISTICALLY REAL?")
        
        # 3 Statistic Cards
        stat_cards = [
            ("PERMUTATION TEST", "p = 0.6920", "Observed beta spread (2.01) is smaller than null spread (2.14). Player clutch response slopes are indistinguishable from random noise.", RR_PINK, PURE_WHITE),
            ("SPLIT-HALF RELIABILITY", "r_SB = 0.1550", "Career-half split across 68 batters shows 95% CI [-0.30, 0.48]. 84.5% of between-batter variance in pressure performance is stochastic noise.", CANARY_YELLOW, SHARP_BLACK),
            ("WALK-FORWARD ACCURACY", "tau = 0.0971", "Historical clutch slope provides zero out-of-season predictive utility for 2025-2026. Precision@10 for predicting future pressure RAE is 0/10.", ELECTRIC_CYAN, SHARP_BLACK)
        ]
        
        for i, (title, val, desc, bg, text_col) in enumerate(stat_cards):
            x = Inches(0.8) + i * Inches(4.0)
            self.add_card(slide, x, Inches(1.8), Inches(3.7), Inches(2.2), bg_color=bg)
            
            tb = slide.shapes.add_textbox(x + Inches(0.15), Inches(1.9), Inches(3.4), Inches(2.0))
            tf = tb.text_frame
            tf.word_wrap = True
            
            p1 = tf.paragraphs[0]
            p1.text = title
            p1.font.name = FONT_TITLE
            p1.font.size = Pt(11)
            p1.font.bold = True
            p1.font.color.rgb = text_col
            
            p2 = tf.add_paragraph()
            p2.text = val
            p2.font.name = FONT_TITLE
            p2.font.size = Pt(28)
            p2.font.bold = True
            p2.font.color.rgb = text_col
            p2.space_after = Pt(4)
            
            p3 = tf.add_paragraph()
            p3.text = desc
            p3.font.name = FONT_BODY
            p3.font.size = Pt(10)
            p3.font.color.rgb = text_col

        # Lower Full-Width Card: What Actually Matters
        self.add_card(slide, Inches(0.8), Inches(4.3), Inches(11.7), Inches(2.6), bg_color=PURE_WHITE)
        self.add_badge(slide, Inches(1.1), Inches(4.5), "FRANCHISE IMPLICATION: WHAT RAJASTHAN ROYALS MUST TARGET", bg_color=NEON_MINT)
        
        tb_low = slide.shapes.add_textbox(Inches(1.1), Inches(5.1), Inches(11.1), Inches(1.7))
        tf_l = tb_low.text_frame
        tf_l.word_wrap = True
        
        p_l = tf_l.paragraphs[0]
        p_l.text = "1. ELITE ALL-SITUATION TALENT (u_i): Hitters like Klaasen and Surya win pressure matches not because they elevate, but because their baseline is so astronomical (+0.26 to +0.35 RAE/ball) that even under pressure compression, they outperform average batters."
        p_l.font.name = FONT_HEADING
        p_l.font.size = Pt(11.5)
        p_l.font.bold = True
        p_l.font.color.rgb = SHARP_BLACK
        p_l.space_after = Pt(6)
        
        p_l2 = tf_l.add_paragraph()
        p_l2.text = "2. DISMISSAL HAZARD MANAGEMENT: High pressure doubles the dismissal rate (4.6% -> 12.7%). Hitters who preserve their wicket under pressure (Shashank Singh: only 4 dismissals in 107 balls, 3.7% rate) provide far higher win probability than reckless boundary-hitters."
        p_l2.font.name = FONT_HEADING
        p_l2.font.size = Pt(11.5)
        p_l2.font.bold = True
        p_l2.font.color.rgb = ROYAL_BLUE
        p_l2.space_after = Pt(6)
        
        p_l3 = tf_l.add_paragraph()
        p_l3.text = "3. PROVEN EXPOSURE VOLUME (n > 200 BALLS): Tim David (300 balls, P=94.9%) and Surya (254 balls, P=88.6%) have weathered extreme variance. Small-sample stars (<125 balls) carry wide bootstrap intervals and must be treated with caution."
        p_l3.font.name = FONT_HEADING
        p_l3.font.size = Pt(11.5)
        p_l3.font.bold = True
        p_l3.font.color.rgb = RR_PINK

    # ==========================================
    # SLIDE 6: BATTERS MASTER TABLE
    # ==========================================
    def _build_slide_06_batters_master_table(self):
        slide = self.prs.slides.add_slide(self.blank_layout)
        self.add_slide_header(slide, "THE TOP 10 PRESSURE BATTERS: MASTER EVALUATION BOARD")
        
        # Add summary card containing clean neobrutalist table
        self.add_card(slide, Inches(0.8), Inches(1.8), Inches(11.73), Inches(5.1), bg_color=PURE_WHITE)
        
        rows = [
            ("PLAYER NAME", "R1 RANK", "R1 RATE", "k* RANK", "SHRUNK RAE", "BALLS", "90% RANK CI", "P(TOP 10)", "RR 2027 TACTICAL ROLE"),
            ("Tim David", "#6", "66.48", "#1", "+0.0768", "300", "[1.0 - 11.0]", "94.9%", "Death Finisher (Overs 17-20)"),
            ("Suryakumar Yadav", "#7", "66.32", "#2", "+0.0634", "254", "[1.0 - 15.0]", "90.3%", "360° Middle Spine (#3 / #4)"),
            ("Heinrich Klaasen", "#1", "77.59", "#3", "+0.0526", "122", "[1.0 - 14.0]", "87.4%", "Jaipur Spin Demolisher (#4 / #5)"),
            ("Shreyas Iyer", "#4", "68.22", "#4", "+0.0463", "169", "[1.0 - 22.0]", "83.6%", "Tactical Captain / Middle Stabilizer"),
            ("Ashutosh Sharma", "#2", "69.71", "#6", "+0.0429", "119", "[1.0 - 30.0]", "70.2%", "Designated Impact Closer (#7)"),
            ("Shashank Singh", "#3", "69.28", "#9", "+0.0387", "107", "[3.0 - 28.0]", "43.6%", "Anti-Collapse Clutch Anchor"),
            ("Dinesh Karthik", "#5", "66.52", "#10", "+0.0345", "129", "[4.0 - 26.0]", "45.4%", "Veteran Pace Ramp Finisher"),
            ("Rashid Khan", "#8", "66.23", "#7", "+0.0321", "179", "[2.0 - 28.0]", "59.0%", "Lethal #8 Boundary Striker"),
            ("Rovman Powell", "#10", "63.11", "#11", "+0.0242", "181", "[3.0 - 24.0]", "49.7%", "Incumbent RR Asset / Boundary Muscle"),
            ("MS Dhoni", "#9", "66.05", "#16", "+0.0124", "127", "[6.0 - 34.0]", "18.6%", "Final-Over Tactical Finisher")
        ]
        
        y_start = Inches(2.0)
        row_h = Inches(0.42)
        col_widths = [Inches(2.2), Inches(0.9), Inches(0.9), Inches(0.9), Inches(1.2), Inches(0.9), Inches(1.3), Inches(1.1), Inches(2.3)]
        
        for r_idx, row in enumerate(rows):
            is_hdr = (r_idx == 0)
            bg = ROYAL_BLUE if is_hdr else (CANARY_YELLOW if r_idx in [1, 2, 3] else (CREAM_CANVAS if r_idx % 2 == 1 else PURE_WHITE))
            txt_col = CANARY_YELLOW if is_hdr else (SHARP_BLACK if r_idx in [1, 2, 3] else ROYAL_BLUE)
            
            x_cur = Inches(0.95)
            for c_idx, val in enumerate(row):
                w = col_widths[c_idx]
                cell = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x_cur, y_start + r_idx * row_h, w, row_h)
                cell.fill.solid()
                cell.fill.fore_color.rgb = bg
                cell.line.color.rgb = SHARP_BLACK
                cell.line.width = Pt(1.5) if not is_hdr else Pt(2.0)
                
                tf = cell.text_frame
                tf.word_wrap = False
                tf.vertical_anchor = MSO_ANCHOR.MIDDLE
                p = tf.paragraphs[0]
                p.text = val
                p.alignment = PP_ALIGN.LEFT if c_idx in [0, 8] else PP_ALIGN.CENTER
                p.font.name = FONT_TITLE if (is_hdr or c_idx == 0) else FONT_BODY
                p.font.size = Pt(9.5) if not is_hdr else Pt(10)
                p.font.bold = True if (is_hdr or c_idx in [0, 7]) else False
                p.font.color.rgb = PURE_WHITE if is_hdr else (RR_PINK if c_idx == 7 and float(val.replace('%',''))>80 else txt_col)
                
                x_cur += w

    # ==========================================
    # SLIDE 7: BATTERS 1 & 2: KLAASEN & DAVID
    # ==========================================
    def _build_slide_07_batters_klaasen_david(self):
        slide = self.prs.slides.add_slide(self.blank_layout)
        self.add_slide_header(slide, "BATTERS #1 & #2: THE DEATH OVER FINISHER GODS")
        
        # Left Card: Heinrich Klaasen
        self.add_card(slide, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1), bg_color=PURE_WHITE)
        self.add_badge(slide, Inches(1.1), Inches(2.0), "RANK #1 (R1) / #3 (k*)", bg_color=CANARY_YELLOW)
        self.add_badge(slide, Inches(3.4), Inches(2.0), "HEINRICH KLAASEN", bg_color=RR_PINK, text_color=PURE_WHITE)
        
        tb = slide.shapes.add_textbox(Inches(1.1), Inches(2.6), Inches(5.0), Inches(4.1))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = "EMPIRICAL DATA PROFILE:"
        p.font.name = FONT_TITLE
        p.font.size = Pt(12)
        p.font.color.rgb = SHARP_BLACK
        
        p1 = tf.add_paragraph()
        p1.text = "• Pressure Balls: 122 balls | RAE: +0.611 / ball (Highest in Dataset)\n• Pressure SR: 204.1 | Normal SR: 163.2 | Delta SR: +40.9\n• Match Consistency: 72.7% positive matches | 17 Sixes, 20 Fours\n• Bootstrap Stability: P(Top 10) = 87.4% | 90% Rank CI: [1.0 - 14.0]"
        p1.font.name = FONT_BODY
        p1.font.size = Pt(11)
        p1.font.color.rgb = ROYAL_BLUE
        p1.space_after = Pt(10)
        
        p2 = tf.add_paragraph()
        p2.text = "HOW HE STRENGTHENS RAJASTHAN ROYALS IN 2027:"
        p2.font.name = FONT_TITLE
        p2.font.size = Pt(12)
        p2.font.color.rgb = RR_PINK
        
        p3 = tf.add_paragraph()
        p3.text = "1. JAIPUR SPIN DEMOLISHER: Sawai Mansingh Stadium has 68-72m square boundaries where finger/wrist spin historically slows RR's middle overs. Klaasen's back-foot pull and lofted sweep demolish spin regardless of grip.\n2. MULTI-PHASE FLEXIBILITY: Can bat #4 if early wickets fall, or #5 to execute a death assault. Doubles as elite overseas wicketkeeping option."
        p3.font.name = FONT_BODY
        p3.font.size = Pt(11)
        p3.font.color.rgb = SHARP_BLACK

        # Right Card: Tim David
        self.add_card(slide, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.1), bg_color=PURE_WHITE)
        self.add_badge(slide, Inches(7.2), Inches(2.0), "RANK #1 (k*) / #6 (R1)", bg_color=NEON_MINT)
        self.add_badge(slide, Inches(9.5), Inches(2.0), "TIM DAVID", bg_color=ROYAL_BLUE, text_color=CANARY_YELLOW)
        
        tb2 = slide.shapes.add_textbox(Inches(7.2), Inches(2.6), Inches(5.0), Inches(4.1))
        tf2 = tb2.text_frame
        tf2.word_wrap = True
        
        p_r = tf2.paragraphs[0]
        p_r.text = "EMPIRICAL DATA PROFILE:"
        p_r.font.name = FONT_TITLE
        p_r.font.size = Pt(12)
        p_r.font.color.rgb = SHARP_BLACK
        
        p_r1 = tf2.add_paragraph()
        p_r1.text = "• Pressure Balls: 300 balls (Most in Dataset) | RAE: +0.467 / ball\n• Pressure SR: 194.7 | 48 Sixes, 37 Fours | 57.8% positive matches\n• Optimal Shrunk RAE: +0.0768 (Rank #1 in World under k*)\n• Bootstrap Stability: P(Top 10) = 94.9% (Highest Certainty) | CI: [1 - 11]"
        p_r1.font.name = FONT_BODY
        p_r1.font.size = Pt(11)
        p_r1.font.color.rgb = ROYAL_BLUE
        p_r1.space_after = Pt(10)
        
        p_r2 = tf2.add_paragraph()
        p_r2.text = "HOW HE STRENGTHENS RAJASTHAN ROYALS IN 2027:"
        p_r2.font.name = FONT_TITLE
        p_r2.font.size = Pt(12)
        p_r2.font.color.rgb = RR_PINK
        
        p_r3 = tf2.add_paragraph()
        p_r3.text = "1. JAIPUR 75m STRAIGHT BOUNDARY CLEARER: When 40 runs are required off the last 3 overs, David's reach and bat speed clear Jaipur's massive long-on/long-off boundary where mishits become catches.\n2. IRONCLAD SAMPLE VOLUME: Unlike 1-season wonders, David has survived 300 pressure deliveries. He is RR's bulletproof 20th-over finisher."
        p_r3.font.name = FONT_BODY
        p_r3.font.size = Pt(11)
        p_r3.font.color.rgb = SHARP_BLACK

    # ==========================================
    # SLIDE 8: BATTERS 3 & 4: SURYA & ASHUTOSH
    # ==========================================
    def _build_slide_08_batters_surya_ashutosh(self):
        slide = self.prs.slides.add_slide(self.blank_layout)
        self.add_slide_header(slide, "BATTERS #3 & #4: 360° FIELD DISRUPTORS & IMPACT CLOSERS")
        
        # Left: Suryakumar Yadav
        self.add_card(slide, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1), bg_color=PURE_WHITE)
        self.add_badge(slide, Inches(1.1), Inches(2.0), "RANK #2 (k*) / #7 (R1)", bg_color=ELECTRIC_CYAN)
        self.add_badge(slide, Inches(3.4), Inches(2.0), "SURYAKUMAR YADAV", bg_color=SHARP_BLACK, text_color=PURE_WHITE)
        
        tb = slide.shapes.add_textbox(Inches(1.1), Inches(2.6), Inches(5.0), Inches(4.1))
        tf = tb.text_frame
        tf.word_wrap = True
        
        tf.paragraphs[0].text = "EMPIRICAL DATA PROFILE:"
        tf.paragraphs[0].font.name = FONT_TITLE
        tf.paragraphs[0].font.size = Pt(12)
        
        p1 = tf.add_paragraph()
        p1.text = "• Pressure Balls: 254 balls | RAE: +0.413 / ball | Pressure SR: 190.6\n• 40 Fours, 31 Sixes | 67.9% Positive Pressure Matches\n• Shrunk RAE: +0.0634 (Rank #2 under k*) | P(Top 10) = 88.6%\n• Bootstrap 90% Rank CI: [1.0 - 15.0] (Mean Rank: 5.15)"
        p1.font.name = FONT_BODY
        p1.font.size = Pt(11)
        p1.font.color.rgb = ROYAL_BLUE
        p1.space_after = Pt(10)
        
        p2 = tf.add_paragraph()
        p2.text = "HOW HE STRENGTHENS RAJASTHAN ROYALS IN 2027:"
        p2.font.name = FONT_TITLE
        p2.font.size = Pt(12)
        p2.font.color.rgb = RR_PINK
        
        p3 = tf.add_paragraph()
        p3.text = "1. GEOMETRY MANIPULATION: Jaipur's deep boundaries mean captains push fielders to the ropes. Surya's scoops, ramps, and late cuts exploit vacant fine-leg and third-man pockets with surgical ease.\n2. SAMSON-SURYA TANDEM: Forming a #3-#4 axis with Sanju Samson makes RR's top order impossible to plan against for any bowling attack in world cricket."
        p3.font.name = FONT_BODY
        p3.font.size = Pt(11)
        p3.font.color.rgb = SHARP_BLACK

        # Right: Ashutosh Sharma
        self.add_card(slide, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.1), bg_color=PURE_WHITE)
        self.add_badge(slide, Inches(7.2), Inches(2.0), "RANK #2 (R1) / #6 (k*)", bg_color=CANARY_YELLOW)
        self.add_badge(slide, Inches(9.5), Inches(2.0), "ASHUTOSH SHARMA", bg_color=RR_PINK, text_color=PURE_WHITE)
        
        tb2 = slide.shapes.add_textbox(Inches(7.2), Inches(2.6), Inches(5.0), Inches(4.1))
        tf2 = tb2.text_frame
        tf2.word_wrap = True
        
        tf2.paragraphs[0].text = "EMPIRICAL DATA PROFILE:"
        tf2.paragraphs[0].font.name = FONT_TITLE
        tf2.paragraphs[0].font.size = Pt(12)
        
        p_r1 = tf2.add_paragraph()
        p_r1.text = "• Pressure Balls: 119 balls | Pressure SR: 192.4 (Normal: 155.8)\n• Delta SR: +36.6 | RAE: +0.431 / ball | 15 Sixes, 19 Fours\n• Win Probability Added / Ball: +1.39% | Positive Match Rate: 57.9%\n• CIE Urgency Response Slope (beta): +0.834 (Hyper-Clutch Accelerator)"
        p_r1.font.name = FONT_BODY
        p_r1.font.size = Pt(11)
        p_r1.font.color.rgb = ROYAL_BLUE
        p_r1.space_after = Pt(10)
        
        p_r2 = tf2.add_paragraph()
        p_r2.text = "HOW HE STRENGTHENS RAJASTHAN ROYALS IN 2027:"
        p_r2.font.name = FONT_TITLE
        p_r2.font.size = Pt(12)
        p_r2.font.color.rgb = RR_PINK
        
        p_r3 = tf2.add_paragraph()
        p_r3.text = "1. IMPACT PLAYER SPECIALIST: High-leverage chase weapon. Entering at 135/5 with 24 balls left needing 48 runs, Ashutosh has proven he can hit boundaries from ball one against elite fast bowling.\n2. HIGH ROSTER VALUE: Indian domestic salary tier allows RR to deploy maximum purse on marquee bowling targets like Pathirana while securing elite death batting."
        p_r3.font.name = FONT_BODY
        p_r3.font.size = Pt(11)
        p_r3.font.color.rgb = SHARP_BLACK

    # ==========================================
    # SLIDE 9: BATTERS 5 & 6: SHASHANK & SHREYAS
    # ==========================================
    def _build_slide_09_batters_shashank_shreyas(self):
        slide = self.prs.slides.add_slide(self.blank_layout)
        self.add_slide_header(slide, "BATTERS #5 & #6: CHASE MASTERS & WICKET PRESERVERS")
        
        # Left: Shashank Singh
        self.add_card(slide, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1), bg_color=PURE_WHITE)
        self.add_badge(slide, Inches(1.1), Inches(2.0), "RANK #3 (R1) / #9 (k*)", bg_color=CANARY_YELLOW)
        self.add_badge(slide, Inches(3.4), Inches(2.0), "SHASHANK SINGH", bg_color=ROYAL_BLUE, text_color=CANARY_YELLOW)
        
        tb = slide.shapes.add_textbox(Inches(1.1), Inches(2.6), Inches(5.0), Inches(4.1))
        tf = tb.text_frame
        tf.word_wrap = True
        
        tf.paragraphs[0].text = "EMPIRICAL DATA PROFILE:"
        tf.paragraphs[0].font.name = FONT_TITLE
        tf.paragraphs[0].font.size = Pt(12)
        
        p1 = tf.add_paragraph()
        p1.text = "• Pressure Balls: 107 balls | Pressure SR: 200.9 (Normal: 152.3)\n• Delta Strike Rate: +48.6 (Highest Delta in Entire Dataset!)\n• Dismissals: ONLY 4 dismissals in 107 balls (Dismissal Rate: 3.7%)\n• Dismissal-Penalized RAE: Ranks #1 among all 40 eligible batters!"
        p1.font.name = FONT_BODY
        p1.font.size = Pt(11)
        p1.font.color.rgb = ROYAL_BLUE
        p1.space_after = Pt(10)
        
        p2 = tf.add_paragraph()
        p2.text = "HOW HE STRENGTHENS RAJASTHAN ROYALS IN 2027:"
        p2.font.name = FONT_TITLE
        p2.font.size = Pt(12)
        p2.font.color.rgb = RR_PINK
        
        p3 = tf.add_paragraph()
        p3.text = "1. ANTI-COLLAPSE INSURANCE: High pressure increases wicket hazard by over 100%. Shashank provides 200+ strike-rate hitting while virtually never getting out, shielding RR's tail from exposure.\n2. DOMESTIC MATURITY: Plays high-percentage cricketing shots with elite power. Ideal at #6 or #7 for tense chases at Jaipur."
        p3.font.name = FONT_BODY
        p3.font.size = Pt(11)
        p3.font.color.rgb = SHARP_BLACK

        # Right: Shreyas Iyer
        self.add_card(slide, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.1), bg_color=PURE_WHITE)
        self.add_badge(slide, Inches(7.2), Inches(2.0), "RANK #4 (R1) / #4 (k*)", bg_color=NEON_MINT)
        self.add_badge(slide, Inches(9.5), Inches(2.0), "SHREYAS IYER", bg_color=SHARP_BLACK, text_color=PURE_WHITE)
        
        tb2 = slide.shapes.add_textbox(Inches(7.2), Inches(2.6), Inches(5.0), Inches(4.1))
        tf2 = tb2.text_frame
        tf2.word_wrap = True
        
        tf2.paragraphs[0].text = "EMPIRICAL DATA PROFILE:"
        tf2.paragraphs[0].font.name = FONT_TITLE
        tf2.paragraphs[0].font.size = Pt(12)
        
        p_r1 = tf2.add_paragraph()
        p_r1.text = "• Pressure Balls: 169 balls | Pressure SR: 191.7 (Normal: 149.3)\n• Delta SR: +42.4 | RAE: +0.430 / ball | 29 Sixes, 11 Fours\n• Shrunk RAE: +0.0463 (Rank #4 under k*) | P(Top 10) = 83.6%\n• Bootstrap 90% Rank CI: [1.0 - 22.0] (Mean Rank: 8.41)"
        p_r1.font.name = FONT_BODY
        p_r1.font.size = Pt(11)
        p_r1.font.color.rgb = ROYAL_BLUE
        p_r1.space_after = Pt(10)
        
        p_r2 = tf2.add_paragraph()
        p_r2.text = "HOW HE STRENGTHENS RAJASTHAN ROYALS IN 2027:"
        p_r2.font.name = FONT_TITLE
        p_r2.font.size = Pt(12)
        p_r2.font.color.rgb = RR_PINK
        
        p_r3 = tf2.add_paragraph()
        p_r3.text = "1. MIDDLE-ORDER TACTICAL SPINE: Shreyas anchors middle overs against spin, with 29 sixes proving he can step on the gas when required run rates mount.\n2. TACTICAL LEADERSHIP: Championship-winning IPL captaincy pedigree. Takes tactical burden off Sanju Samson, giving RR dual leadership on the field."
        p_r3.font.name = FONT_BODY
        p_r3.font.size = Pt(11)
        p_r3.font.color.rgb = SHARP_BLACK

    # ==========================================
    # SLIDE 10: BATTERS 7 & 8: KARTHIK & RASHID
    # ==========================================
    def _build_slide_10_batters_karthik_rashid(self):
        slide = self.prs.slides.add_slide(self.blank_layout)
        self.add_slide_header(slide, "BATTERS #7 & #8: CLUTCH ACCELERATORS & LOWER-ORDER WEAPONS")
        
        # Left: Dinesh Karthik
        self.add_card(slide, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1), bg_color=PURE_WHITE)
        self.add_badge(slide, Inches(1.1), Inches(2.0), "RANK #5 (R1) / #10 (k*)", bg_color=CANARY_YELLOW)
        self.add_badge(slide, Inches(3.4), Inches(2.0), "DINESH KARTHIK", bg_color=ROYAL_BLUE, text_color=PURE_WHITE)
        
        tb = slide.shapes.add_textbox(Inches(1.1), Inches(2.6), Inches(5.0), Inches(4.1))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.paragraphs[0].text = "EMPIRICAL DATA PROFILE:"
        tf.paragraphs[0].font.name = FONT_TITLE
        tf.paragraphs[0].font.size = Pt(12)
        
        p1 = tf.add_paragraph()
        p1.text = "• Pressure Balls: 129 balls | Pressure SR: 196.1 (Normal: 160.0)\n• Delta SR: +36.1 | RAE: +0.368 / ball | 26 Fours, 14 Sixes\n• Positive Match Rate: 52.2% | CIE Urgency Slope (beta): +0.791\n• Boundary Execution: 31.0% boundary rate in high-pressure death overs"
        p1.font.name = FONT_BODY
        p1.font.size = Pt(11)
        p1.font.color.rgb = ROYAL_BLUE
        p1.space_after = Pt(10)
        
        p2 = tf.add_paragraph()
        p2.text = "HOW HE STRENGTHENS RAJASTHAN ROYALS IN 2027:"
        p2.font.name = FONT_TITLE
        p2.font.size = Pt(12)
        p2.font.color.rgb = RR_PINK
        
        p3 = tf.add_paragraph()
        p3.text = "1. PACE RAMP MASTERY: Expert at using bowlers' 145kph pace against them over fine-leg and third-man at Jaipur, turning dot-ball yorkers into boundaries.\n2. CLUTCH FINISHING MENTOR: High situational awareness under pressure; provides vital tactical clarity in frantic final-over chases."
        p3.font.name = FONT_BODY
        p3.font.size = Pt(11)
        p3.font.color.rgb = SHARP_BLACK

        # Right: Rashid Khan (Batter)
        self.add_card(slide, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.1), bg_color=PURE_WHITE)
        self.add_badge(slide, Inches(7.2), Inches(2.0), "RANK #8 (R1) / #7 (k*)", bg_color=NEON_MINT)
        self.add_badge(slide, Inches(9.5), Inches(2.0), "RASHID KHAN (BAT)", bg_color=RR_PINK, text_color=PURE_WHITE)
        
        tb2 = slide.shapes.add_textbox(Inches(7.2), Inches(2.6), Inches(5.0), Inches(4.1))
        tf2 = tb2.text_frame
        tf2.word_wrap = True
        tf2.paragraphs[0].text = "EMPIRICAL DATA PROFILE:"
        tf2.paragraphs[0].font.name = FONT_TITLE
        tf2.paragraphs[0].font.size = Pt(12)
        
        p_r1 = tf2.add_paragraph()
        p_r1.text = "• Pressure Balls: 179 balls | Pressure SR: 183.8 (Normal: 140.9)\n• Delta Strike Rate: +42.9 | 25 Sixes, 20 Fours in 179 balls\n• RAE: +0.344 / ball | Shrunk RAE: +0.0321 (Rank #7 under k*)\n• Dual Qualifier: Only player in world ranked Top 10 in bat AND bowl!"
        p_r1.font.name = FONT_BODY
        p_r1.font.size = Pt(11)
        p_r1.font.color.rgb = ROYAL_BLUE
        p_r1.space_after = Pt(10)
        
        p_r2 = tf2.add_paragraph()
        p_r2.text = "HOW HE STRENGTHENS RAJASTHAN ROYALS IN 2027:"
        p_r2.font.name = FONT_TITLE
        p_r2.font.size = Pt(12)
        p_r2.font.color.rgb = RR_PINK
        
        p_r3 = tf2.add_paragraph()
        p_r3.text = "1. WEAPONIZING #8: Eliminates RR's traditional tail-end paralysis. Having Rashid at #8 means requiring 24 off 10 balls remains completely achievable.\n2. 'SNAKE SHOT' LEVERAGE: Generates boundary power off wide yorkers where standard batters can only manage singles."
        p_r3.font.name = FONT_BODY
        p_r3.font.size = Pt(11)
        p_r3.font.color.rgb = SHARP_BLACK

    # ==========================================
    # SLIDE 11: BATTERS 9 & 10: DHONI & POWELL
    # ==========================================
    def _build_slide_11_batters_dhoni_powell(self):
        slide = self.prs.slides.add_slide(self.blank_layout)
        self.add_slide_header(slide, "BATTERS #9 & #10: ICE-COLD CLOSERS & INCUMBENT ASSETS")
        
        # Left: MS Dhoni
        self.add_card(slide, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1), bg_color=PURE_WHITE)
        self.add_badge(slide, Inches(1.1), Inches(2.0), "RANK #9 (R1) / #16 (k*)", bg_color=CANARY_YELLOW)
        self.add_badge(slide, Inches(3.4), Inches(2.0), "MS DHONI", bg_color=SHARP_BLACK, text_color=CANARY_YELLOW)
        
        tb = slide.shapes.add_textbox(Inches(1.1), Inches(2.6), Inches(5.0), Inches(4.1))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.paragraphs[0].text = "EMPIRICAL DATA PROFILE:"
        tf.paragraphs[0].font.name = FONT_TITLE
        tf.paragraphs[0].font.size = Pt(12)
        
        p1 = tf.add_paragraph()
        p1.text = "• Pressure Balls: 127 balls | Pressure SR: 181.1 (Normal: 137.8)\n• Delta SR: +43.3 | 15 Sixes, 17 Fours | 8 Dismissals\n• CIE Urgency Response Slope (beta): +1.025 (Hyper-Clutch Closer)\n• Note on k*: Low volume/matches drops rank to #16 (P(Top10)=18.6%)"
        p1.font.name = FONT_BODY
        p1.font.size = Pt(11)
        p1.font.color.rgb = ROYAL_BLUE
        p1.space_after = Pt(10)
        
        p2 = tf.add_paragraph()
        p2.text = "HOW HE STRENGTHENS RAJASTHAN ROYALS IN 2027:"
        p2.font.name = FONT_TITLE
        p2.font.size = Pt(12)
        p2.font.color.rgb = RR_PINK
        
        p3 = tf.add_paragraph()
        p3.text = "1. FINAL-OVER SPECIALIST: Enters in over 19 or 20 purely to hit boundaries against express pace. Elite muscle memory against wide yorkers.\n2. PRESSURE BENCHMARK: Demonstrates that genuine closing ability requires absorbing pressure and punishing execution errors."
        p3.font.name = FONT_BODY
        p3.font.size = Pt(11)
        p3.font.color.rgb = SHARP_BLACK

        # Right: Rovman Powell
        self.add_card(slide, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.1), bg_color=PURE_WHITE)
        self.add_badge(slide, Inches(7.2), Inches(2.0), "RANK #10 (R1) / #11 (k*)", bg_color=ELECTRIC_CYAN)
        self.add_badge(slide, Inches(9.5), Inches(2.0), "ROVMAN POWELL", bg_color=RR_PINK, text_color=PURE_WHITE)
        
        tb2 = slide.shapes.add_textbox(Inches(7.2), Inches(2.6), Inches(5.0), Inches(4.1))
        tf2 = tb2.text_frame
        tf2.word_wrap = True
        tf2.paragraphs[0].text = "EMPIRICAL DATA PROFILE:"
        tf2.paragraphs[0].font.name = FONT_TITLE
        tf2.paragraphs[0].font.size = Pt(12)
        
        p_r1 = tf2.add_paragraph()
        p_r1.text = "• Pressure Balls: 181 balls | Pressure SR: 177.9 (Normal: 142.7)\n• Delta SR: +35.2 | RAE: +0.310 / ball | 21 Sixes, 25 Fours\n• Positive Match Rate: 60.0% | Shrunk RAE: +0.0242 (Rank #11)\n• Bootstrap 90% Rank CI: [3.0 - 24.0] (Mean Rank: 11.63)"
        p_r1.font.name = FONT_BODY
        p_r1.font.size = Pt(11)
        p_r1.font.color.rgb = ROYAL_BLUE
        p_r1.space_after = Pt(10)
        
        p_r2 = tf2.add_paragraph()
        p_r2.text = "HOW HE STRENGTHENS RAJASTHAN ROYALS IN 2027:"
        p_r2.font.name = FONT_TITLE
        p_r2.font.size = Pt(12)
        p_r2.font.color.rgb = RR_PINK
        
        p_r3 = tf2.add_paragraph()
        p_r3.text = "1. PROVEN RR RETENTION CANDIDATE: Already familiar with Jaipur home ground and team culture; West Indies T20I captaincy experience.\n2. HIGH-PACE POWER: Hits 145kph+ seam bowling down the ground, complementing touch players in RR's top order."
        p_r3.font.name = FONT_BODY
        p_r3.font.size = Pt(11)
        p_r3.font.color.rgb = SHARP_BLACK

    # ==========================================
    # SLIDE 12: BOWLERS MASTER TABLE
    # ==========================================
    def _build_slide_12_bowlers_master_table(self):
        slide = self.prs.slides.add_slide(self.blank_layout)
        self.add_slide_header(slide, "THE TOP 10 PRESSURE BOWLERS: MASTER EVALUATION BOARD")
        
        self.add_card(slide, Inches(0.8), Inches(1.8), Inches(11.73), Inches(5.1), bg_color=PURE_WHITE)
        
        rows = [
            ("BOWLER NAME", "R1 RANK", "R1 RATE", "k* RANK", "SHRUNK RP", "LEGAL BALLS", "90% RANK CI", "P(TOP 10)", "RR 2027 TACTICAL ROLE"),
            ("Matheesha Pathirana", "#4", "69.35", "#1", "+0.0171", "206", "[1.0 - 12.0]", "93.1%", "Marquee Death Yorker Specialist (17-20)"),
            ("Mustafizur Rahman", "#5", "66.38", "#2", "+0.0113", "222", "[1.0 - 25.0]", "76.2%", "Jaipur Off-Cutter Slower Ball Maestro"),
            ("Rashid Khan", "#3", "71.52", "#7", "+0.0041", "183", "[1.0 - 31.0]", "58.8%", "Middle Overs Choke & Death Overs 17/19"),
            ("Sunil Narine", "#1", "77.83", "#3", "+0.0087", "130", "[1.0 - 19.0]", "75.1%", "Sawai Mansingh Mystery Spin Anchor"),
            ("Krunal Pandya", "#2", "74.73", "#8", "+0.0016", "130", "[3.0 - 29.0]", "47.2%", "Indian Finger Spin & Dart Executioner"),
            ("Maheesh Theekshana", "#7", "64.60", "#9", "+0.0011", "161", "[3.0 - 27.0]", "42.4%", "Powerplay Mystery & Carrom Ball Bowler"),
            ("Varun Chakravarthy", "#8", "62.46", "#12", "-0.0043", "199", "[2.0 - 42.0]", "32.0%", "Overspin & Bounce Specialist for 70m SMS"),
            ("Jason Holder", "#9", "62.21", "#13", "-0.0052", "227", "[4.0 - 40.0]", "27.8%", "Tall Release Cutters & Heavy Back-of-Length"),
            ("Ravichandran Ashwin", "#10", "61.61", "#25", "-0.0109", "128", "[13.0 - 37.0]", "2.5%", "Tactical Master & Jaipur Geometry Specialist"),
            ("Yuzvendra Chahal", "#6", "65.03", "#34", "-0.0161", "247", "[11.0 - 46.0]", "3.9%", "High-Strike-Rate Partnership Breaker")
        ]
        
        y_start = Inches(2.0)
        row_h = Inches(0.42)
        col_widths = [Inches(2.2), Inches(0.9), Inches(0.9), Inches(0.9), Inches(1.2), Inches(1.0), Inches(1.3), Inches(1.1), Inches(2.23)]
        
        for r_idx, row in enumerate(rows):
            is_hdr = (r_idx == 0)
            bg = ROYAL_BLUE if is_hdr else (CANARY_YELLOW if r_idx in [1, 2, 3, 4] else (CREAM_CANVAS if r_idx % 2 == 1 else PURE_WHITE))
            txt_col = CANARY_YELLOW if is_hdr else (SHARP_BLACK if r_idx in [1, 2, 3, 4] else ROYAL_BLUE)
            
            x_cur = Inches(0.95)
            for c_idx, val in enumerate(row):
                w = col_widths[c_idx]
                cell = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x_cur, y_start + r_idx * row_h, w, row_h)
                cell.fill.solid()
                cell.fill.fore_color.rgb = bg
                cell.line.color.rgb = SHARP_BLACK
                cell.line.width = Pt(1.5) if not is_hdr else Pt(2.0)
                
                tf = cell.text_frame
                tf.word_wrap = False
                tf.vertical_anchor = MSO_ANCHOR.MIDDLE
                p = tf.paragraphs[0]
                p.text = val
                p.alignment = PP_ALIGN.LEFT if c_idx in [0, 8] else PP_ALIGN.CENTER
                p.font.name = FONT_TITLE if (is_hdr or c_idx == 0) else FONT_BODY
                p.font.size = Pt(9.5) if not is_hdr else Pt(10)
                p.font.bold = True if (is_hdr or c_idx in [0, 7]) else False
                p.font.color.rgb = PURE_WHITE if is_hdr else (RR_PINK if c_idx == 7 and float(val.replace('%',''))>70 else txt_col)
                
                x_cur += w

    # ==========================================
    # SLIDE 13: BOWLERS 1 & 2: NARINE & PATHIRANA
    # ==========================================
    def _build_slide_13_bowlers_narine_pathirana(self):
        slide = self.prs.slides.add_slide(self.blank_layout)
        self.add_slide_header(slide, "BOWLERS #1 & #2: THE UNPICKABLE CHESSMASTERS")
        
        # Left: Sunil Narine
        self.add_card(slide, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1), bg_color=PURE_WHITE)
        self.add_badge(slide, Inches(1.1), Inches(2.0), "RANK #1 (R1) / #3 (k*)", bg_color=CANARY_YELLOW)
        self.add_badge(slide, Inches(3.4), Inches(2.0), "SUNIL NARINE", bg_color=RR_PINK, text_color=PURE_WHITE)
        
        tb = slide.shapes.add_textbox(Inches(1.1), Inches(2.6), Inches(5.0), Inches(4.1))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.paragraphs[0].text = "EMPIRICAL DATA PROFILE:"
        tf.paragraphs[0].font.name = FONT_TITLE
        tf.paragraphs[0].font.size = Pt(12)
        
        p1 = tf.add_paragraph()
        p1.text = "• Legal Balls: 130 balls | Pressure Economy: 6.09 (Normal: 6.94)\n• Economy Delta: -0.84 (Concedes LESS under pressure than normal!)\n• Runs Prevented / Ball: +0.343 | Positive Match Rate: 88.9%\n• Bootstrap Stability: P(Top 10) = 75.1% | Mean Rank: 7.78 | CI: [1 - 19]"
        p1.font.name = FONT_BODY
        p1.font.size = Pt(11)
        p1.font.color.rgb = ROYAL_BLUE
        p1.space_after = Pt(10)
        
        p2 = tf.add_paragraph()
        p2.text = "HOW HE STRENGTHENS RAJASTHAN ROYALS IN 2027:"
        p2.font.name = FONT_TITLE
        p2.font.size = Pt(12)
        p2.font.color.rgb = RR_PINK
        
        p3 = tf.add_paragraph()
        p3.text = "1. JAIPUR SURFACE CHOKE: Jaipur's red/black clay mixture grips sharply. Narine's 6.09 economy strangles opposition death chases.\n2. POWERPLAY PINCH HITTER: Solves RR's opening balance, pairing with Jaiswal to blast 60 runs in powerplays without burning middle-order wickets."
        p3.font.name = FONT_BODY
        p3.font.size = Pt(11)
        p3.font.color.rgb = SHARP_BLACK

        # Right: Matheesha Pathirana
        self.add_card(slide, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.1), bg_color=PURE_WHITE)
        self.add_badge(slide, Inches(7.2), Inches(2.0), "RANK #1 (k*) / #4 (R1)", bg_color=NEON_MINT)
        self.add_badge(slide, Inches(9.5), Inches(2.0), "MATHEESHA PATHIRANA", bg_color=ROYAL_BLUE, text_color=CANARY_YELLOW)
        
        tb2 = slide.shapes.add_textbox(Inches(7.2), Inches(2.6), Inches(5.0), Inches(4.1))
        tf2 = tb2.text_frame
        tf2.word_wrap = True
        tf2.paragraphs[0].text = "EMPIRICAL DATA PROFILE:"
        tf2.paragraphs[0].font.name = FONT_TITLE
        tf2.paragraphs[0].font.size = Pt(12)
        
        p_r1 = tf2.add_paragraph()
        p_r1.text = "• Legal Balls: 206 balls | 21 Wickets under pressure!\n• Runs Prevented / Ball: +0.350 (Highest in Bowling Dataset)\n• Optimal Shrunk RP: +0.0171 (Rank #1 in World under k*)\n• Bootstrap Stability: P(Top 10) = 93.1% | 90% Rank CI: [1.0 - 12.0]"
        p_r1.font.name = FONT_BODY
        p_r1.font.size = Pt(11)
        p_r1.font.color.rgb = ROYAL_BLUE
        p_r1.space_after = Pt(10)
        
        p_r2 = tf2.add_paragraph()
        p_r2.text = "HOW HE STRENGTHENS RAJASTHAN ROYALS IN 2027:"
        p_r2.font.name = FONT_TITLE
        p_r2.font.size = Pt(12)
        p_r2.font.color.rgb = RR_PINK
        
        p_r3 = tf2.add_paragraph()
        p_r3.text = "1. RR'S MARQUEE AUCTION PRIORITY: In past playoff exits, RR couldn't defend 40 off 18 balls. Pathirana's slingy 148kph toe-crushers make him the undisputed heir to Lasith Malinga.\n2. BULLETPROOF SAMPLE SIZE: 206 pressure deliveries provide immense statistical certainty. He is RR's #1 must-acquire asset."
        p_r3.font.name = FONT_BODY
        p_r3.font.size = Pt(11)
        p_r3.font.color.rgb = SHARP_BLACK

    # ==========================================
    # SLIDE 14: BOWLERS 3 & 4: MUSTAFIZUR & RASHID
    # ==========================================
    def _build_slide_14_bowlers_mustafizur_rashid(self):
        slide = self.prs.slides.add_slide(self.blank_layout)
        self.add_slide_header(slide, "BOWLERS #3 & #4: DEATH CUTTERS & MIDDLE STRANGLERS")
        
        # Left: Mustafizur Rahman
        self.add_card(slide, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1), bg_color=PURE_WHITE)
        self.add_badge(slide, Inches(1.1), Inches(2.0), "RANK #2 (k*) / #5 (R1)", bg_color=CANARY_YELLOW)
        self.add_badge(slide, Inches(3.4), Inches(2.0), "MUSTAFIZUR RAHMAN", bg_color=SHARP_BLACK, text_color=PURE_WHITE)
        
        tb = slide.shapes.add_textbox(Inches(1.1), Inches(2.6), Inches(5.0), Inches(4.1))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.paragraphs[0].text = "EMPIRICAL DATA PROFILE:"
        tf.paragraphs[0].font.name = FONT_TITLE
        tf.paragraphs[0].font.size = Pt(12)
        
        p1 = tf.add_paragraph()
        p1.text = "• Legal Balls: 222 balls (2nd most) | 23 Wickets under pressure!\n• Runs Prevented / Ball: +0.232 | Shrunk RP: +0.0113 (Rank #2 under k*)\n• Positive Match Rate: 73.7% | Bootstrap P(Top 10): 88.2%\n• 90% Rank CI: [1.0 - 25.0] (Mean Rank: 7.60)"
        p1.font.name = FONT_BODY
        p1.font.size = Pt(11)
        p1.font.color.rgb = ROYAL_BLUE
        p1.space_after = Pt(10)
        
        p2 = tf.add_paragraph()
        p2.text = "HOW HE STRENGTHENS RAJASTHAN ROYALS IN 2027:"
        p2.font.name = FONT_TITLE
        p2.font.size = Pt(12)
        p2.font.color.rgb = RR_PINK
        
        p3 = tf.add_paragraph()
        p3.text = "1. CUTTER SPECIALIST ON JAIPUR CLAY: Sawai Mansingh Stadium's surface is famous for holding up into the pitch. The Fizz's off-cutter grips and dies, forcing miscues toward deep mid-wicket.\n2. FORMER RR EXPERTISE: Already familiar with RR's tactical setup and venue layout; delivers elite value at a reasonable purse outlay."
        p3.font.name = FONT_BODY
        p3.font.size = Pt(11)
        p3.font.color.rgb = SHARP_BLACK

        # Right: Rashid Khan (Bowler)
        self.add_card(slide, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.1), bg_color=PURE_WHITE)
        self.add_badge(slide, Inches(7.2), Inches(2.0), "RANK #3 (R1) / #7 (k*)", bg_color=ELECTRIC_CYAN)
        self.add_badge(slide, Inches(9.5), Inches(2.0), "RASHID KHAN (BOWL)", bg_color=RR_PINK, text_color=PURE_WHITE)
        
        tb2 = slide.shapes.add_textbox(Inches(7.2), Inches(2.6), Inches(5.0), Inches(4.1))
        tf2 = tb2.text_frame
        tf2.word_wrap = True
        tf2.paragraphs[0].text = "EMPIRICAL DATA PROFILE:"
        tf2.paragraphs[0].font.name = FONT_TITLE
        tf2.paragraphs[0].font.size = Pt(12)
        
        p_r1 = tf2.add_paragraph()
        p_r1.text = "• Legal Balls: 183 balls | 19 Wickets | Pressure Economy: 7.67\n• Runs Prevented / Ball: +0.181 | Positive Match Rate: 85.2%\n• Shrunk RP: +0.0041 (Rank #7 under k*) | P(Top 10) = 58.8%\n• Rapid Arm Speed: 96-102 kph leg-break and unpickable googly"
        p_r1.font.name = FONT_BODY
        p_r1.font.size = Pt(11)
        p_r1.font.color.rgb = ROYAL_BLUE
        p_r1.space_after = Pt(10)
        
        p_r2 = tf2.add_paragraph()
        p_r2.text = "HOW HE STRENGTHENS RAJASTHAN ROYALS IN 2027:"
        p_r2.font.name = FONT_TITLE
        p_r2.font.size = Pt(12)
        p_r2.font.color.rgb = RR_PINK
        
        p_r3 = tf2.add_paragraph()
        p_r3.text = "1. PHASE AGNOSTIC ATTACK: Can bowl over 8, over 12, and over 17/19. Batters cannot line him up at Jaipur because mistimed drives get caught in the 70m deep ring.\n2. ALL-ROUND VALUE: Combined with his #8 batting ranking, Rashid provides two world-class players in one overseas roster spot."
        p_r3.font.name = FONT_BODY
        p_r3.font.size = Pt(11)
        p_r3.font.color.rgb = SHARP_BLACK

    # ==========================================
    # SLIDE 15: BOWLERS 5 & 6: KRUNAL & THEEKSHANA
    # ==========================================
    def _build_slide_15_bowlers_krunal_theekshana(self):
        slide = self.prs.slides.add_slide(self.blank_layout)
        self.add_slide_header(slide, "BOWLERS #5 & #6: PHASE CONSTRICTORS & MYSTERY OPERATORS")
        
        # Left: Krunal Pandya
        self.add_card(slide, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1), bg_color=PURE_WHITE)
        self.add_badge(slide, Inches(1.1), Inches(2.0), "RANK #2 (R1) / #8 (k*)", bg_color=CANARY_YELLOW)
        self.add_badge(slide, Inches(3.4), Inches(2.0), "KRUNAL PANDYA", bg_color=ROYAL_BLUE, text_color=CANARY_YELLOW)
        
        tb = slide.shapes.add_textbox(Inches(1.1), Inches(2.6), Inches(5.0), Inches(4.1))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.paragraphs[0].text = "EMPIRICAL DATA PROFILE:"
        tf.paragraphs[0].font.name = FONT_TITLE
        tf.paragraphs[0].font.size = Pt(12)
        
        p1 = tf.add_paragraph()
        p1.text = "• Legal Balls: 130 balls | Pressure Economy: 6.42 (Normal: 7.98)\n• Economy Delta: -1.56 (Largest Pressure Improvement in Dataset!)\n• Runs Prevented / Ball: +0.227 | Positive Match Rate: 86.7%\n• P(Top 10) = 47.2% | Shrunk RP: +0.0016 (Rank #8 under k*)"
        p1.font.name = FONT_BODY
        p1.font.size = Pt(11)
        p1.font.color.rgb = ROYAL_BLUE
        p1.space_after = Pt(10)
        
        p2 = tf.add_paragraph()
        p2.text = "HOW HE STRENGTHENS RAJASTHAN ROYALS IN 2027:"
        p2.font.name = FONT_TITLE
        p2.font.size = Pt(12)
        p2.font.color.rgb = RR_PINK
        
        p3 = tf.add_paragraph()
        p3.text = "1. INDIAN SPINNER/ALL-ROUNDER BALANCE: Frees up an overseas slot. Bowls flat, fast darts into the pitch at Jaipur, denying batters elevation.\n2. POWERPLAY & MIDDLE CHOKE: Bowls overs 4-10, drying up runs and forcing risky shots against RR's wicket-taking strike bowlers."
        p3.font.name = FONT_BODY
        p3.font.size = Pt(11)
        p3.font.color.rgb = SHARP_BLACK

        # Right: Maheesh Theekshana
        self.add_card(slide, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.1), bg_color=PURE_WHITE)
        self.add_badge(slide, Inches(7.2), Inches(2.0), "RANK #7 (R1) / #9 (k*)", bg_color=NEON_MINT)
        self.add_badge(slide, Inches(9.5), Inches(2.0), "MAHEESH THEEKSHANA", bg_color=SHARP_BLACK, text_color=PURE_WHITE)
        
        tb2 = slide.shapes.add_textbox(Inches(7.2), Inches(2.6), Inches(5.0), Inches(4.1))
        tf2 = tb2.text_frame
        tf2.word_wrap = True
        tf2.paragraphs[0].text = "EMPIRICAL DATA PROFILE:"
        tf2.paragraphs[0].font.name = FONT_TITLE
        tf2.paragraphs[0].font.size = Pt(12)
        
        p_r1 = tf2.add_paragraph()
        p_r1.text = "• Legal Balls: 161 balls | Pressure Economy: 7.49 (Normal: 7.79)\n• Economy Delta: -0.30 | Runs Prevented / Ball: +0.177\n• Positive Match Rate: 72.0% | 11 Wickets under pressure\n• Carrom Ball Execution: High release point generating skidding bounce"
        p_r1.font.name = FONT_BODY
        p_r1.font.size = Pt(11)
        p_r1.font.color.rgb = ROYAL_BLUE
        p_r1.space_after = Pt(10)
        
        p_r2 = tf2.add_paragraph()
        p_r2.text = "HOW HE STRENGTHENS RAJASTHAN ROYALS IN 2027:"
        p_r2.font.name = FONT_TITLE
        p_r2.font.size = Pt(12)
        p_r2.font.color.rgb = RR_PINK
        
        p_r3 = tf2.add_paragraph()
        p_r3.text = "1. POWERPLAY CONTROL: Capable of bowling 2 overs in the powerplay and 1 in the death. His carrom ball moves away from right-handers without visual tell.\n2. TACTICAL OVERSEAS ROTATION: Gives RR flexibility to rotate mystery spin depending on away venue pitch conditions."
        p_r3.font.name = FONT_BODY
        p_r3.font.size = Pt(11)
        p_r3.font.color.rgb = SHARP_BLACK

    # ==========================================
    # SLIDE 16: BOWLERS 7 & 8: VARUN & HOLDER
    # ==========================================
    def _build_slide_16_bowlers_varun_holder(self):
        slide = self.prs.slides.add_slide(self.blank_layout)
        self.add_slide_header(slide, "BOWLERS #7 & #8: OVERSPIN TRAPS & STEEP BOUNCE CUTTERS")
        
        # Left: Varun Chakravarthy
        self.add_card(slide, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1), bg_color=PURE_WHITE)
        self.add_badge(slide, Inches(1.1), Inches(2.0), "RANK #8 (R1) / #12 (k*)", bg_color=CANARY_YELLOW)
        self.add_badge(slide, Inches(3.4), Inches(2.0), "VARUN CHAKRAVARTHY", bg_color=RR_PINK, text_color=PURE_WHITE)
        
        tb = slide.shapes.add_textbox(Inches(1.1), Inches(2.6), Inches(5.0), Inches(4.1))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.paragraphs[0].text = "EMPIRICAL DATA PROFILE:"
        tf.paragraphs[0].font.name = FONT_TITLE
        tf.paragraphs[0].font.size = Pt(12)
        
        p1 = tf.add_paragraph()
        p1.text = "• Legal Balls: 199 balls | 16 Wickets | Pressure Economy: 7.84\n• Runs Prevented / Ball: +0.088 | Positive Match Rate: 72.0%\n• Shrunk RP: -0.0043 (Rank #12 under k*) | P(Top 10) = 32.0%\n• High Overspin: Generates steep bounce and sharp off-break variation"
        p1.font.name = FONT_BODY
        p1.font.size = Pt(11)
        p1.font.color.rgb = ROYAL_BLUE
        p1.space_after = Pt(10)
        
        p2 = tf.add_paragraph()
        p2.text = "HOW HE STRENGTHENS RAJASTHAN ROYALS IN 2027:"
        p2.font.name = FONT_TITLE
        p2.font.size = Pt(12)
        p2.font.color.rgb = RR_PINK
        
        p3 = tf.add_paragraph()
        p3.text = "1. JAIPUR BOUNDARY CATCHES: Varun's overspin produces mistimed vertical top-edges. On Jaipur's 70m square boundary, these drop comfortably into the hands of long-on or deep mid-wicket.\n2. INDIAN MYSTERY WEAPON: Provides world-class mystery spin without occupying an overseas slot."
        p3.font.name = FONT_BODY
        p3.font.size = Pt(11)
        p3.font.color.rgb = SHARP_BLACK

        # Right: Jason Holder
        self.add_card(slide, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.1), bg_color=PURE_WHITE)
        self.add_badge(slide, Inches(7.2), Inches(2.0), "RANK #9 (R1) / #13 (k*)", bg_color=ELECTRIC_CYAN)
        self.add_badge(slide, Inches(9.5), Inches(2.0), "JASON HOLDER", bg_color=ROYAL_BLUE, text_color=CANARY_YELLOW)
        
        tb2 = slide.shapes.add_textbox(Inches(7.2), Inches(2.6), Inches(5.0), Inches(4.1))
        tf2 = tb2.text_frame
        tf2.word_wrap = True
        tf2.paragraphs[0].text = "EMPIRICAL DATA PROFILE:"
        tf2.paragraphs[0].font.name = FONT_TITLE
        tf2.paragraphs[0].font.size = Pt(12)
        
        p_r1 = tf2.add_paragraph()
        p_r1.text = "• Legal Balls: 227 balls (3rd most) | 22 Wickets under pressure!\n• Runs Prevented / Ball: +0.095 | Positive Match Rate: 81.6%\n• 6ft 7in Frame: High release point generating steep back-of-length bounce\n• Shrunk RP: -0.0052 (Rank #13 under k*) | P(Top 10) = 27.8%"
        p_r1.font.name = FONT_BODY
        p_r1.font.size = Pt(11)
        p_r1.font.color.rgb = ROYAL_BLUE
        p_r1.space_after = Pt(10)
        
        p_r2 = tf2.add_paragraph()
        p_r2.text = "HOW HE STRENGTHENS RAJASTHAN ROYALS IN 2027:"
        p_r2.font.name = FONT_TITLE
        p_r2.font.size = Pt(12)
        p_r2.font.color.rgb = RR_PINK
        
        p_r3 = tf2.add_paragraph()
        p_r3.text = "1. SMS BOUNCE PROFILE: Tall seamers have always troubled visiting batters at Sawai Mansingh Stadium. Holder's heavy ball hits the splice of the bat.\n2. PREVIOUS RR HERITAGE: Proven experience in RR pink; adds valuable lower-order power hitting at #8."
        p_r3.font.name = FONT_BODY
        p_r3.font.size = Pt(11)
        p_r3.font.color.rgb = SHARP_BLACK

    # ==========================================
    # SLIDE 17: BOWLERS 9 & 10: ASHWIN & CHAHAL
    # ==========================================
    def _build_slide_17_bowlers_ashwin_chahal(self):
        slide = self.prs.slides.add_slide(self.blank_layout)
        self.add_slide_header(slide, "BOWLERS #9 & #10: THE SAWAI MANSINGH SPIN LEGACY")
        
        # Left: Ravichandran Ashwin
        self.add_card(slide, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1), bg_color=PURE_WHITE)
        self.add_badge(slide, Inches(1.1), Inches(2.0), "RANK #10 (R1) / #25 (k*)", bg_color=CANARY_YELLOW)
        self.add_badge(slide, Inches(3.4), Inches(2.0), "R. ASHWIN", bg_color=SHARP_BLACK, text_color=CANARY_YELLOW)
        
        tb = slide.shapes.add_textbox(Inches(1.1), Inches(2.6), Inches(5.0), Inches(4.1))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.paragraphs[0].text = "EMPIRICAL DATA PROFILE:"
        tf.paragraphs[0].font.name = FONT_TITLE
        tf.paragraphs[0].font.size = Pt(12)
        
        p1 = tf.add_paragraph()
        p1.text = "• Legal Balls: 128 balls | Pressure Economy: 8.39 (Normal: 7.81)\n• Positive Match Rate: 68.8% | Runs Prevented: +0.040 / ball\n• Shrunk RP: -0.0109 (Rank #25 under k*) | P(Top 10) = 2.5%\n• Tactical Geometry: Uses wide bowling creases, changes pause and pace"
        p1.font.name = FONT_BODY
        p1.font.size = Pt(11)
        p1.font.color.rgb = ROYAL_BLUE
        p1.space_after = Pt(10)
        
        p2 = tf.add_paragraph()
        p2.text = "HOW HE STRENGTHENS RAJASTHAN ROYALS IN 2027:"
        p2.font.name = FONT_TITLE
        p2.font.size = Pt(12)
        p2.font.color.rgb = RR_PINK
        
        p3 = tf.add_paragraph()
        p3.text = "1. MASTER OF JAIPUR CONDITIONS: No active cricketer understands Sawai Mansingh Stadium pitch conditions and boundary angles better than Ashwin.\n2. TACTICAL BRAIN: Directs in-game field adjustments and match-up traps; controls left-handers through powerplay and middle overs."
        p3.font.name = FONT_BODY
        p3.font.size = Pt(11)
        p3.font.color.rgb = SHARP_BLACK

        # Right: Yuzvendra Chahal
        self.add_card(slide, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.1), bg_color=PURE_WHITE)
        self.add_badge(slide, Inches(7.2), Inches(2.0), "RANK #6 (R1) / #34 (k*)", bg_color=ELECTRIC_CYAN)
        self.add_badge(slide, Inches(9.5), Inches(2.0), "YUZVENDRA CHAHAL", bg_color=RR_PINK, text_color=PURE_WHITE)
        
        tb2 = slide.shapes.add_textbox(Inches(7.2), Inches(2.6), Inches(5.0), Inches(4.1))
        tf2 = tb2.text_frame
        tf2.word_wrap = True
        tf2.paragraphs[0].text = "EMPIRICAL DATA PROFILE:"
        tf2.paragraphs[0].font.name = FONT_TITLE
        tf2.paragraphs[0].font.size = Pt(12)
        
        p_r1 = tf2.add_paragraph()
        p_r1.text = "• Legal Balls: 247 balls (Most among Spinners) | 26 WICKETS!\n• Pressure Wickets: Highest in entire dataset across all bowlers!\n• Pressure Economy: 8.87 | Economy Delta: +0.28 (Concedes runs for wkts)\n• Fragility Note: Under k*=2000, runs-conceded penalty drops rank to #34"
        p_r1.font.name = FONT_BODY
        p_r1.font.size = Pt(11)
        p_r1.font.color.rgb = ROYAL_BLUE
        p_r1.space_after = Pt(10)
        
        p_r2 = tf2.add_paragraph()
        p_r2.text = "HOW HE STRENGTHENS RAJASTHAN ROYALS IN 2027:"
        p_r2.font.name = FONT_TITLE
        p_r2.font.size = Pt(12)
        p_r2.font.color.rgb = RR_PINK
        
        p_r3 = tf2.add_paragraph()
        p_r3.text = "1. FRANCHISE WICKET TALISMAN: When opposition batters are cruising, Chahal tosses the ball wide outside off-stump, inducing fatal mis-hits into the deep.\n2. STRIKE ATTACK: While his economy carries risk, his 26 pressure wickets break match-defining partnerships at crucial junctures."
        p_r3.font.name = FONT_BODY
        p_r3.font.size = Pt(11)
        p_r3.font.color.rgb = SHARP_BLACK

    # ==========================================
    # SLIDE 18: JAIPUR SMS STADIUM DYNAMICS
    # ==========================================
    def _build_slide_18_jaipur_venue_dynamics(self):
        slide = self.prs.slides.add_slide(self.blank_layout)
        self.add_slide_header(slide, "SAWAI MANSINGH STADIUM (JAIPUR): VENUE GEOMETRY & PITCH DYNAMICS")
        
        # 3 Cards Layout
        card_w = Inches(3.7)
        spacing = Inches(0.3)
        
        # Card 1: Boundary Geometry
        self.add_card(slide, Inches(0.8), Inches(1.8), card_w, Inches(5.1), bg_color=PURE_WHITE)
        self.add_badge(slide, Inches(1.1), Inches(2.0), "BOUNDARY GEOMETRY", bg_color=CANARY_YELLOW)
        tb1 = slide.shapes.add_textbox(Inches(1.0), Inches(2.6), Inches(3.3), Inches(4.0))
        tf1 = tb1.text_frame
        tf1.word_wrap = True
        tf1.paragraphs[0].text = "DIMENSIONS & OUTFIELD:"
        tf1.paragraphs[0].font.name = FONT_TITLE
        tf1.paragraphs[0].font.size = Pt(12)
        
        p1 = tf1.add_paragraph()
        p1.text = "• Square Boundaries: 68 - 72 meters\n• Straight Boundaries: 75 - 80 meters\n• Outfield: Exceptionally fast, large playing arena\n\nTACTICAL IMPLICATION:\nHitters cannot rely solely on mis-hits clearing the fence. Powerhitters must have genuine distance (Tim David, Heinrich Klaasen) or 360° placement (Suryakumar Yadav) to manipulate deep boundary fielders."
        p1.font.name = FONT_BODY
        p1.font.size = Pt(11)
        p1.font.color.rgb = ROYAL_BLUE

        # Card 2: Surface Characteristics
        self.add_card(slide, Inches(0.8) + card_w + spacing, Inches(1.8), card_w, Inches(5.1), bg_color=PURE_WHITE)
        self.add_badge(slide, Inches(1.1) + card_w + spacing, Inches(2.0), "SURFACE & CLAY", bg_color=ELECTRIC_CYAN)
        tb2 = slide.shapes.add_textbox(Inches(1.0) + card_w + spacing, Inches(2.6), Inches(3.3), Inches(4.0))
        tf2 = tb2.text_frame
        tf2.word_wrap = True
        tf2.paragraphs[0].text = "PITCH BEHAVIOR:"
        tf2.paragraphs[0].font.name = FONT_TITLE
        tf2.paragraphs[0].font.size = Pt(12)
        
        p2 = tf2.add_paragraph()
        p2.text = "• Soil Composition: Red/Black clay mixture with natural abrasive grip\n• Pace: True bounce early, holds up in afternoon & early evening\n• Spin Grip: Middle overs (7-15) offer substantial turn and sticky bounce\n\nTACTICAL IMPLICATION:\nFavors mystery spinners (Sunil Narine, Varun Chakravarthy) and off-cutters (Mustafizur Rahman) who dig the ball into the surface."
        p2.font.name = FONT_BODY
        p2.font.size = Pt(11)
        p2.font.color.rgb = ROYAL_BLUE

        # Card 3: Phase Tactics
        self.add_card(slide, Inches(0.8) + (card_w + spacing) * 2, Inches(1.8), card_w, Inches(5.1), bg_color=PURE_WHITE)
        self.add_badge(slide, Inches(1.1) + (card_w + spacing) * 2, Inches(2.0), "WINNING PHASES", bg_color=RR_PINK, text_color=PURE_WHITE)
        tb3 = slide.shapes.add_textbox(Inches(1.0) + (card_w + spacing) * 2, Inches(2.6), Inches(3.3), Inches(4.0))
        tf3 = tb3.text_frame
        tf3.word_wrap = True
        tf3.paragraphs[0].text = "PHASE EXECUTION:"
        tf3.paragraphs[0].font.name = FONT_TITLE
        tf3.paragraphs[0].font.size = Pt(12)
        
        p3 = tf3.add_paragraph()
        p3.text = "• Powerplay (1-6): Exploit fielding restrictions before the pitch slows\n• Middle Overs (7-15): Spin choke defense; spin demolisher on offense\n• Death Overs (16-20): 148kph slingy yorkers (Pathirana) to eliminate dew effect\n\nTACTICAL IMPLICATION:\nDefending 175 at Jaipur is routine if death overs concede under 32 runs. Pathirana + Narine guarantee this fortress."
        p3.font.name = FONT_BODY
        p3.font.size = Pt(11)
        p3.font.color.rgb = ROYAL_BLUE

    # ==========================================
    # SLIDE 19: RR AUCTION TARGET PRIORITY MATRIX
    # ==========================================
    def _build_slide_19_auction_target_matrix(self):
        slide = self.prs.slides.add_slide(self.blank_layout)
        self.add_slide_header(slide, "RAJASTHAN ROYALS AUCTION WAR ROOM: 3-TIER TARGET MATRIX")
        
        tiers = [
            ("TIER 1: MARQUEE MATCH-WINNERS", 
             "BUDGET ALLOCATION: 45% - 55% OF AUCTION PURSE",
             [("Matheesha Pathirana", "PACE DEATH", "Absolute #1 target. Solves RR's fatal death-bowling leak. Unhittable 148kph yorkers."),
              ("Heinrich Klaasen OR Tim David", "FINISHER", "Must secure one elite finisher. Klaasen demolishes Jaipur spin; David guarantees 20th over power.")],
             RR_PINK, PURE_WHITE),
            ("TIER 2: TACTICAL LINCHPINS", 
             "BUDGET ALLOCATION: 25% - 35% OF AUCTION PURSE",
             [("Sunil Narine OR Rashid Khan", "SPIN STRANGLER", "Transforms SMS Stadium into an unbreachable spin fortress. Both provide lethal batting at #8."),
              ("Shashank Singh OR Ashutosh Sharma", "IMPACT CLOSER", "High-efficiency Indian finishers. Shashank preserves wickets; Ashutosh accelerates instantly.")],
             CANARY_YELLOW, SHARP_BLACK),
            ("TIER 3: VALUE ROTATION ENABLERS", 
             "BUDGET ALLOCATION: 15% - 20% OF AUCTION PURSE",
             [("Mustafizur Rahman", "CUTTER SEED", "Budget-friendly overseas death bowler. Off-cutters thrive on Jaipur's gripping surface."),
              ("Krunal Pandya", "ALL-ROUND BALANCE", "Disciplined Indian finger-spinner. Bowls overs 4-10 and bats #7, saving overseas slot.")],
             NEON_MINT, SHARP_BLACK)
        ]
        
        for i, (t_title, b_budget, players, b_col, t_col) in enumerate(tiers):
            y = Inches(1.8) + i * Inches(1.7)
            self.add_card(slide, Inches(0.8), y, Inches(11.73), Inches(1.55), bg_color=PURE_WHITE)
            self.add_badge(slide, Inches(1.0), y + Inches(0.12), t_title, bg_color=b_col, text_color=t_col)
            
            tb_b = slide.shapes.add_textbox(Inches(5.0), y + Inches(0.12), Inches(7.3), Inches(0.35))
            tf_b = tb_b.text_frame
            p_b = tf_b.paragraphs[0]
            p_b.text = b_budget
            p_b.font.name = FONT_TITLE
            p_b.font.size = Pt(10)
            p_b.font.bold = True
            p_b.font.color.rgb = ROYAL_BLUE
            
            # 2 player sub-boxes
            for p_idx, (p_name, p_role, p_desc) in enumerate(players):
                x_p = Inches(1.0) + p_idx * Inches(5.8)
                tb_p = slide.shapes.add_textbox(x_p, y + Inches(0.55), Inches(5.6), Inches(0.9))
                tf_p = tb_p.text_frame
                tf_p.word_wrap = True
                
                p_p1 = tf_p.paragraphs[0]
                p_p1.text = f"★ {p_name.upper()} [{p_role}]: "
                p_p1.font.name = FONT_TITLE
                p_p1.font.size = Pt(11)
                p_p1.font.bold = True
                p_p1.font.color.rgb = SHARP_BLACK
                
                p_p2 = tf_p.add_paragraph()
                p_p2.text = p_desc
                p_p2.font.name = FONT_BODY
                p_p2.font.size = Pt(10)
                p_p2.font.color.rgb = ROYAL_BLUE

    # ==========================================
    # SLIDE 20: CONCLUSION & WINNING RR 2027 XI
    # ==========================================
    def _build_slide_20_conclusion_winning_xi(self):
        slide = self.prs.slides.add_slide(self.blank_layout)
        self.add_slide_header(slide, "THE CHAMPIONSHIP BLUEPRINT: RAJASTHAN ROYALS 2027 XI")
        
        # Left: Optimal Playing XI Card
        self.add_card(slide, Inches(0.8), Inches(1.8), Inches(6.0), Inches(5.1), bg_color=PURE_WHITE)
        self.add_badge(slide, Inches(1.1), Inches(2.0), "THE PRESSURE-OPTIMIZED LINEUP", bg_color=CANARY_YELLOW)
        
        lineup = [
            ("1. Yashasvi Jaiswal", "Anchor/Exploder (Retained)", ROYAL_BLUE),
            ("2. Sunil Narine (OS)", "Powerplay Pinch-Hitter & Mystery Spin", RR_PINK),
            ("3. Sanju Samson (C/WK)", "Captain & 360° Middle Leader (Retained)", ROYAL_BLUE),
            ("4. Suryakumar Yadav / S. Iyer", "Middle Spine & Spin Controller", SHARP_BLACK),
            ("5. Heinrich Klaasen / T. David (OS)", "Elite Spin Demolisher & Death Striker", RR_PINK),
            ("6. Riyan Parag", "Pace Accelerator & Utility Seam (Retained)", ROYAL_BLUE),
            ("7. Shashank Singh / Ashutosh", "Designated Impact Closer (High Wkt Preservation)", SHARP_BLACK),
            ("8. Rashid Khan / Krunal Pandya", "Lethal Lower-Order Striker & Phase Choke", RR_PINK),
            ("9. Sandeep Sharma", "Swing & Wide Yorker Execution (Retained)", ROYAL_BLUE),
            ("10. Matheesha Pathirana (OS)", "Marquee 148kph Death Yorker Bowler", RR_PINK),
            ("11. Avesh Khan / Kuldeep Sen", "High Pace Seam (Retained)", ROYAL_BLUE),
            ("IMPACT: Mustafizur Rahman (OS)", "Subbed in on Jaipur Gripping Clay", RR_PINK)
        ]
        
        tb = slide.shapes.add_textbox(Inches(1.0), Inches(2.5), Inches(5.6), Inches(4.2))
        tf = tb.text_frame
        tf.word_wrap = True
        
        for name, role, col in lineup:
            p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
            p.text = f"{name} "
            p.font.name = FONT_TITLE
            p.font.size = Pt(10)
            p.font.bold = True
            p.font.color.rgb = col
            
            p_sub = tf.add_paragraph()
            p_sub.text = f"   ↳ {role}"
            p_sub.font.name = FONT_BODY
            p_sub.font.size = Pt(9.5)
            p_sub.font.color.rgb = MUTED_GRAY
            p_sub.space_after = Pt(2)

        # Right: Strategic Summary
        self.add_card(slide, Inches(7.1), Inches(1.8), Inches(5.4), Inches(5.1), bg_color=ROYAL_BLUE, border_width=Pt(2.5))
        self.add_badge(slide, Inches(7.4), Inches(2.0), "THE SCIENTIFIC DIFFERENCE", bg_color=CANARY_YELLOW)
        
        tb_r = slide.shapes.add_textbox(Inches(7.4), Inches(2.6), Inches(4.8), Inches(4.0))
        tf_r = tb_r.text_frame
        tf_r.word_wrap = True
        
        def add_summary_point(tf, head, desc):
            p1 = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
            p1.text = "★ " + head.upper()
            p1.font.name = FONT_TITLE
            p1.font.size = Pt(12)
            p1.font.bold = True
            p1.font.color.rgb = CANARY_YELLOW
            
            p2 = tf.add_paragraph()
            p2.text = desc
            p2.font.name = FONT_BODY
            p2.font.size = Pt(11)
            p2.font.color.rgb = PURE_WHITE
            p2.space_after = Pt(12)

        add_summary_point(tf_r, "NO MORE PSEUDO-CLUTCH GAMBLES",
                          "By identifying that player clutch slope is noise (p = 0.6920), RR avoids overpaying for small-sample flukes. We target massive baseline talent and proven volume.")
        add_summary_point(tf_r, "DEATH RUN-LEAKAGE SEALED",
                          "Acquiring Matheesha Pathirana (RP +0.350, P=93.1%) and Sunil Narine (Econ 6.09) converts RR's death bowling from a liability into the most feared phase in the IPL.")
        add_summary_point(tf_r, "AN IMPENETRABLE JAIPUR FORTRESS",
                          "Tailoring squad acquisition specifically to Sawai Mansingh Stadium's 75m straight boundary and gripping surface guarantees home-match domination.")

if __name__ == '__main__':
    builder = NeobrutalismDeckBuilder()
    builder.build_deck()
