# Ch 43: Sound Editors, DAWs, and Audio Middleware

## Table of Contents

- [1. Three Tools and Their Roles](#1-three-tools-and-their-roles)
- [2. Sound Editors](#2-sound-editors)
- [3. Digital Audio Workstations](#3-digital-audio-workstations)
- [4. Audio Middleware](#4-audio-middleware)

## 1. Three Tools and Their Roles

- **Sound editor** — operates on one or two tracks of sound in fine detail; mainly a time-domain (pressure-graph) tool for recording and modifying sampled waveforms
- **DAW (digital audio workstation)** — organizes dozens of tracks and potentially hundreds of *audio clips* (recorded segments, each in its own file) imported into a *session*, positioned independently in time and mixed with MIDI instrument tracks
- **Audio middleware** — an interface for linking sounds to events in an interactive environment, supporting games, *virtual reality* (VR), and *augmented reality* (AR)

## 2. Sound Editors

- **From tape splicing to digital** — editing once meant physically cutting and *splicing* magnetic tape (raised to an art by Bernard Parmegiani's *De Natura Sonorum*, 1975); digital editors replaced it, using *crossfading* — a gradual transition from one signal to the next — to make splices seamless
- **Nondestructive editing** — *rehearsable* / *nondestructive* editing keeps the original alongside rehearsal edits in memory buffers, saving the new sequence only when confirmed; equivalent to an *undo facility*
- **Random-access history** — random-access media (hard disk, semiconductor memory) retrieve any sample as fast as any other, enabling graphical-waveform editors. Pioneers: Stanford's experimental Edsnd and S editors (1970s); Soundstream (first company, storing up to eighty-four *track-minutes* on a PDP-11 disk). Early commercial editors on *serial media* (tape) had no waveform display (Sony PCM-1610, 1981); Fairlight and Synclavier added displays at high cost; Digidesign's *Sound Designer* for Apple Macintosh (1984) edited sounds for the hardware samplers of the day
- **Display as a lens** — a time-domain display zooms from microseconds to minutes; zooming is essential to set an edit's scope (a minute-wide overview to find a silent gap, sample-level resolution to find a transient click). Editors show amplitude, amplitude in dB, linear/log spectrum, and pitch curve (e.g. Audacity)
- **Core operations** — record, cut, splice (with hand-drawn or menu crossfades), replacement and assembly edits, move, mix, synchronize to video, time-stretch without pitch change, pitch shift (with or without duration change), equalize, sample-rate convert, envelope tracing/reshaping, and spectrum analysis/resynthesis
- **Fade curves** — *linear*, *quarter-sine*, and *logarithmic*; logarithmic fades apply more effective energy, avoiding the *"hole in the middle"* energy drop in a crossfade
- **DC offset** — *direct current* (DC) offset, or *0 Hz*, is a constant signal (from hardware or some plug-ins) that shifts the waveform off the zero-amplitude center; it robs apparent loudness, causes clicks, shrinks dynamic range (worst for bass), and accumulates when offset tracks are mixed. Remove it with a 20 Hz highpass filter

## 3. Digital Audio Workstations

- **Editor vs. DAW** — a sound editor edits one file and saves it; a DAW loads dozens of files as clips on multiple tracks, positioned/cut/copied/pasted on a timeline and rendered to a mixed-down file. The line blurs in multitrack apps like Audacity and Adobe Audition, but a modern DAW is far more than a multitrack mixer
- **Evolution** — first interactive graphical editing/mixing apps were SoundEdit (1986, Steve Capps) and MacMix (1987, Adrian Freed); Opcode's *Studio Vision* (1990) was the first DAW to integrate MIDI tracks with audio tracks. Since then DAWs added automation lanes, synced video, common music notation, plug-in instruments/effects, hardware control surfaces, and network sharing — hundreds of features (many tailored to niches like postproduction or Dolby Atmos/Ambisonics), though the basics learn quickly
- **Typical features** — volume/pan automation, *groups*, *auxiliary (aux) sends* (route to a bus for processing), *track inserts* (plug-in/hardware effects or instruments), *Master Fader*, *VCAs* (emulate voltage-controlled-amplifier console channels), *render in place* (bounce MIDI/audio with all settings to a new track), sound↔MIDI conversion, keyboard shortcuts, audio alignment, drum/chord/pitch editors, and mastering tools (EQ, dynamics, imaging, K-System and EBU loudness metering, phase metering, oscilloscope)
- **Comparing DAWs** — named competitors include Pro Tools, Cubase, Ardour, FL Studio, Studio One, Nuendo, Logic Pro, ACID Pro, Ableton Live, Bitwig Studio, Digital Performer, Reaper, Reason, Samplitude Pro, Cakewalk Sonar, LMMS, Rosegarden, and GarageBand. They differ by platform (Ardour/LMMS/Rosegarden = Linux; FL Studio/Samplitude = Windows; Logic Pro/GarageBand = Apple), license (free/open-source Ardour, LMMS, Rosegarden vs. commercial), and price (under $100 to well beyond $100,000)
- **Orientation and extensibility** — loop/beat-oriented DAWs (Ableton Live, FL Studio, ACID Pro) warp clips to the bar for pop production; Pro Tools is common in TV/film dialog mixing, Nuendo in game audio (native middleware connectivity). Ableton's Session view (originally for DJ performance) and Bitwig's Clip Launcher plus modular *GRID* support live use; *Max for Live* and Reaper's scripting language let users build custom instruments, LFO modulation, and effects. The Avid S6 console uses *EUCON* (Avid's Ethernet control protocol)

## 4. Audio Middleware

- **Purpose** — lets composers and sound designers integrate music and sound into interactive environments (games, VR/AR like Oculus, flight simulators) with minimal text coding, via a *GUI* and a function library that works with a game or VR development system, sparing programmers from reinventing each project
- **Named tools** — early examples were Microsoft's *DirectSound* (1995–2012) and *DirectMusic* (1996–2008); current apps include *AudioKinetic Wwise*, *FMOD Studio*, *Elias Studio*, and *Fabric* (a Unity plugin), serving game engines such as Unity, Unreal, and CryEngine, and providing C/C++ functions for developers
- **Connecting sound to game logic** — the core task is deciding how sounds are triggered, with what real-time effects, and in what order; designers run the game engine (e.g. Unity) alongside the middleware to test triggering and monitor CPU, memory, and audio level
- **Managing sound assets** — an *asset* is any file built into a project (sounds, 3D models, animation, code); middleware links sound files to named in-game events, caching instant sounds while *streaming* latency-tolerant ones (e.g. music) from disk. Default *sound banks* exist, but designers usually prepare custom assets in a DAW
- **Real-time treatment and 3D** — middleware automates real-time effects (spatial movement, early reflections, reverberation, filtering, pitch shifting, granulation) on untreated mono files, supports 3D sound for immersive worlds, and sometimes provides haptic feedback
- **Adaptive music** — a mix that changes in response to conditionals (player position, probabilities) — dynamically fading tracks in/out or re-orchestrating; an adaptive system senses when the music should change, waits for the right moment, and cues a smooth transition into a new section
