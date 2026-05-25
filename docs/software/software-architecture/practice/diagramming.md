# Diagramming

> *Fundamentals* (Ch 23) is the source: why diagrams matter, the three standards (UML, C4, ArchiMate), the *Irrational Artifact Attachment* antipattern, and the practical guidelines (titles, lines, shapes, color, keys). *The Hard Parts* doesn't have an equivalent chapter — it leans on per-chapter diagrams in its narrative without naming a framework.

## Table of Contents

- [1. Why Diagramming Matters](#1-why-diagramming-matters)
- [2. Tools and Ephemeral Artifacts](#2-tools-and-ephemeral-artifacts)
- [3. Diagramming Standards](#3-diagramming-standards)
- [4. Practical Guidelines](#4-practical-guidelines)
- [Sources](#sources)

## 1. Why Diagramming Matters

Communication is roughly half the architect's job. No matter how brilliant the technical idea, an architect who can't convince managers to fund it and developers to build it never sees it manifest. Diagramming is one of the critical communication skills — possibly the most asymmetric, because a single diagram can carry an idea further than a dozen meetings.

Two structural principles shape every diagram:

### 1.1. Multiple Views

Architects typically start with an **overview** of the entire topology, then drill down into specific parts. Showing a portion of a system without indicating its place in the whole confuses viewers. The overview→detail pattern is what lets a stakeholder follow the explanation without losing the map.

### 1.2. Representational Consistency

> **Representational consistency** — always show the relationship between parts of an architecture before changing views.

When describing a plug-in architecture, start with the full topology, then the plug-in container's place in it, then the plug-in details. Each new view re-anchors the viewer in the previous one. A diagram that skips the bridge between scales forces the viewer to do their own anchoring — and they usually anchor wrong.

The same principle is why this section's pages link back to [Foundations → Components and Quantum](foundations/components-and-quantum.md) when they zoom in: representational consistency at the documentation level mirrors representational consistency at the diagram level.

## 2. Tools and Ephemeral Artifacts

Modern diagramming tools (OmniGraffle, Lucidchart, draw.io, Miro) are powerful, and every architect should learn one deeply. The mistake is reaching for them too early.

> **Antipattern: Irrational Artifact Attachment** — a person's irrational attachment to an artifact is proportional to how long it took to produce. Four hours in Visio yields more attachment than two; Agilists prefer index cards and sticky notes precisely because low-tech tools let people throw away what isn't right.

Early-design artifacts should be **ephemeral**:

| Medium | Why it works early |
|---|---|
| **Whiteboards** | Unlimited canvas, fast iteration, "Do Not Erase!" with a phone photo as the record. |
| **Tablets on an overhead projector** | Unlimited canvas, copy/paste of *what-if* scenarios, already digitized, remote-friendly. |
| **Sticky notes and index cards** | Low investment per artifact — designed to be discarded. |

The principle: **iterate before going fancy.** Drop into the high-fidelity tool only after the team has converged on the structure.

### 2.1. Baseline Tool Features

When choosing a high-fidelity tool, look for:

- **Layers** — group items logically; show or hide on demand. Lets one diagram serve as both an overview and a deep dive without becoming a wall of detail.
- **Stencils / templates** — a library of common visual components (microservice icons, database cylinders) creates consistency across diagrams and accelerates new ones.
- **Magnets** — anchor points on shapes where lines snap and align automatically; some tools let you add your own.

**Use layers semantically, not decoratively.** The base layer should represent the topology — containers, databases, dependencies, brokers — and stay focused on architecture rather than implementation (say *"synchronous communication,"* not a specific protocol). Subsequent layers can carry implementation detail; further layers can overlay DDD bounded contexts, transactional scope, or other meta-information.

## 3. Diagramming Standards

Three standards dominate the conversation. Each has a different center of gravity.

### 3.1. UML

Created by Booch, Jacobson, and Rumbaugh in the 1980s to unify their competing design philosophies. Designed by committee; failed to land outside organizations that mandated it. What survives:

- **Class diagrams** — still useful for capturing intra-component design.
- **Sequence diagrams** — still the standard for showing temporal interaction.

Most other UML diagram types (use case, activity, state, deployment, component) have fallen into disuse. The community uses what works and ignores the rest.

### 3.2. C4

Developed by Simon Brown between 2006 and 2011 to address UML's deficiencies and modernize the approach. Active community; tooling ships C4 templates; a healthy ecosystem of supporting tools and frameworks. The four nested views give it its name and structure:

| View | Purpose |
|---|---|
| **Context** | The entire context of the system — users, external dependencies. The first thing a non-technical reviewer should see. |
| **Container** | Physical (and often logical) deployment boundaries and containers. A natural meeting point between architects and operations. |
| **Component** | The component view of the system — the architect's native level. |
| **Class** | C4 reuses UML class diagrams here, since they already work. No need to reinvent. |

C4 is the modern community standard for new diagrams. It encodes the multiple-views principle from §1 directly: each level zooms into the previous one with representational consistency built in.

### 3.3. ArchiMate

A portmanteau of *architecture* and *animate*; an open-source enterprise-architecture modeling language from The Open Group. A lighter-weight modeling language whose stated goal is to be *"as small as possible,"* not to cover every edge case. Popular for cross-domain enterprise ecosystems where the diagram must speak across business, application, and technology layers simultaneously.

The three standards aren't interchangeable. Use UML class/sequence diagrams to capture local interactions; use C4 for the overview-to-component zoom of a single system; use ArchiMate when the audience is the enterprise and the topic crosses domain boundaries.

## 4. Practical Guidelines

Some conventions are near-universal; others are personal. The rule is: be consistent within a diagram, include a key when there's any chance of ambiguity, and don't fall in love with your own creations.

### 4.1. Build Your Own Style

It's fine to borrow from representations you find effective. Most architects build their own shape vocabulary and sometimes adopt it organization-wide. *Fundamentals* uses three-dimensional boxes for deployable artifacts, rectangles for containers, and cylinders for databases — pick what fits, but stay consistent.

### 4.2. Titles

Title every element unless it's already well known to the audience. Use rotation and other effects to make titles "stick" to the right thing and use space efficiently. An untitled box is an invitation to guess.

### 4.3. Lines

- **Thick enough to be clearly visible.** Thin lines disappear at the back of a meeting room.
- **Use arrows for directional or two-way flow.** Different arrowheads can carry different semantics — just be consistent.
- **The one near-universal convention:**

> **Solid lines = synchronous communication. Dotted lines = asynchronous communication.**

This is one of the few conventions an architect can rely on across organizations. Honour it.

### 4.4. Shapes

There is no industry-wide standard set; build your own and document it. The shape vocabulary is part of the architect's personal style — but anything ambiguous needs a key (see §4.7).

### 4.5. Labels

Label every item, especially where there's any chance of ambiguity. A labelled box can survive being torn out of context; an unlabelled one can't.

### 4.6. Color

Architects underuse color. Many books were printed in black-and-white for years, conditioning monochrome habits. Use color where it distinguishes artifacts — but **pair color with unique iconography** so colorblind viewers still get the meaning. Crossing lights work because they use both color *and* figure (red on top, green on bottom). Diagrams should too.

### 4.7. Keys

If shapes or colors are at all ambiguous, include a key. **An easily misinterpreted diagram is worse than no diagram** — it broadcasts confident wrong information.

### 4.8. Standards with Reasonable Exceptions

Organizations should establish diagramming standards but allow architects to break the rules when the standard can't represent the design. Heavyweight CASE tools historically forced architects to add useless detail to satisfy the tool; favour lightweight tools and quick-and-dirty artifacts early — and don't fall in love with your creations.

The throughline of all eight guidelines is **respect the viewer**. Every choice — title, line thickness, color, key — answers the same question: *will the next person reading this without me here understand what I meant?* If the answer is no, the diagram isn't done.

## Sources

- [Fundamentals Ch 23: Diagramming Architecture](software/software-architecture/books/fundamentals-of-software-architecture/ch23_diagramming_architecture.md) (primary — multiple views, representational consistency, Irrational Artifact Attachment, UML/C4/ArchiMate, line/shape/color guidelines)


<!-- prev-next-nav -->

---

← [Analyzing Risk](software/software-architecture/practice/analyzing-risk.md) | [Team Effectiveness](software/software-architecture/practice/team-effectiveness.md) →
