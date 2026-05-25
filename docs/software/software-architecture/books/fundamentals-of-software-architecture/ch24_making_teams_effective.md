# Ch 24: Making Teams Effective

## Table of Contents

- [1. Collaboration Over Hand-Off](#1-collaboration-over-hand-off)
- [2. Constraints and Boundaries](#2-constraints-and-boundaries)
- [3. Architect Personalities](#3-architect-personalities)
- [4. How Much Involvement?](#4-how-much-involvement)
- [5. Team Warning Signs](#5-team-warning-signs)
- [6. Leveraging Checklists](#6-leveraging-checklists)
- [7. Providing Guidance Through Design Principles](#7-providing-guidance-through-design-principles)

## 1. Collaboration Over Hand-Off

- **Architecture and development are not separate activities.** The traditional view — architect produces artifacts, throws them over a wall to developers — has a unidirectional arrow that breaks the system: architect's intent doesn't fully reach the team, and team-side changes rarely get back to the architect.
- **Form one virtual team.** A bidirectional, collaborative model lets the architect mentor and coach developers and lets architecture evolve with each iteration. Today's architectures change with nearly every iteration; static, waterfall-style hand-off no longer works.

## 2. Constraints and Boundaries

- **Boundaries form a "room"** in which the development team works to implement the architecture. The architect's job is to set those constraints.
- **Too tight** — the room is too small: developers can't access the tools, libraries, and practices they need; frustration drives them off the project.
- **Too loose (or none)** — the room is too big: developers must take on the architect role, do too many proofs of concept, and get stuck on design decisions.
- **Effective architects size the room appropriately**, providing the right level of guidance so the team has what it needs without being smothered.

## 3. Architect Personalities

- **Three caricatures:** *control-freak architect* (tight boundaries), *armchair architect* (loose boundaries), *effective architect* (appropriate boundaries).
- **The control-freak architect** — tries to control every detail: restricts third-party libraries, dictates naming conventions, class designs, method lengths, even pseudocode. Steals the art of programming from developers. The temptation hits hardest in newly promoted architects who used to write the class diagrams themselves. Example: for a `Reference Manager` component (`GetData`, `SetData`, `ReloadCache`, `NotifyOnUpdate`), the architect's job is naming it and identifying who interacts with it — *not* dictating a parallel-loader internal cache; that's the developer's job.
- **The armchair architect** — hasn't coded in a long time (if ever); doesn't account for implementation detail; disconnected from the team; moves on to the next project after the initial diagrams. Drawing boxes is easy to fake — writing source code is not. Tells: not understanding the business domain, lacking hands-on experience, ignoring implications like complexity, maintenance, and testing. Few architects intend to become this; it happens when they're spread too thin.
- **The effective architect** — sets appropriate constraints, makes sure the team works well together, provides the right guidance, picks the right tools, and removes roadblocks. Requires gaining the team's respect through close collaboration.

## 4. How Much Involvement?

- **Elastic Leadership** — Roy Osherove's idea that the right level of leader involvement varies. Five factors help architects calibrate:
  - **Team familiarity** — members who know each other self-organize and need less involvement; new teams need the architect to facilitate collaboration and reduce cliques.
  - **Team size** — > 12 is "big"; ≤ 5 is "small." Larger teams need more involvement.
  - **Overall experience** — junior-heavy teams need mentoring; senior teams need a facilitator.
  - **Project complexity** — high complexity ⇒ more involvement to assist with issues.
  - **Project duration** — *counterintuitive*: short projects (e.g., two months) already feel urgent, so the architect should stay out of the way (armchair); long projects (e.g., two years) need the architect to keep momentum and sequence the hard work first.
- **Scoring scale.** Each factor scores +20 (more involvement, control-freak end) or -20 (less, armchair end). Example Scenario 1: new team, 4 members, all experienced, simple, 2 months ⇒ -60 (be hands-off). Scenario 2: team knows each other, 12 members, mostly junior, complex, 6 months ⇒ +20 (mentor and coach, but don't disrupt).
- **Reassess continuously** — the appropriate level changes as the project progresses; some factors may carry more weight than others, so weight them to fit the situation.

## 5. Team Warning Signs

- **Process loss (Brooks's Law)** — coined by Fred Brooks in *The Mythical Man-Month*: adding people to a project lengthens it. Actual productivity always trails group potential; the gap is process loss. Tells: frequent merge conflicts (people working on the same code). Mitigate by finding parallel work streams; if a project manager proposes adding someone and no parallel stream exists, warn that the addition will hurt.
- **Pluralistic ignorance** — everyone privately rejects a norm but goes along because they think they're missing something obvious. Famously dramatized in Andersen's "The Emperor's New Clothes." Example: a large team agrees to use messaging between two services even though one member knows a firewall makes REST simpler — but stays silent. Larger groups make people less willing to confront. The architect, watching faces and body language, draws skeptics out and supports them when they speak up — even if they turn out to be wrong — so the room feels safe.
- **Diffusion of responsibility** — as teams grow, communication suffers; people assume someone else is handling things. Illustrated by the broken-down car: on a country road everyone stops; on a busy highway nobody does. If team members are confused about who owns what and things are getting dropped, the team is too large.

## 6. Leveraging Checklists

- **Checklists work** — pilots use them on every flight; in *The Checklist Manifesto*, Atul Gawande shows surgical checklists drove staph infection rates near zero. They're excellent for making sure every task is covered.
- **When to use them** — for processes that lack a procedural order, lack dependent tasks, or are frequently skipped. Don't checklist a procedural flow with dependencies (e.g., "create a new database table" — you can't verify the table before submitting the form).
- **Don't go overboard** — the **Law of Diminishing Returns** kicks in: more checklists ⇒ less compliance. Keep them as small as possible; automate any item that can be automated and remove it from the list.
- **Stating the obvious is fine** — the obvious tasks are the ones most often missed.

- **Hawthorne effect** — people who think they're being observed change behavior, generally to do the right thing. Tell the team checklists will be verified — occasional spot-checks are enough to keep developers from skipping items or falsely marking them complete.

- **Three high-value checklists:**
  - **Developer code-completion checklist** — defines "done." Includes formatting/coding standards not covered by automation, frequently overlooked items (e.g., absorbed exceptions), project-specific standards, and special team procedures. Example tasks: run code cleanup and formatting; verify only public methods call `setFailure()`; include `@ServiceEntrypoint` annotation; verify the audit log is written. Architect should review for any items that can be automated as plug-ins for a code validator (e.g., the `setFailure()` rule is straightforward to automate; the annotation rule may not be).
  - **Unit and functional testing checklist** — usually the longest; aims to make code production-ready. Includes special characters in text/numeric fields, min/max value ranges, unusual and extreme cases, missing fields. Anytime QA finds a defect from a particular test case, add it. Bridges the gap when test and dev are separate teams.
  - **Software-release checklist** — releases are one of the most error-prone points in the SDLC. Most volatile of the three: changes after each failed deployment. Typically covers configuration changes in servers or external configuration servers, third-party libraries added (JAR, DLL, etc.), and database updates with corresponding migration scripts. Anytime a build or deployment fails, the architect adds an entry.

## 7. Providing Guidance Through Design Principles

- **Design principles shape the room.** Communicating them is one of the keys to a successful team. Example: the *layered stack* of third-party libraries — developers always have questions about which are OK, which aren't, and when they can decide.
- **Two questions for any new library:**
  - Are there overlaps with the proposed library and existing functionality? Prevents duplication, especially in large projects.
  - What is the justification? Ask for both a *technical* and a *business* justification. Forcing a business case raises developers' awareness of the business need.

- **Business-justification story** — a developer obsessed with Scala threatened to fracture a Java team; two key members planned to leave. The architect agreed to allow Scala *if* the enthusiast produced a business justification. The next day the developer returned humbled: every technical advantage carried no business value given the cost, budget, and timeline. They went on to become one of the team's strongest contributors; the two key developers stayed.

- **Categorize libraries to delegate decisions:**
  - **Special purpose** — narrow needs (PDF rendering, barcode scanning) where custom software isn't warranted. *Developers decide on their own.*
  - **General purpose** — wrappers on top of the language API (e.g., Apache Commons, Guava). *Developers analyze overlap, justify, recommend; architect approves.*
  - **Framework** — entire layers/structures of the application (e.g., Hibernate for persistence, Spring for IoC); highly invasive. *Architect's responsibility entirely.*
- **Architects own this work.** Some argue it should fall to a development or project manager; the authors disagree. Architects guide on technical matters and lead implementation; close collaboration is what lets them observe team dynamics and intervene to make the team more productive.
