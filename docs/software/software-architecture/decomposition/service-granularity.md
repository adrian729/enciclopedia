# Service Granularity

> *The Hard Parts* Ch 7 is the sole source — *Fundamentals* introduces the modularity-vs-granularity distinction in passing (see [Modularity, Cohesion, Coupling](foundations/modularity-cohesion-coupling.md)) but doesn't take the next step into the equilibrium of disintegrators and integrators. This is the chapter where *The Hard Parts* most clearly earns its title: there is no best practice for service size. The architect's job here is **facilitation**, not pronouncement — name the trade-off, present the cost on each side, let the business decide. Sysops Squad's ticket-assignment-and-routing decision and the consolidated-Customer-Service decision are worked end-to-end as the ADR examples.

## Table of Contents

- [1. Modularity vs. Granularity — Restated](#1-modularity-vs-granularity--restated)
- [2. Granularity Disintegrators](#2-granularity-disintegrators)
- [3. Granularity Integrators](#3-granularity-integrators)
- [4. The Equilibrium](#4-the-equilibrium)
- [5. The Grains of Sand Antipattern](#5-the-grains-of-sand-antipattern)
- [6. The Architect as Facilitator](#6-the-architect-as-facilitator)
- [7. Sysops Squad — Two ADRs Worked End-to-End](#7-sysops-squad--two-adrs-worked-end-to-end)
- [Sources](#sources)

## 1. Modularity vs. Granularity — Restated

The two terms are not synonyms, and most distributed-system pain is granularity pain, not modularity pain.

| Term | Meaning |
|---|---|
| **Modularity** | *Breaking a system apart.* About logical separation — monolith → services. |
| **Granularity** | *How big each of those services is.* About service size, not service count. |

> *"Embrace modularity, but beware of granularity."* — Mark Richards

Modularity is the implicit characteristic every sustainable codebase needs (see [When to Decompose](decomposition/when-to-decompose.md)). Granularity is the parameter that goes wrong: too coarse and you get a distributed monolith; too fine and you get the *Grains of Sand* antipattern (§ 5).

Granularity is **about what a service does, not how big it is in lines of code.** Number of classes and LOC vary by coding style and don't compare across services. The two more objective signals, both still partially subjective:

- **Statement count** — a single complete action terminated by `;` or newline.
- **Public interfaces / operations** — the count of entrypoints the service exposes.

Right-sized services are not produced by picking a target number on either axis. They emerge from the **equilibrium** between two opposing sets of forces.

## 2. Granularity Disintegrators

The six drivers that justify breaking a service into smaller services. Each answers *when should I split?*

### 2.1. Service Scope and Function

Assess two dimensions: **cohesion** (how strongly the operations relate) and **size** (statements + public entrypoints). A Notification Service handling SMS, email, and postal letters has *strong* cohesion — one purpose: notify the customer — and is not a candidate for splitting on this driver. A service handling customer profile, preferences, and comments has *weak* cohesion (broader scope: customer) and should be split. The driver is related to but not identical to the single-responsibility principle, which is itself subjective at the service level.

### 2.2. Code Volatility

Also called **volatility-based decomposition**. Measure rate of change per area in version control. If postal-letter logic changes weekly while SMS and email change every six months, splitting Postal Letter into its own service shrinks the testing scope and deployment risk for the volatile part and avoids disrupting the stable parts. The signal is git history, not intuition — let the commit log identify volatile regions.

### 2.3. Scalability and Throughput

Different parts of a service often have wildly different throughput needs. The book's example: SMS at 220,000/min, email at 500/min, postal letter at 1/min. As one service, the slow paths must scale to the fast path's needs, hurting cost and **MTTS** (mean time to startup — the elasticity prerequisite). Splitting lets each scale independently.

### 2.4. Fault Tolerance

If one function (e.g., email) crashes repeatedly from out-of-memory while others are stable, isolating the offending function into its own service prevents it from taking down the rest.

> **Naming check on the split.** When splitting for fault tolerance, ensure the *leftover* service has a clear cohesive name. "Email + Other", "Email + Non-Email", "Email + SMS-Letter" all signal forced cohesion — the leftover is a grab-bag. `Email`, `SMS`, `Letter` as three distinct services is the only clean split.

### 2.5. Security

Sensitive data must be protected at the access path, not only at storage. A combined Customer Profile Service exposing both basic profile and credit-card maintenance lets an attacker who finds a profile entrypoint reach credit-card operations. Splitting credit-card maintenance into a dedicated service lets the entire smaller service be restricted at the security boundary.

### 2.6. Extensibility

When new contextual functionality is genuinely planned — e.g., a payment service expected to add reward points, ApplePay, SamsungPay, store credit — splitting payment methods into per-method services lets each new type be added/tested/deployed independently. *Apply only when extensibility is confirmed.* For areas like notification (means rarely expand), this driver doesn't apply, and applying it anyway produces speculative complexity.

| Disintegrator | Reason for applying |
|---|---|
| **Service scope** | Single-purpose services with tight cohesion |
| **Code volatility** | Agility — reduced testing scope and deployment risk |
| **Scalability** | Lower costs and faster responsiveness |
| **Fault tolerance** | Better overall uptime |
| **Security access** | Better security access control to certain functions |
| **Extensibility** | Agility — ease of adding new functionality |

## 3. Granularity Integrators

The four drivers that justify keeping services *together*. Each answers *when should I consolidate?*

### 3.1. Database Transactions

When a single unit of work must be atomic — new-customer registration writes profile and password together — separate services lose ACID guarantees. If the password write fails after the profile commits, you're left with messy compensating logic. Consolidate when business demands all-or-nothing. (The alternative is the saga patterns covered in [Transactional Sagas](distributed/transactional-sagas.md), and those have their own coupling cost.)

### 3.2. Workflow and Choreography

Interservice ("east-west") communication compounds three problems:

- **Fault tolerance is undone.** If Service C is a transitive dependency of A, B, D, E, every service goes down with C. Splitting for fault tolerance and then chaining services synchronously gains nothing.
- **Performance and responsiveness.** Five chained services at 300 ms latency each add 1,500 ms per request. Rule of thumb: **if 70%+ of requests need a workflow, consider consolidation; if only 30% do, splits may be fine.** Weight by criticality of the workflow-bound requests.
- **Reliability and data integrity.** Partial commits across chained services create inconsistent state and force compensating transactions or saga state tracking — see [Workflows & Orchestration](distributed/workflows-orchestration.md).

### 3.3. Shared Code

If services share a library of *domain* logic (not infrastructure cross-cutters like logging/auth/monitoring), every shared-library change forces coordinated change to all dependents. Consolidate when:

- **Specific shared domain functionality** is large — e.g., >40% of the collective codebase.
- **Frequent shared code changes** force frequent coordinated deployments.
- **Defects that cannot be versioned** must apply identically to every service at the same time.

### 3.4. Data Relationships

If splitting a service forces split tables that still reference each other across bounded contexts, the new services must call each other repeatedly to fetch their counterpart's data, reintroducing latency, fault-tolerance, and scalability issues. Often the database-table relationships make consolidation the right call. This integrator has the *fewest* counter-trade-offs because reorganizing entity relationships is rarely feasible — see [Data Decomposition](decomposition/data-decomposition.md) for the data-side view of the same force.

| Integrator | Reason for applying |
|---|---|
| **Database transactions** | Data integrity and consistency |
| **Workflow** | Fault tolerance, performance, and reliability |
| **Shared code** | Maintainability |
| **Data relationships** | Data integrity and correctness |

## 4. The Equilibrium

The disintegrators and integrators are not a checklist; they pull in opposite directions, and right-sized services sit at the equilibrium of those pulls. Every decision is a trade-off statement.

> **Frame it as one explicit question.** For example: *"Better agility through code-volatility isolation, or stronger data integrity through ACID?"*

The point of framing it as a single question is to *force* the trade-off into the open. Vague rhetoric like *"microservices should be small"* doesn't tell the team whether to optimize for volatility-isolation or for ACID — both can't win. The question format makes the choice unambiguous.

Disintegrator-driven splits are easy to justify in isolation (each driver looks like a clear win on its own dimension); integrators are what pull back. Without the integrators, the system slides into Grains of Sand.

## 5. The Grains of Sand Antipattern

> **Grains of Sand antipattern.** Services so fine-grained that every meaningful business operation requires choreographing many of them; the integrators are saying "consolidate" louder than the disintegrators are saying "split", but nobody is listening.

The symptom is the inverse of a Big Ball of Distributed Mud: instead of services that must deploy together, you have services that must *call* together for every workflow. Performance collapses (latency adds up), fault tolerance collapses (more services means more failure points), data integrity collapses (every transaction needs a saga). The fix is *consolidation* — the integrators in § 3 — applied until the equilibrium re-settles.

Both failure modes — Distributed Monolith and Grains of Sand — are *granularity* failures, not modularity failures. The system was decomposed correctly; the pieces were sized wrong. Sizing is the harder problem.

## 6. The Architect as Facilitator

> *The architect's job is to identify the trade-off, present the cost on each side, and let stakeholders weigh business value (security, time-to-market, performance, data integrity) against each other. The decision rests with the business, not the architect.*

This is the cleanest statement in *The Hard Parts* of the role shift introduced in [Trade-Off Analysis](foundations/tradeoff-analysis.md): the architect is not the *decider* on granularity; the architect is the *facilitator* of a decision the business owns. Why? Because the trade-offs being weighed — *agility vs. data integrity*, *security vs. atomic transactions*, *fault tolerance vs. performance* — are business-value trade-offs masquerading as technical ones. The architect's role is to make the choice legible:

1. **Identify** which disintegrators and integrators apply to this service.
2. **Present** the trade-off as a single sentence per pair: *"Splitting buys X, consolidation buys Y, you can't have both."*
3. **Record** the choice as an Architectural Decision Record (see [Architectural Decisions](practice/architectural-decisions.md)): context, decision, consequences.

The role is closer to a mediator's than a designer's. The output is an ADR, and the ADR's authority comes from the stakeholders who signed off, not from the architect's title.

## 7. Sysops Squad — Two ADRs Worked End-to-End

Hard Parts works the Sysops Squad scenario to anchor the granularity decision in concrete trade-offs. Two services were the running examples.

### 7.1. Ticket Assignment and Routing — Consolidate

Taylen wanted the volatile assignment algorithm (changed 2–3 times per month) split out from the more stable routing logic. The volatility disintegrator (§ 2.2) clearly applied. Trade-off analysis:

| Force | Says |
|---|---|
| Code volatility (disintegrator) | Split — assignment changes frequently, routing doesn't. |
| Workflow (integrator) | Consolidate — a failed route forces re-assignment; the two are tightly synchronously bound. |
| Scalability (integrator-ish) | Consolidate — both share scalability needs; splitting buys no scale gain. |
| Fault tolerance (integrator-ish) | Consolidate — splitting buys no fault-tolerance gain because they're synchronously coupled. |

Result: **consolidate** into a single service. Volatility is handled at the *namespace* level inside the single service rather than by service boundary. The ADR records this with the explicit consequence that every assignment-algorithm change re-tests both functions.

### 7.2. Customer Registration — Consolidate

Three options were on the table for handling customer registration:

1. One Customer service.
2. Four separate services — Profile, Credit Card, Password, Supported Product.
3. Two services split by sensitive vs. non-sensitive data.

The product owner required **all-or-nothing registration** — an ACID transaction. The database-transactions integrator (§ 3.1) immediately killed options 2 and 3 unless the team committed to sagas with compensating updates. The security expert pushed for option 2 or 3 on the security-access disintegrator (§ 2.5) — credit-card and password operations behind a stricter boundary.

The compromise: option 1 (single service), *on condition* that the **Tortoise security library** is used at both the API gateway and the service mesh. Security moves from *architecture* (separate deployment units) to *design* (a custom encryption library applied uniformly). The ADR records the decision with consequences: the consolidated service must scale as one unit and any change re-tests the whole service.

### 7.3. What the Two ADRs Show

Both decisions consolidated rather than split, but for opposite reasons — *workflow coupling* for ticket assignment, *atomic transactions* for customer registration. Neither outcome was predictable from a generic "microservices should be small" heuristic; both fell out of explicit trade-off statements between named disintegrators and integrators. That is the pattern: name the forces, frame the question, record the choice. The equilibrium isn't the same shape for any two services.

## Sources

- [The Hard Parts Ch 7: Service Granularity](software/software-architecture/books/software-architecture-the-hard-parts/ch07_service_granularity.md) (primary — modularity-vs-granularity restatement, six disintegrators, four integrators, the equilibrium framing, the architect-as-facilitator role, both Sysops Squad ADRs)


<!-- prev-next-nav -->

---

← [Tactical vs. Strategic Decomposition](software/software-architecture/decomposition/tactical-vs-strategic.md) | [Data Decomposition](software/software-architecture/decomposition/data-decomposition.md) →
