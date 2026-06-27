# Ch 37: Spectrum Analysis by Fourier Methods

## Table of Contents

- [1. Fourier Foundations: FT, DFT, FFT](#1-fourier-foundations-ft-dft-fft)
- [2. The Short-Time Fourier Transform](#2-the-short-time-fourier-transform)
- [3. Windowing and Resolution Trade-offs](#3-windowing-and-resolution-trade-offs)
- [4. Resynthesis and Displays](#4-resynthesis-and-displays)
- [5. Phase Vocoder and Tracking Phase Vocoder](#5-phase-vocoder-and-tracking-phase-vocoder)
- [6. Spectral Modeling Synthesis and Transformation](#6-spectral-modeling-synthesis-and-transformation)

## 1. Fourier Foundations: FT, DFT, FFT

- **Fourier's model** — devised by Jean-Baptiste Joseph, Baron de Fourier (1768–1830), it assumes every sound is the sum of harmonically related sinusoids; it is the analytical counterpart to additive synthesis
- **Fourier series** — a periodic function \( x(t) \) of period \( T \) is an infinite sum of harmonically related sinusoids at frequency \( n\omega = n2\pi/T \), where \( C_0 \) is the DC (0 Hz) offset, \( C_1 \) is the *fundamental*, and \( C_n, \varphi_n \) are each component's magnitude and phase. It synthesizes a periodic signal but does not say how to derive the coefficients from a sound
- **Fourier transform (FT)** — the analysis method that maps a continuous-time waveform \( x(t) \) to a spectrum \( X(f) \), integrating the signal multiplied by an infinite set of pure sinusoids \( e^{-j2\pi ft} \). Each \( X(f) \) is a complex number; *magnitude* is the absolute amplitude of each frequency. The spectrum is symmetric around 0 Hz (negative frequencies are phase-inverted)
- **Phase spectrum** — the FT also carries each component's starting phase, but it usually looks random to the eye, so it is shown less often than the magnitude spectrum
- **Discrete Fourier transform (DFT)** — the frequency-domain representation of a discrete-time periodic signal \( x[n] \) (brackets denote discrete); gives a sampled look at both magnitude and phase, setting a one-to-one correspondence between \( N \) input samples and the number of resolved frequencies. The *discrete cosine transform* (DCT) is the related operation used in MP3
- **Fast Fourier transform (FFT)** — simply an efficient implementation of the DFT; calculation time is proportional to \( N \log_2(N) \), so a 32,768-point FFT takes more than a thousand times as long as a 64-point FFT

## 2. The Short-Time Fourier Transform

- **STFT** — Dennis Gabor's (1946) adaptation of Fourier theory to finite, time-varying signals, treating sonic quanta as rectangles tiled on a time-frequency matrix (the *Gabor matrix*). It imposes a sequence of overlapping *time windows* (typically 10–100 ms) on the input and analyzes each segment separately to yield a time-varying spectrum
- **Frame** — each block of FFT output, by analogy to film frames; contains a *magnitude spectrum* (amplitude per frequency) and a *phase spectrum* (initial phase, \( -\pi \) to \( \pi \)). Normalized to that range it is the *wrapped phase* representation
- **Bin** — a discrete point on the frequency continuum; bins are spaced at integer multiples of \( f_s/N \). The frequency of bin \( k \) is \( f_k = (k/N) \times f_s \) — e.g. at \( f_s \) = 44.1 kHz and \( N \) = 1024 samples, \( f_k \) for \( k = 1 \) is 43 Hz
- **Effective resolution** — since audio is bandlimited to the Nyquist frequency (half \( f_s \)), only half the bins matter: \( N/2 \) bins spread from 0 Hz to Nyquist

## 3. Windowing and Resolution Trade-offs

- **Why windows distort** — the analyzer measures the *product* of signal and window, so the result is the convolution of their two spectra; windowing inevitably smears the measurement
- **Rectangular (boxcar) window** — the crudest: keep part of \( x[n] \), zero everything else. A single sine fed through it *splatters* (clutters) energy across all bins instead of one line, because the bin response depends on distance from the bin center
- **Bell-shaped windows** — symmetric curves whose spectra resemble a sinc function (\( \sin(t)/t \)), with a *center lobe* and *side lobes*. Quality is judged by center-lobe width (in bins) and how many dB down the highest side lobe sits; a Gaussian's first side lobe is \~45 dB down
- **Side-lobe vs resolution trade-off** — suppressing side lobes broadens the center lobe, lowering resolution; the choice is between distortion (high side lobes smothering adjacent peaks) and poor resolution (too broad a center lobe). No universally best window: *Hann* suits stable low-pitched sounds, *Blackman* suits unstable/noisy sounds; *Kaiser* and *Gaussian* are also common
- **Time/frequency uncertainty** — a fundamental *uncertainty principle* (Heisenberg) between time and frequency resolution: high time precision sacrifices frequency precision and vice versa. *Periodicity implies infinitude* — a single pure frequency requires an infinite-duration sinusoid, so a one-sample window reveals nothing about the waveform it belongs to
- **The bin trade-off (worked)** — at 44.1 kHz, \( N \) = 512 gives 256 bins; 1 ms time accuracy (44 samples) allows only \~22 bins → \~1000 Hz resolution; a 30 ms window gives \~33 Hz; reaching 1 Hz resolution requires a 1 s (44,100-sample) window
- **Zero padding** — padding a frame with zero-valued samples up to a larger FFT size (e.g. 64 input samples padded to 1024) increases frequency resolution
- **Frequencies between bins** — when \( f \) sits between bin centers (common for inharmonic gongs or noisy snares), energy leaks across all bins; multiple components cause *beating effects* (periodic cancellation/reinforcement). This *clutter* is benign under direct resynthesis but obscures visual inspection and transformation

## 4. Resynthesis and Displays

- **Overlap-add (OA) resynthesis** — applies the inverse DFT (IDFT) to each frame and overlaps/adds the windows (typically at their −3 dB points). It assumes windows sum to a constant; transformations that break this *perfect summation criterion* (e.g. time stretching) cause audible artifacts like comb filtering and robotic voices. Heavy overlap (factor of eight or more) helps and is equivalent to *oversampling the spectrum*
- **Sinusoidal additive resynthesis (SAR / oscillator-bank)** — drives a bank of oscillators with amplitude/frequency envelopes that span frame boundaries; envelopes are more robust under transformation (stretch, shift, rescale) than raw frames, but the method is poorly suited to real-time operation
- **Sonogram (spectrogram)** — a 2-D display of time (horizontal) versus frequency (vertical) with gray shades for amplitude; long used in speech research (Backhaus 1932; the analog Kay Sonograph), now built with the STFT. A short window gives a vertical, time-precise but frequency-blurred image; a long window gives a horizontal, frequency-sharp but time-smeared one

## 5. Phase Vocoder and Tracking Phase Vocoder

- **Phase vocoder (PV)** — developed at Bell Labs (Flanagan and Golden 1966); passes the windowed input through a bank of equally spaced bandpass filters that measure both amplitude *and* phase per band, enabling highly accurate resynthesis by summing amplitude- and phase-modulated oscillators. Goal in music: transform a sound while keeping its identity (unlike convolution)
- **PV parameters** — *frame size* (sets the time/frequency trade-off and FFT cost), *window type* (any standard bell shape), *FFT size* (nearest power of two, usually double the frame size, padded with zeros), and *hop size / overlap factor* (smaller hop = more overlap; four-times overlap minimum, eight-times for transformation). Rule of thumb: frame large enough for four periods of the lowest frequency of interest
- **Window closing** — running the same signal through repeatedly, progressing from high-time/low-frequency to low-time/high-frequency resolution, since any single window biases the analysis toward harmonics of its own period
- **Phase and resynthesis accuracy** — discarding phase to save data degrades resynthesis (like a jigsaw with every piece centered correctly but not rotated); phase matters most for transients. The phase difference of a bin between successive frames gives its deviation from mid frequency, enabling time-base changes
- **Tracking phase vocoder (TPV / sinusoidal modeling)** — follows the most prominent spectral peaks over time rather than fixed harmonic bins, producing amplitude/frequency envelopes that drive sinusoidal oscillators (more accurate, more transformation-robust, but more parameter-sensitive than the STFT)
- **Peak tracking** — sets a *minimum peak height*, then advances *frequency guides* that match the nearest peak per frame; a guide that cannot continue is *sleeping* and is deleted if it does not wake within a user-set number of frames. *Guide hysteresis* keeps tracking a guide that dips slightly below the *amplitude range* to avoid audible *switching*. Sharp attacks are best processed in time-reversed order so trackers lock onto stable trajectories first
- **TPV residual** — subtracting the tracked ("clean," quasiharmonic) spectrum from the original yields a *residual signal* (the "dirty" part); for fast transients like cymbals the discarded noise energy is audibly missing, leaving the clean part sounding "sanitized." Noisy sounds can balloon analysis data to ten times the original size

## 6. Spectral Modeling Synthesis and Transformation

- **Spectral modeling synthesis (SMS)** — Serra's (1989) extension of the TPV that splits a sound into a *deterministic* component (prominent narrowband sinusoids, tracked and resynthesized as sines) and a *stochastic* component (the residual, modeled as simplified spectrum envelopes equivalent to filtered white noise, implemented as random-phase sines). Envelopes are intuitive for musicians to edit, though the perceptual fusion of the two parts is delicate
- **ATS** — analysis-transformation-synthesis; a sinusoidal-plus-*critical-band noise model* that warps the residual into 25 *Bark scale* bands and re-injects band energy as modulated narrow-band noise, so sinusoidal and noise parts integrate well perceptually
- **Vocaloid** — an SMS-based singing synthesizer (Kenmochi Hideki under Serra, Pompeu Fabra, 2000; commercialized by Yamaha, 2004); combines SMS with a subtractive source-filter model and frequency-domain concatenative synthesis, each voice bank sold as "a singer in a box"
- **Cross-synthesis** — combining two sounds; forms include the channel vocoder (one sound's spectral energy controls another's, e.g. a "talking orchestra"), magnitude-controls-magnitude *filtering by convolution* (most effective when one input is broadband noise), and magnitude-of-one with phase-of-another hybrids
- **Spectral mutation** — Polansky and Erbe's (1996, in SoundHack) frequency-domain interpolation from timbre A to B over time using five mutation functions on phase/amplitude pairs per band — distinct from a time-domain crossfade
- **Morphing** — gradual transformation from sound A to B; Lemur used the TPV, while Loris used *reassigned bandwidth-enhanced* (RBE) analysis whose partials carry a noise (bandwidth) component, with reassignment improving resolution via a nonuniform time-frequency grid. The most common spectral transformation overall is *pitch-time changing*
