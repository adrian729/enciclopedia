# Ch 6.07: Rate Limiter

## Table of Contents

- [1. Requirements](#1-requirements)
- [2. API](#2-api)
- [3. High-Level Design](#3-high-level-design)
- [4. Schema](#4-schema)
- [5. End-to-End Flow](#5-end-to-end-flow)
- [6. Deep Dives](#6-deep-dives)

## 1. Requirements

- **Prompt** — design a rate limiter
- **Scope narrowed to**: external client with a per-customer budget (calls per time frame). Limit is at the customer level, independent of which API is called
- **Assumptions** agreed with interviewer:
  - **10M customers**, ~**1,000 calls/day each**
  - Traffic pattern unknown; anticipate spikes
  - Protected API is an **asynchronous job**; p50 = 500 ms, latency **not** sensitive
  - Short-term over-limit is tolerable; **long-horizon accuracy** matters (over-processing costs money, under-processing angers customers)
  - Availability has leeway (async); **durability** matters for long-horizon accuracy
- **Time frame** — requests per **hour** (default); requests per second considered separately

## 2. API

```
invoke_api(customer_id) → status   // ALLOW or DENY
```

- Only one API because it represents the single async API being throttled

## 3. High-Level Design

- **Rate limiter service** fronts the protected API; rejects or throttles requests exceeding the budget
- **Request queue** behind the rate limiter buffers allowed requests for the async workers
- **Counter storage** (cache and/or database) tracks per-customer counts within the current time window

## 4. Schema

*Skipped by the author — nothing to talk about at the schema level; deep dives cover the counter storage choice.*

## 5. End-to-End Flow

- User calls `invoke_api(customer_id)` → rate limiter checks and increments counter → if under limit, enqueue to request queue for async processing; if over, reject

## 6. Deep Dives

### 6.1 Throttling Placement

| Option | Upside | Downside |
|---|---|---|
| **Throttle at the API level** (reject + retry) | Clear contract; no hidden backlog | Client must retry |
| Throttle after the request queue | Customer doesn't need to retry; smooths load | Backlog grows; jobs expected to run immediately may queue silently; must monitor and reject once backlog is too big |

- **Conclusion** — either works; if throttling post-queue, make the contract explicit and monitor backlog size

### 6.2 Rate Limiter Algorithm

| Option | Upside | Downside |
|---|---|---|
| **Fixed window** | Simple; tiny memory (one count per window) | Inaccurate around window boundaries (a burst spanning two windows can double the limit) |
| Sliding window (store every timestamp) | Accurate | Memory intensive |
| Token bucket (tokens refilled periodically) | Intuitive; flexible refill policy | Can have the same boundary inaccuracy as fixed window depending on refill algorithm |

- **Reminder** — a token bucket that refills X tokens every Y minutes is algorithmically equivalent to a fixed window of X requests per Y minutes; the token bucket is just easier to reason about for ad-hoc refills
- **Conclusion** — start with **fixed window** for simplicity

### 6.3 Rate Limiter Failure

| Option | Upside | Downside |
|---|---|---|
| Fail to close | Never exceeds true rate | Backlog accumulates; workers idle |
| **Fail to open** (fallback constant per processor) | Drains the pipeline | May let customers through more/less than true rate; constant must be tuned |
| **Leader-follower with async replication** | Can elect new leader with recent data | Leader-election pause; every request is a write, so no read-replica scaling |
| CRDT (per-node count, async broadcast) | Very high availability; any node accepts traffic | Broadcast overhead; cascading risk as survivors absorb failed nodes' load |

- **Conclusion** — **combine fail-to-open + leader-follower**. Fail-to-open keeps workers busy with a conservative constant; leader-follower recovers within seconds. CRDT is elegant but broadcast overhead and the async-job tolerance for brief downtime don't justify it

### 6.4 Data Storage — Long Time Horizon (requests per hour)

- **Math** — 10M customers × 1,000 calls/day × 2 peak = **2×10¹⁰ QPD** → ~**200,000 QPS**

| Option | Upside | Downside |
|---|---|---|
| Database (atomic increment) | Durable across the hour | 200k QPS is extremely high; even LSM (Cassandra) strains |
| Cache (atomic increment) | 50k–100k QPS per node; easy to scale | Not durable; crash mid-hour loses significant data |
| **Write-back cache → durable backup** | Cache performance + async durability | Some data loss acceptable given replication lag |

- **Conclusion** — **write-back cache with async replication to durable storage**; accept small inaccuracy from replication lag

### 6.5 Data Storage — Short Time Horizon (requests per second)

- **Conclusion** — plain **cache** without durability. By the time a warm-up from backup finishes, the data is already stale anyway

### 6.6 Client-Facing Latency-Sensitive Rate Limiting

- **New requirement** — 15 ms p99. Disk reads (2–5 ms) and distributed cache round-trips each eat a big chunk of the budget

| Option | Upside | Downside |
|---|---|---|
| **Distributed cache** | Simplest; ~1 ms intra-datacenter | Every request pays a network hop |
| Instance-level (stateful) rate limiter | No network call | App servers become stateful; load balancer must sticky-route; availability hit on instance failure |
| **Stateless instances with approximation** — `instance_limit = global_limit / healthy_hosts` | Stateless; no network call | Inaccurate (instance can over-admit if traffic lands unevenly); topology changes skew math |
| Client-side forward proxy | Offloads cost to client | Bypassable; rolling client changes is hard; centralized proxy reintroduces a hop |

- **Conclusion** — **distributed cache (option 1)** and renegotiate the SLA; fall back to **stateless approximation (option 3)** only if latency is strict and occasional inaccuracy is acceptable. Reject stateful app-server option because it couples rate-limiting state into services that should remain stateless
