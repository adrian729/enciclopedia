# Ch 10: Layered Architecture Style

## Table of Contents

- [1. Topology](#1-topology)
- [2. Layers of Isolation: Open vs. Closed](#2-layers-of-isolation-open-vs-closed)
- [3. Adding Layers and the Architecture Sinkhole Antipattern](#3-adding-layers-and-the-architecture-sinkhole-antipattern)
- [4. Data Topologies and Cloud Considerations](#4-data-topologies-and-cloud-considerations)
- [5. Common Risks](#5-common-risks)
- [6. Governance](#6-governance)
- [7. Team Topology Considerations](#7-team-topology-considerations)
- [8. Style Characteristics](#8-style-characteristics)
- [9. When to Use and When Not to Use](#9-when-to-use-and-when-not-to-use)
- [10. Examples and Use Cases](#10-examples-and-use-cases)

## 1. Topology

- **n-tiered de facto standard** — *layered* (a.k.a. *n-tiered*) is one of the most common styles, the de facto standard for many legacy applications because of its simplicity, familiarity, and low cost.
- **Antipatterns it falls into** — *Architecture by Implication* and *Accidental Architecture*: when developers "just start coding" without choosing a style, they typically end up with layered.
- **Logical layers** — components are arranged in horizontal layers, each performing a specific role. Most layered architectures use four standard layers: **Presentation, Business, Persistence, Database**. Smaller apps may use three; larger ones five or more. Some combine Business and Persistence when SQL is embedded in business components.
- **Physical (deployment) variants** — three common shapes:
  - Presentation + Business + Persistence in one deployment unit; Database external.
  - Presentation in its own unit; Business + Persistence in a second unit; Database external.
  - All four layers (including Database) in one deployment, e.g., mobile apps with embedded/in-memory databases or on-prem packaged products.
- **Separation of concerns** — each layer is an abstraction owning specific responsibility. Presentation handles UI/browser logic; Business handles rules; Persistence handles data access. Each layer is ignorant of the inner workings of the others, which lets developers leverage their technical expertise. The trade-off is a lack of *holistic agility* — the system's overall ability to respond quickly to change.
- **Technically partitioned** — layered is a *technically partitioned* architecture (vs. *domain-partitioned*). Any single domain (e.g., "customer") is spread across Presentation, Business, Rules, Services, and Database layers, making domain changes hard. As a result, DDD does not fit layered well.

## 2. Layers of Isolation: Open vs. Closed

- **Closed layer** — a request cannot skip it; flow must go through the layer immediately beneath. Closed layers protect *layers of isolation*.
- **Open layer** — a request can bypass it. Useful for shared utilities or to mitigate the sinkhole antipattern.
- **Layers of isolation concept** — changes in one layer don't impact others as long as contracts hold; layers are independent with little knowledge of each other's internals. To preserve isolation, layers in the main request flow must be closed; otherwise changes to Persistence would ripple into Business *and* Presentation, producing tightly coupled, brittle architectures.
- **Replaceability benefit** — with isolation and well-defined contracts (and the *Business Delegate* pattern), any layer can be replaced without affecting the others — e.g., swapping the Presentation layer's UI framework for a newer one.
- **Fast-Lane Reader** — early-2000s pattern for letting Presentation reach the database directly for simple reads; only viable when Business and Persistence are open layers.

## 3. Adding Layers and the Architecture Sinkhole Antipattern

- **Why add layers** — to enforce architectural rules. If the Business layer holds shared utility classes (date/string utilities, auditing, logging) that the Presentation layer must not use, splitting them into a new **Services layer** *architecturally* prevents Presentation from reaching them.
- **Mark the new layer open** — otherwise the Business layer would be forced to traverse Services to reach Persistence. Marked open, Business can either use Services or skip it on the way down.
- **Document open vs. closed** — failing to communicate which layers are open or closed (and why) usually produces tightly coupled, brittle architectures that are hard to test, maintain, and deploy.
- **Architecture sinkhole antipattern** — requests pass through layers with no business logic performed. A read of basic customer data goes Presentation → Business → Rules → Persistence → Database and back, with each layer doing nothing but pass-through. This wastes object instantiation, memory, and performance.
- **80/20 rule** — if ~20% of requests are sinkholes, fine; if 80%, layered is the wrong style. Alternative: make all layers open and accept the increased difficulty in managing change.

## 4. Data Topologies and Cloud Considerations

- **Monolithic database** — traditionally a single, monolithic database alongside the monolithic deployment. The Persistence layer often handles object-relational mapping between OO languages and the set-based world of relational databases.
- **Cloud fit is limited** — being monolithic and partitioned by layer, cloud options reduce to deploying one or more layers via a cloud provider. Communication latency between on-prem servers and the cloud can be problematic since most workflows traverse most layers.

## 5. Common Risks

- **No fault tolerance** — monolithic deployment with no architectural modularity: one out-of-memory in any small part crashes the whole application unit.
- **High MTTR** — *mean time to recover* (and overall availability) suffer because monolith startup times range from ~2 minutes for small apps to 15+ minutes for large ones.

## 6. Governance

- **Strong tooling fit** — many structural-testing tools were originally built with the layered style in mind, so governance is unusually well-supported here.
- **ArchUnit fitness function** — an example fitness function defines layers (`Controller`, `Service`, `Persistence` — package-name based via `..pkg..`) and access rules (`whereLayer("Service").mayOnlyBeAccessedByLayers("Controller")`, `whereLayer("Persistence").mayOnlyBeAccessedByLayers("Service")`), enabling automated enforcement of open/closed relationships at build time.

## 7. Team Topology Considerations

Layered is generally independent of team topology and works with any configuration:

- **Stream-aligned teams** — small, self-contained, single-flow nature fits stream-aligned teams that own the journey end-to-end through every layer.
- **Enabling teams** — high modularity by technical concern lets specialists experiment with one layer (e.g., trying a new UI library in Presentation) without affecting others.
- **Complicated-subsystem teams** — each layer's specific task suits complicated-subsystem teams. The Persistence layer is a natural hook for analytics teams that need operational data without disturbing other layers.
- **Platform teams** — can leverage the high modularity and the many tools available for layered systems. Their challenge is the general monolith problem: as features pile up, database connections, memory, performance, or concurrency eventually strain.

## 8. Style Characteristics

| Characteristic | Rating |
|---|---|
| Overall cost | 5 stars |
| Simplicity | 5 stars |
| Deployability | 1 star |
| Elasticity | 1 star |
| Evolutionary | 1 star |
| Fault tolerance | 1 star |
| Modularity | 1 star |
| Performance | 3 stars |
| Reliability | 3 stars |
| Scalability | 1 star |
| Testability | 2 stars |

- **Strengths: cost and simplicity** — being monolithic, layered avoids distributed-architecture complexity; it is simple, easy to understand, and cheap to build and maintain. Ratings degrade quickly as the monolith grows.
- **Deployability and testability** — deployment is high risk, infrequent, ceremony-heavy; a three-line change requires redeploying the whole unit. Testability gets two stars (rather than one) because layers can be mocked or stubbed.
- **Elasticity and scalability** — both one star due to monolithic deployment and absent architectural modularity. The architecture quantum is always 1.
- **Performance** — three stars; can be raised with caching and multithreading but suffers from lack of inherent parallel processing, closed layering, and the architecture sinkhole antipattern.

## 9. When to Use and When Not to Use

- **When to use** — small, simple applications or websites; tight budget/time constraints; situations where the architect is still deciding whether a more complex style is warranted but must start. Keep code reuse minimal and inheritance trees shallow to ease later migration.
- **When not to use** — large applications and systems where maintainability, agility, testability, and deployability degrade as the monolith grows. Use a more modular style instead.

## 10. Examples and Use Cases

- **Operating systems** — Linux and Windows use layers (Hardware → Kernel → System Call Interface → User) for the same reason: separation of concerns.
- **Networking OSI/TCP-IP** — Physical → Data Link → Network (IP) → Transport (TCP) → Application (SMTP/FTP/HTTP) layers delineate responsibility.
- **Feasibility-driven choice** — layered's simplicity makes it common for teams chasing the *feasibility* characteristic — investor-funded startups that must ship something quickly, accepting that parts may be rewritten later for different capabilities.
