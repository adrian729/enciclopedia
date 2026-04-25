# Ch 9: Cyclic Generation

## Table of Contents

- [1. The Cyclic Approach](#1-the-cyclic-approach)
- [2. Graph-Based Pipeline](#2-graph-based-pipeline)
- [3. Level Design Patterns](#3-level-design-patterns)
- [4. Lock-and-Key Attributes](#4-lock-and-key-attributes)
- [5. From Graphs to Tilemaps](#5-from-graphs-to-tilemaps)
- [6. Discussion](#6-discussion)

## 1. The Cyclic Approach

- **Drilling-out generators produce trees** — the popular method (e.g., Brogue) drills tunnels and rooms outward from an entry point. Guarantees accessibility but yields branching dead ends and forced backtracking; Brogue mitigates by sprinkling random doors between branches.
- **Cycles instead of trees** — Unexplored connects start and goal with two paths instead of one, creating a loop. Real-world cities, buildings, parks, and most interesting tabletop dungeon maps are full of cycles; trees are rare.
- **Why cycles matter** — both paths can offer different challenges (one shorter but more dangerous, one one-way as a return route after finding a key, one hidden). Nesting cycles produces richer levels than branching.
- **Unexplored context** — a real-time roguelike modeled on top-down Zelda, with melee combat and lock-and-key puzzles. Levels are smaller and theme-focused (lava, water, teleporters), making cyclic structure especially effective.

## 2. Graph-Based Pipeline

- **Tilemaps are bad at cycles** — Unexplored represents level structure as a graph during initial generation, converting to a tilemap only halfway through.
- **Model-driven engineering** — automated generation runs as multiple steps where each step's output is a model meaningful on its own, passed to the next step. Different model *types* (graphs vs. tilemaps) at different stages preserve structural information across distances.
- **Generic nodes first** — early graphs have generic rooms, obstacles, locks, and keys; exact themes and properties are pinned down later.
- **Transformational graph grammars** — rules look for a pattern on the left-hand side and replace it with the pattern on the right-hand side. Numbered nodes match between sides. Used to grow simple graphs into cycles, lock-and-key chains, and full dungeon structure.
- **Node attributes** — rooms, locks, keys, and edges carry attributes (theme, structural function) that grammar rules can read and write, e.g., dispatching different rules for a "shrine" vs. an "armory."

## 3. Level Design Patterns

- **Pattern-driven generation** — graph rules let the generator manipulate recurring level-design patterns directly, deliberately maximizing positives (e.g., rewarding shortcut for thorough exploration) and minimizing negatives (e.g., shortcut bypassing too much content).
- **The a/b path skeleton** — most levels start with a starting point, a goal, and two paths: `a` from start to goal, `b` from goal back to start. Patterns are selected based on the relative and absolute lengths of `a` and `b`.
- **Example — short a, long b** — place a locked door at the goal and the key at the end of `b` near a cut-back to the main path. Player meets the lock first, finds the key after the long path, and only walks a short distance back.

| Pattern | Shape |
|---|---|
| **Two alternative paths** — long `a`, long `b`; both routes are full challenges | parallel cycle |
| **Hidden shortcut** — long `a`, short hidden `b` | secret-door cycle |
| **Lock-and-key cycle** — short `a` blocked by lock; long `b` reaches the key | classic |
| **Patrolled cycle** — short `a`, short `b`; a patrolling monster sweeps the loop | dynamic threat |
| **Double-key cycle** — two keys plus a valve gating progression around the loop | layered |
| **Key behind valve** — key sits past a one-way valve, forcing route choice | one-way gating |
| **Dramatic cycle** — increasing monster density along one route ramps tension toward the goal | escalation |
| **Dangerous route** — visible reward sits across a hazardous shortcut | risk/reward |
| **Collapsing bridge** — one-way crossing that severs the return path | forced commitment |
| **Unknown return path** — outbound route is clear but the way back is hidden until later | asymmetric exploration |
| **Lure and setback** — visible reward draws the player off-course into a setback | trap |
| **Gambit** — embedded sub-cycle with optional risk for optional reward | side bet |
| **Simple lock and key** — straight pairing of one lock and one key | baseline |

## 4. Lock-and-Key Attributes

Unexplored marks locks and keys with attributes drawn from a formal taxonomy. This avoids deadlocks while widening variety, especially because many game mechanics (potions, scrolls, levers, jumps) double as keys.

| Axis | Values | Meaning |
|---|---|---|
| **Lock barrier type** | conditional / dangerous / uncertain | Conditional = binary, can't pass without key (locked door). Dangerous = passable at a cost (lava lake). Uncertain = passable if found (secret door). Keys to dangerous/uncertain locks reduce risk or increase certainty. |
| **Lock duration** | permanent / reversible / temporary / collapsing | Permanent stays open forever (safest). Reversible can relock. Temporary auto-closes; can act as a valve. Collapsing allows one passage only. |
| **Lock directionality** | valve / asymmetrical | Valves traverse one direction only (e.g., dropping from a high ledge; valves do not always need a key). Asymmetrical locks can only be opened from one side but, once open, traverse both ways. Used in patterns to prevent the player from entering the wrong arc of a cycle. |
| **Lock safety** | safe / unsafe | Safe = guaranteed solution exists; unsafe = no such guarantee. Dangerous and uncertain locks are inherently safe. Conditional locks on the main path must be safe. |
| **Key purpose** | single-purpose / multipurpose | Multipurpose keys serve other functions too (Zelda's bow as both weapon and switch-hitter); single-purpose keys are dead weight in the inventory. |
| **Key particularity** | particular / nonparticular | Particular keys unlock exactly one lock (real-world keys); nonparticular keys can fit multiple locks (Zelda small keys). Nonparticular keys can preempt locks, softening rigidity. |
| **Key persistence** | consumed / persistent | Consumed keys disappear on use (Zelda small keys, a potion-of-resist-fire used to cross lava). Less safe, especially when combined with multipurpose keys. |
| **Keys fixed in place** | fixed-in-place keys | Levers and switches are the canonical example (and usually single-purpose, particular). A single fixed key on one side makes the lock asymmetrical; locks triggered by fixed keys are best made permanent (not reversible) and given clear feedback on door status. |

- **Two-direction solvability** — Unexplored requires returning up the dungeon with the Amulet of Yendor, plus mechanics that bypass locks involuntarily (jumping into chasms, scroll of descend, scroll of teleportation). Many lock-and-key puzzles must therefore be solvable in both directions; attributes prevent the resulting deadlocks.
- **Nonconditional locks** — dangerous and uncertain locks are automatically two-way and easier to wire to varied game mechanics.

## 5. From Graphs to Tilemaps

- **The conversion problem** — graphs encode abstract structure (adjacencies, which key unlocks what, who patrols where), but the renderer needs a 2D tilemap with concrete wall, door, key, and enemy positions.
- **Grid-laid graph trick** — Unexplored builds the graph on a grid layout from the start, storing topological data in node attributes. All graph transformations run on this grid-graph, so mapping to tilemap is mechanical.
- **Resolution refinement** — the tilemap starts with one tile per node/edge, then resolution is increased and further transformation rules expand rooms, place features, and decorate the dungeon.

## 6. Discussion

- **Two to five cycles per level** — gives each level a recognizable shape and a manageable navigational challenge. More cycles clutter the level; the combinatorial space of patterns is already huge with a handful.
- **Why cycles work** — they express more interesting patterns than paths. T-joins or parallel symmetrical branches might do similarly; cycles are simply the most powerful structure encountered so far.
- **Beyond dungeons** — the underlying workshop also targeted parks and meditative gardens (people prefer hikes without backtracking). Open game spaces and world maps can use cycles drawn around forests, lakes, and mountains, with dangerous shortcuts as cross-links and prominent sites at cycle intersections.
