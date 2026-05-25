# Architecture Characteristics

> This page is *Fundamentals*-only: Chapters 4–7 build the vocabulary of architecture characteristics (the "-ilities"), the techniques to identify them, the metrics that measure them, and the fitness functions that govern them. *The Hard Parts* assumes this vocabulary throughout and does not re-derive it; the one place it picks up the thread is its **five modularity drivers** (availability, scalability, deployability, testability, maintainability) — composite characteristics that drive the decision to decompose, covered in `decomposition/when-to-decompose.md`.

## Table of Contents

- [1. What Counts as a Characteristic](#1-what-counts-as-a-characteristic)
- [2. The Four Buckets](#2-the-four-buckets)
- [3. Composite Characteristics](#3-composite-characteristics)
- [4. Identifying Characteristics — Three Sources](#4-identifying-characteristics--three-sources)
- [5. The Katas — Silicon Sandwiches and Going Green](#5-the-katas--silicon-sandwiches-and-going-green)
- [6. The *Vasa* and the Top-Three Rule](#6-the-vasa-and-the-top-three-rule)
- [7. Measuring Characteristics](#7-measuring-characteristics)
- [8. Governing with Fitness Functions](#8-governing-with-fitness-functions)
- [9. Scope — Characteristics Belong to a Quantum](#9-scope--characteristics-belong-to-a-quantum)
- [Sources](#sources)

## 1. What Counts as a Characteristic

A requirement qualifies as an **architecture characteristic** only if it meets **all three** of the following criteria — drawn in *Fundamentals* as an interlocking triangle:

1. **Specifies a nondomain design consideration** — describes *how* and *why* the system must behave, not *what* it does. Performance rarely appears in a requirements document; *"prevent technical debt"* never does.
2. **Influences some structural aspect of the design** — security can be a code-hygiene concern (good enough in a monolith) *or* an architectural concern (hardened service boundaries in microservices). Scalability is almost always structural: no clever code makes a monolith scale past a wall.
3. **Is critical or important to application success** — each characteristic costs design effort, dev effort, and complexity. Strive for the *fewest*, not the most.

**Terminology note.** *Non-functional requirements* is the legacy term (born alongside 1970s function-point analysis); the authors reject it as self-denigrating. *Quality attributes* implies after-the-fact assessment. The preferred term is **architecture characteristics** — the system's *capabilities*, in contrast to the domain (the system's *behavior*).

| Kind | Source | Examples |
|---|---|---|
| **Implicit** | Architect's domain knowledge; rarely in requirements | Availability, reliability, security, modularity; low-latency for HFT firms; data integrity for medical devices |
| **Explicit** | Stated in requirements documents | Specific concurrent-user counts, response-time SLAs, regulatory mandates |

## 2. The Four Buckets

Characteristics organize into four buckets. The lists are intentionally incomplete — new characteristics keep appearing as the ecosystem evolves, and every organization should establish its own vocabulary.

### 2.1. Operational

How well the system runs in production. Heavy overlap with operations and DevOps.

| Term | Definition |
|---|---|
| **Availability** | How much of the time the system must be up; 24/7 implies fast-recovery mechanisms. |
| **Continuity** | Disaster-recovery capability. |
| **Performance** | How well the system performs under stress, peak load, frequency, response times. |
| **Recoverability** | How quickly the system must come back online after disaster — backups, duplicate hardware. |
| **Reliability/safety** | Whether the system is mission-critical or fail-safe. A spectrum, not binary. |
| **Robustness** | Ability to handle errors and boundary conditions (loss of internet or power). |
| **Scalability** | Ability to perform as users or requests increase. |

### 2.2. Structural

Code-quality and code-organization concerns the architect owns or shares.

| Term | Definition |
|---|---|
| **Configurability** | How easily end users can change config through interfaces. |
| **Extensibility** | How well the architecture accommodates additions to existing functionality. |
| **Installability** | How easy it is to install on all needed platforms. |
| **Leverageability/reuse** | Extent to which common components are reusable across products. |
| **Localization** | Multi-language support on entry/query screens. |
| **Maintainability** | How easy it is to apply changes and enhance the system. |
| **Portability** | Ability to run on more than one platform. |
| **Upgradeability** | How easy and quick it is to upgrade servers and clients. |

### 2.3. Cloud

New in the second edition — most systems now touch the cloud in some capacity.

| Term | Definition |
|---|---|
| **On-demand scalability** | Cloud provider's ability to dynamically scale resources up. |
| **On-demand elasticity** | Cloud provider's flexibility under spiky demand. |
| **Zone-based availability** | Provider's ability to separate resources by computing zones for resilience. |
| **Region-based privacy and security** | Provider's legal ability to store data per country/region. |

### 2.4. Cross-Cutting

Concerns that don't fit a category but constrain design.

| Term | Definition |
|---|---|
| **Accessibility** | Access for all users, including those with disabilities. |
| **Archivability** | Constraints on archiving or deleting data after a period. |
| **Authentication** | Ensuring users are who they claim to be. |
| **Authorization** | Ensuring users access only the functions they're entitled to. |
| **Legal** | GDPR, Sarbanes-Oxley, regional regulations. |
| **Privacy** | Hiding transactions even from internal staff. |
| **Security** | DB/network encryption, remote-access authentication. |
| **Supportability** | Logging and other facilities for debugging and tech support. |
| **Usability** | Training required for users to achieve their goals. |

> **Watch for ambiguous terms.** *Interoperability* implies published, documented APIs; *compatibility* implies industry/domain standards. *Learnability* has two meanings — how easily users learn the software vs. how the system itself learns its environment via ML. *Availability* is not *reliability* — IP is available but not reliable; TCP layers reliability on top.

## 3. Composite Characteristics

A **composite characteristic** is one with no single objective measure; it decomposes into other measurable things.

> **Agility = deployability + modularity + testability.**

*The Hard Parts* leans on this exact formula when arguing for decomposition: **speed-to-market is architectural agility**, and agility is unreachable without all three constituents. Its **five modularity drivers** are the same composites in a slightly different mix:

| Driver | Decomposes into |
|---|---|
| **Speed-to-market / agility** | Maintainability + Testability + Deployability |
| **Competitive advantage** | Speed-to-market + Scalability + Availability/Fault Tolerance |

The antipattern of composite characteristics is **focusing on one slice**. *Fundamentals* gives the example of a stakeholder who says *"end-of-day fund pricing must complete on time"* and an ineffective architect who chases performance alone — missing that the system must also be **available**, **scalable** (more funds over time), **reliable** (no crashes mid-run), **recoverable** (resume from 85% complete), and **auditable** (correct prices, not just fast ones).

## 4. Identifying Characteristics — Three Sources

Characteristics surface from three places:

- **Domain concerns** — what business stakeholders care about (mergers, time to market, user satisfaction).
- **Project requirements** — explicit numbers and rules in the spec (concurrent users, regulatory mandates).
- **Implicit domain knowledge** — what an experienced architect in that domain has internalized (data integrity for medical software; low latency for high-frequency trading).

The lost-in-translation problem: architects speak in scalability, interoperability, fault tolerance, learnability; stakeholders speak in mergers, user satisfaction, time to market. **The architect's job is to translate.**

| Domain concern | Architectural characteristics |
|---|---|
| **Mergers and acquisitions** | Interoperability, scalability, adaptability, extensibility |
| **Time to market** | Agility, testability, deployability |
| **User satisfaction** | Performance, availability, fault tolerance, testability, deployability, agility, security |
| **Competitive advantage** | Agility, testability, deployability, scalability, availability, fault tolerance |
| **Time and budget** | Simplicity, feasibility |

## 5. The Katas — Silicon Sandwiches and Going Green

*Fundamentals* uses **architecture katas** (Ted Neward) for practice. A kata states a domain problem, a user count, requirements, and additional context; small teams design within a short timebox.

> *"How do we get great designers? Great designers design, of course."* — Fred Brooks

### 5.1. Silicon Sandwiches

A national sandwich shop wants online ordering. *Fundamentals* uses it to walk through identification end-to-end:

- **Explicit characteristics derived from the spec:** *scalability* (thousands → millions implies many concurrent users), *elasticity* (mealtime spikes — not in the requirements but obvious to an experienced architect), *performance* (nobody buys from a slow sandwich shop, especially at peak; define performance numbers in conjunction with scalability numbers), *reliability* of mapping integration (don't overspecify — degrade gracefully if traffic data is down), *customizability* (national + local promotions per franchise; microkernel or Template Method handle it).
- **Implicit characteristics:** *availability* (users must reach the site), *stability* (no dropped connections mid-checkout), *security* (payments are likely third-party; design hygiene suffices — leave it a design concern unless structure must support it).

**Design vs. architecture trade-off** — for customizability: microkernel (structural) or Template Method (design)? **Never decide in isolation.** Collaborate with developers, project managers, ops, and domain analysts; working alone produces the **Ivory Tower architecture** antipattern.

> *"There are no wrong answers in architecture, only expensive ones."* — Mark Richards

### 5.2. Going Green

Going Green recycles and resells old electronics via public kiosks and a website running the same backend. Three **clusters** of characteristics emerge:

| Cluster | Characteristics | Why |
|---|---|---|
| Public-facing (kiosk + web) | scalability, availability, agility | Customer-facing volume; rapid evolution |
| Back-office | security, data integrity, auditability | Financial and regulatory concerns |
| Assessment | maintainability, deployability, testability | Resale value depends on rapid updates as new device models ship |

These clusters counteract each other (auditability vs. fast deployability; UI scalability vs. back-office throughput). Trying to satisfy all eight in one architecture is possible but painful. **Clusters of characteristics become quantum boundaries** — see [Components and Quantum](foundations/components-and-quantum.md).

## 6. The *Vasa* and the Top-Three Rule

> **Case Study: The *Vasa*.** A 17th-century Swedish warship, designed for King Adolphus as both troop transport *and* gunship, with two decks and cannons twice the usual size — every characteristic the king demanded. To celebrate finishing construction, the *Vasa* sailed into Stockholm harbor, fired a cannon salute, and — being top-heavy — capsized and sank. Salvaged in 1961, now in a Stockholm museum.

The *Vasa* is the canonical antipattern of trying to support every characteristic at once. The fix is procedural:

- **Architectural characteristics worksheet** — seven slots for desired characteristics, a second column for implicit ones, an *Others Considered* column for displaced candidates.
- **Top-three rule** — stakeholders collaboratively pick the **top three highest-priority** characteristics, in *any* order. Ranking all seven wastes time, frustrates stakeholders, and rarely produces consensus. Three is enough to drive design and trade-off analysis.
- **Discovering the least important is also useful.** Architects more often cull *explicit* characteristics; implicit ones (security, availability) underpin general success. For Silicon Sandwiches, *customizability* moves into design, and *performance* is least critical — not because slow is OK, but because scalability and availability take priority in this context.

> **Never strive for the *best* architecture; aim for the *least worst* architecture.**

## 7. Measuring Characteristics

Measurement is genuinely hard, because terms like *agility*, *deployability*, and *wicked fast performance* have vague, contested meanings across the industry. The fixes:

| Category | Technique |
|---|---|
| **Operational** | Don't just measure average response time — track **maximum** and **percentile** latency. Statistical baselines beat hard numbers: a streaming team models scale over time and alarms on deviation. Modern teams track *first contentful paint*, *first CPU idle*, and **K-weight budgets** (cap on total bytes of libraries/frameworks per page). |
| **Structural** | **Cyclomatic Complexity (McCabe, 1976)** — `CC = E − N + 2P` over the function's control-flow graph. Industry says CC < 10 acceptable; the authors prefer < 5. **Crap4J** flags code as "crappy" once CC × low coverage cross a threshold (CC > 50 is unsalvageable). TDD lowers CC as a side effect. |
| **Process** | Composite agility decomposes into measurable testability (code coverage with caveats — 100% coverage with weak assertions provides no real confidence) and deployability (% successful deployments, deployment duration, deployment-induced bug counts). |

**Essential vs. accidental complexity** — CC measures complexity but cannot distinguish a hard problem from a poor design. It is useful for assessing both human-written and generative-AI code; the latter often brute-forces accidental complexity.

## 8. Governing with Fitness Functions

> **Governance** — Greek *kubernan*, "to steer." Architects govern any aspect of software development they want to influence, including quality, security, and modularity.

Modularity is **important but not urgent** — it gets crowded out by schedule pressure unless it is automated. The lineage is XP → CI → DevOps → **architectural fitness functions**, introduced by Ford, Parsons, and Kua in *Building Evolutionary Architectures* (O'Reilly, 2017/2022).

> **Architectural fitness function** — *any mechanism that performs an objective integrity assessment of some architecture characteristic or combination of architecture characteristics.*

It is a perspective, not a new framework. Fitness functions overlap existing tools: chaos engineering, metrics, monitors, unit-test libraries, code-quality tools.

| Scope | Use |
|---|---|
| **Atomic** | Check one characteristic in isolation (e.g., component-cycle detection). |
| **Holistic** | Check combinations because characteristics interact (security vs. performance, scalability vs. elasticity). |
| **Manual** | Slot into deployment pipelines for cases that can't be automated (e.g., legal review). |
| **Dynamic** | Return a context-dependent value (e.g., scalability tests graded against concurrent user count). |

**Test rule of thumb** — *if domain knowledge is required to run the test, it's a unit/functional test; if not, it's a fitness function*. Elasticity is architectural; mailing-address validation is domain.

Concrete tooling:

- **JDepend** (JVM) — `containsCycles()` test wired into CI; can also assert each package stays within tolerance (e.g., 0.5) of the main sequence.
- **ArchUnit** (JVM) — JUnit-style framework for layered-architecture and dependency rules.
- **NetArchTest** (.NET) — analogous tool for C#; e.g., assert `Presentation` types `ShouldNot().HaveDependencyOn("...Data")`.
- **Crap4J** — composite CC × coverage threshold.
- **Chaos Monkey** family — production fitness functions: Chaos Monkey, Latency Monkey, Chaos Kong (entire AWS data-center failure), Conformity Monkey (production rule enforcement), Security Monkey (known security defects), Janitor Monkey (orphan-service cleanup).

**The Equifax framing** *(The Hard Parts)* — a fitness-function "slot" in every deployment pipeline would have let the security team push a check for the vulnerable Struts version across all projects, failing builds automatically instead of relying on manual scans.

**Don't overuse.** Fitness functions are checklists in the *Checklist Manifesto* sense (Atul Gawande, 2009) — lightweight automated reminders for important-but-not-urgent safeguards, not ivory-tower bureaucracy. Architects must ensure developers understand the *purpose* of a function before imposing it; otherwise developers code to the metric (unit tests with no assertions; rule-bypass commits).

## 9. Scope — Characteristics Belong to a Quantum

The hidden assumption in pre-microservices frameworks was that one set of characteristics applies to the whole system — fine for monoliths, fatally wrong for distributed styles. A perfectly elastic codebase fails if its database isn't elastic too; code-level metrics cannot capture dependencies outside the codebase.

The fix is the **architecture quantum** — the unit at which characteristics are scoped. A quantum is the smallest part of the system that runs independently, with its own data and dependencies. Modern architects define characteristics at the quantum level, not the system level. The quantum is defined fully in [Components and Quantum](foundations/components-and-quantum.md); for this page, what matters is that **"the system must be highly available"** is a meaningless statement until you specify *which quantum* must be highly available, because different quanta in the same distributed architecture routinely require different characteristics.

The Going Green kata's three clusters are exactly this insight in disguise: each cluster is a candidate quantum boundary, drawn by the characteristics it must support.

## Sources

- [Fundamentals Ch 4: Architectural Characteristics Defined](software/software-architecture/books/fundamentals-of-software-architecture/ch04_architecture_characteristics_defined.md) (primary — the three criteria, four buckets, *Vasa*, least-worst rule)
- [Fundamentals Ch 5: Identifying Architectural Characteristics](software/software-architecture/books/fundamentals-of-software-architecture/ch05_identifying_architecture_characteristics.md) (the three sources, composite characteristics, Silicon Sandwiches, top-three rule)
- [Fundamentals Ch 6: Measuring and Governing](software/software-architecture/books/fundamentals-of-software-architecture/ch06_measuring_and_governing.md) (cyclomatic complexity, fitness functions, ArchUnit/NetArchTest/JDepend, Simian Army)
- [Fundamentals Ch 7: Scope of Architecture Characteristics](software/software-architecture/books/fundamentals-of-software-architecture/ch07_scope_of_architecture_characteristics.md) (the quantum-as-scope argument, Going Green clusters)


<!-- prev-next-nav -->

---

← [Modularity, Cohesion, Coupling](software/software-architecture/foundations/modularity-cohesion-coupling.md) | [Components and Quantum](software/software-architecture/foundations/components-and-quantum.md) →
