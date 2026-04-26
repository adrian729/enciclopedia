# System Design Interview Fundamentals: Summary

> **Read time: ~15–30 minutes.** This page is a single-sitting narrative summary of the book's key ideas. For a detailed chapter-by-chapter reference with the author's definitions and concrete examples, see the chapter entries in the sidebar.

## Table of Contents

- [1. Thesis and Orientation](#1-thesis-and-orientation)
- [2. The Six-Step Framework](#2-the-six-step-framework)
  - [2.1. Gathering Requirements](#21-gathering-requirements)
  - [2.2. Defining the API](#22-defining-the-api)
  - [2.3. High-Level Diagram](#23-high-level-diagram)
  - [2.4. Schema and Data Model](#24-schema-and-data-model)
  - [2.5. End-to-End Flow](#25-end-to-end-flow)
  - [2.6. Deep Dive Design](#26-deep-dive-design)
- [3. Back-of-the-Envelope Math](#3-back-of-the-envelope-math)
- [4. The Technical Toolbox](#4-the-technical-toolbox)
  - [4.1. Schemas, Indexes, and Databases](#41-schemas-indexes-and-databases)
  - [4.2. Caching](#42-caching)
  - [4.3. Replication](#43-replication)
  - [4.4. Sharding](#44-sharding)
  - [4.5. Concurrency and Transactions](#45-concurrency-and-transactions)
  - [4.6. Async, Batch, Stream, and Lambda](#46-async-batch-stream-and-lambda)
  - [4.7. Queues and Messaging](#47-queues-and-messaging)
  - [4.8. Conflict Resolution](#48-conflict-resolution)
  - [4.9. Resilience Patterns](#49-resilience-patterns)
  - [4.10. Distributed Transactions](#410-distributed-transactions)
- [5. Specialized Toolbox Topics](#5-specialized-toolbox-topics)
  - [5.1. Real-Time Data Updates](#51-real-time-data-updates)
  - [5.2. ID Generation](#52-id-generation)
  - [5.3. Full-Text Search](#53-full-text-search)
  - [5.4. Data Transfer and Compression](#54-data-transfer-and-compression)
  - [5.5. Networking, Gateways, and CDNs](#55-networking-gateways-and-cdns)
  - [5.6. Cold Storage, Monitoring, Security, Product](#56-cold-storage-monitoring-security-product)
- [6. Communication Discipline](#6-communication-discipline)
- [7. The Interviewer's Perspective](#7-the-interviewers-perspective)
- [8. Patterns from the Worked Examples](#8-patterns-from-the-worked-examples)
- [9. Key Takeaways](#9-key-takeaways)

## 1. Thesis and Orientation

Liu's central claim is that the system design interview measures how a candidate approaches an open-ended problem, not how many reference architectures they can recite. "System design is about understanding the problem you're trying to solve before coming up with a solution. It is not about coming up with a solution and finding a problem to fit into that solution." The book teaches the building blocks — a framework for structuring the conversation and a toolbox of scaling primitives — so any question can be composed from fundamentals. Definition-level trivia that is Googleable (exact L1 cache latencies, step-by-step internals of a specific database) is deliberately skipped; what matters is *when, where, and why* to reach for each piece of technology.

Three skills are evaluated in parallel: problem-solving under trade-offs, technical knowledge of the components, and communication of the reasoning. The format mirrors real engineering work — clarify a PM-style prompt, propose an architecture, defend the trade-offs, make a recommendation — and that mirroring is why memorized answers collapse under probing. Interviewers spot rehearsed designs quickly: a candidate who proposes a solution before stating the problem, or who cannot adapt when the prompt shifts from "Instagram" to "Instagram for a different user base with a different query pattern," fails the novelty test. The payoff is material: the total-comp gap between senior and staff is typically **$150k–$200k USD**, and clearing system design is a gate to that jump. Preparation centers on understanding *why* each technology exists and *why its alternatives fell short*, and live mock interviews are the single most important activity because the skill is as much argument presentation as technical depth.

## 2. The Six-Step Framework

Liu organizes every interview around a top-down flow whose steps and timings fit inside a typical 40-minute slot. Starting from the middle loses the big picture.

| Step | Activity | Time |
|---|---|---|
| 1a | Gather Requirements — Functional | 2–3 min |
| 1b | Gather Requirements — Non-Functional | 3–5 min |
| 2 | Define API | 3–5 min |
| 3 | High-Level Diagram | 5–7 min |
| 4 | Schema and Data Structures | 5–7 min |
| 5 | End-to-End Flow | 2–3 min |
| 6 | Deep Dives | 15–20 min |

A critical sequencing rule: back-of-the-envelope math goes *after* API and schema, not upfront. QPS is tied to a specific API; storage is tied to a specific schema. Calculating either before those steps forces guesswork.

### 2.1. Gathering Requirements

Functional requirements are user stories, written the way a PM would: ask *who is it for and why*, narrow to one or two features, and get the interviewer's buy-in rather than sweeping the whole product. Terminologies must be clarified — for a "Netflix recommendations" prompt, drill into what a recommendation contains rather than over-engineering the ML model.

Non-functional requirements are where engineering focus concentrates. Scale questions probe active users, geographic distribution, and scenarios driving high QPS (concert-end for ridesharing) or high storage and bandwidth (super users, peak hours). Performance constraints include availability versus consistency (framed as user experience, not "AP vs CP"), accuracy (distinct from consistency — eventual consistency is eventually *accurate*), response time, freshness, and durability. Freshness falls into three categories: **real-time** (stock trader), **near real-time** (Facebook Live), and **batch process** (static-site crawler). Durability stated in "9s" should be framed by user impact rather than memorized counts.

### 2.2. Defining the API

The API is a detailed contract; without it, discussions get **hand-wavy**. Three things matter: signature name, input parameters, and output response. Most candidates forget the output, which is often as design-shaping as the input. A `request_ride` that returns `{ driver_ids: [1, 2] }` and lets the user pick a driver introduces concurrency at the API boundary; returning `{ driver_id: 1 }` and letting the server assign sidesteps it.

The rule "everything counts" applies to inputs: don't add unjustified parameters, don't omit required ones, don't use vague or nonsensical values (a client-generated `photo_id`, a `friend_name` instead of `friend_user_id`). RESTful and protobuf details are distractions unless the interviewer explicitly asks. Collections in the response imply pagination and thumbnails, called out proactively. Default to idempotent APIs where achievable (`update_quantity(order, 2)` rather than `decrease_quantity(order, 1)`), and default to server-generated data for anything sensitive to client clock skew or tampering.

### 2.3. High-Level Diagram

The high-level diagram sets the foundation and shows an end-to-end flow satisfying the requirements. It sits after the API (the diagram's entry point) and before the schema. The systematic approach draws each API from client to last component, then connects subsequent APIs to what exists; candidates who merely "list microservices" miss components. Premature optimization is a common failure — adding a cache cluster, sharding, a rate limiter, or generic boxes (DNS, auth, logging) without justification reads as hand-wavy. When tempted to dig in, the candidate writes the topic on the side — the **table interesting discussion points** discipline — and returns to it during the deep dive.

### 2.4. Schema and Data Model

Schema concretizes the diagram. Detail belongs on arrows (unsorted driver ID list vs. scored list vs. single ID), on queues (enqueue `raw_video_id` rather than bytes that exhaust memory), and on databases (flat table vs. indexed table changes efficiency). Walking the schema against agreed requirements catches nonsensical designs — a `Message Table(user_id, receiver_id, ...)` fails for group chat where a user and receiver can belong to multiple rooms.

### 2.5. End-to-End Flow

Before jumping into deep dives, the candidate traces each API through the system to confirm the design works and collect discussion items. Most candidates skip this checkpoint, which leaves the interviewer uncertain whether the baseline functions.

### 2.6. Deep Dive Design

The deep dive is where seniority shows. Two central ideas anchor it.

> **The System Design Interview Golden Question** — *"What is the problem I am trying to solve?"* Solution-first thinking (adding a cache, sharding) without stating the problem is the most common failure mode.

Concluding that something *isn't* a problem and doesn't need solving is a strong positive signal — no one would shard a 1-QPS startup database in real life either.

The second idea is the **magic formula**, a six-step loop run repeatedly: (1) identify a bottleneck, (2) come up with options (aim for at least two — one option reveals no problem-solving), (3) talk about trade-offs and tie them back to requirements, (4) pick one solution and take a stance, (5) active discussion with the interviewer, (6) go back to step 1. Because there is no dashboard or PM in the room, candidates must surface their own bottlenecks. Discussion points can be mined from six categories: APIs and interprocess arrows (latency sensitivity, high QPS, bursty traffic, query efficiency, protocols); microservices, queues, and databases (failure modes, data volumes, component choices); algorithms and schemas; concurrency; operational issues and metrics; and security, which most candidates overlook.

## 3. Back-of-the-Envelope Math

Numbers justify design choices; without them, proposals like caching and sharding are hand-wavy. A calculated 10⁸ QPS against a single machine's ~10⁶ capacity identifies a scaling problem. Dismissing the need to scale based on a calculated result reflects strong judgment. The most common failure mode is calculating too soon: QPS is per-API and storage is per-schema.

Liu's QPS formula is `daily active users × percentage making the query × average queries per user per day × scaling factor`, divided by roughly 100,000 (the 86,400 seconds in a day, rounded for mental math — dividing by 100k just subtracts 5 from the power of 10). The storage formula multiplies daily active users by percentage, queries, data size per query, replication factor (typically 3), and time horizon (usually 1–5 years). The scaling factor captures worst-case spikes — ridesharing on weekend nights runs 5–10× average — and the worst case is the number to design for.

The six-step calculation technique is mechanical: convert everything to scientific notation (every comma shifts the exponent by 3), group the 10s, group other numbers, compute, convert to readable units via the conversion table, and *do something with the number*. Calculating 6 PB/day and moving on is worthless. Common mistakes include spending too long, confusing GB with TB (a 1,000× error), and calculating unimportant numbers like bandwidth for a lightweight heartbeat service.

## 4. The Technical Toolbox

Much of the book is a guided tour through the primitives a candidate composes during deep dives. The goal is not to enumerate features of particular databases but to ground each primitive in the problem it solves, the trade-offs it introduces, and the cues that should make a candidate reach for it.

### 4.1. Schemas, Indexes, and Databases

Schemas begin with a logical view — entities, foreign keys, join tables for many-to-many — and defer the database choice until access patterns are clear. Normalized is the default; denormalize only when read throughput is the specific bottleneck.

An **index** is a sorted auxiliary structure that turns `O(N)` scans into `O(log N)` searches, implemented as a B-Tree or as an LSM with a **Sorted Strings Table (SST)**. Database indexes are not hashmaps — hashmaps are in-memory, while on-disk indexes are sorted structures. A primary (clustered) index sorts the main table on disk; a secondary index points back into it, trading write cost for read speed. Indexes power key lookup, range lookup, and prefix search — the last supporting type-ahead and **geohash** prefix lookups where `"a*"` returns every geohash beginning with `"a"`. Composite indexes on `(col_a, col_b)` are order-sensitive: `(status, location)` is efficient for "all busy drivers in Chicago" but not "all drivers in New York." Geographic queries simplify in interviews to a geohash with prefix search, or a reverse index from a grid bucket to object IDs. A **QuadTree** is an in-memory data structure, not a database.

Choosing a database is category reasoning, not name-dropping. "I'll use NoSQL because it scales" is hand-wavy — every competitive database scales. The CAP theorem (pick two of C, A, P) is necessary but not sufficient, and not a clean classification: MySQL with async-replicated followers isn't strictly "CP" once reads hit followers. Liu's categories run from relational (MySQL, Postgres — the default) through document stores, columnar stores for analytics, object stores for blobs, wide-column stores (BigTable, HBase, Cassandra) for write-heavy workloads with LSM indexing, reverse index stores (Elasticsearch) for search, in-memory stores (Redis, Memcache), geo-spatial databases, and **ZooKeeper**-class systems for strong-consistency coordination via consensus (Zab, Paxos, Raft). Multiple databases per question is normal — YouTube needs a blob store for video bytes and a metadata store for the video record.

### 4.2. Caching

Caching is volatile storage that delivers three benefits: latency (memory is ~100× faster than disk), throughput, and bandwidth (data closer to the user — CDNs are a form of cache). Candidates who throw a cache in front of every database without tying the decision to a non-functional requirement get dinged. The latency gain depends on the target: 5 ms to 0.1 ms is pointless at a 500 ms SLO and meaningful at a 20 ms SLO.

**Cache Hit Rate = Hits / (Hits + Misses)**. What is cached changes the rate dramatically: caching a full free-text search query yields a poor hit rate; caching per-token posting lists reuses tokens. Write strategies divide into write-through (synchronous to cache and store, atomicity not guaranteed), write-back (cache first, data loss risk), and write-around (store first, populate cache on read miss). Liu recommends *delete* over *update* on cache invalidation because two concurrent database updates don't guarantee cache ordering, and delete is idempotent.

Invalidation — Phil Karlton's famous hard problem — has four main approaches: listener on source values (freshest, expensive), periodic recomputation (simpler, stale between runs), caching a lower layer and fanning in on read (used in Netflix recommendations and News Feed), and TTL (what DNS does because invalidating browser caches is impractical). Eviction policies — **LRU**, **LFU**, or custom domain-specific rules — trade off against query pattern. A crashed cache loses everything, which can flood the database and cause a **thundering herd**; redundancy options include periodic snapshots, a write-ahead log, no backup for transient data like driver locations, and replication. Thundering herd on a cold cache is mitigated by **cache blocking** — only one request fetches from the data source while the rest wait. And caches do not automatically improve bandwidth: streaming YouTube is network-bound, which is what CDNs solve.

### 4.3. Replication

Replication copies data across sources. Its benefits are availability, durability, latency, bandwidth, and throughput. Leader-follower sends writes to the leader and propagates to followers; synchronous replication guarantees follower freshness at the cost of speed and availability, while asynchronous replication introduces **replication lag** with two visible consequences: **read-your-own-write** (a user who writes to the leader and reads from a follower may feel the change didn't commit) and **inconsistent read from different read replicas** (round-robin reads return different results on successive calls).

Leader-leader keeps writes available when one leader dies but introduces conflict complexity. Leaderless replication uses quorum writes (`w` acknowledgments) and quorum reads (`r` acknowledgments); tuning so `w + r > n` gives stronger freshness guarantees than `w + r <= n`. It avoids leader election and keeps serving through node failures, at the cost of conflict resolution during quorum propagation. The industry average replication factor is 3.

### 4.4. Sharding

Sharding divides data across servers and applies to app servers and caches as well as storage. Benefits cover throughput, capacity, latency, and perceived availability — a failed shard only takes out its partition. Overall availability is *not* improved. Sharding is not the first resort: consider cold storage, compression, and batching first. Vertical sharding splits columns and is rare in interviews; horizontal sharding splits rows and is the default.

The sharding key can be hash-based (good distribution, bad for range queries) or range-based (efficient range queries, hot writes on time-ranges). **Consistent hashing** places nodes on a hash ring, routes each key to the next clockwise node, and uses **virtual nodes** so one failure's load is spread across several successors. Liu is explicit that it is *not* a silver bullet: it solves even distribution and migration minimization, but a super-hot key still hammers its shard. The interview rule is to know *when and why* to use it, not to retell the algorithm.

Sharding also applies to trees, graphs, and grids. Outlier keys (celebrities, enterprise customers, power users) overheat their shard regardless of scheme; remedies include dedicated shards or further sub-sharding with **scatter-gather**. Geo-shards add top-level zone routing and fall apart for social graphs where friends scatter across zones — the heuristic is that friends usually cluster geographically.

### 4.5. Concurrency and Transactions

Concurrency happens when multiple threads access and modify the same resource, and it is a strong interview signal precisely because most candidates avoid it. Canonical examples include the global counter (two threads read `x=1`, both increment, both persist `x=2`), ridesharing matches that assign the same driver to multiple riders, ticket booking, and meeting-room scheduling.

Serialization strategies run from single-thread (no concurrency, poor throughput) through single-thread micro-batching (amortizes IO, sacrifices freshness) to sharded serial processing. **Pessimistic locking** acquires a lock before the transaction — write locks block both readers and writers, read locks allow concurrent reads — and is preferred when QPS is low and correctness is critical. **Optimistic locking** uses a monotonically increasing version number (an **eTag**) checked at commit time; two readers at `v1` race, one commits to `v2`, the second fails and retries. It avoids lock overhead but retry storms under contention bubble up as poor UX. Lock scope spans database, table, row, and in-memory data structures. **Write skew with phantom data** occurs when the resource to lock doesn't exist as a row — booking a continuous time range, for instance. Remedies include scoping up to a broader row, predicate locks, or materializing the data (restricting bookings to 30-minute blocks), which changes the product requirement. That last move generalizes: when concurrency gets hairy, reframing the product can simplify both UX and tech.

### 4.6. Async, Batch, Stream, and Lambda

Asynchronous processing unblocks the caller by offloading work to a background process. The subtlety is "sync up to where?" — for an e-commerce checkout, scoping synchronicity to step 1 shows "we're processing your order" immediately, while scoping to step 2 gives faster feedback if payment fails.

Batch processing periodically grabs a data source, applies logic, and produces output. MapReduce is common but not required; interview prompts to surface are SLO violations if batches run late, missed output if they never run, idempotency if they run more than once, stuck jobs, resource contention, and overlapping logical runs.

Stream processing handles unbounded data with fresher output at higher complexity. **Event time** (when the event occurred) differs from **processing time** (when the system processed it). A **watermark** is a heuristic for "have I received enough data for this window to move on?" — a bigger watermark holds more memory but drops fewer late events. **Checkpointing** persists intermediate state so a failed host doesn't replay from the beginning, and micro-batching amortizes per-event IO overhead at the cost of delay.

Batch versus stream is a spectrum. Liu recommends batch over stream when data is enormous, processing is compute-intensive, streaming complexity outweighs freshness benefits, or the use case doesn't need freshness (daily payroll). **Lambda architecture** runs both — a fast lane for low-latency approximate results and a slow lane for accurate batch reconciliation — the right answer when the interviewer introduces a hypothetical that would break a pure stream design.

### 4.7. Queues and Messaging

Queues hold events waiting to be processed because processing is often slower than producing, and they protect downstream from thundering herds. A queue does not automatically make the flow asynchronous. Message queues (Kafka, Amazon Kinesis) are log-based with per-topic partitions, durable consumer offsets, and a retention window for replay — high-throughput but overkill for events like a ridesharing request where reprocessing a 10-minute-old request is pointless. Publisher-subscriber systems (RabbitMQ, Amazon SQS) push to each subscriber's queue and remove on acknowledgment — fitting when events should be consumed immediately.

Delivery semantics come in three flavors: **at-most-once** (fire-and-forget, highest throughput, occasional loss — metrics, driver location updates), **at-least-once** (producer retries on missing ack, may double-deliver — idempotent file parses, tolerable-duplicate notifications), and **exactly-once** (queue dedupes on an idempotent key, lowest throughput — payment to a third party that doesn't handle idempotency). Application-level exactly-once pairs at-least-once with a data store of processed events. Custom queue shapes — durable priority queue backed by a relational table, in-memory FIFO or max-heap queues — are fair game.

### 4.8. Conflict Resolution

When multiple writers hit the same key on different nodes under leaderless or leader-leader replication, the system must decide whose write sticks. **Last write wins** attaches a timestamp and drops the losing write; simple but lossy and subject to clock skew. A **CRDT** (**Conflict-Free Replicated Data Type**) has each node track its own count plus asynchronously-replicated counts from others, so any node computes a total by summing. The global distributed counter is the canonical example — CRDTs give high availability and low read latency at the cost of broadcast complexity and eventual consistency. Keeping records of conflict preserves all information at the cost of pushing resolution logic into readers. Custom resolution covers domain-specific cases, including the extreme of letting a human resolve it (source-control merge conflicts).

### 4.9. Resilience Patterns

Timeouts convert the uncertainty of a missing response into a decision; the trade-off is that longer timeouts waste resources on dead services while shorter ones give up on responses that would have arrived. Ideally the timeout equals the request's processing time, but that number is never known up front. Timeouts also drive service discovery and leader-health checks.

**Exponential backoff** with a maximum retry cap spaces retries progressively so struggling downstreams are not dog-piled; hitting the cap usually signals real failure. Buffering amortizes per-request overhead for throughput problems — emit metrics every second rather than per event — trading freshness for efficiency. Sampling trades accuracy for performance: persisting every fifth driver-location update cuts QPS and storage by 80%.

**Fail to open** keeps the user experience perceived as available when the ideal path is broken. If the payment processor is down, let the order through and collect later. Cassandra's **hinted handoff** is a storage analog: when a node is down, stash the write on a neighbor and transfer it back when the owner returns. A failing price estimator can fall back to a baseline price without the surge multiplier.

### 4.10. Distributed Transactions

A distributed transaction involves more than one data source, and the complexity is what happens on partial commit. In the money-transfer example, a two-phase commit — prepare, then commit — prevents inconsistency, though a downed coordinator renders the service unavailable. For blob plus metadata storage, the recommended approach is to persist the blob first (producing a URL), then persist metadata; a failed metadata write leaves an **unreferenced blob** a background cleanup can handle. For database-plus-queue inserts, some databases offer a transactional post-processing queue; otherwise, letting it be with a reconciliation job is acceptable when the failure rate is low. Write-through caches face the same issue: the cache may hold a value the underlying store never persisted. Liu's abstract framework asks, for any Service A and Service B, whether to call A then B, B then A, both concurrently, both through a coordinator, or both transactionally — and for each option, to walk through what happens on partial failure.

## 5. Specialized Toolbox Topics

A second tier of primitives shows up in specific question types.

### 5.1. Real-Time Data Updates

Short polling is wasteful; long polling works for simple notifications but carries complexity. Server-Sent Events (SSE) provide unidirectional server-to-client push. **WebSocket** is the bidirectional default. WebSockets are stateful — a connection is tied to a specific physical server by a four-tuple `(from_ip, from_port, to_ip, to_port)` — so they cannot be held at the app load balancer. A load balancer instead hands out endpoints of a WebSocket proxy farm where connections terminate. When a WebSocket server dies, its clients reconnect and can cause a thundering herd on survivors; server sizing trades blast radius against operational cost. Heartbeat pings with a `buffer_seconds` timeout detect dead connections.

### 5.2. ID Generation

Not every system needs globally-ordered, unique, 64-bit IDs. UUIDs are coordination-free and effectively unique but unordered and 128-bit. Single-database auto-increment is simple but neither scalable nor fault-tolerant. Partitioning auto-increment across machines (Flickr's odd/even) multiplies throughput but is inflexible. ZooKeeper-style linearizable generators emit monotonic 64-bit integers via `zxid` — the standard for fencing tokens and **Snowflake** machine IDs.

**Snowflake**, originally from Twitter, lays out 64 bits as timestamp, machine ID (10 bits, 1024 machines max, assigned by ZooKeeper), and sequence (12 bits, 4,096 IDs per millisecond per machine). Roughly ordered, unique, high-throughput, horizontally scalable — powering Twitter tweet IDs and Discord message-table cluster indexes. Offline generation pre-computes a pool for unusual formats (TinyURL's short codes). Custom IDs acknowledge that not every ID needs to be ordered, unique, or fixed-size.

### 5.3. Full-Text Search

Text-to-token preprocessing normalizes (lowercase, strip special chars), tokenizes, removes stop words, and applies stemming. The core index is a **reverse index** mapping each token to its **posting list** of document IDs. N-grams (bigrams like `"system design"` indexed alongside unigrams) let phrase queries hit one entry instead of intersecting two posting lists. Multi-term queries combine posting lists via k-way merge. **TF-IDF** is the canonical ranking algorithm — TF rises with in-document frequency, IDF with corpus rarity — and **Page Rank** extends the idea to webpages by propagating weight through inbound links. Pipeline architecture follows freshness: real-time uses stream processing, periodic uses batch, both uses lambda.

### 5.4. Data Transfer and Compression

Liu distinguishes **encoding** (raw → JPEG), **transcoding** (format → format), **compression** (any size reduction), and **codec** (the algorithm). Lossless compression — Run-Length Encoding turning `AAAABBBBBBBBBBBBBBBAAA` into `4A15B3A` — preserves the original at a modest ratio (~2 for images). Lossy compression — chroma subsampling — gives higher ratios (~20 for JPEG) at the cost of unrecoverable detail. Compression costs compute, influencing whether to encode client-side or server-side. Backend must support multiple formats; **adaptive bit rate (ABR)** dynamically adjusts quality to available bandwidth. Passing only needed data is complementary: server-side field filtering returns only requested fields, and the **rsync** approach hashes 2,048-byte chunks with MD5 and transmits only mismatched chunks, using a **rolling hash** to recompute chunk hashes by moving one byte forward at head and tail.

### 5.5. Networking, Gateways, and CDNs

Networking rarely gets deep trivia, but core concepts unlock geo-sharding, data-center failover, CDN routing, and WebSocket deep dives. A TCP connection is a four-tuple. DNS converts domain to IP with TTL caching; DNS round-robin is a simple load-balancing mechanism with the caveat that stale client caches can keep hitting a downed IP. Routing to the closest region uses either DNS routing or **anycast** edge routers (multiple edges share one IP; each internet router forwards toward the most optimal next hop). The private backbone between edge servers and data centers is company-owned and far more efficient than the public internet. OSI model relevance is mostly Layer 7 (HTTP, DNS) and Layer 4 (TCP for reliable one-to-one, UDP for one-to-many broadcasting where packet loss is tolerable — video streaming, heartbeats).

An **API gateway** sits in front of microservices with its own IP and is the natural home for rate limiting, IP blocklists, and TLS termination. A **CDN** caches static content at geographically distributed nodes, routed via anycast, helping latency (proximity), bandwidth (less data to origin), and availability (multi-region redundancy, cross-CDN failover). In deep dives, Liu pushes back on trivializing CDNs: candidates should raise what is worth storing, what happens on a miss, how nodes stay updated, how content is prepopulated (Netflix predicts regional demand), and whether data differs by region.

Service discovery handles routing to healthy nodes within a pool (load balancing, round-robin or health-aware) and to the right shard (mapping request attributes to a shard and node, typically stored in ZooKeeper). A client can route via a central service (simple, extra hop) or fetch the mapping at startup and cache it locally (lower latency, config drift).

### 5.6. Cold Storage, Monitoring, Security, Product

Recent data is accessed more often than old data. Moving infrequently accessed data from **hot storage** to **cold storage** exploits that skew and is the direct answer to unbounded-growth prompts. Monitoring surfaces because systems don't auto-adjust; naming metrics worth tracking for the specific design (latency, QPS, error rate, storage runway, product-specific signals like order drops or queue backlog) signals on-call awareness.

Security rarely drives a generalist design. API security is the exception: think through the worst thing a malicious user could do against each API — `transfer_money(amount, user_id, to_user_id)` lets any client set the user IDs unless validated; `upload_photo` must defend against malicious bytes; `request_ride` must defend against phantom rides. Man-in-the-middle attacks are mitigated by TLS; the interviewer rarely quizzes the key-exchange steps. OAuth-style tokens with periodic refresh limit the blast radius of a compromised credential.

Finally, not every problem is solved with more infrastructure. User empathy is a seniority signal. For drivers in poor-reception areas, the engineering-only answer is heartbeats marking the driver offline — correct but cold; the product-aware answer also surfaces known poor-reception regions in the app. For ridesharing, fanning a ride request to three drivers introduces acceptance races; redesigning so the backend auto-assigns yields the same UX with dramatically simpler tech. When technical complexity gets hairy, ask whether the product requirement can change.

## 6. Communication Discipline

The interview is heavily about how ideas are presented. Poor pacing makes the interviewer switch off like someone falling asleep in a dull talk. Confidence is signaled by framing: "Do you think this design would work?" reads as asking for hints. Better framing offers options and trade-offs and closes with a pick: "Here are the options and trade-offs I can think of and I would pick option 1 because of the assumptions. Is there any direction you would like me to go into?" Asking for a hint when genuinely stuck is fine; sounding unsure while holding reasonable options is what hurts.

Driving the conversation is a leadership signal — the candidate does most of the talking and steers toward areas of strength — but yielding when redirected is equally important. Talking over the interviewer blocks the candidate from hearing what is really being evaluated. When asked "tell me more about the queue," the scoped-response pattern offers a menu ("Would you like me to discuss what kind of queue and why, or talk about scalability?"), justifies, and checks direction. Justifying designs is the majority of what is evaluated: "I will use a wide-column store" is weak; tying the choice to a 100k write QPS ratio and time-series disk locality is strong. Reciting how WebSocket works is an encyclopedia entry unless it is applied to a design choice.

Scope discipline means narrowing requirements rather than sweeping shallowly. Candidates who over-studied — naming **EdgeRank** signals for Facebook affinity, weight, and decay — can complicate the interview unnecessarily. Better: "I know Facebook uses EdgeRank; for now we'll assume scores are computed and stored." A private messaging design shouldn't burn ten minutes on OAuth 2.0. Math is used with purpose — "QPS is 100k, so we'll need to scale app servers since each handles ~30k QPS" — and never done before API and schema. Canned real-world answers are rejected: applying Cassandra with Snowflake because "that's a well-known design" fails as soon as the interviewer changes an assumption the canned design didn't cover.

Handling disagreement is part of the formula. Disagreements usually stem from different assumptions; neutralizing by addressing the root — "we can A/B test location-update frequency and monitor customer feedback" — is more effective than arguing the surface claim. Keep a backbone: back each stance with strong justifications, but don't make the interviewer look bad. Every deep dive ends in a stance. "It really depends on the use cases" is not a conclusion — senior engineers must deal with ambiguity and commit.

## 7. The Interviewer's Perspective

Liu gives candidates a window into how the rubric works. Level terminology is company-agnostic: Level 2 is 2–5 years of experience, Level 3 is 5–10, Level 4 is 10+. Performance runs from "No Hire" through Level 4; a Level 3 target performing at Level 2 may be down-leveled, and Level 4 targets that perform at Level 2 or below are likely rejected. Junior candidates often outperform senior candidates because they prepare harder.

The same four-tier structure repeats across every step of the framework. The rising axis is consistent: less guidance needed, more trade-offs surfaced proactively, more tying of decisions back to requirements, more awareness of what *not* to include. "No Hire" signals are also consistent — no clarifying questions, no understanding after hints, buzzword answers without internals, designs that fail the requirement even after pointers. Level 4 signals add cost-awareness (understanding why some components are *not* needed and removing unnecessary elements) and proactive listing of all critical trade-offs with alternatives in case requirements change.

## 8. Patterns from the Worked Examples

The eight case studies — ridesharing, top YouTube video, emoji broadcasting, Instagram, distributed counter, cloud file storage, rate limiter, chat — are not meant to be memorized; they illustrate how the framework and toolbox compose under different constraints.

Every case begins the same way: narrow the prompt, agree explicit assumptions about DAU, distribution, bursty traffic, and the dominant non-functional constraint (availability for ridesharing, freshness for emoji broadcasting, durability for Instagram, long-horizon accuracy for the rate limiter). The API is minimal — two or three signatures — and output shape is called out when it changes the design.

Bursty-traffic deep dives follow the same math template: DAU × per-user rate × peak multiplier, divided by 10⁵ seconds. Ridesharing's 100M DAU × 2 rides × 10× peak becomes 20,000 peak QPS on an expensive matching calculation; the distributed counter's 500M DAU × 10 videos × 10× peak becomes 500,000 QPS and exposes hot-key contention at 0.1% traffic. High-write-throughput questions converge on the same move: a queue absorbs the spike, an aggregator processes in micro-batches, and the durable store is reached only after a cache-like layer. Ridesharing uses a cache-backed location store with leaderless replication; top YouTube video routes through a queue to an aggregator that builds in-memory minute segments with a min-heap of size K; emoji broadcasting does the same with a fan-out service and connection storage; the distributed counter uses a CRDT; the rate limiter uses a write-back cache with async replication.

Long-tail distributions surface in nearly every case — celebrity videos, hot channels, super-users. The Instagram feed converges on a **hybrid fan-out + fan-in**: fan-out on write for non-celebrities, fan-in on read for celebrities. Emoji broadcasting layers client-side sampling plus aggregated "emoji confetti" rendering so a celebrity stream with tens of millions of concurrent watchers does not turn every device into a grid of icons. Geo-distribution is usually solved with replication rather than cross-region reads: Instagram replicates feed storage cross-region; emoji broadcasting forwards each emoji to all three regions because the intra-regional savings of a global connection store don't justify cross-region coordination.

Concurrency is handled pragmatically. Ridesharing picks serial batch with a dispatcher over locks because retry storms would be worse than batch tuning. Chat picks server-generated millisecond timestamps as the source of truth for ordering, accepting rare collisions because concurrent messages have no semantic relationship to each other anyway. Cloud file storage uses optimistic locking with an explicit conflict message.

Database choice follows category reasoning. Chat picks Cassandra-style leaderless wide-column because writes dominate and edits/deletes were tabled. Cloud file storage picks MySQL because cross-row transactions and join/union on `parent_folder_id` matter. Top YouTube video mentions **Count-Min Sketch** as an option — Liu's warning is that advanced structures are a plus only when the candidate knows the internals, and a one-sentence dismissal is acceptable otherwise. **HyperLogLog** appears in the distributed counter's "unique users" variant because the 50 TB exact-set cost collapses to 1 GB probabilistic cost. The **QuadTree** appears in ridesharing as the in-memory geo-index; Google S2 is the production equivalent but not required. Checkpoint strategies combine local disk for speed with distributed stores for correlated-failure survival.

A recurring move is *do nothing* when the event is rare and user impact is mild: Instagram's duplicate-posts-on-celebrity-promotion, the rate limiter's replication-lag inaccuracy, the chat app's rare inconsistency between notified and persisted messages. Another is reframing the product when engineering gets tangled: ridesharing's driver acceptance race is solved not by locks but by changing the product so the backend auto-assigns; emoji broadcasting's 10M-emoji flood is solved by sampling plus UI-level confetti. These moves are not engineering shortcuts — they are the senior-level signal Liu wants candidates to show.

## 9. Key Takeaways

- **Problem first, solution second.** The golden question — "What is the problem I am trying to solve?" — filters out buzzword-driven answers. Concluding no problem exists is a positive signal.
- **Follow the six-step framework top-down.** Requirements, API, high-level diagram, schema, end-to-end flow, deep dive. Math goes after API and schema. Don't skip the end-to-end flow checkpoint.
- **Run the magic formula during deep dives.** Identify a bottleneck, list options, discuss trade-offs against requirements, pick one with justification, active discussion, repeat.
- **Justify, don't name-drop.** Name the technology *and* tie the choice to write/read ratios, latency targets, durability needs. Reciting how a technology works is not a replacement for tying it to a design choice.
- **Non-functional requirements drive the design.** Scale, consistency, availability, latency, freshness, accuracy, durability. Most of the gathering time belongs here, and every deep-dive choice should tie back.
- **Sharding, replication, caching, queues, and CRDTs are the recurring primitives.** Know their failure modes — thundering herd on WebSocket death, replication lag, cache invalidation, retry storms under optimistic locking.
- **Consistent hashing is not a silver bullet.** It solves even distribution and migration minimization; it does not solve hot keys.
- **Long-tail distributions are everywhere.** Celebrity followers, hot videos, popular channels, super-users. Hybrid fan-out/fan-in, sub-sharding, sampling, and aggregated UI rendering are the standard responses.
- **Change the product when the tech gets hairy.** Auto-assign rather than let the user pick; render emoji confetti rather than every tap; materialize 30-minute booking slots rather than lock continuous ranges.
- **Communication is half the interview.** Take a stance, drive but listen, handle disagreement by addressing assumption mismatches, scope the response to what the interviewer asked, and table interesting discussion points for the deep-dive phase.
