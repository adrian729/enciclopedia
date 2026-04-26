# Ch 4: Spectral Analysis and Filtering

## Table of Contents

- [1. Cyclical Behavior and the Periodogram](#1-cyclical-behavior-and-the-periodogram)
- [2. Spectral Density and Spectral Representation](#2-spectral-density-and-spectral-representation)
- [3. DFT, FFT, and the Periodogram as an Estimator](#3-dft-fft-and-the-periodogram-as-an-estimator)
- [4. Nonparametric Spectral Estimation](#4-nonparametric-spectral-estimation)
- [5. Parametric Spectral Estimation](#5-parametric-spectral-estimation)
- [6. Cross-Spectra and Coherence](#6-cross-spectra-and-coherence)
- [7. Linear Filters: Gain, Phase, Frequency Response](#7-linear-filters-gain-phase-frequency-response)
- [8. Lagged Regression and Optimum Filtering](#8-lagged-regression-and-optimum-filtering)
- [9. Multidimensional Spectral Analysis](#9-multidimensional-spectral-analysis)

## 1. Cyclical Behavior and the Periodogram

- **Frequency domain motivation** — instead of asking how today depends on yesterday, ask which cycles drive the series; the SOI carries a 12-month seasonal cycle and a 3–7 year El Niño cycle, the Johnson & Johnson series carries a quarterly cycle.
- **Periodic process** — xt = A cos(2πωt + φ), equivalently U1 cos(2πωt) + U2 sin(2πωt) with U1 = A cos φ, U2 = −A sin φ; the **frequency** ω is in cycles per unit time and the **period** is 1/ω; for SOI ω = 1/12 ⇒ period 12 months.
- **Folding (Nyquist) frequency** — discrete sampling needs at least two points per cycle, so the highest observable frequency is 0.5 cycles/point; higher frequencies are **aliased** to lower ones (the wagon-wheel effect in 24 fps movies).
- **Mixture of sinusoids** — xt = Σk [Uk1 cos(2πωkt) + Uk2 sin(2πωkt)] with uncorrelated zero-mean Uk1, Uk2 of variance σk² gives γx(h) = Σk σk² cos(2πωkh) and var(xt) = Σk σk²; the total variance decomposes by frequency.
- **Scaled periodogram** P(j/n) = aj² + bj² with aj, bj the regression coefficients on cos(2πtj/n) and sin(2πtj/n) — sample variance attributable to the **fundamental (Fourier) frequency** ωj = j/n, large where periodic components are strong.
- **Example 4.1 / 4.2 (mixture)** — a sum of three sinusoids at ω = 6/100, 10/100, 40/100 with squared amplitudes 13, 41, 85 produces a periodogram with exactly those heights at the matching frequencies, and zero elsewhere; mirroring at the folding frequency means P(j/n) = P(1 − j/n).
- **Example 4.3 (Star magnitude)** — 600 nightly star magnitudes show a 29-day and a 24-day cycle (an amplitude-modulated signal: cos(2πωt) cos(2πδt) splits into peaks at ω ± δ).

## 2. Spectral Density and Spectral Representation

- **Spectral distribution function F(ω)** — for a stationary process, γ(h) = ∫ e^(2πiωh) dF(ω) with F(1/2) = γ(0); F behaves like a CDF of variances rather than probabilities, distributing the total variance across frequencies.
- **Spectral density f(ω)** — when Σ|γ(h)| < ∞, dF(ω) = f(ω) dω and f(ω) = Σh γ(h) e^(−2πiωh); γ(h) and f(ω) are Fourier transform pairs, f is non-negative and even, and var(xt) = ∫ f(ω) dω is the total variance integrated across frequency.
- **Information equivalence** — autocovariance and spectral density carry the same information; γ(h) expresses it in lags (time domain), f(ω) in cycles (frequency domain).
- **White noise spectrum** — fw(ω) = σw², flat across all frequencies; the analogy with white light gives the noise its name.
- **Filtered output** (Property 4.3) — if yt = Σ aj xt−j, then fy(ω) = |A(ω)|² fx(ω), where A(ω) = Σ aj e^(−2πiωj) is the **frequency response function** and {aj} is the **impulse response**; filtering multiplies the input spectrum frequency by frequency.
- **ARMA spectral density** (Property 4.4) — for φ(B)xt = θ(B)wt, fx(ω) = σw² |θ(e^(−2πiω))|² / |φ(e^(−2πiω))|²; the MA(1) xt = wt + 0.5 wt−1 yields f(ω) = σw²[1.25 + cos(2πω)] (low-frequency power), while AR(2) with φ1 = 1, φ2 = −0.9 concentrates power near ω ≈ 0.16 (period ~6).
- **Spectral representation of xt** (Property 4.5) — every mean-zero stationary series can be written as xt = ∫ e^(2πiωt) dZ(ω) with Z(ω) a complex-valued process of uncorrelated increments whose variances follow F; the theoretical justification for decomposing a series into harmonic components.

## 3. DFT, FFT, and the Periodogram as an Estimator

- **Discrete Fourier transform (DFT)** d(ωj) = n^(−1/2) Σ xt e^(−2πiωjt) at fundamental frequencies ωj = j/n; the **fast Fourier transform (FFT)** computes the DFT in O(n log n) when n is highly composite (Cooley–Tukey 1965).
- **Periodogram** I(ωj) = |d(ωj)|² — squared modulus of the DFT, equal to Σ γ̂(h) e^(−2πiωjh); the **sample spectral density** of xt.
- **Spectral ANOVA** (Example 4.10) — Σ(xt − x̄)² = 2 Σj I(ωj); the periodogram partitions the total sum of squares into harmonic components, each contributing 2 df.
- **Centering and padding** — trends produce huge low-frequency contamination, so the data are mean-adjusted (or detrended) before the DFT; series are zero-padded to a highly composite n′ for the FFT (e.g., SOI with n = 453 is padded to n′ = 480).
- **Periodogram is inconsistent** — under a linear-process assumption, 2 I(ωj)/f(ωj) → χ2², so var[I(ω)] ≈ f²(ω) does **not** vanish as n → ∞; periodogram ordinates are based effectively on two observations each.
- **Example 4.13 (SOI / Recruitment)** — raw periodograms show a narrow peak at the yearly cycle ω = 1/12 and a wide band of power near ω = 1/48 (four-year El Niño); the χ2² confidence interval [2I/χ²(1−α/2), 2I/χ²(α/2)] is so wide as to be nearly useless, motivating smoothing.

## 4. Nonparametric Spectral Estimation

- **Smoothed periodogram** f̄(ω) = L^(−1) Σ I(ωj + k/n) over L = 2m+1 contiguous frequencies — averages the periodogram over a band B of bandwidth L/n; under the band-flat assumption, 2L f̄(ω)/f(ω) ≈ χ²_{2L}, giving narrower confidence intervals.
- **Bias / resolution tradeoff** — wider band B improves variance (more degrees of freedom 2L) but smears narrow peaks; narrower B preserves resolution but produces wide intervals; padding adjusts df to 2Ln/n′.
- **Daniell kernel** — uniform weights {1/L,…,1/L}; iterating it (e.g., apply m=1 twice) gives triangular weights {1/9, 2/9, 3/9, 2/9, 1/9}; the **modified Daniell kernel** half-weights the endpoints.
- **Weighted estimator** f̂(ω) = Σ hk I(ωj + k/n) with Σ hk = 1 — using weights that decrease away from the center improves resolution; effective length Lh = (Σ hk²)^(−1) replaces L in the chi-squared approximation, df = 2Lh n/n′.
- **Tapering** — multiply the series by ht (e.g., Blackman–Tukey cosine bell ht = 0.5[1 + cos(2π(t − t̄)/n)]) before computing the DFT; the spectral window becomes Wn(ω) = |Hn(ω)|², modifying the **Fejér kernel** Wn(ω) = sin²(nπω)/(n sin²(πω)) seen with ht ≡ 1.
- **Leakage and sidelobes** — the untapered Fejér window has large sidelobes that smear power from strong components into neighboring bands (leakage); a cosine taper suppresses sidelobes at the cost of slightly wider main lobe.
- **Example 4.16 (smoothed SOI / Recruitment)** — modified Daniell kernel applied twice with m = 3, taper = 0.1 gives Lh = 9.232, B = 0.019, df ≈ 17; tapering more aggressively (Example 4.17) better separates the yearly and four-year peaks.
- **Bandwidth choice and harmonics** — a non-sinusoidal periodic signal (e.g., the constructed signal in Example 4.15) shows up as a fundamental peak plus **harmonics** at integer multiples; smoothing flattens narrow seasonal peaks but preserves the broad El Niño band.
- **Bonferroni adjustment** — for K simultaneous frequencies of interest, test each at α/K; significance against a baseline level should use one-sided lower confidence limits.

## 5. Parametric Spectral Estimation

- **AR spectrum estimator** — fit AR(p) to the data with order chosen by AIC / AICc / BIC, then plug φ̂, σ̂w² into f̂x(ω) = σ̂w² / |φ̂(e^(−2πiω))|² (Property 4.4); preferred when several closely spaced narrow peaks must be resolved (Kay 1988).
- **AR approximation property** (Property 4.7) — any continuous spectral density can be approximated arbitrarily closely by an AR spectrum of finite order p, though p may need to be very large.
- **Example 4.18 (SOI)** — AIC, AICc, and BIC each minimize at p = 15; the AR(15) spectrum reproduces the four-year and one-year peaks plus harmonics seen in the nonparametric estimates.
- **Whittle likelihood** — approximate log-likelihood ln L ≈ −Σ [ln f(ωj; θ) + |d(ωj)|²/f(ωj; θ)] using the asymptotic independence and complex normality of DFTs; useful for fitting parameterized spectra including long-memory models.

## 6. Cross-Spectra and Coherence

- **Cross-spectrum** fxy(ω) = Σ γxy(h) e^(−2πiωh) — Fourier transform of the cross-covariance; complex-valued, written fxy(ω) = cxy(ω) − i qxy(ω) where cxy is the **cospectrum** and qxy is the **quadspectrum**; fyx(ω) = fxy*(ω).
- **Squared coherence** ρ²y·x(ω) = |fyx(ω)|² / [fxx(ω) fyy(ω)] — frequency-domain analog of squared correlation, bounded between 0 and 1; equals 1 at every frequency when yt is an exact linear filter of xt with no noise (Example 4.19, three-point moving average).
- **Estimator and test** — ρ̂²y·x(ω) = |f̂yx(ω)|² / [f̂xx(ω) f̂yy(ω)]; under H0: ρ²y·x(ω) = 0, F = ρ̄²/(1−ρ̄²) · (L−1) is approximately F_{2, 2L−2}, giving threshold Cα = F_{2,2L−2}(α)/[L−1 + F_{2,2L−2}(α)] above which coherence is significant.
- **Example 4.21 (SOI / Recruitment coherence)** — with L = 19, df ≈ 36, C.001 ≈ 0.32; SOI and Recruitment are strongly coherent at the annual cycle and at low (multi-year) frequencies, with peak coherence near a 9-year cycle.

## 7. Linear Filters: Gain, Phase, Frequency Response

- **Filter modifies the spectrum** — yt = Σ aj xt−j has fy(ω) = |A(ω)|² fx(ω); a **low-pass filter** passes slow frequencies, a **high-pass filter** passes fast ones, a **band-pass filter** passes a chosen band.
- **First difference** ∇xt = xt − xt−1 — high-pass; squared frequency response |A(ω)|² = 2[1 − cos(2πω)] rises with ω, attenuating low frequencies and amplifying high (its slow rise makes it imperfect).
- **Centered 12-month moving average** yt = (xt−6 + xt+6)/24 + Σ xt−r/12 for |r| ≤ 5 — low-pass; cuts most power above 1/12 cycles/month, isolating the El Niño component of SOI by removing the annual cycle.
- **Filter gain and phase** (Example 4.23) — Ayx(ω) = |Ayx(ω)| exp{−i φyx(ω)}; the **gain** |Ayx(ω)| is the amplitude multiplier and the **phase** φyx(ω) measures frequency-dependent time delay; symmetric filters (aj = a−j) have zero phase, while a delay filter yt = A xt−D has linear phase φyx(ω) = −2πωD.
- **Filter input/output relationship for cross-spectrum** — fyx(ω) = Ayx(ω) fxx(ω) so the frequency response can be recovered as Ayx(ω) = fyx(ω) / fxx(ω); polar coordinates yield the gain and phase formulas |Ayx|² = (cyx² + qyx²)/fxx² and tan φyx = −qyx/cyx.

## 8. Lagged Regression and Optimum Filtering

- **Lagged regression** yt = Σr βr xt−r + vt — frequency-domain solution B(ω) = fyx(ω)/fxx(ω); estimate B̂(ωk) = f̂yx(ωk)/f̂xx(ωk) and invert via β̂t = M^(−1) Σk B̂(ωk) e^(2πiωkt) for |t| < M/2 (set zero outside).
- **Mean squared error** of the optimal lagged regression — MSE = ∫ fyy(ω)[1 − ρ²yx(ω)] dω; the cleaner the coherence, the smaller the residual variance, exactly mirroring σy²(1 − ρ²) in classical regression.
- **Example 4.24 (SOI → Recruitment)** — with L = 15, M = 32 the impulse response peaks negatively at lag 5 with exponential decay, fitting Recruitment ≈ 66 − 18.5 SOIt−5 − 12.3 SOIt−6 − 8.5 SOIt−7 − 7 SOIt−8; the inverse direction (Recruitment → SOI) is much simpler, motivating an ARMAX model yt = 12 + 0.8 yt−1 − 21 xt−5 + εt with εt = 0.45 εt−1 + wt.
- **Signal extraction (Wiener filter)** — for yt = Σ βr xt−r + vt with signal xt and noise vt, the optimal filter that minimizes E(xt − Σ ar yt−r)² has Fourier transform A(ω) = B*(ω) / [|B(ω)|² + fvv(ω)/fxx(ω)]; in the simple yt = xt + vt case it reduces to A(ω) = SNR(ω)/[1 + SNR(ω)] with SNR(ω) = fxx(ω)/fvv(ω).
- **Example 4.25 (extracting El Niño)** — design a low-pass filter passing frequencies up to 0.05 cycles/month with cosine-tapered coefficients ãt = ht at to suppress ripples; applied to SOI it recovers a smooth El Niño signal cleaner than the centered moving average, which leaks high frequencies.
- **Recursive filters** — yt = Σ φk yt−k + xt − Σ θk xt−k (ARMA-style with input replacing white noise) gives fy(ω) = |θ(e^(−2πiω))|²/|φ(e^(−2πiω))|² · fx(ω); recursive filters distort phase and are generally avoided when phase fidelity matters.

## 9. Multidimensional Spectral Analysis

- **Wavenumber spectrum** fx(ω) = Σh γx(h) e^(−2πiω′h) for spatial coordinates s = (s1,…,sr); ωi is the cycling rate per unit distance in direction i, generalizing time-frequency to spatial frequency.
- **Two-dimensional periodogram and filter** — d(ω1, ω2) = (n1 n2)^(−1/2) Σ xs1,s2 e^(−2πi(ω1 s1 + ω2 s2)); the spatial filter ys1,s2 = Σ au1,u2 xs1−u1, s2−u2 has fy(ω1, ω2) = |A(ω1, ω2)|² fx(ω1, ω2); smoothed estimator f̄x averages the periodogram over an L1 × L2 grid with χ²_{2 L1 L2} confidence approximation.
- **Example 4.26 (soil temperature)** — 64 × 36 spatial grid; the 2D periodogram shows a ridge at column frequency zero with sharp peaks at ±0.0625 cycles per row (period 16 rows ≈ 272 ft), matching the underlying periodic salt-treatment irrigation pattern.
