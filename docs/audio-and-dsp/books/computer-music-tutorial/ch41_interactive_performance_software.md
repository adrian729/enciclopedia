# Ch 41: Interactive Performance Software

## Table of Contents

- [1. Foundations of Real-Time Computer Performance](#1-foundations-of-real-time-computer-performance)
- [2. Sequencers and Their History](#2-sequencers-and-their-history)
- [3. How a Digital Sequencer Works](#3-how-a-digital-sequencer-works)
- [4. Extended Possibilities of Interactive Software](#4-extended-possibilities-of-interactive-software)
- [5. Networks, Live Coding, and Improvisation Systems](#5-networks-live-coding-and-improvisation-systems)

## 1. Foundations of Real-Time Computer Performance

- **Interactive performance software** — programs that capture human gestures and transmit them to sound generators in real time, for studio, concert hall, gallery, and interactive media; the four main categories are sequencers, interactive performance systems, improvisation systems, and networked bands / live coding
- **Early offline era** — early computer musicians used *offline* punch-card machines and submitted card decks; producing a minute of sound could take days. *Online* timesharing terminals in the late 1970s let musicians edit data and launch immediate calculations
- **Hybrid systems** — 1970s systems pairing a digital computer with an analog synthesizer enabled the first real-time digital gestural input; the *GROOVE* synthesizer at Bell Labs (operational 1970) let a musician play keyboard, joysticks, and knobs and draw envelopes onscreen, with the *CONDUCT* program giving conductor-like control of amplitude, tempo, and balance
- **Prophet-5** — the Sequential Circuits Prophet-5 (1978) was the first mass-produced hybrid polyphonic synthesizer (over 6,000 sold), bringing interactive computer technology to the musical arena

## 2. Sequencers and Their History

- **Sequencer** — a recording/playback system with programmable memory that stores not the waveform but the *control* or *performance data* (e.g. key-up/key-down times) needed to regenerate musical events; can be a software app (in a DAW), a hardware box, a synth subsystem, or a robot
- **Mechanical ancestors** — sequencing predates industry: programmable carillons (1200s Dutch bell mechanisms with peg-and-hole *step mode* recording), Vaucanson's musical *androides*, the *melograph* (paper roll inscribed by J. Charpentier's 1880 *melography*), and early 1900s pneumatic paper-punching machines that drove player pianos
- **Paper-tape and analog** — Givelet and Coupleux's 1929 vacuum-tube synth, and the room-sized RCA *Mark I* (1955) and *Mark II* (1957) by Olsen and Belar, used by Milton Babbitt at Columbia-Princeton. Conlon Nancarrow hand-punched player-piano rolls for mathematically precise counterpoint
- **Analog voltage-controlled sequencers** — optional modules from Moog, Arp, Buchla, EMS; a row of knobs sets voltages the sequencer steps through at a clock rate, looping for repeating melodies. Limited by step count (Moog 960 = 24 steps, Arp 1027 = 30, Buchla 246 = 48), divided by the number of parameters controlled; Steve Reich credited looping sequencers as inspiration for minimalism
- **Digital sequencers** — the EMS *Synthi AKS* (1972) recorded up to 256 events of six parameters (1,536 values); MIDI (1983) made digital sequencing widespread. Today sequencers in DAWs such as Pro Tools, Ableton Live, Logic, Cubase, BitWig, and Performer drive plug-in synths
- **Musical robots** — motorized androids; modern research yields *mechatronic* (electronics + mechanics + acoustics) non-keyboard instruments — flute, sax, drums, guitar, even Theremin (e.g. the Z-Machines robot guitarist)
- **MIDI performance data** — four types: discrete *note data* (start/stop, pitch, velocity, channel), discrete *program change* (selects patches), discrete *system exclusive* (supplies patch parameters), and *continuous controller* data (pitch bend, vibrato, pedals). A note is two messages — note-on and note-off — with pitch 0 (C0) to 127 (G10), velocity 0–127, and channel 1–16
- **Performance practice** — *quantizing* rounds event timing to a grid (correcting errors, aiding notation) while *humanize* / *groove quantization* re-adds variation; *performance setup* maps tracks to MIDI channels, devices, and patches (with *multiport interfaces* extending MIDI 1.0's 16 channels). Subsequences can be assigned as *macros* and chained by conditional logic; full programmability needs toolkits like Max, PureData, SuperCollider, or ChucK

## 3. How a Digital Sequencer Works

- **Core task** — record a performance while simultaneously playing back previously recorded tracks, detecting new note starts/stops, finding upcoming notes in stored tracks, and monitoring controls
- **Event packet** — preprocessed note info: key number, key status (pressed/released), velocity, and the time (in *MIDI clock ticks*) the status changed; packets are assembled into a *track event array*
- **Array vs. linked list** — a sequential array is compact but bad for editing (inserting a note forces shifting every later event); editors use a *linked-list* of *links* (pointer to a track array plus pointer to the next link). Practical sequencers combine both — arrays for unedited runs, links where edits occur
- **Playback** — merges events from several tracks into one time-sorted stream, packages them as MIDI messages, and sends them to one or more synths
- **Machine music** — *trans-human* playback with superhuman speed and precision, foreshadowed by Nancarrow's *Studies for Player Piano* and Arthur Roberts's *Sonatina for CDC 3600*, and heard in *tracker music* and Squarepusher's sequenced electronica
- **Expressive performance software** — a separate category reads a score and renders it expressively using "pronunciation rules" derived from analyzing human performances

## 4. Extended Possibilities of Interactive Software

- **Transmitting cues** — the computer tells performers what or when to play, via headphone cues or projected visual cues (signal-and-response page turns, algorithmically notated scores, sound-structure visualizations driven by machine listening in SuperCollider sent over OSC to the Unity engine)
- **Conducting an ensemble** — software interprets gestures to control *ensemble parameters* (tempo, articulation, stress, balance of voices, spatial projection), beyond a single instrumentalist's voice
- **Accompaniment systems** — play along with a human, following their score in real time (uses include teaching, e.g. MakeMusic SmartMusic, and time-flexible rendition replacing fixed "tape recorder mode"). The central problem is *score following* — tracking pitch and/or tempo, ignoring anomalies, and maintaining multiple location hypotheses for polyphony. Subotnick and Coniglio's *Interactor* tracked landmark pitch/rhythm configurations; Pachet's Markov-based *Continuator* learned and generated styles; recent systems use dynamic time-warping or hidden Markov models
- **Control by gestures** — a performer's or dancer's gestures (often via a custom controller and neural-network recognition) trigger sound responses
- **Shared control** — several musicians drive one multivoice synth; a spectacular example was Sensorband's *Soundnet*, a tension-sensor cable structure played by climbing performers
- **Virtual worlds** — sonic ecosystems of feedback among performer, electronics, and room (Di Scipio), and VR systems that act as interactive visual/sonic/haptic instruments

## 5. Networks, Live Coding, and Improvisation Systems

- **Networked computer bands** — networked computers run autonomously or interactively, from free improvisation to synchronized ensembles; pioneered by the League of Automatic Music Composers and *The Hub* (Mills College), now extended to laptop/tablet/phone ensembles over Ethernet and WiFi
- **Telematic music** — networked performance over the internet; the chief obstacle is *latency* (even at light speed, Santiago–Moscow is 93 ms), which forces free improvisation, drones, or asynchronous layering. Tools include the open-source low-latency router *JackTrip*, plus JamKazam, Soundjack, and Jamulus; *audio dropouts* (packet loss) are another problem
- **Live coding** — fuses improviser and programmer, the music written live onstage (often with the screen projected); rooted in Ron Kuivila's onstage Forth programming. *Algoraves* combine it with a dance-club scene; www\.toplap\.org is the community hub. Trends include pairing live coding with MIDI controllers or EuroRack systems, and *network data sharing* (multiple players live-coding one shared program via JackTrip + ShareDB)
- **Improvisation systems** — the system's response is algorithmically improvised on the spot, not predetermined; one of the first was EMS's 1968 system (whistle a melody into a PDP-8/s, which generated variations). Pioneers include Martirano, Spiegel, Chadabe, Lewis, and Behrman
- **Autonomous performance and installations** — standalone systems recognize patterns and respond by rule, onstage or in interactive sound-art installations responding to light, temperature, sound, and proximity (Liz Phillips). Named systems: *Neurswing* (trained neural net controlled by *hot/cool*, *dissonance/consonance*, *as-is-ness/free* knobs); George Lewis's *Voyager* (64 asynchronous single-voice MIDI "players" improvising with his trombone via pitch followers); and Henning Berg's *Tango* (modular Player, Listener, Modifier, Harmony modules)
