# Analyzing Risk

> *Fundamentals* (Ch 22) is the source: the risk-assessment matrix, the scaled-up risk assessment, direction of risk, the **risk storming** collaborative exercise, and the Nursing Hotline worked example. *The Hard Parts* doesn't have an equivalent chapter; it relies on the same trade-off mindset but doesn't operationalize risk.

## Table of Contents

- [1. Why Risk Needs a Matrix](#1-why-risk-needs-a-matrix)
- [2. The Risk-Assessment Matrix](#2-the-risk-assessment-matrix)
- [3. Scaling Up to a Risk Assessment](#3-scaling-up-to-a-risk-assessment)
- [4. Direction of Risk](#4-direction-of-risk)
- [5. Risk Storming](#5-risk-storming)
- [6. Worked Example: Nursing Hotline](#6-worked-example-nursing-hotline)
- [Sources](#sources)

## 1. Why Risk Needs a Matrix

Risk is otherwise subjective: one architect's "high" is another's "medium." Without a shared scale, the team negotiates feelings instead of facts. The **architecture risk-assessment matrix** makes risk measurable enough to compare, prioritize, and present to stakeholders.

The matrix doesn't claim precision. It claims **shared vocabulary** — two architects who multiply impact and likelihood the same way can debate the *inputs* rather than the conclusion.

## 2. The Risk-Assessment Matrix

Two dimensions, each rated low / medium / high on a 1–3 scale; multiply for the cell value.

| Impact / Likelihood | Low (1) | Medium (2) | High (3) |
|---|---|---|---|
| **Low (1)** | 1 (low) | 2 (low) | 3 (medium) |
| **Medium (2)** | 2 (low) | 4 (medium) | 6 (high) |
| **High (3)** | 3 (medium) | 6 (high) | 9 (high) |

Bands:

- **1–2 — low risk (green).**
- **3–4 — medium risk (yellow).**
- **6–9 — high risk (red).**

Use shading as well as colour so the matrix survives grayscale rendering and colour-blindness.

### 2.1. Order of Consideration

Consider **impact first** and likelihood second. Impact is usually the more knowable input: losing a central database stops the system, period. Likelihood is harder to estimate and easier to argue about.

> **Unknown-likelihood rule** — if you can't confirm the likelihood, **use high (3) until confirmed.** It's safer to over-state risk and refine downward than to under-state and discover the gap in production.

### 2.2. Worked Example

*Primary central database availability.* Impact is high (3) because losing it stops the system; likelihood is low (1) thanks to clustered HA servers. 3 × 1 = 3 — medium risk. The matrix gives this kind of single-line answer for every component-criterion pair.

## 3. Scaling Up to a Risk Assessment

A **risk assessment** is a summarized report of overall risk against meaningful criteria within a context.

| Axis | Convention |
|---|---|
| **Criteria** (rows) | Architecture characteristics that matter most for this system — scalability, elasticity, data integrity, availability. Critical characteristics make better criteria than generic ones like "performance." |
| **Contexts** (columns) | Domains or subdomains across the top — *customer registration*, *catalog checkout*, *order fulfillment*, *order shipping*. Service-level granularity is usually too fine and misses inter-service risk. |
| **Cells** | The multiplied risk score for that criterion in that context. |

### 3.1. Reading the Totals

A row total tells you which **criterion** is the highest-risk system-wide. A column total tells you which **context** is the highest-risk area. In an ecommerce example *Fundamentals* walks through:

- *Data integrity* totals 17 across contexts — highest-risk criterion.
- *Availability* totals 10 — lowest-risk criterion.
- *Customer registration* — highest-risk context.
- *Order fulfillment* — lowest-risk context.

The totals point at where mitigation money should land.

### 3.2. Presenting to Stakeholders

When presenting, hide low and medium cells; leave only the red ones visible. Stakeholders aren't there to scan a noisy heat map — they're there to act on the signal. Improving the signal-to-noise ratio of the message is a real part of the architect's job.

## 4. Direction of Risk

A static risk assessment is a snapshot. It doesn't tell you whether a yellow cell is becoming green or red. **Direction of risk** addresses that.

Continuous measurement via [fitness functions](foundations/architecture-characteristics.md) lets each criterion's trajectory be tracked. Symbol convention:

| Symbol | Meaning |
|---|---|
| Right-side-up triangle | Risk is **worsening** — tip points up to the higher number. |
| Upside-down triangle | Risk is **easing**. |
| Circle | Risk is **static**. |

Always include a key when using symbols — see [Diagramming](practice/diagramming.md) for the broader rule.

A typical reading might be: *data integrity worsening for catalog checkout, order fulfillment, and order shipping (possible DB issue); security and availability improving for customer registration and catalog checkout.* That sentence is a much sharper input to an iteration plan than a static heat map.

## 5. Risk Storming

A single architect can miss risk areas; few architects know every part of a system. **Risk storming** is a collaborative exercise to determine architectural risk within a specific dimension — usually one criterion (e.g. elasticity) or one context (e.g. the diagnostics gateway).

**Participants** — multiple architects plus senior developers and tech leads. Developers add an implementation perspective and learn the architecture by participating.

**Inputs** — a comprehensive or contextual architecture diagram, distributed in advance by the **facilitator** (the architect running the session).

Three phases — identification (individual), consensus (collaborative), mitigation (collaborative).

### 5.1. Phase 1: Identification

**Individual, unbiased work** so participants don't influence each other.

1. Facilitator sends the architecture diagram, the criterion/context to analyze, and session logistics.
2. Each participant uses the risk matrix to score risks individually.
3. Each writes risk numbers on small green (1–2), yellow (3–4), or red (6–9) sticky notes.

Restrict scope when possible — one criterion or one context per session. If multiple dimensions must be covered together, write the criterion next to the score on each sticky so the wall stays legible.

### 5.2. Phase 2: Consensus

Large printed diagram on a wall (or a large electronic display); participants place sticky notes on the relevant area. Notes that all agree on need no discussion; discrepancies do.

Typical patterns in the discussion:

- **A high outlier among mediums.** One participant rates a load balancer high (6); two others rate it medium (3). Discussion: impact is high (system inaccessible if LB fails) but likelihood is low (clustering). Consensus settles at medium.
- **A lone high that nobody else flagged.** One participant rates a service high (9), based on prior outages under similar load. Without that participant, no one would have flagged the risk — *this is the exact value risk storming adds.*
- **The "what's a Redis cache?" rating.** A participant rates Redis cache high (9); on questioning, asks what Redis is. Unknown technologies automatically get the highest rating.

> **Two firm rules of risk storming:**
>
> 1. **Unknown or unproven technologies automatically get rated 9.** The matrix isn't usable for tech the team doesn't know.
> 2. **Always include developers.** Discovering that a developer doesn't know a technology is itself valuable risk information — the architect may swap the technology or budget for training.

### 5.3. Phase 3: Mitigation

Reduce or eliminate the consensus risks. Changes range from light refactoring (adding a queue for backpressure) to redesigning a whole subsystem.

**Cost matters** — mitigation usually costs money, so include business stakeholders with authority to weigh cost against risk. Example negotiation: clustering a database to mitigate availability risk costs $50,000; the business owner refuses. The architect proposes splitting it into two domain databases for $16,000, still reducing risk; stakeholders agree. The point isn't the number; it's that the trade-off is now visible to the person who controls the budget.

### 5.4. User-Story Risk Analysis

The same matrix applies to **user stories** during grooming. Score each story's *impact if not completed in the iteration* against *likelihood of not completing it*. Flag high-risk stories for closer tracking and prioritization; aggregate into an overall iteration-risk score.

## 6. Worked Example: Nursing Hotline

A call-center support system where nurses advise patients on medical conditions. Three web UIs (self-service, nurse, admin), `Call Accepter` and `Call Router` services, a central database, a diagnostics-system API gateway, four backend services (`Case Management`, `Nurse Profile Management`, `Medical Records Interface`, `Diagnostics Engine Interface`). REST throughout except proprietary protocols to external systems.

**Constraints** — a third-party diagnostics engine handles about 500 req/s; 250 concurrent nurses; hundreds of thousands of self-service patients; HIPAA-compliant medical records (nurses only); spikes during cold/flu/COVID outbreaks. Critical characteristics: **availability, elasticity, security.**

### 6.1. Availability

Identified risks:

- Central database — high (6); impact 3, likelihood 2.
- `Diagnostics Engine` — high (9); impact 3, likelihood unknown so 3.
- `Medical Records Interface` — low (2); not required to determine outcomes.

**Mitigation — split the database.** Separate clustered nurse-profile database from single-instance case-notes database. If case-notes DB fails, nurses can write notes manually and `Call Router` keeps working. Bonus: better security separation for case notes.

**External system mitigation via SLAs.** Research published SLAs for the third-party services: `Diagnostics Engine` SLA 99.99% (52.60 min/yr); `Medical Records Interface` SLA 99.90% (8.77 hr/yr). Sufficient evidence to remove these from the risk register; SLAs are added to the architecture diagram.

### 6.2. Elasticity

Identified risk — `Diagnostics Engine` interface unanimously rated high (9). Self-service patients plus nurses overwhelm a 500 req/s engine over REST, especially during outbreaks.

Three mitigations, each addressing a different facet:

| Mitigation | What it fixes |
|---|---|
| **Async queues** between API gateway and diagnostics interface | Backpressure — protects the engine from overload. Doesn't fix user wait times. |
| **Ambulance pattern** — two channels prioritizing nurse requests over self-service | Latency for the priority channel. Doesn't address overall volume. |
| **Diagnostics Outbreak Cache Server** — caches outbreak/flu-related questions so they never reach the engine | Reduces total volume, freeing the engine for unusual symptoms. |

### 6.3. Security

Identified risk — single API gateway rated high (6). Impact 3 (admin or self-service patients reaching medical records would breach HIPAA), likelihood 2. The facilitator initially rated this low (2) but participants convinced them otherwise.

**Mitigation — separate API gateways per user type.** Admin, self-service, and nurse traffic each get their own gateway; non-nurse calls structurally cannot reach `Medical Records Interface`.

### 6.4. Outcome

The original architecture is significantly modified by the risk-storming sessions, addressing availability, elasticity, and security. The systemic point is that single-architect review would have missed each of these — splitting the DB, the cache server, and the per-user-type gateways all emerged from cross-perspective discussion.

**Cadence** — risk storming continues throughout the system's lifecycle. Frequency depends on rate of change, refactoring efforts, and incremental development; common practice is to risk-storm specific dimensions after a major feature or at the end of every iteration. The exercise is cheap; the failures it catches are expensive.

## Sources

- [Fundamentals Ch 22: Analyzing Architecture Risk](software/software-architecture/books/fundamentals-of-software-architecture/ch22_analyzing_architecture_risk.md) (primary — the risk matrix, risk assessment layout, direction of risk, risk storming phases, Nursing Hotline)


<!-- prev-next-nav -->

---

← [Architectural Decisions](software/software-architecture/practice/architectural-decisions.md) | [Diagramming](software/software-architecture/practice/diagramming.md) →
