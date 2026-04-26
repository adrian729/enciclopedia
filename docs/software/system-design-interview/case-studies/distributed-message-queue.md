# Distributed Message Queue (Kafka-Style Broker)

> Vol 2 only — neither Liu nor Xu Vol 1 covers building a queue from scratch. The fundamentals page [Queues & Messaging](fundamentals/queues-and-messaging.md) covers when and why to *use* a queue; this page is how to **build** one. Three core design choices repeat: append-only **WAL** on disk, **zero-copy** message format end-to-end, and **pervasive batching** at producer, broker, and consumer.

## Table of Contents

- [1. Requirements](#1-requirements)
- [2. Topics, Partitions, Brokers](#2-topics-partitions-brokers)
- [3. Consumer Groups](#3-consumer-groups)
- [4. High-Level Architecture](#4-high-level-architecture)
- [5. On-Disk Storage Design](#5-on-disk-storage-design)
- [6. Message Format and Zero-Copy](#6-message-format-and-zero-copy)
- [7. Producer and Consumer Flows](#7-producer-and-consumer-flows)
- [8. Replication and ISR](#8-replication-and-isr)
- [9. Delivery Semantics](#9-delivery-semantics)
- [10. Scalability](#10-scalability)
- [11. Advanced Features](#11-advanced-features)
- [Sources](#sources)

## 1. Requirements

- Text messages in the KB range; configurable per-use-case throughput vs latency.
- Repeated or single consumption; in-order delivery within a partition; **two-week retention** with truncation.
- Configurable delivery semantics — at-most-once, at-least-once, exactly-once.
- Streaming-platform features (long retention, replay, ordering) on top of an MQ shape.

Prerequisites: read [Queues & Messaging](fundamentals/queues-and-messaging.md) for log-based vs pub-sub, delivery-semantics math, and when a queue is the right answer.

## 2. Topics, Partitions, Brokers

- **Topic** — a uniquely-named category that organizes messages.
- **Partition** — splits a topic into shards distributed across brokers; capacity scales by adding partitions. Each partition is a FIFO queue and the message position within it is the **offset**.
- **Broker** — a server that holds one or more partitions; the cluster of brokers is the queue backbone.
- **Message key → partition** — `hash(key) % numPartitions`. Same-key messages always land in the same partition, preserving per-key order. Missing key → random partition.

## 3. Consumer Groups

A consumer group is a set of consumers cooperating to read a subset of partitions; each group maintains its own offsets and can subscribe to multiple topics (e.g., one group per use case: billing, accounting).

**One-partition-one-consumer rule** — within a group, each partition is consumed by exactly one consumer to preserve order. Excess consumers (more than partitions) sit idle.

**Pre-allocate generously** — provision way more partitions than consumers up front; scaling consumers is then just adding instances, no partition resizing.

## 4. High-Level Architecture

Producer pushes; consumer group pulls. Each broker holds:

- **Data storage** — partitions on disk.
- **State storage** — consumer offsets.
- **Metadata storage** — topic configs.

A **coordination service** (Apache ZooKeeper or etcd) handles broker service discovery and elects an **active controller** (one per cluster) responsible for assigning partitions. See [Service Discovery & Load Balancing](fundamentals/service-discovery-and-load-balancing.md).

## 5. On-Disk Storage Design

- **WAL over a database** — relational and NoSQL options struggle with simultaneous heavy reads/writes at scale; an append-only log gives **pure sequential I/O** which rotational disks handle very well (hundreds of MB/s in RAID), and the OS aggressively caches pages in free RAM.
- **Segments** — a single log file can't grow forever, so each partition's log is split into segment files. Only the **active segment** receives appends; older segments are read-only and truncated when retention/capacity expires.
- **Folder layout** — segments live in `Partition-{:partition_id}` directories.

The "sequential disk myth": rotational disks are slow only for *random* access. WAL workloads are sequential and benefit from hardware optimizations down the entire stack.

## 6. Message Format and Zero-Copy

Every component (producer, broker, consumer) agrees on the same byte layout, so the message flows end-to-end without mutation. Mismatches force expensive copies.

| Field | Type |
|---|---|
| `key` | byte[] |
| `value` | byte[] |
| `topic` | string |
| `partition` | int |
| `offset` | long |
| `timestamp` | long |
| `size` | int |
| `crc` | int |

**Locator triple** — a message is uniquely found by `(topic, partition, offset)`. CRC guards integrity. Brokers serve reads via `sendfile(2)` straight from the page cache to the socket, never copying into user space.

> Reminder: message keys are not key-value-store keys. They need not be unique and aren't used for lookup, only for partition routing.

## 7. Producer and Consumer Flows

**Producer** — routing baked into the client library: read the replica plan, batch messages in an in-memory buffer, send directly to the leader replica's broker. No separate routing layer (extra hop avoided).

**Batch size tradeoff** — large batches → higher throughput, higher latency; small batches → lower latency, lower throughput. Tunable per use case.

**Pull vs push** — most queues choose **pull**: consumers control rate, scale out independently, and naturally batch fetches. Push wins on latency but risks overwhelming slow consumers. **Long-polling** fixes the empty-broker spin-wait problem of pull.

**Pull flow** — consumer hashes its group name to locate the **coordinator broker**, joins the group, gets partitions assigned (round-robin or range), fetches from the last committed offset in state storage, processes, then commits the new offset. Order of processing vs commit determines delivery semantics (§9).

**Rebalance protocol** — coordinator picks a **group leader**, leader generates the partition dispatch plan, coordinator broadcasts; followers ask coordinator for their assignments. Triggers: new consumer joins, consumer leaves cleanly, consumer crashes (missed heartbeats).

## 8. Replication and ISR

Each partition has multiple replicas (e.g., 3) on different brokers; one **leader**, others **followers**. Producers write only to the leader; followers pull from the leader. Leaders are elected via the coordination service. See [Replication](fundamentals/replication.md).

**In-Sync Replicas (ISR)** — replicas caught up to the leader within configured lag (e.g., `replica.lag.max.messages=4`). Leader is always in ISR. **Committed offset** = the highest offset acknowledged by all current ISRs.

| ACK level | Semantics | Use case |
|---|---|---|
| `all` | Wait for all ISRs (subject to `min.insync.replicas`) | Strongest durability, slowest |
| `1` | Wait for leader persist only | Low latency; lose messages if leader dies before follower sync |
| `0` | Fire and forget | Lowest latency; metrics where loss is acceptable |

**Read from leader** — simpler operationally; per-partition connection count is bounded since each partition is read by one consumer per group. Cross-DC consumers can read from the closest ISR for latency.

## 9. Delivery Semantics

- **At-most-once** — producer sends async with `ack=0`, no retries; consumer commits offset *before* processing. Messages may be lost, never redelivered.
- **At-least-once** — producer sends with `ack=1` or `ack=all` and retries; consumer commits offset *only after* processing succeeds. Messages may be redelivered (duplicates) but never lost.
- **Exactly-once** — most expensive in performance and complexity. Required when duplicates are unacceptable and downstream services lack idempotency. See [Concurrency & Transactions §9](fundamentals/concurrency-and-transactions.md#9-exactly-once-via-offset-transactions) for the offset-transaction pattern.

## 10. Scalability

- **Producers** — stateless, scale by adding instances.
- **Consumers** — groups isolate; rebalancing handles add/remove/crash automatically.
- **Brokers** — when a broker dies, the controller detects via heartbeats, generates a new replica plan, and new replicas catch up from leaders.
- **Adding brokers safely** — temporarily allow extra replicas: assign the new broker into the plan, let it catch up from the leader, then remove the now-redundant replica.
- **Replica placement rules** — never put all replicas of a partition on one node; cross-DC placement boosts safety but adds latency/cost.
- **Increasing partitions** is straightforward; **decreasing** is complicated — decommissioned partitions can't be deleted until retention expires (consumers may still be reading).

## 11. Advanced Features

- **Tag-based filtering** — attach tags in metadata (not payload — payload may be encrypted or expensive to deserialize); broker filters by tag list, supporting multi-dimensional filtering without parsing payloads.
- **Delayed messages** — sent to temporary on-broker storage with a timing function; delivered to the actual topic when the timer fires. Two implementations: predefined delay levels (RocketMQ uses 1s, 5s, …, 1h, 2h) or a hierarchical time wheel.
- **Scheduled messages** — same mechanism, fired at an absolute time.
- **Retry topics** — failed consumption goes to a dedicated retry topic so failures don't block the main flow.
- **Historical archival** — when retention truncates data, archive to HDFS or object storage if replayability beyond two weeks matters.

## Sources

- [Vol 2 Ch 4: Distributed Message Queue](software/system-design-interview/books/system-design-interview-vol2/ch04_distributed_message_queue.md)
