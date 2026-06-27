# Ch 17: Waveshaping Synthesis

## Table of Contents

- [1. The Waveshaping Principle](#1-the-waveshaping-principle)
- [2. Shaping Functions and Spectral Control](#2-shaping-functions-and-spectral-control)
- [3. Amplitude Normalization](#3-amplitude-normalization)
- [4. Variations on Waveshaping](#4-variations-on-waveshaping)
- [5. Wavefolding](#5-wavefolding)

## 1. The Waveshaping Principle

- **Waveshaping** — also called *nonlinear distortion*; pass an input signal \( x \) through a distortion unit to warp the waveform and enrich its spectrum (Roads 1979). First explored by Jean-Claude Risset at Bell Labs (1969), elaborated independently by Daniel Arfib (1979) and Marc LeBrun (1979)
- **Shaping function / transfer function** — a stored table \( w \) that maps each input sample \( x \) in \( [-1, +1] \) to an output \( w(x) \) in the same range; the output sample is just the table value indexed by \( x \)
- **Musical value** — gives a simple, computationally efficient handle on the time-varying bandwidth and spectrum of a tone; the input \( x \) is typically a sinusoid but can be any signal, including sampled sound
- **Simple instrument** — an envelope generator scales the amplitude \( \alpha \) of a sinusoidal oscillator feeding the table; because \( \alpha \) scales \( x \), it selects which region of \( w \) is referenced, controlling timbre
- **Inverse of wavetable lookup** — Loy (2007): in wavetable lookup a phasor scans a wavetable; in waveshaping a waveform scans a ramped shaping function

## 2. Shaping Functions and Spectral Control

- **Linear function** — a straight diagonal line from \( -1 \) to \( +1 \) maps input to output unchanged (\( -0.4 \to -0.4 \)); only this case produces no distortion. Any other curve distorts \( x \)
- **Example functions** — an inverting line flips sign; a narrow-angle line attenuates; a function that expands low-level signals and sends high-level signals into clipping distortion; a line straight only around zero passes quiet signals cleanly but distorts loud ones (amplitude sensitivity)
- **Amplitude sensitivity** — models how acoustic instruments brighten when played harder (forceful strumming, strident blowing); one stored function yields many output waveforms by varying the input amplitude or offset, so a time-domain amplitude change becomes a frequency-domain spectral change
- **Chebychev shaping functions** — a family of smooth polynomials \( T_k \) valued in \( [-1, +1] \) that allow exact prediction of the steady-state spectrum from an unvarying cosine input. They obey the identity \( T_k(\cos[\theta]) = \cos(k \times \theta) \), so applying \( T_k \) to a cosine yields the \( k \)th harmonic
- **Building a spectrum** — sum weighted Chebychev polynomials into the table; e.g. \( T_1 + (0.3 \times T_2) + (0.17 \times T_3) \) produces a fundamental plus a 2nd harmonic at 0.3 and a 3rd at 0.17. Output is **bandlimited** (no frequencies above Nyquist), hence free of aliasing
- **Chebychev table** — \( T_0 = 1 \), \( T_1 = x \), \( T_2 = 2x^2 - 1 \), \( T_3 = 4x^3 - 3x \), \( T_4 = 8x^4 - 8x^2 + 1 \), and so on up to \( T_8 \), where \( x = \cos(\theta) \)
- **Alternative shaping functions** — for creative or hand-drawn functions (Buxton et al. 1982); Lazzarini and Timoney (2010) note Chebychev limits (target spectrum matched only at one distortion index) and propose alternatives, e.g. hyperbolic tangent functions that generate nearly bandlimited square and sawtooth waves

## 3. Amplitude Normalization

- **The problem** — output amplitude varies greatly with input amplitude even for one shaping function, but the point of waveshaping is to control *timbre*, not loudness; independence requires normalization
- **Three kinds** — *loudness normalization* (ideal: constant perceived loudness for all \( \alpha \)); *power normalization* (divide by the RMS of the harmonic amplitudes, per LeBrun 1979); *peak normalization* (scale output by its maximum value — least complicated, most practical, prevents DAC overload)
- **Peak normalization in practice** — precompute a table of normalization factors indexed by \( \alpha \); since \( \alpha \) sets the amplitude of \( x \), multiply the waveshaper output by the table entry for the current \( \alpha \)

## 4. Variations on Waveshaping

- **Varied inputs** — \( x \) need not be a cosine: a sum of cosines, or a frequency-modulated signal yields inharmonic partials and formant structures (Arfib 1979); a sampled sound input gives phasing-like undulation, or strong amp-style distortion if \( w \) contains horizontal/vertical lines
- **Movable waveshaping** — Xin Chong, Beijing (1987): the shaping function itself varies in time by storing a longer function and scanning different parts of it
- **Fractional waveshaping** — De Poli (1984): \( w \) is a ratio of two polynomials, generating exponential spectra and damped-cosine spectra whose bumps are heard as formants
- **Postprocessing** — feed the waveshaped signal through an AM/FM oscillator or filter to add inharmonic partials; De Poli and Volonnino (1984) developed *frequency-dependent waveshaping* for independent phase/amplitude control. Beauchamp and Horner (1992) modeled instruments with a multiple waveshaper + filter scheme: approximate the tone, subtract to get a *residual*, then approximate the residual again
- **Oversampling with filtering** — waveshaping distortion can alias; insert zero-valued samples to raise the Nyquist frequency, easing the design of smooth anti-aliasing lowpass filters (Pohlmann 2010)

## 5. Wavefolding

- **Wavefolding** — a nonlinear-distortion variant from modular synthesizers, originating in the analog Buchla 259 Complex Waveform Generator (1981) and Serge Wave Multipliers; now in Eurorack and software (VCV Rack, Reaktor)
- **Mechanism** — when the input exceeds a user-set threshold (detected by a comparator), the curved peaks *fold over* (invert at the threshold) rather than clip flat, so a growing signal reflects over itself like a mirror; a simple sine produces complex spectra, with harmonics fading in and out like time-varying filtering
- **Offset / symmetry** — an added positive or negative bias shifts the signal's center point, raising one half and lowering the other; bias can itself be modulated by a bipolar signal for more variation (Hetrick 2020)
- **Aliasing** — Esqueda et al. (2017) modeled the Buchla 259 circuit in Max \~gen, focusing on oversampling to suppress aliasing from the wavefolder's bandwidth expansion
