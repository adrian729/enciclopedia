# Ch 18: Microservices Architecture

## Table of Contents

- [1. Origins and Driving Philosophy](#1-origins-and-driving-philosophy)
- [2. Topology](#2-topology)
- [3. Bounded Context and Data Isolation](#3-bounded-context-and-data-isolation)
- [4. Service Granularity](#4-service-granularity)
- [5. API Layer and Frontends](#5-api-layer-and-frontends)
- [6. Operational Reuse: Sidecar and Service Mesh](#6-operational-reuse-sidecar-and-service-mesh)
- [7. Communication](#7-communication)
- [8. Choreography and Orchestration](#8-choreography-and-orchestration)
- [9. Transactions and Sagas](#9-transactions-and-sagas)
- [10. Data Topologies](#10-data-topologies)
- [11. Cloud Considerations](#11-cloud-considerations)
- [12. Common Risks](#12-common-risks)
- [13. Governance](#13-governance)
- [14. Team Topology Considerations](#14-team-topology-considerations)
- [15. Style Characteristics](#15-style-characteristics)
- [16. Examples and Use Cases](#16-examples-and-use-cases)

## 1. Origins and Driving Philosophy

- **Named, not discovered** — unlike most styles, microservices was named early: Martin Fowler and James Lewis's 2014 blog post crystallized its characteristics and shaped the definition for curious architects.
- **Inspired by DDD's bounded context** — the *bounded context* concept makes microservices a *share-nothing* architecture: code, schemas, and data inside a context can be coupled internally, but never coupled to anything outside.
- **Duplication over reuse** — reuse is implemented via coupling, so a highly decoupled architecture must favor duplication. Microservices physically models the logical bounded context as service plus its corresponding data.

## 2. Topology

- **Single-purpose, very small services** — each service is much smaller than in orchestration-driven SOA, EDA, or service-based architecture, and includes everything (databases, dependent components) needed to run independently.
- **Distributed by definition** — each service runs in its own process inside a VM or container; this extreme decoupling solves resource contention and isolation problems caused by multitenant application servers.
- **Enabled by cheap infrastructure** — open source operating systems plus automated provisioning, cloud, and containers made per-domain infrastructure practical, unlocking decoupling at both the domain and operational level.
- **Performance is the price** — network calls plus per-endpoint security verifications are far slower than in-process calls, forcing architects to think hard about granularity. Transactions across service boundaries are strongly discouraged.

## 3. Bounded Context and Data Isolation

- **Bounded context = service + everything it needs** — components, classes, schemas, and the database itself. Each service models a particular function, subdomain, or workflow.
- **Duplicate, don't share** — common classes like `Address` are duplicated across services rather than shared, to keep all code inside the bounded context.
- **Data isolation is mandatory** — microservices avoids *all* coupling, including shared schemas. Each domain decides whether to be a single source of truth that others query, or to distribute information through replication or caching.
- **Beware the Entity Trap** — don't model services as single database entities (see Ch. 8). Architects must abandon the relational habit of unifying all values around one source of truth.
- **Database freedom as upside** — once freed from a unified database, each team can pick the storage technology that best fits its service's budget, structure, and operational profile; teams can also switch databases later without affecting other services.

## 4. Service Granularity

- **The defining problem** — taking *micro* literally yields services so fine-grained that wiring them back together produces a *Big Ball of Distributed Mud*. As Martin Fowler said: *the term microservice is a label, not a description.*
- **Three boundary guidelines** — *purpose* (one cohesive behavior in the problem domain), *transactions* (entities that must transact together suggest a service boundary), *choreography* (if services chat too much, fold them back into a coarser service).
- **Iteration is the only path** — perfect granularity, data dependencies, and communication styles are never found on the first pass; refine as the domain is better understood.

## 5. API Layer and Frontends

- **API gateway** — sits between consumers (UIs, other systems) and services; can be a simple reverse proxy or a richer gateway carrying cross-cutting concerns like security, naming, and service discovery.
- **No business logic at the gateway** — the API layer must not act as a mediator or orchestrator; all business logic belongs inside a bounded context. Mediators belong in technically partitioned styles, not domain-partitioned microservices.
- **Monolithic frontend** — a single rich-desktop, mobile, or web UI (often a JavaScript SPA) calls services through the API layer.
- **Micro-frontends** — UI components map one-to-one onto backend services, extending bounded-context isolation up to the user interface; see Luca Mezzalira's *Building Micro-Frontends*, 2nd ed. (O'Reilly, 2025).

## 6. Operational Reuse: Sidecar and Service Mesh

- **Operational reuse vs. domain reuse** — microservices splits the two: domain logic stays duplicated and isolated, but operational concerns (monitoring, logging, circuit breakers) genuinely benefit from coupling.
- **Sidecar pattern** — each service ships with a *Sidecar* component that handles the shared operational concerns; a shared infrastructure team can upgrade the sidecar and every service inherits the new capability.
- **Service mesh** — connecting all sidecars through a *service plane* (e.g., Istio) creates a single console where teams globally control monitoring levels, logging, and other cross-cutting operational concerns across the architecture.
- **Service discovery** — a tool that automatically detects, locates, and elastically scales services; often hosted in the API layer or built into the mesh so callers have one consistent place to find services.

## 7. Communication

- **Synchronous vs. asynchronous** — the foundational choice. Sync waits for a response; async (events and messages, EDA-style) decouples in time.
- **Protocol-aware heterogeneous interoperability** — the typical sync model. *Protocol-aware*: services standardize on how they call each other (a REST profile, a queue, etc.). *Heterogeneous*: polyglot stacks are first-class. *Interoperability*: services collaborate over the network without distributed transactions.
- **Enforced heterogeneity (sidebar)** — a microservices pioneer mandated that *each* team use a different stack (Java vs. .NET) so accidental class sharing was physically impossible — the polar opposite of typical enterprise standardization.

## 8. Choreography and Orchestration

- **Choreography** — no central coordinator: each service calls others as needed (e.g., `CustomerWishList` directly calls `CustomerDemographics`). Respects the bounded-context philosophy and yields the most decoupling.
- **Orchestration** — for cross-service coordination, build a *localized* mediator (an *orchestration service*, e.g., `ReportCustomerInformation`); microservices has no global mediator.
- **Front Controller pattern** — when a nominally choreographed service ends up coordinating many others, it becomes a de facto mediator with extra responsibilities and added complexity.
- **Trade-off** — choreography preserves decoupling but complicates error handling and coordination; orchestration centralizes coupling in one service so the others stay clean. The First Law applies — neither is universally right.

## 9. Transactions and Sagas

- **Avoid cross-service transactions** — they violate the core decoupling principle and create *Connascence of Values* (the worst dynamic connascence). The best advice: *don't do them — fix the granularity instead.* Needing transactions to wire services together is a sign the design is too granular.
- **Saga pattern** — when transactional coordination is unavoidable, a mediator drives each participating service, records success or failure, and coordinates the result; the name comes from the literary *saga* of a long sequence of events leading to a heroic conclusion.
- **Compensating transaction framework** — on partial failure, the mediator instructs successful participants to undo their work; participants typically hold a `pending` state until the mediator confirms overall success. This generates significant network coordination traffic.
- **Eight Saga variants** — the authors enumerate eight transactional Saga patterns in Chapter 12 of *Software Architecture: The Hard Parts* (O'Reilly, 2021). If transactions become the dominant feature, microservices is likely the wrong style.

## 10. Data Topologies

- **The only style that *requires* breaking up data** — monolithic and even domain-based databases aren't viable at microservices scale.
- **Why not monolithic** — 60 services sharing one DB makes a column rename a coordinated 60-service release; the bounded context collapses; the database can't elastically scale with the services; connection pools exhaust; one DB outage kills the entire ecosystem.
- **Database-per-Service pattern** — the standard topology: each service owns its data in a separate database or schema. Other services must request data through a contract, decoupling them from the internal structure and freeing each team to switch DB type without rippling change.
- **Limited sharing exception** — when two or more services genuinely write the same table (e.g., split payment-type services), a few services may share one DB inside a *broader bounded context*. Cap it at five or six; beyond that, the same change-control, scalability, and fault-tolerance pains return.

## 11. Cloud Considerations

- **"Cloud-native" architecture** — on-demand provisioning of VMs, containers, and databases plus the cloud's services-based model are an exceptional fit; works on-prem too with Kubernetes or Cloud Foundry.
- **Serverless is a deployment model, not a style** — AWS Lambda, Google Cloud Functions, and Azure Functions describe single-purpose units that match the microservices definition; the authors classify serverless as a *deployment model* of microservices.
- **Containers are equally valid** — most cloud vendors run Kubernetes, so containerized microservices deploy as easily as serverless ones; the choice is operational, not architectural.

## 12. Common Risks

- **Grains of Sand antipattern** — coined by Mark Richards in 2016 for services made too fine-grained, like grains of sand on a beach; *micro* refers to *what* the service does, not how big it is.
- **Excessive interservice communication** — fine granularity plus tight bounded contexts forces chatter; fix by combining services into coarser ones rather than tolerating dynamic coupling.
- **Over-sharing data** — undermines the architecture's superpowers (change control, scalability, fault tolerance, agility); consolidate services rather than share data freely.
- **Code reuse via shared libraries** — sharing JAR/DLL functionality breaks the *share-nothing* principle: a change to shared code can break services across multiple bounded contexts. Versioning helps but adds significant complication.

## 13. Governance

- **Govern static and dynamic coupling** — static coupling appears in shared libraries and contracts; dynamic coupling appears at runtime communication. Even async protocols don't decouple statically when contracts are shared.
- **Static coupling tooling** — software bills of materials, deployment scripts, and dependency-management tools surface shared artifacts; minimize coupling between services.
- **Dynamic coupling via logs** — services log every interservice call (target service, protocol, etc.); fitness functions analyze the logs. A custom library can enforce consistent logging across services.
- **Dynamic coupling via registry** — services register their interservice contracts (e.g., JSON) in a configuration server like Apache ZooKeeper on first start; the architect queries it for an ecosystem-wide call map.

## 14. Team Topology Considerations

- **Best fit: domain-aligned, cross-functional teams** — domain partitioning lets a team deliver a domain feature end-to-end without interfering with others; technically partitioned teams (UI, backend, DB) require painful cross-team coordination for every domain change.
- **Stream-aligned teams** — work well when the stream maps to a subdomain; if streams cross many bounded contexts, realign granularity or pick a different style.
- **Enabling teams** — leverage microservices' modularity to provide specialized or cross-cutting services without blocking stream-aligned teams; often partner with platform teams on sidecars.
- **Complicated-subsystem teams** — exploit service-level modularity to focus on hard domain or subdomain processing in isolation.
- **Platform teams** — typically build and maintain the cross-cutting operational sidecars and the service mesh, freeing stream-aligned teams from those concerns.

## 15. Style Characteristics

- **Domain-partitioned with the most distinct quanta of any modern style** — bounded contexts produce the cleanest physical embodiment of an architectural quantum; in many ways microservices exemplifies what the quantum measure evaluates.
- **High support for modern engineering practices** — notably high ratings for automated deployment and testability; the style couldn't exist without the DevOps revolution and its march toward automating operational concerns.
- **High fault tolerance** — independent, single-purpose, fine-grained services lead to high fault tolerance.
- **Scalability, elasticity, evolvability** — other high points; some of the most scalable systems ever built use microservices. Heavy reliance on automation supports elasticity; high decoupling at an incremental level supports evolutionary change.
- **Performance is the weak point** — distributed network calls, per-endpoint security checks, and *data latency* (multi-service requests imply multiple database calls) all add up. Mitigated through caching and replication, and partly why choreography is preferred over orchestration (less coupling, fewer bottlenecks).

## 16. Examples and Use Cases

- **Best fit** — systems with high functional and data modularity. Example: a *patient medical-monitoring system* where each vital sign (heart rate, blood pressure, oxygen, sleep monitor) is a separate service with its own data store.
- **Shared services for cross-cutting needs** — `Alert Staff` (notifies a nurse or doctor on abnormal readings) and `Display Vital Signs` (pushes readings to the patient-room monitor) are shared across all vital-sign services.
- **Superpowers in action** — *fault tolerance*: a crashed blood-pressure service doesn't take down the others; *testability*: maintenance on one vital sign is fully testable in isolation; *evolvability*: a new vital-sign monitor can be added without affecting the rest.
- **Recommended further reading** — *Building Microservices*, 2nd ed. (Sam Newman, O'Reilly 2021); *Building Micro-Frontends*, 2nd ed. (Luca Mezzalira, O'Reilly 2025); *Microservices vs. Service-Oriented Architecture* and *Microservices AntiPatterns and Pitfalls* (both Mark Richards, O'Reilly 2016).
