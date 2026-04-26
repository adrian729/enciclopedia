# Geospatial Indexing

> Vol 2 only — neither Liu nor Xu Vol 1 covers spatial indexing as its own topic. Three Vol 2 chapters share the same primitive: [Proximity Service](case-studies/proximity-service.md) (static businesses), [Nearby Friends](case-studies/nearby-friends.md) (moving users via per-grid pub/sub channels), and [Google Maps](case-studies/google-maps.md) (tile URLs and routing tiles). The interesting move is mapping 2D coordinates onto a 1D key so a single B-tree index can answer "what's near me" with a range scan.

## Table of Contents

- [1. Why 2D → 1D](#1-why-2d--1d)
- [2. Geohash](#2-geohash)
  - [2.1. Encoding](#21-encoding)
  - [2.2. Boundary Issues and the Eight-Neighbor Fetch](#22-boundary-issues-and-the-eight-neighbor-fetch)
  - [2.3. Length-to-Grid Reference Table](#23-length-to-grid-reference-table)
- [3. Quadtree](#3-quadtree)
- [4. Google S2 (Brief)](#4-google-s2-brief)
- [5. Decision Tree](#5-decision-tree)
- [Sources](#sources)

## 1. Why 2D → 1D

A naive radius query is a 2D range:

```sql
WHERE lat  BETWEEN ? AND ?
  AND long BETWEEN ? AND ?
```

The database has separate B-tree indexes on `lat` and `long`; the query intersects two huge ranges and the working set explodes. Mapping each (lat, long) point to a single 1D key collapses the query to one index scan. Every spatial index in this page does that mapping; they differ in *how*.

Two families:

- **Hash-based** — even grid, **geohash**, cartesian tiers.
- **Tree-based** — **quadtree**, Google S2, R-tree.

The naive even grid is rejected immediately: fixed cells leave deserts and oceans empty while downtown New York overflows. Density is the killer.

## 2. Geohash

### 2.1. Encoding

Geohash recursively splits the planet into four quadrants, alternating longitude and latitude bits at each level. The bit stream is base-32 encoded so each character represents 5 bits = one quadrant level + a refinement.

The **shared-prefix property** is the whole reason it works: longer shared prefixes mean closer points. Google HQ (`9q9hvu`) and Facebook HQ (`9q9jhr`) share prefix `9q`, so both sit in the same large grid; their refinements diverge only at the fourth character.

A radius query maps a chosen geohash length (= grid size) to a `LIKE '<prefix>%'` lookup, or — better — an exact-equality lookup on `(geohash, business_id)` rows:

```
SELECT business_id FROM geo_index WHERE geohash = '9q9hv';
```

If the result set is too small, **drop the last character** of the geohash to enlarge the grid and re-query. Repeat until enough candidates are returned.

### 2.2. Boundary Issues and the Eight-Neighbor Fetch

Two failure modes break the shared-prefix guarantee:

- **Equator/meridian gap** — close locations on opposite sides of the prime meridian or equator can have *no* shared prefix at all. La Roche-Chalais (`u000`) and Pomerol (`ezzz`) sit 30 km apart in France and share zero characters.
- **Neighbor-grid gap** — two points can share a long prefix and yet sit in different grids near a border. The user is in one grid; the closest restaurant is in the next one over.

Both are solved by the **eight-neighbor fetch**: in addition to the user's geohash, compute the eight neighboring geohashes (constant-time arithmetic on the bit string) and union the results. Nine queries instead of one, but each is a cheap index lookup.

### 2.3. Length-to-Grid Reference Table

| Geohash length | Grid size       | Use for radius |
|---|---|---|
| 4 | ~39.1 km × 19.5 km | 20 km |
| 5 | ~4.9 km × 4.9 km   | 2 km, 5 km |
| 6 | ~1.2 km × 609 m    | 0.5 km, 1 km |

The Vol 2 proximity service exposes fixed UI options (0.5, 1, 2, 5, 20 km) so each radius maps deterministically to a geohash length. Pre-compute the index at lengths 4, 5, and 6 and the lookup is always a single equality scan plus eight neighbors.

## 3. Quadtree

A quadtree is an in-memory tree (not a database) that recursively subdivides the world into four quadrants until each leaf holds at most ~100 points. The threshold is arbitrary — pick whatever makes the leaf size match the radius queries you plan to answer.

Memory math from the proximity service example:

- Leaf node = 832 bytes (32-byte bounding box + 100 × 8-byte business IDs).
- Internal node = 64 bytes.
- 200 M businesses → ~2 M leaves and ~0.67 M internals → **~1.71 GB total**, fits on one server.

Build time is `(n/100) log(n/100)`, on the order of minutes for 200 M points. The server cannot serve traffic while building, so deployment is an **incremental rollout** (rolling deploy or blue/green) and rebuilds happen during a daily window.

The search algorithm walks from root to the leaf containing the user's point; if that leaf is sparse, pull from neighboring leaves until k results accumulate. Native k-nearest support is the quadtree's headline advantage over geohash.

The cost: updates require `O(log n)` traversal, locking under multi-threading, and rebalancing — far more complex than inserting a row keyed by `(geohash, business_id)`.

## 4. Google S2 (Brief)

S2 maps the sphere to 1D using the **Hilbert curve** (close points stay close in 1D). It's used by Google Maps and Tinder and is the strongest fit for **geofencing** thanks to its Region Cover algorithm with configurable min/max levels and a max-cell budget.

In an interview, recommend candidates default to **geohash or quadtree** — S2 internals are too complex to explain clearly under time pressure, and the interviewer can't grade what they can't follow.

## 5. Decision Tree

| Workload | Pick |
|---|---|
| Read-heavy, static or near-static (Yelp-style nearby search) | **Geohash** + read replicas; index fits one server, don't reflexively shard. |
| K-nearest queries with dynamic density (gas stations, ATMs) | **Quadtree** — adapts grid size to density and supports k-nearest natively. |
| Tile URLs / routing tiles (Google Maps) | **Geohash** — `https://cdn.../tiles/<geohash>.png`. Cheap to compute client-side. |
| Per-grid pub/sub fan-out ("nearby random person") | **Geohash** — one channel per grid; subscribe to current + 8 neighbors. |
| Geofencing with millions of polygons | **S2** Region Cover. |

The shared trick across all of these: use the geohash itself as the **cache key**. Raw lat/long is a poor key (GPS jitter, sub-meter movement) but small location changes naturally map to the same geohash, so cache hit rates stay high. See [Caching](fundamentals/caching.md).

## Sources

- [Vol 2 Ch 1: Proximity Service](software/system-design-interview/books/system-design-interview-vol2/ch01_proximity_service.md)
- [Vol 2 Ch 2: Nearby Friends](software/system-design-interview/books/system-design-interview-vol2/ch02_nearby_friends.md)
- [Vol 2 Ch 3: Google Maps](software/system-design-interview/books/system-design-interview-vol2/ch03_google_maps.md)
