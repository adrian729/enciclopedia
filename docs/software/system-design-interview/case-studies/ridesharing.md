# Ridesharing Service (Uber / Lyft)

> Liu's Ch 6.01 only — Xu doesn't cover this product. The interesting parts are the **location store** (cache-backed leaderless replication), **concurrency** (serial batch dispatcher), and the senior-level **product redesign** that eliminates a thorny race condition.

## Table of Contents

- [1. Requirements](#1-requirements)
- [2. Estimation](#2-estimation)
- [3. API](#3-api)
- [4. Location Store](#4-location-store)
- [5. The Matching Concurrency Problem](#5-the-matching-concurrency-problem)
- [6. Geo-Sharding](#6-geo-sharding)
- [7. Architecture](#7-architecture)
- [8. The Product-Redesign Move](#8-the-product-redesign-move)
- [9. Trade-offs](#9-trade-offs)
- [Sources](#sources)

## 1. Requirements

In scope:
- Match riders with drivers.
- Track driver locations in real time.

Out of scope (explicitly tabled): Pool / shared rides, fare calculation, cancellation flows.

Non-functional:
- **Availability** is the dominant constraint. Bursty traffic (10× at concert-end) must not break matching.
- **Freshness** of driver location is near-real-time.

## 2. Estimation

100M DAU × 2 rides per day × 10× peak factor / 86,400 seconds = **~20,000 peak QPS** on the matching path.

Driver location updates: 10M active drivers × 1 update per 5 seconds = **~2M location updates/sec**.

The numbers expose two scaling problems: matching at 20K QPS is expensive (it's a geographic search, not a hash lookup), and location updates at 2M/sec saturates a normal data store.

## 3. API

```
request_ride(user_id, pickup_location, destination)
  → { driver_id, eta }     # server picks the driver — see Section 8

update_driver_location(driver_id, location)
  → ack
```

Output of `request_ride` returns *one* `driver_id`, not a list — see Section 8.

## 4. Location Store

Driver locations are written at 2M/sec but only read during matching. The right data store:

- **Cache-backed** — reads hit memory, not disk.
- **Leaderless replication** — high write throughput, no leader bottleneck.
- **Sampling** is acceptable for performance — Liu's [resilience pattern](fundamentals/resilience-patterns.md): persisting every 5th location update cuts QPS by 80% with tolerable freshness loss.
- **No backup needed** — location is transient; on cache crash, drivers re-emit locations within seconds.

The store is *not* the durable system of record for driver location. It's a hot cache.

## 5. The Matching Concurrency Problem

Naive matching: rider requests; system picks 3 nearby drivers; sends each an "accept this ride?" prompt; first-to-accept wins. Problem: **race condition**. Two riders' requests can both pick the same driver as a candidate. The driver accepts one — but the other rider was already promised the same driver.

Liu's pick: **serial batch dispatcher** per geographic region. The dispatcher serializes matches:

```
Region dispatcher (single-threaded per region)
   ↓
   Pull pending requests for region (micro-batch)
   ↓
   Greedily assign each request to the best available driver
   ↓
   Mark assigned drivers as busy
```

Sharded serial — see [Concurrency & Transactions](fundamentals/concurrency-and-transactions.md) — gives high throughput across the global system (one dispatcher per region, all running concurrently) while serializing within each region where conflicts can occur.

Pessimistic locking would also work but produces retry storms under burst load. Optimistic locking would mean lots of failed assignments. Serial-per-region is the cleanest fit.

## 6. Geo-Sharding

Top-level routing by **geographic zone** (San Francisco, NYC, Tokyo). Each zone has:

- Its own location store.
- Its own dispatcher.
- Its own scaled fleet of matching workers.

Cross-zone matches are rare (a driver crossing a city boundary mid-trip is a separate problem). See [Sharding & Consistent Hashing](fundamentals/sharding-and-consistent-hashing.md).

## 7. Architecture

```
Driver app                                Rider app
   ↓                                          ↓
update_driver_location                  request_ride
   ↓                                          ↓
Geo-routed Location Service       Geo-routed Match Service
   ↓                                          ↓
Cache-backed leaderless         Region Dispatcher (serial batch)
location store                            ↓
                                Driver Selection Algorithm
                                          ↓
                            Notify Driver → Notify Rider
```

A QuadTree (in-memory, see [Databases, Schema, Indexing](fundamentals/databases-schema-indexing.md)) is one option for the geo-index inside the Match Service. Google S2 is the production-grade equivalent.

## 8. The Product-Redesign Move

The headline senior-level move from Liu: when the technical complexity of "user picks driver from a list of candidates" gets thorny (race conditions, retry storms, expired offers), **change the product**.

If the API returns a single `driver_id` (server-assigned), the user has the same UX — they don't actually pick the driver in either design — but the technical complexity collapses. No fanout, no race, no retry on rejection.

This is the pattern Liu emphasizes throughout the book: when concurrency gets hairy, ask whether the product requirement can change. See the [Communication & Evaluation](process/communication.md) framing.

## 9. Trade-offs

- **Sampling vs accuracy.** Persisting every 5th location update is 80% cheaper at the cost of 5x staleness. Tolerable for matching; might not be tolerable for ETA.
- **Geo-sharding granularity.** Smaller zones = more dispatchers = higher throughput, but more cross-zone-edge cases. Bigger zones = simpler, but each dispatcher is bottlenecked.
- **Server-assigned vs user-picked.** Server-assigned is simpler tech and same UX. User-picked is more complex but gives the user a sense of control. Liu picks server-assigned and frames the trade-off explicitly.
- **Cache durability.** No backup is fine for live locations; would not be fine for stored ride history.

## Sources

- [Liu Ch 6.01: Ridesharing Service](software/system-design-interview/books/system-design-interview-fundamentals/ch06_01_ridesharing_service.md)
