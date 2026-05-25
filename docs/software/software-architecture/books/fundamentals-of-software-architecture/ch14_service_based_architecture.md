# Ch 14: Service-Based Architecture Style

## Table of Contents

- [1. Topology](#1-topology)
- [2. Domain Service Design and Granularity](#2-domain-service-design-and-granularity)
- [3. User Interface Variants](#3-user-interface-variants)
- [4. API Gateway Options](#4-api-gateway-options)
- [5. Data Topologies](#5-data-topologies)
- [6. Cloud Considerations](#6-cloud-considerations)
- [7. Common Risks](#7-common-risks)
- [8. Governance](#8-governance)
- [9. Team Topology Considerations](#9-team-topology-considerations)
- [10. Style Characteristics](#10-style-characteristics)
- [11. Examples and Use Cases: Going Green](#11-examples-and-use-cases-going-green)

## 1. Topology

- **Pragmatic distributed hybrid** — *service-based architecture* is a hybrid variant of microservices and one of the most pragmatic styles available, mostly because of its flexibility. It is distributed but does **not** carry the same complexity and cost as microservices or event-driven architecture, which makes it popular for business applications.
- **Macro-layered topology** — a separately deployed user interface, separately deployed remote **coarse-grained services**, and (optionally) a single shared monolithic database.
- **Domain services** — services typically represent a specific domain or subdomain (called *domain services*), are coarse-grained, encompass a meaningful slice of functionality (e.g., order fulfillment, order shipping), are independent of each other, and are separately deployed. They deploy like any monolithic application — containers (Docker, Kubernetes) are an option but not required.
- **Cap on number of services** — when using a single shared monolithic database, keep domain services to **no more than 12** to avoid change-control, scalability, and fault-tolerance problems.
- **Single instance per service (default)** — each domain service typically deploys as a single instance; multiple instances can be added when scalability, fault tolerance, or throughput needs demand it, in which case a load balancer sits between the UI and the service.
- **Remote access** — UIs reach services via a remote protocol (typically REST; alternatives include messaging, RPC, an API layer with proxy/gateway, or even SOAP). The UI usually embeds the **service locator pattern** (which can also live inside an API Gateway/proxy) so it can call services directly.
- **Shared monolithic database is typical** — services can use SQL queries and joins as a layered monolith would. Because the number of services is small, exhausting connections is rarely an issue; managing schema changes is the real challenge.

## 2. Domain Service Design and Granularity

- **Internal layered design** — because domain services are coarse-grained, each is typically built with a layered shape: API Facade layer, Business layer, Persistence layer. An alternative is to partition each service into subdomains (modular-monolith style).
- **API access facade orchestrates** — every domain service must expose an API access facade that the UI talks to; this facade orchestrates the business request internally.
- **Ecommerce ordering example** — a single UI request hits the `OrderService` API facade, which orchestrates everything in-process: place the order, generate the order ID, apply payment, update inventory per product. Microservices would orchestrate many separately deployed services for the same flow — an important *granularity* difference.
- **ACID transactions inside a service** — coarse-grained services let standard ACID transactions (commit/rollback) keep database integrity inside a single domain service. Compare with microservices and BASE (basic availability, soft state, eventual consistency), which can't match that integrity. Example: an expired credit card during checkout can be cleanly rolled back in service-based; in microservices, the order has already been inserted by `OrderPlacement` and a *compensating update* is needed to restore consistency.
- **Granularity trade-off** — coarse grain helps integrity, but changing order placement in the `OrderService` requires testing and redeploying the whole service (including payment processing). With more code per service there is more risk that something else breaks during a change.

## 3. User Interface Variants

- **Many UI variants** — the architect may keep a single monolithic UI or split it apart, even one **user interface variant** per domain service. Splitting improves overall scalability, fault tolerance, and agility.
- **Real-world example** — a typical ordering system can have a customer UI for placing orders, plus separate internal UIs for order packers and customer support.

## 4. API Gateway Options

- **Optional API layer** — a reverse proxy or API Gateway can sit between the UI and the services. Useful for exposing domain-service functionality to external systems, consolidating cross-cutting concerns (metrics, security, auditing, service discovery), and load-balancing services that have multiple instances.

## 5. Data Topologies

- **Database topology spectrum** — service-based is unique among distributed architectures in being able to effectively support a **single shared database**. The same database can also be broken into separate databases — even one per domain service (microservices-style). When splitting, ensure no other service needs that data; sharing data is usually preferable to invoking another domain service.
- **Schema-change risk** — with a shared monolithic database, table changes can affect every service. The shared class files representing tables (called *entity objects*) usually live in a custom shared library (JAR/DLL), often containing SQL too.
- **Single-shared-library antipattern** — placing **all** entity objects in one shared library is the *least* effective approach: any table change forces every service to redeploy, even those that don't use the changed table. Versioning the library helps but determining impact still requires manual analysis. This is considered an antipattern in service-based architecture.
- **Logical partitioning into multiple shared libraries** — partition the database logically (e.g., common, customer, invoicing, order, tracking) and ship one shared library per partition. A change in the `Invoicing` domain only affects services that import `invoicing_entities_lib`.
- **Common library considerations** — a `common_entities_lib` shared by all services is fine, but changes to its tables coordinate across all services. Lock the common entity objects in version control and let only the database team modify them.
- **Tip** — make logical partitioning in the database as fine-grained as possible while still maintaining well-defined data domains.

## 6. Cloud Considerations

- **Good cloud fit** — being distributed, service-based works well in the cloud despite its coarse-grained services. Services are typically containerized (not serverless functions) due to their large scope and easily leverage cloud file storage, database, and messaging services.

## 7. Common Risks

- **Inter-service communication** — typical in microservices but **avoided** in service-based. Heavy chatter between domain services usually signals badly partitioned domains or the wrong style for the problem.
- **Too many domain services** — practical upper limit is ~12; beyond that, testing, deployment, monitoring, and database connections/changes start to suffer.

## 8. Governance

- **Cross-domain change is a smell** — the first thing to govern is whether changes span multiple domain services. If they do, domain boundaries are wrong, or service-based isn't the right style.
- **Limit inter-service communication** — measure how often one domain service calls another. Some flows legitimately require it (e.g., `OrderProcessing` calling `CustomerNotification`), but most orchestration should live in the UI or API Gateway, not between services.

## 9. Team Topology Considerations

Service-based is *domain-partitioned*; teams should align by domain area. Technically partitioned teams (UI/backend/DB) struggle because every domain change requires cross-team coordination.

- **Stream-aligned teams** — work well when domain boundaries are properly aligned and streams are scoped to a domain. Streams that cross domain boundaries call for re-evaluating granularity or a different style.
- **Enabling teams** — less effective than with finer-grained distributed styles because services are coarse-grained; modularity can be increased by carefully identifying components inside each service for specialists to experiment with.
- **Complicated-subsystem teams** — leverage domain-level and subdomain-level modularity to focus on complicated processing independently of other teams and services.
- **Platform teams** — high modularity helps platform teams provide common tools, services, APIs, and tasks.

## 10. Style Characteristics

| Characteristic | Rating |
|---|---|
| Overall cost | $$ |
| Partitioning type | Domain |
| Number of quanta | 1 to many |
| Simplicity | 3 stars |
| Modularity | 3 stars |
| Maintainability | 4 stars |
| Testability | 4 stars |
| Deployability | 4 stars |
| Evolvability | 4 stars |
| Responsiveness | 3 stars |
| Scalability | 3 stars |
| Elasticity | 2 stars |
| Fault tolerance | 4 stars |

- **Domain-partitioned, 1-to-many quanta** — services share a single shared database with single quantum by default; federating UI and database can produce multiple quanta. Going Green example: a customer-facing quantum (UI + database + `Quoting` and `Item Status` services) and an internal-operations quantum (separate UIs but a shared internal database for receiving, assessment, recycling) — two quanta total.
- **Strong four-star areas (agility/testability/deployability)** — splitting into separately deployed domain services enables faster change, better test coverage thanks to domain scoping, and more frequent deployments with less risk than a monolith. Together they shorten time to market.
- **Fault tolerance and availability (4★)** — even though services are coarse-grained, they are self-contained and (thanks to code/database sharing) avoid inter-service communication. If `Receiving` goes down, the other six services keep running.
- **Scalability (3★) and elasticity (2★)** — coarse grain limits both. Programmatic scaling is possible but replicates more functionality than finer-grained styles, making it less cost-effective. Most services run as a single instance unless throughput or failover demands more (e.g., Going Green's `Quoting` and `Item Status`).
- **Simplicity and cost** — much cheaper and simpler than microservices, EDA, or space-based architecture; a top reason teams choose it. Trade-off: those higher-cost styles score better on scalability, elasticity, and fault tolerance.
- **DDD fit** — coarse-grained, domain-scoped services map cleanly onto DDD bounded contexts.
- **ACID over eventual consistency** — leverages ACID transactions better than any other distributed style because the transaction scope is the domain service.
- **Stepping stone** — service-based architectures make good migration targets *before* moving to microservices: analyze which domains genuinely need to be broken further. *Not every portion of an application needs to be microservices.* — Mark Richards.

## 11. Examples and Use Cases: Going Green

- **Going Green processing flow** — electronics recycling pipeline:
  1. Customer asks (web/kiosk) how much for an old device — *quoting*.
  2. Customer ships the device — *receiving*.
  3. Going Green assesses the device — *assessment*.
  4. If working, the customer is paid — *accounting*; status is checkable any time — *item status*.
  5. Device is destroyed and parts recycled, or resold (Facebook Marketplace, eBay) — *recycling*.
  6. Periodic financial/operational reports — *reporting*.
- **Service breakdown** — each domain becomes a separately deployed service. Customer-facing `Quoting` and `ItemStatus` need multiple instances for throughput; the rest run as single instances.
- **UI partitioning** — three UI domains (*Customer Facing*, *Receiving*, *Recycling and Accounting*) deliver UI-level fault tolerance, scalability, and security (external customers have no path to internal functions).
- **Two physical databases** — one for external customer-facing operations, one for internal — across a network-zone boundary; one-way firewall rules let internal services read/update customer data but not vice versa, forming **two architectural quanta**. Alternative: internal table mirroring and external table synchronization.
- **High-change service** — `Assessment` changes constantly as new products arrive; isolating it as its own domain service yields agility, testability, and deployability.
- **Migration insight** — a stepping-stone analysis of Going Green reveals that `Recycling` and `Accounting` should remain domain services, while `Assessment` should be split into separate services per device type if the team eventually moves to microservices.
