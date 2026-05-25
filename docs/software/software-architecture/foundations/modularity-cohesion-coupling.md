# Modularity, Cohesion, Coupling

> *Fundamentals* (Ch 3) gives the foundational vocabulary — modularity vs. granularity, cohesion levels, Yourdon and Constantine's afferent/efferent coupling, Martin's derived metrics, and Page-Jones connascence (re-popularized by Weirich). *The Hard Parts* (Ch 2, Ch 3) keeps the vocabulary and adds the missing axis: the formal split between **static** and **dynamic** coupling, and the three sub-axes of dynamic coupling (communication, consistency, coordination). The two books agree on everything in this chapter; *The Hard Parts* simply sharpens the coupling half of the picture.

## Table of Contents

- [1. Modularity vs. Granularity](#1-modularity-vs-granularity)
- [2. Cohesion](#2-cohesion)
- [3. Coupling — Static and Dynamic](#3-coupling--static-and-dynamic)
- [4. Martin's Metrics — Abstractness and Instability](#4-martins-metrics--abstractness-and-instability)
- [5. Distance from the Main Sequence](#5-distance-from-the-main-sequence)
- [6. Connascence](#6-connascence)
- [7. Page-Jones's Three Guidelines and Weirich's Two Rules](#7-page-joness-three-guidelines-and-weirichs-two-rules)
- [Sources](#sources)

## 1. Modularity vs. Granularity

*Fundamentals* opens with a distinction architects routinely confuse:

| Term | Meaning |
|---|---|
| **Modularity** | *Breaking a system apart* into smaller pieces (monolith → microservices, or just package decomposition). About logical separation. |
| **Granularity** | *The size of those pieces* — how big a service or component should be. |

> *"Embrace modularity, but beware of granularity."* — Mark Richards

Modularity is the **implicit** architecture characteristic — no requirements document asks for it, but every sustainable codebase needs it because, like physical systems, software tends toward entropy unless someone actively pushes back. Granularity is where things go wrong: the wrong-sized pieces produce the named antipatterns **Spaghetti Architecture**, **Distributed Monolith**, and the famous **Big Ball of Distributed Mud**. The cure is paying attention to coupling between services and components.

> *"95% of the words written about software architecture are spent extolling the benefits of 'modularity' and little, if anything, is said about how to achieve it."* — Glenford J. Myers

The granularity question — *how big should each service be?* — is the subject of `decomposition/service-granularity.md`, where *The Hard Parts* introduces the **disintegrators** and **integrators** that pull granularity toward equilibrium. For now, the relevant idea is that granularity is not a free parameter; it falls out of the architecture characteristics each piece must support.

## 2. Cohesion

**Cohesion** measures the extent to which a module's parts belong together. An ideally cohesive module cannot be split without forcing extra coupling between the resulting pieces.

> *"Attempting to divide a cohesive module would only result in increased coupling and decreased readability."* — Larry Constantine

The classical levels, best to worst:

| Level | Meaning |
|---|---|
| **Functional** | Every part is related; the module contains everything it needs to function. |
| **Sequential** | One module's output feeds the next module's input. |
| **Communicational** | Modules form a chain, each contributing to a shared output (add DB record → email notification). |
| **Procedural** | Modules must execute in a particular order. |
| **Temporal** | Related only by timing (e.g., startup initialization tasks). |
| **Logical** | Data is logically related but not functionally (Java's `StringUtils` static helpers). |
| **Coincidental** | Elements share only a source file — the worst form. |

Cohesion is **subjective**. *Fundamentals* uses the example of `get/cancel customer orders`: does it live in `Customer Maintenance` or split into `Order Maintenance`? It depends on growth expectations, the rest of the order behavior, and how much knowledge the split would force across the boundary.

**LCOM (Lack of Cohesion in Methods)**, from Chidamber & Kemerer, is the structural cohesion metric. Roughly: *the sum of sets of methods not shared via fields*. A class with private fields `a` and `b`, where most methods touch only one or the other, scores high LCOM — those field/method pairs could each become their own class. LCOM finds **structural** lack of cohesion, never **logical** lack: it is blind to whether the related-looking code actually belongs together. That blindness is a reminder of the Second Law — *why* matters more than *how*.

## 3. Coupling — Static and Dynamic

*Fundamentals* uses Yourdon and Constantine's classic pair from *Structured Design* (1979):

- **Afferent coupling (CA)** — *incoming* connections to a code artifact. Mnemonic: *a* before *e*, like *incoming* before *outgoing*.
- **Efferent coupling (CE)** — *outgoing* connections from the artifact to other artifacts. Mnemonic: *e* in *efferent* matches *e* in *exit*.

(The names are a mathematical artifact; the metrics should arguably have been called *incoming* and *outgoing*. Every major platform has tooling for both.)

*The Hard Parts* keeps these metrics but layers a second, architecturally critical distinction on top: **static** vs. **dynamic** coupling.

| Type | What it captures |
|---|---|
| **Static coupling** | How services and components are *wired together*. All the dependencies needed to *bootstrap* a quantum: OS, frameworks, transitive libraries, brokers, container orchestration, databases, even IP addresses and URLs. |
| **Dynamic coupling** | How services *call one another at runtime* to form workflows. Observable only when the system is running. |

The point of the split is that you cannot reason about runtime entanglement until you have separated it from wiring entanglement. *The Hard Parts* opens with a braid metaphor: you cannot study any one force until you have untangled it from the others. Static coupling is the wiring diagram you can draw before turning the system on; dynamic coupling is the temporary entanglement that appears when one service blocks on another mid-workflow.

**Dynamic coupling decomposes further** into three forces that interact:

| Sub-axis | Spectrum |
|---|---|
| **Communication** | synchronous (caller blocks) ↔ asynchronous (caller posts and continues). |
| **Consistency** | atomic (all-or-nothing) ↔ eventual (varying degrees). |
| **Coordination** | orchestrated (a dedicated coordinator) ↔ choreographed (services share coordination). |

The three forces cannot be chosen independently: atomicity is easier with synchronous + mediated; high scale requires asynchronous + eventually consistent + choreographed. Every binary combination of the three has a name and a coupling rating — Epic Saga, Phone Tag, Fairy Tale, Time Travel, Fantasy Fiction, Horror Story, Parallel, Anthology — but the eight sagas belong on a different page; see [Transactional Sagas](distributed/transactional-sagas.md) for the matrix.

**Coupling rule of thumb** *(Fundamentals)*: **higher coupling is allowed for narrower scopes; the broader the scope, the looser the coupling should be**. Inside one module, dense connascence is normal. Across module boundaries, the same density is a code smell. Across service boundaries, it is a distributed monolith.

## 4. Martin's Metrics — Abstractness and Instability

Robert C. Martin's derived metrics, applicable to most OO languages, both bounded in [0, 1]:

- **Abstractness (A)** — ratio of abstract artifacts (interfaces, abstract classes) to concrete ones. A 5,000-line `main()` method sits near 0; a tower of `AbstractSingletonProxyFactoryBean` sits near 1. Formula: `A = Σmᵃ / (Σmᶜ + Σmᵃ)`.
- **Instability (I)** — ratio of efferent coupling to total coupling: `I = Cᵉ / (Cᵉ + Cᵃ)`. Measures volatility: a class with many outgoing calls breaks easily when any callee changes.

Both can be measured automatically and trended over time; they feed the next metric.

## 5. Distance from the Main Sequence

> *"Distance from the Main Sequence" — D = A + I − 1.*

The metric is structural and holistic. The **main sequence** is the idealized line `A + I = 1` on the Abstractness-vs-Instability plane. Classes near the line are well balanced; classes far from it sit in one of two named zones.

| Zone | Where | Symptom |
|---|---|---|
| **Zone of Uselessness** | upper-right (high A, high I) | Too abstract to use; nobody can wire it up. |
| **Zone of Pain** | lower-left (low A, low I) | Too concrete and too coupled; brittle, hard to maintain. |

Distance is most useful for **codebase analysis**, **pre-migration scoping**, and **technical-debt assessment**. *The Hard Parts* uses it as part of the **feasibility check** before a decomposition — a codebase deep in the Zone of Pain is signaling that a pure decomposition will not deliver the agility characteristics being chased.

**Limit of structural metrics.** Even good metrics need interpretation. Cyclomatic Complexity cannot tell *essential* complexity (the problem is hard) from *accidental* complexity (the code made it harder than necessary). Establish baselines, apply judgment, and use metrics as conversation starters, not verdicts.

## 6. Connascence

Connascence is Meilir Page-Jones's vocabulary from *What Every Programmer Should Know about Object-Oriented Design* (1996), re-popularized by Jim Weirich. It is a **vocabulary for kinds of coupling**, not a metric.

> **Definition** — two components are *connascent* if changing one would force the other to change to keep the system correct.

Connascence splits into **static** (source-code coupling) and **dynamic** (runtime coupling) — the same top-level partition *The Hard Parts* lifts up to the architecture level for quanta.

### 6.1. Static Connascence

| Type | Meaning |
|---|---|
| **Connascence of Name** | Components must agree on the name of an entity. Most common, most desirable — IDEs rename safely. |
| **Connascence of Type** | Components must agree on the type of an entity (statically typed languages, plus opt-ins like Clojure Spec). |
| **Connascence of Meaning** (a.k.a. *Convention*) | Components must agree on what values mean. Classic case: hard-coded `int TRUE = 1; int FALSE = 0`. |
| **Connascence of Position** | Components must agree on order. `updateSeat("14D", "Ford, N")` is type-correct but semantically swapped. |
| **Connascence of Algorithm** | Components must agree on an algorithm — e.g., a security hash that must produce identical output on client and server. |

### 6.2. Dynamic Connascence

| Type | Meaning |
|---|---|
| **Connascence of Execution** | Order of execution matters (`email.send()` before `email.setSubject(...)` is broken). |
| **Connascence of Timing** | Race conditions between threads; timing matters. |
| **Connascence of Values** | Several values must change together (rectangle corners; transactions across distributed databases). |
| **Connascence of Identity** | Multiple components must reference the *same* entity — e.g., a shared distributed queue. |

### 6.3. Three Properties

| Property | What it asks |
|---|---|
| **Strength** | How hard is this coupling to refactor away? Prefer *static* (detectable by source analysis, easy to fix) over *dynamic*. Example refactor: turn a magic value (Meaning) into a named constant (Name). |
| **Locality** | How proximal are the coupled modules? Strong connascence inside the same module is fine; strong connascence across module boundaries is a code smell. DDD's **bounded context** encodes the same insight — limit implementation coupling to a narrow scope. |
| **Degree** | How many classes/modules does the change ripple through? Small degree of strong connascence may be tolerable; degree grows as codebases grow. |

The point of learning the vocabulary is the same as the point of learning design patterns: precise, shared shorthand. *"Don't add a magic string in the middle of a method"* becomes *"You have Connascence of Meaning; refactor it to Connascence of Name."*

## 7. Page-Jones's Three Guidelines and Weirich's Two Rules

The reason connascence has prescriptive power is that it converges to five short rules.

> **Page-Jones's three modularity guidelines** —
> 1. Minimize overall connascence by breaking the system into encapsulated elements.
> 2. Minimize remaining connascence that crosses encapsulation boundaries.
> 3. Maximize connascence within encapsulation boundaries.

> **Jim Weirich's two rules** —
> - **Rule of Degree** — convert strong forms of connascence into weaker ones.
> - **Rule of Locality** — as distance between elements increases, use weaker forms of connascence.

Together, the five rules collapse to a single instruction: **keep strong coupling close, weaken it as it spreads, and stop it at boundaries you mean to keep.** That instruction is the operational heart of every decomposition pattern *The Hard Parts* introduces later — see [Components and Quantum](foundations/components-and-quantum.md) for how it constrains service boundaries, and the upcoming `decomposition/when-to-decompose.md` for how it constrains modularity-driven decompositions.

## Sources

- [Fundamentals Ch 3: Modularity](software/software-architecture/books/fundamentals-of-software-architecture/ch03_modularity.md) (primary — cohesion levels, Martin's metrics, main sequence, connascence, Page-Jones, Weirich)
- [The Hard Parts Ch 2: Discerning Coupling](software/software-architecture/books/software-architecture-the-hard-parts/ch02_discerning_coupling.md) (static vs. dynamic coupling, the three dynamic sub-axes)
- [The Hard Parts Ch 3: Architectural Modularity](software/software-architecture/books/software-architecture-the-hard-parts/ch03_architectural_modularity.md) (the coupling rule of thumb in the context of the five modularity drivers)


<!-- prev-next-nav -->

---

← [Architectural Thinking](software/software-architecture/foundations/architectural-thinking.md) | [Architecture Characteristics](software/software-architecture/foundations/architecture-characteristics.md) →
