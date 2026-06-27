# Ch 18: Physical Modeling Synthesis

## Table of Contents

- [1. Principles and Goals](#1-principles-and-goals)
- [2. Excitation and Resonance](#2-excitation-and-resonance)
- [3. Classical Methods](#3-classical-methods)
- [4. Modal Synthesis](#4-modal-synthesis)
- [5. Waveguide Synthesis](#5-waveguide-synthesis)
- [6. Karplus-Strong and Other Efficient Methods](#6-karplus-strong-and-other-efficient-methods)
- [7. Applications and Assessment](#7-applications-and-assessment)

## 1. Principles and Goals

- **Physical modeling synthesis (PhM)** — starts from mathematical models of the physical acoustics of sound production; equations describe the mechanical/acoustic behavior of the system and compute the waveform directly, without samples or wavetables. Also called *synthesis by rule*, *synthesis from first principles*, or *virtual acoustics*
- **Twofold goals** — *scientific* (test how closely equations simulate real instruments; the closer the simulation, the better the system is understood) and *artistic* (create impossible instruments — an elastic cello that expands and shrinks, unbreakable drums, gongs scaled from 10 cm to 10 m, or strings as thick as bridge cables)
- **Strengths** — excels at note-to-note and timbral transitions; naturally captures performance "accidents" (squeaks, mode locking, multiphonics) and gestures (pitch bend, scrapes, palm muting) as side effects of parameter settings
- **Procedural audio** — a related field (Farnell 2010) that models natural/mechanical sound (wind, helicopters) for games and VR, but adapts efficient methods (waveshaping, granular) for perceptual similarity rather than a true physics solution
- **Historical roots** — von Kempelen's mechanical vocal tract (1791); Lord Rayleigh's *The Theory of Sound* (1894); Kelly and Lochbaum's digital vocal-tract model singing *Bicycle Built for Two* (Bell Labs, 1962, referenced in *2001: A Space Odyssey*); Hiller, Beauchamp, and Ruiz's first FDTD instrument models at Illinois; Yamaha's VL1/VP1 (1993), the first commercial real-time waveguide synths

## 2. Excitation and Resonance

- **Exciter / resonator** — the fundamental PhM principle: an *excitation* (bow stroke, stick hit, air blow) causes vibration; a *resonance* is the body's response, acting as a time-varying filter on the excitation
- **Nonlinear vs linear** — the exciter is generally *nonlinear* (has thresholds that, once crossed, change behavior as if a switch flipped); the resonator is generally *linear* (responds proportionally; two summed inputs give a summed output). The linear assumption fails for cymbal crashes and snare rattling
- **Decoupled vs coupled** — *decoupled* (feed-forward): energy flows one way, e.g. noise through a resonant filter (subtractive synthesis). *Coupled* (feedback): the resonator feeds back to the exciter, e.g. a saxophone reed's frequency driven by bore feedback, or violin bow-string friction. This interaction conveys the gesture behind the sound, unlike fixed-sample playback

## 3. Classical Methods

- **Classical methodology** — Hiller and Ruiz at Illinois built models from difference equations, taking the vibrating string as a starting point. The six-step recipe: specify physical dimensions/constants; *boundary conditions*; *initial state*; the excitation force; *impedance* effects (resistance to a driving force — high impedance needs large force for small amplitude, and impedance mismatches reflect waves); and filtering from friction and radiation
- **Difference equations** — *differential equations* describe continuous analog vibration (first applied by Bernoulli in 1732 to a vibrating string); their discrete digital counterparts, *difference equations*, derive new samples from old ones. The *wave equation* describes how each point moves from neighboring forces; solved recursively, sometimes only by iterative approximation
- **Mass-spring (lumped) model** — models a string as discrete masses connected by springs, capturing two essential qualities: *density* (mass per unit) and *elasticity* (a restoring force on displacement, driving *wave propagation*). Distinguishes *longitudinal* waves (displacement along propagation) from *transverse* waves (perpendicular — the main mode in plucked, hammered, bowed strings). Extends to surfaces (circular mesh = drum head) and volumes (6-way lattice)
- **Nonlinear springs as exciters** — defining springs to be nonlinear turns the mass-spring system into a good exciter model (e.g. a piano hammer: mass + nonlinear spring + nonlinear friction)
- **CORDIS-ANIMA and GENESIS** — Claude Cadoz's Grenoble team built CORDIS-ANIMA, a modular Newtonian language with MAT modules ("matter") and LIA modules (interactions) exchanging positions and forces; GENESIS is its 3D graphical front end for building and visualizing physical networks
- **FDTD and FEM** — Bilbao distinguishes lumped mass-spring models from more flexible *direct simulation by FDTD*, which discretizes a PDE-based model over a spatial grid and time. *Finite-element methods* (FEM) subdivide the system into a mesh whose subdomains use *basis/shape functions*

## 4. Modal Synthesis

- **Modal synthesis** — represents a sound object as a small collection of vibrating substructures (strings, bridges, bodies, tubes, bells, drum heads), each with natural *modes of vibration*; the instantaneous vibration is the sum of the modes' contributions
- **Modal data** — each substructure is characterized by (1) the frequencies and damping coefficients of its resonating modes and (2) coordinates of each mode's shape; data come from engineering equations (simple cases) or experimental measurement (complex objects)
- **Flexibility** — more modular than classical methods; substructures can be added or removed dynamically to expand or shrink an instrument, and modal can combine with FDTD for complex instruments like pianos
- **Functional transform method (FTM)** — Trautmann and Rabenstein (2003): closely related to modal synthesis but models the system more precisely and continuously, since it is not bound to a discrete set of measured modal patterns; harder to set up
- **Implementations** — *Modalys* (Adrien and Morrison): a virtual workbench of *objects* (strings, plates, bows, hammers) joined by *connections* with *controllers* at *access* points, scriptable in LISP/Scheme, OpenMusic, or Max. *REAKTOR PRISM*: an exciter feeds a Modal Bank of dozens of resonant bandpass filters per voice. *Substantia* (Sancristoforo): 16 shapes × 23 materials, hundreds of resonant bandpass filters, excitable by noise, samples, or *contact microphones*

## 5. Waveguide Synthesis

- **Waveguide** — an efficient PhM implementation (Julius O. Smith III); a computational model of a medium (usually a tube or string) along which waves travel, built from a pair of *digital delay lines* injected with waves that reflect at the ends
- **Behavior** — traveling waves cause resonances tied to the medium's dimensions; a symmetric network sounds harmonic, while curves, size changes, or intersections alter the resonant pattern; compatible with the Music N unit-generator paradigm
- **Struck-string model** — a monochord: striking sends two waves in opposite directions; the bridges act as *scattering junctions* that absorb and reflect energy. Pitch relates directly to waveguide length
- **Generic instrument model** (Cook 1992) — a nonlinear excitation injected into a delay line hits a scattering junction (a filter modeling a finger, bow, or tone hole) passing some energy on and reflecting some; an end filter models the bridge/body/bell. Noncylindrical tubes are *sampled in space* into equal sections. The *digital waveguide mesh* (Van Duyne and Smith 1993) extends to 3D for vocal tract and reverberation
- **Specific models** — a five-part *waveguide clarinet* (reed, upper bore, register hole, lower bore, bell), needing only one hole; the *TBone* brass workbench (Cook 1991b) exposing many parameters including a mass-spring-damper lip oscillator. *Banded waveguides* (Essl et al. 2004) split the excitation into frequency bands of one resonant mode each — good for struck bars, musical saws, bowed glasses/cymbals

## 6. Karplus-Strong and Other Efficient Methods

- **Karplus-Strong (KS)** — an efficient delay-line / *recirculating wavetable* method for plucked string and drum synthesis (Karplus and Strong 1983; refined by Jaffe and Smith 1983); a noise burst fed into a feedback filter
- **Plucked string** — a length-\( p \) wavetable filled with random values; each output sample is averaged with the previous (a simple lowpass), then reinserted. The repeating wavetable turns noise into a quasiperiodic pitched tone that starts bright and decays to a dark sine — like a plucked string
- **Drum timbres** — a *blend factor* \( b \) (\( 0 \le b \le 1 \)) controls the modifier: \( b = 1 \) gives a plucked string; \( b = 0.5 \) loses pitch and sounds like a drum (then \( p \) sets decay time — large \( p \) is a snare, small \( p \) a brushed tom); \( b = 0 \) negates every \( p + 0.5 \) samples, halving the pitch to a harp-like odd-harmonic sound
- **Decay stretching** — a *stretch factor* \( s \) decouples decay time from wavetable length; \( s = 1 \) is normal averaging, \( s \to 0 \) stretches the decay
- **KS extensions** — Jaffe and Smith added filters for tuning correction at high pitch, decay shaping, removing the pluck attack, glissandi/slurs, sympathetic vibration, pick position, and string stiffness/inharmonicity
- **Scanned synthesis** — a dynamic wavetable controlled by a performer; a physical model vibrating below \~15 Hz (masses, springs, dampers) is scanned along an arbitrary orbit at the note frequency, combining physical modeling with wave terrain synthesis (Verplank, Mathews, and Shaw 2000)

## 7. Applications and Assessment

- **Models of pianos** — the standout PhM success because pianos have few performance variables; faithfully reproduce free string vibration, string coupling, and restrikes that samples cannot. Three rival approaches (modal, waveguides, FDTD); Chabassier's accurate FDTD model needed 24 hours of 300-processor computation per second of sound. *Modartt Pianoteq* (2006) combines nonlinear exciters + modal strings + finite-element soundboard, licensing Steinway/Bösendorfer brand names
- **Particle-based percussion** — Perry Cook's *PhISEM* models shaken/scraped instruments (maracas, cabasa, guiro) from Newtonian collisions of point masses: bean collisions trigger exponentially decaying noise bursts through a gourd-resonance bandpass filter
- **Input devices** — realism needs a controller with many degrees of freedom played by a virtuoso (force-feedback keyboards like ACROE, MIKEY; Cook's HIRN; Expressive E Arché). Raises the question: why not just learn the acoustic instrument? — the answer is new performance modes plus low cost
- **Parameter estimation** — all analysis can be seen as estimating the synthesis parameters that approximate a sound. Wold (1987) used a *Kalman filter* approach (billions of FLOPs/sec) to separate mixed sources; Cook's *Singer* waveguide vocal-tract model derived the *glottal waveform* by deconvolution; neural networks now estimate PhM parameters
- **Assessment** — massive research but mixed commercial success (Korg/Yamaha hardware sold poorly); products include Logic Sculpture, Ableton Collision, Modartt Pianoteq, Reaktor Prism. A core limit: the algorithm alone is incomplete — it also needs a physical interface and a player (or a software *player model*), well-developed mainly for bowed strings
