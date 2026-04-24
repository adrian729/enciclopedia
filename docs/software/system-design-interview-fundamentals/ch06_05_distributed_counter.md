# Ch 6.05: Distributed Counter

## Table of Contents

- [1. Requirements](#1-requirements)
- [2. API](#2-api)
- [3. High-Level Design](#3-high-level-design)
- [4. Schema](#4-schema)
- [5. End-to-End Flow](#5-end-to-end-flow)
- [6. Deep Dives](#6-deep-dives)

## 1. Requirements

- **Prompt** — track how many times users view a YouTube video
- **Scope narrowed to**: total count only (no time buckets), purpose is to show popularity to the user (no financial tie for now), viewing the same video twice counts twice, count shown only on video page load
- **Assumptions** agreed with interviewer:
  - **500M DAU** worldwide, each views **10 videos/day**
  - **Long-tail** video popularity
  - **Accuracy** should be as close as possible (possible financial tie in the future) — some leeway
  - **Freshness** — within an **hour or two** is acceptable
  - **Consistency** — not important: two users won't coordinate on the exact count, no causal ordering
  - **Availability** — extremely important; the counter must not block video page load
  - **Durability** of the count — very important
  - **Latency** target: **p99 300 ms** for page load

## 2. API

```
view_video(video_id) → count
```

- `view_video` is the video page load API; viewing a video both fetches the count and increments it
- Video service may return the current count + 1 optimistically instead of waiting for the write to complete

## 3. High-Level Design

- **View queue** absorbs the high write QPS from `view_video`
- **View metrics processor** pulls from the queue and writes counts to view storage
- **Video service** reads the latest count from view storage for page load

## 4. Schema

**View Queue** — only the video ID is needed (no aggregation by user or time)

| Video Id |
|---|

**View Storage** — count per video

| Video Id | Count |
|---|---|

## 5. End-to-End Flow

- **`view_video`**: user → video page load → event fired to view queue → view metrics processor → view storage
- **Read path**: video service reads count from view storage; to hide write latency, service may increment by one locally and return that value to the user

## 6. Deep Dives

- **Math**: 500M DAU × 10 videos/day × 10× peak = **5×10¹⁰ QPD ≈ 500,000 QPS** for both read and write
- **Hot key**: popular video at 0.1% of traffic = **500 QPS** on a single shared key — significant contention

### 6.1 Scale for the Write Throughput — Delay Data

- **Options**:

| Option | Upside | Downside |
|---|---|---|
| **Stream Processing** | Near real-time count | Contention on shared row key for a hot video |
| **Batch Job** — hourly MapReduce over view logs keyed by `video_id` | Eliminates real-time contention | Results delayed by batch interval |

- **Conclusion** — **Batch Job**. The 1–2 hour freshness allowance removes all near-real-time complexity

### 6.2 Scale for the Write Throughput — Near Real-Time

- **Changed requirement** — near real-time view count
- **Options**:

| Option | Upside | Downside |
|---|---|---|
| **Partition the Database Table** — consistent-hash shard by `video_id`; row-level lock for atomic increment | Scales unpopular videos across machines | Hot video still contends on a single row |
| **Shard Further into Multiple Rows** — `[video_id]_1..N` with a `video_id → row_shard_count` mapping; scatter-gather on read | Per-key throughput multiplies by N | Slower reads via scatter-gather; still bounded by a single machine |
| **Shard a Video Key Across Machines** — round-robin writes to multiple machines, each using option 2 internally; scatter-gather on read | Scales a key beyond a single machine | High read latency across machines; availability suffers during leader re-election |
| **CRDT** — each machine takes writes locally; periodically, asynchronously publishes its count to all other nodes; each node has an eventually consistent view | Single-host read; high write throughput; highly available | Extra complexity to implement CRDT |
| **Sample the Video Count** — client sends events with 10% probability, server multiplies by 10 | Reduces QPS by 90% | Sacrifices accuracy — conflicts with the accuracy requirement |

- **Conclusion** — **CRDT**. Strong consistency isn't required; meets latency (single-host read), handles write throughput, and is highly available. Complexity is justified at this scale

### 6.3 Idempotency of Metrics

- **Problem** — if the server commits but the client never gets an ack, retries double-count; at the view queue it's ambiguous whether two events are two views or one retried view
- **Options**:

| Option | Upside | Downside |
|---|---|---|
| **At-Most-Once** — producer doesn't wait for ack | Never double-sends; best throughput | Events can be dropped (undercount) |
| **At-Least-Once** — producer retries on missing ack | No dropped events | Overcounts; throughput slightly worse |
| **Exactly-Once** — idempotency key = `(user_session, timestamp)` checked against temporary storage | Accurate | Needs extra idempotency storage and session metrics; worse throughput |

- **Conclusion** — **At-Most-Once** for simplicity and throughput — retry-driven overcounts would be significantly worse than rare undercounts. A variant of exactly-once is likely needed long term so that page refreshes don't double-count within a timeframe

### 6.4 Number of Unique Users

- **Changed requirement** — count unique users, not total views. API becomes `view_video(user_id, video_id)`. Assume **100M videos**, average **50,000 unique users** per video, `user_id` = 8 bytes (round to 10)
- **Options**:

| Option | Memory | Accuracy |
|---|---|---|
| **Set data structure** — `video_id → {user_id}` | 100M × 50,000 × 10 bytes = **50 TB** | Exact |
| **HyperLogLog** — probabilistic cardinality; one BigInt per video | 100M × 10 bytes = **1 GB** (fits in memory) | Approximate |

- **Conclusion** — **HyperLogLog**. Massive memory savings; acceptable if unique-count accuracy tolerance allows. Scale up with exact structure if tighter accuracy required

> **Warning** — HyperLogLog is an advanced data structure not always expected in a system design interview, but useful when similar questions come up.

### 6.5 Scaling for Read

- **Assumption** — CRDT is in use; each node stores counts on disk. Read throughput = 500,000 QPS
- **Options**:

| Option | Upside | Downside |
|---|---|---|
| **Add More Nodes to CRDT** | More nodes to absorb reads | More fan-out between nodes as each machine pushes to all others |
| **Replicate to Read Replicas** — async replication | Redundancy; read QPS scales | Eventual consistency (fine — CRDT is already eventually consistent) |
| **Read-Through Cache** — cache miss reads from node and populates | Scales reads via cache replicas | Cache invalidation near-impossible — count updates sub-second |
| **Periodic Update to Cache** — scheduled push of latest counts into the cache, no read-through | Cache never cold; scales with cache cluster; cache can be warmed on next update after failure | Periodic delay (tunable) |

- **Conclusion** — **Periodic Update to Cache** for read scale, plus **Read Replicas** for redundancy only (not read scale). Eventual consistency already accepted in the non-functional requirements
