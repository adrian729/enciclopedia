# Ch 23: Concatenative Synthesis

## Table of Contents

- [1. Overview and Background](#1-overview-and-background)
- [2. The Basic Algorithm](#2-the-basic-algorithm)
- [3. Describing Units](#3-describing-units)
- [4. Selection, Sequencing, and Approaches](#4-selection-sequencing-and-approaches)
- [5. Case Studies](#5-case-studies)

## 1. Overview and Background

- **Concatenative synthesis** — automatically assembles new sound from recorded material, mechanizing what tape-splicing once did by hand (Cage's *Williams Mix* took six people nine months); goals range from performances "more real than sampling" to wild remixes (e.g. mapping an orchestra onto monkey sounds)
- **Conceptual lineage** — a form of sampling, vector, or granular synthesis driven by an engine of sound analysis, description, and comparison; also a *dictionary-based* method where the corpus is a dictionary (*codebook*) of atoms. Related to *micromontage* composition (Roads) and tape works like Xenakis's *Analogique B* and *Concret PH*
- **Other names** — *audio/sound/music mosaicking*, *reconstructive phrase modeling*, *audio analogies*, *descriptor-driven transformation*
- **Speech connection** — many text-to-speech systems (e.g. Siri) concatenate *diphones* — adjacent phoneme pairs — extracted from recorded speech; an alternative ML approach uses massive speech databases (Google Assistant's neural-net *Wavenet*)
- **Tools** — *CataRT* (IRCAM, real-time, navigates a descriptor space with the mouse), *MuBu Toolbox*, and free software *AudioGuide* and *SuperSampler*; *Metasynth* can map a sound's spectrum onto an arbitrary corpus, acting like a concatenative synthesizer

## 2. The Basic Algorithm

- **Target, corpus, result** — the aim is to create a *result* resembling a *target* sound using material from a *corpus* (a collection of sound recordings)
- **Pipeline** — analyze the target, segment it into *units*, *describe* each unit, search the corpus for the best matching unit, then combine selected units into the result
- **Unit** — a segment of audio, e.g. a 100 ms windowed segment or an entire musical note
- **Descriptor (feature)** — a quantitative value or qualitative label describing a unit's content (e.g. spectral centroid, note name)
- **Non-audio targets** — the target may instead be a score, MIDI data, or interactive control/gestures, which the algorithm analyzes into target-unit descriptions to guide selection
- **Segmenting into units** — simplest is a sliding window (as in short-time Fourier analysis); richer parsing finds onsets, notes, transitions, beats, instruments, and melodies, requiring acoustic/perceptual/musical knowledge. Automated methods are scalable but sensitive to the audio: speech/silence and phonemes segment reliably, but extracting single notes from mixtures and segmenting general music remains open research

## 3. Describing Units

- **Three descriptor levels** — selection compares a unit's description to the target's at low, mid, or high level:

| Level | Definition | Examples |
|---|---|---|
| **Low-level** | Quantitative, no acoustic/musical model (like descriptive statistics) | *mean energy*, *zero-crossings rate*, *spectral centroid* (frequency below which half the energy lies), *spectral quantiles*, *spectral rolloff*, MPEG-7 descriptors |
| **Mid-level** | Involves a model | *harmonicity* (strength of integer relations among spectral peaks), *fundamental frequency*, frequency-masking from a perceptual model, formant locations from autoregressive modeling |
| **High-level** | Semantic, what people use to discuss music | note, duration, dynamic, instrument, tempo, loudness |

- **High-level caveats** — semantic descriptors need units of appreciable duration (a low pitch or a tempo needs minimum time/multiple beats) and rely on modeling human perception; single-pitch and tempo estimation are mature, but instrument ID in polyphony, source separation, and genre/emotion recognition are unsolved

## 4. Selection, Sequencing, and Approaches

- **Nearest-descriptor selection** — pick the corpus unit whose descriptors are closest to the target's (e.g. target "C4 on oboe" → next-best "C4 on English horn"; target centroid 1,500 Hz → unit at 1,490 Hz)
- **Unit transformation** — selected units can be reshaped to fit the target or neighbors via envelope shaping, time-stretching, or pitch shifting; decomposing samples into sinusoids + transients + noise enhances transformability
- **Specificity** — comparing low-level descriptors is *high specificity* (close to the raw samples but not necessarily perceptual content); comparing mid- or high-level descriptors (models, notes) is *low specificity*, moving from acoustic-pressure samples to *content*, *objects*, or *lexemes*
- **Naïve approach** — selects and sequences units ignoring original context (orchestra-to-monkeys mosaics, micromontage, library navigation); augmented with varied unit durations, randomness, and fallback rules when no match is found
- **Context-aware approach** — selects, transforms, and sequences units sensitive to context, considering several units at once (a complex problem solved with path-following methods), as in text-to-speech and Synful Orchestra

## 5. Case Studies

- **Hybrids** — both case studies combine concatenative and additive synthesis
- **Vocaloid** — Yamaha's singing emulator (Bonada and Serra 2007), a database of vocal fragments covering all phoneme combinations (diphones, sustained vowels, polyphones); e.g. *sing* = #-s, s-I, I-N, N-# plus sustained *I*, with fragments pitch-shifted to the melody and three-to-four pitch ranges stored for naturalness
- **Synful Orchestra** — expressive instrument performance from MIDI via *reconstructive phrase modeling* (RPM), a diphone-like concatenation. Its database stores recorded phrases (attack, sustain, release, transition units) not as raw audio but in a *residual pitch, loudness, and harmonics + noise* (RPLHN) sinusoidal-additive + noise model, separating breath/bow noise as sampled signals; MIDI is converted by rules into a target satisfied by closest-unit selection plus pitch/loudness/duration transformation. RPM exploits the correlation that a harder-blown instrument is louder and brighter, and relies on recorded continuous phrases (detached, slurred, portamento) to supply the rapid note-to-note fluctuations that give realism
