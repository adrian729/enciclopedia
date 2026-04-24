# Ch 6.02: Top Watched YouTube Video

## Table of Contents

- [1. Requirements](#1-requirements)
- [2. API](#2-api)
- [3. High-Level Design](#3-high-level-design)
- [4. Schema](#4-schema)
- [5. End-to-End Flow](#5-end-to-end-flow)
- [6. Deep Dives](#6-deep-dives)

## 1. Requirements

- **Prompt** — design a system to calculate the top YouTube videos
- **Scope narrowed to**: a single global top list, ranking based on the video itself (not metadata/categories); purpose is content discovery on the web/mobile client
- **UI** — a "Top Video" tab with sub-tabs for time windows: **daily**, **last hour**, **real-time**
- **Ranking algorithm** — greatest watch count within the time window wins
- **Assumptions** agreed with interviewer:
  - **50M DAU** worldwide
  - **10B unique videos**; watch volume follows a **long-tail distribution** (a subset of videos is the majority of traffic)
  - **Accuracy and freshness both matter**, but trade-offs are permitted
  - Low query latency on read; data durable for future reads
  - Event source is the live watch event (not a pre-generated log)

## 2. API

```
watch_video(user_id, video_id) → status
get_top_videos(k, start_time, end_time) → [video_info]
```

- No dedup on page refresh for `watch_video`
- `k ≤ 100`; time at **minute granularity**
- `video_info` = `video_id` + metadata to display

## 3. High-Level Design

- **YouTube service** receives `watch_video` and emits to an **event queue** (asynchronous pipeline; raw-event storage would be data-intensive and slow on read)
- **Aggregator service** pulls events from the queue and **rolls up** into minute segments
- **Metrics storage** holds the materialized rollup
- **Metrics service** is a thin read layer over metrics storage for `get_top_videos`

## 4. Schema

**Event queue**

| Video Id | Timestamp |
|---|---|

- Client vs. server-generated timestamp is a deep-dive topic

**Metrics storage (minute table)** — rolled up to minute granularity by `video_id`

| Minute | Video ID | Count |
|---|---|---|

- Top-K read on a minute requires fetching all records for that minute and sorting (expensive; deep-dive topic)

## 5. End-to-End Flow

- **`watch_video`**: user → YouTube service → event queue → aggregator → metrics storage (materialized rollup)
- **`get_top_videos`**: client → metrics service → metrics storage

## 6. Deep Dives

### 6.1 Client vs. Server Timestamp

| Option | Upside | Downside |
|---|---|---|
| **Client-generated** | Accurate event time; captures offline | Clock skew; malicious timestamps |
| **Server-generated** | Clock consistency across events | Network delay / offline loses accuracy |

- **Conclusion** — **server-generated**. Offline is out of scope and the pipeline isn't expected to be backlogged. To further improve, capture client event time, client sent time, and server receive time; use (client sent − server receive) to estimate clock skew and adjust. Monitor outlier timestamps for malicious clients

### 6.2 Aggregation Service Data Structure

- Aggregator fetches a batch of events and rolls them up into an in-memory minute segment (`Minute | Video ID | Count`). Top-K must be extracted before flushing

| Option | Complexity | Notes |
|---|---|---|
| **Sort the list** | N log N | Simple |
| **Min-heap of size K** | K log K | K ≪ N |

- **Conclusion** — **min-heap of size K**

### 6.3 Aggregation Service Scaling

- **Math**: 100M unique videos/min × 30 bytes × 20-min buffer = **6 × 10¹⁰ bytes ≈ 60 GB** in memory; fits on a modern machine. Interviewer then constrains to a **16 GB** machine with more than 100M unique videos
- **Options** (doesn't fit in memory):

| Option | Upside | Downside |
|---|---|---|
| **Shard by `video_id`** (consistent hashing) + merge K sorted lists on flush | Mutually exclusive counts per shard; clean merge | Cluster coordination for window flushing; added latency; **long-tail → hotspots** |
| **Random insert** into aggregators, coordinator merges | Even distribution, no hotspots | Scatter-gather per `video_id` lookup |
| **Probabilistic data structure (Count-Min Sketch)** | Less space | Approximate counts; still need min-heap over videos for top-K |
| **Batch pipeline to catch up (lambda architecture)** | Slow but accurate correction path | Complexity of maintaining two similar systems |

- **Conclusion** — **random insert (option 2)** trades some accuracy for speed. Consider **option 3** if an eventually accurate result is required

> **Warning** — Advanced data structures like Count-Min Sketch aren't required; mentioning them is a plus *only if you know the internals*. Read the room: don't spend 5 minutes explaining them. A dismissal like "Count-Min Sketch reduces space at the expense of accuracy; for strong accuracy with memory constraints we need sharding" is acceptable.

### 6.4 Metrics Storage: Hour and Day Aggregation

- Storing only top-K per minute **breaks** for hourly/daily rollups: the hour/day winner's count may not appear in every minute's top-K
- **Options**:

| Option | Upside | Downside |
|---|---|---|
| **Aggregate 60 min-intervals anyway** | Simple; data already available | Inaccurate — minute intervals lack full count list |
| **Store K + buffer** (e.g., K=100, buffer=500 → top 600/min) | Less lossy | More data; still lossy over long horizons |
| **Also process hour-interval in streaming** (Count-Min Sketch for memory) | Accurate hourly data persisted | Memory pressure; more complex |
| **Hourly batch job** | Accurate | Batch jobs less reliable to finish on time with high volume |

- **Conclusion** — **option 3** for best-effort accuracy with timely results; keep **option 4** as an override if strict accuracy matters

### 6.5 Aggregation Service Failures

- Aggregator going down loses in-memory aggregations → rebuild via **periodic checkpointing** and replay from the durable queue's offset
- **Options**:

| Option | Upside | Downside |
|---|---|---|
| **Checkpoint on local disk** | Fast checkpoint and recovery | Correlated instance failure loses disk + memory; disk capacity concerns |
| **Checkpoint on distributed store** | Scales; survives correlated failure | Network overhead slows checkpoint and recovery |
| **Both: frequent local + less frequent distributed** | Fast recovery in-process; distributed backup for correlated failure | Asynchronous backup risks data loss; delay between backups |

- **Conclusion** — **option 3**, accepting some backup-delay data loss. Tune checkpoint frequency: more frequent = faster recovery, slower processing

### 6.6 Late Events: Watermark Length

| Option | Upside | Downside |
|---|---|---|
| **Longer watermark delay** | Better accuracy | Holds more data in stream processing |
| **Shorter watermark delay** | Faster finalization; less memory | Late events must be handled separately |

- **Conclusion** — **shorter watermark**; accuracy has leeway, and server-generated timestamps + reliable internal network mean few late events

### 6.7 Post-Watermark Processing

| Option | Upside | Downside |
|---|---|---|
| **Discard late events** | Simple | Lossy |
| **Queue for modification pipeline** | No data loss | Complexity of a second pipeline |

- **Conclusion** — **discard**. Accuracy has leeway, and the slow batch path (lambda) will eventually reconcile — no need for a dedicated modification pipeline
