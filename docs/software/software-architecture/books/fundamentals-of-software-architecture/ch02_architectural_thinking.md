# Ch 2: Architectural Thinking

## Table of Contents

- [1. Architecture Versus Design](#1-architecture-versus-design)
- [2. Technical Breadth](#2-technical-breadth)
- [3. Analyzing Trade-Offs](#3-analyzing-trade-offs)
- [4. Understanding Business Drivers](#4-understanding-business-drivers)
- [5. Balancing Architecture and Hands-On Coding](#5-balancing-architecture-and-hands-on-coding)

## 1. Architecture Versus Design

- **House analogy** — number of floors, footprint, roof shape define the *structure* (architecture); carpet, wall colors, lamp choices define the *design*. Software follows the same split.
- **Decisions live on a spectrum**, not a binary. Three criteria help place a decision toward architecture or design:
  - **Strategic vs. tactical** — long-term, multi-stakeholder, weeks of planning ⇒ architecture; quick, solo, easily reversed ⇒ design.
  - **Level of effort** — Martin Fowler's "architecture is the stuff that's hard to change." Moving a monolith to microservices is architecture; rearranging fields on a screen is design.
  - **Significance of trade-offs** — choosing microservices buys scalability/agility/elasticity/fault tolerance but costs complexity, money, data consistency, and performance — significant trade-offs ⇒ architectural. Splitting a class file (better maintainability vs. more files to manage) is a minor trade-off ⇒ design.

## 2. Technical Breadth

- **Breadth over depth.** Developers need technical *depth* (deep mastery of a stack); architects need technical *breadth* (a little about a lot) so they can match capabilities to constraints.
- **The Knowledge Pyramid — three tiers:**
  - **Stuff you know** — your daily-use, expert-level skills (smallest tier; nobody's an expert at everything).
  - **Stuff you know you don't know** — things you've heard of but can't use deeply (e.g., a Java dev who knows Clojure exists but can't write it).
  - **Stuff you don't know you don't know** — the largest tier; the perfect tool for a problem you've never heard of.
- **Career goal:** keep promoting items upward — from the bottom tier into "know you don't know," and (when needed) up into "know."
- **Maintenance cost.** "Stuff you know" decays without continual investment; ignore Ruby on Rails for a year and your expertise is gone.
- **Architects trade some depth for breadth** — a wider portfolio of options yields better trade-off analysis. Some pet expertise survives; the rest usefully atrophies.
- **Two dysfunctions of the depth-to-breadth transition:**
  - Trying to maintain expertise everywhere — succeeding nowhere, working ragged.
  - **Stale expertise** — believing your outdated information is still cutting edge. Common in long-tenured leaders making decisions with ancient criteria.

> **Antipattern: Frozen Caveman** — an architect who reverts to a pet irrational concern on every project (Andrew Koenig: an antipattern seems good at the start but leads to trouble). One client's architects, burned years earlier by a freak comms outage with their Italy stores, asked "but what if we lose Italy?" on every centralized design afterward. Distinguish genuine from perceived risk.

### 2.1. The 20-Minute Rule

- **Spend at least 20 minutes a day** learning something new — look up an unfamiliar buzzword, read a chapter, browse InfoQ, DZone Refcardz, or the Thoughtworks Technology Radar.
- **Do it first thing in the morning, before email.** Lunch and evening slots get eaten by work and life; once email is open, the day owns you.

### 2.2. Building a Personal Technology Radar

The Thoughtworks Technology Radar is a biannual living document the firm produces to assess existing and nascent technologies. The same structure works as a personal tool.

- **Four quadrants** — slices of the technology landscape:

| Quadrant | Includes |
|---|---|
| Tools | IDEs through enterprise integration tools |
| Languages and frameworks | Computer languages, libraries, frameworks (often open source) |
| Techniques | Processes, engineering practices, and advice |
| Platforms | Databases, cloud vendors, operating systems |

- **Four rings** — what to do with a given "blip" (innermost = most committed):

| Ring | Original (Thoughtworks) meaning | Suggested personal meaning |
|---|---|---|
| Hold | "Don't start anything new with this technology" — fine on existing projects, think twice for new ones | Things and habits to avoid (e.g., low-value news streams) |
| Assess | Worth exploring via spikes, research, or talks to gauge organizational impact | Promising tech you've heard about but not yet examined |
| Trial | Worth a low-risk pilot project to learn how to build with it | Active R&D, e.g., spike experiments inside a larger codebase |
| Adopt | Thoughtworks recommends industry-wide adoption | New things you're most excited about, your current best practices |

- **Diversify like a financial portfolio** — mix in-demand skills with speculative gambits (e.g., generative AI, embedded IoT). The exercise of building the radar matters more than the chart itself; Thoughtworks' "Build Your Own Radar" tool generates the visualization from a Google spreadsheet.
- **Technology bubbles.** Heavy investment in one stack creates a memetic echo chamber; honest outside appraisals don't penetrate, and collapse comes without warning. The radar is the antidote.

## 3. Analyzing Trade-Offs

> **Architecture is the stuff you can't Google or ask an LLM about.** — Mark Richards

> **There are no right or wrong answers in architecture — only trade-offs.** — Neal Ford

- **"It depends"** is the famous (and accurate) answer to every architecture question — REST vs. messaging, microservices vs. not, etc. — because the answer depends on deployment environment, business drivers, culture, budgets, deadlines, team skills, and more.
- **Concrete example: auction system, queues vs. topic.** A `Bid Producer` must send each bid to `Bid Capture`, `Bid Tracking`, and `Bid Analytics`. Two options: pub/sub topic or point-to-point queues.

| Topic advantages | Topic disadvantages |
|---|---|
| Architectural extensibility — adding a new `Bid History` consumer requires zero changes to existing services or infrastructure (it just subscribes to the topic) | Data access and security concerns — anyone can wiretap a topic; queues are point-to-point so a rogue listener immediately causes detectable data loss |
| Service decoupling — `Bid Producer` doesn't know who consumes the data | No heterogeneous contracts — all consumers share one schema, so a contract change for one service ripples to all |
|   | No per-channel monitoring or programmatic auto-scaling (technology-specific: AMQP-style exchange-vs-queue separation can support both) |

> **Programmers know the benefits of everything and the trade-offs of nothing. Architects need to understand both.** — Rich Hickey

- **The architect's question** isn't "which is better?" but "which of these trade-offs matters more in *this* context — extensibility, or security?"

## 4. Understanding Business Drivers

- Architects must understand business goals and **translate them into architecture characteristics** (scalability, performance, availability, etc.). This requires business-domain knowledge plus collaborative relationships with stakeholders. Chapters 4–7 cover defining, identifying, measuring, and scoping these characteristics.

## 5. Balancing Architecture and Hands-On Coding

- **Every architect should code** to retain a level of technical depth — but balancing it with the architect role (diagrams, meetings, more meetings) is hard.

> **Antipattern: Bottleneck Trap** — the architect owns critical-path or framework code but isn't full-time on it, so the team waits on them. Avoid by delegating critical-path code to the team and having the architect work on a minor business feature one to three iterations out. Three benefits: hands-on practice, the team gains ownership of the hard parts, and the architect feels the team's day-to-day pain points.

- **If you can't code with the team, stay hands-on through:**
  - **Frequent proofs-of-concept** — best for picking between options (e.g., two caching products). Write *production-quality* code, because POCs often end up checked in as the reference architecture, and because sloppy POC habits become coding habits.
  - **Tackle technical debt** — usually low priority, so missing a sprint doesn't sink the iteration; frees the team to work on user stories.
  - **Fix bugs** — exposes weak points in code and architecture.
  - **Automate** — build small CLI tools, validators, lint rules, refactoring scripts; or write architectural fitness functions (e.g., ArchUnit on the JVM) for compliance checks. Covered further in Chapter 6.
  - **Do code reviews** — keeps the architect involved with the source even when not writing it; doubles as a compliance check and a mentoring opportunity.
