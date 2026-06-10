# Procedural Animation & Generation

> A from-scratch, Rust + Bevy reference for **procedural animation** (motion that emerges from rules and constraints instead of pre-authored keyframes) and a primer on **procedural generation** (content built deterministically from a seed). Synthesised from argonautcode's [animal-proc-anim](https://github.com/argonautcode/animal-proc-anim) and [soft-body-proc-anim](https://github.com/argonautcode/soft-body-proc-anim) (Processing) and [zalo's](https://zalo.github.io/) blog posts on [constraints](https://zalo.github.io/blog/constraints/) and [inverse kinematics](https://zalo.github.io/blog/inverse-kinematics/). Examples are ported to Bevy `0.18`; the source is in Processing/JavaScript.

## Table of Contents

- [1. Two Throughlines](#1-two-throughlines)
  - [1.1. Animation Is Position-Based Dynamics](#11-animation-is-position-based-dynamics)
  - [1.2. Generation Is a Function of a Seed](#12-generation-is-a-function-of-a-seed)
- [2. When to Use What](#2-when-to-use-what)
- [3. How to Read This Section](#3-how-to-read-this-section)
- [4. Section Map](#4-section-map)
- [Sources](#sources)

## 1. Two Throughlines

Almost everything in this section collapses into one of two ideas. Keeping them in view is the fastest way to understand any individual technique — each page is an instance of one throughline.

### 1.1. Animation Is Position-Based Dynamics

Every animation technique here — chains, inverse kinematics, cloth, soft bodies — is the same loop:

\[ \text{integrate points} \;\rightarrow\; \big(\text{project points onto constraints}\big) \times N \;\rightarrow\; \text{render} \]

You never solve forces and accumulate them into velocities. Instead you move points by inertia (Verlet integration), then **repeatedly nudge each point the minimum distance needed to satisfy a constraint** (a fixed bone length, a joint-angle limit, a target area). This is **Position-Based Dynamics (PBD)**. "The essence of constraint is projection. Find the minimum movement that satisfies the constraint." Once that clicks, a rope, a lizard's spine, an arm reaching for a cup, and a wobbling blob are all the *same program* with different constraints.

### 1.2. Generation Is a Function of a Seed

Procedural *generation* shares no physics with animation, but it has its own unifying idea: content is a **pure function of a seed**. The same seed always yields the same world, so you store the seed, not the terabytes. Two families cover most of it:

- **Noise fields** — `f(x, y) -> height/density/colour`, continuous and smooth (terrain, clouds, textures).
- **Rewriting grammars & local rules** — start from a symbol or grid and apply rules repeatedly (L-systems for plants, cellular automata for caves).

## 2. When to Use What

| You want… | Use | Page |
|---|---|---|
| A rope, chain, or cloth that hangs and swings | Verlet points + distance constraints | [Foundations](software/procedural/foundations.md) |
| A tentacle / fish spine that *follows* a moving head | Angle-constrained forward chain | [Chains & IK](software/procedural/chains-and-ik.md) |
| A limb to *reach* a fixed target from a fixed root | Inverse kinematics (FABRIK / CCD / analytic) | [Chains & IK](software/procedural/chains-and-ik.md) |
| A creature with a skin and a walking gait | Spine chain + body outline + step cycle | [Creature Rigging](software/procedural/creature-rigging.md) |
| A squishy, deformable, volume-preserving body | Soft body (Verlet ring + area constraint) | [Soft Bodies](software/procedural/soft-bodies.md) |
| Terrain, clouds, or organic textures | Value / Perlin / simplex noise + fBm | [Noise & Heightmaps](software/procedural/generation-noise.md) |
| Plants, trees, or recursive structures | L-systems (rewriting grammars) | [Grammars & Systems](software/procedural/generation-grammars.md) |
| Cave layouts / organic blobs on a grid | Cellular automata | [Grammars & Systems](software/procedural/generation-grammars.md) |
| Natural-looking scatter (trees, rocks) | Poisson-disk sampling | [Grammars & Systems](software/procedural/generation-grammars.md) |

## 3. How to Read This Section

- **Read in order.** The animation pages are strictly bottom-up: [Foundations](software/procedural/foundations.md) builds the Verlet + constraint + relaxation primitives that every later page reuses. You cannot follow the soft-body area solver without the Jacobi-vs-Gauss-Seidel choice made in Foundations.
- **The generation pages are independent** of the animation pages and of each other — jump straight in.
- **Keep [Synthesis & Reference](software/procedural/synthesis.md) open** while implementing. It holds the Processing→Bevy API cheat-sheet, the y-down→y-up sign-flip checklist, and the correctness-gotcha list — the things that bite during a port.
- **This section owns** Verlet/PBD, IK, noise, gizmos, fixed-timestep mechanics, and runtime mesh generation. For Bevy ECS basics (components, systems, schedules, `Transform`, `Time`) it leans on the existing [Bevy](software/bevy.md) guide rather than repeating them.

## 4. Section Map

- **Animation** — motion from constraints (Position-Based Dynamics).
  - [Foundations: Verlet & Constraints](software/procedural/foundations.md) — the integrator, the distance constraint, relaxation, and the Bevy scaffold. Worked example: a hanging rope.
  - [Kinematic Chains & IK](software/procedural/chains-and-ik.md) — angle-constrained chains, FABRIK, CCD, and the IK-method comparison. Worked examples: a chain that follows the cursor; a FABRIK arm.
  - [Creature Rigging](software/procedural/creature-rigging.md) — rendering a body around a spine and a procedural walk cycle. Worked example: the lizard.
  - [Soft Bodies](software/procedural/soft-bodies.md) — a Verlet ring with area preservation. Worked example: the Blob.
- **Generation** — content from a seed.
  - [Noise, fBm & Heightmaps](software/procedural/generation-noise.md) — value/Perlin/simplex noise, octaves, and terrain.
  - [Grammars & Systems](software/procedural/generation-grammars.md) — L-systems, cellular automata, and sampling.
- [Synthesis & Reference](software/procedural/synthesis.md) — the throughline restated, a reasoning index, and the Bevy port cheat-sheet.

## Sources

- argonautcode — [animal-proc-anim](https://github.com/argonautcode/animal-proc-anim) (Processing) and its video [*A simple procedural animation technique*](https://www.youtube.com/watch?v=qlfh_rv6khY).
- argonautcode — [soft-body-proc-anim](https://github.com/argonautcode/soft-body-proc-anim) (Processing) and its video [*Simulating soft body animals*](https://www.youtube.com/watch?v=GXh0Vxg7AnQ).
- zalo — [*Constraints*](https://zalo.github.io/blog/constraints/) and [*Inverse Kinematics*](https://zalo.github.io/blog/inverse-kinematics/).
- Related reading already in this knowledge base: [Procedural Generation in Game Design](software/books/procedural-generation-in-game-design/book_summary.md), [Procedural Storytelling in Game Design](software/books/procedural-storytelling-in-game-design/book_summary.md), and the [Bevy](software/bevy.md) guide.
