# Ch 10: Distributed Data Access

## Table of Contents

- [1. The read-access problem](#1-the-read-access-problem)
- [2. Interservice Communication pattern](#2-interservice-communication-pattern)
- [3. Column Schema Replication pattern](#3-column-schema-replication-pattern)
- [4. Replicated Caching pattern](#4-replicated-caching-pattern)
- [5. Data Domain pattern](#5-data-domain-pattern)
- [6. Comparing the four data access patterns](#6-comparing-the-four-data-access-patterns)
- [7. Sysops Squad saga: ticket assignment](#7-sysops-squad-saga-ticket-assignment)

## 1. The read-access problem

- **Why reads are hard now** — in monoliths a single SQL join retrieves anything; once data is split into per-service schemas, services need read access to data they no longer own.
- **Running example** — a Wishlist Service must show item descriptions, but the description column lives in the Catalog Service's Product table.
- **Four patterns** — Interservice Communication, Column Schema Replication, Replicated Caching, Data Domain; each balances coupling, consistency, performance, and data volume differently.

## 2. Interservice Communication pattern

- **Mechanism** — the consumer makes a remote call (REST, gRPC, messaging) to the owning service to fetch the data on demand.
- **Latency stack** — *network latency* (~30–300 ms), *security latency* (~20–400 ms when endpoints are secured), *data latency* (~10–50 ms for the extra database call inside the owning service); cumulative latency can approach a second.
- **Coupling cost** — semantic and static coupling: if the Catalog Service is unavailable the Wishlist Service is too; both must scale together.
- **Best fit** — simple cases with low call volume, no fault-tolerance pressure, and large data volumes that rule out replication-based patterns.

## 3. Column Schema Replication pattern

- **Mechanism** — the columns the consumer needs (e.g., `item_desc`) are replicated into the consumer's own table so it can serve queries locally.
- **Synchronization** — owner pushes changes via async messaging or event streams; preferred over synchronous to keep responsiveness and decouple availability.
- **Data ownership risk** — because the column physically lives in the consumer's table, the consumer can update it even though it does not own it; governance is required.
- **Best fit** — data aggregation, reporting, or situations where the other patterns are not a good fit because of large data volumes, high responsiveness requirements, or high-fault-tolerance requirements; the authors generally caution against this pattern for scenarios like the Wishlist/Catalog example.

## 4. Replicated Caching pattern

- **Mechanism** — every consumer holds an in-memory replica of the owner's cache; cache instances synchronize behind the scenes when the owner updates.
- **Replicated vs other caching models** — *single in-memory cache* (per-service, no sharing) is unsuitable for cross-service data; *distributed cache* (external caching server) shifts the fault-tolerance dependency to the cache server, allows other services to update data and break ownership, and adds network latency on retrieval; *replicated* keeps in-memory copies inside each service and synchronizes them.
- **Owner semantics** — the owning service is the sole writer (e.g., Catalog Service); consumers (e.g., Wishlist Service) hold a read-only replica.
- **Supported products** — Hazelcast, Apache Ignite, Oracle Coherence (not all caching products support replicated mode).
- **Startup dependency** — only the *first* consumer instance must wait for the owner to be running; subsequent consumer instances bootstrap from peer caches and the owner can disappear afterward without disrupting the consumer.
- **Volume ceiling** — feasibility drops past ~500 MB; replicated cache memory cost scales by `cache size × number of consumer instances` (e.g., 500 MB × 5 instances = 2.5 GB).
- **Update-rate ceiling** — high write churn (e.g., inventory counts) cannot stay in sync; pattern fits relatively static data (e.g., product descriptions).
- **Configuration challenge** — services discover each other via TCP/IP broadcast and lookups; cloud and containerized environments make this harder due to dynamic IPs.

## 5. Data Domain pattern

- **Mechanism** — shared tables are placed in a single schema accessible to multiple services, forming a broader bounded context (the same Data Domain Technique introduced for joint ownership in Chapter 9).
- **What it gains** — full decoupling of services, native SQL joins, very high consistency and integrity (foreign keys, views, stored procedures, triggers all available), no replication or synchronization overhead.
- **Contract trade-off** — the table schema *is* the contract; structural changes to any shared table can ripple to multiple services, unlike the abstraction layer offered by Interservice Communication or Replicated Cache.
- **Security trade-off** — co-locating data exposes it to all services attached to the schema; tighter bounded contexts with explicit contracts can restrict access more precisely.
- **Best fit** — high data volumes that defeat replication, high consistency/integrity needs, scenarios where the other three patterns fail their own constraints.

## 6. Comparing the four data access patterns

| Pattern | Mechanism | Performance | Service coupling | Data consistency | Notable limit |
|---------|-----------|-------------|------------------|------------------|---------------|
| **Interservice Communication** | Remote call on demand | Poor (latency stack) | High (availability + scaling) | Always current | Scales/fails with the owner |
| **Column Schema Replication** | Replicate columns into consumer table | Good | Decoupled at runtime | Eventual; ownership leaks | Sync infrastructure required |
| **Replicated Caching** | In-memory replica per consumer | Very good | Decoupled after startup | Consistent for low-churn data | Data volume and update rate; cloud/container config |
| **Data Domain** | Shared schema across services | Very good | Decoupled | Strong (SQL + constraints) | Broader bounded context; security exposure |

## 7. Sysops Squad saga: ticket assignment

- **Problem** — Ticket Assignment Service must continuously query the expert profile table now owned by the User Management Service; remote calls per query were not feasible.
- **Eliminated options** — Service Consolidation (services live in different domains), Data Domain (Ticket Assignment already connects to the ticketing data domain and a service cannot attach to two schemas), so the choice narrowed to Interservice Communication or Replicated Caching.
- **Sizing analysis** — 900 experts × ~1.3 KB per expert ≈ 1,200 KB total; up to 2 User Management instances and up to 4 Ticket Assignment instances; total in-memory footprint is small and the data is mostly static.
- **Decision** — Replicated Caching with the User Management Service as the sole writer; resolves the performance and fault-tolerance pain of remote calls.
- **Consequences accepted** — startup ordering (at least one User Management instance must be running before the first Ticket Assignment instance), licensing cost for the chosen caching product, and team learning curve mitigated by a planned proof-of-concept.
