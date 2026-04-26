# Ch 1: Characteristics of Time Series

## Table of Contents

- [1. Nature of Time Series Data](#1-nature-of-time-series-data)
- [2. Statistical Models](#2-statistical-models)
- [3. Measures of Dependence](#3-measures-of-dependence)
- [4. Stationarity](#4-stationarity)
- [5. Estimating Correlation from Data](#5-estimating-correlation-from-data)
- [6. Vector and Multidimensional Series](#6-vector-and-multidimensional-series)

## 1. Nature of Time Series Data

- **Time series analysis** — systematic methods for data observed at successive time points; classical iid-based statistics fail because adjacent observations are correlated.
- **Two complementary approaches** — *time domain* asks how today affects tomorrow (lagged relationships); *frequency domain* asks what cycles drive the series (periodicities).
- **First step is always plotting** — visual inspection of the recorded data over time suggests the model and the summary statistics that will matter.
- **Worked examples introduced as motivation** — Johnson & Johnson quarterly earnings (trend + quarterly seasonality), global land–ocean temperature deviations 1880–2015 (trend), speech recording of "aaa…hhh" (regular pitch period), DJIA daily returns 2006–2016 (volatility clustering), monthly Southern Oscillation Index and fish Recruitment 1950–1987 (joint cycles, El Niño), fMRI BOLD signal under periodic brushing (designed-experiment cycles), earthquake vs. explosion seismic phases P and S (discrimination problem).

## 2. Statistical Models

- **Stochastic process** — collection of random variables {xt} indexed by integer time; the realized data are one *realization* of the process.
- **White noise** wt ~ wn(0, σw²) — uncorrelated zero-mean variates with finite variance; "white" by analogy with white light, all periodic oscillations equally present.
  - **iid noise** wt ~ iid(0, σw²) — strengthens uncorrelated to independent.
  - **Gaussian white noise** wt ~ iid N(0, σw²) — independent normal variates; serves as the canonical building block.
- **Moving average / filtering** — replacing wt with a local average, e.g. vt = (wt−1 + wt + wt+1)/3, smooths the series; any linear combination of values at different lags is called a *filtered series*.
- **Autoregression** — current value is a linear function of past values plus noise; example xt = xt−1 − 0.9 xt−2 + wt produces quasi-periodic behavior similar to the speech series.
- **Random walk with drift** — xt = δ + xt−1 + wt with x0 = 0, equivalently xt = δt + Σwj; serves as a model for trend such as the global temperature record. Pure random walk is δ = 0.
- **Signal-plus-noise model** xt = st + vt — fixed signal st obscured by noise vt; the **signal-to-noise ratio (SNR)** is the ratio of signal amplitude to noise standard deviation; larger SNR makes the signal easier to detect. Sinusoidal signal A cos(2πωt + φ) parameterized by amplitude A, frequency ω, phase φ.

## 3. Measures of Dependence

- **Joint distribution function** Ft1,…,tn — fully describes the series but is unwieldy except in the Gaussian case.
- **Mean function** μxt = E(xt) — the expected level of the series at time t.
- **Autocovariance function** γx(s, t) = E[(xs − μs)(xt − μt)] — measures linear dependence between two points on the same series; γ(t, t) = var(xt). Smooth series have γ that stays large at large separations; choppy series have γ that decays to zero quickly.
- **Autocorrelation function (ACF)** ρ(s, t) = γ(s, t) / √(γ(s, s)γ(t, t)) — scaled to [−1, 1]; measures how well xs linearly predicts xt.
- **Cross-covariance** γxy(s, t) = E[(xs − μxs)(yt − μyt)] and **cross-correlation (CCF)** ρxy(s, t) = γxy / √(γx(s,s)γy(t,t)) — extend the same ideas to two series.
- **Property 1.1 (Covariance of linear combinations)** — for U = Σaj Xj and V = Σbk Yk, cov(U, V) = ΣΣ aj bk cov(Xj, Yk); the workhorse for computing γ of filtered series.
- **Three-point moving average** has γv(h) = (3/9)σw² at h=0, (2/9)σw² at |h|=1, (1/9)σw² at |h|=2, 0 beyond — autocovariance depends only on lag, not absolute time, motivating the concept of stationarity.
- **Random walk** has γx(s, t) = min(s, t)σw² — depends on absolute times, and var(xt) = tσw² grows without bound.

## 4. Stationarity

- **Strictly stationary** — every joint distribution {xt1, …, xtk} matches the time-shifted set {xt1+h, …, xtk+h} for all k, all times, all shifts. Too strong to verify or impose in practice.
- **Weakly stationary** — finite variance, constant mean μt = μ, and autocovariance γ(s, t) depends on s, t only through |s − t|. Used as the working definition; "stationary" without qualifier means weakly stationary.
- **Lag notation** — for stationary series write γ(h) = cov(xt+h, xt) and ρ(h) = γ(h)/γ(0); ACF is symmetric γ(h) = γ(−h) and bounded |γ(h)| ≤ γ(0) (Cauchy–Schwarz).
- **Examples** — white noise is stationary; the three-point moving average is stationary; a random walk is **not** stationary because var grows with t; a random walk with drift fails both conditions.
- **Trend stationarity** — xt = α + βt + yt with yt stationary: mean depends on t (not stationary), but γx(h) = γy(h), so the series is stationary *around a linear trend*. The price-of-chicken series is the canonical example.
- **Jointly stationary** — two stationary series xt, yt are jointly stationary if γxy(h) = cov(xt+h, yt) depends only on lag h. CCF is generally **not** symmetric: ρxy(h) = ρyx(−h).
- **Lead/lag detection** — for yt = A xt−ℓ + wt, γyx(h) peaks at h = ℓ; a peak on the positive side of lag means x leads y, a peak on the negative side means x lags y.
- **Linear process** xt = μ + Σ ψj wt−j with Σ|ψj| < ∞ — autocovariance γx(h) = σw² Σ ψj+h ψj. **Causal** linear process has ψj = 0 for j < 0 (no dependence on the future); only causal models are useful for forecasting.
- **Gaussian process** — every finite collection (xt1, …, xtn) is multivariate normal. Weak stationarity + Gaussianity ⇒ strict stationarity. Marginal Gaussianity is **not** sufficient for joint Gaussianity.
- **Wold Decomposition** (Theorem B.5) — any stationary non-deterministic series is a causal linear process (with Σ ψj² < ∞); a Gaussian stationary series is one with iid N(0, σw²) innovations. This is why stationary Gaussian processes are the foundation for time series modeling.

## 5. Estimating Correlation from Data

- **Single realization problem** — only one time series is usually observed, so without stationarity we cannot average to estimate population quantities.
- **Sample mean** x̄ = (1/n) Σ xt, with var(x̄) = (1/n) Σ_{h=−n}^{n} (1 − |h|/n) γx(h); reduces to σx²/n only under white noise; under positive autocorrelation the standard error is **larger** than the iid formula suggests.
- **Sample autocovariance** γ̂(h) = (1/n) Σ_{t=1}^{n−h} (xt+h − x̄)(xt − x̄). Dividing by n (not n − h) preserves non-negative definiteness, at the cost of bias.
- **Sample autocorrelation** ρ̂(h) = γ̂(h)/γ̂(0).
- **Property 1.2 (Large-sample distribution of ACF)** — if xt is white noise (iid with finite fourth moment), ρ̂(h) is approximately N(0, 1/n) for fixed h. Practical rule: peaks outside ±2/√n are roughly 95% significant against the white-noise null.
- **Use** — many modeling procedures reduce a series to white noise residuals; their ACFs should then lie within ±2/√n.
- **Sample CCF** ρ̂xy(h) = γ̂xy(h) / √(γ̂x(0) γ̂y(0)); same ±2/√n band applies (Property 1.3) **only if at least one of the series is white noise**.
- **Prewhitening** — to use the ±2/√n band on a CCF, first remove the structure from one series (e.g., regress out a fitted sinusoid) so it becomes white noise; then cross-correlate. Without prewhitening, two independent cyclic series can show spurious significant CCF, as illustrated by simulating xt and yt with shared period 12.
- **SOI / Recruitment example** — both ACFs show 12-month periodicity; CCF peaks at h = −6 (negative), meaning SOI 6 months earlier predicts lower Recruitment now.

## 6. Vector and Multidimensional Series

- **Vector time series** xt = (xt1, …, xtp)' — stack p univariate series; the **mean vector** μ = E(xt) and **autocovariance matrix** Γ(h) = E[(xt+h − μ)(xt − μ)'] generalize the scalar case.
- **Symmetry** — Γ(−h) = Γ(h)' (transpose, not equality), reflecting that γij(h) = γji(−h).
- **Sample autocovariance matrix** Γ̂(h) = (1/n) Σ (xt+h − x̄)(xt − x̄)'.
- **Multidimensional series** xs indexed by spatial coordinates s = (s1, …, sr) rather than time alone; example is a 64×36 grid of soil temperature measurements.
- **Multidimensional autocovariance** γ(h) = E[(xs+h − μ)(xs − μ)] depends on the lag vector h; estimator γ̂(h) averages over a uniform grid; ρ̂(h) = γ̂(h)/γ̂(0).
- **Variogram** 2Vx(h) = var(xs+h − xs) and its sample form 2V̂x(h) = (1/N(h)) Σ (xs+h − xs)² — used when observations are irregularly spaced (geostatistics; Journel & Huijbregts, Cressie); covariance estimators on irregular grids face indexing and non-negative-definiteness difficulties.
