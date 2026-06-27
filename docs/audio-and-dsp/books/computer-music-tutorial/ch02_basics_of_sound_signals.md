# Ch 2: Basics of Sound Signals

## Table of Contents

- [1. Frequency, Period, and Amplitude](#1-frequency-period-and-amplitude)
- [2. Time-Domain and Frequency-Domain Representations](#2-time-domain-and-frequency-domain-representations)
- [3. Phase](#3-phase)
- [4. Sound Magnitude and Dynamic Range](#4-sound-magnitude-and-dynamic-range)

## 1. Frequency, Period, and Amplitude

- **Periodic vs noise** — a *periodic waveform* repeats in a regular pattern; *noise* has no discernible pattern; between the two extremes lies a vast domain of quasiperiodic and quasinoisy sounds
- **Cycle and fundamental frequency** — one repetition of a periodic waveform is a *cycle*; the *fundamental frequency* is the number of cycles per second, measured in *Hz* (hertz, after acoustician Heinrich Hertz)
- **Period** — the length of one cycle, the inverse of frequency: 1 Hz → 1 s, 100 Hz → 10 ms, 1000 Hz → 1 ms, 10 kHz → 100 µs. As the period shortens, frequency rises
- **Wavelength** — the physical distance spanned by one period. Since sound travels \~343 m/s at 20 °C, a 1 Hz wave unfolds over \~343 m while a 20 kHz wave spans only \~1.7 cm
- **Amplitude** — the amount of air-pressure change, measured as the vertical distance from the zero-pressure point to the highest (or lowest) point of a waveform segment

## 2. Time-Domain and Frequency-Domain Representations

- **Time-domain representation** — a graph of air pressure versus time; when the curve is near the top the pressure is higher, near the bottom it is lower
- **How sound is produced** — instruments and loudspeakers create sound by changing air pressure: a speaker moving *out* raises pressure, moving *in* lowers it; these vibrations must fall in the \~20–20,000 Hz range to be audible
- **Frequency-domain (spectrum) representation** — shows the frequency content of a sound, typically plotting each component as a vertical line whose height is its amplitude
- **Harmonics vs partials** — *harmonics* are integer multiples of the fundamental (a 100 Hz fundamental has harmonics at 200, 300 Hz, …); a *partial* is any frequency component, whether or not it is an integer multiple — useful because many sounds have no particular fundamental
- **Sine wave** — the purest signal, computed from the trigonometric sine; it contains a single frequency component, appearing as just one line in the spectrum
- **Spectra of other waveforms** — a sawtooth shows exponentially decreasing harmonics; constantly changing (aperiodic) signals are heard as noise, whose spectrum is very complex (one analyzed noise snapshot contained 252 frequencies)

## 3. Phase

- **Initial phase** — the starting point of a periodic waveform on the amplitude axis; a typical sine starts at 0 and completes its cycle at 0
- **Cosine** — a sine wave phase-shifted by π/2 radians (90°), so it starts and ends at amplitude 1
- **In phase vs out of phase** — two signals starting at the same point are *in phase* (*phase aligned*); a delayed signal is *out of phase*
- **Reversed polarity** — when signal B is exactly 180° out of phase with A (every positive value mirrored by a negative), B has *reversed polarity* / is a *phase-inverted* copy; summing such inverse-phase signals cancels them to zero
- **Why phase matters** — although two signals differing only in initial phase are hard to distinguish, polarity (180°) differences can be detected by some listeners. Every filter works by phase shifting (frequency-dependent cancellation and reinforcement); a time-varying phase shift produces the *phasing* / *flanging* sweep effect; analysis-resynthesis systems need each component's starting phase, which is critical for short *transient* sounds
- **Phase distortion** — unwanted frequency-dependent phase shifts that audibly distort signals and blur loudspeaker *imaging* (the stable "audio picture" that localizes each source); a phase-distorted signal is, by analogy, *out of focus*

## 4. Sound Magnitude and Dynamic Range

- **Decibel (dB)** — a unit for *ratios* of magnitude (voltage, intensity, power): \( \text{dB} = 10 \times \log_{10}(\text{level} / \text{reference level}) \), where the reference is usually the threshold of hearing (\( 10^{-12} \) W/m²)
- **Logarithmic consequence** — because the scale is logarithmic, two 60 dB notes sounding together rise only 3 dB, and a millionfold intensity increase yields only a 60 dB boost
- **Dynamic range** — the ratio between the loudest and softest sound a system can handle without distortion. Human hearing spans \~0 dB (softest audible) to \~125 dB (threshold of pain); the smallest audible amplitude difference is somewhat less than 1 dB
- **Capturing musical dynamics** — a live orchestra ranges from silence to over 110 dB at full tutti, so wide dynamic range is essential. Professional analog reel-to-reel tape manages \~80 dB, whereas a high-quality digital recorder reaches \~120 dB
