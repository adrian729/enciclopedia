# Ch 4: Architectural Characteristics Defined

## Table of Contents

- [1. What Counts as an Architecture Characteristic](#1-what-counts-as-an-architecture-characteristic)
- [2. Implicit Versus Explicit Characteristics](#2-implicit-versus-explicit-characteristics)
- [3. Operational Characteristics](#3-operational-characteristics)
- [4. Structural Characteristics](#4-structural-characteristics)
- [5. Cloud Characteristics](#5-cloud-characteristics)
- [6. Cross-Cutting Characteristics](#6-cross-cutting-characteristics)
- [7. ISO Categories](#7-iso-categories)
- [8. Trade-Offs and Least Worst Architecture](#8-trade-offs-and-least-worst-architecture)

**Two activities define structural design.** *Architectural characteristics analysis* (this chapter) identifies the system's *capabilities*; *logical component design* (Ch 8) defines the system's *behavior* from the problem domain. They can run in any order and converge at a critical join point.

## 1. What Counts as an Architecture Characteristic

A requirement qualifies as an **architecture characteristic** only if it meets **all three** criteria — drawn as an interlocking triangle in the book:

1. **Specifies a nondomain design consideration** — describes *how* and *why* the system must behave, not *what* it does. Performance levels rarely appear in requirements docs; "prevent technical debt" never does.
2. **Influences some structural aspect of the design** — security can be a code-hygiene concern (good enough in a monolith) *or* an architectural concern (hardened service boundaries in microservices). Scalability is almost always structural — no clever code makes a monolith scale past a wall.
3. **Is critical or important to application success** — each characteristic costs design effort, dev effort, and complexity. Strive for the *fewest*, not the most.

**Terminology note.** *Non-functional requirements* is the legacy term (born alongside 1970s function-point analysis); the authors reject it as self-denigrating. *Quality attributes* implies after-the-fact assessment. The authors prefer **architecture characteristics** — the system's *capabilities* (vs. the domain, which is the system's *behavior*).

## 2. Implicit Versus Explicit Characteristics

| Kind | Where it comes from | Examples |
|---|---|---|
| **Implicit** | Architect's domain knowledge; rarely in requirements | Availability, reliability, security, modularity; low-latency for HFT firms; data integrity for medical devices |
| **Explicit** | Stated in requirements documents | Specific concurrent-user counts, response-time SLAs, regulatory mandates |

- The triangle's three sides *interact* — that's why architects spend so much time talking about **trade-offs**.

## 3. Operational Characteristics

How well the system runs in production. Heavy overlap with operations and DevOps.

| Term | Definition |
|---|---|
| **Availability** | How much of the time the system must be up; 24/7 implies fast-recovery mechanisms |
| **Continuity** | Disaster-recovery capability |
| **Performance** | How well the system performs under stress, peak load, frequency, response times |
| **Recoverability** | How quickly the system must come back online after disaster — backups, duplicate hardware |
| **Reliability/safety** | Whether the system is mission-critical or fail-safe; lives or large sums on the line. A spectrum, not binary |
| **Robustness** | Ability to handle errors and boundary conditions (e.g., loss of internet or power) |
| **Scalability** | Ability to perform as users or requests increase |

## 4. Structural Characteristics

Code-quality and code-organization concerns the architect owns (or shares).

| Term | Definition |
|---|---|
| **Configurability** | How easily end users can change config through interfaces |
| **Extensibility** | How well the architecture accommodates additions to existing functionality |
| **Installability** | How easy it is to install on all needed platforms |
| **Leverageability/reuse** | Extent to which common components are reusable across products |
| **Localization** | Multi-language support on entry/query screens |
| **Maintainability** | How easy it is to apply changes and enhance the system |
| **Portability** | Ability to run on more than one platform (e.g., Oracle and SAP DB) |
| **Upgradeability** | How easy and quick it is to upgrade servers and clients to a new version |

## 5. Cloud Characteristics

New in the second edition — most systems now touch the cloud in some capacity.

| Term | Definition |
|---|---|
| **On-demand scalability** | Cloud provider's ability to dynamically scale resources up |
| **On-demand elasticity** | Cloud provider's flexibility under spiky demand; closely related to scalability |
| **Zone-based availability** | Provider's ability to separate resources by computing zones for resilience |
| **Region-based privacy and security** | Provider's legal ability to store data per country/region (data-residency law compliance) |

## 6. Cross-Cutting Characteristics

Concerns that don't fit a category but constrain design.

| Term | Definition |
|---|---|
| **Accessibility** | Access for all users, including those with disabilities (colorblindness, hearing loss) |
| **Archivability** | Constraints on archiving or deleting data after a period |
| **Authentication** | Ensuring users are who they claim to be |
| **Authorization** | Ensuring users access only the functions they're entitled to |
| **Legal** | GDPR, Sarbanes-Oxley, regional regulations, build/deploy mandates, reservation rights |
| **Privacy** | Hiding transactions even from internal staff (DBAs, network architects) |
| **Security** | DB/network encryption, remote-access authentication, etc. |
| **Supportability** | Logging and other facilities required for debugging and tech support |
| **Usability/achievability** | Training required for users to achieve their goals |

- **Beware of overlapping or imprecise terms.**
  - **Interoperability vs. compatibility** — interoperability implies published, documented APIs; compatibility implies industry/domain standards.
  - **Learnability** has two definitions — how easily *users* learn the software, vs. how the system itself learns its environment via ML.
  - **Availability vs. reliability** — IP is *available* but not *reliable* (packets may arrive out of order); TCP layers reliability on top.

## 7. ISO Categories

The ISO publishes a capability-organized list. The authors quote it (with terminology updates) but reject the inclusion of *Functional Suitability* — that describes domain requirements, not architecture characteristics.

| Category | Subcharacteristics |
|---|---|
| **Performance efficiency** | Time behavior, resource utilization, capacity |
| **Compatibility** | Coexistence, interoperability |
| **Usability** | Appropriateness recognizability, learnability, user-error protection, accessibility |
| **Reliability** | Maturity, availability, fault tolerance, recoverability |
| **Security** | Confidentiality, integrity, nonrepudiation, accountability, authenticity |
| **Maintainability** | Modularity, reusability, analyzability, modifiability, testability |
| **Portability** | Adaptability, installability, replaceability |

- **The list is necessarily incomplete.** No universal standard exists; new characteristics keep appearing as the ecosystem evolves. Each organization should establish its own vocabulary.
- **DDD's ubiquitous language** is the recommended antidote to terminology drift across an organization.

## 8. Trade-Offs and Least Worst Architecture

Why architects must support *only* a few characteristics:

- **Each characteristic has a cost** — design effort, dev effort, ongoing maintenance, often structural support.
- **Characteristics are synergistic** — pushing one almost always disturbs another. Tightening *security* (encryption, indirection) typically degrades *performance*. Like a helicopter's controls, every input affects every other.
- **Definitions are ambiguous** — without a ubiquitous language, organizations argue past each other.
- **The category set keeps growing** — operations was once a "black box"; microservices forced architects and ops together. Architecture is entangling with more of the organization over time.

**Never strive for the *best* architecture; aim for the *least worst* architecture.**

- **Trying to support every characteristic** produces generic, unwieldy designs that solve no problem well.
- **Iterate.** Make architecture as easy to change as possible — Agile's lesson holds at every level, including architecture. Stop stressing about the perfect first attempt.
