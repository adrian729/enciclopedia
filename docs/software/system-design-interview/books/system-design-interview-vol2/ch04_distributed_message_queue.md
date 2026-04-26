# Ch 4: Distributed Message Queue

## Table of Contents

- [1. Problem and Scope](#1-problem-and-scope)
- [2. Messaging Models](#2-messaging-models)
- [3. Topics, Partitions, Brokers](#3-topics-partitions-brokers)
- [4. Consumer Groups](#4-consumer-groups)
- [5. High-Level Architecture](#5-high-level-architecture)
- [6. On-Disk Storage Design](#6-on-disk-storage-design)
- [7. Message Data Structure](#7-message-data-structure)
- [8. Producer and Consumer Flows](#8-producer-and-consumer-flows)
- [9. Consumer Rebalancing](#9-consumer-rebalancing)
- [10. Replication and ISR](#10-replication-and-isr)
- [11. Scalability](#11-scalability)
- [12. Delivery Semantics](#12-delivery-semantics)
- [13. Advanced Features](#13-advanced-features)

## 1. Problem and Scope

- **Why message queues** — provide decoupling, independent scaling of producers/consumers, availability when components go offline, and asynchronous communication for better performance.
- **Traditional MQ vs event streaming** — RabbitMQ/RocketMQ/ActiveMQ/ZeroMQ are message queues; Kafka and Pulsar are event streaming platforms. Lines blur: RabbitMQ added an append-log-based streams feature; Pulsar can serve as a typical MQ. This chapter designs a queue with streaming-platform features (long retention, repeated consumption, ordering).
- **Functional requirements** — text messages in the KB range, repeated or single consumption, configurable delivery semantics (at-most-once / at-least-once / exactly-once), in-order delivery, two-week retention with truncation, configurable per-use-case throughput vs latency.
- **Adjustments for traditional queues** — RabbitMQ-style queues retain only enough memory for in-flight delivery, with small disk overflow, and don't guarantee order; this simplifies the design wherever those features can be dropped.

## 2. Messaging Models

| Model | Behavior | Notes |
|---|---|---|
| **Point-to-point** | One message → one consumer; removed from queue after ack | Common in traditional MQs; no retention |
| **Publish-subscribe** | One message → all subscribers of a topic | Native to this design via topics; point-to-point can be simulated by putting all consumers in one consumer group |

- **Topic** — a uniquely-named category that organizes messages; producers write to topics and consumers read from them.

## 3. Topics, Partitions, Brokers

- **Partition (sharding)** — splits a topic into shards distributed across brokers; capacity scales by adding partitions. Each partition is a FIFO queue and the message position within it is the **offset**.
- **Broker** — a server that holds one or more partitions; the cluster of brokers is the message-queue backbone.
- **Message key → partition** — `hash(key) % numPartitions`; messages with the same key (e.g., user ID) always land in the same partition, preserving per-key order. Missing key → random partition. Producers may override the mapping with custom logic.

## 4. Consumer Groups

- **Consumer group** — a set of consumers cooperating to consume a subset of partitions; each group maintains its own offsets and can subscribe to multiple topics (e.g., one group per use case: billing, accounting).
- **One-partition-one-consumer rule** — within a group, a partition is consumed by exactly one consumer to preserve order. Excess consumers (more than partitions) sit idle.
- **Pre-allocate generously** — provision way more partitions than consumers up front; scaling consumers is then just adding instances, no partition resizing required.

## 5. High-Level Architecture

- **Clients** — producer (pushes to topics) and consumer group (subscribes and pulls).
- **Broker** — holds partitions; messages persisted in **data storage**, consumer offsets in **state storage**, topic configs in **metadata storage**.
- **Coordination service** — Apache Zookeeper or etcd; handles broker service discovery and elects an **active controller** (one per cluster) responsible for assigning partitions.
- **Three core design choices** — sequential on-disk WAL to exploit disk + OS cache; immutable message format passed end-to-end without copying; pervasive batching at producer, broker, and consumer.

## 6. On-Disk Storage Design

- **WAL over a database** — relational and NoSQL options struggle with simultaneous heavy reads/writes at scale; a write-ahead log (append-only file, like MySQL redo log or ZooKeeper WAL) gives pure sequential I/O which rotational disks handle very well.
- **Segments** — a single log file can't grow forever, so each partition's log is split into segment files; only the **active segment** receives appends, older segments are read-only and truncated when retention/capacity expires.
- **Folder layout** — segments live in `Partition-{:partition_id}` directories.
- **Sequential disk myth** — rotational disks are slow only for random access; in RAID with sequential workloads they hit hundreds of MB/s, while the OS aggressively caches pages in free RAM, accelerating WAL reads.

## 7. Message Data Structure

- **Schema** — `key` (byte[]), `value` (byte[]), `topic` (string), `partition` (int), `offset` (long), `timestamp` (long), `size` (int), `crc` (int).
- **Zero-copy contract** — every component (producer, broker, consumer) agrees on the same byte layout, so the message can flow end-to-end without mutation; mismatches force expensive copies.
- **Locator triple** — a message is uniquely found by `(topic, partition, offset)`.
- **CRC** — cyclic redundancy check guards integrity.

> **Reminder** — message keys are not key-value-store keys: they need not be unique and aren't used for lookup, only for partition routing.

## 8. Producer and Consumer Flows

- **Routing baked into the producer client** — instead of a separate routing layer (extra network hop), the producer library reads the replica plan, batches messages in an in-memory buffer, and sends directly to the leader replica's broker.
- **Batch size tradeoff** — large batches → higher throughput, higher latency; small batches → lower latency, lower throughput. Tunable per use case.
- **Pull vs push** — most queues choose **pull**: consumers control rate, scale out independently, and naturally batch fetches. Push wins on latency but risks overwhelming slow consumers and is poor at batching. Long-polling fixes the empty-broker spin-wait problem of pull.
- **Pull flow** — consumer hashes its group name to locate the **coordinator broker**, joins the group, gets partitions assigned (round-robin / range), fetches from the last committed offset in state storage, processes, then commits the new offset. Order of processing vs commit determines delivery semantics.

## 9. Consumer Rebalancing

- **Coordinator broker** — one broker per consumer group; receives heartbeats, manages partition assignments, triggers rebalance on join/leave/crash/partition change. Distinct from the cluster-wide coordination service.
- **Rebalance protocol** — coordinator picks a **group leader**, leader generates the partition dispatch plan, coordinator broadcasts it; followers ask coordinator for their assignments.

| Trigger | Flow |
|---|---|
| New consumer joins | Sends join request → coordinator notifies all → all rejoin → leader generates plan → consumers consume new partitions |
| Consumer leaves cleanly | Sends leave → remaining heartbeats trigger rejoin → same flow |
| Consumer crashes | Missed heartbeats → marked dead after timeout → rebalance triggered |

## 10. Replication and ISR

- **Replication** — each partition has multiple replicas (e.g., 3) on different brokers; one **leader**, others **followers**. Producers write only to the leader; followers pull from leader. Leaders are elected via the coordination service; the active controller publishes the replica distribution plan into metadata storage.
- **In-Sync Replicas (ISR)** — replicas caught up to the leader within the configured lag (e.g., `replica.lag.max.messages=4`). Leader is always in ISR. **Committed offset** = the highest offset acknowledged by all current ISRs.
- **ACK tradeoffs**:

| ACK | Semantics | Use case |
|---|---|---|
| `all` | Wait for all ISRs (subject to `min.insync.replicas`) | Strongest durability, slowest |
| `1` | Wait for leader persist only | Low latency; lose messages if leader dies before follower sync |
| `0` | Fire and forget, no retry | Lowest latency; metrics/logging where loss is OK |

- **Read from leader** — simpler operationally and connection count is bounded since each partition is read by one consumer per group; if a topic is hot, scale by adding partitions. Cross-DC consumers can read from the closest ISR for latency.

## 11. Scalability

- **Producers** — stateless, scale by adding instances.
- **Consumers** — groups isolate; rebalancing handles add/remove/crash automatically.
- **Brokers** — when a broker dies, the controller detects it via heartbeats, generates a new replica plan, and new replicas catch up from leaders.
- **Adding brokers safely** — temporarily allow extra replicas: assign the new broker into the plan, let it catch up from leader, then remove the now-redundant replica.
- **Replica placement rules** — never put all replicas of a partition on one node (no fault tolerance, wasteful); cross-DC placement boosts safety but adds latency/cost. Loss of all replicas = permanent data loss.
- **Increasing partitions** — straightforward: existing data stays in place, new messages distribute across more partitions; producer is notified, consumers rebalance.
- **Decreasing partitions** — complicated: decommissioned partition can't be deleted until retention expires (consumers may still be reading). During the window producers write only to remaining partitions, consumers still read all; rebalance after retention.

## 12. Delivery Semantics

- **At-most-once** — producer sends async with `ack=0`, no retries; consumer commits offset before processing. Messages may be lost, never redelivered. Use case: monitoring metrics where some loss is fine.
- **At-least-once** — producer sends with `ack=1` or `ack=all` and retries on failure; consumer commits offset only after processing succeeds. Messages may be redelivered (duplicates) but never lost. Acceptable where consumers can dedupe (e.g., unique-key DB writes).
- **Exactly-once** — most expensive in performance and complexity; needed when duplicates are unacceptable and downstream services lack idempotency (financial transactions, payments, accounting).

## 13. Advanced Features

- **Message filtering by tag** — naive client-side filtering wastes bandwidth; a dedicated topic per consumer subtype tightly couples producer to consumers. Solution: attach **tags** in message metadata (not payload — payload may be encrypted or expensive to deserialize); broker filters by tag list, supporting multi-dimensional filtering without parsing payloads.
- **Delayed messages** — sent to a temporary on-broker storage with a timing function; delivered to the actual topic when the timer fires. Two implementations: predefined delay levels (RocketMQ uses 1s, 5s, 10s, …, 1h, 2h) or a hierarchical time wheel.
- **Scheduled messages** — same mechanism as delayed, fired at an absolute scheduled time.
- **Wrap-up topics** — protocols (AMQP, Kafka protocol), retry consumption via dedicated retry topics so failures don't block the main flow, historical archival to HDFS or object storage when truncated data must be replayable.
