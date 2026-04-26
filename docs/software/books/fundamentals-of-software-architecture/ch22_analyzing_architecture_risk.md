# Ch 22: Analyzing Architecture Risk

## Table of Contents

- [1. Risk Matrix](#1-risk-matrix)
- [2. Risk Assessments](#2-risk-assessments)
- [3. Direction of Risk](#3-direction-of-risk)
- [4. Risk Storming](#4-risk-storming)
- [5. User-Story Risk Analysis](#5-user-story-risk-analysis)
- [6. Risk-Storming Use Case: Nursing Hotline](#6-risk-storming-use-case-nursing-hotline)

## 1. Risk Matrix

- **Why a matrix** — risk is otherwise subjective: one architect's "high" is another's "medium." The architecture **risk-assessment matrix** makes risk more measurable.
- **Two dimensions** — *overall impact* and *likelihood of occurrence*. Each rated low (1), medium (2), or high (3); multiply for the cell value.
- **Bands** — 1–2 low risk (green), 3–4 medium risk (yellow), 6–9 high risk (red). Use shading for grayscale rendering and color blindness.

| Impact / Likelihood | Low (1) | Medium (2) | High (3) |
|---|---|---|---|
| **Low (1)** | 1 (low) | 2 (low) | 3 (medium) |
| **Medium (2)** | 2 (low) | 4 (medium) | 6 (high) |
| **High (3)** | 3 (medium) | 6 (high) | 9 (high) |

- **Order of consideration** — when qualifying risk, consider impact first and likelihood second. If unsure of the likelihood, use high (3) until confirmed.
- **Worked example: primary central database availability** — impact is high (3) because losing it stops the system; likelihood is low (1) thanks to clustered HA servers. 3 × 1 = 3 (medium risk).

## 2. Risk Assessments

- **A risk assessment** — a summarized report of overall architecture risk against meaningful criteria within a context (services, subdomain areas, or domain areas).
- **Architecture characteristics make great criteria** — analyze the characteristics that matter most for the system (e.g., scalability, elasticity, data integrity), not generic ones (e.g., performance) that don't. The most critical characteristics make the best risk-assessment criteria.
- **Layout** — criteria down the left, contexts across the top; cells contain the multiplied risk score.
- **Granularity** — domain or subdomain works well; service-level is usually too fine and ignores risk in inter-service communication and coordination.
- **Reading the totals — ecommerce ordering example:**
  - *Data integrity* totals 17 across contexts — highest-risk criterion.
  - *Availability* totals 10 — lowest-risk criterion.
  - *Customer registration* — highest-risk context.
  - *Order fulfillment* — lowest-risk context.
- **Filtering for stakeholders** — when presenting, hide low/medium cells (noise) to highlight the high cells (signal). Improves the signal-to-noise ratio of the message.

## 3. Direction of Risk

- **Snapshot limitation** — a static assessment doesn't show whether risks are improving or worsening.
- **Continuous measurement via fitness functions** (Ch 6) lets you track each criterion's trajectory and observe trends.
- **Symbol convention** — right-side-up triangle = risk getting worse (tip points up to higher number); upside-down triangle = risk easing (tip points down); circle = static. Always include a key when using symbols.
- **Example reading** — data integrity worsening for catalog checkout, order fulfillment, and order shipping (possible DB issue); security and availability improving for customer registration and catalog checkout.

## 4. Risk Storming

- **Why** — a single architect can miss risk areas; few architects know every part of a system. **Risk storming** is a collaborative exercise to determine architectural risk within a specific dimension (context or criterion).
- **Participants** — multiple architects plus senior developers and tech leads. Developers add an implementation perspective and learn the architecture in the process.
- **Three phases** — identification (individual), consensus (collaborative), mitigation (collaborative).
- **Inputs** — a comprehensive or contextual architecture diagram. The *facilitator* (the architect running the session) distributes updated diagrams beforehand.

### 4.1. Phase 1: Identification

- **Individual, unbiased work** so participants don't influence each other.
- **Steps:**
  1. Facilitator sends the architecture diagram, the criterion/context to analyze, and session logistics.
  2. Each participant uses the risk matrix to score risks individually.
  3. Each writes risk numbers on small green (1–2), yellow (3–4), or red (6–9) sticky notes.
- **Restrict scope when possible** — analyzing a single criterion or context per session keeps focus and avoids confusion. If multiple dimensions must be covered together, write the criterion next to the score on each sticky.

### 4.2. Phase 2: Consensus

- **Setup** — large printed diagram on the wall (or large electronic display); participants place sticky notes on the relevant area.
- **Goal** — reach consensus on each identified risk level. Notes that all agree on need no discussion; discrepancies do.
- **Worked example readings:**
  - Two participants rated the Elastic Load Balancer medium (3); one rated it high (6). Discussion: high impact (system inaccessible if LB fails) but low likelihood (clustering) — consensus settles at medium (3).
  - One participant alone rated Push Expansion Servers high (9), based on prior outages under similar load. Without that participant, no one would have flagged the risk — illustrates the value of risk storming.
  - One participant rated Redis cache high (9); on questioning, they ask "What's a Redis cache?" Unknown technologies automatically get high (9).
- **Unknown-tech rule** — always assign unproven or unknown technologies the highest risk rating (9), since the risk matrix cannot be used for this criterion or context.
- **Why include developers** — discovering that a developer doesn't know a technology is itself valuable risk information; the architect may swap technologies or budget for training.

### 4.3. Phase 3: Risk Mitigation

- **Goal** — reduce or eliminate the consensus risks. Changes range from architectural refactoring (e.g., adding a queue for backpressure) to redesigning the architecture.
- **Cost matters** — mitigation usually costs money, so include business stakeholders with authority to weigh cost against risk.
- **Negotiation example** — clustering a database to mitigate availability risk (4) costs $50,000; the business owner refuses. The architect proposes splitting it into two domain databases for $16,000, still reducing risk; stakeholders agree.

## 5. User-Story Risk Analysis

- **Beyond architecture** — the same risk matrix applies to user stories during grooming. Score each story's *impact if not completed in the iteration* against *likelihood of not completing it*.
- **Use** — flag high-risk stories for closer tracking and prioritization, and assess overall iteration risk.

## 6. Risk-Storming Use Case: Nursing Hotline

- **System** — call-center support system where nurses advise patients on medical conditions. Three web UIs (self-service, nurse, admin), `Call Accepter` and `Call Router` services, central database, diagnostics-system API Gateway. Four main backend services: `Case Management`, `Nurse Profile Management`, `Medical Records Interface`, `Diagnostics Engine Interface`. REST throughout, except proprietary protocols to external systems and call-center services.
- **Constraints** — third-party diagnostics engine handles ~500 req/s; 250 concurrent nurses, hundreds of thousands of self-service patients; HIPAA-compliant medical records (nurses only); spikes during cold/flu/COVID outbreaks. Critical characteristics: availability, elasticity, security.

### 6.1. Availability

- **Identified risks:**
  - Central database — high (6); impact 3, likelihood 2.
  - `Diagnostics Engine` — high (9); impact 3, likelihood unknown so 3.
  - `Medical Records Interface` — low (2); not required to determine outcomes.
  - Other components covered by multiple instances and clustered API Gateway.
- **Mitigation — split the database** — separate clustered nurse-profile database and single-instance case-notes database; nurses can write notes manually if case-notes DB fails, and `Call Router` keeps working. Bonus: better security separation for case notes.
- **External system mitigation via SLAs/SLOs** — research published SLAs for the third-party services. Found: `Diagnostics Engine` SLA 99.99% (52.60 min/yr downtime); `Medical Records Interface` SLA 99.90% (8.77 hr/yr). Sufficient evidence to remove these from the risk register; SLAs are added to the architecture diagram.

### 6.2. Elasticity

- **Identified risk** — `Diagnostics Engine` interface unanimously rated high (9). Self-service patients (potentially hundreds of thousands) plus nurses overwhelm a 500 req/s engine over REST, especially during outbreaks.
- **Mitigation 1 — async queues** — between API Gateway and `Diagnostics Engine` interface for backpressure; doesn't fix wait times.
- **Mitigation 2 — Ambulance pattern** — two message channels prioritizing nurse requests over self-service requests; still doesn't address overall wait times.
- **Mitigation 3 — Diagnostics Outbreak Cache Server** — new service caches outbreak/flu-related diagnostics questions so they never reach the engine; reduces volume and frees the engine for other symptoms.

### 6.3. Security

- **Identified risk** — single API Gateway rated high (6). Impact 3 (admin or self-service patients reaching medical records would breach HIPAA), likelihood 2. The facilitator initially rated this low (2) but participants convinced them otherwise.
- **Mitigation — separate API Gateways per user type** — admin, self-service, nurses each get their own gateway, ensuring non-nurse calls cannot reach `Medical Records Interface`.

- **Outcome** — the original architecture is significantly modified by risk storming, addressing availability, elasticity, and security. Risk storming surfaces issues that single-architect review would miss.
- **Cadence** — risk storming continues throughout the system's lifecycle. Frequency depends on rate of change, refactoring efforts, and incremental development; common practice is to risk-storm specific dimensions after a major feature or at the end of every iteration.
