# Ch 13: Contracts

## Table of Contents

- [1. Why contracts cut across architecture](#1-why-contracts-cut-across-architecture)
- [2. Strict vs Loose Contracts](#2-strict-vs-loose-contracts)
- [3. Trade-offs between Strict and Loose Contracts](#3-trade-offs-between-strict-and-loose-contracts)
- [4. Contracts in microservices](#4-contracts-in-microservices)
- [5. Stamp Coupling](#5-stamp-coupling)
- [6. Sysops Squad: managing ticketing contracts](#6-sysops-squad-managing-ticketing-contracts)

## 1. Why contracts cut across architecture

- **Contract, broadly defined** — *the format used by parts of an architecture to convey information or dependencies*; encompasses transitive dependencies, internal/external integration points, caches, and any other communication among parts.
- **Cross-cutting dimension** — communication, consistency, and coordination form the three-axis space of dynamic coupling (Ch. 2 and 12); contracts act like time orthogonal to those axes, affecting every other decision.
- **Implementation comes after type** — architects choose strict vs loose first; gRPC, REST, JSON, and the rest are how to implement, not what to decide. Fitness functions then enforce whichever style is chosen.

## 2. Strict vs Loose Contracts

- **Spectrum, not binary** — contracts run from very strict (RMI, gRPC) through schema-validated JSON, to REST and GraphQL, ending at bare name-value pairs in JSON or YAML.
- **Strict Contracts** — require adherence to names, types, ordering, and all other details, leaving no ambiguity. RPC-style frameworks mimic internal method calls and default to strict semantics.
- **Schema-augmented JSON** — even ostensibly loose JSON can be tightened by referencing a schema (`$schema`, `properties`, `required`) to enforce types and required fields.
- **REST** — models resources rather than method/procedure endpoints; adding fields to a resource (e.g., engines on an airplane parts resource) does not break existing seat queries.
- **GraphQL** — used for read-only aggregated data instead of costly orchestration calls; different consumers (Wishlist, Customer Profile) can request only the slice they need.
- **Loose Contracts** — bare name-value pairs (no metadata, no types) yield maximum decoupling, the lingua franca of integration, at the cost of contract certainty.

## 3. Trade-offs between Strict and Loose Contracts

| Dimension | Strict Contracts | Loose Contracts |
|-----------|------------------|-----------------|
| Coupling | Tight | Highly decoupled |
| Fidelity | Guaranteed by schema | Must be enforced via fitness functions |
| Build-time verification | Easy (type tools) | Limited; requires consumer-driven contracts |
| Documentation | Excellent (typed parameters) | Sparse |
| Versioning | Required; supports gradual change but risks integration nightmares | Easier evolution; semantic changes still need coordination |
| Best fit | Domains where contract changes must be coordinated tightly | Microservices and other highly decoupled architectures |

- **Versioned cuts both ways** — a clear deprecation strategy is an asset; supporting too many versions becomes liability.
- **Semantic coupling cannot be reduced by implementation** — looser contracts only loosen *implementation* coupling.

## 4. Contracts in microservices

- **Aspirational decoupling** — microservices typically prefer loose contracts (name-value pairs) so each bounded context can evolve internally and switch tech stacks without affecting collaborators.
- **Consumer-driven contracts** — invert the push model into a pull model: each consumer hands the provider a contract test specifying the fields and shapes it requires; the provider runs those tests in CI and keeps them green.
- **Dual-mechanism solution** — name-value pairs plus consumer-driven contracts give loose coupling *and* contract fidelity, simulating stricter verification (including value ranges schemas don't express).
- **Trade-offs of consumer-driven contracts** — *Advantages*: loose coupling between services, variability in strictness, evolvable. *Disadvantages*: requires engineering maturity (teams must run and respect contract tests), and uses two interlocking mechanisms instead of one.

## 5. Stamp Coupling

- **Definition** — passing a large data structure between services where each service interacts with only a small portion of it; common when an industry-standard XML/JSON document is shared.
- **Over-coupling** — anti-pattern when the architect over-specifies fields "just in case." Wishlist needs only `name` from Profile, but contracting on the whole Profile makes any unrelated field change (e.g., `state`) break Wishlist.
- **Bandwidth fallacy** — falling for the *"bandwidth is infinite"* fallacy of distributed computing. 2,000 req/s × 500 KB payloads = 1,000,000 KB/s; trimming the contract to just `name` collapses overhead to ~200 bytes/s, a perfectly reasonable 400 KB.
- **Workflow management (legitimate use)** — when scalability forces choreography over orchestration, stamp coupling can carry workflow status, transactional state, and error info alongside domain data; each service updates its slice and forwards the document.
- **Atomicity caveat** — for transactional consistency in such a workflow, services must rebroadcast the contract to previously visited services to restore atomic consistency.
- **Trade-offs** — *Advantage*: enables complex workflows in choreographed solutions. *Disadvantages*: artificially high coupling between collaborators; bandwidth pressure at scale.

## 6. Sysops Squad: managing ticketing contracts

- **Tight contracts where semantics are tightly coupled** — orchestrator-to-Ticket Management and orchestrator-to-Ticket Assignment use strict contracts; new ticket types must propagate to assignment logic together.
- **Loose contracts where change is slow** — Notification Service and Survey Service get looser contracts because the information evolves slowly and brittle coupling adds no value.
- **Mobile app exception** — though the expert mobile app is semantically as tight as assignment, a loose name-value contract is chosen because public app store approvals delay releases.
- **ADR outcome** — loose contract for the Sysops Squad expert mobile app, with an extension mechanism for short-term flexibility, validation logic placed in the orchestrator and the mobile app, revisitable if the app store allows continuous deployment.
