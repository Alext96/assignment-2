import matplotlib
import numpy as np
import pandas as pd

matplotlib.use('Agg')
import warnings

import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.filters.hp_filter import hpfilter
from statsmodels.tsa.stattools import adfuller

warnings.filterwarnings('ignore')

np.random.seed(42)

# PART A: Nelson-Plosser ADF Test on Real GNP (RGNP)

df_np = pd.read_excel('Nelson_Plosser_data.xlsx', sheet_name='nelson_plosser')

# Use RGNP: remove zeros, log-transform
rgnp = df_np[df_np['RGNP'] > 0][['Year', 'RGNP']].copy()
rgnp['log_RGNP'] = np.log(rgnp['RGNP'])
rgnp = rgnp.set_index('Year')

print("=" * 60)
print("PART A: ADF Test on log(Real GNP), 1909-1970")
print("=" * 60)
print(f"Sample: {rgnp.index[0]} - {rgnp.index[-1]}, T = {len(rgnp)}")
print()

# Plot the series
fig, axes = plt.subplots(2, 1, figsize=(10, 8))
axes[0].plot(rgnp.index, rgnp['log_RGNP'], 'b-o', markersize=3)
axes[0].set_title('Log Real GNP (Nelson-Plosser), 1909–1970', fontsize=13)
axes[0].set_xlabel('Year')
axes[0].set_ylabel('log(RGNP)')
axes[0].grid(True, alpha=0.3)

# First difference
d_log_rgnp = rgnp['log_RGNP'].diff().dropna()
axes[1].plot(d_log_rgnp.index, d_log_rgnp, 'r-o', markersize=3)
axes[1].axhline(0, color='k', linewidth=0.8, linestyle='--')
axes[1].set_title('First Difference of Log Real GNP', fontsize=13)
axes[1].set_xlabel('Year')
axes[1].set_ylabel('Δlog(RGNP)')
axes[1].grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('partA_rgnp_plot.png', dpi=150)
plt.close()
print("Saved: partA_rgnp_plot.png")

# ADF top-down approach following Lecture Notes pp. 138-141
# Since log(RGNP) has a clear upward trend, start with the most general
# model: constant + trend (Model 3), then test down.
#
# The key test is the JOINT F-test (phi_3): H0: gamma = a2 = 0
#   Unrestricted: dy = a0 + a2*t + gamma*y_{t-1} + b1*dy_{t-1} + ...
#   Restricted:   dy = a0                         + b1*dy_{t-1} + ...
# (Restricting both the unit root coefficient AND the trend to zero jointly)
# Critical value (phi_3) at 5%: 6.49, at 10%: 5.47 (Fuller 1976 / DW tables)

y_level = rgnp['log_RGNP'].values
n = len(y_level)
dy_arr = np.diff(y_level)
trend_arr = np.arange(1, n)  # 1, 2, ..., T-1 (aligns with dy)
y_lag = y_level[:-1]         # y_{t-1}

# Choose lag length by BIC over lags 0..4 for the unrestricted model
best_bic = np.inf
best_lag = 0
for lag in range(5):
    if lag == 0:
        X_ur = np.column_stack([np.ones(n-1), trend_arr, y_lag])
        y_ur = dy_arr
    else:
        # Need to trim for lagged differences
        X_ur = np.column_stack([
            np.ones(n-1-lag),
            trend_arr[lag:],
            y_lag[lag:],
            *[dy_arr[lag-j-1:n-1-j-1] for j in range(lag)]
        ])
        y_ur = dy_arr[lag:]
    b = np.linalg.lstsq(X_ur, y_ur, rcond=None)[0]
    resid = y_ur - X_ur @ b
    T_eff = len(y_ur)
    k = X_ur.shape[1]
    bic = T_eff * np.log(np.sum(resid**2) / T_eff) + k * np.log(T_eff)
    if bic < best_bic:
        best_bic = bic
        best_lag = lag

print(f"\nBIC-selected lag order: {best_lag}")

# Run tests with best lag
lag = best_lag
if lag == 0:
    X_ur = np.column_stack([np.ones(n-1), trend_arr, y_lag])
    y_reg = dy_arr
else:
    X_ur = np.column_stack([
        np.ones(n-1-lag),
        trend_arr[lag:],
        y_lag[lag:],
        *[dy_arr[lag-j-1:n-1-j-1] for j in range(lag)]
    ])
    y_reg = dy_arr[lag:]

# Restricted model (H0: gamma = a2 = 0): dy = a0 + b_j * dy_{t-j}
if lag == 0:
    X_r = np.ones((n-1, 1))
else:
    X_r = np.column_stack([
        np.ones(n-1-lag),
        *[dy_arr[lag-j-1:n-1-j-1] for j in range(lag)]
    ])

b_ur = np.linalg.lstsq(X_ur, y_reg, rcond=None)[0]
b_r  = np.linalg.lstsq(X_r,  y_reg, rcond=None)[0]
SSE_ur = np.sum((y_reg - X_ur @ b_ur)**2)
SSE_r  = np.sum((y_reg - X_r  @ b_r )**2)
T_eff  = len(y_reg)
k_ur   = X_ur.shape[1]

# phi_3 F-statistic (2 restrictions: gamma=0 and a2=0)
n_restrictions = 2
F_phi3 = ((SSE_r - SSE_ur) / n_restrictions) / (SSE_ur / (T_eff - k_ur))

# ADF t-statistic on gamma (coefficient on y_{t-1})
se_ur = np.sqrt(np.diag(SSE_ur / (T_eff - k_ur) * np.linalg.inv(X_ur.T @ X_ur)))
gamma_hat = b_ur[2]   # coefficient on y_{t-1} (index 2: after intercept and trend)
t_gamma = gamma_hat / se_ur[2]

print(f"\n--- Joint F-test (phi_3): H0: gamma = a2 = 0 ---")
print(f"  gamma_hat (coef on y_{{t-1}}): {gamma_hat:.6f}")
print(f"  t(gamma):                     {t_gamma:.4f}  [DF 5% CV (ct): -3.49]")
print(f"  phi_3 F-statistic:            {F_phi3:.4f}  [5% CV: 6.49, 10% CV: 5.47]")
if F_phi3 < 6.49:
    print("  => Do NOT reject H0 (phi_3 < 6.49): unit root present, trend not significant")
    print("     --> log(RGNP) is consistent with a RANDOM WALK (with drift)")
else:
    print("  => Reject H0: series is trend-stationary")

# Also report standard ADF stat for completeness
res_ct = adfuller(rgnp['log_RGNP'], maxlag=best_lag, regression='ct', autolag=None)
print(f"\n--- ADF t-statistic (constant + trend, lag={best_lag}) ---")
print(f"  ADF stat: {res_ct[0]:.4f} | CV 1%={res_ct[4]['1%']:.3f}, 5%={res_ct[4]['5%']:.3f}, 10%={res_ct[4]['10%']:.3f}")

# Confirm stationarity of first difference
print(f"\n--- ADF on first difference (no constant, lag=0) ---")
res_d = adfuller(d_log_rgnp, regression='n', autolag='BIC')
print(f"  ADF stat: {res_d[0]:.4f} | CV 1%={res_d[4]['1%']:.3f}, 5%={res_d[4]['5%']:.3f}, 10%={res_d[4]['10%']:.3f}")
print(f"  => {'Reject H0: first difference is STATIONARY (I(1) confirmed)' if res_d[0] < res_d[4]['5%'] else 'Fail to reject'}")


# PART B.1: Random Walk Monte Carlo Simulation

print("\n" + "=" * 60)
print("PART B.1: Random Walk Monte Carlo Simulation")
print("=" * 60)

N = 100_000
T = 81

# Simulate N random walks of length T+1 (x0=0, then T steps)
innovations = np.random.normal(0, 1, size=(N, T))
x = np.zeros((N, T + 1))
for t in range(1, T + 1):
    x[:, t] = x[:, t - 1] + innovations[:, t - 1]

# x has shape (N, T+1): x[:,0]=0, x[:,1]...x[:,T]
# Regressors: x_{t-1} for t=1..T -> x[:,0:T]
# Dependent:  x_t     for t=1..T -> x[:,1:T+1]

Y = x[:, 1:]          # (N, T)
X_lag = x[:, :-1]     # (N, T)
t_trend = np.arange(1, T + 1)  # 1,2,...,T

rho_hat = np.zeros((N, 3))
se_rho  = np.zeros((N, 3))

# Vectorized OLS across all N simulations simultaneously
ones = np.ones(T)
t_vec = t_trend  # shape (T,)

# Model 1: y = rho * x_{t-1}   (no intercept)
# beta = (X'X)^{-1} X'y; X = x_lag (N x T), treat each row as one regression
# X'X for model 1 is scalar: sum(x_lag^2) over t, shape (N,)
# Note: professor's fastols uses uhat'uhat/T (not T-k) for SEs — we match that here.
XtX1 = np.sum(X_lag**2, axis=1)                     # (N,)
Xty1 = np.sum(X_lag * Y, axis=1)                    # (N,)
rho_hat[:, 0] = Xty1 / XtX1
resid1 = Y - rho_hat[:, 0:1] * X_lag               # (N, T)
s2_1 = np.sum(resid1**2, axis=1) / T
se_rho[:, 0] = np.sqrt(s2_1 / XtX1)

# Model 2: y = c + rho * x_{t-1}
# Use Frisch-Waugh: partial out constant analytically
Xm_lag = X_lag - X_lag.mean(axis=1, keepdims=True)  # demeaned x_lag
Ym = Y - Y.mean(axis=1, keepdims=True)              # demeaned y
XtX2_rho = np.sum(Xm_lag**2, axis=1)
Xty2_rho = np.sum(Xm_lag * Ym, axis=1)
rho_hat[:, 1] = Xty2_rho / XtX2_rho
resid2 = Ym - rho_hat[:, 1:2] * Xm_lag
s2_2 = np.sum(resid2**2, axis=1) / T
se_rho[:, 1] = np.sqrt(s2_2 / XtX2_rho)

# Model 3: y = c + delta*t + rho * x_{t-1}
Z = np.column_stack([ones, t_vec])  # (T, 2)
ZtZ_inv = np.linalg.inv(Z.T @ Z)
PZ = Z @ ZtZ_inv @ Z.T
MZ = np.eye(T) - PZ

Xm3 = X_lag @ MZ.T   # (N, T)
Ym3 = Y @ MZ.T       # (N, T)
XtX3 = np.sum(Xm3**2, axis=1)
Xty3 = np.sum(Xm3 * Ym3, axis=1)
rho_hat[:, 2] = Xty3 / XtX3
resid3 = Ym3 - rho_hat[:, 2:3] * Xm3
s2_3 = np.sum(resid3**2, axis=1) / T
se_rho[:, 2] = np.sqrt(s2_3 / XtX3)

# t-statistics under H0: rho = 1
t_stats = (rho_hat - 1.0) / se_rho

print("\nPercentiles of rho_hat:")
print(f"{'Model':<10} {'Mean':>8} {'Std':>8} {'14th':>8} {'86th':>8}")
for m in range(3):
    print(f"  Model {m+1}  {rho_hat[:,m].mean():8.4f} {rho_hat[:,m].std():8.4f} "
          f"{np.percentile(rho_hat[:,m], 14):8.4f} {np.percentile(rho_hat[:,m], 86):8.4f}")

print("\nPercentiles of t-statistics (H0: rho=1):")
print(f"{'Model':<10} {'Mean':>8} {'Std':>8} {'14th':>8} {'86th':>8}")
for m in range(3):
    print(f"  Model {m+1}  {t_stats[:,m].mean():8.4f} {t_stats[:,m].std():8.4f} "
          f"{np.percentile(t_stats[:,m], 14):8.4f} {np.percentile(t_stats[:,m], 86):8.4f}")

# Plots for Part B.1
fig, axes = plt.subplots(2, 3, figsize=(15, 9))
model_labels = ['Model 1: No constant', 'Model 2: Constant', 'Model 3: Constant + Trend']
colors = ['steelblue', 'darkorange', 'green']

for m in range(3):
    # Top row: rho_hat distributions
    axes[0, m].hist(rho_hat[:, m], bins=100, density=True, color=colors[m], alpha=0.75, edgecolor='none')
    axes[0, m].axvline(1.0, color='red', linewidth=1.5, linestyle='--', label='True ρ=1')
    axes[0, m].axvline(np.percentile(rho_hat[:, m], 14), color='black', linewidth=1.2,
                       linestyle=':', label='14th/86th pct')
    axes[0, m].axvline(np.percentile(rho_hat[:, m], 86), color='black', linewidth=1.2, linestyle=':')
    axes[0, m].set_title(f'{model_labels[m]}\nρ̂ distribution', fontsize=10)
    axes[0, m].set_xlabel('ρ̂')
    axes[0, m].legend(fontsize=8)
    axes[0, m].grid(True, alpha=0.3)

    # Bottom row: t-statistic distributions
    axes[1, m].hist(t_stats[:, m], bins=100, density=True, color=colors[m], alpha=0.75, edgecolor='none')
    # Overlay standard normal for reference
    x_norm = np.linspace(-6, 4, 300)
    axes[1, m].plot(x_norm, stats.norm.pdf(x_norm), 'k--', linewidth=1.2, label='N(0,1)')
    axes[1, m].axvline(np.percentile(t_stats[:, m], 14), color='red', linewidth=1.2,
                       linestyle=':', label='14th/86th pct')
    axes[1, m].axvline(np.percentile(t_stats[:, m], 86), color='red', linewidth=1.2, linestyle=':')
    axes[1, m].set_title(f't-stat distribution (H₀: ρ=1)', fontsize=10)
    axes[1, m].set_xlabel('(ρ̂ − 1) / se(ρ̂)')
    axes[1, m].legend(fontsize=8)
    axes[1, m].grid(True, alpha=0.3)

plt.suptitle('Monte Carlo: Random Walk (N=100,000, T=81)', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('partB1_simulation.png', dpi=150)
plt.close()
print("\nSaved: partB1_simulation.png")


# PART B.2: GDP Beveridge-Nelson + HP Filter

print("\n" + "=" * 60)
print("PART B.2: BN Decomposition & HP Filter on US Real GDP")
print("=" * 60)

df_gdp = pd.read_excel('real_gdp_US_2022Q4.xlsx', sheet_name='Sheet1')
df_gdp['dates'] = pd.to_datetime(df_gdp['dates'], dayfirst=True)
df_gdp = df_gdp.sort_values('dates').reset_index(drop=True)

# Truncate to 2019:Q4
df_gdp = df_gdp[df_gdp['dates'] <= '2019-12-31'].copy()
df_gdp['log_gdp'] = np.log(df_gdp['gdpc1'])
df_gdp = df_gdp.set_index('dates')

print(f"Sample: {df_gdp.index[0].strftime('%Y-Q%q' if hasattr(df_gdp.index[0],'quarter') else '%Y-%m-%d')} "
      f"to {df_gdp.index[-1].strftime('%Y-%m-%d')}, T={len(df_gdp)}")

y = df_gdp['log_gdp'].values
T_gdp = len(y)
dy = np.diff(y)  # Delta y_t

# --- (a) ARMA(1,0) on Delta y_t ---
model_ar1 = ARIMA(dy, order=(1, 0, 0), trend='c')
res_ar1 = model_ar1.fit()
print("\nARMA(1,0) fit on Δy_t:")
print(res_ar1.summary().tables[1])

mu_hat   = res_ar1.params[0] / (1 - res_ar1.params[1])  # long-run mean E[Δy_t]
phi_hat  = res_ar1.params[1]
c_hat    = res_ar1.params[0]

print(f"\n  c (intercept):  {c_hat:.6f}")
print(f"  φ (AR coeff):   {phi_hat:.6f}")
print(f"  Long-run mean μ = c/(1-φ): {mu_hat:.6f}")

# BN cycle for ARMA(1,0): C_t = -φ/(1-φ) * (Δy_t - μ)
# Only defined for t=1,...,T (since Δy has T-1 observations from T_gdp observations)
delta_y_series = np.concatenate([[np.nan], dy])  # align with y (index 0 has no diff)
bn_cycle = np.full(T_gdp, np.nan)
for t in range(1, T_gdp):
    bn_cycle[t] = -phi_hat / (1 - phi_hat) * (dy[t - 1] - mu_hat)

bn_trend = y - bn_cycle

# --- (b) HP Filter ---
hp_cycle, hp_trend = hpfilter(y, lamb=1600)

# --- (c) Plot ---
fig, axes = plt.subplots(2, 1, figsize=(12, 9))

# Top panel: trends
axes[0].plot(df_gdp.index, y, 'k-', linewidth=1.5, label='log(GDP)', alpha=0.8)
axes[0].plot(df_gdp.index, bn_trend, 'b--', linewidth=1.5, label='BN Trend', alpha=0.9)
axes[0].plot(df_gdp.index, hp_trend, 'r-.', linewidth=1.5, label='HP Trend', alpha=0.9)
axes[0].set_title('US Real GDP: Log Level, BN Trend, and HP Trend (1947Q1–2019Q4)', fontsize=12)
axes[0].set_ylabel('log(Real GDP)')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Bottom panel: cycles
axes[1].plot(df_gdp.index[1:], bn_cycle[1:], 'b-', linewidth=1.5,
             label='BN Transitory Component', alpha=0.85)
axes[1].plot(df_gdp.index, hp_cycle, 'r--', linewidth=1.5,
             label='HP Transitory Component', alpha=0.85)
axes[1].axhline(0, color='k', linewidth=0.8, linestyle='-')

# Shade NBER recessions (NBER column in dataset)
nber = df_gdp['NBER'].values
for t in range(len(nber) - 1):
    if nber[t] == 1:
        axes[1].axvspan(df_gdp.index[t], df_gdp.index[t + 1], alpha=0.12, color='gray')

axes[1].set_title('Transitory Components: BN vs HP Filter (shaded = NBER recessions)', fontsize=12)
axes[1].set_ylabel('Deviation from trend')
axes[1].set_xlabel('Quarter')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('partB2_bn_hp.png', dpi=150)
plt.close()
print("Saved: partB2_bn_hp.png")

# Summary stats for cycles
bn_c = bn_cycle[1:]
hp_c = hp_cycle[1:]
print("\nCycle summary statistics:")
print(f"{'':20s} {'BN':>12} {'HP':>12}")
print(f"{'Std Dev':20s} {np.std(bn_c):12.5f} {np.std(hp_c):12.5f}")
print(f"{'Min':20s} {np.min(bn_c):12.5f} {np.min(hp_c):12.5f}")
print(f"{'Max':20s} {np.max(bn_c):12.5f} {np.max(hp_c):12.5f}")
print(f"{'Correlation':20s} {np.corrcoef(bn_c, hp_c[:])[0,1]:12.4f}")
print("\nDone. All figures saved.")
