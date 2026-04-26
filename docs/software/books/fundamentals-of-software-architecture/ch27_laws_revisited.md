# Ch 27: The Laws of Software Architecture, Revisited

## Table of Contents

- [1. The Three Laws](#1-the-three-laws)
- [2. First Law: Trade-Off Analysis in Practice](#2-first-law-trade-off-analysis-in-practice)
- [3. First Law Corollaries](#3-first-law-corollaries)
- [4. Second Law: Why Over How](#4-second-law-why-over-how)
- [5. Third Law: The Spectrum Between Extremes](#5-third-law-the-spectrum-between-extremes)
- [6. Parting Words of Advice](#6-parting-words-of-advice)

## 1. The Three Laws

- **Origin** — the first edition codified two universal observations as *laws*; the second edition adds a third, uncovered while writing.

> **First Law of Software Architecture** — Everything in software architecture is a trade-off.

> **Second Law of Software Architecture** — *Why* is more important than *how*.

> **Third Law of Software Architecture** — Most architecture decisions aren't binary but rather exist on a spectrum between extremes.

## 2. First Law: Trade-Off Analysis in Practice

- **The architect's real job is trade-off analysis** — not silver bullets. Architects rarely get credit for good decisions but always get blamed for bad ones; cultivate a reputation as an *objective arbiter* rather than an evangelist.
- **Why evangelism is dangerous** — yesterday's best practice becomes tomorrow's antipattern; the ecosystem keeps evolving and weakens once-sound decisions. Decision makers want sober objectivity, not advocacy.
- **Example: shared library vs. shared service** — pertinent factors are *heterogeneous code* (service wins), *high code volatility* (service wins), *ability to version changes* (library wins), *overall change risk* (library wins, compile-time verification), *performance* (library wins, in-process call), *fault tolerance* (library wins), *scalability* (library wins). Tallied positives favor the library — *for these factors and this context*.
- **Example: queue vs. topic** — queues give heterogeneous payloads per consumer, independent monitoring/scaling, better security, but tighter coupling and lower extensibility (must add queues for new consumers). Topics give low coupling, single-message broadcast, high extensibility, but homogeneous payloads, possible *stamp coupling*, less per-consumer monitoring/scaling, weaker security. Pick by organizational priority: queues if security dominates, topics if extensibility does.

## 3. First Law Corollaries

> **Corollary 1: Missing Trade-Offs** — If you think you've discovered something that *isn't* a trade-off, more likely you just haven't *identified* the trade-off… yet.

- **Hidden cost of code reuse** — effective reuse needs both *abstraction* and *low volatility*. Architects spot the first and miss the second; sharing high-churn code creates breaking-change ripple across the system. This is exactly what burned orchestration-driven SOA (Ch. 17). "Plumbing" (frameworks, libraries, platforms) is the right reuse target; domain concepts are not — which is why DDD bounded contexts forbid implementation-detail reuse.

> **Sidebar: Why we can't have nice things — trade-offs!** — clients ask for both high decoupling (microservices agility) *and* high institutional reuse. Reuse is implemented via coupling; decoupling and reuse are fundamentally incompatible.

> **Corollary 2: You Can't Do It Just Once** — trade-off analysis must be repeated; subtle differences in dozens or hundreds of variables (complexity, team experience, budget, team topology, schedule) push the result one way or the other. There are no sweeping, semipermanent decisions.

## 4. Second Law: Why Over How

- **Diagrams alone capture *how*** — experienced architects can read a system and explain *how* it works, but rarely *why* a previous architect chose this option over another, because the decision criteria weren't recorded.
- **Document with diagrams *and* ADRs** — architecture diagrams plus ADRs (Ch. 21) preserve the trade-off context, known compromises, and limitations so future architects (often you) don't have to redo the analysis.

> **Antipattern: Out of Context** — the architect knows the trade-offs but not how to *weight* them for the current context. The shared-library/shared-service tally favored the library overall, but a polyglot team that doesn't care about performance or scale should weight *heterogeneous code* and *volatility* higher and pick the shared service. Generic trade-off analysis is only useful when applied in a specific context.

## 5. Third Law: The Spectrum Between Extremes

- **Few decisions are binary** — concepts resist clean definitions (architecture vs. design, orchestration vs. choreography, topics vs. queues) precisely because their criteria lie on a messy spectrum.
- **A useful test for what counts as architecture** — *a software architecture decision is one where each of the options has significant trade-offs.* If everything in architecture is a trade-off, then an architectural decision must involve trade-offs on every option.
- **Don't force binaries** — every answer in software architecture is *it depends* because each criterion sits somewhere on a spectrum. Architects decide in a swamp of uncertainty, often on incomplete information.

## 6. Parting Words of Advice

- **Practice is the only path** — Fred Brooks: *great designers design*. Ted Neward's corollary: how do we get great architects when they only architect a half-dozen times in a career? The companion *architecture katas* (modeled on the book's examples) are designed for that practice.
- **No answer guide exists** — the authors tried to keep student kata drawings as a repository but gave up: the drawings captured *how* but not *why*, and per Neal, *there are not right or wrong answers in architecture — only trade-offs.*
- **Always learn, always practice, *go do some architecture*.**
