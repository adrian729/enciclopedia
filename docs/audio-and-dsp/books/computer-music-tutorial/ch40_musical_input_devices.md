# Ch 40: Musical Input Devices

## Table of Contents

- [1. What Input Devices Are and Why They Matter](#1-what-input-devices-are-and-why-they-matter)
- [2. Taxonomy of Controllers](#2-taxonomy-of-controllers)
- [3. Mapping, Ergonomics, and Design Choices](#3-mapping-ergonomics-and-design-choices)
- [4. Musical Keyboards](#4-musical-keyboards)
- [5. Remote Sensing, Conducting, and Haptic Response](#5-remote-sensing-conducting-and-haptic-response)

## 1. What Input Devices Are and Why They Matter

- **Musical input device (controller)** — the instrument of real-time performance; the device a musician plays to mediate gesture and sound, as distinct from the sound generator it drives
- **Model of a device** — a *sensor* (responding to a physical stimulus: light, sound, temperature, pressure, magnetism, biometrics, etc.) connected to an *electronic interface circuit* that translates the response into a *discrete* (on-off) or *continuous* control signal, typically a MIDI or OSC message
- **Two advantages of going electronic** — (1) control is *detached* from sound production, so any device can drive the same synth and soft/loud sounds cost minimal effort; (2) tuning and timbral flexibility — scales and timbres change at the press of a button. The cost is reduced *feel*
- **Voltage control vs. digital control** — 1970s modular analog synths used *voltage control* (pitch, amplitude, filter frequency varied by a changing voltage on a *control input* jack), responding to *triggers*, *gates*, faders, and an *envelope follower*; digital control began with Mathews and Rosler's light-pen envelope drawing at Bell Labs and the Dartmouth digital synthesizer (first with real-time keyboard, knob, and buttons)
- **Historical instruments** — expressive electronic instruments predated MIDI by decades: Theremin (1928), Ondes Martenot (1928), Croix Sonore (1934), Ondioline (1941), Electronic Sackbut (1948), Mixtur-Trautonium (1949)
- **Maker era** — low-cost microcontroller boards (Arduino, Raspberry Pi, Bela) plus cheap sensors and the NIME conference community make custom controllers easy to build; game controllers, phones, tablets, and DJ apps (Serato) add more options

## 2. Taxonomy of Controllers

- **Switches and continuous controls** — switches, pushbuttons, *linear potentiometers/faders*, rotary knobs, motorized faders (recall positions in a DAW), trackballs, joysticks, thumbwheels (pitchbend/vibrato), footpedals/switches, organ bass pedals
- **Computer pointing devices** — alphanumeric keyboard, mouse, graphics tablet and stylus (Wacom), multitouch screens and trackpads — favored in the studio for programming and fine DAW control
- **Keyboard family** — musical keyboard, *three-dimensional keyboard* (Notebender; Moog's finger-position sensing)
- **Augmented/emulated acoustic instruments** — drum pads and percussion controllers (Mathews Sequential Drum, Daton, Radio Drum), *ribbon controller* (Moog, Buchla, Kurzweil 2600), breath controller (Yamaha), wind controllers (Yamaha WX5, AKAI EWI 5000, Roland Aerophone), flute controllers (IRCAM 4X), guitar controllers (Fender Stratocaster GC-1, Roland GR-55), violin/cello controllers (Zeta, Yamaha, NS Design; Overtone violin)
- **Sensing and exotic controllers** — microphone (sound source or voice recognition), phone/tablet sensors, *Theremin* and capacitance fields, ultrasonic detector (sonar ranger), video camera (machine vision, WABOT-2 robot), glove interfaces (Waisvisz's The Hands, Sonami's *Lady's Glove*), Airdrums (accelerometer drumsticks). Other named devices: Haken Continuum, Reactable, VideoHarp, Buchla Lightning, EigenHarp, Biomuse brainwave controller

## 3. Mapping, Ergonomics, and Design Choices

- **Mapping** — linking a parameter from the input device to a parameter on the synth, the job MIDI and OSC were built for; software like SuperCollider, Max, or Pure Data processes the raw data (inversion, compression/expansion, limiting, smoothing, quantizing) before it reaches the synth
- **Sources of mapping complexity** — (1) programmable input devices, (2) remapping software, (3) programmable synthesizers; a common setup tool is *MIDI Learn*
- **Ergonomics** — design fitted to human proportion; if a device is easy to manipulate its built-in precision is usable, otherwise it is squandered. *Long-throw linear faders* (100–120 mm) give studio pros finer control than short faders, because a small nudge yields a small change
- **Traditional vs. novel** — modeling a controller on a familiar instrument lets virtuosos transfer skill and sells better commercially (*augmented instruments*), but a traditional interface can cap a synth's full power, motivating custom devices and the creation of OSC

## 4. Musical Keyboards

- **Dominant controller** — twelve-note equal-tempered keyboards outnumber every other type; MIDI was designed with keyboard performance in mind. Early analog keyboards were *monophonic*; modern digital ones are *polyphonic* (though often fewer than 88 simultaneous notes)
- **State sensing** — a microprocessor scans the key switches many times per second; an *exclusive-or* against the previous state cheaply isolates only the keys that changed, reducing the data to a handful of bits
- **Velocity sensing** — measures how fast a key travels (e.g. 5 ms = hard, 35 ms = soft) to infer initial amplitude and brightness; the standard two-bus-bar switch measures the *transition time* between an *up bus bar* and *down bus bar*. Capturing velocity needs high scan rates (the Digital Keyboards Synergy sampled at 40 kHz; transition timing accurate to \~0.5 ms)
- **Aftertouch and pressure** — *aftertouch* is data sent while a struck key is held (often controlling vibrato); *monophonic aftertouch* applies one global effect, *polyphonic aftertouch* applies it per held key. True *pressure-sensitive* keyboards gauge how hard the key is held (often via conductive rubber)
- **Action and computer-controlled pianos** — *haptic feel/action* ranges from unweighted organ keys to a full *double escapement* grand-piano action; Yamaha's *Disklavier* (1987, PRO models record key-down/key-up velocity, extending values past MIDI 1.0's 0–127 range) and Steinway's *Spirio* reproduce performances, sharing patented technology
- **Layout, splitting, and expressive MIDI** — a normal piano key is \~2 cm \× 14 cm; *keyboard splitting* divides the span into *zones* at *split points*, each on its own MIDI channel/voice. *MIDI Polyphonic Expression (MPE)*, ratified 2018, lets each note bend and vibrato individually — the *ROLI Seaboard* senses five dimensions of touch (strike, glide sideways, slide up/down, press, lift); LinnStrument, Haken Continuum, and Osmose are similar

## 5. Remote Sensing, Conducting, and Haptic Response

- **Remote control vs. remote sensing** — *remote control* keeps a tactile device within reach (via cable, fiber, infrared, or WiFi/Bluetooth); *remote sensing* places the performer at a distance from the sensor, the realm of *motion tracking*
- **Conducting as the test case** — the conductor's baton is the original remote controller (Berlioz's 1843 electrified key signaled tempo to an offstage chorus). Sensing means include magnetic trackers, ultrasound, video cameras, infrared LEDs/cameras, accelerometers, and conducting gloves; examples are the MIT ultrasonic-wand system, Buchla's Lightning II (two IR wands), and the Leap Motion Controller
- **Gesture recognition** — the deep problem, comparable to understanding spoken language; *machine learning* / neural nets can be trained by demonstration to map gestures to synthesis parameters. Joel Chadabe used theremin antennae for conductor-like control before MIDI existed
- **Responsive input devices and haptic feedback** — devices with a *programmable response* to touch, applying forces, vibrations, and motion via *haptic feedback* technology to restore the *feel* electronic instruments lack. Using digitally controlled motors, a key can be given *force-feedback* (stiff, loose, or stepped action); named examples include the ACROE keyboard (one motor per key), Touchback keyboard, vBow violin-bow controller, and MIKEY keyboard (emulates grand piano, harpsichord, Hammond organ)
