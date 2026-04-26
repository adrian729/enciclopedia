# Sharding & Consistent Hashing

> Xu treats consistent hashing as a standalone primitive (full chapter, Ch 5); Liu folds it inside sharding strategy (Ch 5.07) and is *explicit* that it is not a silver bullet — it solves even distribution, not hot keys. Reading the two together gives the full picture.

## Table of Contents

- [1. Why Shard](#1-why-shard)
- [2. Horizontal vs Vertical](#2-horizontal-vs-vertical)
- [3. Choosing a Sharding Key](#3-choosing-a-sharding-key)
- [4. Naive Hash Sharding and the Rehashing Problem](#4-naive-hash-sharding-and-the-rehashing-problem)
- [5. Consistent Hashing](#5-consistent-hashing)
  - [5.1. The Ring](#51-the-ring)
  - [5.2. Adding and Removing Nodes](#52-adding-and-removing-nodes)
  - [5.3. Virtual Nodes](#53-virtual-nodes)
- [6. Hot Keys — What Consistent Hashing Doesn't Solve](#6-hot-keys--what-consistent-hashing-doesnt-solve)
- [7. Geo-Sharding](#7-geo-sharding)
- [8. When Not to Shard](#8-when-not-to-shard)
- [Sources](#sources)

## 1. Why Shard

Sharding divides data across servers. It applies to app servers, caches, and storage. Benefits: throughput, capacity, latency (smaller working sets per shard), and **perceived availability** — a failed shard only takes out its partition. Liu is sharp on a common claim: overall availability is *not* improved by sharding. The system as a whole has more failure points, not fewer.

## 2. Horizontal vs Vertical

- **Horizontal** — split rows across shards. Default in interviews.
- **Vertical** — split columns. Rare except as a tactical separation of hot vs cold columns.

## 3. Choosing a Sharding Key

The key determines distribution and query pattern. Two families:

- **Hash-based** — `hash(key) % N`. Even distribution, but range queries (`WHERE created_at BETWEEN ...`) must scatter-gather across all shards.
- **Range-based** — partition by key ranges (`A–F`, `G–M`). Range queries hit one or two shards. Bad for monotonically increasing keys (timestamps): all current writes hit the last shard.

The tradeoff is a recurring interview question.

## 4. Naive Hash Sharding and the Rehashing Problem

Naive `hash(key) % N` works at fixed `N`, but breaks when servers are added or removed. With `N` going from 4 to 5, *nearly every* key remaps. For caches, this produces a **cache-miss storm** that floods the origin. For databases, the migration is huge.

This is the problem consistent hashing solves.

## 5. Consistent Hashing

### 5.1. The Ring

Servers and keys are placed on a hash ring (Xu's example: the SHA-1 hash space, wrapped). A key's owner is the first server clockwise from the key's position. Per Wikipedia's definition Xu cites: only `k/n` keys need to be remapped on average when a slot is added or removed (where `k` is the number of keys and `n` is the number of slots).

### 5.2. Adding and Removing Nodes

Adding a server only relocates keys between the new node and its anticlockwise neighbor. Removing a server reassigns only that node's keys to the next clockwise neighbor. The disruption is bounded.

### 5.3. Virtual Nodes

Two practical issues with the basic ring: unequal partition sizes (servers with bad luck on hash placement get tiny or huge slices) and non-uniform key distribution (keys cluster in regions of the hash space). Both are solved with **virtual nodes** — each real server is represented by many virtual replicas scattered around the ring. More virtual nodes = better balance at higher memory cost.

Real-world systems built on consistent hashing (Xu's list): Amazon Dynamo, Apache Cassandra, Discord, Akamai, Maglev.

## 6. Hot Keys — What Consistent Hashing Doesn't Solve

Liu's emphasis: consistent hashing solves even distribution and migration minimization. It does *not* solve hot keys. A super-popular video, a celebrity user, an enterprise customer with 100× the traffic — these still hammer their assigned shard.

Mitigations (Liu Ch 5.07 and case studies):

- **Dedicated shards** for known whales (an enterprise customer with their own infrastructure).
- **Sub-sharding with scatter-gather.** The hot key is split across multiple sub-shards; each request fans out and aggregates. Used in distributed counters (Liu Ch 6.05).
- **Caching** in front of the hot shard.
- **Reframing the workload** — e.g., read-side aggregation for celebrity feeds while non-celebrities are pre-computed (the [News Feed](case-studies/news-feed.md) hybrid fanout).

## 7. Geo-Sharding

Top-level routing by geographic zone (US-West, EU, APAC). Works well when access is regional (ridesharing, food delivery). Falls apart for social graphs where friends span zones — the heuristic is that friends usually cluster geographically, but enough of them don't to require cross-zone aggregation.

## 8. When Not to Shard

Sharding is not the first resort. Before sharding, consider:

- **Cold storage** — moving infrequently accessed data out (see [Observability, Security, Cold Storage](fundamentals/observability-security-cold-storage.md)).
- **Compression** — reduces storage and bandwidth at the cost of CPU.
- **Batching** — amortizes per-write overhead.
- **Vertical scaling** — bigger boxes are simpler when the ceiling is far enough.

Sharding adds operational cost (resharding, cross-shard joins, hot-key issues) that's only worth paying when no cheaper option fits.

## Sources

- [Liu Ch 5.07: Sharding](software/system-design-interview/books/system-design-interview-fundamentals/ch05_07_sharding.md)
- [Xu Ch 5: Design Consistent Hashing](software/system-design-interview/books/system-design-interview-insiders-guide/ch05_design_consistent_hashing.md)
- [Xu Ch 1: Scale From Zero to Millions of Users](software/system-design-interview/books/system-design-interview-insiders-guide/ch01_scale_zero_to_millions.md) (database scaling and resharding section)
