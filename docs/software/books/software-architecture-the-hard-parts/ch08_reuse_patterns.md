# Ch 8: Reuse Patterns

## Table of Contents

- [1. The reuse problem in distributed systems](#1-the-reuse-problem-in-distributed-systems)
- [2. Code Replication](#2-code-replication)
- [3. Shared Library](#3-shared-library)
- [4. Shared Service](#4-shared-service)
- [5. Sidecars and Service Mesh](#5-sidecars-and-service-mesh)
- [6. Comparing the four reuse patterns](#6-comparing-the-four-reuse-patterns)
- [7. When does reuse add value?](#7-when-does-reuse-add-value)
- [8. Sysops Squad sagas](#8-sysops-squad-sagas)

## 1. The reuse problem in distributed systems

- **Reuse is unavoidable** — common business code (formatters, calculators, validators, auditing) and infrastructure code (security, logging, metrics) are pervasive; monoliths solve it by importing class files, distributed architectures cannot.
- **DRY vs WET** — microservices culture promotes "share nothing!" and the WET acronym (*Write Every Time* / *Write Everything Twice*) as a counter to *Don't Repeat Yourself* abuse.
- **Four techniques to manage shared code** — Code Replication, Shared Library, Shared Service, Sidecars/Service Mesh; each has distinct trade-offs.

## 2. Code Replication

- **Definition** — shared code is copied into each service repository, eliminating sharing entirely; preserves the bounded context.
- **Origin** — popularized in the early microservices era to chase a "share nothing architecture"; rarely a good first choice today.
- **Sweet spot** — highly static one-off code such as Java annotations or C# attributes (e.g., a `@ServiceEntrypoint` marker) that contain no logic and are unlikely to ever change.
- **Migration use** — a `Utility.cs` class can be replicated so each service evolves it for its own context (similar to the *tactical forking* technique from Chapter 3).
- **Risk** — bug fixes or change propagation are extremely difficult; code drifts inconsistently across services and there are no versioning capabilities.

## 3. Shared Library

- **Definition** — an external artifact (JAR, DLL) bound to services at compile time; the most common reuse technique in distributed architectures.
- **Granularity trade-off** — coarse-grained libraries simplify dependency management but force every consumer to retest/redeploy on any change; fine-grained libraries scope changes tightly but produce a "distributed monolith" of dependency relationships.
- **Authors' guidance** — favor change control over dependency management; carve relatively static functionality (formatters, security) into their own libraries to isolate version churn.
- **Versioning Strategies — always version!** — versioning provides backward compatibility and agility; one consumer can adopt a new `Validation.jar` without forcing the other nine to retest.
- **Versioning is the ninth fallacy of distributed computing** — communication of changes, deprecation policy, and version rollouts are far harder than they look.
- **Custom vs global deprecation** — custom deprecation per library matches each library's change rate (e.g., 2–3 versions for stable `Security.jar`, 10 versions for volatile `Calculators.jar`) at the cost of tracking overhead; global deprecation (e.g., keep last four versions for everything) is simpler but causes churn.
- **Avoid `LATEST`** — services pinning to the LATEST version risk breaking on emergency hot deployments; explicit pinning is mandatory.
- **Best fit** — homogeneous environments with low-to-moderate change rates; compile-time binding leaves performance, scalability, and fault tolerance unaffected.

## 4. Shared Service

- **Definition** — shared functionality lives in a separately deployed service consumed at runtime via remote calls; uses *composition*, not inheritance.
- **Change is a double-edged sword** — a single redeploy of the shared service propagates the change to all consumers, but a bad change is now a runtime change that can take down the system.
- **Versioning via API endpoints** — patterns like `app/1.4/discountcalc?orderid=123` work for REST but are subjective (when do you bump?), require consumer reconfiguration, and break down across messaging/gRPC protocols.
- **Performance** — every call adds network latency and (when endpoints are secured) security latency; gRPC and asynchronous messaging (request/reply via correlation ID) help mitigate.
- **Scalability** — the shared service must scale in lockstep with every consumer that uses it.
- **Fault tolerance** — if the shared service goes down, every consumer is non-operational until it recovers.
- **Best fit** — highly polyglot environments and shared functionality with high volatility, where compile-time binding is impractical.

## 5. Sidecars and Service Mesh

- **Problem framed** — microservices favor *duplicate over couple* for domain code, but operational concerns (monitoring, logging, auth, circuit breakers) benefit from coupling and consistency.
- **Hexagonal heritage** — Cockburn's *Ports and Adaptors* pattern separates domain logic from infrastructure logic; the **Sidecar** pattern updates that idea for microservices, with data and transactionality kept inside the domain core (per DDD).
- **Sidecar mechanics** — the operational portion of every service is extracted into a sidecar component owned by a shared infrastructure team or shared across teams; the sidecar attaches to the service like a motorcycle sidecar.
- **Service Mesh** — when every service includes the sidecar (enforced by fitness functions), the sidecars interconnect via a service plane to form a mesh that supports unified dashboards, scale control, and cross-cutting governance.
- **Orthogonal Coupling** — two parts of an architecture with distinct purposes that must still intersect; operational concerns are orthogonal to domain concerns, and the Sidecar pattern is an *orthogonal reuse pattern* that decorates behavior across the architecture, similar to the GoF Decorator pattern.
- **Trade-offs** — provides consistent infrastructure coupling and unified governance but requires one sidecar per platform and the sidecar can grow large/complex.
- **Best fit** — operational coupling, security/observability standardization, polyglot governance; *not* for domain classes (e.g., do not put `Customer` or `Address` in the sidecar).

## 6. Comparing the four reuse patterns

| Pattern | Binding | Best for | Key advantage | Key disadvantage |
|---------|---------|----------|---------------|------------------|
| **Code Replication** | Copy into each repo | Highly static one-off code | Preserves bounded context; no sharing | No versioning; near-impossible to propagate fixes |
| **Shared Library** | Compile-time | Homogeneous stacks; low-to-moderate change | Versioned changes; no runtime impact | Dependency management; deprecation/communication complexity |
| **Shared Service** | Runtime | Polyglot stacks; high code volatility | No code duplication; good agility for changes | Latency, scalability lockstep, fault-tolerance, runtime risk |
| **Sidecars / Service Mesh** | Runtime (per service) | Operational/cross-cutting concerns | Consistent infrastructure; unified governance | One sidecar per platform; size growth |

## 7. When does reuse add value?

- **Two prerequisites for useful reuse** — abstraction (how candidates are discovered) *and* slow rate of change (what makes them useful).
- **Reuse is derived via abstraction but operationalized by slow rate of change** — operating systems and external frameworks reuse well because their cadence is well understood; internal domain capabilities and fast-moving frameworks do not.
- **Centralized Customer Service anti-pattern** — orchestration-driven SOA's drive to consolidate every domain's view of an entity (e.g., Customer) into a single service produces brittleness: the entity grows complex enough to handle every scenario, and any change ripples throughout the architecture.
- **Reuse via Platforms** — modern target of reuse; each domain capability is exposed via a platform with a well-defined API, hiding implementation details and limiting breaking changes through encapsulation and contracts.

## 8. Sysops Squad sagas

- **Common Infrastructure Logic** — duplicated logging in libraries and services led to sidecar adoption. Decision: a shared infrastructure team owns the sidecar; it provides Monitoring, Logging, Service Discovery, Authentication, Authorization. Domain classes (e.g., `Address`, `Customer`) must not go in the sidecar; shared utility code (e.g., `JSONtoXML`) goes in only when used by at least half the teams.
- **Shared Domain Functionality** — for common ticketing database logic across Ticket Creation, Ticket Assignment, and Ticket Completion services, a shared library was chosen over a shared data service. The repository history showed minimal change rate, so versioned shared libraries gave better performance, scalability, and fault tolerance with acceptable change risk; service teams manage their own database connection pools.
