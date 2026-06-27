# Ch 4: Sample Quantization, Conversion, and Audio Formats

## Table of Contents

- [1. Sound Magnitude and Decibels](#1-sound-magnitude-and-decibels)
- [2. Quantization, SNR, and Dynamic Range](#2-quantization-snr-and-dynamic-range)
- [3. Quantization Noise and Dither](#3-quantization-noise-and-dither)
- [4. Oversampling and 1-Bit Converters](#4-oversampling-and-1-bit-converters)
- [5. Audio Media and File Formats](#5-audio-media-and-file-formats)

## 1. Sound Magnitude and Decibels

- **Measures of magnitude** — scientifically distinct but correlated terms: *peak-to-peak amplitude*, *RMS amplitude* (root mean squared, the average power of complex signals like noise), *gain* (input/output ratio), *sound energy* (joules), *sound power* (watts), *sound intensity* (W/m²), *sound pressure level*, and *loudness*
- **Decibel (dB)** — compresses huge exponential ranges via base-10 logarithms (a whisper is a few billionths of a watt, a rocket launch \~10 million watts); the definition shifts with the phenomenon measured
- **dB SPL** — \( \text{SPL in dB} = 20 \log_{10}(W / W_0) \), where \( W \) is the measured sound pressure level and \( W_0 \) is the reference 20 micropascals, the quietest audible sound
- **dB compresses percentages** — 100% = 0 dB, 70% = \~−3 dB, 50% = −6 dB, 25% = −12 dB, dropping \~6 dB per halving of amplitude
- **Inverse square law** — each doubling of distance from a source drops SPL \~6 dB (a 50% amplitude decrease); intensity falls as the square of distance
- **Loudness vs. SPL** — *loudness* is perceived (psychoacoustic) intensity, measured in *phons* (1 phon = 1 dB SPL at 1 kHz); the ear is most sensitive to 1,000–4,000 Hz, so a 30 Hz tone must be boosted \~40 dB over a 1,000 Hz tone to sound equally loud (60 phons)

## 2. Quantization, SNR, and Dynamic Range

- **Quantization** — sampling at discrete *amplitude* intervals (the amplitude counterpart of discrete-time sampling); digital numbers have finite precision and range
- **Bit depth** — bits per sample, also called *sample width* or *quantization level*; more bits → finer amplitude resolution and lower noise
- **Signal-to-noise ratio (SNR)** — ratio of signal strength to noise; the difference in dB between the 0 VU operating level and the noise floor; each added ADC bit contributes \~6 dB
- **Dynamic range (DR)** — difference in dB between loudest and softest reproducible sounds (noise floor to point of distortion); approximated by \( \text{DR in dB} = \text{Number of bits} \times 6.11 \) (theoretical max; \~6.0 is realistic in practice)
- **Bit-depth examples** — 8-bit → \~48 dB (audibly noisy); 16-bit → \~96 dB (the CD standard); 20-bit → \~120 dB, roughly the range of the human ear
- **Linear PCM** — the assumed scheme stores each sample as an integer of its value; other schemes (e.g. MP3) instead aim to reduce stored/transmitted bits

## 3. Quantization Noise and Dither

- **Quantization error / quantization noise** — each sample is rounded to the nearest available level (e.g. 53.x → 53), so it differs slightly from the true value; on complex input the error sounds like noise resembling tape hiss
- **No noise on silence** — unlike analog tape's constant noise halo, digital silence yields all-zero samples and no quantization noise; a pure sinusoid, however, produces a deterministic truncation effect that is audibly gritty at low levels
- **The sampling grid** — fitting a waveform to a time-vs-amplitude grid: finer time grid (sampling rate) → greater bandwidth; finer amplitude grid (quantization level) → greater dynamic range and less noise. A 24-bit sample gives \( 2^{24} \), over 16.7 million possible values
- **Granulation / modulation noise** — at very low but nonzero levels only the lowest bit toggles, forming a square wave rich in odd harmonics whose components can exceed the Nyquist frequency and alias; worsens when a quiet signal is rescaled up
- **Dither** — a small amount (\~3 dB) of uncorrelated noise added before the ADC; it randomizes variations around low-level signals, converting signal-dependent error into wideband noise so tones fade smoothly into a noise bed. The ear can reconstruct tones quieter than the dither itself
- **When to dither** — recommended at 16-bit; often unnecessary at 24-bit, but recommended when *requantizing* 24-bit down to 16-bit to preserve fidelity
- **Converter linearity** — *resolution* is one part in \( 2^n \), but *linearity* is how well the \( 2^n \) steps are evenly spaced; unequal steps cause distortion, so a 24-bit converter may be only 19 bits linear

## 4. Oversampling and 1-Bit Converters

- **Multibit linear converters** — convert a full 16–24-bit sample to/from analog voltage in one step per sample period
- **Oversampling converters** — use more samples in the conversion stage than are stored; most rely on *1-bit oversampling*, converting one bit at a time at a high sampling frequency
- **1-bit converters** — a family called *sigma-delta*, *delta-sigma*, *noise shaping*, *bitstream*, *MASH*, or *direct stream digital (DSD)* (also in Class D amplifiers); they measure only whether the waveform moved positive or negative since the last sample, but do so often enough that 1 bit suffices
- **Width/rate tradeoff** — by Shannon's information theory, sample width can trade off against sample rate at equal resolution; a 1-bit converter oversampling 16× equals a 16-bit converter with no oversampling. Total work \( = \text{Oversampling factor} \times \text{Width of converter} \); a 128× 1-bit system processes \( 128 \times 1 \) bits, 8× the data of a \( 1 \times 16 \) linear converter
- **Noise shaping** — a highpass filter in a feedback loop shifts *requantization error* out of the audio band; a final *decimator* lowpass-filters and reduces the rate, removing that noise. *Second-order noise shaping* yields \~15 dB (2.5 bits) per octave of oversampling minus a fixed 12.9 dB penalty; running a 20-bit converter at 256× gives 24-bit resolution in theory. DSD oversampling reaches 2.8224 MHz and beyond (over 22 MHz)

## 5. Audio Media and File Formats

- **Codec and container** — a *codec* (coder-decoder) encodes/decodes audio data; a file format like AIFF or WAVE is a data structure splitting the file into sections (sample rate, bit depth, channels; raw sample data; markers, loop points, metadata)
- **Three format types** — *uncompressed*, *compressed lossless*, *compressed lossy*

| Type | Examples | Behavior |
|---|---|---|
| Uncompressed | AIFF, WAV; 32-bit *floating-point* (IEEE 754) | Full-resolution PCM, no reduction; FP uses a 24-bit mantissa scaled by an 8-bit exponent for \~1,500 dB dynamic range |
| Compressed lossless | FLAC, ALAC | Exploits redundancy; perfectly reconstructed after unpacking; FLAC reaches \~50% size reduction (ZIP/RAR only \~20%) |
| Compressed lossy | MP3, Vorbis, AAC, ATRAC, WMA | Discards "less audible" data to meet a target bit rate; mediocre quality |

- **Lossless transmission** — bits transfer in real time over standard formats: AES3 / S/PDIF (2 channels), AES10/MADI (56), Ethernet AVB (200), Dante (1024)
- **Perceptual coding** — basing lossy compression on psychoacoustics; MP3 discards frequencies *spectrally masked* by neighbors and tones *temporally masked* by loud events less than \~5 ms before them. An MP3 encoder splits the signal into 32 spectral bands and drops bands below the audition threshold
- **MP3 specifics** — a 128 kbit/s MP3 is \~11× smaller than the equivalent 16-bit 44.1 kHz CD track; *bit rate* (32–320 kbit/s) controls size and quality, with *variable bit rate* (VBR) using low rates for simple passages and high rates for complex ones; playback is essentially additive synthesis
- **Trend** — lossy formats arose when storage was costly and networks slow; with cheap storage and gigabit speeds, audiophiles have moved to high-resolution lossless formats (FLAC, ALAC, DSD)
