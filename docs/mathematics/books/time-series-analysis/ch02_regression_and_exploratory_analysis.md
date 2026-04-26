# Ch 2: Time Series Regression and Exploratory Data Analysis

## Table of Contents

- [1. Classical Regression in Time Series](#1-classical-regression-in-time-series)
- [2. Model Selection: AIC, AICc, BIC](#2-model-selection-aic-aicc-bic)
- [3. Detrending and Differencing](#3-detrending-and-differencing)
- [4. Variance-Stabilizing Transformations](#4-variance-stabilizing-transformations)
- [5. Lagged Scatterplots and Lagged Regression](#5-lagged-scatterplots-and-lagged-regression)
- [6. Smoothing](#6-smoothing)

## 1. Classical Regression in Time Series

- **Model** xt = β0 + β1 zt1 + … + βq ztq + wt — output xt regressed on q fixed inputs ztj plus error wt; for now wt is iid N(0, σw²), an assumption to be relaxed (Ch 3).
- **OLS estimate** β̂ = (Σ zt zt')⁻¹ Σ zt xt — minimizes the sum of squared errors; unbiased and minimum-variance among linear unbiased estimators (Gauss–Markov).
- **Variance and inference** — under normal errors β̂ ~ N(β, σw² C) with C = (Σ zt zt')⁻¹; unbiased σ̂w² = MSE = SSE/(n − q − 1); the t-statistic (β̂i − βi)/(sw √cii) has tn−q−1 distribution.
- **F-test for nested models** — full model vs. reduced model with r < q regressors gives F = (SSR/(q − r))/(SSE/(n − q − 1)) where SSR = SSEr − SSE; rejects H0: βr+1 = … = βq = 0 when F is large.
- **Coefficient of determination** R² = (SSE0 − SSE)/SSE0 where SSE0 = Σ(xt − x̄)² — proportion of variation accounted for by all regressors.
- **Chicken-price example** — monthly whole-bird price 2001–2016 fit as xt = β0 + β1 t + wt; estimated slope 3.59 (SE 0.08) cents/year, an upward linear trend.
- **Pollution / mortality / temperature example** — LA County weekly cardiovascular mortality Mt regressed on time t, centered temperature (Tt − T̄), (Tt − T̄)², and particulates Pt; M̂t = 2831.5 − 1.396 t − 0.472(Tt − T̄) + 0.023(Tt − T̄)² + 0.255 Pt with R² = 0.60. Centering temperature avoids collinearity between Tt and Tt². Residuals still have substantial autocorrelation (handled in Ch 3.8).
- **Lagged regression** — Rt = β0 + β1 St−6 + wt fits Recruitment on SOI six months earlier; β̂1 = −44.28 (SE 2.78), confirming SOI leads Recruitment.

## 2. Model Selection: AIC, AICc, BIC

- **Need** — minimizing σ̂k² = SSE(k)/n decreases monotonically with parameters k, so direct minimization always picks the largest model. Penalize complexity instead.
- **AIC** — log σ̂k² + (n + 2k)/n; an estimate of Kullback–Leibler discrepancy between true and candidate model (Akaike 1969–74).
- **AICc** — log σ̂k² + (n + k)/(n − k − 2); bias-corrected for small samples or large k/n (Sugiura 1978; Hurvich & Tsai 1989).
- **BIC** (Schwarz 1978; also SIC) — log σ̂k² + k log(n)/n; a Bayesian-derived criterion. Heavier penalty than AIC, so BIC tends to choose smaller models.
- **Practical guidance** — BIC tends to pick the right order in large samples; AICc tends to be superior in small samples with relatively many parameters (McQuarrie & Tsai 1998).

## 3. Detrending and Differencing

- **Stationarity is needed** — averaging lagged products over time only makes sense if the dependence structure is stable. Trends, growing variance, and other nonstationarities have to be removed first.
- **Trend-stationary model** xt = μt + yt — observations equal a deterministic trend μt plus stationary residual yt; one estimates μ̂t and works with ŷt = xt − μ̂t. Example: chicken prices detrended by subtracting the fitted line.
- **Random walk with drift as trend** μt = δ + μt−1 + wt — if the trend is itself a stochastic random walk, **differencing** is preferred over detrending: xt − xt−1 = δ + wt + (yt − yt−1) is stationary.
- **Detrending vs. differencing** — detrending estimates parameters and recovers ŷt, but assumes a deterministic functional form; differencing removes trend without estimating parameters and works for both deterministic and stochastic trends, but does not produce an estimate of yt itself.
- **Backshift operator** B — defined by Bxt = xt−1, with Bk xt = xt−k; first difference ∇xt = (1 − B)xt; differences of order d are ∇d = (1 − B)d.
- **What differencing removes** — first difference eliminates linear trend; second difference eliminates quadratic trend; in general, dth difference eliminates a degree-d polynomial trend.
- **Global temperature example** — series behaves more like a random walk than a trend-stationary series; the first difference shows minimal autocorrelation, suggesting random walk with drift δ̂ ≈ 0.008 °C/year (≈ 1 °C per century).
- **Fractional differencing** — extends ∇d to −0.5 < d < 0.5; long memory series (Granger & Joyeux 1980; Hosking 1981) correspond to 0 < d < 0.5; deferred to Section 5.1.

## 4. Variance-Stabilizing Transformations

- **Log transform** yt = log xt — suppresses larger fluctuations where the underlying values are larger; useful when variability scales with level (multiplicative noise).
- **Box–Cox family** yt = (xtλ − 1)/λ for λ ≠ 0, log xt for λ = 0 — generalizes the log transform; methods for choosing λ exist but are not pursued in this chapter.
- **Glacial varves example** — yearly sediment thicknesses span Massachusetts deglaciation (n = 634 years); raw variance grows with thickness, but log(varve) has roughly constant variance and is closer to normal; first differences of log(varve) show significant negative correlation at lag 1, hinting at long memory (revisited in Ch 5).

## 5. Lagged Scatterplots and Lagged Regression

- **Why scatterplot matrices** — the ACF only captures linear dependence between xt and xt−h; nonlinear dependence is invisible to it. Lagged scatterplots of (xt vs xt−h) for h = 1, 2, … reveal nonlinear structure.
- **Locally weighted scatterplot smoothing (lowess)** — robust nearest-neighbor regression that overlays smooth nonlinear fits on the scatterplots, helping to see curvature.
- **SOI / Recruitment** — lagged scatterplots show strong nonlinear relationship at h = 5–8 months: the SOI–Recruitment relationship differs for positive vs. negative SOI values.
- **Dummy-variable lagged regression** — Rt = β0 + β1 St−6 + β2 Dt−6 + β3 Dt−6 St−6 + wt with Dt = 1{St ≥ 0} captures the regime change; piecewise fit roughly matches the lowess smoother but residuals are still autocorrelated.
- **Sinusoid as linear regression** — A cos(2πωt + φ) = β1 cos(2πωt) + β2 sin(2πωt) with β1 = A cos φ, β2 = −A sin φ; if ω is known, amplitude and phase enter linearly. Recovers signal even when the SNR is small (σw = 5, A = 2 example). Spectral methods (Ch 4) handle the case when ω is unknown.

## 6. Smoothing

- **Symmetric moving average** mt = Σ aj xt−j with aj = a−j ≥ 0 and Σ aj = 1 — averages near values to highlight trend or remove a known cycle. SOI smoothed with 12-month box-car weights filters out the annual cycle and emphasizes the El Niño cycle.
- **Kernel smoother (Nadaraya–Watson)** mt = Σ wi(t) xi with wi(t) = K((t − i)/b) / Σ K((t − j)/b); typically uses the standard normal kernel K(z) = (2π)⁻¹/² exp(−z²/2). Bandwidth b controls smoothness — wider b ⇒ smoother fit.
- **Lowess (locally weighted scatterplot smoothing)** — robust k-nearest-neighbor regression: for each xt, the nearest fraction of points is weighted (closer points get higher weight) and a robust local regression produces the smoothed value (Cleveland 1979). Two SOI fits: f = 0.05 isolates the El Niño cycle; f = 2/3 reveals long-term trend.
- **Smoothing splines** — minimize Σ(xt − mt)² + λ ∫(mt'')² dt with cubic spline mt; λ trades off fit and smoothness. λ = 0 returns the data (no smoothing); λ = ∞ forces mt'' = 0 (linear regression). The "long drive" intuition: ∫(mt'')² is total acceleration over the trip.
- **Smoothing one series as a function of another** — lowess of mortality on temperature reveals U-shape with minimum around 83 °F; mortality higher at cold than at hot extremes, matching the curvilinear term in the Section 1 regression.
