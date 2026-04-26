# Proximity Service (Yelp Nearby Search)

> Vol 2 only — neither Liu nor Xu Vol 1 covers this. The interesting move is using the geohash itself as the cache key (raw lat/long jitter is too noisy) and **not** sharding a 1.71 GB geo index that fits comfortably on one server. Geohash and quadtree mechanics live in [Geospatial Indexing](fundamentals/geospatial-indexing.md); this page is the workload-specific design.

## Table of Contents

- [1. Requirements](#1-requirements)
- [2. Estimation](#2-estimation)
- [3. API](#3-api)
- [4. Indexing Choice](#4-indexing-choice)
- [5. High-Level Design](#5-high-level-design)
- [6. Caching: Geohash as the Key](#6-caching-geohash-as-the-key)
- [7. Scaling — Don't Reflexively Shard](#7-scaling--dont-reflexively-shard)
- [8. End-to-End Flow](#8-end-to-end-flow)
- [Sources](#sources)

## 1. Requirements

- Return businesses within a user-supplied (lat, long, radius). Powers Yelp's "nearby" feature.
- Owners can add/update/delete businesses; updates take effect next day, not real-time.
- View business details by ID.
- Non-functional: low latency, high availability, GDPR/CCPA compliance because location is sensitive.

## 2. Estimation

- 100M DAU × 5 searches/user/day → ~5,000 search QPS (using `10⁵` seconds/day).
- 200M businesses worldwide.
- Allowed radii are fixed UI options: 0.5 km, 1 km, 2 km, 5 km, 20 km.

## 3. API

```
GET /v1/search/nearby?lat=...&long=...&radius=...
GET /v1/businesses/{id}
POST/PUT/DELETE /v1/businesses/{id}      ← owner-side CRUD
```

## 4. Indexing Choice

Two services behind a load balancer: a stateless **Location-Based Service (LBS)** for read-heavy nearby search, and a **Business Service** for CRUD + detail.

The geo index is a separate table from the `business` table. The choice between geohash and quadtree is covered in [Geospatial Indexing](fundamentals/geospatial-indexing.md). For Yelp-style proximity, **geohash wins** — it's read-heavy, business locations are static, and a row keyed `(geohash, business_id)` keeps inserts/deletes simple. Each radius (0.5–20 km) maps to a fixed geohash length (4–6).

## 5. High-Level Design

```
Client
  ↓
Load Balancer
  ↓                    ↓
LBS (stateless)        Business Service
  ↓                    ↓
Redis cache       MySQL (primary + replicas)
  ↓                    ↑
MySQL geo_index ────────
  (read replicas)
```

**Why MySQL and not NoSQL?** The workload is read-heavy with low write volume (next-day update SLA). Primary-secondary replication tolerates slight read staleness because business data isn't real-time.

**Geo index row layout — one row per business**, compound key `(geohash, business_id)`. The alternative (a JSON array of business IDs per geohash row) requires array scans, locks, and duplicate checks. The flat layout supports cheap inserts/deletes.

## 6. Caching: Geohash as the Key

Raw lat/long is a **poor cache key** — GPS jitter and sub-meter movement bust the cache constantly. Geohash naturally clusters nearby points to the same key.

Two Redis caches:

| Cache | Key | Value | Size at scale |
|---|---|---|---|
| Geohash → business IDs | `geohash` (precomputed at lengths 4, 5, 6) | List of business IDs | ~5 GB total (200M businesses × 3 precisions × 8 bytes) |
| Business detail | `business_id` | Business object for rendering | Smaller |

Both caches are **replicated globally** for low cross-continent latency. A nightly job updates them in line with the next-day update SLA — no need for write-through.

## 7. Scaling — Don't Reflexively Shard

The full geo index fits in roughly **1.71 GB** of working set (200M businesses × tens of bytes per row in the relevant index, or fully resident in a quadtree as detailed in [Geospatial Indexing](fundamentals/geospatial-indexing.md)). One server handles it. The right move is **read replicas**, not sharding.

**Business table sharding** is acceptable when needed — shard by `business_id` for even load.

**Multi-region deployment** serves users from the geographically nearest data center, balances load across populous regions (e.g., separate regions for Japan/Korea), and uses **DNS routing** to keep traffic in-country where privacy laws require local data residency. See [Networking & DNS](fundamentals/networking-and-dns.md).

## 8. End-to-End Flow

1. Client sends `(lat, long, radius)` to the load balancer; routed to LBS.
2. LBS maps the radius → geohash length (e.g., 500 m → length 6) and computes the user's geohash + the eight neighbors.
3. LBS queries the **geohash → business IDs** Redis cache in parallel for each of the nine geohashes.
4. LBS fetches full objects from the **business detail** cache, ranks by distance, applies any post-fetch filters (time of day, business type), and returns.
5. Business CRUD goes through Business Service → MySQL primary → replicates to secondaries; the nightly cache-update job propagates changes to Redis.

The **eight-neighbor fetch** handles the geohash boundary issue covered in [Geospatial Indexing](fundamentals/geospatial-indexing.md). Filtering is **post-fetch in the application layer** — grid sizes are small enough that the candidate set is manageable.

## Sources

- [Vol 2 Ch 1: Proximity Service](software/system-design-interview/books/system-design-interview-vol2/ch01_proximity_service.md)
