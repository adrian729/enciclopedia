# Ch 6: Level Design I: Case Study

## Table of Contents

- [1. Game Premise and Why PCG](#1-game-premise-and-why-pcg)
- [2. Level Composition Goals](#2-level-composition-goals)
- [3. Generation Rules](#3-generation-rules)
- [4. Generation Pipeline](#4-generation-pipeline)
- [5. Outcomes and Limitations](#5-outcomes-and-limitations)

## 1. Game Premise and Why PCG

- **Catlateral Damage** — a casual physics-based 3D FPS where the player is a house cat knocking the owner's possessions onto the floor across houses, a supermarket, a museum, and a mad scientist's laboratory.
- **Two modes** — timed *Objective Mode* with a primary goal (e.g., 150 objects floored) plus an optional secondary goal (e.g., 15 blue books); seeds can be saved and replayed in untimed *Litterbox Mode*.
- **Solo-developer rationale** — Chung initially planned hand-built levels but switched to PCG after a few months: it saved time long-term and unlocked far more arrangements than he could author by hand, increasing replayability. First-time PCG project, kept deliberately basic.

## 2. Level Composition Goals

- **Cartoony simulation of real interiors** — each level is a one-floor interior divided into purpose-specific rooms (bedroom, bathroom, kitchen, living room) with appropriate objects per room.
- **"Building → rooms → furniture → physics objects" mental model** — levels are layered: bounded space, partitioned rooms, themed furniture acting as platforms, and physics objects sitting on the furniture.
- **Tiered furniture heights** — furniture must double as platforms, so models are built at heights the cat can jump between.
- **Achievable objectives** — primary objectives must be completable within the time limit on every generated level.

## 3. Generation Rules

- **Building rules (early constraints)** — interiors only, single floor only. Interiors avoid the boundary problem of outdoor space and guarantee enough knock-down clutter; single floor avoids stair generation.
- **Room rules (aesthetic believability)** — at least one room per building; each room declares its size class (kitchens/living/dining large, bathrooms small), a door cap (private rooms = 1 door, public rooms = many), and the furniture types it permits. Only functional rooms are placed — entryways, hallways, and closets are excluded due to specific placement needs and small sizes.
- **Furniture rules (gameplay)** — placement must not block doorways or other furniture, must leave floor space for objects to land on, and follows real-world habits (against walls or in the middle). Each furniture piece declares which physics objects can sit on it, plus per-object probability, allowed surfaces, and rotation behavior (match furniture orientation, e.g., a TV faces away from the wall, or randomize for variety).
- **Objective rules** — primary must be attainable; secondary uses only object types actually present in the level; time limit must be tight enough to stay challenging.

## 4. Generation Pipeline

Three sequential steps produce the level, then objectives are derived from the result:

1. **Partition the building into rooms** — a hard-coded per-level-type data file specifies overall size, room set, and textures. A **squarified treemaps algorithm** divides the bounding rectangle into smaller rectangles as close to squares as possible, with open doors between them.
2. **Place furniture in each room** — driven by per-room data files (max count per furniture type, selection probability, wall-aligned flag, player-spawn flag). Each furniture object carries a model, physics colliders, an invisible bounding box (preventing overlap and over-close placement), and rectangular surface areas that accept physics objects.
3. **Place physics objects on furniture** — surface scripts list allowed objects with probabilities and rotation rules; a **rectangle packing algorithm** fits the objects' rectangular bounds inside the surface areas (e.g., onto bookcase shelves).
4. **Derive objective and time limit** — all placed physics objects are tallied in a dictionary; primary objective, secondary objective, and a higher-value bonus object are picked as percentages of those totals so they are always attainable. Time = primary count × **1.4 seconds per object** (measured average), giving e.g. 210 s for a 150-object goal.

## 5. Outcomes and Limitations

- **Authorability inside the ruleset** — the system can group related items as a unit (a dining table with chairs, a row of books) so handcrafted arrangements coexist with generation.
- **Players don't notice it's procedural** — feedback shows levels read as handmade. Double-edged: the polish convinces players, but they may also mistake nine generated level *types* for nine static levels and underestimate the content.
- **Failure cases** — rare furniture-placement glitches in tight spaces (washers, dryers, and sinks blocking the toilet in narrow bathrooms).
- **Wishlist** — minor polish like a permanently closed front door, plus larger features such as multiple floors, were cut for time and the developer's PCG inexperience.
