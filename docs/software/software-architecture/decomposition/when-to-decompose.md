# When to Decompose

> *The Hard Parts* Ch 3 (Architectural Modularity) supplies the *why* — the **modularity drivers** and the **five characteristics** that decomposition is supposed to improve. Ch 4 (Architectural Decomposition) supplies the prior question — *is the codebase decomposable at all?* — and the coupling-metric **feasibility check** that answers it. *Fundamentals* doesn't argue with any of this; it treats decomposition as a per-style detail rather than a topic of its own, so this page is *The Hard Parts*' material with one cross-link to the modularity vocabulary that *Fundamentals* established.

## Table of Contents

- [1. Don't Decompose Without a Driver](#1-dont-decompose-without-a-driver)
- [2. The Five Characteristics Decomposition Can Improve](#2-the-five-characteristics-decomposition-can-improve)
- [3. The Water-Glass Analogy](#3-the-water-glass-analogy)
- [4. Modularity Is Not Distribution](#4-modularity-is-not-distribution)
- [5. Scalability vs. Elasticity](#5-scalability-vs-elasticity)
- [6. Feasibility Check Before Decomposing](#6-feasibility-check-before-decomposing)
- [7. Sysops Squad — Building the Business Case](#7-sysops-squad--building-the-business-case)
- [Sources](#sources)

## 1. Don't Decompose Without a Driver

The most common decomposition mistake is starting one for the wrong reason. "Microservices are the modern style" and "everyone else has moved off the monolith" are not drivers; they are fashion. *The Hard Parts* names exactly two **modularity drivers** that justify the cost of breaking an application apart:

| Driver | What it buys |
|---|---|
| **Speed-to-market** (a.k.a. time-to-market) | The compound architecture characteristic called *agility*, made up of **maintainability + testability + deployability**. |
| **Competitive advantage** | Speed-to-market *plus* **scalability** *plus* **availability / fault tolerance** — the four characteristics together. |

Both drivers are *business*-shaped, which matters: if no stakeholder can name which driver justifies the work, the decomposition is being run on architect enthusiasm rather than business value, and it will lose funding the first time it slips. The Sysops Squad team in *The Hard Parts* spends most of Ch 3 not designing services but building the **business case** — mapping each business complaint (changes break unrelated things; tests are mostly commented out; releases are monthly and risky; reporting crashes ticketing; system freezes above 25 concurrent users) onto a driver and recording the result as the migration ADR.

> *"Embrace modularity, but beware of granularity."* — Mark Richards

Once the driver is named, the architecture characteristics it implies are the forces the rest of the decomposition is optimized against. See [Modularity, Cohesion, Coupling](foundations/modularity-cohesion-coupling.md) for the underlying vocabulary, and [Trade-Off Analysis](foundations/tradeoff-analysis.md) for how the forces become a matrix.

## 2. The Five Characteristics Decomposition Can Improve

The two drivers expand into five concrete characteristics. Every decomposition decision should improve at least one of them; if it doesn't, it's structure-for-its-own-sake.

### 2.1. Maintainability

Ease of adding, changing, or removing features and applying internal upgrades (patches, framework bumps, third-party version bumps). The Von Zitzewitz metric `ML = 100 × Σcᵢ` over `k` logical components, weighted toward incoming coupling, makes it measurable: high afferent coupling drives low maintainability. Layered monoliths score badly because **technical partitioning** spreads any one domain across all layers — adding an expiration date to a wish-list item drags in a UI engineer, a backend engineer, and a DBA. A service-based architecture cuts the change scope to *domain level*; microservices cut it to *function level*.

### 2.2. Testability

Ease *and* completeness of automated testing. In a monolith, even a one-line change runs thousands of tests, most unrelated to the change. Decomposition shrinks per-service test scope — until the services start talking to each other, at which point a change to A drags B and C back into regression. Communication erodes the testability benefit, which is one of the integrators in [Service Granularity](decomposition/service-granularity.md).

### 2.3. Deployability

The compound of *ease of deployment*, *frequency of deployment*, and *risk of deployment*. Agility requires all three. Monoliths impose ceremony — code freezes, mock deployments, weeks between releases — which piles unrelated changes into one risky deploy. Distribution helps only if the services can deploy independently; if they must ship as a set in a specific order, you have produced a **big ball of distributed mud**, in Matt Stine's phrase: *if your microservices must be deployed as a complete set in a specific order, please put them back in a monolith and save yourself some pain.*

### 2.4. Scalability

Ability to remain responsive as user load *gradually* grows. A function of **modularity** — the number of separately deployable units. A monolith scales at application granularity; a service-based architecture scales at domain granularity; microservices scale at function granularity.

### 2.5. Availability / Fault Tolerance

The ability for some parts of the system to remain responsive while other parts fail (search and order placement keep working when payment processing dies). Load-balancing multiple monolith instances doesn't help, because a programming-bug fault exists in every instance. Decomposition isolates failure into separate deployment units — *unless* the surviving services are **synchronously** dependent on the failed one, in which case the failure cascades and fault tolerance is lost. Asynchronous communication is the actual mechanism; modularity is the prerequisite.

## 3. The Water-Glass Analogy

The standard executive-friendly justification: a monolith is a single glass filling up with users. Buying a second glass doesn't help, because the second glass would just hold the same application — same total capacity, just spread across two pieces of hardware. Splitting the application across two glasses gives 50% more capacity per glass; splitting it across ten gives ten times the capacity. *The Hard Parts* recommends this analogy specifically when the audience is non-technical: it converts a structural argument into a volume argument any sponsor can see.

## 4. Modularity Is Not Distribution

A consequential corollary: modularity is the goal, distribution is one *implementation* of it. Maintainability, testability, and deployability can also be achieved without breaking the application into separately deployed services.

- **Modular monolith** — domain-partitioned components inside a single deployment unit. The package structure encodes the domain seams; the application still deploys as one artifact. Gives most of the maintainability and testability gains at none of the distributed-system cost.
- **Microkernel architecture** — a core with **plug-in components**. Gives extensibility and deployability for the plug-ins without distribution.

Distribution is a means, not an end. Picking it when a modular monolith would do is overpaying for fault tolerance and scalability you don't actually need; picking a modular monolith when scalability and fault tolerance are first-class drivers is underpaying and shipping a system that can't meet the load. The driver decides which form modularity should take.

## 5. Scalability vs. Elasticity

The five characteristics include scalability but not elasticity, because the two are different and the architecture decisions for each differ.

| | Scalability | Elasticity |
|---|---|---|
| **Load shape** | Gradual growth over time | Instantaneous spikes |
| **Architectural lever** | Modularity — number of deployment units | Granularity — size of each unit |
| **Hard dependency** | Per-unit performance | **Mean Time To Startup (MTTS)** — how fast a new instance can come online |

The concert-ticketing example from *The Hard Parts*: a system goes from 20 to 3,000 concurrent users in seconds when tickets go on sale. Coarse-grained services can't spin up new instances fast enough; only fine-grained services with very low MTTS can. Scalability is a function of *modularity*; elasticity is a function of *granularity*. A layered monolith scores poorly on both (application-level scalability, poor MTTS); a service-based architecture is fair on scalability and limited on elasticity (domain-level, fair MTTS); microservices maximize both (function-level scalability, excellent MTTS).

Synchronous communication degrades both metrics as services get chattier, which is why the granularity integrators in [Service Granularity](decomposition/service-granularity.md) push back against over-decomposing.

## 6. Feasibility Check Before Decomposing

Before any decomposition pattern runs, the prior question: *can this codebase be decomposed at all?* Two failure modes invalidate the work before it starts.

### 6.1. Big Ball of Mud — No Internal Structure to Pull Apart

> **Big Ball of Mud antipattern** (Brian Foote, 1999) — a system with no internal structure: event handlers wired directly to database calls, no layering, no namespacing, no architecture.

Architects don't write patterns for these because *architecture is internal structure* — there is nothing to refactor along. A Big Ball of Mud doesn't decompose component-wise; it either gets rewritten or it gets **tactically forked** (see [Tactical vs. Strategic](decomposition/tactical-vs-strategic.md)).

### 6.2. Coupling Metrics on the Main Sequence

For codebases that *do* have structure, the feasibility check uses Robert Martin's derived metrics on Yourdon and Constantine's coupling pair.

| Metric | Formula | Meaning |
|---|---|---|
| **Afferent (CA)** | incoming connections | How many other artifacts depend on this one — its blast radius if changed. |
| **Efferent (CE)** | outgoing connections | How many other artifacts this one depends on — its breakability when others change. |
| **Abstractness (A)** | `Σmᵃ / (Σmᶜ + Σmᵃ)` | Ratio of abstract artifacts to concrete ones. |
| **Instability (I)** | `Cᴱ / (Cᴱ + Cᴬ)` | Outgoing-coupling share — volatility. |
| **Distance from Main Sequence (D)** | `|A + I − 1|` | How far a component sits from the idealized line `A + I = 1`. |

Plot the application's components on the abstractness/instability plane. Components near the **main sequence** are well balanced; components far from it sit in one of two named zones:

| Zone | Where | Symptom |
|---|---|---|
| **Zone of Uselessness** | high A, high I | Too abstract to be used; nobody can wire it up. |
| **Zone of Pain** | low A, low I | Too concrete and too coupled; brittle, hard to maintain. |

If many components fall into either zone, restructuring the internals first may not be worth it — the codebase is signaling that a pure decomposition will not deliver the agility characteristics being chased. Addison's Sysops Squad check finds most components near the line with only a few outliers, so decomposition is judged feasible and proceeds.

JDepend (visualized in Eclipse) is the worked example for measuring all four metrics on JVM code; equivalents exist on every major platform. Treat the metrics as a *conversation starter*, not a verdict — Cyclomatic Complexity famously can't distinguish *essential* from *accidental* complexity, and these coupling metrics likewise need an architect's interpretation.

## 7. Sysops Squad — Building the Business Case

Hard Parts works the Sysops Squad scenario to show what *naming the driver* looks like in practice. The application is a monolithic ticketing system that's been showing pain across multiple dimensions; Addison and Austen build the case for migration by mapping each business complaint onto a modularity driver, then recording the result as the migration ADR.

| Business complaint | Driver invoked |
|---|---|
| Changes break unrelated things; codebase too large to navigate | Maintainability |
| 30% of tests commented out; full suite must run for any change | Testability |
| Monthly releases bundle untested changes; high deploy risk | Deployability |
| Survey and reporting features keep crashing the whole system | Availability / fault tolerance |
| System freezes with >25 concurrent ticketers and during report runs | Scalability + database load |

> **ADR — Migrate Sysops Squad Application to a Distributed Architecture.**
> *Decision*: migrate to a distributed architecture to (a) make core ticketing more available via fault tolerance, (b) provide scalability for ticket creation, (c) split reporting load off the database, (d) raise team agility, (e) reduce defects through better testability, (f) deploy weekly/daily.
> *Consequences*: feature work delays during migration; additional cost; release engineers must manage multiple deployable units; the monolithic database must eventually be broken apart (see [Data Decomposition](decomposition/data-decomposition.md)).

Two things to notice about this ADR. First, every justification is named after a *characteristic* — not after a *style*. The decision does not commit to microservices yet; it commits to a distributed architecture motivated by specific characteristics, with style selection left for later (see [Tactical vs. Strategic](decomposition/tactical-vs-strategic.md)). Second, the consequences section is honest about the cost — migration is expensive, and pretending otherwise is what turns sponsors against the project at the first slip.

---

If the codebase is feasible — neither a Big Ball of Mud nor stuck in the Zone of Pain — and the modularity driver is real, the next decision is *how* to decompose. Pick the approach in [Tactical vs. Strategic](decomposition/tactical-vs-strategic.md); the structured path is detailed in [Component-Based Decomposition](decomposition/component-based-decomposition.md); the data half is covered in [Data Decomposition](decomposition/data-decomposition.md).

## Sources

- [The Hard Parts Ch 3: Architectural Modularity](software/software-architecture/books/software-architecture-the-hard-parts/ch03_architectural_modularity.md) (primary — modularity drivers, five characteristics, water-glass analogy, scalability vs. elasticity, modular monolith / microkernel alternatives)
- [The Hard Parts Ch 4: Architectural Decomposition](software/software-architecture/books/software-architecture-the-hard-parts/ch04_architectural_decomposition.md) (primary for the feasibility check — Big Ball of Mud, afferent/efferent coupling, abstractness/instability, distance from the main sequence)


<!-- prev-next-nav -->

---

← [Microservices](software/software-architecture/styles/microservices.md) | [Component-Based Decomposition](software/software-architecture/decomposition/component-based-decomposition.md) →
