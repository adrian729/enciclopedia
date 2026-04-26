# Ch 21: Architectural Decisions

## Table of Contents

- [1. Architectural Decision Antipatterns](#1-architectural-decision-antipatterns)
- [2. Architectural Significance](#2-architectural-significance)
- [3. Architectural Decision Records (ADRs)](#3-architectural-decision-records-adrs)
- [4. Basic ADR Structure](#4-basic-adr-structure)
- [5. ADR Example: Going, Going, Gone](#5-adr-example-going-going-gone)
- [6. Storing ADRs](#6-storing-adrs)
- [7. ADRs as Documentation and Standards](#7-adrs-as-documentation-and-standards)
- [8. ADRs with Existing Systems](#8-adrs-with-existing-systems)
- [9. Generative AI and LLMs in Architectural Decisions](#9-generative-ai-and-llms-in-architectural-decisions)

## 1. Architectural Decision Antipatterns

- **Antipattern** (Andrew Koenig) — something that seems like a good idea when you begin but leads you into trouble; or, a repeatable process that produces negative results.
- **Progressive flow** — the three antipatterns chain: overcoming Covering Your Assets exposes Groundhog Day; overcoming Groundhog Day exposes Email-Driven Architecture. Effective decisions require overcoming all three.
- **Covering Your Assets antipattern** — the architect avoids or defers a decision out of fear of being wrong. Two cures: (1) wait until the *last responsible moment* — the point where the cost of further deferral exceeds the risk of deciding (don't wait so long it becomes Analysis Paralysis); (2) collaborate closely with development teams so issues surface fast and the decision can be adjusted. Example: deciding to use replicated in-memory caches for product reference data, then learning from the team that scalability requirements demand more in-process memory than is available — adjust the decision quickly because of the collaboration.
- **Groundhog Day antipattern** — people don't know *why* a decision was made, so they keep relitigating it endlessly (named after the 1993 film). Cause: incomplete justification. Always provide both *technical* and *business* justification. Example: breaking a monolith into services has a clean technical rationale (decoupling, independent maintenance/deployment) but needs a business rationale (faster time to market, lower release costs).
- **Four common business justifications** — cost, time to market, user satisfaction, strategic positioning. Match the justification to what stakeholders care about; cost savings won't land if the business cares about time to market. If you can't produce a business justification, reconsider the decision.
- **Email-Driven Architecture antipattern** — people lose, forget, or never knew about a decision and therefore can't implement it. Email is a great communication tool but a terrible document repository. Cure: don't put the decision in the email body — that creates multiple systems of record, often missing details, and makes superseding hard. Instead, mention only the *nature* and *context* of the decision and link to the single system of record (wiki page, document). Example: *"Hi, Sandra, I've made an important decision regarding communication between services that directly impacts you. Please see the decision using the following link…."* The phrase *"directly impacts you"* doubles as the litmus test for whom to notify.

## 2. Architectural Significance

- **Architecturally significant** (Michael Nygard) — a decision is architectural, even if it picks a specific technology, when it affects any of: structure, non-functional characteristics, dependencies, interfaces, or construction techniques.
- **Structure** — affects the patterns or styles in use (e.g., sharing code across microservices impacts bounded contexts and therefore system structure).
- **Non-functional characteristics** — if the technology choice affects an architecture characteristic that matters (e.g., performance), the choice is architectural.
- **Dependencies** — coupling points between components/services that affect scalability, modularity, agility, testability, reliability, etc.
- **Interfaces** — how services and components are accessed and orchestrated (gateway, integration hub, service bus, adapter, API proxy); includes contracts, versioning, and deprecation strategies.
- **Construction techniques** — platforms, frameworks, tools, even processes that, although technical, affect the architecture.

## 3. Architectural Decision Records (ADRs)

- **Definition** — a short text file (one to two pages) describing a specific architectural decision. Evangelized by Michael Nygard in a 2011 blog post; recommended for widespread adoption by the 2017 Thoughtworks Technology Radar.
- **Format** — usually written in plain text, AsciiDoc, or Markdown; a wiki page template also works. ADR Tools by Nat Pryce provides a CLI for managing numbering, location, and superseded logic.

## 4. Basic ADR Structure

Five standard sections plus two strongly recommended additions:

- **Title** — sequentially numbered short phrase. Example: *"42. Use of Asynchronous Messaging Between Order and Payment Services."* Concise but unambiguous.
- **Status** — one of three: *Proposed*, *Accepted*, *Superseded*. Proposed requires sign-off from a higher-level decision maker or architecture review board. Superseded always replaces a previously *Accepted* ADR; both ADRs are cross-linked by number.
  - Example: ADR 42 is later superseded after a decision to switch to REST. *ADR 42 Status: Superseded by 68.* *ADR 68 Status: Accepted, supersedes 42.* The link prevents the inevitable "what about messaging?" question on ADR 68.
  - **RFC variant** — a *Request for Comments* status (with deadline) lets architects circulate a draft before deciding. Example: *STATUS — Request For Comments, Deadline 09 JAN 2026.*
  - **Approval criteria** — the Status section forces a discussion about who can approve what. Three good starting axes: cost (purchase, hardware, level of effort × FTE rate), cross-team impact, and security. Example threshold: "costs exceeding $5,000 must be approved by the architecture review board."
- **Context** — the forces at play. "What situation is forcing me to make this decision?" Concisely names the scenario and the alternatives considered. Example: *"The Order service must pass information to the Payment service to pay for an order currently being placed. This could be done using REST or asynchronous messaging."* Detailed alternative analysis goes in a separate Alternatives section if needed.
- **Decision** — what was decided plus full justification. Nygard recommends *affirmative, commanding voice*: *"We will use asynchronous messaging between services"* — not *"I think asynchronous messaging would be best."* Emphasize the *why*; future architects need rationale, not mechanism. Example: gRPC was chosen for low latency; a later switch to REST without that context caused timeouts and upstream failures.
- **Consequences** — the overall impact, good and bad, and the trade-off analysis. Example: choosing async fire-and-forget messaging for review posting to drop response time from 3,100 ms to 25 ms — at the cost of complex error handling for "bad words" reviews. Document that the trade-off was discussed with stakeholders in this section.
- **Compliance** *(recommended addition)* — how the decision is measured and governed: manual review or automated fitness function. Example: in a layered architecture, the rule "shared objects used by Business-layer business objects must reside in the Shared Services layer" can be enforced by an ArchUnit test:

  ```java
  @Test
  public void shared_services_should_reside_in_services_layer() {
      classes().that().areAnnotatedWith(SharedService.class)
          .should().resideInAPackage("..services..")
          .check(myClasses);
  }
  ```

  This requires creating an `@SharedService` annotation and applying it to all shared classes. NetArchTest is the equivalent in C#.
- **Notes** *(recommended addition)* — metadata about the ADR: original author, approval date, approved by, superseded date, last modified date, modified by, last modification. Useful even when ADRs live in version control.
- **Extensions are fine** — keep templates consistent and concise. An *Alternatives* section is a common useful addition.

## 5. ADR Example: Going, Going, Gone

- **Decision context** — `Bid Capture` must forward bids to `Bid Streamer` and `Bidder Tracker`; choices were single pub/sub topic, separate point-to-point queues, or REST via the Online Auction API layer.
- **Decision** — separate queues for `Bid Streamer` and `Bidder Tracker`. Justifications:
  - Communication is one-way; `Bid Capture` needs no return information.
  - FIFO queues preserve exact bid ordering for `Bid Streamer`.
  - Multiple identical-amount bids ("Do I hear a hundred?"): `Bid Streamer` only needs the first; `Bidder Tracker` needs all. A pub/sub topic would force `Bid Streamer` to dedupe across instances and store shared state.
  - `Bid Streamer` uses an in-memory cache; `Bidder Tracker` writes to a database (slower, may need backpressure). A dedicated queue gives the dedicated backpressure point.
- **Consequences** — message queues require clustering and HA; `Bid Capture` must send the same data to multiple queues; internal bid events bypass API-layer security checks (ARB at 14 JAN 2025 reviewed and accepted this trade-off — recorded as an UPDATE in the Consequences section).
- **Compliance** — periodic manual code reviews to confirm async pub/sub is used between `Bid Capture`, `Bid Streamer`, and `Bidder Tracker`.
- **Notes** — Author: Subashini Nadella; Approved: ARB Meeting Members, 14 JAN 2025; Last Updated: 14 JAN 2025.

## 6. Storing ADRs

- **One file or wiki page per ADR.**
- **Avoid the application Git repo for large orgs** — not everyone needing access has it; integration/enterprise/common decisions live outside any single application.
- **Recommended locations** — dedicated ADR Git repo with broad access, a wiki, or a shared filesystem rendered by wiki/document software.
- **Suggested directory structure:**

| Directory | Contents |
|---|---|
| `application/common` | ADRs that apply to all applications (e.g., framework annotation/attribute conventions) |
| `application/<app-name>` | ADRs specific to a particular application or system |
| `integration` | ADRs for communication between applications, systems, or services |
| `enterprise` | Global ADRs impacting all systems (e.g., "all access to a system database is only from the owning system") |

- **Names are recommendations** — pick names that fit the company, but stay consistent across teams.

## 7. ADRs as Documentation and Standards

- **As documentation** — no industry standard exists for documenting software architecture (C4 Model, ArchiMate are emerging). ADRs fill the gap: Context describes the area and alternatives; Decision captures *why*, the most valuable form of architecture documentation; Consequences captures the trade-off analysis (e.g., performance vs. scalability).
- **For standards** — most developers dislike standards because they often exist for control, not purpose. ADRs flip this: Context names the situation forcing the standard, Decision names the standard *and why it must exist*, Consequences forces thinking about implications. If an architect can't justify a standard via an ADR, perhaps the standard shouldn't exist. Developers who understand *why* are more likely to follow standards.

## 8. ADRs with Existing Systems

- **Still valuable** — ADRs aren't only documentation; they help architects and developers understand *why* a decision was made and whether it was appropriate.
- **Approach** — write ADRs for the more significant existing decisions and question whether they are correct. Example: a group of services share a single database — *why?* Should it be split?
- **When original authors are gone** — the architect must identify alternatives, analyze trade-offs, and validate (or invalidate) the existing decision. Either way the team builds up justifications, rationales, and a brain trust, and surfaces architectural inefficiencies and incorrect design.

## 9. Generative AI and LLMs in Architectural Decisions

- **Why LLMs struggle** — most LLMs predict the most probable answer given the prompt, often referencing "best practices." But probability and "best practices" have no place in architectural decisions, which require trade-off analysis grounded in a specific business and technical context.
- **First Law of Software Architecture** — *everything in software architecture is a trade-off.* There are no "best practices" for structural questions.
- **Translation problem** — architects must translate business concerns (time to market, sustained growth) into architecture characteristics (maintainability, testability, deployability). Example: time to market makes maintainability dominate performance, so payment processing splits into a service per type rather than a single service.
- **Best current use** — have a generative AI tool outline the *possible trade-offs* of a decision, helping identify trade-offs the architect may have missed. Generative AI has *knowledge* but lacks the *wisdom* required to make the most appropriate architectural decision.
