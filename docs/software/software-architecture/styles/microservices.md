# Microservices Architecture

> *Fundamentals* Ch 18 is the primary source. Microservices was *named*, not discovered — Martin Fowler and James Lewis's 2014 blog post crystallized its characteristics. *The Hard Parts* assumes microservices and supplies almost all of its machinery: granularity ([Service Granularity](decomposition/service-granularity.md)), data ownership ([Data Ownership](distributed/data-ownership.md)), the eight saga patterns ([Transactional Sagas](distributed/transactional-sagas.md)). This page covers the style; the linked pages cover the problems.

## Table of Contents

- [1. Origins and Philosophy](#1-origins-and-philosophy)
- [2. Topology](#2-topology)
- [3. Bounded Context and Data Isolation](#3-bounded-context-and-data-isolation)
- [4. Service Granularity — Three Iteration Criteria](#4-service-granularity--three-iteration-criteria)
- [5. API Layer and Frontends](#5-api-layer-and-frontends)
- [6. Operational Reuse — Sidecar and Service Mesh](#6-operational-reuse--sidecar-and-service-mesh)
- [7. Communication — Sync vs. Async](#7-communication--sync-vs-async)
- [8. Choreography and Orchestration](#8-choreography-and-orchestration)
- [9. Transactions and Sagas](#9-transactions-and-sagas)
- [10. Data Topology](#10-data-topology)
- [11. Cloud and Serverless](#11-cloud-and-serverless)
- [12. When to Use and When Not To](#12-when-to-use-and-when-not-to)
- [13. Risks and Antipatterns](#13-risks-and-antipatterns)
- [14. Architecture Characteristic Ratings](#14-architecture-characteristic-ratings)
- [15. Example — Patient Monitoring](#15-example--patient-monitoring)
- [Sources](#sources)

## 1. Origins and Philosophy

> Microservices was named, not discovered — Martin Fowler and James Lewis's 2014 blog post crystallized its characteristics.

Three core ideas inherited from DDD:

- **Bounded context.** Code, schemas, and data inside a context can be coupled internally, but never coupled to anything outside.
- **Share-nothing architecture.** Logical bounded context modeled physically as service + corresponding data.
- **Duplication is preferable to coupling.** Reuse is implemented *via* coupling, so a highly decoupled architecture must favor duplication. Common classes like `Address` are duplicated across services rather than shared.

Enabled by cheap infrastructure — open source operating systems plus automated provisioning, cloud, and containers made per-domain infrastructure practical, unlocking decoupling at both the domain and operational level. Microservices was the *architectural cash-in* of the DevOps revolution.

Performance is the price. Network calls plus per-endpoint security verifications are far slower than in-process calls, forcing architects to think hard about granularity.

## 2. Topology

- **Single-purpose, very small services.** Much smaller than in orchestration-driven SOA, EDA, or service-based architecture; each service includes everything (databases, dependent components) needed to run independently.
- **Distributed by definition.** Each service runs in its own process inside a VM or container; this extreme decoupling solves resource contention and isolation problems caused by multitenant application servers.

> *The term microservice is a label, not a description.* — Martin Fowler.

## 3. Bounded Context and Data Isolation

- **Bounded context = service + everything it needs** — components, classes, schemas, and the database itself.
- **Duplicate, don't share.** Common classes are duplicated across services rather than shared.
- **Data isolation is mandatory.** Microservices avoids *all* coupling, including shared schemas. Each domain decides whether to be a single source of truth that others query, or to distribute information through replication or caching. See [Data Ownership](distributed/data-ownership.md).
- **Beware the Entity Trap.** Don't model services as single database entities. Architects must abandon the relational habit of unifying all values around one source of truth.
- **Database freedom as upside.** Once freed from a unified database, each team can pick the storage technology that best fits its service's budget, structure, and operational profile; teams can also switch databases later without affecting other services.

## 4. Service Granularity — Three Iteration Criteria

> **The defining problem.** Taking *micro* literally yields services so fine-grained that wiring them back together produces a **Big Ball of Distributed Mud**.

Three boundary guidelines:

| Criterion | Question |
|---|---|
| **Purpose** | Is the service one cohesive behavior in the problem domain? |
| **Transactions** | Do these entities need to transact together? If yes, they suggest a single service boundary. |
| **Choreography** | If services chat too much, fold them back into a coarser service. |

> **Iteration is the only path.** Perfect granularity, data dependencies, and communication styles are never found on the first pass; refine as the domain is better understood.

The full vocabulary — the six disintegrators and four integrators, the equilibrium framing, and the Grains of Sand antipattern — is in [Service Granularity](decomposition/service-granularity.md).

## 5. API Layer and Frontends

- **API gateway** sits between consumers (UIs, other systems) and services. Can be a simple reverse proxy or a richer gateway carrying cross-cutting concerns like security, naming, and service discovery.
- **No business logic at the gateway.** The API layer must not act as a mediator or orchestrator; all business logic belongs inside a bounded context. Mediators belong in technically partitioned styles, not domain-partitioned microservices.
- **Monolithic frontend.** A single rich-desktop, mobile, or web UI (often a JavaScript SPA) calls services through the API layer.
- **Micro-frontends.** UI components map one-to-one onto backend services, extending bounded-context isolation up to the user interface; see Luca Mezzalira's *Building Micro-Frontends*, 2nd ed. (O'Reilly, 2025).

## 6. Operational Reuse — Sidecar and Service Mesh

Microservices splits *domain reuse* (forbidden — duplicate instead) from *operational reuse* (encouraged — share via mesh):

| Concern | Approach |
|---|---|
| **Domain logic** | Duplicated and isolated per bounded context. |
| **Operational concerns** — monitoring, logging, circuit breakers, auth, metrics | Genuinely benefit from coupling; share via sidecar + service mesh. |

- **Sidecar pattern.** Each service ships with a sidecar component that handles shared operational concerns; a shared infrastructure team can upgrade the sidecar and every service inherits the new capability.
- **Service mesh.** Connecting all sidecars through a *service plane* (e.g., **Istio**) creates a single console where teams globally control monitoring levels, logging, and other cross-cutting operational concerns across the architecture.
- **Service discovery.** A tool that automatically detects, locates, and elastically scales services; often hosted in the API layer or built into the mesh so callers have one consistent place to find services.

The sidecar/mesh is the canonical implementation of **orthogonal coupling** — see [Styles Overview § 10.1](styles/overview.md#101-reuse--separating-domain-and-operational-coupling).

## 7. Communication — Sync vs. Async

The foundational choice.

- **Sync** waits for a response.
- **Async** (events and messages, EDA-style) decouples in time.
- **Protocol-aware heterogeneous interoperability** — the typical sync model.
  - **Protocol-aware** — services standardize on how they call each other (a REST profile, a queue, etc.).
  - **Heterogeneous** — polyglot stacks are first-class.
  - **Interoperability** — services collaborate over the network without distributed transactions.
- **Enforced heterogeneity (sidebar).** A microservices pioneer mandated that each team use a different stack (Java vs. .NET) so accidental class sharing was physically impossible — the polar opposite of typical enterprise standardization.

## 8. Choreography and Orchestration

| Pattern | Behavior |
|---|---|
| **Choreography (default)** | No central coordinator: each service calls others as needed (e.g., `CustomerWishList` directly calls `CustomerDemographics`). Respects bounded-context philosophy. Yields the most decoupling. |
| **Local orchestration** | For cross-service coordination, build a *localized* mediator — an *orchestration service* (e.g., `ReportCustomerInformation`). |
| **No global mediator** | Microservices has no global mediator. |

**Front Controller antipattern.** When a nominally choreographed service ends up coordinating many others, it becomes a de facto mediator with extra responsibilities and added complexity.

Choreography preserves decoupling but complicates error handling and coordination; orchestration centralizes coupling in one service so the others stay clean. The First Law applies — neither is universally right.

See [Workflows & Orchestration](distributed/workflows-orchestration.md) for the full trade-off table and semantic-coupling discussion.

## 9. Transactions and Sagas

> **Avoid cross-service transactions** — they violate the core decoupling principle and create *Connascence of Values* (the worst dynamic connascence). **Don't do them — fix the granularity instead.** Needing transactions to wire services together is a sign the design is too granular.

When transactional coordination is unavoidable:

- **Saga pattern.** A mediator drives each participating service, records success or failure, and coordinates the result. The name comes from the literary *saga* — a long sequence of events leading to a heroic conclusion.
- **Compensating transaction framework.** On partial failure, the mediator instructs successful participants to undo their work; participants typically hold a `pending` state until the mediator confirms overall success. This generates significant network coordination traffic.

If transactions become the dominant feature of the architecture, microservices is likely the wrong style.

The full eight-pattern saga catalog — Epic Saga, Phone Tag, Fairy Tale, Time Travel, Fantasy Fiction, Horror Story, Parallel, Anthology — is at [Transactional Sagas](distributed/transactional-sagas.md).

## 10. Data Topology

> **The only style that *requires* breaking up data.** Monolithic and even domain-based databases aren't viable at microservices scale.

| Topology | Behavior |
|---|---|
| **Monolithic shared DB** | Not viable. 60 services sharing one DB makes a column rename a 60-service coordinated release; the bounded context collapses; the database can't elastically scale with the services; connection pools exhaust; one DB outage kills the entire ecosystem. |
| **Database-per-service** (standard) | Each service owns its data in a separate database or schema. Other services request data through a contract, decoupling them from internal structure and freeing each team to switch DB type without rippling change. |
| **Limited sharing exception** | When two or more services genuinely write the same table (e.g., split payment-type services), a few services may share one DB inside a *broader bounded context*. Cap it at five or six; beyond that, the change-control, scalability, and fault-tolerance pains return. |

## 11. Cloud and Serverless

- **Cloud-native fit.** On-demand provisioning of VMs, containers, and databases plus the cloud's services-based model are an exceptional fit. Works on-prem too with Kubernetes or Cloud Foundry.
- **Serverless is a deployment model, not a style.** AWS Lambda, Google Cloud Functions, and Azure Functions describe single-purpose units that match the microservices definition; the authors classify serverless as a *deployment model* of microservices.
- **Containers are equally valid.** Most cloud vendors run Kubernetes, so containerized microservices deploy as easily as serverless ones; the choice is operational, not architectural.

## 12. When to Use and When Not To

**When to use:**

- Systems with high functional and data modularity (clean bounded contexts).
- High requirements for scalability, elasticity, fault tolerance, evolvability.
- Teams with strong DevOps and automation maturity.
- Patient-monitoring, e-commerce, large SaaS — domains that decompose into independent contexts.

**When not to use:**

- Domains that don't decompose cleanly into bounded contexts.
- Teams lacking Agile engineering and automation maturity.
- Heavy transactional coupling — if transactions are the dominant concern, use service-based or modular monolith instead.
- Performance-critical paths that can't tolerate network overhead.

## 13. Risks and Antipatterns

- **Grains of Sand antipattern.** Coined by Mark Richards in 2016 for services made too fine-grained, like grains of sand on a beach. *Micro* refers to *what* the service does, not how big it is. See [Service Granularity § 5](decomposition/service-granularity.md#5-the-grains-of-sand-antipattern).
- **Excessive interservice communication.** Fine granularity plus tight bounded contexts forces chatter; fix by combining services into coarser ones rather than tolerating dynamic coupling.
- **Over-sharing data.** Undermines the architecture's superpowers (change control, scalability, fault tolerance, agility). Consolidate services rather than share data freely.
- **Code reuse via shared libraries.** Sharing JAR/DLL functionality breaks the share-nothing principle: a change to shared code can break services across multiple bounded contexts. Versioning helps but adds complication.
- **Front Controller** — a nominally choreographed service that drifts into mediation responsibilities. See [§ 8](#8-choreography-and-orchestration).
- **Entity Trap** — modeling services as single database entities. See [§ 3](#3-bounded-context-and-data-isolation).

Governance:

- **Govern static and dynamic coupling.** Static coupling appears in shared libraries and contracts; dynamic coupling appears at runtime communication. Even async protocols don't decouple statically when contracts are shared.
- **Static coupling tooling.** Software bills of materials, deployment scripts, and dependency-management tools surface shared artifacts; minimize coupling between services.
- **Dynamic coupling via logs.** Services log every interservice call (target service, protocol, etc.); fitness functions analyze the logs. A custom library can enforce consistent logging across services.
- **Dynamic coupling via registry.** Services register their interservice contracts (e.g., JSON) in a configuration server like Apache ZooKeeper on first start; the architect queries it for an ecosystem-wide call map.

## 14. Architecture Characteristic Ratings

- **Domain-partitioned with the most distinct quanta of any modern style.** Bounded contexts produce the cleanest physical embodiment of an architectural quantum; in many ways microservices exemplifies what the quantum measure evaluates.
- **High support for modern engineering practices.** Notably high ratings for automated deployment and testability; the style couldn't exist without the DevOps revolution.
- **High fault tolerance.** Independent, single-purpose, fine-grained services lead to high fault tolerance.
- **Scalability, elasticity, evolvability.** Some of the most scalable systems ever built use microservices. Heavy reliance on automation supports elasticity; high decoupling at an incremental level supports evolutionary change.
- **Performance is the weak point.** Distributed network calls, per-endpoint security checks, and *data latency* (multi-service requests imply multiple database calls) all add up. Mitigated through caching and replication, and partly why choreography is preferred over orchestration (less coupling, fewer bottlenecks).

## 15. Example — Patient Monitoring

A patient medical-monitoring system where each vital sign (heart rate, blood pressure, oxygen, sleep monitor) is a separate service with its own data store.

Shared services for cross-cutting needs:

- `Alert Staff` — notifies a nurse or doctor on abnormal readings.
- `Display Vital Signs` — pushes readings to the patient-room monitor.

The superpowers in action:

- **Fault tolerance** — a crashed blood-pressure service doesn't take down the others.
- **Testability** — maintenance on one vital sign is fully testable in isolation.
- **Evolvability** — a new vital-sign monitor can be added without affecting the rest.

**Recommended further reading:**

- *Building Microservices*, 2nd ed. (Sam Newman, O'Reilly 2021).
- *Building Micro-Frontends*, 2nd ed. (Luca Mezzalira, O'Reilly 2025).
- *Microservices vs. Service-Oriented Architecture* and *Microservices AntiPatterns and Pitfalls* (both Mark Richards, O'Reilly 2016).

## Granularity and Data Ownership

Microservices is where the granularity equilibrium and the data-ownership decision are most acute — they are the topics *The Hard Parts* exists to handle. Two pages cover them:

- [Service Granularity](decomposition/service-granularity.md) — the six disintegrators, four integrators, the Grains of Sand antipattern, the architect as facilitator.
- [Data Ownership](distributed/data-ownership.md) — single / common / joint ownership and the four joint-ownership resolution techniques.

## Sources

- [Fundamentals Ch 18: Microservices Architecture](software/software-architecture/books/fundamentals-of-software-architecture/ch18_microservices_architecture.md) (primary — origins, topology, bounded context, granularity guidelines, API layer, sidecar/mesh, communication, choreography vs. orchestration, sagas, data-per-service, serverless-as-deployment-model, governance, characteristic ratings, patient-monitoring example)


<!-- prev-next-nav -->

---

← [Orchestration-Driven SOA](software/software-architecture/styles/orchestration-driven-soa.md) | [When to Decompose](software/software-architecture/decomposition/when-to-decompose.md) →
