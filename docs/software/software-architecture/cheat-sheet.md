# Software Architecture Cheat Sheet

> Single-page reference distilled from both books. For depth, follow the links.

## Table of Contents

- [1. The Three Laws](#1-the-three-laws)
- [2. The Four Dimensions of an Architecture](#2-the-four-dimensions-of-an-architecture)
- [3. Coupling Vocabulary](#3-coupling-vocabulary)
- [4. Architecture Characteristics](#4-architecture-characteristics)
- [5. Style Catalog At-a-Glance](#5-style-catalog-at-a-glance)
- [6. Decomposition Decision Trees](#6-decomposition-decision-trees)
  - [6.1. When to Decompose](#61-when-to-decompose)
  - [6.2. Tactical Forking vs. Component-Based](#62-tactical-forking-vs-component-based)
  - [6.3. Granularity Forces](#63-granularity-forces)
- [7. Distributed Concerns](#7-distributed-concerns)
  - [7.1. Reuse Patterns](#71-reuse-patterns)
  - [7.2. Data Ownership](#72-data-ownership)
  - [7.3. Distributed Data Access](#73-distributed-data-access)
  - [7.4. The Eight Sagas](#74-the-eight-sagas)
  - [7.5. Contracts](#75-contracts)
- [8. ADR Skeleton](#8-adr-skeleton)
- [9. Diagramming Conventions](#9-diagramming-conventions)
- [10. Red Flags Checklist](#10-red-flags-checklist)

## 1. The Three Laws

| # | Law | Test |
|---|---|---|
| 1 | Everything in software architecture is a **trade-off** | If you can't see the trade-off, you haven't identified it yet |
| 2 | **Why** is more important than **how** | Future architects can recover *how* from the code; *why* rots unless preserved |
| 3 | Most decisions are **spectra**, not binaries | A decision is *architectural* when each option carries significant trade-offs |

**Working goal:** strive for the *least worst* architecture, not the best.

See [Foundations → Trade-Off Analysis](foundations/tradeoff-analysis.md).

## 2. The Four Dimensions of an Architecture

| Dimension | What it answers |
|---|---|
| **Style** | How the system is shaped (layered, microservices, …) |
| **Characteristics** | What capabilities it must support (-ilities) |
| **Components** | Logical units that implement behavior |
| **Decisions** | The recorded justifications for the above |

A decision is *architecturally significant* (Nygard) when it affects structure, non-functional characteristics, dependencies, interfaces, or construction techniques.

See [Foundations → Architectural Thinking](foundations/architectural-thinking.md).

## 3. Coupling Vocabulary

**Architecture quantum:** independently deployable artifact with high functional cohesion, high static coupling, synchronous dynamic coupling.

**Static coupling** — how services are wired (OS, framework, libraries, brokers, databases). Drawn as a *static quantum diagram*.

**Dynamic coupling** — how services interact at runtime. Three axes:

| Axis | Options |
|---|---|
| Communication | synchronous (`s`) / asynchronous (`a`) |
| Consistency | atomic (`a`) / eventual (`e`) |
| Coordination | orchestrated (`o`) / choreographed (`c`) |

Eight combinations → eight saga patterns (see §7.4).

**Connascence** (static): Name, Type, Meaning, Position, Algorithm. **Dynamic:** Execution, Timing, Values, Identity. Rule of Degree: convert strong → weaker. Rule of Locality: weaker as distance grows.

**Martin metrics:** afferent `Ca`, efferent `Ce`, abstractness `A = Σma / (Σmc + Σma)`, instability `I = Ce / (Ce + Ca)`, distance from main sequence `D = |A + I − 1|`. Too far up: *Zone of Uselessness*. Too far down: *Zone of Pain*.

See [Foundations → Modularity, Cohesion, Coupling](foundations/modularity-cohesion-coupling.md).

## 4. Architecture Characteristics

| Bucket | Examples |
|---|---|
| Operational | availability, performance, recoverability, scalability |
| Structural | configurability, extensibility, maintainability |
| Cloud | on-demand scalability, elasticity, zone availability, region privacy |
| Cross-cutting | accessibility, authentication, security, supportability |

**Qualify** as a characteristic when: non-domain design consideration ✓ influences structure ✓ critical or important to success ✓.

**Limit to a top three** — the *Vasa* lesson; ranking seven never produces consensus.

**Composite characteristics:** *agility* = deployability + modularity + testability.

**Govern with fitness functions** — any objective mechanism that assesses a characteristic. JDepend cycle tests, ArchUnit/NetArchTest layer rules, Cyclomatic Complexity < 5, Chaos Monkey, security CVE scans in CI.

See [Foundations → Architecture Characteristics](foundations/architecture-characteristics.md).

## 5. Style Catalog At-a-Glance

| Style | Type | Quantum count | Best when |
|---|---|---|---|
| **Layered** | Monolith | 1 | Small app, tight budget, feasibility-driven |
| **Modular Monolith** | Monolith | 1 | DDD team, new system, mostly domain-based changes |
| **Pipeline** | Monolith | 1 | Distinct, ordered, deterministic processing |
| **Microkernel** | Monolith | 1 | Customization (per-state, per-client rules) |
| **Service-Based** | Distributed | ≤12 services, 1 DB | Pragmatic distributed; ACID transactions still needed |
| **Event-Driven** | Distributed | many | Fault tolerance, responsiveness, async workflows |
| **Space-Based** | Distributed | many | High variable load (concert tickets, auctions) |
| **Orchestration SOA** | Distributed | many | (Historical cautionary tale) |
| **Microservices** | Distributed | many | Share-nothing, independent deployability, polyglot persistence |

**Default direction of travel:** synchronous unless you have a reason; duplication is preferable to coupling.

See [Styles → Overview](styles/overview.md).

## 6. Decomposition Decision Trees

### 6.1. When to Decompose

Two primary drivers:

| Driver | Composed of |
|---|---|
| **Speed-to-market** | maintainability + testability + deployability |
| **Competitive advantage** | speed-to-market + scalability + availability/fault tolerance |

**Modularity ≠ distribution.** A modular monolith or microkernel can achieve maintainability/testability/deployability without distribution costs.

**Feasibility check:** plot components on the main sequence. Too much code in *Zone of Uselessness* or *Zone of Pain* → decompose later, fix structure first.

### 6.2. Tactical Forking vs. Component-Based

| Approach | Use when |
|---|---|
| **Component-Based Decomposition** | Components already discernible; preferred default |
| **Tactical Forking** | Chaotic, hard-to-extract codebase; fast but inner quality matches the monolith |

Avoid the **Elephant Migration Anti-Pattern** (pull out whatever's easy without a holistic plan) → produces a Big Ball of Distributed Mud.

### 6.3. Granularity Forces

Right-size services at the equilibrium of:

| Disintegrators (break apart) | Integrators (keep together) |
|---|---|
| Service scope & function | Database transactions |
| Code volatility | Workflow & choreography |
| Scalability & throughput | Shared code |
| Fault tolerance | Data relationships |
| Security | |
| Extensibility | |

**Grains of Sand antipattern** — taking "micro" too literally. Iterate via the three criteria: purpose, transactions, choreography.

See [Decomposition](decomposition/when-to-decompose.md), [Service Granularity](decomposition/service-granularity.md).

## 7. Distributed Concerns

### 7.1. Reuse Patterns

| Pattern | Best for | Trade-off |
|---|---|---|
| **Code Replication** | Static one-off code (annotations) | No versioning at all |
| **Shared Library** | Most common; compile-time bind | Always version, never `LATEST` (the 9th fallacy) |
| **Shared Service** | Polyglot / volatile shared logic | Latency, lockstep scaling, runtime fault path |
| **Sidecar / Service Mesh** | Operational concerns only | Orthogonal coupling; never for domain code |

Reuse needs *both* abstraction *and* slow rate of change. The **Centralized Customer Service** anti-pattern is what happens when a domain entity gets shared. Duplication is preferable to coupling.

### 7.2. Data Ownership

The **writer** is the owner. Read-only consumers don't change ownership.

| Scenario | Resolution |
|---|---|
| **Single Owner** | Unambiguous |
| **Common Owner** (most/all services write) | Dedicate one owner service; others send async write requests |
| **Joint Owner** (a few services in one domain) | Pick: Table Split / Data Domain / **Delegate** (default; domain-priority variant) / Service Consolidation |

ACID stops at the service boundary. Replace with **BASE**: Basic Availability, Soft state, Eventual consistency.

### 7.3. Distributed Data Access

| Pattern | Best for | Cost |
|---|---|---|
| **Interservice Communication** | Real-time freshness | \~30–300 ms network + security + data latency |
| **Column Schema Replication** | Aggregation/reporting | Ownership leakage |
| **Replicated Caching** | Mostly static, ≲500 MB | Startup ordering, license cost |
| **Data Domain** | Strong integrity, native joins | Broader bounded context |

### 7.4. The Eight Sagas

Code is communication / consistency / coordination → `s/a` `a/e` `o/c`.

| Pattern | Code | Coupling | When |
|---|---|---|---|
| **Epic Saga** | sao | Very high | Atomicity non-negotiable (mimics monolith) |
| **Phone Tag Saga** | sac | High | Front-controller flows |
| **Fairy Tale Saga** | seo | High | Balanced default |
| **Time Travel Saga** | sec | Medium | Pipes-and-filters throughput |
| **Fantasy Fiction Saga** | aao | High | Race conditions common (avoid) |
| **Horror Story** | aac | Medium | Anti-pattern by name |
| **Parallel Saga** | aeo | Low | Complex, high-scale workflows |
| **Anthology Saga** | aec | Very low | Simple high-throughput pipelines |

**Defaults:** *Fairy Tale (seo)* and *Parallel (aeo)*. Avoid compensating-update reliance for state — prefer a finite state machine.

### 7.5. Contracts

| Stance | Examples | Trade-off |
|---|---|---|
| **Strict** | RMI, gRPC, schema-validated JSON | Type safety, no ambiguity |
| **Middle** | REST, GraphQL | Resource modeling absorbs additions |
| **Loose** | Bare name/value JSON or YAML | Maximum decoupling; needs **consumer-driven contracts** for fidelity |

**Stamp coupling** — over-fat payloads. Legitimate only when scalability forces choreography and the payload carries workflow state.

See [Distributed](distributed/data-ownership.md), [Transactional Sagas](distributed/transactional-sagas.md), [Contracts](distributed/contracts.md).

## 8. ADR Skeleton

```
Title         A short imperative — "Use asynchronous messaging for X"
Status        Proposed | Accepted | Superseded
Context       The forces at play, including constraints and pressures
Decision      Affirmative, commanding voice: "We will…"
Consequences  What becomes easier and what becomes harder
Compliance    How conformance is verified (preferably a fitness function)
Notes         Author, date, last review, related ADRs
```

**Three antipatterns it cures:**

| Antipattern | Cure |
|---|---|
| **Covering Your Assets** (deferring to avoid blame) | Wait until the *last responsible moment*, then decide |
| **Groundhog Day** (relitigating without `why`) | Give *technical and business* justification |
| **Email-Driven Architecture** (decisions lost in inboxes) | One system of record; email links to it |

**LLM note (per *Fundamentals*):** LLMs predict probable answers and reference "best practices" — neither has a place in architectural decisions. LLMs have *knowledge*, not *wisdom*. Use them to outline trade-offs you might have missed.

See [Practice → Architectural Decisions](practice/architectural-decisions.md).

## 9. Diagramming Conventions

| Convention | Detail |
|---|---|
| **Standards** | UML (class, sequence), C4 (Context/Container/Component/Class), ArchiMate |
| **Lines** | Solid = synchronous; dotted = asynchronous (near-universal) |
| **Views** | Multiple — overview before drill-down; representational consistency |
| **Anti-pattern** | Irrational Artifact Attachment — value low-fidelity early artifacts (whiteboards, sticky notes) |
| **Accessibility** | Pair color with iconography; always include a key |

See [Practice → Diagramming](practice/diagramming.md).

## 10. Red Flags Checklist

Avoid these — both books mark them as failure modes:

- "It's a best practice" — there are no best practices for the hard parts.
- Sharing a domain entity across services (Centralized Customer Service anti-pattern).
- Synchronous + atomic distributed transactions by default (Epic Saga everywhere).
- Compensating-update soup with no state machine.
- Using `LATEST` for shared-library versions (the ninth fallacy).
- Stamp coupling — passing a 500 KB payload to satisfy a 200-byte need.
- Choosing modularity but skipping granularity equilibrium → Grains of Sand or Distributed Monolith.
- Naming components after entities (`OrderManager`) — the Entity Trap.
- "We need five nines" without converting to "86 seconds of downtime per day."
- Architects who dictate without justification — the Ivory Tower antipattern.
- ADRs that don't say *why*, just *what*.
- Defining characteristics in unbounded number — pick a top three.
- Decomposing without a business driver — modularity for its own sake.
- Decomposing without first picking the architecture target (component-based vs. tactical-fork).
- Sidecars carrying domain logic instead of operational concerns.
- Background Synchronization between bounded contexts as the long-term answer (breaks ownership).

See [Practice → Negotiation & Leadership](practice/negotiation-and-leadership.md).


<!-- prev-next-nav -->

---

← [Laws and Intersections](software/software-architecture/practice/laws-and-intersections.md)
