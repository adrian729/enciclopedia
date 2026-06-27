# Ch 35: Rhythm Recognition and Automatic Transcription

## Table of Contents

- [1. The Rhythm Recognition Problem](#1-the-rhythm-recognition-problem)
- [2. Event Detection](#2-event-detection)
- [3. Separating Voices in Polyphonic Music](#3-separating-voices-in-polyphonic-music)
- [4. Automatic Transcription](#4-automatic-transcription)
- [5. Transcribing Rhythmic Structure](#5-transcribing-rhythmic-structure)

## 1. The Rhythm Recognition Problem

- **The task** — turn an input waveform into a list of sonic events, assign them note durations (half, quarter, etc.), then group them into beamed groups, tuplets, measures, and phrases while determining meter
- **Why it is hard** — human performance is imperfect and notation is ambiguous: the same rhythm can be notated many ways, so a recognizer must ignore "insignificant" variation (a slightly staccato whole note is not a tied half-quarter-eighth-sixteenth-thirty-second). Harder than sequencer *quantization* because the note list and (possibly varying) tempo are unknown at the outset
- **Three levels** — *low level* = event detection (raw acoustic signal segmented into start/end times); *middle level* = transcription into notation (note assignment and grouping, where MIDI data begins); *high level* = style/genre/mood analysis. The chapter covers the first two
- **Machine listening** — serves *music information retrieval (MIR)*, *audio content analysis*, or *semantic audio*: query-by-humming, tempo/beat tracking, meter estimation, un-mixing, structure segmentation ("Play the chorus"), and audio fingerprinting
- **Machine learning** — increasingly central; statistical algorithms trained on large labeled example sets (e.g. correlating triplet notation images with triplet audio spectrograms). Methods include nearest-neighbor classifiers, hidden Markov models, Bayesian networks, Gaussian mixture models, nonnegative matrix factorization, support vector machines, and deep neural networks

## 2. Event Detection

- **Amplitude thresholding** — for simple monophonic non-reverberant music, scan the waveform for attack transients exceeding an amplitude threshold; highpass preprocessing emphasizes *transients* (sharp onsets/decays)
- **Detection function** — a data-reduced set of event triggers: the *amplitude envelope* (rectify and lowpass-filter) or the *energy envelope* (square instead of rectify); its derivative spots sudden energy increases
- **Limits of amplitude cues** — slurred bowed attacks, notes blurred by sustain or reverberation, chords, and dynamic-range-compressed music defeat time-domain methods. A vibraphone with sustain pedal down gives no clear attack times — pitch and spectrum changes are then the best clue
- **Combining domains** — Puckette et al. (1998) found rapid spectral-envelope change a better percussive-attack indicator than power change. An *autoregression* (AR) model detects periodicity (pitch) changes and pairs well with amplitude thresholding (one frequency-sensitive, one amplitude-sensitive); large high-frequency energy in the STFT also flags transients

## 3. Separating Voices in Polyphonic Music

- **Source separation / cocktail party problem** — isolating one line from a polyphonic texture; tractable for a few instruments (Melodyne, Zynaptiq Stem Maker, Audionamix Xtrax Stems) but impossible beyond a complexity threshold (no one segments every note of an orchestral tutti)
- **Informed source separation** — exploiting a known score's pitch and timing; the common testbed without a score is vocals/drums/bass/guitar in popular music, where results are good
- **Separation strategies** — multi-band filtering by register; spatial location; matching *spectral templates* (known spectrum patterns); *source coherence criteria* / *common fate* (shared vibrato/tremolo); per-instrument attack patterns; leakage reduction across tracks; neural nets; and user-"painted" labels training an ML algorithm (the ISSE editor)
- **Spectral signatures** — organ/guitar/bass show stable harmonics (horizontal spectrogram lines); drums are transient broadband noise (vertical blocks); the voice mixes harmonic vowels and noisy consonants. Separation starts from time-frequency analysis, iteratively matching source models per \~100 ms frame
- **Neural-net training** — supervised, with mixed-audio spectrograms as input and desired-source spectrograms as targets; quantity and quality of training data matter (e.g. the Jamendo Corpus for sung vocals)

## 4. Automatic Transcription

- **Definition** — the middle level, beginning once a list of discrete events exists; subtasks are pulse induction, tempo tracking, rhythm-value assignment, note grouping, meter and measure-boundary determination, and phrase structure
- **Setup template** — practical notation software constrains the problem by having the user declare expectations in advance; given a good template, MIDI transcription works well. *Automatic transcription from audio* (Sibelius AutoScore, ScoreCloud, AnthemScore) is far harder and uses ML
- **Historical background** — clavier transcription dates to Engramelle's *La Tonotechnie* (1775) inscribing keystrokes as piano-roll notation; Unger and Hohlfeld built a harpsichord-attached system in 1752. J. A. Moorer's 1975 Stanford doctoral "musical scribe" was the first major application to musical sound — it faithfully reproduced a guitar mistuned a half-step high. *WABOT-2* (Waseda University, 1985) read notation, understood spoken Japanese song requests, and adjusted pitch and rhythm to accompany a singer

## 5. Transcribing Rhythmic Structure

- **Pulse induction and tempo tracking** — a *metrical level* (pulse) is the periodic recurrence of a feature; *pulse induction* highlights periodicities and *tempo tracking* finds the beat. Tempo is perceptual with no well-defined physical correlate, so methods are heuristic. The beat is usually a common denominator of measured event durations; syncopation must not be mistaken for tempo change
- **Memory window** — a short memory follows fast tempo changes but is unstable; a long memory steadies tempo but ignores fast changes. Mont-Reynaud's tracker runs two parallel strategies: extracting *phenomenal accents* (long-note onsets, loudness/timbre/harmony changes) as structural anchors, plus statistics on recurring durations. Scheirer (2000) showed beat can be extracted from subband temporal envelopes alone, without pitch data
- **Note duration assignment** — assign each event a metrically related duration, but expressive performance varies durations (staccato shrinks, *agogic accents* stretch). *Quantization* rounds to a grid, yet naive grids cause pathologies — a 64th-note grid can notate a triplet so note A is played shorter than B though notated longer
- **Grouping into patterns** — subdivide notes into rhythm patterns; Rosenthal (1988) applied five Lerdahl-Jackendoff-derived rules: (1) groups begin on accented notes; (2) no single-event groups; (3) short notes group with following long notes; (4) a boundary separates long from following short notes; (5) same-level groups should be as equal in duration as possible. These derive from written, not performed, music
- **Estimating meter** — meter is a ratio between the beat period and the larger measure period. Finding the *perceived meter* (divisible by integer \( n \) — duple, triple, etc.) suits listening models; estimating the *exact time signature* (2/4 vs. 4/4) needs musicological style knowledge since many signatures sound identical. Rosenthal (1992) used multiple specialized agents weighed by a manager
- **Recovery from confusion** — without a metronome reference and quantization range, recognition is imperfect; wild performances, ambiguity, low-amplitude passages, missed chord notes, and modernist scores cause errors. Maintaining multiple interpretations (Allen and Dannenberg 1990) makes complete confusion less likely
