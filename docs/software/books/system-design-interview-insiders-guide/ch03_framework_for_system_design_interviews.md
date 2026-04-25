# Ch 3: A Framework for System Design Interviews

## Table of Contents

- [1. What the Interview Is Really Testing](#1-what-the-interview-is-really-testing)
- [2. The 4-Step Process](#2-the-4-step-process)
- [3. Step 1: Understand the Problem and Establish Design Scope](#3-step-1-understand-the-problem-and-establish-design-scope)
- [4. Step 2: Propose High-Level Design and Get Buy-In](#4-step-2-propose-high-level-design-and-get-buy-in)
- [5. Step 3: Design Deep Dive](#5-step-3-design-deep-dive)
- [6. Step 4: Wrap Up](#6-step-4-wrap-up)
- [7. Dos and Don'ts](#7-dos-and-donts)
- [8. Time Allocation](#8-time-allocation)

## 1. What the Interview Is Really Testing

- **Not a trivia contest** — questions are deliberately ambiguous and open-ended; no one expects a real Google-search-grade design in an hour
- **Simulates real collaboration** — two co-workers tackling an ambiguous problem together; the process matters more than the final answer
- **Signals beyond technical skill** — collaboration, working under pressure, resolving ambiguity constructively, and asking good questions are all under evaluation
- **Red flags interviewers watch for** — over-engineering (delight in design purity, ignoring tradeoffs and compounding cost), narrow-mindedness, stubbornness

## 2. The 4-Step Process

| Step | Purpose | Time (45-min interview) |
|------|---------|-------------------------|
| 1. Understand the problem and establish design scope | Clarify requirements and assumptions | 3–10 min |
| 2. Propose high-level design and get buy-in | Sketch a blueprint and align with the interviewer | 10–15 min |
| 3. Design deep dive | Drill into prioritized components | 10–25 min |
| 4. Wrap up | Discuss bottlenecks, follow-ups, next-scale | 3–5 min |

## 3. Step 1: Understand the Problem and Establish Design Scope

- **Don't be Jimmy** — the chapter's archetype of the kid who blurts out an answer fast; jumping to a solution without understanding requirements is a major red flag
- **Ask before you build** — gather the right information, make proper assumptions, and confirm scope; an engineer's most valuable skill is asking the right questions
- **Write down assumptions** — when the interviewer pushes them back at you ("make your own assumption"), record them on the whiteboard for later reference
- **Sample clarifying questions** — what specific features are we building, how many users does the product have, anticipated growth at 3/6/12 months, current technology stack and existing services to leverage
- **News-feed example** — clarify mobile vs web, key features (post + see friends' feed), feed ordering (reverse chronological vs weighted), max friends per user (5,000), DAU (10M), media support (images and videos)

## 4. Step 2: Propose High-Level Design and Get Buy-In

- **Collaborate, don't lecture** — treat the interviewer as a teammate; many good interviewers want to be involved
- **Sketch box diagrams** — clients (mobile/web), APIs, web servers, data stores, cache, CDN, message queue
- **Back-of-the-envelope on the blueprint** — verify the design fits the scale constraints; think out loud and check whether sizing is welcome before diving in
- **Walk through concrete use cases** — anchors the design and surfaces edge cases you hadn't yet considered
- **API endpoints and DB schema** — depth depends on the problem: too low-level for "design Google search," reasonable for "design a multi-player poker backend"; ask the interviewer
- **News-feed example** — split into two flows: feed publishing (write to cache/DB and fan out to friends' feeds) and news-feed building (aggregate friends' posts in reverse chronological order)

## 5. Step 3: Design Deep Dive

- **Prerequisites** — by this point you've agreed on goals/scope, sketched the blueprint, gotten feedback, and identified deep-dive areas
- **Prioritize together** — work with the interviewer to pick the components that matter; some interviewers prefer staying high-level, some (especially senior loops) want bottlenecks and resource estimates
- **Pick the right depth** — for URL shortener, dive into the long-to-short hash function; for chat, dive into latency and online/offline status
- **Time management** — easy to get lost in minutiae; details that don't demonstrate scaling skill (e.g., the EdgeRank algorithm in Facebook feed ranking) burn time without delivering signal
- **News-feed example** — deep dive into feed publishing and news-feed retrieval (full design covered in Ch 11)

## 6. Step 4: Wrap Up

- **Identify bottlenecks and improvements** — never claim the design is perfect; calling out limits shows critical thinking and leaves a strong final impression
- **Recap the design** — refresh the interviewer's memory after a long session, especially if you proposed multiple solutions
- **Error cases** — server failure, network loss, partial outages
- **Operational concerns** — monitoring metrics and error logs, rollout strategy
- **Next scale curve** — what changes are needed to go from 1M users to 10M users
- **Future refinements** — propose what you'd do with more time

## 7. Dos and Don'ts

| Do | Don't |
|---|---|
| Always ask for clarification | Be unprepared for typical questions |
| Understand the requirements | Jump into a solution without clarifying |
| Recognize there is no single right answer (a startup design ≠ an established-company design) | Drill into one component before high-level design exists |
| Communicate your thinking | Stay silent if stuck — ask for hints |
| Suggest multiple approaches | Think in silence |
| Drill into the most critical component first after blueprint agreement | Assume you're done before the interviewer says you're done — ask for feedback early and often |
| Bounce ideas off the interviewer; never give up | |

## 8. Time Allocation

- **Step 1 — Understand the problem and establish design scope** — 3–10 minutes
- **Step 2 — Propose high-level design and get buy-in** — 10–15 minutes
- **Step 3 — Design deep dive** — 10–25 minutes
- **Step 4 — Wrap up** — 3–5 minutes
- **Caveat** — actual distribution depends on the problem's scope and the interviewer's priorities; treat as a rough guide, not a script
