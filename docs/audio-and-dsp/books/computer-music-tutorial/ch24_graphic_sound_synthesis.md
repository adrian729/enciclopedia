# Ch 24: Graphic Sound Synthesis

## Table of Contents

- [1. The Graphic Synthesis Paradigm](#1-the-graphic-synthesis-paradigm)
- [2. History of Optical and Photoelectric Sound](#2-history-of-optical-and-photoelectric-sound)
- [3. The UPIC System and Descendants](#3-the-upic-system-and-descendants)
- [4. Image-Based Software Synthesizers](#4-image-based-software-synthesizers)

## 1. The Graphic Synthesis Paradigm

- **Graphic sound synthesis** — an interactive approach based on drawing and image transformation, providing paint-box tools (brushes, spray jets, image-modifying implements) for sculpting sound on the time-frequency plane
- **Precise or improvisatory** — a composer who plans each brush stroke gets exact results; one who improvises treats the surface as a sketchpad. A key fact: a beautiful image does not necessarily make a beautiful sound, and vice versa
- **Natural pitch control** — graphics make microtonal phrases, glissandi, portamento, and vibrato filigree easy to draw, provided the surface is labeled at every time scale; even simple operations like *rotate by 45°* can radically transform the audio
- **Sound as picture** — unlike the standard signal-processing library (sound as amplitude/frequency over time, rooted in linear system theory and physical models), graphic synthesis treats sound as an image, opening it to image-processing operations; it overlaps with sonographic spectrum editors

## 2. History of Optical and Photoelectric Sound

- **Optical sound roots** — principles known by 1880 (Bell's light-beam *photophone*); Sholpo's 1918 vision of a graphically controlled "mechanical orchestra" anticipated the field. R. Michel patented photographic tone notation (1925); Avraamov (1929), Pfenninger, and Fischinger hand-drew forms on optical film
- **Photoelectric tone generators** — Potter's *photoelectric tone generator* (1928) and Schmalz's instrument with removable optical *phonogram* discs (1929); rotating-disc instruments followed — the Celluophone, Superpiano, and Welte Light-Tone Organ (1936) scanned photoetched waveforms. The Photona (Ivan Eremeef, 1936) used a light chopper and photocell, supported by conductor Leopold Stokowski
- **Drawn-waveform film** — Norman McLaren drew sound waveforms onto sprocketed optical soundtrack one frame at a time (1948)
- **Graphic-notation scanners** — Lavallée's *sonothèque* read conductive-ink notation with charged brushes; the Cross-Grainger Free Music Machine (1944) read paper notation through eight vacuum-tube oscillators, realizing Grainger's *Free Music* (demanding "non-human performance"); LeCaine's Coded Music Apparatus (1952) used five continuous curves and his Oscillator Bank (1959) optically scanned a sonogram-like score; the Composer-Tron (Kendall, late 1950s) scanned envelopes drawn on a CRT
- **Gabor's speech painting (1952)** — the Nobel physicist painted speech formants on a sonogram scanned by ten photocells, achieving partial intelligibility despite discarding amplitude gradations
- **Oramics (Daphne Oram, 1957–62)** — the composer drew control functions (pitch, vibrato, tremolo, filter, amplitude) on transparent film scanned optically into control voltages for an analog synthesizer
- **ANS synthesizer (Yevgeny Murzin, 1938–57)** — named for composer Alexander Nikolayevich Scriabin; a photo-optical generator of rotating glass disks each holding 144 *phonograms*. The composer etched a *coding field* (a black-mastic glass plate, vertical = pitch, horizontal = time) read by photocells; used by Artemiev in Tarkovsky's *Solaris* (1972)

## 3. The UPIC System and Descendants

- **UPIC** — *Unité Polyagogique Informatique de CEMAMu*, conceived by Iannis Xenakis (engineered by Guy Médigue) in Paris; a flexible graphical interface where one drawn function can serve equally as envelope, waveform, pitch-time score, tempo curve, or performance trajectory — a uniform treatment of composition data at every level
- **First UPIC (1977)** — used a large high-resolution graphics tablet on a drafting table; composers drew waveforms and envelopes (or tapped points joined by interpolation) and drew score *pages* whose frequency/time lines are called *arcs* (movable, stretchable, cut/copy/paste). Xenakis's *Mycenae-Alpha* (1980), with its *arborescences*, was made on it
- **Real-time UPIC** — a 64-oscillator engine (Raczinski and Marino 1988) coupled by 1991 to a Windows PC; a page held 64 simultaneous arcs (4,000 per page), durations from 6 ms to over 2 hours, with four assignable tuning-table scales. Score reading could be driven left-to-right at constant rate or steered (rate and direction) by mouse in real time, with motions recordable and editable, turning UPIC into a performance instrument. The Phonogramme software (1993) offered an UPIC-like interface with *harmonic pens*
- **UPISketch** — the latest UPIC incarnation (Centre Iannis Xenakis), designed for ease (a 675-word manual) and running on Windows, OSX, and iOS. Pick a pencil and sound from a palette, draw a trace (a *gesture* enclosed in a box) with a finger; boxes can be moved in pitch/time, have breakpoint amplitude envelopes, and support microtonal scales and zooming for multitimbral composition

## 4. Image-Based Software Synthesizers

- **Virtual ANS** — a software simulator of the ANS that extends it with hundreds of tone generators (limited only by the processor); converts any sound to an image, plays loaded pictures, and draws microtonal music with various brushes
- **MetaSynth** — Eric Wenger's 1997 rethinking with real-time playback. Any image (even a photograph) becomes sound, with color mapping spatial position (green = left, yellow = center, red = right). The sonographic image can be played back with *any* sound \( A \) (each trace plays a pitch-shifted copy), mapped across a sample bank, mapped to arbitrary scales, and time-scaled (10 s rescaled to 1 s or 100 s), letting it function like a concatenative synthesizer (e.g. mapping speech onto percussion samples)
- **Kaleidoscope** — 2C-Audio's MetaSynth-like interface but built on a bank of 64–512 resonating filters; graphic *image maps* act as envelope controls determining which resonators play and at what intensity as a cursor scans left to right, with tunable resonators and color setting stereo position. It acts as an effects processor for an input sound, or as a synthesizer when fed pure noise
- **Implementation** — Jean-François Charles (2008) wrote a Max/Jitter tutorial on spectral sound processing as a guide to manipulating sonographic data, with universal principles beyond the Max specifics
