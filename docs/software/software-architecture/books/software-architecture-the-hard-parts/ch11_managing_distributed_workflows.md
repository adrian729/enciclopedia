# Ch 11: Managing Distributed Workflows

## Table of Contents

- [1. Coordination as a coupling force](#1-coordination-as-a-coupling-force)
- [2. Orchestration communication style](#2-orchestration-communication-style)
- [3. Choreography communication style](#3-choreography-communication-style)
- [4. Semantic versus implementation coupling](#4-semantic-versus-implementation-coupling)
- [5. Workflow state management](#5-workflow-state-management)
- [6. Trade-offs between orchestration and choreography](#6-trade-offs-between-orchestration-and-choreography)
- [7. Sysops Squad saga: managing workflows](#7-sysops-squad-saga-managing-workflows)

## 1. Coordination as a coupling force

- **Three coupling forces revisited** — Chapter 2 named *communication*, *consistency*, and *coordination* as the three dimensions of dynamic quantum coupling; this chapter zooms into coordination.
- **"Never use absolutes when talking about architecture, except when talking about absolutes"** — Logan's mentor's rule: there is no universal "always use choreography" advice; the choice is a trade-off analysis like every other hard part.
- **Two fundamental coordination patterns** — *orchestration* (a dedicated orchestrator/mediator manages the workflow) and *choreography* (no central coordinator; participating services share the responsibility).

## 2. Orchestration communication style

- **Orchestrator role** — coordinates workflow state, optional behavior, error handling, notification, and other workflow maintenance; named after a musical conductor unifying the parts.
- **One orchestrator per workflow** — microservices avoid a global orchestrator (e.g., an ESB) because that becomes a coupling point; each workflow gets its own dedicated orchestrator that contains no domain behavior outside the workflow it mediates.
- **Happy path example** — Place Order goes to the Order Placement Orchestrator, which calls Order Placement Service synchronously, then Payment Service synchronously, then Fulfillment Service asynchronously (no strict timing dependency), then Email Service asynchronously.
- **Error paths reuse existing communication links** — payment-rejected and back-order scenarios are handled by the orchestrator without adding new edges between domain services, unlike choreography.
- **Advantages** — **Centralized workflow** — a unified place for state and behavior as complexity rises. **Error handling** — easier with a state owner. **Recoverability** — orchestrator can retry on short-term outages. **State management** — workflow state becomes queriable.
- **Disadvantages** — **Responsiveness** — all traffic flows through the mediator, creating a throughput bottleneck. **Fault tolerance** — orchestrator is a potential single point of failure (mitigatable with redundancy + complexity). **Scalability** — fewer parallelism opportunities than choreography. **Service coupling** — central orchestrator tightly couples to domain components.

## 3. Choreography communication style

- **No central coordinator** — services interact like dance partners; the moves are pre-planned by the architect/choreographer but executed without a conductor.
- **Happy path is simpler** — fewer services (no orchestrator) and a chain of asynchronous messages: Order Placement → Payment → Fulfillment → Email.
- **Error paths add edges** — failed payment or back-order requires services to issue **compensating messages** to peers, often broadcast to multiple subscribers (Email, Payment, Order Placement); each error scenario adds communication links that did not exist on the happy path.
- **Advantages** — **Responsiveness** — fewer single choke points and more parallelism. **Scalability** — lack of coordination points enables independent scaling. **Fault tolerance** — no single orchestrator to fail; multiple instances easy. **Service decoupling** — no orchestrator means less coupling.
- **Disadvantages** — **Distributed workflow** — no workflow owner makes error and boundary management harder. **State management** — no centralized state holder. **Error handling** — domain services must carry workflow knowledge. **Recoverability** — no central place to retry or remediate.

## 4. Semantic versus implementation coupling

- **Semantic coupling** — the inherent coupling that exists in the problem domain (the workflow steps the business actually requires). Mandated by domain requirements; the architect cannot reduce it.
- **Implementation coupling** — how the architect models that interaction. Implementation choices can only preserve or *worsen* semantic coupling, never improve it.
- **Technical vs domain partitioning** — a layered monolith partitioned by technical capability "smears" a domain concern like Catalog Checkout across persistence, business rules, and UI layers; a domain-partitioned architecture aligns one component per workflow, keeping implementation complexity close to semantic complexity.
- **Lesson of the last decade** — model the semantics of the workflow as closely as possible with the implementation; the more steps a workflow requires, the more potential error and optional paths emerge, and the more coordination matters.

## 5. Workflow state management

Most workflows include transient state (what has executed, what is left, ordering, errors, retries). Orchestrated solutions have an obvious owner (the orchestrator); choreography does not. Three common techniques for choreographed state:

- **Front Controller pattern** — first service in the chain of responsibility owns workflow state in addition to its domain behavior (e.g., Order Placement Service). Creates a pseudo-orchestrator within choreography. **Trade-offs**: simplifies queries and centralizes state but adds workflow state to a domain service, increases inter-service chatter, and harms performance/scale.
- **Stateless choreography** — keep no transient workflow state at all; rebuild the snapshot on demand by querying each service. **Trade-offs**: high performance and scale, extremely decoupled, but state must be reconstructed on the fly and complexity rises swiftly with workflow size.
- **Stamp coupling** — store extra workflow state in the message contract passed between services; each service updates its part and forwards. Eliminates the need for a front controller and lets any consumer inspect status, but contracts grow larger and there is still no single place for ad hoc state queries.

## 6. Trade-offs between orchestration and choreography

| Force | Orchestration | Choreography |
|-------|---------------|--------------|
| Workflow ownership | Mediator owns state | Front controller, stateless, or stamp coupling |
| Error handling | Centralized, easier | Distributed across domain services |
| Recoverability | Mediator can retry | Each service must remediate |
| Responsiveness | Bottlenecked at mediator | Fewer choke points |
| Scalability | Lower | Higher |
| Fault tolerance | Single point of failure | Multiple instances easy |
| Service coupling | Higher | Lower |
| Best fit | Complex workflows with frequent error/boundary conditions | Simple workflows needing scale, infrequent errors |

- **Complexity drives orchestration** — as workflow complexity rises, the utility of an orchestrator rises proportionally; semantic complexity especially favors a mediator.
- **Choreography sweet spot** — workflows that need responsiveness and scalability, with simple or infrequent error scenarios; underpins **Phone Tag Saga(sac)**, **Time Travel Saga(sec)**, and **Anthology Saga(aec)**, but can also produce the **Horror Story(aac)** anti-pattern.
- **Orchestration sweet spot** — complex workflows with rich boundary/error handling; underpins **Epic Saga(sao)**, **Fairy Tale Saga(seo)**, **Fantasy Fiction Saga(aao)**, and **Parallel Saga(aeo)**.

## 7. Sysops Squad saga: managing workflows

- **Workflow under analysis** — primary ticket flow involving Ticket Management, Ticket Assignment, Notification, and Survey services.
- **Trade-off table built collaboratively** — workflow control favors orchestration; state query favors both (orchestration query, or stamp coupling/per-service query in choreography); error handling for cancellations and reassignments favors orchestration.
- **Decision (ADR)** — use orchestration for the primary ticket workflow; consequence: revisit if scalability requirements around the single orchestrator change.
