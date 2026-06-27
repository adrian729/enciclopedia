# Ch 30: Time Delay Effects

## Table of Contents

- [1. Delay Lines and Their Implementation](#1-delay-lines-and-their-implementation)
- [2. Fixed Delay Effects](#2-fixed-delay-effects)
- [3. Variable Delay and Comb-Sweep Effects](#3-variable-delay-and-comb-sweep-effects)
- [4. Chorus, Doppler, and Rotary Effects](#4-chorus-doppler-and-rotary-effects)

## 1. Delay Lines and Their Implementation

- **Time-delay effect** — fundamental electronic-music technique that stores incoming samples briefly before re-emitting them; originated with tape recorders (e.g., Pauline Oliveros patching record-to-playback head distance into a feedback loop to make infinitely repeating *tape echo feedback*)
- **Digital delay line (DDL)** — a unit that takes a stream of input samples, holds them in memory for a brief period, then outputs them; mixing the delayed sound with the original undelayed signal produces musical effects. DDLs also underlie filtering, reverberation, pitch shifting, and physical-modeling wave propagation
- **Circular queue** — the efficient data structure for a delay line: a list of sequential memory locations where, each sample period, the oldest sample is read and replaced by a new incoming sample; the read/write pointer advances and *wraps around* to the start at the end — hence "circular"
- **Delay tap** — a read pointer into the queue. A *multitap delay line* has more than one tap, reading several differently-delayed copies simultaneously each sample period
- **Fixed vs variable delay** — in a *fixed* unit the delay time is constant while sound passes through; in a *variable* unit the delay time constantly changes by moving the tap points at a control rate (*delay modulation*)

## 2. Fixed Delay Effects

- **Short delays (< \~10 ms)** — perceived as frequency-domain anomalies: a one-to-several-sample delay mixed with the original equals an FIR lowpass filter; a [0.1 ms, 10 ms] delay produces comb filter effects
- **Medium delays (\~10–50 ms)** — magnify a signal perceptually, creating ambience and an illusion of greater loudness without higher amplitude; a 15–50 ms delay yields a *doubling* effect (as if more than one person sings), enhanced by subtle time-varying pitch shifts
- **Long delays (> \~50 ms)** — create discrete echoes heard as repetitions. Since sound travels \~344 m/s at 20 °C, 1 ms equals \~1 foot of path; a discrete echo needs \~50 ms delay, i.e. \~25 feet to the reflective surface or \~50 feet total source-to-surface-to-listener path
- **Repeating echoes** — require a feedback loop; with feedback amplitude < 1.0 the echoes decay exponentially, with feedback > 1.0 they grow exponentially and overload. This is a recursive (feedback) filter; Putnam (2015) used complex-valued signals to make truncated *echo shapes* that stop after a set number of echoes
- **Delays as localization cue** — applying a short (\~0.2–10 ms) delay to one of two equal-amplitude loudspeakers shifts the apparent source toward the earlier (undelayed) speaker (Blauert 1983); a room's pattern of multi-surface reflections is its *impulse response* / sonic signature

## 3. Variable Delay and Comb-Sweep Effects

- **Flanging** — `flanging = signal + delayed signal` where the delay time constantly varies; a *swept comb filter effect* in which peaks and nulls (at integer multiples of 1/\(D\)) sweep up and down the spectrum. Discovered acoustically by Huygens (1693); Les Paul first used it as a studio effect (1945) by varying the speed of one of two disk recorders, later done by finger pressure on a tape reel *flange*
- **Electronic flanging** — replaces manual reel pressure with a low-frequency oscillator (sine or triangle) sweeping the delay at \~0.1–20 Hz; depth is maximal when original and delayed amplitudes are equal. Most modern implementations use an IIR/recursive feedback comb structure
- **Fractional delays** — at 48 kHz the smallest integer delay is 20.8 µs, but a *modulated delay line* needs continuous delay times to avoid discontinuities when swept: \( y(n) = x(n - [M + frac]) \). Requires interpolation at the read point; Dattorro warned linear interpolation causes distortion and high-frequency loss, recommending polynomial or allpass interpolation
- **Phasing** — similar to flanging but less pronounced; a spectrally rich signal is sent through a series of *allpass filters* (flat frequency response, but phase-shifting), swept by an LFO and mixed at unity gain with the original. Difference from flanging: flanging gives complete, uniformly-spaced peaks and nulls, whereas a phaser's number of notches equals its number of filter stages, with adjustable spacing, depth, and width

## 4. Chorus, Doppler, and Rotary Effects

- **Chorus effect** — processes one voice so it sounds like many, requiring small inter-voice differences: slight delays, fundamental-frequency alterations (beating), and asynchronous vibrato. No single algorithm exists; electromechanical precursors include Hanert's 1940s delay lines (Hammond *choral tone effect*) and Wayne's 1950s Baldwin *choral tone modulator*
- **Digital chorus methods** — send sound through a multitap delay line with delays constantly varying over a narrow range (equivalent to parallel flangers, but with longer delays); often using negative (phase-reversed) feedback to avoid resonances and overload. Another design splits the signal into octave bands, applies a per-band *frequency shifter* (adding a constant Hz to every component, destroying harmonic relations), then a time-varying delay — best for simulating large ensembles (Chamberlin 1985)
- **Harmonizer effects** — kept as a separate category: creates pitch-shifted "ghost voices" at specific intervals (see Ch 31)
- **Doppler shift, vibrato, rotary (Leslie) effect** — all implementable with a modulated delay line. Doppler shift is the primary cue to a source's radial velocity (described by Christian Doppler, 1842; first simulated for computer music by John Chowning, 1971). Vibrato is the basic case where the delayed signal is *not* mixed with the input. Current stereo/headphone rotary-speaker emulations are simplified and do not match the immersive 360° experience of a physical room
