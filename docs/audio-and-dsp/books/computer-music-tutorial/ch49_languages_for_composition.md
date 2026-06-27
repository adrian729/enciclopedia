# Ch 49: Languages for Composition

## Table of Contents

- [1. Categories and Origins](#1-categories-and-origins)
- [2. Score Input Languages](#2-score-input-languages)
- [3. Procedural Composition Languages](#3-procedural-composition-languages)
- [4. Embedded and Live Coding Languages](#4-embedded-and-live-coding-languages)
- [5. Live Notation Languages](#5-live-notation-languages)

## 1. Categories and Origins

- **Four basic types** — composition languages divide into score input languages, procedural composition languages, languages embedded in general-purpose languages, and live coding / live notation languages; the categories overlap (Christopher Ariza lists one hundred systems from 1966–2007)
- **Score input vs procedural** — *score input languages* encode already-composed scores for analysis or synthesis; *procedural languages* foster a generative/algorithmic approach, generating events by stipulated procedures or rules. Some serve both (note lists in SuperCollider, procedures in the score-input language Abjad)
- **MUSICOMP** — the original composition environment: a library of assembly-language subroutines by Robert Baker and Lejaren Hiller, run on the ILLIAC I at the University of Illinois. It offered functions for probability-weighted list selection, list shuffling, tone-row manipulation, melodic-rule enforcement, and rhythmic coordination. Baker called it a "facilitator" with no compositional logic of its own; Hiller used it for his *Computer Cantata* (1963)

## 2. Score Input Languages

- **Purpose: data entry** — score input (a.k.a. *music markup*) languages transcribe *common music notation* (CMN) into alphanumeric code; pioneers DARMS (Erickson 1975) and MUSTRAN (Wenker 1972) targeted musicology, faithfully transcribing graphic symbols (measures, metrical rhythms, equal-tempered pitches, slurs, ties, parts) for archiving or analysis
- **MusicXML** — the modern standard for interchanging scores between notation apps; though verbose, it is easy to generate and parse algorithmically, and over two hundred notation programs read/write it. SMDL was an earlier XML-compliant effort
- **Music information retrieval (MIR)** — builds large-scale collections (audio, symbolic, metadata) for data mining. KernScores holds over 100,000 pieces in the `**kern` format, analyzed with the Humdrum Toolkit (e.g. querying whether Stravinsky's dissonances favor strong metric positions). Commercial MIR instead analyzes tens of millions of songs for recommendation and marketing
- **MIDI and optical scanning** — MIDI sequencers and printing packages reduced the need for score input languages, but MIDI was never designed to read/write CMN symbols. *Optical music recognition* is a pattern-recognition problem: WABOT-2 (Waseda University, Sadamu Ohteru) read a sheet in \~10 seconds; the first commercial OMR app was MIDISCAN (now SmartScore, 1991); machine-learning methods now apply
- **The performance problem** — a score is an incomplete description; rote playback sounds wooden because performative gestures (e.g. slight time/amplitude exaggeration of phrase structure) are unencoded. Remedies are explicit phrase-structure representation, or formalized, style-dependent performance rules (Sundberg, Friberg, et al.)

## 3. Procedural Composition Languages

- **Generative focus** — *procedural composition languages* go beyond traditional scores to support alternative tunings, multiple timbre/spatial envelopes, voice interplay, performer interaction, and compositional algorithms; they represent music as interacting processes, emphasizing *mesostructure* (patterns and phrases)
- **Two advantages** — compositional logic becomes explicit (formal consistency, prized for abstract unity), and composers extend control over far more processes than manual techniques allow (microfrequency control of partials, sifting massive data, precise spatial paths, rapid variation generation, impossible polyphony, real-time algorithmic accompaniment)
- **No dominant standard** — because no two composers compose alike. Examples in Table 49.1:

| Language | Trait |
|---|---|
| Common Music | LISP-based; score-file generation plus a pattern-oriented composing language |
| Open Music | Incorporates notation; originally for spectral music, extended to theory |
| Nyquist | LISP-based; combines synthesis with algorithmic composition |
| SuperCollider | Object-oriented environment for real-time audio synthesis and algorithmic composition |
| Max / PureData (Pd) | Modular visual patchers for music/multimedia; Pd is open source |
| ChucK | Sound synthesis plus algorithmic composition; arrays/functions for patterns |
| JSyn / jMusic / JMSL | Java APIs for synthesis and computer-assisted composition |
| AthenaCL | Open-source, object-oriented, written in Python |
| SCAMP | Multiple clocks at different tempi for parallel structures |
| OMN | Scripting core of the Opusmodus composition system |

- **Synthesis languages can compose too** — Music V had algorithmic hooks via its PLF routines (Mathews 1969), and several chapters of *The Csound Book* cover algorithmic control of synthesis

## 4. Embedded and Live Coding Languages

- **Embedded languages** — *extensible* host languages let a specialized *embedded language* reuse the host's facilities. LISP/Scheme spawned MIDI-LISP, FORMES, PatchWork, Canon, Common Music, and Opusmodus; Python's readability and modularity made it popular for adding scriptable interfaces to existing applications; KYMA (Scaletti and Hebel) revolves around a Smalltalk patcher. Cmusic and Music 4C were embedded in C; the MusicKit used Objective C; JMSL is a Java API
- **Live coding** — a branch of computer art: real-time coding of a sonic/multimedia performance with the code text often displayed. Pioneers include Ron Kuivila (Forth onstage, 1980s) and The Hub; Nick Collins advanced it early 2000s; TOPLAP (2004) promotes it and Algoraves
- **Live coding languages (Table 49.2)** — ChucK (strongly timed, concurrent, on-the-fly), Extempore (Scheme + xtlang), Impromptu (Scheme/LISP), ixi lang, Lua/LuaAV, Max, Pharo (Smalltalk-inspired), Pure (schedules Faust UGs), Pure Data, Sonic Pi (Ruby + a SuperCollider engine), SuperCollider, TidalCycles (embedded in Haskell, for audible/visual patterns), and the Wolfram Language
- **Note list returns** — although gestural control replaced the stored Music N note list in many performances, in live coding the performer types events; a common strategy is to spawn algorithmic variations from an initial note list

## 5. Live Notation Languages

- **Real-time notation** — emerged at the confluence of live coding, gestural interactive composition, and mixed instrumentalist/laptop ensembles; pioneered by Roger Dannenberg's Temporal Programming Language (1996)
- **Music21** — a Python-based toolkit for computer-aided musicology, supporting dataset queries plus notation scripting and both algorithmic and directly specified composition
- **Abjad** — embedded in Python, helps composers build complex notation iteratively and make systematic changes; generates output via the LilyPond notation package and has been tested with algorithmic input in performance
- **MaxScore** — software tools (Didkovsky and Hajdu) integrated with the Max environment; controllable by Max messages, with output read by sound-generating patches for polyphonic and microtonal playback
- **INScore** — an environment for interactive music scores allowing arbitrary graphics; supports CMN via Guido notation or MusicXML, extended with operators that take scores as arguments to compute new scores
