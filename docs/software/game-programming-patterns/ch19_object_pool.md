# Ch 19: Object Pool

## Table of Contents

- [1. The Problem](#1-the-problem)
- [2. The Pattern](#2-the-pattern)
- [3. When to Use It](#3-when-to-use-it)
- [4. Sample: Particle Pool](#4-sample-particle-pool)
- [5. Design Decisions](#5-design-decisions)
- [6. Keep in Mind](#6-keep-in-mind)

## 1. The Problem

- **Allocating and freeing constantly is deadly on consoles/mobile** — memory is scarce, compacting memory managers are rarely available, allocation can be slow, and users expect rock-solid stability
- **Fragmentation** — free space gets broken into pieces scattered among in-use chunks. Total free memory may be large, but the largest **contiguous** block may be too small for the next allocation. Allocation fails even though the heap has space
- **Console soak tests** — games run for days in demo mode to certify stability. Failures are usually fragmentation or memory leaks creeping over time
- **The usual shortcut** — grab a big block at startup and never free it. Safe, but painful when objects naturally come and go during play
- **The compromise** — allocate one big block up front; hand out chunks internally. Best of both worlds: memory manager sees a single allocation; game code sees free create/destroy

## 2. The Pattern

- Define a **pool class** that maintains a collection of reusable objects. Each object supports an **"in use"** query. On initialization, the pool creates the whole collection up front (usually in a single contiguous allocation) and marks all objects "not in use"
- **To create**: ask the pool; it finds a free object, marks it "in use", returns it
- **To destroy**: flip the object back to "not in use". No heap activity

## 3. When to Use It

- You need to frequently create and destroy objects
- Objects are similar in size
- Allocating on the heap is slow or causes fragmentation
- Each object encapsulates an expensive-to-acquire resource (DB connection, network socket, etc.)
- **Common game uses** — particles, enemies, visual effects, currently-playing sounds

## 4. Sample: Particle Pool

### 4.1. Naive version

- **Particle** has an `inUse()` method that returns `framesLeft_ > 0` (no separate flag needed since lifetime already encodes it)
- **ParticlePool** holds `Particle particles_[POOL_SIZE]` in-place. `create()` scans linearly for the first `!inUse()` slot and initializes it — **O(n)** creation. `animate()` ticks every slot
- If no slot is free, simply skip creating the particle

### 4.2. Free list optimization

- **Problem** — linear scan to find a free slot is slow for large, mostly-full pools
- **Idea** — keep a linked list of available particles. Naive implementation needs a separate pointer array the size of the pool — wasteful
- **Trick: the free list lives inside the dead objects themselves** — an inactive particle's position/velocity fields are irrelevant, so reuse that memory via a `union` to store a `next` pointer to the next free particle
- **Result** — O(1) creation and destruction with zero extra memory for the list
- **Pool constructor** — threads all particles into a single free list; `firstAvailable_` points at the head
- **Create** — pop the head: `firstAvailable_ = newParticle->getNext()`
- **Destroy** (particle's lifetime ends mid-animate) — push it back on the head of the free list

## 5. Design Decisions

### 5.1. Are objects coupled to the pool?

- **Coupled** — simpler implementation. Pool can be a `friend`, making the object's constructor private so only the pool creates them; the object may already have state (lifetime, off-screen position) that doubles as the "in use" signal, saving memory
- **Decoupled** — enables a generic, reusable pool (templates). Cost: "in use" state must be tracked outside the objects, typically with a parallel `bool inUse_[POOL_SIZE]` bitfield

### 5.2. Who initializes reused objects?

- **Pool initializes internally** — pool fully encapsulates its objects; no external reference to an object that might be unexpectedly reused. Cost: the pool's interface must mirror every `init(...)` overload the object exposes
- **Outside code initializes** — pool's interface stays simple (`create()` returns a pointer or NULL). Caller invokes any `init()` it likes. Cost: caller must null-check the returned pointer when the pool is full

## 6. Keep in Mind

- **The pool may waste memory on unneeded objects** — too small crashes; too big steals memory from elsewhere. Size must be tuned
- **Fixed active capacity** — the pool can fill. Strategies for the full case:
  - **Prevent it outright** — tune size so overflow is impossible (right answer for important objects like bosses or gameplay items)
  - **Just don't create** — fine for particles; nobody notices one missing sparkle on a full screen
  - **Forcibly kill an existing object** — good for sounds: replace the quietest playing sound; the new one masks the cutoff
  - **Grow the pool** — allocate more at runtime or spill into an overflow pool; decide whether to shrink back later
- **Slot size is fixed** — all slots must be big enough for the largest object, wasting memory for smaller ones. When sizes vary a lot, use separate pools per size class
- **Reused objects are not auto-cleared** — you lose the memory manager's debug fill (e.g., `0xdeadbeef`). Worse, the previous object was the same type, so forgetting to initialize may leave "almost correct" stale data. Discipline every init path; consider debug-clearing slots on release
- **With a garbage collector, pooled objects prevent reclamation of their referenced objects** — when a pooled object is released, clear its references so the GC can free what it pointed to
- **vs. Flyweight** — both keep a collection of reusable objects. Flyweight shares a single instance across multiple owners *simultaneously*; Object Pool reuses an object *over time*, one owner at a time. No sharing expectation within a lifetime
- **Synergy with Data Locality** — packing same-type objects contiguously keeps the CPU cache full when iterating
