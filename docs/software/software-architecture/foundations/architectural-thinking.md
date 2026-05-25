# Architectural Thinking

> *Fundamentals* opens with two chapters that frame the entire book: what software architecture *is*, and how an architect *thinks*. *The Hard Parts* doesn't have an equivalent opening — it assumes the reader already has this vocabulary. This page is mostly Richards & Ford, with *The Hard Parts* cited where it sharpens a definition.

## Table of Contents

- [1. The Four-Dimensional Definition](#1-the-four-dimensional-definition)
- [2. The Three Laws](#2-the-three-laws)
- [3. Architecture vs. Design](#3-architecture-vs-design)
- [4. Technical Breadth Over Depth](#4-technical-breadth-over-depth)
- [5. Analyzing Trade-Offs](#5-analyzing-trade-offs)
- [6. Eight Expectations of an Architect](#6-eight-expectations-of-an-architect)
- [7. Staying Hands-On](#7-staying-hands-on)
- [Sources](#sources)

## 1. The Four-Dimensional Definition

Software architecture has no industry-standard definition. *Fundamentals* offers a working one with four dimensions:

| Dimension | What it covers |
|---|---|
| **Architecture style** | The overall topology — layered, microservices, event-driven, etc. Chosen *after* characteristics and components are known, because the style is the easiest implementation path for those requirements. |
| **Architecture characteristics** | The system's *capabilities*, commonly the "-ilities" — scalability, availability, performance, security. They define what the system should do *well*, beyond functional requirements. |
| **Logical components** | The *behavior* of the system, expressed as domains, entities, and workflows. Designing them is one of the architect's core structural activities. |
| **Architecture decisions** | The constraints that justify the other three — e.g. *"only the Business and Services layers may access the database."* |

The four dimensions are an analytical tool, not a sequence. An architect cycles among them whenever a new constraint arrives, and each decision is justified by tradeoffs across the other three.

**Architecture is contextual.** Every architecture is a product of its era's constraints. Microservices were inconceivable in 2002 because servers, OS, app servers, and databases were all expensive proprietary commercial software; the DevOps revolution and open source made today's distributed styles affordable. The implication is that any architectural recommendation has an implicit shelf life — what counts as "the right answer" rotates with the underlying economics.

## 2. The Three Laws

Richards and Ford set out to find ten or fifteen universal laws and ended up with three.

> **First Law of Software Architecture** — Everything in software architecture is a trade-off.

The First Law has two corollaries:
- If you think you've found something that *isn't* a trade-off, you just haven't *identified* the trade-off yet.
- You can't do trade-off analysis once and be done; every situation forces re-evaluation. Teams that try to standardize ("always use choreography") discover it works sometimes and fails spectacularly elsewhere.

> **Second Law of Software Architecture** — *Why* is more important than *how*.

An experienced architect can usually figure out *how* an unfamiliar architecture works, but struggles to recover *why* prior decisions were made. *How* is in the code; *why* rots out of memory unless it is preserved — typically in ADRs (see [Practice → Architectural Decisions](practice/architectural-decisions.md)).

> **Third Law of Software Architecture** — Most architecture decisions aren't binary but rather exist on a spectrum between extremes.

The Third Law produces a useful test for whether a decision counts as architectural: it does when each option carries significant trade-offs. *The Hard Parts* leans on this exact test as the trigger for its entire book — the chapters are organized around problems where each option has significant trade-offs and no single "best practice" wins.

## 3. Architecture vs. Design

The line between architecture and design is itself spectrum-shaped (Third Law). Richards and Ford offer a house analogy: number of floors, footprint, and roof shape are *architecture* (structure); carpet, wall colors, and lamp choices are *design* (decoration). Three criteria place any given decision on the spectrum:

| Criterion | Architecture side | Design side |
|---|---|---|
| **Strategic vs. tactical** | Long-term, multi-stakeholder, weeks of planning | Quick, solo, easily reversed |
| **Level of effort** | Hard to change (monolith → microservices) | Easy to change (rearrange UI fields) |
| **Significance of trade-offs** | Many large trade-offs (e.g. microservices buys agility/elasticity, costs complexity/money/consistency/perf) | A minor trade-off (split a class file: better maintainability vs. more files) |

Martin Fowler's phrase — *"architecture is the stuff that's hard to change"* — captures the level-of-effort dimension. *The Hard Parts* picks up the same point with a different framing: the word *hard* is intentional double duty — hard meaning *difficult*, and hard meaning *solid/structural* (the foundational stuff that, once chosen, is expensive to change).

## 4. Technical Breadth Over Depth

Developers need technical *depth* — deep mastery of a stack. Architects need technical *breadth* — a little about a lot — so they can match capabilities to constraints. The book maps knowledge into three tiers:

- **Stuff you know** — your daily-use, expert-level skills. Smallest tier; nobody is an expert at everything. Decays without continual investment.
- **Stuff you know you don't know** — things you've heard of but can't use deeply.
- **Stuff you don't know you don't know** — the largest tier. The perfect tool for a problem you've never heard of lives here.

The career goal of an architect is to keep promoting items upward: from the bottom tier into "know you don't know," and (when needed) into "know." Architects trade some depth for breadth; a wider portfolio of options yields better trade-off analysis.

**Two dysfunctions** of the depth-to-breadth transition:

1. Trying to maintain expertise everywhere — succeeding nowhere, working ragged.
2. **Stale expertise** — believing outdated information is still cutting edge. Common in long-tenured leaders making decisions with ancient criteria.

> **Antipattern: Frozen Caveman** — an architect who reverts to a pet irrational concern on every project. One client's architects, burned years earlier by a freak comms outage with their Italy stores, asked *"but what if we lose Italy?"* on every centralized design afterward. Distinguish genuine from perceived risk.

**The 20-Minute Rule.** Spend at least 20 minutes a day learning something new — look up an unfamiliar buzzword, read a chapter, browse the Thoughtworks Technology Radar. Do it *first thing in the morning, before email*; once email is open, the day owns you.

**A personal technology radar** — four quadrants (Tools, Languages & Frameworks, Techniques, Platforms) crossed with four rings (Hold, Assess, Trial, Adopt) — is the recommended way to keep the portfolio diverse and to surface "stuff you don't know you don't know."

## 5. Analyzing Trade-Offs

> *Architecture is the stuff you can't Google or ask an LLM about.* — Mark Richards

> *There are no right or wrong answers in architecture — only trade-offs.* — Neal Ford

> *Programmers know the benefits of everything and the trade-offs of nothing. Architects need to understand both.* — Rich Hickey

The famous (and accurate) answer to every architecture question is *"it depends"* — on deployment environment, business drivers, culture, budgets, deadlines, team skills, and more.

Richards & Ford illustrate with an **auction system** that must broadcast bids to three consumers (capture, tracking, analytics). The choice is a pub/sub topic vs. point-to-point queues:

| Topic advantages | Topic disadvantages |
|---|---|
| Architectural extensibility — a new consumer just subscribes | Anyone can wiretap; queues are point-to-point so a rogue listener immediately causes detectable data loss |
| Producer doesn't know who consumes the data | All consumers share one schema — a contract change for one ripples to all |
| | No per-channel monitoring or programmatic auto-scaling |

The architect's question isn't *"which is better?"* but *"which of these trade-offs matters more in this context — extensibility, or security?"*

*The Hard Parts* expands this stance into its central method: a three-step **trade-off analysis** — *find what parts are entangled, analyze how they couple, assess the impact of change on each side.* See [Trade-Off Analysis](foundations/tradeoff-analysis.md) for the mechanics.

## 6. Eight Expectations of an Architect

Eight core expectations apply regardless of title or seniority:

| # | Expectation | What it means |
|---|---|---|
| 1 | **Make architecture decisions** | *Guide* technology choices rather than specify them — mandate a reactive frontend framework, not React specifically. Pin specific choices only when needed to preserve a characteristic. |
| 2 | **Continually analyze the architecture** | Assess *architecture vitality* — how viable a 3+ year-old architecture is today. Combat *structural decay* from changes that erode the required characteristics. Remember test and release pipelines: fast code changes don't help if releases take months. |
| 3 | **Keep current with latest trends** | Architecture decisions are long-lasting and hard to reverse — trend awareness matters more for architects than for developers. |
| 4 | **Ensure compliance with decisions** | Verify teams follow the documented decisions. A UI dev bypassing a layered-access rule for performance silently undermines the architecture. Use automated *fitness functions* (see [Architecture Characteristics](foundations/architecture-characteristics.md)). |
| 5 | **Understand diverse technologies** | Breadth over depth. Knowing the trade-offs of 10 caching products is more valuable than mastery of one. |
| 6 | **Know the business domain** | An architect at a bank who can't speak about *aleatory contracts* loses credibility with stakeholders and can't design effectively. |
| 7 | **Possess interpersonal skills** | *"It's always a people problem"* (Weinberg). Leadership and communication are at least half the job. Many strong technologists fail in the role for lack of them. |
| 8 | **Understand and navigate politics** | *Almost every architect decision will be challenged.* A dev's pattern choice rarely needs approval; an architect's call to silo a CRM database affects everyone touching that data, and they must negotiate it through. |

## 7. Staying Hands-On

Every architect should code to retain technical depth, but balancing it with the rest of the role (diagrams, meetings, more meetings) is hard.

> **Antipattern: Bottleneck Trap** — the architect owns critical-path or framework code but isn't full-time on it, so the team waits. Avoid by delegating critical-path code to the team and having the architect work on a *minor business feature one to three iterations out*. Three benefits: hands-on practice, the team gains ownership of the hard parts, and the architect feels the team's day-to-day pain points.

When direct feature work isn't viable, stay hands-on through:

- **Frequent proofs-of-concept** — best for picking between options (e.g. two caching products). Write *production-quality* code, because POCs often end up checked in as the reference architecture, and because sloppy POC habits become coding habits.
- **Tackle technical debt** — usually low priority, so missing a sprint doesn't sink the iteration; frees the team to work on user stories.
- **Fix bugs** — exposes weak points in code and architecture.
- **Automate** — small CLI tools, validators, lint rules, refactoring scripts; or write architectural fitness functions (ArchUnit on the JVM, NetArchTest on .NET) for compliance checks.
- **Do code reviews** — keeps the architect involved with the source even when not writing it; doubles as a compliance check and a mentoring opportunity.

The cross-cutting message of both books: the architect's real value is becoming the **objective arbiter of trade-offs**. Not chasing silver bullets, not evangelizing, not dictating from on high — analyzing each decision's forces in its own context and recording the *why* so the work can survive successor architects.

## Sources

- [Fundamentals Ch 1: Introduction](software/software-architecture/books/fundamentals-of-software-architecture/ch01_introduction.md)
- [Fundamentals Ch 2: Architectural Thinking](software/software-architecture/books/fundamentals-of-software-architecture/ch02_architectural_thinking.md)
- [The Hard Parts Ch 1: What Happens When There Are No "Best Practices"?](software/software-architecture/books/software-architecture-the-hard-parts/ch01_no_best_practices.md) (secondary — for the *hard* double-meaning and the trade-off stance)


<!-- prev-next-nav -->

---

← [Summary](software/software-architecture/summary.md) | [Modularity, Cohesion, Coupling](software/software-architecture/foundations/modularity-cohesion-coupling.md) →
