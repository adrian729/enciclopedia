# URL Shortener

> Xu only — Liu doesn't cover this product. The interesting part is the long-to-short hash function and the choice between hash-and-truncate-with-collision-resolution vs base-62 conversion of a unique numeric ID.

## Table of Contents

- [1. Requirements](#1-requirements)
- [2. Estimation](#2-estimation)
- [3. API](#3-api)
- [4. The Long-to-Short Hash](#4-the-long-to-short-hash)
  - [4.1. Hash + Collision Resolution](#41-hash--collision-resolution)
  - [4.2. Base-62 Conversion of a Unique ID](#42-base-62-conversion-of-a-unique-id)
- [5. High-Level Design](#5-high-level-design)
- [6. Redirect Behavior — 301 vs 302](#6-redirect-behavior--301-vs-302)
- [7. Scaling Moves](#7-scaling-moves)
- [Sources](#sources)

## 1. Requirements

- Shorten a long URL to a short URL.
- Redirect short → long with low latency.
- Track clicks (analytics).
- Custom aliases optional.

## 2. Estimation

- **Writes**: 100M URLs/day → ~1,160 writes/second.
- **Reads**: 10:1 read:write ratio → ~11,600 reads/second.
- **Storage**: 100M × 365 days × 10 years = **365 billion records**.
- **Hash length**: alphabet of 62 characters (`a-z`, `A-Z`, `0-9`). Smallest `n` where `62^n ≥ 365B` is **n=7**.

7 characters is the magic number — every short URL fits in 7 alphanumeric characters.

## 3. API

```
POST /api/v1/shorten
  body: { long_url }
  → { short_url }

GET /:short_code
  → 301 or 302 redirect to long_url
```

## 4. The Long-to-Short Hash

### 4.1. Hash + Collision Resolution

`MD5(long_url)`, take the first 7 characters, check the DB; if it's already taken (collision), append a salt and re-hash. A **bloom filter** in front of the DB makes the existence check cheap.

Drawbacks: collision-handling complexity grows as the corpus fills; verifying uniqueness requires either a DB lookup or a bloom filter that itself needs sizing.

### 4.2. Base-62 Conversion of a Unique ID

Generate a globally-unique 64-bit ID (e.g., [Snowflake](fundamentals/id-generation.md)) and convert to base-62. Each digit is a character in `[0-9, a-z, A-Z]`; 7 base-62 digits cover up to ~3.5 trillion values.

**Base-62 wins** in Xu's analysis:

- No collision check.
- Predictable behavior (no probabilistic verification).
- Easy overflow handling — when 7 characters fill up, extend to 8.
- The Snowflake ID is monotonically increasing, so short codes are roughly time-ordered.

The trade-off: short codes leak the rough creation time. For a public URL shortener that doesn't matter; for a private one that wants randomness, hash-and-truncate is the alternative.

## 5. High-Level Design

```
Client
  ↓
API Gateway (rate limit, auth)
  ↓
Web Servers (stateless)
  ↓                   ↓
Redis cache    URL DB (sharded)
                ↓
              Snowflake ID generator
```

- **API Gateway** handles rate limiting (see [Rate Limiter](case-studies/rate-limiter.md)).
- **Web tier** is stateless — any server handles any request.
- **URL DB** is sharded by `short_code` (or by Snowflake ID range). Read-heavy.
- **Cache** sits in front of the DB for hot short URLs (popular links get most of the read traffic).

## 6. Redirect Behavior — 301 vs 302

| Code | Meaning | Behavior |
|---|---|---|
| 301 | Permanently moved | Browsers cache the redirect; subsequent clicks bypass the shortener server. Reduces server load. |
| 302 | Temporarily moved | Browsers re-check on every click. Useful for click analytics. |

The choice is a product decision: 301 reduces infrastructure cost; 302 enables analytics. Many shorteners pick 302 specifically to keep the analytics flow.

## 7. Scaling Moves

- **DB sharding** by short_code.
- **Web tier statelessness** for autoscaling (see [Scaling Evolution](fundamentals/scaling-evolution.md)).
- **Cache** in front of the DB — Redis or Memcached, LRU eviction. Hot short URLs (a viral link) dominate read traffic.
- **Rate limiting** at the API gateway prevents abuse (mass-shortening, scraping).
- **Analytics integration** — write a click event to a separate stream (Kafka) for the analytics pipeline; the redirect path doesn't wait for analytics. See [Async, Batch, Stream](fundamentals/async-batch-stream.md).

## Sources

- [Xu Ch 8: Design a URL Shortener](software/system-design-interview/books/system-design-interview-insiders-guide/ch08_design_a_url_shortener.md)
