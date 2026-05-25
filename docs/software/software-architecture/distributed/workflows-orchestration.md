# Workflows & Orchestration

> *The Hard Parts* (Ch 11) is the only source — the chapter is dedicated to the *coordination* axis of dynamic coupling and to the difference between orchestration and choreography. The page also picks up the semantic-vs-implementation coupling lemma that recurs across the rest of the section: workflow logic cannot be reduced by clever patterns, only relocated. Hard Parts works the Sysops Squad scenario to settle the ticket workflow on orchestration after a collaborative trade-off table.

## Table of Contents

- [1. Coordination as the Third Coupling Force](#1-coordination-as-the-third-coupling-force)
- [2. Orchestration](#2-orchestration)
- [3. Choreography](#3-choreography)
- [4. Semantic vs. Implementation Coupling](#4-semantic-vs-implementation-coupling)
- [5. State Management in Choreography](#5-state-management-in-choreography)
- [6. Choosing Between the Two](#6-choosing-between-the-two)
- [7. The Sysops Squad Ticket Workflow](#7-the-sysops-squad-ticket-workflow)
- [Sources](#sources)

## 1. Coordination as the Third Coupling Force

[Modularity, Cohesion, Coupling](foundations/modularity-cohesion-coupling.md) introduced the three sub-axes of dynamic coupling: **communication** (sync ↔ async), **consistency** (atomic ↔ eventual), and **coordination** (orchestrated ↔ choreographed). This page is the deep dive on the third axis.

> *"Never use absolutes when talking about architecture, except when talking about absolutes."* — Logan's mentor

There is no universal *"always use choreography"* answer. The choice between orchestration and choreography is a trade-off analysis like every other hard part, and the trade-offs differ per workflow even within one system.

**Two fundamental coordination patterns:**

- **Orchestration** — a dedicated *orchestrator* (a.k.a. *mediator*) manages the workflow. One service per workflow owns state, error handling, recovery, and progression.
- **Choreography** — no central coordinator. Participating services share the responsibility, like dancers executing a pre-planned routine without a conductor.

The two are not "good vs. bad" — they sit at opposite ends of a coordination spectrum, and the rest of this page is about where on the spectrum each workflow belongs.

## 2. Orchestration

**Orchestrator role.** The orchestrator coordinates workflow state, optional behavior, error handling, notification, and other workflow maintenance. The name comes from a musical conductor unifying the parts — the orchestrator contains no domain behavior of its own, only the workflow it mediates.

**One orchestrator per workflow.** Microservices avoid a *global* orchestrator (e.g., an ESB) because that becomes a coupling point for every workflow. Each workflow gets its own dedicated orchestrator. This rule is what separates microservices orchestration from the previous-decade SOA orchestration anti-pattern.

**Happy path example.** A *Place Order* workflow:

```
Place Order
  → Order Placement Orchestrator
    → Order Placement Service (sync)
    → Payment Service (sync)
    → Fulfillment Service (async — no strict timing dependency)
    → Email Service (async)
```

**Error paths reuse existing communication links.** Payment rejection and back-order scenarios are handled by the orchestrator without adding new edges between domain services. Order Placement does not need to know that Payment rejected an order — the orchestrator catches the error and acts. Choreography does not get this property for free.

**Advantages:**

| Advantage | What it buys |
|---|---|
| **Centralized workflow** | A unified place for state and behavior as complexity rises. |
| **Error handling** | Easier with a state owner who sees the whole workflow. |
| **Recoverability** | Orchestrator can retry on short-term outages. |
| **State management** | Workflow state becomes queriable — *"what's happening to order #42?"* has a single answer. |

**Disadvantages:**

| Disadvantage | What it costs |
|---|---|
| **Responsiveness** | All traffic flows through the mediator — throughput bottleneck. |
| **Fault tolerance** | Orchestrator is a potential single point of failure (mitigable with redundancy + complexity). |
| **Scalability** | Fewer parallelism opportunities than choreography. |
| **Service coupling** | Central orchestrator tightly couples to every domain component it calls. |

## 3. Choreography

**No central coordinator.** Services interact like dance partners — the moves are pre-planned by the architect/choreographer but executed without a conductor.

**Happy path is simpler than orchestration's.** Fewer services (no orchestrator) and a chain of async messages:

```
Order Placement → Payment → Fulfillment → Email
```

**Error paths add edges.** A failed payment or a back-order forces services to issue **compensating messages** to peers, often broadcast to multiple subscribers (Email, Payment, Order Placement). Each error scenario adds communication links that did not exist on the happy path; the topology grows whenever an error case is added.

**Advantages:**

| Advantage | What it buys |
|---|---|
| **Responsiveness** | Fewer choke points; more parallelism. |
| **Scalability** | Lack of coordination points enables independent scaling. |
| **Fault tolerance** | No single orchestrator to fail; multiple instances trivially possible. |
| **Service decoupling** | No orchestrator means lower static coupling. |

**Disadvantages:**

| Disadvantage | What it costs |
|---|---|
| **Distributed workflow** | No workflow owner — error and boundary management is harder. |
| **State management** | No centralized state holder. |
| **Error handling** | Domain services must carry workflow knowledge — semantic bleed. |
| **Recoverability** | No central place to retry or remediate. |

## 4. Semantic vs. Implementation Coupling

The chapter's key lemma — and one that recurs across [Transactional Sagas](distributed/transactional-sagas.md) and [Contracts](distributed/contracts.md):

> **Semantic coupling** is the inherent coupling in the problem domain — the workflow steps the business actually requires. The architect cannot reduce it.

> **Implementation coupling** is how the architect models the interaction. Implementation choices can only preserve or *worsen* semantic coupling, never improve it.

Workflow logic must live somewhere. Choreography does not *remove* the orchestrator's responsibilities; it *spreads* them across the participating services. The total coupling is the same; the location is different. A team that claims *"we removed the orchestrator and reduced coupling"* has confused implementation coupling with semantic coupling.

**Technical vs. domain partitioning.** A layered monolith partitioned by technical capability "smears" a domain concern like *Catalog Checkout* across persistence, business rules, and UI layers — every workflow step crosses every layer. A domain-partitioned architecture aligns one component (or service) per workflow, keeping implementation complexity close to semantic complexity.

**The decade's lesson** — model the semantics of the workflow as closely as possible with the implementation. The more steps a workflow has, the more error and optional paths emerge, and the more coordination matters. This is the same instruction as the Page-Jones/Weirich rules in [Modularity, Cohesion, Coupling](foundations/modularity-cohesion-coupling.md): keep strong coupling close, weaken it as it spreads.

## 5. State Management in Choreography

Most workflows include transient state — what has executed, what is left, ordering, errors, retries. Orchestrated solutions have an obvious owner (the orchestrator). Choreography does not. Three common techniques fill the gap:

### 5.1. Front Controller

The first service in the chain owns workflow state in addition to its domain behavior. In the *Place Order* example, Order Placement Service tracks the whole workflow.

| Trade-off | Detail |
|---|---|
| **Buys** | Simplifies state queries; centralizes workflow knowledge in one place. |
| **Costs** | Adds workflow state to a domain service (it now does two jobs); increases inter-service chatter; harms performance/scale of the front controller; creates a *pseudo-orchestrator* inside what was supposed to be choreography. |

The Front Controller is honest about what it is — it's choreography with one service playing orchestrator on the side. Sometimes that is the right balance; often it is choreography hedging back toward orchestration without admitting it.

### 5.2. Stateless Choreography

Keep no transient workflow state at all. Rebuild any needed snapshot on demand by querying each service.

| Trade-off | Detail |
|---|---|
| **Buys** | Maximum performance and scale; extremely decoupled. |
| **Costs** | State must be reconstructed on the fly; complexity rises swiftly with workflow size; ad hoc queries are expensive. |

### 5.3. Stamp Coupling

Store workflow state in the **message contract** passed between services. Each service updates its part and forwards the message. The order moves through the workflow carrying its own status.

| Trade-off | Detail |
|---|---|
| **Buys** | Eliminates need for a front controller; any consumer can inspect status from the message. |
| **Costs** | Contracts grow larger (see [Contracts](distributed/contracts.md) for the bandwidth math); still no single place for ad hoc state queries. |

Stamp coupling is sometimes called an anti-pattern in the contracts chapter and a legitimate technique here. Both are true: it depends on whether you are deliberately using the message as a state carrier or accidentally over-specifying a payload.

## 6. Choosing Between the Two

| Force | Orchestration | Choreography |
|---|---|---|
| Workflow ownership | Mediator owns state | Front controller / stateless / stamp coupling |
| Error handling | Centralized, easier | Distributed across domain services |
| Recoverability | Mediator can retry | Each service must remediate |
| Responsiveness | Bottlenecked at mediator | Fewer choke points |
| Scalability | Lower | Higher |
| Fault tolerance | SPOF (mitigable) | Multiple instances easy |
| Service coupling | Higher | Lower |
| Best fit | Complex workflows with frequent error/boundary conditions | Simple workflows needing scale, infrequent errors |

**The complexity heuristic.** *As workflow complexity rises, the utility of an orchestrator rises proportionally.* Semantic complexity in particular favors a mediator — many steps, many optional paths, many error cases. A workflow with three sequential happy-path steps and zero error branches barely needs coordination; choreography wins. A workflow with twelve steps, parallel branches, three error compensations, and an SLA on user-visible status queries needs an orchestrator.

**Saga implications.** The communication × consistency × coordination cube produces eight saga patterns (see [Transactional Sagas](distributed/transactional-sagas.md)). Choreography underpins **Phone Tag Saga(sac)**, **Time Travel Saga(sec)**, and **Anthology Saga(aec)** — and can also produce the **Horror Story(aac)** anti-pattern. Orchestration underpins **Epic Saga(sao)**, **Fairy Tale Saga(seo)**, **Fantasy Fiction Saga(aao)**, and **Parallel Saga(aeo)**.

## 7. The Sysops Squad Ticket Workflow

Hard Parts works the Sysops Squad scenario to settle the primary ticket workflow on orchestration. The workflow involves Ticket Management, Ticket Assignment, Notification, and Survey services.

The team built a trade-off table collaboratively rather than reaching for a slogan:

| Force | Verdict |
|---|---|
| Workflow control | Favors orchestration — the team wants a single place to drive ticket lifecycle. |
| State query | Slightly favors orchestration; choreography with stamp coupling could also support it. |
| Error handling (cancellations, reassignments) | Favors orchestration — the error paths are frequent and complex. |
| Throughput requirements | Modest — does not force choreography. |

**ADR outcome** — use orchestration for the primary ticket workflow.

**Consequence recorded** — revisit if scalability requirements around the single orchestrator change. The decision is intentionally reversible: the next page ([Transactional Sagas](distributed/transactional-sagas.md)) shows the **Fairy Tale Saga(seo)** built on top of this orchestrator, with the state machine that drives ticket lifecycle.

The closing pattern of the page generalizes: *complexity drives orchestration*. When the workflow is simple, choreography buys responsiveness and scale at no real cost. When the workflow is complex, orchestration buys state ownership and error handling at the cost of throughput. Both books agree that the choice is per-workflow, not per-system — a microservices architecture often has orchestrated workflows and choreographed workflows side by side, and that is fine.

## Sources

- [The Hard Parts Ch 11: Managing Distributed Workflows](software/software-architecture/books/software-architecture-the-hard-parts/ch11_managing_distributed_workflows.md) (primary — orchestration vs. choreography, semantic-vs-implementation coupling, the three state-management techniques, Sysops Squad ticket workflow)


<!-- prev-next-nav -->

---

← [Distributed Data Access](software/software-architecture/distributed/distributed-data-access.md) | [Transactional Sagas](software/software-architecture/distributed/transactional-sagas.md) →
