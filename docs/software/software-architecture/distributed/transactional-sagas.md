# Transactional Sagas

> *The Hard Parts* (Ch 12) is the primary source — the eight saga patterns, the FSM-vs-compensating-update choice, the annotation technique, and the Sysops Squad ticket-completion FSM. *The Hard Parts* (Ch 2) is the secondary source — the dynamic-coupling cube that generates the eight patterns and the per-pattern coupling ratings. For the three sub-axes themselves see [Modularity, Cohesion, Coupling](foundations/modularity-cohesion-coupling.md). Hard Parts works the Sysops Squad scenario to show why Epic Saga(sao) with compensating updates fails for ticket completion and why Fairy Tale Saga(seo) with a state machine is the right replacement.

## Table of Contents

- [1. The Saga Concept](#1-the-saga-concept)
- [2. The Eight-Pattern Cube](#2-the-eight-pattern-cube)
- [3. Per-Pattern Ratings and Defaults](#3-per-pattern-ratings-and-defaults)
- [4. Compensating Updates vs. Finite State Machines](#4-compensating-updates-vs-finite-state-machines)
- [5. The Sysops Squad Ticket-Completion FSM](#5-the-sysops-squad-ticket-completion-fsm)
- [6. Managing Sagas in Source Code](#6-managing-sagas-in-source-code)
- [Sources](#sources)

## 1. The Saga Concept

The **saga** concept predates microservices by three decades. The 1987 ACM paper *Sagas* (Garcia-Molina and Salem) proposed sequences of small local transactions as a way to limit database-lock scope in early distributed architectures. Chris Richardson re-popularized the term for microservices:

> *A saga is a sequence of local transactions where each update publishes an event, triggering the next; if any step fails, the saga issues a series of **compensating updates** to undo prior changes.*

Hard Parts observes that Richardson's saga is *one* combination of the three dynamic-coupling forces (communication, consistency, coordination), not the only one. Each force is binary; 2 × 2 × 2 = **eight named patterns**, each with a different coupling profile and a different failure mode.

**Pattern existence ≠ pattern solvability.** A named pattern only recognizes commonality; distributed transactions have legendary failure modes regardless of which saga shape you pick. The whole point of the cube is that *several* of the eight produce intractable systems, and they are nameable so teams can avoid them deliberately.

## 2. The Eight-Pattern Cube

Hard Parts encodes each pattern with a three-letter superscript code: **(communication)(consistency)(coordination)** in that alphabetical order — `s/a` (sync/async), `a/e` (atomic/eventual), `o/c` (orchestrated/choreographed).

| Pattern | Code | Communication | Consistency | Coordination | Coupling | Notes |
|---|---|---|---|---|---|---|
| **Epic Saga** | `(sao)` | Sync | Atomic | Orchestrated | **Very high** | Mimics monolith via compensating transactions; familiar but bottlenecked, low scale, classical failure modes. |
| **Phone Tag Saga** | `(sac)` | Sync | Atomic | Choreographed | High | First service acts as front controller; complexity rises linearly with workflow length; OK for simple workflows with idempotent retries. |
| **Fairy Tale Saga** | `(seo)` | Sync | Eventual | Orchestrated | High | **Balanced default.** Each service owns its own transaction; orchestrator coordinates without holding a transaction open. |
| **Time Travel Saga** | `(sec)` | Sync | Eventual | Choreographed | Medium | Chain of Responsibility / Pipes and Filters; each service owns its transactionality. Great fire-and-forget throughput, weak on complex errors. |
| **Fantasy Fiction Saga** | `(aao)` | Async | Atomic | Orchestrated | High | Mediator must track many in-flight async transactions; race conditions, deadlocks. Usually a misguided performance "fix" to Epic Saga. |
| **Horror Story** | `(aac)` | Async | Atomic | Choreographed | Medium | **Anti-pattern.** Atomicity with the two loosest coupling styles; each service tracks undo for many out-of-order pending transactions. Aptly named. |
| **Parallel Saga** | `(aeo)` | Async | Eventual | Orchestrated | Low | **Balanced default.** Mediator coordinates compensations asynchronously; good for complex workflows that need high scale. |
| **Anthology Saga** | `(aec)` | Async | Eventual | Choreographed | **Very low** | Opposite of Epic Saga; least coupled pattern. Best for simple, mostly linear, high-throughput pipelines; weak for complex error coordination. |

**Coupling is not monotonically worst-to-best.** Horror Story(aac) is *not* the most coupled — Epic Saga(sao) holds that distinction by relaxing none of the three forces. *Worst* in Horror Story's case means *most complex to operate*, not most coupled.

## 3. Per-Pattern Ratings and Defaults

Each pattern is scored across four qualitative dimensions: **coupling**, **complexity**, **responsiveness/availability**, **scale/elasticity**.

| Pattern | Coupling | Complexity | Responsiveness/availability | Scale/elasticity |
|---|---|---|---|---|
| Epic Saga(sao) | Very high | Low | Low | Very low |
| Phone Tag Saga(sac) | High | High | Low | Low |
| **Fairy Tale Saga(seo)** | High | Very low | Medium | High |
| Time Travel Saga(sec) | Medium | Low | Medium | High |
| Fantasy Fiction Saga(aao) | High | High | Low | Low |
| Horror Story(aac) | Medium | Very high | Low | Medium |
| **Parallel Saga(aeo)** | Low | Low | High | High |
| Anthology Saga(aec) | Very low | High | High | Very high |

**Three guidance defaults:**

- **Fairy Tale(seo)** and **Parallel(aeo)** are the most balanced choices — both score well across responsiveness and scale without paying excessive complexity. Reach for one of them when no specific force dominates.
- **Anthology(aec)** wins for simple, mostly linear, high-throughput pipelines where the workflow has few error paths and choreography can stay simple.
- **Epic(sao)** should be reserved for cases where atomicity is non-negotiable and synchronous orchestration genuinely matches the domain. Most workflows that *feel* like they need Epic actually fit Fairy Tale or Parallel once the team accepts eventual consistency.

The defaults are not absolute — the trade-off matrix from [Trade-Off Analysis](foundations/tradeoff-analysis.md) still runs per workflow.

## 4. Compensating Updates vs. Finite State Machines

Two ways to manage saga state when something fails:

### 4.1. Compensating Updates

A compensating update *reverses* a data write performed by another service — reversing an update, reinserting a deleted row, deleting an inserted row. Epic Saga(sao) relies on them heavily.

**Five failure modes** that recur across the chapter:

| Issue | What goes wrong |
|---|---|
| **Lack of transaction isolation** | Compensating the original write doesn't roll back side effects — an Analytics Service that already consumed the original event keeps its derived data. *Turtles all the way down*. |
| **Compensation failures** | Compensating updates can *themselves* fail. If reversal of a `complete` status errors, the system is in an inconsistent state and retries produce confusing errors (*"Ticket already marked as complete"*). |
| **Poor responsiveness** | The end user waits for all corrective action before seeing the error response. |
| **Semantic over-coupling** | The end user (e.g., a Sysops Squad expert) shouldn't have to care whether a survey was sent. Atomic distributed transactions semantically couple the user to the entire business process. |
| **Rollback failures + locking dilemma** | A service may be unable to undo its operation. Locking participants for the duration would guarantee validity but destroys performance and scale — and is precisely the lock scope sagas were invented to avoid in 1987. |

### 4.2. Finite State Machine (Preferred)

The alternative is to **manage the saga via a finite state machine** that always knows the saga's current state and corrects errors via retries or manual remediation rather than by undoing writes.

| Property | Compensating Updates | Finite State Machine |
|---|---|---|
| Data restoration | Restored to prior state | Soft state held until convergence |
| Isolation | None during the workflow | Same — but irrelevant; no rollback expected |
| Responsiveness | Poor (user waits for compensations) | Good (user moves on; system reconciles in background) |
| Error handling | Compensations can fail | Retries + escalation; FSM survives a failure cleanly |
| Best fit | Mandatory atomicity | Anything else |

**The trade-off** — *Advantages of FSM*: good responsiveness; less impact to end user on errors. *Disadvantages*: data may be temporarily out of sync; eventual consistency may take time.

Both compensating updates and state management are valid; the choice depends on situation and a trade-off between responsiveness and consistency. Either way: **the state of the distributed transaction should be known and managed.**

## 5. The Sysops Squad Ticket-Completion FSM

Hard Parts works the Sysops Squad scenario to make the FSM concrete. The Sysops expert marks a ticket complete from the mobile app; the workflow involves Ticket Service, Analytics Service, and Survey Service.

**The state machine:**

```
START → CREATED → ASSIGNED → ACCEPTED → (COMPLETED | REASSIGN)
COMPLETED → (CLOSED | NO_SURVEY)
NO_SURVEY → CLOSED
REASSIGN → ASSIGNED
```

A transition table formalizes initiating state, transition state, and action (e.g., `START → CREATED: Assign ticket to expert`). Developers implement the triggers in the orchestrator (Fairy Tale) or per-service (choreographed variants).

**The Survey-Service-unavailable example.** When the Survey Service is unavailable at the completion step:

1. The saga moves to **`NO_SURVEY`** and returns a successful response to the expert immediately.
2. The Ticket Orchestrator Service retries the survey send asynchronously.
3. On persistent failure, the orchestrator escalates to an admin/supervisor for manual remediation.
4. When the survey eventually sends (or is administratively closed), the saga transitions `NO_SURVEY → CLOSED`.

**User-experience benefit** — the expert is decoupled from a background failure they cannot fix. Responsiveness stays good; the system reconciles. Contrast with the Epic Saga version where the expert waits for the survey send to succeed and sees an error on its failure for which they have no recourse.

**Why this beats compensating updates here:**

- The Analytics Service has already consumed the `complete` event; there is no clean way to undo its derivation. The FSM does not try.
- The expert does not have to know about the survey — semantic coupling is honest.
- The orchestrator owns the state, so retries and escalations have a clear home.

**Decision** — prefer **Fairy Tale Saga(seo)** or **Parallel Saga(aeo)** with state management and eventual consistency over **Epic Saga(sao)** with compensating updates whenever atomicity is not a hard requirement.

> *Transactions force participants to stop their individual worlds and synchronize on a particular value.* Much of the real world isn't transactional — Gregor Hohpe's *Starbucks Does Not Use Two-Phase Commit*. Transactional coordination is one of the hardest parts of architecture, and the broader the scope, the worse it becomes.

## 6. Managing Sagas in Source Code

**Sagas are not a download.** They cannot be installed like an ACID transaction manager. They must be designed, coded, and maintained — and that means the architecture needs a way to keep track of which services participate in which sagas.

**Java annotations / C# attributes** give a programmatic way to document each saga in source code. A single `Transaction` enum holds the saga catalog:

```java
public enum Transaction {
    NEW_TICKET,
    CANCEL_TICKET,
    NEW_CUSTOMER,
    UNSUBSCRIBE,
    NEW_SUPPORT_CONTRACT
}
```

Each service entry-point class is marked with the sagas it participates in:

```java
@ServiceEntrypoint
@Saga(Transaction.NEW_TICKET)
public class SurveyServiceAPI { ... }

@ServiceEntrypoint
@Saga({Transaction.NEW_TICKET, Transaction.CANCEL_TICKET})
public class TicketServiceAPI { ... }
```

C# uses the equivalent attribute syntax — `[ServiceEntrypoint]`, `[Saga(Transaction.NEW_TICKET)]`. The mechanism is the same.

**Code-walking CLI tool.** A simple custom tool scans the codebase for `@ServiceEntrypoint` + `@Saga` annotations and answers queries like:

```
$ ./sagatool.sh NEW_TICKET -services
TicketServiceAPI
SurveyServiceAPI
NotificationServiceAPI
TicketAssignmentServiceAPI
```

The output is a worked impact-analysis answer: *"if I'm about to change the NEW_TICKET saga, here are the services I need to test."* The tool also catches the dual antipattern — a service that *implements* saga-relevant code but forgot the annotation, surfacing the gap before it causes a production surprise.

The annotation technique is the Sagas-as-Architecture move: making the saga membership visible in source so the architecture can be governed by fitness functions rather than tribal knowledge. It pairs with the consumer-driven contract testing from [Contracts](distributed/contracts.md) — both convert opinion into automated check.

## Sources

- [The Hard Parts Ch 12: Transactional Sagas](software/software-architecture/books/software-architecture-the-hard-parts/ch12_transactional_sagas.md) (primary — eight saga patterns, FSM vs. compensating updates, Sysops Squad ticket-completion saga, annotation technique)
- [The Hard Parts Ch 2: Discerning Coupling in Software Architecture](software/software-architecture/books/software-architecture-the-hard-parts/ch02_discerning_coupling.md) (secondary — the dynamic-coupling cube that produces the eight patterns, the per-pattern coupling ratings)


<!-- prev-next-nav -->

---

← [Workflows & Orchestration](software/software-architecture/distributed/workflows-orchestration.md) | [Contracts](software/software-architecture/distributed/contracts.md) →
