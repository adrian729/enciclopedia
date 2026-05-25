# Summary

> A 15–30 minute narrative crash-course on the Software Architecture section. It distills the merged synthesis of *Fundamentals of Software Architecture* (Richards & Ford) and *Software Architecture: The Hard Parts* (Ford, Richards, Sadalage, Dehghani) into the essential mental model — the role, the three laws, the coupling vocabulary, the nine-style landscape, the decomposition machinery, the saga catalog, and the soft-skills of the architect. This is not a reference cheat-sheet (see the [Cheat Sheet](software/software-architecture/cheat-sheet.md) for that) and it is not a replacement for the merged pages — it is the section's story arc at higher altitude, intended for a first read, a refresh, or a top-down overview.

## Table of Contents

- [1. What an Architect Is and What They Do](#1-what-an-architect-is-and-what-they-do)
- [2. The Three Laws](#2-the-three-laws)
- [3. The Vocabulary of Trade-Off Analysis](#3-the-vocabulary-of-trade-off-analysis)
- [4. The Nine-Style Landscape](#4-the-nine-style-landscape)
- [5. Decomposition — Pulling a Monolith Apart](#5-decomposition--pulling-a-monolith-apart)
- [6. Distributed Concerns — Data, Workflows, Sagas](#6-distributed-concerns--data-workflows-sagas)
- [7. The Architect's Artifacts and Soft Skills](#7-the-architects-artifacts-and-soft-skills)
- [8. Where to Go Next](#8-where-to-go-next)
- [Sources](#sources)

## 1. What an Architect Is and What They Do

*Fundamentals* opens by admitting the discipline has no industry-standard definition and offers a working one with four dimensions: an architecture is a **style** (overall topology), a set of **architecture characteristics** (the -ilities the system must support well), a set of **logical components** (the behavior expressed as domains, entities, workflows), and the **architecture decisions** (the constraints justifying the other three). The four dimensions are an analytical tool, not a sequence — an architect cycles among them whenever a new constraint arrives, and each decision is justified by trade-offs across the others. Michael Nygard's test for whether a particular call counts is whether it touches structure, non-functional characteristics, dependencies, interfaces, or construction techniques; if it does, it is architectural and deserves an ADR.

Architecture lives on a spectrum with design. Three criteria place a decision on the spectrum: whether it is **strategic vs. tactical**, whether the **level of effort** to change is high or low, and whether the **trade-offs are significant**. Martin Fowler's pithy form — *"architecture is the stuff that's hard to change"* — captures the level-of-effort axis; *The Hard Parts*' title puns on the same word, meaning both *difficult* and *solid/structural*. The Third Law's spectrum framing makes this a soft boundary rather than a hard one.

*Fundamentals* names **eight expectations** of an architect (*The Hard Parts* threads the same themes through its narrative but doesn't enumerate them): make architecture decisions (guide rather than specify); continually analyze the architecture for vitality and structural decay; keep current with trends; ensure compliance with the decisions (preferably via automated fitness functions); understand diverse technologies; know the business domain; possess interpersonal skills; and navigate organizational politics. Every architect call gets challenged; politics is half the job. The mindset is *technical breadth over depth* — knowing a little about a lot beats knowing one thing perfectly, because trade-off analysis rests on the breadth of options the architect can compare. A useful map of any architect's knowledge: *stuff you know*, *stuff you know you don't know*, *stuff you don't know you don't know*. The bottom tier is the biggest and most dangerous; the daily practice of promoting items upward is the architect's career.

The **20-Minute Rule** — twenty minutes a day spent learning something unfamiliar, *before* opening email — is the proposed habit; a personal technology radar (Tools / Languages & Frameworks / Techniques / Platforms × Hold / Assess / Trial / Adopt) is the suggested tool. Two named dysfunctions block the depth-to-breadth shift: trying to be expert at everything, and *stale expertise* — believing yesterday's information is still current. The third archetype to avoid is the **Frozen Caveman antipattern**: the architect who reverts to a pet irrational concern on every project (the team that asked *"but what if we lose Italy?"* after a single freak outage years ago). Distinguish genuine risk from perceived risk.

The architect must also stay hands-on. The recommended pattern: delegate critical-path code to the team and take on a minor business feature one to three iterations out. This avoids the **Bottleneck Trap** (architect owns blocking code part-time) while keeping the architect close to the codebase via POCs, technical-debt work, bug fixes, automation, fitness functions, and code reviews.

The cross-cutting message: the architect's real value is becoming the **objective arbiter of trade-offs** — not chasing silver bullets, not evangelizing, not dictating from on high. Analyze each decision's forces in its own context, record the *why* so the work survives successor architects.

## 2. The Three Laws

The section's spine is three universal observations Richards and Ford codified after looking for ten or fifteen and finding only three.

> **First Law** — Everything in software architecture is a trade-off.

> **Second Law** — *Why* is more important than *how*.

> **Third Law** — Most architecture decisions aren't binary but rather exist on a spectrum between extremes.

Each law produces a concrete operational move.

The **First Law** has two corollaries: (1) if you can't see the trade-off, you haven't identified it yet, and (2) you can't do trade-off analysis once and be done — every situation forces re-evaluation. *The Hard Parts* layers its own inverse claim on top: *the hard parts have no best practices* — entire classes of architecture problems have no general good solution, only one messy set of trade-offs against another. The replacement goal for "best design" is the **least worst combination of trade-offs**, the design where no characteristic is maximized but the balance promotes project success. The *Vasa* — the seventeenth-century Swedish warship that capsized because it tried to maximize every characteristic at once — is *Fundamentals*' cautionary tale for the urge to optimize everything.

The **Second Law** is the reason ADRs exist. Future architects can recover *how* by reading the code; *why* rots out of memory unless preserved. Diagrams capture *how* but not *why*. An experienced architect can read an unfamiliar system and explain how it works but rarely why a prior architect chose this option over another — because the criteria weren't recorded. Document with diagrams *and* ADRs.

The **Third Law** yields the operational test for what counts as architectural: *a decision is architectural when each option carries significant trade-offs*. If one option clearly dominates, it isn't architecture — it's design, and it shouldn't sit on the architect's plate. *The Hard Parts* uses this same test as its organizing principle: its fifteen chapters are organized around problems where each option has significant trade-offs and no single best practice wins.

The accumulated practical instruction: enumerate forces, never pretend an answer is universal, always preserve the *why*, and refuse to debate decisions whose options aren't comparable.

## 3. The Vocabulary of Trade-Off Analysis

Architects argue in a precise vocabulary. A reader of this section should leave knowing what these words mean and how they are used.

**Modularity vs. granularity.** *Modularity* is breaking a system apart — logical separation. *Granularity* is how big the resulting pieces are. Most distributed-system pain is granularity pain, not modularity pain. Mark Richards's catchphrase: *embrace modularity, but beware of granularity.*

**Cohesion** measures how strongly a module's parts belong together. The classical levels (best to worst): functional → sequential → communicational → procedural → temporal → logical → coincidental. Cohesion is subjective; LCOM (Lack of Cohesion in Methods) only finds *structural* lack of cohesion, never logical lack — a reminder of the Second Law (*why* matters more than *how*).

**Coupling** splits into static and dynamic — the most important contribution of *The Hard Parts* on this page. **Static coupling** is how services are *wired together* — all the dependencies needed to bootstrap a quantum (OS, frameworks, transitive libraries, brokers, container orchestration, databases, IP addresses, URLs). It is drawn as a *static quantum diagram* before the system runs. **Dynamic coupling** is how services *call one another at runtime* to form workflows; observable only when the system is running. The split matters because you cannot reason about runtime entanglement until you separate it from wiring entanglement.

Dynamic coupling decomposes into three sub-axes that cannot be chosen independently:

| Sub-axis | Spectrum |
| --- | --- |
| **Communication** | synchronous (caller blocks) ↔ asynchronous (caller posts and continues) |
| **Consistency** | atomic (all-or-nothing) ↔ eventual (varying degrees) |
| **Coordination** | orchestrated (a dedicated coordinator) ↔ choreographed (services share coordination) |

The three sub-axes are also written `s/a` × `a/e` × `o/c`, producing 2 × 2 × 2 = **eight named saga patterns** covered in §6.

**Connascence** (Page-Jones, re-popularized by Weirich) is the vocabulary for *kinds* of coupling. Two components are connascent if changing one would force the other to change to stay correct. Static forms (Name, Type, Meaning, Position, Algorithm) and dynamic forms (Execution, Timing, Values, Identity) are both classified. Weirich's two rules collapse the catalog to a single instruction: **Rule of Degree** — convert strong forms into weaker ones; **Rule of Locality** — as distance between elements grows, use weaker forms. Together with Page-Jones's three guidelines (minimize overall connascence, minimize what crosses boundaries, maximize what stays inside), the rules condense to: *keep strong coupling close, weaken it as it spreads, stop it at boundaries you mean to keep*.

**Architecture quantum** (also from *The Hard Parts*) is the foundational unit of a distributed architecture: an *independently deployable artifact with high functional cohesion, high static coupling, and synchronous dynamic coupling*. A microservices system has many quanta; a layered monolith has one. The quantum is what you count when answering "how many separately scalable, separately deployable parts does this system have?"

**Architecture characteristics** are the *-ilities* the system must support well — availability, scalability, performance, security, maintainability, testability, deployability, and dozens more. *Fundamentals* sorts them into operational, structural, cloud, and cross-cutting buckets, and qualifies a candidate as a characteristic when it is non-domain, influences structure, and is critical or important to success. *Limit the explicit list to a top three* — the *Vasa* rule again; ranking seven never produces consensus. Composite characteristics combine primitives — *agility* = deployability + modularity + testability.

**Fitness functions** are the governance tool: any objective mechanism that assesses a characteristic. ArchUnit and NetArchTest enforce layer rules; JDepend detects cycles; Cyclomatic Complexity stays below a threshold; Chaos Monkey tests resilience; CVE scans gate the security characteristic. Every ADR pairs naturally with a fitness function — the ADR records *what* and *why*; the fitness function automates that the decision still holds.

The meta-method that organizes all of this is *The Hard Parts*' **three-step trade-off analysis**: (1) find what parts are entangled (the static-coupling diagram); (2) analyze how they are coupled (a dimension matrix — rate each candidate in isolation against each force, then consolidate); (3) assess trade-offs by determining the impact of change. Fix the gating dimension first (e.g., sync vs. async), then iterate. Around this core sit five techniques worth knowing by name: **MECE** lists (Mutually Exclusive, Collectively Exhaustive — comparing comparable things); the **Out-of-Context Trap** (choosing the option that wins on generic criteria when narrower context would invert the decision); **modeling relevant domain cases** (don't decide in a vacuum); **bottom line over overwhelming evidence** (the matrix is the architect's tool, the bottom line is the stakeholder's); and **avoiding snake oil and evangelism** (force balanced assessments; never accept a binary debate without fitness functions). The three quotes that frame the discipline: *"architecture is the stuff you can't Google or ask an LLM about"* (Richards), *"there are no right or wrong answers in architecture — only trade-offs"* (Ford), and *"programmers know the benefits of everything and the trade-offs of nothing — architects need to understand both"* (Hickey).

## 4. The Nine-Style Landscape

A style is a *named topology* with assumed characteristics — both beneficial and detrimental. The naming gives architects a concise shorthand for a complex set of factors. *Fundamentals* catalogs nine; *The Hard Parts* assumes you already have them. Every style is described by the same five aspects: component topology, physical architecture, deployment, communication style, and data topology.

Before the catalog: top-level partitioning is either **technical** (presentation / business / services / persistence — the classic layered monolith) or **domain** (workflows like `CatalogCheckout` or `OrderFulfillment` — modular monolith, service-based, microservices). The industry trend is decisively domain partitioning, because it aligns with cross-functional teams and with later migration to distributed styles. Conway's Law and the **Inverse Conway Maneuver** make the team-shape decision deliberate; Skelton and Pais's **Team Topologies** vocabulary (stream-aligned / enabling / complicated-subsystem / platform) is the recommended team grammar.

The nine styles:

| Style | Type | Quanta | Best when |
| --- | --- | --- | --- |
| **Layered** | Monolith | 1 | Small app, tight budget, feasibility-driven. Beware the *Architecture Sinkhole*. |
| **Modular Monolith** | Monolith | 1 | DDD-aligned team, new system, mostly domain-based changes. |
| **Pipeline** | Monolith | 1 | Distinct, ordered, deterministic processing (Producer / Transformer / Tester / Consumer). |
| **Microkernel** | Monolith | 1 | Customization-heavy domains (per-state insurance, per-client packages). |
| **Service-Based** | Distributed | 1 (shared DB) | Pragmatic distributed (≤12 coarse services on one DB); ACID transactions still needed. |
| **Event-Driven** | Distributed | many | Fault tolerance, responsiveness, async workflows. Broker or mediator topology. |
| **Space-Based** | Distributed | many | High variable load — concert tickets, auctions, ticket sales. |
| **Orchestration-Driven SOA** | Distributed | 1 (ESB collapse) | A historical cautionary tale; modern integration use remains valid. |
| **Microservices** | Distributed | many | Share-nothing bounded contexts, independent deployability, polyglot persistence. |

Picking a style funnels through four prior inputs (domain, characteristics analysis, data architecture, organizational constraints) and three core determinations: **monolith vs. distributed** (one set of characteristics enough, or different parts need different sets?); **where does the data live** (monolithic DB vs. distributed ownership); **sync vs. async communication** (default to sync; use async only when necessary, because async buys performance and scale at the price of synchronization, deadlocks, races, and harder debugging). The output is a topology, a set of ADRs for the highest-effort decisions, and fitness functions to protect the principles.

The 1994 Sun **Fallacies of Distributed Computing** must be designed *against*, never assumed: the network is reliable; latency is zero; bandwidth is infinite; the network is secure; the topology never changes; there is only one administrator; transport cost is zero; the network is homogeneous. *Fundamentals* adds three more — versioning is easy; compensating updates always work; observability is optional. The fallacies are false beliefs; every distributed style must engineer against each one explicitly. The **Big Ball of Mud** (and its distributed cousin, the **Big Ball of Distributed Mud**) is the anti-style — what teams produce when they "just start coding" without choosing a style at all.

A few **architectural patterns** sit above the catalog and compose with any style: Hexagonal Architecture (Ports and Adapters), Sidecar / Service Mesh (orthogonal coupling for operational concerns), CQRS (separate read/write datastores), and the broker vs. mediator topology choice in event-driven systems. The eight saga patterns from *The Hard Parts* live in this plane too.

## 5. Decomposition — Pulling a Monolith Apart

Decomposition is *The Hard Parts*' deep-dive territory. The first question is whether to decompose at all.

**Don't decompose without a business driver.** Only two drivers justify the cost: **speed-to-market** (which compounds to maintainability + testability + deployability) and **competitive advantage** (speed-to-market + scalability + availability/fault tolerance). If no stakeholder can name the driver, the work is being run on architect enthusiasm and will lose funding the first time it slips. The **water-glass analogy** — a single monolith glass keeps overflowing; ten glasses give ten times the capacity — converts the structural argument into a volume argument any sponsor can see.

**Modularity is not distribution.** A modular monolith or microkernel can deliver maintainability/testability/deployability without distribution costs. Distribution is one *implementation* of modularity; pick it only when scalability and fault tolerance are genuine drivers. Scalability (gradual load growth) is a function of *modularity*; **elasticity** (instantaneous spikes — concert tickets, auctions) is a function of *granularity* and depends critically on **Mean Time To Startup (MTTS)** — how fast a new instance comes online. Microservices maximize both; layered monoliths score poorly on both.

**Feasibility check.** Before any decomposition, ask whether the codebase is decomposable at all. Two failure modes invalidate the work before it starts: a *Big Ball of Mud* with no internal structure to refactor along (rewrite or tactically fork instead); or a codebase plotted on the abstractness/instability plane that sits mostly in the **Zone of Pain** (low A, low I — too concrete and too coupled) or the **Zone of Uselessness** (high A, high I — too abstract to wire up). Robert Martin's Distance from the Main Sequence (D = |A + I − 1|) makes this measurable.

**Two approaches.** Once decomposition is justified and feasible, pick between **component-based decomposition** (preferred default — components are already discernible) and **tactical forking** (for chaotic, hard-to-extract codebases; fast but inner quality matches the monolith). Avoid the **Elephant Migration Anti-Pattern** — pulling out whatever feature seems easy without a holistic plan — because it produces a Big Ball of Distributed Mud.

*The Hard Parts*' **six refactoring patterns** are the structured path, applied in order:

| # | Pattern | Move |
| --- | --- | --- |
| 1 | **Identify and Size Components** | Catalog every component; resize outliers using *statements* as the metric. |
| 2 | **Gather Common Domain Components** | Consolidate duplicated domain logic (not infrastructure cross-cutters) into one shared component. |
| 3 | **Flatten Components** | Ensure source code lives only in leaf-node namespaces — no orphans in roots. |
| 4 | **Determine Component Dependencies** | Analyze cross-component coupling to predict the resulting service graph. CIO question: *golf ball / basketball / airliner*. |
| 5 | **Create Component Domains** | Group components into logical domains so coarse-grained services can be built. |
| 6 | **Create Domain Services** | Physically extract each component domain into a separately deployed service — typically a service-based architecture as the first stop. |

Each pattern ships with its own fitness function (e.g., *no component shall exceed 30% of the codebase*; *all components in `<some domain>` should start with the same namespace*). The sequence is non-negotiable: resizing must precede dependency analysis; domain identification must precede physical extraction. Service-based architecture is recommended as the *first stop* (rather than jumping straight to microservices) because it defers data decomposition, doesn't require operational automation, and exposes which domains genuinely *need* finer microservice granularity.

**Granularity is the harder problem.** Right-size services at the equilibrium of two opposing sets of forces. **Disintegrators** (push to split) are *service scope and function*, *code volatility*, *scalability and throughput*, *fault tolerance*, *security access*, and *extensibility*. **Integrators** (push to consolidate) are *database transactions*, *workflow and choreography*, *shared code*, and *data relationships*. The two sets pull in opposite directions, and right-sized services emerge from the equilibrium. The architect's job is to frame the trade-off as a single explicit question — *"better agility through volatility isolation, or stronger data integrity through ACID?"* — and let the business decide. The architect is a *facilitator* here, not a decider; the trade-offs being weighed are business-value trade-offs masquerading as technical ones.

Two failure modes bracket the granularity space: the **Distributed Monolith** (services that must deploy together — Matt Stine: *if your microservices must be deployed as a complete set in a specific order, please put them back in a monolith and save yourself some pain*) and the **Grains of Sand antipattern** (services so fine-grained that every business operation requires choreographing many of them). Both are *granularity* failures, not modularity failures. The cure for Grains of Sand is consolidation — apply the integrators until the equilibrium re-settles.

**Data decomposition** is the inverse half of the same problem: pulling apart the operational database that the six refactoring patterns deliberately deferred. It runs on its own five-step process and uses parallel data-disintegrator / data-integrator forces. The data decomposition typically lags the service decomposition by one stage, which is why service-based architecture (services split, single DB) sits between monolith and microservices in the migration path.

## 6. Distributed Concerns — Data, Workflows, Sagas

Once the services are separate, an entirely new class of problems appears. This is the territory where best practices fail and *The Hard Parts* lives.

**Data ownership.** Every table needs an answer to a simple question: *which service owns it?* The rule: **the service that performs writes is the owner.** Three scenarios in resolution order: **Single Owner** (exactly one writer — unambiguous); **Common Owner** (most or all services write, e.g., an Audit table — dedicate one owner service and route writes to it via async fire-and-forget or request-reply); **Joint Owner** (a few services in one domain — Catalog and Inventory both write the Product table). Joint Ownership is resolved by one of four techniques: **Table Split** (split the table per *Refactoring Databases*); **Data Domain** (shared schema with multiple owners — widens the bounded context); **Delegate** (one service becomes sole owner; the other calls it to perform writes — the default, with the primary-domain-priority variant preferred); or **Service Consolidation** (merge the joint owners — the honesty check when the services share data, domain, scalability, and volatility profile).

**ACID stops at the service boundary.** Inside one service, ACID holds. Across services, every property breaks: no single commit straddles boundaries; foreign-key constraints can't enforce cross-service consistency; partial workflows are visible through intermediate state; durability covers individual commits, not workflows. The replacement is **BASE** — *Basically Available, Soft state, Eventually consistent*. BASE is not a bug; it is the price of decomposition. Three patterns achieve eventual convergence: **Background Synchronization** (a batch job — services decoupled but data sources coupled; *breaks bounded contexts* and should not be the long-term answer); **Orchestrated Request-Based** (the saga family); and **Event-Based** (pub/sub or stream — usually the strongest fit).

**Orchestration vs. choreography.** Workflows in distributed systems are coordinated either by a dedicated **orchestrator** (one service holds the workflow state) or by **choreography** (services react to each other's events with no central coordinator). The trade-offs are symmetric: orchestration is easier to reason about and observe, but creates a hot spot; choreography is scalable and resilient, but distributes the workflow logic across services that must know about each other. *The Hard Parts*' lemma: **semantic coupling can only be increased by implementation, never decreased** — workflow logic has to live somewhere, and choosing choreography over orchestration just relocates it.

**The eight saga patterns.** The dynamic-coupling cube from §3 (`s/a` × `a/e` × `o/c`) produces 2 × 2 × 2 = 8 named patterns, one per combination of communication × consistency × coordination. This is the section's most-cited framework:

| Pattern | Code | Coupling | When |
| --- | --- | --- | --- |
| **Epic Saga** | `(sao)` | Very high | Atomicity non-negotiable; mimics the monolith via compensating transactions. |
| **Phone Tag Saga** | `(sac)` | High | Front-controller flows; first service acts as controller. |
| **Fairy Tale Saga** | `(seo)` | High | **Balanced default.** Each service owns its own transaction; orchestrator coordinates without holding one open. |
| **Time Travel Saga** | `(sec)` | Medium | Pipes-and-filters throughput; great fire-and-forget. |
| **Fantasy Fiction Saga** | `(aao)` | High | Mediator tracks many async in-flight transactions; race conditions common. Avoid. |
| **Horror Story** | `(aac)` | Medium | Atomicity with the two loosest coupling styles. Aptly named anti-pattern. |
| **Parallel Saga** | `(aeo)` | Low | **Balanced default.** Complex, high-scale workflows; mediator coordinates compensations asynchronously. |
| **Anthology Saga** | `(aec)` | Very low | Simple, mostly linear, high-throughput pipelines. |

**Defaults.** Reach for *Fairy Tale (seo)* or *Parallel (aeo)* when no single force dominates. Use *Anthology (aec)* for simple linear pipelines. Reserve *Epic (sao)* for cases where atomicity is genuinely non-negotiable — most workflows that *feel* like they need Epic actually fit Fairy Tale or Parallel once the team accepts eventual consistency.

**State management beats compensating updates.** Saga state can be managed by **compensating updates** (reverse the prior writes) or by a **finite state machine** (record the saga's current state; correct errors via retries and escalation rather than rollback). Compensating updates have five recurring failure modes: lack of transaction isolation, compensation failures, poor responsiveness, semantic over-coupling, and the rollback-failures-plus-locking dilemma. FSMs accept soft state during the workflow and converge in the background; the user is decoupled from background failures they can't fix. Prefer FSM unless atomicity is mandatory. Either way: **the state of the distributed transaction must be known and managed.**

**Contracts** between services run on a strict-to-loose spectrum: **strict** (RMI, gRPC, schema-validated JSON — type safety, no ambiguity); **middle** (REST, GraphQL — resource modeling absorbs additions); **loose** (bare name/value JSON or YAML — maximum decoupling, requires *consumer-driven contracts* for fidelity). The named anti-pattern is **stamp coupling** — passing a 500 KB payload to satisfy a 200-byte need, legitimate only when scalability forces choreography and the payload carries workflow state.

**Reuse without coupling.** The four reuse patterns: **Code Replication** (static one-off code only — no versioning); **Shared Library** (most common; compile-time bind — always version, never `LATEST`); **Shared Service** (polyglot or volatile shared logic — pays in latency and lockstep scaling); **Sidecar / Service Mesh** (operational concerns only — never for domain code). Reuse needs both *abstraction* and *slow rate of change*; the **Centralized Customer Service** anti-pattern is what happens when a domain entity gets shared. Microservices guidance: **duplication is preferable to coupling**.

**Analytical data and Data Mesh.** The operational/analytical split has gone through three generations. The **Data Warehouse** centralizes data via ETL into a Star Schema and suffers from integration brittleness, technical partitioning, contract brittleness, and synchronization bottlenecks. The **Data Lake** inverts to load-then-transform but keeps centralization, doesn't help discovery, raises PII risk, and is still technically partitioned. **Data Mesh** (Dehghani) decentralizes — four principles: domain ownership of data, data as a product, self-serve data platform, and computational federated governance. The architectural unit is the **Data Product Quantum (DPQ)** — code-plus-data adjacent to a service, operationally independent but contract-coupled to it. Three DPQ types: source-aligned (native), aggregate, fit-for-purpose. The DPQ is a **Cooperative Quantum** — operationally separate, async + eventually consistent, tightly contract-coupled to its cooperator service but loosely contract-coupled to the analytics quantum. Dynamic-coupling constraint: a DPQ must use Parallel(aeo) or Anthology(aec) — never a transactional sync between operational and analytical data.

## 7. The Architect's Artifacts and Soft Skills

*Fundamentals* names the architect's durable artifacts as diagrams, ADRs, risk assessments, and fitness functions, and dedicates three chapters to the soft skills around them. *The Hard Parts* threads ADRs and fitness functions through every chapter but doesn't enumerate risk storming or the soft-skills curriculum — those are *Fundamentals*-only contributions.

**Architectural Decision Records.** A short text file (one to two pages) — Title, Status, Context, Decision, Consequences, plus the strongly-recommended Compliance and Notes. The Decision section uses an **affirmative, commanding voice** — *"We will use asynchronous messaging between services"* — never hedge-language. The emphasis is on *why*: *how* is recoverable from code; *why* is not. RFC status with a deadline lets architects circulate a draft before deciding; superseded ADRs cross-link by number so the chain survives. Three antipatterns ADRs cure, each exposed by the previous fix:

| Antipattern | Failure mode | Cure |
| --- | --- | --- |
| **Covering Your Assets** | Architect defers the decision out of fear of being wrong. | Decide at the *last responsible moment* — the point where deferral costs more than choosing. |
| **Groundhog Day** | People don't know *why*, so they keep relitigating. | Provide *technical and business* justification (cost / time-to-market / user satisfaction / strategic positioning). |
| **Email-Driven Architecture** | Decisions live in inboxes; nobody can find them. | One system of record; email links to it. |

The architect's stance on LLMs in architectural decisions: LLMs predict probable answers and reference "best practices" — neither belongs in architecture. *Generative AI has knowledge but lacks the wisdom required to make the most appropriate architectural decision.* Use LLMs to outline possible trade-offs you might have missed; not as decision-makers.

**Fitness functions** automate the verification that an ADR's decision still holds. ArchUnit (Java), NetArchTest (.NET), PyTestArch (Python), TSArch (TypeScript) cover the structural checks; CVE scans cover security; cyclomatic complexity thresholds cover maintainability; Chaos Monkey covers fault tolerance. *The Hard Parts* threads the ADR-plus-fitness-function pairing through every chapter — every decomposition pattern, reuse pattern, ownership scenario, and saga choice closes with an ADR and a corresponding fitness function. The pairing converts opinion into automated check.

**Risk storming** is *Fundamentals*' collaborative risk-assessment technique. Architects, developers, and stakeholders independently rate areas of the architecture on a risk matrix (impact × likelihood, scored 1–9), then converge to discuss the deltas. The exercise's value comes from the *deltas* — one participant's high rating that nobody else flagged exposes a risk that single-architect analysis would have missed. Two firm rules: it is collaborative, not consensus-driven, and ratings are individual until consolidation.

**Diagramming.** Use UML (class, sequence), C4 (Context / Container / Component / Class), or ArchiMate — the emerging standards. Convention: **solid lines for synchronous, dotted lines for asynchronous** is near-universal. Use multiple views for representational consistency; show the overview before the drill-down. Pair color with iconography and always include a key. The **Irrational Artifact Attachment** anti-pattern — over-investing in low-fidelity early artifacts (whiteboards, sticky notes) — warns against treating throwaway sketches as commitments.

**The 4 Cs of architecture leadership** (not to be confused with the C4 Model): **Communication, Collaboration, Clear, Concise**. ADRs preserve *why* in writing; the 4 Cs preserve *why* in conversation. The architect's job in stakeholder communication is to translate buzzwords into numbers (*"five nines"* becomes *"86 seconds of downtime per day"*) and to demonstrate over discuss. The **Ivory Tower antipattern** is the architect who dictates from on high without justification, ignoring developer opinions — the team loses respect, dynamics break down, and the architect ends up arguing each decision from scratch. The cure is the same as the cure for Groundhog Day: justify in business terms, record the *why*, govern with fitness functions.

The closing-chapter additions from *Fundamentals*: architecture must align across **nine intersections** — implementation, infrastructure, data topologies, engineering practices, team topologies, systems integration, the enterprise, the business environment, and generative AI. Misalignment kills systems that look architecturally sound. The 80,000-user microservices crash (the in-memory replicated cache between Order Placement and Inventory that exhausted VM memory under load) is the canonical illustration: architecture optimized for scalability and elasticity, implementation optimized for responsiveness and decoupling, both locally correct, the misalignment fatal.

**Residuality theory** (Barry O'Reilly, 2024) is *Fundamentals*' newest framing: treat business changes as **stressors** and architectural responses as **residues**; accumulated residues push the architecture into a *critical state* from complexity theory, and the residue of every survived stressor is what makes the architecture resilient to the next unknown unknown. *All architectures become iterative because of unknown unknowns; Agile just recognizes this and does it sooner.*

The parting advice from both books, paraphrased: *practice is the only path*. The artifacts, matrices, ADRs, diagrams, risk-storming sessions, the 4 Cs, the nine intersections — all are in service of doing the work. *Great designers design.* *Always learn, always practice, go do some architecture.*

## 8. Where to Go Next

This summary is the top-down read. For depth, walk the merged section in order:

- New to the discipline: read [Foundations](software/software-architecture/foundations/architectural-thinking.md) end-to-end, then skim [Styles → Overview](software/software-architecture/styles/overview.md) for the catalog map.
- Decomposing a monolith: start with [When to Decompose](software/software-architecture/decomposition/when-to-decompose.md), then walk through [Component-Based Decomposition](software/software-architecture/decomposition/component-based-decomposition.md), [Service Granularity](software/software-architecture/decomposition/service-granularity.md), [Data Decomposition](software/software-architecture/decomposition/data-decomposition.md), and the distributed pages.
- Designing a new service boundary: read [Foundations → Components and Quantum](software/software-architecture/foundations/components-and-quantum.md) and [Service Granularity](software/software-architecture/decomposition/service-granularity.md) together.
- Picking a style: [Styles → Overview](software/software-architecture/styles/overview.md) first, then the individual style pages.
- Documenting a decision: [Architectural Decisions](software/software-architecture/practice/architectural-decisions.md).
- Day-of review: the [Cheat Sheet](software/software-architecture/cheat-sheet.md).

The two books behind the merged section diverge by design. *Fundamentals* gives the **landscape and the role** — the catalog, the soft skills, the framing of the discipline as trade-off analysis. *The Hard Parts* gives the **machinery** — precise vocabulary (static/dynamic coupling, quantum, granularity equilibrium, joint ownership, BASE, the eight sagas, the Data Product Quantum) for the problems where the landscape leaves off. The 8-saga matrix, the granularity disintegrators/integrators, the joint-ownership resolutions, and the Data Mesh formalism are *Hard Parts* contributions; the 9-style catalog, the eight expectations, residuality theory, the nine intersections, and the soft-skills chapters are *Fundamentals* contributions. Where they overlap (modularity, coupling, characteristics, quantum, the First Law, ADRs), the merged section already unifies them; this summary follows the same convention.

## Sources

- [Software Architecture — Section Index](software/software-architecture/README.md)
- [Cheat Sheet](software/software-architecture/cheat-sheet.md)
- [Foundations → Architectural Thinking](software/software-architecture/foundations/architectural-thinking.md)
- [Foundations → Modularity, Cohesion, Coupling](software/software-architecture/foundations/modularity-cohesion-coupling.md)
- [Foundations → Architecture Characteristics](software/software-architecture/foundations/architecture-characteristics.md)
- [Foundations → Components and Quantum](software/software-architecture/foundations/components-and-quantum.md)
- [Foundations → Trade-Off Analysis](software/software-architecture/foundations/tradeoff-analysis.md)
- [Styles → Overview](software/software-architecture/styles/overview.md)
- [Decomposition → When to Decompose](software/software-architecture/decomposition/when-to-decompose.md)
- [Decomposition → Component-Based Decomposition](software/software-architecture/decomposition/component-based-decomposition.md)
- [Decomposition → Tactical vs. Strategic](software/software-architecture/decomposition/tactical-vs-strategic.md)
- [Decomposition → Service Granularity](software/software-architecture/decomposition/service-granularity.md)
- [Decomposition → Data Decomposition](software/software-architecture/decomposition/data-decomposition.md)
- [Distributed → Data Ownership](software/software-architecture/distributed/data-ownership.md)
- [Distributed → Distributed Data Access](software/software-architecture/distributed/distributed-data-access.md)
- [Distributed → Workflows & Orchestration](software/software-architecture/distributed/workflows-orchestration.md)
- [Distributed → Transactional Sagas](software/software-architecture/distributed/transactional-sagas.md)
- [Distributed → Contracts](software/software-architecture/distributed/contracts.md)
- [Distributed → Analytical Data & Data Mesh](software/software-architecture/distributed/analytical-data-and-mesh.md)
- [Practice → Architectural Decisions](software/software-architecture/practice/architectural-decisions.md)
- [Practice → Analyzing Risk](software/software-architecture/practice/analyzing-risk.md)
- [Practice → Diagramming](software/software-architecture/practice/diagramming.md)
- [Practice → Negotiation and Leadership](software/software-architecture/practice/negotiation-and-leadership.md)
- [Practice → Laws and Intersections](software/software-architecture/practice/laws-and-intersections.md)


<!-- prev-next-nav -->

---

[Architectural Thinking](software/software-architecture/foundations/architectural-thinking.md) →
