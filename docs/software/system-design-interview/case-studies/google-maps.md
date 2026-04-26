# Google Maps

> Vol 2 only — neither Liu nor Xu Vol 1 covers this. The big move is **pre-generating every map tile and serving from a CDN** — dynamic tile generation is too costly per request and uncacheable. Pathfinding splits the world into hierarchical routing tiles loaded on demand. Geohash mechanics live in [Geospatial Indexing](fundamentals/geospatial-indexing.md); this page is the maps-specific design.

## Table of Contents

- [1. Requirements](#1-requirements)
- [2. Map Fundamentals](#2-map-fundamentals)
- [3. Routing Tiles](#3-routing-tiles)
- [4. Estimation](#4-estimation)
- [5. High-Level Services](#5-high-level-services)
- [6. Map Rendering Deep Dive](#6-map-rendering-deep-dive)
- [7. Navigation Service Deep Dive](#7-navigation-service-deep-dive)
- [8. Adaptive ETA and Rerouting](#8-adaptive-eta-and-rerouting)
- [Sources](#sources)

## 1. Requirements

Three features for mobile: user location update, navigation + ETA, map rendering. Out of scope: business places, photos, multi-stop routes.

- 1B DAU; road data is TBs of raw input from external sources.
- Non-functional: accuracy (no wrong directions), smooth client-side rendering, minimal mobile data and battery, standard availability/scalability.

## 2. Map Fundamentals

- **Lat/long** is the unique reference; **map projection** flattens the 3D globe to a 2D plane (Google Maps uses **Web Mercator**).
- **Geocoding** converts an address to (lat, long); reverse geocoding inverts.
- **Map tiling** — instead of one giant image, the world is broken into 256×256 pixel tiles per zoom level; clients fetch only the tiles needed for the current viewport and stitch them together like a mosaic.
- **Geohash for tiling** — recursively split the flattened surface into 4 sub-grids labeled 0–3 until grids hit a target size; used for both map tiles and routing tiles. See [Geospatial Indexing](fundamentals/geospatial-indexing.md).

## 3. Routing Tiles

A **routing tile** is a small graph (intersections = nodes, roads = edges) covering a geographical grid. Binary file of road data, distinct from PNG map tiles. Each tile holds references to neighboring tiles.

**Why tiling is required** — Dijkstra/A* pathfinding is sensitive to graph size; the whole world won't fit in memory or run efficiently. Tiles are loaded on demand during traversal.

**Hierarchical routing tiles** — three resolution levels:

| Level | Contents |
|---|---|
| Small | Local roads |
| Mid-size | Arterial roads between districts |
| Large | Major highways between cities |

Inter-level edges let the algorithm "enter" a bigger tile (e.g., a freeway entrance from a local street). Long routes traverse the highway layer; short routes stay local.

## 4. Estimation

| Quantity | Value |
|---|---|
| Map tiles at zoom 21 | ~4.4 trillion 256×256 tiles × 100 KB ≈ 440 PB |
| After ocean/desert compression (~90%) | ~50 PB at top zoom |
| Sum across 22 zoom levels (each level = ¼ tiles) | 50 + 50/4 + 50/16 + … ≈ **~100 PB** |
| Navigation QPS | 1B × 5 sessions × 35 min/wk → ~7,200 avg, ~36,000 peak |
| Location update QPS | 1s cadence = 3M; **batched to 15s = 200K avg, 1M peak** |
| Mobile data per session | 256-pixel tiles at 100 KB; 25 tiles per 1 km² → **1.25 MB/min** at 30 km/h |
| CDN load | 5B nav-min/day × 1.25 MB ≈ 62,500 MB/s; **200 POPs** each serve ~few hundred MB/s |

## 5. High-Level Services

Three top-level services:

- **Location service** — records user GPS updates. Clients buffer locally (every 1s) and POST batches every ~15s via `POST /v1/locations` over HTTP keep-alive (reduces traffic + battery). Stored in Cassandra, also published to Kafka so downstream consumers (live traffic, road detection, personalization) can tap the stream. See [Async, Batch, Stream](fundamentals/async-batch-stream.md).
- **Navigation service** — `GET /v1/nav?origin=...&destination=...` returns distance, duration, polyline, geocoded waypoints, travel mode, HTML turn instructions.
- **Map rendering** — pre-generate static tiles, serve via **CDN**. Dynamic generation per request is too costly and uncacheable. See [CDN](fundamentals/cdn.md).

**Tile URL via geohash** — each tile has a unique geohash; URL `https://cdn.map-provider.com/tiles/<geohash>.png`. Computing the geohash from (lat, long) + zoom is cheap and can run **on the client**.

**Client-side vs server-side geohash mapping** — a hardcoded client-side calculation requires shipping new mobile builds if the encoding changes; alternative is a thin **map tile service** that returns 9 tile URLs (current + 8 neighbors), trading a hop for operational flexibility.

## 6. Map Rendering Deep Dive

- **21 zoom levels**. Level 0 = entire world in one 256×256 tile; each increment doubles tiles in both axes (4× total pixels).
- **Vector tiles via WebGL** — sending vector paths/polygons instead of rasterized PNGs compresses far better and yields smooth zooming (no pixelation between levels) since the client scales each element independently.

**Data model** — four data types:

| Data | Storage | Reason |
|---|---|---|
| Routing tiles | Object storage (S3) | Binary adjacency lists organized by geohash; no DB features needed |
| User location | Cassandra | 1M peak QPS write demands write-optimized horizontal store; partition `user_id`, cluster `timestamp` for latest-position lookups |
| Geocoding DB | Redis | Read-heavy, rare writes, KV pattern |
| Precomputed map tiles | S3 + CDN | Massive static asset corpus |

## 7. Navigation Service Deep Dive

- **Geocoding service** — resolves origin/destination strings to (lat, long) before downstream routing.
- **Route planner** — orchestrates: shortest-path → ETA → ranker.
- **Shortest-path service** — runs A*-style traversal over routing tiles in object storage; converts (lat, long) → geohash to load start/end tiles, hydrates neighbors (or jumps to coarser hierarchical tiles) on demand. Routes are cacheable since the road graph rarely changes; ignores live traffic.
- **ETA service** — ML over current and historical traffic predicts travel time, including 10–20 min projections.
- **Ranker service** — applies user filters (avoid tolls, avoid freeways) and orders candidate routes by ETA, returning top-k.
- **Updater services** — Kafka consumers: **routing tile processing service** rebuilds tiles when new/closed roads are detected; **traffic update service** writes live traffic from location streams into the live traffic DB.

## 8. Adaptive ETA and Rerouting

When traffic changes mid-trip, the server must figure out which active users are affected without scanning every route.

**Hierarchical routing-tile index** — for each active user, store the current tile plus its parents at each higher level (`s_1, super(s_1), super(super(s_1))`). To check if user is affected by a change in tile X, just test whether X falls inside the user's top-level container. Quickly filters out unaffected users.

**Recovery when traffic clears** — keep alternative routes per user, recompute ETAs periodically, notify when a faster route appears.

**Delivery protocol for live updates:**

| Protocol | Verdict |
|---|---|
| Mobile push | Rejected — 4,096-byte iOS payload limit, no web support |
| Long polling | Rejected — heavier server footprint than WebSocket |
| SSE | Viable but unidirectional |
| **WebSocket** | **Chosen** — bi-directional, low footprint, supports last-mile features |

See [Real-Time Communication](fundamentals/real-time-communication.md).

## Sources

- [Vol 2 Ch 3: Google Maps](software/system-design-interview/books/system-design-interview-vol2/ch03_google_maps.md)
