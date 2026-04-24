# Ch 20: Spatial Partition

## Table of Contents

- [1. The Problem](#1-the-problem)
- [2. The Pattern](#2-the-pattern)
- [3. When to Use It](#3-when-to-use-it)
- [4. Sample: A Fixed Grid](#4-sample-a-fixed-grid)
- [5. Design Decisions](#5-design-decisions)
- [6. Keep in Mind](#6-keep-in-mind)

## 1. The Problem

- **Games ask "what's near this location?" a lot** — physics collisions, audio falloff, local chat, AI target selection. Each query can cost a frame's budget if done naively
- **Naive pairwise check is O(n²)** — for every unit, test against every other unit. With hundreds of RTS units, this spirals out of control each frame
- **Root cause** — the object array has no spatial order. To find neighbors you must scan the whole collection
- **Insight from 1D** — if units lay along a line, sort by position and binary-search to O(log n) (or pigeonhole-sort to O(n)). The Spatial Partition pattern generalizes this idea to 2D/3D

## 2. The Pattern

- For a set of objects, each with a position in space, store them in a **spatial data structure** organized by their positions. This data structure efficiently answers **queries for objects at or near a location**. When an object's position changes, update the structure so it can continue to find the object

## 3. When to Use It

- **Applies to both moving game objects and static world geometry/art** — sophisticated games run multiple spatial partitions for different content types
- **Requirement 1** — objects each have a position
- **Requirement 2** — you're doing enough location-based queries that performance is suffering. For small `n`, the bookkeeping may cost more than it saves

## 4. Sample: A Fixed Grid

### 4.1. The grid

- Superimpose a grid of fixed-size cells over the world. Each cell stores a list of units within its bounds
- **Combat loop** — for each cell, resolve combat only among units in that cell. You've sliced one big battlefield into many small ones
- **Analysis** — nested cell×unit×unit loop looks worse, but the inner loops shrink enough to dominate. Cell granularity matters: too small and the outer cell loop starts to hurt

### 4.2. Grid storage as linked lists

- Each cell points to the head of a **doubly linked list** of units in it
- Each unit has `prev_` and `next_` pointers, plus a `Grid*` back-reference
- Linked lists (not arrays) because units frequently move between cells, and list insert/remove is a few pointer assignments

### 4.3. Entering the field

- Unit constructor calls `grid_->add(this)`
- `Grid::add` — divide position by `CELL_SIZE`, cast to `int` for the cell index; link the unit at the head of that cell's list

### 4.4. Movement

- `Unit::move` → `Grid::move`. Compute old cell and new cell from old/new positions
- If the cell didn't change, just update the unit's coordinates
- Otherwise: unlink from the old cell's list (adjusting `prev_`/`next_` neighbors, and the cell head if the unit was at the front), then `add` it to the new cell

### 4.5. Attack range across cells

- If attack radius > 0, units in *different* cells may still be close enough. Check neighbors
- Only check **half** of the eight neighbors — otherwise every pair gets processed twice (A finds B to the right; B finds A to the left). Which half is arbitrary
- **Corner case** — if attack distance exceeds cell size, you must scan multiple rings of neighbors

## 5. Design Decisions

### 5.1. Is the partition hierarchical or flat?

| | Flat (grid) | Hierarchical |
|---|---|---|
| Complexity | Simpler to implement and reason about | More complex |
| Memory | Constant; fixed up front | Grows with subdivisions |
| Update when objects move | Faster; adjust one cell at a time | May adjust multiple hierarchy levels |
| Empty space | Allocated and walked anyway | Left as one big partition; efficient |
| Dense clumps | Degenerates — one cell holds everything | Subdivides adaptively back to small groups |

### 5.2. Does the partitioning depend on the set of objects?

- **Object-independent** (fixed grid) — add objects incrementally; move objects quickly; but partitions may be imbalanced if objects clump
- **Object-dependent** (**BSP**, **k-d tree**, **bounding volume hierarchy**) — boundaries chosen to balance object counts per region. Gives consistent query performance (important for stable frame rate) but is best computed on a whole object set at once. Used more for static art and geometry. Analogous to self-balancing trees (red-black, AVL): adding one item may force reshuffling
- **Hybrid: quadtree** (2D; **octree** in 3D) — fixed half-splitting boundaries, but only subdivides a square when its population crosses a threshold
  - Adding incrementally is cheap: at most one subdivision per add, bounded by the max-count
  - Removing collapses a subdivision when the parent drops below threshold
  - Moving is add + remove, both cheap
  - Balanced: no square ever exceeds the population cap, even when objects cluster

### 5.3. Are objects only stored in the partition?

- **Only in the partition** — cheaper (one collection), no sync burden
- **Plus a flat collection** — faster to iterate every object regardless of position. Two structures, each optimized for a use case; both must stay in sync on create/destroy

## 6. Keep in Mind

- **It's a memory-for-speed trade** — bookkeeping structures cost RAM. Worth it only when the `n` and query volume are large enough
- **Moving objects is the hard case** — reorganizing the structure on position change adds code complexity and CPU. Like a hash table whose keys change spontaneously
- **Common structures and their 1D cousins** — useful mental anchors:

  | Structure | Analogue in 1D |
  |-----------|----------------|
  | Grid | Persistent bucket sort |
  | BSP, k-d tree, bounding volume hierarchy | Binary search tree |
  | Quadtree, octree | Trie |
