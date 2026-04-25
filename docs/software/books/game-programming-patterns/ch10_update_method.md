# Ch 10: Update Method

## Table of Contents

- [1. The Problem](#1-the-problem)
- [2. The Pattern](#2-the-pattern)
- [3. When to Use It](#3-when-to-use-it)
- [4. Sample Implementation](#4-sample-implementation)
- [5. Design Decisions](#5-design-decisions)
- [6. Keep in Mind](#6-keep-in-mind)

## 1. The Problem

- **Entities must animate across frames, not within one** — a naive `while(true)` loop that patrols a skeleton left-then-right never yields, so the player never sees motion. Behavior must advance one frame at a time and return control to the outer loop
- **Stuffing logic into the game loop doesn't scale** — adding a skeleton needs a `patrollingLeft` flag and a position; adding two magic statues needs two frame counters. Each new entity adds more variables and imperative code directly to the loop. When "mushed" describes your architecture, you have a problem
- **Solution direction** — each entity should encapsulate its own behavior. The game loop shouldn't know concrete types — only that objects can be updated

## 2. The Pattern

- **Definition** — the game world maintains a collection of objects. Each object implements an `update()` method that simulates one frame of the object's behavior. Each frame, the game updates every object in the collection
- **Abstraction** — an abstract `update()` method hides concrete entity types from the game loop. Each entity's behavior is decoupled from the loop and from other entities
- **Simultaneity illusion** — calling `update()` on every object each frame makes them appear to behave concurrently from the player's perspective
- **Dynamic population** — adding and removing entities is just adding and removing from the collection. The world can be built from a data file or level editor rather than hardcoded

## 3. When to Use It

- **Good fit when**:
  - The game has many objects or systems that need to run simultaneously
  - Each object's behavior is mostly independent of the others
  - The objects need to be simulated over time
- **Poor fit** — abstract games where pieces act like chess pieces rather than living actors. A chess pawn doesn't need to update every frame (though you might still use the pattern for its animation)
- **Natural trinity** — along with Game Loop and Component, Update Method often forms the nucleus of a game engine

## 4. Sample Implementation

- **Abstract `Entity`** — holds position and declares `virtual void update() = 0`
- **`World`** — owns an array of `Entity*` and a `gameLoop()` that, each turn, calls `update()` on every entity
- **Skeleton subclass** — moves 1 unit per frame, flips direction at 0 and 100. The `patrollingLeft_` local from the original imperative loop becomes a field so it persists between `update()` calls
- **Statue subclass** — increments `frames_`; when it hits `delay_`, shoots lightning and resets. Each statue instance has its own timer — you can create as many as you like without adding new variables to the game loop
- **Passing time** — fixed time step assumes each `update()` advances the world by the same unit. Games using variable time steps pass `elapsed` in: `update(elapsed)`. Entity code then scales motion by elapsed time and must handle overshoot carefully (e.g., skeleton crossing the patrol bound during a large slice)
- **On inheritance** — the Gang of Four's "favor object composition over class inheritance" pushed the industry away from giant entity hierarchies. Modern practice puts `update()` on components via the Component pattern; the subclass-based example here is just the simplest way to illustrate the method itself

## 5. Design Decisions

- **What class does the update method live on?**

  | Host | When it fits |
  |------|--------------|
  | The entity class | Simplest option if an entity class already exists, and there are few kinds of entities. Industry is moving away — subclassing for every new behavior is brittle |
  | The component class | Natural if already using Component. Each component (render, physics, AI) updates itself, decoupling parts of a single entity from each other |
  | A delegate class | State pattern or Type Object: `Entity::update()` is non-virtual and forwards to `state_->update()`. Change behavior by swapping the delegate |

- **How are dormant objects handled?** Disabled, off-screen, or unlocked objects waste cycles if iterated every frame

  | Approach | Upside | Downside |
  |----------|--------|----------|
  | Single collection including inactive objects | Simple; one list | Wastes time on per-object enabled checks; iterating over inactive objects can blow the CPU data cache, forcing slow RAM reads |
  | Separate collection of active objects only | Skip the wasted iteration entirely | Extra memory; must keep master and active collections in sync when objects are created/destroyed |

  - **Guiding metric** — the more inactive objects you typically have, the more valuable the separate active collection becomes. A variant: keep one master collection plus a collection of *inactive* entities

## 6. Keep in Mind

- **Single-frame slicing adds complexity** — the imperative "walk back and forth" is shorter than the update-method version because it doesn't have to yield. The yield is almost always necessary, but there's a real up-front cost
- **You must store state to resume each frame** — execution position is lost every return. Variables like `patrollingLeft_` exist only to encode what was implicit in the original control flow. The State pattern often helps
- **Coroutines/fibers escape the cost** — if the language supports lightweight concurrency (generators, coroutines, fibers), object behavior can be written in a straight-line imperative form that pauses and resumes. Actual OS threads are usually too heavyweight. Bytecode is another option for application-level "threads"
- **Objects simulate each frame but are not truly concurrent** — inside `update()`, an object can touch the rest of the world. If A precedes B, A sees B's previous state, while B sees A's *new* state. A "turn" is one frame long; the game is still turn-based internally
- **Sequential update avoids ambiguity** — parallel updates force reconciliation (imagine black and white both moving to the same chess square at once). If you *do* want parallelism, use Double Buffer so both A and B see the previous frame's state
- **Be careful modifying the object list while updating**:
  - **Additions** — new objects can act in the frame they spawned before the player sees them. Fix: cache the object count at loop start and only iterate that many
  - **Removals** — deleting before the current index shifts everything up, so `i++` skips the next object. Fixes: walk the list backwards, carefully adjust the index, or mark objects "dead" and sweep them after the update loop. With multiple update threads, deferring list modification avoids costly synchronization
- **Cache performance** — when updating many entities or components per frame becomes a bottleneck, the Data Locality pattern can help
- **In the wild** — Unity's `MonoBehaviour`, Microsoft XNA's `Game` and `GameComponent`, and the Quintus JavaScript engine's `Sprite` all use this pattern
