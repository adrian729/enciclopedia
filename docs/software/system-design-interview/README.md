# System Design Interview

> A merged synthesis of two complementary books: **System Design Interview Fundamentals** by Alex Liu and **System Design Interview: An Insider's Guide** by Alex Xu. Topics that both books cover are unified into a single page; topics unique to one book are kept and labelled. The original chapter-by-chapter book pages remain available in the **Books** section.

## Table of Contents

- [1. Why a Merged Section](#1-why-a-merged-section)
- [2. How the Two Books Compare](#2-how-the-two-books-compare)
- [3. How to Use This Section](#3-how-to-use-this-section)
- [4. Section Map](#4-section-map)

## 1. Why a Merged Section

The two books overlap heavily on technical fundamentals (consistent hashing, replication, ID generation, caching, rate limiting) and on canonical case studies (chat, news feed, file storage, video streaming). Reading them in parallel forces a reader to keep cross-referencing. This section rewrites the shared material once, calls out where the authors disagree or emphasize differently, and preserves each book's unique contributions in their own pages.

## 2. How the Two Books Compare

| Aspect | Liu (Fundamentals) | Xu (Insider's Guide) |
|---|---|---|
| Interview framework | 6 steps, 40 minutes, math *after* API and schema | 4 steps, 45 minutes, math during high-level design |
| Toolbox depth | 24 small reference chapters with decision trees | 4 deep distributed primitives (rate limiter, consistent hashing, KV store, ID generator) plus a "scale from zero" walkthrough |
| Case studies | 8 (ridesharing, top YouTube, emoji broadcast, Instagram, distributed counter, cloud file, rate limiter, chat) | 8 (URL shortener, web crawler, notifications, news feed, chat, autocomplete, YouTube, Google Drive) |
| Communication coverage | Full chapter on tactics + leveling rubric | A few paragraphs of "do/don't" advice |
| Distinctive emphasis | Long-tail distribution patterns, product-redesign as a senior signal, communication discipline | Composing primitives bottom-up, consistent-hashing-everywhere, Snowflake-everywhere |

Neither book is wrong — they cover the same skill from different angles. Liu trains the candidate to argue; Xu trains the candidate to compose primitives.

## 3. How to Use This Section

- **Preparing for an interview cold:** read the [Process](system-design-interview/process/framework.md) pages first, then [Scaling Evolution](system-design-interview/fundamentals/scaling-evolution.md) for the foundation, then any case study that matches the role's domain.
- **Refreshing on a specific primitive:** jump straight to the relevant [Fundamentals](system-design-interview/fundamentals/scaling-evolution.md) page; each one is self-contained and links back to the originating book chapters.
- **Day-of review:** open the [Cheat Sheet](system-design-interview/cheat-sheet.md) — it consolidates framework steps, math formulas, and decision trees in one page.

Every page ends with a **Sources** section linking to the originating chapters in the books. When the books disagree on emphasis or recommendation, that disagreement is called out inline so the reader can form their own view.

## 4. Section Map

- **Process** — how the interview is structured and evaluated.
  - [Framework](system-design-interview/process/framework.md) — the 4-step and 6-step frameworks side-by-side.
  - [Communication & Evaluation](system-design-interview/process/communication.md) — tactics, leveling rubric, common red flags.
  - [Back-of-the-Envelope Estimation](system-design-interview/process/estimation.md) — formulas, capacity numbers, worked example.
- **Fundamentals** — building blocks composed during deep dives.
  - [Scaling Evolution](system-design-interview/fundamentals/scaling-evolution.md), [Networking & DNS](system-design-interview/fundamentals/networking-and-dns.md), [Databases, Schema, Indexing](system-design-interview/fundamentals/databases-schema-indexing.md), [Caching](system-design-interview/fundamentals/caching.md), [CDN](system-design-interview/fundamentals/cdn.md), [Replication](system-design-interview/fundamentals/replication.md), [Sharding & Consistent Hashing](system-design-interview/fundamentals/sharding-and-consistent-hashing.md), [CAP, Consensus & Conflict Resolution](system-design-interview/fundamentals/cap-consensus-and-conflict-resolution.md), [Concurrency & Transactions](system-design-interview/fundamentals/concurrency-and-transactions.md), [Real-Time Communication](system-design-interview/fundamentals/real-time-communication.md), [Queues & Messaging](system-design-interview/fundamentals/queues-and-messaging.md), [Async, Batch, Stream](system-design-interview/fundamentals/async-batch-stream.md), [ID Generation](system-design-interview/fundamentals/id-generation.md), [API Design & Gateway](system-design-interview/fundamentals/api-design-and-gateway.md), [Service Discovery & Load Balancing](system-design-interview/fundamentals/service-discovery-and-load-balancing.md), [Search](system-design-interview/fundamentals/full-text-search.md), [Resilience Patterns](system-design-interview/fundamentals/resilience-patterns.md), [Observability, Security, Cold Storage](system-design-interview/fundamentals/observability-security-cold-storage.md).
- **Case Studies** — worked product designs.
  - [Rate Limiter](system-design-interview/case-studies/rate-limiter.md), [URL Shortener](system-design-interview/case-studies/url-shortener.md), [Key-Value Store](system-design-interview/case-studies/key-value-store.md), [Web Crawler](system-design-interview/case-studies/web-crawler.md), [Notification System](system-design-interview/case-studies/notification-system.md), [News Feed](system-design-interview/case-studies/news-feed.md), [Chat System](system-design-interview/case-studies/chat-system.md), [Search Autocomplete](system-design-interview/case-studies/search-autocomplete.md), [YouTube](system-design-interview/case-studies/youtube.md), [Cloud File Storage](system-design-interview/case-studies/cloud-file-storage.md), [Ridesharing](system-design-interview/case-studies/ridesharing.md), [Distributed Counter](system-design-interview/case-studies/distributed-counter.md), [Emoji Broadcasting](system-design-interview/case-studies/emoji-broadcasting.md).
- [**Cheat Sheet**](system-design-interview/cheat-sheet.md) — single-page reference.

## Sources

- [System Design Interview Fundamentals — Book Summary](software/system-design-interview/books/system-design-interview-fundamentals/book_summary.md) (Alex Liu)
- [System Design Interview: An Insider's Guide — Book Summary](software/system-design-interview/books/system-design-interview-insiders-guide/book_summary.md) (Alex Xu)
