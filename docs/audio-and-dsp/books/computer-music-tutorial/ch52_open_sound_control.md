# Ch 52: Open Sound Control

## Table of Contents

- [1. What OSC Is and Why It Exists](#1-what-osc-is-and-why-it-exists)
- [2. OSC Compared with MIDI](#2-osc-compared-with-midi)
- [3. Addresses, Messages, and Bundles](#3-addresses-messages-and-bundles)
- [4. Designing Schemas and Assessment](#4-designing-schemas-and-assessment)

## 1. What OSC Is and Why It Exists

- **Open Sound Control (OSC)** — a communications protocol for sending data between *entities* (programs or devices); it defines the format and order of messages but, unlike MIDI, does not predefine what any message means
- **Origin** — designed by Matthew Wright and Adrian Freed at UC Berkeley's CNMAT (Wright and Freed 1997); the original need was a high-speed network protocol to control a custom synthesizer with dozens of parameters running on one computer from a Max patch on another over Ethernet
- **Motivation** — built for general-purpose high-speed communication that MIDI's slow bit rate, 16-channel limit, simple note model, and lack of floating-point representation could not serve; it transmits human-readable parameter names such as `/grain-density` plus integers and floats
- **Open protocol** — no license requirements, no patented algorithms or protected IP, and no strong assertions about use (Schmeder, Freed, and Wessel 2010); each implementer designs a scheme of messages meaningful in their own context
- **Wide adoption** — used in interactive systems, robotics, video performance, and distributed music; supported by Ableton Live, Max, Faust, ChucK, PureData, Processing, Reaper, Stride, SuperCollider, and Csound, among others. A PureData alternative is the *fast universal digital interface* (FUDI), a simple string-based networking protocol (Puckette 1997)

## 2. OSC Compared with MIDI

| Aspect | MIDI | OSC |
|---|---|---|
| Messages | Predefined, standardized meanings | Not predefined — implementer must define each one |
| Addressing | Fixed channels and controller numbers | Custom *address schemas* designed per system |
| Data types | MIDI 1.0: integers only (2.0 adds fractional) | Integers, floats, strings, and arbitrary-length blobs |
| Hardware | 5-pin DIN connector and USB | No hardware specification — transport-independent |
| Speed | 31,250 bits/s per channel | Up to gigabits/s via a network transport |
| Setup | Plug-and-play in most home studios | Must be designed and debugged for each system |

- **Transport** — OSC rides on a *network transport protocol*, most often the internet's *User Datagram Protocol* (UDP), which is fast because it does not guarantee delivery yet is reliable enough on local networks; *TCP* can be used for guaranteed delivery, and OSC also runs over serial/USB or within a single computer
- **Ports** — under IP, communication endpoints are *ports*; each IP address has 65,536, some reserved for *registered* functions and others available for user processes like OSC. Setting up internet OSC requires a port number plus the receiver's host name or IP address
- **Identification** — over a serial link, sender and receiver are implicitly whatever is on each end (as with MIDI); over Ethernet or the internet they are explicitly identified

## 3. Addresses, Messages, and Bundles

- **OSC packet** — the basic transmission unit, always a multiple of 4 bytes (32 bits); its contents must be either a message or a bundle. Anything sending one is an *OSC sender*, anything receiving it an *OSC receiver*
- **OSC message format** — `<address pattern> <type tag string> <arguments>`; the address is a string of letters, numbers, and punctuation that always starts with a forward slash `/`
- **Hierarchical addressing** — the `/` works like a URL or Unix file path, naming locations in a tree; a stereo white-noise synth might expose `/left/start`, `/left/volume`, `/right/start`, etc.
- **Pattern matching** — the receiver's address interpreter supports wildcards so one message reaches multiple destinations: `?` (any character), `*` (any sequence), `[string]` (any character in the set), and `{string1,string2}` (comma-delimited alternatives)
- **Argument data types** — primary type tags are `int32` (i), `float32` (f), *OSC-timetag* (t, a 64-bit NTP timestamp of seconds and picoseconds since 1 January 1900), *OSC-string* (s, NULL-terminated and padded to a multiple of 4 bytes), and *OSC-blob* (b, a byte count plus padded bytes)
- **Byte order** — OSC data use *big-endian* (most significant value stored first), the common data-networking convention, also called *network byte order*
- **OSC bundles** — a *timetag* plus any number of messages or sub-bundles (typically within a 64 KB UDP packet); a timetag implies a scheduler on the receiver. A single message is invoked immediately; a bundle whose timetag is at or before the current time is invoked at once, while a future timetag is stored until that time

## 4. Designing Schemas and Assessment

- **Address space vs. address schema** — the *address space* is the set of all meaningful OSC messages for a sender or receiver; the *address schema* is that space plus a specification of what each message means (e.g. the address space `/osc1/p-height` *and* the specification "/p-height controls the pitch")
- **Designing a connection** — to make two entities A and B interoperate, the designer must analyze and specify A's *output namespace* (every message it sends) and B's inputs and the response each triggers; the receiver dispatches a method for each address matching a message's pattern
- **Flexibility's downside** — because nothing is standardized, two equivalent granular synthesizers can name identical parameters differently, so a controller built for one will not talk to the other without modification — OSC must be debugged per system
- **Example (PureData → Csound)** — Csound provides four OSC opcodes: `OSCinit` (open a listening port, returning a *handle*), `OSClisten` (receive messages at an address path), `OSCsend`, and `OSCraw`. A PD patch's `sendOSC` object connects to `localhost` port `9999`; the Csound instrument runs `kans OSClisten giosc1, "/amp", "f", kamp` so an incoming `/amp` float continuously sets an oscillator's amplitude
- **Assessment** — OSC is an effective, flexible, high-speed choice for interactive performances and installations, and despite never being formally registered by a standards body it is supported in many commercial products
- **Will OSC replace MIDI?** — unlikely: MIDI is backed by an industry consortium, and MIDI 2.0 adds more channels, controllers, and finer control while keeping its message grammar; OSC remains favored by independent builders for custom solutions
