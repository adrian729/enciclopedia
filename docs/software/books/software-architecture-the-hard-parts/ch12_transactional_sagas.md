# Ch 12: Transactional Sagas

## Table of Contents

- [1. Saga origins and the eight-pattern matrix](#1-saga-origins-and-the-eight-pattern-matrix)
- [2. The eight transactional saga patterns](#2-the-eight-transactional-saga-patterns)
- [3. Per-pattern ratings](#3-per-pattern-ratings)
- [4. State management and eventual consistency](#4-state-management-and-eventual-consistency)
- [5. Saga state machines](#5-saga-state-machines)
- [6. Techniques for managing sagas](#6-techniques-for-managing-sagas)
- [7. Sysops Squad saga: atomic transactions and compensating updates](#7-sysops-squad-saga-atomic-transactions-and-compensating-updates)

## 1. Saga origins and the eight-pattern matrix

- **Saga predates microservices** — concept goes back to a 1987 ACM paper concerned with limiting the scope of database locks in early distributed architectures.
- **Chris Richardson's microservices saga** — *a sequence of local transactions where each update publishes an event, triggering the next; if any step fails, the saga issues a series of **compensating updates** to undo prior changes*.
- **Eight possible saga types** — Richardson's saga is just one combination of the three dynamic-coupling forces (communication, consistency, coordination). Each binary force gives 2x2x2 = 8 named patterns.
- **Superscript coding (sao/sac/seo/sec/aao/aac/aeo/aec)** — three letters in alphabetical order of the dimensions: communication (s/a), consistency (a/e), coordination (o/c). Example: Epic Saga(sao) = synchronous, atomic, orchestrated.
- **Pattern existence ≠ pattern solvability** — a named pattern only recognizes commonality; distributed transactions in particular have legendary failure modes regardless of pattern.

## 2. The eight transactional saga patterns

| Pattern | Communication | Consistency | Coordination | Coupling | Key trade-offs |
|---------|---------------|-------------|--------------|----------|----------------|
| **Epic Saga(sao)** | Synchronous | Atomic | Orchestrated | Very high | Mimics monolith via compensating transactions; familiar but bottlenecked, transaction failure modes, low scale. |
| **Phone Tag Saga(sac)** | Synchronous | Atomic | Choreographed | High | First service acts as front controller; complexity rises linearly with workflow; OK for simple workflows with idempotent retries, slow on errors. |
| **Fairy Tale Saga(seo)** | Synchronous | Eventual | Orchestrated | High | Each service owns its own transaction; orchestrator manages compensating calls without holding a transaction open; popular, balanced trade-offs. |
| **Time Travel Saga(sec)** | Synchronous | Eventual | Choreographed | Medium | Chain of Responsibility / Pipes and Filters; each service owns transactionality; great fire-and-forget throughput, weak on complex errors. |
| **Fantasy Fiction Saga(aao)** | Asynchronous | Atomic | Orchestrated | High | Mediator must track many in-flight async transactions; race conditions, deadlocks; "far-fetched" — usually a misguided performance fix to Epic Saga. |
| **Horror Story(aac)** | Asynchronous | Atomic | Choreographed | Medium | Atomicity with the two loosest coupling styles; each service tracks undo for many out-of-order pending transactions; aptly named anti-pattern. |
| **Parallel Saga(aeo)** | Asynchronous | Eventual | Orchestrated | Low | Mediator coordinates compensations asynchronously; good for complex workflows that need high scale. |
| **Anthology Saga(aec)** | Asynchronous | Eventual | Choreographed | Very low | Opposite of Epic Saga; least coupled pattern; best for simple, mostly linear, high-throughput workflows; weak for complex error coordination. |

- **Coupling is not monotonically worst-to-best** — Horror Story(aac) is *not* the most coupled (that distinction belongs to Epic Saga(sao)) because it relaxes two of three forces; "worst" instead means most complex to operate.
- **Compensating updates** — a *compensating update* reverses a data write performed by another service (reversing an update, reinserting a deleted row, deleting an inserted row). Used heavily in Epic Saga(sao); riddled with side effects, isolation gaps, and possible compensation failures.

## 3. Per-pattern ratings

The book scores each pattern across four qualitative dimensions: **coupling**, **complexity**, **responsiveness/availability**, **scale/elasticity**.

| Pattern | Coupling | Complexity | Responsiveness/availability | Scale/elasticity |
|---------|----------|------------|-----------------------------|------------------|
| Epic Saga(sao) | Very high | Low | Low | Very low |
| Phone Tag Saga(sac) | High | High | Low | Low |
| Fairy Tale Saga(seo) | High | Very low | Medium | High |
| Time Travel Saga(sec) | Medium | Low | Medium | High |
| Fantasy Fiction Saga(aao) | High | High | Low | Low |
| Horror Story(aac) | Medium | Very high | Low | Medium |
| Parallel Saga(aeo) | Low | Low | High | High |
| Anthology Saga(aec) | Very low | High | High | Very high |

- **Selection guidance** — Fairy Tale(seo) and Parallel(aeo) come out as the most balanced default choices; Anthology(aec) wins for simple high-throughput pipelines; Epic(sao) should be reserved for cases where atomicity is non-negotiable.

## 4. State management and eventual consistency

- **Alternative to compensating updates** — instead of undoing prior writes, manage the saga via a **finite state machine** that always knows the saga's current state and corrects errors via retries or manual remediation.
- **Fairy Tale ticket completion example** — when the Survey Service is unavailable, the saga moves to `NO_SURVEY` and a successful response is returned to the Sysops Expert; the Ticket Orchestrator Service retries asynchronously and escalates to an admin/supervisor on persistent failure.
- **User experience benefit** — end user is decoupled from background failures; responsiveness stays good and the user moves on while the system reconciles.
- **Trade-off versus compensating updates** — *Advantages*: good responsiveness, less impact to end user on errors. *Disadvantages*: data may be temporarily out of sync, eventual consistency may take time.

## 5. Saga state machines

- **Definition** — a state machine describes all possible paths within a distributed architecture, starting at a beginning state and progressing through transition states with associated actions.
- **Sysops Squad ticket saga states** — `START` → `CREATED` → `ASSIGNED` → `ACCEPTED` → (`COMPLETED` | `REASSIGN`); `COMPLETED` → (`CLOSED` | `NO_SURVEY`); `NO_SURVEY` → `CLOSED`; `REASSIGN` → `ASSIGNED`.
- **Transition table** — formalizes initiating state, transition state, and the action that fires (e.g., `START → CREATED: Assign ticket to expert`); developers implement these triggers in the orchestrator (or per service in choreography).
- **Either compensating updates or state management** — both are valid; the choice depends on situation and a trade-off between responsiveness and consistency. Either way, *the state of the distributed transaction should be known and also managed*.

## 6. Techniques for managing sagas

- **Sagas are not a download** — they cannot be installed like an ACID transaction manager; they must be designed, coded, and maintained.
- **Annotations / custom attributes** — Java annotations (`@Saga`) and C# custom attributes provide a programmatic way to capture and document each saga in source code; enum values like `NEW_TICKET`, `CANCEL_TICKET`, `NEW_CUSTOMER`, `UNSUBSCRIBE`, `NEW_SUPPORT_CONTRACT` live in one `Transaction` enum as a single source of truth.
- **`@ServiceEntrypoint` + `@Saga`** — mark each service entry-point class with the sagas it participates in (e.g., `SurveyServiceAPI` participates in `NEW_TICKET`; `TicketServiceAPI` participates in `NEW_TICKET` and `CANCEL_TICKET`).
- **Code-walking CLI tool** — a simple custom tool can scan the codebase for `@ServiceEntrypoint` + `@Saga` annotations and answer queries like `./sagatool.sh NEW_TICKET -services`, listing every service in the saga; helps developers scope tests and impact analysis when a service changes.

## 7. Sysops Squad saga: atomic transactions and compensating updates

- **Workflow modeled** — Sysops Squad expert marks ticket complete via mobile app; Ticket Orchestrator synchronously updates Ticket Service, Ticket Service async-publishes analytics to a queue for the Analytics Service, then orchestrator synchronously calls Survey Service to email the customer survey; final ack returns to the expert.
- **Issue 1: lack of transaction isolation** — when Survey Service fails and the orchestrator issues a compensating update to revert the ticket, the Analytics Service has already consumed and processed the original "complete" event — a **side effect** that cannot be cleanly undone without complex catch-up logic ("turtles all the way down").
- **Issue 2: compensation failures** — compensating updates can themselves fail; if the Ticket Service errors when reverting from completed to in-progress, the system is in an inconsistent state and the end user gets confusing errors (e.g., "Ticket already marked as complete" on retry).
- **Issue 3: poor responsiveness** — atomic distributed transactions force the end user to wait for all corrective action before seeing the error response.
- **Issue 4: semantic over-coupling** — the Sysops Squad expert should not have to care whether the survey was sent; atomic distributed transactions semantically couple the end user to the entire business process.
- **Issue 5: rollback failures and locking dilemma** — a service may not be able to undo its operation (orchestrator needs coordination code for this); locking participants during the workflow guarantees validity but destroys performance and scale.
- **Trade-offs of atomic distributed transactions with compensating updates** — *Advantages*: data restored to prior state; allows retries and restart. *Disadvantages*: no transaction isolation; side effects on compensation; compensation may fail; poor responsiveness.
- **Decision** — prefer **Fairy Tale Saga(seo)** or **Parallel Saga(aeo)** with state management and eventual consistency over Epic Saga(sao) with compensating updates whenever atomicity is not a hard requirement; the user is shielded from background errors and responsiveness improves.
- **Closing principle** — *transactions force participants to stop their individual worlds and synchronize on a particular value*; much of the real world isn't transactional (Hohpe's "Starbucks Does Not Use Two-Phase Commit"); transactional coordination is one of the hardest parts of architecture, and the broader the scope, the worse it becomes.
