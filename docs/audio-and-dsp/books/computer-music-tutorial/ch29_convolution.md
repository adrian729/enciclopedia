# Ch 29: Convolution

## Table of Contents

- [1. What Convolution Is](#1-what-convolution-is)
- [2. The Operation and the Law of Convolution](#2-the-operation-and-the-law-of-convolution)
- [3. Fast and Real-Time Convolution](#3-fast-and-real-time-convolution)
- [4. Deconvolution and Measuring Impulse Responses](#4-deconvolution-and-measuring-impulse-responses)
- [5. Musical Significance](#5-musical-significance)

## 1. What Convolution Is

- **Convolution** — a fundamental DSP operation that "marries" two signals (from French *convoluer*); often disguised as *filtering* or *reverberation*. It combines an input signal with another, usually an *impulse response* (IR)
- **Impulse response (IR)** — a system's response to a brief impulse; in a digital system the briefest signal is one sample, which contains energy at all representable frequencies (an approximation of the infinitely brief *unit impulse*). Convolving a hall's IR with any sound imposes the hall's sonic signature onto it — likewise for any mic, amplifier, loudspeaker, filter, or effect
- **IR libraries** — since the convolution algorithm is well known, commercial products' value lies in proprietary IR libraries recorded at exotic locations; free libraries and IR-design tools (Voxengo Impulse Modeler) also exist
- **Cross-synthesis** — convolving two arbitrary sounds rather than a sound and an IR, so one instrument seems to "play" the other (a chain of bells playing a gong). It transforms time-space structure and spectral morphology simultaneously; effects range from subtle enhancements to destructive distortions that obliterate both inputs, and many seemingly interesting ideas yield amorphous "sound blobs," so the terrain needs exploring before systematic use (Roads 1997)

## 2. The Operation and the Law of Convolution

- **Time vs frequency domain** — a *time-domain* (pressure graph) plots amplitude versus time; a *frequency-domain* (spectrum) plots energy versus frequency, obtained by spectrum analysis. The *Discrete Fourier Transform* (DFT), realized by the *Fast Fourier Transform* (FFT), has a privileged tie to convolution and represents a spectrum as paired magnitude and phase arrays, enabling point-by-point *multiplication of spectra*
- **Building blocks** — convolution with the *unit impulse* is an identity operation (signal unchanged, denoted with `*`); convolution with a scaled impulse \( c \times unit[n] \) scales the signal by \( c \); convolution with a time-shifted impulse \( unit[n-t] \) delays the signal. Any function is a sequence of scaled, delayed unit impulses
- **General operation** — to convolve \( a[n] \) with \( b[n] \), place a scaled copy of \( b \) at each point of \( a \) and sum them. Two widely spaced impulses in \( b \) produce an echo; closely spaced impulses produce overlapping repetitions — *time-smearing*, the beginning of reverberation (a 3 s hall IR at 48 kHz is 144,000 samples)
- **Properties** — convolution is *commutative* (\( x*h = h*x \)) and *linear*; the convolution product length is \( \text{length}(x) + \text{length}(h) - 1 \)
- **Convolution as LTI filtering** — *to filter is to convolve.* A length-\( N \) FIR filter's output is the convolution of the input \( x[n] \) with the coefficient sequence \( b[n] \), which is the filter's impulse response; an IIR filter is the same with \( b[n] \) of infinite length. Convolving two signals passes one through an LTI filter whose IR is the other
- **The Law of Convolution** — *Convolution in the time domain is equivalent to multiplication in the frequency domain, and vice versa.* By Fourier symmetry, multiplying two waveforms (amplitude or ring modulation) convolves their spectra, and *windowing* a sound convolves the spectra of envelope and sound

## 3. Fast and Real-Time Convolution

- **Cost of direct convolution** — the convolution sum needs \~\( N^2 \) operations; for an IR over \~4,096 samples, *time-domain convolution* is impractical in real time without a *GPU*, since laptop CPU clock speeds have barely risen since 2012
- **Fast convolution** — exploits the law of convolution: FFT the two inputs, multiply (\~\( N \) operations), then IFFT back. Convolving a 2 s sound with a 2 s IR at 48 kHz needs \~9 billion operations directly but under 1.5 million via fast convolution — a \~6,100× speed-up. Practical narrow-band filters and reverberators use this *block-transform* method (Stockham 1966, 1969)
- **Instant (single-pulse) convolution** — when the IR is only positive/negative unit impulses and zeros, no multiplication is needed: add the sound at a positive impulse, add a phase-inverted copy at a negative one, do nothing at a zero. Used in pitch-synchronous granular synthesis and *reverberation with velvet noise*
- **Real-time convolution** — aims to minimize *latency* from block processing (input buffers of 32–1,024+ samples). Convolution's linearity lets it run in *sections*; Gardner (1995) achieved zero input-output delay by applying direct (FIR) convolution to the first short block (e.g. 128 samples, \~1.3 ms at 96 kHz) then scheduling block FFTs. Brandtsegg, Saue, and Lazzarini (2018) update IR coefficients at audio rates for live cross-synthesis
- **Dynamic convolution** — simple convolution uses one "snapshot" IR (fine for linear reverberation). *Dynamic* (nonlinear) convolution applies a level-dependent IR to every sample to model nonlinear devices like compressors, requiring an array of stored IRs per input level. Pioneered by Focusrite Liquid Channel (2004), modeling 40 classic compressors and preamps (AMEK, API, dbx, Pultec, Fairchild, Millennia, Neve, Solid State Logic, Trident, UREI, etc.)

## 4. Deconvolution and Measuring Impulse Responses

- **Deconvolution** — dividing spectra: if \( H(f) \) is known, multiply the convolved spectrum \( X(f)H(f) \) by \( 1/H(f) \) (the *matched filter*) to recover \( X(f) \). It is an element-by-element complex division per frequency bin. Unlike convolution, deconvolution is *not* commutative (\( X(f)/H(f) \neq H(f)/X(f) \)) — dividing a voice out of a drum-voice convolution leaves the drum, and vice versa. Used to remove reverberation by dividing out a known acoustic IR
- **Statistical deconvolution** — for signals known only approximately; *autoregressive* and *homomorphic* deconvolution can separate speech excitation (glottal pulses) from resonance (vocal tract formants), the latter via *cepstrum* analysis
- **Sine-sweep IR measurement** — traditional balloon-pop / starter-pistol methods are hard to record undistorted and have nonlinear frequency response. The preferred *sine-sweep* method records a sine sweeping from \~20 Hz to Nyquist over \~15 s; it gives the best signal-to-noise ratio and separates nonlinear loudspeaker distortion from the linear acoustic space (Farina 2000)
- **Extracting the IR** — the recorded sweep contains all reflections stretched across its length, so it is deconvolved by convolving with an inverse filter (the reversed, delayed sweep) that nullifies the sweep via spectrum multiplication, then dividing by the squared magnitude spectrum of the original sweep to time-align all reflections to the file's start

## 5. Musical Significance

- **Filtering as convolution** — any LTI filter is implemented by convolving the input with the desired filter's IR; cross-synthesis extends this to filtering one sound by another (multiplying their analyzed spectra and resynthesizing). Convolving two smooth-attack saxophone tones mixes their pitches while accentuating shared metallic resonances
- **Temporal effects** — convolution induces echo, time-smearing, and reverberation. An IR of two impulses 500 ms apart gives a clear echo; a room's many-impulse IR maps a sound into the room's echo pattern; closely spaced peaks time-smear, smoothing transients and blurring onsets (e.g. a cowbell convolved with itself). Noise with a sharp-attack/exponential-decay envelope convolves into naturalistic reverberation
- **Modulation as convolution** — ring modulation multiplies bipolar waveforms, which convolves their spectra and produces sidebands (using complex-number arithmetic, as the FFT yields a complex number per component). Convolving a 100 Hz sinusoid with a 1 kHz sinusoid scales the 100 Hz pulses to the 1 kHz region, yielding sum (1.1 kHz) and difference (900 Hz) frequencies
- **Convolution with grains and pulsars** — convolving a sound with a cloud of sonic *grains* treats the cloud as a *virtual impulse response*: a sparse cloud gives a statistical distribution of echoes, a denser cloud fuses into irregular reverberation, longer grains accentuate time-smearing, and a smooth-attack input yields time-varying filtering. Convolution with trains of variable-waveform impulses called *pulsars* spans infrasonic to audio rates, giving rhythmic and timbral effects (Roads 2001a)
