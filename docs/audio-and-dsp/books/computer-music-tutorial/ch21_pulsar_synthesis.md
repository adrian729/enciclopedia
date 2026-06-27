# Ch 21: Pulsar Synthesis

## Table of Contents

- [1. Anatomy of a Pulsar](#1-anatomy-of-a-pulsar)
- [2. Pulsaret-Width Modulation and Time Scales](#2-pulsaret-width-modulation-and-time-scales)
- [3. Spectra of Basic Pulsar Synthesis](#3-spectra-of-basic-pulsar-synthesis)
- [4. Advanced Pulsar Synthesis](#4-advanced-pulsar-synthesis)
- [5. Implementations and Applications](#5-implementations-and-applications)

## 1. Anatomy of a Pulsar

- **Pulsar synthesis (PS)** — Roads' own digital method generating pulses and pitched tones, named after spinning neutron stars whose periodic signals fall in the \~0.25–642 Hz range between rhythm and tone; it belongs to the *microsonic* / *particle synthesis* family alongside granular synthesis
- **Pulsar** — a single particle of sound: an arbitrary *pulsaret* waveform \( w \) of period \( d \) followed by a silent interval \( s \). Total duration \( p = d + s \), where \( p \) is the *pulsar period* and \( d \) is the *duty cycle*. Repetitions form a *pulsar train*
- **Two frequencies** — fundamental \( f_p = 1/p \) (typically 1 Hz–5 kHz) controls the rate of pulsar emission; duty-cycle frequency \( f_d = 1/d \) (typically 80 Hz–10 kHz) acts as a *formant frequency*. Both are continuously variable, each driven by its own envelope across the train
- **Pulsaret waveform \( w \)** — can be any shape: sine, multicycle sine, bandlimited pulse, decaying sinusoid, even the cosmic waveform of neutron star Vela X-1
- **Pulsaret envelope \( v \)** — the rectangular window time-limiting \( w \) can also be any shape (rectangular, Gaussian, linear/exponential decay or attack, FOF, bipolar modulator); the FOF formant-synthesis envelope is a special case of PS. The envelope strongly shapes the spectrum
- **Filterless formant sweep** — holding \( p \) and \( w \) constant while varying \( d \) produces the effect of a resonant filter swept across a tone, though no filter exists; the duty-cycle frequency appears as a movable formant peak

## 2. Pulsaret-Width Modulation and Time Scales

- **Pulsaret-width modulation (PulWM)** — extends analog *pulse-width modulation* (PWM, which varies a rectangular pulse's duty cycle to add/remove odd harmonics). PulWM allows any pulsaret waveform and lets \( f_d \) drop to or below \( f_p \); when \( d > p \) the fundamental period cuts the pulsaret mid-waveform, smoothed by a user-set *edge* factor crossfade
- **Overlapped PulWM (OPulWM)** — the fundamental period is purely the emission rate; each pulsaret's duty cycle always completes, so when \( d > p \) successive pulsars overlap (subject to an overlap limit), yielding a subtler, more phase-canceled effect than PulWM
- **Synthesis across time scales** — PS spans infrasonic pulsation to audio frequency in one continuum. Below \~one twentieth of a second between impulses, *forward masking* fuses them into a continuous tone; reliable pitch emerges around 40 Hz, so for \( p \) between \~25 ms (40 Hz) and 200 µs (5 kHz) listeners hear pitch
- **Pulsar graph of rhythm** — when \( f_p < 20 \) Hz pulsars are heard individually; between thirty-second-note (62.5 ms) and two-tied-whole-note (8 s) spans (at quarter = 60 MM) the fundamental-frequency envelope becomes a drawable graph of rhythm, plotting note values against frequency (e.g. 5 Hz = a quintuplet)

## 3. Spectra of Basic Pulsar Synthesis

- **Spectrum formula** — the pulsar stream's spectrum is the convolution product of \( w \) and \( v \), biased in frequency by \( f_d \) and \( f_p \); because all four are arbitrary/continuous, the range of producible spectra is very large
- **Spectral template** — \( w \) acts as a spectrum-shape template repeating at \( f_p \) and time-scaled by \( f_d \); a harmonic amplitude ratio (e.g. 5:4:3:2:1) is preserved independent of \( p \) and \( d \) when \( f_p \le f_d \)
- **Envelope shapes the profile** — a rectangular \( v \) gives a broad *sinc* spectrum with peaks at 1.5\( f_d \), 2.5\( f_d \), … and nulls at harmonics of \( f_d \); an *expodec* (exponential-decay) envelope smooths these peaks and valleys; a Gaussian envelope concentrates energy around the central formant frequency

## 4. Advanced Pulsar Synthesis

- **Three principles** — advanced PS adds (1) multiple pulsar generators sharing one fundamental but with individual formant and spatial trajectories, (2) pulsar masking to shape rhythm, and (3) convolution of pulsar trains with sampled sounds
- **Seven generator parameters** — train duration, fundamental-frequency envelope \( f_p \), formant-frequency envelope \( f_d \), pulsaret waveform \( w \), pulsaret envelope \( v \), amplitude envelope \( a \), and spatial path \( s \); adding trains with shared \( f_p \) but separate formant trajectories \( f_{d1}, f_{d2}, … \) builds complex multi-resonance tones, each formant able to follow its own spatial path
- **Pulsar masking** — deletes individual pulsarets to introduce intermittency, in three forms: *burst masking* (regular on-off pattern set by *burst ratio b:r*, modeling tone-burst generators like the Krohn-Hite 5300A, dividing the fundamental into a subharmonic \( b+r \)); *channel masking* (deletes pulsars in alternate channels to create N-channel dialog); *stochastic masking* (a probability envelope, where values 0.8–0.9 mimic an erratic analog contact)
- **Convolution with sampled sounds** — convolving an infrasonic pulsar train with a sampled object replaces each impulse with a filtered, spatially placed copy, mapping the sound into the train's rhythm; short, sharp-attack samples (rise time under 100 ms, e.g. percussion) preserve rhythm, while long or slow-attack samples smear the stream into a continuum

## 5. Implementations and Applications

- **Software lineage** — the author first implemented PS in 1991 in James McCartney's Synth-O-Matic; *PulsarGenerator* (Alberto de Campo and Roads, CNMAT/CREATE) added control envelopes saved as crossfadeable *settings* in SuperCollider, achieving over 6,000 pulsars/second
- **nuPG** — Marcin Pietruszewski's newer SuperCollider version combining graphic interaction with live coding; extensions include *sieve-based masking* (Xenakis sieves with logical operators), matrix modulation (sine, saw, chaotic hennon, latocarfian, stochastic gendyn modulators), parameter linkage, and per-pulsar modulation
- **Nuklear** — Hamburg Audio's plug-in making PS playable from a MIDI keyboard, with LFOs and a 16-step sequencer
- **Musical works** — Roads developed PS for *Clang-tint* (1993, movement *Organic*), used asynchronous pulsar clouds (multiple infrasonic trains beating at 6–18 Hz); *Half-life* (1998–99) derives an entire work from one varying one-minute pulsar train via granulation and feedback; *Tenth/Eleventh vortex* are granulations and *Pictor alpha* (2003) is pure PS
- **Assessment** — unlike wave-oriented synthesis, rhythm is built into particle techniques; PS seamlessly links the time scales of particle rhythm, periodic pitch, and the phrase level, with independent formant trajectories each on its own spatial path
