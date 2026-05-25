# Team Effectiveness

> *Fundamentals* (Ch 24) is the source: architecture and development as one collaborative activity, the *constraints and boundaries* metaphor, the three architect caricatures, Roy Osherove's Elastic Leadership scoring, the three team warning signs, Atul Gawande's checklists, and the library-categorization framework for delegating technical decisions. *The Hard Parts* assumes this material and doesn't repeat it.

## Table of Contents

- [1. Collaboration Over Hand-Off](#1-collaboration-over-hand-off)
- [2. Constraints and Boundaries](#2-constraints-and-boundaries)
- [3. Three Architect Caricatures](#3-three-architect-caricatures)
- [4. Elastic Leadership](#4-elastic-leadership)
- [5. Team Warning Signs](#5-team-warning-signs)
- [6. Leveraging Checklists](#6-leveraging-checklists)
- [7. Guiding Library Decisions](#7-guiding-library-decisions)
- [Sources](#sources)

## 1. Collaboration Over Hand-Off

Architecture and development are **not separate activities**. The traditional view — architect produces artifacts, throws them over a wall to developers — fails on both sides of the wall:

- The architect's intent doesn't fully reach the team.
- Team-side changes rarely flow back to the architect.

A bidirectional, collaborative model is the only one that survives modern iteration speeds. Architectures change with nearly every sprint; static, waterfall-style hand-off no longer works. The architect is part of the virtual team, not a separate role with a deliverable.

This collaboration is the prerequisite for the [Architectural Decisions](practice/architectural-decisions.md) discipline: ADRs cover *Covering Your Assets* (deferring decisions) by ensuring issues surface through close collaboration. Without the team in the loop, ADRs become bureaucracy.

## 2. Constraints and Boundaries

The architect's job is to define a **"room"** — the set of constraints inside which developers implement. The room metaphor compresses several ideas into one:

| Room size | Result |
|---|---|
| **Too tight** | Developers can't access the tools, libraries, and practices they need; frustration drives them off the project. |
| **Too loose (or none)** | Developers must take on the architect role themselves, do too many proofs of concept, get stuck on design decisions. |
| **Right-sized** | Developers have what they need; the architecture is preserved without smothering. |

**Effective architects size the room appropriately.** Sizing is contextual: a junior team on a novel domain needs a smaller room; a senior team on a familiar domain needs a larger one.

## 3. Three Architect Caricatures

Three personality patterns map onto the three room sizes.

| Caricature | Pattern | Why it fails |
|---|---|---|
| **Control-freak architect** | Restricts third-party libraries, dictates naming conventions, class designs, method lengths, even pseudocode. | Steals the art of programming from developers. The temptation hits hardest in newly promoted architects who used to write the class diagrams themselves. The job is naming a component and identifying who interacts with it — *not* dictating its internal cache implementation. |
| **Armchair architect** | Hasn't coded in a long time (if ever); doesn't account for implementation detail; disconnected from the team. | Drawing boxes is easy to fake; writing source code is not. Tells: not understanding the business domain, lacking hands-on experience, ignoring implications like complexity, maintenance, and testing. Few architects intend to become this; it happens when they're spread too thin. |
| **Effective architect** | Sets appropriate constraints, makes sure the team works well together, provides the right guidance, picks the right tools, removes roadblocks. | Requires gaining the team's respect through close collaboration. |

The control-freak/armchair axis is the same axis as the room-size axis. The effective architect doesn't sit on a midpoint — they calibrate.

## 4. Elastic Leadership

Roy Osherove's **Elastic Leadership** idea: the right level of leader involvement varies, and the architect calibrates continuously. Five factors:

| Factor | Direction |
|---|---|
| **Team familiarity** | Members who know each other self-organize and need less involvement; new teams need the architect to facilitate collaboration and reduce cliques. |
| **Team size** | > 12 is "big"; ≤ 5 is "small." Larger teams need more involvement. |
| **Overall experience** | Junior-heavy teams need mentoring; senior teams need a facilitator. |
| **Project complexity** | High complexity ⇒ more involvement to help work through issues. |
| **Project duration** | *Counterintuitive*: short projects (e.g. two months) already feel urgent, so the architect should stay out of the way; long projects (e.g. two years) need the architect to keep momentum and sequence the hard work first. |

### 4.1. Scoring

Each factor scores **+20** (more involvement, toward control-freak) or **−20** (less, toward armchair).

- **Scenario A** — new team, 4 members, all experienced, simple, 2 months. Score: **−60** (be hands-off).
- **Scenario B** — team knows each other, 12 members, mostly junior, complex, 6 months. Score: **+20** (mentor and coach, but don't disrupt).

Reassess continuously — the appropriate level changes as the project progresses. Some factors may carry more weight in a specific situation; weight them to fit.

## 5. Team Warning Signs

Three patterns signal the team has outgrown its current shape.

### 5.1. Process Loss (Brooks's Law)

Fred Brooks's *Mythical Man-Month* observation: adding people to a project lengthens it. Actual productivity always trails group potential; the gap is **process loss**.

**Tell:** frequent merge conflicts (people working on the same code).

**Mitigation:** find parallel work streams. If a project manager proposes adding someone and no parallel stream exists, warn that the addition will *hurt* delivery, not help it.

### 5.2. Pluralistic Ignorance

Everyone privately rejects a norm but goes along because they think they're missing something obvious. Famously dramatized in Andersen's *The Emperor's New Clothes*.

**Example:** a large team agrees to use messaging between two services even though one member knows a firewall makes REST simpler — but stays silent. Larger groups make people less willing to confront.

**Mitigation:** the architect watches faces and body language, draws skeptics out, and supports them when they speak up — even if they turn out to be wrong — so the room feels safe to disagree.

### 5.3. Diffusion of Responsibility

As teams grow, communication suffers; people assume someone else is handling things. Illustrated by the broken-down car: on a country road everyone stops; on a busy highway nobody does.

**Tell:** team members are confused about who owns what and things are getting dropped.

**Mitigation:** the team is too large. Subdivide it along [team-topology lines](practice/laws-and-intersections.md#56-architecture-and-team-topologies) that match the architecture's partitioning.

## 6. Leveraging Checklists

Pilots use checklists on every flight. In *The Checklist Manifesto*, Atul Gawande showed surgical checklists drove staph infection rates near zero. The principle: **checklists make sure every task is covered.**

**When to use them** — for processes that lack a procedural order, lack dependent tasks, or are frequently skipped. *Don't* checklist a procedural flow with dependencies (e.g. "create a database table" — you can't verify the table before submitting the form).

**Don't go overboard** — the Law of Diminishing Returns kicks in fast: more checklists ⇒ less compliance. Keep them small; automate anything that can be automated and remove it from the list. Stating the obvious is fine — obvious tasks are the ones most often missed.

> **Hawthorne effect** — people who think they're being observed change behaviour, generally toward doing the right thing. Tell the team checklists will be verified — **occasional spot-checks** are enough to keep developers from skipping items or falsely marking them complete.

### 6.1. Three High-Value Checklists

| Checklist | Purpose | Composition |
|---|---|---|
| **Developer code-completion** | Defines "done." | Formatting/coding standards not covered by automation, frequently overlooked items (e.g. absorbed exceptions), project-specific standards, and special team procedures. The architect should review for any items that can be promoted into an automated validator plug-in. |
| **Unit and functional testing** | Make code production-ready. | Usually the longest checklist. Special characters in text/numeric fields, min/max value ranges, unusual and extreme cases, missing fields. Anytime QA finds a defect from a particular test case, add it. Bridges the gap when test and dev are separate teams. |
| **Software release** | The most error-prone point in the SDLC. | Configuration changes in servers or external configuration servers, third-party libraries added (JAR, DLL, etc.), database updates with corresponding migration scripts. The most volatile checklist — changes after each failed deployment. Anytime a build or deployment fails, the architect adds an entry. |

The release checklist is the single highest-leverage one; releases break in a hundred small ways and a checklist catches the ones nobody remembered to automate yet.

## 7. Guiding Library Decisions

For any new third-party library, two questions:

1. **Overlap.** Are there overlaps with existing functionality? Prevents duplication, especially in large projects.
2. **Justification.** What's the technical *and* business justification? Forcing a business case raises developers' awareness of the business need. (See [Architectural Decisions → §1.1](practice/architectural-decisions.md#11-the-four-business-justifications) for the four common business categories.)

### 7.1. The Scala Story

A developer obsessed with Scala threatened to fracture a Java team; two key members planned to leave. The architect agreed to allow Scala *if* the enthusiast produced a business justification. The next day the developer returned humbled — every technical advantage carried no business value given the cost, budget, and timeline. They stayed and became one of the team's strongest contributors; the two key developers stayed too. The architect didn't say no; they let the business case say no.

### 7.2. Categorize Libraries to Delegate Decisions

Not every library decision is the architect's. Sizing the room (from §2) means handing the right ones to developers.

| Category | Examples | Decision authority |
|---|---|---|
| **Special purpose** | PDF rendering, barcode scanning — narrow needs where custom software isn't warranted. | **Developers decide on their own.** |
| **General purpose** | Wrappers on top of the language API — Apache Commons, Guava. | **Developers analyze overlap, justify, recommend; architect approves.** |
| **Framework** | Entire layers/structures of the application — Hibernate for persistence, Spring for IoC; highly invasive. | **Architect's responsibility entirely.** |

Some argue this work should fall to a development or project manager; the authors disagree. Architects guide on technical matters and lead implementation; close collaboration with the team is what lets them observe team dynamics and intervene to make the team more productive. The library-categorization framework is one of the most concrete ways to *size the room*.

## Sources

- [Fundamentals Ch 24: Making Teams Effective](software/software-architecture/books/fundamentals-of-software-architecture/ch24_making_teams_effective.md) (primary — collaboration over hand-off, constraints/boundaries, three caricatures, Elastic Leadership, warning signs, checklists, library categorization)


<!-- prev-next-nav -->

---

← [Diagramming](software/software-architecture/practice/diagramming.md) | [Negotiation and Leadership](software/software-architecture/practice/negotiation-and-leadership.md) →
