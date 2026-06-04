# Layered Architecture

> *Fundamentals* Ch 10 is the sole source. *The Hard Parts* mentions the layered monolith only as the starting point for its decomposition chapters; it has nothing distinctive to add to the style itself. The layered style is the de facto default for many legacy applications and the destination of *Architecture by Implication* — what teams produce when they "just start coding."

## Table of Contents

- [1. Topology](#1-topology)
- [2. Layers of Isolation — Open vs. Closed](#2-layers-of-isolation--open-vs-closed)
- [3. The Architecture Sinkhole Antipattern](#3-the-architecture-sinkhole-antipattern)
- [4. Data Topology and Cloud Fit](#4-data-topology-and-cloud-fit)
- [5. When to Use and When Not To](#5-when-to-use-and-when-not-to)
- [6. Risks and Antipatterns](#6-risks-and-antipatterns)
- [7. Architecture Characteristic Ratings](#7-architecture-characteristic-ratings)
- [8. Examples](#8-examples)
- [Sources](#sources)

## 1. Topology

The layered style — also called **n-tiered** — arranges components in horizontal layers, each performing a specific *technical* role:

| Layer | Responsibility |
|---|---|
| **Presentation** | UI / browser logic |
| **Business** | Business rules |
| **Persistence** | Data access |
| **Database** | Storage |

Smaller applications use three layers; larger ones five or more; some merge Business and Persistence when SQL is embedded directly in business components.

Three physical deployment variants are common:

- Presentation + Business + Persistence in one deployment unit; Database external.
- Presentation in its own unit; Business + Persistence in a second; Database external.
- All four (including embedded/in-memory Database) in one deployment unit — typical of mobile apps and on-prem packaged products.

The defining trait is **technical partitioning** — layered is the canonical technical partition (see [Styles Overview](styles/overview.md)). Any single domain (e.g., `Customer`) is spread across Presentation, Business, Persistence, and Database, which makes domain-driven design fit poorly: every domain change touches every layer. The benefit each layer is an abstraction owning a specific responsibility, so specialists can apply deep expertise inside one layer without learning the others. The cost is **lack of holistic agility** — the system's overall ability to respond quickly to change.

## 2. Layers of Isolation — Open vs. Closed

The mechanism that makes layered work is the **layers of isolation** concept: changes in one layer don't ripple to others as long as contracts hold. Each layer is ignorant of the others' internals.

| Layer mode | Meaning |
|---|---|
| **Closed** | A request *must* pass through this layer; it cannot be bypassed. Closed layers protect isolation. |
| **Open** | A request *can* bypass this layer. Useful for shared utilities or to mitigate the sinkhole antipattern. |

Layers in the main request path **must be closed** to preserve isolation; otherwise changes to Persistence ripple into Business *and* Presentation. Adding a new utility layer (e.g., a `Services` layer holding date/string utilities, auditing, logging that Presentation must not see) is the standard move when more architectural rules are needed — the new layer is marked **open** so Business can either use it or skip it on the way to Persistence.

Document every layer as open or closed and *why*. Without that documentation the architecture degenerates into the tightly coupled, brittle, untestable shape the style was supposed to prevent.

With well-defined contracts and the **Business Delegate** pattern, any layer can be replaced without affecting the others — e.g., the Presentation layer's UI framework can be swapped for a newer one. The **Fast-Lane Reader** is an early-2000s pattern that lets Presentation reach the database directly for simple reads, viable only when Business and Persistence are open layers.

## 3. The Architecture Sinkhole Antipattern

> **Architecture Sinkhole.** Requests pass through layers with no business logic performed.

A read of basic customer data goes Presentation → Business → Rules → Persistence → Database and back, with each layer doing nothing but pass-through. This wastes object instantiation, memory, and performance.

> **The 80/20 rule.** If roughly 20% of requests are sinkholes, the cost is acceptable. If 80% are, layered is the wrong style. Alternative: make all layers open and accept the increased difficulty managing change.

The sinkhole is the most common reason teams outgrow layered. It is also the strongest argument for considering a domain-partitioned style instead.

## 4. Data Topology and Cloud Fit

The default and overwhelming choice is a **single monolithic database** alongside the monolithic deployment. The Persistence layer handles object-relational mapping between the OO world and the relational world.

Cloud fit is **limited**. Because the architecture is monolithic and partitioned by layer, the only cloud options are to deploy one or more layers to a cloud provider. Communication latency between on-prem layers and cloud-hosted layers is usually problematic because most workflows traverse most layers.

## 5. When to Use and When Not To

**When to use:**

- Small, simple applications or websites.
- Tight budget and time constraints — investor-funded startups chasing *feasibility* (must ship *something* and accept that parts may be rewritten later).
- Teams still deciding whether a more complex style is warranted but must start. Keep code reuse minimal and inheritance trees shallow to ease the eventual migration.

**When not to use:**

- Large applications where maintainability, agility, testability, and deployability degrade as the monolith grows.
- Domains where every change is a *domain* change — layered's technical partition forces every change to ripple through every layer.
- Systems requiring high scalability, elasticity, fault tolerance, or independent deployment of subsystems.

## 6. Risks and Antipatterns

- **No fault tolerance.** A monolithic deployment with no architectural modularity: an out-of-memory error in any small part crashes the whole unit.
- **High MTTR.** Monolith startup ranges from \~2 minutes (small apps) to 15+ minutes (large ones), eroding mean-time-to-recover and availability.
- **Architecture Sinkhole antipattern** — see [§ 3](#3-the-architecture-sinkhole-antipattern).
- **Architecture by Implication / Accidental Architecture.** Teams that "just start coding" land in layered without an explicit choice. The decision should be deliberate.
- **DDD mismatch.** Domain-driven design fits poorly because every domain change touches every layer.

Governance has unusually strong tooling support — many structural-testing tools were originally built with the layered style in mind. ArchUnit (JVM) and NetArchTest (.NET) can enforce layer access rules at build time:

```
whereLayer("Service").mayOnlyBeAccessedByLayers("Controller")
whereLayer("Persistence").mayOnlyBeAccessedByLayers("Service")
```

These fitness functions catch the silent-bypass case where a UI developer skips a closed layer "for performance" and quietly undermines the architecture.

## 7. Architecture Characteristic Ratings

| Characteristic | Rating |
|---|---|
| Overall cost | ★★★★★ |
| Simplicity | ★★★★★ |
| Deployability | ★ |
| Elasticity | ★ |
| Evolutionary | ★ |
| Fault tolerance | ★ |
| Modularity | ★ |
| Performance | ★★★ |
| Reliability | ★★★ |
| Scalability | ★ |
| Testability | ★★ |

- **Strengths — cost and simplicity.** Layered avoids distributed complexity entirely. Easy to understand, cheap to build and maintain. Both ratings degrade quickly as the monolith grows.
- **Deployability and testability bottom out** because deployment is high-risk, infrequent, and ceremony-heavy — a three-line change requires redeploying the whole unit. Testability gets two stars rather than one because layers can be mocked or stubbed.
- **Elasticity and scalability are one star** due to monolithic deployment and absent architectural modularity. The architecture quantum is always 1.
- **Performance is three stars** — can be raised with caching and multithreading, hurt by the lack of inherent parallel processing, closed layering ceremony, and the sinkhole antipattern.

## 8. Examples

- **Operating systems** — Linux and Windows use layers (Hardware → Kernel → System Call Interface → User) for separation of concerns.
- **Networking (OSI / TCP-IP)** — Physical → Data Link → Network (IP) → Transport (TCP) → Application (SMTP/FTP/HTTP) layers delineate responsibility.
- **Feasibility-driven startups** — investor-funded teams that must ship something quickly, accepting rewrites later.

## When to Decompose This Style

Layered's defining signal that it has outgrown itself is the 80/20 sinkhole tipping past 50/50, paired with the team's struggle to keep up with domain-driven feature requests. Two pages walk the decomposition:

- [When to Decompose](decomposition/when-to-decompose.md) — the modularity drivers and the feasibility check that decide whether to pull apart the monolith at all.
- [Tactical vs. Strategic](decomposition/tactical-vs-strategic.md) — the decision tree between a tactical fork and a component-based decomposition once you commit to breaking it up.

## Sources

- [Fundamentals Ch 10: Layered Architecture Style](software/software-architecture/books/fundamentals-of-software-architecture/ch10_layered_architecture.md) (sole source — topology, open vs. closed layers, sinkhole antipattern, data topology, characteristic ratings, examples)


<!-- prev-next-nav -->

---

← [Styles Overview](software/software-architecture/styles/overview.md) | [Modular Monolith](software/software-architecture/styles/modular-monolith.md) →
