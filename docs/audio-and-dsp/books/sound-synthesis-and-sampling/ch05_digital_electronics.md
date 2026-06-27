# Ch 5: Making Sounds with Digital Electronics

## Table of Contents

- [1. The Nature of Digital Synthesis](#1-the-nature-of-digital-synthesis)
- [2. FM Synthesis](#2-fm-synthesis)
- [3. Waveshaping and Phase Distortion](#3-waveshaping-and-phase-distortion)
- [4. Modeling: Physical, Source-Filter, and Analogue](#4-modeling-physical-source-filter-and-analogue)
- [5. Granular Synthesis](#5-granular-synthesis)
- [6. Formant and Voice Techniques](#6-formant-and-voice-techniques)
- [7. Analysis-Synthesis and Resynthesis](#7-analysis-synthesis-and-resynthesis)
- [8. Hybrid Techniques and Topology](#8-hybrid-techniques-and-topology)
- [9. Digital Samplers](#9-digital-samplers)
- [10. Sample Editing](#10-sample-editing)
- [11. Sample Storage and Transfer](#11-sample-storage-and-transfer)
- [12. The Digital Environment](#12-the-digital-environment)
- [13. Sequencing, Workstations, and Performance](#13-sequencing-workstations-and-performance)

## 1. The Nature of Digital Synthesis

- **Digital synthesis** — any method using predominantly digital techniques to create, manipulate, and reproduce sound; often the only analogue part is the audio leaving the digital-to-analogue converter (DAC), and software synthesizers in computers are purely digital with no DAC inside.
- **Mathematics-based, precise** — most digital techniques rest on mathematics; precision brings repeatability and consistency (an advantage over analogue drift) but also problems, e.g., exact calculations can cancel harmonics that analogue tuning/phase variations would have preserved, so imperfections sometimes have to be artificially reintroduced.
- **Control vs. effort trade-off** — the depth of control digital offers is an advantage but demands a big time investment; misunderstanding a technique (e.g., forgetting phase parameters in FOF) can radically change the sound.
- **Quantization noise** — grainy roughness heard on decays/releases (pianos, reverbs), caused by the limited resolution of the numbers representing the signal: as values get small, rounding errors appear as extra noise.
- **Aliasing** — a side effect of sampling, from imperfect filtering plus "just good enough" sample rates; sounds like ring modulation, appearing as harmonically unrelated high-frequency components. The author notes "clean" (digital) vs. "natural" (analogue) is subjective — digital has its own distinctive "dirt."

## 2. FM Synthesis

- **FM (frequency modulation)** — taking the output of one oscillator and using it to modulate the frequency of another; impractical on analogue VCOs (drift, non-linearities), it became musically usable only with digital technology. "FM" in synthesizers means audio FM, with both oscillators in the 20 Hz-20 kHz range.
- **Carrier and modulator** — the oscillator producing the heard tone is the **carrier**; the one modulating it is the **modulator** (the term "carrier" persists from radio FM though no radio transmission is involved). The **deviation** is the difference between the highest and lowest frequency the carrier reaches.
- **Modulation index and sidebands** — as the modulator level rises, the **modulation index** increases and more **sidebands** (partials at sum/difference of the carrier and multiples of the modulator frequency) appear above and below the carrier; the modulating frequency itself is not present in the output. Roughly two more sidebands than the modulation index.
- **Bessel functions** — the curves describing how each sideband's amplitude varies with the modulation index; the author frames them as smooth versions of per-frequency envelopes, the further a partial is from the carrier the higher the index needed to bring it in.
- **Frequency relationships** — three basic carrier-to-modulator ratios: **integer** (harmonic, square/saw/pulse-like spectra), **slightly detuned from integer** (harmonic but with beating), and **non-integer** (the bell-like, clangorous timbres FM is famous for).
- **Operator** — Yamaha's name for the FM building block: an oscillator + envelope generator (EG) + digital VCA. Early operators held only a sine wave (the DX7); later ones (TX81z) derived extra waveforms by reassembling the quarter-cycle of the sine ROM, and the SY77/SY99 could even use samples.
- **Algorithm** — Yamaha's term for the arrangement and interconnection of operators; an operator is a carrier or modulator purely by its position. Main types: additive (parallel), pairs, stacks, multiple carriers, multiple modulators, feedback, and combinations.
- **Feedback** — routing an operator's output back to its own (or a loop's) frequency input; small amounts enrich harmonics (sawtooth/pulse-like), large amounts produce noise-like ("off-white") timbres. SY-series added a dedicated white-noise generator to avoid relying on feedback noise.
- **Few parameters, strong control** — FM defines a timbre with carrier frequency, modulator frequency, and modulator level (well under 20 parameters total for a full sound) — far fewer than additive/subtractive, making it powerful under real-time control though hard to program.
- **Phase modulation in practice** — Yamaha's FM actually uses phase modulation, which lets an operator be modulated without its pitch changing for asymmetric waveshapes, making musical sounds easier to program; Casio's VZ series used a similar method called phase distortion (PD).
- **History and reach** — John M. Chowning's 1973 JAES paper was the landmark; the DX7 (1983) was the first all-digital synthesizer with huge commercial success and hosted the first public MIDI test. Variants reached the FS1R (voiced/unvoiced "formant" operators, 1998) and the DX200 with sound interpolation/morphing (2001).

## 3. Waveshaping and Phase Distortion

- **Waveshaping** — introducing controlled distortion by passing an oscillator's monophonic output through a **non-linear amplifier**; unlike a guitar fuzz box it changes only the waveshape and adds no intermodulation distortion between notes.
- **Transfer function** — the graph relating input to output (input horizontal, output vertical, both scaled -1 to 1); a straight line passes the signal unchanged, while curves distort the waveform and so change its harmonic content (usually adding harmonics). Symmetry of the curve sets whether odd or even harmonics are added.
- **Chebyshev polynomials** — used to design a transfer function that produces any required spectrum from a sine input; a fourth-order function quadruples the frequency, and summing functions builds a composite curve for the target spectrum.
- **Dynamic waveshaping (filter emulation)** — by designing the curve to pass through the origin and using inputs below maximum, low levels stay sinusoidal while higher levels add harmonics, mimicking a VCF opening up; an amplifier corrects the level. Added harmonics are always harmonically related to the input.
- **Phase distortion (PD)** — Casio's CZ-series name for waveshaping, achieved by varying the read-rate through a sine wavetable (equivalent to a phase change); presented to the user as a DCO followed by a digitally controlled waveshaper (DCW) that behaves like an analogue VCF.

## 4. Modeling: Physical, Source-Filter, and Analogue

- **Physical modeling** — a DSP-based mathematical model of how a real instrument works that produces the whole sound in one operation; because the model covers the entire instrument it yields realistic note-to-note transitions, but needs deep physics/acoustics knowledge and large per-patch data (the Yamaha VL1 used \~3000 bytes/patch vs. a DX7's 155).
- **Continuous vs. impulsive models** — **continuous** models cover blown/bowed instruments with ongoing energy transfer (trumpet, violin); **impulsive** models cover plucked/struck instruments where a sudden energy impulse decays away (piano, snare). Drivers (the excitation signal) and resonators are the two main parts.
- **Karplus-Strong algorithm** — a 1983 plucked-string impulsive model using a damped resonator and a step (or noise-burst) input; simulated with a time delay modeling waves along the string and reflections that lose energy so the sound decays.
- **Digital waveguide** — a computationally efficient resonator simulation: essentially a delay line with feedback taps driven by shaped driver pulses; tubes use one waveguide, strings two (either side of the excitation point), brass several for the horn.
- **Source-filter synthesis** — a simplified modeling technique (from speech research) splitting an instrument into **drivers** (raw sound), **resonators** (filters that color it), and **coupling** (how they interact); a fixed driver "sample" feeds a variable resonator, so timbre can change far more than a filtered S&S sample, but it lacks the true between-note behavior of full physical modeling. Used by the Technics WSA1 (1995).
- **Analogue modeling (virtual analogue)** — converting analogue synthesizer circuitry into software; far simpler than physical modeling and the dominant growth area of the early 2000s (Clavia Nord Lead led, 1995). Oscillators are either **waveform playback** (replaying a sampled waveform) or **oscillator modeling** (modeling the oscillator mathematically, more consistent across pitches).
- **Deliberate degradation** — "perfect" modeled filters are intentionally degraded to sound analogue: adding noise to cutoff/resonance/feedback, reducing resonance as cutoff drops, and rolling off high frequencies; envelopes and VCA distortions can likewise be modeled.

## 5. Granular Synthesis

- **Granular synthesis** — building sounds from very short fragments called **grains** (10-100 ms, near the ear's 10-50 ms timing resolution), much as a printed image is built from dots; approaches sound bottom-up rather than via the source-and-modifier model. Historically academic, now available in software (e.g., the grain-wave synth in Propellerhead's Reason).
- **Grain control** — main parameters are the number of grains per time period, their frequency content, and amplitude; grains are enveloped to start and end at zero amplitude to avoid clicks, and may contain single-frequency waveforms, band-pass noise, or processed samples.
- **Limiting case of wavetable** — granular can be seen as wavetable synthesis with the table swept very rapidly with smoothly enveloped, zero-crossing grains; the constant change of grains yields "glistening" or "shimmering" textures (likened to film frames combining into motion).

## 6. Formant and Voice Techniques

- **Formants** — fixed resonant peaks in a spectrum; the voice produces a harmonic-rich vocal-cord pulse filtered by the (largely fixed) tube of mouth/nose/throat, so formant peaks stay put regardless of the sung pitch. Modeled as a source (pulse triggered at the fundamental rate) plus dynamic band-pass/notch filters.
- **Vocoder** — a Bell Labs (1930s) device splitting a signal into frequency bands with band-pass filters and **envelope followers**; by separating analysis and synthesis it can extract one sound's spectral envelope and impose it on another. Octave bands need \~8 filters, third-octave bands \~30-31 for finer resolution; voiced/unvoiced detection substitutes noise for unvoiced sounds.
- **Phase vocoder** — a digital vocoder using narrow, high-resolution bands that outputs both amplitude and phase information, improving processing quality and creative possibilities.
- **VOSIM (VOice SIMulation)** — a 1970s University of Utrecht oscillator producing pulse trains of decaying raised sine-squared pulses; because the spectrum depends on the pulse parameters (width, decay, count, repetition rate) not the repetition rate, the harmonic content is independent of pitch — ideal for fixed formants, suited to speech rather than mass-market music.
- **FOF (Fonctions d'Onde Formantique)** — Xavier Rodet's early-1980s formant-wave-function synthesis; each FOF "oscillator" generates one formant by outputting a series of smoothly enveloped audio bursts (each the filter's impulse response) whose repetition rate sets the pitch while the burst contents set the formant. Below \~25 Hz it becomes granular (FOG mode), allowing transformation between vocal imitation and granular texture. Part of IRCAM's CHANT package.
- **Dynamic filtering** — techniques like **LPC** (linear predictive coding), CELP, PARCOR, and E-mu's **Z-plane** filters use a single real-time multi-formant digital filter to process a source into the desired output, equivalent to several FOF oscillators at once.

## 7. Analysis-Synthesis and Resynthesis

- **Analysis-synthesis / resynthesis** — take a sampled sound, extract descriptive parameters, then recreate it with a synthesis technique; the two hard problems are converting the sample into meaningful parameters and choosing a suitable synthesis method (plus mapping between them).
- **Analysis tools** — **FFTs (Fast Fourier transforms)** convert time-domain waveforms to frequency-domain spectra (resolution inversely proportional to window length, with overlapping windows for detail); **linear predictive** methods give formant filters; **PCA (Principal Component Analysis)** finds the principal axes of variation to pull a sound apart into reusable components.
- **Pitch extraction** — methods include **zero-crossing** counting (error-prone with harmonics), **auto-correlation** (matching the waveform against a delayed copy), **spectral interpretation** (lowest common divisor of harmonics), and **cepstral analysis** (taking the spectrum of the log-spectrum so the "cepstrum" shows a peak at the fundamental). Envelope is extracted by low-pass filtering plus a leaky peak detector.
- **Choosing a synthesis engine** — **additive** needs few extraction steps but overwhelms the user with per-harmonic envelopes; **FM** has few parameters but no straightforward way to work backwards (deconvolution) from a sound; **subtractive** is too limited; **formant** (FOF/VOSIM) handles complex changing formants; **physical modeling** is itself a kind of analysis-synthesis. Additive and FOF/VOSIM are judged the best resynthesis engines.
- **Resynthesizers in practice** — commercial resynthesizers have largely failed to balance a usable interface, fast analysis, and a versatile engine; Hartmann's Neuron (2003) used Prosoniq's "Multiple Component Feature Extraction" and "resynators" with "scape" (driver) and "sphere" (resonator) parameters, but its unfamiliar metaphors and cost limited it before the company folded.

## 8. Hybrid Techniques and Topology

- **Hybrid techniques** — combining synthesis methods to widen the sound range and dodge any one method's weaknesses; e.g., Yamaha's SY77/SY99 mix AFM and AWM2 (S&S) via **RCM (real-time convolution modulation)**, letting an S&S waveform modulate the FM operators. Korg's Prophecy/Z1, Kurzweil's VAST, Propellerhead's Reason, and Native Instruments' Reaktor combine several techniques (often in software).
- **Topology** — digital synthesizers lift the fixed-signal-path restrictions of analogue instruments; FM's operator algorithms reconfigure carrier/modulator roles far more radically than an S&S synthesizer's two parallel paths, while samplers need little reconfiguration. Software, however, imposes its own topologies to manage complexity.
- **Embedded operating systems** — synthesizers/samplers run embedded computers in assembler or C, historically burned to ROM and rarely updated; reprogrammable memory and field-updatable operating systems did not become common until the twenty-first century, and version counts stay in single digits.

## 9. Digital Samplers

- **Sampler** — equipment that records a sound, stores it, and replays it on demand; the ability to **record** is what distinguishes a sampler from synthesizers that only store and replay. Functionally, tape/cassette/DAT/MiniDisc recorders, echo units, and computers all qualify as samplers.
- **Three devices, three modes** — built on the ADC (records), memory (stores), and DAC (replays); operated in record, edit/store, and replay modes. Recording starts before the sound's onset so the attack is captured, then editing aligns the start.
- **S&S vs. sampler** — the key division is memory type: S&S instruments use fixed **ROM** (samples cannot be edited, so they rely on the synthesizer modifier section), while samplers use volatile **RAM** (samples can be edited). The two have converged, as S&S gained user sample RAM and samplers became largely replay-only.
- **Sampler types** — **stand-alone** (19-inch rack, MIDI-controlled), **keyboard** (less commercially successful than S&S keyboards), and **computer-based** (initially sound cards, later software). **Direct-to-disk / hard disk recording** is a computer-sampling variant storing audio straight to disk, so length is limited only by disk size, evolving into sample-based workstations.

## 10. Sample Editing

- **Normalization** — the most important editing step: setting the loudest sample close to the recorder's maximum and adjusting the others to match, giving consistent apparent loudness across pitch and intonation levels.
- **Truncation (topping and tailing)** — trimming the unwanted portions before and after the wanted sample to set the start and end points so replay begins without delay.
- **Looping** — repeating a portion of the sample (the digital equivalent of a tape loop) to extend the sustain and save memory; the splice between loop end and start can click, addressed by matching level, slope, and rate-of-change-of-slope, by splicing at **zero-crossings**, by reverse-direction playback, or by **cross-fading**. Even a clean splice can shift pitch if the cycle time is not maintained, and timbre mismatches at the loop point are heard as glitches.
- **Stretching (time-stretching / pitch-shifting)** — independently changing timing without pitch, or pitch without timing (unlike transposition, which changes both); done by repeating/removing sample values or whole cycles, or by interpolation filtering, which degrades audio quality.
- **Re-sampling** — recording the output of a sample replay to capture LFO/filter-sweep snapshots or change sample rate; degradation accumulates with each pass, so it is best done at the original pitch.
- **Multi-sampling and keymaps** — using several samples across the note range (e.g., piano) to avoid the artifacts of large transposition; extreme transposition causes **munchkinization** (comic pitch/timing change), and percussion (triangle, tambourine) sounds wrong when transposed at all. The mapping of samples to their home pitch, intonations, and output notes is the **keymap**.

## 11. Sample Storage and Transfer

- **RAM types** — short-term sample storage uses fast read-write RAM: **static RAM** holds data while powered (good for battery backup) and **dynamic RAM** is cheaper but must be continuously refreshed. Longer-term storage uses magnetic, optical, or **flash** memory (which needs no backup battery).
- **Storage demands** — digital audio is large: 16-bit stereo at 44.1 kHz is \~600 Mbytes/hour (about one audio CD); 8-bit halves this with a big quality loss, and lowering the sample rate only suits limited-bandwidth bass/drum sounds.
- **Compression** — **MP3** (the audio layer 3 of MPEG-1) cuts data to \~a tenth of CD rate by removing redundancy then hiding deficiencies where louder sounds mask them; AAC and others go lower. Compression suits broad-spectrum music but exposes weaknesses on single-instrument, single-pitch samples.
- **Transfer standards** — the MIDI **Sample Dump Standard (SDS)** was slow; SMIDI (SCSI-MIDI) saw little uptake; SoundFonts and MIDI **DLS (downloadable sounds)** transfer over LAN/Internet. The music industry lagged the computer industry's moves from SCSI to FireWire/USB 2.0; beyond MIDI, **OSC (Open Sound Control)** and **HD-MIDI** are the main successor protocols.

## 12. The Digital Environment

- **Digital effects** — built-in effects (vs. outboard) can be saved with a sound and controlled by the instrument's own parameters (LFO speed driving chorus, after-touch driving reverb mix, echoes synced to tempo), and avoid the extra DAC/ADC conversions an external unit requires.
- **Digital mixers** — motorized faders allow store/recall of mix scenes per song position, can save the whole user interface as an extension of the instrument, and often include built-in effects; digital inputs remain rarer than digital outputs.
- **Drum machine** — combines a cyclic timing device (a clock counted into beats and bars) with drum sounds; a **pattern buffer** (a set of switches reflecting the stored pattern) determines which beats sound, mapped to drum sounds via a patch-bay-like assignment, with patterns chained into songs. Sounds come from ringing filters and gated filtered noise, sample replay, or modeling.
- **Drum machine history** — from tape-loop units (Chamberlin's Rhythmate 40, 1949) and the Wurlitzer Sideman (1959) to Roland's user-programmable CR-78 (1978) and the influential TR-808 (1979), whose LED step-grid interface became standard; the TR-808 and TR-909 found huge success in dance/hip-hop only after going out of production. The Linn LM-1 (1979) pioneered sampled drum sounds in place of analogue circuitry, though the LinnDrum (1982) was the first commercially successful drum machine with digitally sampled sounds. **GM (General MIDI, 1991)** standardized drum-sound-to-note-number mapping, easing pattern transfer.
- **Recording-pattern metaphors** — **real-time** (play pads as the bar loops, like a tape recorder), **step** (advance one beat at a time, good for complex patterns or transcribing), and **grid** (all pads toggle one drum sound's on/off across the bar, for visual thinkers); a **groove** is the slight timing/volume variations that humanize a pattern and can be captured and applied elsewhere.

## 13. Sequencing, Workstations, and Performance

- **Sequencer** — a device to store and replay a sequence of musical events automatically; analogue **step sequencers** used a counter/multiplexer cycling through control voltages (the economical 8- or 16-note sequence became a staple of 1960s-70s electronic music), with a digital pitch quantizer making them analogue-digital hybrids. Roland's MC-8 (1977) was the first computer-based hardware sequencer with large storage.
- **Hardware-to-software shift** — studio sequencing moved to software (Apple Macintosh) from the mid-1980s; computers were poor for stage use (slow restart, unreliable power) until powerful battery-powered laptops bridged studio and stage. A **MIDI data recorder (MDR)** records and replays raw MIDI data; one that interprets MIDI files is a **MIDI file player**.
- **Workstation** — a single compositional device combining a multi-timbral S&S sound source (with piano, drums, and effects), a multi-track sequencer, and removable storage; Korg's M1 (1988) was arguably the first commercially successful one and drove S&S dominance for a decade. The Korg Karma added "generated effects" — an intelligent arpeggiator-like system for transposing and re-triggering held notes.
- **Accompaniment** — automatic accompaniment (walking bass and chordal backing from the left-hand root note and a chosen genre) on home organs, extended to software in PG Music's "Band-in-a-Box," which turns a chords-and-melody "fake sheet" into a full multi-part arrangement.
- **Groove box** — Roland's term (from the MC-303) for a composite of a phrase/pattern sequencer, drum machine, sound source, effects, and live performance controls; the performer builds looping phrases (intro, verse, chorus, fills, even a bar of silence) and chains them live so song length and structure stay flexible.
- **DJs and decks** — DJs evolved from record-players to music-makers: paired Technics SL-1200 Mk 2 turntables and a cross-fade mixer became standard, with beat-matched tempos, scratching, and samplers; much DJ gear notably lacks MIDI sockets, though hybrids like the Korg KAOSS Mixer exist.
- **Multiple keyboards and performance controls** — stacking keyboards changed sounds, polyphony, playing technique, and controllers. Early monosynths (Minimoog, 1969) were monophonic and played the highest held note, prompting two-handed staccato and held-"open"-note techniques; **velocity** (how fast a key is struck, normally polyphonic) and **after-touch** (pressure once held, usually monophonic) are distinct controls, and pitch-bend/modulation wheels and sustain pedals each grew their own performance idioms.
