# Ch 1: What Happens When There Are No "Best Practices"?

## Table of Contents

- [1. Premise](#1-premise)
- [2. Foundations for decision making](#2-foundations-for-decision-making)
- [3. Architecture fitness functions](#3-architecture-fitness-functions)
- [4. Key definitions](#4-key-definitions)
- [5. Sysops Squad saga](#5-sysops-squad-saga)

## 1. Premise

- **The hard parts have no best practices** — entire classes of architecture problems have no general good solution, only one messy set of trade-offs cast against another.
- **Architects can't Google their way out** — every problem conflates the unique technical, organizational, and political constraints of the company, so common solutions rarely transfer.
- **No silver bullets** — Fred Brooks's 1986 claim still holds: no single technique delivers an order-of-magnitude improvement on its own.
- **Strive for the least worst combination of trade-offs** — the book replaces "best design" with the goal of finding the design where no characteristic is fully maximized but the balance promotes project success.
- **"Hard" does double duty** — *difficult* (problems no one has faced before) and *solid/structural* (the foundational stuff that's expensive to change later).
- **Timelessness via decision-making, not technology** — the book teaches trade-off analysis rather than current tools, since today's dominant style (microservices) replaced yesterday's (orchestrated SOA) once Linux + automation made provisioning free.

## 2. Foundations for decision making

- **Data outlives systems** — Tim Berners-Lee's observation; data tends to live longer than the architecture around it, so architecture is increasingly in service of data.
- **Operational data (OLTP)** — transactional data the business runs on (sales, inventory); inserts/updates/deletes in a database. Interruption stops the business.
- **Analytical data** — data used by data scientists and analysts for predictions, trending, and BI; often non-transactional, may live in a different format or store; not critical day-to-day but drives strategy.
- **Architectural Decision Record (ADR)** — short text file (1–2 pages) documenting one decision, with three sections: **Context** (problem + alternatives), **Decision** (chosen approach + justification), **Consequences** (outcomes and trade-offs considered). Authored as plain text, AsciiDoc, Markdown, or wiki.

## 3. Architecture fitness functions

- **Definition** — *any mechanism that performs an objective integrity assessment of some architecture characteristic or combination of architecture characteristics* (Ford, Parsons, Kua, *Building Evolutionary Architectures*, 2017).
- **Any mechanism** — testing libraries, monitors, chaos engineering frameworks, code-quality tools (e.g., SonarQube), or custom scripts all qualify.
- **Objective integrity assessment** — characteristics must be measurable. "High performance" is not a fitness function; a numeric latency threshold is. Composite traits like "agility" must be decomposed into measurable parts (deployability, testability, cycle time).
- **Atomic vs holistic scope** — atomic functions check one characteristic in isolation (e.g., component-cycle detection); holistic functions check combinations because characteristics interact (e.g., security vs performance, scalability vs elasticity).
- **Fitness functions vs unit tests** — separation rule: *if domain knowledge is required to run the test, it's a unit/functional test; if not, it's a fitness function*. Elasticity (burst handling) is architectural; mailing-address validation is domain.
- **Concrete examples** — JDepend `containsCycles()` test to block cyclic package dependencies; ArchUnit `layeredArchitecture()` rules to enforce layer access (Controller → Service → Persistence); NetArchTest equivalents for .NET.
- **Dynamic fitness functions** — return a context-dependent value (e.g., scalability tests where per-user performance is graded against concurrent user count).
- **Manual fitness functions** — for cases that can't be automated (e.g., legal review of sensitive code paths); slot into deployment pipelines as manual stages.
- **Enterprise governance use case** — the **Equifax data breach** (Apache Struts CVE-2017-5638): a fitness-function "slot" in every deployment pipeline would have let the security team push a check for the vulnerable Struts version across all projects, failing builds automatically instead of relying on manual scans.
- **Guard the important, not the urgent** — projects drown in urgency and skip principles like cycle prevention; fitness functions encode an executable checklist (analogous to Atul Gawande's *Checklist Manifesto* for surgeons and pilots) that runs on every build.
- **Don't overuse** — architects shouldn't build a frustrating, ivory-tower interlock of fitness functions; they're for important-but-not-urgent safeguards, not bureaucracy.

## 4. Key definitions

The book uses deliberately simple definitions to keep focus on architecture rather than design.

| Term | Definition |
|------|------------|
| **Service** | Cohesive collection of functionality deployed as an independent executable; part of an architecture quantum (Ch. 2). |
| **Coupling** | Two artifacts are coupled if a change in one might require a change in the other to maintain proper functionality. |
| **Component** | Architectural building block doing a business or infrastructure function, manifested as a package (Java), namespace (C#), or directory of source files (e.g., `app.business.order.history`). |
| **Synchronous communication** | Caller waits for the response before proceeding. |
| **Asynchronous communication** | Caller does not wait; may optionally be notified later via a separate channel. |
| **Orchestrated coordination** | Workflow includes a service whose primary responsibility is to coordinate it. |
| **Choreographed coordination** | Workflow has no orchestrator; participating services share coordination responsibility. |
| **Atomicity** | Workflow keeps consistent state at all times; opposite end of the spectrum is eventual consistency (Ch. 6). |
| **Contract** | Interface between two software parts — method/function calls, integration calls, dependencies; anywhere two pieces of software join. |

- **Architecture vs design** — the book stays on the architecture side because *why* is more important than *how* (the second law of software architecture from *Fundamentals of Software Architecture*); covering every implementation variant would balloon the book.

## 5. Sysops Squad saga

- **Running example** — the book uses one continuous fictional case study, the *Sysops Squad*, to ground abstract trade-off discussions in a concrete legacy system.
- **The business** — *Penultimate Electronics*, a large electronics retailer, sells support plans; on-site experts (the Sysops Squad) visit customers to repair purchased devices.
- **Four user roles** — **Administrator** (manages experts, billing, reference data), **Customer** (registers, files tickets, takes surveys), **Sysops Squad expert** (receives and fixes tickets, updates the knowledge base), **Manager** (consumes operational and analytical reports).
- **Two workflows** — *nonticketing* (expert onboarding, customer registration, monthly billing, manager reports) and *ticketing* (customer files ticket → system assigns best-fit expert by skill/location/availability → ticket pushed to the expert's mobile app → SMS/email to customer → expert fixes and marks complete → survey emailed → results recorded).
- **The "bad scenario"** — the existing monolith loses tickets, dispatches the wrong experts, freezes for 5 minutes to 2 hours during outages, and is so risky to change that Penultimate is considering shutting the line down. This sets up the rest of the book's decomposition work.
- **Existing components** — single monolith with namespaces like `ss.login`, `ss.billing.payment`, `ss.ticket.assign`, `ss.kb.search`, `ss.survey.notify`, etc. (≈18 components covering login, billing, customer/expert profiles, knowledge base, reporting, ticket lifecycle, support contracts, surveys, user maintenance).
- **Existing data model** — single schema, third-normal-form, few stored procedures/triggers, but many views feeding the Reporting component. The decomposition work in later chapters must bring the database team along.
