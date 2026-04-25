# Ch 17: Generating in the Real World

## Table of Contents

- [1. Procedurality in Analog Works](#1-procedurality-in-analog-works)
- [2. Three Immersive Case Studies](#2-three-immersive-case-studies)
- [3. Why Bother Mixing Digital and Physical](#3-why-bother-mixing-digital-and-physical)
- [4. Computational Flâneur](#4-computational-flâneur)
- [5. Lessons for Any Procgen System](#5-lessons-for-any-procgen-system)

## 1. Procedurality in Analog Works

- **Physical embodiment amplifies ownership** — *Apples to Apples* and *Cards Against Humanity* are effectively comedy generators driven partly by a shuffled deck and partly by player curation, yet players feel genuine agency and real ownership over their jokes. Meaningful input + physical presence = deeper connection to generator output.

## 2. Three Immersive Case Studies

- **Sleep No More (Punchdrunk)** — immersive Macbeth-meets-*Rebecca* hyperdrama in the McKittrick Hotel, a six-story Manhattan warehouse. Actors follow precise pre-planned paths; the player's freedom to wander produces a huge narrative possibility space. The post-show debrief with friends is part of the work. Brute-force emergence fails in infinitely reproducible video games (wikis, Let's Plays), but succeeds in a $90+ bounded 2–3 hour physical event.
- **Then She Fell (Third Rail Productions)** — mostly-linear immersive theatre; only ~12 audience members per performance, each taken on an individually guided journey. Counter-intuitively, linearity enables intensely personal one-on-one actor scenes. Where *Sleep No More* optimises broad exploration, *Then She Fell* optimises vivid shareable moments.
- **Janet Cardiff's audio walks** — half-hour binaural soundscapes recorded over real-world spaces (*Her Long Black Hair*, 2004, Central Park). Static recordings, yet feel tailored to the listener. Cardiff plays with three element types:
  1. **Things that won't change** — police sirens on 59th Street; always there, always specific, feel authored.
  2. **Things meaningful either way** — a polar bear enclosure that was there once but isn't now; if the bear is there, it feels knowing; if not, it becomes a meditation on transience.
  3. **Things she can't possibly know about** — weather, crowds, Keanu Reeves filming by the Bethesda Fountain; open-ended language lets random noise register as deliberate.
  - **Psychology as tech** — Cardiff's narrative is about regret and not looking back (Lot's wife appears), which keeps listeners facing forward so the pre-baked positional audio isn't broken by head-turning. Wayfinding uses similar framing to keep players walking at the intended pace.

## 3. Why Bother Mixing Digital and Physical

- **Static audio walks are singular and hard to make** — Cardiff's pieces require deep binaural expertise. Digital tools can lower the barrier.
- **Reproducible works enable design communities** — traditional theatre builds local scenes; digital works enable cross-time cross-space conversation. Automatable immersive theatre would live on past its run.

## 4. Computational Flâneur

Lazer-Walker's MIT Media Lab project: a generative poetry walk for Fort Mason, San Francisco. Walk near cannons and the phone recites war poems; walk near the waterfront and it recites sea poems.

- **Not trying to be good poetry** — a simulacrum of the poetry-listening experience. Like doodling: interesting enough to break your train of thought, not interesting enough to hold your attention. A "meditation gong" that pulls your attention back to the physical space.
- **Pre-development lessons**:
  - **Bottom-up for alt-control interfaces** — prototype low-level interactions first; infer the experience from what's intrinsically satisfying moment-to-moment.
  - **Not everything technically feasible is understandable to players**. iPhone altimeter could distinguish individual stair steps; players had no mental model for per-step response. It worked better for "get on/off the elevator" because that matched expectation. Moving through a park at different speeds *seems* like useful input, but players have no model for speed-influenced procgen beyond "music gets more intense".
  - **Visual AR rejected** — staring at the world through a handheld glass slab isolates rather than connects.
  - **Head-tracking positional audio rejected** — phone-in-pocket sensors track body rotation, not head rotation; the mismatch broke the illusion. Better solved with Cardiff-style design than tech.
- **Development discipline** — the neural-net poetry generator had to run on laptop with no GPS (generate on demand for a given keyword); the app had to fake regions on any walk (hear shifts without being in SF); and builds had to stay deployable to iOS for real in-park testing. Staged playtesting lets most iteration happen away from the site.
- **Region transitions were not homogeneous** — three kinds for the same geofence system:
  - A visually uninteresting stairs section got its *own* distinct region so players got explicit feedback for climbing.
  - Sub-regions within the fort left their transitions subtle (just let abutting regions generate content).
  - The community garden (single entrance, needs conscious effort) got an oversized geofence so players heard the shift (birds replacing children playing) *before* entering.
- **Neural networks vs. Markov chains** — both are essentially "what statistically comes next?" but a neural net (char-rnn) can keep broader context while weighting recent tokens, producing text that looks more real without parroting. Both reveal themselves as fake quickly — a bad fit for most uses but exactly right for a "bot-like" texture.
- **Variable-reward structure** — the generator is a slot machine. Most output is mediocre; rare moments of real synchrony with the physical world feel like magic. Those moments work as meditation gongs, deepening connection to the place.
- **Cadence and replayability** — Twitterbots are endless streams; narrative games assume return sessions. A physical piece has to work in a single visit, making it Twitterbot-shaped. That should have meant more replay value but in practice most players visited Fort Mason once. Repeat visits need both low-friction re-access and explicit reasons to return — the shipped version had neither.

## 5. Lessons for Any Procgen System

- Weird inputs must be *understandable* by players, not just sensorially available.
- Invisible inputs the player can't control still register emotionally; design for them.
- Break problems into composable sub-problems that can be tested in isolation.
- Sometimes you can skip the digital algorithm entirely and get emergence from pure analog framing.
- Digital/physical isn't a clean binary; the more a system touches the physical, the more these concerns matter.
