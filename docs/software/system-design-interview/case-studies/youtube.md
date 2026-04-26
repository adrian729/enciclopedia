# YouTube / Video Streaming

> Both books cover YouTube but from different angles. Xu's Ch 14 is the full-stack design (transcoding DAG, GOP chunking, CDN economics). Liu's Ch 6.02 narrows in on **Top YouTube Video** — real-time view counting under bursty load. The two designs are complementary; this page covers both.

## Table of Contents

- [1. Two Different Prompts](#1-two-different-prompts)
- [2. Xu — Full-Stack YouTube](#2-xu--full-stack-youtube)
  - [2.1. Video Transcoding](#21-video-transcoding)
  - [2.2. The DAG Programming Model](#22-the-dag-programming-model)
  - [2.3. Architecture](#23-architecture)
  - [2.4. Speed Optimizations](#24-speed-optimizations)
  - [2.5. Safety](#25-safety)
  - [2.6. Cost Optimizations](#26-cost-optimizations)
- [3. Liu — Top YouTube Video](#3-liu--top-youtube-video)
  - [3.1. The Constraint — Freshness Under Burst](#31-the-constraint--freshness-under-burst)
  - [3.2. The Pattern](#32-the-pattern)
- [4. Trade-offs](#4-trade-offs)
- [Sources](#sources)

## 1. Two Different Prompts

The two books frame YouTube differently:

- **Xu** — design the whole product. Upload, transcode, store, stream, recommend. The interesting deep dive is video transcoding.
- **Liu** — design "show the top-watched video right now." A narrow real-time aggregation problem. The interesting deep dive is high-throughput counting.

Both are valid interview prompts. The skills they exercise are different — Xu's is system composition; Liu's is bursty-load aggregation.

## 2. Xu — Full-Stack YouTube

### 2.1. Video Transcoding

Raw video is enormous, and users have heterogeneous devices and network conditions. Transcoding produces multiple resolutions and codecs from one source upload.

A **container** holds video, audio, and metadata. **Codecs** (H.264, VP9, HEVC) compress the video stream. The output is a ladder: 240p, 480p, 720p, 1080p, 4K — each at multiple bitrates for [adaptive bit rate](fundamentals/observability-security-cold-storage.md) streaming.

### 2.2. The DAG Programming Model

Transcoding tasks form a **directed acyclic graph**: inspection → encoding to multiple resolutions → thumbnail generation → watermarking. Stages run sequentially or in parallel; the DAG scheduler dispatches tasks as their dependencies complete.

### 2.3. Architecture

Six components:

| Component | Role |
|---|---|
| Preprocessor | Splits video into Group of Pictures (GOP) chunks; builds the DAG; caches data for retries |
| DAG Scheduler | Dispatches stages as dependencies complete |
| Resource Manager | Holds task queue, worker queue, running queue |
| Task Workers | Execute encoding, thumbnailing, watermarking |
| Temporary Storage | In-memory cache for metadata; BLOB storage (S3) for video/audio |
| Encoded Output | Final transcoded video, ready for streaming |

### 2.4. Speed Optimizations

- **GOP chunking** lets the upload happen in parallel — chunks upload concurrently rather than the whole file in one stream.
- **Global upload centers** route the upload to the nearest origin.
- **Message-queue decoupling** between modules so a slow stage doesn't block faster ones.

### 2.5. Safety

- **Pre-signed upload URLs** (S3 term; "Shared Access Signature" in Azure) — the user uploads directly to storage without the bytes flowing through the application servers.
- **DRM** for license enforcement.
- **AES encryption** for stored content.
- **Visual watermarking** for piracy attribution.

### 2.6. Cost Optimizations

YouTube's viewing pattern is **long-tail** — a small number of videos get most of the traffic; the long tail of unpopular videos is enormous.

- **CDN for popular videos**, in-house storage for unpopular videos. CDN egress is expensive at scale (~$150K/day at AWS CloudFront pricing for a YouTube-scale catalog); serving the long tail from cheaper in-house storage saves substantially.
- **Reduced encoding count for short-tail content** — popular videos get the full ladder of resolutions and codecs; unpopular ones get a minimal set.
- **Regional CDNs** — push popular videos to regional edges based on viewing pattern.
- **Cold storage** for very old or rarely-watched content (see [Observability, Security, Cold Storage](fundamentals/observability-security-cold-storage.md)).

## 3. Liu — Top YouTube Video

### 3.1. The Constraint — Freshness Under Burst

The problem: at any moment, what's the most-watched video globally? The constraint is **freshness** — the answer should reflect views from seconds ago, not minutes.

Bursty load: a viral video can spike to 10× normal QPS in seconds. A single video can get 99% of all views (the long-tail again, in the inverse: a celebrity video is the head).

### 3.2. The Pattern

Same shape recurs in many bursty-aggregation problems:

```
Views (high QPS)
   ↓
Queue absorbs the spike
   ↓
Aggregator processes micro-batches (seconds-long windows)
   ↓
Cache-like layer (in-memory min-heap of size K — the top K videos)
   ↓
Durable store
```

Key moves:

- **Queue absorbs the spike** so the aggregator's pace isn't pinned to the producer's pace.
- **Micro-batching** amortizes per-event cost. See [Async, Batch, Stream](fundamentals/async-batch-stream.md).
- **Min-heap of size K** makes "top K" lookup O(1) — every new view either evicts the current minimum or doesn't make the cut.
- **Durable store** is reached only after the cache layer; the durable store doesn't see every event.

This pattern recurs in [Distributed Counter](case-studies/distributed-counter.md), [Emoji Broadcasting](case-studies/emoji-broadcasting.md), and [Rate Limiter](case-studies/rate-limiter.md). The lesson: a queue plus an aggregator plus a cache absorbs almost any bursty-write workload.

## 4. Trade-offs

- **Transcoding cost vs storage cost.** Producing every resolution and bitrate up front uses CPU and bandwidth. On-demand transcoding saves cost for unpopular content at the price of first-view latency.
- **CDN cost vs in-house cost.** CDN gives the lowest latency; in-house storage is cheaper. The split follows the long-tail viewing distribution.
- **GOP chunk size.** Bigger chunks reduce overhead; smaller chunks parallelize better. ~6-second GOPs are typical.
- **Live counting accuracy vs cost.** The min-heap top-K is approximate during the micro-batch window; exact reconciliation happens in batch.

## Sources

- [Xu Ch 14: Design YouTube](software/system-design-interview/books/system-design-interview-insiders-guide/ch14_design_youtube.md)
- [Liu Ch 6.02: Top Watched YouTube Video](software/system-design-interview/books/system-design-interview-fundamentals/ch06_02_top_youtube_video.md)
