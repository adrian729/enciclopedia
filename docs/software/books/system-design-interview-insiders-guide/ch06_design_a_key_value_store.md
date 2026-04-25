# Ch 6: Design a Key-Value Store

## Table of Contents

- [1. Problem and Design Goals](#1-problem-and-design-goals)
- [2. Single-Server Limitations](#2-single-server-limitations)
- [3. CAP Theorem](#3-cap-theorem)
- [4. Data Partition](#4-data-partition)
- [5. Data Replication](#5-data-replication)
- [6. Quorum Consensus](#6-quorum-consensus)
- [7. Consistency Models](#7-consistency-models)
- [8. Inconsistency Resolution: Versioning and Vector Clocks](#8-inconsistency-resolution-versioning-and-vector-clocks)
- [9. Failure Detection: Gossip Protocol](#9-failure-detection-gossip-protocol)
- [10. Handling Temporary Failures](#10-handling-temporary-failures)
- [11. Handling Permanent Failures: Anti-Entropy and Merkle Trees](#11-handling-permanent-failures-anti-entropy-and-merkle-trees)
- [12. Handling Data Center Outage](#12-handling-data-center-outage)
- [13. System Architecture](#13-system-architecture)
- [14. Write Path](#14-write-path)
- [15. Read Path](#15-read-path)

## 1. Problem and Design Goals

- **Key-value pair** — a non-relational store where each unique key (plain text or hashed, kept short for performance) maps to an opaque value (string, list, object). Examples include Amazon Dynamo, Memcached, Redis
- **Required operations** — `put(key, value)` to insert, `get(key)` to retrieve
- **Design characteristics** — pair size under 10 KB, ability to store big data, high availability under failures, high scalability, automatic add/remove of servers based on traffic, tunable consistency, low latency
- **Tradeoff awareness** — every design balances reads, writes, memory usage, and consistency vs availability; there is no perfect design

## 2. Single-Server Limitations

- **Naive approach** — store pairs in an in-memory hash table; fast but limited by memory
- **Single-server optimizations** — data compression, and keeping only frequently used data in memory while pushing the rest to disk
- **Why it fails at scale** — even with optimizations a single server hits capacity quickly, forcing a distributed design

## 3. CAP Theorem

- **CAP theorem** — impossible for a distributed system to simultaneously provide more than two of these three guarantees: Consistency, Availability, Partition Tolerance
- **Consistency** — all clients see the same data at the same time no matter which node they connect to
- **Availability** — any client which requests data gets a response even if some nodes are down
- **Partition Tolerance** — a partition is a communication break between two nodes; the system continues to operate despite network partitions

| Type | Guarantees | Sacrifices | Example use |
|---|---|---|---|
| CP | Consistency + Partition tolerance | Availability | Bank balance — block writes during partition rather than risk inconsistency |
| AP | Availability + Partition tolerance | Consistency | Keep accepting reads/writes; sync stale replicas after partition heals |
| CA | Consistency + Availability | Partition tolerance | Cannot exist in real-world distributed systems — network partitions are unavoidable |

- **Concrete partition scenario** — with replicas n1, n2, n3, if n3 is cut off: a CP system blocks writes on n1/n2 to preserve consistency; an AP system keeps serving and reconciles n3 later

## 4. Data Partition

- **Why partition** — large datasets cannot fit on one server; data must be split across many servers evenly with minimal movement on add/remove
- **Consistent hashing** — servers and keys are placed on a hash ring; a key is stored on the first server clockwise from its hash position (technique from Ch 5)
- **Automatic scaling** — servers can be added/removed automatically based on load
- **Heterogeneity** — virtual nodes assigned per server are proportional to its capacity, so stronger machines hold more data

## 5. Data Replication

- **N replicas** — after mapping a key to the ring, walk clockwise and pick the first N unique servers to hold copies (asynchronously); N is configurable
- **Virtual node caveat** — skip duplicates so the first N nodes map to N distinct physical servers
- **Cross-data-center replication** — nodes in one data center fail together (power, disasters); replicas should span data centers connected over high-speed networks

## 6. Quorum Consensus

- **Definitions** — N = number of replicas, W = write quorum (acks needed for a successful write), R = read quorum (responses needed for a successful read)
- **Coordinator** — a node acting as proxy between client and replicas; W = 1 means one ack to the coordinator suffices, not that data lives on one server
- **Latency vs consistency** — small W or R means fast operations; larger values give better consistency but the coordinator waits on the slowest replica
- **Strong consistency rule** — `W + R > N` guarantees at least one overlapping node holds the latest data
- **Common configurations** — `R=1, W=N` optimizes reads; `W=1, R=N` optimizes writes; `N=3, W=R=2` is the typical balanced strong-consistency setup

## 7. Consistency Models

- **Strong consistency** — every read returns the value of the most recent write; clients never see stale data, but achieving it usually requires blocking new operations until all replicas agree
- **Weak consistency** — subsequent reads may not reflect the latest write
- **Eventual consistency** — a form of weak consistency where, given enough time, all updates propagate and replicas converge; adopted by Dynamo and Cassandra and recommended for this design. Concurrent writes may produce inconsistent values that the client must reconcile on read

## 8. Inconsistency Resolution: Versioning and Vector Clocks

- **Versioning** — treat every modification as a new immutable version of the data so conflicts can be detected
- **Conflict scenario** — two servers update the same key simultaneously to different values (`johnSanFrancisco` vs `johnNewYork`), producing sibling versions v1 and v2 with no obvious winner
- **Vector clock** — a `[server, version]` pair list `D([S1, v1], [S2, v2], ...)` attached to each data item; on write to server Si, increment vi if present, else add `[Si, 1]`
- **Ancestor vs sibling** — version X is an ancestor of Y (no conflict) if every counter in X is ≤ the corresponding counter in Y; X and Y are siblings (conflict) if some counter in Y is less than X's
- **Conflict resolution** — when a client reads sibling versions it reconciles them and writes back a merged version that descends from both
- **Downsides** — clients must implement reconciliation logic; the `[server, version]` list can grow large. A length threshold drops oldest pairs at the cost of accuracy, but Amazon's Dynamo paper reports this has not been a problem in practice

## 9. Failure Detection: Gossip Protocol

- **Two-source rule** — one server saying another is down is not enough; require independent confirmations
- **All-to-all multicast** — straightforward but inefficient at scale
- **Gossip protocol** — each node keeps a membership list of `(member ID, heartbeat counter)`, periodically increments its own counter, and sends heartbeats to a random subset of nodes which propagate further. If a counter stops increasing for a predefined period, the member is marked offline and the news spreads through the gossip

## 10. Handling Temporary Failures

- **Sloppy quorum** — instead of strict quorum (which can block during failures), pick the first W healthy servers for writes and first R healthy servers for reads on the ring, ignoring offline nodes; improves availability
- **Hinted handoff** — when a server is unavailable, another temporarily handles its requests; once the original returns, the substitute hands the buffered changes back to restore consistency

## 11. Handling Permanent Failures: Anti-Entropy and Merkle Trees

- **Anti-entropy protocol** — keeps replicas in sync by comparing data and updating each replica to the newest version when a node is permanently lost
- **Merkle tree** — a hash tree where every non-leaf node is the hash of its children's labels; allows efficient and secure verification of large data structures
- **Build steps** — divide the key space into buckets (root-level nodes that bound tree depth), hash each key in a bucket, produce one hash per bucket, then build upward to the root by hashing children
- **Comparison** — start at root hashes; if equal, replicas match. If not, recurse into mismatched children to find exactly which buckets diverge, syncing only those
- **Efficiency** — data transferred is proportional to differences between replicas, not total data size. A typical setup uses one million buckets per one billion keys (~1000 keys per bucket)

## 12. Handling Data Center Outage

- **Cross-DC replication** — replicate across multiple data centers so users can still access data when one is fully offline due to power, network, or natural disasters

## 13. System Architecture

- **APIs** — clients call `get(key)` and `put(key, value)`; a coordinator node acts as proxy between client and storage nodes
- **Decentralization** — nodes sit on a consistent-hashing ring with the same set of responsibilities, so adding/removing nodes is automatic and there is no single point of failure
- **Replication** — data is replicated across multiple nodes (and data centers)

## 14. Write Path

- **Based on Cassandra's architecture** — applies to writes once a request reaches a node
- **Step 1** — persist the write to a commit log file (durability)
- **Step 2** — store the data in an in-memory cache (memtable)
- **Step 3** — when the memory cache is full or hits a threshold, flush to an **SSTable** (sorted-string table — a sorted list of `<key, value>` pairs) on disk

## 15. Read Path

- **Memory hit** — if the key is in the in-memory cache, return immediately
- **Disk fallback** — otherwise, consult a **bloom filter** (space-efficient probabilistic membership test) to decide which SSTables might contain the key
- **Read flow** — check memory; on miss, check bloom filter; query the candidate SSTables; return the result to the client
