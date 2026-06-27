# Ch 6: Wavetable Lookup Synthesis

## Table of Contents

- [1. Wavetable Lookup and the Digital Oscillator](#1-wavetable-lookup-and-the-digital-oscillator)
- [2. Controlling Frequency with the Phase Increment](#2-controlling-frequency-with-the-phase-increment)
- [3. The Oscillator Algorithm](#3-the-oscillator-algorithm)
- [4. Table Lookup Noise and Interpolation](#4-table-lookup-noise-and-interpolation)
- [5. Alternatives to Wavetable Lookup](#5-alternatives-to-wavetable-lookup)

## 1. Wavetable Lookup and the Digital Oscillator

- **Wavetable lookup synthesis** — scanning a prestored *wavetable* in memory to produce samples; the core operation of a *digital oscillator*, the fundamental sound generator
- **The process** — for each new sample, read the next value from the table; at the end, wrap back to the beginning and read again. Because the stored waveform never changes during a sound event, it is also called *fixed-waveform synthesis*
- **Table index and phase_index** — each table entry has a numbered location (*table index value*); the current read location is the *phase_index*, named for the phase of the waveform. Example: a table of \( N = 1{,}000 \) entries (each a 16-bit number) is indexed 0 to 999
- **Phasor** — the read pointer moves by an *increment* from 0 toward the table end, then wraps around; this ramp function is the *phasor*, and one sweep of it produces one cycle of the waveform

## 2. Controlling Frequency with the Phase Increment

- **Frequency depends on table length and sampling rate** — reading through the whole table once per second yields 1 Hz; reading it 100 times per second yields 100 Hz. With 1,000 entries and a 50,000-sample/sec rate, the tone is \( 50{,}000 / 1{,}000 = 50 \) Hz
- **Changing pitch by resampling** — rather than changing the sampling rate (which complicates mixing signals of different rates), scan the table at different rates: *skip* samples to raise pitch, *repeat* samples to lower it
- **Concrete shifts** — taking only even-numbered samples goes through the table twice as fast, raising the pitch one octave; skipping two raises it an octave and a fifth; playing each sample twice lowers it an octave
- **Phase increment** — the value added to the current phase location to find the next read location, which sets how many samples are skipped or repeated. Reading every sample is increment 1; reading every other sample is increment 2

## 3. The Oscillator Algorithm

- **Two-step oscillator** — the basic algorithm is:
  1. \( \textit{phase\_index} = \text{mod}_L\,(\textit{previous\_phase} + \textit{increment}) \)
  2. \( \textit{output} = \textit{amplitude} \times \textit{wavetable}[\textit{phase\_index}] \)
- **The modulo operation** — \( \text{mod}_L \) divides the sum by table length \( L \) and keeps the remainder (always \( \le L \)), implementing the wraparound. The whole step costs little computation but assumes the wavetable is already filled
- **Increment sets frequency** — with table length and sampling rate fixed, the output frequency depends only on the increment. The governing relation (the most important equation in table lookup synthesis) is \[ \textit{increment} = \frac{L \times \textit{frequency}}{\textit{sampling frequency}} \] e.g. \( L = 1{,}000 \), sampling frequency 40,000, frequency 2,000 Hz gives increment 50

## 4. Table Lookup Noise and Interpolation

- **Non-integer increments** — for most combinations of table length, frequency, and sampling rate the increment is a real number with a fractional part, but a table index must be an integer
- **Truncation and table lookup noise** — discarding the fractional part (e.g. 6.99 becomes 6) yields a value near, but not exactly, the one needed; the resulting distortion is *table lookup noise*
- **Remedies** — a larger (finer-grain) wavetable reduces lookup error; *rounding* to the nearest integer (6.99 to 7) beats truncating; but the best result comes from an *interpolating oscillator*
- **Interpolating oscillator** — computes the value the table would have at the exact fractional phase by interpolating between adjacent entries (e.g. a *y* value at index 27.5 between entries 27 and 28). Costlier, but produces very clean signals
- **Quality gain** — for a 1024-entry sine wavetable, linear interpolation gives a worst-case 109 dB signal-to-noise ratio versus an abysmal 48 dB for a non-interpolating oscillator of the same size; smaller tables can then match larger ones

## 5. Alternatives to Wavetable Lookup

- **Direct equation evaluation** — memory is often slower than microprocessor instructions; modern CPUs have native instructions for sine/cosine, exponentials, square roots, and dot products, so (per James McCartney, 1997) sine waves, exponentiated sine waves, formant oscillators, and chaotic oscillators can be computed faster directly than by lookup
- **Other efficient methods** — Smith and Cook (1992) gave a highly efficient sinusoidal oscillator based on digital waveguides; Laroche (1998) showed resonant filters synthesizing time-varying sinusoids as an efficient route to additive synthesis
