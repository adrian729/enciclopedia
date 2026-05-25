# Laws and Intersections

> *Fundamentals* closes with two chapters that double as the book's epilogue: Ch 26 — the nine **architectural intersections** the architecture must align with — and Ch 27 — the three laws revisited with worked trade-off examples. *The Hard Parts* doesn't have an equivalent closing pair; its laws are stated in Ch 1 and applied implicitly throughout. This page is the joint epilogue of the merged section.

## Table of Contents

- [1. The Three Laws, Revisited](#1-the-three-laws-revisited)
- [2. First Law in Practice — Trade-Off Worked Examples](#2-first-law-in-practice--trade-off-worked-examples)
- [3. Second Law in Practice — Why Over How](#3-second-law-in-practice--why-over-how)
- [4. Third Law in Practice — The Significance Test](#4-third-law-in-practice--the-significance-test)
- [5. The Nine Architectural Intersections](#5-the-nine-architectural-intersections)
- [6. Parting Advice](#6-parting-advice)
- [Sources](#sources)

## 1. The Three Laws, Revisited

The first edition of *Fundamentals* codified two universal observations as laws; the second edition adds a third, uncovered while writing.

> **First Law of Software Architecture** — *Everything in software architecture is a trade-off.*

> **Second Law of Software Architecture** — *Why is more important than how.*

> **Third Law of Software Architecture** — *Most architecture decisions aren't binary but rather exist on a spectrum between extremes.*

Each one yields a practical move covered below.

## 2. First Law in Practice — Trade-Off Worked Examples

The architect's real job under the First Law is **trade-off analysis**, not silver bullets. Architects rarely get credit for good decisions but always get blamed for bad ones; cultivate a reputation as an **objective arbiter** rather than an evangelist. Yesterday's best practice becomes tomorrow's antipattern; the ecosystem keeps evolving and weakens once-sound decisions. Decision-makers want sober objectivity, not advocacy.

### 2.1. Shared Library vs. Shared Service

Pertinent factors, each rated for which option wins:

| Factor | Shared library | Shared service |
|---|---|---|
| Heterogeneous code | | ✓ |
| High code volatility | | ✓ |
| Ability to version changes | ✓ | |
| Overall change risk | ✓ (compile-time verification) | |
| Performance | ✓ (in-process call) | |
| Fault tolerance | ✓ | |
| Scalability | ✓ | |

**Tallied positives favour the library — *for these factors and this context*.** Change the context (polyglot team that doesn't care about performance or scale) and *heterogeneous code* and *volatility* weight higher; the library tally flips.

### 2.2. Queue vs. Topic

| Factor | Queue | Topic |
|---|---|---|
| Heterogeneous payloads per consumer | ✓ | |
| Independent monitoring and scaling | ✓ | |
| Better security | ✓ | |
| Low coupling | | ✓ |
| Single-message broadcast | | ✓ |
| High extensibility | | ✓ |
| Stamp coupling risk | (avoids) | (exposes) |

Pick by organizational priority: **queues if security dominates, topics if extensibility does.** The tally isn't a winner — it's a framework that forces the architect to declare what the project actually weights.

### 2.3. The First-Law Corollaries

> **Corollary 1 — Missing Trade-Offs.** If you think you've discovered something that *isn't* a trade-off, you just haven't *identified* the trade-off yet.

The hidden cost of **code reuse** is the canonical illustration. Effective reuse needs both **abstraction** and **low volatility**. Architects spot the first and miss the second; sharing high-churn code creates breaking-change ripple across the system. This is exactly what burned orchestration-driven SOA: domain concepts were reused, and every change cascaded.

*"Plumbing"* (frameworks, libraries, platforms) is the right reuse target. Domain concepts are not — which is why DDD bounded contexts forbid implementation-detail reuse.

> **Why we can't have nice things — trade-offs.** Clients ask for both high decoupling (microservices agility) *and* high institutional reuse. **Reuse is implemented via coupling; decoupling and reuse are fundamentally incompatible.**

> **Corollary 2 — You Can't Do It Just Once.** Trade-off analysis must be repeated. Subtle differences in dozens or hundreds of variables (complexity, team experience, budget, team topology, schedule) push the result one way or the other. There are no sweeping, semipermanent decisions.

## 3. Second Law in Practice — Why Over How

Diagrams alone capture *how*. Experienced architects can read a system and explain how it works, but rarely *why* a previous architect chose this option over another — because the decision criteria weren't recorded. **Document with diagrams *and* ADRs.**

The artifacts the rest of this section already built up — [ADRs](practice/architectural-decisions.md), [diagrams](practice/diagramming.md), the [risk assessment](practice/analyzing-risk.md) — are exactly the *why*-preservation machinery the Second Law demands. They're not separate processes; they're the Second Law in operational form.

### 3.1. The Out-of-Context Antipattern

> **Antipattern: Out of Context** — the architect knows the trade-offs but not how to *weight* them for the current context.

The shared-library/shared-service tally in §2.1 favoured the library overall, but a polyglot team that doesn't care about performance or scale should pick the shared service. **Generic trade-off analysis is only useful when applied in a specific context** — the same warning *The Hard Parts* makes about its eight-saga matrix (see [Trade-Off Analysis](foundations/tradeoff-analysis.md)).

The Out-of-Context antipattern is the Second Law's failure mode: the *why* is preserved, but the *weights* aren't.

## 4. Third Law in Practice — The Significance Test

Few decisions are binary. Concepts resist clean definitions (architecture vs. design, orchestration vs. choreography, topics vs. queues) precisely because their criteria lie on a messy spectrum.

The Third Law yields **a useful test for what counts as architectural**:

> *A software architecture decision is one where each of the options has significant trade-offs.*

If everything in architecture is a trade-off (First Law), then an architectural decision must involve trade-offs on every option. A decision with one clearly dominant option isn't architectural — it's design. The test is concrete enough to use in a meeting: *list the options, list the trade-offs, and if any option doesn't have significant ones, this isn't an architecture decision and shouldn't sit on the architect's plate.*

Don't force binaries. Every answer in software architecture is *"it depends"* because each criterion sits somewhere on a spectrum. Architects decide in a swamp of uncertainty, often on incomplete information.

## 5. The Nine Architectural Intersections

Architecture must be **aligned**, not just chosen. Selecting characteristics, picking a style, and leading the team isn't enough; the architecture must align with the rest of the technical and business environment. *Fundamentals* names nine such intersections.

### 5.1. Architecture and Implementation

*"That's an implementation detail"* is often the cause of failure. Source code must align with three things: **operational concerns, internal structure, and constraints.**

> **The 80,000-user crash.** An order-entry system picks microservices for high scalability and elasticity; the team adds an *in-memory replicated cache* between `Order Placement` and `Inventory` for responsiveness. Under real load the cache exhausts VM memory and the system crashes around 80,000 concurrent users. Architecture was optimized for scalability/elasticity; implementation for responsiveness/decoupling. Both made good local decisions; the misalignment killed the system.

Structural integrity needs **governance tooling** — ArchUnit (Java), ArchUnitNet/NetArchTest (.NET), PyTestArch, TSArch — to keep source-code structure aligned with the logical architecture. See [Foundations → Architecture Characteristics](foundations/architecture-characteristics.md) for the fitness-function machinery.

### 5.2. Architecture and Infrastructure

The boundary between architecture and operations has shifted into architecture. Pre-2000s, operations was outsourced and contractually distant; modern styles like microservices freely leverage characteristics (elastic scale) that used to be purely operational.

> **Pets.com sidebar.** The 1998 ecommerce site spent its budget on a sock-puppet mascot rather than infrastructure; the Christmas rush crushed it. Failures like this drove architects toward elastic-scale designs and toward attention to this intersection.

Microservices was born of this collaboration — its creators offloaded operational concerns to operations rather than reimplementing them inside the architecture (as orchestration-driven SOA had to), laying the foundation of DevOps in the process. Cloud can still misalign: deploying services across regions or availability zones may cancel out the gains of in-memory replicated or distributed caches.

### 5.3. Architecture and Data Topologies

Three database topology types — *monolithic*, *distributed domain-based*, *distributed database-per-service*. **Match the database's superpowers to the architecture's.** Scalability and elasticity are superpowers for microservices, EDA, and space-based — and also for **key-value and columnar DBs**, making them strong amplifiers. Relational data fits relational DBs; key-value pairs in a relational DB is a misalignment that hurts both.

### 5.4. Architecture and Engineering Practices

*Processes* are how teams form, run meetings, organize workflow. *Engineering practices* are process-agnostic techniques (CI, CD, TDD). **Style imposes practice** — microservices assumes automated provisioning, testing, and deployment.

> **Waterfall vs. microservices** generates massive friction. Agile shines when migrating between styles thanks to tight feedback loops, the **Strangler Pattern**, and feature toggles. The Strangler Pattern + feature toggles is how an Agile team migrates gracefully without a flag day.

### 5.5. Architecture and Team Topologies

**Partitioning must match.** Domain-partitioned teams (cross-functional, end-to-end ownership) align with domain-partitioned styles like microservices; technically partitioned teams (UI, backend, shared services, DB) align with layered. Misalignment guarantees struggle — even simple changes become hard. The [Team Effectiveness](practice/team-effectiveness.md) page covers the team side.

### 5.6. Architecture and Systems Integration

Systems rarely live in isolation. Every external dependency raises questions about availability, scale, and responsiveness compared to the calling system. Static and dynamic coupling between systems undermines scalability, responsiveness, and agility — even technically excellent solutions must respect security/platform/documentation standards of the systems they integrate with.

### 5.7. Architecture and the Enterprise

Architecture lives inside an enterprise — the collection of systems and products in a company, division, or department comes with **security standards, platforms, technologies, and documentation/diagramming standards.** Ignore them and even technically excellent solutions get labelled failed *one-offs* and discarded.

### 5.8. Architecture and the Business Environment

**Domain-to-architecture isomorphism** — align the architecture with where the business is. Aggressive cost-cutting doesn't fit microservices or space-based (both expensive); aggressive M&A growth doesn't fit monolithic styles that can't evolve.

> **Known unknowns vs. unknown unknowns** — Donald Rumsfeld's distinction. *Known unknowns* are gaps you know exist; *unknown unknowns* are surprises no one anticipated. Big Design Up Front fails because it cannot design for unknown unknowns. *All architectures become iterative because of unknown unknowns. Agile just recognizes this and does it sooner.*

> **Residuality theory** (Barry O'Reilly, *Residues: Time, Change, and Uncertainty in Software Architecture*, Leanpub 2024) — treat business changes as **stressors** and architectural responses as **residues**. Accumulated residues eventually start to absorb unknown changes, pushing the architecture into a *critical state* from complexity theory. The architecture that has survived many stressors carries the residue of all of them, and that residue is what makes it resilient to the next.

### 5.9. Architecture and Generative AI

Incorporate Gen AI via **abstraction and modularity** — be able to swap one LLM for another, add guardrails (rails), and evaluate results (evals). Example: a job-search company uses an LLM to anonymize résumés (reducing bias); accuracy must be measurable across LLMs. Tools like *Langfuse* provide the observability.

**Gen AI as architect assistant — limited.** LLMs handle deterministic coding tasks well but rarely give the right answer to *"microservices or space-based?"* because everything in software architecture is a trade-off and LLMs lack the contextual *wisdom* required. See [Architectural Decisions → §8](practice/architectural-decisions.md#8-generative-ai-in-architectural-decisions) for the full position.

## 6. Parting Advice

**Practice is the only path.**

> *Great designers design.* — Fred Brooks

Ted Neward's corollary: *how do we get great architects when they only architect a half-dozen times in a career?* The answer is **architecture katas** — practice problems modeled on real systems that give architects the rep-volume their day job doesn't.

*Fundamentals'* authors once tried to keep student kata drawings as a reference repository but gave up: the drawings captured *how* but not *why*, and per Neal, *there are no right or wrong answers in architecture — only trade-offs.* The drawings without the trade-off discussions were exhibits without context.

> **Always learn, always practice, *go do some architecture*.**

That's the entire merged section in one sentence. Everything else — the trade-off matrices, the ADRs, the diagrams, the risk-storming sessions, the four Cs, the nine intersections — is in service of doing the work.

## Sources

- [Fundamentals Ch 26: Architectural Intersections](software/software-architecture/books/fundamentals-of-software-architecture/ch26_architectural_intersections.md) (primary — the nine intersections, Pets.com origin of elastic scale, residuality theory, Gen AI alignment)
- [Fundamentals Ch 27: The Laws of Software Architecture, Revisited](software/software-architecture/books/fundamentals-of-software-architecture/ch27_laws_revisited.md) (primary — the three laws restated, shared-library/shared-service and queue/topic trade-off tallies, Out-of-Context antipattern, parting advice and katas)


<!-- prev-next-nav -->

---

← [Negotiation and Leadership](software/software-architecture/practice/negotiation-and-leadership.md) | [Cheat Sheet](software/software-architecture/cheat-sheet.md) →
