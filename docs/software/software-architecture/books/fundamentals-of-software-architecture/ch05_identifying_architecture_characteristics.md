# Ch 5: Identifying Architectural Characteristics

## Table of Contents

- [1. Three Sources of Architectural Characteristics](#1-three-sources-of-architectural-characteristics)
- [2. Translating Domain Concerns to "-ilities"](#2-translating-domain-concerns-to--ilities)
- [3. Composite Architectural Characteristics](#3-composite-architectural-characteristics)
- [4. Architecture Katas](#4-architecture-katas)
- [5. Silicon Sandwiches Kata: Setup](#5-silicon-sandwiches-kata-setup)
- [6. Silicon Sandwiches: Explicit Characteristics](#6-silicon-sandwiches-explicit-characteristics)
- [7. Silicon Sandwiches: Implicit Characteristics](#7-silicon-sandwiches-implicit-characteristics)
- [8. Limiting and Prioritizing Characteristics](#8-limiting-and-prioritizing-characteristics)

## 1. Three Sources of Architectural Characteristics

To create or validate an architecture, an architect analyzes both the domain *and* the architecture characteristics. Characteristics surface from three places:

- **Domain concerns** — what business stakeholders care about (mergers, time to market, user satisfaction).
- **Project requirements** — explicit numbers and rules in the spec (concurrent users, regulatory mandates).
- **Implicit domain knowledge** — what an experienced architect in that domain already internalizes (e.g., data integrity for medical-diagnostic software; low latency for high-frequency trading).

## 2. Translating Domain Concerns to "-ilities"

- **The lost-in-translation problem** — architects speak in scalability, interoperability, fault tolerance, learnability, availability; stakeholders speak in mergers, user satisfaction, time to market, competitive advantage. Neither can act on the other's vocabulary.
- **The architect's job** is to translate.

| Domain concern | Architectural characteristics |
|---|---|
| **Mergers and acquisitions** | Interoperability, scalability, adaptability, extensibility |
| **Time to market** | Agility, testability, deployability |
| **User satisfaction** | Performance, availability, fault tolerance, testability, deployability, agility, security |
| **Competitive advantage** | Agility, testability, deployability, scalability, availability, fault tolerance |
| **Time and budget** | Simplicity, feasibility |

## 3. Composite Architectural Characteristics

- **Composite characteristic** — one with no single objective measure; composed of other measurable things. **Agility** is the canonical example: it decomposes into *deployability*, *modularity*, and *testability*.
- **Antipattern: focusing on one slice of a composite.** A stakeholder says *"end-of-day fund pricing must complete on time"* and an ineffective architect chases performance alone — missing that it must also be **available**, **scalable** (more funds over time), **reliable** (no crashes mid-run), **recoverable** (resume from 85% complete), and **auditable** (correct prices, not just fast ones). Decomposing composites into objectively measurable parts is the architect's job.

## 4. Architecture Katas

- **Origin** — Ted Neward devised architecture katas a decade ago to give nascent architects a place to practice. *Kata* is Japanese for a martial-arts training exercise emphasizing form and technique. The book's authors host an updated version at *fundamentalsofsoftwarearchitecture.com*.

> *"How do we get great designers? Great designers design, of course."* — Fred Brooks

- **The premise** — small teams design from a domain-stated problem in a short timebox; groups share results and vote on the best design.
- **Kata sections:**
  - **Description** — the overall domain problem.
  - **Users** — expected number and types.
  - **Requirements** — domain requirements.
  - **Additional context** — realistic context that influences design but isn't in the spec.

## 5. Silicon Sandwiches Kata: Setup

The chapter's worked example.

- **Description** — A national sandwich shop wants online ordering in addition to its current call-in service.
- **Users** — Thousands today, perhaps millions one day.
- **Requirements:**
  - Place orders; if shop offers delivery, choose pickup or delivery.
  - Pickup customers get a pickup time and directions (must integrate with external mapping services with traffic info).
  - For delivery, dispatch a driver with the order.
  - Mobile device accessibility.
  - National and local daily promotions/specials.
  - Accept payment online, at the shop, or upon delivery.
- **Additional context:**
  - Sandwich shops are franchised, each with a different owner.
  - Parent company plans to expand overseas.
  - Corporate goal: hire inexpensive labor to maximize profit.

The architect doesn't design the whole system — they look for things that influence structure.

## 6. Silicon Sandwiches: Explicit Characteristics

- **Scalability** — "thousands, perhaps millions" implies handling many concurrent users without degradation. Note: the spec didn't *say* "scalability" — the architect decoded it from a user count.
- **Elasticity** — handling *bursts*. Distinct from scalability: a hotel reservation site may be predictably seasonal (scalable, not elastic); a concert-ticket site is bursty (elastic *and* scalable). A sandwich shop has obvious mealtime spikes — even though elasticity isn't in the requirements, the architect must surface it.

| Concept | What it measures |
|---|---|
| **Scalability** | Increase of users over time |
| **Elasticity** | Bursts of traffic |

- **Going requirement-by-requirement:**

| Requirement | Architectural impact |
|---|---|
| Place order, choose pickup/delivery | None special |
| Pickup time + external map/traffic integration | **Reliability** of integration points; *guard against overspecifying* — should the site fail if traffic data is down, or just degrade gracefully? |
| Dispatch driver | None special |
| Mobile device accessibility | UX-driven; suggests a mobile-optimized web app over native (budget/simplicity), which in turn argues for **performance**-related characteristics (page load) |
| National + local daily promotions | **Customizability** — traffic info, specials, recipes vary by location. Microkernel architecture supports this natively; design patterns (e.g., Template Method) can also handle it |
| Online/at-shop/on-delivery payment | Implies **security**, but nothing exotic — design-level security hygiene suffices |
| Franchised shops, different owners | Cost constraint — consider feasibility, possibly a *sacrificial architecture* |
| Overseas expansion | **Internationalization** (i18n) — UX-heavy, no special structure required |
| Inexpensive labor | **Usability** — design concern more than architecture |

- **Performance** — derived as a third explicit characteristic; nobody buys from a slow sandwich shop, especially at peak. *Define performance numbers in conjunction with scalability numbers*: a baseline without scale, then an acceptable level under load.

## 7. Silicon Sandwiches: Implicit Characteristics

- **Availability** — users must be able to reach the site.
- **Stability** — the site must stay up *during* an interaction; no dropping connections mid-checkout.
- **Security** — implicit in every system. Promote it to architectural only when it requires structural support. Here, payments are likely third-party; general hygiene (no plain-text card numbers, minimal storage) suffices — security stays a design concern.
- **Customizability** — multiple requirements (recipes, local specials, locally overridable directions) push it from design into architecture territory, since structure may best support it.

> *"There are no wrong answers in architecture, only expensive ones."* — One of Mark's famous quotes

- **Design vs. architecture trade-off (sidebar).** Customizability via microkernel (structural) or via Template Method (design)? It depends — competing concerns may make microkernel costly; other characteristics may suffer in one option more than the other. **Never decide in isolation** — collaborate with developers, project managers, ops, and domain analysts. Working alone produces the **Ivory Tower architecture** antipattern.

## 8. Limiting and Prioritizing Characteristics

- **Antipattern — generic architecture** — designing one architecture that supports *all* possible characteristics. Each added characteristic compounds complexity *before* the team has even begun the domain work.

> **Case Study: The Vasa.** A 17th-century Swedish warship (built 1626–1628 for King Adolphus) designed to be both troop transport *and* gunship, with two decks and cannons twice the usual size — every characteristic the king demanded. To celebrate finishing construction, the *Vasa* sailed into Stockholm harbor, shot a cannon salute, and — being top-heavy — capsized and sank. Salvaged in 1961, now in a Stockholm museum.

- **Why architects can't just ask stakeholders.** Hand a stakeholder a list of characteristics and ask which they want — the answer is always *"all of them!"*
- **Technique: the architectural characteristics worksheet** (downloadable from *developertoarchitect.com/resources.html*).
  - **Seven slots** for desired characteristics. Why seven? Some bounded number was needed — six or eight would do (with a nod to the psychology behind the number seven).
  - **Second column** lists implicit characteristics; the architect "pulls" any that need explicit prioritization into the first column.
  - **Others Considered** captures displaced candidates.
  - **Final step:** stakeholders collaboratively pick the **top three highest-priority** characteristics, in *any* order. Don't try to rank all seven — that wastes time, frustrates stakeholders, and rarely produces consensus. Top-three is enough to drive design and trade-off analysis.
- **Discovering the least important is a useful exercise.** If you had to drop one, which would it go? Architects more often cull *explicit* characteristics; implicit ones (security, availability) underpin general success. For Silicon Sandwiches, *customizability* could move into design, and of the operational characteristics *performance* is least critical — not because slow is OK, but because scalability and availability take priority in this design.
