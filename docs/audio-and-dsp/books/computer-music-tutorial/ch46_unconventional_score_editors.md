# Ch 46: Unconventional Score Editors

## Table of Contents

- [1. Why Go Beyond Common Music Notation](#1-why-go-beyond-common-music-notation)
- [2. Roles and History of Unconventional Editors](#2-roles-and-history-of-unconventional-editors)
- [3. Graphic Synthesis and Graphical Notation](#3-graphic-synthesis-and-graphical-notation)
- [4. Notation as Real-Time Visualization](#4-notation-as-real-time-visualization)
- [5. Notation for Documentation and Analysis](#5-notation-for-documentation-and-analysis)
- [6. Automatic Notation from Sound](#6-automatic-notation-from-sound)

## 1. Why Go Beyond Common Music Notation

- **Scope of the problem** — much notated music falls outside CMN: medieval notation, guitar tablature, non-European systems (Indian, Chinese, Japanese, Indonesian), *extended techniques*, and the graphical scores central to electronic-music culture (e.g. Stockhausen's *Kontakte*, 1960); John Cage's *Notations* (1969) collected fragments from 269 composers, \~one-third using non-staved notation
- **Pitch/time bias** — CMN is biased toward pitch and duration, limited to equal-tempered pitches, durations of a single geometric series (1/4, 1/8, 1/16…), and pulsed rhythms
- **Missing dimensions** — CMN has few provisions for timbre, no representation of spatial trajectories, and its single-event *note* abstraction cannot capture mutating multi-event sound complexes like granular streams and clouds, nor multiple synthesis-parameter envelopes
- **Other limits** — sight-reading takes years (excluding the untrained, whereas gestural/graphical notation can be grasped intuitively); CMN addresses only one level of form, cannot look below the note, and is largely unnecessary for editing Music *N* note lists or DAW clip/MIDI data
- **Music Notation Project** — an initiative to raise awareness of CMN's disadvantages and explore alternative systems

## 2. Roles and History of Unconventional Editors

- **Four roles** — graphical *sketching* as a working medium before/during composition; a *GUI* for drawing synthesis-parameter envelopes; a reading score made *after* composition for study, analysis, and teaching; and real-time *visual music* presented alongside electronic sound
- **\_Notation concrète\_** — Pierre Schaeffer (founder of the Groupe de Recherches Musicales, GRM) made an early machine-aided transcription (Schaeffer and Moles 1952), a written amplitude-versus-time trace on sprocketed graph paper, hand-transcribed into familiar notation
- **Scriva** — an advanced 1978 University of Toronto editor (Buxton) supporting CMN (with or without staves), piano-roll, envelope, and *iconic* (timbre-by-icon) notation; users could encircle notes with a pointer to scope an editing operation — a pioneering musician-friendly GUI

## 3. Graphic Synthesis and Graphical Notation

- **Graphic sound synthesis** — an interactive draw-and-transform approach; apps like MetaSynth and UPISketch are visual editors organizing user drawings on a timeline, with paint boxes, brushes, and spray jets for applying "sound color"
- **Heterogeneous sketches** — Delalande's study of 400 GRM acousmatic-composition sketches found no dominant notational convention, showing the difficulty of building a *computer-aided composition* (CAC) system supporting alternative notation
- **CAC systems** — PatchWork kept both a CMN representation and the *patch* that generated it; OpenMusic adds rhythm trees, curves, arrays, text, functions, and pictures, organized in a *maquette* — a container of musical objects manipulable by temporal and graphical parameters, which to a certain extent can itself be considered a patch
- **Other tools** — Vaggione built micro-rhythmic micromontage figures with *IRIN* (Caires), encapsulating figures hierarchically into mesostructure; Decibel ScorePlayer network-synchronizes scrolling proportional color scores across tablets; *bach* (in Max) implements CMN and proportional notation with arbitrary-resolution accidentals, rhythmic trees, and polymetric notation, exposing every element's graphic position for reactive systems

## 4. Notation as Real-Time Visualization

- **Visual music lineage** — a long tradition from Castel's *ocular harpsichord* (1725) through the iconic *Poème électronique* (1958, Varèse / Le Corbusier, Philips Pavilion designed by Xenakis) and Xenakis's *Polytopes* sound-and-light spectacles
- **Synchronized but unrelated** — in both *Polytope de Cluny* (1972) and Bauder and Henke's *Deep Web* (2016), visuals were synced to sound only in timing, with no direct relationship between visual and sonic patterns
- **Data-driven real-time notation** — JoAnn Kuchera-Morin's 3D immersive Allosphere works drive music and visuals from the same data set (e.g. a hydrogen-atom electron's wave functions), functioning as real-time notation
- **\_Kinetic scores\_ / animated notation** — Juan Manuel Escalante's code-generated animations (e.g. *The Generation of Maps*, 2020, where a grid controls a modular synth patch); movement adds narrative resources and eases reading, with the open-source *Processing* generating simple vector shapes paralleling hand-drawn diagrams

## 5. Notation for Documentation and Analysis

- **Why DAW files fall short as scores** — a DAW timeline is a form of score (a GUI front end to a Music *N* note list), but MIDI piano-roll notation lacks meta-information (key/time signatures, accidentals, tuplet ties) and audio waveforms are largely illegible amorphous "blobs"
- **No ground truth** — notating electronic music requires inventing a conceptual framework and a visual language seemingly per piece, due to the heterogeneity of its sounds, processes, and forms; even *Stria* (1977, Chowning), which derives micro- and macrostructure from the Golden Section, calls for a specific spectral-component visualization unsuited to other works
- **Acousmographe** — a pioneering integrated GRM tool (Koechlin and Vinet) that inscribes a library of color graphic symbols onto a spectrogram, which can then be removed to leave a readable, expressive form
- **Sonic Visualiser** — "the first program you reach for when you want to study a musical recording rather than simply listen to it"; offers waveforms, spectrograms, chromagrams, 3D plots, plug-in analysis, audio annotation, and export to Music Ontology RDF for the Semantic Web
- **TIAALS, Aural Sonology, eAnalyse / iAnalyse** — TIAALS pairs a sonogram with a chart maker via a *palette* of objects (abstract symbols on the chart); the Aural Sonology Project derives Schaeffer-based signs to "describe, transcribe and analyze music-as-heard"; Couprie's eAnalyse/iAnalyse adds video and image support and multitrack playback
- **Spectromorphology** — Denis Smalley's model describing perceived sound shapes/morphologies in spectra over time; Thoresen, Hedman, and Blackburn created visual languages for its types

## 6. Automatic Notation from Sound

- **Harder than CMN transcription** — automatic transcription from sound to symbolic notation is more challenging without a standard notational framework; spectrum analysis (time-frequency plotting) is the usual starting point
- **Early systems** — Haus's pioneering *EMPS* (1983) transcribed synthesized music into a reading score, with registers as distinct symbols and amplitudes as histograms, similar to the transcription of Ligeti's *Artikulation* (1970) — a model cited for several editors in the chapter
- **MIR study and ground truth** — Klien, Grill, and Flexer applied *music information retrieval* (MIR) with *spectromorphology* descriptors; because there is no scientifically "correct" transcription (no ground truth) and machines lack semantic comprehension, fully automated transcription is impossible — MIR can aid a human analyst but more interactive-tool research is needed
- **Machine learning** — now leads progress; conceptually a short step from training on traditional music/CMN to training on electronic music and a new graphic/symbolic notation — which still must be invented
