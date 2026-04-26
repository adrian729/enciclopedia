# Key-Value Store

> Xu's Ch 6 only — Liu doesn't have a dedicated KV-store case study. This is the densest and most-foundational case study in either book; it's where consistent hashing, replication, vector clocks, gossip, and Merkle trees all come together. Most of the underlying primitives are covered in fundamentals pages; this page is the assembly.

## Table of Contents

- [1. Requirements](#1-requirements)
- [2. Single-Server Baseline](#2-single-server-baseline)
- [3. CAP Decision](#3-cap-decision)
- [4. Data Partitioning](#4-data-partitioning)
- [5. Replication](#5-replication)
- [6. Quorum Tuning](#6-quorum-tuning)
- [7. Consistency and Conflict Resolution](#7-consistency-and-conflict-resolution)
- [8. Failure Detection — Gossip](#8-failure-detection--gossip)
- [9. Failure Handling](#9-failure-handling)
  - [9.1. Temporary — Sloppy Quorum + Hinted Handoff](#91-temporary--sloppy-quorum--hinted-handoff)
  - [9.2. Permanent — Anti-Entropy with Merkle Trees](#92-permanent--anti-entropy-with-merkle-trees)
  - [9.3. Data Center Outage](#93-data-center-outage)
- [10. Putting It Together](#10-putting-it-together)
- [Sources](#sources)

## 1. Requirements

- `get(key) → value`
- `put(key, value)`
- Horizontally scalable, low latency, highly available.

## 2. Single-Server Baseline

A naive in-memory hash table works on one server. Caps out fast — RAM is finite, single-node availability is bounded by uptime. Distribution surfaces every interesting problem.

## 3. CAP Decision

A distributed KV must handle network partitions, so the choice is **CP or AP**:

- **CP** — block writes during a partition; preserve consistency. Banking, distributed locks.
- **AP** — keep serving reads/writes through partitions; reconcile divergence later. Cassandra, Dynamo, most modern KV stores.

Xu picks AP for the canonical KV-store design. See [CAP, Consensus & Conflict Resolution](fundamentals/cap-consensus-and-conflict-resolution.md).

## 4. Data Partitioning

[Consistent hashing](fundamentals/sharding-and-consistent-hashing.md) places servers and keys on a ring. The first server clockwise from a key is its primary owner. **Virtual nodes** smooth out unequal partitions, with the count tunable to reflect heterogeneous server capacity (a 2× server gets 2× virtual nodes).

## 5. Replication

Replicate each key to **N nodes** by walking clockwise on the ring from the primary owner. Two practical refinements:

- Skip virtual-node duplicates that map to the same physical node.
- Spread replicas across data centers for regional outage survival.

See [Replication](fundamentals/replication.md).

## 6. Quorum Tuning

`W + R > N` guarantees overlap between any read and any write. Common picks:

| Configuration | Use case |
|---|---|
| `R=1, W=N` | Read-optimized — fast reads, slow writes. |
| `W=1, R=N` | Write-optimized — fast writes, slow reads. |
| `N=3, W=R=2` | Balanced strong consistency. |

Tuning lets the same KV substrate serve both consistency-leaning and availability-leaning use cases.

## 7. Consistency and Conflict Resolution

Eventual consistency is the AP norm. Concurrent writes to the same key on different replicas produce divergent versions. The resolution mechanism:

- **Vector clocks** detect whether two versions are ancestor/descendant (no conflict) or siblings (conflict — client must merge).
- The client receives all conflicting versions on read and writes back a merged version.
- Application semantics determine what "merge" means (e.g., shopping cart = union of items).

See [CAP, Consensus & Conflict Resolution](fundamentals/cap-consensus-and-conflict-resolution.md) for the mechanism.

## 8. Failure Detection — Gossip

A peer-to-peer **gossip protocol** distributes node-liveness information without a central coordinator. Each node maintains a member list with heartbeat counters; periodically it picks a peer at random, exchanges lists, and increments its own counter. A node whose counter hasn't risen in some interval is suspected dead — and the suspicion propagates as nodes gossip.

## 9. Failure Handling

### 9.1. Temporary — Sloppy Quorum + Hinted Handoff

When some replicas are temporarily down, write to the first `W` healthy nodes the writer can reach (even if some aren't the canonical replicas). The temporary node holds a **hint** for the down node; when the owner returns, the hint is replayed and removed.

Trade-off: keeps writes flowing through transient failure at the cost of weaker durability guarantees during the failure window.

### 9.2. Permanent — Anti-Entropy with Merkle Trees

For long-down nodes returning, full data scans to detect drift are prohibitively expensive. A **Merkle tree** over the keyspace lets two replicas compare:

1. Compare root hashes. If equal, agree — done.
2. If different, recurse into children. Compare their hashes.
3. Walk only the subtrees that disagree.

Cost scales with the *number of differences*, not data size.

### 9.3. Data Center Outage

Replicas span multiple DCs. A regional outage takes some replicas offline; quorum can still be assembled from survivors. Cross-DC writes increase latency (~150 ms transcontinental); systems often serve reads locally and replicate writes asynchronously.

## 10. Putting It Together

A complete picture of an AP KV store:

```
Client
  ↓
Coordinator (any node — chosen via consistent hashing of the key)
  ↓
N replicas (consistent-hash ring, walked clockwise from primary)
  ↓                     ↓
Vector clocks       Gossip (failure detection)
Read: R replicas    Anti-entropy: Merkle tree comparison
Write: W replicas   Hinted handoff for temporary failures
```

Production examples that match this template: Amazon Dynamo (the original), Apache Cassandra, Riak.

## Sources

- [Xu Ch 6: Design a Key-Value Store](software/system-design-interview/books/system-design-interview-insiders-guide/ch06_design_a_key_value_store.md)
