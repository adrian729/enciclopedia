# Service-Based Architecture

> *Fundamentals* Ch 14 is the sole source. Service-based is the most pragmatic distributed style — distributed, but without the cost and complexity of microservices or event-driven architecture. *The Hard Parts* doesn't cover the style as a style, but its decomposition machinery often *targets* a service-based topology as the stepping stone before microservices, and the granularity equilibrium in [Service Granularity](decomposition/service-granularity.md) applies fully.

## Table of Contents

- [1. Topology](#1-topology)
- [2. Domain Service Design](#2-domain-service-design)
- [3. User Interface Variants and the API Layer](#3-user-interface-variants-and-the-api-layer)
- [4. Data Topology](#4-data-topology)
- [5. When to Use and When Not To](#5-when-to-use-and-when-not-to)
- [6. Risks and Antipatterns](#6-risks-and-antipatterns)
- [7. Architecture Characteristic Ratings](#7-architecture-characteristic-ratings)
- [8. Example — Going Green](#8-example--going-green)
- [Sources](#sources)

## 1. Topology

> Service-based is a *hybrid variant of microservices* and one of the most pragmatic styles available — mostly because of its flexibility.

A macro-layered topology:

- **Separately deployed user interface** (one or many).
- **Separately deployed remote coarse-grained domain services** — typically ≤ 12.
- **A single shared monolithic database** (optionally split into per-domain databases).

| Property | Service-based shape |
|---|---|
| Number of services | Coarse-grained — typically no more than \~12 when sharing a database. |
| Service shape | Each represents a specific domain or subdomain (a *domain service*) and encompasses a meaningful slice of functionality (`OrderFulfillment`, `Shipping`). |
| Independence | Domain services are independent of each other and separately deployed. |
| Deployment | Containers (Docker, Kubernetes) optional but not required — services deploy like any monolithic application. |
| Instances | Each service typically deploys as a single instance; multiple instances + load balancer added when scalability, fault tolerance, or throughput demand it. |
| UI communication | Typically REST. Alternatives: messaging, RPC, an API layer with proxy/gateway, even SOAP. The UI usually embeds the **service locator** pattern (which can also live in an API Gateway). |

The cap on number of services comes from sharing one monolithic database — beyond \~12, change-control, scalability, and fault-tolerance problems compound.

## 2. Domain Service Design

Because domain services are coarse-grained, each is typically built as a layered architecture internally:

- **API access facade layer** — the entrypoint the UI calls. **Orchestrates** the business request inside the service.
- **Business layer.**
- **Persistence layer.**

An alternative is to partition each service into subdomains, modular-monolith style.

> **The defining advantage: ACID still works.** Coarse-grained services let standard ACID transactions (commit/rollback) keep database integrity inside one service. Microservices and BASE (basic availability, soft state, eventual consistency) can't match that.

E-commerce example: a single UI request hits the `OrderService` API facade, which orchestrates everything in-process — place the order, generate the order ID, apply payment, update inventory per product. The same flow in microservices would orchestrate many separately deployed services and require a [Saga](distributed/transactional-sagas.md) for any cross-service transactional behavior. If an expired credit card is detected during checkout, service-based rolls back cleanly; microservices needs a compensating update because `OrderPlacement` has already committed.

**Granularity trade-off.** Coarse grain helps integrity, but changing order placement requires testing and redeploying the *whole* `OrderService` (including payment processing). More code per service means more risk that something else breaks during a change. This is the disintegrator/integrator equilibrium of [Service Granularity](decomposition/service-granularity.md) playing out in the most permissive distributed style.

## 3. User Interface Variants and the API Layer

The architect can keep a single monolithic UI or split it apart, even **one UI variant per domain service**. Splitting improves overall scalability, fault tolerance, and agility. A typical ordering system can have a customer-facing UI for placing orders plus separate internal UIs for order packers and customer support.

An **API Gateway** or reverse proxy is optional. It sits between the UI and services and is useful for:

- Exposing domain-service functionality to external systems.
- Consolidating cross-cutting concerns — metrics, security, auditing, service discovery.
- Load-balancing services with multiple instances.

## 4. Data Topology

> **Unique in the distributed catalog.** Service-based is the only distributed style that can effectively support a **single shared monolithic database**.

The same database can also be broken into separate databases — even one per domain service, microservices-style. When splitting, ensure no other service needs that data; sharing data is usually preferable to invoking another domain service.

Schema-change risk is the main concern with the shared topology. Table changes can affect every service. The shared class files representing tables (called *entity objects*) usually live in a custom shared library (JAR/DLL), often containing SQL too.

### 4.1. The Single Shared-Library Antipattern

> **Antipattern.** Placing **all** entity objects in one shared library is the *least* effective approach: any table change forces every service to redeploy, even those that don't use the changed table.

Versioning the library helps but determining impact still requires manual analysis. The fix is **logical partitioning into multiple shared libraries**:

- Partition the database logically (e.g., `common`, `customer`, `invoicing`, `order`, `tracking`).
- Ship one shared library per partition: `customer_entities_lib`, `invoicing_entities_lib`, etc.
- A change in the `Invoicing` domain only affects services that import `invoicing_entities_lib`.
- A `common_entities_lib` shared by all services is fine, but changes there coordinate across all services. Lock the common entity objects in version control and let only the database team modify them.

> **Tip.** Make logical partitioning in the database as fine-grained as possible while still maintaining well-defined data domains.

## 5. When to Use and When Not To

**When to use:**

- Distributed needs with limited budget — far cheaper and simpler than microservices, EDA, or space-based.
- DDD-aligned designs where domain services map onto bounded contexts.
- Systems that benefit from ACID transactions on the service boundary.
- **Stepping stone** toward microservices: analyze later which domains genuinely need to be broken further. *Not every portion of an application needs to be microservices.* — Mark Richards.

**When not to use:**

- Domains requiring 5★ scalability or elasticity — service-based scores 3★/2★. Use space-based or microservices instead.
- Cases where every service requires its own database from the start.
- Heavy inter-service communication — that signals badly partitioned domains or the wrong style.

## 6. Risks and Antipatterns

- **Inter-service communication.** Typical in microservices but *avoided* in service-based. Heavy chatter between domain services usually signals badly partitioned domains or the wrong style.
- **Too many domain services.** Practical upper limit is \~12; beyond that, testing, deployment, monitoring, and database connections/changes start to suffer.
- **Single shared-library antipattern.** See [§ 4.1](#41-the-single-shared-library-antipattern).
- **Cross-domain change.** The first thing to govern is whether changes span multiple domain services. If they do, domain boundaries are wrong, or service-based isn't the right style. Measure how often one domain service calls another. Some flows legitimately require it (`OrderProcessing` calling `CustomerNotification`), but most orchestration should live in the UI or API Gateway, not between services.

## 7. Architecture Characteristic Ratings

| Characteristic | Rating |
|---|---|
| Overall cost | $$ |
| Partitioning | Domain |
| Quanta | 1 to many |
| Simplicity | ★★★ |
| Modularity | ★★★ |
| Maintainability | ★★★★ |
| Testability | ★★★★ |
| Deployability | ★★★★ |
| Evolvability | ★★★★ |
| Responsiveness | ★★★ |
| Scalability | ★★★ |
| Elasticity | ★★ |
| Fault tolerance | ★★★★ |

- **Domain-partitioned, 1-to-many quanta.** Services share a single database with single quantum by default; federating UI and database can produce multiple quanta. Going Green example: a customer-facing quantum (UI + database + `Quoting` and `Item Status` services) and an internal-operations quantum (separate UIs but a shared internal database for receiving, assessment, recycling) — two quanta total.
- **Strong four-star areas (agility / testability / deployability).** Splitting into separately deployed domain services enables faster change, better test coverage thanks to domain scoping, and more frequent deployments with less risk than a monolith. Together they shorten time-to-market.
- **Fault tolerance and availability (4★).** Even though services are coarse-grained, they are self-contained and (thanks to code/database sharing) avoid inter-service communication. If `Receiving` goes down, the other six services keep running.
- **Scalability (3★) and elasticity (2★).** Coarse grain limits both. Programmatic scaling is possible but replicates more functionality than finer-grained styles, making it less cost-effective.
- **DDD fit.** Coarse-grained, domain-scoped services map cleanly onto DDD bounded contexts.
- **ACID over eventual consistency.** Leverages ACID transactions better than any other distributed style because the transaction scope is the domain service.

## 8. Example — Going Green

An electronics-recycling pipeline:

| Step | Domain |
|---|---|
| 1 | Customer asks (web/kiosk) how much for an old device — **Quoting**. |
| 2 | Customer ships the device — **Receiving**. |
| 3 | Going Green assesses the device — **Assessment**. |
| 4 | If working, customer is paid — **Accounting**; status is checkable any time — **Item Status**. |
| 5 | Device is destroyed and parts recycled, or resold (Facebook Marketplace, eBay) — **Recycling**. |
| 6 | Periodic financial/operational reports — **Reporting**. |

Each domain becomes a separately deployed service. Customer-facing `Quoting` and `ItemStatus` need multiple instances for throughput; the rest run as single instances. Three UI domains (*Customer Facing*, *Receiving*, *Recycling and Accounting*) deliver UI-level fault tolerance, scalability, and security — external customers have no path to internal functions.

**Two physical databases**: one for external customer-facing operations, one for internal — across a network-zone boundary. One-way firewall rules let internal services read/update customer data but not vice versa, forming **two architectural quanta**. Alternative: internal table mirroring and external table synchronization.

`Assessment` changes constantly as new products arrive; isolating it as its own domain service yields agility, testability, and deployability. A stepping-stone analysis reveals that `Recycling` and `Accounting` should remain domain services, while `Assessment` should later be split into separate services per device type if the team moves to microservices.

## Granularity and Data Ownership

Service-based is where the granularity-and-ownership decisions become real: the equilibrium between disintegrators and integrators decides where to put the ≤ 12 service boundaries, and the data-ownership decision (single, common, or joint) decides whether the shared monolithic database survives or splits. Two pages walk these:

- [Service Granularity](decomposition/service-granularity.md) — the disintegrators and integrators, the Grains of Sand antipattern, the architect as facilitator.
- [Data Ownership](distributed/data-ownership.md) — single / common / joint ownership and the four joint-ownership resolution techniques.

## Sources

- [Fundamentals Ch 14: Service-Based Architecture Style](software/software-architecture/books/fundamentals-of-software-architecture/ch14_service_based_architecture.md) (sole source — topology, domain service design, API gateway options, data topology + single-shared-library antipattern, Going Green example, characteristic ratings)


<!-- prev-next-nav -->

---

← [Microkernel](software/software-architecture/styles/microkernel.md) | [Event-Driven](software/software-architecture/styles/event-driven.md) →
