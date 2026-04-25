# Ch 1: Getting Started with Generators

## Table of Contents

- [1. Before You Build](#1-before-you-build)
- [2. Generative Methods](#2-generative-methods)
- [3. How Generators Fail](#3-how-generators-fail)

## 1. Before You Build

- **Artifact** — the thing your generator will make (birds, stories, dance choreography, quests). Name it first before picking a technique.
- **List desirable properties** — what makes a "good" artifact? The more specific the artifact, the more specific the rules (fun for Mario ≠ fun for Civilization).
- **List constraints** — what must absolutely not happen. Star the hard constraints. Reliable generators start from concrete constraints, not vibes.
- **Possibility space** — the set of all artifacts the generator can make. Aim for a range where most artifacts are good and few are bad; the width of that range is a design choice.
- **Alternative flow** — for jams and prototypes, start with loose pieces, see what the method *wants* to generate, then revise the target artifact to match.
- **Artist-in-a-box** — sit with someone who makes the artifact by hand (Spore did this with its art team). Capture their questions, decisions, tradeoffs, and vocabulary (their **ontology**). Existing frameworks (music theory, hero's journey, TV tropes, golden ratio) can seed rules but none is complete.
- **Five skills a generative method can give a computer** — encapsulate options (A), create structure (B), encode conditional rules (A2), vary structure (B2), check its own constraints (C). Pick a method based on which skills your artifact needs.

## 2. Generative Methods

| Method | What it does | Strong on | Weak on | Examples |
|---|---|---|---|---|
| **Distribution** | Spread items across a space or timeline | Option selection (A, A2) | Structure (B, B2) | RPG monster/loot tables; weighted random; deck shuffling |
| **Parametric** | Tweak a mostly-built artifact along fixed axes | Reliability, controllability | No structural surprise | No Man's Sky creatures; Photoshop brushes; Perlin/Simplex noise, Voronoi, metaballs, diamond-square |
| **Tile-based** | Fill modular same-sized slots with hand-authored pieces | Small-scale structure | Large-scale structure; rigid option set | Settlers of Catan, Betrayal at the House on the Hill, Civilization; Musikalisches Würfelspiel (1750s) |
| **Grammars** | Big things recursively made of smaller things | Encoding deep structure + options in one piece of data | Cross-cutting constraints (e.g. foreshadowing) | Orteil's *Nested*; **Tracery** (Compton's own library) |
| **Constraint solvers** | Search a possibility space to satisfy hard rules | Many hard constraints at once | Heavy, new, hard to integrate | Brute-force; Answer Set Solving (Adam Smith); Craft (Ian Horswill) |
| **Agents & simulations** | Many simple actors produce emergent behaviour | Surprising emergent outcomes | Control | Braitenberg vehicles, Boids, genetic algorithms, cellular automata |

- **Genetic algorithms** need three ingredients: a **genotype** (something you can modify), a **phenotype** (something you can judge), and a mapping from one to the other. Compton's flower app uses a float array (genotype) fed into a parametric flower generator (phenotype); users pick favourites, whose genotypes are cloned and mutated.
- **Cellular automata** — many tiny agents with simple rules running in parallel. Conway's Game of Life is the canonical case; more complex rules power Dwarf Fortress, the Powder game, and voxel-based worlds like Minecraft.

## 3. How Generators Fail

- **Generate-and-test** — if you can computationally detect a bad output, just regenerate. Breaks down when the pass rate is too low; then switch to a constraint solver or restrict the generator.
- **Undescribable constraints** — "I know it when I see it" (offensive text, accidental genitalia, looks-like-a-logo) can't be filtered reliably. Best option is to bias the generator away from the bad region, accepting a smaller possibility space.
- **Aesthetic failure** — the most common failure: output is technically correct but uninteresting.
- **10,000 Bowls of Oatmeal problem** — a generator can produce mathematically unique outputs (e.g. 2^64 planets) that all feel the same to a player. Mathematical uniqueness ≠ perceived variety.
- **Perceptual differentiation vs. perceptual uniqueness** — differentiation (a tree isn't identical to the last tree) is the easier bar; uniqueness (this NPC is *memorable*) is much harder. Most generated artifacts should stay drab background so the few characterful ones can stand out.
- **Readable meaning** — humans respond to evidence of process and forces (soil pushed up at a tree's base, grass sheltered by a gravestone). Hints of a living world behind the object amplify character. Kevin Lynch's *Image of the City* shows similar principles for what makes cities memorable.
