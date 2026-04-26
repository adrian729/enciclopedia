# Ch 4: Design a Rate Limiter

## Table of Contents

- [1. What a Rate Limiter Is and Why It Matters](#1-what-a-rate-limiter-is-and-why-it-matters)
- [2. Step 1: Requirements](#2-step-1-requirements)
- [3. Step 2: Where to Put the Rate Limiter](#3-step-2-where-to-put-the-rate-limiter)
- [4. Algorithms Compared](#4-algorithms-compared)
- [5. Token Bucket](#5-token-bucket)
- [6. Leaking Bucket](#6-leaking-bucket)
- [7. Fixed Window Counter](#7-fixed-window-counter)
- [8. Sliding Window Log](#8-sliding-window-log)
- [9. Sliding Window Counter](#9-sliding-window-counter)
- [10. High-Level Architecture](#10-high-level-architecture)
- [11. Step 3: Rules, Headers, and Detailed Design](#11-step-3-rules-headers-and-detailed-design)
- [12. Distributed Environment: Race Conditions and Synchronization](#12-distributed-environment-race-conditions-and-synchronization)
- [13. Performance Optimization and Monitoring](#13-performance-optimization-and-monitoring)
- [14. Step 4: Wrap-Up Talking Points](#14-step-4-wrap-up-talking-points)

## 1. What a Rate Limiter Is and Why It Matters

- **Definition** — controls the rate of traffic from a client or service; in HTTP, caps client requests per period and blocks excess calls
- **Examples** — no more than 2 posts per second per user, max 10 accounts per day per IP, max 5 reward claims per week per device
- **Prevent DoS resource starvation** — almost every large-tech API enforces some rate limiting (Twitter: 300 tweets per 3 hours; Google Docs API: 300 reads per user per 60 seconds)
- **Reduce cost** — fewer servers, more headroom for high-priority APIs, and crucial when paying per call to third-party APIs (credit checks, payments, health records)
- **Prevent server overload** — filters bot traffic and misbehaving users before they degrade the system

## 2. Step 1: Requirements

- **Server-side API rate limiter** — not client-side; flexible enough to support different throttle rule sets
- **Scale** — must handle a large number of requests in a distributed environment
- **Constraints** — accurate, low-latency (must not slow HTTP responses), memory-efficient, distributed (shared across servers/processes), informs throttled users with clear exceptions, fault-tolerant (a failed cache server must not bring down the system)

## 3. Step 2: Where to Put the Rate Limiter

- **Client-side** — unreliable: client requests are easily forged and clients are often outside your control
- **Server-side** — limiter sits next to or inside the API server
- **Middleware** — a dedicated rate-limiter middleware throttles before hitting API servers; example: 2 req/sec allowed, third request returns HTTP 429 (Too Many Requests)
- **API gateway** — in cloud microservices, rate limiting is commonly handled by a fully managed API gateway alongside SSL termination, authentication, IP whitelisting, and static content
- **Choosing server vs gateway** — depends on tech stack, engineering resources, and priorities: server-side gives full algorithm control, gateway is fastest if you already use one or lack engineering capacity to build your own

## 4. Algorithms Compared

| Algorithm | Allows bursts? | Memory | Accuracy | Notable users |
|-----------|----------------|--------|----------|---------------|
| Token bucket | Yes (up to bucket size) | Low | Good | Amazon, Stripe |
| Leaking bucket | No (fixed outflow) | Low | Good for stable outflow | Shopify |
| Fixed window counter | No (but edge spikes leak) | Low | Edge-burst flaw | — |
| Sliding window log | No | High (stores all timestamps) | Very accurate | — |
| Sliding window counter | Smoothed | Low | Approximate | — |

## 5. Token Bucket

- **Mechanics** — a bucket of fixed capacity; a refiller adds tokens at a preset rate; once full, extra tokens overflow; each request consumes one token, and requests with no tokens available are dropped
- **Parameters** — `bucket size` (max tokens) and `refill rate` (tokens added per second)
- **Bucket count** — depends on rules: per-endpoint buckets (e.g., 1 post/sec, 150 friends/day, 5 likes/sec needs 3 buckets per user), per-IP buckets, or one global bucket for system-wide caps (e.g., 10,000 req/sec)
- **Pros** — easy to implement, memory-efficient, allows short bursts of traffic as long as tokens remain
- **Cons** — tuning bucket size and refill rate properly can be challenging

## 6. Leaking Bucket

- **Mechanics** — a FIFO queue: arriving requests are enqueued if there's room, otherwise dropped; requests are pulled and processed at a fixed rate
- **Parameters** — `bucket size` (queue length) and `outflow rate` (requests processed per second)
- **Used by** — Shopify for rate-limiting
- **Pros** — memory-efficient, stable outflow rate suits use cases needing predictable downstream load
- **Cons** — a burst fills the queue with old requests, so recent requests get rate-limited while stale ones are still being served; two parameters to tune

## 7. Fixed Window Counter

- **Mechanics** — divide the timeline into fixed-size windows, assign a counter per window, increment on each request, drop once the threshold is reached, reset at the next window
- **Edge-burst flaw** — bursts straddling a boundary can double the allowed quota: 5 req/min limit with 5 requests at 2:00:00–2:01:00 and 5 more at 2:01:00–2:02:00 lets 10 requests through in the 2:00:30–2:01:30 window
- **Pros** — memory-efficient, easy to understand, fits cases that naturally reset on round time boundaries
- **Cons** — edge-of-window traffic spikes can exceed the intended quota

## 8. Sliding Window Log

- **Mechanics** — track a timestamp per request (typically in a Redis sorted set); on each new request, evict timestamps older than the window start, append the new one, and accept if the log size is at or below the limit
- **Worked example (2 req/min)** — request at 1:00:01 logged and allowed; 1:00:30 allowed (log size 2); 1:00:50 rejected because log size becomes 3 (timestamp still kept); 1:01:40 allowed after evicting two outdated entries (1:00:01 and 1:00:30)
- **Pros** — very accurate; in any rolling window, requests never exceed the rate limit
- **Cons** — high memory usage because rejected requests still keep their timestamps

## 9. Sliding Window Counter

- **Mechanics** — hybrid of fixed-window counter and sliding-window log; a request's effective count is `requests in current window + requests in previous window × overlap percentage of the rolling window with the previous window`
- **Worked example (7 req/min)** — 5 requests in previous minute, 3 in current; new request at 30% into current minute → `3 + 5 × 0.7 = 6.5`, rounded down to 6; allowed (one more request would hit the limit)
- **Pros** — smooths traffic spikes (uses average rate of previous window), memory-efficient
- **Cons** — approximate; assumes evenly distributed requests in the previous window. Cloudflare experiments on 400M requests showed only 0.003% of requests wrongly allowed or limited

## 10. High-Level Architecture

- **Counter store** — disk DBs are too slow; an in-memory cache supports time-based expiration and is the natural fit
- **Redis primitives** — `INCR` increments the counter by 1; `EXPIRE` sets a timeout that auto-deletes the counter
- **Flow** — client → rate-limiter middleware → fetch counter from Redis → if limit reached, reject; otherwise forward to API server, increment counter, save back to Redis

## 11. Step 3: Rules, Headers, and Detailed Design

- **Rule storage** — rules live in configuration files on disk; workers periodically pull them from disk into the cache
- **Lyft rate-limiting config example** — domain `messaging`, key `message_type`, value `marketing`, `unit: day`, `requests_per_unit: 5` (max 5 marketing messages per day); auth example caps logins at 5 per minute
- **HTTP 429 response** — returned when a request is throttled; rate-limited orders may be enqueued for later processing instead of dropped
- **Rate limiter headers** — `X-Ratelimit-Remaining` (allowed requests left in window), `X-Ratelimit-Limit` (calls per window), `X-Ratelimit-Retry-After` (seconds to wait before retrying); 429 responses include `X-Ratelimit-Retry-After`
- **Detailed flow** — request hits middleware, which loads rules from cache and counters/last-request timestamps from Redis, then either forwards or returns 429 (dropping the request or routing it to a queue)

## 12. Distributed Environment: Race Conditions and Synchronization

- **Race condition** — two concurrent requests read counter `3`, each computes `4`, and both write `4`; the correct value should be `5`
- **Lock-free fixes** — locks are obvious but slow the system; the chapter recommends Lua scripts or Redis sorted sets to eliminate the race without locks
- **Synchronization issue** — multiple stateless rate-limiter servers handling the same client need shared state; without it, limiter 1 has no record of requests routed to limiter 2
- **Sticky sessions** — pin a client to one rate limiter; rejected as not scalable or flexible
- **Centralized data store** — use Redis as the shared counter store so any rate-limiter server can serve any client correctly

## 13. Performance Optimization and Monitoring

- **Multi-data-center setup** — latency is high for users far from the data center; cloud providers route traffic to the nearest edge (Cloudflare had 194 globally distributed edge servers as of 5/20 2020)
- **Eventual consistency** — synchronize data across rate limiters with an eventual-consistency model (see "Consistency" section in Ch 6: Design a Key-value Store)
- **Monitoring goals** — confirm the rate-limiting algorithm is effective and the rules are effective
- **Acting on monitoring** — too-strict rules drop valid requests (relax them); ineffectiveness during flash-sale traffic spikes suggests switching to a burst-friendly algorithm like token bucket

## 14. Step 4: Wrap-Up Talking Points

- **Hard vs soft rate limiting** — hard caps cannot be exceeded; soft caps allow brief overshoots
- **Rate limiting at different OSI layers** — chapter focuses on layer 7 (HTTP, application); IP-level limiting at layer 3 is possible via Iptables. The OSI model has 7 layers: Physical, Data link, Network, Transport, Session, Presentation, Application
- **Client best practices to avoid being rate-limited** — use client cache to skip frequent API calls, know the limit and don't burst, catch exceptions/errors for graceful recovery, add sufficient back-off time to retry logic
