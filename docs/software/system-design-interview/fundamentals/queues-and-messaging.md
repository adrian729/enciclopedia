# Queues & Messaging

> Liu's chapter (5.10) is the deeper reference on system types and delivery semantics; Xu introduces queues in his scaling-evolution chapter as a decoupling primitive and reuses them in nearly every product design (notification per-channel queues, transcoding pipeline, news feed fanout). The headline rule both agree on: a queue does not automatically make a flow asynchronous.

## Table of Contents

- [1. Why Queue](#1-why-queue)
- [2. Two System Types](#2-two-system-types)
  - [2.1. Message Queue (Log-Based)](#21-message-queue-log-based)
  - [2.2. Publisher-Subscriber](#22-publisher-subscriber)
- [3. Delivery Semantics](#3-delivery-semantics)
- [4. Custom Queue Shapes](#4-custom-queue-shapes)
- [5. When a Queue Is the Right Answer](#5-when-a-queue-is-the-right-answer)
- [Sources](#sources)

## 1. Why Queue

Queues hold events waiting to be processed because processing is often slower than producing, and they protect downstream from thundering herds. Producer and consumer scale independently. A queue does *not* make the flow async by itself — that requires the producer not to wait for the consumer.

Common reasons to introduce one:

- **Spike absorption** — bursty traffic feeds a queue; consumers drain at a steady rate.
- **Decoupling** — producer doesn't know who consumes, or how many consumers exist.
- **Retry buffer** — failed deliveries to a third party (e.g., FCM in [Notification System](case-studies/notification-system.md)) re-enqueue without blocking new requests.
- **Pipeline staging** — successive transformations run as independent stages (Xu's YouTube transcoding DAG).

## 2. Two System Types

### 2.1. Message Queue (Log-Based)

Examples: Kafka, Amazon Kinesis. Per-topic partitions, durable consumer offsets, retention windows for replay. High-throughput; a single message can be consumed by multiple independent consumers reading at different offsets.

Trade-off: durability is high, but reprocessing 10-minute-old events is often pointless (a stale ridesharing request shouldn't be matched). The retention window doesn't always match the use case.

### 2.2. Publisher-Subscriber

Examples: RabbitMQ, Amazon SQS. Each subscriber gets its own queue; messages are removed on acknowledgment. No retention beyond ack. Fits when events should be consumed once, immediately.

Liu's mental model: log-based for replayable streams; pub-sub for "just deliver this once and remove it."

## 3. Delivery Semantics

Three flavors, in order of throughput cost:

| Semantics | Meaning | Best for |
|---|---|---|
| At-most-once | Fire-and-forget; occasional loss tolerated | Metrics, driver location updates, telemetry |
| At-least-once | Producer retries until ack; may double-deliver | Idempotent file parses, tolerable-duplicate notifications |
| Exactly-once | Queue dedupes on an idempotent key | Payments to a third party that doesn't handle idempotency |

**Application-level exactly-once** pairs at-least-once delivery with a data store of processed events: each consumer checks the store before acting. This is the pattern most "exactly once" production systems actually run.

## 4. Custom Queue Shapes

Not every queue needs to be Kafka-or-RabbitMQ. Liu's reminders:

- **Durable priority queue** backed by a relational table — query by priority, lock-and-claim a row.
- **In-memory FIFO** for transient workloads (a worker's local task list).
- **Max-heap** for top-K aggregation in a streaming pipeline (used in Liu's Top YouTube Video case study).

The shape follows the access pattern.

## 5. When a Queue Is the Right Answer

A queue is justified when at least one of these is true:

- Producer rate exceeds consumer rate, even briefly (spikes).
- Consumer can be slow or unavailable without affecting the producer (decoupling).
- Multiple consumer types need the same events (pub-sub).
- The pipeline has discrete stages with different scaling profiles (transcoding, fanout).
- A retry buffer is needed for unreliable downstreams.

Queues add operational cost (offsets, dead-letter handling, ordering guarantees, retention tuning). Adding one without justification reads as hand-wavy.

## Sources

- [Liu Ch 5.10: Queues and Messaging](software/system-design-interview/books/system-design-interview-fundamentals/ch05_10_queues_and_messaging.md)
- [Xu Ch 1: Scale From Zero to Millions of Users](software/system-design-interview/books/system-design-interview-insiders-guide/ch01_scale_zero_to_millions.md) (message queue section)
- [Xu Ch 10: Design a Notification System](software/system-design-interview/books/system-design-interview-insiders-guide/ch10_design_a_notification_system.md) (per-channel queue isolation)
