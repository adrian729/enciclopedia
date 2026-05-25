# Ch 4: Architectural Decomposition

## Table of Contents

- [1. Why vs how](#1-why-vs-how)
- [2. Is the codebase decomposable?](#2-is-the-codebase-decomposable)
- [3. Component-Based Decomposition](#3-component-based-decomposition)
- [4. Tactical Forking](#4-tactical-forking)
- [5. Sysops Squad saga: choosing the approach](#5-sysops-squad-saga-choosing-the-approach)

## 1. Why vs how

- **Modularity is the why, decomposition is the how** — Chapter 3 motivated breaking a monolith apart; this chapter is about whether and how to do it.
- **Two viable approaches** — **Component-Based Decomposition** (extract refined components incrementally) and **Tactical Forking** (clone the monolith, delete what you don't want).
- **Elephant Migration Anti-Pattern** — the "eat the elephant one bite at a time" approach: pick whatever feature seems easy and pull it out. Without a holistic view it leads to a *big ball of distributed mud* (also called a distributed monolith).
- **Decision tree** — first ask *is the codebase decomposable at all?* If yes, ask *is the source structured into observable components?* Structured codebase → Component-Based Decomposition. Unstructured → Tactical Forking.

## 2. Is the codebase decomposable?

- **Big Ball of Mud Anti-Pattern** — coined by Brian Foote (1999); a system with no internal structure (e.g., a web app with event handlers wired straight to database calls). Architects don't write patterns for these because architecture *is* internal structure.
- **No single decomposability metric exists** — judgment falls to the architect, but coupling metrics give macro signals.

### 2.1. Afferent and Efferent Coupling

- **Afferent coupling (Ca)** — number of *incoming* connections to a code artifact (component, class, function). Defined by Yourdon and Constantine (*Structured Design*, 1979).
- **Efferent coupling (Ce)** — number of *outgoing* connections to other artifacts.
- **Practical use during migration** — when pulling a monolith apart, a shared class such as `Address` is reused widely; afferent coupling tells the architect how many other parts depend on it. JDepend (visualized in Eclipse) is the tool example given.

### 2.2. Abstractness and Instability

- **Abstractness (A)** — Robert Martin's metric: ratio of abstract artifacts (interfaces, abstract classes) to concrete ones. `A = Σma / (Σmc + Σma)`. A 10,000-line `main()` scores ~0 and is hard to understand.
- **Instability (I)** — `I = Ce / (Ce + Ca)`. Measures volatility: a value near 1 means highly unstable (changes in others ripple in); near 0 means either stable (if abstract) or rigid (if concrete). Trade-off: high stability without abstraction implies duplication.
- **Read I and A together** — neither metric alone is meaningful; the next metric combines them.

### 2.3. Distance from the Main Sequence

- **Definition** — `D = | A + I - 1 |`. The "main sequence" is the idealized line where abstractness and instability balance.
- **Zone of uselessness** — upper-right corner: code so abstract it cannot be used.
- **Zone of pain** — lower-left corner: too much implementation, not enough abstraction; brittle and hard to maintain.
- **Decomposition guidance** — if many components fall into either zone, restructuring the internals first may not be worth the effort; the codebase may not be a good migration candidate.

## 3. Component-Based Decomposition

- **Definition** — an extraction approach that applies refactoring patterns to refine and extract **components** (logical building blocks, manifested as namespaces or directory structures) so they can become services in a controlled, incremental fashion.
- **Build services from components, not classes** — explicit guidance from the authors when migrating.
- **Target = service-based architecture** — the patterns produce a hybrid distributed style with separately deployed coarse-grained domain services sharing one database. Useful as a final destination *or* as a stepping-stone to microservices.
- **Why service-based architecture is a good first step**:
  - Determines which domains need finer microservice granularity and which can stay coarse.
  - Doesn't require breaking apart the database (deferred to Chapter 6).
  - Doesn't require operational automation or containerization; can deploy as the same EAR/WAR/Assembly as before.
  - Purely technical move; usually no organizational change is needed.

## 4. Tactical Forking

- **Origin** — named by Fausto De La Torre as a pragmatic option for big balls of mud.
- **Core insight** — instead of *extracting* desired pieces (which drags a tangle of dependencies along), *clone* the monolith and *delete* what isn't wanted. Compilation and tests verify removal; you avoid the unraveling effect of extraction.
- **Procedure** —
  1. Start with the single monolith and target two or more coarse-grained services (e.g., a hexagon+square service and a circle service).
  2. Clone the entire codebase per team.
  3. Each team deletes code unrelated to its target functionality, iteratively.
  4. End state: multiple coarse-grained services, each preserving the original behavior of its slice.

| Aspect | Tactical Forking |
|--------|------------------|
| **Benefit** | Teams can begin work immediately with virtually no up-front analysis. |
| **Benefit** | Deleting code is easier than extracting it from a tightly coupled chaotic codebase. |
| **Shortcoming** | Resulting services still contain large amounts of latent code from the monolith. |
| **Shortcoming** | Without extra work, the inner code quality is no better than the monolith — there is just less of it. |
| **Shortcoming** | Inconsistencies in shared code names/files make common code hard to identify and keep consistent. |

- **The name is apt** — "tactical" rather than strategic: a fast, unstructured way to migrate critical systems forward.

## 5. Sysops Squad saga: choosing the approach

- **Feasibility check** — Addison plotted the application against the main sequence. Most components landed near the line with only a few outliers, so decomposition was deemed feasible.
- **Why not Tactical Forking** — although Austen liked the sculptor metaphor, Addison pointed out the duplication problem: shared infrastructure code (logging, security) and shared persistence-layer database calls would have to be maintained in every fork. Most of Sysops Squad's pain points were maintainability, testability, and reliability — duplication makes those worse.
- **Why Component-Based Decomposition** — well-defined component boundaries already exist; service boundaries can emerge from component grouping rather than being defined up front; gives a safer, more controlled incremental migration.
- **ADR — Migration Using the Component-Based Decomposition Approach** — *Decision*: use Component-Based Decomposition. Justifications: pre-existing component boundaries; reduces duplication versus tactical forking; lets service boundaries emerge naturally; safer for reliability/availability/scalability concerns; team can collaborate without splitting. *Consequences*: longer migration timeline accepted; team stays together rather than splitting per fork.
