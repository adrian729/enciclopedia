# System Design Interview

> A merged synthesis of three complementary books: **System Design Interview Fundamentals** by Alex Liu, **System Design Interview: An Insider's Guide (Vol 1)** by Alex Xu, and **System Design Interview: An Insider's Guide Vol 2** by Alex Xu and Sahn Lam. Topics that multiple books cover are unified into a single page; topics unique to one book are kept and labelled. The original chapter-by-chapter book pages remain available in the **Books** section.

## Table of Contents

- [1. Why a Merged Section](#1-why-a-merged-section)
- [2. How the Two Books Compare](#2-how-the-two-books-compare)
- [3. How to Use This Section](#3-how-to-use-this-section)
- [4. Section Map](#4-section-map)

## 1. Why a Merged Section

The three books overlap heavily on technical fundamentals (consistent hashing, replication, ID generation, caching, rate limiting) and on canonical case studies (chat, news feed, file storage, video streaming, distributed message queue). Reading them in parallel forces a reader to keep cross-referencing. This section rewrites the shared material once, calls out where the authors disagree or emphasize differently, and preserves each book's unique contributions in their own pages.

## 2. How the Three Books Compare

| Aspect | Liu (Fundamentals) | Xu Vol 1 (Insider's Guide) | Xu Vol 2 (Insider's Guide Vol 2) |
|---|---|---|---|
| Interview framework | 6 steps, 40 minutes, math *after* API and schema | 4 steps, 45 minutes, math during high-level design | Same 4-step framework as Vol 1 |
| Toolbox depth | 24 small reference chapters with decision trees | 4 deep distributed primitives (rate limiter, consistent hashing, KV store, ID generator) plus a "scale from zero" walkthrough | 13 end-to-end designs that surface a recurring-primitives table (geohash, hash ring, append-only log, idempotency keys, event sourcing, double-entry ledger) |
| Case studies | 8 (ridesharing, top YouTube, emoji broadcast, Instagram, distributed counter, cloud file, rate limiter, chat) | 8 (URL shortener, web crawler, notifications, news feed, chat, autocomplete, YouTube, Google Drive) | 13 (proximity, nearby friends, Google Maps, distributed message queue, metrics monitoring, ad-click aggregation, hotel reservation, distributed email, S3-like object storage, gaming leaderboard, payment, digital wallet, stock exchange) |
| Communication coverage | Full chapter on tactics + leveling rubric | A few paragraphs of "do/don't" advice | Brief — Vol 2 leans on Vol 1's framework |
| Distinctive emphasis | Long-tail distribution patterns, product-redesign as a senior signal, communication discipline | Composing primitives bottom-up, consistent-hashing-everywhere, Snowflake-everywhere | Primitive-to-workload mapping; the same handful of primitives (geohash, hash ring, append-only WAL, idempotency keys, event sourcing) reappear across thirteen domains |

No book is wrong — they cover the same skill from different angles. Liu trains the candidate to argue; Vol 1 trains primitive depth on a few canonical primitives (rate limiter, KV store, ID gen); Vol 2 trains primitive *application* across thirteen end-to-end designs.

## 3. How to Use This Section

- **Preparing for an interview cold:** read the [Process](system-design-interview/process/framework.md) pages first, then [Scaling Evolution](system-design-interview/fundamentals/scaling-evolution.md) for the foundation, then any case study that matches the role's domain.
- **Refreshing on a specific primitive:** jump straight to the relevant [Fundamentals](system-design-interview/fundamentals/scaling-evolution.md) page; each one is self-contained and links back to the originating book chapters.
- **Day-of review:** open the [Cheat Sheet](system-design-interview/cheat-sheet.md) — it consolidates framework steps, math formulas, and decision trees in one page.

**Routing convention:** the merged section (`fundamentals/`, `case-studies/`, `process/`) is the canonical interview-prep reading path. The per-chapter pages under `books/` are reference originals — consult them when you want the author's exact phrasing or the full chapter context, but the merged pages are the ones to read first.

Every page ends with a **Sources** section linking to the originating chapters in the books. When the books disagree on emphasis or recommendation, that disagreement is called out inline so the reader can form their own view.

## 4. Section Map

- **Process** — how the interview is structured and evaluated.
  - [Framework](system-design-interview/process/framework.md) — the 4-step and 6-step frameworks side-by-side.
  - [Communication & Evaluation](system-design-interview/process/communication.md) — tactics, leveling rubric, common red flags.
  - [Back-of-the-Envelope Estimation](system-design-interview/process/estimation.md) — formulas, capacity numbers, worked example.
- **Fundamentals** — building blocks composed during deep dives.
  - [Scaling Evolution](system-design-interview/fundamentals/scaling-evolution.md), [Networking & DNS](system-design-interview/fundamentals/networking-and-dns.md), [Databases, Schema, Indexing](system-design-interview/fundamentals/databases-schema-indexing.md), [Caching](system-design-interview/fundamentals/caching.md), [CDN](system-design-interview/fundamentals/cdn.md), [Replication](system-design-interview/fundamentals/replication.md), [Sharding & Consistent Hashing](system-design-interview/fundamentals/sharding-and-consistent-hashing.md), [Geospatial Indexing](system-design-interview/fundamentals/geospatial-indexing.md), [CAP, Consensus & Conflict Resolution](system-design-interview/fundamentals/cap-consensus-and-conflict-resolution.md), [Concurrency & Transactions](system-design-interview/fundamentals/concurrency-and-transactions.md), [Real-Time Communication](system-design-interview/fundamentals/real-time-communication.md), [Queues & Messaging](system-design-interview/fundamentals/queues-and-messaging.md), [Async, Batch, Stream](system-design-interview/fundamentals/async-batch-stream.md), [ID Generation](system-design-interview/fundamentals/id-generation.md), [API Design & Gateway](system-design-interview/fundamentals/api-design-and-gateway.md), [Service Discovery & Load Balancing](system-design-interview/fundamentals/service-discovery-and-load-balancing.md), [Search](system-design-interview/fundamentals/full-text-search.md), [Resilience Patterns](system-design-interview/fundamentals/resilience-patterns.md), [Observability, Security, Cold Storage](system-design-interview/fundamentals/observability-security-cold-storage.md).
- **Case Studies** — worked product designs, grouped by domain.
  - **Spatial & Mapping** — [Proximity Service](system-design-interview/case-studies/proximity-service.md), [Nearby Friends](system-design-interview/case-studies/nearby-friends.md), [Google Maps](system-design-interview/case-studies/google-maps.md), [Ridesharing](system-design-interview/case-studies/ridesharing.md).
  - **Storage & Retrieval** — [URL Shortener](system-design-interview/case-studies/url-shortener.md), [Key-Value Store](system-design-interview/case-studies/key-value-store.md), [Cloud File Storage](system-design-interview/case-studies/cloud-file-storage.md), [Object Storage (S3-like)](system-design-interview/case-studies/object-storage.md), [YouTube](system-design-interview/case-studies/youtube.md).
  - **Messaging & Real-Time** — [Distributed Message Queue](system-design-interview/case-studies/distributed-message-queue.md), [Notification System](system-design-interview/case-studies/notification-system.md), [News Feed](system-design-interview/case-studies/news-feed.md), [Chat System](system-design-interview/case-studies/chat-system.md), [Emoji Broadcasting](system-design-interview/case-studies/emoji-broadcasting.md), [Distributed Email](system-design-interview/case-studies/distributed-email.md).
  - **Search & Crawling** — [Web Crawler](system-design-interview/case-studies/web-crawler.md), [Search Autocomplete](system-design-interview/case-studies/search-autocomplete.md).
  - **Analytics & Monitoring** — [Metrics Monitoring](system-design-interview/case-studies/metrics-monitoring.md), [Ad-Click Aggregation](system-design-interview/case-studies/ad-click-aggregation.md), [Distributed Counter](system-design-interview/case-studies/distributed-counter.md).
  - **Transactions & Financial** — [Hotel Reservation](system-design-interview/case-studies/hotel-reservation.md), [Payment System](system-design-interview/case-studies/payment-system.md), [Digital Wallet](system-design-interview/case-studies/digital-wallet.md), [Stock Exchange](system-design-interview/case-studies/stock-exchange.md).
  - **Real-Time Ranking & Throttling** — [Rate Limiter](system-design-interview/case-studies/rate-limiter.md), [Gaming Leaderboard](system-design-interview/case-studies/gaming-leaderboard.md).
- [**Cheat Sheet**](system-design-interview/cheat-sheet.md) — single-page reference.

## Sources

- [System Design Interview Fundamentals — Book Summary](software/system-design-interview/books/system-design-interview-fundamentals/book_summary.md) (Alex Liu)
- [System Design Interview: An Insider's Guide — Book Summary](software/system-design-interview/books/system-design-interview-insiders-guide/book_summary.md) (Alex Xu)
- [System Design Interview: An Insider's Guide Vol 2 — Book Summary](software/system-design-interview/books/system-design-interview-vol2/book_summary.md) (Alex Xu and Sahn Lam)
