# Ch 7: Scatter/Gather

## Table of Contents

- [1. Pattern Definition](#1-pattern-definition)
- [2. Root Distribution (Replicated Leaves)](#2-root-distribution-replicated-leaves)
- [3. Leaf Sharding](#3-leaf-sharding)
- [4. Choosing the Right Number of Leaves](#4-choosing-the-right-number-of-leaves)
- [5. Scaling for Reliability and Scale](#5-scaling-for-reliability-and-scale)

## 1. Pattern Definition

- **Scatter/gather pattern** — a tree-shaped serving pattern that uses replication for scalability *in time*, farming a single request out to many leaves in parallel and merging their partial responses at the root.
- **Root vs. leaves** — the root distributes the incoming request to all leaf replicas simultaneously, then combines the partial results into one final response back to the client.
- **Sharding the computation** — unlike replicated (per-request scaling) or sharded (per-data scaling) patterns, scatter/gather shards the work needed for *one* request, so it fits problems with large amounts of mostly-independent processing per request.

## 2. Root Distribution (Replicated Leaves)

- **Root distribution** — the simplest variant: every leaf is homogeneous (holds the same data) and the root distributes pieces of the work across leaves to parallelize a single request — equivalent to solving an "embarrassingly parallel" problem.
- **Cross-machine vs. multi-threaded** — parallelizing across machines (e.g., 30 leaves) avoids the memory/network/disk bandwidth bottlenecks that cap multi-threaded single-machine speedups, keeping CPU as the bottleneck.
- **Dynamic load redistribution** — because every leaf can handle every request, the root can route work to faster nodes when one leaf slows down (e.g., a noisy neighbor), preserving response time.
- **Hands-On: distributed document search** — search documents containing both "cat" and "dog" by building an inverted index (word → list of documents); the root farms one leaf per word and returns the *intersection* of the per-word document sets.

## 3. Leaf Sharding

- **Leaf sharding** — when total data exceeds the memory or disk of one machine, partition data across leaves; every request is sent to *all* shards, each searches its slice, and the root merges partial results.
- **Patent-search example** — patents partitioned across machines (using e.g. patent number modulo shard count to avoid having to add shards as new patents register); a query for "rockets" is broadcast to every shard and the root collates matches.
- **Hands-On: sharded document search** — for the "cat" AND "dog" query under sharding, each leaf locally returns documents matching both terms; the root then takes the *union* across shards (whereas with replicated leaves the root took an intersection across per-term leaves).

## 4. Choosing the Right Number of Leaves

- **Parallelization gains are asymptotic** — every leaf adds constant per-request overhead (parsing, HTTP, etc.); as leaf count grows this overhead eventually dominates the actual business-logic compute.
- **Straggler problem** — the root must wait for *all* leaves before responding, so overall latency is set by the slowest leaf; rare tail latencies on individual leaves become common at the system level.
- **Tail-latency math** — with a 99th-percentile latency of 2s on one leaf, scattering to 5 leaves makes 2s a 95th-percentile event (0.99^5 ≈ 0.95); scattering to 100 leaves makes 2s essentially guaranteed.
- **p99 matters more here** — because every user request becomes many backend requests, tail-percentile performance dominates user-visible behavior more than in non-scatter systems.
- **Availability suffers symmetrically** — with a 1% per-leaf failure rate and 100 leaves, nearly every user request fails; reliability of individual leaves must be much higher than in non-scatter systems.

## 5. Scaling for Reliability and Scale

- **Single-replica shards are fragile** — every request needs every shard, so one shard's failure or upgrade kills all requests; you can't simply add shards to gain compute since more shards worsens stragglers and overhead.
- **Replicated, sharded scatter/gather** — replicate each leaf shard so the root load-balances each shard request across that shard's healthy replicas, masking failures and enabling rolling upgrades under load (potentially across multiple shards at once).
