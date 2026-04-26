# Ch 12: Coordinated Batch Processing

## Table of Contents

- [1. Aggregating Parallel Output](#1-aggregating-parallel-output)
- [2. Join (Barrier Synchronization)](#2-join-barrier-synchronization)
- [3. Reduce](#3-reduce)
  - [3.1. Count](#31-count)
  - [3.2. Sum](#32-sum)
  - [3.3. Histogram](#33-histogram)
- [4. Hands-On](#4-hands-on)

## 1. Aggregating Parallel Output

- **Coordinated batch processing** — patterns that pull the parallel outputs of many workers back together into an aggregate result; the counterpart to splitting/sharding from the previous chapter.
- **MapReduce framing** — sharding a work queue is the *map* phase; coordinating outputs into a single answer is the *reduce* phase. This chapter covers reduce-style coordination plus a stricter variant (join).

## 2. Join (Barrier Synchronization)

- **Join (barrier synchronization)** — work proceeds in parallel, but no item is released past the join until *all* parallel work items upstream have completed; analogous to joining a thread.
- **Why merge isn't enough** — the merger pattern blends two streams into one but gives no guarantee the dataset is complete, so it can't support correctness-critical aggregates (e.g., "sum every value in the set").
- **Guarantees vs. cost** — join ensures completeness so aggregates are correct, but it serializes the workflow at the barrier — the next stage can't start until the slowest upstream worker finishes, increasing overall latency.

## 3. Reduce

- **Reduce** — optimistically merges parallel outputs into a single comprehensive representation, instead of waiting for everything to finish like join.
- **Repeatable** — each reduce step takes two or more outputs and produces one output of the same shape, so the operation can be applied iteratively until a single result remains.
- **Why "reduce"** — it reduces both the *number* of outputs and the *data per output* down to just what's needed for the answer.
- **Concurrency advantage over join** — because reduce produces partial results of the same type, it can run *concurrently* with the still-executing map/shard phase, shortening end-to-end latency.

### 3.1. Count

- **Count example** — counting word occurrences in a book: shard pages across 10 work queues by the page-number's last digit; each worker emits per-word counts (e.g., `a: 50, the: 17`); reduce sums matching keys across pairs of outputs until one final tally remains.

### 3.2. Sum

- **Sum example** — total US population: shard by state, then re-shard by county; workers emit `(town, population)` tuples; reduce repeatedly combines pairs like `(Seattle, 4,000,000) + (Northampton, 25,000)` into `(Seattle-Northampton, 4,025,000)`.
- **Reduce is shape-agnostic** — the reducer doesn't need to know about the two-level sharding upstream; it just keeps merging tuples until one remains.

### 3.3. Histogram

- **Histogram** — a model of a distribution (e.g., families with 0–10 children expressed as percentages per bucket).
- **Merging weighted histograms** — to combine per-town histograms into a national one, multiply each town's histogram by its population to recover counts, sum the counts across towns, then divide by the merged population to renormalize. Apply repeatedly until one histogram remains.

## 4. Hands-On

- **Image tagging and processing pipeline** — license-plate detection + blurring (multi-worker container group, sharded for throughput), join barrier so originals aren't deleted until *every* image is blurred, copier to fan out into a deletion queue and a vehicle/color recognition queue, then a reduce stage that sums the per-image JSON `{vehicles, colors}` tuples into a final aggregate count.
