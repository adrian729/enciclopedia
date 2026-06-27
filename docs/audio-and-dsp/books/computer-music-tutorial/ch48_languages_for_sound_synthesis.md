# Ch 48: Languages for Sound Synthesis

## Table of Contents

- [1. Formal Languages for Synthesis](#1-formal-languages-for-synthesis)
- [2. The Music N Model: Scores and Orchestras](#2-the-music-n-model-scores-and-orchestras)
- [3. Score Language Features and Limitations](#3-score-language-features-and-limitations)
- [4. Implementation Trade-offs](#4-implementation-trade-offs)
- [5. Real-Time Synthesis Languages](#5-real-time-synthesis-languages)
- [6. Beyond Unit Generators: Open Questions](#6-beyond-unit-generators-open-questions)

## 1. Formal Languages for Synthesis

- **Synthesis vs composition split** — the book divides music languages into sound synthesis (this chapter) and composition (chapter 49); the boundary is pedagogical, since real systems cross it
- **Text languages vs patchers** — this chapter covers text-based languages, not visual patchers like Pure Data (chapter 47); an FM instrument has the same semantics in both but a different interface paradigm
- **General-purpose languages too** — most professional audio developers use C and C++ for apps/plug-ins; MATLAB explicates algorithms in the research literature; Python is common for machine-learning audio. Audio-specific layers (libraries, frameworks, APIs) like JUCE, AudioKit, RtAudio, RtMidi, PortAudio, and libsndfile spare developers from rewriting common operations
- **Why formal languages** — they liberate a music system from canned presets: any imaginable synthesis method or interface can be coded, with precision and efficiency (one command can apply to a massive group of events). *Live coding* — improvised interactive programming for sound-and-image performance — is one offshoot
- **Three strengths, three weaknesses** — synthesis languages offer an open modular toolkit, arbitrarily complex algorithms with arbitrary voice counts, and fine numerical precision; the costs are a learning curve plus software-engineering burden, possible inability to run in real time (forcing render-to-file), and the need to specify masses of minutiae

## 2. The Music N Model: Scores and Orchestras

- **Orchestra + score** — classic languages based on the *Music N* model (e.g., Csound) split work into a synthesis *orchestra* (instruments) and a *score* that invokes it; a compiler reads both, builds the patches, feeds them score data, and renders a *sound file*
- **Unit generator (UG)** — a software module that emits audio or control signals (oscillators, noise/impulse generators) or modifies signals (filters, delays, reverberators, spatializers); a UG's output can patch to virtually any other UG's input, giving great flexibility
- **Lineage** — the first UG language was Music III (Max V. Mathews, Bell Telephone Laboratories, 1960); descendants include Music IV, Music V, Music 11, MUS10, Cmusic, Csound (Vercoe/Karstens 1986), Common Lisp Music, SuperCollider (McCartney 1996/2002), Nyquist (Dannenberg 1997), Faust (Orlarey 2002), ChucK (Wang 2003), and many others
- **Score language's two jobs** — defines the *note list* (instrument names, start times, durations, parameters per *note event*) and the *function tables* (time functions used as waveforms and envelopes)
- **Orchestra language** — a toolkit for building instruments by interconnecting UGs: assign a UG's output to a *signal variable*, then feed that variable into another UG's input. Implemented via shared data arrays in memory that connected UGs read and write
- **Music 0 teaching example** — an imaginary language where `←` means "is assigned"; *parameter fields* (*pfields*, e.g. `p3`, `p4`) carry per-note values from score columns, and *function generators* (line-segment, Fourier, exponential, polynomial) precompute the waveform/envelope tables

## 3. Score Language Features and Limitations

- **Flat note list** — the Music N score is a nonhierarchical list of mostly numeric notes; weaknesses (known since Haynes 1980) are numerical orientation, rigid syntax, and no high-level structures (phrases, voices, clouds, streams, textures, gestures)
- **Score preprocessors** — supply friendlier syntax, e.g. pitch as a pitch-class/octave code like `C4` instead of hertz, converted to a numerical note list before synthesis
- **Expression evaluation** — computation within the score (e.g. `p8 = p7/2`) lets a composer set a few global variables and have the compiler derive specific parameters, easing rapid variation
- **Sound file input** — a UG like Csound's `soundin` reads audio files so filtering, re-enveloping, reverberation, or spatialization can be applied; overlapping note statements cross-fade files, enabling algorithmic mixing. Cmix was built expressly for automated mixing
- **Physical-modeling mismatch** — Chafe (1985) argued note lists suit isolated event calls but not *physical modeling*, which needs multiple parallel processes with variable synchronization (e.g. violin slurs involve asynchrony between the two hands)

## 4. Implementation Trade-offs

- **Extensibility spectrum** — ranges from fully open (Common Lisp Music, embedded in LISP) to closed (Music 11, assembler for the DEC PDP-11); most sit between. Music V was closed but offered Pass 1 / Pass 2 hooks for user-written subroutines; SuperCollider can incorporate C/C++ extensions, and Csound can also be extended (and has been ported to mobile devices)
- **Block vs sample computation** — *block-oriented* compilers compute many samples per parameter load (efficient); *sample-oriented* compilers can change every value per sample (flexible but slower). Music IV, Music 4C, Common Lisp Music, and ChucK are sample-oriented; Music V and Csound are block-oriented (Csound's *control rate* sets block size — too low yields clicks and zipper noise)
- **Note initialization variables** — *i-variables* set once per note, enabling note-to-note control such as glissandi that store where the previous note's pitch left off

## 5. Real-Time Synthesis Languages

- **Asynchronous focus** — real-time languages respond to spontaneous gestural input rather than a prewritten note list
- **Hardware history** — early slow computers forced hybrid digital-control-of-analog approaches (MUSYS at EMS London; Bartlett's KIM-1 program in 1,152 bytes). *Fixed-function* synthesizers (New England Digital Synclavier) wired components in a fixed configuration; *variable-function* DSPs (IRCAM 4X, Stanford Samson Box) let users patch units in software. The Yamaha DX7 and MIDI (both 1983) showed MIDI could simplify synthesizer control
- **Controlling hardware synths** — via front panel, input device, or a program generating MIDI/OSC; MIDI carries discrete note data, continuous controller messages, and program-change messages, plus *system exclusive* messages for synth-specific parameters. OSC is more open and customizable
- **Csound** — a classic UG language with explicit instrument/score separation; users combine opcodes into patches, played by a separate score with a note list; maintains backward compatibility with Music 11 syntax and has evolved into an embeddable library
- **SuperCollider (SC)** — separates the language client (sclang) from the synthesis server (scsynth); object-oriented (drawing on C++ and Smalltalk); designed for live performance, allowing modules to be created/deleted/repatched while sounding, with MIDI and TCP/UDP OSC control plus GUI widgets
- **ChucK** — concise syntax for live coding; processes audio one sample at a time rather than in blocks; a *strongly timed* language with explicit logical-time control to sample-rate accuracy. Chunity embeds it in the Unity game engine
- **Faust** — a *meta-programming language* for DSP; compiles a block-diagram syntax to efficient C/C++/Java code operating at the sample level (enabling one-sample feedback), then to executables, libraries, or plug-ins

## 6. Beyond Unit Generators: Open Questions

- **Questioning the UG paradigm** — can any algorithm, however complex, be encapsulated in a UG, and when does that abstraction hide valuable information? The issue arises in granular/microsound synthesis and in Fourier analysis. ChucK's *unit analyzer* exposes per-frame and per-sample data; Faust builds UG functionality from simpler primitives
- **Parallel processing** — with CPU clock speeds stagnant, developers exploit multiple cores, DSP chips, or *graphics processing units* (GPUs) for physical-modeling, granular, and additive synthesis, at the cost of hardware dependency. Frameworks: OpenCL (heterogeneous CPUs/GPUs/DSPs/FPGAs), OpenMP (multicore C/C++/FORTRAN, used to parallelize Faust), and Nvidia's CUDA (GPU access for C/C++)
