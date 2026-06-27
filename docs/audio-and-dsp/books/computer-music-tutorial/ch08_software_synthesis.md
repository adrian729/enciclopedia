# Ch 8: Software Synthesis

## Table of Contents

- [1. Hardware vs. Software Synthesis](#1-hardware-vs-software-synthesis)
- [2. History of Software Synthesis](#2-history-of-software-synthesis)
- [3. Types of Software Synthesizers](#3-types-of-software-synthesizers)
- [4. Real-Time vs. Non-Real-Time Synthesis](#4-real-time-vs-non-real-time-synthesis)
- [5. Audio Programming](#5-audio-programming)

## 1. Hardware vs. Software Synthesis

- **Real time** — completing all calculations for a sample within one sample period; a system that takes ten seconds to compute one second of sound is a *non-real-time system* and must write output to a file for later listening
- **Motivation for hardware** — early computers were too slow for real time, so specialized digital hardware was built to synthesize sound live
- **Yamaha DX7 (1983)** — a breakthrough mass-produced keyboard using specialized chips for *frequency modulation* (FM) synthesis; sold for under $2,000, over 200,000 units, and defined much 1980s pop
- **Software synthesis** — running all sample calculations on a general computer with no extra hardware; the most flexible approach, since fixed hardware (e.g. the DX7's FM-only chips) cannot realize other synthesis methods

## 2. History of Software Synthesis

- **Music V (Mathews 1969)** — an early software synthesis language: one wrote a program in the language and executed it, a non-real-time process that could take hours. Its source was classic FORTRAN IV with GOTO control flow
- **Orchestra and score** — a Music V program pairs an *instrument* (e.g. an oscillator feeding an output box) with a *score* of note statements; each note statement gives starting time, instrument number, duration, amplitude, and pitch
- **Speedups** — by the mid-1970s synthesis languages ran on minicomputers, cutting waits to minutes for short experiments; by the late 1980s the first real-time software arrived: Csound (1990), SuperCollider (1996), Seer Reality (1997), and Max/MSP (1997) on home computers
- **Today** — countless real-time software synthesizers exist; e.g. any user of the Native Instruments REAKTOR modular system can design and publish a synth, yielding thousands on that platform alone

## 3. Types of Software Synthesizers

| Category | Trait / example |
|---|---|
| **Closed apps** | Optimized for one technique, not freely reprogrammable; e.g. Native Instruments FM8, which emulates a Yamaha DX7 |
| **Patchable apps** | A limited fixed set of modules with some patching; e.g. NI Absynth (twelve *semimodular* slots), Madrona Labs Aalto (a Buchla-style West Coast synth) |
| **Virtual modular synthesizers** | Software emulations of vintage modular hardware; Arturia's Modular V (2003, with Robert Moog), VCV Rack, Cherry Audio Voltage Modular |
| **Graphical instrument patch editors** | Build patches by wiring icons (UGs) on screen, any number of modules; e.g. Max, PureData, AudioMulch |
| **Textual synthesis languages** | Specify sounds in text interpreted by a synthesis engine; Csound, Nyquist, ChucK, Faust, SuperCollider |
| **Custom apps in general-purpose languages** | Ultimate customization/efficiency; most market synths are coded in C++ |

- **Standalone vs. plug-in** — commercial synths can run *standalone* or as a *plug-in* inside a *digital audio workstation* (DAW); plug-ins allow multiple *instances* and recording as they play
- **Code libraries** — vital for custom C++ apps, solving common tasks: GUI (ImGui, JUCE), audio I/O (PortAudio, RtAudio), MIDI (RtMidi), signal processing (Pedal, STK), music information retrieval (FluCoMa)

## 4. Real-Time vs. Non-Real-Time Synthesis

- **Moore's law fading** — Moore's law (1965) predicted transistor density would double each year; by 2012 it began losing relevance as microprocessor clock speeds stalled below 4 GHz; chip makers turned to *multicore* processors, but many real-time interactive audio algorithms do not benefit from *multithreaded* processing
- **The timing budget** — each step of a synthesis algorithm takes time; at a 50 kHz sampling rate the budget per sample is 20 microseconds, so if six lookup steps take \~1 µs, a computer could run only about twenty simple oscillators in real time. Adding interpolation, filters, reverb, more channels, GUI updates, and interaction pushes work into the non-real-time domain
- **Non-real-time (offline) synthesis** — a substantial delay between computing and hearing a sound; the only option in early computer music. A two-minute portion of J. K. Randall's *Lyric Variations for Violin and Computer* (1965–1968, Princeton) took nine hours to compute, and any tweak meant recomputing
- **Faster than real time** — many tasks render quickly: a multitrack mix lasting minutes can render to a sound file in seconds in a DAW like Pro Tools, Logic, or Ableton Live
- **Sound files** — output stored on disk; formats include WAVE and AIFF. A sound file holds a *header text* (name, sampling rate, bits per sample, channel count) plus the numbers representing samples; utilities like SoundHack convert between formats
- **Return of hardware** — by the 1980s tiny chips realized multivoice synthesis in real time in cheap synths; 1990s *sound cards* embedded similar chips in computers; later the *Eurorack* phenomenon brought hardware (analog and digital) back alongside software
- **Real-time advantage** — controllers played as sound is heard give expressive *gestural control*, fast exploration of a method's parameter space, and recording/editing via *sequencers* and *score editors*; live control uses MIDI or OSC

## 5. Audio Programming

- **Depth of the field** — entire books cover it; *The Audio Programming Book* (Boulanger and Lazzarini 2011) runs over 3,000 pages, and language-specific texts exist for SuperCollider, Csound, Max, Pd, ChucK, FAUST
- **Audio I/O management** — environments like SuperCollider and Max handle I/O automatically; in C/C++ the programmer is more responsible, though libraries like libsndfile, PortAudio, and ROLI's JUCE (favored by professionals) handle low-level details
- **Block processing and latency** — real-time synthesis generates a *block* of samples at a time (typically 32 to 2,048); larger buffers guard against glitches but add *latency* (delay from synthesis to hearing)
- **Audio callback loop** — the mechanism for low-latency audio: it repeatedly takes a block of samples from the synthesizer into a memory buffer and sends it to the output. Because processing a block may exceed one sample period and competes with OS processes, a single buffer risks *dropouts* — hence *double-* or *quad-buffering*, where one buffer plays while another is filled
- **Plug-in standards** — the spread of software synths is fostered by formats: Steinberg's Virtual Studio Technology (VST, 1996), Apple's Audio Units (AU), and LV2 for Linux
