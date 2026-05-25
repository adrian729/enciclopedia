# Software Architecture

> A merged synthesis of two complementary books: **Fundamentals of Software Architecture: A Modern Engineering Approach** by Mark Richards and Neal Ford (2nd ed., O'Reilly 2025), and **Software Architecture: The Hard Parts** by Neal Ford, Mark Richards, Pramod Sadalage, and Zhamak Dehghani (O'Reilly 2021). Topics that both books cover are unified into a single page; topics unique to one book are kept and labelled. The original chapter-by-chapter book pages remain available in the **Books** section.

## Table of Contents

- [1. Why a Merged Section](#1-why-a-merged-section)
- [2. How the Two Books Compare](#2-how-the-two-books-compare)
- [3. How to Use This Section](#3-how-to-use-this-section)
- [4. Section Map](#4-section-map)

## 1. Why a Merged Section

The two books overlap heavily on the foundations of the discipline — modularity, cohesion, coupling, architecture characteristics, the architecture quantum, and the First Law that *everything is a trade-off* — and they diverge on what they each go deep on. *Fundamentals* surveys the full landscape (theory → nine-style catalog → artifacts → soft skills); *The Hard Parts* zooms in on the problems for which no best practice exists and builds the machinery (eight saga patterns, granularity equilibrium, four reuse patterns, four ownership scenarios, Data Mesh) to resolve them.

Reading both books in parallel forces a reader to keep cross-referencing. This section rewrites the shared material once with the disagreements called out inline, then organizes the unique material by *concept* — foundations, styles, decomposition, distributed concerns, practice — rather than by chapter order. The original chapter pages stay intact under **Books** as the author-voiced reference layer.

## 2. How the Two Books Compare

| Aspect                  | Fundamentals (Richards & Ford, 2025)                                                                          | The Hard Parts (Ford, Richards, Sadalage, Dehghani, 2021)                                                                                                                            |
| ----------------------- | ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Shape                   | Survey — 27 chapters across theory, style catalog, artifacts, soft skills                                     | Deep dive — 15 chapters on the problems where no best practice exists                                                                                                                |
| Style coverage          | Catalog of nine styles (layered, modular monolith, pipeline, microkernel, service-based, EDA, space-based, orchestration-driven SOA, microservices) with a shared evaluation template | None — assumes the reader already has the catalog and zooms straight to "how do I decompose / re-integrate a distributed architecture"                                              |
| Decomposition           | Brief — included as part of the modular-monolith and microservices chapters                                   | Six refactoring patterns + tactical-vs-component-based decision tree + monolithic data decomposition + granularity disintegrators/integrators equilibrium                            |
| Distributed transactions| Mentions saga pattern, points readers to *The Hard Parts*                                                     | Eight named saga patterns (Epic, Phone Tag, Fairy Tale, Time Travel, Fantasy Fiction, Horror Story, Parallel, Anthology) covering all combinations of communication/consistency/coordination |
| Data                    | Data topologies covered in the styles chapters                                                                | Data ownership (single / common / joint), distributed data access patterns, contracts, Data Mesh                                                                                     |
| Soft skills             | Three chapters on teams, negotiation, leadership                                                              | Embedded in narrative — ADRs and trade-off tables threaded through every chapter                                                                                                     |
| Running example         | Multiple katas (Silicon Sandwiches, Going Green, Going Going Gone, Nursing Hotline)                           | One scenario — Sysops Squad — worked end to end across all 15 chapters                                                                                                               |
| Distinctive emphasis    | The architecture *catalog* and the role *practice*; framing the discipline as the work of trade-off analysis | The architecture *machinery*; precise vocabulary (static/dynamic coupling, quantum, granularity, ownership, BASE) for the problems that resist best-practice answers                 |

Neither book is wrong — they are deliberately complementary. Together they cover what an architect needs: *Fundamentals* gives the landscape and the role; *The Hard Parts* gives the depth where the landscape leaves off.

## 3. How to Use This Section

- **Coming to architecture cold:** read [Foundations](software/software-architecture/foundations/architectural-thinking.md) in order, then skim [Styles → Overview](software/software-architecture/styles/overview.md) for the catalog map. The Styles pages are reference-shaped — visit them per-style as you need.
- **Decomposing an existing monolith:** start with [Decomposition → When to Decompose](software/software-architecture/decomposition/when-to-decompose.md), then walk through Component-Based Decomposition, Granularity, and Data Decomposition. Cross-reference [Distributed → Data Ownership](software/software-architecture/distributed/data-ownership.md) and [Transactional Sagas](software/software-architecture/distributed/transactional-sagas.md) when designing the target architecture.
- **Designing a new service boundary:** read [Foundations → Components and Quantum](software/software-architecture/foundations/components-and-quantum.md) and [Decomposition → Service Granularity](software/software-architecture/decomposition/service-granularity.md) together; both feed into the granularity equilibrium decision.
- **Picking an architecture style:** read [Styles → Overview](software/software-architecture/styles/overview.md) first; it cross-links the comparison criteria each individual style page is rated against.
- **Documenting a decision:** [Practice → Architectural Decisions](software/software-architecture/practice/architectural-decisions.md) covers the ADR template and the three antipatterns it cures.
- **Day-of review:** open the [Cheat Sheet](software/software-architecture/cheat-sheet.md) — the three laws, the four-dimensions test, coupling axes, saga matrix, granularity drivers, ADR skeleton, all on one page.

**Routing convention:** the merged section (`foundations/`, `styles/`, `decomposition/`, `distributed/`, `practice/`) is the canonical reading path. The per-chapter pages under `books/` are reference originals — consult them when you want each author's exact phrasing, the full chapter context, or the Sysops Squad / kata narrative voice, but the merged pages are the ones to read first.

Every merged page ends with a **Sources** section linking to the originating chapters in the books. When the books disagree on emphasis or recommendation, that disagreement is called out inline so the reader can form their own view. The Sysops Squad scenario from *The Hard Parts* is preserved on pages where it sharpens the explanation (most of `decomposition/` and `distributed/`) and stripped on pages where it would add no value (most of `styles/` and `practice/`).

## 4. Section Map

- **Foundations** — the vocabulary of the discipline.
  - [Architectural Thinking](software/software-architecture/foundations/architectural-thinking.md) — what an architect is, how the role differs from a senior developer, expectations.
  - [Modularity, Cohesion, Coupling](software/software-architecture/foundations/modularity-cohesion-coupling.md) — connascence (static/dynamic), Martin's metrics, static vs. dynamic coupling axes.
  - [Architecture Characteristics](software/software-architecture/foundations/architecture-characteristics.md) — what characteristics are, identifying them, measuring them, governing them with fitness functions.
  - [Components and Quantum](software/software-architecture/foundations/components-and-quantum.md) — logical components, the architecture quantum, the four reuse patterns (Code Replication, Shared Library, Shared Service, Sidecar/Mesh).
  - [Trade-Off Analysis](software/software-architecture/foundations/tradeoff-analysis.md) — the three-step method, MECE, the Out-of-Context Trap, snake oil, qualitative judgment.
- **Styles** — the nine-style catalog, one page per style.
  - [Overview & Choosing a Style](software/software-architecture/styles/overview.md) — the comparison template, fallacies of distributed computing, choosing-a-style decision flow, architectural patterns vs. styles.
  - Monolithic: [Layered](software/software-architecture/styles/layered.md), [Modular Monolith](software/software-architecture/styles/modular-monolith.md), [Pipeline](software/software-architecture/styles/pipeline.md), [Microkernel](software/software-architecture/styles/microkernel.md).
  - Distributed: [Service-Based](software/software-architecture/styles/service-based.md), [Event-Driven](software/software-architecture/styles/event-driven.md), [Space-Based](software/software-architecture/styles/space-based.md), [Orchestration-Driven SOA](software/software-architecture/styles/orchestration-driven-soa.md), [Microservices](software/software-architecture/styles/microservices.md).
- **Decomposition** — pulling a monolith apart.
  - [When to Decompose](software/software-architecture/decomposition/when-to-decompose.md) — modularity drivers, the water-glass analogy, feasibility (coupling metrics, main sequence).
  - [Component-Based Decomposition](software/software-architecture/decomposition/component-based-decomposition.md) — the six refactoring patterns with fitness functions.
  - [Tactical vs. Strategic](software/software-architecture/decomposition/tactical-vs-strategic.md) — tactical forking vs. component-based, the decision tree.
  - [Service Granularity](software/software-architecture/decomposition/service-granularity.md) — disintegrators/integrators equilibrium, the Grains of Sand antipattern.
  - [Data Decomposition](software/software-architecture/decomposition/data-decomposition.md) — pulling apart operational data; data disintegrators/integrators; the five-step process.
- **Distributed** — the concerns that only appear once services are separate.
  - [Data Ownership](software/software-architecture/distributed/data-ownership.md) — single / common / joint ownership and the four joint-ownership resolution techniques.
  - [Distributed Data Access](software/software-architecture/distributed/distributed-data-access.md) — Interservice Communication, Column Schema Replication, Replicated Caching, Data Domain.
  - [Workflows & Orchestration](software/software-architecture/distributed/workflows-orchestration.md) — orchestration vs. choreography, semantic coupling, state-management techniques.
  - [Transactional Sagas](software/software-architecture/distributed/transactional-sagas.md) — the eight saga patterns, compensating updates vs. state machines, the saga annotation technique.
  - [Contracts](software/software-architecture/distributed/contracts.md) — strict vs. loose, consumer-driven contracts, stamp coupling.
  - [Analytical Data & Data Mesh](software/software-architecture/distributed/analytical-data-and-mesh.md) — Warehouse → Lake → Mesh; the Data Product Quantum; Cooperative Quantum.
- **Practice** — the artifacts and soft skills of the role.
  - [Architectural Decisions](software/software-architecture/practice/architectural-decisions.md) — ADRs, the three antipatterns (Covering Your Assets, Groundhog Day, Email-Driven Architecture), affirmative voice.
  - [Analyzing Risk](software/software-architecture/practice/analyzing-risk.md) — the risk-assessment matrix, risk storming.
  - [Diagramming](software/software-architecture/practice/diagramming.md) — UML / C4 / ArchiMate, representational consistency, solid-vs-dotted line convention.
  - [Team Effectiveness](software/software-architecture/practice/team-effectiveness.md) — constraints and boundaries, Elastic Leadership, checklists.
  - [Negotiation & Leadership](software/software-architecture/practice/negotiation-and-leadership.md) — the 4 Cs, demonstration over discussion, the Ivory Tower antipattern.
  - [Laws & Intersections](software/software-architecture/practice/laws-and-intersections.md) — the three laws revisited, the nine architectural intersections, residuality theory.
- [**Cheat Sheet**](software/software-architecture/cheat-sheet.md) — single-page reference.

## Sources

- [Fundamentals of Software Architecture — Book Summary](software/software-architecture/books/fundamentals-of-software-architecture/book_summary.md) (Mark Richards and Neal Ford)
- [Software Architecture: The Hard Parts — Book Summary](software/software-architecture/books/software-architecture-the-hard-parts/book_summary.md) (Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani)
