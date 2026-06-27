# Ch 26: Sound Mixing

## Table of Contents

- [1. Fundamentals of Mixing](#1-fundamentals-of-mixing)
- [2. Software Mixing](#2-software-mixing)
- [3. Mixing Consoles](#3-mixing-consoles)
- [4. Multitrack Recording and Remixing](#4-multitrack-recording-and-remixing)
- [5. Audio Monitoring](#5-audio-monitoring)

## 1. Fundamentals of Mixing

- **Mixer** — hardware or software that sums many signals into a composite signal; in the digital domain mixing is literally sample-by-sample addition (e.g. 32,767 + (\(-\)32,767) = 0)
- **Track vs channel** — a *track* (colloquially a *lane*) is sound stored on a medium (mono or stereo); a *channel* is a source or destination for audio (a mic input, a loudspeaker output)
- **Mixdown vs upmixing** — *mixdown* blends many tracks/channels into fewer; *upmixing* distributes a few into many (e.g. spatializing a stereo track over eight loudspeakers)
- **Fusion vs fission** — the core aesthetic problem: *fusion* melds sounds into a single gestalt, *fission* comingles them while keeping each perceptually distinct; mixing plays between these poles and so articulates musical structure

## 2. Software Mixing

- **Non-real-time software mixing** — the musician plans the mix, then software executes it; handles dozens of tracks and hundreds of files beyond any physical console's capacity, integrates with plug-ins, and (e.g. Reaper) can be scripted via an *API* in EEL, Lua, or Python
- **Mixing by script** — synthesis languages (Csound's *soundin* unit generator reading *note* statements) read and scale sound files; enables *algorithmic mixing*, as in the author's 1974 granular synthesis that generated thousands of overlapping grains (Roads 1978c)
- **Digital audio workstation (DAW)** — graphical timeline interface for editing/mixing; pioneered by SoundEdit (Steve Capps, 1986) and MacMix (Adrian Freed, 1987), where waveform clips could be dragged freely along the timeline — impossible on serial multitrack tape. Successors include Pro Tools, Cubase, Ableton Live, Logic Pro, Reaper
- **Assessment** — software mixing offers flexibility and precision but requires planning and rehearsal, and lacks the intuitive "feel" of real-time faders (a mouse or keys are poor controllers); a console with precision faders is a valuable complement

## 3. Mixing Consoles

- **Mixing console** (*desk*/*mixer*) — combines input channels into output channels in real time, plus filtering and routing; can be analog (AMS Neve BCM-10 mk2, $70,000 in 2020), all-digital, or hybrid
- **Input/output ratio** — characterizes a mixer: an 8/2 handles 8 inputs mixed to 2 outputs; an 8/4/2 adds a four-output bus, enabling simultaneous four- and two-track recordings via separate *output buses*
- **Six main sections** — *input*, *output*, *auxiliary return*, *talkback*, *monitor*, and *metering*; signals route to buses via *output bus assignment buttons* and *pan pots* (panoramic potentiometers, which also place a sound in the stereo field)
- **Input module stages** — input select / phantom power / phase reverse; input attenuator (pad); parametric EQ (bandwidth, center frequency, boost/cut per band; a *semiparametric* EQ omits bandwidth); *auxiliary send/return* (to effects or a *cue* submix, pre- or postfader); pan pot; Mute/Solo/PFL (*prefader listen*, used by DJs to audition with the fader down); channel assignment; channel fader

| Section | Function |
|---|---|
| Auxiliary returns (*effects*/*cue*) | Blends effects-processed sound into output; builds monitor/cue submixes for performers |
| Talkback | Engineer-to-musician communication; also *slates*/*logs* a recording |
| Monitor | Routes L/R bus to control-room and studio loudspeakers/headphones |
| Metering | *Peak meters* (rise time a few ms) catch instantaneous peaks; *VU meters* (\~300 ms rise) track average loudness |
| Grouping | *Subgroup* fader controls level of several assigned channels at once |

- **Hybrid consoles** — combine analog audio (bandwidth beyond 100 kHz) with digital *motorized fader automation*; faders recall recorded moves robotically (top-to-bottom fades under 100 ms over 4,096 steps of 0.1 dB), and the engineer can override by touching a moving fader
- **Digital mixing consoles** — keep processing in the digital domain (no repeated DAC/ADC artifacts); use *assignable* controls (one knob set serves any channel), separate control surface from hardware, build in effects, integrate scene recall and networking (AVB, Dante, MADI), and are software-updatable. Downside: less standardized than analog, and small units bury controls in menus

## 4. Multitrack Recording and Remixing

- **Multitrack recorder** — has several discrete tracks each recordable at a different time, unlike early mono/stereo recording where the balance was fixed at recording time. Les Paul pioneered overdubbing in the 1950s; Stockhausen used a Telefunken T9 four-track for *Kontakte* (1960); a Studer J37 four-track made The Beatles' *Sgt. Pepper's* (1964)
- **Advantages** — each source on its own track defers balancing to mixdown; allows *track bouncing* (a.k.a. *submixing* / *stem mixing*); digital media have no *generation loss* (noise buildup from copying) that plagues analog
- **Mix automation** — continuously scans all console settings many times per second, recording only changed positions; lets a lone engineer build a complex mix incrementally and override stored settings manually at any time
- **Remixing problems** — isolating sources (isolation booths, baffles, directional/close mics) yields an unnatural perspective where each track sounds inches from the ear; engineers fuse tracks into a unified sound stage with global reverberation, balancing, and stereo placement
- **"Purist" approach** — a reaction to multitracking (Streicher and Dooley 1978) using fewer mics and channels to recreate the concert-hall image; determines the mix at recording time, demanding careful musician and microphone placement in a good-sounding hall

## 5. Audio Monitoring

- **Headphones** — the only option for *location recording*; magnify subtle flaws (splices, clicks, noise, distortion, phase problems) but can deceive — a crossfade perfect on headphones may sound abrupt on loudspeakers, with bass misjudged
- **Near-field monitoring** — small monitors under \~2 m from the engineer so direct sound dominates room reflections; smallness lets them project a *fused* image (a large speaker's *tweeter* may sit a meter from its *woofer*); weak below \~200 Hz, with "boominess" or missing bass
- **Control room monitoring** — speakers mounted in the forward wall of an acoustically tuned room, often *biamplified*/*triamplified*, equalized flat at a *sweet spot* at the engineer's head; supports high sound pressure levels typical of pop studios
- **Listening room monitoring** — informal living-room-like setting with large full-range *dynamic* (tweeter/midrange/woofer) or *electrostatic* loudspeakers; preferred by mastering engineers and classical producers at moderate levels
- **Mixing in performance** — best mixing position is among the audience in the middle of the hall; loudspeaker configuration and whether to blend or separate acoustic and electronic sound are open artistic decisions
