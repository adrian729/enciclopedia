# Ch 5.06: Replication

## Table of Contents

- [1. Definition](#1-definition)
- [2. Why Replicate](#2-why-replicate)
- [3. Leader-Follower Replication](#3-leader-follower-replication)
- [4. Consequences of Async Replication](#4-consequences-of-async-replication)
- [5. Handling Follower and Leader Failure](#5-handling-follower-and-leader-failure)
- [6. Leader-Leader Replication](#6-leader-leader-replication)
- [7. Leaderless Replication](#7-leaderless-replication)
- [8. Picking a Strategy and Replication Factor](#8-picking-a-strategy-and-replication-factor)

## 1. Definition

- **Replication** — copying data from one data source to other data sources; if DB A has records 1, 2, 3, after replication DB B also has 1, 2, 3
- **Not just databases** — the same strategies apply to cache servers and app servers with in-memory data structures

## 2. Why Replicate

- **Availability** — when one database is down, another serves live traffic
- **Durability** — when databases fail and break, replicated databases still hold the data so it isn't lost forever
- **Latency** — replicate to another data center or point of presence so data is physically closer to users; less distance means less travel time
- **Bandwidth** — bytes travel through fewer networks when data is closer; farther means more bottleneck networks to cross. Analogy: a 100-mile dinner delivery incurs more time and gas than a 1-mile one. CDNs apply the same principle
- **Throughput** — more databases with the same data means the system handles more requests

## 3. Leader-Follower Replication

- **Shape** — writes go to the leader; the system replicates to one or many followers; reads can hit any database
- **Synchronous replication** — the write waits for both leader and followers to commit before it's successful
  - Advantage: followers have up-to-date data on success
  - Disadvantages: slow and relatively unavailable — if any follower is far away latency is high/unpredictable; if any follower is unavailable the write fails, lowering overall availability
- **Asynchronous replication** — leader commits, then fires-and-forgets to followers
  - Advantage: faster writes, higher availability (follower failure doesn't fail the write)
  - Disadvantage: inconsistent data between leader and followers due to **replication lag** — time it takes to copy data from leader to followers

## 4. Consequences of Async Replication

> **Read Your Own Write** — if you write to the leader and read from the follower, the user may feel they didn't commit because the newest data hasn't reached the follower yet. For photo upload, if metadata queries go to read replicas, a user might not see their just-uploaded image. Think about the implication for the end-user.

> **Inconsistent Read from Different Read Replicas** — a round-robin load balancer across read replicas can return inconsistent results on successive reads. Acceptable for some applications, not others.

## 5. Handling Follower and Leader Failure

- **Follower failure** — detect the faulty follower and stop forwarding requests to it; beware of snowball effect where redirecting traffic to near-capacity followers brings them down too
- **Leader failure** — nobody handles writes until a replacement exists; either manually configure a follower as leader or run a leader election via quorum. Process takes time (timeouts + election), so the system can be down for seconds or more — unacceptable for some systems

## 6. Leader-Leader Replication

- **Motivation** — single-leader setups have no write path while the leader is down
- **Shape** — multiple leader nodes accept writes; the system replicates between leaders; each leader can still have follower replication for backup and reads
- **Advantages** — writes remain available if one leader dies; latency can improve when a leader is closer to the user
- **Caveats** — the failover leader may be farther away (worse performance) and subject to replication lag (not up to date)
- **Disadvantage** — conflict complexity when users write the same key to different leaders; multiple resolution strategies exist and the choice depends on the application. When a leader goes down, a new one still has to be selected for writes

## 7. Leaderless Replication

- **Quorum write** — write is committed to some replicas; if at least **w** nodes acknowledge, the write is considered successful
- **Quorum read** — read from some of the nodes; if at least **r** succeed, the read is considered successful
- **Tuning w and r** — higher values give stronger guarantees of up-to-date data; with *n* nodes, `w + r > n` provides a stronger guarantee than `w + r <= n`. If `r = n` you're guaranteed to find the latest data; if `w = n`, even `r = 1` guarantees latest reads
- **Availability** — example: with `n=3, w=2`, one node can be down and writes still succeed
- **Advantage** — no leader selection or election needed; cluster keeps taking reads and writes even when some nodes are down → better availability
- **Disadvantage** — data consistency complexity; multiple requests can write the same key to multiple nodes (like multi-leader), and during quorum write propagation it's unclear which update wins. Candidates should discuss the conflict resolution strategy

## 8. Picking a Strategy and Replication Factor

| Strategy | Writes | Reads | Availability on leader failure | Main complication |
|---|---|---|---|---|
| Leader-Follower (sync) | Leader only, waits for followers | Any node | Election/manual failover required | Slow writes, unavailable if any follower is down |
| Leader-Follower (async) | Leader only | Any node | Election/manual failover required | Replication lag, read-your-own-write |
| Leader-Leader | Any leader | Any node | Another leader takes over | Conflict resolution across leaders |
| Leaderless | Quorum of w nodes | Quorum of r nodes | No election needed | Conflict resolution during quorum propagation |

- **Strategy picking** — whenever you have a data source, replication is an option; list them out and reason through the trade-offs for databases, cache servers, or in-memory data structures
- **Replication factor** — industry average is 3. Higher means more cost to maintain and, under sync replication, worse query performance. Lower means weaker durability with fewer backup replicas. Discuss the trade-off in the interview
