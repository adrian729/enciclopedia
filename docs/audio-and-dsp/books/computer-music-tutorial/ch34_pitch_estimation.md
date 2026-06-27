# Ch 34: Pitch Estimation

## Table of Contents

- [1. The Pitch Estimation Problem](#1-the-pitch-estimation-problem)
- [2. Applications and Difficulties](#2-applications-and-difficulties)
- [3. Time-Domain Methods](#3-time-domain-methods)
- [4. Frequency-Domain Methods](#4-frequency-domain-methods)
- [5. Perceptual, Neural, and Polyphonic Methods](#5-perceptual-neural-and-polyphonic-methods)

## 1. The Pitch Estimation Problem

- **Pitch estimator (PE)** — also called a *pitch detector* or *pitch tracker*; software/hardware that takes a sound signal and finds its *fundamental pitch period*, i.e. the frequency a human would agree is the signal's pitch (assuming one exists)
- **Inherent limits** — pitch is ambiguous in many sounds (a cymbal crash, impulses, rumblings have no "pitch"); even steady tones have microvariations, so a PE must be "accurate, but not too accurate—like a human listener"
- **MIDI vs acoustic** — parsing MIDI/OSC messages is easy (the input device detects pitch electromechanically); acoustic instruments need a microphone plus detection hardware/software, or a *pitch-to-MIDI converter* (PMC) that emits MIDI values matching the input pitch
- **State of the art** — non-real-time speech PEs are "very reliable" (Hermes 1992); real-time PE is harder, but commercial pitch correction now runs with latencies below 50 ms

## 2. Applications and Difficulties

- **Applications** — *melody transcription* (e.g. the Seeger Melograph producing a *melogram* of pitch and amplitude vs. time); real-time tracking for teaching/improvisation systems; *pitch editing* (Antares Auto-Tune's *pitch correction*, famous as the *Cher effect* from her 1998 hit *Believe*; Celemony Melodyne editing notes inside chords); *un-mixing* (extracting a vocal melody); *automatic dialog replacement* (ADR)
- **Attack transients** — instrument attacks are chaotic and inharmonic; some take over 100 ms to settle, so PEs add a latency/delay before estimating
- **Low frequencies** — at least three steady-state cycles must be sampled first; 55 Hz (A, MIDI 33) needs 54 ms for three cycles, plus attack and computation time, making delay inevitable; favors time-domain methods
- **High frequencies** — fewer samples per period reduce time-domain resolution
- **Legato and melisma** — note changes may have no amplitude change (or no frequency change), yet two events must be detected
- **Myopic pitch tracking** — PEs analyze a narrow 10–100 ms frame and lack human context/expectation, so they may track unintended unsteadiness or excessive vibrato
- **Acoustic ambience** — close miking exaggerates noises (bow scraping, key clicks); reverberation smears notes; non-real-time ambience removal can help

## 3. Time-Domain Methods

- **Fundamental period (periodicity) detection** — treats the signal as fluctuating amplitude (like an oscilloscope trace) and hunts for repeating patterns indicating periodicity
- **Zero-crossing / peak detection** — measures intervals between *zero-crossings* (sign changes) or between peaks; simple and cheap but inaccurate — high-frequency components add spurious crossings, causing octave errors, poor noise performance, and no polyphony. Kuhn (1990) improved it by zero-crossing only the lowest two filter-bank outputs with significant amplitude
- **Autocorrelation** — compares a signal with versions of itself delayed by successive *lags*; correlation of 1 means identical, 0 means uncorrelated. Autocorrelation of a sine is itself a sine peaking at integer multiples of the period; recurrent peaks reveal (possibly hidden) periodicities. Formula: \( \text{autocorrelation}[lag] = \sum_n \text{signal}[n] \cdot \text{signal}[n + lag] \), for \( 0 < lag \le N \)
- **Autocorrelation traits** — best at mid-to-low frequencies; direct computation needs millions of multiply-adds per second, so it is often computed via FFT (multiply spectrum by its complex conjugate, then inverse FFT). The *normalized square difference function* (McLeod and Wyvill 2005) and *YIN* (de Cheveigné and Kawahara 2002, which minimizes difference rather than maximizing product and suppresses subharmonics) are refinements
- **Adaptive filter** — a self-tuning narrow bandpass filter whose center frequency is driven by a *difference detector* until it converges on the input frequency. The *optimum comb method* (Moorer 1973) tunes comb-filter notches to minimize the input. Das et al. (2020) used an extended Kalman filter

## 4. Frequency-Domain Methods

- **FD basics** — start from the spectrum (via the *short-time Fourier transform*, STFT) and find peaks, then decide which are fundamentals versus harmonics/partials; a fundamental may be the perceived pitch even when not the strongest component
- **Linear-bin limitation** — STFT bins are equally spaced \( n \) Hz apart, but pitch perception is logarithmic, so low pitches resolve poorly (20 Hz resolution gives microtones near 10–20 kHz but under a semitone below middle C)
- **Constant-Q transform** — Brown and Puckette (1993) frequency-warp the FFT onto a logarithmic grid (constant \( Q \)) and match against an ideal harmonic template
- **Tracking phase vocoder (TPV)** — unlike fixed STFT channels, generates frequency-changing *tracks* of prominent partials, "sanitizing" the input by attenuating noise/ambience; Beauchamp, Maher, and Brown (1993) estimate the fundamental as the harmonic hypothesis with least overall difference
- **Cepstrum** — the inverse Fourier transform of the *log-magnitude Fourier spectrum* (name is "spectrum" with its first four letters reversed); separates *excitation* (pitched vibration) from *resonances* (instrument body / vocal tract). A peak gives the fundamental period; no peak signals *unvoiced* (breathy/consonant) sound. It effectively *deconvolves* the two convolved spectra
- **Maximum likelihood (MLE)** — statistically matches STFT data to known harmonic frequency maps, assuming the strongest partial belongs to the fundamental's series

## 5. Perceptual, Neural, and Polyphonic Methods

- **Ear-model PEs** — three submodels (outer/middle ear, cochlea, central nervous system); a filter bank, then transduction into nerve-firing spike trains, then time-domain interval estimation. Combining FD and time-domain stages filters out inharmonic contamination
- **Neural networks** — *CREPE* (Convolutional Representation for Pitch Estimation, Kim et al. 2018) runs six convolutional networks on 64 ms time-domain grains, trained on 15 hours of labeled audio, outputting 360 pitches at 20-cent resolution
- **Polyphonic detection** — sifts one or more melodic lines from a spectrum of many peaks (fundamentals or strong harmonics) using *expectation-driven search* and AI heuristics. Paiva et al. (2006) used *salience* (loudest) and *smoothness* (stepwise) rules, then eliminated *ghost octaves* and *false positives*, reaching an 81% melody-identification rate; computation far exceeds the monophonic case
- **Analysis of musical context** — beyond detection: identifying key, clef, and correct note spelling (F-sharp vs. G-flat) for transcription, and fast chord/melodic analysis for interactive performance systems
