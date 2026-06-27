# Ch 5: History of Digital Sound Synthesis

## Table of Contents

- [1. Earliest Computer Sounds](#1-earliest-computer-sounds)
- [2. Bell Labs and the First Sample Synthesis](#2-bell-labs-and-the-first-sample-synthesis)
- [3. Music I and Music II](#3-music-i-and-music-ii)
- [4. The Modular Unit Generator Concept](#4-the-modular-unit-generator-concept)
- [5. The Music N Family](#5-the-music-n-family)

## 1. Earliest Computer Sounds

- **Sonifying computation** — early computers had no visual displays, so programmers monitored a machine by the audible radio interference it produced; when the sound stopped, the computer had halted
- **Audio-rate loops** — a repeating program loop running at an audio rate produced a sustained pitch; programmers wrote loops of varying lengths matching popular melodies for amusement
- **"Blurt" / "hoot"** — on machines with a loudspeaker output, raw 1-bit pulses sent over the serial bus, interspersed with delays, produced a pitched tone
- **First musical machines** — in 1949 Frances E. "Betty" Holberton programmed the BINAC to play "For He's a Jolly Good Fellow"; in 1951 the Australian CSIRAC and the British Manchester Mark II played tunes the same way. None were formal research
- **No DAC yet** — digital-to-analog converters for sound samples did not exist, so generalized waveform synthesis was impossible

## 2. Bell Labs and the First Sample Synthesis

- **Theory of sampling** — the most general way to control a computer-generated waveform is to synthesize it per the 1928 *theory of sampling* of Harold Nyquist, a Bell Labs communications researcher
- **Max V. Mathews** — an MIT electrical-engineering doctorate who, under J. R. Pierce at Bell Telephone Laboratories (Murray Hill, NJ), began the first sound-sample synthesis experiments in 1957
- **What they proved** — Mathews's program made a computer generate a sequence of binary numbers (samples) representing successive amplitudes of a sound wave, demonstrating a computer could synthesize any pitch scale or waveform, with time-varying frequency, amplitude envelopes, and polyphony
- **IBM 704** — the first programs ran on this vacuum-tube machine (36-bit word, built-in floating-point, up to 32 kwords of core, up to 4,000 multiplications/sec); billed at $600/hour in 1957 dollars at IBM headquarters in Manhattan
- **First sound DAC** — a 12-bit vacuum-tube converter designed by Bernard Gordon, then the only one in the world capable of sound production, turned the tape-stored samples into sound

## 3. Music I and Music II

- **Music I** — Mathews's first program; generated a single fixed waveform (an equilateral triangle) and let a user specify notes only by pitch and duration
- **First D-to-A composition** — Newman Guttman's monophonic etude *In a Silver Scale* (May 17, 1957), the first composition synthesized by digital-to-analog conversion, contrasting an equal-beating chromatic scale with just intonation
- **Music II (1958)** — written in assembly for the faster IBM 7090; offered four independent voices and a choice of sixteen stored waveforms, enabling more ambitious algorithms
- **Spreading the idea** — a 1958 New York concert (panel moderated by John Cage) presented the new *computer music*; Guttman's *Pitch Variations* was later played at Hermann Scherchen's villa in Gravesano, Switzerland, with Iannis Xenakis in the audience

## 4. The Modular Unit Generator Concept

- **Unit generators (UGs)** — signal-processing modules (oscillators, filters, amplifiers) that can be interconnected to form synthesis *instruments* or *patches*; the most important development in synthesis-software design
- **Music III (1960)** — programmed by Mathews and Joan E. Miller, the first synthesis language built on the modular UG concept; users designed their own synthesis networks from UGs, and routing the signal through a series of them made many algorithms easy to implement, including polyphony
- **Music From Mathematics (1961)** — historic Bell Labs recording of computer-generated studies by Pierce, Mathews, Guttman, and David Lewin, plus an excerpt of Lejaren Hiller's algorithmic *Illiac Suite for String Quartet*

## 5. The Music N Family

- **Music IV** — a re-coding of Music III in BEFAP, a macro assembly language developed at Bell Labs
- **Music V (1968)** — the culmination of Mathews's software-synthesis work, written almost entirely in FORTRAN IV and exported worldwide to universities and labs in the early 1970s
- **Music N languages** — the general rubric for the family of UG-based systems descended from Music IV/V: Music 4BF, Music 360, Music 7, Music 11, Csound, MUS10, Cmusic, Common Lisp Music, SuperCollider, ChucK, Synthesis ToolKit, Nyquist, and Max
- **Mathews's legacy** — as inventor of the modular unit-generator paradigm for generalized waveform synthesis, Max V. Mathews (1926–2011) is the father of computer-generated sound; synthesis from modular graphs of UGs remains the standard for flexible, experimental synthesis
