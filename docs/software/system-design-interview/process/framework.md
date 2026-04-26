# Interview Framework

> Both books prescribe a top-down framework for the interview. Xu's 4-step version is looser and emphasizes collaboration; Liu's 6-step version is more prescriptive and adds a critical sequencing rule (math *after* API and schema). They are compatible — the 6-step framework expands what Xu calls "Step 2."

## Table of Contents

- [1. The Two Frameworks Side-by-Side](#1-the-two-frameworks-side-by-side)
- [2. Step-by-Step](#2-step-by-step)
  - [2.1. Clarify Scope and Gather Requirements](#21-clarify-scope-and-gather-requirements)
  - [2.2. Define the API](#22-define-the-api)
  - [2.3. High-Level Diagram](#23-high-level-diagram)
  - [2.4. Schema and Data Model](#24-schema-and-data-model)
  - [2.5. Back-of-the-Envelope Math](#25-back-of-the-envelope-math)
  - [2.6. End-to-End Flow](#26-end-to-end-flow)
  - [2.7. Deep Dives](#27-deep-dives)
  - [2.8. Wrap-Up](#28-wrap-up)
- [3. The Magic Formula for Deep Dives](#3-the-magic-formula-for-deep-dives)
- [4. The Golden Question](#4-the-golden-question)
- [Sources](#sources)

## 1. The Two Frameworks Side-by-Side

| Liu (6-step, ~40 min) | Xu (4-step, ~45 min) | Time |
|---|---|---|
| 1a. Functional requirements | 1. Understand and establish design scope | 2–3 min |
| 1b. Non-functional requirements |  | 3–5 min |
| 2. Define API | (folded into Step 2) | 3–5 min |
| 3. High-level diagram | 2. Propose high-level design and get buy-in | 5–7 min |
| 4. Schema and data model | (folded into Step 2) | 5–7 min |
| 5. End-to-end flow | (folded into Step 2) | 2–3 min |
| 6. Deep dives | 3. Design deep dive | 15–20 min |
| (closure during deep dives) | 4. Wrap up | 3–5 min |

**Key sequencing rule (Liu, often missed by Xu's looser layout):** back-of-the-envelope math goes *after* the API and schema. QPS is per-API; storage is per-schema. Calculating either upfront forces guesswork that has to be redone.

## 2. Step-by-Step

### 2.1. Clarify Scope and Gather Requirements

Functional requirements are user stories — *who is the user, why this feature, which one or two cases*. Liu's rule is to ask like a PM and get the interviewer's buy-in on a narrow slice rather than sweep the whole product. Xu uses the news-feed example: clarify mobile vs web, reverse-chronological vs weighted, max friend count (5,000), DAU (10M), media support.

Non-functional requirements are where most of the gathering minutes belong. Both authors agree on the categories: scale (DAU, geographic distribution, peak QPS, storage growth), consistency vs availability (framed as user experience, not "AP vs CP"), latency, freshness (real-time / near real-time / batch), accuracy (distinct from consistency — eventual consistency is eventually *accurate*), and durability (in 9s, framed by impact).

Whenever the interviewer pushes assumptions back at the candidate, write them on the whiteboard. They become the reference point for every later trade-off.

### 2.2. Define the API

The API is the contract; without it, deep-dive discussions get hand-wavy. Three things matter: signature name, input parameters, output response. Liu emphasizes that most candidates forget the output, which is often the design-shaping part — `request_ride` returning `{ driver_ids: [1, 2] }` and letting the user pick a driver introduces concurrency at the API boundary; returning `{ driver_id: 1 }` and letting the server assign sidesteps it.

Defaults: idempotent where achievable (`update_quantity(order, 2)` rather than `decrease_quantity(order, 1)`); server-generated for anything sensitive to client clock skew or tampering; pagination called out for collection responses.

### 2.3. High-Level Diagram

The diagram sets the foundation and shows an end-to-end flow that satisfies the requirements. Liu's systematic approach: draw each API from client to last component, then connect subsequent APIs to what already exists. Don't list microservices and call it a day. Don't add caches, sharding, rate limiters, or generic boxes (DNS, auth, logging) without justification — that reads as hand-wavy.

When tempted to dig in, write the topic on the side. Liu calls this the **table interesting discussion points** discipline; Xu calls it deferring to the deep-dive phase.

### 2.4. Schema and Data Model

Schema concretizes the diagram. Detail belongs on arrows (unsorted driver ID list vs scored list vs single ID), on queues (enqueue `raw_video_id`, not bytes that exhaust memory), and on databases (flat table vs indexed table changes efficiency). Walking the schema against requirements catches nonsensical designs: a `Message Table(user_id, receiver_id, ...)` fails for group chat where a user and receiver belong to multiple rooms.

### 2.5. Back-of-the-Envelope Math

Numbers justify caching and sharding choices. A calculated 10⁸ QPS against a single machine's ~10⁶ capacity identifies a scaling problem; calculating that the load is well within one machine's capacity and dismissing the need to scale is also a strong signal.

Common failure modes: calculating too soon (before API and schema are nailed), spending too long on it, confusing GB with TB (1,000× error), and calculating numbers that don't drive a decision. See the [Estimation](process/estimation.md) page for formulas.

### 2.6. End-to-End Flow

Trace each API through the system once before deep dives to confirm the baseline works and to collect deep-dive talking points. Most candidates skip this checkpoint, which leaves the interviewer uncertain whether the baseline functions.

### 2.7. Deep Dives

This is where seniority shows. The candidate runs the magic formula (below) repeatedly until time runs out. Discussion points can be mined from six categories: APIs and inter-process arrows (latency sensitivity, bursty traffic, query efficiency, protocols), microservices/queues/databases (failure modes, data volumes, component choices), algorithms and schemas, concurrency, operational issues and metrics, and security (most candidates overlook this).

Xu's specific advice on what *not* to deep-dive: minutiae that don't demonstrate scaling skill — for example, EdgeRank ranking internals during a Facebook feed deep dive — waste signal.

### 2.8. Wrap-Up

Identify bottlenecks ("never claim the design is perfect"), recap the design, discuss error and operational concerns, project the next scale curve (1M → 10M users). Don't go silent; don't assume the interview is done before the interviewer says so.

## 3. The Magic Formula for Deep Dives

A six-step loop, run repeatedly: (1) identify a bottleneck, (2) come up with options — aim for at least two, since one option reveals no problem-solving, (3) talk about trade-offs and tie them back to requirements, (4) pick one solution and take a stance, (5) active discussion with the interviewer, (6) go back to step 1. Because there's no PM in the room, the candidate must surface bottlenecks themselves.

## 4. The Golden Question

> **What is the problem I am trying to solve?**

Solution-first thinking — adding a cache, sharding, applying Cassandra because "that's a well-known design" — is the most common failure mode. Concluding that something *isn't* a problem and doesn't need solving is a strong positive signal. No one would shard a 1-QPS startup database in real life either.

## Sources

- [Liu Ch 2: The Six-Step Framework](software/system-design-interview/books/system-design-interview-fundamentals/ch02_six_step_framework.md)
- [Liu Ch 5.01: Back-of-the-Envelope Math](software/system-design-interview/books/system-design-interview-fundamentals/ch05_01_back_of_envelope_math.md)
- [Liu Ch 5.02: API Design](software/system-design-interview/books/system-design-interview-fundamentals/ch05_02_api_design.md)
- [Xu Ch 3: A Framework for System Design Interviews](software/system-design-interview/books/system-design-interview-insiders-guide/ch03_framework_for_system_design_interviews.md)
