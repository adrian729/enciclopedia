# Ch 23: Diagramming Architecture

## Table of Contents

- [1. Why Diagramming Matters](#1-why-diagramming-matters)
- [2. Tools and Ephemeral Artifacts](#2-tools-and-ephemeral-artifacts)
- [3. Diagramming Standards: UML, C4, ArchiMate](#3-diagramming-standards-uml-c4-archimate)
- [4. Diagram Guidelines](#4-diagram-guidelines)

## 1. Why Diagramming Matters

- **Communication is half the job** — no matter how brilliant the technical idea, an architect who can't convince managers to fund it and developers to build it never sees it manifest. Diagramming is one of the critical communication skills.
- **Multiple views are needed** — architects often start with an overview of the entire topology, then drill down into specific parts; showing a portion without indicating its place in the whole confuses viewers.
- **Representational consistency** — always show the relationship between parts of an architecture before changing views. Example: when describing the Silicon Sandwiches plug-in structure, start with the full topology, then the plug-in container's place in it, then the plug-in details.

## 2. Tools and Ephemeral Artifacts

- **Modern diagramming tools are powerful** — every architect should learn one deeply, but don't neglect low-fidelity artifacts early in design. Building ephemeral artifacts prevents over-attachment to what you've created.

> **Antipattern: Irrational Artifact Attachment** — a person's irrational attachment to an artifact is proportional to how long it took to produce. Four hours in Visio yields more attachment than two; Agilists prefer index cards and sticky notes precisely because low-tech tools let people throw away what isn't right.

- **Whiteboards and tablets** — the classic ephemeral artifact is a phone photo of a whiteboard with "Do Not Erase!" Many architects now favor a tablet on an overhead projector: unlimited canvas, copy/paste of "what if" scenarios, already digitized, and remote-friendly.
- **Iterate before going fancy** — the authors used OmniGraffle for this book, but only after the team had iterated enough on the design.
- **Baseline tool features to look for:**
  - **Layers** — group items logically; show or hide them on demand. Useful for a presentation that hides overwhelming detail and for incrementally building up a picture.
  - **Stencils/templates** — a library of common visual components (e.g., a microservice icon) creates consistency across diagrams and speeds new ones up.
  - **Magnets** — anchor points on shapes where lines snap and align automatically; some tools let you add your own.

- **Use layers semantically, not decoratively** — the base layer should represent the topology (containers, databases, dependencies, brokers) and stay focused on architecture, not implementation — say "synchronous communication," not a specific protocol. The next layer can carry implementation detail; further layers can overlay DDD bounded contexts, transactional scope, or other meta-information.

## 3. Diagramming Standards: UML, C4, ArchiMate

- **UML** — created by Booch, Jacobson, and Rumbaugh in the 1980s to unify their competing design philosophies. Designed by committee; failed to land outside organizations that mandated it. Class and sequence diagrams remain in use; most other UML diagram types have fallen into disuse.
- **C4 model** — developed by Simon Brown between 2006 and 2011 to address UML's deficiencies and modernize the approach. Strong, active community; many diagramming tools ship C4 templates; the C4 ecosystem provides supporting tools and frameworks. The four Cs are:
  - **Context** — the entire context of the system, including users and external dependencies.
  - **Container** — physical (and often logical) deployment boundaries and containers; a good meeting point between operations teams and architects.
  - **Component** — the component view of the system; the view that aligns most cleanly with an architect's perspective.
  - **Class** — C4 reuses UML class diagrams since they already work well, so there is no need to replace them.
- **ArchiMate** — a portmanteau of *architecture* and *animate*; an open source enterprise-architecture modeling language from The Open Group. A lighter-weight modeling language whose stated goal is to be "as small as possible," not to cover every edge case; popular for cross-domain enterprise ecosystems.

## 4. Diagram Guidelines

- **Build your own style** — use a formal language or your own; it's fine to borrow from representations you find effective.
- **Titles** — title every element unless it's already well-known to the audience. Use rotation and other effects to make titles "stick" to the right thing and use space efficiently.
- **Lines** — thick enough to be clearly visible. Use arrows for directional or two-way flow; different arrowheads can carry different semantics, just be consistent. The one near-universal convention: **solid lines = synchronous, dotted lines = asynchronous**.
- **Shapes** — there is no industry-wide standard set; most architects build their own and sometimes adopt them organization-wide. The authors use three-dimensional boxes for deployable artifacts, rectangles for containers, and cylinders for databases.
- **Labels** — label every item, especially where there's any chance of ambiguity.
- **Color** — architects underuse it. Many books were printed in black and white for years, conditioning monochrome habits. The authors still favor monochrome but use color where it distinguishes artifacts (e.g., shades of gray to group microservices quanta in Chapter 19). Pair color with unique iconography so colorblind viewers still get the meaning — like crossing lights that use both color and figure.
- **Keys** — if shapes are at all ambiguous, include a key. An easily misinterpreted diagram is worse than no diagram.
- **Standards with reasonable exceptions** — organizations should establish diagramming standards but allow architects to break the rules when the standard can't represent the design. Heavyweight CASE tools forced architects to add useless detail; favor lightweight tools and quick-and-dirty artifacts early — and don't fall in love with your creations.
