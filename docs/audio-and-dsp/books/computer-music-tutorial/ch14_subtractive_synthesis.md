# Ch 14: Subtractive Synthesis

## Table of Contents

- [1. Principle and Background](#1-principle-and-background)
- [2. How Filters Work](#2-how-filters-work)
- [3. Filter Types and Response](#3-filter-types-and-response)
- [4. Q, Gain, and Phase](#4-q-gain-and-phase)
- [5. Filter Banks, Comb, and Allpass](#5-filter-banks-comb-and-allpass)
- [6. Analysis/Resynthesis: Vocoder and LPC](#6-analysisresynthesis-vocoder-and-lpc)

## 1. Principle and Background

- **Subtractive synthesis** — uses *filters* to shape the spectrum of a spectrally rich source (impulse trains, sawtooth waves, white noise); the filter carves selected regions of the spectrum, hence "subtractive," though it can cut *or* boost
- **Colored noise** — passing white noise through a filter yields *colored noises*, an electronic-music staple (e.g., Milton Babbitt's RCA Synthesizer works *Vision and Prayer*, 1961)
- **Subtractive tone forming** — analog filters shaping raw tone-generator waveforms typified early instruments (Mixtur-Trautonium, RCA Synthesizer) and standalone units like the Albis Tonfrequenz filter at the WDR studio; *voltage-controlled filters* defined the first modular-synthesizer era
- **Digital filtering** — advanced in the 1960s with the *Z-transform calculus*, introducing *stability* and *causality*; real-time digital filters appeared in 1980s research machines (Stanford's Systems Concepts Digital Synthesizer, IRCAM's 4X, GRM's SYTER) before becoming cheap a decade later

## 2. How Filters Work

- **What a filter is** — technically any operation with an input and output; in audio, a device that boosts or attenuates spectral regions
- **Feed-forward filter** — delays a copy of the *input* signal by one or more sample periods and combines it with the new input
- **Feedback filter** — delays a copy of the *output* signal and combines it with the input
- **Mechanism** — tiny delays cause *phase cancelation* (attenuation) and *phase reinforcement* (boost). A 100 Hz signal (period 10 ms) delayed by 10 ms is in phase → boost; delayed by 5 ms it is 180° out of phase → cancelation. Combination can be by sum (+) or difference (−)

## 3. Filter Types and Response

- **Frequency response (FR)** — the amplitude-versus-frequency (magnitude) response curve; a flat/linear FR passes all frequencies without boost or attenuation
- **Four basic types** — *lowpass* (passes lows, cuts highs), *highpass* (opposite), *bandpass* (passes a middle band), *bandreject/notch* (passes all but a band)
- **Shelving filters** — boost or cut all frequencies above (*high shelving*) or below (*low shelving*) a threshold; a high shelf set to cut equals a lowpass
- **Cutoff frequency** — the point where the filter reduces the signal to 0.707 of maximum; also the *half-power point* (since \( 0.707^2 = 0.5 \), power ∝ amplitude squared) and the *3 dB point* (0.707 ≈ −3 dB). Components below it are in the *stopband*, above in the *passband*
- **Ideal vs actual** — an ideal filter splits cleanly into passband and stopband; real filters show *ripple* and a *transition band* between them
- **Slope** — steepness in dB/octave: 6 dB/octave is a smooth *rolloff*, 24 dB/octave a sharp cutoff, 96 dB/octave a *brickwall* filter

## 4. Q, Gain, and Phase

- **Q** — the degree of resonance of a bandpass filter; high Q gives a sharp peak that *rings* (oscillates) at the resonant frequency. Defined as center frequency over −3 dB bandwidth: \( Q = \frac{center}{highcutoff - lowcutoff} \). Example: center 2000 Hz, 3 dB points 1800 and 2200 Hz → \( Q = 2000 / (2200 - 1800) = 5 \). High-Q filters excited by a pulse train simulate tuned drums (tablas, wood blocks, marimba)
- **Constant Q filter** — varies bandwidth proportionally to center frequency to hold Q fixed (e.g., Q 1.5 → 20 Hz bandwidth at 30 Hz, 6000 Hz bandwidth at 9 kHz); spans the same musical interval at any center frequency; appears as a *third-octave filter bank* in sound level meters
- **Gain** — amount of boost or cut of a band; high-Q gain can overload the system, so *gain-compensation* circuits exist
- **Phase response vs latency** — a *linear-phase filter* shifts all frequencies by a constant time (*group delay*), avoiding phase distortion but adding *latency* (up to >500 ms) and possible pre-echoes; a *zero-latency filter* is efficient and instant but introduces *phase distortion* that blurs transients — best for live performance

## 5. Filter Banks, Comb, and Allpass

- **Filter bank / spectrum shaper** — parallel filters splitting a sound into *subbands*; with per-filter level controls it becomes a spectrum shaper
- **Graphic equalizer** — a spectrum shaper whose faders mirror the FR curve; each filter has fixed center frequency, bandwidth, and Q. A *parametric equalizer* has fewer filters but independently adjustable center frequency, Q, and cut/boost; a *semiparametric* equalizer has fixed Q
- **Comb filter** — has regularly spaced peaks/troughs (delays up to 10 ms); recognizable timbre, used to vary sounds; continuously varying the delay gives *flanging*
- **Allpass filter** — passes all frequencies with unity gain for steady-state input but introduces a frequency-dependent phase shift; colors time-varying signals (especially transients), can correct another filter's phase shift, and serves as an *impulse diffuser* in Schroeder-model reverberators
- **Time-varying subtractive synthesis** — *fixed* filters are set once (in mixing, called *EQ* / equalization); music wants *time-varying* control of center/cutoff frequency, bandwidth, gain, and Q. The signature Moog sound was a sawtooth through a sweeping high-Q lowpass (Moog 904); GRM's SYTER realized dozens of real-time high-Q bandpass filters (Risset's *Sud*, 1985)

## 6. Analysis/Resynthesis: Vocoder and LPC

- **Analysis/resynthesis** — an initial analysis stage enhances subtractive synthesis; most techniques originate in speech research
- **Vocoder (channel vocoder)** — demonstrated 1936; stage 1 is a bank of fixed bandpass filters each feeding an *envelope detector* that outputs energy at its band; stage 2 is an identical filter bank whose outputs feed *voltage-controlled amplifiers* (VCAs) driven by stage-1 control signals (*driving functions*). Source A supplies the *spectrum envelope*, source B the *excitation function* (white noise or pulse train) supplying pitch — separating rhythm, pitch, and timbre and enabling *cross-synthesis* (the *talking orchestra* effect)
- **Linear predictive coding (LPC)** — a flexible vocoder that data-reduces a sound (e.g., voice) and resynthesizes an approximation; separates excitation from spectrum envelope so pitch, rhythm, and timbre are independently editable (Dodge's *Speech Songs*, 1973). *Voiced* sounds (vowels, vocal-cord buzz) vs *unvoiced* (consonants like *s*, *f*); a third *mixed voice* category combines tone and noise
- **What linear prediction is** — output samples are predicted by a linear combination of filter *coefficients* and previous samples; the known input gives the error estimate. Because the predictor sums time-delayed samples, it acts as a filter describing the waveform; a side effect is estimating the input's spectrum
- **LPC analysis** — branches into spectrum (formant) analysis, pitch analysis, amplitude analysis, and the voiced/unvoiced decision, all frame-by-frame (50–200 frames/s). Filter poles are resonances/formants, zeros are notches; an *allpole filter* (smooth peaks) models voice and instruments. *Autoregressive* analysis fits an inverse (*allzero*) filter, leaving a *residual* (excitation plus noise) to minimize; the inverse is then inverted (FIR → IIR) for resynthesis. *Code-excited linear prediction* mixes pitched pulses and noise from a codebook to reduce artificiality
- **Frame data** — each frame carries residual amplitude (RMS1), original amplitude (RMS2), their ratio (ERR — a value >0.2 signals unvoiced), estimated PITCH, duration (DUR), and allpole coefficients
- **LPC synthesis and editing** — voiced frames drive a bandlimited pulse train, unvoiced frames a noise generator, both shaped by amplitude and fed to the allpole filter (up to 12 poles for speech, up to 250 for music). An editing language sets pitch, trills, time-stretches, interpolates glissandi, and rearranges frames to turn speech into song
- **Cross-synthesis and WaveGAN** — LPC cross-synthesis takes excitation (pitch, timing) from one sound to drive the spectral envelope of another (wideband sources like full orchestra make speech most intelligible); *warped linear prediction* clones an instrument family (violin → viola, cello, bass). *WaveGAN* is experimental *adversarial audio synthesis*: a neural network filters random noise into waveforms that fool a *discriminator* (classifier), generating up to 4 s at 16 kHz
