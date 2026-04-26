# Ch 7: Statistical Methods in the Frequency Domain

## Table of Contents

- [1. Motivation and the Frequency Domain Likelihood](#1-motivation-and-the-frequency-domain-likelihood)
- [2. Regression on Stationary and Deterministic Inputs](#2-regression-on-stationary-and-deterministic-inputs)
- [3. Random Coefficients and Signal Extraction](#3-random-coefficients-and-signal-extraction)
- [4. Spectral ANOVA for Designed Experiments](#4-spectral-anova-for-designed-experiments)
- [5. Discriminant and Cluster Analysis for Time Series](#5-discriminant-and-cluster-analysis-for-time-series)
- [6. Principal Components and Factor Analysis](#6-principal-components-and-factor-analysis)
- [7. The Spectral Envelope](#7-the-spectral-envelope)

## 1. Motivation and the Frequency Domain Likelihood

- **Why frequency domain** — many physical/biological phenomena are best described by Fourier components rather than ARIMA difference equations; multivariate techniques (regression, ANOVA, PCA, discriminant analysis) extend naturally because DFTs at distinct Fourier frequencies are approximately uncorrelated.
- **DFT of a vector process** — for `xt = (xt1, …, xtp)'`, define `X(ωk) = n^(-1/2) Σ xt e^(-2πiωk t)` at Fourier frequencies `ωk = k/n`; cosine and sine transforms are jointly normal with covariance built from the cospectrum `C(ωk)` and quadrature `Q(ωk)`, so the spectral matrix is `f(ωk) = C(ωk) - iQ(ωk)`.
- **Whittle likelihood** — DFTs are approximately complex multivariate normal, giving the log likelihood `-L ln|f(ωk)| - Σ (X_l - M_l)* f(ωk)^(-1) (X_l - M_l)` summed over `L = 2m+1` neighboring frequencies. This Whittle approximation (Whittle 1961, Brillinger 1981, Hannan 1970) underlies every multivariate frequency-domain method in the chapter.
- **Smoothed spectral estimator** — the MLE for the spectral matrix in the band is `f̂(ω) = L^(-1) Σ (X_l - M_l)(X_l - M_l)*`, the standard averaged periodogram matrix.

## 2. Regression on Stationary and Deterministic Inputs

- **Jointly stationary regression** — output `yt = Σ βr' xt-r + vt` with `xt` a `q × 1` stochastic input vector; minimizing MSE via the Projection Theorem gives the frequency-domain estimator `B'(ω) = fxy*(ω) fxx^(-1)(ω)` and the residual spectrum `fy·x(ω) = fyy(ω) - fxy*(ω) fxx^(-1)(ω) fxy(ω)`.
- **Multiple coherence** — `ρ²y·x(ω) = fxy* fxx^(-1) fxy / fyy ∈ [0,1]` is the proportion of `yt`'s power at frequency `ω` predictable from a linear filter of the inputs; mirrors `R²` in classical regression.
- **F-test and ANOPOW** — `F = (L-q)ρ̂²/(q[1-ρ̂²]) ~ F_{2q, 2(L-q)}` tests `B(ω) = 0`. A partitioned test `β2 = 0` decomposes power into `SSR(ω)`, `SSE(ω)`, `Total` in an Analysis of Power table that parallels classical ANOVA. Significance is judged via false discovery rate (Benjamini–Hochberg) thresholds across frequencies.
- **Lake Shasta inflow example** — log inflow regressed on five candidate inputs (temperature, dew point, cloud cover, wind speed, square-root precipitation); precipitation has the highest squared coherence at all frequencies, with seasonal-period dominance. A two-input model (temperature + precipitation) reveals an instantaneous positive temperature effect and an exponentially decaying precipitation response, motivating a transfer function model with `δ0/(1 - ω1 B)`.
- **Deterministic-input regression** — when `zjt` is a known design (replicated `j = 1,…,N`), Gauss–Markov gives `B̂(ωk) = Sz^(-1)(ωk) szy(ωk)` with `Sz = Z*Z`. The F-statistic `F = (N-q)SSR/(q SSE)` has degrees of freedom `2Lq, 2L(N-q)`.
- **Infrasonic array example** — three sensors record a nuclear explosion 25 km south of Christmas Island; the BLUE estimator of the common waveform reduces to the **delayed beam** `β̂t = (1/N) Σ y_{j,t+τj}`. Detection peaks near 0.02 cycles per second.

## 3. Random Coefficients and Signal Extraction

- **Random coefficient regression** — replace fixed `βr` with a stationary stochastic signal vector with spectrum `fβ(ω) Iq`; output spectrum becomes `fy(ω) = fβ(ω) Z(ω) Z*(ω) + fv(ω) IN`. Generalizes Wiener–Kolmogorov signal extraction and treats deconvolution and ridge-type inversion.
- **Ridge-corrected estimator** — `B̂(ω) = [Sz(ω) + θ(ω) Iq]^(-1) szy(ω)` with `θ(ω) = fv(ω)/fβ(ω)` the inverse signal-to-noise ratio at frequency `ω`. The additive `θ(ω) Iq` term is exactly a frequency-dependent ridge penalty.
- **Variance components** — the random-effects ANOVA in the frequency domain falls out from this framework: `E[SSR(ω)] = L fβ(ω) tr{Sz(ω)} + Lq fv(ω)` and `E[SSE(ω)] = L(N-q) fv(ω)` give unbiased estimators of the signal and noise spectra by method of moments.

## 4. Spectral ANOVA for Designed Experiments

- **Equality of means** — for `yijt = µt + αit + vijt` with `Σαit = 0`, the test for `αit = 0` reduces to between-group `SSR(ωk)` and within-group `SSE(ωk)` evaluated on DFTs, smoothed over `L` frequencies, and compared via an F-statistic — a frequency-by-frequency one-way ANOVA.
- **Two-way spectral ANOVA** — `yijkt = µt + αit + βjt + γijt + vijkt` partitions power into stimulus, consciousness, and interaction components; unequal cell counts handled via the general regression form `Y(ωk) = Z B(ωk) + V(ωk)`.
- **fMRI brain activation example** — BOLD signal at nine brain locations in a pain-perception experiment (Antognini et al. 1997): three periodic stimuli (brush, heat, shock) crossed with two consciousness levels (awake, sedated), 26 subjects in unequal cells. Equality-of-means tests reject at the four cortex locations and cerebellum 2 around the stimulus frequency 1/64 Hz; consciousness is the dominant factor at the signal frequency, with a significant interaction at the ipsilateral primary somatosensory cortex.
- **Simultaneous inference (Scheffé)** — a contrast `Ψ(ωk) = A*(ωk) B(ωk)` is tested via `F(A) = (N-q)|Ψ̂ - Ψ|²/(q sy²·z(ωk) Q(A))`; the bound is valid for infinitely many compounds at level α. Used to isolate which of brush, heat, shock drives the fMRI signal at each location.
- **Multivariate equality tests** — for `p`-variate group series, between/within cross-power matrices `SPR(ωk), SPE(ωk)` lead to the likelihood ratio `Λ(ωk) = |SPE|/|SPE + SPR|`; `χ² = -2 Σ(Ni - I - p - 1) log Λ` (Khatri 1965, Hannan 1970) tests equality of means with `2(I-1)p` df. The `I = 2` case reduces to **Hotelling's T²**.
- **Equality of spectral matrices** — likelihood-ratio statistic `L'(ωk)` compares per-group spectral matrices to the pooled estimator; `χ²_{(I-1)p²} = -2r log L'(ωk)` (Krishnaiah et al. 1976, Shumway 1982) with a Bartlett-type correction `r`.
- **Earthquake vs. explosion example** — eight earthquakes vs. eight explosions, bivariate (P, S) phases. Equality-of-means is not rejected, but equality of spectral matrices, of P-spectra, and of S-spectra is strongly rejected — differences live in the **second-order** structure, motivating spectral-matrix-based discrimination.

## 5. Discriminant and Cluster Analysis for Time Series

- **Two paradigms** — *optimality approach* makes Gaussian assumptions and minimizes a well-defined error criterion (likelihood-based); *feature extraction approach* picks visually discriminating quantities (e.g., log-amplitude ratios) without an explicit optimality target.
- **Bayes/Neyman–Pearson rule** — assign `x` to `Πi` if `pi(x)/pj(x) > πj/πi`; under multivariate normality with equal covariance this is the **linear discriminant** `dl(x) = (µ1 - µ2)' Σ^(-1) x - …`, with error `Φ(-D/2)` controlled by the **Mahalanobis distance** `D² = (µ1 - µ2)' Σ^(-1) (µ1 - µ2)`.
- **Magnitude-feature classification** — log peak-to-peak P and S amplitudes for the eight earthquakes and eight explosions form a 2D feature; jackknifed posterior probabilities range .621–1.000 for earthquakes and .717–1.000 for explosions, and the Novaya Zemlya event of unknown origin classifies as an **explosion** with posterior .960.
- **Time series discriminant analysis (frequency-domain Whittle rule)** — using the complex Gaussian likelihood, `gj(X) = ln πj - Σ [ln|fj(ωk)| + X*(ωk) fj^(-1)(ωk) X(ωk) - 2 Mj* fj^(-1) X + Mj* fj^(-1) Mj]` summed over `0 < ωk < 1/2`. When means are equal but spectra differ (the seismic case), it reduces to a **quadratic detector** in the periodogram matrix `I(ωk) = X(ωk) X*(ωk)`.
- **Kullback–Leibler discrimination** — `I(f1; f2) = (1/n) Σ [tr{f1 f2^(-1)} - ln(|f1|/|f2|) - p]` is a non-negative disparity (zero iff `f1 = f2`); classifying `x` as `Πi` minimizing `I(f̂; fi)` is equivalent to choosing the population whose theoretical spectrum is closest to the sample spectrum.
- **Chernoff information** — `Bα(f1; f2) = (1/2n) Σ [ln|αf1 + (1-α)f2|/|f2| - α ln|f1|/|f2|]` indexed by `α ∈ (0,1)`; `α = 1/2` is Bhattacharya's symmetric divergence. The regularizer `α` is chosen to maximize disparity between training-group spectra (Kakizawa et al. 1998).
- **Earthquake vs. explosion discrimination** — at `α = .4`, Chernoff and K-L differences classify the Novaya Zemlya event as an explosion; Earthquake 1 is borderline and Explosion 6 is misclassified.
- **Cluster analysis via J-divergence** — symmetric disparity `J(f1; f2) = I(f1; f2) + I(f2; f1)` (and analogous `JBα`) gives a quasi-distance matrix usable in hierarchical or partitioning clustering.
- **PAM clustering of seismic events** — Partitioning Around Medoids (Kaufman & Rousseeuw 1990), a robustification of k-means, with two clusters reproduces the earthquake/explosion split with EQ1 and EX8 misclassified; NZ again clusters with explosions.

## 6. Principal Components and Factor Analysis

- **Principal components in frequency domain** — at fixed `ω`, find complex unit `c(ω)` maximizing `c(ω)* fxx(ω) c(ω)`; solution is the leading eigenvector `e1(ω)` of the Hermitian spectral matrix, eigenvalue `λ1(ω)` is the spectral density of the first PC series `yt1(ω) = e1(ω)* xt`. Equivalent to optimal univariate reconstruction (Brillinger 1981, Theorem 9.3.1) where the analyzing and synthesizing filters coincide.
- **fMRI PCA example** — for the eight-location BOLD series at the stimulus frequency `ω = 4/128`, the first PC explains ~98% of total power (`λ̂1 = 2.00`, `tr(f̂xx) = 2.05`); the eigenvector identifies cortex locations 1–4 and surprisingly cerebellum 1 as responding, while location 6 (thalamus 2) is not contributing (zero in 99% confidence region).
- **Factor analysis** — classical model `x = Bz + ε` writes the covariance as `Σxx = BB' + D` with `B` the `p × q` loadings (`q ≪ p`), `D` diagonal error variance; loadings are unique only up to orthogonal rotation `B* = BQ`. Estimated by principal components (`B̂ = [√λ̂1 ê1, …, √λ̂q êq]`) or maximum likelihood via EM.
- **Frequency-domain factor model** — `fxx(ω) = B(ω) B(ω)* + Dε(ω)` with `B(ω)` complex `p × q`. Motivating signal-plus-noise model: `xtj = cj st-τj + εtj` (common signal with phase shifts) yields `X(ω) = a(ω) Xs(ω) + Xε(ω)`, the one-factor spectral model.
- **Macroeconomic factor example** — quarterly growth rates 1948–1988 of unemployment, GNP, consumption, government investment, private investment (`n = 160`); first factor `λ̂1` peaks at `ω = .25` (one cycle every four years) loading on unemployment, GNP, consumption, private investment; second factor `λ̂2` peaks at `ω = .125` (one cycle every eight years) loading almost exclusively on government investment.

## 7. The Spectral Envelope

- **Categorical time series scaling problem** — for a series taking values in `{c1, …, ck}`, arbitrary numerical scalings give different spectra; the spectral envelope (Stoffer et al. 1993) finds the optimal scaling at each frequency rather than fixing one a priori.
- **Definition** — represent categories as unit vectors `yt = uj` when `xt = cj`; the spectral envelope is `λ(ω) = max_β β' fyy^re(ω) β / (β' V β)`, the largest eigenvalue (in the metric of `V = D - pp'`) of the real part of the spectral matrix. `λ(ω) dω` is the maximal proportion of total power attributable to frequencies `(ω, ω + dω)` over any scaling.
- **Optimal scaling** — the eigenvector `β(ω)` corresponding to `λ(ω)` is the **optimal scaling**; invariant under location/scale changes of `β`. Significance threshold: `(2/n) exp(zα/ηn)` from a log-normal first-order expansion.
- **Infant EEG sleep states** — categorical time series with categories NR1–NR4, REM, AW; the spectral envelope locates a peak at one cycle per 60 minutes, the natural sleep-cycling frequency, without requiring the analyst to choose a numerical scaling.
- **DNA sequences and Epstein–Barr virus** — for the four-letter alphabet `{A, C, G, T}`, the spectral envelope of the BNRF1 gene (3954 bp) shows a strong signal at frequency `1/3` with optimal scaling `A = .10, C = .61, G = .78, T = 0` — the **strong–weak hydrogen-bonding alphabet** `S = {C,G}, W = {A,T}`. A sliding-window analysis over four sub-segments confirms the 1/3 signal in the first three windows but not the fourth, suggesting the last quarter is noncoding.
- **Real-valued extension** — for a real series and a basis `{g1, …, gk}` (e.g., `{x, |x|, x²}`), the same eigenvalue problem `fyy^re(ω) β(ω) = λ(ω) V β(ω)` defines `λ(ω)` as the largest fraction of power explainable by any transformation in the span (McDougall et al. 1997); related to projection pursuit.
- **NYSE returns example** — with `G = {x, |x|, x²}`, considerable power appears at low frequencies; the optimal transformation near `ω = .001` is `g(x) = -x + 921|x| - 2596x²`, essentially `|x|` with mild asymmetry and dampened tails — supports findings (Ding et al. 1993) that absolute returns capture long-range dependence better than squared returns.
