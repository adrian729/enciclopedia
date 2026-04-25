# Ch 26: Algorithms and Approaches

## Table of Contents

- [1. Framing](#1-framing)
- [2. Random Numbers](#2-random-numbers)
- [3. Heightmaps](#3-heightmaps)
- [4. Sequence Generation](#4-sequence-generation)
- [5. Filling Space](#5-filling-space)
- [6. Partitioning Space](#6-partitioning-space)
- [7. Putting It All Together](#7-putting-it-all-together)

## 1. Framing

- **A first-time hiker's map** — the chapter catalogs the most well-worn techniques in PCG so the reader knows where to start and recognizes the landmarks every practitioner names. It does not fill in the wilderness between them; the rewarding adventure is "among the brambles."

## 2. Random Numbers

- **Pseudorandom number generators (PRNGs)** — almost all environments ship one. They are *pseudo* because they don't return truly random numbers but a sequence that *appears* random: from an initial seed, a math operation produces the next value and updates the seed.
- **Determinism from the seed** — a given PRNG with seed 5 always emits the same series (e.g., 3, 23, 195, 1, …); seed 6 produces a different but equally fixed series.
- **Uses of repeatable series** — three core applications:
  - **Shared worlds across machines** — two players sharing one seed get identical generated content as long as choices happen in the same order; *Caves of Qud* uses this for daily/weekly challenges.
  - **Bandwidth reduction in multiplayer** — ship a small seed instead of large generated payloads.
  - **Regenerable persistence** — huge or infinite worlds need not save state; regenerate from seeds. The original *Elite* used this to fit an explorable universe on a memory-constrained machine.
- **Seeds and hashing** — a typical seed is a 32-bit integer. A raw integer like `1235100523` is unmemorable, so games accept a phrase ("a magic monkey") and convert it to an integer with a **hash function**.
- **Hash function** — takes input data and returns a value (usually shorter) that is the *same for any given input* and *statistically unrelated* across different inputs. Same input always returns the same hash; different inputs have only a vanishingly small chance of colliding (≈ 1 in 2³² for a good 32-bit hash).
- **Truncation works** — a smaller chunk of bits drawn from a perfectly random number is itself perfectly random, so taking the first 32 bits of a 128-bit hash yields a perfectly good 32-bit seed.
- **Common hash functions** — comparison:

  | Hash | Notes |
  |---|---|
  | **MD5** | Fast, statistically adequate for games |
  | **SHA family** | Strongly statistically random; useful for cryptography but slower |
  | **xxHash** | Less statistically random, very high performance |
  | **Murmer** | Common general-purpose option |

  Games typically choose fast hashes (MD5, xxHash) since cryptographic strength is unnecessary.

- **Hash use cases** — three concrete examples:
  - Hashing player-entered "watermelons" via MD5 for world-gen seed.
  - Hashing the date string "June 7, 2016" via MD5 for a daily challenge identical across all players.
  - Hashing "Worldseed51234 Galaxy 5 Solar System 118" via xxHash to derive a unique, regenerable seed for that solar system without storing its contents.
- **Rolling dice notation** — `1d6` = one six-sided die (1–6), `1d8` = one d8, `3d6` = three d6 summed (3–18). Many PRNGs only emit large integers, so you wrap them to map onto a die range.
- **Range helpers** — `RangeInclusive(max, min)` returns `(rng.next() % (max - min + 1)) + min`; `FloatingPointRange(max, min)` returns `(rng.next() / MAX_INTEGER) * (max - min) + min`.
- **Dice in use** — `d100` as a percentile success roll (compare against percentage chance); small dice pools for tunable damage ranges. One die yields a flat distribution; multiple dice summed yield a bell curve, making middle values more likely.
- **Normal (Gaussian) distribution** — the "bell curve." Adding several same-type dice approximates one; more dice → closer to truly normal. Described by **mean** (peak) and **standard deviation** (width); ≈ 68.27% of values fall within one standard deviation, ≈ 99.73% within three.
- **Basic implementation** — `GaussianRandomNumber(mean, std)`: draw two floats `A, B` in [0, 1], compute `C = sqrt(-2 * log(A)) * sin(2 * PI * B)`, return `mean + std * C`. The **Ziggurat algorithm** is faster when performance matters.
- **Normal distribution use cases** — daily temperature around a seasonal median with rare extremes; NPC bedtime around 10 p.m. with wide std producing morning larks and night owls; planet sizes clustered near Earth-sized with rare giants and dwarfs.
- **Weighted distribution** — like a bag of balls with each item assigned a weight equal to its number of balls. To draw: roll an integer in [1, sum-of-weights], walk items accumulating weights, return the item whose accumulator first meets or exceeds the roll.
- **Weighted distribution without replacement** — variant: after drawing, decrement the picked item's weight by 1 (simulates not returning the ball), preventing repeated draws.
- **Weighted distribution use cases** — random-encounter templates (common grunts heavy, rare leader-and-retinue light); weapon material (iron heavy, diamond light); shopkeeper inventory (drawing without replacement until shop is full).

## 3. Heightmaps

- **Heightmap defined** — a 2D grid of values that vary smoothly from cell to cell; used for lakes, continents, weed clumps, topographical maps.
- **Box linear filter (box blur)** — initialize a grid with high values clustered where peaks should be, then smooth by replacing each cell with the average of its neighbors; repeat to spread peaks. A weight matrix controls shape; an example "hill-like" 3×3 weight set is `1 3 1 / 3 5 3 / 1 3 1`.
- **Square-diamond midpoint displacement** — assign random values to the four corners of a grid; set the center cell to the corner average ± a small random variance; set each edge midpoint to the average of its two corners and the center ± variance; recurse on the four resulting subsquares. Variance shrinks exponentially per iteration so detail gets finer as the grid fills.
- **Perlin noise and simplex noise** — produce gradients with rolling waves at similar rates in every direction (think egg-crate foam): randomly placed peaks, statistically even distribution, valleys at 0 and peaks at 1. Generalize to 1D, 2D, 3D, and higher dimensions.
- **Layered noise** — most surfaces aren't egg-crate, so combine layers: a high-amplitude low-frequency layer for mountain ranges and broad valleys, then progressively higher-frequency lower-amplitude layers adding "potholes" and "anthills" of detail.
- **Perlin vs. simplex** — comparison:

  | Property | Perlin | Simplex |
  |---|---|---|
  | Speed | Slower | Faster |
  | Directional artifacts | Some | Visually isotropic |
  | Patent | Free | U.S. Patent 6,867,776 |

  **OpenSimplex** (2014) is an open-source alternative sharing simplex's positives without patent encumbrance.

## 4. Sequence Generation

- **Lindenmayer systems (L-systems)** — produce a fractal-like sequence by repeatedly applying transformation rules to a seed string. Example with rules `A → AB`, `B → A`, seed `A`: iterations yield `A`, `AB`, `ABA`, `ABAAB`, `ABAABABA`, `ABAABABAABAAB`. Elements can be reinterpreted as drawing instructions (e.g., `A` = move forward 1 step, `B` = turn right 45°).
- **L-system use cases** — road divisions and building placement for city layouts; branching headwaters of a river system; branching road networks and satellite villages around a trade hub.
- **Markov chain** — a directed graph of nodes with weighted edges. Pick a start node, emit its value, then repeatedly choose the next node from the weighted outgoing edges of the current node until termination (length cap or end-flagged node). Example weather chain: rainy with 25%/75% edges to itself/sunny, sunny with 25%/75% edges to rainy/itself, generates a weeklong sequence.
- **Building Markov chains from data** — given a sequence like `ABCAABACBACDB`, count each letter's successor frequencies (e.g., A → A 20%, B 40%, C 40%) to build the graph and then generate new sequences with similar stochastic properties.
- **Order of a Markov chain** — order 1 uses single elements as nodes; order 2 uses pairs (`AB`, `BC`, `CA`, …); higher orders capture longer-range structure.
- **Markov chain use cases** — generating music from note patterns; simulating dwarves' volatile mood swings; generating random recipes.

## 5. Filling Space

- **Random walk** — start at a point and step in random directions; many natural processes (e.g., molecular motion) follow this pattern, useful for naturalistic paths.
- **1D random walk** — at each step, move randomly up or down one unit; produces a sequence of hills and valleys (e.g., for a platformer skyline).
- **2D random walk** — start at a location and step in a random cardinal direction (north/south/east/west). Common practice: generate many candidate walks and discard those failing criteria (e.g., for a river, discard any walk that climbs in altitude or crosses a desert tile).
- **Loop-erased random walk (Wilson's algorithm)** — when the walk crosses itself, discard the entire walk and restart. To generate a maze: select start and end, run a loop-erased walk between them; then pick a random point on that path and run another loop-erased walk until it touches an already-walked cell; repeat until the maze grid is filled.
- **Random walk use cases** — river systems between mountains and water bodies; road systems between points of interest; cavern systems; connecting doors of separately generated rooms; sewer layouts.
- **Cellular automata** — broad family operating on a graph of discrete cells. Each cell has a state and a rule that updates it based on adjacent cells' states. Updates are typically applied to every cell simultaneously per step.
- **Conway's Game of Life** — canonical example on a 2D grid with two states (alive/dead); rules:

  | Current + Live Neighbors | New State |
  |---|---|
  | Live + 0 or 1 alive | Dead |
  | Live + 2 or 3 alive | Alive |
  | Live + 3 or 4 alive | Dead |
  | Dead + 3 alive | Alive |

- **Cave-map automaton** — initialize a 2D grid randomly with ~55% wall cells, leave a two-wide border, then iterate the rules:

  | Current + Wall Neighbors | New State |
  |---|---|
  | Open + 6–8 wall neighbors | Wall |
  | Wall + 0–4 wall neighbors | Open |

  Two passes on a random field yields a cave-like set of chambers; this is the technique used in *Caves of Qud*.
- **Cellular automata use cases** — spreading plants/forests; spreading fire; migration and proliferation patterns of animal populations.
- **Settling** — generate a set of overlapping shapes, give them rigid-body physics representations, and run a simulation that pushes overlapping shapes apart until none overlap. Yields a connected, non-overlapping arrangement of varied-size pieces.
- **Settling use cases** — pile of dungeon rooms with oversize colliders that settle and then connect with hallways; randomly shaped areas that settle into a cave system; straight and elbow pieces that settle into a sewer system.
- **Wang tiles** — squares with a colored side per edge; tiles are placed so adjacent edges share colors. In games, colors signify connection types (e.g., "blue" = door, "green" = hallway), guaranteeing properly connected layouts.
- **Aperiodic Wang tilings** — carefully chosen tile sets that tile the plane *without* repeating patterns. Not every (tile count, side color count) combination admits aperiodic tilings, but many such sets are known; some are as small as 11 tiles.
- **Wang tile use cases** — placing hand-built tiles with predefined edge connections to form 2D platformer worlds; placing detail tiles inside rooms; varying plant type and tree density across a forest with each tile carrying a hand-designed population.

## 6. Partitioning Space

- **Partitioning problem** — taking an undifferentiated space and dividing it into regions: landmasses into countries, countries into states, areas into pathfinding/decision-making units.
- **Binary space partition (BSP)** — split a space in half, then split each half, recursively, until a threshold (split count or average region size) is hit.
- **BSP with connection guarantees** — *Caves of Qud* generates many ruins this way: outline a building, pick a random column or row, place a wall splitting the area in two, then place a door on that wall. Because each split inserts a connecting door, every leaf region is reachable from every other.
- **BSP use cases** — placing smaller rectangular rooms inside each region and connecting them with hallways through the portals (Rogue-style layouts); filling an area with walls and doors to form connected rooms.
- **Voronoi diagram** — given a set of seed points on a plane, partition the plane so that the region of each seed contains exactly the points closest to that seed. Various distance metrics may be used. Best suited to continuous, uninterrupted spaces (e.g., continents); variants exist that respect obstacles.
- **Voronoi use cases** — farmed-field areas around farmhouses; territorial control of dragons around their lairs; encounter-difficulty zones around major dungeons.
- **Dijkstra map** — same partitioning idea as Voronoi but on a discrete graph (e.g., a square grid with 4- or 8-connectivity). Run breadth-first search from each seed, marking each node with its closest seed and the distance to it; regions form around seeds.
- **Dijkstra use in *Caves of Qud*** — random seeds are placed on a cave map until the largest region reaches a target size; resulting regions are populated with similar object counts, producing an even content distribution irrespective of the map's open-space layout.
- **Dijkstra map use cases** — finding the furthest point from a cave entrance for treasure or boss placement; evenly distributing encounters across non-uniform space; placing internal features (e.g., square buildings or tents) within irregular areas; filling national territories around capital cities.
- **Tree mapping** — partition a rectangular 2D field into rectangles whose areas are proportional to a list of input values. Algorithms trade off consistent visual aspect ratio against layout stability when values change.
- **Tree map use cases** — basic city street grids for buildings and blocks of known size; rooms of a side-view building given a list of room sizes.

## 7. Putting It All Together

- **Worked example: an "adorable little galaxy"** — composing the techniques in layers:
  - **Star positions** — 3D normal distribution generates a globular cluster of thousands or millions of stars.
  - **Per-star seeds** — assign each star a random seed, possibly hashed from its physical position so the seed is regenerable from location alone.
  - **Star type/temperature/size** — a weighted distribution picks the type (super giant 1a/1b, bright giant, giant, main sequence, white dwarf) with weights `1, 1, 2, 5, 20, 2`, mapped to temperature ranges and size buckets ("Mega huge!" down to Small); display color follows from temperature.
  - **Star names on demand** — when the player hovers a star, seed the PRNG with `(starseed + hash("starname"))` and run a Markov chain over syllables learned from a star-name catalog; fast enough to do in real time.
  - **Zoom-in detail** — weighted tables for companion stars, inner rocky planets, outer gas planets; per-planet seeds derived from hashing system + orbital identifiers (e.g., `Algotauri 4`).
  - **Planet zoom** — Perlin noise layers for topography; L-systems for city layouts; binary partition for individual building rooms; weighted tables for room contents; Markov chains for, e.g., the text on a notepad in a desk.
- **Closing image** — "Procedural generation opens endless doors in endless hallways to endless untracked worlds. Happy hiking!"
