# Ch 36: Introduction to Spectrum Analysis

## Table of Contents

- [1. What Spectrum Analysis Is](#1-what-spectrum-analysis-is)
- [2. Applications](#2-applications)
- [3. Spectrum Plots](#3-spectrum-plots)
- [4. Analysis Models and Timbre](#4-analysis-models-and-timbre)
- [5. Historical Background](#5-historical-background)

## 1. What Spectrum Analysis Is

- **Spectrum analysis** — gauging the balance among a sound's elementary acoustic components, each corresponding to a rate of variation in air pressure; by analogy, decomposing sound the way an image decomposes into colors
- **Working definition** — *a measure of the distribution of signal energy as a function of frequency*; no more precise general definition exists because different techniques measure diverging things they each call "spectrum"
- **Spectrum estimation** — since results approximate the true spectrum, the practice is better called *spectrum estimation* than analysis; it is not an exact science
- **Time-frequency (TF) analysis** — measuring a spectrum as it evolves in time; the output is a *time-frequency (TF) representation*. Musicians use analysis not only to measure but to modify and transform sound

## 2. Applications

- **Engineering and restoration** — acoustic measurement of rooms, voices, instruments; tuning sound-reinforcement systems with test tones; restoring old recordings (clicks, hum) and *source separation* — famously substituting a new orchestra behind Enrico Caruso's voice
- **Compression and retrieval** — fundamental to MP3 and AAC audio compression; enables *music information retrieval* (MIR) and recommendation via *audio descriptors*; *adaptive audio effects* map descriptors to effect parameters (a process called *sidechaining*)
- **Analysis and interaction** — psychoacoustics (correlating spectrum with perception), musicology, artistic VJ visualization, automatic transcription, and real-time machine listening for interactive systems
- **Transformation** — many techniques begin with an analysis stage: time compression/expansion, frequency shifting, convolution (filtering, reverberation), and *cross-synthesis* (hybridizing two sounds)

## 3. Spectrum Plots

- **Static vs. time-varying** — static plots are a snapshot (amplitude vs. frequency, averaging energy over the analysis *window*); time-varying plots are like a motion-picture film of an evolving spectrum
- **Window trade-off** — the analysis window can span a brief instant to several seconds; window length governs a trade-off discussed throughout
- **Line (discrete) spectrum** — a vertical line per frequency component; clearest via *pitch-synchronous* analysis, which measures harmonic amplitudes of a tone whose pitch is known beforehand (a trumpet's third harmonic can exceed its fundamental)
- **Continuous plot and spectral envelope** — interpolating between discrete points hides individual sinusoids but reveals the *spectral envelope* (overall shape); a dB scale compresses amplitude differences into a narrow band, exposing formant peaks
- **Power spectrum** — the square of the amplitude spectrum (physicists define *power* as amplitude squared); correlates better with perception. *Power spectrum density* (PSD) is power per bandwidth, used for continuous spectra like noise
- **Time-varying displays** — a 3-D spectrum-vs-time graph stacks static plots; the *waterfall display* scrolls the time axis in real time; the *sonogram* (or *spectrogram*, originally *visible speech*) plots frequency vertically, time horizontally, and amplitude as trace darkness

## 4. Analysis Models and Timbre

- **No universal method** — no spectrum estimation method is ideal for all applications; Fourier analysis is itself an evolving family of techniques. As Risset observed, one must scrutinize the sound and ask which features matter to the ear
- **Model fitting** — every technique fits input data to an assumed model: Fourier models sound as a sum of harmonically related sinusoids; others use excitation-plus-resonance, damped sinusoids, inharmonic sinusoids, or formant peaks with noise. Performance differences trace to how well the assumed model matches the actual sound
- **Spectrum vs. timbre** — *spectrum* is a physical energy-vs-frequency distribution; *timbre* is a perceptual catchall. Formally, timbre is what can vary in a tone without affecting pitch, duration, or loudness — letting us identify a piano on any note
- **Timbre cues** — attack morphology, amplitude envelope, vibrato/tremolo, formants, loudness, duration, and the time-varying spectral envelope; amplitude and duration matter (a flute tone at 120 dB is heard as a loud blast). Grey (1975, 1978) mapped a 3-D *timbre space* where similar tones cluster
- **MPEG-7 timbre descriptors** — introduced in 2002, the first set of mathematically defined, perceptually relevant timbre terms stored as file *metadata*. Examples: *audio spectral centroid* (center of gravity, a "brightness" indicator), *audio spectral spread*, *audio spectral flatness* (flags tonal components), *harmonicity* (harmonic vs. inharmonic vs. nonharmonic), *log attack time*, and *temporal centroid* (distinguishing a decaying piano note from a sustained organ note). It focuses on sustained harmonic and percussive sounds; describing "noises" remains undone

## 5. Historical Background

- **Origins of the term** — Newton coined *spectrum* (1781) for prism color bands; Fourier's *Analytical Theory of Heat* (1822) proved any periodic function is an infinite sum of sine and cosine terms (*harmonic analysis*). Ohm (1843) first applied it to acoustics; Helmholtz (1885) tied instrumental timbre to the steady-state harmonic series
- **Mechanical analyzers** — Lord Kelvin's gear-and-pulley harmonic analyzer (1870s) integrated hand-traced waveforms; the Michelson-Stratton analyzer (1898) resolved up to 80 harmonics and could resynthesize (the *inverse Fourier transform* reconstructs a waveform from spectrum data)
- **Toward continuous spectra** — Tyndall coined *clang-tint* for Helmholtz's *Klangfarbe*; Wiener's *generalized harmonic analysis* (1930) shifted emphasis from harmonics to a continuous spectrum, showing white noise contains all frequencies equally
- **The FFT and Gabor** — digital Fourier transforms (1940s) were costly until the *fast Fourier transform* (Cooley and Tukey 1965) slashed the computation. Gabor (1946–1947) gave a method for time-varying signals — the basis of the *short-time Fourier transform* (STFT) — analyzing sound into *quanta*, now called *grains, wavelets, atoms,* or *frames*
- **Computer-based analysis** — Mathews and Risset analyzed brass at Bell Labs with *pitch-synchronous* analysis (breaking the waveform into pseudoperiodic segments sized to the estimated pitch). *Heterodyne filters* multiplied the input by sine and cosine at harmonic frequencies and summed, good for resolving harmonics but confused by attacks under 50 ms and pitch changes over \~2%
- **The phase vocoder (PV)** — Flanagan and Golden (1966) built the first PV as a speech-coding method, but it causes a *data explosion* (analysis data far exceeds the input). Portnoff (1976–1980) made it efficient via the FFT, leading to Moorer's landmark 1978 application of the PV to computer music
