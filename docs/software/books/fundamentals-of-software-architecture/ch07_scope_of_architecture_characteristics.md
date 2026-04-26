# Ch 7: The Scope of Architectural Characteristics

## Table of Contents

- [1. Scope as a Forgotten Dimension](#1-scope-as-a-forgotten-dimension)
- [2. The Architecture Quantum](#2-the-architecture-quantum)
- [3. Types of Coupling](#3-types-of-coupling)
- [4. Synchronous Communication and Quanta](#4-synchronous-communication-and-quanta)
- [5. Using Scope to Drive Style](#5-using-scope-to-drive-style)
- [6. Kata: Going Green](#6-kata-going-green)
- [7. Scoping and the Cloud](#7-scoping-and-the-cloud)

## 1. Scope as a Forgotten Dimension

- **Old frameworks assumed one set of characteristics for the whole system** — fine for monoliths, fatally wrong for modern styles like microservices, where service-level and system-level characteristics differ.
- **Code-level metrics don't capture scope** — the structural measures from Ch 6 reveal low-level details but cannot evaluate dependent components outside the codebase (e.g., databases). A perfectly elastic codebase fails if its database isn't elastic too.
- **Architects need a scope measure** — needed while writing *Building Evolutionary Architectures* to express the structural evolvability of an architecture style; lacking one, the authors coined the **architecture quantum**.

## 2. The Architecture Quantum

- **Informal definition** — the smallest part of the system that runs independently. *Quantum* is Latin ("how great / how much"); plural is *quanta*, like *data*.
- **Microservice as canonical example** — a service that runs independently within the architecture, including its own data and dependencies, often forms an architecture quantum.
- **Formal definition — four properties:**
  - **Independent deployment from other parts of the architecture** — the quantum includes everything it needs to function. A database the system can't run without is part of the quantum, so a legacy app sharing one database is a quantum of one. In microservices each service owns its database (the **bounded context**), so each is its own quantum.
  - **High functional cohesion** — the quantum does something purposeful. A `Customer` component (cohesive) vs. a `Utility` component (random methods) illustrates the contrast. Distributed services are typically designed around a single workflow (a **bounded context**), exhibiting high cohesion by construction.
  - **Low external implementation static coupling** — coupling between quanta should be loose; quanta sit one abstraction higher than components and often align with service boundaries.
  - **Synchronous communication with other quanta** — see section 4.
- **Bounded Context (DDD)** — Eric Evans (Addison-Wesley, 2003): rather than a single shared `Customer` class across the org, each problem domain owns its own and reconciles at communication boundaries. Replaces the pre-DDD impulse to share entities globally, which caused tight coupling and coordination overhead.

## 3. Types of Coupling

- **Two things are coupled if changing one might break the other.** Architects must distinguish four flavors.

| Coupling | What it captures |
|---|---|
| **Semantic coupling** | The natural coupling of the problem domain (orders, inventory, carts, customers). No architecture pattern eliminates it; changing the domain changes the requirements. |
| **Implementation coupling** | How the team chose to implement dependencies — single DB vs. partitioned, monolith vs. distributed. Doesn't affect semantics but shapes the architecture. |
| **Static coupling** | The "wiring" of an architecture — how services depend on one another. If two microservices both depend on the same shared component or relational database, they belong to the same architecture quantum. |
| **Dynamic coupling** | The forces involved when quanta communicate at runtime to form workflows. Covered for event-driven architectures in Ch 15. |

- **Brittle architecture** — when a single implementation change ripples through ostensibly unrelated parts (e.g., renaming `State` to `StateCode` breaks unsuspected callers).

- **Coupling rule of thumb** — higher coupling is allowed for narrower scopes; the broader the scope, the looser the coupling should be.

## 4. Synchronous Communication and Quanta

- **Communication is dynamic coupling** — particularly relevant for operational architecture characteristics (Ch 4), which determine timing and blocking in distributed systems.
- **Mismatched characteristics example** — an `Auction` service synchronously calls a `Payment` service that handles only one payment per 500 ms. When many auctions end at once, calls fail; the services have different operational characteristics, and synchronous communication exposes the mismatch.
- **Asynchronous communication softens the impact** — a message queue acts as a buffer; bursts can be absorbed up to the queue's capacity. Sustained overflow still fails, but transient bursts succeed.
- **Synchronous communication is unforgiving** in distributed architectures with mismatched characteristics. The choice between sync and async itself can shift quantum boundaries.
- **New scope semantic** — modern architects define architecture characteristics at the *quantum* level, not the system level.

## 5. Using Scope to Drive Style

- **Decision tree** — quantum analysis drives a sequence of architectural choices: monolith vs. distributed → quantum boundaries → persistence → communication style.
- **Step 1 — single vs. multiple characteristic groups.** If one set of characteristics suffices, choose a monolithic architecture; if multiple groups are required, go distributed.
- **Step 2 — quantum boundaries (distributed only).** Determine granularity (covered in Ch 18 for microservices).
- **Step 3 — persistence.** Monolith ⇒ single database, developed and deployed in lockstep with the architecture. Distributed ⇒ either a single database (common in event-driven architectures) or partitioned along service granularity (microservices).
- **Step 4 — communication.** Synchronous vs. asynchronous between quanta; choosing synchronous can collapse quantum boundaries that static coupling had separated, since the two coupling types interact frequently.

## 6. Kata: Going Green

- **The system** — Going Green (GG) recycles and resells old electronics via public kiosks and a website running the same backend. Users upload model and condition, GG bids; if accepted the user drops the device in a kiosk or mails it; GG assesses, pays, then either recycles or resells. The system also produces reports and analytics.
- **Three clusters of architectural characteristics emerge:**

| Cluster | Characteristics | Why |
|---|---|---|
| Public-facing (kiosk + web) | scalability, availability, agility | Customer-facing volume and rapid evolution |
| Back-office | security, data integrity, auditability | Financial and regulatory concerns |
| Assessment | maintainability, deployability, testability (i.e., agility) | Business model relies on rapid updates as new device models ship — faster updates ⇒ higher resale value |

- **Why three quanta** — these characteristics counteract each other (auditability vs. fast deployability; UI scalability vs. back-office throughput). Trying to satisfy all eight in one architecture is possible but painful.
- **Use clusters as quantum boundaries** — let the architectural characteristics scope drive service granularity. Each cluster becomes an architectural quantum with its own boundary.

## 7. Scoping and the Cloud

- **Cloud resources encapsulate operational characteristics** — they hide elasticity, availability, and other concerns inside provider configuration, complicating quantum analysis.
- **Two cloud scenarios:**
  - **Cloud as container host** — teams run and orchestrate containers (e.g., **Kubernetes**) in the cloud. Architects must consider container-level characteristics and the orchestrator's constraints.
  - **Cloud-provider resources as system components** — the application is assembled from triggered functions, managed databases, and other building blocks. Architects must read the provider's advertised (and hopefully maintained) capabilities to design suitable behavior for that context.
- **Trade-offs shift, but the job stays constant** — capabilities once hard-won (elasticity) became configuration settings; new trade-offs (provider availability, security) replaced the old ones. Analyzing trade-offs remains the architect's role.
