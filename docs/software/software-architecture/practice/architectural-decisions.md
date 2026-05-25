# Architectural Decisions

> *Fundamentals* (Ch 21) is the canonical chapter on Architectural Decision Records — the antipatterns they cure, the template, storage, and the place of generative AI. *The Hard Parts* (Ch 1) opens its entire book with the same artifact: a short doc with **Context / Decision / Consequences**, threaded as the documentation backbone through every chapter (ch03, ch06, ch07, ch09, ch12 all close with an ADR). The two books agree on the structure; *The Hard Parts* adds the pairing with fitness functions as the governance layer.

## Table of Contents

- [1. The Three Antipatterns ADRs Cure](#1-the-three-antipatterns-adrs-cure)
- [2. Architecturally Significant](#2-architecturally-significant)
- [3. The ADR Template](#3-the-adr-template)
- [4. Affirmative Voice and Why Over How](#4-affirmative-voice-and-why-over-how)
- [5. Storing ADRs](#5-storing-adrs)
- [6. ADRs as Documentation and Standards](#6-adrs-as-documentation-and-standards)
- [7. ADRs and Fitness Functions](#7-adrs-and-fitness-functions)
- [8. Generative AI in Architectural Decisions](#8-generative-ai-in-architectural-decisions)
- [Sources](#sources)

## 1. The Three Antipatterns ADRs Cure

The architect's record-keeping problem is structural: decisions are made under pressure, communicated incompletely, and forgotten. *Fundamentals* names three antipatterns that chain — overcoming the first exposes the second, overcoming the second exposes the third.

| Antipattern | Failure mode | Cure |
|---|---|---|
| **Covering Your Assets** | Architect defers or avoids the decision out of fear of being wrong. | Decide at the **last responsible moment** — the point where the cost of further deferral exceeds the risk of choosing. Avoid Analysis Paralysis at the other end. Pair with close team collaboration so issues surface fast and the decision can be adjusted. |
| **Groundhog Day** | People don't know *why* a decision was made, so they keep relitigating it (named after the 1993 film). | Provide both **technical** *and* **business** justification. A clean technical rationale (decoupling, independent deployment) isn't enough — stakeholders need a business case. |
| **Email-Driven Architecture** | Decisions live in inboxes. People lose, forget, or never knew about them — and therefore can't implement them. | Don't put the decision in the email body; keep a single system of record (wiki, document, ADR repo). Email only mentions the *nature* and *context* of the decision and links to the record. |

### 1.1. The Four Business Justifications

When the Groundhog Day cure asks for a business justification, four categories cover most cases:

- **Cost** — purchase, hardware, level of effort × FTE rate.
- **Time to market** — release speed, parallel delivery streams.
- **User satisfaction** — performance, availability, the user-visible experience.
- **Strategic positioning** — competitive advantage, optionality, M&A readiness.

Match the justification to what stakeholders actually care about. Cost savings won't land if the business cares about time to market; if you can't produce *any* business justification, reconsider the decision.

### 1.2. The Email Template

Email is a great communication tool but a terrible document repository. The template *Fundamentals* recommends contains a notification, a litmus test for who needs to know, and a link to the system of record:

> *"Hi, Sandra, I've made an important decision regarding communication between services that directly impacts you. Please see the decision using the following link…"*

The phrase *"directly impacts you"* doubles as the test for whom to include on the email.

## 2. Architecturally Significant

The trigger for writing an ADR is **architectural significance**. Michael Nygard's definition:

> A decision is architectural — even if it picks a specific technology — when it affects any of: **structure, non-functional characteristics, dependencies, interfaces, or construction techniques.**

| Dimension | What counts |
|---|---|
| **Structure** | Patterns and styles in use. Sharing code across microservices impacts bounded contexts, which is structural. |
| **Non-functional characteristics** | A technology choice that affects a characteristic the system needs to preserve (performance, scalability, security) is architectural. See [Foundations → Architecture Characteristics](foundations/architecture-characteristics.md). |
| **Dependencies** | Coupling points between components/services that affect scalability, modularity, agility, testability, reliability. |
| **Interfaces** | How services and components are accessed and orchestrated — gateways, integration hubs, service buses, adapters, API proxies — including contracts, versioning, and deprecation. |
| **Construction techniques** | Platforms, frameworks, tools, and even processes that, although technical, shape the architecture. |

If a decision touches none of these, it is design, not architecture, and an ADR is overkill.

## 3. The ADR Template

An ADR is a short text file (one to two pages), evangelized by Nygard in 2011 and put on the Thoughtworks Technology Radar as Adopt in 2017. Plain text, AsciiDoc, Markdown, or a wiki page all work. Nat Pryce's *ADR Tools* CLI handles numbering and superseded logic.

Five standard sections plus two strongly recommended additions:

- **Title** — sequentially numbered short phrase. *"42. Use of Asynchronous Messaging Between Order and Payment Services."* Concise but unambiguous.
- **Status** — one of *Proposed*, *Accepted*, or *Superseded*. *Proposed* requires sign-off from a higher-level decision maker or an Architecture Review Board (ARB). *Superseded* always replaces an *Accepted* ADR; both ADRs cross-link by number so future readers find the chain.
- **Context** — the forces at play. *"What situation is forcing me to make this decision?"* Names the scenario and the alternatives. Detailed analysis of alternatives can go in a separate *Alternatives* section.
- **Decision** — what was decided plus full justification. Emphasis is on *why*, not mechanism.
- **Consequences** — overall impact, good and bad, plus the trade-off analysis. Document that the trade-off was discussed with stakeholders.
- **Compliance** *(recommended)* — how the decision is measured and governed: manual review or automated fitness function. See [§7](#7-adrs-and-fitness-functions).
- **Notes** *(recommended)* — author, approval date, approver, superseded date, last modified, modifier. Useful even when ADRs live in version control.

### 3.1. The RFC Variant

A *Request for Comments* status — with a deadline — lets architects circulate a draft before deciding:

> *STATUS — Request For Comments, Deadline 09 JAN 2026.*

The RFC variant turns the Status section into the place where the team negotiates *who can approve what*. Three common approval axes are cost (e.g. *"over $5,000 must go to ARB"*), cross-team impact, and security.

### 3.2. Superseding

When ADR 42 is replaced by ADR 68 after a switch to REST:

- *ADR 42 — Status: Superseded by 68.*
- *ADR 68 — Status: Accepted, supersedes 42.*

The link prevents the inevitable *"what about messaging?"* question from coming around again on ADR 68. This is exactly the cure for Groundhog Day.

## 4. Affirmative Voice and Why Over How

Nygard recommends an **affirmative, commanding voice**:

> *"We will use asynchronous messaging between services."*

Not *"I think asynchronous messaging would be best."* Hedge-language signals an ADR that hasn't actually made the decision.

The Decision section emphasizes *why*. *How* is recoverable from code; *why* is not. A gRPC choice motivated by latency, recorded without that motivation, was once silently swapped to REST in a later refactor — the new request shape caused timeouts and cascading upstream failures. The *why* would have flagged the swap.

This is the **Second Law of Software Architecture** in concrete form: *why is more important than how.* The ADR is the durable artifact that preserves *why* across team turnover. See [Foundations → Architectural Thinking](foundations/architectural-thinking.md) for the law itself.

## 5. Storing ADRs

- **One file or wiki page per ADR.**
- **Avoid the application Git repo for large orgs.** Not everyone needing access has it; integration, enterprise, and common decisions live outside any single application.
- **Recommended locations** — a dedicated ADR Git repo with broad access, a wiki, or a shared filesystem rendered by wiki/document software.

A suggested directory structure:

| Directory | Contents |
|---|---|
| `application/common` | ADRs that apply to all applications (e.g. framework annotation conventions). |
| `application/<app-name>` | ADRs specific to a particular application or system. |
| `integration` | ADRs for communication between applications, systems, or services. |
| `enterprise` | Global ADRs impacting all systems (e.g. *"all access to a system database is only from the owning system"*). |

Names are recommendations; pick what fits the company but stay consistent across teams.

## 6. ADRs as Documentation and Standards

There is no industry standard for documenting architecture (C4 Model and ArchiMate are emerging — see [Diagramming](practice/diagramming.md)). ADRs fill the gap: *Context* describes the area and the alternatives, *Decision* captures the most valuable form of architecture documentation, *Consequences* captures the trade-off analysis.

For **standards**, ADRs flip the usual posture. Developers dislike standards because they exist for control, not purpose. An ADR forces every standard to declare *why it must exist*:

- *Context* names the situation forcing the standard.
- *Decision* names the standard and the rationale.
- *Consequences* forces thinking through implications.

If an architect can't justify a standard via an ADR, perhaps the standard shouldn't exist. Developers who understand *why* are more likely to follow standards.

For **existing systems**, ADRs are still valuable as a thinking tool. Pick the more significant existing decisions and write ADRs that question whether they are correct: a group of services sharing a single database — *why?* Should it be split? When original authors are gone, the architect identifies alternatives, analyzes trade-offs, and validates (or invalidates) the existing decision. Either way the team accumulates justifications, rationales, and a brain trust.

## 7. ADRs and Fitness Functions

The Compliance section bridges the ADR to **fitness functions**: any mechanism that performs an objective integrity assessment of an architecture characteristic. *The Hard Parts* introduces fitness functions in Ch 1 and threads them through every governance discussion in the book. The pairing is:

- **ADR** records *what* was decided and *why*.
- **Fitness function** automates verification that the decision still holds.

Example: a layered-architecture decision *"shared objects used by Business-layer business objects must reside in the Shared Services layer"* can be enforced with ArchUnit:

```java
@Test
public void shared_services_should_reside_in_services_layer() {
    classes().that().areAnnotatedWith(SharedService.class)
        .should().resideInAPackage("..services..")
        .check(myClasses);
}
```

NetArchTest is the .NET equivalent; PyTestArch covers Python; TSArch covers TypeScript/JavaScript. The full machinery is on [Foundations → Architecture Characteristics](foundations/architecture-characteristics.md).

When automation isn't viable, the Compliance section names a manual cadence: *"periodic code review confirms async pub/sub between Bid Capture and downstream services."* Manual fitness functions slot into deployment pipelines as manual stages.

> **Hard Parts framing.** *The Hard Parts* opens with this exact pattern as the documentation backbone: every chapter that proposes a decomposition pattern, a reuse pattern, an ownership scenario, or a saga closes with an ADR for the Sysops Squad scenario. The ADRs are short — Context, Decision, Consequences — and they sit beside a fitness function that prevents the decision from quietly eroding. The book reads as a series of trade-off analyses, each terminated by an ADR.

## 8. Generative AI in Architectural Decisions

Most LLMs predict the *most probable* answer given the prompt and reference *best practices*. **Neither has a place in architectural decisions.** Architecture requires trade-off analysis grounded in a specific business and technical context; probability gives the average answer, and best practices are the First Law's antonym (*everything in software architecture is a trade-off*).

LLMs also struggle with the translation problem: stakeholders speak in business outcomes (*time to market, sustained growth*), architects must translate those into architecture characteristics (*maintainability, testability, deployability*). The translation requires knowledge of the specific business; the LLM doesn't have it.

> *Generative AI has* **knowledge** *but lacks the* **wisdom** *required to make the most appropriate architectural decision.*

**Best current use:** have the LLM outline the *possible trade-offs* of a decision so the architect can spot any they missed. The LLM is a brainstorming partner, not a decision maker.

The architect's value is the trade-off analysis itself — see [Foundations → Trade-Off Analysis](foundations/tradeoff-analysis.md) — and the ADR is the durable record of that analysis. Neither piece is replaced by an LLM.

## Sources

- [Fundamentals Ch 21: Architectural Decisions](software/software-architecture/books/fundamentals-of-software-architecture/ch21_architectural_decisions.md) (primary — the three antipatterns, ADR template, RFC variant, storage, LLM stance)
- [The Hard Parts Ch 1: What Happens When There Are No "Best Practices"?](software/software-architecture/books/software-architecture-the-hard-parts/ch01_no_best_practices.md) (secondary — ADR definition, fitness-function pairing, ADR as the book's documentation backbone for ch03/06/07/09/12)


<!-- prev-next-nav -->

---

← [Analytical Data & Data Mesh](software/software-architecture/distributed/analytical-data-and-mesh.md) | [Analyzing Risk](software/software-architecture/practice/analyzing-risk.md) →
