# Ch 9: Foundations

## Table of Contents

- [1. Styles Versus Patterns](#1-styles-versus-patterns)
- [2. Fundamental Patterns](#2-fundamental-patterns)
- [3. Architecture Partitioning](#3-architecture-partitioning)
- [4. Monolithic Versus Distributed Architectures](#4-monolithic-versus-distributed-architectures)
- [5. The Fallacies of Distributed Computing](#5-the-fallacies-of-distributed-computing)
- [6. Team Topologies and Architecture](#6-team-topologies-and-architecture)

## 1. Styles Versus Patterns

- **Styles vs. patterns** — a *pattern* captures a contextualized solution; an *architectural style* describes the architecture's topology and its assumed/default characteristics (both beneficial and detrimental). Naming a style provides a concise way to refer to a complex set of factors.
- **An architectural style describes five aspects:**
  - **Component topology** — how components and their dependencies are organized (e.g., layered groups by technical capability; modular monolith groups by domain).
  - **Physical architecture** — the style usually dictates *monolithic* (single deployment unit) or *distributed* (multiple deployment units). A modular monolith is monolithic with a single database; event-driven architecture is always distributed.
  - **Deployment** — granularity and cadence. Monoliths deploy as a single unit alongside one relational database; agile distributed styles like microservices deploy in pieces with automated provisioning and faster cadence.
  - **Communication style** — monoliths can use in-process method calls; distributed architectures communicate via network protocols like REST or message queues.
  - **Data topology** — monoliths tend toward a monolithic database; distributed architectures sometimes separate data based on the style's philosophy.
- **Where styles come from** — there is no architectural cabal in an ivory tower. New styles emerge from evolving ecosystems: someone combines new capabilities with old ones, others copy it, and the pattern gets a name. *Microservices* is a label (not a description) coined as a reaction to the era's large-service, heavily orchestrated styles, made possible by DevOps, open source OSes, and DDD.

## 2. Fundamental Patterns

- **Big Ball of Mud antipattern** — Brian Foote and Joseph Yoder's 1997 term for "a haphazardly structured, sprawling, sloppy, duct-tape-and-baling-wire, spaghetti-code jungle." Information is shared promiscuously between distant elements until nearly all important information becomes global or duplicated. Avoid at all costs: change becomes terrifying because side effects are unpredictable, and deployment, testability, scalability, and performance all suffer.
- **Unitary architecture** — software and hardware as a single entity (early mainframes, early PCs). Few exist today outside embedded systems and constrained environments.
- **Client/server (two-tier)** — separates technical functionality between frontend and backend. Variants:
  - **Desktop and database server** — rich Windows-style client + standalone database server over standard network protocols.
  - **Browser and web server** — thin browser client + web server (often + database server). Many architects still call this two-tier because web/database run together in the operations center.
  - **Single-page JavaScript applications** — rich client written in browser-side JavaScript, mirroring the original desktop variant.
  - **Three-tier** — popular late 1990s, with database, application server, and HTML/JavaScript frontend tiers. Coincided with CORBA and DCOM.
- **Three-tier and Java serialization** — when Java was designed in the 1990s, three-tier was assumed to be the future, so serialization was baked into every object's contract. The style faded; the leftover constraint endures, frustrating language designers and illustrating the long-term cost of architectural assumptions.

## 3. Architecture Partitioning

- **First Law of Software Architecture applies to partitioning** — components can be partitioned many ways, each with trade-offs. *Top-level partitioning* has an outsized impact because it defines the fundamental architecture style.
- **Two top-level partitioning styles:**
  - **Technical top-level partitioning** — components organized by technical capability (presentation, business rules, services, persistence). The layered monolith is the canonical example; matches the MVC design pattern, making it the default in many organizations.
  - **Domain partitioning** — components organized by domain or workflow (inspired by Eric Evans's *Domain-Driven Design*). The modular monolith and microservices both follow this philosophy.
- **The CatalogCheckout illustration** — in a technically partitioned architecture the `CatalogCheckout` workflow appears smeared across all layers; in a domain-partitioned architecture it is a single top-level component (which may itself contain layers internally).
- **Industry trend** — over recent years, a decided trend toward domain partitioning for both monolithic and distributed architectures. Neither approach is correct; refer to the First Law of Software Architecture.
- **Conway's Law** — Melvin Conway (late 1960s): "Organizations which design systems…are constrained to produce designs which are copies of the communication structures of these organizations." The *Inverse Conway Maneuver* (coined by Jonny Leroy of Thoughtworks) suggests evolving team and organization structures together to promote the desired architecture — now universally known as *team topologies*.

- **Kata: Silicon Sandwiches partitioning trade-offs:**

| Domain partitioning advantages | Domain partitioning disadvantage |
|---|---|
| Modeled on how the business functions, not implementation | Customization code appears in multiple places |
| Easier to build cross-functional teams around domains |  |
| Aligns with modular monolith and microservices |  |
| Message flow matches the problem domain |  |
| Easy to migrate data and components to a distributed architecture |  |

| Technical partitioning advantages | Technical partitioning disadvantages |
|---|---|
| Clearly separates customization code | Higher degree of global coupling — changes to `Common` or `Local` likely affect every component |
| Aligns with the layered architecture pattern | Developers may duplicate domain concepts across `Common` and `Local` layers |
|  | Higher coupling at the data level; one shared database makes later migration to a distributed system difficult |

## 4. Monolithic Versus Distributed Architectures

- **Two main classifications:** *monolithic* (single deployment unit of all code) and *distributed* (multiple deployment units connected through remote access protocols). Distributed architectures share a common set of challenges absent from monoliths, making this a useful separation.
- **Monolithic styles covered in Part II** — Layered (Ch. 10), Pipeline (Ch. 12), Microkernel (Ch. 13).
- **Distributed styles covered in Part II** — Service-based (Ch. 14), Event-driven (Ch. 15), Space-based (Ch. 16), Service-oriented (Ch. 17), Microservices (Ch. 18).

## 5. The Fallacies of Distributed Computing

The original eight fallacies were listed by L. Peter Deutsch and colleagues at Sun Microsystems in 1994. The authors add three more.

- **Fallacy #1: The network is reliable** — networks have improved but remain generally unreliable. Service B may be healthy yet unreachable, or process a request without a response coming back. Hence timeouts and circuit breakers between services.
- **Fallacy #2: Latency is zero** — local calls (`t_local`) are nanoseconds/microseconds; remote calls (`t_remote`) are milliseconds. Knowing the average latency is essential; knowing the *95th–99th percentile* is even more important — average might be 60 ms while the 95th is 400 ms, and that long tail kills performance. At 100 ms average latency per request, chaining service calls for one business function can add 1,000 ms.
- **Fallacy #3: Bandwidth is infinite** — once a system is broken into services, communication consumes significant bandwidth. **Stamp coupling** — when a service returns 500 KB to satisfy a 200-byte need, multiplied by 2,000 requests/second, costs 1 GBps; trimming to the needed 200 bytes costs only 400 Kbps. Mitigations: private RESTful endpoints, field selectors, GraphQL, value-driven/consumer-driven contracts, internal messaging endpoints — anything that transmits only necessary data.
- **Fallacy #4: The network is secure** — every endpoint must be secured against unknown or bad requests. The threat surface area increases by magnitudes when moving from monolithic to distributed, and securing every interservice call is one reason synchronous distributed styles (microservices, service-based) tend to be slower.
- **Fallacy #5: The topology never changes** — routers, hubs, switches, firewalls all change constantly. A "minor" 2 a.m. network upgrade can invalidate all latency assumptions and trigger timeouts and circuit breakers. Architects must stay in constant communication with operations and network admins.
- **Fallacy #6: There is only one administrator** — large companies have dozens of network administrators. Distributed architecture requires significant coordination across them; monoliths do not.
- **Fallacy #7: Transport cost is zero** — *monetary* cost, not latency. Distributed architectures cost significantly more due to additional hardware, servers, gateways, firewalls, subnets, and proxies. Analyze current capacity, bandwidth, latency, and security zones before embarking.
- **Fallacy #8: The network is homogeneous** — most companies use multiple network-hardware vendors that don't always interoperate cleanly, feeding back into reliability, latency, and bandwidth assumptions.
- **Fallacy #9: Versioning is easy** — versioning contracts seems simple but raises trade-offs: version per service or system-wide? How far does versioning reach? How many versions to maintain? Deprecate per service or system-wide?
- **Fallacy #10: Compensating updates always work** — *compensating updates* let an `Orchestrator` reverse a multi-service update on failure. But what if the compensating update itself fails? Designs must accommodate the recovery path when both the update and the compensation fail.
- **Fallacy #11: Observability is optional (for distributed architectures)** — *observability* is the ability to observe each service's interactions with others through monitors and logs. Useful in monoliths, *critical* in distributed architectures because they have many hard-to-debug communication failure modes.

## 6. Team Topologies and Architecture

From *Team Topologies* by Matthew Skelton and Manuel Pais (IT Revolution Press, 2019):

- **Stream-aligned teams** — focus narrowly on one stream of work (a product, service, or feature set) scoped to a business domain or capability. Goal: deliver discrete value as quickly as possible. Other team types exist to reduce friction for them.
- **Enabling teams** — bridge a capability gap, providing space for research, learning, and other important-but-not-urgent work. Highly collaborative and proactive; supply specialized knowledge to stream-aligned teams.
- **Complicated-subsystem teams** — own a complex subsystem or domain that requires specialized skills, helping stream-aligned teams apply it and reducing their cognitive load.
- **Platform teams** — provide internal services and building blocks (per Evan Botcher: "a foundation of self-service APIs, tools, services, knowledge and support arranged as a compelling internal product"). Support other teams while providing governance for quality and security.
