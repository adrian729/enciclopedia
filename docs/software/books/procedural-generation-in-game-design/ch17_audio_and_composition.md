# Ch 17: Audio and Composition

## Table of Contents

- [1. Skipping Stones and the Two Components](#1-skipping-stones-and-the-two-components)
- [2. Procedural Audio: Sampling, Pitch, Implementation](#2-procedural-audio-sampling-pitch-implementation)
- [3. Procedural Composition: Beat, Scale, Steps, Chords, Motif](#3-procedural-composition-beat-scale-steps-chords-motif)
- [4. Closing Lessons](#4-closing-lessons)

## 1. Skipping Stones and the Two Components

- **Skipping Stones** — an experiential game where the player throws beach rocks over water and each bounce generates music. The chapter uses it as the running case study.
- **Two components of a procedural audio system** — *producing sound* (procedural audio) and *composing* (procedural composition).

## 2. Procedural Audio: Sampling, Pitch, Implementation

### 2.1. Sampling

- **Sample-based synthesis** — record audio from real instruments first and use those recordings as the basis for all in-game audio. Alternative: in-engine synthesis, which demands deeper audio-programming knowledge and strains the CPU.
- **Sampler** — plays back short audio files while modulating them. Even the most basic sampler — playing one sample at different speeds (which also shifts pitch) — is enough to start a procedural audio system.

### 2.2. Pitch

- **Twelve notes** — Western music has 12 notes (C, C#, D, D#, E, F, F#, G, G#, A, A#, B), repeated across roughly 11 octaves. Note names are arbitrary labels; octaves indicate how high or low a note is (A4 is one octave above A3).
- **Note as frequency** — every note is a sound wave at a specific frequency (A4 = 440 Hz). Each note maps to a fixed frequency; the chapter includes a lookup table of note frequencies by name and octave.
- **Constant ratio between neighbors** — the ratio between any note and its neighbor is the same, and so is the ratio between any note and its *n*-th neighbor. Multiplying a note's pitch by that fixed ratio lands squarely on a neighbor — the key to sample-based synthesis.
- **Stretch limits** — a basic sampler shifts pitch by changing playback speed. Stretching too far sounds terrible (typically no more than a couple of octaves); wider ranges use multiple samples (e.g., one per every other octave).

### 2.3. Implementation in Skipping Stones

- **One C sample per instrument** — most instruments are just basic samplers loaded with a C note (usually C3). Pitch is then modified to play any other note.
- **Unity pitch as float** — pitch 1 = normal speed, 0.5 = half speed, 2 = double speed. A precomputed pitch lookup table is built by repeatedly multiplying by the constant note ratio (e.g., 1.059463 → C#, 1.122462 → D, …).
- **Cross-instrument consistency** — because every instrument is loaded with a C sample, the same pitch value across instruments produces the same note.

## 3. Procedural Composition: Beat, Scale, Steps, Chords, Motif

### 3.1. Approach

- **Music theory as software** — encode music-theory principles into the composer, then add randomly triggered or statistically driven rules to mimic a chosen composer's style. Music theory is treated as guiding principles for "sounding good," not science.

### 3.2. Beat

- **Metronome system** — Skipping Stones bounces are physically driven, so without timing fixes the music sounded "more like a cat walking across a piano than actual music." When a stone hits the water, it submits an event to an internal metronome, which schedules audio playback on the next appropriate beat.
- **Sub-beat resolution** — the metronome tracks half, quarter, eighth, and sixteenth beats by doubling BPM per division (180 BPM half-beats = 90 BPM whole-beats).
- **InvokeRepeating, not coroutines** — `InvokeRepeating("ProcessAudioSources", 60/bpm, 60/bpm)` schedules a tick per beat. Using Unity coroutines with `WaitForSeconds()` drifts off beat over time. `ProcessAudioSources` plays queued audio and applies volume/pitch/filter on the next available source.
- **Note length via envelope** — note duration was usually controlled by sample length, but adding a simple envelope (lowering volume over a number of beats and stopping at zero) gives procedural control over whole/half/quarter notes.

### 3.3. Scale

- **Scale** — tells you which of the 12 notes are "allowed" in a piece. Most Western scales are variations on the major scale.
- **Major scale = 7 notes from a root** — the root is the first note, chosen by the designer or algorithm; the rest follow from a step pattern.
- **Mood via scale choice** — major sounds happy; Skipping Stones aims for moody atmosphere and uses the minor scale primarily. The root is picked at game start and changes with time of day; changing it often risks musical incoherence.

### 3.4. Steps

- **Half step vs. whole step** — a half step moves one note forward (E → F); a whole step moves two (E → F#).
- **Major scale step pattern** — `whole, whole, half, whole, whole, whole, half`. Starting from E gives `E F# G# A B C# D# E` — the E major scale.
- **Encoded as int arrays**:
  ```
  int[] Major          = {2, 2, 1, 2, 2, 2, 1};
  int[] Minor          = {2, 1, 2, 2, 1, 2, 2};
  int[] PentatonicMajor= {2, 2, 3, 2, 3};
  ```
  Cross-reference with the pitch table and chosen root to build the playable note array.
- **State-machine traversal** — purely sequential traversal sounds like piano practice. The composer uses a state-machine-like walk that starts on the root and moves no more than a few scale steps, with momentum: an upward run keeps going up briefly before reversing.
- **Tension and release** — some scale notes create tension, others release it; jumping randomly is unwise. A useful rule: after the 4th or 7th note of the major scale (most tension), follow with the root (most release). The pentatonic major scale (major minus the 4th and 7th) sounds good in any order but cannot build tension/release.

### 3.5. Chords

- **Chord** — notes that sound good played together; usually three notes, but not required.
- **Quick construction** — pick a chord root in the scale, take the note two scale-steps up, and the note two scale-steps up from there (so the 1st-3rd-5th, 2nd-4th-6th, or 3rd-5th-7th of the scale).
- **Mood from scale interval** — within the major scale, the 1-3-5 chord is a major chord (uplifting); the 2-4-6 chord is minor (moodier).
- **Inversions** — a chord's root need not be the lowest note. C major (C3-E3-G3) can be played E2-G2-C3 (first inversion) or G2-C3-E3 (second inversion); same notes, subtle change in sound.

### 3.6. Motif and Repetition

- **Bar redefined** — Skipping Stones can't assume continuous music, so each *stone thrown* is treated as one bar, and four bars form a section.
- **Motif** — a short melody repeated through a piece. Skipping Stones records the first throw's note sequence as the section's motif, then on throw 2 inserts notes from the motif among new notes; throw 3 generates fresh notes ignoring the motif; throw 4 repeats the motif with some notes replaced by chords using each note as a root.
- **Sink notes resolve the bar** — when a stone sinks the system plays the 2nd, 5th, or 7th scale note (tension); on the *final* stone of a section it plays the root (release), so each four-throw section builds and resolves like a musical idea.
- **Variety flourishes** — to avoid predictability, the composer randomly inserts a quick **arpeggio** (chord notes played in sequence) on the first skip of a stone, plus occasional well-placed chords substituted for single notes.
- **Accompanying instruments** — each time of day has a primary "lead" instrument and a dreamier accompanying instrument (more reverb, slow release). The player actually throws *two* stones at once: the first drives the primary instrument and musical structure; the second drives the accompaniment, which shares the key, sometimes echoes the motif or plays arpeggios, and is otherwise free.

## 4. Closing Lessons

- **Every addition compounds** — each rule added to the composer made an outsized difference in music quality; deeper music-theory study unlocks substantially better procedural composers. Recommended reading: Reed's *Improvise for Real* and DeSantis's *Making Music*.
- **Authored + algorithmic must collaborate** — Skipping Stones' beauty came not just from the procedural composer but from instruments crafted by a human composer to work *within* the engine. Procedural game audio requires a balance between authored and algorithmic elements.
