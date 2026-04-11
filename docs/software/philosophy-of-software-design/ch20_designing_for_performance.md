# Ch 20: Designing for Performance

## Table of Contents

- [1. How to Think About Performance](#1-how-to-think-about-performance)
- [2. Measure Before Modifying](#2-measure-before-modifying)
- [3. Design Around the Critical Path](#3-design-around-the-critical-path)
- [4. Example: RAMCloud Buffers](#4-example-ramcloud-buffers)
- [5. Clean Design and High Performance are Compatible](#5-clean-design-and-high-performance-are-compatible)

## 1. How to Think About Performance

- **Avoid both extremes** — optimizing every statement slows development and adds needless complexity; completely ignoring performance creates a "death by a thousand cuts" scenario where the system ends up 5-10x slower than necessary, with no single fix that helps
- **Choose "naturally efficient" alternatives** — develop an awareness of which operations are fundamentally expensive, then pick the clean option that is also cheap. Often the efficient approach is just as simple as the slow one

| Expensive operation | Approximate cost |
|---------------------|-----------------|
| **Network round-trip (datacenter)** | 10-50 us (tens of thousands of instruction times) |
| **Network round-trip (wide-area)** | 10-100 ms |
| **Disk I/O** | 5-10 ms (millions of instruction times) |
| **Flash storage I/O** | 10-100 us |
| **Dynamic memory allocation** | Significant overhead for allocation, freeing, and garbage collection |
| **Cache miss (DRAM fetch)** | A few hundred instruction times |

- **Micro-benchmarks** — small programs that measure the cost of a single operation in isolation. Building a micro-benchmark framework pays for itself quickly by making it trivial to add new measurements
- **Prefer efficient defaults** — e.g., use a hash table instead of an ordered map when ordering isn't needed (easily 5-10x faster); store structs inline in an array rather than as an array of pointers (one allocation instead of many)
- **When efficiency requires complexity** — if the faster design adds only a small, hidden amount of complexity, it may be worth it. If it complicates interfaces or adds significant implementation complexity, start simple and optimize later only if performance proves to be a problem. However, if you have clear evidence that performance will be important in a particular situation (e.g., prior measurements showing kernel networking is too slow), implement the faster approach immediately
- **Simpler code tends to run faster** — defining away special cases eliminates checks; deep classes reduce layer crossings and method-call overhead. Complexity and slowness often have the same root cause

## 2. Measure Before Modifying

- **Don't trust intuition** — programmers' guesses about what is slow are unreliable, even for experienced developers. Intuition-driven changes waste time and add complexity for no measurable gain
- **Measure to identify bottlenecks** — top-level performance numbers tell you the system is slow, not why. Drill deeper to find the specific places where the system spends the most time and where you have ideas for improvement
- **Measure to verify improvements** — re-measure after every change. If a change doesn't produce a measurable speedup, back it out (unless it also simplified the design). Retaining complexity that doesn't improve performance is never worth it

## 3. Design Around the Critical Path

- **Fundamental fixes first** — introducing a cache, changing an algorithm (e.g., balanced tree vs. list), or bypassing a slow layer (e.g., kernel-bypass networking) are the highest-leverage performance improvements. Apply standard design techniques to implement them cleanly
- **When no fundamental fix exists** — redesign the code around the critical path. This is a last resort, but it can produce large speedups
- **Identify the ideal** — ask: what is the smallest amount of code that must execute in the common case? Ignore existing class structure, method boundaries, and special cases. Imagine all relevant code in a single method with the most convenient data structure. This "ideal" is the simplest and fastest the code can ever be
- **Close the gap** — find a clean design that comes as close as possible to the ideal. You may need a bit of extra code for proper abstractions (e.g., a method call into a general-purpose hash table), but the goal is to keep the critical path nearly intact
- **Minimize special cases on the critical path** — each conditional or extra method call on the hot path adds latency. Ideally, a single test at the beginning detects all special cases; if it passes, the normal path executes with no further checks. Special-case handling branches off to separate code where simplicity matters more than speed

## 4. Example: RAMCloud Buffers

- **Buffer concept** — stores a logically linear byte array using discontiguous memory chunks (internal chunks owned by the Buffer, external chunks owned by the caller). Avoids expensive large memory copies by referencing external data in place
- **Critical path: allocating a small internal chunk** — the most common operation. In the simplest case, the last chunk can be enlarged if it is internal and has space remaining

| Aspect | Original design | Redesigned |
|--------|----------------|------------|
| **Special-case checks** | 6 separate conditions tested along the critical path | 1 single test rules out all special cases |
| **Method calls on critical path** | 3 (alloc -> allocateAppend -> Allocation::allocateAppend) | 1 (entire path in a single method) |
| **Layer depth** | 3 shallow layers with nearly identical signatures (a red flag) | Shallow layers eliminated; deeper internal abstractions |
| **Code size** | 1886 lines | 1476 lines (20% smaller) |
| **Performance (1-byte append)** | 8.8 ns | 4.75 ns (~2x faster) |
| **Performance (construct + append + destroy)** | 24 ns | 12 ns (~2x faster) |

- **Key technique: `extraAppendBytes`** — a new instance variable that tracks available space after the last chunk. Consolidates multiple checks (is last chunk internal? is there space? does the buffer have chunks at all?) into a single zero-vs-nonzero test

## 5. Clean Design and High Performance are Compatible

- **Not a trade-off** — the Buffer rewrite achieved a 2x speedup while simultaneously simplifying the design and shrinking the code by 20%
- **Complicated code tends to be slow** — it performs extraneous or redundant work. Clean, simple code usually performs well enough without explicit optimization
- **When optimization is needed** — the key is still simplicity: find the critical paths and make them as simple as possible
