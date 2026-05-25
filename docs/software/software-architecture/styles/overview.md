# Styles — Overview and Choosing One

> *Fundamentals* devotes Part II to a nine-style catalog (Ch 9–18), a choosing-a-style chapter (Ch 19), and a closing chapter on architectural patterns (Ch 20). *The Hard Parts* skips the catalog entirely and assumes the reader already has it. This overview page is therefore single-source — *Fundamentals* — and the per-style pages that follow are also predominantly *Fundamentals*. The catalog itself is the contribution; the discipline of [Trade-Off Analysis](foundations/tradeoff-analysis.md) is how an architect actually picks among the styles.

## Table of Contents

- [1. What an Architectural Style Is](#1-what-an-architectural-style-is)
- [2. Styles vs. Patterns](#2-styles-vs-patterns)
- [3. Technical vs. Domain Partitioning](#3-technical-vs-domain-partitioning)
- [4. Conway's Law and Team Topologies](#4-conways-law-and-team-topologies)
- [5. The Fallacies of Distributed Computing](#5-the-fallacies-of-distributed-computing)
- [6. The Big Ball of Mud](#6-the-big-ball-of-mud)
- [7. Choosing a Style — Three Core Determinations](#7-choosing-a-style--three-core-determinations)
- [8. Domain/Architecture Isomorphism](#8-domainarchitecture-isomorphism)
- [9. Kata Cases — Silicon Sandwiches and Going, Going, Gone](#9-kata-cases--silicon-sandwiches-and-going-going-gone)
- [10. Architectural Patterns vs. Styles](#10-architectural-patterns-vs-styles)
- [11. Section Map](#11-section-map)
- [Sources](#sources)

## 1. What an Architectural Style Is

A style is a *named topology* with assumed (and named) characteristics — both beneficial and detrimental. Naming a style gives architects a concise shorthand for a complex set of factors. Every style describes the same five aspects:

| Aspect | What it captures |
|---|---|
| **Component topology** | How components and their dependencies are organized — by technical capability (layered) or by domain (modular monolith, microservices). |
| **Physical architecture** | *Monolithic* (single deployment unit) or *distributed* (multiple deployment units). A modular monolith is monolithic with one database; event-driven is always distributed. |
| **Deployment** | Granularity and cadence. Monoliths deploy as a single unit, infrequently. Agile distributed styles like microservices deploy in pieces, automated, frequently. |
| **Communication style** | Monoliths use in-process method calls. Distributed styles use network protocols (REST, gRPC, messaging). |
| **Data topology** | Monoliths tend toward a single monolithic database. Distributed styles sometimes split data per service. |

Styles don't come from an ivory-tower cabal. New styles emerge as the ecosystem evolves: someone combines new capabilities with old ones, others copy it, and the shape gets a name. *Microservices* is a label, not a description — it was coined as a reaction to the heavily orchestrated styles of the era, made possible by DevOps, open source operating systems, and DDD.

## 2. Styles vs. Patterns

> A **style** is a topology. A **pattern** is a contextualized solution to a recurring problem inside or across styles.

*Fundamentals* Ch 20 is emphatic that patterns are *not* solutions and not "best practices." Frameworks, tools, and libraries *implement* patterns with varying fidelity. Identify the pattern first; only then choose an implementation.

A consequence: **any distributed style can use any of these patterns.** Orchestration, choreography, CQRS, sidecar/service mesh, single-broker, domain-broker, and hexagonal layering all live above the catalog. The eight Saga variants from *The Hard Parts* sit in the same plane — see [Transactional Sagas](distributed/transactional-sagas.md).

The pattern catalog is summarized in [§ 10](#10-architectural-patterns-vs-styles) below.

## 3. Technical vs. Domain Partitioning

Top-level partitioning has outsized impact because it sets the style. There are exactly two top-level choices:

| Partitioning | Components organized by | Canonical style |
|---|---|---|
| **Technical** | Technical capability — presentation, business rules, services, persistence | Layered monolith (matches MVC; the default in many organizations) |
| **Domain** | Domain or workflow — `CatalogCheckout`, `OrderFulfillment`, `Payment` (Eric Evans, *Domain-Driven Design*) | Modular monolith, service-based, microservices |

The classic illustration: in a technical partition, a single domain (e.g., `CatalogCheckout`) smears across Presentation, Business, Rules, Services, and Database; in a domain partition, the same workflow is one top-level component that *may itself* contain technical layers internally.

The industry trend over the last decade is decided: **domain partitioning** for both monolithic and distributed architectures. Neither approach is universally correct (First Law), but domain partitioning aligns better with cross-functional teams and with later migration to distributed styles.

## 4. Conway's Law and Team Topologies

> *Organizations which design systems…are constrained to produce designs which are copies of the communication structures of these organizations.* — Melvin Conway, late 1960s.

The **Inverse Conway Maneuver** (Jonny Leroy, Thoughtworks) advises evolving the organization's structure deliberately to *promote* the desired architecture, rather than passively inheriting whatever shape the org chart produces. This idea has matured into Skelton and Pais's **Team Topologies** vocabulary, which assigns four canonical roles:

| Team type | Role |
|---|---|
| **Stream-aligned** | Owns a discrete stream of work scoped to a business domain or capability. Delivers value end-to-end. All other team types exist to reduce friction for stream-aligned teams. |
| **Enabling** | Bridges a capability gap. Provides time for research and learning. Supplies specialized knowledge to stream-aligned teams. |
| **Complicated-subsystem** | Owns a complex subsystem requiring specialized skills, reducing cognitive load on stream-aligned teams. |
| **Platform** | Provides a *foundation of self-service APIs, tools, services, knowledge and support* arranged as an internal product. Also handles governance for quality and security. |

The style pages each include a team-topology section noting which team configurations the style supports well or poorly. Notable mismatches: technically partitioned teams (UI / backend / DB silos) struggle with domain-partitioned styles, because every domain change requires cross-team coordination.

## 5. The Fallacies of Distributed Computing

L. Peter Deutsch and colleagues at Sun listed the original eight in 1994; *Fundamentals* adds three more. The fallacies are *false beliefs* — every one of them must be designed *against*, not assumed *true*.

| # | Fallacy | What goes wrong |
|---|---|---|
| 1 | **The network is reliable** | Services can be healthy yet unreachable; responses can vanish. Use timeouts and circuit breakers. |
| 2 | **Latency is zero** | Local calls are nanoseconds; remote calls are milliseconds. Track *95th and 99th percentile*, not average — at 100 ms average, five chained services adds 500 ms baseline; the long tail is worse. |
| 3 | **Bandwidth is infinite** | **Stamp coupling** — returning 500 KB to satisfy a 200-byte need × 2,000 req/s = 1 GBps. Mitigate with private endpoints, field selectors, GraphQL, consumer-driven contracts. |
| 4 | **The network is secure** | Threat surface grows by orders of magnitude moving from monolith to distributed. Every endpoint must authenticate; this is one reason synchronous distributed styles are slow. |
| 5 | **The topology never changes** | Routers, hubs, firewalls change constantly. A 2 a.m. "minor" network change can invalidate every latency assumption. Stay in touch with network/ops. |
| 6 | **There is only one administrator** | Large organizations have dozens. Distributed architecture requires significant cross-administrator coordination. |
| 7 | **Transport cost is zero** | *Monetary*, not latency. Servers, gateways, firewalls, subnets, proxies. Calculate the bill before choosing distributed. |
| 8 | **The network is homogeneous** | Multiple vendors that don't always interoperate cleanly — feeds back into 1, 2, 3. |
| 9 | **Versioning is easy** | Per-service or system-wide? How far does versioning reach? How many versions live concurrently? |
| 10 | **Compensating updates always work** | An orchestrator can reverse a multi-service update — but what if the compensation itself fails? Designs must accommodate compensation-of-compensation. See [Transactional Sagas](distributed/transactional-sagas.md). |
| 11 | **Observability is optional** | Critical, not optional, for distributed architectures, because failure modes are many and hard to debug. |

## 6. The Big Ball of Mud

> *A haphazardly structured, sprawling, sloppy, duct-tape-and-baling-wire, spaghetti-code jungle.* — Brian Foote and Joseph Yoder, 1997.

The anti-style. Information is shared promiscuously between distant elements until nearly all important information becomes global or duplicated. Change becomes terrifying because side effects are unpredictable; deployment, testability, scalability, and performance all suffer simultaneously. The Big Ball of Mud is the destination of *Architecture by Implication* and *Accidental Architecture* — what teams produce when they "just start coding" without choosing a style.

Its distributed cousin is the **Big Ball of Distributed Mud** — a microservices architecture where the granularity is wrong and services are coupled at runtime. See [Service Granularity](decomposition/service-granularity.md) for the granularity equilibrium that prevents it.

## 7. Choosing a Style — Three Core Determinations

After the domain, the characteristics analysis (see [Architecture Characteristics](foundations/architecture-characteristics.md)), the data architecture review, and the organizational/cloud constraints, the architect must answer three questions:

| Determination | Tool |
|---|---|
| **Monolith vs. distributed?** | One set of architecture characteristics enough, or do different parts need different sets? **Architecture quantum** is the measure — see [Components and Quantum](foundations/components-and-quantum.md). |
| **Where does data live?** | Monoliths assume one relational DB. Distributed forces the *single ownership / common / joint* decision — see [Data Ownership](distributed/data-ownership.md). |
| **Sync or async communication?** | Sync is more convenient but trades off scalability/reliability. Async buys performance and scale at the price of synchronization, deadlocks, races, and harder debugging. **Default to sync; use async only when necessary.** |

The output of the design process is an architecture topology (chosen style plus any hybridizations), Architectural Decision Records (ADRs) for the highest-effort parts, and architecture fitness functions to protect the principles and characteristics that justify the choice.

## 8. Domain/Architecture Isomorphism

*Isomorphism* (Greek *isos* "equal" + *morph* "shape") names the generic shape of an architecture and how its components depend on each other. A style fits a domain when their isomorphisms match.

- **Microkernel** suits a domain dominated by *customizability* — many variants of the same flow (per-state insurance rules, per-form tax preparation, per-customer product packages).
- **Space-based** suits a domain dominated by *concurrent processing of many discrete operations* — genome analysis, online auctions, ticket sales.
- **Service-based** suits a *highly coupled domain* where each step depends on the previous (a multipage insurance form, a guided checkout) — intentionally coupled coarse-grained services fit better than decoupled microservices.
- **Microservices** suits a domain that decomposes cleanly into independent bounded contexts (patient monitoring with independent vitals).

A mismatch produces architectural friction: a highly scalable system buried in a coupled monolith, or a heavily-coupled domain shoehorned into share-nothing microservices.

## 9. Kata Cases — Silicon Sandwiches and Going, Going, Gone

*Fundamentals* uses two case studies as worked examples of the style-choice process.

### 9.1. Silicon Sandwiches — Monolith Path

A simple application, modest budget, single quantum sufficient. The characteristics analysis pointed to a monolith. Two component designs:

| Option | Customization mechanism | Data | API | Best fit |
|---|---|---|---|---|
| **Modular Monolith** | Single `Override` endpoint referenced by every domain component | Single relational DB; tables aligned to domains for future split | Single web UI | Simple app, single quantum, low budget |
| **Microkernel** | Plug-ins (common set + local set, each with its own data) | Core relational DB + per-plug-in stores | API layer with Backends-for-Frontends (BFF) adapters per frontend | Customizability is a primary architecture characteristic |

Either is defensible. The modular monolith with `Override` was the recommended baseline; the microkernel variant becomes the right answer if per-customer customization is a *primary* characteristic.

### 9.2. Going, Going, Gone — Distributed Path

A live online-auction system. Different parts need different characteristics (auctioneer availability vs. bidder elasticity), so the analysis ruled out a monolith. Microservices wins over event-driven because microservices supports *varying operational characteristics across components* directly; event-driven typically separates by orchestrated/choreographed communication, not by characteristics.

Five resulting quanta: `Payment`, `Auctioneer`, `Bidder`, `Bidder Streams`, `Bid Tracker`. Mixed sync/async: async chosen primarily to absorb variation in operational characteristics (e.g., `Payment` processes one new payment per 500 ms — a queue absorbs the spike when many auctions end at once). Not the only valid design — the design with the *least worst* trade-offs.

## 10. Architectural Patterns vs. Styles

*Fundamentals* Ch 20 catalogs a small set of patterns that compose with the styles.

### 10.1. Reuse — Separating Domain and Operational Coupling

> **Microservices guidance.** *Duplication is preferable to coupling.*

Operational capabilities (monitoring, logging, auth, circuit breakers) *do* benefit from coupling — letting every team build its own descends into chaos. Two pattern families implement the same idea of *operational reuse without domain coupling*:

| Pattern | Notes |
|---|---|
| **Hexagonal Architecture (Ports and Adapters)** | Alistair Cockburn. Domain logic in the center, adapters at the edges. Useful as shorthand for "separation of domain and operational concerns" but be cautious applying literally with microservices — treating the database as just-another-adapter conflicts with the schema-belongs-to-business-logic stance of DDD. |
| **Sidecar / Service Mesh** | Each service ships a sidecar that handles cross-cutting operational concerns; sidecars are wired together by a control plane (e.g., Istio) for global configuration. The canonical implementation of **orthogonal coupling**: two parts with distinct purposes that must intersect to form a complete solution. |

### 10.2. Communication — Orchestration vs. Choreography

*Orchestration* and *mediation* are the same pattern. The trade-offs are symmetric — see the [Workflows & Orchestration](distributed/workflows-orchestration.md) page for the full discussion.

### 10.3. CQRS

Command-Query Responsibility Segregation splits writes and reads into separate datastores synchronized (usually asynchronously) from write to read. Pays off when read and write volumes diverge sharply, when reads must be isolated for security, or when read and write sides need different architecture characteristics. A *data communication pattern*, not a style.

### 10.4. Broker Patterns

In event-driven architectures, brokers are infrastructure-level participants.

| Pattern | Use when |
|---|---|
| **Single-broker** | One broker for the whole workflow. Centralized discovery, least infrastructure; fragile under high volume and a single point of failure. |
| **Domain-broker** | One broker per domain group, mirroring the architecture's domain partitioning. Better isolation, fault tolerance, and scalability; more discovery overhead and more infrastructure. |

Neither is a best practice. Architects balance discovery against domain isolation in their specific system.

## 11. Section Map

Monolithic styles (closed, single deployment, single quantum):

| Style | One-line summary |
|---|---|
| [Layered](styles/layered.md) | n-tiered, technically partitioned. Cheapest, simplest, default fallback. Beware the *Architecture Sinkhole*. |
| [Modular Monolith](styles/modular-monolith.md) | Domain-partitioned monolith. DDD-aligned. Cost + simplicity of a monolith with cleaner module boundaries. |
| [Pipeline](styles/pipeline.md) | Pipes-and-filters. Producer / Transformer / Tester / Consumer. Best for distinct, ordered, deterministic processing. |
| [Microkernel](styles/microkernel.md) | Core + plug-ins. The only style that can be *both* domain- and technically-partitioned. Best for customization-heavy domains. |

Distributed styles (multiple deployment units, distributed-computing fallacies apply):

| Style | One-line summary |
|---|---|
| [Service-Based](styles/service-based.md) | Coarse-grained domain services (≤12) + shared monolithic DB. The most pragmatic distributed style; keeps ACID. |
| [Event-Driven](styles/event-driven.md) | Asynchronous, broker- or mediator-topology. Five-star responsiveness/evolutionary/fault tolerance; low simplicity/testability. |
| [Space-Based](styles/space-based.md) | In-memory data grid replaces the DB as bottleneck. Five-star scalability/elasticity/performance for unpredictable spikes. |
| [Orchestration-Driven SOA](styles/orchestration-driven-soa.md) | The historical cautionary tale — strict taxonomy, ESB orchestration, reuse-via-coupling. Modern integration use remains valid. |
| [Microservices](styles/microservices.md) | Share-nothing bounded contexts. Highest testability/deployability/fault tolerance. Pays for it in perf and DevOps maturity. |

## Sources

- [Fundamentals Ch 9: Styles Foundations](software/software-architecture/books/fundamentals-of-software-architecture/ch09_styles_foundations.md) (primary — styles vs. patterns, the five aspects, partitioning, fallacies, team topologies)
- [Fundamentals Ch 19: Choosing the Appropriate Architecture Style](software/software-architecture/books/fundamentals-of-software-architecture/ch19_choosing_architecture_style.md) (the three core determinations, domain/architecture isomorphism, the two kata cases)
- [Fundamentals Ch 20: Architectural Patterns](software/software-architecture/books/fundamentals-of-software-architecture/ch20_architectural_patterns.md) (Hexagonal, Sidecar/Service Mesh, CQRS, Single-Broker, Domain-Broker, orthogonal coupling)


<!-- prev-next-nav -->

---

← [Trade-Off Analysis](software/software-architecture/foundations/tradeoff-analysis.md) | [Layered](software/software-architecture/styles/layered.md) →
