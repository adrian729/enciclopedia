# Ch 1: Introduction

## Table of Contents

- [1. Defining Software Architecture](#1-defining-software-architecture)
- [2. The Three Laws of Software Architecture](#2-the-three-laws-of-software-architecture)
- [3. Expectations of an Architect](#3-expectations-of-an-architect)
- [4. Roadmap](#4-roadmap)

## 1. Defining Software Architecture

- **Architecture is contextual** — every architecture is a product of its era's constraints (cost of licenses, hardware, ops practices). Microservices were inconceivable in 2002 because servers, OS, app servers, and DBs were all expensive proprietary commercial software; the DevOps revolution and open source made today's styles affordable.
- **Architects make the decisions AI cannot** — evaluating trade-offs within complex, changing contexts is precisely the work generative AI struggles with, which is why many developers see architecture as a robust next career step.
- **Four-dimensional definition** — software architecture = an **architecture style** + the **architecture characteristics** it must support + the **logical components** that implement behavior + the **architecture decisions** justifying it all. Together these denote the system's structure.
- **Architecture characteristics** — the system's *capabilities*, commonly called the "-ilities" (performance, scalability, availability, etc.). They define what the system should *do* well, beyond functional requirements.
- **Logical components** — the *behavior* of the system, expressed as domains, entities, and workflows. Designing them is one of the architect's key structural activities.
- **Architecture style** — chosen *after* analyzing characteristics and components; it picks the easiest implementation path for the given requirements.
- **Architecture decisions** — rules that constrain how the system is built (e.g., "only the Business and Services layers in a layered architecture may access the database"). They direct teams on what is and isn't allowed.

## 2. The Three Laws of Software Architecture

The authors set out to find ~10–15 universal laws and ended up with three.

> **First Law of Software Architecture** — Everything in software architecture is a trade-off.

- **Corollary 1** — if you think you've found something that *isn't* a trade-off, you just haven't *identified* the trade-off yet.
- **Corollary 2** — you can't do trade-off analysis once and be done; every situation forces re-evaluation. Teams that try to standardize (e.g., "always use choreography") discover it works sometimes and fails spectacularly elsewhere.

> **Second Law of Software Architecture** — *Why* is more important than *how*.

- An experienced architect can usually figure out *how* an unfamiliar architecture works, but struggles to recover *why* prior decisions were made — the trade-offs and context that justified them.

> **Third Law of Software Architecture** — Most architecture decisions aren't binary but rather exist on a spectrum between extremes.

## 3. Expectations of an Architect

Eight core expectations regardless of role or title:

| # | Expectation | What it means |
|---|---|---|
| 1 | Make architecture decisions | *Guide* technology choices rather than specify them — e.g., mandate a reactive frontend framework, not React specifically. Make specific picks only when needed to preserve a characteristic like scalability. |
| 2 | Continually analyze the architecture | Assess **architecture vitality** — how viable a 3+ year-old architecture is today. Combat **structural decay** from coding/design changes that erode required characteristics. Remember test and release pipelines: fast code changes don't help if releases take months. |
| 3 | Keep current with latest trends | Architecture decisions are long-lasting and hard to reverse, so trend awareness is even more critical for architects than for developers. |
| 4 | Ensure compliance with decisions | Verify teams follow documented decisions; e.g., a UI dev bypassing a layered-access rule for performance silently undermines the architecture. Chapter 6 covers automated **fitness functions** for measuring compliance. |
| 5 | Understand diverse technologies | Favor **technical breadth over depth** — knowing the pros/cons of 10 caching products is more valuable than mastery of one. |
| 6 | Know the business domain | An architect at a bank who can't speak about *aleatory contracts* or *nonpriority debt* loses credibility with stakeholders and can't design effectively. |
| 7 | Possess interpersonal skills | "It's always a people problem" (Weinberg). Leadership and communication are *at least half* of being an effective architect; many strong technologists fail in the role for lack of them. |
| 8 | Understand and navigate politics | *Almost every architect decision will be challenged.* A developer's design-pattern choice rarely needs approval; an architect's call to silo a CRM database affects everyone touching that data, and they must negotiate it through. |

## 4. Roadmap

The book has three parts:

- **Part I: Foundations** — defines the key components of architecture, focusing on architectural characteristics and logical components, leading to selection of an architectural style.
- **Part II: Architecture Styles** — a catalog of named topologies, comparing structural and communication differences, data topologies, teams, and physical architectures.
- **Part III: Techniques and Soft Skills** — the people-facing side of the role, often the hardest skills for technically-promoted architects to develop yet vital on the job.
