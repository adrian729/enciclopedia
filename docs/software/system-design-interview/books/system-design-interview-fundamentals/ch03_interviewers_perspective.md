# Ch 3: Interviewer's Perspective

## Table of Contents

- [1. How Leveling Works](#1-how-leveling-works)
- [2. Rubric Shape Across Sections](#2-rubric-shape-across-sections)
- [3. Requirements: Functional and Non-Functional](#3-requirements-functional-and-non-functional)
- [4. API Design](#4-api-design)
- [5. High-Level Diagram](#5-high-level-diagram)
- [6. Data Structure and Schema](#6-data-structure-and-schema)
- [7. Deep Dives](#7-deep-dives)

## 1. How Leveling Works

- **Why the chapter exists** — most candidates have never sat on the interviewer's side; understanding how the rubric maps performance to a level lets you give interviewers the data points they need
- **Level terminology used in the book** — intentionally company-agnostic, mapped to years of experience:

| Level | Experience |
|---|---|
| Level 1 | 0–2 years (excluded — entry-level engineers typically don't get system design rounds) |
| Level 2 | 2–5 years |
| Level 3 | 5–10 years |
| Level 4 | 10+ years |

- **Performance-to-outcome mapping** — the rubric runs on a spectrum from "No Hire" up to "Level 4". If you interview for Level 3 but perform at Level 2, you may be down-leveled; if you perform at No Hire, you're rejected. Interviewing for Level 4 and performing at Level 2 or below is a likely reject
- **Junior candidates often outperform senior candidates** — because they prepare harder; to minimize rejection risk, prepare fully even when you're experienced
- **Rubric caveat** — varies heavily between companies and interviewers; the examples are perspective, not a contract

## 2. Rubric Shape Across Sections

- **Same four-tier structure repeats** — every step of the framework (functional reqs, non-functional reqs, API, high-level diagram, schema, deep dives) is scored on the same No Hire / Level 2 / Level 3 / Level 4 ladder
- **Rising axis across all sections** — the signal that pushes a candidate up a level is consistent: (1) less guidance needed from the interviewer, (2) more trade-offs surfaced proactively, (3) more tying of decisions back to the requirements, (4) more awareness of what *not* to include
- **No Hire signals are also consistent** — missing clarifying questions, not understanding the problem after multiple hints, buzzword-level answers without internals, and designs that fail the requirement even after pointers

## 3. Requirements: Functional and Non-Functional

**Functional Requirement Gathering**

| Level | Signal |
|---|---|
| No Hire | Didn't ask any clarifying questions; couldn't understand the problem statement after multiple hints; kept discussing different features and failed to elaborate on the technical details |
| Level 2 | Came up with some features but was murky on the user story (e.g., for Google Photo, asked if photos need to be displayed but didn't wireframe it); considered some cases and rushed into the next section; got to important features with a little guidance |
| Level 3 | Interacted well with the interviewer; very clear on user-experience steps; narrowed to a few important features; needed no hints or guidance |
| Level 4 | Same as Level 3 |

**Non-Functional Requirement Gathering**

| Level | Signal |
|---|---|
| No Hire | No clarifying questions about design constraints or performance; said words like *consistency, availability, reliability* without relating them to end-user experience |
| Level 2 | Asked some important non-functional questions but missed others; picked up the missed ones later in the interview |
| Level 3 | Listed most of the important design constraints and qualities and occasionally used them throughout design decisions to make the final recommendation |
| Level 4 | Raised **all** critical design constraints and qualities and used them throughout the interview to drive design decisions and trade-offs |

## 4. API Design

| Level | Signal |
|---|---|
| No Hire | Missed critical APIs; the API wouldn't work after multiple hints; API was highly inefficient and candidate didn't see the issues after hints |
| Level 2 | Got to a reasonable, efficient API after guidance and course-corrected quickly; was murky on components, missed important inputs/outputs, but filled gaps once pointed out |
| Level 3 | Efficient API without much guidance; suggested ways to improve and make it more extensible; needed little guidance on API trade-offs |
| Level 4 | Efficient API with no guidance; proactively listed **all** major trade-offs; proposed alternative solutions for major trade-offs in case requirements change |

## 5. High-Level Diagram

| Level | Signal |
|---|---|
| No Hire | Missed most major components; had difficulty connecting them; architecture wouldn't satisfy the requirements; diagrams and data flows were unclear and stayed unclear even after the interviewer pointed it out |
| Level 2 | Identified most components but needed guidance to fill gaps; introduced components without discussing *why* but course-corrected with hints; initial design had issues, addressed after pointers; some diagrams/flow slightly murky but improvable |
| Level 3 | Identified most major components; surfaced some major trade-offs to defer to deep dives; understood and articulated why each component is necessary |
| Level 4 | Identified **all** major components and trade-offs; cost-aware — understood why some components are **not** needed and removed unnecessary elements |

## 6. Data Structure and Schema

| Level | Signal |
|---|---|
| No Hire | Very difficult time coming up with a schema and often incorrect; data structures and schema were inefficient and wouldn't work, and the candidate didn't understand why even with guidance; failed to discuss trade-offs |
| Level 2 | Produced a reasonable alternative but needed guidance on other options; came up with a schema but didn't self-identify trade-offs until hinted |
| Level 3 | Reasonable schema with some trade-offs surfaced; missed a couple of important points but addressed them with a small nudge |
| Level 4 | Reasonable and efficient schema with trade-offs; identified issues and proposed solutions for them; connected data structures and schema to user experiences in detail and proactively listed trade-offs to address |

## 7. Deep Dives

| Level | Signal |
|---|---|
| No Hire | Stuck after the high-level diagram and thought the design was complete and trivial; failed to understand how high traffic and data volume impact the design; significant knowledge gaps in fundamentals; couldn't go beyond buzzwords |
| Level 2 | Self-identified some bottlenecks but needed guidance on solutions and trade-offs; produced solutions and trade-offs but missed critical risks, then addressed them after guidance |
| Level 3 | Identified most or all bottlenecks; provided most pros/cons for alternatives; some surfaced bottlenecks weren't significant enough to discuss; needed a little guidance on some technical details |
| Level 4 | Self-identified **all** critical bottlenecks; proposed solutions with pros/cons and picked a final recommendation knowing the trade-offs; supplied technical detail tied to requirements and their impact on solutions; prioritized the right areas for the most critical bottlenecks |
