# Ch 7: Level Design II: Handcrafted Integration

## Table of Contents

- [1. Why Mix Handcrafted Rooms with PCG](#1-why-mix-handcrafted-rooms-with-pcg)
- [2. Standard Dungeon Generation](#2-standard-dungeon-generation)
- [3. Crypt Generation](#3-crypt-generation)
- [4. Comparison of the Two Approaches](#4-comparison-of-the-two-approaches)
- [5. Best Practices](#5-best-practices)

## 1. Why Mix Handcrafted Rooms with PCG

- **Hybrid goal** — bolstering procedural environments with handcrafted rooms adds variety and depth while steering players toward the parts of the game system the designer wants to showcase.
- **Dungeonmans adventure zones** — Shepard used the technique to build graveyards, fallen castles, crypts, friendly towns, mighty towers, and standard dungeons, each with its own algorithm and feel.
- **Room data format** — plain ASCII text files where each character maps one-to-one to a tile. Stored as `x × y` rectangles but the *playable* shape inside can be irregular, which makes layered placement far more visually interesting than packing only rectangles.
- **What handcrafted data omits** — external walls (added by area-gen code) and enemy/treasure spawns (handled procedurally so frequently visited rooms don't feel stale).

## 2. Standard Dungeon Generation

- **Goal** — extend traditional "room and hallway" gameplay with shapes that exploit Dungeonmans' position- and motion-based player powers and let dynamic enemies shine.
- **Initial state** — define a playfield where every tile is **unused space** (a blank protodungeon block, distinct from "empty floor"); place a starter room (typically containing the stairs back up).
- **Iterative loop** — repeat until a target room count is hit or no valid placements remain:

| Step | Action |
|---|---|
| 1 | Find all wall tiles that have two neighboring walls along the same axis *and* are exposed to unused space — these become **candidates**, dropped into a "jellybean bag" for random draw |
| 2 | Pull a candidate; decide room or hallway; pick a random handcrafted room and align it against the candidate |
| 3a | Fits → place the room, drop a door at the candidate's position, recompute the candidate set |
| 3b | Doesn't fit → discard, return to Step 1 (do *not* dynamically carve the room to fit — that loses authored design value and homogenizes shapes into rectangles) |
| 4 | Convert any unused-space tile adjacent to a new floor tile into a wall |

- **Optional spice-up pass** — add doors between adjacent doorless rooms (creating circular routes that reduce backtracking), widen long openings with adjacent extra doors (preventing easy enemy funneling into bottlenecks), and add secret doors.
- **Authoring guideline** — make many handcrafted rooms; the player will see them often, so combinatorial variety matters. Mix large arenas, twisting paths, grand hallways, tight room clusters, and open spaces with cover.

## 3. Crypt Generation

- **Goal** — arrange handcrafted areas procedurally as in standard dungeons, but produce tight catacomb-style passages punctuated by larger chambers for breathing room.
- **Room data** — each room is a fixed **7×7 block** with cardinal-direction exit indicators (N/E/S/W) and additional data for treasure and statue placements that sell the creepy crypt aesthetic.
- **Loose edges** — rooms aren't always solid; some edges have multiple openings that, when aligned with neighbors, read as larger rooms, endcaps, or open atria.
- **Exit-list bucketing** — at load time, rooms are sorted into four lists by which cardinal exits they offer. A room with multiple exits appears in multiple lists.
- **Algorithm** — place a starter room with at least two exits; repeatedly pick a placed room with an unmatched exit, draw a new room from the list whose opposite exit matches, place it adjacent on a grid, and recalculate. When no unmatched exits remain, evaluate the result against a minimum room count — if too small, **discard the dungeon and start over**.
- **Pseudocode summary** — `GoalCount = 40`, capped at 1000 attempts per generation; bounds-checked placements; whole layout retried on failure; final pass to "salt dungeon to taste" once a valid layout exists.
- **Sensory pairing** — crypt-specific art and enemy roster (hordes that pressure down hallways, ice enemies with controlling powers) reinforce the structural difference from standard dungeons.

## 4. Comparison of the Two Approaches

| Aspect | Standard Dungeon | Crypt |
|---|---|---|
| Room shape | Irregular shapes inside rectangular bounds | Fixed 7×7 grid blocks |
| Placement rule | Adjacent to wall **candidates** drawn from a jellybean bag | Aligned on grid where exits match |
| Connectivity | Door dropped at candidate position post-fit | Implicit via matching cardinal exits |
| Failure handling | Skip the room, keep building | Throw the whole dungeon out, restart |
| Spawn data | Treasure/enemies fully procedural | Treasure and statue locations baked into room data |
| Resulting feel | Varied combat arenas, circular routes, secret doors | Tight catacombs with chamber breathers |

## 5. Best Practices

- **Keep the data simple** — fast iteration matters; for tile-based games, plain text files in a plain text editor beat any custom format.
- **Keep the data lean and purposeful** — don't pre-populate every detail. Let procedural systems place creatures, treasure, and traps so players can't memorize every threat upon entering. Place specifics only when there's a clear design reason.
- **Don't write an editor** — building a custom editor mid-project is the surest way to derail momentum. Notepad ("nature's perfect fruit") or existing well-tested tools are faster than rolling your own. Verify the complexity is genuinely needed before investing.
