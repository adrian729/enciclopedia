# Ch 28: Digital Filtering

## Table of Contents

- [1. What a Digital Filter Is](#1-what-a-digital-filter-is)
- [2. Filters in the Time Domain](#2-filters-in-the-time-domain)
- [3. Filters in the Frequency Domain](#3-filters-in-the-frequency-domain)
- [4. Examples of Filters](#4-examples-of-filters)
- [5. Filter Design and Perception](#5-filter-design-and-perception)

## 1. What a Digital Filter Is

- **Digital filter** — a computational process that transforms an input sequence \( x \) into an output sequence \( y \) (Rabiner et al. 1972). Beyond spectral boost/cut, mixers, reverberators, compressors, companders, and spatializers are all digital filters — they can change a signal's spectrum, amplitude, and temporal structure
- **Three guiding properties** — *stability* (bounded output for any input; an unstable filter "explodes" into numerical *overflow*, e.g. guitar/mic feedback, whereas room reverb is stable); *time invariance* (effect doesn't depend on when the input arrives — flanging and chorus are *not* time-invariant); *linearity* (output for a sum of inputs equals the sum of the individual outputs — reverb is linear, a compressor is not)
- **Linear time-invariant (LTI) filter** — a filter that is both linear and time-invariant; a chain of LTI filters can be reordered with identical results. Built from just three components: *adders*, *scalar multipliers* (triangles), and *delays* (D, one sample). An LTI filter changes only the *amplitude* and *phase* of an input sinusoid, never its frequency

## 2. Filters in the Time Domain

- **How filters work** — they split the input into an original part and a delayed part; delays create out-of-phase (attenuating) or in-phase (boosting) copies that are added to or subtracted from the original, sculpting the spectrum by *phase cancelation* or *phase reinforcement*
- **Filter equation** — relates indexed samples, e.g. \( y[n] = 2x[n] + x[n-1] \) (output is twice the input plus the input delayed one sample). \( y[n] = x[n] \times y[n-1] \) involves *feedback* because it uses past output values
- **Filter order** — the number of delays used to compute an output sample; a *first-order* filter has one delay, a *second-order* (e.g. \( y[n] = 2x[n] + x[n-2] \)) has two
- **Feed-forward vs feedback** — feed-forward uses only past *input*, feedback uses past *output*. The general LTI equation is \( y[n] = b_0 x[n] + \ldots + b_M x[n-M] - a_1 y[n-1] - \ldots - a_N y[n-N] \), realized as two *tapped delay lines*: the \( b \) coefficients control the feed-forward line, the \( a \) coefficients the feedback line
- **Impulse response (IR)** — *Any LTI filter can be completely characterized by its impulse response.* An impulse contains all frequencies with equal energy (the shorter the signal, the wider its spectrum), so its output response reveals the filter's effect on every frequency
- **FIR vs IIR** — a *finite impulse response* (FIR) filter's output returns to zero after some time and uses only feed-forward (always stable); an *infinite impulse response* (IIR) filter has infinitely many non-zero output samples and typically uses feedback

## 3. Filters in the Frequency Domain

- **Filtering as spectral multiplication** — multiplying an input spectrum \( X(f) \) by a filter spectrum \( H(f) \) shapes the output \( X(f)H(f) \); the inverse Fourier transform shows this equals convolving \( x[n] \) with the time-domain sequence \( h[n] \)
- **Frequency response (FR)** — how a filter changes the impulse's flat spectrum, split into *magnitude response* (effect on a sinusoid's amplitude) and *phase response* (effect on its phase). The FR is the Fourier transform of the IR, and the IR the inverse transform of the FR — same information in different domains
- **Cutoff frequency and passband** — a *lowpass* filter passes frequencies below a *cutoff frequency* and attenuates those above; a linear phase response in the *passband* preserves the signal's envelope (the example filter is flat below \~\( 0.2\pi \) radians/sample, strongly attenuating above \( 0.3\pi \))
- **Poles and zeros** — analyzed via the *Z-transform*, plotted on the *unit circle* (DC at far right, the Nyquist frequency at far left, frequency increasing counterclockwise). A *pole* is a resonance/peak in the FR — the closer to the circle's edge, the sharper the peak; a *zero* is a trough — the closer to the circle, the deeper. If any pole is on or outside the circle the filter is unstable; a zero's location never affects stability

## 4. Examples of Filters

- **Simple FIR lowpass** — averages samples: \( y[n] = 0.5 x[n] + 0.5 x[n-1] \) (the 0.5s are *filter coefficients*); its FR resembles the first quadrant of a cosine and smooths sudden changes. Cascading an averager into another (averaging the average) steepens the high-frequency rolloff; averaging four samples instead is also lowpass but not equivalent to the average of the average
- **Simple FIR highpass** — subtracts instead of adds: \( y[n] = 0.5 x[n] - 0.5 x[n-1] \); small differences between samples suppress low frequencies while large differences pass highs. Cascading differences attenuates more lows
- **Simple bandpass** — passing a second-order difference through a second-order average (or vice versa) yields a bandpass response
- **Exponential smoothing filter** — a simple IIR filter using feedback: \( y[n] = x[n] + a \times y[n-1] \), equivalent to an infinite feed-forward line \( y[n] = x[n] + a x[n-1] + a^2 x[n-2] + \ldots \). As \( a \to 1 \) it attenuates above DC; as \( a \to -1 \) it attenuates below Nyquist. Stability requires \( |a| < 1 \)
- **Comb filter** — creates equally spaced spectral peaks and troughs (like comb teeth) via a multiple-sample delay; the FIR form is \( y[n] = x[n] + x[n-M] \). A *positive summing* comb has its first off-DC peak at \( f = \frac{1}{M} \times f_s \) with peaks at \( 2f, 3f, \ldots \) (reinforcing a fundamental and its harmonics) and nulls between them; the *negative summing* form \( y[n] = x[n] - x[n-M] \) instead removes the fundamental and harmonics. Short delays (<5 ms) give the richest effect; an *IIR comb* \( y[n] = x[n] + a \times y[n-N] \) adds resonance but becomes unstable if \( a \) is too high
- **Allpass filter** — passes all frequencies with a flat magnitude response but imposes a frequency-dependent phase shift (*dispersion*), delaying frequency regions by different amounts. Perceptually it colors transients and attacks (not steady-state tones); used in *Schroeder reverberators* (delay \( M \) of 10–30 ms gives decaying echoes). Moorer noted the allpass nature is "more a theoretical nature than a perceptual one"

## 5. Filter Design and Perception

- **Filter design** — choosing \( M \), \( N \), and the coefficients to meet specs (frequency response, FIR or IIR); a lowpass is specified by *passband* (limited *ripple*), *transition band*, and *stopband* (attenuation by \( 1/A \)), with cutoff where amplitudes are at least halved. Realization is nontrivial and usually an approximation balancing competing traits
- **Automated design tools** — code libraries and interactive programs (MATLAB) hide the algebra; FAUST generates efficient real-time C++ from high-level specs (GRAME)
- **FIR vs IIR tradeoffs** — FIR filters are always stable and simple but need many coefficients (delays/multiplications, hence latency) for a narrow transition band; IIR filters achieve sharp responses with few delays via feedback but risk instability, *ringing*, and phase distortion. A *linear phase FIR* avoids phase distortion at the cutoff but adds latency and a time-symmetric IR that can cause audible pre-echoes; for live use a *zero-latency minimum-phase filter* (e.g. Butterworth) is preferable
- **Second-order section (biquad)** — a popular IIR building block looking back two output samples: \( y[n] = b_0 x[n] + b_1 x[n-1] + b_2 x[n-2] - a_1 y[n-1] - a_2 y[n-2] \). The \( b \) (feed-forward) coefficients create notches, the \( a \) (feedback) coefficients create peaks; named *biquad* for its two quadratic formulas. Realizes bandpass (and, with zeroed coefficients, lowpass/highpass) responses — a standard EQ block, so common that DSP power is sometimes expressed as the number of second-order sections it can realize in real time
- **Subjective perception** — rooted in *psychophysics* (Fechner) and context-dependent. Gerzon (1990) showed tiny phase (\~1°) and amplitude (\(\pm 0.1\) dB) nonlinearities can cause audible coloration in some contexts while large deviations cause none — "The best equaliser is no equaliser!" Yet for the sound artist, the distinct color of a Moog 904A, Buchla 291, or Krohn-Hite 3550 filter is a feature, not a bug
