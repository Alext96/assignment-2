from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, HRFlowable, PageBreak,
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
import os

BASE   = "/Users/alex/Downloads"
OUT    = os.path.join(BASE, "Assignment2_Solutions.pdf")
FIG_A  = os.path.join(BASE, "partA_rgnp_plot.png")
FIG_B1 = os.path.join(BASE, "partB1_simulation.png")
FIG_B2 = os.path.join(BASE, "partB2_bn_hp.png")

doc = SimpleDocTemplate(
    OUT, pagesize=A4,
    leftMargin=2.5*cm, rightMargin=2.5*cm,
    topMargin=2.5*cm,  bottomMargin=2.5*cm
)
W = A4[0] - 5*cm

base = getSampleStyleSheet()
def S(name, **kw):
    return ParagraphStyle(name, parent=base['Normal'], **kw)

title_st   = S('T',  fontSize=18, leading=22, alignment=TA_CENTER, fontName='Helvetica-Bold', spaceAfter=6)
sub_st     = S('Su', fontSize=12, leading=16, alignment=TA_CENTER, fontName='Helvetica', spaceAfter=4,
                textColor=colors.HexColor('#444444'))
h1_st      = S('H1', fontSize=13, leading=17, fontName='Helvetica-Bold',
                textColor=colors.HexColor('#1a3a6b'), spaceBefore=14, spaceAfter=4)
h2_st      = S('H2', fontSize=11, leading=15, fontName='Helvetica-Bold',
                textColor=colors.HexColor('#2e5d9e'), spaceBefore=10, spaceAfter=3)
body_st    = S('Bo', fontSize=10, leading=14, alignment=TA_JUSTIFY, spaceAfter=6)
mono_st    = S('Mo', fontSize=9,  leading=13, fontName='Courier', spaceAfter=4,
                leftIndent=12, textColor=colors.HexColor('#222222'))
caption_st = S('Ca', fontSize=9,  leading=12, alignment=TA_CENTER,
                textColor=colors.HexColor('#555555'), spaceAfter=8, spaceBefore=2)
result_st  = S('Re', fontSize=10, leading=14, fontName='Helvetica-Bold',
                textColor=colors.HexColor('#1a6b1a'), spaceAfter=6)
tc_st      = S('TC', fontSize=9,  leading=12)          # for table cells that need markup
tc_c_st    = S('TC2',fontSize=9,  leading=12, alignment=TA_CENTER)

def tbl_style(hc='#1a3a6b'):
    return TableStyle([
        ('BACKGROUND',   (0,0),(-1,0),  colors.HexColor(hc)),
        ('TEXTCOLOR',    (0,0),(-1,0),  colors.white),
        ('FONTNAME',     (0,0),(-1,0),  'Helvetica-Bold'),
        ('FONTSIZE',     (0,0),(-1,0),  9),
        ('FONTNAME',     (0,1),(-1,-1), 'Helvetica'),
        ('FONTSIZE',     (0,1),(-1,-1), 9),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, colors.HexColor('#f0f4fa')]),
        ('GRID',         (0,0),(-1,-1), 0.4, colors.HexColor('#aaaaaa')),
        ('ALIGN',        (1,0),(-1,-1), 'CENTER'),
        ('ALIGN',        (0,0),(0,-1),  'LEFT'),
        ('VALIGN',       (0,0),(-1,-1), 'MIDDLE'),
        ('TOPPADDING',   (0,0),(-1,-1), 4),
        ('BOTTOMPADDING',(0,0),(-1,-1), 4),
        ('LEFTPADDING',  (0,0),(-1,-1), 6),
        ('RIGHTPADDING', (0,0),(-1,-1), 6),
    ])

def hr():        return HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#cccccc'), spaceAfter=6, spaceBefore=2)
def sp(h=6):     return Spacer(1, h)
def P(t, s=None):return Paragraph(t, s or body_st)
# Table cell helpers — use these whenever a cell needs subscripts/superscripts
def TC(t):       return Paragraph(t, tc_st)
def TCC(t):      return Paragraph(t, tc_c_st)
def fig(path, w, cap): return [Image(path, width=w, height=w*0.62), P(cap, caption_st)]

# ── Story ──────────────────────────────────────────────────────────────────────
story = []

story += [
    sp(10),
    P('Time Series Econometrics for Finance', title_st),
    P('Assignment 2 — Solutions', sub_st),
    sp(4), hr(), sp(16),
]

# ══════════════════════════════════════════════════════════════════════════════
# PART A
# ══════════════════════════════════════════════════════════════════════════════
story += [P('A.  Empirical Exercise: Unit-Root Test on Log Real GNP', h1_st), hr()]

story += [
    P('1)  Series Selection and Plot', h2_st),
    P('The series chosen is <b>Real GNP (RGNP)</b> from the Nelson-Plosser dataset. '
      'After removing the leading zero observations (1860–1908), the usable annual sample '
      'runs from <b>1909 to 1970</b> (T = 62 observations). The log transformation '
      'y<sub>t</sub> = ln(RGNP<sub>t</sub>) is applied as instructed.', body_st),
    P('The upper panel of Figure 1 shows a clear and persistent <i>upward trend</i> with no '
      'obvious tendency to revert to a fixed mean — a first visual indication of non-stationarity. '
      'The lower panel shows the first difference (annual growth rates), which fluctuates '
      'around zero with no trend, consistent with stationarity after differencing.', body_st),
    sp(4),
]
story += fig(FIG_A, W, 'Figure 1.  Log Real GNP (top) and its first difference (bottom), 1909–1970.')

story += [
    P('2)  Data Preparation', h2_st),
    P('Observations with zero values (years 1860–1908) are dropped, leaving 62 annual '
      'observations. The series is log-transformed: y<sub>t</sub> = ln(RGNP<sub>t</sub>). '
      'RGNP is not the Bond Yield series, so the log transformation applies.', body_st),
    P('3)  Unit-Root Testing Format', h2_st),
    P('We follow the <b>top-down approach</b> from the Lecture Notes (pp. 138–141), '
      'incorporating prior information from the visual inspection of the series:', body_st),
    P('<b>Step 1.</b>  Since the log level clearly trends upward, we begin with the most '
      'general ADF specification — <b>Model 3</b> (constant + deterministic trend):', body_st),
    P('&nbsp;&nbsp;&nbsp;&nbsp;'
      '&#916;y<sub>t</sub> = a<sub>0</sub> + a<sub>2</sub>t + '
      '&#947;y<sub>t-1</sub> + b<sub>1</sub>&#916;y<sub>t-1</sub> + '
      '&#949;<sub>t</sub>', mono_st),
    P('<b>Step 2.</b>  Lag order selected by BIC over lags 0–4. BIC selects <b>p = 1</b>.', body_st),
    P('<b>Step 3.</b>  The key test is the <b>joint F-test (&#981;<sub>3</sub>)</b>, which tests '
      'H<sub>0</sub>: &#947; = 0 <i>and</i> a<sub>2</sub> = 0 simultaneously (unit root with no '
      'deterministic trend). The restricted model under H<sub>0</sub> is:', body_st),
    P('&nbsp;&nbsp;&nbsp;&nbsp;'
      '&#916;y<sub>t</sub> = a<sub>0</sub> + b<sub>1</sub>&#916;y<sub>t-1</sub> + '
      '&#949;<sub>t</sub>&nbsp;&nbsp;&nbsp;(random walk with drift)', mono_st),
    P('The F-statistic is compared to the Dickey-Fuller &#981;<sub>3</sub> critical values '
      '(5%: 6.49, 10%: 5.47). Standard t-table critical values do <i>not</i> apply under '
      'the unit-root null.', body_st),
    P('4)  Results and Interpretation', h2_st),
]

adf_data = [
    ['Test', 'Statistic', 'CV 1%', 'CV 5%', 'CV 10%', 'Decision'],
    [TC('ADF t-stat (ct, p=1)'),
     '-2.9939', '-4.118', '-3.486', '-3.171',
     TC('Fail to reject H<sub>0</sub>')],
    [TC('&#981;<sub>3</sub> F-stat (ct, p=1)'),
     '4.619', '—', '6.49', '5.47',
     TC('Fail to reject H<sub>0</sub>')],
    [TC('ADF t-stat (&#916;y, n, p=0)'),
     '-4.692', '-2.604', '-1.946', '-1.613',
     TC('Reject H<sub>0</sub>')],
]
t = Table(adf_data, colWidths=[W*0.30, W*0.12, W*0.10, W*0.10, W*0.10, W*0.28])
t.setStyle(tbl_style())
story += [t, P('Table 1.  ADF test results for log(RGNP), 1909–1970.', caption_st)]

story += [
    P('<b>Interpretation:</b>', h2_st),
    P('Both the ADF t-statistic (&#8722;2.994) and the &#981;<sub>3</sub> F-statistic (4.619) '
      'are above their 5% critical values of &#8722;3.49 and 6.49 respectively. '
      'We therefore <b>fail to reject the null hypothesis of a unit root</b> at any '
      'conventional significance level. The &#981;<sub>3</sub> test also confirms that '
      'no significant deterministic trend is present beyond the stochastic one.', body_st),
    P('In contrast, the ADF test on the <b>first difference</b> &#916;y<sub>t</sub> '
      'gives &#8722;4.692, well below the 1% critical value of &#8722;2.604. '
      'The first difference is strongly stationary.', body_st),
    P('<b>Conclusion:</b> log(RGNP) is an <b>I(1)</b> process — a difference-stationary '
      'series driven by a stochastic trend. This replicates Nelson and Plosser (1982): '
      'most US macro series are indistinguishable from unit-root processes, implying '
      'that shocks have permanent effects on output.', result_st),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# PART B.1
# ══════════════════════════════════════════════════════════════════════════════
story += [
    P('B.1  Computer Exercise: Random Walk Monte Carlo Simulation', h1_st), hr(),
    P('<b>Setup.</b>  We simulate N = 100,000 independent sequences of the pure random walk', body_st),
    P('&nbsp;&nbsp;&nbsp;&nbsp;x<sub>t</sub> = x<sub>t-1</sub> + u<sub>t</sub>,&nbsp;&nbsp;'
      'u<sub>t</sub> ~ N(0,1),&nbsp;&nbsp;x<sub>0</sub> = 0,&nbsp;&nbsp;T = 81', mono_st),
    P('For each simulated series, three OLS models are estimated:', body_st),
]

models_data = [
    ['Model', 'Specification', 'Deterministics'],
    ['1', TC('x<sub>t</sub> = &#961; x<sub>t-1</sub> + u<sub>t</sub>'),                    'None'],
    ['2', TC('x<sub>t</sub> = c + &#961; x<sub>t-1</sub> + u<sub>t</sub>'),                'Constant'],
    ['3', TC('x<sub>t</sub> = c + &#948;t + &#961; x<sub>t-1</sub> + u<sub>t</sub>'), 'Constant + Trend'],
]
t = Table(models_data, colWidths=[W*0.08, W*0.52, W*0.28])
t.setStyle(tbl_style())
story += [t, sp(4)]

story += [P('(a)  Percentiles of rho-hat and t-statistics', h2_st)]

rho_data = [
    ['', 'Mean rho-hat', 'Std rho-hat', '14th pct', '86th pct'],
    ['Model 1 (no constant)', '0.9787', '0.0380', '0.9442', '1.0091'],
    ['Model 2 (constant)',    '0.9359', '0.0525', '0.8831', '0.9847'],
    ['Model 3 (const+trend)', '0.8794', '0.0681', '0.8076', '0.9465'],
]
t = Table(rho_data, colWidths=[W*0.30, W*0.175, W*0.175, W*0.175, W*0.175])
t.setStyle(tbl_style('#2e5d9e'))
story += [t, P('Table 2.  Distribution of OLS estimates of rho under the unit-root DGP.', caption_st)]

tstat_data = [
    ['', 'Mean t-stat', 'Std t-stat', '14th pct', '86th pct'],
    ['Model 1 (no constant)', '-0.421', '0.990', '-1.442', '+0.672'],
    ['Model 2 (constant)',    '-1.550', '0.867', '-2.448', '-0.625'],
    ['Model 3 (const+trend)', '-2.219', '0.792', '-3.046', '-1.403'],
]
t = Table(tstat_data, colWidths=[W*0.30, W*0.175, W*0.175, W*0.175, W*0.175])
t.setStyle(tbl_style('#2e5d9e'))
story += [t, P('Table 3.  Distribution of t-statistics (rho-hat - 1) / se(rho-hat) under H<sub>0</sub>: rho = 1.', caption_st)]

story += [P('(b)  Distributions of rho-hat and t-statistics', h2_st)]
story += fig(FIG_B1, W,
    'Figure 2.  Top row: distribution of rho-hat for each model (red dashed = true rho = 1, '
    'dotted = 14th/86th percentiles). Bottom row: t-statistic distribution vs N(0,1) reference.')

story += [
    P('(c)  Comments', h2_st),
    P('<b>Downward bias of rho-hat.</b>  Even though the true value is rho = 1, the OLS estimator '
      'is biased downward. The bias worsens as more deterministic components are included: '
      'Model 1 has mean rho-hat &#8776; 0.979, while Model 3 has mean rho-hat &#8776; 0.879. '
      'Including a constant or trend absorbs variation from x<sub>t-1</sub>, pulling the '
      'estimated coefficient toward zero.', body_st),
    P('<b>Non-standard t-distribution.</b>  The t-statistics are <i>not</i> normally distributed '
      'under the unit-root null. They are left-skewed and shifted well below zero — Model 3 '
      'has a mean t-stat of &#8722;2.22, far from the N(0,1) mean of zero. '
      'This is the Dickey-Fuller distribution.', body_st),
    P('<b>Critical implication for inference.</b>  Using standard t-table critical values '
      '(&#8722;1.645 at 5%) would massively over-reject the unit-root null. The correct '
      '5% left-tail cutoff is &#8722;1.44 (Model 1), &#8722;2.45 (Model 2), and '
      '&#8722;3.05 (Model 3) — all more negative than standard critical values.', body_st),
    P('<b>Role of deterministics.</b>  Adding a constant or trend shifts the entire '
      'distribution of both rho-hat and the t-statistic further left. This is why '
      'Dickey-Fuller tables have three separate sets of critical values depending '
      'on the model specification.', body_st),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# PART B.2
# ══════════════════════════════════════════════════════════════════════════════
story += [
    P('B.2  Computer Exercise: BN Decomposition and HP Filter (US Real GDP)', h1_st), hr(),
    P('<b>Data.</b>  US Real GDP (GDPC1), quarterly, 1947:Q1–2019:Q4 (T = 292 observations, '
      'truncated at 2019:Q4 to exclude COVID). Log series: y<sub>t</sub> = ln(GDP<sub>t</sub>).', body_st),
    P('(a)  ARMA(1,0) Fit and Beveridge-Nelson Decomposition', h2_st),
    P('An ARMA(1,0) model with intercept is fitted to the first differences '
      '&#916;y<sub>t</sub> by maximum likelihood. BIC also selects ARMA(1,0) '
      'from models up to ARMA(2,1), confirming the specification.', body_st),
    P('Estimated model:&nbsp;&nbsp;'
      '&#916;y<sub>t</sub> = 0.00775 + 0.3585 &#916;y<sub>t-1</sub> + '
      '&#949;<sub>t</sub>,&nbsp;&nbsp;'
      'sigma<super>2</super> = 7.47 &#215; 10<super>-5</super>', mono_st),
]

arma_data = [
    ['Parameter', 'Estimate', 'Std. Error', 'z-stat', 'p-value', '95% CI'],
    ['c (intercept)',  '0.00775', '0.00080', '9.67', '0.000', '[0.006, 0.009]'],
    [TC('&#981; (AR coef)'), '0.3585', '0.047', '7.66', '0.000', '[0.267, 0.450]'],
    [TC('&#963;<super>2</super>'), '7.47e-5', '4.4e-6', '16.97', '0.000', '[6.6, 8.3]e-5'],
]
t = Table(arma_data, colWidths=[W*0.22, W*0.14, W*0.14, W*0.12, W*0.12, W*0.26])
t.setStyle(tbl_style())
story += [t, P('Table 4.  ARMA(1,0) estimation results for &#916;y<sub>t</sub>, 1947:Q1–2019:Q4.', caption_st)]

story += [
    P('The long-run mean of &#916;y<sub>t</sub> is '
      'mu-hat = c-hat / (1 &#8722; phi-hat) = 0.00775 / (1 &#8722; 0.3585) = <b>0.01207</b> '
      'per quarter (&#8776; 4.8% annualised).', body_st),
    P('<b>Beveridge-Nelson decomposition.</b>  For ARMA(1,0) on &#916;y<sub>t</sub>, '
      'the BN transitory component has a closed-form expression:', body_st),
    P('&nbsp;&nbsp;&nbsp;&nbsp;'
      'C<super>BN</super><sub>t</sub> = &#8722; phi-hat / (1 &#8722; phi-hat) '
      '&#215; (&#916;y<sub>t</sub> &#8722; mu-hat)', mono_st),
    P('&nbsp;&nbsp;&nbsp;&nbsp;With phi-hat = 0.3585:&nbsp;&nbsp;&nbsp;'
      'C<super>BN</super><sub>t</sub> = &#8722;0.558 &#215; (&#916;y<sub>t</sub> &#8722; 0.01207)',
      mono_st),
    P('The BN permanent component is '
      'tau<super>BN</super><sub>t</sub> = y<sub>t</sub> &#8722; C<super>BN</super><sub>t</sub>. '
      'The cycle captures how much current growth deviates from the long-run average, '
      'scaled by the persistence of those deviations.', body_st),
    P('(b)  Hodrick-Prescott Filter', h2_st),
    P('The HP filter finds the trend tau<super>HP</super><sub>t</sub> by minimising:', body_st),
    P('&nbsp;&nbsp;&nbsp;&nbsp;'
      '&#931;(y<sub>t</sub> &#8722; tau<sub>t</sub>)<super>2</super> + '
      '&#955; &#931;(&#916;<super>2</super>tau<sub>t</sub>)<super>2</super>', mono_st),
    P('with <b>&#955; = 1,600</b> (standard for quarterly data). A higher &#955; produces '
      'a smoother trend.', body_st),
    P('(c)  Comparison of Transitory Components', h2_st),
]
story += fig(FIG_B2, W,
    'Figure 3.  Top: log(GDP), BN trend and HP trend. '
    'Bottom: BN cycle (blue) vs HP cycle (red dashed), shaded = NBER recessions.')

cycle_data = [
    ['Statistic', 'BN Cycle', 'HP Cycle'],
    ['Std. Deviation',       '0.0052',  '0.0158'],
    ['Minimum',              '-0.0148', '-0.0623'],
    ['Maximum',              '+0.0214', '+0.0372'],
    ['Correlation (BN, HP)', '-0.257',  '—'],
]
t = Table(cycle_data, colWidths=[W*0.44, W*0.28, W*0.28])
t.setStyle(tbl_style('#2e5d9e'))
story += [t, P('Table 5.  Summary statistics for cyclical components.', caption_st)]

story += [
    P('<b>Amplitude.</b>  The HP cycle has a standard deviation of 1.58% — about three times '
      'larger than the BN cycle (0.52%). The HP filter attributes large, persistent swings '
      'in GDP (e.g., the 2008–09 recession, reaching &#8722;6.2%) to the cycle. '
      'The BN cycle is smaller because positive autocorrelation in growth (phi = 0.36) '
      'means above-average growth today raises the permanent component by more than just '
      'the current increment, absorbing much of the swing.', body_st),
    P('<b>Negative correlation.</b>  The two cycles are negatively correlated (&#8722;0.26), '
      'meaning they often move in opposite directions. The BN and HP decompositions embed '
      'fundamentally different views of what constitutes the "trend": the HP trend is a '
      'smooth curve, while the BN trend is a martingale that jumps every period.', body_st),
    P('<b>Recession behaviour.</b>  Both cycles turn negative during NBER recessions '
      '(shaded grey). The HP cycle more clearly identifies business cycle turning points. '
      'The BN cycle is noisier at quarterly frequency with only an AR(1), but is '
      'theoretically grounded in rational expectations.', body_st),
    P('<b>Conclusion:</b>  Both filters agree on the direction of cyclical swings around '
      'recessions but disagree on their magnitude. The choice depends on whether one views '
      'the trend as a smooth path (HP) or a stochastic process incorporating all '
      'predictable future growth (BN). Neither is universally correct.', result_st),
]

doc.build(story)
print(f"Saved: {OUT}")
