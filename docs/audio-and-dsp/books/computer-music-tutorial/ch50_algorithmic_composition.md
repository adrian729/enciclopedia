# Ch 50: Algorithmic Composition

## Table of Contents

- [1. Foundations of Algorithmic Composition](#1-foundations-of-algorithmic-composition)
- [2. Historical Precursors and Machinery](#2-historical-precursors-and-machinery)
- [3. Pioneers and Four Composition Programs](#3-pioneers-and-four-composition-programs)
- [4. Strategies for Algorithmic Composition](#4-strategies-for-algorithmic-composition)
- [5. Aesthetic and Philosophical Issues](#5-aesthetic-and-philosophical-issues)
- [6. Assessment](#6-assessment)

## 1. Foundations of Algorithmic Composition

- **Formal composition algorithm** — a generative engine for music creation; many musical processes can be *formalized* into symbolic representation, so a computer becomes a vehicle for musical ideas (Hiller and Isaacson 1959). Wolfram: any system's rules correspond to a program and its behavior to a computation
- **Four forms of compositional algorithm** — interactive command languages (including live coding), musical extensions to programming languages, modular patching environments, and self-contained automated composition apps (this chapter focuses on the last)
- **Style imitation excluded** — to focus on original composition, the chapter sets aside systems that imitate known styles (Bach chorales, Palestrina, Mozart, species counterpoint, 12-tone, jazz improvisation, EDM)
- **Machine learning (ML)** — much recent work uses ML: OpenAI's MuseNet, Google's WaveNet (sounded like spliced classical clips, reminiscent of a high-order *Markov chain* with local coherence but meandering phrases), and *attention models* that reference past output for long-term structure (Music Transformer)
- **Commercial automation** — rule-based *style template* apps (Band in a Box, Orb Composer) code each style as a rule set; phrase-based sample libraries (Sonokinetic) mix precomposed orchestral phrases; an AI-services industry (Flow Machines, IBM Watson Beat, OpenAI's Jukebox, Amper Music) generates generic pop, a descendant of 1920s Muzak

## 2. Historical Precursors and Machinery

- **Ancient formal processes** — Guido d'Arezzo (\~1026) mapped vowels to pitches; Dufay (1400–1474) derived tempi from cathedral proportions and used the *golden section* (1:1.618) plus *inversion* and *retrograde*; Machaut's *isorhythmic* motets inserted a recurring rhythmic pattern across melodic layers
- **Dice games** — Mozart's *Musikalisches Würfelspiel* assembled minuets from prewritten measures via dice throws (chance, still common today); commercial card systems followed — the Kaleidacousticon (1822, \~214 million waltzes) and the Quadrille Melodist (1865, \~428 million quadrilles)
- **20th-century mathematics** — serial and stochastic strategies manipulate elements via set theory or probabilistic processes (Babbitt, Xenakis); virtually any data set or formula can become a music generator (Schillinger)
- **Pre-computer machines** — Kirchner's Arca Musirithmica (1660), Winkel's room-sized Componium (1821), and Olson and Belar's electromechanical composing machine (\~1951), whose innovation was automating a probabilistic system using asynchronous bistable multivibrators to generate random digits
- **Sequence-control hybrids** — one-off systems coupled composition logic with sequenced performance: the RCA Mark I/II (used by Milton Babbitt), the Barr and Stroud Solidac (1959, billions of Haydn-like trios), Raymond Scott's knob-and-switch Electronium (early 1960s; "not played; it is guided"), Chadabe's CEMS (Moog modules), and Martirano's Sal-Mar Construction (1971, performed live)

## 3. Pioneers and Four Composition Programs

- **Lejaren Hiller** — laid the groundwork of modern computer music; with Isaacson created the first computer-composed work, the *Illiac Suite for String Quartet* (1956), on the room-sized ILLIAC I (1,024 words of memory), coding in binary machine language; later *HPSCHD* with John Cage
- **Other pioneers** — Brün, Myhill, Tenney, Barbaud, Phillipot, Xenakis (whose hand-computed stochastic *Metastasis* premiered 1955), and Koenig; commercially, *Push-Button Bertha* (1956, Burroughs Datatron) flopped; Zaripov recomposed folk music on Soviet URAL computers
- **Stochastic Music Program (SMP)** — Iannis Xenakis; uses stochastic formulas originally describing gas particles, modeling a composition as *clouds of sound* (particles = notes). The composer stipulates global attributes (section duration, note density, *timbre classes*, per-instrument play probabilities) and runs the program; used for *Eonta* (1964)
- **Project 1** — G. M. Koenig (Institute of Sonology, Utrecht, 1970); applies seven *selection principles* — ranging from completely random to completely deterministic, with an intermediate "selection without replacement" — to five *parameters* (instrument, rhythm, harmony, register, dynamics), generating seven structures as a note list. Embodies "Serial music, Cologne style"; rewritten in SuperCollider
- **POD** — Barry Truax's Poisson-distribution programs, built for direct digital synthesis; replaces the *note concept* with *sound objects*, distributing events within *tendency masks* (frequency-vs-time regions) per a composer-set *event density*. PODX added real-time interaction (works *Arras*, *Wave Edge*)
- **AUTOBUSK** — Clarence Barlow's real-time program (MIDI output); applies probabilistic methods to four formalized concepts: *harmonicity* (intervallic stability for any octave division), *metricity* (rhythmic-stream variation), *tonicality* (closeness to a tonality), and *eventfulness* (note density). Theories presented in *On Musiquantics* (2012)

## 4. Strategies for Algorithmic Composition

- **Borrowed models** — algorithms import concepts from biology, mathematics, engineering, computer science, linguistics (formal grammars), and machine learning; *data sonification* maps arbitrary data sets (chess moves, skylines, brain waves) to sonic parameters, directly or via complex mappings
- **Common strategies (Table 50.1)**:

| Strategy | What it is |
|---|---|
| Set/group theory, combinatorics | Permutations, rotations, partitions, series operations (invert, transpose, reverse), sampling without replacement |
| Linked automata / transition networks | Finite-state automata in graphs; inputs trigger rule-based state transitions |
| Cellular automata | Like linked automata but every cell is identical and the interconnection lattice is fixed; complex behavior self-organizes from local interaction |
| Stochastic processes / Markov chains | Use probability distributions; in a Markov chain the next event's probability is conditional on previous events |
| Fractal processes | Rules generating self-similar nested patterns |
| Chaotic systems | Deterministic algorithms swinging between stable and turbulent states across nonlinear thresholds |
| Genetic algorithms / artificial life | Imitate natural selection: a random population is evaluated for *fitness* and bred until a termination condition |
| Translational methods | Translate a nonmusical medium into sound (data sonification), rule-based or stochastic (Schillinger's skyline mappings) |
| Grammars / Lindenmeyer systems | Rules that rewrite strings per a predefined grammar |
| Generate-and-test / constrained search | Generate a random value, test it, output if it passes else retry |
| Process models | Model control flow; transitions *fire* on a state condition (Petri nets) |
| Pattern matching and search | Find database symbols matching a composer's general pattern |
| Constraints | A network of devices on wires propagating locally computed values, giving multiple viewpoints |
| Expert systems | A knowledge base of facts and rules reasoning by inference, or brute-force search |
| Machine learning / neural networks | Many identical interconnected elements detect patterns after training on thousands of examples |
| MIR-based | Extract audio features, then navigate a database for similar/dissimilar material |

- **Combining strategies** — methods are listed separately for teaching but combine in practice (one algorithm for microstructure, another for macrostructure; one for the beginning, another for the end)

## 5. Aesthetic and Philosophical Issues

- **Aesthetic motivations** — generative methods let composers "reach beyond themselves" (Berg), exploring novel processes; they are driven by romantic ideals (growth, evolution) and rewarded by institutions, and they grant control over domains impossible to manage manually (Chowning's *Stria*, built on golden-mean carrier:modulator ratios)
- **Deterministic vs stochastic** — *deterministic* procedures generate notes by a fixed task from seed data (e.g. rule-based chorale harmonization, Barlow's dynamics formulas, Ames's constrained-search counterpoint); *stochastic* procedures integrate random choice weighted by probability tables, guaranteeing trends while keeping local detail unpredictable. Apart from simple cases, listening cannot reveal which was used — many algorithms are perceptually opaque
- **Total automation vs interaction** — feared replacement of composers never occurred; using someone else's program demands little creativity (extreme case: *found art*). Hiller and Barbaud held that output should never be hand-edited — only the program logic changed and rerun — whereas Xenakis freely rearranged SMP's raw output
- **Batch mode** — fully automated programs impose *batch* interaction: prepare input, execute, accept/reject the whole score, with no online editing — the unit of composition is an entire score
- **Interactive composition** — adding interaction gives access to different layers and time scales (POD, AUTOBUSK, Spiegel's Music Mouse were interactive); scope (parameter to whole strategy), degree (live performance to reflective studio work), and mode (manual control to live coding) are compositional choices, per Vaggione's formal/informal plurality
- **Heuristic algorithms** — narrative qualities (wit, irony, tension, surprise) resist formalization; a hybrid formal/informal approach pairs algorithmic power with *heuristics* (experience-based, context-dependent rules of thumb and inspired guesswork, per Chaitin), since an inspired rule violation at the right moment is sometimes correct

## 6. Assessment

- **Widespread tools** — algorithmic toolkits (Max, SuperCollider) and DAW features (Max for Live, Logic's MIDI Scripter, Reaper's MIDI tools) are common
- **Shift of attention** — algorithms process more data than a lone composer, letting the composer move from tiny details to higher-level formal architecture and process models
- **Limits in aesthetic domains** — computers excel at enumerating solutions and dominate rule-based games (AlphaZero at Go, Chess, Shogi), but their aesthetic decision-making is severely limited; ML can imitate any style, yet generating nonimitative original innovation — solving the aesthetic problems a piece poses to itself — remains the strong suit of human talent. Excessive complexity or virtuosity for its own sake is a tiresome musical diet
