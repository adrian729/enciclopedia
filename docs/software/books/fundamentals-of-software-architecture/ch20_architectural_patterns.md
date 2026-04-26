# Ch 20: Architectural Patterns

## Table of Contents

- [1. Patterns vs. Styles vs. Solutions](#1-patterns-vs-styles-vs-solutions)
- [2. Reuse: Separating Domain and Operational Coupling](#2-reuse-separating-domain-and-operational-coupling)
- [3. Communication: Orchestration vs. Choreography](#3-communication-orchestration-vs-choreography)
- [4. CQRS](#4-cqrs)
- [5. Infrastructure: Broker-Domain Patterns](#5-infrastructure-broker-domain-patterns)

## 1. Patterns vs. Styles vs. Solutions

- **Styles** — named topologies distinguished by physical architecture, deployment, communication style, and data topology (covered in Part II).
- **Patterns** — contextualized solutions to common problems, inspired by *Design Patterns*. Any distributed style can use any of these patterns.
- **Patterns are not "best practices"** — labelling something a "best practice" lets architects shut off their brains and always apply the same solution; *better practice* would at least invite argument.
- **Patterns are not solutions** — frameworks, tools, and libraries *implement* patterns with varying fidelity and intermingling. Identify the pattern first, then choose the implementation.

## 2. Reuse: Separating Domain and Operational Coupling

- **Microservices guidance** — "duplication is preferable to coupling." Two services sharing a `Profile` typically each keep an internal representation and pass loose name-value JSON, so internal types and tech stacks can change without breaking integration.
- **Operational capabilities benefit from coupling** — monitoring, logging, auth, circuit breakers should be common across services. Letting each team own its own implementation of these descends into chaos (verification, coordinated upgrades, etc.).

### 2.1. Hexagonal Architecture (Ports and Adapters)

- **Origin** — Alistair Cockburn drew it as a hexagon and immediately regretted it; *Ports and Adapters* is the more descriptive name, but "Hexagonal" stuck because architects thought it sounded cool. Only four of the six sides are actually used.
- **Topology** — domain logic in the center; ports and adapters connect to the ecosystem.
- **Data fidelity flaw vs. microservices** — Hexagonal treats the database as just another adapter, excluding schema from business logic. Eric Evans (Domain-Driven Design) corrected this misperception: schemas must change to reflect business logic regardless of where they reside. Using Hexagonal literally with microservices isolates data and violates a core microservices principle.
- **Use as shorthand** — fine for "separation of operational and domain concerns" so long as context isn't misleading.

### 2.2. Service Mesh and Sidecar

- **Sidecar pattern** — isolates cross-cutting operational concerns into a consistent layer; an example of an *Orthogonal Reuse* pattern.

> **Sidebar — Orthogonal Coupling.** In math, two lines are orthogonal if they intersect at right angles, implying independence. In architecture, two parts may be *orthogonally coupled* — distinct purposes that must intersect to form a complete solution. Operational concerns (e.g., monitoring) are necessary but independent from domain behavior (e.g., catalog checkout). Recognizing orthogonal coupling lets architects find intersection points with minimum entanglement.

- **Sidecar/Service Mesh trade-offs:**

| Advantages | Disadvantages |
|---|---|
| Consistent way to create isolated coupling | Must implement a sidecar per platform |
| Consistent infrastructure coordination | Sidecar component may grow large/complex |
| Ownership per team, centralized, or hybrid | Implementation "drift" between independent teams |

- **Hexagonal vs. Service Mesh** — both implement the reuse-by-separation pattern. Hexagonal is general-purpose; Service Mesh suits microservices and other distributed architectures. Identify the pattern (separation), then choose the implementation.

## 3. Communication: Orchestration vs. Choreography

- **Setup** — four domain services (A–D) collaborate in a workflow. Orchestration adds a separate *orchestrator* service as coordinator; choreography has none.
- **Pattern equivalence** — *orchestration* and *mediation* are the same pattern; recognizing patterns inside implementations makes trade-offs apparent.

| Aspect | Orchestration | Choreography |
|---|---|---|
| Workflow control | Centralized in orchestrator | Distributed across services |
| Error handling | Easier — orchestrator is state owner | Harder — services need workflow knowledge |
| Recoverability | Orchestrator monitors state, can retry | Harder — no central retry point |
| State management | Orchestrator makes state queryable | No central state holder |
| Responsiveness | Bottleneck through orchestrator | More parallelism, fewer chokepoints |
| Fault tolerance | Single point of failure (mitigated by redundancy + complexity) | Easier to scale instances independently |
| Scalability | Orchestrator coordination cuts parallelism | Better — fewer coordination points |
| Service coupling | Tighter (frowned on in microservices) | Looser |

- **Second Law of Software Architecture** — you can't just do trade-off analysis once and be done with it. Any distributed style can use any of these communication patterns.

## 4. CQRS

- **Command-Query-Responsibility-Segregation** — splits a single client/server data interaction into two: writes go to one datastore (DB or durable queue), which synchronizes (usually async) to a separate read database.
- **When it pays off** — systems with stark differences between read and write volumes, or that want to isolate reads from writes for security or other reasons.
- **Independent characteristics per side** — different data models per database if needed, allowing different architecture characteristics for reads vs. writes.
- **Pattern type** — a data communication pattern that facilitates differing architecture characteristics for different data capabilities, security concerns, or other reasons benefiting from physical separation.

## 5. Infrastructure: Broker-Domain Patterns

- **EDA event handling** — handlers are implemented by *brokers* in the architecture's infrastructure. Topics/queues are typically owned by the sender (e.g., `Payment` knows the topic address to subscribe to). Coupling extends to infrastructure, not just code/data.

### 5.1. Single-Broker Pattern

- **One broker for the whole workflow** — every event processor knows where to go to subscribe; single place for logging, monitoring, governance.
- **Risks** — if the single broker goes down, the whole workflow stops; under high message volume the broker can become swamped.

| Advantages | Disadvantages |
|---|---|
| Centralized discovery | Fault tolerance |
| Least possible infrastructure | Throughput limits |

### 5.2. Domain-Broker Pattern

- **Broker per domain group** — each group of related services shares a broker, mirroring the architecture's domain partitioning. Preserves discovery while raising fault tolerance, scalability, and elasticity.

| Advantages | Disadvantages |
|---|---|
| Better isolation | More difficult discovery of queues/topics |
| Matches domain boundaries | More infrastructure = more expensive |
| More scalable | More moving parts to maintain |

- **Neither is a "best practice"** — architects must balance discovery against domain isolation in their specific system.
