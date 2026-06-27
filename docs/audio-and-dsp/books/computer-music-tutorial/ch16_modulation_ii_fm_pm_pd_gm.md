# Ch 16: Modulation II: FM, PM, PD, and GM

## Table of Contents

- [1. Frequency Modulation: Principle and History](#1-frequency-modulation-principle-and-history)
- [2. C:M Ratio, Modulation Index, and Bandwidth](#2-cm-ratio-modulation-index-and-bandwidth)
- [3. The FM Formula and Bessel Functions](#3-the-fm-formula-and-bessel-functions)
- [4. Multiple-Carrier and Multiple-Modulator FM](#4-multiple-carrier-and-multiple-modulator-fm)
- [5. Feedback FM](#5-feedback-fm)
- [6. Phase Modulation, Phase Distortion, and General Modulations](#6-phase-modulation-phase-distortion-and-general-modulations)

## 1. Frequency Modulation: Principle and History

- **Frequency modulation (FM)** — a classic digital synthesis method (not one technique but a family) in which a carrier oscillator is varied in frequency by a modulating oscillator; world-famous after Yamaha (the Yamaha implementation is technically *phase modulation*)
- **John Chowning** — first to systematically explore musical digital FM (1973); sought efficient time-varying spectra (replacing 50 oscillators with 2) after experimenting with extreme vibrato that becomes fast enough to alter timbre. Compositions: *Sabelithe*, *Turenas*, *Stria*, *Phoné*
- **Commercial impact** — Chowning patented FM (U.S. 4,018,121); Yamaha licensed it, releasing the GS-1 (1980, $16,000) and the wildly successful DX7 (1983, $2,000) that made FM synonymous with digital synthesis
- **Simple FM (Chowning FM)** — unlike RM/AM's single sum-and-difference pair, FM of two sinusoids generates a *series* of sidebands around the carrier C, each spaced at a multiple of the modulator M; the number of sidebands depends on the amount of modulation

## 2. C:M Ratio, Modulation Index, and Bandwidth

- **C:M ratio** — the ratio of carrier to modulating frequency sets sideband positions. A simple integer ratio (e.g., 4:1, as in 800/200 Hz) gives *harmonic* spectra with sidebands at C, C ± M, C ± 2M, …; a non-integer ratio (e.g., 8:2.1, as in 800/210 Hz) gives *inharmonic* spectra
- **Modulation index** — \( I = D / M \), where \( D \) is the frequency *deviation* (Hz) from the carrier — the depth of modulation. So D = 100 Hz with M = 100 Hz gives \( I = 1.0 \). As \( I \) increases, the number of sidebands increases and energy is "stolen" from the carrier into the sidebands
- **Number of sidebands and bandwidth** — significant sideband pairs (amplitude > 1/100 of carrier) ≈ \( I + 1 \); total bandwidth ≈ \( 2 \times (D + M) \). Because bandwidth grows with \( I \), FM mimics how instrumental brightness rises with amplitude (using shared envelope shapes for carrier amplitude and \( I \))
- **Reflected sidebands** — partials above the Nyquist frequency fold over (alias); sidebands extending below 0 Hz reflect back in 180° *phase-inverted* form (drawn as downward lines), adding richness but potentially canceling overlapping positive components

## 3. The FM Formula and Bessel Functions

- **FM formula** — for sinusoidal carrier and modulator: \( FM_t = A \times \sin(C_t + [I \times \sin(M_t)]) \), where \( A \) is carrier peak amplitude, \( C_t = 2\pi \times C \), \( M_t = 2\pi \times M \). Efficient: two multiplications, an addition, two table lookups
- **Bessel functions** — sideband amplitudes vary according to *Bessel functions of the first kind and nth order* \( J_n(I) \), whose argument is the modulation index \( I \). The amplitude of the nth partial is \( J_n(I) \) times two sine components on either side of the carrier; odd-order lower-side components are phase-inverted
- **Sweeping behavior** — each \( J_n(I) \) undulates like a damped sinusoid (wide variation at low \( I \), little at high \( I \)); the audible signature of simple FM. Because \( J_n(I) \) for different \( n \) cross zero at different \( I \), sidebands drop in and out quasi-randomly as \( I \) sweeps
- **No amplitude normalization needed** — maximum amplitude and signal power need not vary with \( I \), so amplitude and index can be controlled by independent envelopes — unlike waveshaping and discrete summation formulas
- **Applications** — brasslike tones (sharp attack on amplitude and index envelopes, C:M = 1, index 0–7); C:M = 1:2 gives odd harmonics for a crude clarinet; irrational C:M ratios give inharmonic bell/percussion tones. Composers Dashow and Truax mapped spectral *families* of C:M ratios. *Parameter estimation* (matching FM to a target sound) is inherently difficult and now less motivated, since additive synthesis and physical modeling run in real time — FM's value lies in its unique synthetic spectra
- **Linear, exponential, through-zero FM** — *linear FM* spaces sidebands equally around the carrier (center frequency stays fixed as \( I \) rises); *exponential FM* on analog VCOs (one volt per octave) spaces them asymmetrically, detuning the perceived center pitch; *through-zero FM (TZFM)* inverts the waveform when frequency passes below zero, keeping pitch in tune regardless of modulation depth

## 4. Multiple-Carrier and Multiple-Modulator FM

- **Multiple-carrier FM (MC FM)** — one modulator drives two or more carriers whose summed outputs create *formant regions* (peaks) characteristic of voice and instruments, and allow separate decay times per region. The waveform is the sum of \( n \) simple FM equations, with carrier weights \( w1 \ldots wn \), \( M \) usually set equal to fundamental \( C1 \)
- **MC FM applications** — trumpet tones (Morrill's double-carrier: \( C1 \) for the fundamental and first 5–7 partials, \( C2 \) at 1500 Hz for the trumpet formant); Chowning's sung-vowel simulations requiring periodic + random vibrato (*vibrato percent deviation* \( V = 0.2 \times \log(pitch) \), ≈1.2% at 440 Hz). Sampled sounds can serve as carriers (Yamaha SY77 + AWM)
- **Multiple-modulator FM (MM FM)** — more than one modulator drives a single carrier, in *parallel* or *series* configuration
- **Parallel MM FM** — two sines simultaneously modulate one carrier, generating sidebands at \( C \pm (i \times M1) \pm (k \times M2) \) (integers \( i, k \)) — an explosion of partials. Equation: \( PMMFM_t = A \times \sin\{C_t + [I1 \times \sin(M1_t)] + [I2 \times \sin(M2_t)]\} \)
- **Series MM FM** — \( M1 \) is itself modulated by \( M2 \): \( SMMFM_t = A \times \sin\{C_t + [I1 \times \sin(M1_t + [I2 \times \sin(M2_t)])]\} \). \( I2 \) sets sidebands in the modulating signal, \( I1 \) in the output; M1:C places the carrier's sidebands, M2:M1 places each sideband's own sidebands. Schottstaedt used double-modulator FM for piano tones (modulators ≈ 1× and 4× the carrier; inharmonicity matches real pianos), and triple-modulator FM (C:M1:M2 = 1:3:4) for strings

## 5. Feedback FM

- **Feedback FM** — Yamaha's patented method; solves a problem of simple FM: as \( I \) increases, partial amplitudes undulate unevenly per the Bessel functions, giving an "electronic" sound. Feedback FM makes the spectrum evolve more *linearly* — partials and their amplitudes increase roughly monotonically
- **One-oscillator feedback** — an oscillator feeds its output back into its frequency input through a *feedback factor* \( \beta \) (acting as the modulation index); next-sample address is \( x + [\beta \times \sin(y)] \). As \( \beta \) rises, the signal evolves continuously from sine to sawtooth. Characterized via Bessel functions \( J_n(n) \) where the order \( n \) is folded into the modulation index \( n \times \beta \), and a \( 2/(n \times \beta) \) coefficient ensures amplitude decreases with partial order — unlike simple FM's common index \( J_n(I) \)
- **Two-oscillator feedback** — a feedback oscillator modulates a second non-feedback oscillator; multiplier \( M \) is the inter-oscillator modulation index. With \( M \) = 1 and equal frequencies it equals the one-oscillator case; \( \beta > 1 \) boosts high partials (a strident, variable-filter effect)
- **Three-oscillator indirect feedback** — three oscillators modulate each other (factors \( \beta1, \beta2, \beta3 \)) with global output fed back to the first; noninteger frequencies give nonpitched sounds, near-integer ones a beating chorus; rich spectra with high-end energy ideal for metallic/distorted timbres
- **FM parameter space** — commercial FM has dozens of interacting parameters (the Jellinghaus DX-Programmer had 30 switches and 148 knobs), driving heavy reliance on preset libraries (Native Instruments FM8 ships 1,200+ presets)

## 6. Phase Modulation, Phase Distortion, and General Modulations

- **Phase modulation (PM)** — with FM, two cases of *angle modulation*: PM is \( \cos([phase + increment] + f(t)) \) while FM is \( \cos(phase + [increment + f(t)]) \) — PM modulates the phase, FM the phase increment. In simple cases they sound identical, but **most "FM synthesis" (Chowning's patent, Yamaha chips) is actually implemented as PM**
- **Why PM is preferred** (McCartney) — the modulation index does not depend on carrier frequency (it equals the phase deviation in radians); and a DC component in the modulator does not shift the carrier's pitch, enabling chained/stacked modulators (MM FM) and feedback FM without DC-bias side effects. SuperCollider's PMOsc and ChucK emulate this
- **Phase distortion (PD)** — Casio's term (CZ synthesizers, 1980s): a sine-wavetable oscillator scans nonlinearly, speeding from 0 to an inflection point \( d \) then slowing from \( d \) to \( 2\pi \); overall frequency stays constant but the output becomes harmonically rich — effectively phase-synchronous phase modulation
- **General modulations (GM)** — substituting a time-varying periodic function for a constant in a synthesis equation; *waveshape parameter modulation* covers AM and FM. Moorer showed simple FM is one instance of *discrete summation formulas* (DSFs) — *closed-form* solutions to sums of trigonometric series, compact and efficient, capable of spectra impossible with FM (e.g., *one-sided spectra* extending in one direction from the carrier) but requiring amplitude normalization
- **Other approaches** — *Doppler FM* (panning at audio rates, spectrally equivalent to FM); allpass-filter-chain methods producing AM/FM-like spectra; the Mutable Instruments Warps module's *exclusive-or (XOR) modulation*, XORing carrier and modulator as 16-bit numbers
