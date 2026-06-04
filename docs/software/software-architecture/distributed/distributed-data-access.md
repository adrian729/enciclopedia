# Distributed Data Access

> *The Hard Parts* (Ch 10) is the single source — the chapter is dedicated to *reading data across a service boundary you don't own*. The four patterns below (Interservice Communication, Column Schema Replication, Replicated Caching, Data Domain) are what the chapter spends its pages on, with a worked Sysops Squad sizing analysis that justifies Replicated Caching. Hard Parts works the Sysops Squad scenario to settle the Ticket Assignment → User Management read path.

## Table of Contents

- [1. The Read-Access Problem](#1-the-read-access-problem)
- [2. Interservice Communication](#2-interservice-communication)
- [3. Column Schema Replication](#3-column-schema-replication)
- [4. Replicated Caching](#4-replicated-caching)
- [5. Data Domain](#5-data-domain)
- [6. Choosing Among the Four](#6-choosing-among-the-four)
- [7. The Sysops Squad Sizing Walk-Through](#7-the-sysops-squad-sizing-walk-through)
- [Sources](#sources)

## 1. The Read-Access Problem

[Data Ownership](distributed/data-ownership.md) settles writes. Reads are a different problem. In a monolith, any service could `JOIN` any other table. Once data is partitioned across per-service schemas, a service routinely needs read access to columns it no longer owns.

Hard Parts uses a running example. A **Wishlist Service** must show item descriptions on a user's wishlist page; the `item_desc` column lives in the **Catalog Service's** Product table. Four patterns address this read, balancing coupling, consistency, performance, and data volume differently. None of them is "best" — each fits a different envelope of constraints.

| Pattern | One-line summary |
|---|---|
| **Interservice Communication** | Caller asks the owner on demand. |
| **Column Schema Replication** | Owner pushes a copy of the needed columns into the caller's table. |
| **Replicated Caching** | Owner-as-sole-writer in-memory cache mirrored into each consumer. |
| **Data Domain** | Shared schema; treat reads like a monolith would. |

## 2. Interservice Communication

**Mechanism** — the consumer makes a remote call (REST, gRPC, messaging) to the owning service to fetch the data on demand. The data is always current because it is fetched live.

**The latency stack** — this is the hidden cost. A single cross-service read accrues all three:

| Component | Typical range |
|---|---|
| Network latency | \~30–300 ms |
| Security latency (auth/authz on secured endpoints) | \~20–400 ms |
| Data latency (the extra database call inside the owning service) | \~10–50 ms |

Worst-case cumulative latency approaches a second per cross-boundary read. A page that needs three such reads can become unusable.

**Coupling cost** — both semantic and static. If Catalog is unavailable, Wishlist is unavailable too. Both must scale together. Fitness functions for Wishlist's availability now include Catalog's availability whether the team wanted that or not.

**Best fit** — simple cases with low call volume, no fault-tolerance pressure, and data volumes too large for replication-based patterns. Reach for it when the data is fundamentally too big to ship around but the call rate is low enough that latency doesn't compound.

## 3. Column Schema Replication

**Mechanism** — replicate only the columns the consumer needs (e.g., `item_desc`) into the consumer's own table. Wishlist now has its own `item_desc` column and serves queries locally with native SQL joins.

**Synchronization** — owner pushes changes via async messaging or an event stream when its source row changes. Async is preferred over sync to preserve responsiveness and decouple availability.

**Data-ownership leak** — this is the dark side. Because the column physically lives in the consumer's table, the consumer *can* update it even though it doesn't own it. The writer-is-owner rule from [Data Ownership](distributed/data-ownership.md) becomes a governance problem rather than a structural one. Linting, code review, or runtime fitness functions are the only enforcement.

**Best fit** — *data aggregation, reporting,* or scenarios where the other patterns fail their own constraints (data too large for caching, fault-tolerance demands too high for synchronous fetch). The authors generally caution against Column Schema Replication for the Wishlist/Catalog example specifically — the ownership leak isn't worth it when a simpler pattern fits.

## 4. Replicated Caching

**Mechanism** — every consumer instance holds an **in-memory replica** of the owner's cache. Cache instances synchronize behind the scenes when the owner updates. The owner is the sole writer; consumers hold a read-only replica.

This is not a single in-memory cache (no sharing across services) and not a distributed cache (an external caching server that becomes a new fault-tolerance dependency and another place where writers can break ownership). Replicated caching keeps in-memory copies **inside each service's process** and synchronizes them.

| Caching mode | Why it doesn't fit here |
|---|---|
| Single in-memory cache | Per-service only; no cross-service sharing. |
| Distributed cache | Cache server becomes a new SPOF; multiple services can write, breaking ownership. |
| **Replicated cache** | In-memory replica per service instance; owner is sole writer. |

**Supported products** — Hazelcast, Apache Ignite, Oracle Coherence. Not all caching products support replicated mode.

**Startup dependency** — only the *first* consumer instance must wait for the owner to be running. Subsequent consumer instances bootstrap from peer caches; once propagated, the owner can disappear and the consumers continue functioning. This is a key fault-tolerance property.

**Two ceilings** — beyond which the pattern doesn't work:

| Ceiling | Threshold | Why it matters |
|---|---|---|
| **Data volume** | \~500 MB | Memory cost scales by `cache size × consumer instances`. 500 MB × 5 instances = 2.5 GB. |
| **Update rate** | High churn | Synchronization can't keep up; consumers diverge. Inventory counts are too volatile; product descriptions are fine. |

**Configuration challenge** — services discover each other via TCP/IP broadcast and lookups. Cloud and containerized environments with dynamic IPs make this harder; the platform team owns the discovery configuration.

## 5. Data Domain

**Mechanism** — shared tables go into a single schema attached by multiple services, forming a broader bounded context (the same Data Domain Technique that resolves Joint Ownership in [Data Ownership](distributed/data-ownership.md)).

| Property | What it buys |
|---|---|
| Full runtime decoupling between services | No remote calls; each service queries its own connection. |
| Native SQL joins | The monolith's read ergonomics return. |
| High consistency / integrity | Foreign keys, views, stored procedures, triggers all available. |
| No replication overhead | The data is already in one place. |

**Contract trade-off** — the table schema *is* the contract. A structural change to any shared table can ripple to every service attached to the schema. The other three patterns offer an abstraction layer; Data Domain does not.

**Security trade-off** — colocating data exposes it to every service attached. The tighter bounded contexts of the other patterns allow more precise access restriction.

**Best fit** — high data volumes that defeat replication, high consistency/integrity needs, and scenarios where the other three patterns fail their own constraints. Often the right choice for analytics or reporting subschemas where the broader bounded context is intentional.

## 6. Choosing Among the Four

| Pattern | Mechanism | Performance | Service coupling | Data consistency | Notable limit |
|---|---|---|---|---|---|
| **Interservice Communication** | Remote call on demand | Poor (latency stack) | High (availability + scaling) | Always current | Scales/fails with the owner |
| **Column Schema Replication** | Replicate columns into consumer table | Good | Decoupled at runtime | Eventual; ownership leaks | Sync infrastructure required |
| **Replicated Caching** | In-memory replica per consumer | Very good | Decoupled after startup | Consistent for low-churn data | Data volume; update rate; cloud config |
| **Data Domain** | Shared schema across services | Very good | Decoupled at runtime | Strong (SQL + constraints) | Broader bounded context; security exposure |

The trade-off analysis from [Trade-Off Analysis](foundations/tradeoff-analysis.md) applies directly: enumerate the forces that matter for *your* read (call rate, data volume, churn, consistency need, fault-tolerance budget), rate each pattern against them, and pick the one that minimizes the dimension you cannot afford to lose.

## 7. The Sysops Squad Sizing Walk-Through

Hard Parts works the Sysops Squad scenario to make the decision concrete. The **Ticket Assignment Service** must continuously query the expert profile table now owned by the **User Management Service** (post-decomposition). Remote calls per assignment were not feasible — too slow and too tightly coupled to User Management's availability.

**Eliminated options first:**

- *Service Consolidation* — Ticket Assignment and User Management live in different domains; merging them re-monolithizes.
- *Data Domain* — Ticket Assignment is already attached to the ticketing data domain, and a service cannot connect to two schemas.

That leaves two candidates: **Interservice Communication** or **Replicated Caching**.

**Sizing analysis** — the deciding numbers:

| Quantity | Value |
|---|---|
| Active experts | 900 |
| Profile size per expert | \~1.3 KB |
| Total dataset | 900 × 1.3 KB ≈ **1.2 MB** |
| Max User Management instances | 2 |
| Max Ticket Assignment instances | 4 |
| Total in-memory footprint across consumers | 1.2 MB × 4 ≈ 5 MB |

1.2 MB sits comfortably below the \~500 MB ceiling, and expert profiles are mostly static (updated rarely). Both ceilings are clear; Replicated Caching is the right choice.

**Decision** — Replicated Caching with **User Management Service as sole writer**; Ticket Assignment instances hold read-only replicas. Performance and fault-tolerance pain of remote calls are resolved.

**Consequences accepted:**

- *Startup ordering* — at least one User Management instance must be running before the first Ticket Assignment instance starts; subsequent instances bootstrap from peers.
- *Licensing cost* — the chosen replicated-cache product (Hazelcast, Ignite, Coherence) is a paid dependency for some versions.
- *Team learning curve* — mitigated by a planned proof-of-concept, in line with [Architectural Thinking](foundations/architectural-thinking.md)'s POC-as-staying-hands-on guidance.

The walk-through is the canonical worked example of the chapter's method: eliminate impossible options on structural grounds, size the remaining ones with real numbers, and decide on the surviving pattern. See [Service Granularity](decomposition/service-granularity.md) for the upstream decisions about why these services are separate at all, and [Data Ownership](distributed/data-ownership.md) for the writer-is-owner rule that makes "sole writer" load-bearing in the cache configuration.

## Sources

- [The Hard Parts Ch 10: Distributed Data Access](software/software-architecture/books/software-architecture-the-hard-parts/ch10_distributed_data_access.md) (primary — the four data access patterns, the latency stack, the Sysops Squad sizing analysis)


<!-- prev-next-nav -->

---

← [Data Ownership](software/software-architecture/distributed/data-ownership.md) | [Workflows & Orchestration](software/software-architecture/distributed/workflows-orchestration.md) →
