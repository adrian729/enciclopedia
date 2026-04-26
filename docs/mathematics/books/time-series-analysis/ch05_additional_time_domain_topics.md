# Ch 5: Additional Time Domain Topics

## Table of Contents

- [1. Long Memory and Fractional Differencing](#1-long-memory-and-fractional-differencing)
- [2. Unit Root Testing](#2-unit-root-testing)
- [3. Volatility Modeling: ARCH and GARCH](#3-volatility-modeling-arch-and-garch)
- [4. Threshold Models for Nonlinear Series](#4-threshold-models-for-nonlinear-series)
- [5. Lagged Regression and Transfer Functions](#5-lagged-regression-and-transfer-functions)
- [6. Multivariate Models: VAR, VARMA, and ARMAX](#6-multivariate-models-var-varma-and-armax)

## 1. Long Memory and Fractional Differencing

- **Short vs. long memory** — ARMA(p, q) is "short memory" because its ψ-coefficients decay exponentially and ρ(h) → 0 quickly; **long memory** (or persistent) series have sample ACFs that are not necessarily large but persist over many lags. The log-transformed glacial varve series shows the textbook pattern: ACF still nonzero at lag 100.
- **Fractional differencing** — extends (1 − B)^d to fractional d via the binomial expansion (1 − B)^d x_t = w_t with coefficients π_j = Γ(j − d) / [Γ(j+1)Γ(−d)]; for |d| < 0.5 the process is stationary. Long memory corresponds to 0 < d < 0.5; **antipersistent** to negative d. Plain Box–Jenkins differencing is the special case d = 1.
- **ARFIMA(p, d, q)** — fractionally integrated ARMA, φ(B)∇^d (x_t − μ) = θ(B)w_t with −0.5 < d < 0.5; combines long-memory persistence with short-memory ARMA structure when both are present.
- **Long-memory ACF and spectrum** — ρ(h) ∼ h^(2d−1), so Σ |ρ(h)| = ∞ for 0 < d < 0.5 (hence the name); the spectrum f_x(ω) = [4 sin²(πω)]^(−d) σ_w² blows up as ω → 0, contrasting with the finite spectral peak of an AR fit.
- **Estimation of d** — Gauss–Newton time-domain MLE on the truncated representation w_t(d) = Σ π_j(d) x_{t−j}; alternatively the **Whittle approximation** maximizes a periodogram-based likelihood over d ∈ (0, 0.5); the **Geweke–Porter-Hudak (GPH)** regression of log I(ω_k) on log[4 sin²(πω_k)] near ω = 0 gives an approximate slope estimate of −d.
- **Varves example** — fitting (1 − B)^d x_t = w_t to mean-adjusted log(varve) yields d̂ = 0.384 (time domain), d̂ = 0.380 with SE 0.028 (Whittle), d̂ = 0.383 (GPH); residual ACFs match those from the ARIMA(1, 1, 1) fit, suggesting long memory rather than overdifferencing.

## 2. Unit Root Testing

- **Why test** — first differencing a causal AR(1), x_t = φ x_{t−1} + w_t with |φ| < 1, produces a noninvertible ARMA(1, 1) and introduces extraneous correlation; differencing only makes sense when the series truly has a unit root.
- **Dickey–Fuller statistic** — under H₀: φ = 1 (random walk), n(φ̂ − 1) →d (½ χ₁² − 1) / ∫₀¹ W²(t) dt, where W(t) is standard Brownian motion; the limit has no closed form, so quantiles come from simulation. Test H₀: φ = 1 versus H₁: |φ| < 1.
- **Augmented Dickey–Fuller (ADF)** — for AR(p) the regression is rewritten as ∇x_t = γ x_{t−1} + Σ ψ_j ∇x_{t−j} + w_t; testing H₀: γ = 0 via a Wald statistic on γ̂/se(γ̂) extends the unit root test to autocorrelated errors. Choice of lag p is crucial; default rule is p = ⌊(n − 1)^{1/3}⌋.
- **Phillips–Perron (PP) test** — alternative correction for serial correlation and heteroscedasticity in the errors; differs from ADF mainly in how nuisance correlation is handled.
- **With drift or trend** — extension x_t = β₀ + β₁ t + φ x_{t−1} + w_t lets one test random-walk-with-drift vs. trend-stationary alternatives (e.g., the chicken price series).
- **Varves example** — DF, ADF, and PP tests on log(varve) all reject the unit root null (p < 0.05), supporting the long-memory interpretation over an integrated one.

## 3. Volatility Modeling: ARCH and GARCH

- **Returns** — for asset value x_t, the return r_t = (x_t − x_{t−1})/x_{t−1}; for small returns ∇log(x_t) ≈ r_t and is often used as a proxy. Financial returns typically show **volatility clustering**: stable periods punctuated by bursts (DJIA daily returns 2006–2016).
- **ARCH(1)** — Engle (1982) models r_t = σ_t ε_t with σ_t² = α₀ + α₁ r_{t−1}², ε_t ∼ iid N(0, 1); the conditional variance depends on the previous squared return. Equivalent representation r_t² = α₀ + α₁ r_{t−1}² + v_t makes the squared returns a non-Gaussian AR(1) with v_t = σ_t²(ε_t² − 1).
- **ARCH(1) properties** — r_t is a martingale difference (uncorrelated, mean-zero); E(r_t²) = α₀/(1 − α₁) for 0 ≤ α₁ < 1; finite fourth moment requires α₁ < 1/√3 ≈ 0.58; the marginal distribution is **leptokurtic** (kurtosis ≥ 3, "fat tails").
- **GARCH(p, q)** — Bollerslev (1986) generalizes by adding lagged variance terms: σ_t² = α₀ + Σ α_j r_{t−j}² + Σ β_j σ_{t−j}². The squared series r_t² then follows a non-Gaussian ARMA when α₁ + β₁ < 1.
- **GARCH variants** — **APARCH** (asymmetric power) σ_t^δ = α₀ + Σ α_j (|r_{t−j}| − γ_j r_{t−j})^δ + Σ β_j σ_{t−j}^δ captures the leverage effect (negative shocks moving volatility more than positive); **IGARCH** sets α₁ + β₁ = 1 to model persistent volatility.
- **DJIA example** — AR(1)-GARCH(1, 1) with t-errors fits DJIA returns: α̂₁ = 0.124, β̂₁ = 0.870 (so α₁ + β₁ ≈ 0.99, near IGARCH); one-step-ahead σ̂_t spikes during the 2008 financial crisis.
- **GNP example** — AR(1)-ARCH(1) on diff(log(gnp)) gives α̂₁ = 0.194 (significant), confirming mild conditional heteroscedasticity in U.S. GNP residuals.
- **Drawbacks of GARCH** — symmetric response to positive and negative shocks (fixed by APARCH), tight parameter constraints, flat likelihood unless n is large, slow response to large isolated returns; **stochastic volatility** models (Ch 6) add a noise term to log σ_t² to address the deterministic-conditional-variance assumption.

## 4. Threshold Models for Nonlinear Series

- **Time reversibility limitation** — stationary Gaussian series have identical forward and backward distributions; many real series do not. Monthly U.S. pneumonia/influenza deaths (1968–1978) rise faster than they fall during epidemics, with peaks shifting between January, February, and March, behavior that seasonal ARMA cannot capture.
- **Self-exciting threshold ARMA (SETARMA)** — Tong (1983, 1990): k regimes, each with its own ARMA dynamics, switched by comparing x_{t−d} to fixed thresholds r₁ < … < r_{k−1}. The delay d and partition are part of the specification; each different ARMA model is called a **regime**.
- **TAR appeal** — relatively simple to specify, estimate, and interpret compared with other nonlinear models, yet flexible enough to reproduce many nonlinear phenomena. Generalizations replace the self-exciting variable with an exogenous one (e.g., Snowshoe Hare population driving the Canadian lynx series).
- **Flu mortality TAR fit** — applied to first differences x_t = flu_t − flu_{t−1}, two regimes split at threshold x_{t−1} = 0.05, both order p = 4. The "above-threshold" regime has large negative coefficients (e.g., φ̂₄ = −6.71) capturing the epidemic crash; one-step-ahead predictions track epidemic peaks well except for 1976.

## 5. Lagged Regression and Transfer Functions

- **Transfer function model** — y_t = α(B) x_t + η_t with α(B) = Σ α_j B^j and α_j coefficients summable; input x_t and noise η_t are stationary and mutually independent. Box–Jenkins propose a parsimonious rational form α(B) = δ(B) B^d / ω(B), a small number of coefficients plus a delay d.
- **Prewhitening** — fit an ARMA model to x_t to get white residuals w_t; apply the same operator to y_t to get ỹ_t. Then γ_{ỹw}(h) = σ_w² α_h, so the cross-correlation of prewhitened input with transformed output directly estimates the α_h sequence.
- **SOI / Recruitment example** — detrended SOI fits AR(1) with φ̂ = 0.588; CCF of prewhitened SOI with filtered Recruitment peaks at lag −5 with subsequent decay, suggesting α(B) = δ₀ B⁵ / (1 − ω₁ B). Final fit y_t = 12 + 0.8 y_{t−1} − 21 x_{t−5} + u_t with u_t = 0.45 u_{t−1} + w_t matches the frequency-domain coherency analysis.
- **Sequential Box–Jenkins fitting** — (i) fit ARMA to input x_t; (ii) apply that operator to y_t to get ỹ_t; (iii) use CCF(ỹ_t, ŵ_t) to identify δ(B), ω(B), and d; (iv) regress on lagged inputs/outputs for β̂; (v) fit ARMA to the resulting noise residuals. Procedure is reasonable but not optimal; simultaneous least squares is also possible.

## 6. Multivariate Models: VAR, VARMA, and ARMAX

- **Multivariate regression** — vector y_t = B z_t + w_t with cov(w_t) = Σ_w (k × k); MLE B̂ = (Σ y_t z_t')(Σ z_t z_t')⁻¹, Σ̂_w = (n − r)⁻¹ Σ (y_t − B̂ z_t)(y_t − B̂ z_t)'; multivariate AIC adds a kr + k(k+1)/2 penalty, BIC replaces the second term with K ln n / n.
- **Vector autoregression (VAR(p))** — x_t = α + Σ Φ_j x_{t−j} + w_t; reduces to multivariate regression with z_t = (1, x_{t−1}', …, x_{t−p}')'. Yule–Walker equations Γ(h) = Σ Φ_j Γ(h − j) generalize directly. Property 5.1: √n (φ̂ − φ) is asymptotically normal with covariance Σ_w ⊗ Γ_pp⁻¹.
- **Vector ARMAX** — adds an exogenous r × 1 input vector u_t via a Γ u_t term; replaces the constant α and lets dynamics of the system depend on external regressors.
- **Pollution-mortality VAR example** — three-variable system (cardiovascular mortality M_t, temperature T_t, particulates P_t); BIC selects p = 2, AIC and FPE pick p = 9, Hannan–Quinn picks p = 5. VAR(2) prediction equation M̂_t = 56 − 0.01 t + 0.3 M_{t−1} − 0.2 T_{t−1} + 0.04 P_{t−1} + 0.28 M_{t−2} − 0.08 T_{t−2} + 0.07 P_{t−2}; residual Q-test rejects whiteness because zero-lag cross-correlations of M with T (0.22) and P (0.28) remain.
- **VARMA(p, q)** — Φ(B) x_t = Θ(B) w_t with k × k matrix operators; **causal** when roots of |Φ(z)| lie outside |z| ≤ 1; **invertible** when roots of |Θ(z)| do.
- **Identifiability problem** — unlike the univariate case, two VARMA models can be **observationally equivalent** when related by a **unimodular** operator U(B) (one whose determinant is constant). Identifiability requires (i) Φ(B) and Θ(B) share no common left factor other than unimodular ones and (ii) [Φ_p, Θ_q] has full rank k with p, q minimal. Practical advice: prefer pure VAR(p), or recast VARMA estimation as a state-space problem (Ch 6).
- **Spliid algorithm** — quick iterative VARMA fitter (Spliid 1983): treat lagged shocks as observed regressors, run multivariate regression, recompute residuals, re-iterate; converges fast but not to the MLE. Applied via R package marima to the mortality–pollution data, fitting a VARMA(2, 1) for one-step-ahead predictions of cardiovascular mortality.
