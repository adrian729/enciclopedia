# Ch 11: Puzzles

## Table of Contents

- [1. Defining a Puzzle](#1-defining-a-puzzle)
- [2. Puzzle-Spaces](#2-puzzle-spaces)
- [3. Required Outputs](#3-required-outputs)
- [4. Generation Approaches](#4-generation-approaches)
- [5. Desktop Dungeons Case Study](#5-desktop-dungeons-case-study)
- [6. Player Hope as a Resource](#6-player-hope-as-a-resource)
- [7. Conclusion](#7-conclusion)

## 1. Defining a Puzzle

- **Operational definition** — a puzzle has a determined starting state, an end/goal state, and a set of atomic actions players use to move from one to the other. The full state may be hidden from the player but is always known internally.
- **Generator's job** — given that frame, decide which puzzles can usefully be procedurally generated and what the system must output.

## 2. Puzzle-Spaces

> **Puzzle-space** — the abstract space populated by every single puzzle that could emerge out of a set of gameplay rules.

| Axis | Term | Meaning |
|---|---|---|
| Size | **Large** | Many distinct start/goal pairs |
| Size | **Small** | Few distinct start/goal pairs |
| Depth | **Shallow** | Each start has exactly one goal state |
| Depth | **Deep** | A start has multiple viable goals (or a goal has multiple starts) |

- **Where humans beat algorithms** — extreme ends of the spectrum. One-shot puzzles whose appeal is a novel twist, setting, or presentation need a human in the loop. Vast or extremely deep puzzle-spaces also need humans to cherry-pick standout goal states (humor, novelty); generators in those spaces produce too-similar, boring puzzles.
- **Where algorithms shine** — variations on a theme drawn from a large but reasonably uniform puzzle-space.

## 3. Required Outputs

A generator typically trims a larger puzzle-space into an easily-randomized subset; complete games often run multiple generators (or parameterized samplers) over different regions of the puzzle-space.

- **Solvability** — every produced puzzle must actually have a goal state players can reach. Without this, the generator wastes the player's time.
- **Continuous solution** — players must be able to progress from start to goal by following the rules; atomic actions should drive them toward the goal. Counterexample: the *Gabriel Knight* cat-hair-mustache puzzle. Sudoku puzzles with multiple solutions are discontinuous because the player must arbitrarily choose a value rather than deduce it.
- **Continuity is compatible with depth** — removing walls in a single-path maze to add multiple viable paths keeps it continuous; only removing enough adjacent walls to make traversal actions meaningless renders it discontinuous.
- **Determinism (optional)** — not required for viable puzzles, but speeds debugging, lets players replay the same puzzle, and is essential for shared "daily" puzzles.

## 4. Generation Approaches

| Approach | How it works | Best fit | Caveats |
|---|---|---|---|
| **Random start state** | Generate an initial state directly, relying on the rules to make it solvable | Information-revealing puzzles with deep spaces and few axes of differentiation; *Minesweeper* (mines placed at random; players deduce positions) | Game rules must guarantee solvability and continuity automatically |
| **Backward from goal state** | Generate a goal, then repeatedly undo random atomic player actions until the desired complexity is reached | Shallow puzzle-spaces with high information transparency where players follow a single-path solution; word search puzzles, math puzzles | Player actions must be bidirectional (no info introduced during play); track previous states to avoid loops/shortcuts |
| **Heuristics** | Game-relevant rules layered on any of the above, often as disqualification states that force regeneration | Any approach that needs richer or faster-to-validate puzzles | Heuristics like Sudoku difficulty calculations are post-generation; you keep regenerating until one matches the desired rating |
| **Permutations** | Transpose elements of an existing valid puzzle while preserving solvability and continuity | Adding variety to an existing pool | Cannot create puzzles from nothing; needs a sample size large enough that players can't reverse-engineer the permutation rules |

- **Random start as designer inspiration** — for very broad puzzle-spaces, randomly generated states need not even be playable; designers can mine them for serendipitous arrangements to polish into hand-tweaked puzzles.
- **Heuristic examples for Minesweeper** — guarantee the player's typical first-click squares are mine-free; suggest or auto-play a safe first move; reposition mines that produce discontinuous states.

## 5. Desktop Dungeons Case Study

- **Premise** — *Desktop Dungeons* is a puzzle roguelike with disposable adventurers in single-screen 20x20 dungeons. Started as a 48-hour prototype by Rodain Joubert exploring a 10-minute roguelike; went through alpha, year-long beta with weekly updates, and 2015 update.
- **More puzzle than roguelike** — immobile enemies that only attack when attacked, deterministic combat (game shows 100%-accurate projected attack results), granular resources, and UI tuned to make calculated truths instinctively graspable.
- **Exploration as resource** — players regenerate health and mana by uncovering new terrain (pushing back fog of war), which also regenerates damaged enemies. Turns "boring" exploration into the core economic decision: when, where, and how to explore.
- **More roguelike than puzzle** — permadeath is hostile to puzzles but produces the tension that drives roguelike storytelling. Resource economy trades health, mana, experience, black space, gold, items, gods, piety, conversion points, and inventory space against each other in non-atomic ways with side effects, requiring intuitive feel rather than strict planning.

## 6. Player Hope as a Resource

- **Knife-edge balance risk** — when every run feels one wrong move from defeat, players assume early defeat even when a path still exists. Players are usually wrong about early defeats: the game is about uncovering resource-economy efficiencies they don't yet know.
- **Difficulty = forgiveness of resource-spending values** — tuned to push at the boundary of player skill while skill itself grows.
- **Train players to keep trying** — deep puzzle-space gives a large buffer for non-optimal actions across many solution paths. But this only holds if no run is *actually* unsolvable; an unsolvable run shatters the optimism.

**Why standard solvability tools failed here:**

- **Rules-based solvability** — impossible because hidden information in black space forced irreversible decisions in discontinuous puzzle states.
- **Backward-from-goal** — possible, but the resulting single-path solutions were too unlikely for players to find given the breadth of available actions.
- **Solver-based proof** — two blockers: defining "good enough" solution counts and producing varied-enough searches; and the prohibitive cost of writing an AI capable of playing *Desktop Dungeons*, a game so hard the team couldn't afford the engineering.

**The original quick-and-dirty pipeline:**

- Clear lines of walls until enough contiguous walkable space exists.
- Place up to 40 monsters (including bosses) randomly on the map.
- Add pickups and interactive items in empty spaces.
- Place the player and clear a 3x3 space around the start.
- Failure mode: high-level enemies surrounding low-level players blocked progress because the experience needed to level up cost more health and mana than the player could pay.

**Heuristics that fixed it (without abandoning random start-state generation):**

- **Minimum spawn distance for high-level enemies** — high-level monsters spawning too close to the player reroll their position. No maximum distance, so easy enemies still spawn anywhere; pickups tend to fall in easy-to-reach spots as a side effect.
- **Counter-effect** — depopulated starts caused players to skip nearby low-level enemies, wasting exploration on pickups instead of using fights to refill resources via post-fight regeneration.
- **Low-level enemy clustering** — low-level enemies search near their random spawn for positions that block player movement. Reproduces the original "blocked-in" layouts but with level-1/2 fights, not unbeatable level-5+ walls; also lets enemies cooperatively block wider areas.
- **Bias useful glyphs toward player start** — spells (mana-spending world effects) that are useful at low levels spawn closer to the start, mirroring the high-level monster bias in reverse, giving players extra options to deal with blockages.
- **Preparations metagame** — players bring items into a run at a cost; raises resource efficiency and supplies blockage-handling tools.

**Validation:**

- **Doubledoom dungeon** — a callout to the alpha that deliberately omits all positioning heuristics and warns players it might be impossible. Modern unfair-dungeon complaints are now almost exclusively about Doubledoom; veterans ask new complainers if they were playing it.
- **Daily dungeon record** — across 500 seeded daily dungeons, every one has been beaten by at least 32 players. The 32-player threshold filters extreme difficulty; no truly impossible dailies have shipped.
- **Caveat** — the team still does no real solvability checking; statistical heuristics may only make unfair starts less likely, not eliminate them.

## 7. Conclusion

- **Define needs in puzzle-space terms** — depth/shallowness, viable solution paths, whether solvability must be guaranteed, and continuity. The chosen approach depends on the interaction between player actions and the information the game presents.
- **Start naive** — learning what makes a bad puzzle is as important as producing good ones in a new puzzle-space; layer heuristics on once requirements and player limits are clearer.
- **Prefer broad coverage over narrow specificity** — pruning unwanted puzzles from a generous generator is easier than coaxing variety out of an over-constrained one.
