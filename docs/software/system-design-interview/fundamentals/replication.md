# Replication

> Liu provides the full taxonomy (leader-follower, leader-leader, leaderless, with sync/async variants); Xu introduces master-slave replication in his scaling-evolution chapter and revisits leaderless replication on the consistent-hashing ring in his Key-Value Store chapter. Both agree the industry-default replication factor is 3.

## Table of Contents

- [1. Why Replicate](#1-why-replicate)
- [2. Leader-Follower](#2-leader-follower)
  - [2.1. Synchronous Replication](#21-synchronous-replication)
  - [2.2. Asynchronous Replication and Replication Lag](#22-asynchronous-replication-and-replication-lag)
- [3. Leader-Leader](#3-leader-leader)
- [4. Leaderless Replication and Quorum](#4-leaderless-replication-and-quorum)
- [5. Replication on the Consistent-Hashing Ring](#5-replication-on-the-consistent-hashing-ring)
- [6. Failover](#6-failover)
- [Sources](#sources)

## 1. Why Replicate

Replication copies data across nodes for five benefits:

- **Availability** — survive single-node failure.
- **Durability** — survive disk loss.
- **Latency** — read from a geographically closer replica.
- **Bandwidth** — distribute read load across replicas.
- **Throughput** — more readers in parallel.

Industry-average replication factor: **3** (one primary plus two replicas, often spread across availability zones or data centers).

## 2. Leader-Follower

The simplest model. The leader takes writes; followers serve reads. Xu calls this "master-slave" in Ch 1; the modern term is leader-follower.

### 2.1. Synchronous Replication

The leader doesn't ack the write until at least one follower has the data. Follower freshness is guaranteed at the cost of write latency and write availability — if the synchronous follower is unreachable, writes block.

### 2.2. Asynchronous Replication and Replication Lag

The leader acks the write before the follower catches up. Faster, but introduces **replication lag** with two visible consequences:

- **Read-your-own-write inconsistency.** A user writes to the leader and reads from a follower; the read may not see the write yet. Mitigation: route the user's reads to the leader for a short window after a write, or to a "your own state" service backed by the leader.
- **Inconsistent reads from different replicas.** Round-robin reads return different results on successive calls. Mitigation: stick a session to one replica; use monotonically-increasing version tokens so the client can detect regression.

## 3. Leader-Leader

Multiple leaders accept writes. Survives a leader's death without promotion, and reduces write latency for geographically distributed users. The cost is **conflict resolution** — concurrent writes to the same key on different leaders must be merged. See [CAP, Consensus & Conflict Resolution](fundamentals/cap-consensus-and-conflict-resolution.md).

## 4. Leaderless Replication and Quorum

No designated leader. Writes go to multiple replicas in parallel; reads do too. The **quorum rule** controls consistency vs latency:

- `N` = number of replicas.
- `W` = write quorum (acks needed before a write is considered successful).
- `R` = read quorum (replicas read before a value is returned).
- `W + R > N` guarantees at least one overlapping replica between any read and any write — the read will see the latest write.

Common configurations (Xu Ch 6):

| Configuration | Use case |
|---|---|
| `R=1, W=N` | Read-optimized — fast reads, slow writes. |
| `W=1, R=N` | Write-optimized — fast writes, slow reads. |
| `N=3, W=R=2` | Balanced strong consistency. |

Conflicts during quorum propagation are resolved with **vector clocks**, **CRDTs**, or domain-specific logic (see [CAP, Consensus & Conflict Resolution](fundamentals/cap-consensus-and-conflict-resolution.md)).

## 5. Replication on the Consistent-Hashing Ring

Xu's Key-Value Store walks the [consistent-hashing ring](fundamentals/sharding-and-consistent-hashing.md) clockwise from a key's primary owner to find its `N - 1` replicas. Two practical refinements:

- **Skip virtual-node duplicates.** When using virtual nodes, the next clockwise position may belong to the same physical node; skip it and continue clockwise.
- **Spread replicas across data centers.** A replica in a different DC survives a regional outage.

## 6. Failover

If a follower dies, traffic routes elsewhere; replication backlog catches up when the follower returns. If the leader dies, a follower is promoted (election, often via consensus systems like ZooKeeper or Raft); recovery scripts handle whatever the new leader hadn't yet replicated. **Sloppy quorum with hinted handoff** (Xu Ch 6) handles transient unavailability without an election: the write is buffered on a healthy neighbor and replayed when the owner returns.

## Sources

- [Liu Ch 5.06: Replication](software/system-design-interview/books/system-design-interview-fundamentals/ch05_06_replication.md)
- [Xu Ch 1: Scale From Zero to Millions of Users](software/system-design-interview/books/system-design-interview-insiders-guide/ch01_scale_zero_to_millions.md) (master-slave section)
- [Xu Ch 6: Design a Key-Value Store](software/system-design-interview/books/system-design-interview-insiders-guide/ch06_design_a_key_value_store.md) (quorum, sloppy quorum, hinted handoff)
