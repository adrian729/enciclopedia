# Ch 20: Formant Synthesis

## Table of Contents

- [1. Formants and Formant Synthesis](#1-formants-and-formant-synthesis)
- [2. FOF Synthesis and CHANT](#2-fof-synthesis-and-chant)
- [3. VOSIM](#3-vosim)
- [4. Window Function Synthesis](#4-window-function-synthesis)
- [5. PAF and ModFM](#5-paf-and-modfm)

## 1. Formants and Formant Synthesis

- **Formant** — a resonance peak of energy in a spectrum, which can include harmonic and inharmonic partials as well as noise. Within 0-5,000 Hz the vocal tract is characterized by five formant regions (including the fundamental)
- **Spectral signature** — formant regions serve as a timbral cue to a sound's source; they are not fixed but shift relative to the fundamental frequency
- **Formant synthesis** — a body of techniques designed to generate spectral resonance peaks, simulating the vocal tract or instruments; rooted in centuries of speech research ("singing flames," Dr. Marage's rubber-lipped vocal emulator, Howard's 2017 3D-printed vocal tracts)
- **The five methods covered** — FOF (formant wave-function), VOSIM, window-function (WF), phase-aligned formant (PAF), and ModFM. FOF and VOSIM grew from speech simulation; WF was built for instrument formants; PAF and ModFM derive from mathematical analysis. They are grouped here because they fit no other synthesis category and were designed primarily for formants

## 2. FOF Synthesis and CHANT

- **FOF** — *formant wave-function* synthesis (from French *fonction d'onde formantique*), the basis of IRCAM's CHANT system (*chant* = song). Conceived by Rodet and colleagues from 1975; reimplemented from the IRCAM 4X to PCs, Csound, and OpenMusic
- **CHANT's model** — natural mechanisms that resonate when excited but are damped by friction (a bell rings long, a wood block cuts off fast; the vocal cords send fast impulses to continuously excite vocal-tract resonances). Built around the voice but tunable to instruments and synthetic effects
- **From filters to sine bursts** — Rodet showed the complex filter of subtractive synthesis (or LPC) decomposes into parallel bandpass filters (second-order sections) excited by pulses; each FOF realizes one such filter, and several in parallel model a *spectrum envelope* of multiple formants. The filters can be replaced by a bank of damped sine generators — more efficient, less precision-hungry, and able to transition continuously from formant to additive synthesis
- **FOF grain** — at each pitch period an FOF generator emits a grain: a damped sine with a steep or smooth attack and quasi-exponential decay, shaped by a *local envelope* (vs the note's global envelope). Because the grain lasts only a few milliseconds, its envelope convolves with the sinusoid to add sidebands, creating the formant. The local envelope is \( env_t = \tfrac{1}{2} \times [1 - \cos(\pi_t / tex)] \times \exp(-atten_t) \) during attack, then \( env_t = \exp(-atten_t) \), with attack time \( tex \) and decay \( atten \)
- **Four formant parameters** — \( p1 \): formant center frequency; \( p2 \): formant bandwidth (width at \( -6 \) dB), set by the grain *decay* (long decay → sharp peak); \( p3 \): peak amplitude; \( p4 \): width of the *formant skirt* (the foothills around \( -40 \) dB), set by the grain *attack* (longer attack → narrower skirt). Frequency-domain features are thus controlled by time-domain envelope properties
- **CHANT program** — three interaction modes: supplying preset singing variables (loudness, fundamental, vibrato, spectrum shape, local/global envelopes); using FOFs as time-varying filters on sampled sound; and writing timbre-interpolation algorithms in OpenMusic. Implementations can have over sixty parameters, requiring a rule database
- **FOF analysis/resynthesis** — two historical methods generate FOF parameters: *Models of Resonance* (MOR), which captures only the resonance stage via iteratively widening FFT windows and works best on pitched percussion (marimba, vibraphone, tubular bells); and an LPC-based approach tracing the spectrum envelope per frame (Depalle 1991) — both similar to, but not identical reconstructions of, the original

## 3. VOSIM

- **VOSIM** — *voice-simulation*, developed by Werner Kaegi and Stan Tempelaars at the Institute of Sonology, Utrecht (early 1970s); generates a repeating tone-burst signal producing a strong formant, linked in spirit to FOF. Originally for vowels, later extended to fricatives ([sh]) and quasi-instrumental tones
- **Waveform** — a series of pulse trains where each pulse is a squared sine (\( \sin^2 \)); amplitude \( A \) for the tallest pulse, \( N \) pulses decaying by factor \( b \), each of width \( T \) (which sets formant position), followed by a variable delay \( M \). The period is \( (N \times T) + M \) — e.g. seven 300 µs pulses plus a 900 µs delay gives a 3 ms period, a 333.33 Hz fundamental, and a formant at 5,000 Hz
- **Two percepts** — a fundamental from the whole signal's repetition rate, and a formant peak from the \( \sin^2 \) pulse width. One formant per oscillator; several VOSIM oscillators are mixed for multiple formants
- **Parameters and modulation** — primary parameters \( T, M, N, A, b \); modulating delay \( M \) yields vibrato, FM, and noise (variables \( S \), \( D \), \( NM \) for type, deviation, rate); transitional variables \( NP, dT, dM, dA \). Changing \( T \) sweeps the formant (*formant shifting*)
- **Aliasing** — the raw VOSIM signal is not bandlimited (problematic at low sampling rates), though components fall \( \ge 30 \) dB at twice the formant frequency and \( \ge 60 \) dB at six times. Built in hardware at Sonology and Toronto's SSSP; now in Csound, Max, SuperCollider, REAKTOR, and the Mutable Instruments Braids module

## 4. Window Function Synthesis

- **Window function (WF) synthesis** — a multistage technique (Bass and Goeddel 1981) for formant synthesis using purely *harmonic* partials: build a broadband harmonic signal, then weight harmonics to create time-varying formant regions emulating traditional instruments
- **WF pulse** — the broadband building block is a *window function pulse* (windows are envelopes used in filter design and analysis); window spectra have a high *center lobe* and low *side lobes*. The Blackman-Harris window attenuates side lobes by \( \ge 60 \) dB, making the signal effectively bandlimited and aliasing-free
- **Building the signal** — a periodic series of WF pulses separated by zero-amplitude *dead time*; for different fundamentals the pulse width stays fixed and only the dead time varies. As the fundamental falls, more harmonics fit inside the center lobe, so low tones are rich and high tones thin — characteristic of pipe organs and pianos (but not harpsichords or inharmonic instruments)
- **Slot weighting** — a *time slot* is one WF pulse plus part of its dead time; multiplying the pulse stream by a periodic sequence of \( N \) *slot weights* sculpts peaks and valleys (formants) into the spectrum, each weight optionally time-varying. An *amplitude compensation* scheme scales amplitude inversely with frequency to balance the sparse low and dense high tones
- **Practical results** — a setup of eight WF oscillators, up to 256 slots/period, 40 kHz sampling, 150 µs pulse width, and 28-segment slot-weight functions gave reasonable emulations, including a difficult alto saxophone tone

## 5. PAF and ModFM

- **Phase-aligned formant (PAF)** — invented by Miller Puckette, patented by IRCAM; combines a two-cosine carrier with a *waveshaping* pulse modulator (ch. 17). Has a well-defined spectrum with predictable phases and is efficient. The modulator sinusoid is rectified; the waveshaping function \( g \) is a Gaussian-like bell curve, \( a \) a waveshaping index controlling modulator bandwidth, \( \omega \) the fundamental, and \( k, p, q \) the formant center frequency. The carrier is a weighted sum of two cosines (frequencies \( k \) and \( k+1 \)) with all phases driven by one sawtooth oscillator — hence *phase-aligned*. Six PAF generators have synthesized vocal formants
- **ModFM** — Lazzarini and Timoney (2013); *phase-synchronous ModFM* generates an impulse train by heterodyne synthesis \( s(n) = M(n) \times \sin(\omega_c \times n) \), where a center-frequency sinusoidal carrier is amplitude-modulated by a phase-synchronous \( M(n) \), and waveshaping dynamically controls the modulator spectrum
- **Modified Bessel functions** — derived from classic FM, ModFM uses a summation formula of *modified* Bessel functions, which (unlike the undulating Bessel functions of classic FM) are unipolar and decaying, always yielding a decaying spectral envelope. The modulator is tuned as the fundamental and the carrier to the formant center; \( k \) is the distortion index controlling bandwidth. A two-carrier, two-waveshaper variant (synced by one phasor) is available, with the spectrum mix set by \( A \) in \( [0,1] \); Csound has a `modfm` opcode
