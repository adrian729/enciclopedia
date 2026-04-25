# Ch 22: Understanding the Generated

## Table of Contents

- [1. Why Look Beyond Single Outputs](#1-why-look-beyond-single-outputs)
- [2. Expressive Range and Generative Spaces](#2-expressive-range-and-generative-spaces)
- [3. Qualities of the Generated](#3-qualities-of-the-generated)
- [4. Qualities of the Generator](#4-qualities-of-the-generator)
- [5. Visualizing Expressive Range](#5-visualizing-expressive-range)

## 1. Why Look Beyond Single Outputs

- **Generators make spaces, not artifacts** — QA must cover every potential output of the software, not a handcrafted set; eyeballing a few "generate" clicks misses biases hidden in the bulk of the space.
- **Running example: Launchpad** — a parameterized generator for Mario-like 2D platforming levels supporting static platforms, moving platforms, gaps, springs, pacing enemies, and stompers. Used throughout the chapter to illustrate metrics and visualizations.

## 2. Expressive Range and Generative Spaces

- **Generators as minidesigners** — each has its own style, quirks, strengths, and weaknesses, all highly sensitive to underlying data and algorithms.
- **expressive range** — the potential range of content the system as a whole might create across all parameter and code configurations.
- **generative spaces** — the content space produced by a single fixed instantiation (fixed parameters + codebase). The expressive range is made up of many generative spaces; changing a parameter or a line of code yields a new one.
- **Core questions a single generative space must answer** — how different are the millions of outputs from each other, is the system biased toward certain content, and are the few visible samples representative or stuck in a corner of the space.

## 3. Qualities of the Generated

- **Step 1: name the qualities you care about** in individual artifacts before you can characterize the space they fill. Four types adapted from prior research:

| Type | Describes | Example for a level | Example elsewhere |
|---|---|---|---|
| **Topological** | Underlying structure, independent of skin | Loops, cycles, branching of player path | Length or arc shape of a generated story |
| **Experiential** | How the player interacts with and experiences content | Rhythm of movement, difficulty estimate | Number of solutions in a puzzle, target strategies |
| **Aesthetic** | Visual and auditory qualities | Color palette, warm/cool balance, contrast | Salience used to highlight features |
| **Semantic** | Real-world meaning of what is created | (no level example given in source) | Share of clothing reading masculine vs. feminine in a character creator |

- **Launchpad's two example qualities** —
  - **Linearity (topological)** — vertical change in platform heights across a level; flat or steady-slope levels score high, curvy levels score low.
  - **Leniency (experiential)** — how forgiving challenges are when the player fails; gap-laden levels score low, levels of safe jumps score high.
- **Other qualities one could track** — **density** (aesthetic: screen space taken by elements vs. open space) and **risk–reward ratio** (experiential: average reward per risky maneuver).
- **Formalizing qualities into metrics** — turn each quality into an algorithm that produces a number, ideally normalized to `[0, 1]` and cheap to compute, so thousands of outputs can be scored and compared.
- **Linearity metric for Launchpad** — fit a line through platform midpoints by linear regression, then average the absolute distance of each platform from the line. Captures *how linear*, not *which line* — a flat level and a steady upward slope score the same; a slope-aware variant could use the line's gradient.
- **Leniency metric for Launchpad** — assign a per-element score to the seven obstacle types and average over the level's elements:

| Score | Element |
|---|---|
| 0.0 | Gaps, enemies, long falls |
| 0.25 | Springs, stompers |
| 0.75 | Moving platforms |
| 1.0 | Jumps without a gap |

- **Formalization is necessarily lossy** — no metric perfectly captures fun, beauty, or difficulty; e.g., the leniency metric ignores ordering and clustering of hazards. Acceptable as long as the gap between the formal score and the fuzzy quality is kept in mind during interpretation.
- **metrics versus requirements** — generate-and-test or optimization-based generators already encode some desired features as a fitness function. Those constraints are useful to look at ("how often does the generator hit its own requirements?") but understanding emergent qualities means measuring features the generator does *not* already enforce. Launchpad illustrates this: its requirements concern rhythmic pacing, while linearity and leniency are emergent and unconstrained by the input parameters.

## 4. Qualities of the Generator

- **A generative space as an n-dimensional plot** — every output is scored by each metric and plotted at that point; for Launchpad, linearity × leniency gives a 2D space.
- **Variety** — high variety means broad coverage of the space, ideally with at least one piece of content at every point. More usefully, variety can be characterized per metric: a generator can be high-variety in color palette while low-variety in risk–reward.
- **Unintentional bias** — uneven density across the space reveals where the generator over- or under-produces; valuable to detect before shipping (e.g., the share of feminine-coded characters a player is likely to see).
- **Responsiveness** — how the generative space shifts when inputs change. Small parameter or data tweaks can propagate unpredictably; tracking the space across changes builds an understanding of the full expressive range.
- **Content families** — clusters of similar outputs that sit far from other clusters; a generator's recognizable "style," whether intentional or an artifact of the system.

## 5. Visualizing Expressive Range

- **Two visualization strategies** — heatmap **histograms** of metric scores and **distance-based clustering**.
- **Histograms** — 2D heatmaps of a generative space where brightness encodes density of outputs at each point; bright clumps reveal what the generator *most often* produces, dark zones reveal what it cannot or rarely produces.
- **Side-by-side histograms expose hidden bias** — for Launchpad, comparing histograms across all combinations of rhythm length/type/density showed that regular rhythms bias the system toward highly linear levels and short swing-beat rhythms unlock greater leniency variety. Single-output inspection misses this because the same rough regions stay covered, just with very different frequencies.
- **2D-slice limit and box plots** — a 2D heatmap shows only one slice of a higher-dimensional space; box-and-whiskers plots trade shape information for compact mean/median/standard-deviation views across many metrics, useful for side-by-side generator-version comparisons.
- **distance-based clustering** — alternative for high-dimensional spaces; group outputs into clusters and visualize cluster size and membership over time. More implementation effort, but exposes emergent content families. Launchpad's tool shows clusters as colored rectangles sized by membership; selecting one (e.g., a cluster of upward-sloping levels with many stompers) lists every level in that family.
- **Distance functions are flexible** — Launchpad uses **edit distance** between level segments (edits to convert level A into B), but Euclidean distance in the metric space, or any function that returns small for similar and large for dissimilar pairs, will work.
- **Why this pays off** — for designers, expressive-range views show the range of content a player might (or might not) ever see, guiding both the generator and the surrounding game. For developers, watching the generative space evolve across builds catches bugs (a small code change radically reshaping the space) and reveals emergent consequences of seemingly local decisions.
