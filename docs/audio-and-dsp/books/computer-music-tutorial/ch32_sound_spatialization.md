# Ch 32: Sound Spatialization

## Table of Contents

- [1. Spatialization and Its History](#1-spatialization-and-its-history)
- [2. Localization Cues](#2-localization-cues)
- [3. Panning and Stereo Image](#3-panning-and-stereo-image)
- [4. Distance, Velocity, and Altitude](#4-distance-velocity-and-altitude)
- [5. Loudspeaker Radiation and Beams](#5-loudspeaker-radiation-and-beams)
- [6. Immersive Sound Systems](#6-immersive-sound-systems)
- [7. Transmission Formats](#7-transmission-formats)

## 1. Spatialization and Its History

- **Two aspects of spatialization** — the *virtual* (studio illusions via delays, filters, panning, reverberation, sometimes architecturally impossible spaces) and the *physical* (projecting sound over multichannel systems around, above, below, and within the audience)
- **Two dominant illusions** — horizontal *panning* (lateral movement between speakers) and *reverberating* (a dense diffuse echo pattern situating sound in a larger space); vertical/*periphonic* "sound with height" panning (Gerzon 1973) adds overhead effects
- **Five spatialization paradigms** — live manual diffusion (GMEB, GRM, 1970s), interactive upmixing (SpatialChords), automated spatial sequencing (IRCAM Spat, ZKM Zirkonium), immersive naturalistic imagery in VR/games on headphones, and sound-art installations the audience wanders through
- **Historical lineage** — spatial antiphony at San Marco Venice (Willaert, Gabrieli), Mozart's two-orchestra works, then post-WWII landmarks: Stockhausen's *Gesang der Jünglinge* (1956, five speaker groups) and *Kontakte* (1960, first four-channel tape piece); Varèse's *Poème Electronique* and Xenakis's *Concret PH* over 425 loudspeakers in the Philips pavilion (1958); Xenakis's *Hibiki Hana Ma* on 800 speakers (Osaka 1970); the GRM Acousmonium (1974)
- **Performance enhancements** — use at least a *quadraphonic* (or *octophonic*/8.1) ring; reverse the rear left-right configuration so a front L→R pan becomes a rear R→L pan; elevate corner speakers for periphony; give each amplified performer a local speaker to avoid the *disembodied performer* syndrome (the *precedence effect* means the first sound to arrive dominates, so global reinforcement should be delayed up to 40 ms)

## 2. Localization Cues

- **Three dimensions** — *azimuth* (horizontal angle), *distance* (static) or *velocity* (moving), and *zenith* (altitude/elevation)
- **Azimuth cues** — interaural arrival-time difference (the maximum, \~650 µs, is the *binaural delay*); the head's high-frequency *shadow effect* causing an interaural amplitude difference; and spectral cues from asymmetrical reflections off the pinnae, shoulders, and torso
- **Distance cues** — the ratio of direct to reverberated signal (direct intensity falls with the square of distance); loss of high-frequency components; and loss of soft-sound detail with distance
- **Velocity cue** — *Doppler shift*, a pitch change when source and listener move relative to each other
- **Zenith cue** — spectrum changes from sound reflecting off the pinnae and shoulders
- **Binaural sound** — originally a controlled anechoic-chamber listening condition with restrained heads and probe tubes; now a genre of *binaural recordings* made with a dummy head's two microphones for headphone playback. A source can be placed anywhere in the *binaural field* through HRTF filtering alone

## 3. Panning and Stereo Image

- **Two-speaker positioning** — for equidistant speakers in a ring, the algorithm need only compute the amplitudes of the two adjacent loudspeakers, using the source angle \( \theta \) measured from the midpoint (\( \theta_{max} \) typically ±45°)
- **Linear panning** — \( A_{amp} = \theta / \theta_{max} \), \( B_{amp} = 1 - (\theta / \theta_{max}) \). Creates a "hole in the middle": at center both amplitudes are 0.5, so intensity drops to 0.707 (a 3 dB dip), making the sound seem to recede
- **Constant power panning** — uses sinusoidal curves so that at center both amplitudes are 0.707, preserving constant intensity and a stable perceived distance; the pan is perceived as rotating at constant distance from the listener (Reveillon 1994)
- **Spatial image operations** — a stereo signal decomposes into pure-left (L), center/mono (M), and pure-right (R) components; *image widening* minimizes M to push sound to the extremes. Brief phase inversion or a few-ms delay of one channel shifts the image; *decorrelation* (delays, filters, modulation producing dissimilar copies) enlarges the image across multichannel playback (Kendall)
- **Reflections** — adding small delays to the *nondirect* channels simulates hall reflections and reinforces source direction; sound travels \~340 m/s at 19 °C (1 ms ≈ 0.34 m), and the reflection delay uses the full source-to-surface-to-listener distance

## 4. Distance, Velocity, and Altitude

- **Simulating distance** — lower amplitude, lowpass-filter (air absorption), add echoes, or blend reverberation; to model a fixed room distance, hold reverberation level constant and scale the direct signal inversely with distance
- **Local vs global reverberation** — global reverberation is distributed equally to all speakers, local reverberation feeds adjacent pairs; making local reverberation rise with distance (\( Local\_reverberation \cong 1 - (1/distance) \)) overcomes a masking effect that erases the azimuth cue when direct and reverberant amplitudes are equal
- **Doppler shift** — a cue to *radial* velocity (motion toward/away); *angular* velocity (circling at constant distance) produces zero Doppler. \( new\_pitch = original\_pitch \times [v_{sound} / (v_{sound} - v_{source})] \), with \( v_{sound} \approx 344 \) m/s; positive \( v_{source} \) shifts pitch up. Implemented with a *modulated delay line*. Doppler shifts all frequencies by the same *logarithmic* interval (preserving harmonic relations), unlike linear frequency shifting, which destroys them
- **Altitude (zenith) cues and HRTF** — high-frequency (> \~6 kHz) sound reflecting off the pinnae and shoulders creates short delays manifested as a comb-filter effect; simulated by filtering the input with the *head-related transfer function* (HRTF) (Begault 1991)
- **HRTF problems** — every head, shoulder, and earlobe differs, so no two people share an HRTF and a wrong HRTF collapses the vertical illusion. VR/AR demand for 360° audio drives customized HRTF services (e.g., Genelec's Aural ID); head-motion tracking helps disambiguate elevation and front/back. In concerts, actual overhead loudspeakers beat the fragile virtual illusion

## 5. Loudspeaker Radiation and Beams

- **Radiation pattern** — every sound source has a characteristic 3D *radiation pattern* (frequency-dependent in acoustic instruments), itself a cue to source identity and locale; loudspeaker *dispersion* (a typical studio monitor: 90° lateral) describes where it keeps a linear response. The detectability of a real violin vs its recording is attributed to differing radiation patterns
- **Rotating loudspeakers** — the *Leslie Tone Cabinet* (1949) routed highs to a spinning horn and lows to a rotating baffle over a stationary woofer, with adjustable motor speed; designed for the Hammond B3 but used on voice and guitar. Stockhausen hand-rotated a turntable-mounted speaker for *Kontakte* and *Hymnen*
- **Simulating rotation** — Doppler alone is straightforward (Chowning 1971), but the full Leslie effect is immersive and hard to model: it involves Doppler vibrato, time-varying filtering/phase shifts from diffraction, air-turbulence distortion, and the transfer characteristics of tube amps, speakers, and microphones
- **Superdirectional sound beams** — act like an "audio spotlight" (\~15° wide). Loudspeaker arrays (e.g., Yamaha YSP digital sound projector) bounce focused beams off walls so sound seems to come from around the room. Ultrasonic beams use *acoustic heterodyning* (Helmholtz): two high-amplitude ultrasonic tones (e.g., 90 and 91 kHz) produce sum (181 kHz) and difference (1 kHz, audible) tones via air nonlinearity, projecting a collimated beam

## 6. Immersive Sound Systems

- **Immersive environments** — dozens of surrounding loudspeakers (above and sometimes below), e.g., the ZKM Klangdom, Virginia Tech Cube, Belfast SARC, and the UCSB AlloSphere (also visually immersive). Four main competing techniques: VBAP, DBAP, ambisonics, and WFS; commercial entrants include Dolby Atmos and Apple Spatial Audio. Techniques can be mixed (e.g., VBAP for point sources, ambisonics for environmental sound)
- **Vector base amplitude panning (VBAP)** — a 3D extension of stereo panning that projects a phantom source from *triples* of loudspeakers arranged in triangles, allowing vertical as well as horizontal panning; highly effective for panning around a dome or sphere (Pulkki 1997)
- **Distance based amplitude panning (DBAP)** — takes speaker positions as the starting point, makes no assumption about listener location, and uses *all* speakers with gain set by a distance-attenuation model; suited to irregular layouts (stages, installations, museums)
- **Ambisonics** — reconstructs coherent *wave fronts* using *all* loudspeakers cooperatively (rear speakers help locate front sounds). Invented by Michael Gerzon (1973), revived by AR/VR because it keeps a stable image when the sound field rotates. The raw stream is *independent of loudspeaker layout* (scalable from mono to many speakers); a tetrahedral-capsule mic yields *A-format*, converted to first-order *B-format* (\(W, X, Y, Z\)). *Higher-order ambisonics* (HOA) adds channels for greater spatial resolution and a larger sweet spot
- **Spherical harmonics** — the theoretical foundation: a "Fourier series for spatial position" decomposing the sound field's directionality into orthogonal spherical-harmonic components (shapes resembling omni and figure-eight mic patterns). Decoding needs a regular speaker layout (cube minimum for periphony); rotation matrices enable *tilt/roll*, *tumble/pitch*, and *rotate/yaw* of the encoded field
- **Wave field synthesis (WFS)** — based on the *Huygens principle* (1678) and the Kirchhoff-Helmholtz integral; uses an array of closely spaced loudspeakers, each delayed and weighted, to synthesize a wave front. Uniquely, it can place a virtual point source *within* the listening area between speakers and listener. Demands hundreds of speakers spaced a half-wavelength apart (typically 10–15 cm in practice); wider spacing causes *spatial aliasing*

## 7. Transmission Formats

- **Software formats** — address incompatible, non-portable spatial control data: *ADM* (a .wav with spatial metadata), *SpatDIF* (a structured spatial-scene description), and MPEG standards — MPEG-4 (object-based scene description), MPEG-H 3D Audio (channels, *audio objects*, or HOA; up to 64 channels, binaural rendering), and MPEG-D SAOC
- **Hardware formats** — digital transmission carries hundreds of channels over one fiber-optic or Ethernet cable, replacing heavy analog *snakes*. Competing standards: *MADI* (AES10, 28/56/64 channels over coax/fiber, up to 96 kHz/24-bit, unidirectional); *AES67* (audio-over-IP interoperability); *AVB* (IEEE Ethernet standards reserving up to 75% bandwidth with quality-of-service prioritization); and *Dante* (Audinate, up to 1,024 channels, 192 kHz/32-bit, low latency)
