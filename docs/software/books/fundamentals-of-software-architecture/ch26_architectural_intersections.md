# Ch 26: Architectural Intersections

## Table of Contents

- [1. Why Intersections Matter](#1-why-intersections-matter)
- [2. Architecture and Implementation](#2-architecture-and-implementation)
- [3. Architecture and Infrastructure](#3-architecture-and-infrastructure)
- [4. Architecture and Data Topologies](#4-architecture-and-data-topologies)
- [5. Architecture and Engineering Practices](#5-architecture-and-engineering-practices)
- [6. Architecture and Team Topologies](#6-architecture-and-team-topologies)
- [7. Architecture and Systems Integration](#7-architecture-and-systems-integration)
- [8. Architecture and the Enterprise](#8-architecture-and-the-enterprise)
- [9. Architecture and the Business Environment](#9-architecture-and-the-business-environment)
- [10. Architecture and Generative AI](#10-architecture-and-generative-ai)

## 1. Why Intersections Matter

- **Architecture must be aligned, not just chosen** — selecting characteristics, picking a style, and leading the team isn't enough; the architecture must align with other facets of the technical and business environment. The authors call these alignments the *intersections of architecture*.
- **Nine intersections covered** — implementation, infrastructure, data topologies, engineering practices, team topologies, systems integration, the enterprise, the business environment, and generative AI.

## 2. Architecture and Implementation

- **"That's an implementation detail" is often the cause of failure** — for an architecture to work, the source code must be aligned with three things: operational concerns, internal structure, and constraints.
- **Operational-concerns misalignment example** — an order-entry system picks microservices for high scalability and elasticity; the team adds an *in-memory replicated cache* (Apache Ignite, Hazelcast) between `Order Placement` and `Inventory` for responsiveness; once instances multiply under real load, internal cache memory exhausts the VMs and the system crashes around 80,000 concurrent users. Architecture optimized for scalability and elasticity; implementation optimized for responsiveness and decoupling — both made good decisions for different goals.
- **Structural integrity** — logical components form the *logical architecture* (usually mirrored in directory or namespace structure); without governance, developers create directories as they please and the system becomes hard to maintain, test, deploy, and evolve.
- **Governance tooling for structure** — ArchUnit (Java), ArchUnitNet/NetArchTest (.NET), PyTestArch (Python), TSArch (TypeScript/JavaScript) keep the source-code structure aligned with the logical architecture.
- **Architectural constraints** — governing rules required to achieve goals (e.g., "all DB logic in the Persistence layer"; "Presentation must traverse all layers, even for simple queries"). If UI developers shortcut the database directly and backend developers fuse business and data logic, every DB change ripples everywhere and the layered architecture's promise evaporates.

## 3. Architecture and Infrastructure

- **The boundary has shifted into architecture** — pre-2000s, operations was outsourced and contractually distant. Modern styles like microservices freely leverage characteristics (e.g., elastic scale) that used to be purely operational, now handled through tighter collaboration with DevOps.
- **Pets.com sidebar — the origin of elastic scale** — the 1998 ecommerce site spent its budget on a sock-puppet mascot rather than infrastructure; the Christmas rush crushed it. Hard-won failures like this drove architects toward elastic-scale designs and toward attention to this intersection.
- **Misalignment is usually a communication failure** — architects often don't realize how much infrastructure influences scalability, responsiveness, fault tolerance, performance, availability, and elasticity.
- **Microservices was born of this collaboration** — its creators offloaded operational concerns to operations rather than reimplementing them inside the architecture (as orchestration-driven SOA had to), and laid the foundation of DevOps in the process.
- **Cloud can still misalign** — deploying services across regions or availability zones may cancel out the gains of in-memory replicated or distributed caches; co-locating services, containers, or Kubernetes Pods on the same VM boosts performance but hurts scalability, fault tolerance, availability, and elasticity.

## 4. Architecture and Data Topologies

- **Three database topology types** — *monolithic*, *distributed domain-based*, and *distributed database-per-service*. Microservices typically requires database-per-service to maintain a strict bounded context; service-based architecture is more flexible.
- **Match the database's superpowers to the architecture's** — in *Software Architecture: The Hard Parts*, the authors rate six DB types (relational, key-value, document, columnar, graph, NoSQL). Scalability and elasticity are superpowers for microservices, EDA, and space-based — and also for key-value and columnar DBs, making them strong amplifiers.
- **Data structure** — relational data fits relational DBs; key-value pairs in a relational DB is a misalignment that hurts both. Given mixed structures (relational, document for JSON event payloads, key-value), prefer polyglot persistence.
- **Read/write priority** — write-heavy workloads favor columnar; read-heavy favor key-value, document, or graph; balanced workloads favor relational and NewSQL. Misaligning this factor leads to poor performance.

## 5. Architecture and Engineering Practices

- **Process vs. engineering practices** — *processes* are how teams form, run meetings, and organize workflow (Waterfall, Scrum, XP, Lean, Crystal); *engineering practices* are the process-agnostic techniques (XP, CI, CD, TDD) used to develop and release software. *Software engineering* is the union.
- **Estimation is the Achilles' heel** — civil engineers can predict structural change far more accurately than software engineers; traditional estimation can't accommodate software's exploratory nature.
- **Iterative process is a better fit** — Waterfall against microservices generates massive friction; Agile shines when migrating between styles thanks to tight feedback loops, the *Strangler Pattern*, and feature toggles.
- **Style imposes practice** — microservices assumes automated provisioning, testing, and deployment. Building it on a manual operations group with little testing fails predictably.
- **Evolutionary architecture and fitness functions** — Neal Ford's *Building Evolutionary Architectures* introduces *architectural fitness functions* (metrics, unit tests, monitors, chaos engineering) to objectively assess and protect characteristics over time. Example: *agility* (composite of maintainability, testability, deployability) can be measured to flag misalignment between practice and architecture.

## 6. Architecture and Team Topologies

- **Partitioning must match** — *domain-partitioned* teams (cross-functional, end-to-end ownership of a domain area) align with domain-partitioned styles like microservices; *technically partitioned* teams (UI, backend, shared services, DB) align with layered; business-function plus data-synchronization teams align with space-based.
- **Misalignment guarantees struggle** — if team topology doesn't match the architecture, even simple changes become hard and business goals slip.

## 7. Architecture and Systems Integration

- **Systems rarely live in isolation** — every external dependency raises questions about availability, scale, and responsiveness compared to the calling system.
- **Underweighting integration breaks the architecture** — static and dynamic coupling between systems undermines scalability, responsiveness, and agility. Consider communication protocols, contract types, characteristic compatibility, and whether each system's architectural quantum is preserved.

## 8. Architecture and the Enterprise

- **Architecture lives inside an enterprise** — the collection of systems and products in a company, division, or department comes with security standards, platforms, technologies, and documentation/diagramming standards.
- **Ignore them and the architecture is scrapped** — even technically excellent solutions get labeled failed *one-offs* and discarded when they conflict with enterprise practices.

## 9. Architecture and the Business Environment

- **Domain-to-architecture isomorphism** — align the architecture with where the business is: aggressive cost-cutting doesn't fit microservices or space-based (both expensive); aggressive M&A growth doesn't fit monolithic styles that can't evolve.
- **Known unknowns vs. unknown unknowns** — Donald Rumsfeld's distinction maps onto software: *known unknowns* are gaps you know exist; *unknown unknowns* are surprises no one anticipated. Big Design Up Front fails because it cannot design for unknown unknowns. Per Mark: *all architectures become iterative because of unknown unknowns. Agile just recognizes this and does it sooner.*
- **Plan for change with the right characteristics** — portability, scalability, evolvability, and adaptability make architecture more flexible; evolutionary and iterative practices help an architecture survive change.
- **Residuality theory** — Barry O'Reilly (*Residues: Time, Change, and Uncertainty in Software Architecture*, Leanpub 2024) treats business changes as *stressors* and architectural responses as *residues*; accumulated residues eventually start to absorb unknown changes, pushing the architecture into a critical state from complexity theory.

## 10. Architecture and Generative AI

- **Incorporate Gen AI via abstraction and modularity** — be able to swap one LLM for another, add guardrails (rails), and evaluate results (evals). Example: a job-search company uses an LLM to anonymize résumés (reducing bias by hiding demographics); accuracy must be measurable across LLMs. Tools like *Langfuse* provide the necessary observability.
- **Gen AI as architect assistant — limited so far** — LLMs (e.g., Copilot) handle deterministic coding tasks well, but as of early 2025 they rarely give the right answer to "microservices or space-based?" because *everything in software architecture is a trade-off* and LLMs lack the contextual *wisdom* required.
- **Promising tools** — *Thoughtworks Haiven* interprets architecture diagrams and answers questions about bottlenecks or issues; other efforts translate PlantUML or pseudolanguage descriptions into executable ArchUnit governance code. The space is moving fast.
