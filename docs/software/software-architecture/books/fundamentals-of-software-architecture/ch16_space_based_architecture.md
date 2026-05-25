# Ch 16: Space-Based Architecture Style

## Table of Contents

- [1. Driving Problem and Philosophy](#1-driving-problem-and-philosophy)
- [2. Topology and Primary Artifacts](#2-topology-and-primary-artifacts)
- [3. Processing Unit and Virtualized Middleware](#3-processing-unit-and-virtualized-middleware)
- [4. Data Grid and Caching Models](#4-data-grid-and-caching-models)
- [5. Data Pumps, Writers, and Readers](#5-data-pumps-writers-and-readers)
- [6. Data Topologies and Cloud Considerations](#6-data-topologies-and-cloud-considerations)
- [7. Common Risks](#7-common-risks)
- [8. Governance](#8-governance)
- [9. Team Topology Considerations](#9-team-topology-considerations)
- [10. Style Characteristics](#10-style-characteristics)
- [11. Examples and Use Cases](#11-examples-and-use-cases)

## 1. Driving Problem and Philosophy

- **The bottleneck cascade** — request flow from browser to web server to application server to database creates a triangle topology. Scaling out web servers is cheap and easy; the bottleneck moves to app servers; scaling those moves it to the database, which is hardest and most expensive to scale.
- **Database as the synchronous constraint** — in any high-volume application the database is the final limiting factor on concurrent transactions; caching products and DB-scaling tools only stretch this so far.
- **Solve scale architecturally, not by retrofitting** — space-based architecture is designed for high scalability, elasticity, and concurrency, especially for variable and unpredictable user loads.
- **Tuple space inspiration** — the name comes from **tuple space**, the technique of multiple parallel processors communicating through shared memory. Space-based systems replace the central database (as a synchronous constraint) with replicated in-memory data grids.
- **Asynchronous DB writes** — when a processing unit updates data, it asynchronously sends that data to the database through a data pump (usually messaging with persistent queues). Processing units start and stop dynamically with load.

## 2. Topology and Primary Artifacts

- **Processing units** — contain the application functionality.
- **Virtualized middleware** — infrastructure-related artifacts that manage and coordinate the processing units.
- **Messaging grid** — manages input requests and session state.
- **Data grid** — manages synchronization and replication of data between processing units.
- **Processing grid** — manages request orchestration when multiple processing units are involved.
- **Deployment manager** — manages dynamic startup and tear-down of processing-unit instances based on load.
- **Data pumps** — asynchronously send updated data to the database.
- **Data writers** — perform the database updates from data-pump messages.
- **Data readers** — read database data and deliver it to processing units on startup or recovery.

## 3. Processing Unit and Virtualized Middleware

- **Processing unit contents** — application logic (web components plus backend business logic), an in-memory data grid, and a replication engine. Implementations include **Hazelcast**, **Apache Ignite**, and **Oracle Coherence**.
- **Granularity** — small applications deploy as a single processing unit; larger ones split by functional area; processing units can also be small, single-purpose services (microservices-like).
- **Virtualized middleware** — at minimum a **messaging grid**, **data grid**, and **deployment manager**; optionally a **processing grid** for multi-unit orchestration. Architects can add security, metrics, and other infrastructure functions. Implemented by stitching together third-party products (web servers, caches, load balancers, service orchestrators, deployment managers).
- **Messaging grid behavior** — when a request arrives the messaging grid picks an available processing unit (round-robin or next-available) and forwards. Typically a load-balancing web server such as HAProxy or Nginx.
- **Processing grid behavior** — modern implementations favor fine-grained **orchestration processing units**, each handling one major workflow (e.g., an *Order Placement Orchestrator* coordinating *Order Placement*, *Payment*, and *Inventory Adjustment*) instead of one coarse-grained engine.
- **Deployment manager** — continuously monitors response times and load, starts and stops processing units accordingly. Cloud infrastructure or **Kubernetes** typically fills this role.

## 4. Data Grid and Caching Models

- **Why critical** — because the messaging grid can route any request to any processing unit, every processing unit's in-memory data grid must contain *exactly the same data*. Replication is asynchronous, typically completing in under 100 ms.
- **Named cache synchronization** — same-named caches in different processing units stay in sync via the caching product (e.g., Hazelcast `getReplicatedMap`). New instances broadcast for joiners; one peer ships the cache to the new instance so it's pre-warmed without hitting the database.
- **Member list** — each processing unit holds a member list of IPs and ports for all other processing-unit instances sharing the same named cache; the list updates automatically as instances join or leave.
- **Replicated caching** — each processing unit holds its own in-memory cache; updates fan out to all peers. Extremely fast and fault-tolerant (no single point of failure).
- **Distributed caching** — an external server holds a centralized cache; processing units fetch data via a proprietary protocol. Offers strong consistency but higher latency and a single point of failure (mitigable by mirroring).
- **Replicated vs. distributed cache trade-offs:**

| Decision criteria | Replicated cache | Distributed cache |
|---|---|---|
| Optimization | Performance | Consistency |
| Cache size | Small (<100 MB) | Large (>500 MB) |
| Type of data | Relatively static | Highly dynamic |
| Update frequency | Relatively low | High update rate |
| Fault tolerance | High | Low |

- **Use both** — different processing units can mix models: distributed cache for inventory (consistency); replicated cache for customer profile (performance and fault tolerance).
- **Near-cache (not recommended)** — hybrid model with a **full backing cache** (distributed) and a **front cache** (in-memory grid per processing unit), with eviction policies (most recently used, most frequently used, random replacement). Front caches are kept in sync with the backing cache but *not* with each other, producing inconsistent performance and data across processing units.

## 5. Data Pumps, Writers, and Readers

- **Data pump** — sends data to a downstream processor (the data writer) for eventual database update. Always asynchronous, providing eventual consistency between cache and database. The processing-unit instance that updates the cache becomes the owner of the update and is responsible for sending it through the data pump.
- **Messaging implementation** — pumps are typically messaging-based, giving guaranteed delivery, message persistence, and FIFO order. Decouples the processing unit from the data writer.
- **Multiple pumps** — usually one per domain or subdomain (Customer, Inventory), per cache type (`CustomerProfile`, `CustomerWishlist`), or per processing-unit domain.
- **Pump contracts** — JSON, XML, an object, or a **value-driven message** (map of name/value pairs). Updates send only changed values plus an action (add, delete, update).
- **Data writers** — accept pump messages and update the database. Implemented as services, applications, or data hubs (e.g., **Ab Initio**).
  - **Domain-based data writer** — one writer per domain, listens to all pumps in the domain (e.g., one customer writer for `Profile`, `WishList`, `Wallet`, `Preferences` pumps).
  - **Dedicated data writer** — one writer per processing unit; produces more components but better scalability and agility.
- **Data readers** — read from the database and deliver data to processing units via a **reverse data pump** (a separate queue). Invoked only in three situations: all instances of a named cache crash; all instances of a named cache redeploy; archive data not in the cache must be retrieved.
- **Cold-start flow** — restarting instances race to grab a cache lock; the winner becomes temporary cache owner, requests data via a queue, the data reader runs the SQL and returns rows on the reverse data pump; the temporary owner loads the cache then releases the lock; remaining instances synchronize.
- **Data abstraction layer** — readers and writers together form a **data abstraction layer** (or data access layer). The abstraction layer decouples processing-unit cache schemas from database schemas via separate contracts; readers and writers contain transformation logic so incremental DB changes (column type, dropped column, dropped table) can be buffered.

## 6. Data Topologies and Cloud Considerations

- **DB topology flexibility** — because processing units don't read or write to the database synchronously, request processing is largely DB-independent and the architect has wide topology choice.
- **Choice drivers** — how the system uses the backing database. Reporting and analytics may favor a monolithic DB unless a data mesh is used (then domain-based). A monolithic DB can become a synchronization bottleneck; a domain-based DB may sync faster if data partitions cleanly. Downstream consumers may push you back toward monolithic.
- **Cloud and hybrid deployment** — the entire architecture can run in the cloud, fully on-prem, or split: processing units and virtualized middleware in cloud, databases on-prem. The asynchronous data pumps and eventual-consistency model make hybrid effective — transactional processing happens in elastic cloud environments while physical data, reporting, and analytics stay on-prem.

## 7. Common Risks

- **Frequent reads from the database** — defeats the architecture. DB reads should occur only for archived data or **cold-starting** a processing unit. Frequent crashes, redeployments, or large archives may indicate the wrong style for the domain.
- **Data synchronization and consistency** — pump bottlenecks delay the DB write, hurting downstream systems that need fresh data. Mitigate data loss with **persisted queues** (queue contents stored on disk and in memory) plus client-acknowledgment mode, but both slow responsiveness and degrade consistency.
- **High data volumes** — all transactional memory is cached in processing units; cache size must remain low to avoid out-of-memory crashes, especially as instances multiply.
- **Data collisions** — when one cache (A) updates the same row as another cache (B) before replication completes, both caches end up inconsistent. Occurs in active/active replicated caching when the update rate exceeds **replication latency (RL)**.
- **Inventory collision example** — both A and B start at 500. A processes a 10-unit purchase to 490. Before replicating, B processes a 5-unit purchase to 495. Replication then writes A's 490 over B and B's 495 over A. Final state: 490 and 495; correct value: 485.
- **Collision rate formula** — `Collision Rate = N * (UR² / S) * RL`, where `N` is instance count, `UR` is updates/second (squared), `S` is cache size in rows, `RL` is replication latency in ms. Used to estimate collision percentage.

| Scenario | UR | N | S | RL | Updates/hr | Collisions/hr | Percentage |
|---|---|---|---|---|---|---|---|
| Base | 20/s | 5 | 50,000 | 100 ms | 72,000 | 14.4 | 0.02% |
| Faster replication | 20/s | 5 | 50,000 | 1 ms | 72,000 | 0.1 | 0.0002% |
| Fewer instances | 20/s | 2 | 50,000 | 100 ms | 72,000 | 5.8 | 0.008% |
| Smaller cache | 20/s | 5 | 10,000 | 100 ms | 72,000 | 72.0 | 0.1% |

- **Cache size is inversely proportional to collisions** — smaller caches collide more often. Plan for minimum, normal, and peak update rates.

## 8. Governance

- **Memory consumption fitness function** — given the style's heavy memory usage, write a continuous fitness function to make each processing unit's memory consumption observable; pair with a fitness function that records instance counts to compute total memory per processing unit.
- **Synchronization-time fitness function** — track how long a cache update takes to reach the database. Each processing unit streams the request ID and timestamp on update; each data writer streams the same ID and timestamp after DB commit. The fitness function correlates IDs and subtracts timestamps, reporting atomically or in aggregate to track architectural change effects against business sync-time goals.
- **Data-pump bottleneck fitness function** — pumps are backpressure points and DB writes outpace cache writes, so pumps can bottleneck. Track queue depth per pump or aggregate; high queue depths increase synchronization time, data loss risk, and data collisions during peak load.
- **Other useful fitness functions** — frequency of reads to data readers (signals scalability/elasticity erosion); direct measurement of scalability, elasticity, and responsiveness, since those are the architecture's reasons to exist.

## 9. Team Topology Considerations

- **Technically partitioned** — the architecture is largely technically partitioned (functionality, pumps, readers, writers, DB). It works best with technically partitioned teams aligned to those areas, though domain-aligned cross-functional teams can still succeed.
- **Stream-aligned teams** — struggle as system size grows, because a stream change can ripple across processing units, pumps, readers, writers, cache contracts, orchestrators, and the DB.
- **Enabling teams** — fit well; pumps, readers, writers, and virtualized middleware are often shared/cross-cutting and benefit from a dedicated team optimizing them.
- **Complicated-subsystem teams** — fit well for the data grid or data-pump artifacts; data collisions and async-sync errors in data writers are good candidates for this topology.
- **Platform teams** — useful when pumps and virtualized middleware are treated as platform; common tools, services, APIs, and tasks help all developers.

## 10. Style Characteristics

- **Five-star drivers** — elasticity, scalability, performance. In-memory caching plus removing the DB as a constraint allows millions of concurrent users.
- **One-star testability** — simulating hundreds of thousands of concurrent users at peak load is complex and expensive; high-volume testing usually has to happen in production with real load.
- **Cost** — relatively expensive due to overall complexity, caching-product licensing, and the cloud or on-prem resource utilization needed for high scalability and elasticity.
- **Simplicity trade-off** — caching, eventual consistency, and many moving parts make the architecture very complicated.
- **Partitioning** — technically partitioned: any given domain spans processing units, pumps, readers, writers, and the DB.
- **Quanta** — the database is not part of the quantum equation because processing units don't communicate synchronously with it; quanta are delineated by associations between UIs and processing units. Synchronously communicating processing units (or those orchestrated through the processing grid) belong to the same quantum.

## 11. Examples and Use Cases

- **Suitability** — applications with high spikes in user/request volume and throughput exceeding 10,000 concurrent users. Two canonical examples: online concert ticketing and online auction systems.
- **Concert ticketing system** — concurrent volume is low until a popular concert is announced, then spikes from hundreds to tens of thousands as everyone races for good seats; tickets sell out in minutes. A central database can't survive the synchronous load. The deployment manager spins up many processing units on demand, ideally pre-warmed shortly before tickets go on sale.
- **Online auction system** — like ticketing, unpredictable spikes when an auction starts and an unknown number of bidders. Individual processing units can be devoted to each auction for bidding consistency. Asynchronous data pumps stream bidding data to bid history, bid analytics, and auditing without latency, increasing bidding-process performance.
- **Specialized style** — the only architecture that maximizes the combination of responsiveness, scalability, and elasticity, primarily because of caching and the absence of direct database access. Used where those characteristics must be maximized.
