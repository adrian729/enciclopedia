# Ch 31: Pitch-Time Changing

## Table of Contents

- [1. Pitch Shifting versus Pitch-Time Changing](#1-pitch-shifting-versus-pitch-time-changing)
- [2. Time-Domain Methods: Granulation and Harmonizers](#2-time-domain-methods-granulation-and-harmonizers)
- [3. Spectrum-Based Methods: Phase Vocoder, Wavelets, Atoms](#3-spectrum-based-methods-phase-vocoder-wavelets-atoms)
- [4. Linear Predictive Coding](#4-linear-predictive-coding)

## 1. Pitch Shifting versus Pitch-Time Changing

- **Simple pitch shifting (*varispeed*, *speed change*)** — changing playback speed (e.g., a record from 78 to 33 RPM, or slowing a tape) shifts pitch *and* duration together; a staple of electronic-music practice controlled by a knob or envelope
- **Pitch-time changing** — separates pitch and time by combining *time stretching/shrinking* (also *time warping*) with *pitch shifting*; alters duration while holding pitch constant (changing the *time base* / *time support*), or transposes pitch while holding duration constant
- **Applications** — fitting audio to video clips or a tempo grid (Ableton Live's Warp mode), slowing recordings for transcription, and *pitch editors* (e.g., Melodyne) combining pitch-time changing with pitch detection for auto-tune, harmony generation, vibrato/portamento editing, and formant manipulation (male-to-female)
- **Context-sensitive processing** — best results preserve the fine structure of attacks/transients and process only the steady state; stretching vowels more than consonants preserves speech intelligibility and naturalness
- **Two method categories** — *time-domain techniques* operating directly on the waveform (granular, harmonizer) and *spectrum-based methods* (phase vocoder, wavelets, atomic decomposition, LPC) that analyze the spectrum before manipulating it

## 2. Time-Domain Methods: Granulation and Harmonizers

- **Granulation** — segments a waveform into short *grains* (\~1 ms to 200 ms), cut at regular intervals or extracted from overlapping enveloped intervals that re-sum to the original
- **Electromechanical granulation** — pioneered by Dennis Gabor (1946, optical recording) and the Springer *Tempophon* (magnetic tape; used in Herbert Eimert's 1963 *Epitaph für Aikichi Kuboyama*). A rotating sampling head spins across the recording, taking audio snapshots; slowing the head shrinks duration (grains separated), speeding it clones grains to expand duration — local frequency content is preserved either way. Analogy: time-lapse vs slow-motion cinematography
- **Digital time-granulation** — early Illinois implementation (Otis, Grossman, Cuomo 1968) exposed the core flaw: grain endpoints don't match in level, causing periodic clicking *splicing transients*. Lee's Lexicon Varispeech added level matching; Jones and Parks (1988) used smooth overlapping grain envelopes for a seamless crossfade. Stretching clones grains, shrinking deletes every nth grain; arbitrary (non-power-of-two) ratios come from sample-rate changing combined with grain cloning/deleting
- **PSOLA (pitch-synchronous overlap add)** — a granular method that pitch-shifts while keeping formant peaks in their correct frequency position. Steps: (1) a pitch detector finds the period; (2) the signal is granulated at a *pitch-synchronous* rate; (3) grains are retriggered at a different rate and overlap-added. Because each grain holds a whole period (entire spectral signature), pitch changes by *retriggering* rather than resampling. Side effects (pitch-detection errors, windowing artifacts, timbral mismatch) grow with large intervals (> an octave). It can be hacked for formant shifting by resampling grains while retriggering at the original rate
- **Harmonizer** — a real-time transposer that shifts pitch without altering duration; the Eventide H910 (1975) was the first commercial digital one. Loads a buffer at input rate \(SR_{in}\), reads out at \(SR_{out}\); the ratio sets the pitch change. To hold duration in real time, input samples are repeated (upward shifts) or skipped (downward shifts), with the splice timed to the signal's periodicity and smoothed by fade-out/fade-in envelopes

## 3. Spectrum-Based Methods: Phase Vocoder, Wavelets, Atoms

- **Phase vocoder (PV)** — applies the FFT to short overlapping segments, producing spectrum frames that capture the sound's frequency evolution; the sound is resynthesized (e.g., by additive synthesis) as a simulacrum. Transforming the analysis data before resynthesis yields variations
- **Overlap-add PV transformations** — time stretching moves the resynthesis frame onset times farther apart, shrinking moves them closer. The PV prefers integer transposition ratios (Dolson 1986); pitch transposition scales component frequencies but also shifts formants, so Dolson reimposed the original spectral envelope. Laroche and Dolson (1999) reduced the audible "phasiness" / "loss of presence" of time-stretched material
- **Tracking phase vocoder (TPV)** — converts spectrum frames into per-component amplitude and frequency *envelope functions* (arrays); editing them shifts pitch or duration independently. Stretch by interpolating points; shrink by factor \(n\) using every \(n\)th value; transpose by multiplying frequency values (e.g., a major second multiplies each component by 11.892%, 1 kHz → 1118.92 Hz). SPEAR (Klingbeil) provides a graphical TPV interface
- **Frequency-domain formant-corrected pitch shifting** — uses the *cepstrum* to find formant peaks defining the spectral envelope; after FFT and pitch-shifting, the original envelope is reimposed via FFT convolution (moving formants opposite to the pitch shift), then IFFT back to the time domain
- **Wavelet transform** — analyzes into time-frequency wavelets whose duration depends on frequency (higher frequency → shorter wavelet → greater temporal resolution). Pitch-shift by multiplying analyzed wavelets' phase values by a factor; time-stretch/shrink by changing the resynthesis overlap point
- **Atomic decomposition** — an analytical counterpart to granular synthesis; outputs a list of atoms with parameters (start time, amplitude, frequency, duration, spatial position). Pitch-shift or time-stretch by scaling these numerical values (e.g., the real-time SCATTER app)

## 4. Linear Predictive Coding

- **Linear predictive coding (LPC)** — a subtractive analysis/resynthesis method modeling a signal as an *excitation function* (vocal cords, reed, bowed string) driving a set of *time-varying resonances* (vocal tract, instrument body) implemented as a time-varying filter
- **Character and limits** — does not perfectly reconstruct the signal; originally designed for low-bandwidth speech coding, its musical resynthesis has an artificial character that is hard to mitigate (Moorer)
- **Frame editing for transformation** — LPC encodes results as short *frames* (\~50–120 per second), each holding filter coefficients, pitch, and voiced/unvoiced data. Editing frame durations changes time; editing the pitch column changes pitch — so duration and pitch transform independently. Musical applications appear in works by James A. Moorer, Paul Lansky, and Charles Dodge
