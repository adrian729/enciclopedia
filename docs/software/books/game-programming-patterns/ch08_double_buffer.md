# Ch 8: Double Buffer

## Table of Contents

- [1. The Problem](#1-the-problem)
- [2. The Pattern](#2-the-pattern)
- [3. When to Use It](#3-when-to-use-it)
- [4. Beyond Graphics: Sequential Update Ordering](#4-beyond-graphics-sequential-update-ordering)
- [5. Design Decisions](#5-design-decisions)
- [6. Keep in Mind](#6-keep-in-mind)

## 1. The Problem

- **Computers are sequential beasts** — they perform one tiny step after another, but users need to see operations appear instantaneous or simultaneous. Rendering is the canonical case: every game engine must address it
- **Framebuffer** — an array of pixels in memory; the video driver streams it to the screen ~60 times a second, pixel by pixel, row by row
- **Tearing** — if game code writes to the framebuffer *while* the video driver reads it, the driver can race past the renderer. The user sees half of something drawn on screen — the bottom half looks "torn off"
- **Two causes of mid-modification access**:
  1. State accessed from another thread or interrupt (e.g., video driver reading framebuffer)
  2. Code doing the modification reads the same state it's modifying (common in physics and AI where entities interact)

## 2. The Pattern

- **Buffered class** — encapsulates a buffer (a piece of state that can be modified incrementally) while making outside code see every edit as a single atomic change
- **Two instances** — the class holds a *next* buffer and a *current* buffer
- **Reads go to current; writes go to next** — outside observers only ever see the completed `current`; in-progress edits land on `next`
- **Swap** — when writes complete, a swap operation instantly exchanges `next` and `current`. The old current becomes available for reuse as the new next
- **Stage analogy** — two stages, one lit for the audience (current) and one dark where stagehands set up the next scene (next). At the transition, the lights switch. The audience never sees the work

## 3. When to Use It

- This pattern announces itself — without it, a system will *look* visibly wrong (tearing, flicker) or *behave* incorrectly
- **Appropriate when all of these hold**:
  - State is modified incrementally
  - The same state may be accessed mid-modification
  - Observers must not see work-in-progress
  - Reads cannot wait for writes to finish

## 4. Beyond Graphics: Sequential Update Ordering

- **Slapstick example** — actors on a Stage each `update()` once per frame, and an actor can `slap()` another. With a single `slapped_` flag, the slap propagates through the chain in one frame if actors are ordered front-to-back, but stalls for several frames if ordered back-to-front
- **Diagnosis** — the update both reads and writes the same `slapped_` state, so the frame's result depends on array ordering. This violates the requirement that actors appear to run in parallel
- **Fix — buffer each actor's state at fine granularity**:
  - Two flags per actor: `currentSlapped_` (read) and `nextSlapped_` (write)
  - `slap()` sets `nextSlapped_`; `wasSlapped()` reads `currentSlapped_`
  - Stage loops twice per frame: once calling `update()` on every actor, then once calling `swap()` on every actor
- **Result** — an actor sees a slap one frame after it was delivered, regardless of array order. All actors appear to update simultaneously

## 5. Design Decisions

- **How are the buffers swapped?**

  | Strategy | Speed | Limitation |
  |----------|-------|------------|
  | Swap pointers/references | Very fast — a couple of pointer assignments regardless of buffer size | Outside code cannot cache persistent pointers into the buffer; data on "next" is two frames old (frames ping-pong between the two buffers) |
  | Copy data between buffers | Slow — cost grows with buffer size; everything blocks during the copy | Data on next is only one frame old; works when video driver requires the framebuffer at a fixed address |

- **Old framebuffer data as feature** — one classic use of the "two frames old" data under pointer swaps is simulating motion blur by blending the current frame with the prior one
- **What is the granularity of the buffer?**
  - **Monolithic** — one pair of buffers, one swap. Graphics example. Swap is trivial
  - **Distributed across many objects** — each object holds its own pair. Actor example. Swap must iterate all objects
- **Static-index optimization for distributed buffers** — replace per-object pointers with an array of two slots and a single static `current_` index (0 or 1). `next()` returns `1 - current_`. `swap()` flips one static variable, and every object's state swaps at once — the speed of a monolithic swap with the layout of a distributed buffer

## 6. Keep in Mind

- **Lower-level pattern** — unlike larger architectural patterns, most of the game won't be aware of it. Consequences are local
- **The swap itself takes time** — it must be atomic: no reads or writes to either buffer during the swap. If swapping takes longer than modifying the state, the pattern loses its value
- **Two buffers means double memory** — on memory-constrained devices this price is steep. If you can't afford two buffers, look for alternative ways to keep state from being read during modification
- **Ubiquity** — found in nearly every graphics API: OpenGL's `swapBuffers()`, Direct3D's "swap chains", Microsoft XNA's `endDraw()`
