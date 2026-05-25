# Space-Based Architecture

> *Fundamentals* Ch 16 is the sole source. Space-based is a *specialist* style — the only architecture that maximizes the combination of responsiveness, scalability, and elasticity, primarily because of in-memory caching and the absence of direct database access in the request path. *The Hard Parts* doesn't address it. Used where unpredictable user volume spikes would crush a database — online concert ticketing, auctions.

## Table of Contents

- [1. Driving Problem](#1-driving-problem)
- [2. Topology and Primary Artifacts](#2-topology-and-primary-artifacts)
- [3. Processing Units and Virtualized Middleware](#3-processing-units-and-virtualized-middleware)
- [4. Data Grid — Replicated vs. Distributed Cache](#4-data-grid--replicated-vs-distributed-cache)
- [5. Data Pumps, Writers, and Readers](#5-data-pumps-writers-and-readers)
- [6. Data Collisions](#6-data-collisions)
- [7. Data Topology and Cloud Considerations](#7-data-topology-and-cloud-considerations)
- [8. When to Use and When Not To](#8-when-to-use-and-when-not-to)
- [9. Risks and Antipatterns](#9-risks-and-antipatterns)
- [10. Architecture Characteristic Ratings](#10-architecture-characteristic-ratings)
- [11. Examples](#11-examples)
- [Sources](#sources)

## 1. Driving Problem

Request flow from browser → web server → application server → database creates a triangle topology. Scaling out web servers is cheap and easy; the bottleneck moves to app servers; scaling those moves it to the database, which is hardest and most expensive to scale.

> **Solve scale architecturally, not by retrofitting.** Space-based architecture is designed from the ground up for high scalability, elasticity, and concurrency, especially for variable and unpredictable user loads.

The name comes from **tuple space** — the technique of multiple parallel processors communicating through shared memory. Space-based systems replace the central database (as a synchronous constraint) with **replicated in-memory data grids**. When a processing unit updates data, it asynchronously sends that data to the database through a *data pump* (usually messaging with persistent queues). Processing units start and stop dynamically with load.

## 2. Topology and Primary Artifacts

| Artifact | Role |
|---|---|
| **Processing units** | Contain the application functionality. |
| **Virtualized middleware** | Infrastructure-related artifacts that manage and coordinate the processing units. |
| **Messaging grid** | Manages input requests and session state. |
| **Data grid** | Manages synchronization and replication of data between processing units. |
| **Processing grid** | (Optional) Manages request orchestration when multiple processing units are involved. |
| **Deployment manager** | Manages dynamic startup and tear-down of processing-unit instances based on load. |
| **Data pumps** | Asynchronously send updated data to the database. |
| **Data writers** | Perform the database updates from data-pump messages. |
| **Data readers** | Read database data and deliver it to processing units on startup or recovery. |

## 3. Processing Units and Virtualized Middleware

**Processing unit contents:** application logic (web components plus backend business logic), an in-memory data grid, and a replication engine. Implementations include **Hazelcast**, **Apache Ignite**, and **Oracle Coherence**.

**Granularity.** Small applications deploy as a single processing unit; larger ones split by functional area; processing units can also be small, single-purpose services (microservices-like).

**Virtualized middleware.** At minimum a messaging grid, data grid, and deployment manager; optionally a processing grid for multi-unit orchestration. Architects can add security, metrics, and other infrastructure functions. Implemented by stitching together third-party products (web servers, caches, load balancers, service orchestrators, deployment managers).

| Subsystem | Typical implementation |
|---|---|
| **Messaging grid** | Load-balancing web server such as HAProxy or Nginx. When a request arrives, picks an available processing unit (round-robin or next-available) and forwards. |
| **Processing grid** | Modern implementations favor fine-grained *orchestration processing units*, each handling one major workflow (an `Order Placement Orchestrator` coordinating `Order Placement`, `Payment`, and `Inventory Adjustment`) instead of one coarse-grained engine. |
| **Deployment manager** | Continuously monitors response times and load; starts and stops processing units accordingly. Cloud infrastructure or **Kubernetes** typically fills this role. |

## 4. Data Grid — Replicated vs. Distributed Cache

Because the messaging grid can route any request to any processing unit, every processing unit's in-memory data grid must contain **exactly the same data**. Replication is asynchronous, typically completing in under 100 ms.

- **Named cache synchronization.** Same-named caches in different processing units stay in sync via the caching product (e.g., Hazelcast `getReplicatedMap`). New instances broadcast for joiners; one peer ships the cache to the new instance so it's pre-warmed without hitting the database.
- **Member list.** Each processing unit holds a member list of IPs and ports for all other instances sharing the same named cache; the list updates automatically as instances join or leave.

Two caching models:

| Decision criteria | Replicated cache | Distributed cache |
|---|---|---|
| **Optimization** | Performance | Consistency |
| **Cache size** | Small (< 100 MB) | Large (> 500 MB) |
| **Type of data** | Relatively static | Highly dynamic |
| **Update frequency** | Relatively low | High update rate |
| **Fault tolerance** | High | Low |

| Model | Mechanism |
|---|---|
| **Replicated cache** | Each processing unit holds its own in-memory cache; updates fan out to all peers. Extremely fast and fault-tolerant (no single point of failure). |
| **Distributed cache** | An external server holds a centralized cache; processing units fetch data via a proprietary protocol. Strong consistency but higher latency and a single point of failure (mitigable by mirroring). |

Different processing units can **mix models**: distributed cache for inventory (consistency); replicated cache for customer profile (performance and fault tolerance).

> **Near-cache (not recommended).** Hybrid model with a *full backing cache* (distributed) and a *front cache* (in-memory grid per processing unit) with eviction policies. Front caches stay in sync with the backing cache but *not* with each other, producing inconsistent performance and data across processing units.

## 5. Data Pumps, Writers, and Readers

**Data pump.** Sends data to a downstream processor (the data writer) for eventual database update. **Always asynchronous**, providing eventual consistency between cache and database. The processing-unit instance that updates the cache becomes the owner of the update and is responsible for sending it through the data pump.

- Pumps are typically messaging-based, giving guaranteed delivery, message persistence, and FIFO order.
- Multiple pumps are usually one per domain or subdomain (Customer, Inventory), per cache type (`CustomerProfile`, `CustomerWishlist`), or per processing-unit domain.
- Pump contracts: JSON, XML, an object, or a **value-driven message** (map of name/value pairs). Updates send only changed values plus an action (add, delete, update).

**Data writers.** Accept pump messages and update the database. Implemented as services, applications, or data hubs (e.g., **Ab Initio**).

| Writer model | Behavior |
|---|---|
| **Domain-based** | One writer per domain, listens to all pumps in the domain (e.g., one customer writer for `Profile`, `WishList`, `Wallet`, `Preferences` pumps). |
| **Dedicated** | One writer per processing unit; more components but better scalability and agility. |

**Data readers.** Read from the database and deliver data to processing units via a *reverse data pump* (a separate queue). Invoked only in three situations:

1. All instances of a named cache crash.
2. All instances of a named cache redeploy.
3. Archive data not in the cache must be retrieved.

**Cold-start flow.** Restarting instances race to grab a cache lock; the winner becomes temporary cache owner, requests data via a queue, the data reader runs SQL and returns rows on the reverse pump; the temporary owner loads the cache then releases the lock; remaining instances synchronize.

**Data abstraction layer.** Readers and writers together form a data abstraction layer that decouples processing-unit cache schemas from database schemas via separate contracts; readers and writers contain transformation logic so incremental DB changes (column type, dropped column, dropped table) can be buffered.

## 6. Data Collisions

When one cache (A) updates the same row as another cache (B) before replication completes, both caches end up inconsistent. Occurs in active/active replicated caching when the update rate exceeds **replication latency (RL)**.

**Inventory collision example.** Both A and B start at 500. A processes a 10-unit purchase to 490. Before replicating, B processes a 5-unit purchase to 495. Replication then writes A's 490 over B *and* B's 495 over A. Final state: 490 and 495; correct value: 485.

> **Collision rate formula.** `Collision Rate = N × (UR² / S) × RL`
>
> where `N` is instance count, `UR` is updates/second (squared), `S` is cache size in rows, `RL` is replication latency in ms.

| Scenario | UR | N | S | RL | Updates/hr | Collisions/hr | Percentage |
|---|---|---|---|---|---|---|---|
| Base | 20/s | 5 | 50,000 | 100 ms | 72,000 | 14.4 | 0.02% |
| Faster replication | 20/s | 5 | 50,000 | 1 ms | 72,000 | 0.1 | 0.0002% |
| Fewer instances | 20/s | 2 | 50,000 | 100 ms | 72,000 | 5.8 | 0.008% |
| Smaller cache | 20/s | 5 | 10,000 | 100 ms | 72,000 | 72.0 | 0.1% |

> **Cache size is inversely proportional to collisions.** Smaller caches collide more often. Plan for minimum, normal, and peak update rates.

## 7. Data Topology and Cloud Considerations

Because processing units don't read or write to the database synchronously, request processing is largely DB-independent and the architect has wide topology choice. Choice drivers: how the system uses the backing database. Reporting and analytics may favor a monolithic DB unless a data mesh is used (then domain-based); downstream consumers may push you back toward monolithic.

The entire architecture can run in the cloud, fully on-prem, or **split** — processing units and virtualized middleware in the cloud, databases on-prem. Async data pumps and eventual consistency make hybrid effective: transactional processing happens in elastic cloud environments while physical data, reporting, and analytics stay on-prem.

## 8. When to Use and When Not To

**When to use:**

- Throughput exceeding 10,000 concurrent users.
- High, unpredictable spikes in user/request volume.
- Variable load patterns (concert ticketing, online auctions, flash sales).
- Domains where database scale is the binding constraint.

**When not to use:**

- Steady, predictable workloads where simpler styles suffice.
- Strong consistency requirements that can't tolerate eventual consistency.
- Small or budget-constrained projects — the licensing for caching products and the resource cost for high elasticity make this an expensive style.
- Teams without operational maturity for caching, persisted queues, and active/active data grids.

## 9. Risks and Antipatterns

- **Frequent reads from the database** defeat the architecture. DB reads should occur only for archived data or **cold-starting** a processing unit. Frequent crashes, redeployments, or large archives may indicate the wrong style for the domain.
- **Data synchronization and consistency.** Pump bottlenecks delay the DB write, hurting downstream systems that need fresh data. Mitigate data loss with **persisted queues** (queue contents stored on disk and in memory) plus client-acknowledgment mode, but both slow responsiveness and degrade consistency.
- **High data volumes.** All transactional memory is cached in processing units; cache size must remain low to avoid out-of-memory crashes, especially as instances multiply.
- **Data collisions** — see [§ 6](#6-data-collisions).
- **Near-cache** model produces inconsistent performance and data; avoid.

Governance fitness functions:

- **Memory consumption** — track per processing unit; pair with instance counts to compute total memory.
- **Synchronization time** — track how long a cache update takes to reach the database. Each processing unit streams the request ID and timestamp on update; each data writer streams the same ID and timestamp after DB commit. The fitness function correlates IDs and subtracts timestamps.
- **Data-pump bottleneck** — track queue depth per pump or aggregate; high queue depths increase sync time, data-loss risk, and collisions during peak load.
- **Frequency of reads to data readers** — signals scalability/elasticity erosion.
- Direct measurement of scalability, elasticity, and responsiveness, since those are the architecture's reasons to exist.

## 10. Architecture Characteristic Ratings

- **Elasticity ★★★★★, scalability ★★★★★, performance ★★★★★.** In-memory caching plus removing the DB as a constraint allows millions of concurrent users.
- **Testability ★.** Simulating hundreds of thousands of concurrent users at peak load is complex and expensive; high-volume testing usually has to happen in production with real load.
- **Cost.** Relatively expensive due to overall complexity, caching-product licensing, and the cloud or on-prem resources needed for high scalability and elasticity.
- **Simplicity trade-off.** Caching, eventual consistency, and many moving parts make the architecture very complicated.
- **Partitioning.** Technically partitioned — any given domain spans processing units, pumps, readers, writers, and the DB.
- **Quanta.** The database is not part of the quantum equation because processing units don't communicate synchronously with it; quanta are delineated by associations between UIs and processing units. Synchronously communicating processing units (or those orchestrated through the processing grid) belong to the same quantum.

## 11. Examples

The only architecture that maximizes the combination of responsiveness, scalability, and elasticity. Two canonical examples:

- **Concert ticketing system.** Concurrent volume is low until a popular concert is announced, then spikes from hundreds to tens of thousands as everyone races for good seats; tickets sell out in minutes. A central database can't survive the synchronous load. The deployment manager spins up many processing units on demand, ideally pre-warmed shortly before tickets go on sale.
- **Online auction system.** Like ticketing, unpredictable spikes when an auction starts and an unknown number of bidders. Individual processing units can be devoted to each auction for bidding consistency. Asynchronous data pumps stream bidding data to bid history, bid analytics, and auditing without latency.

## Granularity and Data Ownership

The granularity question in space-based becomes "how do I size the processing unit?" — answered by the disintegrators and integrators of [Service Granularity](decomposition/service-granularity.md). The cache-vs-database ownership question is sharpened by [Data Ownership](distributed/data-ownership.md), where the in-memory grid is effectively a *common* ownership model with the data writers acting as the canonical writer and the database as the eventually-consistent system of record.

## Sources

- [Fundamentals Ch 16: Space-Based Architecture Style](software/software-architecture/books/fundamentals-of-software-architecture/ch16_space_based_architecture.md) (sole source — topology, processing units, virtualized middleware, replicated vs. distributed cache, data pumps/writers/readers, collision formula, governance fitness functions, characteristic ratings, ticketing/auction examples)


<!-- prev-next-nav -->

---

← [Event-Driven](software/software-architecture/styles/event-driven.md) | [Orchestration-Driven SOA](software/software-architecture/styles/orchestration-driven-soa.md) →
