# Time Series Analysis and Its Applications: Summary

> **Read time: ~15–30 minutes.** This page is a single-sitting narrative summary of the book's key ideas. For a detailed chapter-by-chapter reference with the author's definitions and concrete examples, see the chapter entries in the sidebar.

## Table of Contents

- [1. Thesis](#1-thesis)
- [2. The Two Domains](#2-the-two-domains)
- [3. Stationarity as the Foundational Assumption](#3-stationarity-as-the-foundational-assumption)
- [4. The ARIMA Family](#4-the-arima-family)
- [5. Forecasting](#5-forecasting)
- [6. Spectral Analysis](#6-spectral-analysis)
- [7. Filtering, Coherence, and Lagged Regression](#7-filtering-coherence-and-lagged-regression)
- [8. State Space Models as a Unifying Framework](#8-state-space-models-as-a-unifying-framework)
- [9. Specialized Models: Long Memory, GARCH, Threshold, HMM](#9-specialized-models-long-memory-garch-threshold-hmm)
- [10. Multivariate Frequency-Domain Methods](#10-multivariate-frequency-domain-methods)
- [11. Key Takeaways](#11-key-takeaways)

## 1. Thesis

Shumway and Stoffer write the book as a working textbook for time series analysis, balancing theoretical integrity with practical computation in R. The central premise is that data observed sequentially in time violate the iid assumption that underpins classical statistics, and serial correlation must be modeled rather than ignored. The book develops two complementary languages for this: a **time domain** approach that treats current values as functions of past values (the ARIMA family, state space models) and a **frequency domain** approach that decomposes a series into cycles (spectral analysis, coherence, the spectral envelope). Each is presented as a full toolkit — model class, estimation, forecasting, diagnostics — and the second half of the book shows how state space methods unify the two and extend to nonlinear, switching, and Bayesian variants.

## 2. The Two Domains

The book opens by introducing time series through seven motivating data sets: Johnson & Johnson quarterly earnings, global land–ocean temperature deviations 1880–2015, recorded speech, daily DJIA returns, the monthly Southern Oscillation Index (SOI) paired with fish Recruitment, fMRI BOLD signals under periodic brushing, and seismic waveforms from earthquakes and explosions. Each example illustrates a different question — trend, cycle, joint dependence, classification — and each will be revisited as new tools are introduced.

Two complementary perspectives run through the entire book. The **time domain** asks how today's value depends on yesterday's, and answers via lagged regressions, ARMA models, and state space representations. The **frequency domain** asks which periodic components dominate the series, and answers via the spectral density, the periodogram, and coherence between series. They are not rival approaches but two languages for the same object: the autocovariance function and the spectral density are Fourier-transform pairs, carrying the same information.

The basic building block in either language is **white noise**, denoted wt ~ wn(0, σw²): a sequence of uncorrelated zero-mean variates with finite variance. Strengthening this to iid noise or Gaussian white noise gives stronger independence assumptions used for inference. From white noise the book builds three running prototypes — moving averages, autoregressions, and random walks — that prefigure the ARIMA family of Chapter 3.

A signal-plus-noise model xt = st + vt provides the second template, where a deterministic signal st (often a sinusoid) is obscured by stationary noise vt; the **signal-to-noise ratio (SNR)** controls how easily the signal can be recovered, and the same model motivates state space methods later.

## 3. Stationarity as the Foundational Assumption

Because only one realization of the process is usually observed, the book argues that some form of regularity in time is needed before averages can estimate population quantities. **Strict stationarity** — invariance of every joint distribution under time shifts — is too strong to verify. The working definition is **weak stationarity**: finite variance, constant mean, and an autocovariance γ(s, t) that depends only on the lag |s − t|. Henceforth "stationary" means weakly stationary.

Under stationarity the **autocovariance function** γ(h) and **autocorrelation function** ρ(h) = γ(h)/γ(0) summarize all linear dependence; they are symmetric in h and bounded by γ(0). The sample versions are estimated from a single realization by averaging over time, with the convention of dividing by n (rather than n − h) to preserve non-negative definiteness. Under white noise, the sample ACF is approximately N(0, 1/n), giving the practical ±2/√n significance bands that recur throughout the book. For two series, the **cross-covariance** and **cross-correlation** functions extend the same ideas, with the asymmetry ρxy(h) = ρyx(−h) becoming useful for detecting which series leads.

Many real series are nonstationary. Chapter 2 discusses the easiest case to handle, **trend stationarity** xt = μt + yt with stationary residual yt, and contrasts two ways to remove trend. **Detrending** estimates μ̂t and works with the residual ŷt = xt − μ̂t; it returns an explicit estimate of yt but assumes a deterministic functional form. **Differencing** with the backshift operator (1 − B)xt = xt − xt−1 removes trend without estimating parameters, works for both deterministic polynomial trends and stochastic random-walk trends, but does not recover yt. Fractional differencing extends this to non-integer powers and connects to long-memory models in Chapter 5.

Variance-stabilizing transformations (logarithm, Box–Cox) handle the other common nonstationarity, where variability scales with level. The glacial varves series illustrates: raw thicknesses have variance proportional to mean, and log-thickness has roughly constant variance and is closer to normal.

## 4. The ARIMA Family

Chapter 3 develops the **autoregressive integrated moving average** family, the workhorse of time-domain modeling. An **AR(p)** writes xt as a linear function of its last p values plus white noise; an **MA(q)** writes xt as a linear combination of the last q innovations; an **ARMA(p, q)** combines the two as φ(B)xt = θ(B)wt with polynomial operators in the backshift B.

The clean theory needs three regularity conditions. **Causality** requires the roots of φ(z) to lie outside the unit circle; this gives a one-sided linear-process representation xt = Σ ψj wt−j depending only on the past, the only kind of model useful for forecasting. **Invertibility** requires the roots of θ(z) to lie outside the unit circle; this gives a unique infinite AR representation and resolves the ambiguity that two different MA(1) models can have the same ACF. **Parameter redundancy** is avoided by requiring φ and θ to share no common factors, since a common factor inflates parameter count without changing dynamics — the authors warn explicitly that fitting an ARMA(1,1) to white noise can return apparently significant parameters that are pure artifacts.

Identification proceeds through the **autocorrelation function (ACF)** and the **partial autocorrelation function (PACF)**, with the famous diagnostic table:

| | AR(p) | MA(q) | ARMA(p, q) |
|---|---|---|---|
| ACF | tails off | cuts off after lag q | tails off |
| PACF | cuts off after lag p | tails off | tails off |

The Recruitment series is the canonical example: the sample ACF cycles at roughly 12 months, while the PACF has spikes at lags 1 and 2 and drops to zero, suggesting an AR(2). OLS gives x̂t = 6.74 + 1.35 xt−1 − 0.46 xt−2.

Estimation uses several routes that all coincide asymptotically under regularity conditions. **Yule–Walker** for AR(p) replaces population autocovariances with sample ones in the linear equations γ(h) = φ1 γ(h−1) + … + φp γ(h−p) and is asymptotically optimal. For MA and ARMA, method of moments is suboptimal (its asymptotic variance can be 3.5× the MLE), so the book uses **conditional or unconditional Gaussian likelihood** maximized via Newton–Raphson, scoring, or Gauss–Newton iteration. The asymptotic distribution √n(β̂ − β) → N(0, σw² Γ−1) is the same across estimators. Bootstrap is recommended when n is small or parameters are near a boundary, because the asymptotic normal can be badly skewed; the AR(1) with φ = 0.95 and Laplace errors is the textbook illustration.

**ARIMA(p, d, q)** extends ARMA by allowing the d-th difference to be ARMA. This handles stochastic trends — random walks that detrending cannot fix — and includes the random walk with drift (ARIMA(0,1,0) with constant) and the **IMA(1,1)**, which underlies the **exponentially weighted moving average (EWMA)** beloved by business forecasters. **Multiplicative seasonal ARIMA**, written ARIMA(p, d, q) × (P, D, Q)s, layers ordinary ARMA dynamics with operators acting at the seasonal lag s and is the Box–Jenkins standard for monthly or quarterly data; the canonical example is the international Air Passengers series 1949–1960, where the final fit is ARIMA(0,1,1) × (0,1,1)12.

The **Box–Jenkins procedure** sews these pieces into a workflow: plot, transform, identify p and d and q from ACF/PACF, estimate, check residual diagnostics, choose among candidates by AIC, AICc, or BIC. Diagnostics inspect standardized residuals for whiteness, with the **Ljung–Box–Pierce Q-statistic** Q ~ χ²H−p−q the omnibus test against residual autocorrelation. The U.S. census fitted with an 8th-degree polynomial — predicting near-zero population in 2000 — serves as the cautionary example against overfitting.

The chapter closes with **regression with autocorrelated errors**: when ordinary regression yt = Σ βj zt,j + xt has a stationary but non-white residual, OLS standard errors are wrong. Multiplying through by the AR operator that whitens xt produces a transformed regression with correct inference. The Cochrane–Orcutt-style procedure iterates between OLS, ARMA modeling of residuals, and re-fitting with the chosen error structure; the LA mortality example revisits the regression of cardiovascular mortality on time, temperature, temperature², and particulates with AR(2) errors.

## 5. Forecasting

The forecasting framework is set up in three regimes parameterized by horizon: **forecasting** when the prediction horizon exceeds the data, **filtering** when it equals the latest observation, and **smoothing** when it is in the past. The **minimum mean squared error (MMSE)** predictor is the conditional expectation E(xn+m | x1:n); under Gaussianity this equals the **best linear predictor (BLP)**, which depends only on second moments and so applies to any stationary process. The prediction equations characterize the BLP as orthogonal to the data.

For AR(p), the prediction equations collapse: once n ≥ p, the BLP coefficients are simply the AR parameters. For general ARMA, the **Durbin–Levinson** algorithm builds the prediction recursively, and as a by-product produces the partial autocorrelations φnn used for identification. The **innovations algorithm** is a second recursion built from one-step prediction errors and is particularly clean for MA processes. The truncated ARMA forecast, used in practice, simply runs the model forward and replaces unobserved past with zero. Stationary ARMA forecasts converge exponentially to the unconditional mean μx, and prediction error grows toward the marginal variance σx². The Recruitment 24-month forecast levels off rapidly with wide bands, illustrating why far-horizon forecasts of stationary series are uninformative.

**ARIMA forecasts** behave differently because the integrated component has unbounded variance. The random walk with drift forecast is xn+m^n = mδ + xn, a straight line whose prediction variance mσw² grows without bound, accurately reflecting the fundamental forecasting difficulty of nonstationary series.

## 6. Spectral Analysis

Chapter 4 builds the parallel frequency-domain toolkit. Any stationary series can be represented as a superposition of cosines and sines at different frequencies: xt = Σ [Uk1 cos(2πωk t) + Uk2 sin(2πωk t)] with uncorrelated coefficients. The variance of the series partitions across frequencies — and that distribution is exactly what the spectral analysis describes.

The **spectral density** f(ω) is the Fourier transform of the autocovariance, f(ω) = Σ γ(h) e^(−2πiωh), and the variance integrates as var(xt) = ∫ f(ω) dω. For white noise f(ω) = σw² is flat — the analogy with white light gives the noise its name. ARMA spectra take the closed form fx(ω) = σw² |θ(e^(−2πiω))|² / |φ(e^(−2πiω))|², so the time-domain and frequency-domain descriptions are linked algebraically. The **spectral representation theorem** justifies decomposing any mean-zero stationary series into harmonic components, the theoretical foundation for everything that follows.

Discrete sampling forces a fundamental constraint: the **folding (Nyquist) frequency** is 0.5 cycles per sample, and higher frequencies are **aliased** down — the wagon-wheel effect of motion picture cameras that the book uses as a memorable example. This is why sampling rate matters.

Estimation starts from the **discrete Fourier transform (DFT)** d(ωj) at the fundamental frequencies ωj = j/n, computed in O(n log n) by the **fast Fourier transform (FFT)**. The squared modulus is the **periodogram** I(ωj), the natural sample analog of f(ω). Unfortunately the periodogram is **inconsistent**: under standard regularity conditions, 2 I(ωj)/f(ωj) is approximately χ²2 in the limit, so its variance does not vanish as n grows. Periodogram ordinates are essentially based on two observations each.

The fix is smoothing. **Nonparametric estimators** average the periodogram over neighboring frequencies — uniform Daniell weights, modified Daniell with half-weighted endpoints, or general weighted averages — trading resolution for variance. The smoothed estimator has approximately χ²2L distribution, narrower confidence intervals, but smears narrow peaks. **Tapering** the data before transforming — multiplying by a cosine bell window before the DFT — suppresses the **leakage** caused by the **Fejér kernel**'s sidelobes, at the cost of slightly wider main lobes. **Parametric estimators** fit an AR(p) and plug into the closed-form ARMA spectrum, useful when narrow peaks must be resolved but at the price of model dependence; Property 4.7 shows that a sufficiently high-order AR can approximate any continuous spectral density.

The SOI shows the canonical pattern: a narrow peak at ω = 1/12 (the annual cycle) and a wider band of power near ω = 1/48 (the four-year El Niño cycle), separated by smoothing with appropriate tapering.

## 7. Filtering, Coherence, and Lagged Regression

A linear filter yt = Σ aj xt−j multiplies the input spectrum by the squared modulus of its **frequency response function** A(ω) = Σ aj e^(−2πiωj), so spectra are altered frequency by frequency. **Low-pass filters** (smoothing operations) preserve slow components and attenuate fast ones; **high-pass** does the opposite (the first difference is high-pass); **band-pass** isolates a chosen band. Each filter has a **gain** and a **phase**: gain is the amplitude multiplier, phase is the frequency-dependent time delay. Symmetric filters have zero phase, while a pure delay yt = xt−D has linear phase −2πωD.

For two series the **cross-spectrum** fxy(ω) = cxy(ω) − i qxy(ω) decomposes into the **cospectrum** (in-phase covariance) and **quadspectrum** (out-of-phase). The **squared coherence** ρ²y·x(ω) is the frequency-domain analog of squared correlation, between 0 and 1, equal to 1 at every frequency when yt is an exact linear filter of xt with no noise. SOI and Recruitment are highly coherent at the annual cycle and at low frequencies, with peak coherence near a 9-year cycle.

This sets up the **lagged regression** problem yt = Σ βr xt−r + vt, solved frequency by frequency as B(ω) = fyx(ω)/fxx(ω); the inverse DFT recovers the impulse response coefficients β̂t. The mean squared error is ∫ fyy(ω)[1 − ρ²yx(ω)] dω, mirroring σy²(1 − ρ²) in classical regression. The same machinery solves **signal extraction** problems: the **Wiener filter** A(ω) = SNR(ω)/[1 + SNR(ω)] for the simple case yt = xt + vt isolates the signal optimally given the spectra of signal and noise. For SOI, a low-pass Wiener filter cleanly extracts the El Niño signal that the centered moving average corrupts with high-frequency leakage.

Chapter 5 returns to the time domain to handle the same lagged-regression problem with the **transfer function model** of Box–Jenkins, where α(B) is parameterized parsimoniously as a rational polynomial δ(B) Bd / ω(B). **Prewhitening** the input — fitting an ARMA to xt to make it white, then applying the same operator to yt — converts the cross-correlation into a direct estimator of the impulse response coefficients. The SOI/Recruitment fit yt = 12 + 0.8 yt−1 − 21 xt−5 + ut (with ut an AR(1)) recovers the same structure as the frequency-domain coherency analysis.

## 8. State Space Models as a Unifying Framework

Chapter 6 introduces the **linear Gaussian state space model**, a two-equation system in which a hidden Markov **state** xt = Φ xt−1 + Υ ut + wt is observed through yt = At xt + Γ ut + vt. Originated by Kalman (1960) for spacecraft tracking, the framework is general enough to embed VAR, ARMA, ARMAX, structural decompositions, regression with autocorrelated errors, and (with extensions) hidden Markov models. The state is Markovian; observations are conditionally independent given the state; all serial dependence flows through x.

The **Kalman filter** is the central recursion: from the previous filtered estimate xt−1|t−1 it computes a one-step prediction, applies the **innovation** εt = yt − At xt|t−1 weighted by the **Kalman gain** Kt = Pt|t−1 At'(At Pt|t−1 At' + R)⁻¹, and arrives at xt|t. The filter never needs to reprocess the full data. The **innovations** are independent zero-mean Gaussian and form the basis of both the likelihood and the bootstrap. The **Kalman smoother** (also called the RTS smoother) runs backward through the data using the smoothing gain Jt to produce the most precise state estimate xt|n.

Estimation uses the innovations form of the Gaussian likelihood, optimized either by Newton–Raphson on the innovations directly or by the **EM algorithm**, which alternates running the smoother (E-step) with closed-form Gaussian MLE updates (M-step). EM is conceptually simpler but slower. Missing data are handled cleanly: the filter applies to whatever portion of yt is observed, and the smoother fills in unobserved components, providing imputation as a by-product of filtering.

The state space framework gives elegant solutions to several problems:

- **Structural models** decompose yt into trend, seasonal, and irregular components, each with its own state subequation. The Johnson & Johnson example fits an exponentially growing trend (φ = 1.035, a 3.5% annual growth rate) plus a constrained seasonal term, smoothed and forecast 12 quarters ahead with widening uncertainty.
- **ARMAX and regression with autocorrelated errors** fit naturally by placing inputs in the state equation or observation equation respectively, all via the modified filter when noise terms are correlated.
- **Bootstrap** resamples the standardized innovations and refits, exposing finite-sample skewness and bimodalities that asymptotic standard errors miss; the inflation/interest example reveals that what looks like a stochastic regression coefficient is better described as fixed.
- **Smoothing splines** turn out to be a special state space model: minimizing Σ(yt − μt)² + λ Σ(∇²μt)² is equivalent to MAP estimation under the random-walk-on-second-difference state model, with smoothing parameter λ = σv²/σw² recovered from MLE.

## 9. Specialized Models: Long Memory, GARCH, Threshold, HMM

Chapter 5 collects time-domain extensions for situations where ARMA is inadequate. **Long memory** series have ACFs that persist over very many lags rather than decaying exponentially; the log-varve series shows nonzero ACF at lag 100. The **fractionally integrated ARMA (ARFIMA)** model φ(B) ∇d (xt − μ) = θ(B) wt with −0.5 < d < 0.5 captures this: ρ(h) ~ h^(2d−1) so Σ |ρ(h)| diverges for 0 < d < 0.5, and the spectrum blows up as ω → 0. Estimation uses time-domain MLE, the **Whittle approximation** in the frequency domain, or the **Geweke–Porter-Hudak** regression of log periodogram on log-frequency near zero. For the varves, all three methods give d̂ ≈ 0.38.

**Unit root testing** asks whether differencing is even appropriate, since differencing an already stationary series with |φ| < 1 introduces extraneous correlation. The **Dickey–Fuller** statistic has a non-standard limiting distribution (an integral of Brownian motion) and quantiles come from simulation; the **augmented Dickey–Fuller (ADF)** test extends to autocorrelated errors, and the **Phillips–Perron** test handles serial correlation differently. For the log-varves, all three reject the unit root null, supporting the long-memory interpretation over a unit-root one.

Financial returns motivate **conditional heteroscedasticity** models. **ARCH(1)** sets the conditional variance σt² = α0 + α1 rt−1², so volatility tracks the previous squared return; **GARCH(p, q)** generalizes by adding lagged variance terms. These models reproduce the volatility clustering visible in DJIA returns (an AR(1)-GARCH(1,1) fit gives α̂1 + β̂1 ≈ 0.99) and the leptokurtic marginal distribution of returns. Variants include **APARCH** (asymmetric power, capturing the leverage effect) and **IGARCH** (forcing α1 + β1 = 1 for persistent volatility). GARCH limitations — symmetric response to positive and negative shocks, slow response to large isolated returns — motivate **stochastic volatility** models in Chapter 6 that place log-variance in a latent state rather than determining it from past returns.

**Threshold autoregression (TAR / SETARMA)** of Tong handles non-Gaussian, time-irreversible dynamics by switching among k regimes based on whether xt−d crosses fixed thresholds, each regime with its own ARMA dynamics. Pneumonia/influenza mortality, which rises faster than it falls during epidemics, fits a two-regime TAR with threshold at first-difference 0.05.

**Hidden Markov models (HMM)** make the regime itself unobserved — a finite-state Markov chain whose value selects an emission distribution for yt. The **forward–backward** recursions compute filtered, smoothed, and joint regime probabilities; the **EM (Baum–Welch)** algorithm estimates parameters; the **Viterbi** algorithm gives the most-likely state sequence. Annual earthquake counts (mean 19.4, variance 51.6) fit a two-state Poisson HMM with intensities 15.4 and 26.0; weekly S&P 500 returns fit a three-state Gaussian HMM separating regular volatility, transient large negatives, and high volatility. **Switching dynamic linear models** combine continuous Gaussian states with a regime indicator that switches the observation matrix, applied to multi-target tracking and to influenza epidemic detection.

The book's stochastic volatility example combines all of this. A two-component normal mixture approximates the log(χ1²) distribution of the squared-and-logged returns, recasting SV as a switching DLM whose Section 6.10 filtering equations apply directly. For NYSE returns around the 1987 crash, φ̂ = 0.988 (highly persistent volatility) and the one-step-ahead predicted log-volatility spikes around October 19. Bayesian analysis is added via the **forward-filtering, backward-sampling (FFBS)** Gibbs algorithm of Frühwirth-Schnatter and Carter & Kohn, which alternates Kalman filtering forward with sampling backward, demonstrated on the J&J structural model with a posterior trend growth rate of 3.7% closely matching the MLE.

## 10. Multivariate Frequency-Domain Methods

Chapter 7 lifts the multivariate machinery into the frequency domain. The DFTs of a vector series are approximately complex multivariate normal at each Fourier frequency and approximately independent across frequencies, giving the **Whittle likelihood** that underlies every method in the chapter. The smoothed periodogram matrix is the natural spectral matrix estimator.

**Frequency-domain regression** estimates the transfer function B(ω) = fxy*(ω) fxx⁻¹(ω) frequency by frequency, with the **multiple coherence** ρ²y·x(ω) playing the role of R². An **Analysis of Power (ANOPOW)** table parallels classical ANOVA for partitioned tests, and inference uses false-discovery-rate adjustments across frequencies. The Lake Shasta inflow analysis identifies precipitation as the dominant predictor at all frequencies and motivates a transfer function model. **Spectral ANOVA** for designed experiments — between-group SSR(ω) over within-group SSE(ω) — handles the fMRI pain-perception experiment with three stimuli, two consciousness levels, and 26 subjects, identifying which brain locations and which factors operate at the stimulus frequency 1/64 Hz.

**Time series discriminant analysis** uses the Whittle likelihood to compare competing spectra; when group means are equal but spectra differ (as for earthquakes versus explosions), the Bayes/Neyman–Pearson rule reduces to a quadratic detector in the periodogram matrix. **Kullback–Leibler discrimination** measures the disparity between candidate spectra and the sample spectrum, and the **Chernoff information** is a tunable variant. With either, the Novaya Zemlya event of unknown origin classifies as an explosion. **Cluster analysis via J-divergence**, a symmetric form of the K-L disparity, supports unsupervised partitioning; PAM clustering on seismic events recovers the earthquake/explosion split.

**Principal components in the frequency domain** find, at each frequency, the linear combination that maximizes the spectral density of the resulting series — the leading eigenvector of the Hermitian spectral matrix. For the fMRI BOLD signal at the stimulus frequency, the first PC explains ~98% of total power. **Factor analysis** in the frequency domain models fxx(ω) = B(ω) B(ω)* + Dε(ω), and the macroeconomic example (unemployment, GNP, consumption, government investment, private investment 1948–1988) extracts a four-year business-cycle factor and an eight-year factor loaded almost exclusively on government investment.

The chapter closes with the **spectral envelope** for **categorical time series**. When values are categories rather than numbers, arbitrary numerical scalings give different spectra; the spectral envelope finds the optimal scaling at each frequency as the largest eigenvalue (in an appropriate metric) of the real part of the spectral matrix. Infant EEG sleep states (NR1–NR4, REM, AW) reveal a peak at one cycle per 60 minutes — the natural sleep cycling frequency — without the analyst pre-specifying numbers. For the four-letter DNA alphabet of the BNRF1 gene of Epstein–Barr virus, the spectral envelope finds a strong signal at frequency 1/3 (matching the codon structure of coding regions) with optimal scaling that recovers the strong–weak hydrogen-bonding alphabet S = {C, G}, W = {A, T}; sliding-window analysis localizes the signal to the first three quarters of the gene, suggesting the last quarter is noncoding. A real-valued extension over a basis {x, |x|, x²} applied to NYSE returns supports the finding (Ding et al. 1993) that absolute returns capture long-range dependence better than squared returns.

## 11. Key Takeaways

- **Time series analysis is the systematic study of correlated observations over time.** Classical statistics fails because adjacent observations are not independent, so dependence must be modeled rather than averaged away.
- **The time domain and frequency domain are dual descriptions** of the same object. The autocovariance function and the spectral density are Fourier-transform pairs; choose the language that matches the question (lagged dependence vs. cyclical structure).
- **Stationarity is the foundational working assumption.** Weak stationarity — constant mean and lag-only autocovariance — is enough for almost every method; nonstationary series should be detrended, differenced, or transformed first.
- **The ARIMA family covers a large fraction of practical time-domain modeling.** Causality and invertibility ensure unique, forecast-usable representations; ACF/PACF identify orders; AIC/AICc/BIC choose among candidates; Ljung–Box checks residual whiteness.
- **The periodogram is inconsistent and must be smoothed.** Nonparametric (smoothed periodogram with appropriate tapering) and parametric (AR-based) estimators are both valid; tapering controls leakage from strong components.
- **Coherence and spectral filtering generalize correlation and regression** to the frequency domain, with the squared coherence playing the role of R² and the Wiener filter giving optimal signal extraction.
- **State space models unify everything.** ARMA, VAR, structural decompositions, ARMAX, smoothing splines, HMMs, and stochastic volatility all fit; the Kalman filter and smoother provide filtering, smoothing, forecasting, missing-data imputation, and a likelihood for estimation.
- **Specialized models extend ARIMA where it fails**: ARFIMA for long memory, GARCH for volatility clustering, TAR for time-irreversible nonlinear dynamics, HMM for unobserved-regime switching.
- **Multivariate frequency-domain methods extend regression, ANOVA, discrimination, clustering, PCA, and factor analysis to time series**, with the Whittle likelihood as the common foundation.
- **The spectral envelope solves the categorical-scaling problem** by finding optimal numerical codes at each frequency, opening time-series spectral analysis to DNA, EEG sleep stages, and other discrete-valued processes.
