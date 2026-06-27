# Ch 13: Granular Synthesis

## Table of Contents

- [1. Grains and the Microsonic Time Scale](#1-grains-and-the-microsonic-time-scale)
- [2. History and Theory](#2-history-and-theory)
- [3. Per-Grain Parameters](#3-per-grain-parameters)
- [4. Density and Fill Factor](#4-density-and-fill-factor)
- [5. High-Level Organizational Models](#5-high-level-organizational-models)

## 1. Grains and the Microsonic Time Scale

- **Granular synthesis** — builds acoustic events from combinations of brief sound particles or *grains*; a single grain is a building block, and thousands combined over time create animated sonic textures
- **Grain** — an acoustic event whose duration sits near the threshold of auditory perception, between \~1 ms and \~100 ms (1/1000 to 1/10 of a second), the shortest spans in which duration, frequency, spectrum, amplitude, envelope, and spatial position differences can still be perceived; below \~1 ms, events are heard as subsymbolic clicks
- **Why the grain is apt** — it combines *time-domain* information (start time, duration, envelope shape, waveform shape) with *frequency-domain* information (the frequency and spectrum of the waveform inside the grain)
- **Microsonic / quantum representation** — viewing complex sound as constellations of elementary energy units, each bounded in time and frequency; the same idea recurs under many names — *quantum* (Gabor), *Gaussian elementary signal*, *wavelet*, *FOF* (formant wave function), *VOSIM pulse*, *wave packet*, *pulsar*, *grainlet*, *trainlet*

## 2. History and Theory

- **Corpuscular precedent** — Isaac Beeckman (1616) proposed a *corpuscular* theory of sound: a vibrating string cuts air into spherical corpuscles; scientifically false but a vivid metaphor for granular perception
- **Dennis Gabor** — British physicist who proposed the *quantum*/granular approach in 1946–1947, representing all sound on a time-frequency grid now called the *Gabor matrix* (verified mathematically by Bastiaans); he built an optical-film granulator for *time stretching*, *time shrinking*, and *pitch shifting*
- **Iannis Xenakis** — first to give grains a compositional theory (1960), treating all sound as an assemblage of thousands of pure sounds disposed over a short interval \(\Delta t\); realized in *Analogique A-B* (1959)
- **Computer implementations** — Roads built the first computer granular synthesis (sine waves) in 1974; Barry Truax developed the first real-time implementations (1986–1990); later tools include CloudGenerator, EmissionControl2, and many commercial systems — now mainstream rather than exotic
- **Classical granular synthesis** — the simplest instrument: a sine-wave oscillator controlled by an envelope generator (the Gabor/Xenakis model); substituting a sample player for the oscillator lets any sound be granulated, the prevalent model today. Even a plain sound demands massive control data — thousands of parameter updates per second

## 3. Per-Grain Parameters

- **Per-grain processing** — the heterogeneous sonorities of granular synthesis come from controlling each grain independently; all parameters can be modulated by LFOs, noise, or gestural envelopes
- **Envelope** — an amplitude envelope shapes each grain. Gabor posited a *Gaussian* bell curve \( P(x) \) where \(\sigma\) sets the standard deviation (spread) and \(\mu\) the mean (center peak). The *Tukey* (quasi-Gaussian) window extends the peak over 30–50% of grain duration; *expodec* and *rexpodec* envelopes give percussive and backward-sounding grains; sharp envelope angles cause strong spectral side effects via convolution
- **Duration** — can be constant, function-driven, or random within limits; linking short durations to high-frequency grains characterizes *wavelet* and *grainlet* paradigms. The 100 ms ceiling is soft — second-long grains spawn cascades of pitch-shifted, filtered echoes
- **Effect of grain duration** — a profound signal-processing law: the shorter the event, the greater its bandwidth. Short grains crackle and explode; long grains are smooth. Shrinking a 500 Hz, 100 ms sinusoidal stream to 1 ms explodes the spectrum into broadband noise
- **Waveform** — can derive from any source: synthetic, sampled, or live; classically a sinusoid, but per-grain variation yields polychrome emissions
- **Granulation of sampled sounds** — feeds material through a "threshing machine," delivering grains in new order/microrhythm. The *sample read pointer* (file pointer / scan head) sets where reading starts; it can scan forward, stutter (loop), stagger (time-stretch), reverse, or jump randomly (scrambling). Moving the pointer does NOT change pitch — playback sampling rate is independent of pointer rate
- **Frequency (pitch shift for samples)** — for sinusoidal grains, sets cycles/second; varied per-grain within a *band*, grains scatter as glissandi, pitch scales, or random frequencies (random + wide band → ambiguous pitch). For sampled grains it is a per-grain pitch shift
- **Spatial position** — monaural grains sound flat; scattering each grain to a unique location yields vivid spatial morphology. Per-grain (*selective*) reverberation is most striking at low densities; at high densities halos fuse into a continuous cloud
- **Synchronicity** — degree of periodicity. *Synchronous granular synthesis* (SGS) emits grains at regular intervals where density sets emission frequency (0.1–20 grains/s → metrical rhythms); *asynchronous granular synthesis* (AGS) randomizes onset times (*jitter*) without changing density
- **Intermittency** — degree to which the regular flow is interrupted so that grains are *lost*; distinct from asynchronicity, it overrides the stipulated density

## 4. Density and Fill Factor

- **Density** — grains generated per second; the global control of texture. Low density → sparse rhythm; at a critical point grains fuse into continuous texture; high density → massive clouds
- **Fill factor (FF)** — the product of density and grain duration, the true determinant of opacity. Twenty 100 ms grains/second gives FF \(= 20 \times 0.1 = 2\) (continuous), whereas twenty 1 ms grains gives FF \(= 20 \times 0.01 = 0.2\) (sparse). FF \( < 0.5 \) is sparse; FF \(\geq 1.0\) is continuous
- **Density thresholds (25 ms grains)** — \( < 15 \)/s rhythmic sequences; 15–25/s fluttering (rhythm disappears); 25–50/s increased granular flow; 50–100/s texture band; \( > 100 \)/s continuous sound mass resembling reverberation
- **Density + frequency band** — narrow bands + high density → pitched streams with formant spectra; medium bands → turgid colored noises; wide bands (octave+) → massive clouds

## 5. High-Level Organizational Models

- **Why high-level units** — with \(n\) parameters per grain and density \(d\), specifying one second takes \(d \times n\) values; since \(d\) reaches hundreds or thousands, composers need meso-scale units to stipulate masses of grains from a few global parameters
- **Time-frequency projections** — project grains onto a frequency-vs-time plane: the *Gabor matrix*, Xenakis's *screens* (amplitude-frequency grids filled by set-theory operations — intersection, union, complement), the *short-time Fourier transform* (STFT, linear frequency spacing, fixed window) and the *wavelet transform* (logarithmic spacing, constant \( \Delta f/f \), frequency-dependent window length). STFT/wavelet hide their granular structure from the user
- **Clouds** — a region on the time-frequency plane (like Koenig's *tendency masks*) with fixed duration and adjustable frequency boundaries within which grains scatter at varying densities; non-real-time, pioneered by Roads (1978) and the CloudGenerator app
- **Streams** — real-time generation pioneered by Truax (1986); a streaming granulator spawns derived material by manipulating the sample read pointer (position, speed, direction); examples include EmissionControl2 (multi-file, LFO-controlled) and the Instruo Arbhar Eurorack module
- **Pitch-synchronous granular synthesis (PSGS)** — generates tones with formant regions; a multistage operation of pitch estimation, spectrum analysis, and filtering where each pitch period is a grain driving a bank of *finite impulse response* (FIR) filters; related to *pitch-synchronous overlap and add* (PSOLA)
- **Other models** — *sprays* (MetaSynth, spraying grains onto the time-frequency grid à la Xenakis's UPIC); *scrubbing* (Borderlands Granular, multitouch manipulation of the read pointer); *micromontage* (Vaggione's manual arranging of microsounds into *microfigures* on a DAW timeline); *physical/biological models* (mapping equations like Schrödinger's, percussion shaking, particle systems); *abstract generative models* (cellular automata, chaos, fractals — multiscale coherence is the challenge)
