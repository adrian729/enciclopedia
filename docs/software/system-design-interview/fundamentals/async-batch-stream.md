# Async, Batch, Stream Processing

> Liu's Ch 5.09 covers the async / batch / stream / lambda spectrum end-to-end. Xu doesn't have a dedicated chapter but uses these patterns inside transcoding (DAG, stage queues), search autocomplete (weekly trie rebuild), and YouTube top-views (real-time aggregation).

## Table of Contents

- [1. Asynchronous Processing](#1-asynchronous-processing)
- [2. Batch Processing](#2-batch-processing)
- [3. Stream Processing](#3-stream-processing)
  - [3.1. Event Time vs Processing Time](#31-event-time-vs-processing-time)
  - [3.2. Watermarks](#32-watermarks)
  - [3.3. Checkpointing](#33-checkpointing)
  - [3.4. Micro-Batching](#34-micro-batching)
- [4. Lambda Architecture](#4-lambda-architecture)
- [5. Choosing Between Them](#5-choosing-between-them)
- [Sources](#sources)

## 1. Asynchronous Processing

Asynchronous processing unblocks the caller by offloading work to a background process. The subtle question is **"sync up to where?"**

Liu's e-commerce checkout example: scoping synchronicity to step 1 returns "we're processing your order" immediately and runs payment async; scoping to step 2 confirms payment before returning, giving faster feedback if the card is rejected. Both are valid — the right choice depends on what the user needs to know synchronously.

## 2. Batch Processing

Periodically grab a data source, apply logic, produce output. MapReduce is one common implementation, but interview prompts can use any batch framework.

Liu's checklist of batch failure modes to surface proactively:

- **SLO violations** if the batch runs late.
- **Missed output** if it never runs.
- **Idempotency** if it runs more than once (re-running shouldn't double-count).
- **Stuck jobs** holding resources without progress.
- **Resource contention** between concurrent batches.
- **Overlapping logical runs** — a 6-hour batch scheduled hourly will overlap with itself.

## 3. Stream Processing

Unbounded data, fresher output, higher complexity. The defining concepts:

### 3.1. Event Time vs Processing Time

**Event time** is when the event occurred at the source (a sensor reading, a user click). **Processing time** is when the system processed it. The two diverge under network delay, retries, and out-of-order arrival. Most aggregations want event time, but the system can only see processing time directly.

### 3.2. Watermarks

A watermark is a heuristic answer to "have I received enough data for this window to move on?" A bigger watermark holds more memory and drops fewer late events; a smaller one closes windows faster but loses late arrivals. Tuning the watermark is the freshness-vs-completeness lever.

### 3.3. Checkpointing

Persists intermediate state so a failed host doesn't replay from the beginning. Without checkpointing, every node failure requires reprocessing the whole stream from the source. With it, a node restarts from its last checkpoint — minutes of work lost instead of hours.

### 3.4. Micro-Batching

Amortizes per-event I/O overhead at the cost of delay. Spark Streaming uses ~1-second micro-batches; Flink can run truly per-event. The sweet spot depends on the freshness target.

## 4. Lambda Architecture

Run *both* a fast lane (stream, low-latency, approximate) and a slow lane (batch, high-latency, accurate). Reads merge the two. Used when neither pure lane is sufficient — the canonical case is a counter that needs to be live but also exactly correct over a long horizon.

The trade-off: you operate two pipelines, with two failure modes, and reconciliation logic between them.

## 5. Choosing Between Them

Liu's recommendation matrix:

| Picks | When |
|---|---|
| Async (in-request) | Single-user latency reduction; the work is small and the user gets a response. |
| Batch | Data is enormous; processing is compute-intensive; freshness target is hours-to-days; use case doesn't need freshness (daily payroll, weekly trie rebuild for search autocomplete). |
| Stream | Freshness target is seconds-to-minutes; the user-visible value depends on it (real-time dashboards, fraud detection, live counts). |
| Lambda | Both are needed: live-ish updates plus accurate eventual reconciliation. The interview prompt usually introduces this when a hypothetical breaks a pure-stream design. |

Batch beats stream when streaming complexity outweighs the freshness benefit. Lambda beats both when neither lane alone meets the requirement.

## Sources

- [Liu Ch 5.09: Async, Batch, Stream, Lambda](software/system-design-interview/books/system-design-interview-fundamentals/ch05_09_async_batch_stream_lambda.md)
- [Xu Ch 13: Design a Search Autocomplete System](software/system-design-interview/books/system-design-interview-insiders-guide/ch13_design_a_search_autocomplete.md) (weekly batch trie rebuild)
- [Xu Ch 14: Design YouTube](software/system-design-interview/books/system-design-interview-insiders-guide/ch14_design_youtube.md) (transcoding DAG with staged queues)
