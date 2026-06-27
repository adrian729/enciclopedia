# Ch 1: Background

## Table of Contents

- [1. What Synthesis Is](#1-what-synthesis-is)
- [2. Synthesis Methods](#2-synthesis-methods)
- [3. Origins and History](#3-origins-and-history)
- [4. Acoustics Fundamentals](#4-acoustics-fundamentals)
- [5. Electronics Fundamentals](#5-electronics-fundamentals)
- [6. Digital Audio and Sampling](#6-digital-audio-and-sampling)
- [7. MIDI](#7-midi)
- [8. Computers, Software, and Virtualization](#8-computers-software-and-virtualization)

## 1. What Synthesis Is

- **Sound synthesis** — the process of producing sound, whether generating it electronically/mechanically or reusing and processing existing sounds; it blends art and science (musical skill plus technical expertise), and the tools alone don't make the music.
- **All instruments are "synthesizers"** — the vocal tract, a violin, a clarinet all produce sound by essentially synthetic methods; in popular use "synthesizer" has narrowed to mean an electronic instrument that can make a wide range of (often "synthetic") sounds.
- **Two functional blocks** — every synthesizer has a *control interface* (sets the parameters) and a *synthesis engine* (turns parameters into output); an abstraction or model usually sits between them so the user needn't know the inner workings. Models and abstraction are a recurring theme of the book.
- **Performance vs. modular** — performance synthesizers have fixed internal signal paths (fast to use, limited, the commercial majority); modular synthesizers have no fixed connections (very flexible, slow to patch, mostly academic/research). A synthesizer with no keyboard or controller is an **expander** or **module**.
- **The keyboard isn't ideal** — the music keyboard became the dominant controller but is arguably a poor one; its choice has been called "the biggest setback" to the synthesizer's acceptance as a musical instrument.
- **Sound categories** — *imitations/emulations* (mimic real instruments), *suggestions/hints* (e.g., 1970s "synth brass" — just enough cues to suggest brass), *alien/off-the-wall* (entirely synthetic), *noise-like* (white noise has equal energy across the audible band), and *factory presets* (demo sounds, often drenched in reverb and a poor guide to true capability).
- **Source-and-modifier model** — many techniques use a raw sound source shaped by a modifier (the "excitation and filter" model borrowed from speech synthesis); clearest in subtractive synthesis. Easier-to-grasp metaphors (subtractive, S&S) have proved the most commercially successful.

## 2. Synthesis Methods

- **Analogue families** — *subtractive* (filter harmonics out of a harmonically rich raw wave; the resonant low-pass "filter sweep" is its cliché), *additive* (sum many sine waves; the difficulty is controlling so many oscillators), and *wavetable* (more sophisticated stored waveshapes as the starting point).
- **FM (frequency modulation)** — modulate one audio-frequency signal with another to create complex spectra; hard to program intuitively, but in the 1970s it needed very little memory to store many sounds. First described by John Chowning (1973 paper, later patented) and commercialized by Yamaha.
- **Wavetable and sample replay** — wavetable loops and splices short sample segments (memory-efficient, lower quality); *sample replay* plays back complete samples with a loop for the sustain (memory-hungry, now ubiquitous), marketed as AWM, RS-PCM, and similar.
- **S&S (samples and synthesis)** — combines wavetable/sample replay with the digital filtering and shaping of subtractive synthesis; the dominant commercial technique, sold under coined names like HI, XA, AI2, and VX.
- **Physical modeling** — mathematical equations describing how an instrument works; the model responds like a real instrument, so real playing techniques transfer. Its heavy processing limited it to pro gear in the mid-1990s; "modeling" is now a generic term, marketed as VCM, MMT, etc.
- **Software synthesis** — powerful general-purpose computers replace the traditional rig (sequencer, synthesizer, mixer, effects, recorder), doing everything on digital signals; the audio becomes analogue only for monitoring or final playback.

## 3. Origins and History

- **Human roots** — synthesis begins with the species: the vocal tract is a biological synthesizer, and the ear-and-brain pairing forms an **analysis–synthesis** feedback loop (the same idea reused later in resynthesis).
- **Telecoms research** — the telephone, the **vocoder** (Bell Labs, 1930s, from "VOice enCODER"), and especially **PCM** (pulse code modulation) for digitizing audio all came out of telecommunications; the **DSP** chip followed in the 1970s. Cahill's Teleharmonium (1906) even distributed music down telephone lines.
- **Tape techniques** — the analogue tape recorder enabled splicing, tape loops, reversing, sound-on-sound, and multi-tracking; varispeed ties pitch and duration together (doubling speed raises pitch an octave but halves length). Pierre Schaeffer coined **musique concrète** (1948) for music built from recorded "found"/prepared sounds.
- **Research to product** — academic prototypes are innovative but fragile and resource-hungry; commercial products are cost-optimized variants, often renamed for marketing. Walter Carlos's *Switched-On Bach* (Moog) brought synthesis to the public, the Yamaha DX7 (1982) made FM a mass-market success, and the Fairlight CMI (1979) launched commercial sampling.
- **Cyclic fashion** — synthesis techniques fall in and out of favor; FM, analogue modular, and "retro" sounds have repeatedly been rediscovered and re-marketed (often re-created in software).

## 4. Acoustics Fundamentals

- **Sound = vibration** — pressure waves (compressions and rarefactions) traveling through a medium; **frequency** (in hertz) is the rate of pressure change and the **period** is the time for one cycle.
- **Pitch vs. frequency** — frequency is objective and measurable; pitch is musical and can be subjective. A4 = 440 Hz; an octave doubles frequency; the equal-tempered semitone ratio is the 12th root of two (≈1.0595); a semitone divides into 100 **cents** (the ear detects about 5).
- **Fundamental, harmonics, partials** — the **fundamental** is the lowest major frequency (the pitch you'd whistle); **harmonics** are integer multiples (the harmonic series); **overtones/partials** are not integer-related. A higher fundamental leaves fewer audible harmonics within the hearing range.
- **Phase and interference** — a cycle spans 360°; in-phase signals add (**constructive interference**), 180°-opposed signals cancel (**destructive interference**). Two slightly different frequencies produce **beating** — a level wobble whose rate equals the frequency difference, often used to "liven up" analogue sounds.
- **Timbre** — "tone color," set by the harmonic content and how it evolves over time; missing harmonics give a hollow sound, and non-integer frequency ratios give bell-like or noise-like timbres.
- **Loudness and decibels** — the **dB** is a logarithmic ratio (named after Bell); ≈1 dB is just audible while ≈10 dB sounds "twice as loud," and the whole range from silence to pain is only about 12 power doublings. Musicians instead use dynamics marks (ppp to fff).
- **Envelope (ADSR)** — a sound's volume over time: **attack**, **decay**, **sustain**, **release**; very fast events are **transients** (the ear's time resolution is roughly 10 ms).

## 5. Electronics Fundamentals

- **Core quantities** — *voltage* (potential difference), *current* (electron flow), *resistance* (Ohm's law, `V = I × R`), and *power* (`P = V × I`). **Capacitors** store charge; **inductors** store energy as a magnetic field.
- **Active devices** — **transistors** use a small current or field to control a larger one (so they act as amplifier or switch); **diodes** pass current one way; **integrated circuits** pack many transistors onto silicon, leading to microprocessors and **DSPs** (processors optimized for signal math).
- **Analogue electronics** — works with continuous signals where any distortion changes the actual value (a 4 V vs. 4.1 V error can shift an oscillator's tuning); **op-amps** with feedback are the basic gain block, and **filters** (frequency-dependent gain) are central to synthesizers.

## 6. Digital Audio and Sampling

- **Digital = numbers** — values are stored in binary (bits, bytes, MSB/LSB); **ROM** holds the operating system and **RAM** holds working data — samplers need a lot of it.
- **Sampling** — converting analogue to digital: sample the signal, convert the value to a number, output it, repeated at the sample-clock rate (a CD does 44,100 samples per second). The reverse — number to voltage to audio — is **sample replay**, the basis of nearly every digital synthesizer.
- **PCM (pulse code modulation)** — encodes each sampled value as a number, unlike PAM/PWM/PPM, which keep size/width/position analogue; uncompressed digital audio uses **Linear PCM**.
- **Conversion chain** — ADC: anti-aliasing filter → sample-and-hold → ADC chip → RAM; DAC: RAM → DAC chip → deglitcher → reconstruction filter → audio.
- **Nyquist criterion** — sample at a rate at least twice the highest frequency present; sampling faster adds no information but can simplify filter design.
- **Aliasing** — any frequency above half the sample rate folds down and masquerades as a lower frequency — a one-way loss of information — so anti-aliasing (input) and reconstruction (output) filters are required.
- **Resolution** — more bits mean more available values (`D = 2ⁿ`) and a wider dynamic range, roughly 6 dB per bit (16-bit ≈ 96 dB, "CD quality"). Cutting volume by dropping bits introduces grainy **quantisation noise**, so volume is better scaled at full resolution with a multiplying DAC.

## 7. MIDI

- **What MIDI carries** — not audio but musical *events* (note pressed, drum hit, sequencer stopped), sent as numeric "messages" over a serial interface; an **opto-isolator** (LED plus light-sensitive transistor) keeps sending and receiving devices electrically separate to avoid hum.
- **Layers** — the **physical layer** (the opto-isolator circuit), the **transport** (how bits are framed), and the **protocol** (how the 8-bit messages carry meaning) — the same terms used in computer networking.
- **Ports and connections** — *in*, *out*, and *thru* ports (5-pin DIN); the single rule is "connect an out or thru to an in," with information flowing from a controller source to a sink.
- **Channels and modes** — 16 channels per cable (like TV channels, or "omni" to receive any); operating modes are monophonic, polyphonic, and multi-timbral.
- **Common messages** — *note on* (carries channel, key, and **velocity**; a velocity of 0 means note off), *pitch-bend*, *after-touch* (pressure once the key bottoms out), *program/bank changes* (select sounds — GM/XG/GS standardize the mapping), *continuous controllers* (e.g., the mod wheel), and *system exclusive* (sysex) for manufacturer-specific data.

## 8. Computers, Software, and Virtualization

- **General-purpose machines** — computers descend from calculators and automation (Jacquard's punched-card loom); programmability with **branching** is what makes them general-purpose. They appear as embedded, server, and desktop/laptop forms.
- **Object-oriented programming** — splits software into self-contained **objects** that each know how to do one thing, so specific knowledge lives only where it's needed; this simplifies, debugs, and maintains complex software — the same abstraction theme as the synthesizer's control interface.
- **Virtualization and plug-ins** — software presents apparently physical resources (a reverb unit, a mixer, a tape recorder) that are really just code; **plug-ins** are standardized, encapsulated software objects that make or process sound, yielding a flexible sound-making environment. There is no real plug or socket — even the term is a virtualization.
