# Ch 3: Flyweight

## Table of Contents

- [1. The Problem](#1-the-problem)
- [2. Forest for the Trees](#2-forest-for-the-trees)
- [3. Instanced Rendering](#3-instanced-rendering)
- [4. The Pattern](#4-the-pattern)
- [5. A Place To Put Down Roots](#5-a-place-to-put-down-roots)
- [6. What About Performance?](#6-what-about-performance)
- [7. See Also](#7-see-also)

## 1. The Problem

- **Too many objects, too much data** — a forest with thousands of trees, each carrying a mesh, bark/leaf textures, position, orientation, and tuning parameters, is too heavy to hold in memory and push over the bus to the GPU every 1/60 of a second
- **Key observation** — most of those thousands of trees look similar. Mesh and textures are typically identical across instances. Most fields are duplicated data

## 2. Forest for the Trees

- **Split the object in half** — extract the shared, instance-independent data into a separate class (`TreeModel` holding mesh, bark texture, leaves texture). Each `Tree` keeps only its instance-specific data (position, height, thickness, tint) plus a pointer to the shared `TreeModel`
- **One model, many trees** — the game only needs a single `TreeModel` in memory even if thousands of trees reference it
- **Not the same as Type Object** — Type Object also delegates part of an object's state to a shared object, but its intent is to minimize the number of classes by lifting "types" into the object model. Flyweight's intent is *purely efficiency*

## 3. Instanced Rendering

- **Share on the GPU too** — splitting in main memory is not enough; the forest still has to traverse the bus to the graphics card
- **Two data streams** — graphics APIs accept a common data blob (mesh, textures) plus a list of per-instance parameters (position, color, scale). A single draw call renders the entire forest
- **Direct3D and OpenGL both support this** as "instanced rendering"
- **Hardware support** — Flyweight may be the only Gang of Four pattern with actual hardware support, since the graphics card implements it directly

## 4. The Pattern

- **When to use** — when you have too many objects, so they must be more lightweight. "Too many" can mean too much memory *or* too much time pushing each one over the bus
- **Split state in two kinds**:

  | Kind | Gang of Four term | Author's gloss | Tree example |
  |------|-------------------|----------------|--------------|
  | Shared across instances | **Intrinsic** state | "Context-free" stuff | Geometry, textures |
  | Unique to each instance | **Extrinsic** state | — | Position, scale, tint |

- **Saves memory** by holding one copy of the intrinsic state across every place the object appears
- **Less obvious when there's no natural identity** — in the tree case, the shared state already had a clean identity (`TreeModel`). The pattern becomes more clever when the shared object doesn't have a well-defined identity, making one object "magically in multiple places at the same time"

## 5. A Place To Put Down Roots

- **Tile-based ground** — surface of the world is a huge grid; each tile has a terrain type with properties (movement cost, is-water flag, texture)
- **The ugly alternative** — an `enum Terrain` plus `switch` statements scattered across `getMovementCost`, `isWater`, etc. Data for one terrain type is smeared across many methods; terrain data is trapped in code
- **Terrain as a real class** — one `Terrain` class holding movement cost, wetness, texture. All methods `const` because…
- **Flyweights are almost always immutable** — same object appears in multiple contexts, so a mutation would appear everywhere simultaneously. Memory sharing should not change observable behavior
- **All terrain state is intrinsic** — nothing in `Terrain` depends on *where* the tile is, so one instance per terrain type suffices
- **World as grid of pointers** — `Terrain* tiles_[WIDTH][HEIGHT]`. Every grass tile points to the same `grassTerrain_` instance
- **Store flyweights directly in World** — owning them as fields (`grassTerrain_`, `hillTerrain_`, `riverTerrain_`) avoids the lifetime complexity of dynamic allocation
- **API wins** — `world.getTile(2, 3).getMovementCost()` is pleasant, `World` is no longer coupled to terrain internals, and a pointer is often no larger than an enum

## 6. What About Performance?

- **Indirection cost** — following the pointer in the grid to the terrain object can cause a cache miss (see *Data Locality* chapter)
- **Golden rule** — profile first; modern hardware is too complex for performance to be pure reasoning
- **Author's test result** — no penalty vs. an enum; flyweights were actually noticeably faster. Entirely dependent on how other data is laid out in memory
- **Guidance** — don't dismiss flyweights out of hand. If you find yourself writing an enum plus many switches, consider this pattern. If worried about performance, profile before choosing the less maintainable style

## 7. See Also

- **Factory Method** — if you can't predict which flyweights you need, create them on demand. Hide construction behind an interface that looks up existing instances first — this is Factory Method
- **Object Pool** — a natural place to store the pool of previously-created flyweights you're reusing
- **State pattern** — when state objects have no fields specific to their owning state machine, apply Flyweight to reuse the same state instance across multiple state machines simultaneously
