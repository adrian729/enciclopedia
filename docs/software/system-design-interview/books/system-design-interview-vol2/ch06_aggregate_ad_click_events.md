# Ch 6: Aggregate Ad Click Events

## Table of Contents

- [1. Problem and Scope](#1-problem-and-scope)
- [2. Data Model and APIs](#2-data-model-and-apis)
- [3. High-Level Architecture](#3-high-level-architecture)
- [4. Aggregation Service (MapReduce DAG)](#4-aggregation-service-mapreduce-dag)
- [5. Time, Watermarks, and Windows](#5-time-watermarks-and-windows)
- [6. Delivery Guarantees and Deduplication](#6-delivery-guarantees-and-deduplication)
- [7. Scaling and Hotspots](#7-scaling-and-hotspots)
- [8. Fault Tolerance and Correctness](#8-fault-tolerance-and-correctness)

## 1. Problem and Scope

- **Ad click event aggregation** — system that ingests raw click logs and produces per-minute counts to drive Real-Time Bidding (RTB) feedback, billing, and dashboards (CTR, CVR); errors translate directly into millions of dollars of advertiser charges.
- **Input event** — log line per click with `ad_id, click_timestamp, user_id, ip, country`, appended to log files on many servers.
- **Three required queries** — count clicks of an `ad_id` in the last `M` minutes; top 100 most clicked ads in the past 1 minute (configurable); both filterable by `ip`, `user_id`, or `country`.
- **Edge cases called out** — late events, duplicate events, partial system failures.
- **Latency target** — end-to-end of a few minutes (unlike RTB itself, which is sub-second). Workload is **billing-grade**, so correctness beats latency.
- **Scale** — 1B DAU, 1 click/user/day → ~10,000 QPS average, 50,000 QPS peak; 0.1 KB per event → 100 GB/day, ~3 TB/month; 2M total ads; volume grows 30% YoY (doubling every 3 years).

## 2. Data Model and APIs

- **Two query APIs cover all three use cases** — `GET /v1/ads/{:ad_id}/aggregated_count` (params `from`, `to`, `filter`) and `GET /v1/ads/popular_ads` (params `count`, `window`, `filter`); filtering is just a query parameter.
- **Raw vs aggregated — store both** — raw is the immutable source of truth for replay and debugging (movable to cold storage); aggregated is the active, query-optimized layer. Querying raw directly is too slow at this scale; relying only on aggregates loses information after a bug.
- **Aggregated row shape** — `(ad_id, click_minute, count)`; with filters, an extra `filter_id` column splits a minute into one row per active filter (e.g., country=US).
- **Top-N table** — separate `most_clicked_ads(window_size, update_time_minute, most_clicked_ads[])` precomputed every minute.
- **Database choice — NoSQL time-series** — workload is write-heavy (10–50K QPS). Cassandra (or InfluxDB) is recommended for both raw and aggregated stores because they are tuned for writes and time-range queries; alternative is columnar files (ORC/Parquet/AVRO) on S3 with size-capped rotation. Aggregated data is read-heavy too (every ad polled every minute → 2M reads/min), so the same database type serves both.

## 3. High-Level Architecture

- **Asynchronous pipeline with two Kafka queues** — log watcher → **Queue 1** (raw click events) → aggregation service → **Queue 2** (per-minute aggregates and top-N) → database writer → DB. Decoupling protects consumers from producer spikes and lets each stage scale independently.
- **Why two queues, not direct DB writes** — the second queue is required to achieve **end-to-end exactly-once (atomic commit) semantics** between aggregation output and storage.
- **Lambda vs Kappa** — lambda runs separate batch and streaming paths (two codebases to maintain); **Kappa** uses one stream-processing engine for both real-time and reprocessing. The design adopts **Kappa**: historical replay reuses the same aggregation service, just pointed at raw data.
- **Data recalculation flow** — recalculation service pulls raw data in batch → routes through a **dedicated** aggregation service (so live traffic isn't impacted) → second queue → DB. Triggered when a bug requires recomputing aggregates from a known point.

## 4. Aggregation Service (MapReduce DAG)

- **DAG model** — break the pipeline into Map/Aggregate/Reduce nodes; each node does one task and forwards results downstream via TCP (cross-process) or shared memory (cross-thread).
- **Map node** — reads, cleans/normalizes, and routes events (e.g., `ad_id % 2` to two downstream nodes). Needed even with Kafka partitioning because the producer may not control partition placement and same-`ad_id` events can land on different partitions.
- **Aggregate node** — counts events by `ad_id` in memory each minute. In MapReduce terms it's part of Reduce, so the pipeline is really map-reduce-reduce.
- **Reduce node** — combines per-aggregator partial results into the final answer (e.g., merges three local top-3 heaps of 9 candidates into the global top-3).
- **Use case 2 — top-N** — each Aggregate node maintains a heap of size N for its local data; Reduce merges all heaps into the global top-N every minute.
- **Use case 3 — filtering via star schema** — pre-aggregate by filter dimensions (country, etc.) so a query like "ad001 clicks in USA" hits a precomputed bucket. Limitation: dimensions multiply the number of buckets.

## 5. Time, Watermarks, and Windows

- **Event time vs processing time** — event time = when the click happened (client clock); processing time = when the aggregator handled it (server clock). Network/queue delays can put them hours apart (a 5-hour late event is shown as an example).

| Choice | Pros | Cons |
|---|---|---|
| Event time | More accurate (client knows the real click moment) | Client clock may be wrong or maliciously set |
| Processing time | Reliable server timestamp | Late events are misattributed to the wrong window |

- **Recommendation — event time**, since billing accuracy outweighs clock-trust concerns.
- **Watermark** — a fixed extension (e.g., +15s, adjustable) appended to each aggregation window so events arriving slightly late still fall into the correct window. Long watermark = better accuracy, more latency; short = the opposite. Watermarks don't fix very late events — those are corrected by **end-of-day reconciliation**.
- **Window types used** — **tumbling** (fixed, non-overlapping minute buckets) for use case 1; **sliding** (overlapping window slid by an interval) for use case 2 (top-N over the last `M` minutes). Hopping and session windows exist but aren't applicable here.

## 6. Delivery Guarantees and Deduplication

- **Exactly-once required** — at-least-once is fine for most apps, but a few percent duplicates here means millions of dollars in billing errors. Yelp's published implementation is cited as a real-world reference.
- **Sources of duplicates** — (1) clients resending the same event (malicious cases handled by separate ad fraud/risk components); (2) aggregator outage between processing events and committing the upstream Kafka offset, causing the replacement node to reprocess from the old offset.
- **Naive offset-in-external-storage fix is insufficient** — if the aggregator stores the new offset in HDFS/S3 *before* downstream ack, a crash after step 3.2 means events 100–110 are skipped forever. Saving the offset *after* downstream ack is also insufficient because a crash before that save causes redelivery.
- **Solution — wrap the offset-update + downstream-send in a distributed transaction**; rollback on partial failure. Achieving exactly-once is intentionally hard and is treated as an advanced topic; reference [9] is suggested for deeper reading.

## 7. Scaling and Hotspots

- **Three independently scalable components** — message queue, aggregation service, database.
- **Queue scaling** — producers scale freely; consumers scale via Kafka consumer-group rebalancing (slow at hundreds of consumers — do it off-peak); use `ad_id` as the partition key so all events for an ad land in one partition; **pre-allocate partitions** because changing partition count remaps `ad_id`s; physically shard topics by geography (`topic_north_america`) or business type (`topic_web_ads`) to raise throughput at the cost of complexity.
- **Aggregation service scaling — two options** — (1) multi-threading by routing different `ad_id`s to different threads; (2) deploy on a resource manager like **Apache Hadoop YARN** for multi-process scale-out. Option 2 is more widely used because compute can be added as a resource.
- **Database scaling** — Cassandra natively scales horizontally via consistent-hashing virtual nodes; adding a node auto-rebalances vnodes, no manual resharding.
- **Hotspot** — a shard or aggregator getting disproportionate load (large advertisers' ads attract more clicks, and partitioning by `ad_id` concentrates them). Mitigation: ask a resource manager for extra aggregation nodes when capacity is exceeded, fan out the events to them, and write the merged result back to the original aggregator. More advanced techniques: **Global-Local Aggregation** and **Split Distinct Aggregation**.

## 8. Fault Tolerance and Correctness

- **In-memory aggregation is volatile** — when a node dies, the partial counts are lost. Replaying from the start of Kafka is too slow.
- **Snapshotting "system status"** — periodically persist not just the upstream offset but also the heaps and partial counts for the current top-N/last-M-minute windows; on failure, a replacement node restores the snapshot and replays only the events after it.
- **Continuous monitoring** — track latency by stamping events at each stage; watch Kafka **records-lag** (Kafka is a distributed commit log, so queue size is exposed as lag); monitor CPU/disk/JVM on aggregator nodes — sudden lag spikes signal that more aggregators are needed.
- **Reconciliation** — at end of day, sort raw events by event time per partition and recompute aggregates via batch job, then compare to the streaming result; smaller windows (e.g., 1h) give finer reconciliation. There is no third-party ground truth (unlike banking), so the batch job *is* the reference. Late events mean exact match isn't expected, only a known-bounded discrepancy.
- **Alternative architecture** — store raw clicks in **Hive** with an **Elasticsearch** layer for fast queries, and run aggregation in an OLAP database such as **ClickHouse** or **Druid**. The book's main design favors the generic Kafka + stream-processing approach because interview discussion focuses on trade-offs, not specific vendor internals.
