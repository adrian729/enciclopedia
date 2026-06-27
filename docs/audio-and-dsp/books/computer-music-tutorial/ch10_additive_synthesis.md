# Ch 10: Additive Synthesis

## Table of Contents

- [1. Principle and History](#1-principle-and-history)
- [2. Fixed-Waveform Additive Synthesis](#2-fixed-waveform-additive-synthesis)
- [3. Time-Varying Additive Synthesis](#3-time-varying-additive-synthesis)
- [4. Analysis/Resynthesis](#4-analysisresynthesis)
- [5. Data Reduction Models](#5-data-reduction-models)
- [6. Machine Learning and Walsh Functions](#6-machine-learning-and-walsh-functions)

## 1. Principle and History

- **Additive synthesis** — building a complex audio signal by *summing elementary waveforms* (typically sine waves); one of the oldest synthesis techniques, rooted in the theory of Jean-Baptiste Joseph Fourier (1768–1830) that any complex waveform can be approximated as a sum of elementary waveforms
- **Strength and weakness** — slowly varying sinusoidal sounds are well modeled and simply described; modulations and noise textures are poorly modeled and need more complex analysis
- **Historical instruments** — the pipe organ realized additive sound through *register stops* (pulling several added the sound of several pipe sets); the Telharmonium (1906) summed dozens of electrical tone generators; the Hammond organ (1935–1972) was a pure additive instrument using electromechanical rotating tone-wheels
- **Why organs sound unrealistic** — they produce a *fixed waveform* that doesn't vary at the micro time scale; realistic simulation requires the sine-wave mixture to vary constantly over time

## 2. Fixed-Waveform Additive Synthesis

- **Harmonic addition** — the user adjusts the relative strengths of a set of *harmonics* (integer multiples of a fundamental; term coined by Sauveur, 1701) shown as a *histogram* / *spectrum template*; a digital oscillator sums them (e.g. odd harmonics with amplitudes 1, 1/3, 1/5, … through the 101st approximate a square wave)
- **The phase factor** — changing the starting phases of a fixed waveform's components is *inaudible* though it radically alters the waveform's visual shape; phase *does* matter for the perception of attacks, grains, and transients, and for reconstructing analyzed sounds
- **Addition of partials** — generalizing from harmonics to *partials* (any frequency component); an *inharmonic partial* is not an integer ratio of the fundamental. Fixed-waveform partial addition only approximates the *steady-state* portion of a tone — a constant spectrum is less compelling than a time-varying timbre

## 3. Time-Varying Additive Synthesis

- **Risset's discovery** — pioneer Jean-Claude Risset (1938–2016) analyzed instrumental tones and found that *variations in each harmonic's amplitude on a micro time scale* are the secret to a tone's identity; he composed *Inharmonique* (1977) exploring inharmonic sine waves
- **How it works** — vary the sine-wave mixture over time; a trumpet attack may need twelve sine waves, dropping to three or four after 300 ms. In digital implementation each oscillator's frequency and amplitude inputs are *time-varying envelope functions* rather than constants
- **Milestones** — early analog practice (Stockhausen, 1950s) needed two people adjusting oscillator balance in real time; David Wessel's *Antony* (1977) was first to use 256 time-varying oscillators
- **Demands** — voracious for computation (16 partials \(\times\) 24 simultaneous events \(\times\) 48 kHz \(\approx\) 18.4 million samples/second, now feasible on laptops or GPUs) and for control data (a 10,000-event score needs 160,000 frequency plus 160,000 amplitude envelopes)
- **Sources of control data** — (1) interactive GUI apps with *macros* mapping one knob to many partials (NI Razor: 320 partials; Air Loom: 512); (2) data imported/*sonified* from another domain (Dodge's *Earth's Magnetic Field*, 1970); (3) algorithmic composition programs; (4) manual specification from psychoacoustic knowledge; (5) output of an analysis subsystem (Wishart's *Vox-5*)

## 4. Analysis/Resynthesis

- **Three-step process** — (1) analyze a recorded sound, (2) modify the analysis data, (3) resynthesize the transformed sound; not exclusive to additive synthesis (can use subtractive or hybrid methods)
- **How additive resynthesis works** — the input is segmented into short overlapping *windowed* segments, each sent through a bank of narrow bandpass filters; in *oscillator bank resynthesis* each filter's measured amplitude becomes that frequency range's *amplitude control function*, and frequency deviations are derived from adjacent filters (*analysis bins*) — these envelopes then drive the resynthesis oscillators
- **Musical transformations** — editing the control functions enables variations, spectrum scaling vs. shifting (scaling breaks formants; small shifts preserve them), hybrid timbres, time stretch/shrink without pitch change, timbral interpolation (morphing), spectral filtering, and *cross-synthesis* (using one sound's envelopes to scale another's). Pioneering works: Harvey's *Mortuos Plango, Vivos Voco* (1981, boy/bell chorus), Murail's *Désintegrations* (1983, spectral composition), Carlos's *Digital Moonscapes* (1985)
- **Analysis methods** — variations on Fourier analysis: *pitch-synchronous*, the *phase vocoder* (PV), *constant-Q*, Bark-scale warping; the practical form is the *short-time Fourier transform* (STFT), built on the *fast Fourier transform* (FFT) (Cooley and Tukey, 1965). The PV converts a signal into time-varying frequency/amplitude curves, enabling time stretch/shrink without pitch change
- **Information explosion** — contrary to the inventors' coding goals, analysis data can occupy many times more memory than the original (a 2 Mbyte noise file can yield tens of Mbytes), mandating *data reduction*

## 5. Data Reduction Models

- **Goal** — compress amplitude/frequency control functions without losing perceptually salient features, ideally leaving the data editable by a composer
- **Line-segment approximation** — store only *breakpoint pairs* (time/amplitude points of maximum inflection) and interpolate straight lines between them on resynthesis; Grey achieved hundredfold reduction by hand; Beauchamp inferred all harmonic amplitude curves from the first harmonic's
- **Principal components analysis (PCA)** — decomposes a waveform via *covariance matrix* calculation into basic waveforms (principal components) plus weights; each successive component fits the *residual* left by the previous, so the fewest components capture the most variance
- **Spectral interpolation synthesis (SIS)** — crossfades between analyzed spectra in the *frequency* domain (unlike time-domain multiple wavetable crossfading), compressed into common spectral paths plus ramp functions
- **Spectral modeling synthesis (SMS)** — splits the sound into a *deterministic* component (prominent frequencies isolated by *peak detection* and *peak continuation*, resynthesized with sine waves) and a *stochastic* component (the *residual*, modeled as white noise through frequency-shaping filters); the two are transformable separately, so noisy parts stay noisy. Filtered pseudorandom noise gives large data reduction
- **ATS** — extends SMS with psychoacoustic processing: the *signal-to-mask ratio*, the 24-band *Bark scale* (perceptually equal *critical bands*), and analysis of whether a peak *masks* others; data-reduced to a few perceptually meaningful parameters (interface ATSH; implemented in Csound, SuperCollider, Pure Data, etc.)
- **Reconstructive phrase modeling (RPM)** — Lindemann's Synful Orchestra models the *transitions* between notes (slurs, portamento, tongued attacks, runs) from a compact database of recorded fragments, additive-coded and reduced via *vector quantization*; it scans for fragments to concatenate in real time from MIDI input, capturing musical *coarticulation* while letting samples be stretched, shifted, and spliced without clicks

## 6. Machine Learning and Walsh Functions

- **Magenta / DDSP** — Google's *machine learning* research (from \(\sim\)2015); *Differentiable Digital Signal Processing* (DDSP, 2020) uses *neural networks* to extract synthesizer parameters (fundamental frequency via the CREPE — *convolutional representation for pitch estimation* — model, amplitude, harmonic distribution) that drive a harmonics-plus-noise (SMS) synthesizer; reconstructs violin performances faithfully and enables cross-synthesis (singing voice to violin timbre, reverb extraction)
- **Autoencoder synthesis** — a *variational autoencoder* (VAE) is trained to compress and reconstruct magnitude STFT frames, driving an additive synthesizer; lightweight relative to other ML audio methods
- **Walsh function synthesis** — uses *Walsh functions* (rectangular waves taking only +1 and −1, analyzed via the *Walsh-Hadamard transform*) instead of sine waves; builds waveforms from differing *sequencies* (one-half the average zero-crossings per second). Conceptually opposite to sine synthesis — Walsh struggles to make a smooth sine, sine struggles to make a square wave
- **Why Walsh stayed marginal** — rectangular shapes compute fast on cheap digital circuits, but individual Walsh functions don't map to specific harmonics (though one can transform between Fourier and Walsh domains). Only a few experimental devices were built and none sold commercially, since sine additive synthesis is now cheap on any laptop
