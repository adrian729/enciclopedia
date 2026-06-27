# Ch 42: Sequence Editors

## Table of Contents

- [1. Tracks, Lanes, and Controller Data](#1-tracks-lanes-and-controller-data)
- [2. Loop and Step Sequencer Models](#2-loop-and-step-sequencer-models)
- [3. Visual Representations for Editing](#3-visual-representations-for-editing)
- [4. Editing Operations and Sharing Data](#4-editing-operations-and-sharing-data)

## 1. Tracks, Lanes, and Controller Data

- **Sequence editor** — the tool for editing the MIDI data a sequencer records: *note-on*/*note-off* messages (with key velocity = how hard/fast a key was pressed) and *controller data* (positions of wheels, pedals, knobs, plus mouse-drawn data). It is a core function of *digital audio workstations* (DAWs)
- **Track** — a unit of musical organization; can be tied to one MIDI channel or hold many. MIDI 1.0's sixteen-channel limit does *not* apply to software instruments, so a DAW like Pro Tools allows an arbitrary number of tracks without channel worries; *takes* of a line can be kept in separate tracks, selecting one for the final mix or muting to switch between the best parts of several
- **Controller lane (automation lane)** — where controller data is displayed and edited. Two kinds: *generic MIDI controller data* (velocity, volume, mute, pan, pitch bend, aftertouch, program change, sysex) applying to any plug-in, and *specific controller data* (e.g. a filter's on/off, type, gain, center frequency, *Q*) for one plug-in
- **Discrete vs. continuous display** — *discrete* values (e.g. note velocity) appear as vertical spikes whose height is the value; *continuous controller data* appears as a drawable envelope. Lanes can be superimposed over the piano roll or shown beneath the track

## 2. Loop and Step Sequencer Models

- **Loop/pattern orientation** — breaks a sequence into *subsequences* (patterns) that can be looped, combined, or externally triggered, and operated on like note events. *Ableton Live* is a classic example: audio clips are *warped* (time-stretched) to fit bar lines, imported MIDI snaps to a metric grid, and Session-view clips triggered by mouse or the Push controller wait for the next bar to start. *Studio One* lets a MIDI pattern be inserted anywhere on the timeline at the current tempo
- **Step sequencer** — has a limited number of *steps* and typically loops at the end; classic analog units (Moog, Buchla) offered 8–48 steps, with modern analog equivalents in EuroRack format (e.g. MakeNoise Brains/Pressure Points). Software step sequencers like *Numerology* emulate but surpass them — multiple parallel sequences, each with an arbitrary number of steps, sharing a common clock

## 3. Visual Representations for Editing

- **Data entry methods** — opening a pre-existing MIDI file, playing an input device in real time, entering data non-real-time with keyboard and mouse, or generating from another app (e.g. Max) routed in via *ReWire*
- **Piano roll notation** — derives from player-piano punched rolls; note events run left-to-right on a timeline, pitch laid out vertically, start time and duration shown as a dot or horizontal line (e.g. Reaper)
- **Event list** — recorded MIDI as text sorted in time order, showing event type, channel, and data; the most detailed view, used for fine-tuning. Types include note, control change, pitch bend, program change, aftertouch, poly pressure, system exclusive, and *meta events* (manufacturer-specific)
- **Common music notation (CMN)** — some DAWs transcribe MIDI into raw notation (Digital Performer's QuickScribe, Pro Tools via Sibelius, Cubase/Nuendo's Score Editor); manual cleanup is needed, and scores export as XML for refinement in Dorico, Finale, or MuseScore
- **Metrical grid / drum editor** — a grid whose horizontal axis is time subdivided by beat resolution (a 4/4 measure shows 4 or 16 divisions) and whose vertical rows are percussion instruments; a coarser *overview grid* shows one box per measure, shaded if it contains events
- **Controller envelopes and faders** — continuous controller messages (from pitch/vibrato wheels, foot pedals, breath controllers) drawn as envelopes applied to a note, selection, or track, with a palette of line/curve/random tools; recorded *fader* movements enable automated mixing
- **Audio waveforms** — waveform clips sit in audio tracks alongside MIDI tracks, movable and editable, ideal for seeing time alignment between MIDI and audio; some sequencers convert audio to MIDI (pitch detection) and MIDI to audio (rendering through a plug-in synth)

## 4. Editing Operations and Sharing Data

- **Edit modes** — beyond insert/delete/copy/paste, edits can be *real-time replacement* (*punch-in/punch-out*, tied to the Record button), non-real-time *step mode* (note by note, often drawing note lengths with the mouse), or *random-access* (editing any point of a displayed event list or piano roll)
- **Operation groups** — editing divides into time/tempo, pitch, amplitude, aftertouch, channel, program change, continuous controller, and sysex:

| Group | What it does |
|---|---|
| Time and tempo | *Quantization* (round rhythms to a meter) and *dequantization*/humanizing; millisecond time offsets for feel; inserted or curved tempo changes |
| Pitch | Transposition, pitch bend, vibrato; scale alignment, reflection, arpeggiation, density thinning/thickening |
| Amplitude | Adjust per-note *velocity* (or compress/expand a region's velocities); apply crescendi/diminuendi via a MIDI volume controller envelope (affects loudness regardless of velocity); MIDI mute on/off |
| Aftertouch | *Channel/mono aftertouch* transmits only the highest held value; *polyphonic aftertouch* transmits per key |
| Channel | Reassign channel numbers — akin to reorchestration, since channels map to voices |
| Program change | Insert *program change messages* to select a synth voice/patch |
| Continuous controller | Vary timbre over time (e.g. map filter center frequency to a controller envelope) |
| System exclusive | *Sysex* dumps recorded at a point in time, usually patch data such as envelope settings |

- **Sharing sequence data** — trivial between identical sequencers (swap native files); otherwise via real-time transfer or the *standard MIDI file* (.smf/.mid) format. Real-time transfer runs app A playing while app B records, over a MIDI interface or network (MacOS Audio MIDI Setup Network/Bluetooth icons), or between apps on one machine via a virtual MIDI bus (IAC Driver on MacOS, MIDI Yoke on Windows, ALSA or JACK + Catia on Linux)
- **ReWire** — ReasonStudios' protocol (supported by Digital Performer, Logic, Ableton, Pro Tools, Sibelius, Cubase, Reaper, Max, etc.) transfers MIDI and audio tracks in real time between two programs, enabling on-the-fly transformation — e.g. generating algorithmic MIDI in Max and recording it into a DAW
