# Ch 14: Managing Analytical Data

## Table of Contents

- [1. Operational vs analytical data](#1-operational-vs-analytical-data)
- [2. The Data Warehouse](#2-the-data-warehouse)
- [3. The Data Lake](#3-the-data-lake)
- [4. Data Warehouse vs Data Lake vs Data Mesh](#4-data-warehouse-vs-data-lake-vs-data-mesh)
- [5. The Data Mesh](#5-the-data-mesh)
- [6. Data Product Quantum](#6-data-product-quantum)
- [7. When to use Data Mesh](#7-when-to-use-data-mesh)
- [8. Sysops Squad: Data Mesh](#8-sysops-squad-data-mesh)

## 1. Operational vs analytical data

- **Two purposes, two shapes** — operational and analytical data have widely different purposes in modern architectures; the formats and schemas of one don't necessarily fit (or even allow) the other. Many analytical problems require aggregations and calculations, which are expensive on relational databases under heavy transactional load.
- **Long-standing split** — the split between operational and analytical data is not new. As architecture styles evolved (mainframes, then client/server with networked database servers), architects looked for ways to support specialized queries and historical analytics.

## 2. The Data Warehouse

- **Pattern** — extract operational data from many source databases, transform into a single denormalized **Star Schema** (facts + dimensions), load into a centralized warehouse; analysts query via a SQL-like interface to produce BI reports and dashboards.
- **Star Schema** — separates facts (quantifiable measurements such as hourly rate, time to repair) from dimensions (descriptive metadata such as squad specialties, store locations); deliberately denormalized for simpler joins, faster aggregations, and multidimensional queries.
- **Technical partitioning** — the warehouse organizes by ingestion/transformation/storage capabilities, dissolving domain boundaries that must then be re-created in queries.
- **Failings** — *integration brittleness* (schema changes ripple through ingestion logic), *extreme partitioning of domain knowledge* (architects, DBAs, data scientists must coordinate constantly), *complexity* (separate ecosystem to maintain), *limited functionality for intended purpose* (often can't answer the questions asked of it), *synchronization bottlenecks* (the convergence point couples otherwise independent streams), *operational vs analytical contract differences* (transformation pipelines amplify contract brittleness).

## 3. The Data Lake

- **Pattern** — inverse of the warehouse: keep centralized pipelines but replace "transform and load" with "load and transform"; dump operational data into the lake in raw form and let data scientists transform on demand.
- **Why it appeared** — pre-built warehouse schemas rarely fit the actual question; ML models often work better with semi-raw data; transforming away domain context just to query it back is wasteful.
- **Characteristics** — data extracted from many sources with little or no transformation, loaded (often in cloud storage) as regular dumps, used by data scientists who discover and aggregate as needed.
- **Limitations** — *difficulty discovering proper assets* (relationships evaporate without structure), *PII risk* (unstructured dumps can expose information that can be stitched together to violate privacy), *still technically partitioned, not domain partitioned* (data is severed from its originating context), and *staleness* from batch ingestion if upstream changes aren't tracked.

## 4. Data Warehouse vs Data Lake vs Data Mesh

| Dimension | Data Warehouse | Data Lake | Data Mesh |
|-----------|---------------|-----------|-----------|
| Partitioning | Technical | Technical | Domain |
| Transformation timing | ETL up front | Load raw, transform later | Per-domain at the **Data Product Quantum** |
| Centralization | Centralized warehouse | Centralized lake | Decentralized peer-to-peer |
| Ownership | Central data team | Central data team | Owning domain teams |
| Schema | Star Schema, denormalized | Raw / minimal | Domain-defined product contract |
| Best fit | Monolithic, transactional eras | Early distributed, ML-heavy | Modern microservices with domain isolation |
| Main risk | Brittleness, limited functionality | Discovery, PII, staleness | Requires async + eventual consistency, contract coordination |

## 5. The Data Mesh

- **Definition** — *a sociotechnical approach to sharing, accessing, and managing analytical data in a decentralized fashion*; supports reporting, ML training, and insight generation by aligning data ownership with business domains and enabling peer-to-peer consumption.
- **Domain ownership of data** — data is owned by the domains that originate or first-consume it; no central lake/warehouse and no dedicated data team.
- **Data as a product** — domains serve data through organizational roles and metrics that prioritize the consumer experience; the architectural unit is the **Data Product Quantum**.
- **Self-serve data platform** — platform capabilities for declarative creation, discovery, lineage, and knowledge graphs across the mesh.
- **Computational federated governance** — federated decision-making among domain product owners; policies (compliance, security, privacy, quality, interoperability) are automated as code embedded in each Data Product Quantum's sidecar.

## 6. Data Product Quantum

- **DPQ structure** — a quantum adjacent to a service, containing both code and data, acting as the analytical interface; operationally independent yet contract-coupled to its service.
- **Source-aligned (native) DPQ** — provides analytical data on behalf of one collaborating service.
- **Aggregate DPQ** — combines data from multiple inputs synchronously or asynchronously.
- **Fit-for-purpose DPQ** — custom-built to serve a specific reporting, BI, or ML need.
- **Cooperative quantum** — *operationally separate quantum that communicates with its cooperator via asynchronous communication and eventual consistency, yet features tight contract coupling with its cooperator and generally looser contract coupling to the analytics quantum.*
- **Static coupling** — the DPQ and its communication implementation belong to the static coupling of the architecture quantum; in a microservices architecture, the service plane must be available, just as a message broker must be available if messaging is used. Like the Sidecar pattern in a service mesh, the DPQ stays orthogonal to in-service implementation changes and maintains a separate contract with the data plane.
- **Dynamic coupling** — must use **Parallel Saga(aeo)** or **Anthology Saga(aec)** patterns; never a transactional sync between operational and analytical data, which would defeat orthogonal decoupling.

## 7. When to use Data Mesh

- **Trade-offs** — *Advantages*: highly suitable for microservices, follows modern architecture principles, excellent decoupling between operational and analytical data, carefully formed contracts allow loose evolution. *Disadvantages*: requires contract coordination with each DPQ; requires asynchronous communication and eventual consistency.
- **Best fit** — distributed architectures with well-contained transactionality and good service isolation; domain teams control the cadence, quality, and transparency of shared data.
- **Hard fit** — environments demanding analytical and operational data to stay in sync at all times; very strict contracts with eventual consistency can mitigate this.

## 8. Sysops Squad: Data Mesh

- **Rejected alternatives** — Data Warehouse fit older monolithic systems and couldn't support the ML use cases now needed; Data Lake still suffered from technical (not domain) partitioning and PII concerns.
- **Per-service DPQs** — every new service ships with a DPQ owned and maintained by the same domain team responsible for the service.
- **Aggregation point** — the **Tickets DPQ** is its own architecture quantum, aggregating ticket views consumed by other systems.
- **Self-serve platform** — the data mesh platform team supplies discovery, connection, monitoring, and governance compliance tooling; downtime and policy violations are flagged back to domain teams.
- **Federated governance group** — domain data product owners, security, legal, risk, compliance, and platform product owners jointly standardize sharing contracts, async transport modes, and access control; the platform pushes new policy capabilities into DPQ sidecars uniformly.
- **Experts Supply DPQ outcome** — new aggregate DPQ takes async input from the Tickets DPQ (long-term ticket history), User Maintenance DPQ (daily expert profile snapshots), and Survey DPQ (customer survey log) to feed an ML model producing daily *supply recommendations*.
- **ADR outcome** — Expert Supply DPQ source feeds must deliver a complete day's snapshot or none (so an empty day can be exempted from trend analysis); two fitness functions enforce this — a *complete daily snapshot* check based on message timestamps (>1 minute gap marks the day exempt) and a *consumer-driven contract* between the Ticket DPQ and Expert Supply DPQ to prevent internal Ticket Domain evolution from breaking the aggregate.
