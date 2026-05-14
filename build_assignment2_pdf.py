from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import os

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE   = "/Users/alex/Downloads"
OUT    = os.path.join(BASE, "Assignment2_Solutions.pdf")
FIG_A  = os.path.join(BASE, "partA_rgnp_plot.png")
FIG_B1 = os.path.join(BASE, "partB1_simulation.png")
FIG_B2 = os.path.join(BASE, "partB2_bn_hp.png")

# ── Document ───────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUT, pagesize=A4,
    leftMargin=2.5*cm, rightMargin=2.5*cm,
    topMargin=2.5*cm, bottomMargin=2.5*cm
)
W = A4[0] - 5*cm   # usable width

# ── Styles ─────────────────────────────────────────────────────────────────────
base = getSampleStyleSheet()

def S(name, **kw):
    s = ParagraphStyle(name, parent=base['Normal'], **kw)
    return s

title_st   = S('MyTitle',   fontSize=18, leading=22, alignment=TA_CENTER,
                fontName='Helvetica-Bold', spaceAfter=6)
sub_st     = S('MySub',     fontSize=12, leading=16, alignment=TA_CENTER,
                fontName='Helvetica', spaceAfter=4, textColor=colors.HexColor('#444444'))
h1_st      = S('H1',        fontSize=13, leading=17, fontName='Helvetica-Bold',
                textColor=colors.HexColor('#1a3a6b'), spaceBefore=14, spaceAfter=4)
h2_st      = S('H2',        fontSize=11, leading=15, fontName='Helvetica-Bold',
                textColor=colors.HexColor('#2e5d9e'), spaceBefore=10, spaceAfter=3)
body_st    = S('Body',      fontSize=10, leading=14, alignment=TA_JUSTIFY, spaceAfter=6)
mono_st    = S('Mono',      fontSize=9,  leading=13, fontName='Courier',
                spaceAfter=4, leftIndent=12, textColor=colors.HexColor('#222222'))
caption_st = S('Caption',   fontSize=9,  leading=12, alignment=TA_CENTER,
                textColor=colors.HexColor('#555555'), spaceAfter=8, spaceBefore=2)
note_st    = S('Note',      fontSize=9,  leading=13, alignment=TA_JUSTIFY,
                textColor=colors.HexColor('#333333'), leftIndent=12, spaceAfter=6)
result_st  = S('Result',    fontSize=10, leading=14, fontName='Helvetica-Bold',
                textColor=colors.HexColor('#1a6b1a'), spaceAfter=6)

def tbl_style(header_color='#1a3a6b'):
    return TableStyle([
        ('BACKGROUND',  (0,0), (-1,0),  colors.HexColor(header_color)),
        ('TEXTCOLOR',   (0,0), (-1,0),  colors.white),
        ('FONTNAME',    (0,0), (-1,0),  'Helvetica-Bold'),
        ('FONTSIZE',    (0,0), (-1,0),  9),
        ('FONTNAME',    (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE',    (0,1), (-1,-1), 9),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f0f4fa')]),
        ('GRID',        (0,0), (-1,-1), 0.4, colors.HexColor('#aaaaaa')),
        ('ALIGN',       (1,0), (-1,-1), 'CENTER'),
        ('ALIGN',       (0,0), (0,-1),  'LEFT'),
        ('VALIGN',      (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING',  (0,0), (-1,-1), 4),
        ('BOTTOMPADDING',(0,0),(-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING',(0,0), (-1,-1), 6),
    ])

def hr(): return HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#cccccc'), spaceAfter=6, spaceBefore=2)
def sp(h=6): return Spacer(1, h)
def P(text, style=None): return Paragraph(text, style or body_st)
def fig(path, width, caption):
    return [Image(path, width=width, height=width*0.62), P(caption, caption_st)]

# ══════════════════════════════════════════════════════════════════════════════
story = []

# ── Title ──────────────────────────────────────────────────────────────────────
story += [
    sp(10),
    P('Time Series Econometrics for Finance', title_st),
    P('Assignment 2 — Solutions', sub_st),
    sp(4),
    hr(),
    sp(16),
]

# ══════════════════════════════════════════════════════════════════════════════
# PART A
# ══════════════════════════════════════════════════════════════════════════════
story += [
    P('A.  Empirical Exercise: Unit-Root Test on Log Real GNP', h1_st),
    hr(),
]

# A.1 Series choice
story += [
    P('1)  Series Selection and Plot', h2_st),
    P('The series chosen is <b>Real GNP (RGNP)</b> from the Nelson-Plosser dataset. '
      'After removing the leading zero observations (1860–1908), the usable annual sample '
      'runs from <b>1909 to 1970</b> (T = 62 observations). The log transformation '
      'y<sub>t</sub> = ln(RGNP<sub>t</sub>) is applied as instructed.', body_st),
    P('The upper panel of Figure 1 shows a clear and persistent <i>upward trend</i> with no '
      'obvious tendency to revert to a fixed mean — a first visual indication that the series '
      'may be non-stationary. The lower panel shows the first difference '
      '(approximately annual growth rates), which fluctuates around zero with no apparent '
      'trend, consistent with a stationary process after differencing.', body_st),
    sp(4),
]
story += fig(FIG_A, W,
    'Figure 1.  Log Real GNP (top) and its first difference (bottom), 1909–1970.')

# A.2 Data prep
story += [
    P('2)  Data Preparation', h2_st),
    P('Observations with zero values (years 1860–1908) are dropped, leaving a clean '
      'balanced sample. The series is then log-transformed: y<sub>t</sub> = ln(RGNP<sub>t</sub>). '
      'RGNP is not the Bond Yield series, so the log transformation applies.', body_st),
]

# A.3 Testing format
story += [
    P('3)  Unit-Root Testing Format', h2_st),
    P('We follow the <b>top-down approach</b> described in the Lecture Notes (pp. 138–141), '
      'incorporating prior information from the visual inspection of the series:', body_st),
    P('<b>Step 1.</b>  Since the log level clearly trends upward, we begin with the most '
      'general ADF specification — <b>Model 3</b> with a constant and a deterministic '
      'time trend:', body_st),
    P('&nbsp;&nbsp;&nbsp;&nbsp;'
      '&#916;y<sub>t</sub> = a<sub>0</sub> + a<sub>2</sub>t + '
      '&#947;y<sub>t&#8722;1</sub> + b<sub>1</sub>&#916;y<sub>t&#8722;1</sub> + '
      '&#949;<sub>t</sub>', mono_st),
    P('<b>Step 2.</b>  The lag order is selected by BIC over lags 0–4 applied to '
      'the unrestricted model. BIC selects <b>p = 1</b> lagged difference.', body_st),
    P('<b>Step 3.</b>  The key test is the <b>joint F-test (&#981;<sub>3</sub>)</b>, '
      'which tests H<sub>0</sub>: &#947; = 0 <i>and</i> a<sub>2</sub> = 0 simultaneously '
      '(unit root with no deterministic trend). The restricted model under H<sub>0</sub> is:', body_st),
    P('&nbsp;&nbsp;&nbsp;&nbsp;'
      '&#916;y<sub>t</sub> = a<sub>0</sub> + b<sub>1</sub>&#916;y<sub>t&#8722;1</sub> + '
      '&#949;<sub>t</sub>&nbsp;&nbsp;&nbsp;(random walk with drift)', mono_st),
    P('The F-statistic is compared to the Dickey-Fuller &#981;<sub>3</sub> critical values '
      '(5%: 6.49, 10%: 5.47) from Fuller (1976). Standard t-table critical values are <i>not</i> '
      'applicable — the null distribution is non-standard under a unit root.', body_st),
    P('The individual ADF t-statistic on &#947; is also reported for completeness and compared '
      'to the DF critical values for the model with constant and trend '
      '(5%: &#8722;3.49, 1%: &#8722;4.12).', body_st),
]

# A.4 Results
story += [
    P('4)  Results and Interpretation', h2_st),
]

adf_data = [
    ['Test', 'Statistic', 'CV 1%', 'CV 5%', 'CV 10%', 'Decision'],
    ['ADF t-stat (ct, p=1)',     '-2.9939', '-4.118', '-3.486', '-3.171', 'Fail to reject H₀'],
    ['ϕ3 F-stat (ct, p=1)', '4.619',   '—',      '6.49',   '5.47',   'Fail to reject H₀'],
    ['ADF t-stat (Δy, n, p=0)', '-4.692', '-2.604', '-1.946', '-1.613', 'Reject H₀'],
]
t = Table(adf_data, colWidths=[W*0.30, W*0.12, W*0.10, W*0.10, W*0.10, W*0.28])
t.setStyle(tbl_style())
story += [t, P('Table 1.  ADF test results for log(RGNP), 1909–1970.', caption_st)]

story += [
    P('<b>Interpretation:</b>', h2_st),
    P('Both the ADF t-statistic (&#8722;2.994) and the &#981;<sub>3</sub> F-statistic (4.619) '
      'fall well above their respective 5% critical values of &#8722;3.49 and 6.49. '
      'We therefore <b>fail to reject the null hypothesis of a unit root</b> at any '
      'conventional significance level. Moreover, the &#981;<sub>3</sub> test jointly '
      'rejects neither the unit root nor the deterministic trend, confirming that no '
      'significant trend is present beyond the stochastic one.', body_st),
    P('In contrast, the ADF test applied to the <b>first difference</b> &#916;y<sub>t</sub> '
      'yields a statistic of &#8722;4.692, which comfortably exceeds the 1% critical value '
      'of &#8722;2.604. The first difference is strongly stationary.', body_st),
    P('<b>Conclusion:</b> log(RGNP) is an <b>I(1)</b> process — a difference-stationary '
      'series driven by a stochastic trend (random walk with drift). This replicates the '
      'original finding of Nelson and Plosser (1982), who showed that most US macro series '
      'cannot be distinguished from unit-root processes, implying that permanent shocks '
      'have lasting effects on the level of real output.', result_st),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# PART B.1
# ══════════════════════════════════════════════════════════════════════════════
story += [
    P('B.1  Computer Exercise: Random Walk Monte Carlo Simulation', h1_st),
    hr(),
    P('<b>Setup.</b>  We simulate N = 100,000 independent sequences of the pure random walk', body_st),
    P('&nbsp;&nbsp;&nbsp;&nbsp;x<sub>t</sub> = x<sub>t&#8722;1</sub> + u<sub>t</sub>,&nbsp;&nbsp;'
      'u<sub>t</sub> ~ N(0,1),&nbsp;&nbsp;x<sub>0</sub> = 0,&nbsp;&nbsp;T = 81', mono_st),
    P('For each simulated series, three OLS models are estimated:', body_st),
]

models_data = [
    ['Model', 'Specification', 'Deterministics'],
    ['1', 'xₜ = ρ xₜ₋₁ + uₜ',                'None'],
    ['2', 'xₜ = c + ρ xₜ₋₁ + uₜ',            'Constant'],
    ['3', 'xₜ = c + δt + ρ xₜ₋₁ + uₜ', 'Constant + Trend'],
]
t = Table(models_data, colWidths=[W*0.08, W*0.52, W*0.28])
t.setStyle(tbl_style())
story += [t, sp(4)]

# (a) percentiles
story += [P('(a)  Percentiles of ρ̂ and t-statistics', h2_st)]

rho_data = [
    ['', 'Mean ρ̂', 'Std ρ̂', '14th pct', '86th pct'],
    ['Model 1 (no constant)', '0.9787', '0.0380', '0.9442', '1.0091'],
    ['Model 2 (constant)',    '0.9359', '0.0525', '0.8831', '0.9847'],
    ['Model 3 (const+trend)', '0.8794', '0.0681', '0.8076', '0.9465'],
]
t = Table(rho_data, colWidths=[W*0.30, W*0.15, W*0.15, W*0.20, W*0.20])
t.setStyle(tbl_style('#2e5d9e'))
story += [t, P('Table 2.  Distribution of OLS estimates of ρ under the unit-root DGP.', caption_st)]

tstat_data = [
    ['', 'Mean t-stat', 'Std t-stat', '14th pct', '86th pct'],
    ['Model 1 (no constant)', '-0.421', '0.990', '-1.442', '+0.672'],
    ['Model 2 (constant)',    '-1.550', '0.867', '-2.448', '-0.625'],
    ['Model 3 (const+trend)', '-2.219', '0.792', '-3.046', '-1.403'],
]
t = Table(tstat_data, colWidths=[W*0.30, W*0.15, W*0.15, W*0.20, W*0.20])
t.setStyle(tbl_style('#2e5d9e'))
story += [t, P('Table 3.  Distribution of t-statistics (ρ̂−1)/se(ρ̂) under H₀: ρ=1.', caption_st)]

# (b) histograms
story += [P('(b)  Distributions of ρ̂ and t-statistics', h2_st)]
story += fig(FIG_B1, W,
    'Figure 2.  Top row: distribution of ρ̂ for each model (red dashed = true ρ=1, '
    'dotted = 14th/86th percentiles). Bottom row: t-statistic distribution vs N(0,1) reference.')

# (c) comments
story += [
    P('(c)  Comments', h2_st),
    P('<b>Downward bias of ρ̂.</b>  Even though the true value is ρ = 1, the OLS estimator '
      'is systematically biased downward. The bias worsens as more deterministic components are '
      'included: Model 1 has a mean ρ̂ ≈ 0.979, while Model 3 has mean ρ̂ ≈ 0.879. '
      'This reflects the fact that including a constant or trend "absorbs" variation from '
      'x<sub>t&#8722;1</sub>, pulling the estimated coefficient toward zero.', body_st),
    P('<b>Non-standard t-distribution.</b>  The t-statistics are <i>not</i> normally distributed '
      'under the unit-root null. They are left-skewed and shifted well below zero — especially '
      'when deterministic terms are present. Model 3 has a mean t-stat of &#8722;2.22, far from '
      'the N(0,1) mean of zero. This is the Dickey-Fuller distribution.', body_st),
    P('<b>Critical implication for inference.</b>  If one incorrectly used standard t-table '
      'critical values (&#8722;1.645 at 5%) to test H<sub>0</sub>: ρ = 1, one would massively '
      'over-reject the unit-root null. The simulated 14th and 86th percentiles give the '
      'empirical DF critical values, confirming that the correct 5% left-tail cutoff is '
      'around &#8722;1.44 (Model 1), &#8722;2.45 (Model 2), and &#8722;3.05 (Model 3) — '
      'all more negative than the standard t critical values.', body_st),
    P('<b>Role of deterministics.</b>  Adding a constant or trend under the unit-root null '
      'shifts the entire distribution of both ρ̂ and the t-statistic further left. '
      'This is why Dickey-Fuller tables have three separate sets of critical values '
      'depending on the model specification chosen.', body_st),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# PART B.2
# ══════════════════════════════════════════════════════════════════════════════
story += [
    P('B.2  Computer Exercise: BN Decomposition and HP Filter (US Real GDP)', h1_st),
    hr(),
    P('<b>Data.</b>  US Real GDP (GDPC1), quarterly, 1947:Q1–2019:Q4 (T = 292 observations, '
      'truncating at 2019:Q4 to exclude COVID). The log series is '
      'y<sub>t</sub> = ln(GDP<sub>t</sub>).', body_st),
]

# (a) ARMA
story += [
    P('(a)  ARMA(1,0) Fit and Beveridge-Nelson Decomposition', h2_st),
    P('An ARMA(1,0) model with intercept is fitted to the first differences '
      '&#916;y<sub>t</sub> = y<sub>t</sub> &#8722; y<sub>t&#8722;1</sub> by maximum '
      'likelihood. Note that BIC also selects ARMA(1,0) from models up to ARMA(2,1), '
      'confirming the specification.', body_st),
    P('Estimated model: &nbsp;&nbsp;&#916;y<sub>t</sub> = 0.00775 + 0.3585&#916;y<sub>t&#8722;1</sub> + '
      '&#949;<sub>t</sub>,&nbsp;&nbsp;&#963;̂<super>2</super> = 7.47 × 10<super>&#8722;5</super>',
      mono_st),
]

arma_data = [
    ['Parameter', 'Estimate', 'Std. Error', 'z-stat', 'p-value', '95% CI'],
    ['c (intercept)', '0.00775', '0.00080', '9.67', '0.000', '[0.006, 0.009]'],
    ['ϕ (AR coef)',    '0.3585',  '0.047',   '7.66', '0.000', '[0.267, 0.450]'],
    ['σ²',        '7.47×10⁻⁵', '4.4×10⁻⁶', '16.97', '0.000', '[6.6, 8.3]×10⁻⁵'],
]
t = Table(arma_data, colWidths=[W*0.22, W*0.14, W*0.14, W*0.12, W*0.12, W*0.26])
t.setStyle(tbl_style())
story += [t, P('Table 4.  ARMA(1,0) estimation results for Δyₜ, 1947:Q1–2019:Q4.', caption_st)]

story += [
    P('The long-run mean of &#916;y<sub>t</sub> is '
      '&#956;̂ = ĉ/(1&#8722;ϕ̂) = 0.00775/(1&#8722;0.3585) = <b>0.01207</b> '
      'per quarter (~4.8% annualised), representing the steady-state quarterly growth rate of '
      'the US economy.', body_st),
    P('<b>Beveridge-Nelson decomposition.</b>  For an ARMA(1,0) model on &#916;y<sub>t</sub>, '
      'the BN transitory (cyclical) component has a closed-form expression. The BN permanent '
      'component is defined as the expected long-run level, discounting predictable future '
      'deviations from the long-run mean. Formally:', body_st),
    P('&nbsp;&nbsp;&nbsp;&nbsp;'
      'C<super>BN</super><sub>t</sub> = &#8722; ϕ̂/(1&#8722;ϕ̂) '
      '× (&#916;y<sub>t</sub> &#8722; μ̂)', mono_st),
    P('&nbsp;&nbsp;&nbsp;&nbsp;With ϕ̂ = 0.3585:&nbsp;&nbsp;&nbsp;'
      'C<super>BN</super><sub>t</sub> = &#8722;0.558 × (&#916;y<sub>t</sub> &#8722; 0.01207)',
      mono_st),
    P('The BN permanent component is then '
      'τ<super>BN</super><sub>t</sub> = y<sub>t</sub> &#8722; C<super>BN</super><sub>t</sub>. '
      'Intuitively, the cycle captures the degree to which current growth exceeds or falls short '
      'of the long-run average, scaled by the persistence of those deviations.', body_st),
]

# (b) HP
story += [
    P('(b)  Hodrick-Prescott Filter', h2_st),
    P('The HP filter decomposes y<sub>t</sub> into trend τ<super>HP</super><sub>t</sub> '
      'and cycle C<super>HP</super><sub>t</sub> = y<sub>t</sub> &#8722; τ<super>HP</super><sub>t</sub> '
      'by minimising:', body_st),
    P('&nbsp;&nbsp;&nbsp;&nbsp;'
      'Σ(y<sub>t</sub> &#8722; τ<sub>t</sub>)<super>2</super> + '
      'λ Σ(Δ<super>2</super>τ<sub>t</sub>)<super>2</super>', mono_st),
    P('with smoothing parameter <b>λ = 1,600</b> (standard for quarterly data). '
      'A higher λ penalises curvature in the trend more strongly, producing a '
      'smoother permanent component.', body_st),
]

# (c) Plot and comments
story += [P('(c)  Comparison of Transitory Components', h2_st)]
story += fig(FIG_B2, W,
    'Figure 3.  Top: log(GDP), BN trend and HP trend. '
    'Bottom: BN cycle (blue) vs HP cycle (red dashed), shaded areas = NBER recessions.')

cycle_data = [
    ['Statistic', 'BN Cycle', 'HP Cycle'],
    ['Std. Deviation',  '0.0052', '0.0158'],
    ['Minimum',         '-0.0148', '-0.0623'],
    ['Maximum',         '+0.0214', '+0.0372'],
    ['Correlation (BN vs HP)', '−0.257', '—'],
]
t = Table(cycle_data, colWidths=[W*0.44, W*0.28, W*0.28])
t.setStyle(tbl_style('#2e5d9e'))
story += [t, P('Table 5.  Summary statistics for cyclical components.', caption_st)]

story += [
    P('<b>Amplitude.</b>  The HP cycle has a standard deviation of 1.58% — about three times '
      'larger than the BN cycle (0.52%). The HP filter attributes large, persistent swings '
      'in GDP (e.g., the 2008–09 Great Recession, reaching &#8722;6.2%) to the cyclical '
      'component. The BN cycle is far smaller because it incorporates predictability: '
      'since &#916;y<sub>t</sub> has positive autocorrelation (ϕ = 0.36), '
      'above-average growth today implies above-average growth next quarter, so the '
      'permanent component rises by more than just the current increment, absorbing '
      'much of the swing.', body_st),
    P('<b>Negative correlation.</b>  The two cycles are negatively correlated (&#8722;0.26), '
      'meaning they frequently move in opposite directions. This is a well-documented '
      'phenomenon: the BN and HP decompositions embed fundamentally different views of '
      'what constitutes the "trend." The HP trend is a smooth curve penalising curvature, '
      'while the BN trend is a martingale that jumps every period.', body_st),
    P('<b>Recession behaviour.</b>  Both cycles turn negative during all NBER recessions '
      '(shaded grey), consistent with economic downturns reducing output below trend. '
      'The HP cycle more clearly identifies business cycle turning points and produces '
      'smoother cycles that align closely with the conventional business cycle narrative. '
      'The BN cycle is noisier and harder to interpret economically at quarterly frequency '
      'with only an AR(1), but it is theoretically grounded in the rational expectations '
      'permanent income framework.', body_st),
    P('<b>Conclusion:</b>  The two filters agree that the US economy experienced pronounced '
      'cyclical swings around recessions, but disagree strongly on their magnitude. The '
      'choice between them depends on whether one views the trend as a smooth deterministic '
      'path (HP) or as a stochastic process that incorporates all predictable future growth '
      '(BN). Neither decomposition is universally "correct" — they answer different '
      'economic questions.', result_st),
]

# ── Build ──────────────────────────────────────────────────────────────────────
doc.build(story)
print(f"Saved: {OUT}")
