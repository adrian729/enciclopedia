# Ch 19: Virtual Analog

## Table of Contents

- [1. Evolution of Analog Synthesis](#1-evolution-of-analog-synthesis)
- [2. Digital versus Analog and the VA Approach](#2-digital-versus-analog-and-the-va-approach)
- [3. Waveform Generation and Aliasing](#3-waveform-generation-and-aliasing)
- [4. Filter and Interface Emulation](#4-filter-and-interface-emulation)
- [5. Modeling Analog Signal Processing](#5-modeling-analog-signal-processing)

## 1. Evolution of Analog Synthesis

- **Origins** — analog synthesis began with vacuum-tube oscillators (\~1912); the Theremin was demonstrated in 1920. Pre-WWII instruments (Theremin, Ondes Martenot) had limited timbral variety, expressive mainly through pitch and loudness
- **Ondioline** — Georges Jenny's 1940s breakthrough in timbral variety: pulse trains through a resonant filter bank plus a spring-mounted keyboard for vibrato; in Jean-Jacques Perrey's hands it imitated dozens of instruments
- **Modular voltage-controlled synthesizers** — the 1960s breakthrough (Moog, Arp, EMS, Buchla): *modular* meant functions (oscillators, filters, amplifiers) in separate modules sharing a chassis; *voltage-controlled* meant one module could control another via patch cords, providing automation (e.g. an LFO sweeping a bandpass filter's center frequency)
- **Fall and rise** — analog fell out of favor with cheap digital synths like the Yamaha DX7 (1980s), then revived in the late 1990s; Doepfer's small-format *Eurorack* standard (1995) sparked a boutique-module revolution

## 2. Digital versus Analog and the VA Approach

- **Digital synthesis** — generates *sampled* (tens of thousands of waveform snapshots) and *quantized* (finite set of amplitude values) signals; the core of any digital synth is a sample-generation algorithm
- **Analog synthesis** — no microprocessor; hardware circuits of op-amps, resistors, capacitors, diodes, transformers, and inductors generate *continuous* signals with no sampling clock, amplitude varying freely and instantaneously
- **Virtual analog (VA)** — also *analog modeling* / *analog emulation*: digital techniques that mimic the voltage-control behavior and sound of analog synths, delivering many sonic benefits at lower cost. Each vintage synth (Moog, Arp, EMS, Buchla, Serge) has a discernible sound traceable to circuit topology, components, and interface
- **Generations** — the first VA synths (1990s: Nord Modular, Korg Prophecy, Roland JP-8000) were generic, not emulating any specific instrument; later ones emulated classic 1960-1980 synths (Arturia Buchla Music Easel) or Eurorack modules (Softube Modular). Platforms include Reaktor Blocks, VCV Rack, Cherry Audio Voltage Modular
- **Why emulate?** — cost and convenience: a polyphonic analog modular can cost over $10,000 and is hard to transport, whereas software sells for a fraction or is free (VCV Rack). Software adds stable tuning, hundreds of presets, arbitrary waveforms, displays, and effects
- **Philosophy of emulation** — should a model capture the flaws (the "personality") or create an idealized version with less noise and more features? *Component-level modeling* reverse-engineers actual transistors/resistors/capacitors/diodes; generic models, sample-based plug-ins, and convolution-based methods do not model the circuit. Tellingly, oscillator frequency *drift* — once a flaw — has been reintroduced as a feature

## 3. Waveform Generation and Aliasing

- **Analog waveforms are nonbandlimited** — impulses, square, sawtooth, and noise bands contain frequencies extending up to and beyond audio sampling rates — a feature, not a flaw, of analog
- **Digital must be bandlimited** — a digital synth must stay below the Nyquist frequency or suffer *aliasing distortion* (frequencies above Nyquist reflected into the audio band). Aliasing cannot be removed by output lowpass filtering, since the aliased frequencies are already present
- **Concrete cases** — at 44.1 kHz a bandlimited square wave of 16 odd harmonics aliases above 760 Hz; Lane et al. (1997) showed sawtooth aliasing at 1,500 Hz
- **Three anti-aliasing strategies** — (1) construct bandlimited waveform approximations (windowed-sinc functions per Stilson and Smith 1996; differentiated parabolic sawtooth per Välimäki 2005; IFFT methods; waveshaping; polynomials with interpolation); (2) run the emulation at a higher internal rate (e.g. 96 kHz) then lowpass-filter and downsample; (3) as a last resort, limit the oscillator's frequency range

## 4. Filter and Interface Emulation

- **Filter emulation** — analog synths often work as source-filter (subtractive) systems, so modeling hardware filter circuits is central. Authentic analog filter design balances theory with practice ("the regulation of the filter response is best achieved by ear" — Douglas 1968); only a handful of topologies are captured in software
- **Discrete-time issues** — analog-to-digital filter conversion preserves properties (frequency response, order, control structure) only in standard cases; digital filter changes lag the sampling clock, so states reflect the previous coefficients. Higher rates and resolution help
- **Soft limiting** — Rossum (1992): analog filters limit *softly* when resonating, whereas basic digital filters overload into instant harshness; he fed the distortion back through a lowpass filter for a smoother tone
- **Moog ladder filter** — Stilson and Smith (1996) reverse-engineered it as four one-pole filters in series with global feedback for resonance (US Patent 3,475,623). Välimäki and Huovilainen (2006) listed five goals for a digital resonant filter: per-sample coefficient updates; independent cutoff and resonance (\( Q \)); stability within ranges; analog-like response; and self-oscillation
- **Buchla 292 lowpass-gate** — Parker and D'Angelo (2013) modeled its *vactrol* (electro-optical part), which responds quickly to rising values but slowly to falling ones, giving the struck-object Buchla sound of Morton Subotnick
- **Control interfaces** — analog synths are *nonmodal* (a control's meaning is fixed, all controls accessible in parallel), favoring immediate access; digital interfaces are often *modal* (one knob serves many parameters via modes/menus), cheaper but blocking simultaneous control. Digital patching adds savable, recallable routings impossible to reproduce exactly on hardware modulars
- **Modulation** — one signal (the *carrier*) varies by an aspect of another (the *modulator*), whether low-frequency (tremolo, vibrato, PWM) or audio-rate (AM, ring, FM). Notable distinctions: *exponential FM* (voltage-controlled synths) vs *linear FM* (digital); diode ring modulation vs digital multiplication; *spatial modulation* / voltage-controlled panning (Subotnick's *Touch*, 1968)

## 5. Modeling Analog Signal Processing

- **Beyond synthesizers** — VA extends to loudspeakers, microphones, guitar pickups, electric pianos, tube amplifiers, preamps, equalizers, tape recorders, spring/plate reverberators, tape echoes, phasers, distortion boxes, and compressors. *Convolution* plays a central, revolutionizing role
- **Modeling amplifiers** — two forms: hardware boxes (analog amp with a DSP input stage emulating tube/transistor amps, sometimes a *stomp box*) and software plug-ins (which can include microphone/room models). Vacuum-tube amps have a recognizable color when overdriven — conventional wisdom: tubes emphasize "sweet" even harmonics, transistors "harsh" odd ones (Lassfolk 1996 used waveshaping for tube emulation)
- **Circuit-level emulation** — sophisticated models treat each internal amplifier stage separately; Peavey's ReValver lets designers edit schematics at the component level. Engineers measure a device with many test signals, build emulating algorithms, then run difference and listening tests — a well-engineered emulation differs from the original by less than the unit-to-unit manufacturing variation
- **Machine learning** — the Kemper Profiling Amplifier sends test tones into a real amp, captures them by microphone, and learns an accurate sonic profile of the amp's dynamics and drive
