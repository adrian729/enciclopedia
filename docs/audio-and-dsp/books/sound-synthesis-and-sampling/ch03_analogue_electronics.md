# Ch 3: Making Sounds with Analogue Electronics

## Table of Contents

- [1. Analogue, Digital, and Voltage Control](#1-analogue-digital-and-voltage-control)
- [2. Pre-Synthesizer Audio Electronics](#2-pre-synthesizer-audio-electronics)
- [3. Subtractive Synthesis: Source and Modifier](#3-subtractive-synthesis-source-and-modifier)
- [4. Sources: Oscillators and Waveforms](#4-sources-oscillators-and-waveforms)
- [5. Filters](#5-filters)
- [6. Envelopes and Amplifiers](#6-envelopes-and-amplifiers)
- [7. LFOs, Sample and Hold, and Modulation](#7-lfos-sample-and-hold-and-modulation)
- [8. Additive Synthesis](#8-additive-synthesis)
- [9. Other Analogue Methods](#9-other-analogue-methods)
- [10. Topology and Instrument Types](#10-topology-and-instrument-types)
- [11. Early vs Modern Implementations](#11-early-vs-modern-implementations)
- [12. Environment and Example Instruments](#12-environment-and-example-instruments)

## 1. Analogue, Digital, and Voltage Control

- **Analogue** — representing values continuously rather than in discrete steps, implying (in principle) infinite resolution, though real systems are limited by noise and physical grain. An analogue synthesizer uses voltages and currents to directly represent both audio signals and the control signals that manipulate them; in synthesizer usage the word usually implies voltage-controlled oscillators (VCOs) and filters (VCFs).
- **Analogue vs digital** — illustrated by counting traffic: the cars' movement is continuous (analogue) while the number passing per interval is discrete (digital). Analogue synths are prized for bass, brass, and the synthesizer "cliché" (detuned oscillators beating against each other, plus a resonant filter swept by a decaying envelope), but are poor at imitating "real" sounds, where precise digital synths excel.
- **Voltage control** — a key innovation: instead of mechanical knobs and switches, parameters are set by control voltages (CVs). Because the synth's audio signals are themselves voltages, the same kind of signal serves both as audio and as control — e.g. one oscillator at a few tens of hertz is a tremolo/vibrato modulator, but at a few hundred hertz it becomes a sound source.
- **Sources and destinations** — voltage control has two parts. Sources of CV include low-frequency oscillators (LFOs), envelope generators (EGs), pitch and keyboard controls, and self-oscillating VCFs/VCOs. Destinations include VCO frequency/pulse width, VCF cutoff and resonance, EG times, VCA gain, and voltage-controlled pan.
- **Source and modifier model** — the recurring framework: VCOs are the source of raw audio, while the VCF, VCA, and ADSR (attack decay sustain release) envelopes are the modifiers. Controls split into performance controls (changed while playing) and fixed parameter controls (set and left). Because analogue came first, its terminology and metaphors were reused in later digital methods.

## 2. Pre-Synthesizer Audio Electronics

- **Roots in telecommunications and radio** — audio electronics began with the telephone; microphones, loudspeakers, and Alan Blumlein's 1930s stereo all followed. Oscillators, mixers, amplifiers, filters, and modulation circuits are largely spin-offs from radio electronics adapted to audio frequencies.
- **Building blocks before the synth** — laboratory oscillators (sine and other waveshapes) were used musically before affordable synths existed; mixers combine and select sources; amplifiers boost signals and, via feedback between mic and speaker, can be coaxed into edge-of-oscillation tones; filters pass some frequencies and reject others.
- **Tape, disk, and effects** — tape and (older) wire recorders served as sound sources and simple echo units (two machines, with feedback for repeating echoes); adjusting playback speed changes pitch and tempo together. Reverb/echo come from a room with non-parallel walls; flanging comes from mixing two tape-delayed signals and varying one machine's speed (literally touching the reel flange). The original BBC "Doctor Who" theme used hand-tuned oscillators for the swoops, with the Tardis sound derived from scraping a piano string.

## 3. Subtractive Synthesis: Source and Modifier

- **Subtractive synthesis** — the dominant method in commercial analogue synths: start with a harmonically rich source and use a filter to "subtract" unwanted harmonics, then shape the volume envelope. Its many knobs and switches are intimidating but, because of the near one-to-one control-to-knob relationship, it is excellent for teaching acoustics principles.
- **Three-part instrument model** — real instruments break into a source of sound, a modifier (processes the source's output), and controllers (the performer's interface). Clearest in a clarinet: the reed (source) produces a harsh tone, and the tube acts like a series of resonant filters (modifier). The model is weaker for a guitar, where source (string) and modifier (body) are tightly coupled and cannot be examined in isolation.

## 4. Sources: Oscillators and Waveforms

- **VCO (voltage-controlled oscillator)** — provides voltage control of output frequency/pitch, with typical controls for coarse (semitones) and fine (cents) tuning, a waveform selector, pulse width, and output level. Some offer sub-octave outputs and an audio sync input. **Hard sync** forces the VCO to reset to the incoming signal so it tracks at the same or multiple frequencies, producing a characteristically harsh sound; softer schemes change timbre without locking.
- **Standard waveforms and harmonic content** — the source waveshapes are chosen for being easy to describe mathematically and produce electronically. On some early synths (e.g. the Minimoog) they are ordered by increasing harmonic content:

| Waveform | Harmonic content |
|---|---|
| Sine | Only the fundamental (one harmonic) — no harmonics to filter, so poorly suited to subtractive synthesis |
| Triangle | Small amounts of odd harmonics — just enough for a filter to act on |
| Square | Only odd harmonics — distinctive "hollow" sound |
| Sawtooth | Both odd and even harmonics — bright |
| Pulse | Both odd and even (not all present); content increases as the pulse narrows |

- **Pulse width modulation (PWM)** — varying the mark-space ratio (duty cycle) of a pulse waveform changes its harmonic content. A 50:50 square is the special case with no even harmonics. Cyclically varying pulse width with an LFO sounds similar to two oscillators beating together; the modulation depth must be controlled so a too-narrow pulse doesn't vanish.
- **Idealized vs real waveshapes** — actual analogue waveforms only approximate the mathematical ideals (softer edges, less precise spectra), and these imperfections are part of analogue sound's appeal. Some "sine" outputs are made by rounding a triangle through a non-linear amplifier rather than from a true sine formula.
- **Noise** — random waveshapes contain a constantly changing mixture of all frequencies, providing a non-pitched source.

## 5. Filters

- **Filter** — an amplifier whose gain (more properly, attenuation, since maximum gain is usually one) varies with frequency; a VCF lets a CV alter one or more of its parameters. Filters are powerful timbre modifiers because they change the relative proportions of harmonics.
- **Four response types** — classified by attenuation curve:

| Type | Action |
|---|---|
| Low-pass | Attenuates above the cutoff; sweeping cutoff down makes a sound "darker" (open → closed) |
| High-pass | Attenuates below the cutoff; removes the fundamental first, thinning and brightening the timbre |
| Band-pass | Passes only a range (the pass-band); equivalent to real-world resonances; controls for center frequency and bandwidth |
| Notch | Opposite of band-pass — attenuates a band and passes the rest; can remove single harmonics |

- **Cutoff frequency** — the point of 3 dB attenuation, also the half-power point (half the signal power lost). Below it a low-pass filter is flat; above it attenuation rises at a slope set by the number of **poles** — each RC pole adds 6 dB/octave, so two-pole = 12 dB/octave (more "natural"), four-pole = 24 dB/octave (more "synthetic," larger timbral changes).
- **Resonance (Q)** — a peak in the response at (for low/high-pass) the cutoff frequency; `Q = center frequency / bandwidth`. Usually produced by feeding output back into the input. Most subtractive synths only do low-pass and a "peaky" low-pass that mimics band-pass — a phenomenon called **corner peaking**.
- **Filter self-oscillation** — push resonance high enough that the filter-plus-feedback gain exceeds one at the cutoff, and the filter breaks into self-oscillation, producing a sine wave (often purer than the VCO's). This is itself one way to build an oscillator. Below that point the filter will "ring" — a decaying oscillation used to make many 1970s drum-machine sounds.
- **Keyboard scaling / pitch tracking** — routing the keyboard pitch CV to the filter cutoff makes cutoff follow the played pitch, so every note gets the same relative filtering.
- **Constant-Q vs constant-bandwidth** — constant-Q filters keep Q fixed as frequency changes (bandwidth scales with frequency, sounding "musical"; most analogue filters are this type); constant-bandwidth filters keep bandwidth fixed regardless of frequency.

## 6. Envelopes and Amplifiers

- **Envelope** — the overall shape of a sound's volume over time. In an analogue synth the VCA's gain is driven by a CV produced by an envelope generator (EG); EGs are categorized by how many segments of the shape they control.
- **Envelope segments and the ADSR family** — segments are named attack, decay, sustain, release. The widely adopted **ADSR** produces many shapes from just four controls; its weakness is the static, fixed-level sustain, which makes it poorly suited to percussive piano-type sounds whose "sustain" actually decays to zero. Common variants:

| Variant | Idea |
|---|---|
| AR (attack release) | Two segments only; common on 1970s string machines |
| AD (attack decay) | No sustain; percussive sounds; on a VCO produces a pitch "chirp" |
| ADR / ADS | Add a release or a sustain to AD |
| AHDSR | Adds a fixed-time "hold" after attack (keeps very short percussive sounds audible) |
| ADBDR (attack decay 1 break decay 2 release) | Splits decay at a break-point level; the long second decay ("slope") emulates decaying piano sustains better than ADSR |
| DADSR | A delay before the envelope starts |

- **Gate and trigger** — a keyboard produces two signals: a **gate** indicating whether the key is held, and a **trigger** pulse marking each new key-press. Single-trigger EGs restart only on a fresh gate; multi-trigger EGs restart part of the attack/decay on extra trigger pulses (used on monophonic synths when a held key is joined by another). Gate/trigger routing is usually hard-wired from the keyboard.
- **Linear vs exponential** — many natural envelopes are non-linear (rapid at first, then slowing). A linear attack sounds too slow at first, whereas an exponential rise sounds "correct" — in fact it sounds linear to the ear; many EGs can switch between curve types.
- **VCA (voltage-controlled amplifier)** — usually the final modifier stage, with a CV setting the gain to control volume; an offset can act as a master volume. Linear inputs suit tremolo/AM and exponential envelopes; exponential inputs suit volume changes and linear envelopes. A VCA driven by keyboard pitch CV can act as a crude high-pass (or, inverted, low-pass) "filter" by attenuating low notes — another form of scaling.

## 7. LFOs, Sample and Hold, and Modulation

- **LFO (low-frequency oscillator)** — produces low-frequency CVs for cyclic effects; its waveform *shape* matters more than harmonic content. Beyond sine/square/sawtooth it offers inverted shapes (e.g. ramp-down) and specialized outputs. In practice sine is almost always used for vibrato/tremolo and square almost exclusively for trills.
- **Sample and hold (S&H)** — an LFO repeatedly samples another voltage source and holds that value until the next sample. Fed with noise it produces unpredictable random steps; fed with another oscillator it can be partly random or fully repeating depending on synchronization. Often used to step a resonant low-pass filter's cutoff for "movement," though the rhythmic random-timbre effect became an overused cliché.
- **Arbitrary / function generators** — multi-segment shapes built from levels, slopes, or curves; can replace EGs, control panning, or act as simple sequencers.
- **Envelope follower** — almost the inverse of a VCA: it rectifies an audio signal and low-pass filters it (cutoff a few hertz) to extract a CV representing the input's envelope, letting external audio drive a synth (some also output gate/trigger).
- **Waveshaper** — a non-linear amplifier that changes a waveform's shape and thus its harmonic content; effectively adds distortion (the guitarist's "fuzz box" is a familiar example), best on monophonic signals.
- **Vibrato vs tremolo, and modulation types**:

| Type | What changes |
|---|---|
| AM (amplitude modulation) | Level of the signal; low rate (under \~25 Hz) gives tremolo, higher adds extra frequencies |
| FM (frequency modulation) | Frequency of the signal; low rate gives vibrato, higher produces sidebands |
| PWM | Pulse width of the source waveform (timbre) |

- **Cross-modulation** — connecting two VCOs to each other's frequency CV input so each modulates the other, giving complex FM-like timbres that are hard to keep in tune.

## 8. Additive Synthesis

- **Additive synthesis** — the near-opposite of subtractive: build the final sound by adding together sine waves of different frequencies. Because so many parameters must be controlled at once, the user interface is far more complex.
- **Fourier foundation** — based on Fourier's 1807 theorem that any periodic waveform can be reproduced by adding a series of sine waves (specified by frequency and amplitude). Harmonics are integer multiples of the fundamental `f` (2f, 3f, …); the second harmonic is also called the first overtone.
- **Shape vs harmonic content** — waveform shape is a poor guide to harmonic content: small shape changes can cause large harmonic changes, and phase shifts of harmonics greatly alter the shape while (above \~440 Hz) leaving timbre essentially unchanged. A spectrum (frequency vs level) shows harmonic content directly; a "waterfall"/"mountain" graph stacks spectra to show change over time.
- **Number of harmonics** — most additive synths use between 32 and 64 harmonics. Real sounds also contain **inharmonic** content (noise, beat frequencies, sidebands, and inharmonics — non-integer partials that sound bell- or gong-like); purely deterministic harmonic-only synths miss these.
- **Per-harmonic control and filter emulation** — ideally each harmonic gets its own EG and VCA (plus an overall envelope for quick changes). Grouping/ganging harmonics (e.g. "all odd," "all even") tames the control count. A filter can be *emulated* by giving higher harmonics shorter decay times so they fade first, mimicking a low-pass sweep but with finer control than a single VCF.
- **Practical difficulty** — generating many stable, pure sine waves at once is hard, and a 32-harmonic instrument with eight parameters each yields over 250 controls; practical additive synthesizers have therefore tended to be digital.

## 9. Other Analogue Methods

- **Amplitude modulation (AM)** — borrowed from radio: a modulator changes a carrier's level. The output contains the carrier plus the sum and difference frequencies (sidebands); the modulator itself is not present. With non-sinusoidal inputs every harmonic produces its own sidebands, giving complex inharmonic spectra. Made by feeding a VCO into a VCA's modulation input.
- **Frequency modulation (FM)** — a modulator changes the carrier's frequency by an amount called the deviation. Unlike AM it produces many sidebands; the **modulation index** = `deviation / modulator frequency` sets roughly two more sidebands than its value, and sideband amplitudes follow Bessel functions. Very powerful for complex spectra but limited in analogue by VCO tuning stability. Made by feeding one VCO into another's frequency input.
- **Ring modulation** — uses a "balanced modulator" to output only the sum and difference of two inputs; neither carrier nor modulator appears in the output. Useful where original pitch must be lost (pitch transposition) and for bell-like timbres; widely used for "alien" and robot voices.

| Modulation | Carrier in output? | Sidebands (sine inputs) |
|---|---|---|
| AM | Yes | Simple |
| FM | Yes | Multiple |
| Ring (RM) | No | Simple |

- **Formant synthesis** — emulates the strong resonances ("formants") that dominate real instruments and the voice, by adding a graphic equalizer or complex filter (often several parallel sections) on top of the VCF/VCA to control the bandwidth of the sound.
- **Damped oscillators / ringing filters** — resonant circuits made to ring produce decaying sine waves ideal for percussive sounds; many 1970s/early-1980s rhythm-machine drum sounds were built this way (filters and oscillators are just different uses of resonant circuits).
- **Organ and piano technologies** — traditional organs are essentially additive: a master oscillator generates many sine waves that drawbars mix, though (until the mid-1980s) without per-harmonic envelopes. Pre-sampling electronic pianos and 1970s "string machines" gated and filtered square/pulse waves from a master-oscillator-plus-divider to make polyphonic piano- and string-like sounds.
- **Tape, optical, and other techniques** — tape recording stores sounds for later manipulation; optical film soundtracks let sound be drawn or painted directly onto film (slow and exacting, hence usually combined with tape); Foley/sound-effects work and turntable/vinyl manipulation are further "analogue" methods of sound generation.

## 10. Topology and Instrument Types

- **Topology** — how the modules are arranged and ordered. The most common arrangement follows the source-and-modifier (excitation-and-filter) model: one or more VCOs plus a noise source, then a VCF and VCA controlled by EGs, with an LFO for cyclic modulation. This basic patch is so common it is hard-wired into many designs; **normalized jack sockets** preserve the wiring until a plug is inserted to override it.
- **Monophonic synthesizers** — performance instruments for melodies and lead lines; despite the name many are duophonic. Multiple held notes need an assignment strategy: **last-note priority** (most recently played note) or **low-note priority** (lowest pitch, enabling drone-plus-run playing). Front panels run sources/controllers on the left, modifiers and output on the right.
- **Portamento and glissando** — **portamento** is a smooth glide between pitches, produced by limiting how fast the pitch CV can change (the portamento time). **Glissando** moves chromatically through every note in between; at speed the two sound similar.
- **Polyphonic synthesizers** — typically several monophonic "voices" sharing one keyboard, with key-assignment circuitry handling note allocation and note-stealing; voices usually share one timbre (multi-timbrality is mainly digital). Memory recall is emphasized over front-panel programming (e.g. the Yamaha CS-80 hides tiny programming controls under a flap while large memory-recall buttons sit at the front). Separate per-voice LFOs (vs one shared LFO) give slightly different rates/phases, improving string and vocal sounds.
- **Performance vs modular synthesizers** — performance instruments use a fixed VCO-VCF-VCA topology and memories for quick results. **Modular** synthesizers have few or no preset connections and great flexibility, but are slow to patch, usually have no memory, are nearly "write-only" (hard to reconstruct a patch later), and have very limited polyphony — impressive on stage but better at variations on a narrow set of sounds.
- **Keyboards vs other controllers** — most synths are keyboard-centric (pitch-bend, modulation wheel, after-touch, keyboard tracking). Alternative controllers (violin/cello bow pressure, guitar per-note vibrato, woodwind breath/lip techniques) expose parameters that have no keyboard equivalent.

## 11. Early vs Modern Implementations

- **Tuning and stability** — early Moog VCOs were refined prototypes built at the limits of knowledge, and their oscillators drifted with temperature because diodes/transistors (used to make the exponential control law) change with heat. Fixes evolved from a special "Q81" temperature-compensation resistor to matched differential transistor pairs and finally custom chips. Tuning problems fall into overall tuning, scaling, high-frequency tracking (VCOs going flat at the top of their range), and controllers; ironically the resulting "beating oscillator" sound is now emulated in temperature-stable digital instruments.
- **Voltage-control standards** — despite the name most circuitry is actually current-controlled. Two pitch standards competed: **1 volt/octave** (linear voltage-to-pitch, logarithmic voltage-to-frequency; the popular choice) and **exponential** (linear voltage-to-frequency, more resolution at high frequencies); converters between them existed.
- **Circuit techniques** — VCOs commonly use a relaxation oscillator (a current charges a capacitor that discharges at a threshold, giving a sawtooth). Filters include the Moog **ladder filter** (cascaded RC networks whose transistor/diode junction resistances are set by a control current) and the **state-variable filter** (a three-op-amp loop giving simultaneous low-pass, high-pass, and band-pass outputs; constant-Q), with the related bi-quad being constant-bandwidth.
- **Integration over time** — construction moved from discrete transistors to op-amps, then custom chips integrating a whole VCO or VCF, and by the mid-1980s a complete VCO/VCF/VCA/LFO/EG "voice" on a single chip; in the 1990s the VCO was often replaced by digital generation feeding analogue VCF/VCA chips.
- **The impact of MIDI** — MIDI replaced incompatible CV/gate/trigger schemes with digital data, standardized performance controllers (permanently fixing the pitch-bend and modulation wheels into the design), provided system-exclusive sound storage, and made layering as simple as connecting a cable. It coincided with microprocessors becoming near-obligatory, enabling auto-tuning, sound memories, and eventually keyboard-less rack modules and synths-inside-the-computer.

## 12. Environment and Example Instruments

- **Analogue sampling without tape** — the **bucket-brigade delay line** stores audio as charge passed along a chain of capacitors via switches; cheap and easy to integrate, popular in 1970s/80s echo, chorus, and reverb units, but limited by charge leakage and clock signals bleeding into the audio (hence a reputation for poor high-frequency response). Acoustic **spring-line and plate** delay lines carry sound mechanically, suited to reverb rather than true sampling.
- **Tape sample-replay (Mellotron)** — the **Mellotron** is a trademarked tape sample-replay instrument with a separate length of tape per key: pressing a key pulls its tape across a replay head, and a spring/bin returns it to the start so the sound re-synchronizes. Loops cannot be used (no start sync), so notes have a fixed maximum length; user recording is so hard it is effectively a sample-replay (not true sampling) device. Tape speed links pitch and time inversely — exploited by Les Paul in the 1950s to record slow and replay fast for virtuoso passages.
- **Sequencing** — analogue sequencing comes in two forms: **step sequencers** (usually 16-step loops of CV/gate set by rows of knobs/sliders with scanning LEDs; a **quantiser** turns continuous CV into discrete semitones) and more general **CV-and-gate** sequencing storing pitches, durations, and rests (e.g. Roland's 1977 MC-8 MicroComposer, programmed as numbers). Synchronization before MIDI used standards like DIN-Sync 24 (24 pulses per quarter-note plus start/stop).
- **Recording and performing** — analogue rigs face ground-loop hum, tuning drift, mostly-mono outputs needing panning, and bass-heavy mixes from heavy low-pass use. Polyphony from a monosynth means multiple machines or multiple takes (with their tuning and LFO-rate differences becoming an asset). Live, synths were stacked (synth over string machine over organ) for two-handed multi-keyboard playing; early instruments lacking memories required performers to make fast edits (VCO waveform, detune, cutoff, resonance, attack, decay) by hand mid-performance.
- **Landmark instruments** — the **Moog modular (1965)** established the patchable module format; the **Minimoog (1969)** hard-wired VCOs-VCF-VCA with two ADS EGs into the de facto "basic" voice circuit for portable performance; the **Yamaha CS-80 (1978)** was an early expressive polyphonic synth (eight dual-voice card sets); the **Sequential Prophet 5 (1979)** added digital sound storage and "poly-mod" cross-modulation to five Minimoog-like voices; the **Roland SH-101 (1982)** was a strap-on live monosynth; and the **Oberheim Matrix-12 (1985)** packed modular flexibility with reassignable display-driven panel controls into a performance case.
