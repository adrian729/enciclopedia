# Ch 51: MIDI

## Table of Contents

- [1. What MIDI Is and How It Connects](#1-what-midi-is-and-how-it-connects)
- [2. Channels, Bytes, and Messages](#2-channels-bytes-and-messages)
- [3. Modes, General MIDI, and Control Change](#3-modes-general-midi-and-control-change)
- [4. Files and Timing](#4-files-and-timing)
- [5. Limitations and MPE](#5-limitations-and-mpe)
- [6. MIDI 2.0](#6-midi-20)

## 1. What MIDI Is and How It Connects

- **MIDI** — the *Musical Instrument Digital Interface*, a protocol (published August 1983 by a consortium of Japanese and American makers; first drafted by Dave Smith of Sequential) that specifies a hardware interconnection scheme, a data-communications method, and a grammar for encoding musical performance information
- **Control data, not sound** — MIDI transmits gestures ("start a note now," "change volume now"), never audio waveforms; timbre is not encoded in a MIDI 1.0 message, so the same message can trigger dissimilar sounds on different synthesizers
- **Separation of control from synthesis** — one input device (keyboard, breath controller, drum pad, guitar) can drive many sound generators, enabling generic device-independent music software and exchange of score/sequencer data between manufacturers
- **Background: hybrid systems** — before MIDI, computers controlled analog synths by sending *control functions* (pitch/amplitude envelopes) through a *demultiplexer* to DACs feeding voltage-controlled modules; pioneers were Bell Labs' GROOVE (early 1970s) and Kobrin's HYBRID
- **Serial asynchronous transmission** — bits are sent one at a time whenever an event occurs, at a standard rate of 31,250 bits/s (1.0 MHz ÷ 32)
- **Traditional ports** — three 5-pin DIN jacks: IN, OUT, and THRU; connections are *optically isolated* to block hum, and a *UART* chip frames incoming bits into 10-bit packets (start bit 0, 8 data bits, stop bit 1) for the device's microprocessor
- **Daisy chaining** — THRU (an echo of IN, not the same as OUT) passes data to the next device's IN; reliable for only \~2 links before opto-isolator pulse smearing causes frame errors
- **USB-MIDI and Ethernet** — bidirectional USB-MIDI carries hundreds of internal channels on one cable (per-channel rate still 31,250 bits/s for compatibility); *RTP-MIDI* (Lazarro and Warzynek 2004) transmits MIDI over Ethernet for long runs (up to 100 m)

## 2. Channels, Bytes, and Messages

- **MIDI channel** — an electronic address label routing a packet to its destination; traditional setups carry 16 channels over one cable, and a channel usually corresponds to one instrument timbre (channel 1 = Piano, etc.)
- **Status vs. data bytes** — a *status byte* begins with 1 and names a function (note-on, pitch-wheel change); a *data byte* begins with 0, leaving 7 bits for a value (0–127). The status byte's first nibble is the function, the last nibble is the channel (`0000` = channel 1)
- **Pitch and amplitude representation** — a note-on carries a 7-bit pitch (\(2^7 = 128\) equal-tempered keys); key 60 is MIDI middle C / C5 (261.63 Hz, nonstandard naming), key 127 is G10 (12,543.89 Hz). Amplitude is a 0–127 *velocity* — how fast the key travels top to bottom
- **Note-on / note-off** — pressing a key sends a 3-byte note-on (channel, key number, velocity); releasing sends note-off (or, by convention, a note-on with velocity 0)
- **Channel voice messages** — the common note-related messages: note-on/off, polyphonic and channel key pressure (*aftertouch*), *pitch bend* (14-bit, 16,384 divisions, applies to all notes on the channel), *program change* (an integer selecting a preset/patch), and *bank select* (extends past 128 patches)
- **System messages** — received by all devices regardless of channel: *system common* (song select, song position pointer), *system real time* (clock, start/stop/continue for synchronizing drum machines and sequencers), and *system exclusive (sysex)* — manufacturer-specific data for dumping patches and parameter settings
- **Running status** — once a status byte is received it persists until a new one arrives, so a burst of notes can be sent as one note-on status followed by data-byte pairs, trimming 3-byte messages to 2 and tightening chord timing

## 3. Modes, General MIDI, and Control Change

- **MIDI modes** — a device interprets channel data by *mode*; in practice only three are used today:

| Mode | Behavior |
|---|---|
| Mode 3 Poly | Default; each device listens to one channel and plays as many notes as it can — most flexible, channels switchable individually |
| Mode 4 Multi | Multitimbral; consecutive channels from a *base channel* each play a preset (used by MIDI guitars: one channel per string; enables per-note pitch bend) |
| General MIDI | Standard channel-patch-sample mapping for cross-system playback |

- **General MIDI (GM, 1990)** — a standard mapping so a sequence sounds roughly the same across systems; requires 16-part multitimbral, 24-voice polyphony, 128 preset patch names (patch 57 = Trumpet), channel 10 reserved for percussion (47 sounds). Aims for similarity, not identical timbre. *GM 2* (1999) raised polyphony to 32 notes and added spatial panning but saw little adoption
- **SoundFonts** — an interchange format (.sf2, a RIFF variant) letting any musician distribute a custom sharable sound palette of wavetable samples plus *articulation data* (envelopes, filters, vibrato range); largely superseded by SFZ and Kontakt formats
- **Control Change (CC)** — messages from non-keyboard controllers (faders, knobs, foot pedals, breath/ribbon controllers, mod wheel); the first data byte is the controller number, the second its value. A controller emits a new CC whenever its position changes
- **RPN and NRPN** — *Registered Parameter Numbers* have functions assigned by manufacturers; *Non-Registered Parameter Numbers* are unassigned and used freely; both extend the available controller set and edit sound patches
- **MIDI Learn** — a mapping mode where the user selects a target parameter, then moves a hardware slider/knob to bind it to that controller automatically (also called MIDI Map)

## 4. Files and Timing

- **Standard MIDI Files (SMF)** — designed by David Oppenheim of Opcode for exchanging sequences (.smf / .mid); unlike real-time messages, every message is *time-stamped* in *clock ticks* (the delta since the previous event)
- **SMF types** — Type 0 = single track (whole composition, tempo map embedded); Type 1 = multitrack with shared tempo/time signature stored in the first track; Type 2 = independent patterns (*drum machine format*, rarely supported)
- **Meta-events** — stored in the file but not transmitted: tempo, time/key signature, track names, lyrics, markers, copyright, end-of-track, and sequencer-specific data (the file equivalent of sysex)
- **MIDI Clock** — a *relative time* system: a one-byte "tick" sent 24 times per beat plus start/stop/continue commands; one device is the *leader* generating ticks, the others are *followers*. Song Position Pointer locates playback to within \~a sixteenth note
- **MIDI Time Code (MTC)** — converts SMPTE *absolute time* (hours, minutes, seconds, frames) into MIDI to sync audio/video tape with MIDI devices; seldom used now that DAWs and video editors handle audiovisual production

## 5. Limitations and MPE

- **Bandwidth limit** — the 31,250 bits/s cable (chosen \~1983 to cost \~$5/device) carries only \~1,000–1,500 messages/s; a single continuous controller (vibrato wheel) can consume nearly a whole channel's bandwidth, causing "MIDI choke" with gaps and jerkiness on dense beats
- **Device and buffer latency** — separate from MIDI: a single oscillator may take \~7 ms to respond, eight "simultaneous" note-ons up to \~21 ms; oversized DAW audio buffers add 100 ms or more, so keep buffers small when recording
- **Music-representation limits** — no representation of timbre (the "canned" quality), pitch is equal-tempered with only channel-wide bending and no tuning spec, and note lists are device-independent so the same data can sound completely different across devices
- **MIDI Polyphonic Expression (MPE)** — enables *per-note* control of synthesis parameters by temporarily assigning each sounding note its own channel, so pitch bend, aftertouch, and CC apply individually; arose with multidimensional controllers (Roli Seaboard Block, Linnstrument, Haken Continuum)
- **MPE tenets** — channels are divided into *zones* (set via RPN 6); when notes outnumber channels they share one (no longer uniquely controllable); each zone has a *Master Channel* conveying common information (program change, pedal, global pitch bend) in a single message

## 6. MIDI 2.0

- **MIDI 2.0 (2020)** — published by AMEI-MMA; backward compatible (MIDI 1.0 remains supported), motivated by greater gestural expressivity. It does not mandate new features — it defines a *way* for manufacturers to add them: bidirectional communication, better timing, and higher resolution for velocity, pressure, pitch bend, and CC
- **Universal MIDI Packet (UMP)** — a transport-agnostic container (32–128 bits) holding both MIDI 1.0 and 2.0 messages; adds 16 groups of 16 channels (up to 256 channels) and a large reserved space for future messages
- **Higher resolution** — note-on velocity expands from 128 (7-bit) to 65,536 (16-bit) values; new *attribute* fields let a note map to any pitch for microtonal scales
- **Single unified messages** — operations that needed several MIDI 1.0 messages (bank + program change, RPN/NRPN edits) collapse into one; RPN/NRPN are replaced by 16,384 *registered* and 16,384 *assignable controllers* with up to 32-bit resolution
- **Per-note controllers** — 256 registered + 256 assignable; registered per-note controller #3 is *Pitch 7.25*, a 7.25 fixed-point value (7 bits = 128 semitones, 25 bits = fractional semitone) anchored to A = 440 Hz, enabling precise non-equal-tempered pitch
- **Jitter Reduction (JR) time stamps** — high-resolution absolute time stamps prepended to packets (as in OSC) so messages, including clock, mark identical playback timing
- **MIDI Capability Inquiry (MIDI-CI)** — connected devices use MIDI 1.0 to query, negotiate, and test shared expanded features, falling back to 1.0 if a test fails; covers three areas: *protocol negotiation* (1.0 vs. 2.0), *profile configuration* (auto-config rule sets, e.g. a piano or organ profile), and *property exchange* (discover/get/set device properties, automap controllers, supply visual editors to DAWs)
