# Ch 3: ARIMA Models

## Table of Contents

- [1. AR, MA, and ARMA Models](#1-ar-ma-and-arma-models)
- [2. Causality, Invertibility, and Parameter Redundancy](#2-causality-invertibility-and-parameter-redundancy)
- [3. Difference Equations and the Linear-Process Form](#3-difference-equations-and-the-linear-process-form)
- [4. ACF, PACF, and Order Identification](#4-acf-pacf-and-order-identification)
- [5. Forecasting](#5-forecasting)
- [6. Estimation](#6-estimation)
- [7. Integrated Models for Nonstationary Data](#7-integrated-models-for-nonstationary-data)
- [8. The Box-Jenkins Model-Building Procedure](#8-the-box-jenkins-model-building-procedure)
- [9. Regression with Autocorrelated Errors](#9-regression-with-autocorrelated-errors)
- [10. Multiplicative Seasonal ARIMA (SARIMA) Models](#10-multiplicative-seasonal-arima-sarima-models)

## 1. AR, MA, and ARMA Models

- **Autoregressive AR(p)** — xt = φ1 xt−1 + … + φp xt−p + wt with wt ~ wn(0, σw²); current value is a linear function of p past values plus white-noise innovation. In operator form, φ(B) xt = wt with φ(B) = 1 − φ1 B − … − φp Bp.
- **Moving average MA(q)** — xt = wt + θ1 wt−1 + … + θq wt−q; current value is a linear combination of the last q innovations. In operator form, xt = θ(B) wt with θ(B) = 1 + θ1 B + … + θq Bq. Stationary for *any* parameter values, unlike AR.
- **ARMA(p, q)** — combines both: φ(B) xt = θ(B) wt. The compact form makes it possible to read off properties of the process from the polynomials φ(z) and θ(z) treated as polynomials in a complex z (the backshift operator B is treated like a complex number).
- **AR(1) prototypes** — φ = .9 produces a smooth sample path; φ = −.9 produces a choppy alternating path. ACF of AR(1) is ρ(h) = φh.
- **MA(1) prototype** — ρ(1) = θ/(1 + θ²), with |ρ(1)| ≤ 1/2 always; ρ(h) = 0 for h > 1. The cutoff at lag q is the signature of MA(q).

## 2. Causality, Invertibility, and Parameter Redundancy

- **Three pathologies** of the raw ARMA(p, q) definition the chapter must rule out: (i) parameter redundancy, (ii) stationary AR models that depend on the future ("explosive" with |φ| > 1), and (iii) MA models with non-unique parameterizations.
- **Causal** — xt admits a one-sided linear-process form xt = Σ ψj wt−j with ψj absolutely summable; equivalently, all roots of φ(z) lie *outside* the unit circle (|z| > 1). Only causal models are useful for forecasting.
- **Invertible** — xt admits an infinite AR representation Σ πj xt−j = wt with πj absolutely summable; equivalently, all roots of θ(z) lie outside the unit circle. Picks the unique MA representation: e.g., MA(1) pairs (σw² = 1, θ = 5) and (σw² = 25, θ = 1/5) give the same ACF, and only the second is invertible.
- **Every explosion has a cause** — an explosive AR(1) (|φ| > 1) is stochastically equivalent to a causal AR(1) with reciprocal parameter 1/φ and rescaled noise variance, so excluding explosive models loses nothing.
- **Causal region for AR(2)** — φ1 + φ2 < 1, φ2 − φ1 < 1, |φ2| < 1; a triangular region in (φ1, φ2)-space, with real roots above φ2 = −φ1²/4 and complex roots below.
- **Parameter redundancy** — multiplying both sides of φ(B) xt = θ(B) wt by a common operator η(B) leaves dynamics unchanged but inflates parameter count; e.g., white noise xt = wt rewritten as (1 − .5B) xt = (1 − .5B) wt looks like an ARMA(1,1). The author requires φ(z) and θ(z) to share no common factors. Fitting an ARMA(1,1) to 150 iid normals returned φ̂ = −.96, θ̂ = .95, both "significant" — illustrating the danger.

## 3. Difference Equations and the Linear-Process Form

- **Why difference equations** — ACFs and ψ-weights of ARMA processes satisfy homogeneous linear recurrences whose general solution is determined by the roots of the AR polynomial.
- **General solution** — for the order-p homogeneous equation un − α1 un−1 − … − αp un−p = 0 with associated polynomial α(z) having roots z1, …, zr of multiplicities m1, …, mr, the solution is un = Σ zj−n Pj(n) where Pj is a polynomial in n of degree mj − 1. Initial conditions pin down the polynomial coefficients.
- **ψ-weights from matching coefficients** — for causal ARMA, ψ(z) = θ(z) / φ(z); equating coefficients in φ(z)ψ(z) = θ(z) gives a homogeneous recurrence in ψj that can be solved using the AR roots. For ARMA(1,1) xt = .9xt−1 + .5wt−1 + wt, ψj = 1.4(.9)j−1 for j ≥ 1.
- **Complex roots ⇒ pseudo-cyclic behavior** — when roots of φ(z) are complex conjugates z1 = |z1| eiθ, the ACF decays as ρ(h) = a |z1|−h cos(hθ + b). Example: AR(2) xt = 1.5xt−1 − .75xt−2 + wt has roots 1 ± i/√3, giving pseudo-period 2π/arg(z1) = 12 time points; the simulated path visibly cycles every 12 steps.

## 4. ACF, PACF, and Order Identification

- **ACF cutoffs and tails** — for MA(q) the ACF is exactly zero for h > q (cuts off), giving a clean read on the order. For AR(p) and ARMA(p, q), the ACF tails off (decays) and cannot reveal p directly.
- **Partial autocorrelation function (PACF)** — φhh = corr(xt+h − x̂t+h, xt − x̂t), where x̂t+h and x̂t are the regressions on the intermediate values {xt+1, …, xt+h−1}; measures correlation between xt+h and xt with the linear effect of everything in between removed.
- **PACF cutoffs and tails** — for AR(p) the PACF is exactly zero for h > p (cuts off, with φpp = φp), and for invertible MA(q) it tails off. So ACF and PACF play symmetric roles for the two model classes.

| | AR(p) | MA(q) | ARMA(p, q) |
|---|---|---|---|
| ACF | tails off | cuts off after lag q | tails off |
| PACF | cuts off after lag p | tails off | tails off |

- **Recruitment series identification** — sample ACF cycles at ~12-month period; sample PACF has large values at h = 1, 2 then drops to zero. Suggests AR(2); OLS regression gives x̂t = 6.74 + 1.35 xt−1 − .46 xt−2 with σ̂w² = 89.72.

## 5. Forecasting

- **MMSE forecast** — minimum mean square error predictor is xn+m^n = E(xn+m | x1:n); under Gaussian assumption it equals the **best linear predictor (BLP)** (Theorem B.3). BLPs use only the second-order moments of the process.
- **Prediction equations** — Property 3.3: BLP coefficients α0, …, αn for xn+m^n are characterized by E[(xn+m − xn+m^n) xk] = 0 for k = 0, 1, …, n. In matrix form Γn φn = γn for one-step-ahead prediction.
- **AR(p) forecast collapses** — once n ≥ p, the BLP is xn+1^n = φ1 xn + … + φp xn−p+1; the coefficients are simply the AR parameters, no matrix inversion.
- **Durbin-Levinson algorithm** — recursive solution to the prediction equations that avoids matrix inversion; iteratively builds φnn (which equals the PACF at lag n) and Pn+1^n = γ(0) ∏ (1 − φjj²).
- **Innovations algorithm** — alternative recursion (Brockwell-Davis) using uncorrelated innovations xt − xt^t−1; particularly clean for MA processes.
- **Truncated ARMA forecast** (Property 3.7) — practical recursion x̃n+m^n = φ1 x̃n+m−1^n + … + φp x̃n+m−p^n + θ1 w̃n+m−1^n + … + θq w̃n+m−q^n, with x̃t^n = xt for 1 ≤ t ≤ n and zero otherwise; w̃t^n iterated forward from w̃0^n = 0.
- **Long-range behavior** — ARMA forecasts converge exponentially to the mean μx as m → ∞, and the prediction error converges to the marginal variance σx². The Recruitment 24-month forecast (Example 3.25) levels off rapidly with wide intervals.
- **Mean-square prediction error** — Pn+m^n = σw² Σj=0..m−1 ψj²; grows with horizon and saturates at γx(0).
- **Backcasting** — predicting x1−m from x1:n; for stationary Gaussian processes, backward and forward prediction problems are equivalent (just reverse the data, fit, predict).

## 6. Estimation

- **Yule-Walker for AR(p)** — equations γ(h) = φ1 γ(h−1) + … + φp γ(h−p) for h = 1, …, p plus σw² = γ(0) − φ′γp; replace γ by sample estimates to get φ̂ = R̂p−1 ρ̂p, σ̂w² = γ̂(0)(1 − ρ̂p′ R̂p−1 ρ̂p). For AR(p), Yule-Walker estimators are asymptotically optimal: √n (φ̂ − φ) → N(0, σw² Γp−1).
- **Method of moments fails for MA/ARMA** — for MA(1), solving ρ̂(1) = θ̂/(1 + θ̂²) gives an estimator with asymptotic variance ~3.5× that of the MLE at θ = .5; nonlinear in parameters means moment matching is suboptimal.
- **Conditional vs. unconditional likelihood** — for an AR(1), the unconditional sum of squares S(μ, φ) = (1−φ²)(x1−μ)² + Σ[(xt−μ) − φ(xt−1−μ)]²; conditioning on x1 drops the leading term and makes the problem linear in (α, φ) where α = μ(1−φ). Conditional LS, unconditional LS, Yule-Walker, and MLE all coincide asymptotically.
- **Innovations form of the likelihood** — for ARMA, write L in terms of one-step prediction errors xt − xt^t−1 and their variances Pt^t−1 = σw² rt; concentrated likelihood l(β) = log(n−1 S(β)) + n−1 Σ log rt(β) is minimized numerically.
- **Newton-Raphson and scoring** — standard numerical optimizers; Newton-Raphson uses the observed Hessian, scoring uses the information matrix (its expectation). Inverse of the information matrix gives asymptotic variance.
- **Gauss-Newton for ARMA** — linearize wt(β) around an initial estimate β(0) and iterate β(j+1) = β(j) + Δ(β(j)) until convergence. Glacial varves example: ∇log(varve) modeled as MA(1); 11 Gauss-Newton iterations starting from method-of-moments θ(0) = −.495 converge to θ̂ = −.773 with σ̂w² = .236.
- **Property 3.10** — under regularity, MLE, conditional LS, and unconditional LS all give √n(β̂ − β) → N(0, σw² Γp,q−1) for causal/invertible ARMA. Specific cases: AR(1) gives var(φ̂) ≈ (1 − φ²)/n; MA(1) gives var(θ̂) ≈ (1 − θ²)/n — the same form, because in both cases an AR-type "regressor" governs asymptotic variance.
- **Overfitting caveat** — fitting AR(2) to true AR(1) data inflates var(φ̂1) from (1 − φ1²)/n to 1/n, hurting precision. Used as a diagnostic: adding parameters should not change a satisfactory fit.
- **Bootstrap** — when n is small or parameters are near a boundary, the asymptotic normal approximation fails; resample sample innovations, regenerate paths, refit. Demonstrated on AR(1) with φ = .95 and Laplace errors where the empirical sampling distribution of φ̂ is highly skewed and unlike the normal approximation.

## 7. Integrated Models for Nonstationary Data

- **ARIMA(p, d, q)** — defined by φ(B)(1−B)d xt = θ(B) wt; the d-th difference ∇d xt = (1−B)d xt is a stationary causal/invertible ARMA(p, q). Captures stochastic trends that detrending cannot.
- **Why differencing handles trends** — if μt = β0 + β1 t + … + βq tq is a polynomial trend, ∇k yt is stationary for k ≥ q. Stochastic trends (random walks) also collapse under differencing.
- **Random walk with drift** as ARIMA(0, 1, 0) with constant — m-step forecast xn+m^n = mδ + xn (a straight line), prediction error mσw² grows without bound, unlike the bounded ARMA case.
- **IMA(1,1) and EWMA** — model xt = xt−1 + wt − λwt−1 yields the **exponentially weighted moving average** forecast x̃n+1^n = (1−λ)xn + λ x̃n^n−1, a convex combination of last observation and last forecast. Often used and abused in business forecasting because practitioners pick λ arbitrarily without verifying the IMA(1,1) structure.

## 8. The Box-Jenkins Model-Building Procedure

- **Six steps** — plot the data; transform if needed (log for variance scaling, Box-Cox); identify p, d, q; estimate parameters; check diagnostics; choose among candidate models.
- **Differencing decision** — slow decay of sample ACF signals a unit root (need to difference). Avoid overdifferencing: ∇wt = wt − wt−1 is MA(1), so differencing white noise *creates* spurious dependence.
- **GNP example (Example 3.39)** — quarterly U.S. GNP 1947-2002. Strong trend in raw series; growth rate xt = ∇log(yt) is stable. ACF of the growth rate could be read as cutting off at lag 2 (MA(2) for growth, ARIMA(0,1,2) for log GNP) or as tailing off with PACF cutting off at lag 1 (AR(1) for growth, ARIMA(1,1,0) for log GNP). Both fits are nearly equivalent: the AR(1) implies xt ≈ .35 wt−1 + .12 wt−2 + wt, matching the MA(2) coefficients .303 and .204.
- **Diagnostics on standardized residuals** — should look like iid mean-zero unit-variance: time plot inspection, ACF check against ±2/√n bounds, Q-Q plot for normality.
- **Ljung-Box-Pierce Q-statistic** — Q = n(n+2) Σh=1..H ρ̂e²(h)/(n−h); under model adequacy Q ~ χ²H−p−q. Tests collective magnitude of residual autocorrelations rather than individual lags. Typically H = 20.
- **Glacial varves revisited** — initial ARIMA(0,1,1) fit leaves significant Q-statistics; adding an AR(1) term to give ARIMA(1,1,1) with φ̂ = .23, θ̂ = −.89 yields clean diagnostics.
- **Overfitting illustrated** — U.S. census 1910-1990 (9 points) fit with an 8th-degree polynomial: perfect fit but predicts U.S. population near zero in year 2000.
- **Model choice via AIC, AICc, BIC** — for the GNP growth rate, AIC and AICc slightly prefer MA(2), BIC prefers the simpler AR(1); BIC tends to choose smaller-order models. Either is defensible; pure AR is often retained for ease of use.

## 9. Regression with Autocorrelated Errors

- **Setup** — yt = Σ βj ztj + xt with xt a stationary process (not necessarily white). OLS standard errors are wrong; weighted least squares or transformed regression is needed.
- **AR-error transformation** — if φ(B) xt = wt, multiply the regression equation by φ(B); transformed series yt* = φ(B) yt and ztj* = φ(B) ztj satisfy a white-noise-error linear model with the *same* β. Generalizes to ARMA errors via π(B) = θ(B)−1 φ(B).
- **Cochrane-Orcutt-style procedure** — (i) OLS regression, retain residuals x̂t; (ii) identify ARMA model for x̂t from sample ACF/PACF; (iii) refit by weighted LS or MLE with the chosen error model; (iv) check residuals for whiteness, iterate if needed.
- **LA mortality example revisited** — Mt regressed on time, centered temperature, temperature², and particulates; OLS residuals show AR(2) structure, and refitting with AR(2) errors gives coefficients comparable to OLS but with corrected standard errors.

## 10. Multiplicative Seasonal ARIMA (SARIMA) Models

- **Pure seasonal ARMA(P, Q)s** — ΦP(Bs) xt = ΘQ(Bs) wt with operators in Bs only (lags at the seasonal period). Causal iff roots of ΦP(zs) lie outside the unit circle, invertible iff roots of ΘQ(zs) do; ACF/PACF have nonzero values *only* at multiples of s.
- **Multiplicative SARIMA** — ARIMA(p, d, q) × (P, D, Q)s defined by ΦP(Bs) φ(B) ∇sD ∇d xt = δ + ΘQ(Bs) θ(B) wt; the product structure forces the cross-lag coefficient (e.g., wt−13 in an (0,1,1)×(0,1,1)12 model) to be the *product* of the seasonal and nonseasonal coefficients rather than a free parameter, parsimoniously capturing seasonal and within-season dynamics.
- **Seasonal differencing** — ∇sD = (1 − Bs)D; D = 1 typically suffices when the sample ACF decays slowly at multiples of s but not in between, indicating seasonal persistence (e.g., each January resembles each other January).
- **Identification table for pure seasonal**:

| | AR(P)s | MA(Q)s | ARMA(P, Q)s |
|---|---|---|---|
| ACF | tails off at lags ks | cuts off after lag Qs | tails off at lags ks |
| PACF | cuts off after lag Ps | tails off at lags ks | tails off at lags ks |

- **Air Passengers (Box-Jenkins canonical example)** — monthly international airline totals 1949-1960. log stabilizes variance; ∇log removes trend; ∇12 ∇log removes residual seasonality. Sample ACF of ∇12 ∇log xt cuts off at lag 1s (s = 12) in the seasonal direction, suggesting SMA(1) at season 12; nonseasonal lags both tail off, suggesting ARMA(1,1) within seasons. Initial ARIMA(1,1,1)×(0,1,1)12 fit has insignificant AR; final model ARIMA(0,1,1)×(0,1,1)12 wins on AIC/AICc/BIC and produces clean residuals plus a clean 12-month forecast.
