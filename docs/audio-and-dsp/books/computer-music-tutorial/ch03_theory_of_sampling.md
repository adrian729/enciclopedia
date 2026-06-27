# Ch 3: Theory of Sampling

## Table of Contents

- [1. Analog vs. Digital Representations](#1-analog-vs-digital-representations)
- [2. The Conversion Chain (ADC/DAC)](#2-the-conversion-chain-adcdac)
- [3. Sampling and Reconstruction](#3-sampling-and-reconstruction)
- [4. Aliasing and the Sampling Theorem](#4-aliasing-and-the-sampling-theorem)
- [5. Practical Concerns: Sampling Rate and Jitter](#5-practical-concerns-sampling-rate-and-jitter)

## 1. Analog vs. Digital Representations

- **Analog** — a property (e.g. wire *voltage*) varies in a manner *analogous* to air pressure; stored as a *continuous-time* signal, such as the lateral groove of a phonograph record traced by a needle
- **Generation loss** — every analog copy adds noise, so a copy is never as good as the original; *first-generation* tape is acceptable but copies degrade audibly
- **Digital advantage** — handles *discrete-time* signals and can produce any number of perfect (noise-free) clones of the original

## 2. The Conversion Chain (ADC/DAC)

- **Recording path** — microphone → *antialiasing filter* → *analog-to-digital converter* (ADC), which samples the voltage into *binary numbers* at each tick of the sample clock, then stores them in memory
- **Playback path** — numbers read from storage → *digital-to-analog converter* (DAC), clock-driven, outputs voltage levels → lowpass smoothing filter → amplifier → loudspeaker
- **Bit** — abbreviation of *binary digit*; binary (base two) uses only 0 and 1; physical encoding varies by medium (magnetic charge on disc, reflectance on optical CD, transistor charge in *flash memory*); the leftmost bit often signals sign
- **Digital audio is not MIDI** — audio samples the waveform itself; MIDI captures only control events (start, end, pitch, amplitude). Four quarter notes at 60 BPM = 16 MIDI values, but the same 4 s recorded at 44.1 kHz stereo = 352,800 samples (\( 44{,}100 \times 2 \times 4 \)), over 700,000 bytes at 16 bits — \~44,100× more data than MIDI

## 3. Sampling and Reconstruction

- **Sample** — one measured value of the signal at a discrete instant, stored as a binary number; the higher the value, the larger the number
- **Quantization** — the number of bits used per sample; sets noise level and amplitude range (a CD uses 16 bits); more bits → finer amplitude resolution, lower noise, wider dynamic range
- **Sampling frequency (sampling rate)** — samples taken per second, in Hz; a CD samples at 44.1 kHz. Rates near 50 kHz are common, yielding \~6,000,000 samples per minute of stereo
- **Bandlimited reconstruction** — if the signal contains only frequencies within a finite range, the DAC's lowpass smoothing filter can exactly restore the continuous waveform between the discrete samples

## 4. Aliasing and the Sampling Theorem

- **Aliasing (foldover)** — when too few samples per cycle are taken, the reconstructed signal has a *different* frequency than the original, sounding at the wrong pitch; an unacceptable distortion of a musical signal
- **Foldover formula** — for an input above half the sampling frequency: \( \text{new frequency} = \text{sampling frequency} - \text{original frequency} \). Example: 30 kHz fed to an ADC sampling at 48 kHz reconstructs as \( 48 - 30 = 18 \) kHz
- **Sampling (Nyquist) theorem** — stated by Harold Nyquist (1928): to reconstruct a continuous signal from its samples, the sampling frequency must be at least *twice* the highest frequency in the signal (at least two samples per period)
- **Nyquist frequency** — the highest reproducible frequency, equal to half the sampling rate; usually set above the \~20 kHz hearing limit, so the sampling rate must exceed 40 kHz. At 44.1 kHz the Nyquist frequency is 22.05 kHz
- **Antialiasing vs. anti-imaging filters** — the *antialiasing filter* sits before the ADC, removing input content above half the sampling frequency to prevent aliasing; the *lowpass anti-imaging* (smoothing) filter sits after the DAC, connecting samples into a continuous waveform

## 5. Practical Concerns: Sampling Rate and Jitter

- **Audio interface** — external box with high-quality ADCs/DACs and mic/line preamps connected via USB, Thunderbolt, or Ethernet; far better than built-in computer/phone converters. Prices range from \< $100 home units to \> $10,000 multichannel professional units
- **Standard rates** — the AES recommends 32, 44.1, 48, and 96 kHz, with multiples (88.2, 176.4, 192, 352.8, 384, even 768 kHz) in use
- **High-resolution tradeoffs** — higher rates widen bandwidth and reduce *temporal blur*, *pre-echo*, and *ringing* from brick-wall filters, but produce far larger files (192 kHz/24-bit is \~9× the size of 44.1 kHz/16-bit) and heavier processing loads. Microphones like the Sanken CO-100K capture up to 100 kHz
- **Frequency headroom** — at 44.1/48 kHz, synthesis must emit only sine waves above \~11–12 kHz (since nonsinusoidal partials can exceed the Nyquist rate), and downward *pitch-shifting* of standard-rate recordings muffles tone because content above Nyquist was already filtered out
- **Jitter** — time-based error from an unstable ADC/DAC clock, audible as high-frequency clicking; worsened by clock instability, poor cables, impedance mismatches, or software. Remedy: a *master wordclock generator* synchronizing all devices
