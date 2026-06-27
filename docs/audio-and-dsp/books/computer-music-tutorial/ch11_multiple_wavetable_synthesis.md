# Ch 11: Multiple Wavetable Synthesis

## Table of Contents

- [1. Overview](#1-overview)
- [2. Wavetable Cross-Fading (Vector Synthesis)](#2-wavetable-cross-fading-vector-synthesis)
- [3. Wavestacking](#3-wavestacking)

## 1. Overview

- **Multiple wavetable synthesis** — a family of two simple but sonically effective methods, *wavetable cross-fading* and *wavestacking*, defined by the use of *several wavetables* as their essential trait (other methods like FM can also use multiple tables but aren't classified here)
- **Purpose** — a central technique in popular synthesizers; creates lively, animated cross-faded and stacked hybrids by blending sampled and synthetic waveforms into exotic time-varying sounds
- **Origin** — Horner, Beauchamp, and Hakken (1993) coined the term; best classified as a variant of additive analysis/resynthesis, and viewable as a wavestacking instance where the wavetables are sums of sinusoids from an analysis/data-reduction stage

## 2. Wavetable Cross-Fading (Vector Synthesis)

- **Wavetable cross-fading** — instead of repeatedly scanning one wavetable (the static timbre of fixed-waveform synthesis, chapter 6), the oscillator *cross-fades* between two or more wavetables over an event: waveform 1 fades out as waveform 2 fades in, etc., so the sound mutates or morphs from one source to another
- **Aliases by vendor** — the core of *vector synthesis* / *wave sequencing* (Sequential Circuits, Korg, Yamaha), *L/A* or *linear arithmetic* (Roland), *dynamic spectral wavetable synthesis* (Waldorf PPG Wave), and *wavetable morphing* (XferRecords Serum). Each wavetable has its own amplitude envelope
- **Hardware lineage** — first commercial implementation was the eight-voice Sequential Circuits Prophet VS (1985), cross-fading four waveforms; followed by the Korg Wavestation (1990, software reissue 2010) and the 64-voice Korg Wavestate (2020)
- **Control and wave sequencing** — cross-fading can be automatic (note-triggered, modulated by a cross-fade function) or manual (joystick); some synths let a single event cross-fade through an arbitrary number of waveforms (e.g. 128) — *wave sequencing* — producing animated sweeps with radical timbre and pitch shifts unlike any acoustic instrument
- **L/A synthesis** — Roland's *linear arithmetic* (D-50, 1987; revived in the D-05, 2017) grafts sampled attack transients onto the front of a composite of a subtractive waveform (filtered sawtooth or pulse) mixed with a continuously loopable sampled waveform; a defining sound of its era
- **Piston Honda** — an extreme example: a Eurorack module (Industrial Music Electronics) with a bank of 512 wavetables arranged as an 8×8×8 cube (*X, Y, Z*) indexed by faders or LFOs, either morphing smoothly or stepping abruptly between tables for highly animated timbral contrasts

## 3. Wavestacking

- **Wavestacking** — a simple variation on additive synthesis in which each event sums several waveforms (typically four to eight); implemented in the hugely successful Korg M1 (over 250,000 sold, 1988–1995; reissued as iM1 for iPad in 2015)
- **Difference from classical additive synthesis** — instead of summing pure sine waves, each stacked waveform can be a complex signal such as a *sampled sound*; layering them creates hybrid timbres like saxophone/flute or violin/clarinet, and each has its own amplitude envelope so sounds fade in and out during the event
- **Implementation** — a library of waveforms is scanned by table-lookup oscillators; each waveform's envelope must be scaled by \( 1/n \) (where \( n \) is the number of stacked waveforms) so the sum stays within the synthesizer's quantization range and avoids numerical overflow
