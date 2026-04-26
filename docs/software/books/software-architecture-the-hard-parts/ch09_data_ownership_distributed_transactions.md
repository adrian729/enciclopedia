# Ch 9: Data Ownership and Distributed Transactions

## Table of Contents

- [1. Assigning Data Ownership](#1-assigning-data-ownership)
- [2. Single Ownership scenario](#2-single-ownership-scenario)
- [3. Common Ownership scenario](#3-common-ownership-scenario)
- [4. Joint Ownership scenario](#4-joint-ownership-scenario)
- [5. ACID vs BASE: distributed transactions](#5-acid-vs-base-distributed-transactions)
- [6. Eventual Consistency Patterns](#6-eventual-consistency-patterns)
- [7. Sysops Squad saga: ticket processing](#7-sysops-squad-saga-ticket-processing)

## 1. Assigning Data Ownership

- **General rule of thumb** — the service that performs *write* operations on a table is the owner; read-only consumers do not change ownership.
- **Three scenarios** — **Single Ownership** (exactly one writing service), **Common Ownership** (most or all services write to it), **Joint Ownership** (a few services in the same domain write to it).
- **Authors' sequencing advice** — resolve Single Ownership tables first to clear the field, then tackle Common and Joint Ownership.

## 2. Single Ownership scenario

- **Definition** — only one service writes to the table; ownership is unambiguous, the table joins the service's bounded context.
- **Read access** — other services that only need reads do not affect ownership; their access is solved later via the patterns in Chapter 10.

## 3. Common Ownership scenario

- **Definition** — most or all services write to the same table (e.g., an Audit table that potentially hundreds of services append to).
- **Why a shared schema fails** — reintroduces change-control, connection-starvation, scalability, and fault-tolerance issues from Chapter 6.
- **Recommended technique** — assign a dedicated owner service (e.g., a new Audit Service); other services send write requests to it.
- **Communication style** — fire-and-forget asynchronous messaging on a *persisted queue* when no acknowledgement is required (guaranteed delivery); REST, gRPC, or request-reply messaging when a confirmation/key must come back.

## 4. Joint Ownership scenario

- **Definition** — a couple of services in the same domain perform writes on the same table (e.g., Catalog Service and Inventory Service both writing to a Product table).
- **Four resolution techniques** — **Table Split Technique**, **Data Domain Technique**, **Delegate Technique**, **Service Consolidation**.

| Technique | What it does | Advantages | Disadvantages |
|-----------|--------------|------------|---------------|
| **Table Split Technique** | Splits one table into multiple tables so each service owns its portion (per *Refactoring Databases*) | Preserves bounded context; restores single ownership | Schema restructuring; consistency issues; no ACID across new tables; sync between tables is hard |
| **Data Domain Technique** | Shared tables go into a shared schema/database, forming a broader bounded context with multiple owners | Good performance; consistent data; no service dependency | Schema changes touch many services; write governance harder; broader bounded context |
| **Delegate Technique** | One service is the sole owner (delegate); others call it to perform writes | Single table ownership; good schema change control; abstracts table from non-owners | Service coupling; slow non-owner writes; no atomic transactions across services; low fault tolerance for non-owners |
| **Service Consolidation** | Merge the joint owners into one coarser-grained service | Preserves atomic transactions; good performance | Coarser-grained scalability; reduced fault tolerance; bigger deploy/test scope |

- **Delegate Technique — choosing the delegate** — two options: **primary domain priority** (assign to the service performing most CRUD on the primary entity) or **operational characteristics priority** (assign to the service needing higher performance, scalability, or availability).
- **Domain priority is usually preferred** — keeps domain responsibility coherent; performance gaps for non-owners are addressed via replicated or distributed caches rather than by inverting ownership.
- **Data Domain Technique caveat** — if data is genuinely common to multiple services, reevaluate why the services are separate; valid reasons include scalability differences, fault-tolerance needs, throughput differences, or isolating code volatility.

## 5. ACID vs BASE: distributed transactions

- **ACID — atomic transaction inside one service**:
  - **Atomicity** — all updates in the unit of work commit or roll back together.
  - **Consistency** — integrity constraints (e.g., foreign keys) hold throughout the transaction.
  - **Isolation** — uncommitted changes are not visible to other transactions.
  - **Durability** — committed data survives system failures.
- **Distributed transaction** — an atomic *business* request whose database updates span multiple services; ACID properties are lost across that boundary.
- **Why each ACID property breaks** — atomicity is bound per service, consistency cannot enforce cross-service constraints, isolation leaks intermediate state to other requests, durability covers only individual commits.
- **BASE — properties of distributed transactions**:
  - **Basic Availability** — all participants are expected to be available; asynchronous communication helps but extends consistency time.
  - **Soft state** — the in-progress (or unknown) state during the workflow.
  - **Eventual consistency** — given enough time, all data sources converge.

## 6. Eventual Consistency Patterns

- **Background Synchronization Pattern** — an external batch or periodic process reconciles tables; longest convergence time; *breaks bounded contexts* because the sync process must write into every owned table.
- **Orchestrated Request-Based Pattern** — a dedicated orchestrator coordinates the distributed transaction during the user request, favoring data consistency over responsiveness; error handling typically requires *compensating transactions*, which themselves can fail and may need human intervention.
- **Event-Based Pattern** — services publish to a topic/event stream and consumers update their data via async pub/sub; high decoupling, fast convergence, good responsiveness; durable subscribers (or persistent topics in Kafka) prevent message loss; failed consumers are retried by the broker, then routed to a Dead Letter Queue.

| Pattern | Coordinator | Consistency speed | Service coupling | Main weakness |
|---------|-------------|-------------------|------------------|---------------|
| **Background Sync** | External batch/job | Slow (often nightly) | Decoupled services, **but data sources coupled** | Breaks bounded contexts; duplicated business logic |
| **Orchestrated Request-Based** | Dedicated orchestrator service | Synchronous with the request | Decoupled (via orchestrator) | Slow responsiveness; complex error handling; compensating transactions |
| **Event-Based** | None (pub/sub or stream) | Near real-time | Highly decoupled | Complex error handling on consumer failures |

- **Background Sync drawback in detail** — the process must hold structural knowledge of every table; schema changes require coordinating an external job, and business rules (e.g., a 3-month `remove_date` retention before deletion) end up duplicated between services and the sync process.
- **Orchestrated Request-Based variant** — the orchestrator role can be a designated existing service or a new dedicated one; the dedicated form is preferred to avoid overloading a domain service with workflow responsibilities.
- **Event-Based default** — usually the strongest fit for microservices and event-driven architectures because of decoupling and convergence time.

## 7. Sysops Squad saga: ticket processing

- **Single ownership ADR** — when only one service writes to a table, that service is the owner; cross-bounded-context read access is *not* permitted via direct database/schema connection (a service may not connect to multiple schemas).
- **Survey table joint ownership** — Ticket Completion Service and Survey Service both wrote to the Survey table. Table splitting was unsuitable, the Data Domain Technique was unavailable (Ticket Completion already attaches to the ticketing data domain and a service cannot connect to multiple schemas), and merging Survey tables into the ticketing domain would re-monolithize the database.
- **Decision** — apply the Delegate Technique with the Survey Service as sole owner. Ticket Completion already sends a notification event when a ticket completes, so the necessary survey payload rides on that event, eliminating any direct write access for Ticket Completion.
- **Consequence** — survey-record creation is no longer part of ticket completion's local commit; it becomes a separate activity owned by the Survey Service.
