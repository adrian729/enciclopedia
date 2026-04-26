# Ch 2: Nearby Friends

## Table of Contents

- [1. Problem and Scope](#1-problem-and-scope)
- [2. High-Level Design](#2-high-level-design)
- [3. Location Update Flow](#3-location-update-flow)
- [4. Scaling the Pub/Sub Layer](#4-scaling-the-pubsub-layer)
- [5. Operational Concerns](#5-operational-concerns)
- [6. Extensions and Alternatives](#6-extensions-and-alternatives)

## 1. Problem and Scope

- **Nearby Friends** — opt-in feature that shows a list of friends currently within a configurable radius (default 5 miles), updated every few seconds.
- **Key contrast with proximity service** — businesses are static, but **friends move**, making this a dynamic, write-heavy real-time message-passing problem rather than a spatial-search problem.
- **Scope assumptions** — straight-line distance only; inactive friends (>10 min idle) drop off; opt-in users only; privacy laws ignored for the design.
- **Functional requirements** — list nearby friends with distance + last-updated timestamp; refresh every few seconds.
- **Non-functional requirements** — low latency, reliability with occasional drops acceptable, eventual consistency (a few seconds of replica lag is fine).
- **Scale assumptions** — 1B total users, 100M DAU on this feature, 10% concurrent (10M), avg 400 friends/user, **30-second location refresh** (chosen because 3–4 mph walking speed makes finer updates pointless).
- **Derived QPS** — location update QPS = 10M / 30 ≈ **334K updates/sec**; with ~10% of friends online and nearby, the backend must forward ~13M location messages/sec downstream.

## 2. High-Level Design

- **Why not peer-to-peer** — direct phone-to-phone connections drain battery and break on flaky mobile networks; a shared backend is the practical choice.
- **Two server tiers behind a load balancer** — stateless **RESTful API servers** for friend management and profile updates; stateful **WebSocket servers** for the persistent bidirectional location stream.
- **WebSocket connection** — each client maintains one long-lived WebSocket connection used both for sending its own location updates and for receiving nearby friends' updates.
- **Redis location cache** — stores the latest `user_id → {lat, long, timestamp}` for each active user with a **TTL** that auto-expires inactive users; durability not needed because a cold cache just refills from incoming updates.
- **User database** — holds profiles and the friendship graph; sharded by user ID; often fronted by an internal API at scale.
- **Location history database** — stores historical points for ML and other downstream uses; **Cassandra** is a good fit because it handles heavy writes and scales horizontally (a sharded relational DB also works).
- **Redis Pub/Sub as the routing layer** — every user has a personal channel; their location updates publish to that channel, and each friend's WebSocket connection handler subscribes. Channels are extremely cheap to create — a Redis server with GBs of memory can hold millions, and idle channels (no updates) consume no CPU after creation.

## 3. Location Update Flow

1. Mobile client sends new location over its WebSocket to the load balancer, which routes to the user's WebSocket server.
2. WebSocket server **persists to the location history DB**, **updates the Redis location cache** (refreshing TTL) and stores the location in the connection handler's local variable for distance math, and **publishes the new location to the user's personal Redis Pub/Sub channel** — these three steps can run in parallel.
3. Pub/Sub broadcasts to all subscribers — i.e., the WebSocket connection handlers of online friends, which may live on different WebSocket servers.
4. Each receiving handler computes the distance between its subscriber and the publisher; if within the search radius, it pushes the new location and timestamp down the subscriber's WebSocket; otherwise the update is dropped silently.

- **Client initialization sequence** — on app startup, the client opens a WebSocket and sends its location; the server (a) updates the location cache, (b) loads all friends from the user DB, (c) batch-fetches friends' locations from the cache, (d) returns those within radius to the client, (e) **subscribes to every friend's pub/sub channel — active or not** — because creating idle channels is essentially free, simplifying the design at the cost of slightly more memory.

## 4. Scaling the Pub/Sub Layer

- **Bottleneck is CPU, not memory** — back-of-envelope: 100M users × 100 active friends × 20 bytes ≈ 200 GB → ~2 servers worth of memory; but pushing 13M messages/sec at a conservative 100K pushes/server-sec needs ~130 Redis servers. The fan-out load dwarfs the storage need.
- **Distributed pub/sub via consistent hashing** — channels are sharded across the pub/sub server cluster using a **hash ring** keyed on the publishing user's ID; the ring is stored in a **service discovery component** (etcd or ZooKeeper).
- **Service discovery requirements** — keep the active server list under a key like `/config/pub_sub_ring`, and let WebSocket servers subscribe to changes so their cached copy of the ring stays current.
- **Treat pub/sub as a stateful cluster** — even though messages aren't persisted, the **subscriber list per channel is state**; moving a channel forces every subscriber to unsubscribe from the old server and resubscribe on the new one.
- **Implication for capacity planning** — don't auto-scale pub/sub up and down daily like stateless services; over-provision for daily peak with comfortable headroom and resize only when necessary, during low-traffic windows.
- **Resizing procedure** — provision new servers, update the hash-ring key in service discovery, watch for the expected CPU spike from the mass resubscription event; some location updates may be missed during the transition (acceptable per the relaxed reliability requirement).

## 5. Operational Concerns

- **Replacing a single failed pub/sub server is much cheaper than resizing** — only the channels on that server move; the on-call operator swaps the dead node for a standby in service discovery, and WebSocket handlers only resubscribe channels mapped to the replaced node.
- **Draining stateful WebSocket servers** — to remove a node, mark it "draining" at the load balancer so no new connections route to it, wait for existing connections to close, then remove. Same pattern for rolling out new versions.
- **Location cache scaling** — at 334K updates/sec a single Redis server is overloaded, but location data per user is independent, so shard the cache by user ID and replicate each shard to a standby for failover.
- **Users with many friends** — friendships are bi-directional and capped (Facebook's cap is 5,000); subscribers spread across many WebSocket servers and the publisher's channel sits on one pub/sub server among many, so even "whale" users don't create hotspots. Note this is a friendship model, not a follower/celebrity model.
- **Adding/removing friends** — the client app fires a callback to the WebSocket server on friend add/remove, which subscribes to or unsubscribes from the friend's pub/sub channel; the same callback handles opt-in/opt-out toggles.

## 6. Extensions and Alternatives

- **Nearby random person (extension)** — instead of per-user channels, allocate **one pub/sub channel per geohash grid**; each client subscribes to its current geohash plus the eight neighboring grids (to handle border cases), and location updates are published to the user's grid channel. Reuses the geohash machinery from Chapter 1.
- **Erlang as an alternative to Redis Pub/Sub** — the authors argue Erlang/Elixir on the BEAM VM with OTP is technically a better fit: each Erlang process is ~300 bytes (millions per server) and idle processes consume zero CPU, so each user can be modeled as a process that subscribes to friends' processes natively. The drawback is purely organizational — Erlang expertise is hard to hire, so Redis Pub/Sub is the default recommendation unless a team already has Erlang skills.
