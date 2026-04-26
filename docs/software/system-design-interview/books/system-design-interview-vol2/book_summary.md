# System Design Interview – An Insider's Guide: Volume 2: Summary

> **Read time: ~15–30 minutes.** This page is a single-sitting narrative summary of the book's key ideas. For a detailed chapter-by-chapter reference with the author's definitions and concrete examples, see the chapter entries in the sidebar.

## Table of Contents

- [1. Thesis and Approach](#1-thesis-and-approach)
- [2. Spatial Systems and Geohash](#2-spatial-systems-and-geohash)
  - [2.1. Static Geography: Proximity Service](#21-static-geography-proximity-service)
  - [2.2. Moving Targets: Nearby Friends](#22-moving-targets-nearby-friends)
  - [2.3. Map Tiles and Routing: Google Maps](#23-map-tiles-and-routing-google-maps)
- [3. Pipelines, Streams, and Aggregation](#3-pipelines-streams-and-aggregation)
  - [3.1. Distributed Message Queue](#31-distributed-message-queue)
  - [3.2. Metrics Monitoring](#32-metrics-monitoring)
  - [3.3. Ad-Click Aggregation](#33-ad-click-aggregation)
- [4. Correctness Under Contention](#4-correctness-under-contention)
  - [4.1. Hotel Reservation](#41-hotel-reservation)
  - [4.2. Payment System](#42-payment-system)
  - [4.3. Digital Wallet](#43-digital-wallet)
- [5. Storage and Retrieval at Scale](#5-storage-and-retrieval-at-scale)
  - [5.1. S3-like Object Storage](#51-s3-like-object-storage)
  - [5.2. Distributed Email Service](#52-distributed-email-service)
- [6. Real-Time Ranking and Matching](#6-real-time-ranking-and-matching)
  - [6.1. Gaming Leaderboard](#61-gaming-leaderboard)
  - [6.2. Stock Exchange](#62-stock-exchange)
- [7. Recurring Building Blocks](#7-recurring-building-blocks)
- [8. Key Takeaways](#8-key-takeaways)

## 1. Thesis and Approach

The second volume of *System Design Interview – An Insider's Guide* by Alex Xu and Sahn Lam is a tour of thirteen large-scale system designs that go deeper than the introductory examples in Volume 1. Each chapter is structured around the same four-step interview framework — clarify the problem and scope, propose a high-level design, drill into a deep dive, and wrap up — and the recurring lesson across all thirteen is that good systems come from selecting the right primitive for the workload (geohashes for spatial joins, sorted sets for ranking, append-only logs for ordered streams) and being deliberate about the trade-offs implied by that choice.

The thirteen problems split naturally into five clusters: spatial systems, streaming and aggregation pipelines, transactional systems demanding correctness under contention, large-scale storage, and real-time ranking and matching. The same handful of primitives — consistent hashing, geohash, Kafka-style logs, idempotency keys, double-entry ledgers, optimistic locking, event sourcing — show up again and again, repurposed for each domain. Reading the book end-to-end builds an intuition for which primitive belongs to which class of problem.

## 2. Spatial Systems and Geohash

The first three chapters all hinge on representing locations on a sphere efficiently, but each demands a different technique because the *workload* differs.

### 2.1. Static Geography: Proximity Service

A proximity service finds nearby places — restaurants on Yelp, gas stations on Google Maps — within a radius of the user's location. The traffic profile is read-heavy and the underlying business locations rarely change, which lets the design rely on a primary-secondary relational database (e.g., MySQL) with replication.

The core technical question is how to index two-dimensional points so a "what's near me" query is fast. A naive 2D `WHERE lat BETWEEN ... AND long BETWEEN ...` requires intersecting two huge index scans; the trick is to map 2D points into 1D so a single B-tree index can answer range queries. The book surveys five options — two-dimensional search, evenly divided grid, **geohash**, **quadtree**, and **Google S2** — and recommends discussing geohash or quadtree in interviews because S2 is too complex to explain clearly under time pressure.

**Geohash** encodes (lat, long) as a base-32 string by recursively splitting the planet into four quadrants, alternating longitude and latitude bits at each level. Longer shared prefixes mean closer geohashes — Google HQ (`9q9hvu`) and Facebook HQ (`9q9jhr`) share `9q`. Two boundary issues need attention: close locations on opposite sides of the equator or prime meridian can have *no* shared prefix (La Roche-Chalais `u000` and Pomerol `ezzz` are 30km apart but share nothing), and two close points can share a long prefix yet sit in different grids. Both are solved by also fetching the eight neighboring geohashes, which can be computed in constant time.

A **quadtree** instead recursively subdivides the world into four quadrants until each leaf holds at most ~100 businesses. It's an in-memory data structure (not a database), built on each LBS server at startup; with 200M businesses it fits in ~1.71 GB and takes minutes to build. Quadtree adapts grid size to density (granular in cities, coarse in oceans) and natively supports k-nearest queries, but updates are harder — `O(log n)` traversal, locking, and rebalancing.

The deep-dive lessons generalize to other read-heavy systems: don't reflexively shard a geo index that already fits in one server's working set (~1.71 GB); prefer read replicas. Use the **geohash itself as the cache key** in Redis, because raw lat/long is a poor key (GPS jitter, tiny user movement) but small location changes naturally map to the same geohash. Replicate the cache globally for low cross-continent latency, and use multi-region deployment plus DNS routing to comply with privacy laws (GDPR, CCPA).

### 2.2. Moving Targets: Nearby Friends

The Nearby Friends feature looks superficially similar to a proximity service, but the workload is fundamentally different: businesses are static, while **friends move**, making this a real-time message-passing problem rather than a spatial-search problem. With 100M DAU on this feature, 10% concurrent, and a 30-second refresh cadence (chosen because human walking speed makes finer updates pointless), the design must handle ~334K location updates per second and forward roughly 13M location messages downstream every second.

The architecture splits into a load balancer fronting **stateless RESTful API servers** (for friend management) and **stateful WebSocket servers** (for the persistent location stream). Each user maintains one long-lived WebSocket carrying both their outgoing location updates and incoming friends' updates. The latest location for each active user lives in a Redis cache with a TTL, durability not required because a cold cache simply refills as new updates stream in.

The fan-out trick is **Redis Pub/Sub**: every user has a personal channel, their location updates publish to it, and each friend's WebSocket connection handler subscribes. Channels are extremely cheap to create — millions per server — and idle channels consume no CPU. On client startup, the server **subscribes to every friend's channel — active or not** — because creating idle subscriptions is essentially free, simplifying the design at the cost of slightly more memory.

Scale forces the pub/sub layer to become a distributed cluster. Channels are sharded across servers using a **hash ring** keyed on the publishing user's ID, with the ring stored in a service discovery component (etcd or ZooKeeper). The bottleneck turns out to be CPU, not memory — back-of-envelope memory needs are ~200 GB (two servers' worth), but pushing 13M messages/sec at 100K pushes/server-sec requires ~130 servers. Critically, even though messages aren't persisted, **the subscriber list per channel is state**, so the pub/sub cluster must be treated as stateful: over-provisioned for peak, resized only deliberately, never auto-scaled like stateless services.

The chapter closes with two extensions. For "nearby random people," allocate one pub/sub channel per geohash grid and have each client subscribe to the current grid plus its eight neighbors — reusing geohash machinery from chapter 1. As an alternative to Redis Pub/Sub, the authors argue **Erlang/Elixir on the BEAM VM** is technically a better fit (~300 bytes per process, millions per server, zero CPU when idle), but recommend Redis as the default because Erlang expertise is hard to hire.

### 2.3. Map Tiles and Routing: Google Maps

The simplified Google Maps design covers three features: location updates, navigation with ETA, and map rendering. The scale is daunting — 1B DAU, terabytes of road data, ~25M daily map updates in real Google Maps — and the storage estimates are striking: pre-rendered tiles across 21 zoom levels come to roughly 100 PB.

The flattened sphere is split via **map tiles** (256×256 PNG images, one URL per tile, served from a CDN with the geohash baked into the URL) and **routing tiles** (binary graphs of intersections and roads). Map tiles are precomputed because dynamic generation is too costly per request and uncacheable. Routing tiles use a **hierarchical** structure with three resolution levels — small tiles for local roads, mid-size for arterial roads, large for highways between cities — connected by inter-level edges so an A*-style traversal can "enter" a coarser tile via a freeway entrance and load only the tiles it needs.

Three top-level services handle the workload: a **location service** (clients buffer GPS samples every second and POST batches every ~15 seconds, reducing traffic and battery; data lands in Cassandra and is also published to Kafka so live-traffic and road-detection consumers can tap the stream), a **navigation service** (geocoding → shortest-path over routing tiles → ETA via ML over current and historical traffic → ranker), and **map rendering** (CDN-fronted static tiles). On the client, **vector tiles via WebGL** compress better than rasterized PNGs and yield smooth zooming because the client scales each element independently rather than pixelating between zoom levels.

## 3. Pipelines, Streams, and Aggregation

The middle of the book covers three streaming systems. The same primitives recur — Kafka-style append-only logs, partitioning, exactly-once semantics, watermarks — applied to messaging infrastructure itself, to monitoring, and to billing-grade ad-click aggregation.

### 3.1. Distributed Message Queue

The book designs a Kafka- and Pulsar-flavored distributed queue with long retention, repeated consumption, and ordering guarantees, then discusses how a traditional RabbitMQ-style queue would simplify when those features can be dropped. Topics are split into **partitions** distributed across **brokers**; each partition is a FIFO queue and a message's position within it is its **offset**. A message's partition is `hash(key) % numPartitions`, so messages with the same key (e.g., user ID) always land in the same partition, preserving per-key order.

**Consumer groups** let multiple consumers cooperate to consume a topic; within a group, a partition is consumed by exactly one consumer, so excess consumers sit idle — meaning you should **pre-allocate generously many partitions** up front. A coordination service like Apache ZooKeeper handles broker discovery and elects an **active controller** that assigns partitions.

The three core design choices are: a sequential on-disk **write-ahead log** to exploit disk and OS cache (rotational disks are slow only for random access; in RAID with sequential workloads they hit hundreds of MB/s, and the OS aggressively caches pages); an immutable message format passed end-to-end without copying (zero-copy contract between producer, broker, and consumer); and pervasive batching at every layer.

**Replication** keeps each partition on multiple brokers with one leader and several followers; producers write only to the leader, followers pull, and leaders are elected via the coordination service. The chapter walks through consumer rebalancing protocols (join, leave, crash) and discusses **delivery semantics** — at-most-once, at-least-once, and exactly-once — with the latter requiring transactional commits across the offset and the downstream effect.

### 3.2. Metrics Monitoring

The internal metrics monitoring system targets 100M DAU, 10M metrics, 1-year retention with tiered resolution (raw for 7 days, 1-minute for 30 days, 1-hour for a year). The data is **time-series**: a value stream uniquely identified by (metric name, set of `<key:value>` labels), with an array of `<value, timestamp>` pairs.

Relational databases are wrong for this — moving averages require gnarly nested SQL, and constant heavy writes plus per-tag indexes overwhelm them. Generic NoSQL (Cassandra, Bigtable) can technically work but requires deep schema-design expertise. Purpose-built **time-series databases** like InfluxDB and Prometheus win on every axis: time-series-friendly query languages (InfluxDB's Flux turns an exponential moving average into one fluent line), retention/aggregation features baked in, and engines tuned for the access pattern — write-heavy and constant, read-spiky for visualization and alerting, with **≥85% of operational queries** hitting data from the last 26 hours per Facebook research.

The collection layer can be **pull** (Prometheus polls each service's `/metrics` endpoint, with consistent hashing across collectors and service discovery feeding the live endpoint list) or **push** (a long-running collection agent on each server pushes to an auto-scaling collector cluster). Pull wins on debugging and clear health signals; push wins on firewalls/multi-DC and short-lived jobs. Large organizations support both, especially with serverless where agents can't be installed.

A **Kafka buffer between collectors and the TSDB** protects against TSDB unavailability, decouples ingestion from storage, and lets stream processors (Storm, Flink, Spark) consume in parallel — partitioned by metric name. Aggregations can happen client-side (limited), in the ingestion pipeline (cheap but loses precision), or query-side (full precision but slow).

### 3.3. Ad-Click Aggregation

Ad-click aggregation sits between Real-Time Bidding feedback and billing, where a few percent error translates into millions of dollars of misbilling. The pipeline is **billing-grade**: correctness beats latency, and the design must handle late events, duplicate events, and partial failures.

The architecture is a **Kappa-style** stream pipeline (one engine for both real-time and reprocessing, vs. lambda's separate batch and streaming codepaths) with **two Kafka queues**: log watcher → Queue 1 (raw click events) → aggregation service → Queue 2 (per-minute aggregates and top-N) → DB writer → DB. The second queue is required to achieve **end-to-end exactly-once** semantics between aggregation output and storage. The aggregation stage is structured as a MapReduce-style DAG (Map → Aggregate → Reduce) running on stream-processing engines.

**Time semantics** are central. Event time (when the click happened, on the client) is preferred over processing time (when the aggregator handled it) because billing accuracy outweighs concerns about client clock trust. **Watermarks** — a fixed extension (e.g., +15 seconds) appended to each window — let slightly-late events fall into the right bucket; very late events are corrected by end-of-day **reconciliation**. Aggregation uses **tumbling** windows for per-minute counts and **sliding** windows for "top-N over the past M minutes."

Achieving exactly-once requires wrapping the offset update and downstream send in a distributed transaction; naïve "store offset before downstream ack" or "after ack" both produce gaps or duplicates under crashes. Both raw and aggregated data are stored in a write-optimized time-series DB like Cassandra; raw data is immutable, the source of truth for replay, and movable to cold storage, while aggregates are the active query layer.

## 4. Correctness Under Contention

Three chapters tackle problems where the storage and fan-out are easy, but the system must guarantee that no row gets sold twice, no payment gets double-charged, and no balance goes negative.

### 4.1. Hotel Reservation

A hotel reservation system is read-heavy but has nasty concurrency on contested rooms during peak events. Reservation TPS is naturally low — 5,000 hotels × 1M rooms × 70% occupancy / 3-day stay ÷ 86,400s ≈ **3 reservations/sec average**.

A relational database with **ACID** is the right call to prevent negative balance, double charge, and double booking. The schema's central insight is that you reserve a **room *type*, not a specific room** — hotels assign room numbers at check-in, unlike Airbnb where the listing ID is fixed at booking. So the inventory table has composite key `(hotel_id, room_type_id, date)` with `total_inventory` and `total_reserved`, pre-populated two years ahead by a scheduled job. With 5,000 hotels × 20 room types × 2 years × 365 days = 73M rows, the whole table fits a single DB; use cross-region replication for HA before reaching for sharding.

Two distinct double-booking problems need two distinct fixes. **User double-clicks** are solved by making `reservation_id` (a globally-generated UUID created before submit) the **primary key**: the second insert violates uniqueness and is rejected. **Multi-user races** for the last room need locking. The book compares pessimistic locking (`SELECT … FOR UPDATE`, deadlock-prone), optimistic locking (a `version` column, fails fast under contention), and database constraints (`CHECK (total_inventory - total_reserved >= 0)`, easy but DB-dependent). For this workload, **optimistic locking** wins because reservation QPS is low enough that version-check failures are rare.

The cache layer (Redis, key `hotelID_roomTypeID_{date}` → available count) is updated asynchronously, possibly via Change Data Capture with Debezium. Crucially, **the DB does the final inventory validation on every reserve** — never trust the cache alone to commit. If the cache stales out, the user gets a "someone just booked it" error and the system stays correct.

### 4.2. Payment System

A payment system settles transactions between buyers, sellers, and intermediaries. Pay-in moves the buyer's card → the e-commerce bank account → the seller's account; pay-out is the mirror, often via a third-party payable provider like Tipalti. Scale is modest — 1M transactions/day, ~10 TPS — but correctness is everything.

The data model centers on a **double-entry ledger**: every transaction posts to two accounts with equal magnitude (debit one, credit the other), and the sum across all entries must equal zero. "One cent lost means someone else gains a cent." Money amounts are stored as **strings, not doubles**, to avoid floating-point precision loss — Japan's GDP at ~5×10¹⁴ yen and 1 satoshi at 10⁻⁸ BTC both break double precision. To stay out of PCI DSS scope, merchants embed a **PSP-hosted payment page** (iframe or SDK) so card data never touches the merchant backend.

**Reconciliation** — daily comparison of state across services and against PSP/bank settlement files — is "the last line of defense" because async messages aren't guaranteed to deliver. Mismatches sort into three buckets: classifiable and auto-fixable, classifiable but not cost-effective to automate (fixed by the finance team from a queue), and unclassifiable (manual investigation).

**Reliability** comes from an append-only payment-state log so any failure resumes from the last known state. Transient failures route to a **retry queue** with exponential backoff; messages that exhaust retries land in a **dead letter queue** for engineering review (Uber's payment system uses Kafka for both, per a cited engineering post). **Exactly-once = at-least-once (via retry) + at-most-once (via idempotency)**: a client-generated UUID in an `<idempotency-key: ...>` header (the cart ID is a natural choice, per Stripe's and PayPal's recommendations) becomes the primary key of the payment record, so duplicates fail the unique constraint and the system replays the original status.

### 4.3. Digital Wallet

The digital wallet is a more demanding cousin: 1M TPS, 99.99% availability, and **reproducibility** so historical balances can be reconstructed by replaying data from the beginning. Each transfer is two operations (debit + credit), so the design must push per-node TPS up to lower hardware cost (1,000 TPS/node → 2,000 nodes; 10,000 TPS/node → 200 nodes).

The chapter walks through three designs that each fix the prior one's limitation. **In-memory sharding** — a Redis cluster keyed by `accountID.hashCode() % partitionNumber`, with shard config in ZooKeeper — is fast but two updates aren't atomic, so a wallet-service crash mid-transfer leaves the system inconsistent. **Distributed transactions on relational DBs** fix atomicity. **Two-phase commit (2PC)** locks all participants for the entire transaction (kills performance, single-coordinator failure point). **Try-Confirm/Cancel (TC/C)** uses two independent local transactions — phase 1 reserves resources, phase 2 confirms or cancels via business-logic undo — and is database-agnostic. **Saga** orders all operations linearly and rolls back from the failure point with compensating transactions; choreography is decentralized but hard to reason about, while orchestration with a single coordinator is preferred for wallets.

The third design — **Event Sourcing with CQRS** — is the only one that satisfies reproducibility. State-changing facts are persisted as an immutable sequence of **Events** (validated past-tense facts), with a deterministic **State Machine** that turns inbound **Commands** into Events. Replaying the event log from the beginning reconstructs any historical balance, verifies correctness after a code change, and supports auditors. **Command-Query Responsibility Segregation** publishes Events instead of State so many read-only views (current balance, hourly windows for double-charge investigation, audit trail) can be built independently.

For 1M TPS the chapter optimizes event sourcing in three steps. **Local file-based stores** with `mmap` give in-memory read speed and disk durability in a single primitive; per ACM Queue, sequential disk writes can outpace random memory access. **Raft replication** ensures no single-node data loss: leader election, log replication, retry-until-recover for crashed followers. Finally, **distributed event sourcing** shards by account ID, with each shard running its own Raft group, scaling linearly to the target throughput.

## 5. Storage and Retrieval at Scale

### 5.1. S3-like Object Storage

The S3-like object storage chapter opens with a useful taxonomy. **Block storage** presents raw blocks owned by one server (highest performance, used by databases and VMs). **File storage** layers files and directories on top, shared via NFS/SMB (general-purpose, mutable). **Object storage** offers a flat namespace, RESTful API, immutable objects, vast scale, and low cost — targeting cold and archival data. The design targets 100 PB in year one with 6 nines durability and 4 nines availability.

The architectural insight is **object immutability**: objects can be replaced or deleted but never edited in place, which buys vast scale and durability. The design separates a mutable **metadata store** (UNIX inode-equivalent) from an immutable **data store** (block-equivalent), so each is independently optimizable, and per LinkedIn research ~95% of object-storage requests are reads, justifying read-optimized choices.

The **data store** has three subcomponents: a stateless **data routing service**, a **placement service** (cluster topology with consensus-backed Paxos/Raft, tracking datacenter → rack → node so replicas spread across failure domains), and **data nodes** holding the disks. Data flow is primary-coordinated: the router writes to a primary replica, which replicates to secondaries before acking. Three-copy replication gives ~6 nines durability assuming 0.81% annual disk-failure rate.

Two storage tricks address physical media inefficiency. **Small-file packing** appends many small objects into one large read-write file (one per CPU core to avoid serialization), promoting it to read-only when it hits a few-GB threshold; otherwise small files waste disk blocks and exhaust the inode table. An **object lookup table** in a per-data-node SQLite holds `(object_id, file_name, start_offset, object_size)` so lookups need no cross-node coordination.

For better durability per dollar, **erasure coding (k+m)** splits an object into k data chunks plus m parity chunks computed via a linear formula; an (8+4) configuration tolerates up to four chunk losses while keeping storage overhead at 50% (vs. 200% for 3-copy replication) and reaches 11 nines durability. The trade is computational cost on writes (parity calc) and reads (multi-node fetch + reconstruction on failure), so erasure coding fits cost-minimizing archival workloads while replication fits latency-sensitive ones.

### 5.2. Distributed Email Service

Distributed email is storage-heavy by nature: 1B users, 100,000 send QPS, ~730 PB/year of metadata, ~1,460 PB/year of attachments. Traditional designs (one file per email à la Maildir) bottleneck on disk I/O and provide no HA, and the 1960s-era email protocols (SMTP, POP, IMAP) weren't designed for threading, labels, search, multimedia, or billions of users.

The architecture splits responsibilities: stateless web servers for REST APIs, stateful **real-time servers** with WebSocket (long-polling fallback) for push, a custom-built **metadata database**, an **attachment store** in object storage like S3 (Cassandra is rejected because its 2 GB blob limit is theoretical and large blobs break the row cache), a Redis cache for hot recent emails, and a **distributed search store** with an inverted index. JMAP over WebSocket (as Apache James implements) is a real-world reference.

The **metadata DB** design is the most distinctive choice. Workload analysis shows isolated per-user operations and **82% of read queries hitting data younger than 16 days**. Relational DBs handle the >100 KB HTML bodies poorly; pure object storage can't support read flags or threading; NoSQL is the leading candidate. Gmail uses Bigtable; large providers ultimately build **custom KV stores** with specific properties — multi-MB columns, strong consistency, minimized disk I/O, fault tolerance, easy incremental backups. Partition by `user_id` so a user's data stays on one shard; denormalize **`read_emails`** and **`unread_emails`** into separate tables because NoSQL can't filter efficiently on a non-key `is_read` column, and moving rows on read trades write complexity for fast list views. Conversation threads are reconstructed client-side from `Message-Id`, `In-Reply-To`, and `References` headers using the **JWZ algorithm**.

The send/receive flow includes a **same-domain shortcut** (skip outbound SMTP if the recipient is on the same provider), an outgoing queue with exponential backoff for downstream failures, and a separate incoming queue that decouples spam/virus filtering from SMTP intake. Email correctness is favored over availability: each mailbox has a single primary, and during failover the mailbox is **paused** rather than served stale.

## 6. Real-Time Ranking and Matching

### 6.1. Gaming Leaderboard

The gaming leaderboard problem — top 10, a specific user's rank, optionally ±4 neighbors — looks trivial but defeats relational databases. The naive `ORDER BY score DESC` is a table scan that takes tens of seconds at millions of rows; caching doesn't help because scores change continuously, and `LIMIT 10` answers the top-N but still can't answer "what's user X's rank."

The right primitive is the **Redis sorted set**: each unique member carries a score, internally backed by a hash table (member → score) plus a **skip list** (score → member). A skip list is a sorted linked list augmented with multi-level indexes that skip every other node at each level, giving binary-search-like traversal — the chapter cites a 62-node walk reduced to 11 nodes with 5 index levels. Every operation — insert, update, top-N, rank lookup — runs in `O(log n)`. A score-a-point becomes one `ZINCRBY`, top 10 is one `ZREVRANGE`, a user's rank is one `ZREVRANK`, and ±4 neighbors is a positional `ZREVRANGE`. New leaderboard keys roll over each month (`leaderboard_feb_2021`).

The whole leaderboard at original scale (25M MAU × 26 bytes ≈ ~650 MB) fits one Redis instance. Persistence works but cold-start from disk is slow, so standard practice is a read replica that gets promoted on primary failure with a fresh replica attached. At 100× the scale (500M DAU, ~250K QPS, ~65 GB), Redis must shard. **Fixed partition** by score range keeps top-10 entirely in the highest-range shard but requires tuning for distribution. **Hash partition (Redis Cluster)** with 16,384 slots and `CRC16(key) % 16384` distributes evenly but forces scatter-gather for top-10 and has no way to compute global rank — so the book leans toward fixed partition. As an alternative architecture, AWS Lambda + API Gateway + Redis offers serverless auto-scaling for greenfield games.

### 6.2. Stock Exchange

The stock exchange chapter is the latency outlier of the book. The system supports limit orders (place, cancel) on stocks, with risk checks, wallet integration to withhold funds for resting orders, real-time order books, and matched-trade dissemination. The non-functional bar is brutal: 99.99% availability, **millisecond round-trip with focus on 99th-percentile latency**, KYC + DDoS protection. NYSE trades billions of matches per day; the design targets ~43,000 QPS average and 215,000 peak.

Three flows share components but with different latency budgets — **trading flow** on the critical path, **market data flow** publishing to subscribers, **reporter flow** for compliance and settlements. The critical path is `client gateway → order manager → sequencer → matching engine`, with even logging removed to save microseconds. The **matching engine** maintains the order book per symbol, matches buys against sells emitting two executions per match (one per side), and must be **deterministic**: given the same input order sequence, it produces the same execution sequence on replay. Determinism rules out HotSpot JVM stop-the-world garbage collection in the critical path.

The **sequencer** stamps every incoming order and outgoing execution pair with a sequential ID. It provides timeliness/fairness, fast recovery/replay, and exactly-once guarantees, functioning as both message queue and event store. Kafka could fill the role but its latency is too high and unpredictable for an exchange.

The order book itself is a tight data structure: an `OrderBook` with `Book<Buy>` and `Book<Sell>`, each a `Map<Price, PriceLevel>` where each `PriceLevel` holds a doubly-linked list of orders. A top-level `Map<OrderID, Order>` enables O(1) cancel by jumping straight to the linked-list node. Pre-allocated **ring buffers** avoid allocations in the hot path, and in-memory candlesticks are capped with the rest persisted to disk.

The killer move is **single-server design with mmap message bus**. Naive multi-server hops cost ~500μs round-trip plus tens of ms for sequencer disk persistence. Putting gateway, order manager, sequencer, and matching engine on one machine and communicating via `mmap(2)` over a file in `/dev/shm` (memory-backed filesystem) gives sub-microsecond message sends with no disk access. A single-threaded `while(true)` polling loop pinned to a fixed CPU core avoids context switches, locks, and contention, driving end-to-end latency into **tens of microseconds**.

For high availability with these constraints, the exchange uses **event sourcing** (orders pass through many state transitions; the immutable log is the golden source of truth) and **Raft replication** for the sequencer, with active-active failover. **Network security** combines colocation (broker software runs on rented servers inside the exchange's data center, with latency = speed-of-light over cable length), the **FIX protocol over Simple Binary Encoding (SBE)** for vendor-neutral securities transactions, and TLS plus hardware security for the wires.

## 7. Recurring Building Blocks

A handful of primitives appear in chapter after chapter, repurposed for each domain.

| Primitive | Where it shows up |
|---|---|
| **Geohash** | Proximity service (caching, indexing), Nearby Friends (random-person extension), Google Maps (tile URLs and routing tiles) |
| **Consistent hashing / hash ring** | Nearby Friends (distributed pub/sub), S3-like (placement service), Metrics monitoring (collector pool), Digital Wallet (Redis sharding) |
| **Sorted append-only log** | Distributed message queue (WAL), Payment system (state log), Digital wallet (event store), Stock exchange (sequencer) |
| **Idempotency key / dedup primary key** | Hotel reservation (`reservation_id`), Payment system (cart ID), Ad-click aggregation (offset transactions), PSP integrations (nonce → token) |
| **Event sourcing + CQRS** | Digital wallet (reproducibility), Stock exchange (state recovery), Payment system (state log) |
| **Cache + DB with DB as source of truth** | Proximity service, Hotel reservation, Payment system, Email metadata |
| **Optimistic locking (`version` column)** | Hotel reservation; mentioned implicitly in any low-contention transactional path |
| **Kafka between stages** | Ad-click aggregation, Metrics monitoring, Google Maps location stream, Email retry/DLQ |
| **Stateful cluster with hash ring + service discovery** | Nearby Friends pub/sub, Metrics collectors, S3-like placement |
| **Pre-compute and serve from CDN/cache** | Google Maps (map tiles), Proximity service (geohash → business IDs) |

A few thematic principles cut across the book:

- **Match the primitive to the workload, not the brand to the headline.** Cassandra is right for write-heavy time-series in metrics and ad clicks but rejected for email attachments; relational is right for hotel reservations but wrong for time-series.
- **Don't reflexively shard.** If the working set fits one server, prefer read replicas over sharding (proximity service geo index, hotel inventory table).
- **The cache lies; the DB tells the truth.** Always re-validate at the source on the write path (hotel reservation, payment commit).
- **Stateful clusters need care.** Even pub/sub messages aren't persisted, but subscriber lists are state — over-provision and resize deliberately.
- **Idempotency is the universal double-write defense.** Client-generated UUIDs as primary keys cover double-clicks, retries, and crash-redo across reservation, payment, and ad pipelines.
- **Reproducibility requires events, not state.** Auditability and historical reconstruction force event sourcing; current-state-only stores cannot answer "why is this balance what it is."
- **Latency requires removal, not addition.** The stock exchange achieves microseconds by stripping the network, the disk, the GC, and the locks — not by adding caches.

## 8. Key Takeaways

- Use **geohash** to map 2D spatial data into 1D so a single B-tree index answers radius queries; choose between geohash, quadtree, and S2 based on whether you need k-nearest queries, dynamic grid sizing, or geofencing.
- Build real-time fan-out on **WebSocket + Redis Pub/Sub**, then shard the pub/sub layer with a **consistent hash ring** in service discovery; treat it as a stateful cluster, never auto-scale daily.
- For event streaming infrastructure, lean on **append-only WAL on disk + zero-copy message format + pervasive batching**; let the OS page cache do the work that disk seeks would otherwise kill.
- For **billing-grade aggregation**, choose event time over processing time, use watermarks for slightly-late events plus end-of-day reconciliation for very-late ones, and wrap offset+downstream-ack in a distributed transaction for exactly-once.
- For correctness under contention, prefer **optimistic locking** when contention is rare and **idempotency keys as primary keys** to defang client retries and double-clicks. Keep the DB as the final inventory check, never the cache.
- Money math demands **double-entry ledgers, string-typed amounts, and PSP-hosted pages** to stay correct, precise, and out of PCI DSS scope.
- For reproducibility (auditing, replay, code-change verification), store **immutable events** and rebuild state via a deterministic state machine; combine with CQRS to support many read views.
- Object storage trades immutability for vast scale; pack small files, separate metadata from data, and pick **replication for latency-sensitive** workloads or **erasure coding for archival** to optimize the durability-cost frontier.
- For ranking at scale, a **Redis sorted set with skip-list internals** turns rank queries from table scans into `O(log n)` lookups; shard by score range when you outgrow one node.
- Ultra-low-latency systems are built by **removing**: collapse to one server, communicate via `mmap` shared memory, pin a single-threaded loop to a CPU core, and design every component to be **deterministic** so replay reconstructs state exactly.
