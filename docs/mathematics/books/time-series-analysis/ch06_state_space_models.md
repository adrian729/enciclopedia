# Ch 6: State Space Models

## Table of Contents

- [1. The Linear Gaussian State Space Model](#1-the-linear-gaussian-state-space-model)
- [2. Kalman Filter, Smoother, and Forecasting](#2-kalman-filter-smoother-and-forecasting)
- [3. Maximum Likelihood Estimation](#3-maximum-likelihood-estimation)
- [4. Missing Data and Irregular Observation](#4-missing-data-and-irregular-observation)
- [5. Structural Models and Signal Extraction](#5-structural-models-and-signal-extraction)
- [6. ARMAX and Regression with Autocorrelated Errors](#6-armax-and-regression-with-autocorrelated-errors)
- [7. Bootstrap and Smoothing Splines](#7-bootstrap-and-smoothing-splines)
- [8. Discrete States: Hidden Markov Models](#8-discrete-states-hidden-markov-models)
- [9. Switching Dynamic Linear Models](#9-switching-dynamic-linear-models)
- [10. Stochastic Volatility](#10-stochastic-volatility)
- [11. Bayesian Analysis via MCMC](#11-bayesian-analysis-via-mcmc)

## 1. The Linear Gaussian State Space Model

- **Two-equation form** — a hidden **state equation** xt = Φxt−1 + Υut + wt drives a Markov state, observed through an **observation equation** yt = At xt + Γut + vt; wt ~ iid Np(0, Q), vt ~ iid Nq(0, R), x0 ~ N(µ0, Σ0). Originated in Kalman (1960) for spacecraft tracking.
- **Two defining principles** — the state xt is Markovian (future and past independent given present), and observations yt are conditionally independent given the states; all serial dependence in y flows through x.
- **Generality** — VAR(p) models embed by stacking lagged states; ARMA, ARMAX, structural decompositions, regression with autocorrelated errors, and HMMs all fit the framework with appropriate choices of Φ and At.
- **Biomedical monitoring example** — three blood markers (log WBC, log PLT, HCT) measured for 91 days post bone-marrow transplant with ~40% missing; modeled as a 3-dim VAR(1) state with At equal to identity on observed days and zero on missing days.
- **AR(1) plus noise example** — yt = xt + vt with xt = φxt−1 + wt produces observations whose ACF mimics ARMA(1,1); illustrates that noisy observation of a simple state can yield richer marginal dynamics than the state itself.

## 2. Kalman Filter, Smoother, and Forecasting

- **Three estimation regimes by horizon s vs. t** — *forecasting* (s < t), *filtering* (s = t), *smoothing* (s > t); xts = E(xt | y1:s) and Pts is the corresponding error covariance.
- **Kalman filter (Property 6.1)** — recursive update from xt−1t−1 to xtt: compute one-step prediction xtt−1 = Φxt−1t−1 + Υut, prediction covariance Ptt−1 = ΦPt−1t−1Φ' + Q, then correct with **innovation** εt = yt − At xtt−1 − Γut weighted by **Kalman gain** Kt = Ptt−1 At'(At Ptt−1 At' + R)⁻¹. No need to reprocess the full data set when a new yt arrives.
- **Innovations** — εt are zero-mean independent Gaussian with covariance Σt = At Ptt−1 At' + R; they form the basis of the likelihood and the bootstrap.
- **Kalman smoother / RTS smoother (Property 6.2)** — backward recursion using Jt−1 = Pt−1t−1 Φ'(Ptt−1)⁻¹: xt−1n = xt−1t−1 + Jt−1(xtn − xtt−1); each smoothed estimate uses past, present, and future, so Ptt−1 ≥ Ptt ≥ Ptn (smoother is most precise).
- **Lag-one covariance smoother (Property 6.3)** — recursion for Pt,t−1n needed by the EM algorithm to evaluate cross-time second moments under the smoother.
- **Local level model** — yt = µt + vt with µt = µt−1 + wt; closed-form filter recovers Property 6.1 and is the canonical illustration of "completing the square" derivation.
- **Steady state** — when eigenvalues of Φ are inside the unit circle, Ptt converges to P solving the Riccati equation P = Φ[P − PA'(APA' + R)⁻¹AP]Φ' + Q; gain Kt → K and innovation covariance Σt → Σ stabilize, justifying asymptotic theory.

## 3. Maximum Likelihood Estimation

- **Innovations form of the Gaussian likelihood** — −2 ln LY(Θ) = Σ ln |Σt(Θ)| + Σ εt(Θ)' Σt(Θ)⁻¹ εt(Θ); evaluated by running the Kalman filter once at each parameter value.
- **Newton–Raphson / BFGS** — direct numerical optimization of the innovations likelihood; standard errors from the Hessian. Demonstrated on the AR(1)+noise example (φ̂ = .81, σ̂w = .85, σ̂v = .87) and on the global temperature signal (drift δ̂ ≈ .006 °C/yr).
- **EM algorithm (Baum–Welch)** — alternates Kalman smoother (E-step computing S00, S10, S11) with closed-form multivariate-normal MLE updates Φ = S10 S00⁻¹, Q = n⁻¹(S11 − S10 S00⁻¹ S10'), R = n⁻¹ Σ[(yt − At xtn)(yt − At xtn)' + At Ptn At']. Conceptually simpler but slower convergence than Newton–Raphson.
- **Asymptotic distribution (Property 6.4)** — under filter stability, √n(Θ̂n − Θ0) → N(0, I(Θ0)⁻¹); the Hessian at convergence estimates n I(Θ0).
- **Global temperature signal extraction** — two series globtemp (land–ocean) and globtempl (land only) modeled as yt1 = xt + vt1, yt2 = xt + vt2 with shared random-walk-with-drift signal xt = δ + xt−1 + wt; smoothed x̂tn extracts the common climatic signal with two-RMSE bands.

## 4. Missing Data and Irregular Observation

- **Time-varying observation dimension** — partition yt into observed yt(1) and unobserved yt(2); the filter still applies to the q1t-dimensional observed equation, with Kt set to zero when yt is fully missing (so xtt = xtt−1).
- **Zero-padding device** — replace missing components by zero, replace corresponding rows of At by zero, and replace the missing block of R by an identity (Stoffer 1982); keeps observation dimension fixed at q while preserving the correct innovations likelihood.
- **EM with missing data** — extra terms in the M-step handle E∗(yt(2) | y1:n(1)) and the corresponding cross-product; in the uncorrelated-errors case the missing M-step looks structurally like the complete-data updates with smoothers replaced by missing-data smoothers xt(n), Pt(n), Pt,t−1(n).
- **Biomedical longitudinal data** — fitted via EM to the three blood markers; estimated transition shows weak coupling between WBC and PLT but strong dependence x̂t3 = −1.495 xt−1,1 + 2.289 xt−1,2 + .794 xt−1,3 of HCT on the other two; smoothed trajectories provide imputations for the missing 40%.

## 5. Structural Models and Signal Extraction

- **Structural model** — decompose yt into trend, seasonal, and irregular components, each given its own state subequation with direct interpretation. Fits naturally into the state-space framework via block-diagonal Φ and a row-selector At.
- **J&J quarterly earnings example** — yt = Tt + St + vt with exponentially growing trend Tt = φ Tt−1 + wt1 (φ > 1) and seasonal constraint St + St−1 + St−2 + St−3 = wt2; state vector xt = (Tt, St, St−1, St−2)'. Estimated growth φ̂ = 1.035 (3.5% per year); 12-quarter forecast extends the data with widening RMSPE bounds.
- **Forecasting** — uses the Kalman prediction equations iterated forward from xnn, Pnn; standard errors come from At Pt+ht At' + R.
- **Signal extraction** — smoothing recovers the unobserved components (e.g., separated trend and seasonal of J&J); same machinery as Kalman smoother applied component-wise via the structural state vector.

## 6. ARMAX and Regression with Autocorrelated Errors

- **Correlated-error formulation** — write xt+1 = Φxt + Υut+1 + Θwt and yt = At xt + Γut + vt with cov(ws, vt) = S δst; the matrix Θ avoids singular state covariances and ARMAX-style noise. Property 6.5 gives the modified filter with gain Kt = (Φ Ptt−1 At' + Θ S)(At Ptt−1 At' + R)⁻¹.
- **ARMAX in state-space form (Property 6.6)** — for yt = Υut + Σ Φj yt−j + Σ Θk vt−k + vt, build companion matrices F, G, H so xt+1 = F xt + H ut+1 + G vt and yt = A xt + vt; inputs enter the state equation.
- **Regression with autocorrelated errors** — for yt = Γut + εt with vector ARMA(p,q) errors, set H = 0 and place Γut in the observation equation; inputs enter the observation equation rather than the state.
- **Mortality example combining both** — detrended cardiovascular mortality M̃t = φ1 M̃t−1 + φ2 M̃t−2 + β1 Tt−1 + β2 Pt + β3 Pt−4 + vt with M̃t = Mt − (α + β4 t); a quick two-stage fit (lm + sarima) gives starting values for joint Newton–Raphson over all parameters using Property 6.5.

## 7. Bootstrap and Smoothing Splines

- **Why bootstrap state space models** — asymptotic SEs assume large samples and parameters away from the boundary; bootstrap exposes finite-sample skewness, multimodality, and parameter-space-boundary behavior (Stoffer & Wall 1991).
- **Algorithm** — compute MLE Θ̂; standardize innovations et = Σt⁻¹/² εt; resample {et∗} from the empirical distribution; rebuild bootstrap data via the stacked vector first-order equation ξt = Ft ξt−1 + G ut + Ht et∗; refit to get Θ̂∗; repeat B times. The empirical distribution of Θ̂∗ − Θ̂ approximates that of Θ̂ − Θ0.
- **Stochastic regression on inflation/interest** — inflation yt = α + βt zt + vt with βt as latent AR(1); B = 500 bootstraps yield SEs typically ≥ 50% larger than asymptotic, plus a bimodal distribution for σ̂w (mass at 0 and at .25) revealing that the data are best described by a fixed regression coefficient rather than truly stochastic.
- **Smoothing splines as a state-space model** — minimizing Σ(yt − µt)² + λ Σ(∇²µt)² is equivalent to maximum-a-posteriori state estimation under ∇²µt = wt, yt = µt + vt with smoothing parameter λ = σv²/σw²; the Kalman smoother recovers µ̂tn, and λ̂ is obtained from the variance MLEs.

## 8. Discrete States: Hidden Markov Models

- **Hidden Markov model (HMM)** — state xt is a finite-state Markov chain on {1, ..., m} with stationary distribution πj and transition probabilities πij; observation density depends on regime: pj(yt) = p(yt | xt = j). Developed in parallel to linear state-space models (Goldfeld & Quandt 1973; Lindgren 1978).
- **Forward-backward recursions (Properties 6.7, 6.8)** — *forward* filter πj(t|t) ∝ πj(t)pj(yt) updates; *backward* smoother uses ϕj(t) = p(yt+1:n | xt = j) with ϕj(n) = 1; smoother πj(t|n) and joint πij(t|n) needed for EM.
- **Likelihood and EM** — ln LY(Θ) = Σ ln(Σ πj(t|t−1) pj(yt)); Baum–Welch updates transition probabilities via π̂ij = Σ πij'(t|n) / Σ Σ πik'(t|n), and the emission parameters via standard MLE under the smoothed regime weights.
- **Viterbi algorithm** — dynamic-programming recursion for the most-likely state sequence; companion to forward-backward when point estimates of regimes are wanted rather than posterior probabilities.
- **Earthquake counts (Poisson HMM)** — annual counts 1900–2006, mean 19.4 vs. variance 51.6 (overdispersed); two-state Poisson-HMM with intensities (λ̂1, λ̂2) = (15.4, 26.0) and persistent transitions (π̂11 = .93, π̂22 = .88) explains both overdispersion and serial correlation.
- **S&P 500 weekly returns (normal HMM)** — three-state Gaussian HMM identifies regular-volatility regime, transient large-negative-return regime, and high-volatility regime, with very persistent diagonal transitions (.945, .942) and a transient middle state.
- **Switching autoregression** — yt = φ0(xt) + Σ φi(xt) yt−i + σ(xt) vt with latent Markov regime; differs from threshold AR (Section 5.4) because regime is unobserved rather than driven by an observable. Influenza mortality differenced data fit with a two-state AR(2)-HMM separates epidemic from mild seasons.

## 9. Switching Dynamic Linear Models

- **Switching DLM** — generalize HMM by combining a linear Gaussian state xt with a regime indicator At taking one of m measurement matrices {M1, ..., Mm}; only the observation matrix switches, dynamics of xt remain linear. Approach of Shumway & Stoffer (1991).
- **Filter as weighted innovations** — xtt = xtt−1 + Σ πj(t|t) Ktj εtj where εtj = yt − Mj xtt−1 and Ktj = Ptt−1 Mj' Σtj⁻¹; the filter is a probability-weighted mix over the m possible measurement matrices.
- **Computational difficulty** — exact pj(t|t−1) is a mixture over mt−1 possible histories; mitigated by Viterbi-style trimming, by Kullback–Leibler approximation to a single normal N(Mj xtt−1, Σtj), or by Kim/Shumway approximations.
- **Tracking multiple targets** — sensor vector yt observes unknown subset of target signals; possible detection configurations form the candidate set {M1, ..., Mm}.
- **Modeling economic change** — Lam (1990) extension of Hamilton (1989): yt = zt + nt with AR(2) zt and random walk nt whose drift switches between α0 and α0 + α1, capturing positive vs. negative growth periods.
- **Influenza epidemic detection** — three-component structural model (seasonal AR(2), epidemic AR(1), fixed trend) with switching observation matrix M1 = [1, 0, 0, 1] (no epidemic) vs. M2 = [1, 0, 1, 1] (epidemic); approximate Markov-chain regime probabilities with π11 = π22 = .75; one-month-ahead epidemic predictions correctly flag most peaks 1969–1978.

## 10. Stochastic Volatility

- **SV model (Taylor 1982)** — returns rt = β exp(xt/2) εt with hidden log-volatility xt = log σt² following an AR(1) xt = φ xt−1 + wt; alternative to GARCH that places volatility dynamics in a latent state rather than in past returns.
- **Linear form via squaring and logging** — yt = log rt² satisfies yt = α + xt + vt with vt = log εt² distributed as log(χ1²), highly skewed with mean −(γ + log 2) and variance π²/2; non-Gaussian so direct Kalman filtering does not apply.
- **Mixture-of-normals approximation** — Kim, Shephard & Chib (1998) approximate log(χ1²) by a fixed mixture of seven normals; Stoffer adopts a two-component mixture ηt = It zt0 + (1 − It) zt1 with Bernoulli switch, reducing the model to a switching DLM so the Section 6.10 filtering equations apply directly.
- **NYSE crash 1987 example** — ~400 daily returns around October 19, 1987; estimated φ̂1 = .988 (highly persistent volatility), one-step-ahead predicted log-volatility x̂tt−1 spikes around the crash and tracks subsequent calmer periods.
- **Bootstrap for SV** — block-diagonal vector first-order equation ξt = F ξt−1 + Gt + Ht et generalizes the Section 6.7 procedure; applied to GNP-growth-rate residuals reveals a bootstrap distribution of φ̂1 with positive skewness and kurtosis missed by the asymptotic normal.

## 11. Bayesian Analysis via MCMC

- **Goal** — sample from the posterior p(Θ, x0:n | y1:n); Gibbs sampler alternates between (i) drawing Θ | x0:n, y1:n and (ii) drawing x0:n | Θ, y1:n. The first step is easy under conjugate priors because conditioning on the states restores complete-data form.
- **Conjugate priors for Gaussian models** — normal priors on transition coefficients and inverse-gamma (IG) priors on σw², σv² yield closed-form full conditionals: φ | σw, x0:n ~ N(Bb, B); σw² | rest ~ IG; σv² | rest ~ IG.
- **Forward-filtering, backward-sampling (FFBS)** — Frühwirth-Schnatter (1994) and Carter & Kohn (1994) algorithm for step (ii): run the Kalman filter forward; sample xn ~ N(xnn, Pnn); then for t = n−1, ..., 0 sample xt ~ N(mt, Vt) where mt = xtt + Jt(xt+1 − xt+1t) and Vt = Ptt − Jt Pt+1t Jt'.
- **Bivariate-normal Gibbs illustration** — alternating draws (X | Y) ~ N(ρy, 1−ρ²) and (Y | X) ~ N(ρx, 1−ρ²) converge to the joint N(0, [[1, ρ], [ρ, 1]]) at a rate governed by ρ; canonical demonstration that conditional sampling generates joint posteriors.
- **Local level model MCMC** — IG(.02, .02) priors on σv² and σw²; FFBS with 1010 iterations (10 burn-in) recovers posterior means near true σw² = .5 and σv² = 1, with pointwise 95% credible intervals on the smoothed states.
- **J&J structural model MCMC** — same model as the structural-model J&J fit, sampled by FFBS with normal-IG priors on (β, σw,11²) and IG priors on σv² and σw,22²; growth-rate posterior centered at 3.7% (matches the MLE 3.5%), with full posterior trace plots, ACFs, and 99% credible bands on trend and trend+season smoothers.
- **Beyond linear-Gaussian** — non-conjugate models replace step (i) with a Metropolis–Hastings step (the complete-data density p(Θ, x0:n, y1:n) can be evaluated pointwise); nonlinear / non-Gaussian state-space models fall outside the FFBS framework and the reader is referred to Douc, Moulines & Stoffer (2014).
