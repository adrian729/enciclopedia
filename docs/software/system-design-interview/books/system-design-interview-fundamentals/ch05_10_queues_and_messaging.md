# Ch 5.10: Queues and Messaging

## Table of Contents

- [1. Why Queues](#1-why-queues)
- [2. Message Queue](#2-message-queue)
- [3. Publisher Subscriber](#3-publisher-subscriber)
- [4. Delivery Semantics and Guarantees](#4-delivery-semantics-and-guarantees)
- [5. Custom Queue](#5-custom-queue)

## 1. Why Queues

- **Purpose** — in asynchronous processing, a queue holds events waiting to be processed because processing speed is often slower than producing speed
- **Thundering herd protection** — without a queue, a burst of events can break downstream or cause events to be dropped
- **A queue does not automatically make the flow asynchronous** — the caller can still wait for the queue's result and make it synchronous; whether that wait is useful depends on the queue type
- **Deep-dive angle** — queue choice and its trade-offs (reliability, durability) is a rich area to explore in an interview

## 2. Message Queue

- **Model (Kafka-style)** — clients insert events as logs for a given topic (a user-defined category). Each topic can be partitioned; each partition preserves message ordering. Multiple partitions means no global ordering
- **Consumer offset** — each partition has a consumer that maintains a durable offset as batches are processed; on failure, it resumes from the last offset
- **Retention period** — event logs are retained for a window (Kafka default: 7 days) so consumers can still replay within that window
- **Strengths** — high throughput via horizontal scaling and additional partitions; good fit when the system ingests very high write rates (metrics, logs) and downstream aggregates
- **Costs** — complexity of sharding and durability; higher maintenance cost. Overkill for events like a ridesharing request where by the time you reprocess, the event is stale
- **Application complexity** — consumers are generally partition-aware so app developers must reason about which partition to connect to
- **Deep-dive discussion points**:
  - Horizontal scaling — sharding scheme, hotspots, how to query results after processing, replication scheme, rebalancing when partitions are added/removed (reuse knowledge from sharding and replication chapters)
  - Global ordering — are you willing to drop to one partition (sacrificing throughput) to guarantee it?
  - Retention period — longer retention = more storage, but safer for replays
- **Examples** — Kafka, Amazon Kinesis

## 3. Publisher Subscriber

- **Model** — subscribers subscribe to events based on configuration. The producer publishes to a message exchange, which forwards to each subscriber's queue per subscription. The consumer sends an acknowledgment on success, and the queue removes the event
- **Subscriber independence** — each subscriber behaves independently
- **No retention** — once the subscriber pulls, the event is removed; durability of processed data becomes the subscriber's responsibility, not the queue's. This eliminates the complexity and maintenance cost of durable storage in the queue itself
- **Fit** — use when events should be consumed and removed immediately. A ridesharing match request should be processed ASAP and discarded; there's no point replaying a 10-minute-old request
- **Examples** — RabbitMQ, Amazon SQS

## 4. Delivery Semantics and Guarantees

- **Why it matters** — the choice affects performance and user experience. A payments queue delivering more than once overcharges; failing to deliver undercharges

| Semantic | Producer behavior | Consumer behavior | Trade-off | Use cases |
|---|---|---|---|---|
| **At-Most-Once** | Fire-and-forget into the queue's acknowledgment | Poll and remove the message; consumer failure loses the message forever | Best throughput (low overhead); occasional event loss | Metrics collection (server health), driver location updates in ridesharing (another update arrives in 5–10 seconds) |
| **At-Least-Once** | If producer doesn't get an ack and resends, data may be duplicated in the queue | Consumer polls, commits the change, but fails to ack — event is processed again on retry | Guarantees no loss but may process multiple times; slightly worse throughput than at-most-once (needs acks on both sides) | Periodic file parse idempotent by `file_id`; notifications where occasional duplicates are tolerable (no need for idempotency if the product accepts duplicates) |
| **Exactly-Once** | Queue dedupes using an idempotent key — inserting the same event multiple times is coalesced | Processed exactly once | Worst throughput (idempotency check); simplest to reason about — behaves as people expect a queue to | Payment to a third party that doesn't handle idempotency; downstream so costly that reprocessing wastes resources |

- **Application-level exactly-once** — for queues that don't natively support exactly-once, use at-least-once delivery and handle idempotency in the application with a data store of processed events

## 5. Custom Queue

- **Queues can take many forms** — not every queue has to be a message queue or pub/sub. Pick the shape that makes sense for the question
- **Durable priority queue (relational table)** — a table with `event_id` and `priority_number`, indexed on priority, fetches highest-priority events first. Alternative: a table of `event_id` and `status`, grabbing all `pending` rows
- **In-memory FIFO queue** — e.g., a Java concurrent queue on the application server
- **In-memory priority queue** — a max heap where the root holds the highest-priority event. Discuss concurrent thread access and throughput impact, and what happens when the in-memory queue goes down
