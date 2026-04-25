# Ch 8: Level Design III: Architecture and Destruction

## Table of Contents

- [1. Windforge Context](#1-windforge-context)
- [2. Divide and Conquer Approach](#2-divide-and-conquer-approach)
- [3. The Seven-Step Architecture Process](#3-the-seven-step-architecture-process)
- [4. Discussion and Trade-offs](#4-discussion-and-trade-offs)

## 1. Windforge Context

- **Windforge** — a 2D action building-block RPG set in a floating-island dieselpunk world; nearly everything is destructible, players can build structures anywhere, and functional flying airships serve as long-distance transport.
- **Block-based world** — the world is almost entirely composed of blocks, which give substance to geometry (so destruction reveals meaningful interiors) and double as crafting materials.
- **Why PCG was unavoidable** — hand-authoring a world this size would have been impractical and tedious. Procedurally generated aspects, top-down: area definition and landmark placement, playable world areas, **architecture**, object placement, and enemy placement and spawning.
- **Chapter scope** — focuses on architecture generation: temples, dungeons, mines, and abandoned buildings.

## 2. Divide and Conquer Approach

- **Core idea** — a complete building or dungeon is complex as a whole but simple when decomposed into small individual sections.
- **High-level pipeline** — determine bounding area → recursively split into regions → assign high-level layout and connectivity → fill in blocks and objects.

## 3. The Seven-Step Architecture Process

| # | Step | What it does |
|---|---|---|
| 1 | Calculate the bounding box | Choose a target floating island (largest island for essential landmarks); generate a random bounding box constrained by per-architecture-type parameters for size, aspect ratio, placement, and overlap with the island |
| 2 | Split the box into regions | Recursive **axis-aligned binary splits** until a region's dimension gets too small (or stop early occasionally for variety); also maintain the connection info between regions for use in Step 4 |
| 3 | Skim perimeter regions | Remove perimeter regions to break out of the rectangle; different removal patterns yield different structures |
| 4 | Place connections | Build a region graph and traverse it to lay down typed connections; detect and drop any orphan regions left by Step 3 |
| 5 | Assign region types | Tag regions with intended purpose (treasure, boss, entrance, hub, trap) using priority rules |
| 6 | Make adjustments | Iterate the graph to refine connection types based on the regions they join |
| 7 | Generate the regions | First step that produces visible content: build walls, doors, backgrounds, platforms, and objects |

### 3.1. Splitting Strategies (Step 2)

Three primitive axis-choice rules, each with characteristic output:

| Strategy | Behavior |
|---|---|
| **Random axis** | Most variety, most unpredictable, can produce undesirable results |
| **Always shorter axis** | Long narrow regions; boring alone, useful in hybrids |
| **Always longer axis** | Similar-sized, near-square regions |

Windforge uses a **weighted-random hybrid** plus a chance of terminating splitting early to occasionally yield larger-than-normal regions.

### 3.2. Skim Patterns (Step 3)

The same machinery produces different structure types just by changing how perimeter regions are removed:

- **Embedded dungeons** — remove a random percentage of perimeter regions.
- **Building-like formations** — iteratively strip regions from the top.
- **Mines and mazes** — traverse the region connections in a way that avoids adjacent visited regions where possible, then remove unvisited regions.

### 3.3. Connection Graph (Step 4)

- Connection edges are tracked across every split, producing a graph where each region is a node connected to zero or more neighbors; each edge also carries the bounding region of the shared border to simplify later block and door generation.
- A **random traversal** of the graph guarantees every region is reachable without breaking walls; bias on the traversal (e.g., favoring horizontal moves) sets the predominant axis players travel on.
- Each traversed edge gets a weighted-random connection type. Types used in Windforge: **regular door**, **small opening**, **empty connection**, **trap door**, **boss door**, **treasure door**.
- Any region the traversal didn't reach is disconnected and can be safely removed.

### 3.4. Region-Type Assignment (Step 5)

Region types are assigned in order of importance using rule sets. Types include **treasure room**, **boss room**, **entrance room**, **hub region**, and **trap region**. Example placement rules:

- Place the boss treasure room in a terminal region far from the entrance.
- Place the boss room near the treasure room so the player must pass through it to reach the loot.
- Assign trap rooms to terminal regions with ceiling connections.
- Assign treasure and storage rooms to other terminal regions.

### 3.5. Connection Adjustments (Step 6)

The random connection types from Step 4 are revisited and overridden where the joined regions demand it:

- Empty connections between adjacent boss rooms.
- Trap doors on connections to trap regions.
- Treasure doors on connections to treasure regions.

### 3.6. Region Generation (Step 7)

- **Two responsibilities** — generate walls and connections between regions, and generate the contents of each region.
- **Subregion subdivision** — each region is further subdivided (similar in spirit to Step 2 but more flexible). Subregion types may divide into more subregions, and some emit custom procedural content such as background decorations or stairs.
- **Why subregions matter** — they tie platform and object placement to background patterns, making placements look intentional, and as long as objects fit a subregion's dimensions, they are guaranteed not to overlap.

## 4. Discussion and Trade-offs

- **Design priorities shaped the algorithm** — Windforge's open-endedness, easy create/destroy interaction, and traversal aids (grappling hooks, airships) let the team de-emphasize puzzle generation and precise platform placement; instead they prioritized varied, interesting places to explore at world scale.
- **Extensibility** — the seven-step structure made it easy to slot in new generation techniques for landmarks that feel distinct, and to produce dungeons, mines, small towns, and more just by varying Step 3's region-removal approach.
- **On-the-fly versus authored overrides** — most architecture is regenerated each visit, but major towns and a few quest-specific areas were generated once and then manually modified, blending procedural output with handcrafted polish where it was cost-effective.
