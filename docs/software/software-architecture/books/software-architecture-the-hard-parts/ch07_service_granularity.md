# Ch 7: Service Granularity

## Table of Contents

- [1. Modularity vs granularity](#1-modularity-vs-granularity)
- [2. Granularity Disintegrators](#2-granularity-disintegrators)
- [3. Granularity Integrators](#3-granularity-integrators)
- [4. Finding the right balance](#4-finding-the-right-balance)
- [5. Sysops Squad: ticket assignment and customer registration](#5-sysops-squad-ticket-assignment-and-customer-registration)

## 1. Modularity vs granularity

- **Modularity** — breaking a system into separate parts. **Granularity** — the size of those parts. Most distributed-system pain comes from granularity, not modularity.
- **Granularity is about what a service does, not how big it is in lines of code** — number of classes and LOC are bad proxies because they vary by coding style.
- **Better metrics** — count of **statements** in a service (a single complete action terminated by `;` or newline) and the count of **public interfaces/operations** the service exposes. Both are still partially subjective, but more objective than lines of code.
- **Two opposing forces** — **Granularity Disintegrators** answer "When should I break a service apart?"; **Granularity Integrators** answer "When should I put services back together?" Equilibrium between the two yields right-sized services.

## 2. Granularity Disintegrators

The six drivers that justify breaking a service into smaller services:

- **Service scope and function** — assess two dimensions: **cohesion** (how strongly the operations relate) and **size** (statements + public entrypoints). A Notification Service handling SMS, email, and postal letters has *strong* cohesion (one purpose: notify the customer) and is not a candidate. A service handling profile, preferences, and comments has *weak* cohesion (broader scope: customer) and should be split. Related to but not equivalent to the single-responsibility principle, which is itself subjective at the service level.
- **Code volatility** — also called *volatility-based decomposition*. Measure rate of change per area in version control. If postal-letter logic changes weekly while SMS and email change every six months, splitting Postal Letter into its own service shrinks testing scope and deployment risk for the volatile part and avoids disrupting the stable parts.
- **Scalability and throughput** — different parts of a service may have wildly different throughput needs. Example: SMS at 220,000/min, email at 500/min, postal letter at 1/min. As one service, the slow paths must scale to the fast path's needs, hurting cost and MTTS (mean time to startup). Splitting lets each scale independently.
- **Fault tolerance** — if one function (e.g., email) crashes from out-of-memory while others are stable, isolating the offending function prevents it from taking down the rest. **Naming check:** when splitting, ensure the leftover service has a clear cohesive name. "Email + Other"/"Email + Non-Email"/"Email + SMS-Letter" all signal forced cohesion; `Email`, `SMS`, `Letter` is the only good split.
- **Security** — sensitive data must be protected at the access path, not only at storage. A combined Customer Profile Service exposing both basic profile and credit-card maintenance lets an attacker who finds an entrypoint reach credit-card operations. Splitting credit-card maintenance into a dedicated service lets the entire service be restricted at the security boundary.
- **Extensibility** — when new contextual functionality is genuinely planned (e.g., a payment service expected to add reward points, ApplePay, SamsungPay, store credit), splitting payment methods into per-method services lets each new type be added/tested/deployed independently. Apply only when extensibility is confirmed; for areas like notification (means rarely expand), this driver doesn't apply.

## 3. Granularity Integrators

The four drivers that justify keeping services together:

- **Database transactions** — when a single unit of work must be atomic (e.g., new-customer registration writes profile and password together), separate services lose ACID guarantees. If the password write fails after the profile commits, you're left with messy compensating logic. Consolidate when business demands all-or-nothing.
- **Workflow and choreography** — interservice ("east-west") communication compounds three problems:
  - **Fault tolerance is undone** — if Service C is a transitive dependency of A, B, D, E, every service goes down with C. Splitting for fault tolerance and then chaining services synchronously gains nothing.
  - **Performance/responsiveness** — five chained services at 300 ms latency each add 1500 ms per request. Rule of thumb: if 70%+ of requests need a workflow, consider consolidation; if only 30% do, splits may be fine. Weight by criticality of the workflow-bound requests.
  - **Reliability and data integrity** — partial commits across chained services create inconsistent state and force compensating transactions or saga state tracking.
- **Shared code** — if services share a library of *domain* logic (not infrastructure cross-cutters like logging/auth/monitoring), every shared-library change forces coordinated change to all dependents. Consolidate when:
  - **Specific shared domain functionality** is large (e.g., >40% of collective codebase).
  - **Frequent shared code changes** force frequent coordinated deployments.
  - **Defects that cannot be versioned** must apply identically to every service at the same time.
- **Data relationships** — if splitting a service forces split tables that still reference each other across bounded contexts, the new services must call each other repeatedly to fetch their counterpart's data, reintroducing latency, fault-tolerance, and scalability issues. Often the database table relationships make consolidation the right call. This integrator has the fewest counter-trade-offs because reorganizing entity relationships is rarely feasible.

## 4. Finding the right balance

Summary tables of disintegrator and integrator drivers:

| Disintegrator | Reason for applying |
|---|---|
| **Service scope** | Single-purpose services with tight cohesion |
| **Code volatility** | Agility (reduced testing scope and deployment risk) |
| **Scalability** | Lower costs and faster responsiveness |
| **Fault tolerance** | Better overall uptime |
| **Security access** | Better security access control to certain functions |
| **Extensibility** | Agility (ease of adding new functionality) |

| Integrator | Reason for applying |
|---|---|
| **Database transactions** | Data integrity and consistency |
| **Workflow** | Fault tolerance, performance, and reliability |
| **Shared code** | Maintainability |
| **Data relationships** | Data integrity and correctness |

- **Trade-off statements** — frame disintegrator vs integrator as one explicit question to a product owner or business sponsor (e.g., "Better agility through code-volatility isolation, or stronger data integrity through ACID?"). The decision rests with the business, not the architect.
- **Architect's job is facilitation** — identify the trade-off, present the cost on each side, and let stakeholders weigh business value (security, time-to-market, performance, data integrity) against each other.

## 5. Sysops Squad: ticket assignment and customer registration

- **Ticket assignment + routing → single service** — Taylen wanted the volatile assignment algorithm split out (changed 2–3 times/month). Trade-off analysis showed assignment and routing are tightly synchronously bound (a failed route forces re-assignment), share scalability needs, and gain no fault tolerance from being split. ADR records consolidation; volatility is handled by separate namespaces inside the single service. Consequence: every assignment-algorithm change retests both functions.
- **Customer registration → single consolidated Customer Service** — three options were on the table: one Customer service, four separate services (Profile, Credit Card, Password, Supported Product), or two services split by sensitive vs nonsensitive data. The product owner required all-or-nothing registration (ACID transaction), which kills the multi-service options. The security expert accepted a single service on condition the **Tortoise security library** is used at both API gateway and service mesh. ADR records the decision; security is handled by **design** (custom encryption library) rather than **architecture** (separate deployment units). Consequences: the consolidated service must scale as one unit and any change re-tests the whole service.
