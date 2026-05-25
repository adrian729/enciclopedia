# Data Ownership

> *The Hard Parts* (Ch 9) is the only source for the *ownership* vocabulary — Single / Common / Joint — and for the four resolution techniques the joint case requires. The page also folds in the chapter's ACID-to-BASE pivot, which is the bridge between monolithic data assumptions and every other page in this section. Hard Parts works the Sysops Squad scenario to settle a real Joint Ownership case (Survey table) and to motivate why ACID stops at the service boundary.

## Table of Contents

- [1. The Writer-Is-Owner Rule](#1-the-writer-is-owner-rule)
- [2. Single Ownership](#2-single-ownership)
- [3. Common Ownership](#3-common-ownership)
- [4. Joint Ownership](#4-joint-ownership)
- [5. ACID Stops at the Service Boundary; BASE Takes Over](#5-acid-stops-at-the-service-boundary-base-takes-over)
- [6. Three Eventual-Consistency Patterns](#6-three-eventual-consistency-patterns)
- [Sources](#sources)

## 1. The Writer-Is-Owner Rule

Once a monolithic schema is decomposed, every table needs an answer to a deceptively simple question: *which service owns it?* The Hard Parts gives a single rule:

> **The service that performs *writes* on a table is the owner.** Read-only consumers do not affect ownership.

This rule converts the ownership question into a counting question. For every table, count the writing services. Three counts produce three scenarios, listed in resolution order:

| Scenario | Writers | Resolution effort |
|---|---|---|
| **Single Owner** | Exactly one service writes | Unambiguous; clear it first to shrink the problem. |
| **Common Owner** | Most or all services write (e.g., an Audit table) | Dedicate one owner, route writes to it. |
| **Joint Owner** | A few services in one domain write (e.g., Catalog + Inventory both writing `Product`) | Apply one of four resolution techniques. |

The sequencing advice — *resolve Single Owner first* — is the same braid-untangling instinct introduced in [Trade-Off Analysis](foundations/tradeoff-analysis.md). Clear the unambiguous cases first; the remaining problem is smaller and more tractable.

Reads are a separate concern. Cross-service read access is solved by the four patterns in [Distributed Data Access](distributed/distributed-data-access.md) — Interservice Communication, Column Schema Replication, Replicated Caching, Data Domain — never by widening the writer set.

## 2. Single Ownership

When only one service writes to a table, the table joins that service's bounded context and the analysis ends. Other services that need to read those columns go through the access patterns; they do not become co-owners.

The rule that protects this clarity is the **no-direct-schema-attachment** rule from the Sysops Squad ADR: *a service may not connect to multiple schemas*. The ownership boundary is not just a write boundary — it is a connection boundary, enforced by deployment topology.

## 3. Common Ownership

The classic case: an **Audit** table that hundreds of services append to. A shared schema looks like the obvious answer and is the wrong one — it reintroduces every monolithic-data pain from [Data Decomposition](decomposition/data-decomposition.md):

- Change-control bottlenecks — every audit-row addition requires coordinated schema change.
- Connection starvation — every service holds a pool against the same database.
- Scalability ceiling — a hot Audit table becomes the system's slowest writer.
- Fault-tolerance collapse — Audit downtime breaks every service that writes to it.

**The technique** — dedicate a single **Audit Service** as the owner. Every other service sends *write requests* to it instead of writing the table directly. The communication style depends on whether the writer needs a receipt:

| Write style | When to use | Mechanism |
|---|---|---|
| **Fire-and-forget async** | No acknowledgement needed | Persisted queue (guaranteed delivery, but writer doesn't block on confirmation) |
| **Request-reply** | Confirmation or generated key must come back | REST, gRPC, or request-reply messaging |

The Audit Service is now a Single Owner and joins that scenario for everything downstream. Common Ownership is, in effect, *Single Ownership pending a refactor*.

## 4. Joint Ownership

A few services *in the same domain* both write to one table. The Hard Parts example: **Catalog Service** and **Inventory Service** both writing to a **Product** table — Catalog updates `name`, `description`, `category`; Inventory updates `stock_level`, `reorder_threshold`, `last_restocked`. Splitting feels artificial; merging feels coarse. Hard Parts gives **four resolution techniques**:

| Technique | Move | Restores | Pays in |
|---|---|---|---|
| **Table Split** | Split the table so each service owns its portion (per *Refactoring Databases*) | Single Ownership per resulting table | Schema restructuring; no ACID across the split; sync between halves is hard |
| **Data Domain** | Place the shared table(s) in a shared schema with multiple owners — a broader bounded context | Performance, SQL joins, strong consistency | Wider blast radius for schema changes; harder write governance |
| **Delegate** | One service becomes sole owner; the other calls it to perform writes | Single Ownership of the table | Service coupling; slow non-owner writes; no atomic transactions across services; non-owner fault tolerance drops |
| **Service Consolidation** | Merge the joint owners into one coarser-grained service | ACID; clean performance | Coarser scalability and fault-tolerance unit; bigger deploy/test scope |

### 4.1. Delegate Is the Default

The Delegate Technique is the most commonly applicable; the question becomes *which service is the delegate?* Two variants:

- **Primary domain priority (preferred)** — assign delegation to the service performing most CRUD on the primary entity. For the Product table, Catalog is the natural delegate because product identity is a Catalog concern.
- **Operational characteristics priority** — assign to the service that needs higher performance, scalability, or availability. Sometimes Inventory wins because stock updates dominate the workload.

Hard Parts recommends *domain priority* as the default. It keeps domain responsibility coherent; the non-owner's performance gap is closed by [Replicated Caching or Column Schema Replication](distributed/distributed-data-access.md), not by inverting ownership for performance reasons.

### 4.2. Data Domain Caveat

Data Domain is fast and consistent, but it widens the bounded context. Before reaching for it, ask why the joint owners are separate services in the first place. Legitimate reasons to keep them separate even with Data Domain: differing scalability profiles, differing fault-tolerance budgets, throughput skew, isolating code volatility (a service that changes weekly should not share its release cadence with one that changes yearly). Without one of those reasons, Service Consolidation may be the honest answer.

### 4.3. Service Consolidation as Honesty Check

If the joint owners share data, share domain, share scalability profile, and share volatility — the architecture is asking for a single service. Service Consolidation collapses the join and restores ACID locally. The cost is the coarser deploy/test scope; the benefit is that all the resolution-technique pain disappears.

## 5. ACID Stops at the Service Boundary; BASE Takes Over

The whole reason ownership matters is that *transactional guarantees stop at the boundary*. Inside one service, ACID holds:

| Property | Meaning |
|---|---|
| **Atomicity** | All updates in the unit of work commit or roll back together. |
| **Consistency** | Integrity constraints (foreign keys, uniqueness) hold throughout the transaction. |
| **Isolation** | Uncommitted changes are not visible to other transactions. |
| **Durability** | Committed data survives failures. |

A **distributed transaction** is an atomic *business* request whose database updates span multiple services. Every ACID property breaks across the boundary:

- *Atomicity* is per service; no single commit straddles boundaries.
- *Consistency* cannot enforce cross-service constraints (no FK from one schema to another).
- *Isolation* leaks: a partial workflow is visible to other requests through any intermediate state.
- *Durability* covers only individual commits, not the workflow as a whole.

The replacement is **BASE** — *Basically Available, Soft state, Eventually consistent*:

| Property | Meaning |
|---|---|
| **Basic Availability** | All participants are *expected* to be available; async communication helps but lengthens consistency time. |
| **Soft state** | The in-flight (or unknown) state during the workflow; the system has values that may not yet be settled. |
| **Eventual consistency** | Given enough time, all data sources converge. |

BASE is not a bug — it is the *price of decomposition*. A team that wanted ACID across all services either gave up decomposition (back to monolith) or accepted distributed transactions with their well-known failure modes (see Issue 1–5 in [Transactional Sagas](distributed/transactional-sagas.md)).

The First Law restated for data: *the boundary you draw between services is the boundary that ACID can no longer cross.* See [Modularity, Cohesion, Coupling](foundations/modularity-cohesion-coupling.md) for the static-vs-dynamic split that makes the boundary load-bearing.

## 6. Three Eventual-Consistency Patterns

Once BASE is on the table, three patterns recur for actually achieving the eventual convergence:

| Pattern | Coordinator | Speed | Coupling | Main weakness |
|---|---|---|---|---|
| **Background Synchronization** | External batch/job | Slow (often nightly) | Services decoupled, **data sources coupled** | Sync process holds structural knowledge of every table; *breaks bounded contexts* |
| **Orchestrated Request-Based** | Dedicated orchestrator | Sync with the request | Decoupled via orchestrator | Slow responsiveness; compensating transactions can themselves fail |
| **Event-Based** | None (pub/sub or stream) | Near real-time | Highly decoupled | Consumer-side error handling is the hard part |

**Background Sync's hidden cost.** The job must encode business rules duplicated from the owning services — e.g., the 3-month `remove_date` retention before deleting an audit row — because it touches every table directly. Schema changes propagate through both the owners *and* the sync job. Bounded contexts are violated by construction.

**Orchestrated Request-Based** is the saga family's central case. The orchestrator can be an existing domain service or a dedicated one; the dedicated form is preferred so that workflow logic doesn't overload a domain service. Error handling typically uses *compensating transactions* — covered exhaustively in [Transactional Sagas](distributed/transactional-sagas.md), including why compensations themselves can fail.

**Event-Based** is usually the strongest fit for microservices and event-driven architectures because of decoupling and convergence time. Durable subscribers (or persistent topics in Kafka) prevent message loss; failed consumers retry, then route to a Dead Letter Queue. The mechanics live in [Workflows & Orchestration](distributed/workflows-orchestration.md).

The three patterns are not exclusive — they recombine. The next four pages of this section name the recombinations: data access patterns ([Distributed Data Access](distributed/distributed-data-access.md)), workflow shapes ([Workflows & Orchestration](distributed/workflows-orchestration.md)), saga shapes ([Transactional Sagas](distributed/transactional-sagas.md)), and contract shapes ([Contracts](distributed/contracts.md)). Ownership is the page that sets the question; the rest of the section answers it.

## Sources

- [The Hard Parts Ch 9: Data Ownership and Distributed Transactions](software/software-architecture/books/software-architecture-the-hard-parts/ch09_data_ownership_distributed_transactions.md) (primary — the three scenarios, four joint-ownership techniques, ACID/BASE, three eventual-consistency patterns, Catalog+Inventory + Sysops Squad Survey examples)


<!-- prev-next-nav -->

---

← [Data Decomposition](software/software-architecture/decomposition/data-decomposition.md) | [Distributed Data Access](software/software-architecture/distributed/distributed-data-access.md) →
