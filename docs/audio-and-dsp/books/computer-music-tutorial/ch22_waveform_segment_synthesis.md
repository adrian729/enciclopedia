# Ch 22: Waveform Segment Synthesis

## Table of Contents

- [1. The Waveform Segment Approach](#1-the-waveform-segment-approach)
- [2. Waveform Interpolation](#2-waveform-interpolation)
- [3. SAWDUST and SSP](#3-sawdust-and-ssp)
- [4. Instruction Synthesis](#4-instruction-synthesis)

## 1. The Waveform Segment Approach

- **Waveform segment synthesis** — a family of experimental, computer-idiomatic methods that build sounds from individual amplitude points (samples) stitched into larger waveforms, sections, and whole pieces; motivated by conceptual/compositional aesthetics rather than acoustical theory
- **Time-domain construction** — sound is built from amplitude points, so frequency, spectrum, and rhythm are not explicit parameters but arise as by-products of compositional manipulation
- **Common trait** — these techniques readily produce rich, wide-bandwidth, raw, noisy sounds; the chapter covers four: *waveform interpolation*, *SAWDUST*, *SSP*, and *instruction synthesis*

## 2. Waveform Interpolation

- **Interpolation** — generating a line between two *breakpoints* (each an x-y pair). Algorithms include *constant* (horizontal line), *linear* (straight connector), *exponential*, *logarithmic*, *half-cosine* (two inflection points for smoothness), and *polynomial* (cubic splines, Chebychev)
- **Uses in synthesis systems** — found in interpolating oscillators (improving signal-to-noise ratio vs. non-interpolating), in envelope generators (connecting breakpoint pairs, more memory-efficient than storing every point), and in Music \( N \) ITP unit generators that crossfade between two waveforms via a weight envelope
- **GEN functions** — Music \( N \) table-generation functions (line-segment, exponential, cubic spline, Chebychev) interpolate between composer-specified breakpoints to build envelopes and waveforms
- **Interpolation synthesis** — Bernstein and Cooper (1976) synthesized one period from \( n \) equally spaced breakpoints; linear interpolation's sharp angles create harsh, uncontrollable high-frequency partials, and constant interpolation (all right angles, like Walsh-function synthesis but skipping the weighted sums, so potentially more efficient) suffers from the same uncontrollable higher partials
- **Half-cosine and polynomial (Mitsuhashi 1982a)** — half-cosine avoids the high-partial problem and can control the harmonic mixture with fewer resources than additive synthesis; polynomial interpolation with uniform breakpoints is evaluated efficiently by the *forward differences* method
- **Breakpoint control of spectrum** — for \( n \) breakpoints per period, the amplitudes of \( n/2 \) harmonics can be controlled by varying breakpoint ordinates (20 breakpoints → harmonics 0–10); linear ordinate changes yield linear harmonic-amplitude changes, enabling time-varying spectra. *Nonuniform* breakpoints placed at points of greatest change approximate a waveform better, lowering distortion
- **Fractal interpolation synthesis (FIS)** — Gordon Monro (1995): generate functions through a point set, then iteratively superimpose the previous waveform on each point (scaled by a positive/negative displacement \( d \)) for fractal self-similarity. More iterations add high-frequency content; plucked sounds come from a high initial \( d \) reduced after attack; small displacements and frequency-tailored iteration counts limit aliasing

## 3. SAWDUST and SSP

- **SAWDUST** — Herbert Brün's system (University of Illinois): the *saw* is the computer and the *dust* is the data, minuscule amplitude points he calls *elements*; an interactive environment combining elements hierarchically into waveforms, sections, and complete compositions, yielding raw jagged-edged signals
- **SAWDUST operations** — `LINK` orders unordered elements into a *link*; `MINGLE` cycles/repeats a collection \( n \) times (e.g. `MINGLE(2, L3, L4)` = {L3, L4, L3, L4}) to make periodic waveforms; `MERGE` interleaves elements from two links; `VARY` transforms an initial link into a final link over a duration via a composer-specified polynomial degree
- **SSP** — G. M. Koenig's system (implemented by Paul Berg, Institute of Sonology, Utrecht, late 1970s); rooted in serial/postserial *selection principles* from Koenig's Project 1 and Project 2 rather than signal-processing theory. *Elements* are time-amplitude points (samples) joined by linear interpolation; *segments* are waveforms built from operations on elements
- **SSP selection principles** — the composer builds time- and amplitude-point databases, then combines them:

| Principle | Arguments | Behavior |
|---|---|---|
| Alea | A, Z, N | N random numbers chosen between A and Z |
| Series | A, Z, N | N values drawn without replacement; pool refills when empty |
| Ratio | Factors; A, Z, N | N values chosen, occurrence weighted by a probability list (Factors) |
| Tendency | N, M; A1,A2; Z1,Z2… | N values per M tendency masks, between initial (A1,A2) and final (Z1,Z2) boundaries |
| Sequence | Count, Chunks | Directly specify a sequence; Count elements with values in Chunks |
| Group | A, Z, N, Type, LA, LZ | Random value(s) between A and Z form a group of size randomly chosen between LA and LZ |

- **Shared traits** — both SAWDUST and SSP suit direct synthesis through a DAC on a small computer and tend toward raw, spectrally rich waveforms derived from no standard acoustical model

## 4. Instruction Synthesis

- **Instruction synthesis** — a conceptual approach specifying sound *only* in terms of logical computer instructions (addition, subtraction, AND, OR, loop, delay, branch) operating on binary data treated as samples sent to a DAC; the conceptual opposite of synthesis-by-rule / physical modeling, and efficient enough to run in real time on inexpensive computers
- **Virtual-machine assemblers** — most work came from associates of the Institute of Sonology; one category is an *assembler* for a *virtual machine* (a simulated abstract computer with its own instruction set). The composer writes a long program that generates the individual samples, so the program *is* the score
- **PILE (Paul Berg)** — the canonical example, built on Berg's belief that fast numeric/symbolic manipulation is "the idiom of the computer." Its instruction set includes `RANDOM`, `INCR`, `SELECT`, and `CONVERT` (send a sample to the DAC); random variables make results unpredictable in advance, biasing the language toward trial-and-error improvisation (though Berg proved tight control by realizing a popular song)
- **Holtzman's system (1979)** — a higher-level program generator producing short synthesis programs, with the composer specifying their execution order; because outputs are unpredictable, the instruction-synthesis composer works in a fast trial-and-error mode, generating many candidates per session and selecting the most useful
