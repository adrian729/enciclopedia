# Ch 2: Discerning Coupling in Software Architecture

## Table of Contents

- [1. Trade-off framework](#1-trade-off-framework)
- [2. Architecture quantum](#2-architecture-quantum)
- [3. Static coupling](#3-static-coupling)
- [4. Dynamic coupling](#4-dynamic-coupling)
- [5. Sysops Squad: understanding quanta](#5-sysops-squad-understanding-quanta)

## 1. Trade-off framework

- **"All things are poison, and nothing is without poison; the dosage alone makes it so a thing is not a poison"** — Paracelsus epigraph: coupling isn't bad, it must be applied appropriately. Fully decoupled services can't communicate with anything.
- **Why distributed decisions got harder** — pre-microservices distributed systems usually shared one relational database, which absorbed integrity and transaction concerns. Microservices push the database inside the service boundary (per bounded context), promoting transactionality from a data concern to a first-class architectural concern.
- **The pervasive question** — *how do architects determine the size and communication styles for microservices?* Too small breeds transaction and orchestration pain; too large breeds scale and distribution pain.
- **Three-step trade-off analysis** — (1) find what parts are entangled; (2) analyze how they are coupled; (3) assess trade-offs by determining the impact of change on interdependent systems.
- **Untangle before you decide** — the braid metaphor: you can't reason about a force without first separating it from the others it's wound into.

## 2. Architecture quantum

> **Architecture quantum** — an independently deployable artifact with high functional cohesion, high static coupling, and synchronous dynamic coupling. The plural is *quanta* (Latin *quantus*); a well-formed microservice within a workflow is the canonical example.

- **Independently deployable** — each quantum is a separate deployable unit, so a monolith is by definition a single quantum. Boundaries become a shared vocabulary across architects, developers, and operations, and force discussion of *deployment* dependencies (databases, UIs) that abstract diagrams usually elide.
- **High functional cohesion** — structural proximity of related elements; overlaps with the DDD bounded context (behavior + data implementing one domain workflow). A monolith is independently deployable but is rarely functionally cohesive, so it fails the second test.
- **Quantum ≠ bounded context** — they are similar but not identical: bounded context is a DDD term about model scope; the quantum extends it with explicit static and dynamic coupling characteristics, which is why the book uses a separate term.
- **Static vs dynamic coupling, in one sentence** — static coupling is *how services are wired together*; dynamic coupling is *how they call one another at runtime*.

## 3. Static coupling

- **Definition** — how static dependencies resolve through contracts: operating system, frameworks, libraries (transitive deps), brokers, container orchestration, databases — anything required to *bootstrap* the quantum.
- **Strictest possible contracts** — operational dependencies (IP addresses, URLs, broker presence) count as contracts, not just REST or SOAP.
- **Quantum count by architecture style:**

| Style | Quantum count | Why |
|-------|--------------|-----|
| Any monolith | 1 | Single deployable + single database. |
| Service-based architecture | 1 | Independently deployed coarse-grained services, but a *shared monolithic database* couples them. |
| Mediated event-driven architecture | 1 | The shared database *and* the Request Orchestrator are both holistic coupling points. |
| Broker event-driven architecture (no mediator) | 1 if shared DB | Services without DB access still depend on services that do, pulling them into the same quantum. |
| Event-driven with multiple data stores and no static deps | Multiple | Each side runs independently in a production-like ecosystem (may not participate in every workflow, but operates). |
| Microservices (highly decoupled) | Many | Each service forms its own quantum; per-service architecture characteristics become possible. |
| Microservices with tightly coupled UI | 1 | UI ties front and back together, especially with synchronous calls. |
| Micro-frontends | Many | Each service emits its own UI element; service + UI element together form a quantum, communicating via events. |

- **Service-based architecture** (book's specific definition) — a hybrid distributed macro-layered style with a separately deployed UI, separately deployed coarse-grained services, and a single relational database. Common target when restructuring a monolith because it sidesteps database decomposition.
- **Diagnostic use** — drawing a *static quantum diagram* of a legacy system surfaces the wiring, shows which systems are impacted by a change, and reveals decoupling opportunities.
- **Why coupling-point analysis matters** — any shared dependency (database, broker, mediator, UI) collapses what looks like a distributed architecture into a single quantum, undermining per-service architecture characteristics.

## 4. Dynamic coupling

Dynamic coupling concerns how quanta interact at runtime to form workflows. It is a multidimensional decision space defined by three interlocking forces:

- **Communication** — synchronous (caller blocks until receiver returns; e.g., gRPC) vs asynchronous (caller posts to a message queue, optionally gets a reply via a return queue, continues working in parallel). Queues are the common implementation but architects often omit them from diagrams as visual shorthand.
- **Consistency** — the strictness of transactional integrity required across calls; spectrum from atomic (all-or-nothing) to varying degrees of eventual consistency.
- **Coordination** — how the workflow is steered: orchestration (a dedicated coordinator service) vs choreography (services share coordination responsibility). Simple one-reply workflows don't need this dimension; complex ones do.
- **The forces interact** — atomicity is easier with synchronous + mediated; high scale comes from asynchronous + eventually consistent + choreographed. Architects can't pick each axis independently.
- **The eight-pattern matrix** — every combination of the three binary forces gets a name and a coupling rating, and Chapter 12 untangles the trade-offs:

| Pattern | Communication | Consistency | Coordination | Coupling |
|---------|---------------|-------------|--------------|----------|
| **Epic Saga(sao)** | synchronous | atomic | orchestrated | very high |
| **Phone Tag Saga(sac)** | synchronous | atomic | choreographed | high |
| **Fairy Tale Saga(seo)** | synchronous | eventual | orchestrated | high |
| **Time Travel Saga(sec)** | synchronous | eventual | choreographed | medium |
| **Fantasy Fiction Saga(aao)** | asynchronous | atomic | orchestrated | high |
| **Horror Story(aac)** | asynchronous | atomic | choreographed | medium |
| **Parallel Saga(aeo)** | asynchronous | eventual | orchestrated | low |
| **Anthology Saga(aec)** | asynchronous | eventual | choreographed | very low |

- **Fitness functions for dynamic coupling must be continuous** — typically monitors, since the behavior is observable only at runtime.

## 5. Sysops Squad: understanding quanta

- **Static coupling = "what's needed to bootstrap"** — for a Sysops Squad service: Java, SpringBoot, ~15–20 frameworks/libraries listed in the Maven POM, Postgres, Docker, *and* the event broker the service uses to communicate. The presence of the broker is static; calls *through* the broker are dynamic.
- **Defensive use** — the team built static quantum diagrams per service for *reliability analysis*: if X changes, what must be tested? The diagrams also expose how teams impact one another.
- **No off-the-shelf tool** — the platform team is building a custom mapper from container manifests, POM files, NPM dependencies, and observability log data (call graph) to maintain the static coupling view.
- **Dynamic coupling and elasticity (book's recap)** — scalability = supporting many concurrent users; elasticity = supporting bursts. If Ticketing operates at 10× the elastic scale of Assignment, a *synchronous* call bogs the workflow down on the slower service; an *asynchronous* call via a queue lets each service stay operationally independent and the caller move on.
- **Temporary entanglement** — even statically decoupled quanta become temporarily coupled during synchronous calls because performance, responsiveness, and scale all entangle for the duration of the call.
