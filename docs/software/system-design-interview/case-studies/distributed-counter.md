# Distributed Counter

> Liu's Ch 6.05 only. The interesting part is **CRDT** as the resolution to hot-key contention at 500K QPS, where consistent hashing alone doesn't help (a hot key still hammers its assigned shard).

## Table of Contents

- [1. Requirements](#1-requirements)
- [2. Why Naive Approaches Fail](#2-why-naive-approaches-fail)
- [3. CRDT — The Pattern](#3-crdt--the-pattern)
- [4. Architecture](#4-architecture)
- [5. Variant — Unique-User Count via HyperLogLog](#5-variant--unique-user-count-via-hyperloglog)
- [6. Trade-offs](#6-trade-offs)
- [Sources](#sources)

## 1. Requirements

- Increment a counter (e.g., view count for a video) at very high QPS.
- Read the current count with low latency.
- 500M DAU × 10 videos viewed × 10× peak factor / 86,400 seconds ≈ **500,000 QPS** globally.
- A single hot video can receive 0.1% of all traffic = **500 QPS on one key**, dwarfing what a single shard can serve at low latency.

## 2. Why Naive Approaches Fail

| Approach | Why it fails |
|---|---|
| Single counter row in a SQL DB | Lock contention; 500 QPS on one row exceeds DB throughput |
| Shard counters by `video_id` | Consistent hashing distributes evenly, but a hot key still hammers its shard |
| Optimistic locking on a counter | Retry storms — every increment competes with every other |
| Pessimistic locking | Serialized increments; throughput capped at single-thread rate |

[Consistent hashing](fundamentals/sharding-and-consistent-hashing.md) doesn't solve this — Liu's emphasis. It evens out the *across-key* distribution, but a single super-hot key still saturates its shard.

## 3. CRDT — The Pattern

A **CRDT counter** has each node track its own count plus the latest known counts from every other node.

```
Node A: { A: 1500, B: 800, C: 1200 }
Node B: { A: 1450, B: 820, C: 1190 }
Node C: { A: 1480, B: 810, C: 1230 }
```

Total at any node = sum of all per-node counts. Each node's *own* count is up-to-date for its writes; the *other* nodes' counts are propagated asynchronously via gossip or a similar mechanism.

Key properties:

- **Writes don't conflict.** Each node only modifies its own row. There's no global counter to lock.
- **Reads are eventually consistent.** A read may see slightly stale counts from other nodes; the discrepancy converges as gossip catches up.
- **Any node can compute the total** independently — no coordination per read.

Trade-off: high availability and low read latency at the cost of broadcast complexity and eventual consistency. See [CAP, Consensus & Conflict Resolution](fundamentals/cap-consensus-and-conflict-resolution.md).

## 4. Architecture

```
View events (500K QPS)
   ↓
Queue absorbs the spike (Kafka or similar)
   ↓
Counter Service nodes (sharded by video_id, but with CRDT redundancy)
   ↓
Each node maintains its own counter for the assigned video
Each node receives async updates from peers
   ↓
Read API: any node returns current sum across all known peers
```

Sub-sharding is an alternative (split the hot key across many sub-shards, scatter-gather on read). Liu mentions both — CRDT is cleaner because reads don't fan out.

For each video, the CRDT pattern can also be applied across regions: each region's nodes track their region's count plus async-replicated counts from other regions. Cross-region propagation happens periodically; intra-region reads are fast.

## 5. Variant — Unique-User Count via HyperLogLog

Counting *unique users* (rather than total views) is a different problem. The exact answer requires storing every user_id ever seen — at scale, **50 TB** for a popular video.

**HyperLogLog** is a probabilistic structure that estimates cardinality at ~1% error using **~1 GB** instead of 50 TB. Liu mentions it as an option for the unique-views variant. Like CRDTs, two HLL sketches can be merged — a regional HLL plus a global HLL gives both regional and global unique-user counts from one structure.

## 6. Trade-offs

- **CRDT freshness.** Async propagation between nodes means a count read may be a few seconds stale. Acceptable for view counts; not acceptable for billing.
- **Sub-sharding alternative.** Easier to reason about (no CRDT machinery), but read fans out across all sub-shards. CRDT keeps reads cheap.
- **Storage cost.** Each node stores N counters per key (one per peer). For 1024 nodes and 1B videos, that's 1T entries — manageable but not free.
- **HLL precision.** 1% error is fine for "this video has approximately 5M unique viewers"; not fine for "this user voted exactly once."

## Sources

- [Liu Ch 6.05: Distributed Counter](software/system-design-interview/books/system-design-interview-fundamentals/ch06_05_distributed_counter.md)
