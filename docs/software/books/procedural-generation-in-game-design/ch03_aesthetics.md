# Ch 3: Aesthetics in Procedural Generation

## Table of Contents

- [1. Aesthetic Rules as a Shared Language](#1-aesthetic-rules-as-a-shared-language)
- [2. The Generator as a Team Member](#2-the-generator-as-a-team-member)
- [3. Sunless Sea: Atmosphere Goals](#3-sunless-sea-atmosphere-goals)
- [4. Establishing the Tile Rules](#4-establishing-the-tile-rules)
- [5. Blurring Tile Boundaries](#5-blurring-tile-boundaries)
- [6. Lessons from the Result](#6-lessons-from-the-result)

## 1. Aesthetic Rules as a Shared Language

- **Aesthetic guides as a coherence engine** — a collection of rules that lets the team communicate themes, sense of place, and story consistently across the project. Without them, today's work clashes with yesterday's.
- **Rules as a safe-experimentation envelope** — they set parameters within which solo developers (and the generator) can improvise without producing something inappropriate for the game.
- **Team alignment** — when more than one person contributes, every individual addition must add up to a coherent whole; rules are how that gets enforced.
- **Account for team strengths** — design rules should bend toward the team's actual technical execution. Imprecise rules get interpreted in unpredictable ways; embrace creative differences instead of fighting them.

## 2. The Generator as a Team Member

- **Treat the generator as a teammate** — it produces work to your rules and is granted some "creative freedom" (usually simulated via randomness).
- **Its strengths** — follows hard-and-fast rules to the letter at scale.
- **Its weaknesses** — falls short on judgments in less strictly defined areas. Identify where it will need help in advance and grant more control to human team members in those zones.

## 3. Sunless Sea: Atmosphere Goals

- **Core experience** — atmosphere and exploration were as important as survival and danger; the game is about leaving the familiar and traveling into the unknown.
- **Why vary the map per playthrough** — to keep threat and freshness alive even after the player learns the setting; no journey should feel like a safe place.
- **Design tension** — variety must not feel arbitrary. The player should still gain skill and understanding, and the world must feel coherent in hindsight even when each discovery is fresh.
- **Greatest fear** — tonally jarring contrasts that throw the player out of the world rather than draw them in. The generator's job was to produce surprise that still felt natural.

## 4. Establishing the Tile Rules

- **Grid-and-tile approach** — chosen because rules for tile placement could be simple enough for the entire team (not just designers and coders) to understand.
- **Original layout: 18 × 18 grid** — each tile holds content (creature, island, geographical feature). Rules constrained which tile types could be placed to the north and east of each tile.
- **Region categories** — tiles sorted by style and difficulty. Blue tiles (icebergs, snowstorms) sit in the north, purple tiles (most alien flora and fauna) sit in the far east.
- **Subcategory trap** — adding ever more specific subcategories to fix aesthetic dissonance reduced variety and randomness; over-constraint defeats the point.
- **Reduction to 6 × 6** — areas naturally read as coherent in 3 × 3 chunks (a few islands, some aquatic features, a sea beast or two), so the grid was shrunk. Fewer tiles allowed more lenient placement rules without losing harmony.
- **Final layout** — 36 tiles total: 24 split across five regions and 12 in fixed positions. Each tile can be placed anywhere within its region, increasing variety without subdividing further.
- **Neutral bridging regions** — clashing aesthetic regions are guaranteed to never adjoin, because neutral bridge regions sit between them.
- **Unifying stylistic rules** — color, lighting, sound, and music rules prevent atmosphere clashes between visuals and audio; long stretches of open water also dampen the uglier transitions.

## 5. Blurring Tile Boundaries

- **Smoothing transitions** — tile rules prevent discordant alignments, but adjacent tiles from different regions still need their joins eased.
- **Intent-aware sea color** — when the player crosses a tile boundary, the system detects whether they intend to continue (vs. zigzagging back) and only then slowly shifts the sea's color, changing atmosphere without a jarring transition.
- **Music gating** — the same intent check decides whether to introduce a new musical theme; the absence of music is treated as an active atmospheric tool, with new tracks introduced only when clearly appropriate to avoid shunting between cues.
- **Boundary-ignoring weather** — the generator places weather effects across tile boundaries (e.g., snow on a non-snowbound tile adjacent to a northern one, rarely), so each tile doesn't feel like an isolated rock pool.

## 6. Lessons from the Result

- **Tradeoff of the puzzle-piece approach** — treating each tile as a piece that can slot into many arrangements forces extra effort to make assets fit every neighbor.
- **Mitigation through coherent assets** — the generator was fed pieces that are visually and aurally of-a-piece: restrained, harmonious palette; consistent contrast; uniform shapes and sizes. Lined up, they show evolution and subtle variation.
- **Regretted decision: handcrafted variants per tile** — adding random per-session variants of each tile was time-consuming, error-prone, and hard to debug.
- **Key lesson** — sometimes it is better to accept the limitations of your PCG approach than to patch over them with manual solutions.
- **Zubmariner's procedural answer** — the underwater expansion reuses the surface tile rules and hands more control to the generator: it picks atmospherically appropriate terrain and decorations from a predefined list and places them in unoccupied map areas at an artist-tunable density, replacing manual variant placement with procedural logic.
