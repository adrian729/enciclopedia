# Components and Quantum

> *Fundamentals* (Ch 8) defines the **logical component** and shows how to identify it iteratively — the Workflow and Actor/Action approaches, plus the **Entity Trap** antipattern. *The Hard Parts* (Ch 2) sharpens the unit one level up: the **architecture quantum**, the independently deployable artifact with high functional cohesion and high static coupling. *The Hard Parts* (Ch 8) then folds in the natural follow-up — what to do when a component recurs across services — with its four **reuse patterns** (Code Replication, Shared Library, Shared Service, Sidecar/Mesh) and the **Centralized Customer Service** anti-pattern that motivates them. The two books are complementary here; *Fundamentals* defines the building block, *The Hard Parts* defines the integration unit.

## Table of Contents

- [1. Logical Components](#1-logical-components)
- [2. Identifying Components — The Workflow](#2-identifying-components--the-workflow)
- [3. The Entity Trap](#3-the-entity-trap)
- [4. The Architecture Quantum](#4-the-architecture-quantum)
- [5. The Four Coupling Flavors](#5-the-four-coupling-flavors)
- [6. Reuse and the Four Patterns](#6-reuse-and-the-four-patterns)
- [7. Why Reuse Needs Slow Change](#7-why-reuse-needs-slow-change)
- [Sources](#sources)

## 1. Logical Components

The **logical component** is the architectural facet of modularity — *Fundamentals*' name for the building block of a system. Where Chapter 3 used *module* as the generic term for "a bundle of related code," Chapter 8 narrows to the unit at which the architect actually thinks.

> **House analogy** — rooms (kitchen, bedrooms, bathrooms, office) are the components of a house; major business functions (manage inventory, ship orders, process payments) are the components of a system. Each contains the code that implements its function.

Components manifest as **namespaces or directory structures**. Leaf nodes typically represent components; higher-level nodes represent domains and subdomains. `order_entry/ordering/payment` ⇒ `Payment Processing`; `order_entry/processing/fulfillment` ⇒ `Order Fulfillment`. **Logical architecture is what you read by analyzing directories and namespaces** — independently of whether those directories ship as one deployable or many.

| | Logical architecture | Physical architecture |
|---|---|---|
| **Shows** | Logical components, their interactions, actors, optional repositories | Services, UIs, databases, deployment artifacts |
| **Independent of style** | Yes | No — reflects a specific style |
| **Question answered** | What does the system do? How is functionality demarcated? | How is it deployed? Where does code run? |

**Don't skip the logical step.** Many architects start straight from the physical view; the trouble is that a physical diagram doesn't show *where* functionality lives (payment processing might be split across several services). Skipping logical architecture leaves teams without guidance on monolith-vs-distributed decisions and produces unstructured systems that are hard to maintain, test, and deploy.

## 2. Identifying Components — The Workflow

Component identification is iterative: produce candidates, then refine via feedback.

1. **Identify initial core components** — best guess based on major workflows or actions. They start as empty buckets, named for their proposed role, with no responsibility until user stories are assigned.
2. **Assign user stories or requirements** — fill the buckets with concrete responsibilities.
3. **Analyze roles and responsibilities** — check cohesion; split components that drift toward kitchen-sinks.
4. **Analyze architectural characteristics** — characteristics may force a component to be split or combined.
5. **Restructure** — apply the analysis and loop back.

The same workflow applies to greenfield work and to feature changes in maintenance systems (e.g., adding store pickup to an order-entry system). Don't try to be perfect first time; iterating beats over-engineering at the moment of least information.

### 2.1. Two Approaches to the Initial Decomposition

**Workflow approach** — derive components from major happy-path workflows. For an order-entry system:

| Step | Component |
|---|---|
| User browses catalog | `Item Browser` |
| User places an order | `Order Placement` |
| User pays | `Order Payment` |
| Email order details | `Customer Notification` |
| Prepare the order | `Order Fulfillment` |
| Ship the order | `Order Shipment` |
| Email shipment | `Customer Notification` (reused) |
| Track shipment | `Order Tracking` |

Not every step yields a new component — `Customer Notification` covers two workflow steps. Model only the **major** workflows.

**Actor/Action approach** — useful when multiple actors exist. The system itself is always an actor (for automated functions like billing or inventory replenishment). For the same order-entry system:

- **Customer** — `Item Search`, `Item Details`, `Order Placement`, `Order Cancel`, `Customer Registration`, `Customer Profile`.
- **Order packer** — `Order Fulfillment`, `Order Shipment`.
- **System** — `Inventory Management`, `Supplier Ordering`, `Order Payment`.

Actor/Action tends to generate **more components** than Workflow, depending on how many flows are modeled.

### 2.2. Refining via Cohesion and Characteristics

A bloated `Order Placement` asked to *validate, display cart, determine shipping address, collect payment info, generate order ID, apply payment, adjust inventory, and email the customer* is doing too much. The **conjunction sniff test** flags it: when the role statement uses *and*, *also*, *in addition*, *as well as*, or piles up commas, the component likely needs splitting. After the split:

- `Order Placement` — validate, display cart, determine shipping address, collect payment info, generate order ID.
- `Payment Processing` — apply payment.
- `Inventory Management` — adjust inventory counts.
- `Customer Notification` — email order summary.

**Characteristics can force a split, too.** *Fundamentals* uses the Going Going Gone auction kata: a single `Bid Capture` component handled both auctioneer and bidders, but their characteristics differ — bidders need elasticity and scalability (potentially thousands); the auctioneer needs reliability and availability (a dropped bidder is bad; a dropped auctioneer is disastrous). The component split into `Bid Capture` (bidders) and `Auctioneer Capture` (auctioneer). **Different load profiles → different components**, even when the functional view says one suffices.

## 3. The Entity Trap

> **Antipattern: Entity Trap.** Naming components after entities (`Customer Manager`, `Item Manager`, `Order Manager`) and dumping all related functionality into them.

The signs:

- **Ambiguous names** — *"what does Order Manager do?"* yields *"manages orders."* Suffixes that should set off alarms: **Manager, Supervisor, Controller, Handler, Engine, Processor.** Compare with `Validate Order`, which is unmistakable.
- **Dumping ground** — all order functionality (validation, placement, history, fulfillment, shipping, tracking) collapses into one entity component, mirroring the "kitchen sink" utility classes every developer has written.
- **Coarse granularity hurts** — components become hard to maintain, test, and deploy.

> **CRUD escape hatch.** If the system genuinely is entity-based and only does CRUD, it doesn't need an architecture; use a CRUD framework or a low-code/no-code tool instead.

## 4. The Architecture Quantum

The component is the unit at which the architect *thinks*. The **architecture quantum** is the unit at which the architect *deploys* and the unit to which **characteristics belong**.

> **Architecture quantum** — an independently deployable artifact with high functional cohesion, high static coupling, and synchronous dynamic coupling. The plural is *quanta* (Latin *quantus*); a well-formed microservice within a workflow is the canonical example.

The formal definition has four properties:

| Property | Meaning |
|---|---|
| **Independently deployable** | The quantum includes everything it needs to function. A database the system can't run without is part of the quantum; a monolith sharing one database is by definition a quantum of one. |
| **High functional cohesion** | The quantum does something purposeful. A `Customer` quantum (cohesive) vs. a `Utility` quantum (random methods) illustrates the contrast. Distributed services are typically designed around a single workflow (a **bounded context**), exhibiting high cohesion by construction. |
| **High static coupling** | Internal wiring is dense — the quantum's bootstrap is tight. External wiring to *other* quanta is sparse. |
| **Synchronous dynamic coupling** | Temporary entanglement that appears when the quantum blocks on another quantum mid-workflow. |

**Quantum ≠ Bounded Context.** They are similar but not identical: bounded context is a DDD term about model scope; the quantum extends it with explicit static and dynamic coupling characteristics, which is why *The Hard Parts* uses a separate term.

### 4.1. Quantum Count by Architecture Style

Drawing a **static quantum diagram** of any legacy system is one of *The Hard Parts*' core diagnostics. It surfaces wiring, shows which systems are impacted by a change, and exposes decoupling opportunities.

| Style | Quantum count | Why |
|---|---|---|
| Any monolith | 1 | Single deployable + single database. |
| **Service-based architecture** | 1 | Independently deployed coarse-grained services, but a *shared monolithic database* couples them. |
| Mediated event-driven | 1 | Shared database *and* the Request Orchestrator are both holistic coupling points. |
| Broker event-driven, shared DB | 1 | Services without DB access depend on services that do, pulling them into the same quantum. |
| Event-driven, multiple stores, no static deps | Many | Each side runs independently. |
| Microservices (highly decoupled) | Many | Each service its own quantum; per-service characteristics become possible. |
| Microservices with tightly coupled UI | 1 | UI ties front and back together. |
| Micro-frontends | Many | Each service emits its own UI element; service + UI element together form a quantum, communicating via events. |

The big result: **any shared dependency (database, broker, mediator, UI) collapses what looks like a distributed architecture into a single quantum**, undermining per-service architecture characteristics. The shared-database service-based style is *one* quantum, not many — which is the central observation behind the data-decomposition chapters of *The Hard Parts*.

## 5. The Four Coupling Flavors

The quantum definition reorganizes coupling into four interacting flavors. *Fundamentals* and *The Hard Parts* line up cleanly on three of them; *The Hard Parts* adds dynamic coupling.

| Flavor | What it captures |
|---|---|
| **Semantic coupling** | The natural coupling of the problem domain (orders, inventory, carts, customers). No architecture pattern eliminates it; changing the domain changes the requirements. **Semantic coupling can only be increased by implementation, never decreased** — workflow logic must live somewhere. |
| **Implementation coupling** | How the team chose to implement dependencies — single DB vs. partitioned, monolith vs. distributed. Doesn't affect semantics but shapes the architecture. |
| **Static coupling** | The wiring of an architecture — how services depend on one another. Two microservices that depend on the same shared component or DB belong to the same quantum. |
| **Dynamic coupling** | The forces involved when quanta communicate at runtime to form workflows. Three sub-axes (communication / consistency / coordination) detailed in [Modularity, Cohesion, Coupling](foundations/modularity-cohesion-coupling.md). |

**Coupling rule of thumb** — higher coupling is allowed for narrower scopes; the broader the scope, the looser the coupling should be.

**Brittle architecture** is what happens when a single implementation change ripples through ostensibly unrelated parts — *Fundamentals* uses the example of renaming `State` to `StateCode` and breaking unsuspected callers.

**Temporary entanglement** *(The Hard Parts)* — even statically decoupled quanta become *temporarily* coupled during synchronous calls, because performance, responsiveness, and scale all entangle for the duration of the call. This is why choosing synchronous communication can collapse quantum boundaries that static coupling had separated.

## 6. Reuse and the Four Patterns

Once components recur across quanta, the architect needs a reuse strategy. Monoliths handle this by importing class files; distributed architectures cannot. *The Hard Parts* names the four available techniques and their trade-offs.

> **DRY vs WET.** Microservices culture promotes "share nothing!" and the WET acronym (*Write Every Time* / *Write Everything Twice*) as a counter to DRY abuse. Choosing among the four patterns is choosing *where* on the DRY–WET spectrum each kind of code belongs.

### 6.1. Code Replication

- **Definition** — shared code is copied into each service repository, eliminating sharing entirely; preserves the bounded context.
- **Sweet spot** — highly static one-off code such as Java annotations or C# attributes (e.g., a `@ServiceEntrypoint` marker) that contains no logic and is unlikely to change.
- **Migration use** — a `Utility.cs` class can be replicated so each service evolves it for its own context (related to the *tactical forking* technique).
- **Risk** — bug fixes or change propagation are extremely difficult; code drifts inconsistently across services, with no versioning.

### 6.2. Shared Library

- **Definition** — an external artifact (JAR, DLL) bound to services at **compile time**; the most common reuse technique in distributed architectures.
- **Granularity trade-off** — coarse-grained libraries simplify dependency management but force every consumer to retest/redeploy on any change; fine-grained libraries scope changes tightly but produce a "distributed monolith" of dependency relationships.
- **Always version.** Versioning provides backward compatibility and agility; one consumer can adopt a new `Validation.jar` without forcing the other nine to retest. **Versioning is the ninth fallacy of distributed computing** — communication of changes, deprecation policy, and version rollouts are far harder than they look.
- **Custom vs global deprecation** — custom deprecation per library matches each library's change rate (2–3 versions for stable `Security.jar`, 10 versions for volatile `Calculators.jar`) at the cost of tracking overhead; global deprecation (keep last four versions for everything) is simpler but causes churn.
- **Avoid `LATEST`.** Services pinning to `LATEST` risk breaking on emergency hot deployments. Explicit pinning is mandatory.
- **Best fit** — homogeneous environments with low-to-moderate change rates; compile-time binding leaves performance, scalability, and fault tolerance unaffected.

### 6.3. Shared Service

- **Definition** — shared functionality lives in a separately deployed service consumed at runtime via remote calls; **composition**, not inheritance.
- **Change is a double-edged sword** — a single redeploy propagates the change to all consumers, but a bad change is now a runtime change that can take down the system.
- **Versioning via API endpoints** — patterns like `app/1.4/discountcalc?orderid=123` work for REST but are subjective, require consumer reconfiguration, and break down across messaging/gRPC.
- **Performance** — every call adds network latency and (when endpoints are secured) security latency. gRPC and asynchronous request/reply via correlation IDs help mitigate.
- **Scalability** — the shared service must scale in lockstep with every consumer.
- **Fault tolerance** — if the shared service goes down, every consumer is non-operational until it recovers.
- **Best fit** — highly polyglot environments and shared functionality with high volatility, where compile-time binding is impractical.

### 6.4. Sidecars and Service Mesh

- **Problem framed** — microservices favor *duplicate over couple* for domain code, but operational concerns (monitoring, logging, auth, circuit breakers) benefit from coupling and consistency.
- **Hexagonal heritage** — Cockburn's *Ports and Adaptors* pattern separates domain from infrastructure; the **Sidecar** pattern updates that idea for microservices, with data and transactionality kept inside the domain core (per DDD).
- **Mechanics** — the operational portion of every service is extracted into a sidecar component owned by a shared infrastructure team; the sidecar attaches to the service like a motorcycle sidecar.
- **Service Mesh** — when every service includes the sidecar (enforced by fitness functions), the sidecars interconnect via a service plane to form a mesh that supports unified dashboards, scale control, and cross-cutting governance.
- **Orthogonal Coupling** — operational concerns are *orthogonal* to domain concerns; the Sidecar is an **orthogonal reuse pattern** that decorates behavior across the architecture, analogous to the GoF Decorator.
- **Best fit — operational coupling only.** Security, observability, polyglot governance. **Not for domain classes** — do not put `Customer` or `Address` in the sidecar.

### 6.5. Comparison

| Pattern | Binding | Best for | Key advantage | Key disadvantage |
|---|---|---|---|---|
| **Code Replication** | Copy into each repo | Highly static one-off code | Preserves bounded context | No versioning; near-impossible to propagate fixes |
| **Shared Library** | Compile-time | Homogeneous stacks; low-to-moderate change | Versioned; no runtime impact | Deprecation/communication complexity |
| **Shared Service** | Runtime | Polyglot stacks; high volatility | No duplication; good agility | Latency, lockstep scaling, runtime risk |
| **Sidecars / Mesh** | Runtime (per service) | Operational / cross-cutting concerns | Consistent infra; unified governance | One sidecar per platform; size growth |

## 7. Why Reuse Needs Slow Change

> **Two prerequisites for useful reuse** — *abstraction* (how candidates are discovered) **and** *slow rate of change* (what makes them useful).

Reuse is derived via abstraction but **operationalized by slow rate of change**. Operating systems and external frameworks reuse well because their cadence is well understood; internal domain capabilities and fast-moving frameworks do not.

> **Antipattern: Centralized Customer Service.** Orchestration-driven SOA's drive to consolidate every domain's view of an entity (e.g., Customer) into a single service produces brittleness: the entity grows complex enough to handle every scenario, and any change ripples throughout the architecture.

The Centralized Customer Service is the Entity Trap repeated at the service level. The cure is the same — **reuse via Platforms**, where each domain capability is exposed via a well-defined API that hides implementation details and limits breaking changes through encapsulation and contracts.

**The shorter rule** *(combining both books)*: choose the reuse pattern by the speed of change, not by the cleanliness of the code. Slow-changing → Shared Library. Fast-changing, polyglot → Shared Service. Cross-cutting infrastructure → Sidecar/Mesh. Genuinely static (annotations, markers) → Code Replication. **Domain reuse needs slow change to survive; if the domain is volatile, replicate it instead of sharing it** (see also tactical forking in the upcoming `decomposition/tactical-vs-strategic.md`).

## Sources

- [Fundamentals Ch 8: Component-Based Thinking](software/software-architecture/books/fundamentals-of-software-architecture/ch08_component_based_thinking.md) (primary — logical components, Workflow and Actor/Action approaches, the Entity Trap, refinement, the Going Going Gone case study)
- [The Hard Parts Ch 2: Discerning Coupling](software/software-architecture/books/software-architecture-the-hard-parts/ch02_discerning_coupling.md) (formal quantum definition, quantum count table, static vs. dynamic coupling)
- [The Hard Parts Ch 3: Architectural Modularity](software/software-architecture/books/software-architecture-the-hard-parts/ch03_architectural_modularity.md) (where the quantum scope intersects the five modularity drivers)
- [The Hard Parts Ch 8: Reuse Patterns](software/software-architecture/books/software-architecture-the-hard-parts/ch08_reuse_patterns.md) (the four reuse patterns, the Centralized Customer Service anti-pattern, the slow-rate-of-change rule, reuse via platforms)
- [Fundamentals Ch 7: Scope of Architecture Characteristics](software/software-architecture/books/fundamentals-of-software-architecture/ch07_scope_of_architecture_characteristics.md) (the four coupling flavors, the coupling rule of thumb)


<!-- prev-next-nav -->

---

← [Architecture Characteristics](software/software-architecture/foundations/architecture-characteristics.md) | [Trade-Off Analysis](software/software-architecture/foundations/tradeoff-analysis.md) →
