# Ch 17: Data Locality

## Table of Contents

- [1. The Problem](#1-the-problem)
- [2. The Pattern](#2-the-pattern)
- [3. When to Use It](#3-when-to-use-it)
- [4. Techniques](#4-techniques)
- [5. Design Decisions](#5-design-decisions)
- [6. Keep in Mind](#6-keep-in-mind)

## 1. The Problem

- **CPUs got faster than RAM** — fetching a byte from main memory can take hundreds of cycles. If most instructions need data, the CPU spends a huge fraction of time stalled waiting on memory
- **Caches bridge the gap** — a small chunk of fast memory on the chip (L1, L2, L3). When data is fetched from RAM, the CPU automatically grabs a whole contiguous chunk (~64–128 bytes) called a **cache line**. Finding data already in cache is a **cache hit**; missing is a **cache miss**, which stalls the CPU
- **Data layout is performance** — two programs doing the exact same computation can differ 50x in speed based on cache miss patterns alone. Performance is not just an aspect of code; it's an aspect of data
- **Goal** — organize data structures so the things you process next are next to each other in memory, maximizing reuse of each cache line pulled in

## 2. The Pattern

- Modern CPUs have caches to speed up memory access. They access memory adjacent to recently-accessed memory much faster. Take advantage by **increasing data locality** — keeping data in contiguous memory in the order you process it

## 3. When to Use It

- **You have a real performance problem** — don't apply pre-emptively; the result is usually more complex and less flexible code
- **The problem is actually cache misses** — confirm with a profiler (Cachegrind is a free option). If slowness has other causes, this pattern won't help
- **Still think about it during design** — even without optimizing, keep cache-friendliness in mind when shaping core data structures

## 4. Techniques

### 4.1. Contiguous arrays

- **The sin** — an array of pointers to entities, each entity holding pointers to components. Processing means chasing two pointers per element per frame — two cache misses minimum, and the heap layout is at the mercy of the memory manager
- **The fix** — store components directly in flat arrays (`AIComponent[]`, `PhysicsComponent[]`, `RenderComponent[]`), one array per type. Each update loop walks its array in memory order
- **Heuristic** — if you want better locality, look for `->` operators you can eliminate. Fewer indirections = fewer cache misses
- **Impact reported** — in the author's test, this change made the update loop 50x faster than the pointer-chasing version
- **Encapsulation preserved** — `GameEntity` can still exist with pointers into those arrays for code that wants a conceptual "entity"; the hot loop just sidesteps it

### 4.2. Packed data

- **Problem** — a large array with an `isActive` flag means iterating still loads inactive objects into cache, wasting cache lines. The `if` check itself risks **branch misprediction and pipeline stall**
- **Fix** — keep active objects at the front of the array, inactive at the back. Loop only over `numActive_`. No flag check, no skipped data
- **Keeping it sorted is cheap** — only when an object is activated/deactivated, swap it with the boundary element. Two assignments, no quicksort per frame
- **Counter-intuitive win** — moving bytes around in memory (swaps) is often cheaper than traversing a pointer, once you count the cache miss
- **Bonus** — active/inactive state is inferred from position + `numActive_`, so the flag field disappears entirely. Smaller objects = more fit per cache line

### 4.3. Hot/cold splitting

- **Problem** — a component carries fields touched every frame (hot: animation, energy, goal position) alongside rarely-used fields (cold: loot drop table). Loading each component pulls cold data into cache too, bloating the per-object footprint
- **Fix** — split the struct into two. The hot piece stays in the packed array; the cold piece lives elsewhere, referenced by pointer from the hot piece (or at the same index in a parallel cold array)
- **Fuzzy in practice** — in toy examples, hot vs. cold is obvious. Real games have fields that are hot in one mode and cold in another; figuring out the split is "between a black art and a rathole"

## 5. Design Decisions

### 5.1. How do you handle polymorphism?

- **Don't** — avoid subclassing in cache-optimized paths. Fast, predictable, safe; all objects are the same size. Cost: inflexible. Consider the **Type Object** pattern for behavioral variance without subclassing
- **Separate array per concrete type** — mix of types becomes multiple homogeneous collections. Enables static dispatch, tight packing. Cost: you must know all types up front; bookkeeping grows with type count
- **Array of pointers** — classic polymorphism; fully flexible and open-ended. Cost: pointer indirection, cache-unfriendly. Fine if the code path isn't performance-critical

### 5.2. How are game entities defined?

| Representation | Upside | Downside |
|---------------|--------|----------|
| Class with pointers to components | Easy to reach components; components live in packed arrays | Moving components breaks raw pointers; care needed |
| Class with IDs for components | Components can move freely in memory | More complex lookup, slower, requires access to the component "manager" |
| Entity *is* just an ID | Entities tiny, no lifetime management (dies when last component dies) | Component lookup during update may be slow; if solved by same-index parallel arrays, you can't independently sort/pack the per-domain arrays |

## 6. Keep in Mind

- **Abstraction vs. locality is a real tradeoff** — interfaces in C++ mean pointer/reference access; virtual method calls traverse vtables. Both are pointer hops, both can cause cache misses
- **You will sacrifice abstractions** — the more you design around data locality, the more you give up inheritance, interfaces, and their decoupling benefits. No silver bullet
- **Single-threaded assumption** — laying data contiguously wins for one thread. For multiple threads modifying nearby data, putting them on different cache lines avoids costly cross-core cache synchronization
- **The Component pattern is the natural fit** — splitting entities by domain (AI, physics, render) lets each domain's array be walked cache-friendly. The pattern generalizes beyond components to any hot loop over lots of data
