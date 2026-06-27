# Ch 27: Dynamic Range Processing

## Table of Contents

- [1. Envelope Shapers and Gates](#1-envelope-shapers-and-gates)
- [2. Compressors](#2-compressors)
- [3. Expanders, Limiters, and Companders](#3-expanders-limiters-and-companders)
- [4. Sidechaining and the Loudness War](#4-sidechaining-and-the-loudness-war)

## 1. Envelope Shapers and Gates

- **Dynamic range processing** — a family of techniques that transform a signal's amplitude, underlying *envelope shapers*, *gates*, *compressors*, *limiters*, *expanders*, *noise reduction units*, and *companders*; uses range from cleaning noisy signals to creatively reshaping an instrument's envelope
- **Envelope shaper** — rescales a sampled sound's overall amplitude envelope, either a simple gain change (dB up/down) or a redesigned envelope (e.g. rounding off a harpsichord's sharp attack into a sustained ring)
- **Gate** — a switch that opens when a music signal exceeds a *threshold* and shuts (maximally attenuating) when the signal drops below it, removing residual hiss/hum; its *attack time* sets how fast it reacts and *release time* how long until it ungates. Works only when the music masks the noise — it cannot remove noise while music plays
- **Creative gating** — beyond noise removal: rhythmic enhancement (a percussion track gating another sound), transient shaping, drum replacement, and even granulation with short attack/decay times

## 2. Compressors

- **Audio vs data compression** — an *audio compressor* reduces a signal's dynamic range/level in real time (analog or digital); *data compression* shrinks a file's bit size. The first industry to adopt compressors was radio broadcasting, as *automatic gain control* to prevent overmodulating the transmitter
- **Compressor** — an amplifier whose gain is controlled by its own input: when the input rises above an upper bound it is attenuated, keeping output level roughly constant. Characterized by its *transfer function* mapping input amplitude to output amplitude (same representation as waveshaping synthesis)
- **Detector** — monitors the input envelope; a *peak* detector reacts to instantaneous peaks (insurance against overload), while an *average* / *root mean square* (RMS) detector responds over \~1–2 s for smoother behavior
- **Threshold** — the level (relative to 0 dB / unity gain) above which compression acts; a \(-40\) dB threshold is more drastic than \(-10\) dB because much more of the signal is compressed
- **Threshold knee** — sets the inflection of the response curve: *soft knee* curves gradually, *hard knee* compresses fully the instant the threshold is crossed; a hard knee with high ratio turns a compressor into a limiter
- **Compression ratio** (*input/output ratio*) — change in input vs change in output; a normal amplifier is 1:1, while 3:1 means a 3 dB input change yields only 1 dB out. Above \~8:1 the signal audibly squashes (flattened transients, distortion); 10:1 makes pop vocals "intimate," and extreme compression gives electric guitars a sustained *sostenuto* effect
- **Attack time** — how fast (in ms) the compressor reacts to sounds above threshold; a few ms can let percussive hits pierce through
- **Release time** — how fast it returns to uncompressed once below threshold; too long and quiet sounds following a loud one get over-reduced
- **Makeup gain** — boosts the whole signal to compensate for the compressed peaks; key to extremely compressed (*phat*) drum tracks where the transient is squashed and the resonance boosted and sustained
- **Multiband compressor** — *band-splits* the input into frequency bands, each compressed separately with its own curve, so side effects are confined to chosen bands. Can run as a frequency-domain device on spectrum-analysis data (e.g. Pro Audio DSP Dynamic Spectrum Mapper) and substitute for time-varying EQ (Waves C4, FabFilter Pro MB)

## 3. Expanders, Limiters, and Companders

- **Expander** — the opposite of a compressor: it exaggerates small input changes into wide output changes; an *expansion ratio* of 1:3 turns a 1 dB input change into 3 dB out. Multiband compressors also expand, focusing on a narrow band
- **Limiter** — extreme compression with ratios beyond 10:1 and a flat threshold knee; input-to-output is linear up to the threshold bounds T, then output stays constant regardless of input. Useful in live recording to keep a digital recorder below its absolute input level, beyond which harsh numerical clipping distortion occurs
- **Noise reduction units / companders** — *compander* = *compressor* + *expander*: compress on recording (boosting signal well above the recorder's noise floor) and expand on playback to restore the original dynamic range, yielding low-noise yet wide-dynamic-range recordings. Multiband companding can produce audible artifacts on glissandi crossing band boundaries (Lagadec and Pelloni 1983)

## 4. Sidechaining and the Loudness War

- **Sidechain (key) input** — lets a signal other than the one being processed control the effect; a vocal can *duck* an instrument's level to make room for it, or a sidechained percussion track can gate another track to enliven rhythm
- **Adaptive effects** (*content-based transformations*) — a generalization of sidechaining: a feature analyzed from a control track drives an effect on the same or another signal (e.g. bass in track 1 controls reverberation on track 2) (Reiss and Brandtsegg 2018)
- **The Loudness War** — named by mastering engineer Bob Katz (2002): compressors let engineers make recordings maximally loud at all times, flattening percussive transients; some pop albums vary under 3 dB end to end. Listeners often just turn the volume down, defeating the purpose
- **Compression is distortion** — reducing amplitude modulates it (AM), generating spectral sidebands; processors react globally regardless of musical context. The *cause–effect* delay is reduced by *lookahead* (delaying the input to anticipate triggering waveforms); too-fast attack causes the well-known *pumping* sound. No single setting suits more than one sound, so settings are a compromise — though distortion is precisely what many pop producers seek
- **Parallel compression** — mixes an uncompressed track with a heavily compressed copy, retaining transients while boosting quiet and attenuating loud sounds, for a thicker mix (especially vocals) (Robjohns 2013)
- **Manual compression** — re-enveloping tracks event-by-event in a sound editor, applying makeup gain to soft passages while leaving transients intact; slower than a compressor but gives the finest amplitude control with minimal transient distortion
