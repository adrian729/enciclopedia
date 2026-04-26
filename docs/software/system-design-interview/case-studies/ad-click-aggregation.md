# Aggregate Ad Click Events

> Vol 2 only — neither Liu nor Xu Vol 1 covers ad-tech aggregation. The interesting move is **billing-grade exactly-once** semantics: pair event-time aggregation with watermarks for slightly-late events, end-of-day reconciliation against the raw log for very-late events, and wrap "downstream ack + offset commit" in a single distributed transaction. The exactly-once mechanism lives in [Concurrency & Transactions §9](fundamentals/concurrency-and-transactions.md#9-exactly-once-via-offset-transactions); idempotency keys live in [§7](fundamentals/concurrency-and-transactions.md#7-idempotency-keys-as-primary-keys).

## Table of Contents

- [1. Requirements](#1-requirements)
- [2. Data Model and APIs](#2-data-model-and-apis)
- [3. High-Level Architecture](#3-high-level-architecture)
- [4. Aggregation Service (MapReduce DAG)](#4-aggregation-service-mapreduce-dag)
- [5. Time, Watermarks, and Windows](#5-time-watermarks-and-windows)
- [6. Delivery Guarantees](#6-delivery-guarantees)
- [7. Scaling and Hotspots](#7-scaling-and-hotspots)
- [8. Fault Tolerance and Reconciliation](#8-fault-tolerance-and-reconciliation)
- [Sources](#sources)

## 1. Requirements

- Ingest raw click logs and produce per-minute counts for Real-Time Bidding (RTB) feedback, billing, and dashboards (CTR, CVR). Errors translate directly into millions of dollars of advertiser charges.
- **Three queries** — clicks of `ad_id` in last `M` minutes; top-100 most-clicked ads in last 1 minute (configurable); both filterable by `ip`, `user_id`, or `country`.
- Edge cases: **late events**, **duplicate events**, partial system failures.
- Latency: a few minutes end-to-end (RTB itself is sub-second; aggregation is not). Workload is **billing-grade** — correctness beats latency.
- Scale: 1B DAU × 1 click/user/day → ~10K QPS avg, 50K peak. 0.1 KB/event → 100 GB/day, ~3 TB/month. 2M total ads. 30% YoY growth.

## 2. Data Model and APIs

```
GET /v1/ads/{ad_id}/aggregated_count?from=&to=&filter=
GET /v1/ads/popular_ads?count=&window=&filter=
```

**Raw + aggregated, both stored.** Raw is the immutable source of truth for replay/debugging (movable to cold storage); aggregated is the active query-optimized layer. Querying raw directly is too slow; relying only on aggregates loses information after a bug.

**Aggregated row shape** — `(ad_id, click_minute, count)`; with filters, an extra `filter_id` column splits a minute into one row per active filter (e.g., `country=US`).

**Top-N table** — separate `most_clicked_ads(window_size, update_time_minute, most_clicked_ads[])` precomputed every minute.

**Database choice — NoSQL time-series**. Workload is write-heavy (10–50K QPS). Cassandra (or InfluxDB) suits both raw and aggregated stores: tuned for writes and time-range queries. Aggregated is also read-heavy (every ad polled every minute → 2M reads/min), so the same database type serves both.

## 3. High-Level Architecture

```
Sources → log watcher → Kafka Q1 (raw) → Aggregation → Kafka Q2 (per-min) → DB writer → DB
                                       ↑
                            recalculation service (replay)
```

**Why two queues, not direct DB writes?** The second queue is required to achieve **end-to-end exactly-once** semantics between aggregation output and storage. The atomic commit happens between Q2 ack and offset commit on Q1.

**Lambda vs Kappa** — Lambda runs separate batch and streaming paths (two codebases). **Kappa** uses one stream-processing engine for both real-time and reprocessing. The design adopts **Kappa**: historical replay reuses the same aggregation service, just pointed at raw data.

**Recalculation flow** — recalculation service pulls raw data in batch → routes through a **dedicated** aggregation service (so live traffic isn't impacted) → second queue → DB. Triggered when a bug requires recomputing aggregates from a known point.

## 4. Aggregation Service (MapReduce DAG)

Break the pipeline into Map / Aggregate / Reduce nodes; each does one task and forwards results downstream via TCP (cross-process) or shared memory (cross-thread).

- **Map** — reads, cleans/normalizes, and routes events (e.g., `ad_id % 2` to two downstream nodes). Needed even with Kafka partitioning because the producer may not control partition placement.
- **Aggregate** — counts events by `ad_id` in memory each minute. In MapReduce terms it's part of Reduce, so the pipeline is really map-reduce-reduce.
- **Reduce** — combines per-aggregator partial results into the final answer (e.g., merges three local top-3 heaps of 9 candidates into the global top-3).
- **Top-N** — each Aggregate node maintains a heap of size N for its local data; Reduce merges all heaps into global top-N every minute.
- **Filtering via star schema** — pre-aggregate by filter dimensions (country, etc.) so a query like "ad001 clicks in USA" hits a precomputed bucket. Limitation: dimensions multiply the number of buckets.

## 5. Time, Watermarks, and Windows

| Choice | Pros | Cons |
|---|---|---|
| Event time (client clock) | Accurate (real click moment) | Client clock may be wrong or maliciously set |
| Processing time (server clock) | Reliable | Late events misattributed to the wrong window |

**Recommendation — event time**, since billing accuracy outweighs clock-trust concerns.

**Watermark** — a fixed extension (e.g., +15s, adjustable) appended to each aggregation window so events arriving slightly late still fall into the correct window. Long watermark = better accuracy, more latency; short = the opposite. Watermarks don't fix very late events — those are corrected by **end-of-day reconciliation**.

**Window types used:**

- **Tumbling** — fixed, non-overlapping minute buckets for use case 1.
- **Sliding** — overlapping window slid by an interval for use case 2 (top-N over last `M` minutes).

Hopping and session windows exist but aren't applicable here.

## 6. Delivery Guarantees

**Exactly-once is required.** At-least-once is fine for most apps, but a few percent duplicates here means millions of dollars in billing errors. Yelp's published implementation is cited as a real-world reference.

**Sources of duplicates:**

1. Clients resending the same event (malicious cases handled by separate ad fraud/risk components).
2. Aggregator outage between processing events and committing the upstream Kafka offset, causing the replacement node to reprocess from the old offset.

**Naive offset-in-external-storage doesn't work.** Saving the new offset *before* downstream ack means a crash skips events forever; saving *after* ack means a crash redelivers. The fix — **wrap the offset-update + downstream-send in a distributed transaction** — is covered generically in [Concurrency & Transactions §9](fundamentals/concurrency-and-transactions.md#9-exactly-once-via-offset-transactions). It's intentionally hard and treated as an advanced topic.

## 7. Scaling and Hotspots

Three independently scalable components: message queue, aggregation service, database.

**Queue scaling** — producers scale freely; consumers scale via Kafka consumer-group rebalancing (slow at hundreds of consumers — do it off-peak); use `ad_id` as the partition key so all events for an ad land in one partition; **pre-allocate partitions** because changing partition count remaps `ad_id`s; physically shard topics by geography (`topic_north_america`) or business type (`topic_web_ads`) to raise throughput at the cost of complexity.

**Aggregation service scaling — two options:**

1. Multi-threading by routing different `ad_id`s to different threads.
2. Deploy on a resource manager like **Apache Hadoop YARN** for multi-process scale-out.

Option 2 is more widely used because compute can be added as a resource.

**Database scaling** — Cassandra natively scales horizontally via consistent-hashing virtual nodes; adding a node auto-rebalances vnodes, no manual resharding. See [Sharding & Consistent Hashing](fundamentals/sharding-and-consistent-hashing.md).

**Hotspot** — large advertisers' ads attract more clicks; partitioning by `ad_id` concentrates them. Mitigations: ask a resource manager for extra aggregation nodes when capacity is exceeded, fan out the events to them, write the merged result back to the original aggregator. Advanced: **Global-Local Aggregation** and **Split Distinct Aggregation**.

## 8. Fault Tolerance and Reconciliation

**In-memory aggregation is volatile** — when a node dies, partial counts are lost. Replaying from the start of Kafka is too slow.

**Snapshotting "system status"** — periodically persist not just the upstream offset but also the heaps and partial counts for the current top-N / last-M-minute windows; on failure, a replacement node restores the snapshot and replays only events after it.

**Continuous monitoring** — stamp events at each stage to track latency; watch Kafka **records-lag** (Kafka exposes queue size as lag); monitor CPU/disk/JVM on aggregator nodes — sudden lag spikes signal more aggregators are needed.

**End-of-day reconciliation** — sort raw events by event time per partition and recompute aggregates via batch job, then compare to the streaming result; smaller windows (e.g., 1h) give finer reconciliation. There is no third-party ground truth (unlike banking), so the batch job *is* the reference. Late events mean exact match isn't expected, only a known-bounded discrepancy.

**Alternative architecture** — store raw clicks in **Hive** with **Elasticsearch** for fast queries, run aggregation in an OLAP database like **ClickHouse** or **Druid**. The book favors the generic Kafka + stream-processing approach because interview discussion focuses on trade-offs, not specific vendor internals.

## Sources

- [Vol 2 Ch 6: Aggregate Ad Click Events](software/system-design-interview/books/system-design-interview-vol2/ch06_aggregate_ad_click_events.md)
