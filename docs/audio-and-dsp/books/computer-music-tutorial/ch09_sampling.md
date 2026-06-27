# Ch 9: Sampling

## Table of Contents

- [1. What Sampling Is and Where It Came From](#1-what-sampling-is-and-where-it-came-from)
- [2. Looping](#2-looping)
- [3. Pitch Shifting and Resampling](#3-pitch-shifting-and-resampling)
- [4. Sample Libraries and Instrument Emulation](#4-sample-libraries-and-instrument-emulation)
- [5. Modeling Note-to-Note Transitions](#5-modeling-note-to-note-transitions)

## 1. What Sampling Is and Where It Came From

- **Sampling (instrument sense)** — making a digital recording of a short sound object (e.g. a one-bar drum pattern) and triggering it via a MIDI note; all samplers play back prerecorded sounds shifted to a desired pitch. Distinct from chapter 3's sampling *theory* (the term derives from those digital *samples* and *sampling rate*)
- **Versus fixed-waveform synthesis** — instead of scanning a small wavetable of one waveform cycle (chapter 6), a sampler scans a large wavetable holding thousands of cycles — usually a second or more of recorded sound — so the waveform changes over attack/sustain/decay, yielding a rich, time-varying tone
- **Musique concrète** — Pierre Schaeffer founded the Studio de Musique Concrète in Paris (1950) and with Pierre Henry used tape to manipulate *concrète* (microphone-recorded) sounds rather than synthetic tones; he coined the *sound object*, any usable sound roughly between one-tenth of a second and eight seconds
- **Predigital samplers** — photoelectric/tape instruments matched a stored sound to the key pressed: the Light-Tone Organ and Singing Keyboard (1936), Phonogène (1953), Chamberlin (1956), and the famous Mellotron (1963), an expensive tape-strip instrument used by the Beatles and Moody Blues but mechanically temperamental
- **Digital samplers** — the Fairlight CMI (1979, Australia) was the first commercial keyboard sampler: 8 bits/sample, over $25,000; the E-mu Emulator (1981) offered 8-bit monophonic sampling for $9,000 with \~10 seconds of sample memory (128 Kbytes)
- **Three design issues** — building a commercial sampler requires solving *looping*, *pitch shifting*, and *data reduction*

## 2. Looping

- **Looping** — sustains a held key by reading repeatedly between specified *loop points* in the recorded sound: play the attack, repeat the looped middle until release, then play the final decay portion
- **Loop placement** — a seamless loop should begin after the attack and end before the decay (the sustained portion); too short a loop (one or two periods of a violin) negates the time-varying qualities and sounds sterile, like fixed-waveform synthesis
- **Automatic loop-point finding** — *pitch detection* searches for repeating patterns to estimate the *pitch period* (the time of one cycle), then suggests loop points spanning whole pitch periods
- **Joining loop ends** — a *splice* is a direct cut (causes a click/pop unless endpoints match at a common zero point); a *crossfade* fades the loop's end out while fading its beginning in, repeating per cycle (typically 10–100 ms)
- **Smoothing variations** — *bidirectional looping* alternates forward and backward playback; forward and backward loops can be layered to mask discontinuities; spectrum-analysis methods can randomize each component's phase and resynthesize

## 3. Pitch Shifting and Resampling

- **Why shift** — cheap samplers store only every third or fourth semitone and derive intermediate notes by shifting a nearby stored note; a side effect is that duration also changes, which looping the sustain compensates for. Both methods below are *time-domain* (distinct from the frequency-domain methods of chapter 31)
- **Method 1 — vary the DAC clock** — changing the output DAC's clock frequency changes the playback sampling rate, shifting pitch; used in the original Emulator. It needed a separate variable-rate DAC and filter per voice over impractically wide ranges (shifting a 250 Hz tone sampled at 44.1 kHz up six octaves demands a 2.82 MHz clock), so transposition was severely limited
- **Method 2 — sample-rate conversion (resampling)** — resamples in the digital domain with a constant output sampling rate; today's standard. *Decimation* (*downsampling*) skips samples to raise pitch (read every third sample = up three octaves); *interpolation* (*upsampling*) inserts intermediate samples to lower pitch
- **Direction confusion** — method 1 raises pitch by *increasing* the playback rate; method 2 raises pitch by *decreasing* the resampling rate (decimation) even though the playback rate is constant
- **Arbitrary ratios** — to shift by a ratio \( N/M \), interpolate by \( M \) then decimate by \( N \) (e.g. down a perfect fourth = interpolate by 4, decimate by 3)
- **Rate conversion without pitch change** — converting between 44.1 and 48 kHz uses staged interpolations/decimations by factors of 2, 3, 5, and 7; works whenever the rate ratio is a simple fraction. Variable resampling enables *flanging* and audio *scrubbing* (simulating rocking tape across a head)
- **Resampling problems** — finite numerical precision adds noise across stages; decimation throws away intermediate samples leaving jagged discontinuities and shifts frequencies up, causing *aliasing*. Lowpass filtering after decimation smooths the waveform; interpolation likewise needs filtering because simple linear interpolation creates aliased components

## 4. Sample Libraries and Instrument Emulation

- **Sample quality depends on recording** — good samples need good players, instruments, microphones, and rooms, so most users buy professionally prepared *sample libraries* or share amateur ones (e.g. freesound.org)
- **Formats** — proprietary (East-West's PLAY engine) or standard (24-bit .wav, Apple Loops) loaded into players like Kontakt, Logic Pro, Reason, HALion; royalty-free open formats include SoundFonts and SFZ; Translator converts between formats
- **Wavetable libraries** — collections of thousands of single-cycle waveforms used as expansion packs for wavetable synths (Absynth, Alchemy, MetaSynth); Galbanum Architecture Waveforms offers over 25,000 waveforms
- **Emulation limits** — the "symphony orchestra in a box" remains elusive; sampled sound often has an artificial, frozen quality. Organs simulate well, but voices, strings, woodwinds, brass, and plucked instruments are hard — individual notes capture fine but stringing them into phrases reveals missing acoustic and performance information
- **Generic samples** — factory samples model the generic player/hall, so a sampler can't reproduce the signature style of a Coltrane solo; raising realism requires understanding the relationship between sound structure and musical performance (contextual cues plus breathing, tonguing, key clicks, finger slides, and effects like rubato, legato, portamento, vibrato)

## 5. Modeling Note-to-Note Transitions

- **Strawn's research** — John Strawn's Stanford doctoral work (1985) analyzed transitions in nine nonpercussive orchestral instruments; *tonguing* (interrupting the windstream as if saying *t* or *k*) produces strong transitional cues, while smooth transitions may dip as little as 10 dB between notes
- **Coarticulation** — the speech analogue: a phoneme's pronunciation depends on neighbors (the *n* in *tenth* is dental, the *n* in *now* is not); the same context-dependence applies to musical notes
- **Diphone / concatenative synthesis** — *diphone synthesis* models speech as stable sounds separated by transition sounds (used by Alexa, Siri); generalized to music, one builds dictionaries of stable and transition sounds (e.g. for bowed cello) — today called *concatenative synthesis*
- **Brute-force and controller-switched transitions** — capture every possible note-to-note transition as a sample and trigger the right one; Yamaha and Roland *expressive samplers* implement *controller-switched transitions* based on which notes follow which (the Yamaha MOTIF XF combines sampling, physical modeling, and real-time keyboard analysis for strumming, string slides, fret noise, etc.)
- **Phrase-level approaches** — NotePerformer analyzes a score to add articulations (mutes, pizzicato, staccato, tremolo) for notation programs like Sibelius and Dorico; Sonokinetic libraries play back entire prerecorded orchestral phrases so transitions are already baked in
