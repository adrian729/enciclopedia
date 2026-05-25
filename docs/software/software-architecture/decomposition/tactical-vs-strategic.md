# Tactical vs. Strategic Decomposition

> *The Hard Parts* Ch 4 is the only source for this page — *Fundamentals* doesn't cover the choice between the two decomposition approaches at all. The chapter frames decomposition as a binary: **Component-Based Decomposition** for codebases with discernible internal structure, and **Tactical Forking** (Fausto De La Torre's name for "clone the monolith, delete what you don't want") for chaotic ones. The decision tree links the two to the feasibility check in [When to Decompose](decomposition/when-to-decompose.md), and the choice itself is recorded as an ADR — Sysops Squad's worked example is preserved at the end.

## Table of Contents

- [1. Why vs. How](#1-why-vs-how)
- [2. The Decision Tree](#2-the-decision-tree)
- [3. Component-Based Decomposition — The Strategic Path](#3-component-based-decomposition--the-strategic-path)
- [4. Tactical Forking — The Sculptor's Approach](#4-tactical-forking--the-sculptors-approach)
- [5. Trade-Offs Side by Side](#5-trade-offs-side-by-side)
- [6. Picking Between the Two — Heuristics](#6-picking-between-the-two--heuristics)
- [7. Sysops Squad — Choosing the Approach](#7-sysops-squad--choosing-the-approach)
- [Sources](#sources)

## 1. Why vs. How

[When to Decompose](decomposition/when-to-decompose.md) handled the *why*: the modularity drivers, the five characteristics, and the feasibility check. This page handles the *how*: once decomposition is justified and feasible, which approach do you use?

*The Hard Parts* names two — and only two — viable approaches.

| Approach | One-liner |
|---|---|
| **Component-Based Decomposition** | Apply the six refactoring patterns (Ch 5) to *extract* well-defined components into separately deployed services, incrementally. |
| **Tactical Forking** | *Clone* the monolith per target service, then *delete* what each fork doesn't need. |

The third "approach" — pick whatever seems easy and pull it out — is the **Elephant Migration Anti-Pattern**, and it produces a big ball of distributed mud. Decomposition needs a structural plan; this page is about which of the two structured plans applies.

## 2. The Decision Tree

The choice runs through two questions in order.

1. **Is the codebase decomposable at all?**
   - **No** — it's a Big Ball of Mud (Brian Foote, 1999) with no internal structure to refactor along. There's nothing to decompose. *Either rewrite or tactically fork.* See [When to Decompose § Big Ball of Mud](decomposition/when-to-decompose.md#61-big-ball-of-mud--no-internal-structure-to-pull-apart).
   - **Yes** — proceed to question 2.

2. **Is the source structured into observable components?**
   - **Structured** — namespaces or directory structures already express domain seams; the **Distance from the Main Sequence** check shows components clustered near the line rather than buried in the Zone of Pain. → **Component-Based Decomposition.**
   - **Unstructured but compilable** — code exists, runs, has tests of some kind, but components are not discernible from the directory tree. The codebase resists structural analysis but isn't a complete mess. → **Tactical Forking.**

The branches are not interchangeable. Picking Component-Based for an unstructured codebase produces a multi-year refactor that never converges; picking Tactical Forking for a well-structured codebase throws away the existing seams and ships duplicate code per fork. The feasibility check from [When to Decompose](decomposition/when-to-decompose.md#62-coupling-metrics-on-the-main-sequence) is what tells you which branch you're on.

## 3. Component-Based Decomposition — The Strategic Path

> **Definition.** An extraction approach that applies refactoring patterns to refine and extract **components** — logical building blocks manifested as namespaces or directory structures — so they can become services in a controlled, incremental fashion.

The full pattern sequence (Identify and Size → Gather Common Domain Components → Flatten → Determine Dependencies → Create Component Domains → Create Domain Services) is detailed in [Component-Based Decomposition](decomposition/component-based-decomposition.md). What matters for the choice is the *shape* of the approach:

- **Build services from components, not classes.** Components are the unit of extraction; class-level extraction loses the cohesion that justified the component boundary.
- **Target is service-based architecture first, microservices later.** The patterns produce a hybrid distributed style — separately deployed coarse-grained domain services sharing one database. That's the final destination for many teams; for others, it's the stepping-stone to finer microservices once they've learned each domain. See [Service Granularity](decomposition/service-granularity.md).
- **Defers data decomposition.** The shared database stays in place during the code extraction; pulling apart the schema is its own project, covered in [Data Decomposition](decomposition/data-decomposition.md).
- **Defers operational automation.** Domain services can be deployed as the same EAR/WAR/Assembly artifact as the monolith; containerization and pipeline overhaul aren't prerequisites.
- **Purely technical move.** Usually no organizational change is needed — the team stays together, with new components extracted iteratively.

**When Component-Based fits.** Pre-existing component boundaries; coupling metrics show components near the main sequence; the team values *control* and *safety* over *speed*; the drivers include maintainability and testability (both of which forking *worsens*).

## 4. Tactical Forking — The Sculptor's Approach

> **Tactical Forking** (Fausto De La Torre) — a pragmatic option for big balls of mud. Instead of *extracting* desired pieces, *clone* the monolith and *delete* what isn't wanted. Compilation and tests verify removal; the unraveling effect of extraction is avoided.

The core insight: in a chaotic codebase, every extraction drags an unknown tangle of dependencies along — pull on `Survey` and you find it threaded into `Login`, `Audit`, and three utility classes you didn't know existed. Deletion has the opposite property: the compiler tells you immediately whether removed code was anyone's dependency.

### 4.1. Procedure

1. Start with the single monolith and target two or more coarse-grained services (e.g., one service for hexagon + square functionality, another for circle functionality).
2. **Clone** the entire codebase per team — one fork per target service.
3. Each team **deletes** code unrelated to its target functionality, iteratively. Compilation and tests catch over-deletion.
4. End state: multiple coarse-grained services, each preserving the original behavior of its slice of the monolith.

The result is what *The Hard Parts* describes as a *"less of it"* version of the monolith — each fork still contains the same chaotic structure as the original, just with the irrelevant chaos deleted. The inner code quality has not improved; the *scope* has shrunk.

### 4.2. Why the Name

The book is deliberate about both halves of the name.

- **Tactical** — not strategic. A fast, unstructured way to migrate a critical system forward when there is no time or budget to build the structure that Component-Based Decomposition needs. Tactical Forking ships services; it doesn't *improve* services.
- **Forking** — not extracting. The codebase splits; the splits diverge; shared code maintenance is now an operational problem rather than a compile-time problem.

### 4.3. The Sculptor Metaphor

Austen in the Sysops Squad narrative likes the metaphor of a sculptor *carving away everything that isn't the statue*. It captures the right intuition for the tactic, but Addison points out the catch: the chunks the sculptor carves off don't disappear — they reappear in every other fork. Logging code, security code, persistence-layer calls all exist *in every fork*, and now they must be maintained in every fork independently.

## 5. Trade-Offs Side by Side

| Dimension | Component-Based | Tactical Forking |
|---|---|---|
| **Up-front analysis** | Heavy — six patterns, fitness functions, dependency mapping | Virtually none — teams can start immediately |
| **Codebase quality after** | Improved (resized components, normalized namespaces, isolated dependencies) | Unchanged inside each fork — *less of it*, same quality |
| **Team structure** | One team continues collaborating | One team per fork |
| **Shared code** | Consolidated into shared components/libraries (Pattern 2) | Duplicated across forks; inconsistent names make it hard to identify |
| **Latent code** | Eliminated by the patterns | Each fork carries large amounts of monolith leftover |
| **Migration timeline** | Longer, incremental | Faster initial split, harder long-term maintenance |
| **When the modularity drivers are…** | Maintainability, testability, deployability | Speed-to-market when the codebase resists analysis |

Tactical Forking benefits:

- **Teams begin work immediately** with virtually no up-front analysis.
- **Deleting code is easier than extracting it** from a tightly coupled chaotic codebase — the compiler is your guide.

Tactical Forking shortcomings (each of which is structural, not fixable by discipline):

- **Resulting services still contain large amounts of latent code** from the monolith.
- **Without extra work, inner code quality is no better than the monolith** — there is just less of it per service.
- **Inconsistencies in shared code names and files** make common code hard to identify and keep consistent across forks.

The asymmetry is the point: Component-Based pays its cost up front and gets a cleaner system; Tactical Forking pays no up-front cost and gets a faster split with the same internal problems. *Neither* approach is wrong; the choice depends on which cost the team can afford.

## 6. Picking Between the Two — Heuristics

The choice is structural — driven by the codebase, not by team preference — but a few rules of thumb compress the decision tree into something an architect can apply in a meeting.

- **Coupling-metric plot first.** Before any other discussion, plot the application on the abstractness/instability plane. Most components near the main sequence → Component-Based is on the table. Most components in the Zone of Pain → only Tactical Forking is viable, and you should call it that explicitly.
- **Modularity drivers second.** If the drivers (see [When to Decompose](decomposition/when-to-decompose.md)) include maintainability, testability, or deployability *as primary*, Tactical Forking is the wrong tool — it doesn't improve any of them inside each fork. If the drivers are *speed-to-market under crisis* or *competitive pressure to migrate now*, Tactical Forking buys time that Component-Based cannot.
- **Shared-code volume third.** If the monolith has substantial shared infrastructure (logging, security, persistence helpers, framework glue), Tactical Forking duplicates *all* of it into every fork, and the long-tail maintenance cost balloons. Component-Based consolidates shared code into shared components or libraries via Pattern 2.
- **Team shape fourth.** Component-Based works for one team incrementally. Tactical Forking assumes you can put a team on each fork independently. A single team trying to do Tactical Forking serially defeats the speed advantage that justified the choice.
- **Don't mix.** Picking Component-Based for the "easy" parts and Tactical Forking for the "hard" parts produces a hybrid that gets the *worst* of both — incomplete patterns *and* duplicated chaotic code.

The decision is committed in an ADR (see [Architectural Decisions](practice/architectural-decisions.md)); the context section is exactly the four heuristics above, and the consequences section is honest about what the *other* approach would have bought.

## 7. Sysops Squad — Choosing the Approach

Hard Parts works the Sysops Squad scenario to illustrate the decision and its ADR. The book is explicit that the choice is recorded as an Architectural Decision Record (see [Architectural Decisions](practice/architectural-decisions.md)), not as a hallway conversation.

### 7.1. The Feasibility Check

Addison plotted the application against the main sequence. Most components landed near the line with only a few outliers — the codebase was decomposable. That answered question 1 of the decision tree: *yes*.

### 7.2. Why Not Tactical Forking

Austen initially liked the sculptor metaphor — fast, immediately actionable, no analysis paralysis. Addison surfaced the duplication problem: Sysops Squad has substantial shared infrastructure code (logging, security) and shared persistence-layer database calls, all of which would have to be maintained in *every* fork. The dominant Sysops Squad pain points are **maintainability, testability, and reliability** — and duplication makes all three worse, not better. Tactical Forking would optimize for the wrong characteristics.

### 7.3. Why Component-Based

Well-defined component boundaries already existed in the namespaces. Service boundaries could emerge from component grouping rather than being defined up front. The team could continue collaborating rather than splitting per fork. The migration would be safer for the reliability/availability/scalability concerns that drove the project.

### 7.4. The ADR

> **ADR — Migration Using the Component-Based Decomposition Approach.**
> *Decision*: Use Component-Based Decomposition.
> *Justifications*: pre-existing component boundaries; reduces duplication versus tactical forking; lets service boundaries emerge naturally; safer for reliability, availability, and scalability concerns; team can collaborate without splitting.
> *Consequences*: longer migration timeline accepted; team stays together rather than splitting per fork; the per-pattern fitness functions become ongoing governance overhead.

The pattern sequence the ADR commits to is the six-pattern run in [Component-Based Decomposition](decomposition/component-based-decomposition.md). The complementary data work runs in parallel — see [Data Decomposition](decomposition/data-decomposition.md). Once the service-based architecture is in place, the granularity question — *should any of these services split further?* — is answered with the [Service Granularity](decomposition/service-granularity.md) disintegrators and integrators.

## Sources

- [The Hard Parts Ch 4: Architectural Decomposition](software/software-architecture/books/software-architecture-the-hard-parts/ch04_architectural_decomposition.md) (primary — the decision tree, Component-Based vs. Tactical Forking, the Sysops Squad ADR)


<!-- prev-next-nav -->

---

← [Component-Based Decomposition](software/software-architecture/decomposition/component-based-decomposition.md) | [Service Granularity](software/software-architecture/decomposition/service-granularity.md) →
