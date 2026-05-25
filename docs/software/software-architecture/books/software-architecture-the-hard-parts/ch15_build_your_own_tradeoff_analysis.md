# Ch 15: Build Your Own Trade-Off Analysis

## Table of Contents

- [1. Why generic answers don't transfer](#1-why-generic-answers-dont-transfer)
- [2. Find Entangled Dimensions](#2-find-entangled-dimensions)
- [3. Trade-Off Techniques](#3-trade-off-techniques)
- [4. Sysops Squad: epilogue](#4-sysops-squad-epilogue)

## 1. Why generic answers don't transfer

- **Generic solutions are starting points** — the book's communication analysis is not exhaustive; readers should add columns for the dimensions entangled with their own problem space.
- **Three-step process (recap of Ch. 2)** — (1) find what parts are entangled, (2) analyze how they are coupled, (3) assess trade-offs by determining the impact of change on interdependent systems.
- **Architecture is the discipline** — when stakeholders complain that ADRs and trade-off tables are "extra process," the answer is: *that's architecture, and it works*.

## 2. Find Entangled Dimensions

### 2.1. Coupling

- **Working definition** — *if someone changes X, will it possibly force Y to change?* — kept deliberately simple and intuitive.
- **Static coupling diagram inputs** — OS/container dependencies, transitive framework/library dependencies, persistence (databases, search engines, cloud), bootstrap integration points, and messaging infrastructure required for inter-quantum communication.
- **What static coupling excludes** — quanta that only communicate through workflow calls; e.g., AssignTicket and ManageTicket are statically independent but dynamically coupled during the workflow.
- **No off-the-shelf tool** — each architecture is unique; teams that already build environments via automation should extend the generative pipeline to document coupling points as systems build.

### 2.2. Analyze Coupling Points

- **Model the combinations lightly** — skip infeasible combinations; the goal is to identify which forces require trade-off analysis.
- **Authors' chosen forces** — for dynamic quantum coupling: communication, consistency, coordination *plus* coupling, complexity, responsiveness/availability, scale/elasticity.
- **Single-pattern ratings first, then matrix** — rate each pattern in isolation (e.g., **Parallel Saga(aeo)**: async, eventual, centralized, low coupling, low complexity, high responsiveness, high scale), then consolidate to surface comparisons.
- **Observed correlations** — coupling level inversely correlates with scale/elasticity (more coupling, worse scale); higher coupling also reduces responsiveness/availability because more services in a workflow means more failure points.
- **Iterative architecture** — building the matrix of permutations is the only way to study unique nuances; first drafts are never perfect.

### 2.3. Assess Trade-Offs

- **Fix a fundamental dimension first** — choose the gating decision (e.g., synchronous vs asynchronous) early; that constrains the rest of the decision space.
- **Iterate on dependent decisions** — perform the same iterative analysis on each subsequent decision encouraged or forced by the first; once entangled dimensions are resolved, what's left is design.

## 3. Trade-Off Techniques

### 3.1. Qualitative vs Quantitative

- **Architecture is qualitative** — virtually no two architectures are similar enough for true quantitative comparison; honing qualitative judgment over a large sample of implementations is the practical skill.
- **Statistical sampling supports qualitative ratings** — comparing scalability across many implementations of communication/consistency/coordination combinations is what produces credible qualitative scales.

### 3.2. MECE Lists

- **MECE Lists** — *mutually exclusive, collectively exhaustive*; borrowed from technology strategy to ensure architects compare comparable things.
- **Mutually exclusive** — capabilities of compared items must not overlap; comparing a simple message queue to an enterprise service bus is invalid because the ESB contains a queue plus much more.
- **Collectively exhaustive** — all relevant options in the decision space are present; e.g., evaluating high-performance messaging without including Kafka leaves a hole.
- **Use it to spot ecosystem drift** — checking exhaustiveness forces architects to verify a new capability hasn't shifted the criteria.

### 3.3. The Out-of-Context Trap

- **Out-of-Context Trap** — choosing the option that wins on *generic* criteria when narrower context would invert the decision (e.g., shared library beats shared service in the abstract, but situation-specific context can flip it).
- **Narrow the context, simplify the design** — finding the correct context lets architects consider fewer options; this is the operational meaning of "embrace simple designs."
- **Iterative diagramming** — sketch sample architectural solutions and play qualitative *what-if* games to reveal the proper context.

### 3.4. Model Relevant Domain Cases

- **Don't decide in a vacuum** — domain drivers (e.g., adding a new payment type, multi-type checkout) filter generic integrators/disintegrators down to the trade-offs that actually matter.
- **Walk through scenarios** — for "single payment service vs one per type," scenarios like *update credit card processing*, *add reward points*, and *checkout using multiple payment types* surface the real choice: performance and data consistency (single service) vs extensibility and agility (separate services).
- **Semantic coupling can only be increased by implementation, never decreased** — workflow logic must live somewhere; choosing choreography over an orchestrator just relocates it.

### 3.5. Bottom Line over Overwhelming Evidence

- **Bottom Line over Overwhelming Evidence** — reduce the trade-off analysis to a few key points (often aggregates of individual trade-offs); arcane technical detail overwhelms nontechnical stakeholders.
- **Frame the choice in domain terms** — for sync vs async credit card processing, surface it as "guarantee credit approval starts immediately" vs "responsiveness and fault tolerance," not as REST vs queues.

### 3.6. Avoiding Snake Oil and Evangelism

- **Snake Oil and Evangelism** — enthusiasm makes architects amplify the upsides and shrink the downsides; trade-offs always return to complicate things.
- **Force balanced assessments** — challenge any tool/technique promising shocking new capabilities; require an honest list of good and bad before deciding.
- **Scenario analysis beats anecdote** — for "single pub/sub topic vs point-to-point queues," modeling shows that one topic invites stamp coupling, exposes all consumers to PII, and prevents per-consumer auto-scaling; point-to-point allows heterogeneous contracts, granular security, and independent operational profiles, at the cost of harder consumer extensibility.
- **Don't be coerced into the opposite foil** — when a teammate evangelizes (e.g., monorepo vs trunk-based), refuse the binary debate; instead agree to try the approach and add fitness functions that prevent the anti-patterns it enables (e.g., accidental coupling between projects in the same repo).
- **Architect's real value** — becoming the objective arbiter of trade-offs, not chasing silver bullets.

## 4. Sysops Squad: epilogue

- **Retrospective conclusions** — the turnaround came from combining business-driver awareness, application/database team collaboration, ADR-backed trade-off analysis, and the discipline to keep doing all three.
- **Discipline is the practice** — continue trade-off tables, ADRs, and cross-team collaboration on every decision; that *is* architecture.
- **Testing as engineering rigor** — software lacks structural engineering's predictive math, but iterative build-and-test allows trade-off analysis to move from qualitative speculation to quantitative measurement of the team's own ecosystem.
