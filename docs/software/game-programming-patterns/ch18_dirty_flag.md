# Ch 18: Dirty Flag

## Table of Contents

- [1. The Problem](#1-the-problem)
- [2. The Pattern](#2-the-pattern)
- [3. When to Use It](#3-when-to-use-it)
- [4. Sample: Scene Graph Transforms](#4-sample-scene-graph-transforms)
- [5. Design Decisions](#5-design-decisions)
- [6. Keep in Mind](#6-keep-in-mind)

## 1. The Problem

- **Scene graphs are hierarchical** — each object has a local transform relative to its parent (ship → crow's nest → pirate → parrot). An object's **world transform** is the combined chain of local transforms down from the root
- **Renderer needs world transforms each frame** — computing them on the fly every frame wastes CPU on objects that haven't moved (static geometry, etc.)
- **Caching is the obvious fix, but eager recalc wastes work** — if the ship, nest, pirate, and parrot all move in one frame, recalculating the parrot's world transform after each parent change recomputes it four times when only the final value is needed. 4 moves → 10 recalculations, 6 of them wasted
- **Root cause** — a world transform depends on several local transforms. Eager recalculation duplicates work when multiple ancestors change in the same frame

## 2. The Pattern

- A set of **primary data** changes over time. A set of **derived data** is determined from it by some expensive process. A **dirty flag** tracks when the derived data is out of sync with the primary data. It is set when the primary data changes. When the derived data is needed, if the flag is set, reprocess and clear it; otherwise use the cached previous result
- **Name origin** — "dirty" is the traditional term for "out of date". Also called **dirty bit**

## 3. When to Use It

- **Two classes of work** — this pattern applies to both **calculation** (expensive math on local data, like transforms) and **synchronization** (derived data lives elsewhere — disk, network — and transport is what's expensive)
- **Primary data must change more often than derived data is used** — the whole point is skipping work for changes that get invalidated before anyone reads them. If every change is immediately read, no wins are possible
- **Must be hard to update incrementally** — if you can "pay as you go" (e.g., keep a running total when items are added/removed), do that instead. Dirty flags earn their keep only when recomputing from scratch is the alternative

## 4. Sample: Scene Graph Transforms

- **Add to each node** — a cached `world_` transform and a `dirty_` flag, initialized `true` (newly created node has no valid world transform yet)
- **On `setTransform`** — update `local_`, set `dirty_ = true`. No recursion into children
- **On render** — pass a `dirty` parameter down the recursion, OR-ing in each node's own `dirty_`. If the accumulated dirty bit is set, recompute `world_` and clear the flag; otherwise reuse the cached value
- **Why this works** — the `dirty` parameter threads ancestor dirtiness down without having to eagerly mark every descendant when a parent moves. Each affected world transform is recomputed exactly once per frame
- **Caveat** — the trick relies on `render()` being the only consumer of world transforms. If other code needed them, the recursive-dirty-param shortcut wouldn't suffice

## 5. Design Decisions

### 5.1. When is the dirty flag cleaned?

| Strategy | Upside | Downside |
|----------|--------|----------|
| When the result is needed | Avoids the calculation entirely if the result is never used; maximal savings when changes vastly outnumber reads | A slow calculation right when the player expects the result causes a visible pause |
| At well-defined checkpoints | Work can be hidden behind a loading screen or cut scene; no in-game pause | You lose control over *when*; player may not reach the checkpoint, deferring longer than expected |
| In the background (timer) | Tune frequency; smooth cost | May do redundant work on barely-changed data; requires async support and concurrent-modification safety of primary state |

- **Hysteresis** — the HCI term for an intentional delay between input and response. Background/timer approaches introduce hysteresis deliberately

### 5.2. How fine-grained is your dirty tracking?

- **Fine-grained** (e.g., dirty flag per plank of a ship) — only the exact data that changed gets processed. Cost: more memory for flags, more fixed per-chunk overhead
- **Coarse-grained** (e.g., dirty flag per deck) — less memory for flags, less overhead per processing chunk. Cost: you reprocess unchanged data bundled with the changed data (add one barrel, re-send the whole deck)

## 6. Keep in Mind

- **Deferring too long has a cost** — the work you skipped still has to happen eventually. If it's a big chunk and it lands right when the player needs the result, that's a pause. If the program crashes before deferred work runs, the work may never happen (hence auto-save in editors — the "unsaved changes" dot is a literal dirty flag visualized)
- **You must set the flag on every primary-data change** — dirty tracking is a cache, and cache invalidation is notoriously hard. Missing one spot means stale derived data and subtle bugs. Mitigation: funnel all mutations through a narrow API that sets the flag
- **You must keep the previous derived data in memory** — dirty flag trades memory for speed. Worthwhile when calculation is slow and memory is cheap; reversed when you have more CPU than RAM
- **GC analogy** — ref-counting is the eager "update as you go" strategy; stop-the-world GC is pure deferred work; incremental/deferred-refcount GC sits in between — the same continuum as the "when to clean" decision
