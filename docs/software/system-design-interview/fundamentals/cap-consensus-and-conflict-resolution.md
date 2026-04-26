# CAP, Consensus, and Conflict Resolution

> Xu's Key-Value Store chapter is the longest single primitive in either book and covers CAP, quorum tuning, vector clocks, gossip, sloppy quorum, and Merkle trees end-to-end. Liu's Conflict Resolution chapter (5.11) adds CRDTs and the "keep records of conflict" pattern. Together they cover the entire AP/CP design space.

## Table of Contents

- [1. CAP Theorem](#1-cap-theorem)
  - [1.1. CP Systems](#11-cp-systems)
  - [1.2. AP Systems](#12-ap-systems)
- [2. Quorum Consensus](#2-quorum-consensus)
- [3. Vector Clocks](#3-vector-clocks)
- [4. Conflict Resolution Strategies](#4-conflict-resolution-strategies)
  - [4.1. Last Write Wins](#41-last-write-wins)
  - [4.2. CRDTs](#42-crdts)
  - [4.3. Keep Records of Conflict](#43-keep-records-of-conflict)
  - [4.4. Custom Resolution](#44-custom-resolution)
- [5. Gossip Protocol](#5-gossip-protocol)
- [6. Sloppy Quorum and Hinted Handoff](#6-sloppy-quorum-and-hinted-handoff)
- [7. Anti-Entropy with Merkle Trees](#7-anti-entropy-with-merkle-trees)
- [Sources](#sources)

## 1. CAP Theorem

A distributed system cannot simultaneously provide more than two of:

- **Consistency** — every read sees the latest write.
- **Availability** — every request gets a response.
- **Partition tolerance** — the system continues operating despite network partitions.

Real networks partition, so the practical choice is **CP** or **AP**.

### 1.1. CP Systems

Block writes during a partition to preserve consistency. Examples: banking, Google Drive metadata (Xu Ch 15), distributed locking via ZooKeeper.

### 1.2. AP Systems

Keep serving reads/writes through partitions and reconcile divergence later. Examples: Cassandra, Amazon Dynamo, news feeds, chat history.

Liu's caveat: CAP is necessary but not sufficient as a classification. MySQL with async-replicated followers isn't strictly "CP" once reads hit followers. Use CAP to frame the trade-off, not to slot a database into a category.

## 2. Quorum Consensus

For replicated stores (see [Replication](fundamentals/replication.md)):

- `N` = replicas, `W` = write quorum, `R` = read quorum.
- `W + R > N` guarantees overlap between reads and writes.

Common configurations:

| Config | Meaning |
|---|---|
| `R=1, W=N` | Read-optimized, slow writes. |
| `W=1, R=N` | Write-optimized, slow reads. |
| `N=3, W=R=2` | Balanced strong consistency. |

Quorum is how AP systems get *configurable* consistency without giving up availability entirely.

## 3. Vector Clocks

Each data item carries a list `[(server, version), ...]`. On a write to server `Si`, increment `vi` if `Si` is in the list, otherwise add `[Si, 1]`. Comparing two vector clocks reveals one of three states:

- **Ancestor** — every entry in `A` is `<=` the corresponding entry in `B`. `A` is older; no conflict.
- **Descendant** — symmetric. `B` is older.
- **Sibling** — neither dominates. **Conflict** — the client must reconcile and write back a merged version.

Vector clocks make conflict *detection* tractable; resolution is still a separate decision.

## 4. Conflict Resolution Strategies

### 4.1. Last Write Wins

Attach a timestamp; the higher timestamp wins. Simple but lossy (the loser disappears) and subject to clock skew. Tolerable for status updates ("user is online"); intolerable for shopping carts (lost items).

### 4.2. CRDTs

A **CRDT** (Conflict-Free Replicated Data Type) has each node track its own state plus asynchronously-replicated state from others, such that any node can compute the merged result deterministically.

Liu's canonical example: a **distributed counter**. Each node tracks its own count plus the latest known count from every other node. The total at any node is the sum of all per-node counts. Writes don't conflict — they append to one node's row. Reads converge to the same total once propagation completes.

Trade-off: high availability and low read latency at the cost of broadcast complexity and eventual consistency. See the [Distributed Counter case study](case-studies/distributed-counter.md).

### 4.3. Keep Records of Conflict

Both versions are persisted; the reader resolves at read time. Not lossy (no data is dropped), but pushes resolution complexity into the read path. Amazon shopping carts famously did this — the cart is the union of all conflicting versions, so adding items always wins.

### 4.4. Custom Resolution

Domain-specific logic. The extreme is **let a human resolve** — source-control merge conflicts work this way.

## 5. Gossip Protocol

Failure detection in a peer-to-peer cluster without a central coordinator. Each node maintains a member list with heartbeat counters; every period, each node randomly picks a peer and exchanges lists, increasing its own counter. A node whose counter hasn't increased in some interval is suspected dead, and the suspicion propagates as nodes gossip.

## 6. Sloppy Quorum and Hinted Handoff

When the canonical quorum can't be assembled (some replicas are temporarily down), Cassandra's **sloppy quorum** writes to the first `W` healthy nodes the writer can reach — even if some of those aren't the canonical replicas. The temporary node holds a **hint** for the down node; when the owner returns, the hint is replayed and removed.

Trade-off: availability through transient failures, at the cost of weaker durability guarantees during the failure window.

## 7. Anti-Entropy with Merkle Trees

For permanent failures (a replica disk lost, a long-down node returning), full data scans to detect drift are prohibitively expensive. A **Merkle tree** over the keyspace is a hash tree where each leaf hashes a key range and each internal node hashes its children. To compare two replicas:

1. Compare root hashes. If equal, replicas agree — done.
2. If different, recurse into the children and compare those hashes.
3. Only walk the subtrees that disagree.

The cost scales with the number of *differences*, not the size of the data.

## Sources

- [Liu Ch 5.11: Conflict Resolution](software/system-design-interview/books/system-design-interview-fundamentals/ch05_11_conflict_resolution.md)
- [Xu Ch 6: Design a Key-Value Store](software/system-design-interview/books/system-design-interview-insiders-guide/ch06_design_a_key_value_store.md) (CAP, quorum, vector clocks, gossip, sloppy quorum, Merkle trees)
