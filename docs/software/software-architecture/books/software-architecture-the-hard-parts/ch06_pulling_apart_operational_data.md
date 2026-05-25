# Ch 6: Pulling Apart Operational Data

## Table of Contents

- [1. Why decomposing data is hard](#1-why-decomposing-data-is-hard)
- [2. Data Disintegrators](#2-data-disintegrators)
- [3. Data Integrators](#3-data-integrators)
- [4. Decomposing Monolithic Data: the five-step process](#4-decomposing-monolithic-data-the-five-step-process)
- [5. Selecting a Database Type](#5-selecting-a-database-type)
- [6. Sysops Squad: justifying decomposition and polyglot databases](#6-sysops-squad-justifying-decomposition-and-polyglot-databases)

## 1. Why decomposing data is hard

- **Data is the most valuable asset** — restructuring it carries more business and application risk than restructuring code, and data tends to be highly coupled to application functionality, hiding well-defined seams inside large data models.
- **Same techniques, different artifacts** — components map to *data domains*, class files map to *database tables*, and class-to-class coupling maps to *foreign keys, views, triggers, and stored procedures*.
- **Style-driven necessity** — microservices require per-bounded-context data, while service-based architectures permit a shared database; the architecture style decides whether decomposition is mandatory.
- **Two opposing forces** — **Data Disintegrators** justify breaking data apart; **Data Integrators** justify keeping it together. Right granularity sits at the equilibrium.

## 2. Data Disintegrators

The six main disintegration drivers that justify breaking apart data:

- **Change control** — every breaking schema change (drop/rename/retype a table or column) forces every service that touches it to be tested and redeployed in lockstep; in a 400-service ecosystem this becomes infeasible. Bounded contexts isolate change to one service-and-data unit, and **database abstraction** within a bounded context lets the service expose a contract (JSON/XML/object) different from the underlying tables (e.g., `EXPIRATION_DT` DATE column exposed as `exp_dt` epoch number), so internal table changes don't break consumers.
- **Connection management** — distributed services each have their own connection pool, so connections multiply quickly (200 monolith connections become 1,000 across 50 services with 2 instances each, 1,700 once half the services scale to an average of 5 instances). **Connection quotas** govern the share each service may hold; start with even distribution, then move to **variable distribution** based on observed waits.
- **Scalability** — when services scale by adding instances, even a tuned quota is invalidated (e.g., 100 connections allocated, 242 actually used after scaling). Splitting databases reduces per-database load and connection pressure.
- **Fault tolerance** — a shared database is a single point of failure: one outage takes down every service. Per-domain databases let unaffected services keep running.
- **Architectural quanta** — the database is part of the static-coupling definition of a quantum, so as long as services share one database they form a single quantum and can't have differing architecture characteristics. Splitting the data is what produces multiple quanta.
- **Database type optimization** — a monolithic relational store forces all data into one paradigm; splitting lets reference data move to key-value, hierarchical data to document, etc.

## 3. Data Integrators

The two drivers that justify keeping data together:

- **Data relationships** — foreign keys, triggers, views, and stored procedures (plus logical relationships like ticket and ticket_status) tightly couple tables. Cross-domain artifacts must be removed or rewritten when splitting; the cost may outweigh the disintegrator's benefit.
- **Database transactions** — a single ACID transaction across multiple writes only exists when the data lives together. Once split into separate schemas/databases, atomic commit/rollback is replaced by remote calls that may leave the system inconsistent (covered by transactional sagas in Ch. 12).

## 4. Decomposing Monolithic Data: the five-step process

A **data domain** is a collection of coupled database artifacts (tables, views, foreign keys, triggers) related to a particular domain and used together within a limited functional scope. Visualized as the white hexagons of a soccer ball, where intra-hexagon dependencies are preserved and cross-hexagon (dotted) dependencies must be broken. The five-step decomposition:

1. **Analyze database and create data domains** — identify domain groupings within the monolithic schema (e.g., Sysops Squad: Customer, Survey, Payment, Profile, Knowledge Base, Ticketing) and assign tables to each.
2. **Assign tables to data domains** — move each table into a schema for its domain (`ALTER SCHEMA payment TRANSFER sysops.billing`). When data domains are tightly coupled, combine them into a broader bounded context. **Synonyms** (database symlinks) may bridge cross-schema queries temporarily, but they are coupling points to remove later.
3. **Separate database connections to data domains** — refactor each service to connect only to its own schema; cross-schema queries must move into service-to-service calls. The end state is **data sovereignty per service** — each service owns its data. Benefits: independent schema change and per-service database type. Shortcomings: performance penalties for large cross-domain reads, loss of database-enforced referential integrity, stored-procedure logic must move to the service layer.
4. **Move schemas to separate database servers** — even with separate schemas, one shared server keeps the system in a single quantum. Two migration options:

| Option | Procedure | Trade-off |
|---|---|---|
| **Backup and restore** | Back up each schema, set up new servers, restore, repoint services, drop old schemas | Requires downtime |
| **Replicate** | Set up new servers, replicate schemas, switch connections, drop originals | No downtime, more setup and coordination |

5. **Switch over to independent database servers** — remove the old connections, drop the schemas from the original server. Each domain now runs on its own server and can be tuned independently for availability, scalability, and database type.

> **Data domain vs schema** — a data domain is an architectural concept; a schema is the database construct that holds it. The relationship is usually one-to-one but a data domain may map to multiple schemas when tightly coupled domains are combined.

## 5. Selecting a Database Type

Each database type is rated against a fixed set of characteristics: **ease-of-learning curve**, **ease of data modeling**, **scalability/throughput**, **availability/partition tolerance**, **consistency**, **programming-language support / product maturity / SQL / community**, and **read/write priority**.

| Type | Strengths | Weaknesses | Read/Write priority | Example products |
|---|---|---|---|---|
| **Relational** | Mature, ubiquitous SQL, ACID, flexible modeling, large community | Vertical scaling only, complex replication setup, weaker availability/partition tolerance | Balanced | PostgreSQL, Oracle, MS SQL, MySQL |
| **Key-Value** | Very fast key lookups, easy scaling, tunable consistency via quorum, simple API (get/put/delete) | Queryable only by key; aggregate redesign forces full data rewrite; no joins/where/order-by | Read priority | Redis, Riak KV, DynamoDB, MemcacheDB |
| **Document** | Self-describing JSON/XML aggregates, secondary indexes, forgiving aggregate design, popular NoSQL with strong tooling | Sharding adds complexity; ACID limited to a collection | Read priority | MongoDB, Couchbase, AWS DocumentDB |
| **Column family** | Horizontal scaling for high read/write throughput, default replication factor 3, tunable consistency, sparse-data efficient via SSTables | Steep learning curve; row-key design takes iteration; super columns are hard | Write priority (high write volume) | Cassandra, Scylla, Amazon SimpleDB |
| **Graph** | Edges as first-class objects make traversal very fast; built-in algorithms (Dijkstra, similarity); ACID in some engines (Neo4j) | Steep learning curve; modeling is hard; sharding writes is hard; relationship-type changes are expensive | Read priority (relationship traversal) | Neo4j, Infinite Graph, Tiger Graph |
| **NewSQL** | SQL + ACID + horizontal scaling via automated sharding; multiple active nodes; survives disk/machine/datacenter failures (CockroachDB) | Sharding design adds wrinkle; some only available as DBaaS | Balanced | VoltDB, ClustrixDB, SimpleStore (aka MemSQL) |
| **Cloud-native** | No upfront cost, automatic scaling, low operational burden, cross-region replication (Snowflake), ACID supported | Variable learning curves (Datomic uses Clojure); tooling/talent gaps; cost grows with scale | Varies (Snowflake/Redshift read-heavy; Datomic balanced) | Snowflake, Redshift, Datomic, CosmosDB |
| **Time-series** | Append-only model fits IoT/observability; automatic timestamping; tag-based querying over time windows; some SQL-like dialects (InfluxQL) | Append-only requires unlearning update/delete; not general-purpose; tag design discipline needed | Read priority | InfluxDB, kdb+, Amazon Timestream, TimeScale |

- **Aggregate orientation** (DDD term, Erik Evans) — the preference to operate on related data with complex structure as one unit. Benefits: easy distribution across cluster nodes, fewer joins, less impedance mismatch. Shortcomings: hard to define correct aggregate boundaries; cross-aggregate analysis is difficult.
- **Schema-less is a misnomer** — NoSQL stores still have a schema, just implicit; applications must handle multiple versions returned at once.
- **Sharding vs partitioning** — partitioning splits table data within one database server; sharding splits data across nodes via a sharding key.

## 6. Sysops Squad: justifying decomposition and polyglot databases

- **Justification accepted** — Addison and Devon convinced Dana with three concrete signals: reporting queries blocked ticketing via shared connections, projected service growth required ~2,000 additional connections, and the shared database created an availability SPOF for ticketing.
- **Six data domains identified** — Customer, Survey, Payment, Profile, Knowledge Base, Ticketing, with Sysops Squad tables assigned to each (e.g., `billing`/`contract`/`payment_method` to Payment; `ticket`/`ticket_history` to Ticketing).
- **Cross-domain view rewritten** — `payment.v_customer_contract` originally joined `payment.contract`, `customer.customer`, and `payment.billing`; the rewrite removes the join to `customer.customer` and the `customer_name` column, forcing the Payment service to call the Customer service for the name.
- **Polyglot decision: Survey moves to a document database** — Marketing required frequent, low-friction survey changes; relational rendering was painful for the UI. ADR records the decision and the trade-off (single aggregate accepted question duplication in exchange for one-shot retrieval and simpler UI rendering).
- **Survey aggregate modeling** — single aggregate (questions embedded in survey document) preferred over split aggregate (separate Question documents referenced by ID), because there are only five survey types and most changes add or remove questions.
