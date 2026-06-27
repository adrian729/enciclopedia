# Ch 25: Noise, Chaotic, and Stochastic Synthesis

## Table of Contents

- [1. Colored Noises](#1-colored-noises)
- [2. Noise Modulation](#2-noise-modulation)
- [3. Stochastic and Chaotic Waveform Synthesis](#3-stochastic-and-chaotic-waveform-synthesis)
- [4. Dynamic Stochastic Synthesis and GENDYN](#4-dynamic-stochastic-synthesis-and-gendyn)

## 1. Colored Noises

- **Noise** — dispersed spectral energy with a *broadband spectrum* (many frequencies low to high in constant flux); a fundamental musical ingredient, from percussion to bowed strings to breathy winds, foregrounded since Russolo's 1916 *Art of Noises* and works like Stockhausen's *Gesang der Jünglinge* (1956) and Xenakis's *Bohor* (1962)
- **White vs. colored noise** — *white noise* contains all frequencies in equal measure; any band-limited noise is *colored noise*, commonly made by passing white noise through a bandpass filter. Colors are defined by spectral shape (analogy to light frequencies):

| Noise | Spectral character |
|---|---|
| **White** | Flat spectrum, equal energy at all frequencies |
| **Pink** (1/f, flicker) | Equal energy per octave; falls off 3 dB/octave; more bass rumble |
| **Blue** (azure) | Power density rises 3 dB/octave (high-pass-filtered white) |
| **Purple** (violet) | Power density rises 6 dB/octave |
| **Green** | White with boosted mids (no mathematical definition) |
| **Red** (brown) | Strong low boost, falls off 6 dB/octave; sometimes = brown (1/f² noise, after botanist Robert Brown) |
| **Gray** | From flipping random bits in integer samples; stronger lows (named after Elisha Gray's code) |
| **Grey** | Random noise shaped by an equal-loudness curve so it sounds equally loud at all frequencies |
| **Black** | Several definitions: \~18 dB/octave falloff; mostly zero power with sparse spikes; or inverted "antinoise" (e.g. noise-canceling headphones) |
| **Infrared** | Random fluctuation below 20 Hz (infrasonic) |
| **Velvet** | Only sample values −1, 0, 1; a sign-randomized jittered impulse train, used for reverberation |

## 2. Noise Modulation

- **Noise modulation** — using a noise generator to modulate a sine's amplitude or frequency, spanning aperiodic tremolo/vibrato to broad and narrow colored-noise bands
- **Pseudorandom noise** — truly random number generation is mathematically impossible (Chaitin), so any finite algorithm is a *pseudorandom number generator* (PRNG) that eventually repeats. Wolfram's *Rule 30* (cellular automata) is notably long-period; most languages use the *Mersenne Twister*, period \( 2^{19937} - 1 \) (after music theorist/mathematician Marin Mersenne)
- **Sources of noise** — sampled natural sounds (wind, sea spray, waterfalls, thunder), speech fricatives/plosives, unpitched percussion, industrial scrapyard recordings; analog circuits give the most complex noise (diode *quantum noise* is among nature's most random); digital aliasing/overload sound noisy but are *deterministic* (correlated with input)
- **Noise-modulated AM and FM** — a noise generator controlling oscillator amplitude (AM) or frequency (FM); infrasonic-filtered noise yields aleatoric tremolo or vibrato, wider-band noise yields a colored-noise band around the carrier. Lowpass-filtering the noise keeps the randomness near the carrier rather than adding an audibly separate high-frequency component
- **Random waveshaping** — replacing the waveshaping *shaping function* (chapter 17) with a random one distorts a periodic signal toward broadband noise; subtler variants stay smooth at low amplitudes and add randomness at higher amplitudes, or link randomness to tone duration

## 3. Stochastic and Chaotic Waveform Synthesis

- **Stochastic waveform synthesis** — generates each sample by comparing a pseudorandom number against a *probability distribution* (a stored curve giving the numerical probability of each possible amplitude outcome). Efficiency matters (tens of thousands of samples/second), so preloading a table of pseudorandom values for lookup beats per-sample PRNG calls
- **Need for constraints** — plain probability-table lookup yields a fixed-spectrum noise, so constraints that vary the probabilities over time are needed for interesting time-varying sound — the goal of dynamic stochastic synthesis
- **Chaos vs. randomness** — *chaotic systems* are deterministic dynamic systems with high sensitivity to initial conditions (a small input change makes output diverge unpredictably); only systems with a *nonlinear feedback path* can be truly chaotic. Chaos has underlying order (commuters all catching trains), whereas randomness does not (a terrified mob)
- **Chaotic equations** — many exist (Lorenz, Chua, Duffing, Henon, FM). The *logistic map* \( x_{n+1} = \lambda(x_n - x_n^2) \) is among the simplest, chaotic for \( \lambda \) between 3.57 and 4; near 3.6 the output is noisy and rapidly changing, near 3.8 an *island of stability* appears — a balance of stability and noise characteristic of chaos
- **Turning chaos into sound** — scan \( \lambda \) across its chaotic range for a chaotic oscillator, vary the step time (e.g. \( n+20 \) instead of \( n+1 \)) for crude pitch control, use the equation to modulate a sinusoid, or take its second/third derivative as waveform or control function

## 4. Dynamic Stochastic Synthesis and GENDYN

- **Xenakis's inversion** — in *Formalized Music*, Xenakis proposed *dynamic stochastic* synthesis: instead of starting from periodic functions and injecting disorder, start from pseudorandom functions and tame them with order (weights, constraints, barriers), via eight strategies — e.g. direct use of probability distributions (Poisson, exponential, Gaussian, uniform, Cauchy, arcsine, logistic); multiplying or additively mixing distributions; random variables under elastic forces or bouncing between elastic boundaries; distributions whose parameters are set by other distributions; and hierarchical/compositional control of waveform generation
- **GENDYN (GENeration DYNamique)** — Xenakis's implementation, conceptually linked to SSP and SAWDUST interpolation/segment techniques (chapter 22), based on abstract time- and amplitude-point manipulation unrelated to pitch/timbre/rhythm; results are unpredictable (Xenakis likened it to a herd of wild horses)
- **Polygon waveform** — GENDYN repeats an initial waveform represented as a polygon whose vertices on time and amplitude axes are joined by interpolated straight segments; each new waveform applies stochastic variations to the previous one
- **The mirror** — vertices are generated from stochastic distributions; unconstrained, the signal rushes toward white noise, so a *mirror* (amplitude barrier + time barrier) reflects out-of-bounds points back in. The amplitude barrier controls the number of reflections (discontinuities → timbre); the time barrier sets the interval between time points (→ perceived frequency). Control parameters per voice: number of time segments, mirror boundaries, and the stochastic distributions for time and amplitude vertices
- **Sensitivity and extensions** — initial conditions and parameter tuning decisively shape the sound; small adjustments vary results enormously. Brown (2005) made hard-coded constants variable and added real-time interaction
- **Real-time stochastic synthesizers** — chaotic GENDYN-type synthesis appears in SuperCollider and Native Instruments REAKTOR; *Stochos* (using stochastic, chaotic, and deterministic envelopes) evolved into SonicLab's Cosmosƒ apps combining granulation, FM, RM, and waveshaping with stochastic control; the Eurorack market offers hundreds of noise/chaotic modules
