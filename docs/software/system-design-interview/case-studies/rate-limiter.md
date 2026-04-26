# Rate Limiter

> Both books cover rate limiting. Xu's Ch 4 is the algorithmic primer (token bucket, leaking bucket, fixed window, sliding window log, sliding window counter). Liu's Ch 6.07 is the case study (write-back cache + async replication, accuracy as a non-functional requirement). They complement: Xu picks the algorithm; Liu picks the topology.

## Table of Contents

- [1. Requirements](#1-requirements)
- [2. Algorithm Comparison](#2-algorithm-comparison)
  - [2.1. Token Bucket](#21-token-bucket)
  - [2.2. Leaking Bucket](#22-leaking-bucket)
  - [2.3. Fixed Window Counter](#23-fixed-window-counter)
  - [2.4. Sliding Window Log](#24-sliding-window-log)
  - [2.5. Sliding Window Counter](#25-sliding-window-counter)
- [3. High-Level Design](#3-high-level-design)
- [4. Distributed Architecture](#4-distributed-architecture)
- [5. Liu's Topology — Write-Back Cache + Async Replication](#5-lius-topology--write-back-cache--async-replication)
- [6. Trade-offs Called Out](#6-trade-offs-called-out)
- [Sources](#sources)

## 1. Requirements

Functional:
- Cap requests per client (or per IP, per API key, per route) over a time window.
- Reject (or queue) excess requests with a clear status code (HTTP 429).

Non-functional:
- **Low latency** — adds to every request; tens of microseconds is the budget.
- **Inaccuracy tolerable.** Liu's framing: a 1% error rate is acceptable. Exact accuracy under contention is expensive and rarely needed.
- **High availability.** A failed rate limiter shouldn't take down the service ([fail to open](fundamentals/resilience-patterns.md)).

Sat at the [API gateway](fundamentals/api-design-and-gateway.md), which has visibility into all incoming requests.

## 2. Algorithm Comparison

| Algorithm | Allows bursts? | Memory | Accuracy | Notable users |
|---|---|---|---|---|
| Token bucket | Yes (up to bucket size) | Low | Good | Amazon, Stripe |
| Leaking bucket | No (fixed outflow) | Low | Good | Shopify |
| Fixed window | Edge bursts leak | Low | Edge-burst flaw | — |
| Sliding window log | No | High (stores all timestamps) | Very accurate | — |
| Sliding window counter | Smoothed | Low | Approximate | — |

### 2.1. Token Bucket

Tokens are added at a fixed refill rate; bucket has a max capacity. Each request consumes one token; if no tokens, reject. Allows bursts up to the bucket size — a quiet client accumulates tokens and can spike.

### 2.2. Leaking Bucket

A FIFO queue with a fixed outflow rate. Requests are added; the bucket drains at a steady rate. Doesn't allow bursts (the outflow rate caps everything) but smooths spiky input into steady output.

### 2.3. Fixed Window Counter

Count requests in the current minute (or hour, day). Reset at boundary. Cheap, simple. **Edge-burst flaw**: a burst spanning the boundary (last second of minute N + first second of minute N+1) can effectively double the allowed quota.

### 2.4. Sliding Window Log

Store every request timestamp in a sorted set. On each new request, remove timestamps older than the window and count what's left. Very accurate; high memory cost (one entry per request).

### 2.5. Sliding Window Counter

Hybrid that smooths the fixed-window edge-burst:

```
estimated = current_window_count + previous_window_count × overlap_percentage
```

Approximates a true sliding window with the cost of a fixed-window counter. Most production rate limiters use this or a near variant.

## 3. High-Level Design

```
Client → API Gateway (rate limiter) → Service
                ↓
              Redis (counters)
```

The gateway intercepts every request, looks up the current counter for the client+route key, decides allow/reject, and forwards or returns 429.

## 4. Distributed Architecture

Multiple gateway instances need a shared view of the counter. Two issues:

- **Race conditions** on `INCR` + check. Mitigated by **Redis Lua scripts** (atomic execution) or **sorted sets** (the sliding-window-log primitive).
- **Synchronization** across gateway instances. Both books reject sticky sessions explicitly — clients shouldn't be pinned to a single gateway. The shared store (Redis cluster) is the source of truth.

Xu's specific recommendation: Redis as the counter store; `INCR` and `EXPIRE` for fixed-window; sorted sets for sliding-window-log; Lua scripts for atomicity.

## 5. Liu's Topology — Write-Back Cache + Async Replication

Liu's case-study framing emphasizes the **non-functional requirement** lever. Because 1% inaccuracy is acceptable:

- The counter lives in a **write-back cache** (memory-fast).
- Replication to a durable store is **async** (replication lag is acceptable).
- The fast path (allow/reject decision) doesn't wait for replication.

The trade-off: under leader failover, some recent counter increments may be lost — but the user-visible impact is at most a 1% over-count, well within tolerance.

This is a senior-level move: tying the storage choice to the *accuracy SLO* rather than picking "Redis with persistence" by default.

## 6. Trade-offs Called Out

- **Allow vs reject under uncertainty.** Fail-to-open: if Redis is down, allow the request. Lets a temporary cache outage avoid taking down the service. Fail-closed (reject) is appropriate only if rate limiting is a hard security boundary.
- **Per-route vs per-client granularity.** Per-route is cheap (one counter per route); per-client is expensive (one counter per (client, route)) but more precise.
- **Quota distribution across gateways.** Each gateway can hold a local quota slice (faster but less accurate) or rely entirely on the shared Redis (slower but exact).
- **Algorithm choice follows workload.** Burst-tolerant API (token bucket); steady-flow API (leaking bucket); approximate-but-cheap (sliding window counter).

## Sources

- [Xu Ch 4: Design a Rate Limiter](software/system-design-interview/books/system-design-interview-insiders-guide/ch04_design_a_rate_limiter.md)
- [Liu Ch 6.07: Rate Limiter](software/system-design-interview/books/system-design-interview-fundamentals/ch06_07_rate_limiter.md)
