# Ch 44: Spectrum Editors

## Table of Contents

- [1. What a Spectrum Editor Is](#1-what-a-spectrum-editor-is)
- [2. Command-Line, Plug-In, and Static Editors](#2-command-line-plug-in-and-static-editors)
- [3. Envelope Editors](#3-envelope-editors)
- [4. Sonographic Sound-Transformation Editors](#4-sonographic-sound-transformation-editors)
- [5. Repair, Restoration, and Source Separation](#5-repair-restoration-and-source-separation)

## 1. What a Spectrum Editor Is

- **Spectrum editor** — a tool that operates on *partials in the frequency domain*, in contrast to a sample editor working on waveforms in the time domain; it first analyzes a sound file (usually via the *fast Fourier transform*, FFT) to build a representation of its frequency content
- **Distinction from filters** — the time-domain filters of chapters 14 and 28 also modify spectra, but spectrum editing here means editing frequency-domain data obtained *after* an analysis of the incoming waveform
- **Range of purposes** — understanding sound evolution, decluttering a mix, removing an unwanted sound, *de-mixing* / *un-mixing* a recording into its sources, denoising, transcription, remixing, and creative sound transformation (overlapping with graphic synthesis)
- **No common paradigm** — because applications are so disparate, editors target different users; the book groups them as command-line/plug-in, static, envelope, and sonogram-like graphical editors

## 2. Command-Line, Plug-In, and Static Editors

- **Composers Desktop Project (CDP)** — a command-line software package (largely written by Trevor Wishart) for "surgical work inside sounds"; e.g. `spec cut infile outfile starttime endtime`; offers spectral blurring, freezing, tracing, harmonizing, pitch shifting, stretching, randomization, interpolation
- **SoundMagic Spectral** — Michael Norris's freeware MacOS plug-in implementation of CDP algorithms, working in *set-then-do* mode (tune parameters, then Apply); plug-ins include Spectral Freeze (holds each bin at its peak), Spectral Blurring, Spectral Tracing (keeps only loudest bins), Spectral Harmonizer, and Spectral Weave (sustained spectral "threads" woven contrapuntally)
- **Static spectrum editor** — a "timeless" frequency-versus-amplitude display showing *which* frequencies are present but not *when*; the Passport Designs Alchemy editor (1988) let users edit individual partial levels, but altering low frequencies also alters the hidden time structure (the analysis window period is the fundamental), introducing waveform discontinuities — limiting its musical usefulness

## 3. Envelope Editors

- **Envelope editing for additive resynthesis** — represents spectrum information as a control envelope per partial; James Beauchamp (University of Illinois) pioneered computer-based analysis and data-reduction of these envelopes with Andrew Horner and Lydia Ayres
- **Phase-vocoder motivation** — James A. Moorer's phase-vocoder analysis produced a time-varying amplitude and frequency function per channel, generating data many times larger than the original file; this drove editors (Strawn's eMerge) to reduce data and creatively transform envelopes before resynthesis
- **Manual labor and \_breebles\_** — hand-adjusting harmonics of every note is impractical; over-rapid amplitude changes in upper harmonics produce audible artifacts Strawn called *breebles*, so line-segment data-reduction algorithms are preferred

## 4. Sonographic Sound-Transformation Editors

- **Sonogram / spectrogram** — plots frequency (vertical) versus time (horizontal), with amplitude shown as darkness or color; any frequency-versus-time display is a *sonographic representation*
- **MetaSynth CTX** — analyzes a sound or image into a sonogram that can be resynthesized with *any* other sound on an arbitrary scale and time base, acting like a concatenative synthesizer (e.g. speech played back by percussion samples)
- **SpecDraw and AudioSculpt** — the SpecDraw prototype (Eckel 1990) let users draw and resynthesize sonograms, later absorbed into IRCAM's AudioSculpt (phase-vocoder based); AudioSculpt offers spectrum/envelope/f0/partial-tracking analysis, a breakpoint editor, region filtering, a harmonic pencil, and *noise signature* removal; IrcamLab TS2 reuses its engine for pitch-time effects
- **\_Common fate\_** — partials sharing a vibrato pattern (McAdams and Bregman) can be encircled to extract a vocal part from an orchestra
- **In sound editors** — Audacity (spectrogram view) and Adobe Audition let users draw a spectral region and apply any plug-in effect; Audition adds an FFT filter giving direct amplitude control of many bands (e.g. 2,048), at the cost of latency and possible ringing
- **Tracking phase vocoder (TPV) / sinusoidal modeling** — follows the most prominent spectral peaks over time; LemurEdit edited Lemur TPV analyses, and Klingbeil's freeware *SPEAR* lets users select partial tracks and pitch-shift, time-shift, frequency-shift, or frequency-flip them; ATSH edits ATS (sinusoidal-plus-critical-band-noise) analyses; SCATTER used atomic decomposition (granular counterpart) to separate transients from sustained tones and spatialize grains

## 5. Repair, Restoration, and Source Separation

- **Repair editors** — iZotope RX (de-click, de-clip, de-hum, denoise) and Steinberg SpectraLayers Pro (de-reverb, de-crackle, de-plosive, repair broken harmonics, clone) target restoration but can also be used creatively (e.g. poking a cavity in a speech spectrum)
- **Source separation** — *un-mixing*/*de-mixing* isolates voices/instruments into component tracks (e.g. extracting a vocal for remix); products include Melodyne, Auto-Tune, ReVoice Pro, Xtrax Stems; methods combine pitch estimation, spectral pattern recognition, statistics, dynamic programming, and trained recurrent neural networks
- **ISSE** — the free, open-source Interactive Source Separation Editor uses *interactive machine learning*: painting colors on a sonogram labels sources, refining a *nonnegative matrix factorization* (NMF) core through iterative human feedback
- **RipX DeepRemix / DeepAudio** — Hit'n'Mix sinusoidal-modeling tools with a painting-program interface for manipulating pitch, duration, timbre, formant, and volume (via the editor or Python), with Clone tools that transfer one note's property to another
