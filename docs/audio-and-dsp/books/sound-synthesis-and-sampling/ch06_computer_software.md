# Ch 6: Making Sounds with Computer Software

## Table of Contents

- [1. From Mainframes to Personal Computers](#1-from-mainframes-to-personal-computers)
- [2. The PC as Integrator](#2-the-pc-as-integrator)
- [3. Computers and Audio](#3-computers-and-audio)
- [4. The Plug-In](#4-the-plug-in)
- [5. Integrating the Audio Cycle](#5-integrating-the-audio-cycle)
- [6. The Integrated Sequencer and the DAW](#6-the-integrated-sequencer-and-the-daw)
- [7. Abstract Controllers and the Fall of MIDI](#7-abstract-controllers-and-the-fall-of-midi)
- [8. Dance, Clubs, DJs, and Live Performance](#8-dance-clubs-djs-and-live-performance)

## 1. From Mainframes to Personal Computers

- **Music and computing's shared roots** — early work linked music and mathematics, and music has been made on computers from almost the start, often to demonstrate processing power in terms ordinary people could grasp; this forged ties between music and computer science that still exist in top universities.
- **The shift from a few to many** — the world moved from a few tens of mainframes in the 1950s (when a "personal" computer was so alien it was B-movie mad-scientist equipment) to ordinary homes with 10+ microprocessors and more than one personal computer.
- **The first computer sequencers** — Roland's late-1970s computer-based sequencers, with calculator-style numeric keypads and limited numeric displays, were based on (and influenced by) the cash-register application of the Intel 8080 chip; they moved computer-controlled music off shared, hugely expensive mainframe time onto something affordable and personal.
- **"Personal" computer as a marketing landmark** — calling a computer "personal" reversed the 1970s model of a shared resource doled out in time slices to many terminals, letting one person monopolize a whole processor and own the machine. The Web and browser later partly reversed this, turning PCs back into terminals to central servers.
- **MIDI bridges the PC and the synthesizer** — the 1980s MIDI specification standardized communication between computers and instruments; before it, control voltages and gates could link analogue synthesizers (only of matching linear or exponential format), but patch selection was inaccessible or required proprietary cabling. MIDI made program switching over a connection easy and introduced the **stack sound** — one note producing more than one sound simultaneously.
- **Low-cost interfacing** — MIDI interfaces were deliberately designed around low-cost standard computer hardware, so they quickly appeared for the 8-bit, cassette-storage, TV-as-monitor home computers of the day; PCs stayed business-priced until the 1990s.

## 2. The PC as Integrator

- **The Integration hypothesis** — the author's coined idea that "computers are a one-way street to integration": being general-purpose, the computer absorbs more and more functions, and its effect on electronic music has been a steady move toward integrating everything into one machine.
- **Moore's law** — Gordon Moore (Intel co-founder) observed that the number of transistors on a chip doubled roughly every couple of years, a trend also tracking processing power and disk size; it became an industry goal, met or bettered for a quarter century, so computer-based devices keep getting better and cheaper, unlike a toothbrush or a car.
- **How computers ate the studio** — MIDI made instruments easy to connect and store; the on-screen sequencer beat the multi-track recorder (any tempo without pitch change); large screens and a mouse simplified sample editing; plug-in effects and plug-in synthesizers removed outboard gear, MIDI cabling, and Sysex downloads. The result is the **Digital Audio Workstation (DAW)** — sequencer, sampler, synthesizers, effects, mixer, and sample libraries in one cheap software package.

## 3. Computers and Audio

- **From 1-bit beeps to CD quality** — early 1980s 8-bit computers made "beeps" by toggling an output port (effectively 1-bit audio); telephone quality is 8 bits, CDs 16 bits, pro interfaces 20+ bits. Modern 32-/64-bit computers have CD-quality audio I/O and built-in MIDI support, though MIDI ports are not standard.
- **The SID chip** — the Sound Interface Device found in Commodore computers, by Robert Yannes (later founder of Ensoniq), was effectively a small subtractive-synthesis chip with three oscillators, multi-mode filter, ring modulation, and envelopes; its musical capability helped make the C64 a best-seller.
- **16-bit milestones** — 16-bit machines played short samples with limited polyphony, controlled by **MOD files** in players called **Trackers** (widely used for video-game music); the Apple Macintosh's graphical interface made it a popular MIDI computer, with the cheaper Atari ST (uniquely shipping MIDI sockets) also succeeding.
- **Adding audio to the PC** — Roland's widely cloned MPU-401 MIDI breakout box (with DIN Sync 24 and MIDI In/Out/Thru) was notable; PCs lacked audio sockets until CD-ROMs arrived (some makers reportedly resisted audio for fear it would be used to play music), and early sound cards used a Yamaha FM chip.
- **Modern connectivity** — separate breakout interfaces give more bit resolution, line-level inputs, and lower noise floors over USB, FireWire, PCMCIA, or PCI/PCI-X/PCI-Express; digital audio (S/PDIF, TOSLINK, AES/EBU, MADI, ADAT, TDIF) is also supported. **GM**-compatible sound sets ship in Mac OSX and Windows, so a default install has basic music capability.
- **Operating-system audio layers** — the OS provides audio functions: Mac OSX has Core Audio, Core MIDI, and the Audio Units extension format; Windows has its own (confusingly same-named) Core Audio plus DirectX/DirectShow filters (XP) or Media Foundation Transforms (Vista) for extending audio processing.

## 4. The Plug-In

- **Plug-in** — a standardized software add-on that lets a third party supply functionality the original ("host") program's authors overlooked or could never anticipate. The general idea matured in Apple's **HyperCard** (1987, programmable card-index metaphor, where MIDI support was added externally); the word itself came in **SuperPaint** (1988); Adobe Photoshop made plug-ins ubiquitous in graphics.
- **VST (Virtual Studio Technology)** — Steinberg's 1996 audio plug-in format, introduced in their Cubase sequencer and released as an open standard (with the ASIO audio interface) in 1997. **VST 1** added audio processing (reverb, effects) to the mixer; **VST 2** added MIDI processing, enabling **VST Instruments** (plug-in synthesizers and sample players); **VST 3** (2008) was a full rewrite adding dynamic processing, sample-accurate automation, and deeper host integration.
- **Host software** — the umbrella term used here for the audio-and-MIDI sequencing application that hosts plug-ins (also called sequencer, DAW, audio/music workstation); a DAW sometimes specifically implies high-quality audio I/O.
- **Plug-in formats** — usually manufacturer-specific, with wrappers bridging between them:

  | Format | Origin | Host sequencer |
  |---|---|---|
  | VST | Steinberg | Cubase |
  | MAS | Mark of the Unicorn (MOTU) | Digital Performer |
  | Audio Units | Apple | Logic |
  | DirectX | Microsoft (DirectShow filters) | several Windows hosts |
  | RTAS | Digidesign | Pro Tools |

- **Compatibility caveats** — plug-ins are usually OS-specific (a Windows VST won't run on Mac OSX) and tied to CPU, OS, and host; always check all four. The interface itself evolves — programmers push its limits, so successive versions add features, and a successful interface can become a cross-vendor standard.
- **Continuous beta** — modern software is released only partly tested, with users acting as testers, then patched and extended while supported. Partitioning into host and plug-ins means a single feature can be updated quickly; some hardware (e.g., the Ensoniq Mirage) puts only essential OS functions in ROM and the rest on removable media so it can be improved over time.
- **Significance of plug-ins** — before plug-ins, chaining software meant slow manual export/import (analogous to pre-synthesizer or modular-era sound-making, like the labor behind Wendy Carlos's *Switched-On Bach*). Plug-ins made connecting easy, so "in many ways, plug-ins are the synthesizers of the twenty-first century," and the host software is the enabling **environment** — a virtual well-equipped studio whose virtual setups can be saved and recalled, which hardware does poorly.
- **The author's six principles** — for any device or plug-in: understand what it does (a good mental model is ideal); explore its limits beyond the manual; understand it in its environment; use and misuse it; do not just collect — compare, choose, and learn one in depth; do not bloat — remove a plug-in you don't like.

## 5. Integrating the Audio Cycle

- **The audio cycle on computers** — the "Produce, Mix, Record, Reproduce" sound cycle (from Section 1.7) is shown as a progression from least to most computer integration: live performance, then multi-track recording, then MIDI sequencers, then computer sample playback, then multi-track audio plus samples, then automated mixing, and finally plug-ins replacing all external instruments and effects, leaving only the computer (and perhaps an audio interface).
- **The endpoint** — once you move onto a computer, working with analogue hardware becomes difficult and doing everything in software becomes easy; the natural consequence is that effects, synths, and samplers in hardware get replaced by software, collapsing many MIDI and audio cables into a few plug-ins whose whole configuration is stored and recalled instantly.
- **Latency** — the time delay between initiating an action and it happening. In a computer sequencer the main cause is the audio output: the host passes samples to the driver through a memory buffer. A large buffer gives high latency but low CPU load; a small buffer gives low latency but high CPU load — so a compromise value is chosen, monitored via the host's CPU-load indicator "like glancing at the speedometer." MIDI-input and audio-conversion delays of external gear can be compensated by sending messages/audio early in time.
- **CPU load** — the major limitation on a computer sound-making environment, capping how many virtual instruments/effects run at once. Two strategies: **CPU load optimization** (e.g., **track freezing** — recording a demanding modeled track to a sample then replaying it; **disk/sample streaming**; using panned mono instead of stereo samples; reducing accompaniment polyphony) and **distributed processing** (spreading load over more CPUs/cores or networked computers; RAID/fast drives for parallel sample access).
- **The changeover** — the author moved fully to software between the second and third editions and now has "more virtual hardware than ever existed previously in real hardware," all usable, more flexible, faster to set up, and better at recalling setups. The computer moved from minor peripheral to the major hardware component, and the synthesist's role shifted from technician/cable-plugger to conductor, arranger, and aspiring computer expert.

## 6. The Integrated Sequencer and the DAW

- **Computer as complete studio** — being general-purpose makes the computer adaptable and so integrative; in electronic music it has moved from minor peripheral to host of complete studio functionality, joining the workstation keyboard as a main way to produce sound.
- **Context and freedom** — making sounds on a computer lets synthesis and sampling be controlled in detail while seen in context (a plug-in synth can be adjusted live within the mix), and frees you from physical constraints (copies of a monophonic synth plug-in replace tedious multi-tracking; complex effect/instrument chains are named and recalled instantly).
- **Evolution of the software sequencer** — first MIDI-only (1980s, with the Atari ST a cheap success alongside the pro-favored Macintosh); storage and power made audio viable in the early 1990s; by the late 1990s MIDI and audio were handled with near-equal ease, and the brief history runs: MIDI → audio + MIDI → + mixing → + effects → + synthesis. At some point the sequencer becomes a **DAW**.
- **Specialist tools and softsamplers** — feature convergence (differentiated mainly by interface metaphor) spawned simpler dedicated tools: ACID for sample replay, Reason as a whole-rack replacement. Once audio is integrated, the sequencer doubles as a virtual sampler, reducing dependence on hardware samplers (though computers suit the road poorly; laptops help with size and battery).
- **Interface metaphors** — most DAWs base their look on the multi-track recorder (time horizontal, mixer as vertical channels), but Propellerhead's **Reason** (2001) presents a realistic "virtual studio rack" with a rear view of patch cables, while Ableton's **Live** is abstract and minimal yet hides deep power, letting per-channel chains of effects and instrument/sample plug-ins build complex virtual instruments.
- **Example software** — *The Music System* (1984, BBC Micro step sequencer/oscillator) and *Ample* (BBC Micro music language driving a 16-channel wavetable synth) proved 8-bit micros could make music; **Max** (IRCAM, Miller Puckette) connected functional blocks with the mouse and changed how programming is presented; *Studio Vision* (Opcode) was the first commercial sequencer for a PC (the Mac) to integrate MIDI and digital audio; *ACID* (1998) signaled the hardware sampler's days were numbered; **Reaktor** (Native Instruments) is a deep audio synthesis/processing toolkit, often compared to a modular synthesizer.

## 7. Abstract Controllers and the Fall of MIDI

- **Abstract controller** — a controller whose physical controls have no fixed mapping (a rotary might set detune, a slider a filter cut-off, a cross-fader a mix between arrangements). Especially useful for plug-ins inside a computer, since the plug-in arrangement can change quickly and the external controls must follow.
- **MIDI hidden inside USB** — most abstract controllers work through MIDI, increasingly tunneled inside a USB connection; a DJ controller with knobs, sliders, cross-faders, and gestural inputs can send MIDI over USB with no MIDI sockets exposed at all — possibly the first examples of a more generic synthesizer/sampler/sequencer controller of the future.
- **MIDI accepted as invisible abstraction** — a Windows Media Player or Mac QuickTime Player replays a MIDI file through a built-in GM soft synthesizer, so to many users a MIDI file behaves like an audio file and its abstraction is no longer apparent; the broader abstraction — that a computer DAW can produce a complete musical performance — has likewise been accepted without question.

## 8. Dance, Clubs, DJs, and Live Performance

- **Dance music as live performance** — dance music has a clear purpose (music to dance to) and must react to its audience; an effective set has dynamics and contrast and follows the crowd's mood, which needs the right controllers so it becomes live performance rather than playlist sequencing. Abstract controllers can hide the computer behind CD/LP decks and mixers, and the DJ is increasingly seen as performer/conductor — blurring where the DJ stops and the musician begins.
- **Rise and fall of the keyboard stack** — when synthesizers were room-sized the synthesist went to the synthesizer (like a conductor to an orchestra); portable instruments such as the Minimoog and EMS VCS-3 (both 1969) brought live use to ordinary musicians. The 1970s saw keyboards literally **stacked** (driving the development of keyboard stands), e.g. a Minimoog atop a Fender Rhodes, growing to a string machine, organ, electric piano, and monosynth.
- **The DX7's impact** — the Yamaha DX7 (the first instrument most people met with MIDI as standard) changed the stack: its "E. Piano 1" preset replaced heavy electric pianos, its vibes/glockenspiel/bell sounds were hard to get on analogue gear, and its affordable 16-note polyphony made it a runaway best-seller — turning the synthesizer from a specialist rarity into a mass-market workhorse and building a solid MIDI user base.
- **Stacks to racks to laptops** — as MIDI spread, string machines and organs gave way to polysynths, and keyboards themselves shrank into MIDI-driven sound modules in 19-inch racks driven by master keyboards (the "one keyboard : one sound" era ended, though the word **stack** survives for several sounds triggered from one keyboard). In the 1990s keyboards moved out of the stage limelight; by the mid-2000s the laptop with a MIDI-over-USB controller keyboard became dominant — "a disk drive full of modeling software instead" of a room of hardware.
- **The remaining role of hardware** — computers carry a relatively high initial cost, OS-stability issues, and frequent update costs, so true cost of ownership exceeds the purchase price and there is still a role for hardware in some circumstances; hardware companies buying software firms (Apple/Emagic, Yamaha/Steinberg) hints at the likely outcome.
- **Reuse and convergence in live rigs** — where in the 1980s an electro-acoustic band, a touring pop band, and a club DJ shared almost no equipment beyond amps and speakers, the early twenty-first century sees much more reuse: experimenter, turntablist, and band might all use a groove box, two turntables, and a laptop running a sequencer.
