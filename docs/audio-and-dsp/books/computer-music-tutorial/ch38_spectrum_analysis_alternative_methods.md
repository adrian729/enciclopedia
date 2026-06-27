# Ch 38: Spectrum Analysis by Alternative Methods

## Table of Contents

- [1. Why Look Beyond Fourier](#1-why-look-beyond-fourier)
- [2. Constant-Q Filter Banks](#2-constant-q-filter-banks)
- [3. Wavelet Analysis](#3-wavelet-analysis)
- [4. The Wigner Distribution](#4-the-wigner-distribution)
- [5. Autoregression and Source-Parameter Methods](#5-autoregression-and-source-parameter-methods)
- [6. Walsh, Prony, and Auditory Models](#6-walsh-prony-and-auditory-models)

## 1. Why Look Beyond Fourier

- **Limits of the STFT** — Fourier methods struggle with transients: limited frequency resolution over short time scales, spectral *leakage* from windowing, inefficiency (non-sparseness) on noisy sounds it must model as hundreds of harmonic sinusoids (a "data explosion"), and the premise of periodicity that blurs aperiodic structure
- **No best method** — Kay and Marple (1981) show one input (three sinusoids plus a noise band) yielding wildly different results across techniques; Fourier methods cannot even separate the sinusoids from the noise, while some methods misrender the noise band as five sinusoids. The right choice depends on what you are looking for

## 2. Constant-Q Filter Banks

- **Constant-Q principle** — \( Q \) is a bandpass filter's center frequency divided by its bandwidth; in a constant-Q bank every filter shares the same \( Q \), so high-frequency filters are wide and low-frequency filters narrow. Analysis is on a logarithmic (musical-interval) frequency scale
- **vs Fourier** — Fourier bins have constant width (Nyquist rate / number of bins; e.g. a 1024-point FFT at 48 kHz gives 23.43 Hz bins), which wastes resolution at high frequencies the ear cannot resolve while failing to separate low semitones like E1 (41.2 Hz) and F1 (43.65 Hz) without a huge window. Constant-Q varies window length with frequency: long windows for low frequencies, short for high
- **Advantages** — concentrates temporal uncertainty in the low octaves (good time localization of high-frequency transients/attacks); matches the ear, whose response resembles constant-Q above 500 Hz (the *critical bands*); needs far fewer channels (often under 100 vs hundreds-to-thousands for the STFT). Related is the *Bark frequency scale* (critical-band) method
- **Implementation** — the direct filter-bank method is computationally inefficient, so constant-Q is built from FFT data or by *frequency warping* an FFT filter, or formulated within wavelet theory. Invertibility (resynthesis) is not guaranteed by every implementation

## 3. Wavelet Analysis

- **Wavelet** — a brief burst of sound energy (similar to a granular grain) with a precise start time, duration, frequency, and phase. The *wavelet transform* (WT) is a time-frequency method from the University of Marseille; the term and its French *ondelette* described energy packets from atomic processes
- **Correlation and feature detection** — a wavelet correlates with a signal containing a similar pattern, so wavelets can be designed to highlight arbitrary features (e.g. a middle-C wavelet flags short middle-C notes; an octave-detection wavelet is the sum of two wavelets an octave apart)
- **Non-uniform tiling** — unlike the STFT's uniform grid, the WT tiles the time-frequency plane non-uniformly: low frequencies long-in-time and narrow-in-frequency, high frequencies short and wide, so a cymbal crash is invisible to *slow* wavelets but caught by *fast* ones. Frequency warping (Evangelista) allows arbitrary, curved-boundary tilings
- **Basis and dilation** — wavelets scaled and time-shifted form an analysis *basis*; an individual wavelet is a *basis function* (as a sine wave is for Fourier). A wavelet always holds a constant number of cycles regardless of frequency, so its window stretches (*dilation*) or shrinks (*contraction*) with the analyzed frequency, trading frequency for time resolution at high frequencies and vice versa. The popular *Morlet* wavelet has a Gaussian envelope. The *fast wavelet transform* (FWT) is a recursive algorithm (Mallat, Daubechies)
- **Display** — the WT output has a *modulus* (magnitude) image and a *phasogram* (phase) image, plotting time horizontally and log frequency vertically; short wavelets sit at a triangle's apex as time-localized *pointers* to transient onsets, long wavelets spread along the bottom
- **Resynthesis and transformation** — done by overlap-add or additive synthesis. Transformations include suppressing frequency channels (filtering), extracting chords (a "harmonic" talking voice), cross-synthesis (amplitude of one sound, phase of another), and frequency/time-grid warping requiring *phase unwrapping*. Substituting Haar's boxcar wavelet for synthesis after a smooth analysis adds noisy distortion
- **Gabor transform (GT)** — straddles wavelets and the STFT; its element, the *gaboret*, is a Gaussian-windowed sine (a *Gaussian atom* in atomic decomposition). Used in Arfib and Delprat's Sound Mutations for pitch-time changing, cross-synthesis, and vibrato modification
- **Comb wavelet transform** — Naples-developed method that fits a comb filter aligned to a fundamental's harmonics to sift out the harmonic ("clean") spectrum; subtracting the inverse WT leaves the "dirty" residual (attack transient and character), enabling cross-synthesis by grafting one sound's dirty part onto another's clean part. *Pink noise* (1/\( f \), −3 dB per octave) can model stochastic components

## 4. The Wigner Distribution

- **Wigner distribution (WD)** — from 1930s quantum physics (Wigner 1932); in acoustics its goal is *system* analysis (the response of a loudspeaker, transducer, or circuit) rather than sound analysis, producing a frequency-versus-time plot
- **Reading a WD plot** — a horizontal slice's area gives the frequency response (magnitude squared) at that frequency and its *center of gravity* gives the *group delay*; a vertical slice's area gives *instantaneous power* and its center of gravity gives *instantaneous frequency*; plotting these over time reveals amplitude and frequency modulation
- **Nonlinearity (clutter)** — the WD of a sum is not the sum of WDs: summing 100 Hz and 300 Hz sinusoids produces a spurious 200 Hz *interference* component (their difference) not present at the input, making visual inspection difficult. The sampled, windowed version is the *pseudo-Wigner distribution*
- **Wigner-Ville distribution (WVD)** — used heavily in atomic decomposition (Ch 39); has time-frequency resolution superior to the spectrogram and does not spread impulses, sinusoids, or Gaussians, but still suffers interference. Superposing the WVD of each separate atom yields a clutter-free composite display Sturm et al. (2009) call a *wivigram*

## 5. Autoregression and Source-Parameter Methods

- **AR family** — *autoregression* (AR), *linear predictive coding* (LPC), and *maximum entropy methods* (MEM) design a filter matching the input spectrum; they estimate a spectrum from little data (better potential time/frequency resolution) but model sound as an *excitation* (e.g. glottal pulses) applied to a *resonator* (vocal tract), estimating spectral peaks/resonances rather than tallying frequencies
- **How AR works** — it predicts the \( t \)th sample as a sum of past samples weighted by \( p \) filter coefficients; inverting the fitted inverse filter gives the spectrum estimate. The order \( p \) is delicate: too low over-smooths, too high adds spurious peaks; iterative methods stop when goodness-of-fit stops improving. *Linear regression* computes the coefficients via matrix operations (hence "autoregression"); LPC is best at extracting spectral peaks, while the cepstrum finds the overall envelope
- **ARMA** — the *autoregressive moving average* generalization combines past inputs *and* past outputs, giving a filter with both poles and zeros; more accurate for sounds with spectral holes (nasal vowels) or percussive impulses where plain AR's prediction error is large, but much more costly
- **Source and parameter analysis** — recovers source information (size, mass, geometry, material) rather than just frequencies, useful for snare hits and cymbals and for separating mixed sources. All analysis is a form of *parameter estimation* — finding the synthesis settings that approximate a sound — using *adaptive* algorithms that minimize error; no universal analysis/resynthesis technique is optimal for all sounds (FM parameter estimation, for instance, gave only gross approximations)

## 6. Walsh, Prony, and Auditory Models

- **Walsh functions** — square (binary-pulse) waves as the decomposition basis; natural for digital implementation, but they break a signal into *sequencies* not directly related to the frequency domain
- **Prony's method** — uses *damped sinusoids* (sharp attack, exponential decay) as basic units; named after Gaspard Riche, Baron de Prony, who analyzed gas expansion. It models a signal as damped sinusoids plus noise, driving frequency, damping, amplitude, and phase (yielding phase data for accurate resynthesis), turned into spectrum analysis via the FFT of its output
- **Prony vs Fourier** — Prony is far more parameter-sensitive (poorly set parameters give incoherent spectra, whereas Fourier is "never totally incoherent"), but properly tuned it resolves inharmonic partials and closely spaced sinusoids that Fourier lumps into formant-like peaks. It is limited to about fifty partials (polynomials stop converging) and is more computationally intensive; LaRoche used it well on damped percussion (glockenspiel, vibraphone, marimba, gong) but poorly on high piano tones and cymbals
- **Auditory models** — analysis methods modeled on hearing, including the *mel frequency cepstrum*, *cochleagrams*, and *correlograms*
- **Higher-order spectrum analysis** — a further alternative family beyond second-order (power) spectra
