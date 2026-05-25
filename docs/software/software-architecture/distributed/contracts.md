# Contracts

> *The Hard Parts* (Ch 13) is the only source — the chapter sets contracts up as a *fourth* dimension that cuts across the three dynamic-coupling axes from [Modularity, Cohesion, Coupling](foundations/modularity-cohesion-coupling.md). The strict-to-loose spectrum, consumer-driven contracts, and the stamp-coupling math all come from this chapter. Hard Parts works the Sysops Squad scenario to settle a mixed-strictness contract strategy: tight where the semantics are tight, loose where deployment latency forces it.

## Table of Contents

- [1. Contracts as the Orthogonal Dimension](#1-contracts-as-the-orthogonal-dimension)
- [2. The Strict-to-Loose Spectrum](#2-the-strict-to-loose-spectrum)
- [3. Trade-Offs Between Strict and Loose](#3-trade-offs-between-strict-and-loose)
- [4. Consumer-Driven Contracts](#4-consumer-driven-contracts)
- [5. Stamp Coupling](#5-stamp-coupling)
- [6. The Sysops Squad Mixed Strategy](#6-the-sysops-squad-mixed-strategy)
- [Sources](#sources)

## 1. Contracts as the Orthogonal Dimension

[Modularity, Cohesion, Coupling](foundations/modularity-cohesion-coupling.md) frames dynamic coupling around three axes: **communication** (sync ↔ async), **consistency** (atomic ↔ eventual), **coordination** (orchestrated ↔ choreographed). Contracts are *orthogonal* to all three — every decision on the three axes is then constrained by the contract style the team picked.

> **Contract, broadly defined** — the format used by parts of an architecture to convey information or dependencies. Includes transitive dependencies, internal and external integration points, caches, and any other communication among parts.

The chapter's framing rule: **implementation comes after type.** Architects choose strict vs. loose first; gRPC, REST, JSON, and the rest are how to implement that decision, not what to decide. Fitness functions then enforce whichever style was chosen — *governance is part of the contract*, not a separate concern.

The reason contracts get their own page rather than living inside [Workflows & Orchestration](distributed/workflows-orchestration.md) or [Distributed Data Access](distributed/distributed-data-access.md) is that every other decision in this section assumes one of these contract styles. Replicated Caching needs a contract for the cache replication channel; sagas need contracts for inter-service messages; the [Data Product Quantum](distributed/analytical-data-and-mesh.md) needs a contract to its cooperator service.

## 2. The Strict-to-Loose Spectrum

Contracts run on a spectrum, not a binary:

| Position | Examples | Properties |
|---|---|---|
| **Very strict** | RMI, gRPC | Names, types, ordering, and all details enforced; no ambiguity; RPC-style frameworks default here. |
| **Strict** | Schema-validated JSON | `$schema`, `properties`, `required` enforce types and required fields. |
| **Middle** | REST, GraphQL | Resource-oriented (REST) or aggregation-oriented (GraphQL); structural changes that don't break resources are absorbed. |
| **Loose** | Bare name-value pairs (JSON, YAML) | No metadata, no types; maximum decoupling; the lingua franca of integration. |

### 2.1. Strict Contracts

Strict contracts require adherence to names, types, ordering, and all other details, leaving no ambiguity. RPC frameworks mimic internal method calls and default to strict semantics — the producer's method signature *is* the contract.

### 2.2. Schema-Augmented JSON

Even ostensibly loose JSON can be tightened by referencing a schema. A `$schema` declaration with `properties` and `required` arrays enforces types and required fields at validation time. Schema augmentation is the cheap way to get most of the safety of a strict contract without leaving JSON.

### 2.3. REST

REST models *resources* rather than method endpoints. Adding fields to a resource (e.g., adding `engines` to an airplane parts resource) does not break existing seat queries — clients only consume the fields they asked for. The contract is the resource shape; structural change is absorbed when the consumer doesn't look at the new field.

### 2.4. GraphQL

GraphQL is used for read-only aggregated data instead of costly orchestration calls. Different consumers (Wishlist, Customer Profile) can request *only* the slice they need. The contract is the schema, but consumers select against it dynamically.

### 2.5. Loose Contracts

Bare name-value pairs — no metadata, no types — yield maximum decoupling at the cost of contract certainty. Two services agreeing to exchange JSON like `{"name": "Pat", "id": 42}` have a contract, but neither side can prove anything about the other's behavior without running it.

## 3. Trade-Offs Between Strict and Loose

| Dimension | Strict Contracts | Loose Contracts |
|---|---|---|
| **Coupling** | Tight | Highly decoupled |
| **Fidelity** | Guaranteed by schema | Must be enforced via fitness functions |
| **Build-time verification** | Easy (type tools) | Limited; requires consumer-driven contracts |
| **Documentation** | Excellent (typed parameters) | Sparse |
| **Versioning** | Required; supports gradual change but risks integration nightmares | Easier evolution; semantic changes still need coordination |
| **Best fit** | Domains where contract changes must be coordinated tightly | Microservices and other highly decoupled architectures |

**Versioning cuts both ways.** A clear deprecation strategy is an asset; supporting too many versions becomes liability. Strict contracts force the versioning conversation early; loose contracts defer it but don't eliminate it.

**Semantic coupling cannot be reduced by implementation.** Looser contracts only loosen *implementation* coupling — the workflow steps the business actually requires don't go away. This is the same lemma from [Workflows & Orchestration](distributed/workflows-orchestration.md): you can move the coupling, not remove it.

## 4. Consumer-Driven Contracts

Microservices typically prefer loose contracts (name-value pairs) so each bounded context can evolve internally and switch tech stacks without affecting collaborators. The cost: contract fidelity drops. The recovery technique:

> **Consumer-driven contracts** invert the push model into a pull model. Each consumer hands the provider a *contract test* specifying the fields and shapes it requires; the provider runs those tests in CI and keeps them green.

### 4.1. How It Works

1. Wishlist Service needs `name` from Customer Profile. Wishlist writes a contract test: "GET /profile/42 returns JSON with a string field `name`."
2. Wishlist hands the test to the Customer Profile team.
3. Customer Profile adds the test to its CI pipeline.
4. Whenever Customer Profile changes, the test runs. A breaking change (renaming `name` → `displayName`) breaks the build before deployment.

### 4.2. The Dual-Mechanism Solution

Name-value pairs + consumer-driven contracts give **loose coupling** *and* **contract fidelity**, simulating stricter verification (including value-range checks that schemas can't express).

| Trade-off | Detail |
|---|---|
| **Advantages** | Loose coupling between services; variability in strictness (one consumer can be strict, another loose, against the same provider); evolvable contracts. |
| **Disadvantages** | Requires engineering maturity — teams must actually run and respect the contract tests; uses two interlocking mechanisms instead of one. |

The maturity requirement is real. Consumer-driven contracts fail in teams that don't have CI discipline; the tests get marked `@Ignore` after the first false-positive and become decoration. Tooling helps (Pact, Spring Cloud Contract) but does not substitute for the practice.

This is the same instruction from [Trade-Off Analysis](foundations/tradeoff-analysis.md)'s snake-oil defense: *convert opinion into an automated check*. The provider's claim that *"this change is non-breaking"* becomes a green test, not a Slack message.

## 5. Stamp Coupling

> **Stamp coupling** — passing a large data structure between services where each service interacts with only a small portion of it. Common when an industry-standard XML or JSON document is shared.

### 5.1. The Anti-Pattern Form

The architect "over-specifies" the contract just in case. Wishlist only needs `name` from Profile, but the contract specifies the *whole* Profile document. Now any unrelated change to Profile (e.g., the `state` field changes type) breaks Wishlist even though Wishlist never reads `state`.

**The bandwidth fallacy** that hides the cost. One of the *Fallacies of Distributed Computing*: bandwidth is infinite. It isn't. The chapter's math:

| Scenario | Calculation |
|---|---|
| Over-coupled contract: 500 KB Profile document, 2,000 req/s | 2,000 × 500 KB = **1,000,000 KB/s = ~1 GB/s** |
| Trimmed to just `name`: ≈100 bytes, 2,000 req/s | 2,000 × 100 B = **≈200 KB/s** |

The over-coupled version is consuming ~5,000× more bandwidth than the trimmed version, almost entirely for fields nobody reads. At scale, the bandwidth cost is real money, and the change-coupling cost is real production incidents. Trim the contract.

### 5.2. The Legitimate Form

Stamp coupling has a legitimate use, called out in [Workflows & Orchestration](distributed/workflows-orchestration.md) — when scalability forces choreography over orchestration, stamp coupling can carry workflow status, transactional state, and error info alongside domain data. Each service updates its slice and forwards the document.

**Atomicity caveat for the legitimate form.** For transactional consistency in such a workflow, services must rebroadcast the contract to previously visited services to restore atomic consistency — every service holds the latest contract version. This adds back the coordination cost that choreography was supposed to remove.

### 5.3. Trade-offs

| Aspect | Detail |
|---|---|
| **Advantage** | Enables complex workflows in choreographed solutions; one message carries both data and workflow state. |
| **Disadvantages** | Artificially high coupling between collaborators in the anti-pattern form; bandwidth pressure at scale; field changes ripple to consumers that don't read those fields. |

The same shape — *one big document passed everywhere* — is either a tool or an anti-pattern depending on whether the team chose it deliberately. The diagnostic: *would every consumer survive renaming a field nobody reads?* If yes, it is stamp coupling done well. If a single bystander breaks, it is over-coupling.

## 6. The Sysops Squad Mixed Strategy

Hard Parts works the Sysops Squad scenario to show that *the right contract style varies per integration point* — even inside one workflow.

**Three contract decisions across the ticket workflow:**

| Edge | Decision | Reason |
|---|---|---|
| Orchestrator ↔ Ticket Management | **Strict** | Semantics are tightly coupled — new ticket types must propagate to assignment logic together; loose contracts would let drift creep in. |
| Orchestrator ↔ Ticket Assignment | **Strict** | Same reason; assignment must see every ticket type. |
| Orchestrator ↔ Notification Service | **Loose** | Notification info evolves slowly; brittle coupling would add no value. |
| Orchestrator ↔ Survey Service | **Loose** | Same — survey contracts change at a different cadence than ticketing core. |
| Orchestrator ↔ Expert Mobile App | **Loose (with extension mechanism)** | Public app store approval delays releases; the contract needs flex even though the *semantics* are as tight as Assignment. |

**The mobile-app exception** is the architecturally interesting one. Semantically the mobile app is as tight as Assignment — the expert sees every ticket type — so the textbook answer is strict. But the *deployment latency* is forced by an external constraint (app-store review). The team chose loose with an extension mechanism, placing validation logic in both the orchestrator and the mobile app, with a note in the ADR: *revisit if the app store allows continuous deployment*.

**ADR outcome.** Loose contract for the Sysops Squad expert mobile app, with an extension mechanism for short-term flexibility, validation logic in both ends, and an explicit revisit trigger. The decision is deliberate, not default — the architecture acknowledges that contract decisions are local, not global.

The general lesson: there is no single "microservices contract style." There is per-edge contract style chosen with the same trade-off matrix that picks every other dimension. Strict where the semantics are tightly coupled and the parties can deploy together. Loose where decoupling buys evolvability or sidesteps an external constraint. Consumer-driven contracts where loose coupling needs the safety net of automated verification. See [Trade-Off Analysis](foundations/tradeoff-analysis.md) for the three-step method that runs this decision per edge.

## Sources

- [The Hard Parts Ch 13: Contracts](software/software-architecture/books/software-architecture-the-hard-parts/ch13_contracts.md) (primary — strict vs. loose spectrum, consumer-driven contracts, stamp coupling, bandwidth math, Sysops Squad mixed strategy)


<!-- prev-next-nav -->

---

← [Transactional Sagas](software/software-architecture/distributed/transactional-sagas.md) | [Analytical Data & Data Mesh](software/software-architecture/distributed/analytical-data-and-mesh.md) →
