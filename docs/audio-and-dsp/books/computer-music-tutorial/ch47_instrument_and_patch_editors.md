# Ch 47: Instrument and Patch Editors

## Table of Contents

- [1. Template Editors versus Patchers](#1-template-editors-versus-patchers)
- [2. Historical Background](#2-historical-background)
- [3. Template Editor Example: FM8](#3-template-editor-example-fm8)
- [4. Patch Editor Example: Max](#4-patch-editor-example-max)
- [5. Other Patchers: REAKTOR and VCV Rack](#5-other-patchers-reaktor-and-vcv-rack)
- [6. Modular Patching in DAWs and Eurorack](#6-modular-patching-in-daws-and-eurorack)

## 1. Template Editors versus Patchers

- **Instrument editor** — a GUI tool that "opens the hood" of a digital synthesizer, giving users access to the synthesis engine to design and tune instruments
- **Template editor** — gives access to a *predefined* synthesis engine: the number of oscillators, envelopes, filters, and other modules — and the way they interconnect — is fixed at the factory; e.g. Sound Quest's Midi Quest, a universal editor/librarian for classic Korg, Roland, Yamaha, and other hardware that tunes and saves presets back to the instrument via MIDI
- **Patch editor (patcher)** — a toolkit letting one design instruments from freely interconnectable modules, also called a *visual programming language* (VPL); the term *patch* comes from the patch cords of modular synthesizers, and the earliest VPL was the GRAIL flowchart interface (1969)
- **Patcher freedom** — unlike a template editor, a patcher lets a musician create arbitrarily many modules (up to processing limits) connected in arbitrary ways (e.g. 29 oscillators into 17 filters), with patches encapsulated by nesting; connection, disconnection, and triggering create musical events
- **Trade-offs** — template editors are easy to learn with GUIs optimized for one method; patchers demand a major commitment and others' patches are hard to read, but they enable rapid prototyping of new synthesis and interactive-composition systems
- **Blurred distinction** — some template editors allow limited patching (e.g. routing modulation) or offer template sets; some patchers (OpenMusic, PWGL) are icon-based and focused on composition rather than synthesis

## 2. Historical Background

- **Analog roots** — modular analog synthesizers gave hands-on patch design but no way to save a patch except detailed notes; a 1970s Moog III had \~150 knobs and 35 switches, and repatching could take hours
- **Unit generator lineage** — the modular toolkit idea also lived in the *unit generator* of Music III/IV/V (Tenney, Mathews); but Music V was a compiled text language with no real-time interaction, so patch diagrams were drawn on paper then translated to text
- **Early template editors** — the Graphical Input (GRIN) system (Bell Labs, Mathews and Rosler) compiled light-pen drawings into envelope and waveform definitions for Music IV, also controlling tempo curves and quadraphonic spatial paths (Chowning 1971); the SSSP's *Objed* sound-object editor (Toronto, 1978–1983) used interactive vector graphics and graphic potentiometers to edit FM instrument waveforms and envelopes
- **Editor/librarians** — after MIDI (1983) and bit-mapped GUIs, software editor/librarians (Opcode a leader) manipulated MIDI *system exclusive* data, editing *bulk patch data*; e.g. the Yamaha DX7's entire 32-patch capacity fit in a 4,096-byte memory
- **Early patchers** — *MITSYN* (William Henke, MIT speech scientist, 1970) connected modules like a pulse-train generator into a filter for voice-like sound; Oedit and Stanford's Reved (patching comb and allpass filters into reverberators) followed
- **Max and Pure Data** — Miller Puckette's *Max* (originally *Patcher*, 1988) processed MIDI to control synthesis hardware, became commercial via Opcode (1989) then Cycling '74 (1990); Max/MSP added audio in 1997; *Pure Data* (Pd) is Puckette's open-source relative, separating asynchronous control messaging from synchronous block-based audio computation
- **Further systems** — Fly30 (Rome's Centro di Ricerche Musicali), Clavia's Nord Modular (downloadable patches to standalone hardware), Carla Scaletti's *KYMA* (template + patching with custom hardware), the Kronos signal-processing language with its Veneer touch front-end, and Troikatronix Isadora for audiovisual performance

## 3. Template Editor Example: FM8

- **Native Instruments FM8** — a software synthesizer emulating the Yamaha DX7 with added reverberation and effects, shipping with hundreds of preset libraries; most users only tweak presets
- **Expert window** — gives access to a patch's internals, letting users adjust waveforms and envelopes and even *repatch* the synthesis circuit of interconnected signal generators — but only within the constraints of the Yamaha FM architecture

## 4. Patch Editor Example: Max

- **Max** — a widely used graphical icon-based toolkit for interactive performance of music and visuals, designed for musicians rather than computer scientists; takes input from MIDI, OSC, audio, video, and microcontroller sensor data (Arduino, Raspberry Pi), and outputs MIDI/OSC, audio/video, or messages to other apps
- **Extensions** — *Max for Live* embeds the patching environment inside Ableton Live; *Gen* compiles visual patches into custom Max objects and extends control to the individual-sample level
- **Patch** — a graphical configuration of object boxes connected by patch cords; a complex patch can be collapsed into a single object for nesting; a patch is in *edit mode* (change connections, add objects from the palette) or *run mode* (interact with it as it reacts to mouse, keyboard, MIDI, and sound)
- **Messages and \_bang\_** — objects respond to inlet messages/signals by sending through outlets; messages carry numbers, symbols, lists, or the symbol *bang* (a trigger/semaphore to start and stop processes)
- **Message boxes** — "wireless" transmitters that send arbitrary messages (separated by semicolons) to named *receive* objects without patch cords; a leading semicolon means "nothing to send out the outlet," and clicking a box in run mode acts like a *bang*
- **Control vs signal objects** — control objects process event-triggered messages, while *signal-processing objects* (named with a trailing tilde, e.g. `cycle~`, `sig~`, `line~`, `adc~`, `dac~`) flow at the audio sampling rate; `sig~` converts control-rate numeric messages into audio-rate signals
- **Waveform generator patch** — a `start` message turns on `dac~`; `line~` generates a ramp (target value over a duration in ms, e.g. 0 to 0.1 in 1000 ms) serving as an amplitude envelope; on the MIDI side, `notein` → `stripnote` → `mtof` converts a note number (60, middle C) to a frequency (261 Hz); `sig~` (default 440) feeds `cycle~`, whose cosine output is scaled by the multiplier `*~` and split to two channels (signals range −1.0 to 1.0)

## 5. Other Patchers: REAKTOR and VCV Rack

- **REAKTOR** — Native Instruments' visual programming environment of basic modules connected by wires; a REAKTOR *instrument* (synth, sequencer, effect) bundles internal structure, MIDI processing, panel, and snapshots (presets), with a large factory library and thousands of user additions
- **REAKTOR \_blocks\_ and Euro Reakt** — *blocks* emulate modular-synth modules, each a separate instrument patchable to others; Michael Hetrick's *Euro Reakt* is a 100+ block collection (Buchla-style lowpass gate, wavefolder, probability router, drum voice, frequency shifter, quadrature LFO, wavetable distortion, Boolean logic) focused on generative composition, multi-output effects, and flexible modulation
- **VCV Rack** — a simulated Eurorack software synthesizer (Andrew Belt, 2017), open source with free core software; notable free modules include a near-complete set of Mutable Instruments modules under the name Audible, plus modules from dozens of developers

## 6. Modular Patching in DAWs and Eurorack

- **Patching within DAWs** — all DAWs host synth plug-ins; some add modular patching: Apple's Environment (virtual MIDI studio), FL Studio's Patcher (chaining instruments and effects), Reason's patchable rack, Ableton's Max for Live, and BitWig's integrated modular synth *The Grid*
- **Eurorack integration** — connecting laptop software to modular hardware is straightforward; interfaces like MOTU's pass DC control voltages (envelopes) as well as analog audio, and a module like the Expert Sleepers ES-8 sends and receives audio and control voltages on a Eurorack synthesizer
