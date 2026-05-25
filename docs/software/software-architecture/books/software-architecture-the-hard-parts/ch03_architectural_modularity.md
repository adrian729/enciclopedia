# Ch 3: Architectural Modularity

## Table of Contents

- [1. Why architecture must keep changing](#1-why-architecture-must-keep-changing)
- [2. Modularity Drivers](#2-modularity-drivers)
- [3. The five characteristics](#3-the-five-characteristics)
- [4. Sysops Squad saga: building the business case](#4-sysops-squad-saga-building-the-business-case)

## 1. Why architecture must keep changing

- **Architecture is no longer static** — mergers, acquisitions, competition, ML/AI automation, containerization, cloud, DevOps, and continuous-delivery pipelines all force the underlying architecture to adapt; software architecture cannot be treated like a building's structural foundation.
- **The water-glass analogy** — a monolith is a single glass filling up; adding another glass (server/VM) doesn't help because the glass would just hold the same application. Splitting the application across two glasses gives 50% more capacity. The book recommends this analogy when justifying decomposition spending to non-technical executives.
- **Modularity is not always distribution** — maintainability, testability, and deployability can also be achieved with a *modular monolith* (domain-partitioned components) or a *microkernel* architecture (plug-in components); breaking into smaller distributed parts is one route, not the only one.

## 2. Modularity Drivers

- **Don't decompose without a business driver** — the primary business drivers for breaking applications into smaller parts are **speed-to-market** (a.k.a. time-to-market) and **competitive advantage**. Architects should not break a system apart to chase fashion.
- **Speed-to-market = architectural agility** — agility is a *compound* characteristic composed of **maintainability**, **testability**, and **deployability**.
- **Competitive advantage = speed-to-market + scalability + availability/fault tolerance** — growth requires scale; fault tolerance keeps the rest of the system working as parts fail.
- **The five architectural characteristics** that support agility, speed-to-market, and competitive advantage are: **availability (fault tolerance)**, **scalability**, **deployability**, **testability**, **maintainability**.

## 3. The five characteristics

### 3.1. Maintainability

- **Definition** — ease of adding, changing, or removing features and applying internal changes (maintenance patches, framework upgrades, third-party upgrades).
- **Von Zitzewitz maintainability metric** — `ML = 100 * Σ ci` over the system's `k` logical components, where `ci` is the coupling level of each component (with emphasis on incoming coupling). Higher incoming coupling drives lower overall maintainability.
- **Practical signals** — component coupling, component cohesion, cyclomatic complexity, component size (number of aggregated statements of code within a component), and technical-vs-domain partitioning.
- **Why monoliths score low** — technical partitioning into layers spreads any one domain across all layers. Adding an expiration date to a wish list item in a layered monolith may need a UI engineer, a backend engineer, and a DBA all coordinating, because the change scope is *application level*. A service-based architecture brings the change scope down to *domain level*; microservices bring it to *function level*.

### 3.2. Testability

- **Definition** — ease *and* completeness of testing (typically via automated tests).
- **Monolith problem** — running thousands of unit tests for a small change is slow and produces failures unrelated to the change.
- **Limit of modularity** — testing scope shrinks per service, but if Service A talks to Service B and C, a change to A again drags B and C into the regression scope; communication erodes the benefit.

### 3.3. Deployability

- **Definition** — combines ease of deployment, frequency of deployment, and risk of deployment; agility requires all three.
- **Monolith ceremony** — code freezes, mock deployments, and weeks/months between releases pile multiple unrelated changes into a single risky deploy.
- **"Big ball of distributed mud"** — Matt Stine: *if your microservices must be deployed as a complete set in a specific order, please put them back in a monolith and save yourself some pain*. Excessive inter-service communication kills the deployability gain.

### 3.4. Scalability

- **Scalability** — ability to remain responsive as user load *gradually* grows over time; a function of *modularity* (number of separate deployment units).
- **Elasticity** — ability to remain responsive during *instantaneous* spikes; a function of *granularity* (size of each deployment unit) and depends on a small **mean time to startup (MTTS)**.
- **Concert-ticketing example** — system goes from 20 to 3,000 concurrent users in seconds when tickets go on sale; only fine-grained services with very low MTTS can spin up fast enough.
- **Star ratings** — layered monolith scales and elasticizes poorly (application-level scalability, poor MTTS). Service-based architecture improves scalability more than elasticity (domain-level scalability, fair MTTS). Microservices maximize both (function-level scalability, excellent MTTS).
- **Synchronous calls hurt** — both metrics degrade as services communicate more synchronously to complete a transaction; minimize synchronous chatter when scale matters.

### 3.5. Availability/fault tolerance

- **Definition (in this context)** — the ability for some parts of the system to remain responsive while other parts fail (e.g., search and order placement keep working even if payment processing dies).
- **Why monoliths fail at this** — load-balancing multiple monolith instances doesn't help if the fault is a programming bug, since the bug exists in every instance.
- **Modularity isolates failure** — separate deployment units contain catastrophic failures. *Caveat*: if other services are *synchronously* dependent on the failing service, fault tolerance is lost. Asynchronous communication is essential for real fault tolerance in distributed systems.

## 4. Sysops Squad saga: building the business case

- **Decision** — Addison and Austen built a business case to migrate the monolithic Sysops Squad application to a distributed architecture by mapping each business complaint to a Modularity Driver.
- **Mapping the complaints**:

| Business complaint | Modularity Driver invoked |
|--------------------|---------------------------|
| Changes break unrelated things; codebase too large to navigate | Maintainability |
| 30% of tests commented out; full suite must run for any change | Testability |
| Monthly releases bundle untested changes; high deploy risk | Deployability |
| Survey and reporting features keep crashing the whole system | Availability / fault tolerance |
| System freezes with >25 concurrent ticketers and during report runs | Scalability + database load |

- **ADR — Migrate Sysops Squad Application to a Distributed Architecture** — *Decision*: migrate to a distributed architecture to (a) make core ticketing more available via fault tolerance, (b) provide scalability for ticket creation, (c) split reporting load off the database, (d) raise team agility, (e) reduce defects through better testability, (f) deploy weekly/daily. *Consequences*: feature work delays during migration, additional cost, release engineers manage multiple deployable units, and the monolithic database must eventually be broken apart.
