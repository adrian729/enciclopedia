# Ch 1: Proximity Service

## Table of Contents

- [1. Problem and Scope](#1-problem-and-scope)
- [2. High-Level Design](#2-high-level-design)
- [3. Geospatial Indexing Options](#3-geospatial-indexing-options)
  - [3.1. Geohash Details](#31-geohash-details)
  - [3.2. Quadtree Details](#32-quadtree-details)
  - [3.3. Geohash vs Quadtree](#33-geohash-vs-quadtree)
- [4. Scaling and Caching](#4-scaling-and-caching)
- [5. End-to-End Flow](#5-end-to-end-flow)

## 1. Problem and Scope

- **Proximity service** — backend that finds nearby places (restaurants, gas stations) within a user-supplied radius and location, powering features like Yelp's nearby search.
- **Functional requirements** — return businesses by (lat, long, radius); allow owners to add/update/delete businesses (effective next day, not real-time); allow customers to view business details.
- **Non-functional requirements** — low latency, high availability/scalability, and data privacy (GDPR, CCPA) since location is sensitive.
- **Scale assumptions** — 100M DAU, 200M businesses, 5 searches/user/day → ~5,000 search QPS (using `10^5` seconds/day shorthand throughout the book).
- **Allowed radii** — fixed UI options of 0.5km, 1km, 2km, 5km, and 20km (max).

## 2. High-Level Design

- **Two services behind a load balancer** — a stateless **Location-Based Service (LBS)** that handles read-heavy nearby-search queries, and a **Business Service** that handles CRUD on business records plus detail reads.
- **API surface** — `GET /v1/search/nearby` for proximity queries; standard REST `GET/POST/PUT/DELETE /v1/businesses/{:id}` for business CRUD and detail fetch.
- **Database choice** — relational store (e.g., MySQL) suits the read-heavy, low-write workload; primary-secondary replication tolerates slight read staleness because business data isn't real-time.
- **Two key tables** — `business` table (full business info, primary key `business_id`) and a separate **geo index table** for spatial lookup.

## 3. Geospatial Indexing Options

- **Why a 1D mapping is needed** — naive 2D `WHERE lat BETWEEN ... AND long BETWEEN ...` requires intersecting two huge index scans; geospatial indexing maps 2D points into 1D so a single B-tree index can answer range queries.
- **Two families of geo indexes** — **hash-based** (even grid, geohash, cartesian tiers) and **tree-based** (quadtree, Google S2, R-tree); all share the idea of dividing the map into smaller areas to build a searchable index.
- **Even grid — rejected** — fixed-size grids leave deserts and oceans empty while downtown New York is overloaded; uneven density makes this approach impractical.

### 3.1. Geohash Details

- **Geohash** — encodes (lat, long) into a base-32 string by recursively splitting the planet into four quadrants, alternating longitude and latitude bits at each level (12 precision levels).
- **Precision-to-grid mapping** — length 4 ≈ 39.1km × 19.5km, length 5 ≈ 4.9km × 4.9km, length 6 ≈ 1.2km × 609.4m; the 0.5–20km radii map to geohash lengths 4–6.
- **Shared-prefix property** — longer shared prefixes mean closer geohashes; e.g., grids near Google HQ (`9q9hvu`) share the prefix `9q` with Facebook HQ (`9q9jhr`).
- **Boundary issue 1** — close locations on opposite sides of the equator or prime meridian can have *no* shared prefix; e.g., La Roche-Chalais (`u000`) and Pomerol (`ezzz`) are 30km apart in France but share nothing.
- **Boundary issue 2** — two points can share a long prefix yet sit in different grids; mitigation: also fetch the eight neighboring geohashes (computable in constant time).
- **Not enough results** — drop the last digit of the geohash to enlarge the grid and re-query; repeat until enough businesses are returned.

### 3.2. Quadtree Details

- **Quadtree** — in-memory tree (not a database) built on each LBS server at startup that recursively subdivides the world into four quadrants until each leaf holds at most ~100 businesses (threshold is arbitrary).
- **Memory footprint** — leaf node = 832 bytes (32-byte bounding box + 100 × 8-byte business IDs); internal node = 64 bytes; with 200M businesses → ~2M leaves and ~0.67M internals → ~1.71 GB total, fits on one server.
- **Build time** — `(n/100) log(n/100)`, on the order of minutes for 200M businesses; the server cannot serve traffic while building.
- **Operational implications** — long warm-up forces incremental rollouts (rolling deploys or blue/green) so the cluster doesn't go offline; nightly rebuilds work given the next-day update policy but invalidate many cache keys at once.
- **Search algorithm** — traverse from root to the leaf containing the user's location; if that leaf has fewer than the desired number of results, pull from neighboring leaves.

### 3.3. Geohash vs Quadtree

| Dimension | Geohash | Quadtree |
|---|---|---|
| Implementation | Easier — no tree to build | Harder — must build and maintain a tree |
| Radius search | Native | Native |
| K-nearest search | Not native | Native (good fit for "k nearest gas stations") |
| Grid size | Fixed at a chosen precision | Dynamic — granular in dense areas, coarse in sparse |
| Index updates | Simple: insert/delete a row keyed by `(geohash, business_id)` | `O(log n)` traversal, requires locking under multi-threading; rebalancing is complex |
| Used by | Bing Maps, Redis, MongoDB, Lyft, Elasticsearch | Yext, Elasticsearch |

- **S2 (Google)** — maps a sphere to 1D using the Hilbert curve (close points stay close in 1D); used by Google Maps and Tinder; strong for **geofencing** via its Region Cover algorithm with configurable min/max levels and max cells. Recommended in interviews to discuss **geohash or quadtree** — S2 internals are too complex to explain clearly under time pressure.

## 4. Scaling and Caching

- **Business table sharding** — shard by `business_id` for even load; simple to operate.
- **Geo index table sharding — usually unnecessary** — the whole index (~1.71 GB) fits in one server's working set; prefer **read replicas** for read scaling. Don't reflexively shard.
- **Geo index row layout — prefer one row per business** — a compound key `(geohash, business_id)` makes inserts/deletes simple and avoids row-level locking; the alternative (a JSON array of business IDs per geohash row) requires array scans, locks, and duplicate checks.
- **Cache key choice** — raw lat/long is a poor key (GPS jitter, tiny user movement), but **geohash naturally clusters nearby points to the same key**.
- **Two cache types in Redis** — `geohash → list of business IDs` (precomputed at lengths 4, 5, 6 = ~5 GB total for 200M businesses × 3 precisions × 8 bytes) and `business_id → business object` for detail rendering.
- **Cache deployment** — replicate the same ~5 GB Redis dataset globally for low cross-continent latency; nightly job updates caches in line with the next-day business-update SLA.
- **Multi-region / availability zones** — serve users from the geographically nearest data center, balance load across populous regions (e.g., separate regions for Japan/Korea), and use DNS routing to keep traffic in-country where privacy laws require local data residency.
- **Filtering by time or business type** — filter post-fetch in the application layer; grid sizes are small enough that the candidate set is manageable.

## 5. End-to-End Flow

1. Client sends (lat, long, radius) to the load balancer, which routes to LBS.
2. LBS maps radius → geohash length (e.g., 500m → length 6) and computes the user's geohash plus the eight neighbors.
3. LBS queries the **Geohash** Redis cache in parallel for each of the nine geohashes to collect candidate business IDs.
4. LBS fetches full objects from the **Business info** Redis cache, ranks by distance, and returns the result.
5. Business CRUD goes through the separate Business Service, which writes through to the database and lets the nightly cache-update job propagate changes.
