# Ch 39: Spectrum Analysis by Atomic Decomposition

## Table of Contents

- [1. Fundamentals of Atomic Decomposition](#1-fundamentals-of-atomic-decomposition)
- [2. Bases, Dictionaries, and Sparsity](#2-bases-dictionaries-and-sparsity)
- [3. Decomposition Methods](#3-decomposition-methods)
- [4. Applications: Analysis, Visualization, Synthesis](#4-applications-analysis-visualization-synthesis)

## 1. Fundamentals of Atomic Decomposition

- **Atomic decomposition** — the analytical dual of *granular synthesis*: just as Fourier analysis builds a sound from sinusoids, this builds it from grains called *atoms*. (Chapter authored by Bob L. T. Sturm)
- **Approximation theory** — because computers have finite memory and precision, they cannot represent real signals exactly; approximation theory provides methods and guarantees for *decomposing* a signal into a finite number of functions. Fourier analysis, for instance, exactly needs an infinite sum of sinusoids but must be truncated to \( N \) sinusoids, and the theory tells which \( N \) to keep for a desired precision
- **A spectrum of decompositions** — sinusoids that exist for all time (Fourier), time-localized sinusoids of finite duration (STFT), single impulses (uniform time-domain sampling, of which the Nyquist theorem is an outcome), and wavelets are all different ways to decompose the same signal

## 2. Bases, Dictionaries, and Sparsity

- **Basis** — a collection of functions in which any signal in the spanned space has *one unique* sum representation. The *Fourier basis* is all complex sinusoids; the discrete *sine basis* is \( N \) length-\( N \) sinusoids (leading to the DFT/FFT); the *Kronecker delta* (spike/impulse) basis is the \( N \) sequences that are all zeros but a single 1
- **Dictionary** — combining several bases (e.g. sine + spike) into a larger collection; each element is an *atom*, and decomposing a signal over a dictionary is *atomic decomposition*. A basis is *complete*; a dictionary with more atoms than needed is *overcomplete* and yields an infinite number of possible decompositions
- **Why combine bases** — the sine basis reveals *frequency content* but no *spike content*, and the spike basis reveals the reverse; a signal with both sine-like and spike-like structures is better described over a combined dictionary, at the cost of losing the uniqueness a single basis provides. Mallat's metaphor: more atoms enrich the *vocabulary* for describing a signal
- **Sparsity** — one measure of the "best" decomposition: fewer selected atoms is better. Sparsity appears natural — evidence suggests the mammalian auditory system itself operates on sparsity principles (Lewicki; Smith and Lewicki)
- **Approximation error** — the second measure of "best": how close the approximation is to the original. Sparsity and error are at odds — an accurate approximation may need many atoms, while a very sparse one may accept large error — and managing this trade-off motivates the various algorithms

## 3. Decomposition Methods

- **Greedy decomposition** — iteratively builds the model: at each step find the optimal atom, add it, subtract it from the *residual* (starting from the original signal), and repeat until a set number of atoms or a residual-energy threshold is reached. Computationally simple but can fail to find ideal solutions
- **Matching pursuit** — the most basic greedy algorithm (Mallat and Zhang 1993); defines the *optimal* atom as the one most correlated with the residual. Variants include *orthogonal matching pursuit*, *orthogonal least squares*, *psychoacoustic-adaptive matching pursuit*, and *cyclic matching pursuit* (better decompositions, higher cost); *gradient pursuit* and *stochastic atom selection* reduce cost
- **Prior-knowledge greedy methods** — *harmonic matching pursuit* uses harmonic-content atoms, *molecular matching pursuit* (Daudet) builds "molecules" modeling tonal vs transient structures, and *stereo matching pursuit* exploits cross-channel correspondence
- **Greedy strengths and weaknesses** — dictionaries can hold billions of atoms (the free Matching Pursuit Toolkit decomposes audio over user-defined dictionaries); but greedy methods ignore the global solution, so a poorly chosen atom forces extra "correction" atoms that model nothing real (*dark energy*)
- **Optimization** — poses decomposition as minimizing a function subject to constraints, balancing sparsity and error directly; more computationally complex but can be more sparse and precise than greedy. Exact sparsity is infeasible, so it is relaxed using the *solution l1-norm* (sum of selected atoms' magnitudes)
- **Basis pursuit denoising** — minimizing residual squared error subject to an l1-norm constraint (Chen, Donoho, Saunders 1998); independently known in statistics as *LASSO* (least absolute shrinkage and selection operator, Tibshirani 1996). Solved by interior-point or simplex methods that *scale down* a solution rather than build it up; rarely used with billion-atom dictionaries because cost grows with dictionary size

## 4. Applications: Analysis, Visualization, Synthesis

- **Sound modeling and coding** — greedy decomposition over an eight-times overcomplete MDCT dictionary gives better fidelity than standard compression at very low bit rates (Ravelli et al.); used for perceptual audio coding. Higher-level content can be modeled: tonal/transient structures (molecular matching pursuit), instrument-specific harmonic-atom dictionaries enabling transcription (Leveau et al.), and feature extraction for indexing/retrieval
- **Dictionary learning** — sparse approximation can *learn* a dictionary from music whose atoms map to note-like, instrument-specific content (piano, guitar, vocals) with no musicological input — independently arriving at notes, timings, and dynamics, useful for source separation and transcription
- **Gabor atom** — a time-localized sinusoid, equivalently a time-shifted, modulated Gaussian window; Dennis Gabor (1947) called it an "acoustic quanta" because its energy is maximally concentrated in time and frequency. The STFT is the magnitudes of a signal projected onto a single-duration Gabor dictionary
- **Spikegram** — a visualization placing a dot in the time-frequency plane for each atom (each centered at a time and frequency), marking precise event onsets; demonstrated on Curtis Roads's *Pictor Alpha* with a dictionary of over five million Gabor atoms (lengths 4 to 1,024 samples)
- **Wivigram** — summing the *Wigner-Ville distributions* of the selected atoms (Mallat and Zhang; Sturm et al. 2009); its superior time-frequency resolution gives greater clarity than projecting onto an STFT dictionary, and it can serve as an interface (e.g. the SCATTER application) to select, delete, and modify atoms — selecting short atoms edits transients, long atoms edit tonal content
- **Synthesis and denoising** — since sparse approximation is regression, *noise* can be defined as structures unlike any dictionary atom, making denoising natural (Gabor-atom denoising of speech); also declipping and corruption repair
- **Parametric manipulation** — because atomic decomposition is granular synthesis in reverse, atoms parameterized by scale, frequency, and time shift enable *atomic filtering* (removing short-scale atoms strips transients), *sonic coalescence*/*disintegration* (raising/lowering atom density), pitch-shifting, time-stretching, *jitter* (random time shifts), *bleed* (increased scales), and dictionary substitution/morphing. Transforming atoms can break the fragile relationships a decomposition added to correct its mistakes, making *dark energy* audible
- **Advanced topics** — open problems are how to *choose* and how to *learn* a dictionary (Aharon, Elad, Bruckstein give a general overcomplete-learning algorithm); best choice depends on objectives. These methods are far more intensive than Fourier analysis, but real-time is nearing (the Matching Pursuit Toolkit runs at four times real time, latency depending on how strongly the signal relates to the dictionary's atoms)
