# Data Decomposition

> *The Hard Parts* Ch 6 is the sole source — *Fundamentals* covers data topologies inside its architecture-style chapters but doesn't treat operational-data decomposition as its own topic. The chapter mirrors the granularity equilibrium of Ch 7 (see [Service Granularity](decomposition/service-granularity.md)) but applied to data: disintegrators justify splitting, integrators justify keeping together, the right answer sits at the equilibrium. The five-step process is the operational core, the **data domain** soccer-ball metaphor is the visual, and the database-type taxonomy is the polyglot menu. Sysops Squad's six-domain split and the Survey-to-document-database polyglot decision are worked as the ADR example. Forward-link to [Data Ownership](distributed/data-ownership.md) for the *who reads/writes what* question that comes next.

## Table of Contents

- [1. Why Decomposing Data Is Hard](#1-why-decomposing-data-is-hard)
- [2. Data Disintegrators](#2-data-disintegrators)
- [3. Data Integrators](#3-data-integrators)
- [4. The Data Domain Concept](#4-the-data-domain-concept)
- [5. The Five-Step Decomposition Process](#5-the-five-step-decomposition-process)
- [6. Selecting a Database Type](#6-selecting-a-database-type)
- [7. Sysops Squad — Polyglot Decisions](#7-sysops-squad--polyglot-decisions)
- [Sources](#sources)

## 1. Why Decomposing Data Is Hard

Data is the most valuable asset in the system, and restructuring it carries more business and application risk than restructuring code. Data is also highly coupled to application functionality, and the seams are buried *inside* large data models rather than visible at the namespace level the way component seams are.

The same vocabulary as code decomposition still applies, with different artifacts:

| Code decomposition | Data decomposition |
|---|---|
| Components | **Data domains** |
| Class files | **Database tables** |
| Class-to-class coupling | **Foreign keys, views, triggers, stored procedures** |

Whether decomposition is mandatory depends on the architecture style: **microservices** require per-bounded-context data; **service-based architecture** permits a shared database (see [Component-Based Decomposition](decomposition/component-based-decomposition.md), which deliberately defers data decomposition until after the code is split). Style decides; this page is about the mechanics once the decision to split data has been made.

As with service granularity, two opposing forces. **Data Disintegrators** justify breaking data apart; **Data Integrators** justify keeping it together. Right granularity sits at the equilibrium.

## 2. Data Disintegrators

The six drivers that justify breaking apart shared data.

### 2.1. Change Control

Every breaking schema change — drop, rename, or retype a table or column — forces every service that touches it to be tested and redeployed in lockstep. In a 400-service ecosystem this is infeasible. Bounded contexts isolate change to one service-and-data unit. **Database abstraction** within a bounded context lets the service expose a *contract* (JSON/XML/object) different from the underlying tables — e.g., `EXPIRATION_DT` as a DATE column internally, exposed as `exp_dt` as an epoch number externally — so internal table changes don't break consumers.

### 2.2. Connection Management

Distributed services each have their own connection pool, so connections multiply quickly. The book's worked numbers: 200 monolith connections become 1,000 across 50 services with 2 instances each, then 1,700 once half the services scale to an average of 5 instances. **Connection quotas** govern the share each service may hold; start with even distribution, then move to **variable distribution** based on observed waits.

### 2.3. Scalability

When services scale by adding instances, even a tuned quota is invalidated — 100 connections allocated, 242 actually used after scaling. Splitting databases reduces per-database load and connection pressure: each per-domain database scales for its own service's traffic profile.

### 2.4. Fault Tolerance

A shared database is a single point of failure: one outage takes down every service. Per-domain databases let unaffected services keep running.

### 2.5. Architectural Quanta

The database is part of the **static-coupling** definition of a quantum (see [Components and Quantum](foundations/components-and-quantum.md)). As long as services share one database they form a single quantum and *can't have differing architecture characteristics*. Splitting the data is what produces multiple quanta — and therefore the ability to have, say, a high-availability Customer quantum and a high-throughput Reporting quantum in the same system.

### 2.6. Database-Type Optimization

A monolithic relational store forces all data into one paradigm. Splitting lets reference data move to a key-value store, hierarchical data to a document store, relationship-heavy data to a graph, time-series data to a time-series store, and so on. See § 6 for the taxonomy.

## 3. Data Integrators

The two drivers that justify keeping data together. There are only two, because data integration forces are heavier and rarer than code integration forces.

### 3.1. Data Relationships

Foreign keys, triggers, views, and stored procedures — plus *logical* relationships like `ticket` and `ticket_status` — tightly couple tables. Cross-domain artifacts must be removed or rewritten when splitting; the cost may outweigh the disintegrator's benefit. Many relational designs include views that join tables from what are now separate domains; those joins become service-to-service calls (with all the latency, fault tolerance, and saga implications).

### 3.2. Database Transactions

A single ACID transaction across multiple writes only exists when the data lives together. Once split into separate schemas or databases, atomic commit/rollback is replaced by remote calls that may leave the system inconsistent — covered by the saga patterns in [Transactional Sagas](distributed/transactional-sagas.md). Consolidate when business demands all-or-nothing across the boundary.

## 4. The Data Domain Concept

> **Data domain** — a collection of coupled database artifacts (tables, views, foreign keys, triggers) related to a particular domain and used together within a limited functional scope.

The visual is a soccer ball: white hexagons connected by black pentagons. **Intra-hexagon dependencies are preserved** — tables inside one data domain stay coupled. **Cross-hexagon dependencies must be broken** — joins, foreign keys, and views that span hexagons either move into one domain (if the relationship is owned there) or get rewritten as service-to-service calls (if the relationship truly crosses).

> **Data domain vs. schema.** A data domain is an *architectural* concept; a schema is the *database construct* that holds it. The relationship is usually one-to-one but a data domain may map to multiple schemas when tightly coupled domains are combined.

Identifying data domains is the analytical step in the five-step process. It is shaped by the same DDD bounded-context thinking that produced the code-side component domains in [Component-Based Decomposition § Pattern 5](decomposition/component-based-decomposition.md#6-pattern-5--create-component-domains) — and ideally the two analyses align, with each data domain owned by one service domain.

## 5. The Five-Step Decomposition Process

The mechanics of pulling apart a shared operational database. Each step is mechanical once the previous one is complete; the *analysis* lives in step 1.

### 5.1. Step 1 — Analyze and Create Data Domains

Identify domain groupings within the monolithic schema. Sysops Squad's six: **Customer, Survey, Payment, Profile, Knowledge Base, Ticketing**. Assignment is informed by:

- Which service-domain (from the code decomposition) owns each table.
- Existing foreign keys and views (their density signals which tables belong together).
- Business semantics — what *functionally* belongs together independent of the current relational design.

This is the step that benefits most from the trade-off framing in [Trade-Off Analysis](foundations/tradeoff-analysis.md): the data domains are not always obvious, and several plausible partitions will exist. Pick the one whose cross-domain breaks are tolerable.

### 5.2. Step 2 — Assign Tables to Data Domains

Move each table into a schema for its domain — `ALTER SCHEMA payment TRANSFER sysops.billing` and equivalents on other engines. When data domains are tightly coupled, combine them into a broader bounded context rather than fighting the coupling. **Synonyms** (database symlinks) may bridge cross-schema queries *temporarily*, but they are coupling points to remove later — they let the system keep working through the migration without committing to permanent cross-schema joins.

### 5.3. Step 3 — Separate Database Connections to Data Domains

Refactor each service to connect *only* to its own schema. Cross-schema queries must move into service-to-service calls. The end state is **data sovereignty per service** — each service owns its data.

| Benefit | Shortcoming |
|---|---|
| Independent schema change | Performance penalties for large cross-domain reads |
| Per-service database type (enables § 6 polyglot) | Loss of database-enforced referential integrity |
| | Stored-procedure logic must move to the service layer |

This is the step at which the decomposition becomes architecturally real: the loss of referential integrity and the cross-domain calls are the same forces that motivated the integrators in § 3, so step 3 is where their cost shows up. See [Data Ownership](distributed/data-ownership.md) for how to design the new cross-service read/write patterns.

### 5.4. Step 4 — Move Schemas to Separate Database Servers

Even with separate schemas, *one shared server keeps the system in a single quantum.* Splitting the server is what produces multiple quanta and lets each domain database be tuned independently. Two migration options:

| Option | Procedure | Trade-off |
|---|---|---|
| **Backup and restore** | Back up each schema; set up new servers; restore; repoint services; drop old schemas | Requires downtime |
| **Replicate** | Set up new servers; replicate schemas; switch connections; drop originals | No downtime, more setup and coordination |

### 5.5. Step 5 — Switch Over

Remove the old connections; drop the schemas from the original server. Each domain now runs on its own server and can be tuned independently for availability, scalability, and database type. The system is now multi-quantum and ready for polyglot persistence.

## 6. Selecting a Database Type

Once data sovereignty exists per service, each service can use the database type that best fits its access pattern. Each type is rated against a fixed set of characteristics — ease-of-learning, ease of data modeling, scalability/throughput, availability/partition tolerance, consistency, programming-language/SQL/community support, and read/write priority.

| Type | Strengths | Weaknesses | R/W priority | Example products |
|---|---|---|---|---|
| **Relational** | Mature, ubiquitous SQL, ACID, flexible modeling, large community | Vertical scaling only, complex replication, weaker availability/partition tolerance | Balanced | PostgreSQL, Oracle, MS SQL, MySQL |
| **Key-Value** | Very fast key lookups, easy scaling, tunable consistency via quorum, simple API | Queryable only by key; aggregate redesign forces full data rewrite; no joins/where/order-by | Read priority | Redis, Riak KV, DynamoDB, MemcacheDB |
| **Document** | Self-describing JSON/XML aggregates, secondary indexes, forgiving aggregate design, strong NoSQL tooling | Sharding adds complexity; ACID limited to a collection | Read priority | MongoDB, Couchbase, AWS DocumentDB |
| **Column-family** | Horizontal scaling for high read/write throughput, replication factor 3 by default, tunable consistency, sparse-data efficient via SSTables | Steep learning curve; row-key design takes iteration; super columns are hard | Write priority (high write volume) | Cassandra, Scylla, Amazon SimpleDB |
| **Graph** | Edges as first-class objects make traversal very fast; built-in algorithms (Dijkstra, similarity); ACID in some engines (Neo4j) | Steep learning curve; modeling is hard; sharding writes is hard; relationship-type changes are expensive | Read priority (relationship traversal) | Neo4j, Infinite Graph, Tiger Graph |
| **NewSQL** | SQL + ACID + horizontal scaling via automated sharding; multi-active nodes; survives disk/machine/datacenter failures (CockroachDB) | Sharding design adds wrinkle; some only available as DBaaS | Balanced | VoltDB, ClustrixDB, SimpleStore (aka MemSQL) |
| **Cloud-native** | No upfront cost, automatic scaling, low operational burden, cross-region replication (Snowflake), ACID supported | Variable learning curves (Datomic uses Clojure); tooling/talent gaps; cost grows with scale | Varies (Snowflake/Redshift read-heavy; Datomic balanced) | Snowflake, Redshift, Datomic, CosmosDB |
| **Time-series** | Append-only model fits IoT/observability; automatic timestamping; tag-based querying over time windows; SQL-like dialects (InfluxQL) | Append-only requires unlearning update/delete; not general-purpose; tag-design discipline needed | Read priority | InfluxDB, kdb+, Amazon Timestream, TimeScale |

Three concepts that recur across types:

- **Aggregate orientation** (DDD, Eric Evans) — preferring to operate on related complex data as one unit. Benefits: easy distribution across cluster nodes, fewer joins, less impedance mismatch. Costs: hard to define correct aggregate boundaries; cross-aggregate analysis is difficult.
- **Schema-less is a misnomer.** NoSQL stores still have a schema, just implicit; applications must handle multiple versions returned at once.
- **Sharding vs. partitioning.** Partitioning splits table data within one database server; sharding splits data across nodes via a sharding key.

## 7. Sysops Squad — Polyglot Decisions

Hard Parts works the Sysops Squad scenario to anchor both the *justification* of decomposition and the *polyglot* decision once decomposition is done.

### 7.1. Justifying the Decomposition

Addison and Devon convinced Dana with three concrete signals:

- Reporting queries blocked ticketing via shared connections (a § 2.2 connection-management failure already in production).
- Projected service growth required \~2,000 additional connections (§ 2.3 scalability).
- The shared database created an availability SPOF for ticketing (§ 2.4 fault tolerance).

The three together carried the ADR. None of them was speculative — all three were live problems.

### 7.2. Six Data Domains Identified

Customer, Survey, Payment, Profile, Knowledge Base, Ticketing. Tables assigned to each — e.g., `billing` / `contract` / `payment_method` to Payment; `ticket` / `ticket_history` to Ticketing.

### 7.3. The Cross-Domain View Rewrite

`payment.v_customer_contract` originally joined `payment.contract`, `customer.customer`, and `payment.billing`. The rewrite removed the join to `customer.customer` and the `customer_name` column, forcing the Payment service to call the Customer service for the name. This is the step-3 cost in concrete form: a database join becomes a network call, and the architect must accept the latency/availability trade-off in exchange for data sovereignty.

### 7.4. Survey Moves to a Document Database

Marketing required frequent, low-friction survey changes; relational rendering was painful for the UI. The ADR moves Survey to a document database — the § 6 database-type-optimization disintegrator. The aggregate-modeling trade-off was between a *single* aggregate (questions embedded in survey document) and a *split* aggregate (separate Question documents referenced by ID). The team chose single, accepting question duplication across surveys in exchange for one-shot retrieval and simpler UI rendering — there were only five survey types and most changes added or removed questions.

The Survey decision shows the payoff of finishing the five-step process: once Survey has its own server (step 4 → 5), it can use a different database engine than Customer or Payment, and the team picks the engine that fits the access pattern rather than the engine the monolith happened to have.

---

The data-side decomposition produces sovereignty per service, but it does not yet answer *who is allowed to read or write each service's data, and how*. That is the topic of [Data Ownership](distributed/data-ownership.md) — single, common, and joint ownership, with the four joint-ownership resolution techniques — and of [Distributed Data Access](distributed/distributed-data-access.md), which catalogs the patterns (Interservice Communication, Column Schema Replication, Replicated Caching, Data Domain) for the cross-domain reads that step 3 forced into the service layer.

## Sources

- [The Hard Parts Ch 6: Pulling Apart Operational Data](software/software-architecture/books/software-architecture-the-hard-parts/ch06_pulling_apart_operational_data.md) (primary — data disintegrators, data integrators, data-domain concept, five-step process, database-type taxonomy, Sysops Squad ADRs)


<!-- prev-next-nav -->

---

← [Service Granularity](software/software-architecture/decomposition/service-granularity.md) | [Data Ownership](software/software-architecture/distributed/data-ownership.md) →
