# Caching

> Liu's chapter is the deeper reference (write strategies, invalidation philosophy, eviction trade-offs, thundering herd). Xu introduces caching in his scaling-evolution narrative and revisits it for multi-layer caching in News Feed. Both agree caching without justification is an anti-pattern.

## Table of Contents

- [1. Why Cache](#1-why-cache)
- [2. Cache Hit Rate](#2-cache-hit-rate)
- [3. Read Patterns](#3-read-patterns)
- [4. Write Strategies](#4-write-strategies)
- [5. Invalidation](#5-invalidation)
- [6. Eviction Policies](#6-eviction-policies)
- [7. Failure Modes](#7-failure-modes)
- [8. Multi-Layer Caches](#8-multi-layer-caches)
- [Sources](#sources)

## 1. Why Cache

Three benefits, in this order: **latency** (memory is ~100× faster than disk), **throughput**, **bandwidth** (data closer to the user — a CDN is a form of cache).

Both authors flag the same anti-pattern: throwing a cache in front of every database without tying the decision to a non-functional requirement. The latency gain depends on the target — 5 ms to 0.1 ms is pointless at a 500 ms SLO and meaningful at a 20 ms SLO.

## 2. Cache Hit Rate

```
Hit Rate = Hits / (Hits + Misses)
```

What is cached changes the rate dramatically. Caching a full free-text search query yields a poor hit rate (each query is unique). Caching per-token posting lists reuses tokens across queries and lifts the rate substantially. The granularity of the cache key is the design lever.

## 3. Read Patterns

**Read-through** (Xu's default): web server checks cache first, queries DB on miss, populates the cache, returns to the client. The cache is consulted on every read; the application never goes directly to the DB.

**Cache-aside**: application reads from cache; on miss, fetches from DB and explicitly writes to cache. Same effect; the difference is who manages the population.

## 4. Write Strategies

Liu's three:

| Strategy | How it works | Trade-off |
|---|---|---|
| Write-through | Synchronous write to cache and store | Atomicity not guaranteed across the two; cache stays warm |
| Write-back | Write to cache first, async to store | Lowest write latency; data loss risk if cache crashes before flush |
| Write-around | Write to store first; cache populated on read miss | Most durable; cache warm-up complex on cold reads |

## 5. Invalidation

> "There are only two hard things in computer science: cache invalidation and naming things." — Phil Karlton

Liu's four approaches:

1. **Listener on source values.** Freshest. Expensive — every store update fires a cache event.
2. **Periodic recomputation.** Simple. Stale between runs.
3. **Cache a lower layer and fan in on read.** Used in Netflix recommendations and Facebook News Feed — each component is cached individually; the response is composed at read time.
4. **TTL.** What DNS does, because invalidating browser caches is impractical.

Liu recommends **delete over update** on cache invalidation: two concurrent database updates don't guarantee cache ordering, and delete is idempotent.

## 6. Eviction Policies

- **LRU** (Least Recently Used) — the most common default; evicts the entry not touched longest.
- **LFU** (Least Frequently Used) — favors hot keys; can starve newcomers without aging.
- **Custom domain-specific** — driver location updates evict by age; leaderboards keep top-N regardless of access.

The right policy follows the query pattern, not a default.

## 7. Failure Modes

- **Crashed cache loses everything.** A cold restart can flood the database. Mitigations: periodic snapshots, write-ahead log, no backup at all (transient data like driver locations), or replication.
- **Thundering herd.** Many readers miss simultaneously and stampede the source. Mitigated by **cache blocking** — only one request fetches; the rest wait for the result. Stale-while-revalidate is a softer variant.
- **Cache as SPOF.** Xu's framing: a single cache instance is a Single Point of Failure. Mitigations: replicate cache servers across DCs, overprovision memory.
- **Caches don't automatically improve bandwidth.** Streaming YouTube is network-bound; that's what CDNs solve. See [CDN](fundamentals/cdn.md).

## 8. Multi-Layer Caches

Xu's News Feed deep dive uses five caches tuned per access pattern:

| Cache | Holds | Why |
|---|---|---|
| News feed cache | Ordered list of post IDs per user | Hot read on feed open |
| Content cache | Full post content by post ID | Hot reads on render |
| Social graph cache | Friend/follower lists | Joined on every fanout |
| Action cache | Like, comment, share counts | Counters change frequently |
| Counter cache | Aggregated view counts | Distinct from per-user actions |

The pattern (cache-a-lower-layer-and-fan-in) is Liu's third invalidation approach in disguise — each component invalidates independently, the response composes at read time.

## Sources

- [Liu Ch 5.08: Cache Strategies](software/system-design-interview/books/system-design-interview-fundamentals/ch05_08_cache_strategies.md)
- [Xu Ch 1: Scale From Zero to Millions of Users](software/system-design-interview/books/system-design-interview-insiders-guide/ch01_scale_zero_to_millions.md) (cache section)
- [Xu Ch 11: Design a News Feed System](software/system-design-interview/books/system-design-interview-insiders-guide/ch11_design_a_news_feed_system.md) (multi-layer cache)
