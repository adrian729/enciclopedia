# Cheat Sheet

> Single-page reference for day-of review. Distilled from both books. For depth, follow the links.

## Table of Contents

- [1. The Framework](#1-the-framework)
- [2. Math Formulas](#2-math-formulas)
- [3. Capacity and Latency Numbers](#3-capacity-and-latency-numbers)
- [4. Decision Trees](#4-decision-trees)
  - [4.1. Database Choice](#41-database-choice)
  - [4.2. Replication Mode](#42-replication-mode)
  - [4.3. Cache Write Strategy](#43-cache-write-strategy)
  - [4.4. Real-Time Protocol](#44-real-time-protocol)
  - [4.5. Delivery Semantics](#45-delivery-semantics)
  - [4.6. ID Strategy](#46-id-strategy)
  - [4.7. Consistency Stance](#47-consistency-stance)
- [5. Recurring Patterns](#5-recurring-patterns)
- [6. Red Flags Checklist](#6-red-flags-checklist)

## 1. The Framework

| Step | What | Time |
|---|---|---|
| 1a | Functional requirements | 2–3 min |
| 1b | Non-functional requirements | 3–5 min |
| 2 | Define API | 3–5 min |
| 3 | High-level diagram | 5–7 min |
| 4 | Schema and data model | 5–7 min |
| 5 | End-to-end flow checkpoint | 2–3 min |
| 6 | Deep dives (run the magic formula) | 15–20 min |

**Sequencing rule:** math goes after API and schema, not before.

**Magic formula:** identify bottleneck → ≥2 options → trade-offs vs requirements → pick + stance → discuss → repeat.

**Golden question:** "What is the problem I am trying to solve?"

See [Framework](process/framework.md), [Communication](process/communication.md).

## 2. Math Formulas

```
QPS = (DAU × % making query × queries/user/day × scaling factor) / 100,000
Storage = DAU × % × queries × data size × replication × time horizon
```

- 86,400 sec/day ≈ 100K → divide by 100K, subtract 5 from the power of 10.
- Replication factor = 3 (default).
- Scaling factor = 5–10× for bursty workloads.

**Six-step calculation:** scientific notation → group 10s → group numbers → compute → readable units → *do something with the number*.

See [Estimation](process/estimation.md).

## 3. Capacity and Latency Numbers

| Power | Approx. | Unit |
|---|---|---|
| 2¹⁰ | 10³ | KB |
| 2²⁰ | 10⁶ | MB |
| 2³⁰ | 10⁹ | GB |
| 2⁴⁰ | 10¹² | TB |
| 2⁵⁰ | 10¹⁵ | PB |

| Operation | Latency |
|---|---|
| L1 cache | 0.5 ns |
| Main memory | 100 ns |
| 1 KB over 1 Gbps | 10 µs |
| Read 4 KB SSD | 150 µs |
| Same-DC round trip | 500 µs |
| Disk seek | 10 ms |
| CA → Netherlands → CA | 150 ms |

| Nines | Yearly downtime |
|---|---|
| 99% | 3.65 days |
| 99.9% | 8.76 hours |
| 99.99% | 52.6 min |
| 99.999% | 5.26 min |

**Single machine rough capacity:** ~10⁶ QPS for cheap reads; less for compute-heavy work.

## 4. Decision Trees

### 4.1. Database Choice

| Need | Pick |
|---|---|
| Default; ACID; joins | MySQL, PostgreSQL |
| Schemaless, nested objects | MongoDB |
| Analytics, range scans | Redshift, ClickHouse |
| Blobs (video, image, large files) | S3, GCS |
| Write-heavy time-series | Cassandra, HBase, BigTable |
| Full-text search | Elasticsearch |
| Cache, session store | Redis, Memcached |
| Consensus / coordination | ZooKeeper, etcd |

It's normal to use 2–3 stores in one design. See [Databases, Schema, Indexing](fundamentals/databases-schema-indexing.md).

### 4.2. Replication Mode

| Need | Pick |
|---|---|
| Read scaling, simple | Leader-follower (async) |
| No data loss on leader fail | Leader-follower (sync) |
| Multi-region writes | Leader-leader (with conflict res) |
| High availability with quorum tunability | Leaderless (Cassandra-style) |

`W + R > N` for quorum overlap. See [Replication](fundamentals/replication.md).

### 4.3. Cache Write Strategy

| Strategy | When |
|---|---|
| Write-through | Hot reads after writes; atomicity not critical |
| Write-back | Lowest write latency; can tolerate loss on cache crash |
| Write-around | Most durable; cache populates from reads |

**Invalidation:** prefer delete over update (idempotent). See [Caching](fundamentals/caching.md).

### 4.4. Real-Time Protocol

| Need | Pick |
|---|---|
| Bidirectional, low latency | WebSocket |
| Server → client only | SSE |
| Infrequent, one-way, no bursts | Long polling |
| Periodic UI refresh | Short polling or HTTP |

WebSocket is stateful — connections bind to one server (TCP four-tuple). Use a proxy farm. See [Real-Time Communication](fundamentals/real-time-communication.md).

### 4.5. Delivery Semantics

| Semantics | When |
|---|---|
| At-most-once | Metrics, telemetry, location updates |
| At-least-once | Idempotent operations, tolerable-duplicate notifications |
| Exactly-once | Payments to non-idempotent third parties |

App-level exactly-once = at-least-once + processed-event store. See [Queues & Messaging](fundamentals/queues-and-messaging.md).

### 4.6. ID Strategy

| Need | Pick |
|---|---|
| Opaque token, no ordering | UUID |
| 64-bit, time-sortable, distributed | Snowflake |
| Single-source, low scale | Auto-increment |
| Lock fencing | ZooKeeper sequence |
| Custom format (short URL codes) | Offline pre-generated pool |

Snowflake bit layout: 1 sign + 41 timestamp + 10 machine + 12 sequence = 64 bits. See [ID Generation](fundamentals/id-generation.md).

### 4.7. Consistency Stance

| Use case | Stance |
|---|---|
| Banking, file metadata | CP — strong consistency, block on partition |
| Chat, news feed, KV store | AP — eventual consistency, reconcile via vector clocks or CRDTs |
| Counters under hot keys | CRDT (per-node tracking, sum on read) |

CAP is necessary but not sufficient. See [CAP, Consensus & Conflict Resolution](fundamentals/cap-consensus-and-conflict-resolution.md).

## 5. Recurring Patterns

- **Bursty-write absorber:** queue → micro-batch aggregator → cache layer (e.g., min-heap) → durable store. Used in: Top YouTube, distributed counter, rate limiter, news feed fanout.
- **Hybrid fanout (push + pull):** push for normal users, pull for celebrities. Used in: news feed, chat for huge channels.
- **Long-tail cost split:** CDN for popular content, in-house storage for unpopular. Used in: YouTube.
- **Delta sync:** chunk + hash + only re-upload changes. Used in: cloud file storage, rsync, Dropbox.
- **CRDT for hot keys:** each node tracks own count; sum on read. Used in: distributed counter.
- **Sub-sharding with scatter-gather:** split a hot key across many shards. Alternative to CRDT.
- **Blob-then-metadata for distributed transactions:** persist the blob first; metadata write is the only transactional one; orphans cleaned up in background.
- **Sampling for resilience:** persist every Nth event; tolerate lost detail for huge cost savings.
- **Fail to open:** keep the user experience perceived-available with a degraded path (baseline price, generic recommendations, accept order without payment).
- **Product redesign over technical fix:** when concurrency or fanout gets hairy, ask if the product requirement can change (auto-assign vs user-pick driver).

## 6. Red Flags Checklist

Avoid these — both books mark them as instant down-level signals:

- Jumping to a solution before scope is clear.
- Adding a cache, sharding, or rate limiter without justifying why.
- Listing microservices instead of drawing the end-to-end flow.
- Calculating QPS before defining the API.
- Calculating storage before defining the schema.
- Skipping the end-to-end flow checkpoint.
- "I'll use NoSQL because it scales."
- "It really depends on the use cases" as a final answer.
- Going silent when stuck.
- Talking over the interviewer.
- Reciting how WebSocket works without tying it to the design.
- Naming **EdgeRank** components for a Facebook feed (over-studied trivia that complicates the conversation).
- Applying canned designs (Cassandra + Snowflake "because that's what Twitter does").
- Failing to ask clarifying questions.
- Failing to take a stance after listing options.

See [Communication & Evaluation](process/communication.md) for the full rubric.
