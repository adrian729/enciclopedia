# Ch 6.01: Ridesharing Service

## Table of Contents

- [1. Requirements](#1-requirements)
- [2. API](#2-api)
- [3. High-Level Design](#3-high-level-design)
- [4. Schema](#4-schema)
- [5. End-to-End Flow](#5-end-to-end-flow)
- [6. Deep Dives](#6-deep-dives)

## 1. Requirements

- **Prompt** — design a ridesharing service like Uber/Lyft
- **Scope narrowed to**: match riders with drivers (features like Uber Pool, cost estimation, cancellation are tabled)
- **Assumptions** agreed with interviewer:
  - **100M DAU**, concentrated in North America and Europe
  - Expect bursty traffic (Friday night, concert/sporting event endings)
  - Match on **linear distance** (ignore real-world edge cases like rivers)
  - Wait time should be minimized; 30 seconds is acceptable
  - Location accuracy tolerance: ~10 seconds (10s of movement doesn't materially change match)
  - **Availability** for ride requests is the priority non-functional requirement

## 2. API

```
Rider:
  request_ride(user_id, from_location, to_location) → status
  matched_ride(driver_info)   // server push callback

Driver:
  update_location(user_id, current_location) → status
```

- **Location** = `(longitude, latitude)` tuple
- `SUCCESS` on `request_ride` = server accepted and is finding a match, not that a driver is assigned
- `matched_ride` is the callback once a match exists

## 3. High-Level Design

- **Request queue** fronts the ride-matching service to absorb bursty traffic
- **Ride-matching service** pulls from the queue, reads from location storage, writes to ride storage
- **Notification service** broadcasts the match to rider and driver
- **Location service** accepts driver location updates and writes to location storage

## 4. Schema

**Request queue event**

| Rider Id | From Location |
|---|---|

**Ride table** — one active ride per rider and per driver

| Ride Id | Rider Id | Driver Id | From Location | To Location | Status |
|---|---|---|---|---|---|

**Location storage** — search by location is a full table scan; to be optimized in deep dive

| Driver Id | Current Location |
|---|---|

## 5. End-to-End Flow

- **`request_ride`**: rider → rider service → request queue; ride-matching service pulls batch → reads location storage → writes to ride storage → notification service broadcasts match to both parties
- **`update_location`**: driver → location service → location storage. Update frequency is itself a deep-dive topic

## 6. Deep Dives

### 6.1 Driver Location Update Throughput

- **Math**: 10% of 100M DAU = 10M drivers. 1 update every 10s = **1M QPS**. Database ≈ 500 QPS, SSD ≈ 10k QPS — direct disk writes need 100–2000+ shards
- **Options**:

| Option | Upside | Downside |
|---|---|---|
| Queue in front of DB + micro-batch | Durability | More machines, more complexity |
| Write to **location cache** | Cache handles 50k+ QPS; low latency | Loss on cache failure |
| Lower update frequency (10s → 20s) | Fewer writes | Matched driver may briefly drive away |

- **Conclusion** — combine options 2 and 3: cache-backed location storage (durability doesn't matter because the next update obsoletes any lost one) and monitor match quality after reducing frequency. No queue needed once cache capacity suffices

### 6.2 Location Cache Failure

- **Leader-follower replication** — leader-election pause interrupts location updates during failover
- **Leaderless replication** — quorum write/read continues through single-node failures at the cost of occasional stale reads
- **Conclusion** — **leaderless** favors availability (and location accuracy isn't critical)

### 6.3 Location Storage Search

- **Full table scan** — correct but too slow
- **QuadTree index** — in-memory quadtree; each quad holds a list of driver IDs. On update, remove the driver from its old quad before inserting into the new one
- **Conclusion** — QuadTree. In production, specialized structures like **Google S2** exist, but QuadTree is enough for the interview

### 6.4 Match-Making Concurrency

- **Scenario** — two riders standing next to each other request at the same time; both best-match the same driver
- **Options**:

| Option | Throughput | Issue |
|---|---|---|
| Serial | Low | IO overhead per request kills throughput |
| **Serial batch** — dispatch a batch of riders against a batch of drivers | High | Complexity; needs batch tuning |
| Pessimistic lock on quadtree cell | Low | Requests block each other |
| Optimistic lock (conditional commit to ride table) | High | Retry storm on failure → poor UX |

- **Conclusion** — **serial batch** with a dispatcher; tune batch size to hit required throughput

### 6.5 Bursty Requests

- **Math**: 100M DAU × 2 rides/day × 10× peak multiplier = 2×10⁹ QPD ÷ 10⁵s = **20,000 QPS** at peak, for an expensive matching calculation
- **Mitigations already in place** — queue absorbs the spike; monitor for spillover; batch matching solves concurrency
- **Sharding** for match-making throughput:
  - **Shard by locality (parent + sub-shards)** — adjacent shards usually on the same host, so cross-shard forwarding is cheap. Downside: one populated region (e.g., San Francisco) creates hotspots on one parent shard
  - **Random (sub-shards only)** — forwards to adjacent sub-shards on other hosts when local driver supply is low
- **Conclusion** — **random sub-sharding**; accept occasional cross-host forwarding (low driver supply events are rare) in exchange for avoiding hotspots
