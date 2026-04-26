# Ch 3: Google Maps

## Table of Contents

- [1. Problem and Scope](#1-problem-and-scope)
- [2. Map Fundamentals](#2-map-fundamentals)
- [3. Routing Tiles](#3-routing-tiles)
- [4. Back-of-the-Envelope Estimates](#4-back-of-the-envelope-estimates)
- [5. High-Level Services](#5-high-level-services)
- [6. Map Rendering Deep Dive](#6-map-rendering-deep-dive)
- [7. Data Model](#7-data-model)
- [8. Navigation Service Deep Dive](#8-navigation-service-deep-dive)
- [9. Adaptive ETA and Rerouting](#9-adaptive-eta-and-rerouting)

## 1. Problem and Scope

- **Scope** — design a simplified Google Maps for mobile with three features: user location update, navigation + ETA, and map rendering. Business places, photos, and multi-stop routes are out of scope.
- **Scale** — 1 billion DAU; road data is TBs of raw input from external sources; 99% world coverage and ~25M daily map updates in real Google Maps as reference.
- **Non-functional requirements** — accuracy (no wrong directions), smooth client-side rendering, minimal mobile data and battery usage, and standard availability/scalability.

## 2. Map Fundamentals

- **Lat/long positioning** — latitude is north-south distance, longitude is east-west distance on the rotating sphere; the unique reference points for every location.
- **Map projection** — the process of flattening the 3D globe to a 2D plane; every projection distorts geometry. Google Maps uses **Web Mercator**, a modified Mercator projection.
- **Geocoding** — converting an address (e.g., "1600 Amphitheatre Parkway, Mountain View, CA") to a (lat, long) pair; **reverse geocoding** is the inverse. One implementation is **interpolation** over GIS street-network data.
- **Geohashing for tiling** — recursively split the flattened surface into 4 sub-grids labeled 0–3, repeating until grids hit a target size; used here both for map tiles and routing tiles. Initial split: 20,000km × 10,000km → four 10,000km × 5,000km cells.
- **Map tiling** — instead of one giant image, the world is broken into 256×256 pixel tiles per zoom level; clients fetch only the tiles needed for the current viewport and stitch them together like a mosaic.

## 3. Routing Tiles

- **Routing tile** — a small graph (intersections = nodes, roads = edges) covering a geographical grid; binary file of road data, distinct from PNG map tiles. Each tile holds references to the neighboring tiles its roads connect to.
- **Why tiling is required** — pathfinding (Dijkstra, A*) is sensitive to graph size; the whole world as one graph won't fit in memory or run efficiently. Tiles are loaded on demand during traversal.
- **Hierarchical routing tiles** — three resolution levels: small tiles with local roads, mid-size tiles with arterial roads between districts, large tiles with only major highways between cities. Inter-level edges allow the algorithm to "enter" a bigger tile (e.g., a freeway entrance from a local street).

## 4. Back-of-the-Envelope Estimates

- **Map tile storage** — at zoom level 21 there are ~4.4 trillion 256×256 tiles at ~100KB each = 440 PB. ~90% of the world (oceans, deserts) compresses heavily, so the highest level drops to ~50 PB. Summing all 22 zoom levels (each level has 4× fewer tiles): 50 + 50/4 + 50/16 + … ≈ 67 PB; rounded estimate **~100 PB**.
- **Navigation QPS** — each user averages 5 navigation sessions totaling 35 min/week → 1B × 35 min/week = 35B nav-min/week ≈ **5B nav-minutes/day**; navigation QPS = 1B × 5 / 7 / 10⁵ ≈ **7,200**, peak (5×) ≈ **36,000**.
- **Location update QPS** — naive (every 1s) = 3M QPS; batching to every 15s drops it to **200,000** average, **1M** peak.
- **Mobile data per session** — at 30 km/h with 200m × 200m tiles (256px, 100KB), a 1km × 1km area = 25 tiles = 2.5MB; usage = 75MB/hour or **1.25 MB/min**.
- **CDN load** — 5B nav-minutes/day × 1.25MB ≈ 6.25 billion MB/day = 62,500 MB/s; with **200 POPs** each serves only a few hundred MB/s.

## 5. High-Level Services

- **Three top-level services** — **Location service** (records user GPS updates), **Navigation service** (computes routes + ETA), **Map rendering** (serves tile imagery to clients).
- **Location service** — clients buffer GPS samples locally (every 1s) and POST batches every ~15s via `POST /v1/locations` over HTTP keep-alive; reduces traffic and battery use. Stored in a write-optimized DB (Cassandra) and also published to Kafka so downstream consumers (live traffic, road-detection, personalization) can tap the stream.
- **Navigation API** — `GET /v1/nav?origin=...&destination=...` returns distance, duration, polyline, geocoded waypoints, travel mode, and HTML turn instructions (matches Google's public API shape).
- **Map rendering — pre-generate, don't build on the fly** — dynamic tile generation is too costly per request and uncacheable; pre-generated static tiles served via **CDN** are scalable and highly cacheable.
- **Tile URL via geohash** — each tile has a unique geohash; URL `https://cdn.map-provider.com/tiles/<geohash>.png`. Computing the geohash from (lat, long) + zoom is cheap and can run on the client.
- **Client-side vs server-side geohash mapping** — a hardcoded client-side calculation requires shipping new mobile builds if the encoding changes; alternative is a thin **map tile service** that returns 9 tile URLs (current + 8 neighbors), trading a hop for operational flexibility.

## 6. Map Rendering Deep Dive

- **Zoom levels** — Google Maps uses 21 zoom levels; level 0 = entire world in one 256×256 tile, each increment doubles tiles in both axes (4× total pixels). The chosen level matches the client's viewport so detail and bandwidth stay in balance.
- **Vector tiles via WebGL** — sending vector paths/polygons instead of rasterized PNGs compresses far better and yields smooth zooming (no pixelation between levels) since the client scales each element independently.

## 7. Data Model

- **Four data types** — routing tiles, user location data, geocoding data, precomputed map tile images.
- **Routing tiles → object storage (S3)** — adjacency lists serialized as binary files, organized by geohash for fast lookup; aggressively cached on the routing service. A database is overkill since no DB features are needed.
- **User location → Cassandra** — 1M writes/sec demands write-optimized, horizontally scalable storage. Per CAP, prioritize availability + partition tolerance over consistency since location is constantly changing. Partition key = `user_id`, clustering key = `timestamp`, so latest position lookups and per-user time ranges are efficient.
- **Geocoding DB → Redis** — places → (lat, long); read-heavy with rare writes makes a KV store ideal.
- **Map tiles → S3 + CDN** — precomputed at every zoom level, served from POPs.

## 8. Navigation Service Deep Dive

- **Geocoding service** — resolves origin/destination strings to (lat, long) via the geocoding DB before downstream routing.
- **Route planner** — orchestrates the chain: shortest-path → ETA → ranker.
- **Shortest-path service** — runs A*-style traversal over routing tiles in object storage; converts (lat, long) → geohash to load start/end tiles, then hydrates neighbors (or jumps to coarser hierarchical tiles) on demand. Routes are cacheable since the road graph rarely changes; ignores live traffic.
- **ETA service** — uses ML over current and historical traffic to predict travel time, including projections of how traffic will look 10–20 minutes ahead.
- **Ranker service** — applies user filters (avoid tolls, avoid freeways) and orders the candidate routes by ETA, returning top-k.
- **Updater services** — Kafka consumers that keep databases fresh: the **routing tile processing service** rebuilds tiles when new/closed roads are detected, and the **traffic update service** writes live traffic from location streams into the live traffic DB.

## 9. Adaptive ETA and Rerouting

- **Problem** — when traffic changes mid-trip, the server must figure out which active users are affected without scanning every route. Naive scan over (n users × m tiles per route) is O(n·m).
- **Hierarchical routing-tile index** — for each active user store the current tile plus its parent tiles at each higher level (`s_1, super(s_1), super(super(s_1))`). To check if user is affected by a change in tile X, just test whether X falls inside the user's top-level container. Quickly filters out unaffected users.
- **Recovery when traffic clears** — keep alternative routes for each user, recompute ETAs periodically, notify when a faster route appears.

| Delivery protocol | Verdict |
|---|---|
| Mobile push | Rejected — 4,096-byte iOS payload limit, no web support |
| Long polling | Rejected — heavier server footprint than WebSocket |
| SSE | Viable but unidirectional |
| **WebSocket** | **Chosen** — bi-directional, low footprint, supports last-mile features |
