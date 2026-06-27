# Ch 15: Modulation I: RM, SSM, and AM

## Table of Contents

- [1. Modulation Fundamentals](#1-modulation-fundamentals)
- [2. Ring Modulation (RM)](#2-ring-modulation-rm)
- [3. Single-Sideband Modulation (SSM)](#3-single-sideband-modulation-ssm)
- [4. Amplitude Modulation (AM)](#4-amplitude-modulation-am)

## 1. Modulation Fundamentals

- **Modulation** — a sound A varies because of the action of a *modulation signal* B (typically an oscillator or noise generator, but any signal will do); patched on a modular synth, or routed via a *modulation matrix* mapping modulation sources (columns) to modulated parameters (rows)
- **Carrier and modulator** — formally, some aspect of the *carrier* (C) varies according to the *modulator* (M). Below 20 Hz this gives *tremolo* (slow amplitude variation) and *vibrato* (slow frequency variation), typically at 6–9 Hz
- **Sidebands / modulation products** — when M rises above \~20 Hz into the audio band, new audible frequencies (*sidebands*) appear, usually on either side of the carrier
- **Inherent limitation** — modulation spectra are constrained by mathematical law to fixed behaviors, so each technique has a characteristic sonic signature (cliché or alluring force; e.g., the Barrons' *Forbidden Planet* soundtrack, 1956)
- **Bipolar vs unipolar signals** — a *bipolar* signal swings both negative and positive around zero (most audio waveforms); a *unipolar* signal stays within the upper half of the range — a bipolar signal plus a constant *DC offset* (a 0 Hz signal). The key distinction: **RM modulates two bipolar signals; AM modulates a bipolar signal with a unipolar signal**

## 2. Ring Modulation (RM)

- **Ring modulation (RM)** — a trademark electronic-music sound; in digital systems, simply the multiplication of two bipolar signals: \( RingMod_t = C_t \times M_t \), with M classically a sine wave. Below 20 Hz it gives tremolo; in the audio band it changes timbre
- **Sidebands** — for each carrier component, RM contributes a pair of sidebands at the *sum* and *difference* of C and M. Integer C:M ratio → harmonic sidebands; otherwise inharmonic. **The carrier frequency itself disappears**
- **Trigonometric basis** — \( \cos(C) \times \cos(M) = 0.5 \times [\cos(C - M) + \cos(C + M)] \); RM can also be viewed as a case of *convolution*
- **Example** — C = 1000 Hz, M = 400 Hz → components at 1400 Hz (sum) and 600 Hz (difference)
- **Negative frequencies** — when M exceeds C (e.g., C = 100, M = 400), the difference \( C - M = -300 \) Hz; a negative frequency merely inverts the sign of the phase, flipping the waveform over the *x*-axis. Phase matters only when summing identical frequencies
- **Applications** — Stockhausen applied RM to mic-recorded percussion and piano (*Kontakte*, *Mantra*, etc.); James Dashow built families of synthetic sounds from harmonic/inharmonic sine ratios
- **Analog RM** — unlike pure digital multiplication, analog circuits use a four-diode *ring* configuration; the diodes clip the carrier into a quasi-square wave, adding sums and differences on odd harmonics: \( C \pm M, 3C \pm M, 5C \pm M, \ldots \), so character depends on diode type (silicon vs germanium)

## 3. Single-Sideband Modulation (SSM)

- **Single-sideband modulation (SSM) / frequency shifting** — pioneered by Harald Bode; *adds* a fixed value (in Hz) to all components, destroying harmonic relations. A tone at 100/200 Hz shifted by 10 Hz becomes 110/210 Hz — no longer harmonic (the second harmonic of 110 is 220, not 210)
- **vs pitch shifting** — pitch shifting *multiplies* all frequencies by a factor (preserving harmonic ratios, e.g., ×2 = up an octave); frequency shifting *adds* a constant (inharmonic result)
- **Separate sum/difference outputs** — a frequency shifter (*Klangumwandler*) outputs sum and difference frequencies separately; used practically to reduce acoustic feedback in live sound by slightly shifting the mic signal
- **Hartley (phasing) method** — uses phase cancelation to null one sideband via the *Hilbert transform* (a *quadrature filter* that converts sines into cosines, defined as convolution with \( 1/(\pi t) \), implemented as a pair of allpass filters). It shifts negative-frequency components by \( +90° \) and positive by \( -90° \); the output feeds two ring modulators (one × cosine, one × sine of frequency \( f \)). **Subtracting gives the upper sideband; summing gives the lower**

## 4. Amplitude Modulation (AM)

- **Amplitude modulation (AM)** — one of the oldest techniques; like RM the carrier's amplitude varies with the modulator, but the **modulator is unipolar** (entirely above zero). Applying an envelope to a sine is the most mundane case of infra-audio AM: \( AmpMod_t = C_t \times M_t \)
- **AM vs RM spectrum** — like RM, AM produces sum and difference sidebands for each component, but **the AM spectrum also contains the carrier frequency**. Sideband amplitude rises with modulation but never exceeds half the carrier level. AM is convolution with one signal offset by a nonzero constant
- **Modulation index** — controls the amount of modulation; the full AM equation is \( AmpMod = A_c \times \cos(C) + \frac{I \times A_c}{2} \times \cos(C + M) + \frac{I \times A_c}{2} \times \cos(C - M) \), where \( A_c \) is carrier amplitude, \( I \) the modulation index, C the carrier frequency, M the modulator frequency. Each sideband amplitude is \( index/2 \)
- **Feedback AM** — a self-modulating oscillator feeding output back to its (amplitude) input; originated with Risset, Mathews, and Moore at Bell Labs (1969, Music V). One-sample-delay form: \( y(n) = \cos(\omega_0 n) \times [1 + \beta \times y(n-1)] \) where \( \omega_0 = 2\pi \times f_0/f_s \); the feedback gain \( \beta \) acts as the modulation index controlling brightness. Produces a pulsating waveform with a large DC component and a lowpass spectral profile; Kleimola et al. (2011) recast it as a *periodically linear time-variant* (PLTV) filter
