# Nearby Friends

> Vol 2 only — neither Liu nor Xu Vol 1 covers this. The headline insight is that this looks like a [Proximity Service](case-studies/proximity-service.md) but the workload is fundamentally different: businesses are static, **friends move**, so the problem is real-time message-passing rather than spatial search. The pub/sub layer is treated as a stateful cluster — even though messages aren't persisted, the **subscriber list is state**.

## Table of Contents

- [1. Requirements](#1-requirements)
- [2. Estimation](#2-estimation)
- [3. Architecture](#3-architecture)
- [4. Location Update Flow](#4-location-update-flow)
- [5. Scaling the Pub/Sub Layer](#5-scaling-the-pubsub-layer)
- [6. Pub/Sub as a Stateful Cluster](#6-pubsub-as-a-stateful-cluster)
- [7. Operational Concerns](#7-operational-concerns)
- [8. The "Nearby Random Person" Extension](#8-the-nearby-random-person-extension)
- [Sources](#sources)

## 1. Requirements

- Show the list of friends currently within a radius (default 5 miles), updated every few seconds.
- Opt-in only; inactive friends (>10 min idle) drop off.
- Straight-line distance is fine; full geocoded routing isn't required.
- Eventual consistency — a few seconds of staleness is acceptable; occasional drops are tolerated.

## 2. Estimation

- 1B total users; 100M DAU on this feature; 10% concurrent → 10M online.
- Average 400 friends/user.
- **30-second location refresh**, chosen because 3–4 mph walking speed makes finer cadence pointless.
- Location update QPS = 10M / 30 ≈ **334K updates/sec**.
- With ~10% of friends online and nearby, the backend forwards ~13M location messages/sec downstream.

## 3. Architecture

Two server tiers behind a load balancer:

- **Stateless RESTful API servers** for friend management and profile updates.
- **Stateful WebSocket servers** for the persistent bidirectional location stream. See [Real-Time Communication](fundamentals/real-time-communication.md) for why WebSocket beats long polling and SSE here.

Each client maintains **one long-lived WebSocket** carrying both its outgoing location updates and incoming friends' updates.

Three data stores:

- **Redis location cache** — `user_id → {lat, long, timestamp}` with a **TTL** that auto-expires inactive users; durability not needed because a cold cache simply refills as updates stream in.
- **User database** — profiles + friendship graph; sharded by user ID.
- **Location history database** — Cassandra for ML and other downstream uses (heavy writes, horizontal scale).

The fan-out trick: **Redis Pub/Sub**. Every user has a personal channel; their location updates publish to it; each friend's WebSocket connection handler subscribes. Channels are extremely cheap to create — millions per server — and idle channels consume **no CPU** after creation.

## 4. Location Update Flow

1. Mobile client sends new location over its WebSocket → load balancer → user's WebSocket server.
2. Server runs three steps in parallel: persist to the location history DB, update the Redis location cache (refreshing TTL) plus the connection handler's local variable, and publish to the user's personal Redis Pub/Sub channel.
3. Pub/Sub broadcasts to all subscribers — i.e., the WebSocket handlers of online friends, which may live on different WebSocket servers.
4. Each receiving handler computes the distance to its subscriber; if within the search radius, it pushes the new location down the subscriber's WebSocket; otherwise the update is dropped silently.

**Client initialization**: on app startup, the client opens a WebSocket and sends its location. The server (a) updates the cache, (b) loads all friends from the user DB, (c) batch-fetches friend locations from the cache, (d) returns those within radius, (e) **subscribes to every friend's pub/sub channel — active or not**, because creating idle channels is essentially free, simplifying the design at the cost of slightly more memory.

## 5. Scaling the Pub/Sub Layer

**Bottleneck is CPU, not memory.** Back-of-envelope:

- Memory: 100M users × 100 active friends × 20 bytes ≈ **200 GB** → ~2 servers' worth.
- CPU: pushing 13M messages/sec at a conservative 100K pushes/server-sec needs **~130 Redis servers**.

The fan-out load dwarfs the storage need.

Channels are sharded across the pub/sub server cluster using a **hash ring** keyed on the publishing user's ID; the ring is stored in a service-discovery component (etcd or ZooKeeper). See [Sharding & Consistent Hashing](fundamentals/sharding-and-consistent-hashing.md) and [Service Discovery & Load Balancing](fundamentals/service-discovery-and-load-balancing.md).

## 6. Pub/Sub as a Stateful Cluster

Even though messages aren't persisted, the **subscriber list per channel is state** — moving a channel forces every subscriber to unsubscribe from the old server and resubscribe on the new one.

Implications:

- **Don't auto-scale daily** like stateless services. Over-provision for daily peak with comfortable headroom and resize only when necessary, during low-traffic windows.
- **Resizing procedure** — provision new servers, update the hash-ring key in service discovery, watch for the expected CPU spike from the mass resubscription event. Some location updates may be missed during the transition (acceptable per the relaxed reliability requirement).

## 7. Operational Concerns

- **Replacing a single failed pub/sub server** is much cheaper than full resizing — only the channels on that server move; the on-call operator swaps the dead node for a standby in service discovery, and WebSocket handlers resubscribe only the affected channels.
- **Draining stateful WebSocket servers** — to remove a node, mark it "draining" at the load balancer so no new connections route to it, wait for existing connections to close, then remove. Same pattern for rolling out new versions.
- **Location cache scaling** — at 334K updates/sec a single Redis server is overloaded; shard by user ID and replicate each shard to a standby for failover.
- **Whale users** — friendships are bi-directional and capped (Facebook caps at 5,000). Subscribers spread across many WebSocket servers and the publisher's channel sits on one pub/sub server among many, so even high-friend-count users don't create hotspots. Note: this is a friendship model, not a follower/celebrity model — the [News Feed](case-studies/news-feed.md) celebrity hybrid doesn't apply.
- **Add/remove friend** — client app fires a callback that subscribes to or unsubscribes from the friend's pub/sub channel; same callback handles opt-in/opt-out toggles.

## 8. The "Nearby Random Person" Extension

For the "show me anyone nearby, not just friends" feature, switch from per-user channels to **one channel per geohash grid**. Each client subscribes to its current geohash plus the eight neighbors. See [Geospatial Indexing](fundamentals/geospatial-indexing.md) for the geohash mechanics — the eight-neighbor fetch is the same trick used in proximity service.

**Erlang as an alternative.** The authors note that Erlang/Elixir on the BEAM VM technically beats Redis Pub/Sub here: each Erlang process is ~300 bytes (millions per server) and idle processes consume zero CPU, so each user is naturally modeled as a process subscribed to friends' processes. The drawback is hiring — Erlang expertise is rare, so Redis Pub/Sub is the default.

## Sources

- [Vol 2 Ch 2: Nearby Friends](software/system-design-interview/books/system-design-interview-vol2/ch02_nearby_friends.md)
