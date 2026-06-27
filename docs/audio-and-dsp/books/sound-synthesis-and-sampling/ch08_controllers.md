# Ch 8: Controllers

## Table of Contents

- [1. Controller and Expander](#1-controller-and-expander)
- [2. MIDI Control and MIDI "Learn"](#2-midi-control-and-midi-learn)
- [3. Keyboards](#3-keyboards)
- [4. Keyboard Control](#4-keyboard-control)
- [5. Wheels and Hand-Operated Controls](#5-wheels-and-hand-operated-controls)
- [6. Foot Controls](#6-foot-controls)
- [7. Ribbon Controllers](#7-ribbon-controllers)
- [8. Wind Controllers](#8-wind-controllers)
- [9. Guitar Controllers](#9-guitar-controllers)
- [10. Mixer, DJ, and 3D Controllers](#10-mixer-dj-and-3d-controllers)
- [11. Front Panel Controls](#11-front-panel-controls)
- [12. Advantages and Disadvantages](#12-advantages-and-disadvantages)

## 1. Controller and Expander

- **Controller vs. expander** — separating the control interface from the sound-generating circuitry yields two devices: the **expander module** is a "keyboard-less" synthesizer (the bare sound producer), since the term "synthesizer" almost always implies an included keyboard. Any non-keyboard interface is called an **alternative controller** (wind instruments, guitars, drums are the commonest).
- **Why a controller exists** — a conventional instrument's control is fixed by its physics (a guitar has six strings, a fretboard, a bridge), but a synthesizer has no physical limits, so its controls are chosen freely; the control determines how the player's expression reaches the listener.
- **Information a controller must supply** — pitch of a note, start/end of a note event, dynamics (volume), changes in pitch, modulation changes, sustain, and additional expression controls; a master keyboard may send only pitch and dynamics, while richer ones add pitch bend, modulation, and sustain.
- **No controller does everything** — each has specific strengths and weaknesses, so controllers can be combined: the **SynthAxe** used guitar strings for pitch but separate keys to trigger sounds, and small six-string "string" controllers can add strumming/plucking on top of a keyboard supplying pitch.
- **The keyboard's accidental dominance** — the organ-type keyboard became the main controller "for all the wrong reasons": it was easy to wire up as control voltages and triggers for the first synthesizers, yet it is naturally polyphonic (bad for early monophonic synths) and offers expression only via attack velocity and after-touch.

## 2. MIDI Control and MIDI "Learn"

- **MIDI as the dominant digital control** — the Musical Instrument Digital Interface is the standard way to control hardware (and even VST software plug-ins assume MIDI-style controllers), but it carries keyboard-based assumptions: pitch and velocity are tied together in note on/off messages, while volume, pitch bend, and modulation each need separate continuous controllers.
- **MIDI's keyboard-origin limits** — it is poor at specifying transitions between notes (so reusing a guitar string is hard), polyphonic vibrato needs mono mode (rarely supported), glissando/portamento are controllable only as parameters like time, and every pitch change is expected to start a new envelope.
- **Two control routes** — MIDI controls parameters either through **controller messages** (a general case of pitch-bend/pressure messages: modulation, expression, vibrato) or through **system exclusive (sysex)** messages.
- **Controller message structure** — 3 bytes: the first identifies it as a controller message and gives the MIDI channel, the second is the controller number (128 possible), the third the value; the most common is the **modulation wheel** (controller 1), usually beside the pitch-bend wheel on the keyboard's left.
- **7-bit vs. 14-bit controllers** — 7-bit controllers give 128 coarse values; 14-bit controllers pair a most-significant-byte (MSByte) controller with a least-significant-byte (LSByte) controller 32 numbers higher (e.g., volume = 7, fine volume = 39) to "fill in" the gaps, giving up to 16,384 values. Few manufacturers exploit 14-bit precision; switches are the extreme limit at just two values.

| Controller numbers | Role |
| --- | --- |
| 0–31 | 14-bit controllers (MSByte) |
| 32–63 | 14-bit controllers (LSByte) |
| 64–69 | Switches (pedals/foot switches: damper/sustain, portamento, sostenuto, soft pedal, legato, hold 2) |
| 70–95 | 7-bit controllers (incl. sound controllers: brightness, attack/release time) |
| 96–101 | Registered and non-registered parameters |
| 102–119 | Undefined (usable for any purpose) |
| 120–127 | Mode messages (all sounds off, reset all controllers, all notes off) |

- **System exclusive (sysex)** — the only MIDI message with explicit start and stop bytes (so it can be any length); a manufacturer's ID byte addresses the message like an envelope, and the contents (sound data, edit/control functions, often a checksum) are entirely manufacturer-defined, giving a compatible "loophole" for proprietary data.
- **MIDI Learn** — a software aid that maps a physical controller to an on-screen parameter: the user puts a parameter into "Learn" mode and the next received controller becomes mapped to it, avoiding the slow, error-prone task of looking up controller numbers and entering them in a mapping table.
- **After MIDI** — proposed successors include **ZIPI** (1996, controller-agnostic transport of performance data, never widely adopted), **OSC** (Open Sound Control), **mLAN** (Yamaha, FireWire/IEEE-1394 carrying audio, MIDI, and sync), Gibson's **MaGIC** (audio-over-IP, used in the HD.6X-Pro guitar), and **RTP-MIDI** (an IETF standard for carrying MIDI over IP networks); meanwhile MIDI itself increasingly travels invisibly inside USB cables.

## 3. Keyboards

- **What a keyboard outputs** — discrete pitch information (which notes) and event information (note start on key-down, note end on key-up); some also report **attack velocity** and **release velocity** (the rate of key movement, sometimes called dynamics) and **after-touch**.
- **Monophonic to polyphonic** — early analogue keyboards used a chain of equal-value resistors so the key position sets an output voltage, with **top-note priority** (highest pressed note wins); **duophonic** keyboards store two voltages; full **polyphonic** keyboards use digital time-division scanning of a key matrix, with polyphony and note priority handled in software.
- **Organ-type vs. piano-type** — organ-type keys are light, hollow plastic with a fast spring-return action (used in low-/mid-range products, 61 or 76 keys); piano-type keys are heavier, wood-cored, "weighted" with a piano-style action that mimics a real piano's feel (used in master controllers and flagship products, usually 76+ keys).

## 4. Keyboard Control

- **Velocity** — measures key speed between two contacts and is polyphonic (measured per key-press); **attack velocity** controls dynamics (level and/or timbre) on key-down, while **release velocity** controls release-segment length on key-up (rarely implemented in keyboards, though many sound generators respond to it).
- **After-touch / key pressure** — the extra pressure applied once a key is fully down; **monophonic** after-touch uses the single highest pressure across the whole keyboard, while **polyphonic** after-touch measures each key separately.
- **Qwerty and controller keyboards** — sequencer software lets the computer's qwerty keyboard enter notes (middle row = white notes, row above = black notes, with octave/velocity keys), and compact **controller keyboards** of a couple of octaves with octave switching serve as space-saving alternatives; keyboard-less versions become DJ, mixer, or performance controllers.
- **Virtual keyboards and piano rolls** — the **piano roll** metaphor maps pitch vertically and time horizontally, with the mouse clicking and dragging notes onto a pitch/time grid and velocity set by bar heights; a **notation display** variant enters notes as music notation from a symbol palette.
- **Drum pad controllers** — velocity-sensitive rubber pads assigned to drum sounds that can also send pitched MIDI notes (a "struck keyboard"); their tactile interface lets drummers capture performances, suits **hocketing** (dynamically switching the sound a pad produces), and can trigger samples, phrases, or whole compositions in stage/theater use.

## 5. Wheels and Hand-Operated Controls

- **Why wheels replaced knobs** — early modular synths used rotary knobs for pitch bend and modulation, but knobs were poor for live use; the four main alternatives are **wheels, levers, joysticks, and pressure pads**.
- **Wheels** — a rotary control turned on its side as a disk (40–80 mm), moving over about 90° with a detent reference point; a pitch-bend wheel is spring-loaded and detented to return to center, while a modulation wheel typically has no spring return so it can be set and left.
- **Pitch bend** — continuous control over pitch (often a semitone or a fifth across the range), produced as a voltage proportional to the control's angle, always sprung and usually detented back to a "zero" center position.
- **Modulation** — controlled by rotary wheels or levers (voltage proportional to angle), not normally sprung to return; on some instruments keyboard pressure can act as the modulation controller.
- **Levers, joysticks, pressure pads** — a **lever** is a short stick with less rotation than a wheel; a **joystick** combines pitch bend and modulation on perpendicular axes (sometimes with rotation or up/down for extra control); **pressure pads** need separate pads to bend pitch up and down and can only add modulation interactively (cannot be set and left).
- **2D controllers** — pads (rather than joysticks) controlling two parameters at once, e.g., the **Korg Kaoss Pad**, which began as an audio effects unit and was extended to DJ twin-deck and even video-synthesis use.

## 6. Foot Controls

- **Foot pedals** — rotary controls operated by the foot, hinged about a third along the plate, giving a voltage proportional to angle; usually used for volume (with a sprung "soft" end stop allowing extra volume for expression), but also usable for modulation or pitch bend, and sensed by potentiometer, optical, or magnetic rotation sensors.
- **Foot switches** — two-value foot-operated switches (piano-style sustain levers, mini-pedals, or push buttons) controlling sustain and portamento, or selecting sounds and starting/stopping drum machines.
- **Foot-operated keyboards** — bass pedalboards adapted from organs; the **Moog Taurus** bass pedal (1970s) was a notable single-octave example, though foot keyboards have generally been less successful on synthesizers.

## 7. Ribbon Controllers

- **Ribbon controller** — a variation on the pitch-bend wheel: a flexible conductive material held above a metal plate produces a voltage where a finger presses it down (like holding a guitar string down), with finger movement changing the voltage; it is mechanically simple and small but the material wears out, and unlike a wheel it can jump in pitch and snap back to the default.
- **Short vs. long ribbons** — **short ribbons** (\~100 mm, silver cloth-like, with a central raised indicator) suit pitch bend and have appeared in Moog, Yamaha, and Korg synths; **long ribbons** (\~300 mm, black flocked plastic) change pitch relative to the finger's start point and movement, suiting portamento and glide (as on the Yamaha CS-50/60/80 series).

## 8. Wind Controllers

- **Breath controller** — a simple pressure-measuring device blown into by the player, its output controlling modulation or replacing the volume control to shape the envelope; especially useful for monophonic melody synthesizers, and able to change volume continuously through a note (hard to do from a keyboard). The Yamaha **BC1** (1983) was an early example grasped in the teeth.
- **Wind instrument controller** — based on a flute, clarinet, or saxophone, converting key fingerings (one or more Boehm-style fingerings) into pitch and breath into modulation/volume, with extra keys for octave switching, portamento, and sustain; normally monophonic but some can hold notes to build sustained chords, and they excel at lead and solo melody lines. The **Lyricon** (1974) was the first commercially available wind-controlled electronic instrument.

## 9. Guitar Controllers

- **Why a guitar controller is hard** — a normal electric guitar's sound comes from steel strings vibrating over magnetic pickups, but extracting each string's pitch is difficult because pitch depends on fret position, string bending, tremolo-arm use, and even whether a harmonic was deliberately played.
- **Per-string sensing** — separating strings requires a **hexaphonic (hex) pickup** with a separate coil per string; even then the controller must also capture per-string dynamics (pluck/strum strength), hand damping, and pluck position (closer to the bridge = brighter), plus global controls like the tremolo arm and pickup mix.
- **Approaches tried** — hex pickups with pitch-extraction signal processing, wiring the frets as electronic switches, and even acoustic radar along the strings to locate plucking/fretting; none is a complete solution, and modified guitar-like controllers (separating fretted from plucked strings, or adding trigger keys) have not been commercially successful.
- **Pitch-to-MIDI** — converting a guitar's playing into MIDI note numbers, e.g., Roland's **GI-10** (1995) hex-pickup pitch-to-MIDI converter.
- **The hex pickup's payoff** — arguably the most useful result of guitar-synth research: distorting the six string signals individually avoids the inter-modulation distortion of a normal combined pickup, giving a bright synthetic sound with the guitar's expressiveness; the guitar thus becomes a **composite instrument** mixing acoustic, processed, hex, and synthesized sound.

## 10. Mixer, DJ, and 3D Controllers

- **Mixer controllers** — compact banks of rotary or linear sliders that control the volume or pan of many channels at once, mainly for digital audio workstation software where simultaneous real-time control of several parameters is needed (on-screen one-at-a-time editing is too slow for live use).
- **DJ controllers** — a specialized mixer controller: twin decks plus the rugged, all-important **cross-fader**, whose "one deck playing while the other is prepared" metaphor adapts to switching between two tracks or variants in time with the beat; their ruggedness suits any live electronic music-making.
- **3D controllers** — control by moving the hands in space (tiring without support): **capacitive** (the Theremin, where hands alter the field around two pitch/volume aerials), **infrared** (the Alesis airFX reflecting IR off the hands; Roland's D-Beam gives simpler 2D control), and **ultrasonic Doppler-shift** "radar" sensing movement via high-frequency sound.

## 11. Front Panel Controls

- **Front panel evolution** — the non-realtime knobs, switches, and sliders that program the synthesizer have changed markedly over its life, mirroring developments in synthesis itself.
- **1970s "form = function"** — modular synths used knobs, switches, and patch-cords plugged into front-panel sockets; cords obscured the panel and made rapid re-patching awkward. Streamlining to a VCO/VCF/VCA signal path let the panel be laid out to mirror signal flow, with usually one knob per parameter, so the layout itself taught how sounds were made.
- **1980s minimalism** — the Yamaha **DX7** introduced one knob and many buttons (roughly one button per parameter across several modes): a fast two-handed edit (select with one hand, adjust with the other) that scaled well to rack expanders.
- **1990s displays and softkeys** — as LCDs grew, a row of assignable **softkeys** under the display took over parameter selection; displays became graphical and dominant, freeing panel space for real-time performance controls like track-balls and joysticks.
- **Touch screens and multi-touch** — touch screens arrived mid-1990s (early ones slow); the late-1990s/2000s split into a return to 1980s minimalism (low-cost), softkeys-plus-softknobs (mid-range), and touch screens (high-end). **Multi-touch** (Apple's iPhone and iTouch MP3 player, 2007; also academic projects and Microsoft Surface) tracks several fingers separately, enabling gestural, multi-channel interaction. Front panels have moved increasingly toward software, again mirroring synthesis trends.

## 12. Advantages and Disadvantages

| Controller | Strengths | Weaknesses |
| --- | --- | --- |
| Keyboard | Complex polyphonic performances based on notes and dynamics | Weak when expression is required |
| Wind controller | Excellent detailed monophonic melodies | Unsuitable for polyphony beyond simple sustained chords |
| Guitar controller | Simple polyphony with notes, dynamics, and expression | Limited to 6-note polyphony; note complexity limited by one fretting hand |
| Drum controller | Good for percussion (dynamics, triggering, pitch) | Two hands limit polyphony to \~2–4 notes |

- **Small-scale controllers compared** — **wheels** and **levers** are similar (wheels far more common); **joysticks** are less popular and tend to be used for vector-style mixing between sounds; **pressure pads** are rare and need pitch bend artificially split into two pads; **pedals** are heavier than wheels/levers, limiting speed and precision.
- **After-touch's limitation** — usable only while a key is held down, which restricts it and slows playing; one workaround with monophonic after-touch is to hold a bass/pedal note with a left-hand finger that also applies the (keyboard-wide) after-touch while the right hand plays melody.
- **Recording with controllers** — over-dubbing performance data in separate takes lets a sequencer act as a filter that replaces imperfect playing with perfect playing, and recording at one tempo to replay at another allows superhuman precision; this trades away some of the "liveness" of a tape recorder, where mistakes must be re-recorded or lived with.
- **Few controllers become instruments** — most alternative controllers serve to perform pre-recorded music (a DJ, or a player driving a **groove box** / phrase remixer as a "conductor") rather than becoming new instruments; the Theremin is a rare exception. Stephen Kay's **KARMA** (Kay Algorithmic Real-time Music Architecture) gives comprehensive real-time control over arpeggiation, stackings, chordings, hocketing, and controller mappings, built into Korg instruments such as the OASYS, Triton, and M3.
