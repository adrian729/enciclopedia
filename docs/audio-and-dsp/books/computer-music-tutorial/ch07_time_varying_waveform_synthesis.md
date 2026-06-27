# Ch 7: Time-Varying Waveform Synthesis

## Table of Contents

- [1. Envelopes, Unit Generators, and Patches](#1-envelopes-unit-generators-and-patches)
- [2. Graphic Notation for Synthesis Instruments](#2-graphic-notation-for-synthesis-instruments)
- [3. Using Envelopes in Patches](#3-using-envelopes-in-patches)

## 1. Envelopes, Unit Generators, and Patches

- **Why time-varying waveforms** — a fixed-frequency sine has constant loudness and controls only pitch and duration; the key to interesting sounds is changing one or more synthesis parameters over the duration of a sound event
- **Envelope** — a function of time that controls a parameter; e.g. the *amplitude envelope* is the curve the amplitude follows over a sound's duration
- **Unit generator (UG)** — the fundamental building block of digital synthesis, either a *signal generator* (e.g. an oscillator, which synthesizes waveforms and envelopes) or a *signal modifier* (e.g. a filter, which transforms an input signal)
- **Patch** — an instrument built by interconnecting UGs, where one UG's output number becomes another's input. The term comes from modular synthesizers connected by *patch cords*, though in software no physical wires exist

## 2. Graphic Notation for Synthesis Instruments

- **Origin of the notation** — the graphic notation for drawing patches was invented to explain the first modular synthesis languages, Music 4BF (Howe 1975) and Music V (Mathews 1969), and is still useful
- **Unique UG shapes** — each unit generator has its own symbol; the *table-lookup oscillator* called *osc* takes three inputs — amplitude, frequency, and a waveform stored in wavetable *f*1 — and outputs *f*1 repeated at the stated frequency and amplitude

## 3. Using Envelopes in Patches

- **Constant vs. varying amplitude** — feeding a constant (e.g. 1.0) to an oscillator's amplitude input gives constant loudness; most interesting sounds instead use an amplitude envelope that rises from 0 to a peak and falls back to 0
- **Attack and release** — the rising beginning of an envelope is the *attack*; the dying-away end is the *release*
- **Normalization** — a *normalized* wave is scaled to standard bounds: 0 to 1 for amplitude envelopes, or \( -1 \) to \( +1 \) for other waves
- **ADSR** — the common four-stage envelope: **A**ttack (zero to peak), **D**ecay (down to a sustained level), **S**ustain (constant level), **R**elease (return to zero). Good for describing a shape verbally ("make the attack sharper") but limiting for precise specification — flexible editors let musicians trace arbitrary curves
- **Adding an envelope** — connecting an envelope to an oscillator's amplitude input gives time-varying loudness; setting the envelope's duration and curve makes it control each note's amplitude
- **Envelope generator (env_gen)** — a UG that takes a duration, a peak amplitude, and a wavetable; it reads the envelope wavetable *f*1 over the specified duration, scaled by the peak, so it adapts to tones of any duration (here the sound waveform is *f*2), sparing the composer from hand-designing an envelope per event
- **Modular generality** — an envelope generator can also drive the frequency input to produce vibrato or glissando; envelopes, oscillators, and other UGs interconnect freely. Envelopes are "profiles of gestures" that, like body movements, infuse life into otherwise lifeless signals
