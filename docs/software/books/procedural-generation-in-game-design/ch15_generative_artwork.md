# Ch 15: Generative Artwork

## Table of Contents

- [1. Framing: Beyond Technical Fidelity](#1-framing-beyond-technical-fidelity)
- [2. Techniques](#2-techniques)
- [3. Perception of Intent](#3-perception-of-intent)
- [4. Case Study: Desolus](#4-case-study-desolus)

## 1. Framing: Beyond Technical Fidelity

- **Desmond Paul Henry's drawing machines** — a re-purposed WWII bomb-guidance computer that drew "energetic, organic lines" with slight flutter and rippling edges; cited as proof that algorithmically simple processes can produce deeply human-feeling computer art.
- **Visual fidelity is not artistic merit** — today's "technical excellence" depends on funding, time, and education; treating it as a quality metric is needlessly discouraging and unhelpful for evaluating art.
- **Goal of the chapter** — share modes of thinking, not new technical tools, for the human side of generative visual art.

## 2. Techniques

- **Scope is not quality; it is a separate axis** — adding flashy features (animated flowers, heat haze, atmospheric scattering) increases scope, not quality. Instead step back: how does the piece feel vs. how you want it to feel? Could it improve by *removing* something?
- **Thinking in terms of processes** — algorithms aren't only judged by whether they work but by whether they are **emotionally relevant** to the project. Code is an expressive language; dissonance creeps in when tools and goals aren't in tune. Either alter the algorithm or alter the goal so they harmonize.
- **Symmetry and structure** — humans engage automatically in pattern detection and respond strongly to symmetry. A few shapes plus iterative symmetry quickly start to look compelling.
- **Mark making** — examine how you make marks (pixels, rasterized vectors, polygons in 3D, letters in a string). Tools have a distinct fingerprint (e.g., JavaScript or Unity work is highly recognizable). If fighting the default look, use built-in functions unconventionally or write your own low-level drawing routines.
- **Postprocessing** — altering output after creation. Real-time 3D conventionally limits itself to vignettes, motion blur, color correction, and SSAO. Custom postprocesses (e.g., feeding **Atkinson** or **Floyd–Steinberg** dithering with unconventional diffusion kernels) open a wide range of effects. The boundary between creation and post-effects can be permeable; feedback between the two is fertile territory.

## 3. Perception of Intent

- **Perception of intent** — viewers naturally search for the creator's intent (Who made this? What were they feeling?). Some generative work fights this tendency to feel more varied and intentional rather than "noise."
- **Linear growth of variety isn't enough** — adding more building types to a town generator is a linear increase that does nothing to address structural blindnesses or perceived lack of intent. The output still reads as random diverse buildings.
- **Self-aware structures over flat variety** — a generator that produces multibuilding complexes (walled courtyards, parks) starts to address the *perception of intent* problem; viewers begin picking out patterns instead of noise.
- **High-level abstract plans** — a generator that first plans neighborhoods (factory complexes along the water, agriculture away from center, markets at neighborhood centers) lets lower-level building generators act with awareness of the plan, producing both variation and a sense of intent.

## 4. Case Study: Desolus

- **Desolus (Mark Mayers)** — a surrealist puzzle game built by a solo developer with no traditional art training, using procedural art to compensate for that gap.
- **Hand-crafted base, algorithmic refinement** — terrain is roughed in by hand, then refined with erosion simulation; trees are hand-modeled species manipulated by **SpeedTree** to grow unique instances per environment.
- **No rigged characters or animations** — the game uses a GPU particle effect system plus shaders to convey gameplay elements abstractly, freeing effort for world design.
- **Black hole as core puzzle mechanic** — built from a gravitational lens shader plus GPU particles; tweaking colors, physics forces, emission, and shaders yields varied scenario-specific results.
- **Dynamic sky and non-organic meshes** — sky is shader-driven (color, atmospheric properties) for mood; non-organic meshes such as the recurring black obelisks are built from fractals and procedural meshes (recursive cloning of a simple cube).
- **Universe from simple rules** — the systems combine into a complex world from simple algorithmic laws; the artist's role is interpreting which aspects of those universal laws are most beautiful.
