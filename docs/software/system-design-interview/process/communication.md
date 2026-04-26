# Communication & Evaluation

> Liu treats communication as roughly half the interview and dedicates a full chapter plus a leveling rubric to it. Xu's coverage is shorter (a few "do/don't" lists) but agrees on every major point. This page merges both, then adds the leveling rubric Liu gives candidates.

## Table of Contents

- [1. Why Communication Is Half the Interview](#1-why-communication-is-half-the-interview)
- [2. Tactics That Work](#2-tactics-that-work)
  - [2.1. Take a Stance](#21-take-a-stance)
  - [2.2. Drive the Conversation, but Listen](#22-drive-the-conversation-but-listen)
  - [2.3. Justify, Don't Name-Drop](#23-justify-dont-name-drop)
  - [2.4. Scope the Response](#24-scope-the-response)
  - [2.5. Handle Disagreement at the Assumption Level](#25-handle-disagreement-at-the-assumption-level)
- [3. Common Red Flags](#3-common-red-flags)
- [4. The Interviewer's Leveling Rubric](#4-the-interviewers-leveling-rubric)
- [5. The "Jimmy" Archetype](#5-the-jimmy-archetype)
- [Sources](#sources)

## 1. Why Communication Is Half the Interview

Both authors agree the interview measures problem-solving under ambiguity, not memorized solutions. Liu's framing: three skills are evaluated in parallel — problem-solving under trade-offs, technical knowledge of components, and communication of the reasoning. Xu's framing: the format simulates two co-workers tackling an unfamiliar problem together. Pacing matters: poor pacing makes the interviewer switch off like someone falling asleep in a dull talk.

## 2. Tactics That Work

### 2.1. Take a Stance

Confidence is signalled by framing. "Do you think this design would work?" reads as asking for hints. The stronger pattern: state the options and trade-offs, then pick one. *"Here are the options I can think of and I would pick option 1 because of these assumptions. Is there any direction you would like me to go into?"* Asking for a hint when genuinely stuck is fine; sounding unsure while holding reasonable options is what hurts.

Every deep dive ends in a stance. "It really depends on the use cases" is not a conclusion — senior engineers must commit under ambiguity.

### 2.2. Drive the Conversation, but Listen

Driving the conversation is a leadership signal — the candidate does most of the talking and steers toward areas of strength. But yielding when redirected is equally important. Talking over the interviewer blocks the candidate from hearing what is being evaluated.

Xu adds: never go silent for long stretches; never assume the interview is done before the interviewer says so.

### 2.3. Justify, Don't Name-Drop

The majority of what is evaluated is the *justification*. "I will use a wide-column store" is weak. Tying the choice to a 100k write QPS, a write-heavy access pattern, and time-series disk locality is strong. Reciting how WebSocket works is an encyclopedia entry unless it is applied to a design choice.

Both authors single out the same anti-pattern: applying a canned design (Cassandra + Snowflake "because that's how Twitter does it") fails the moment the interviewer changes an assumption the canned design didn't cover.

### 2.4. Scope the Response

When asked "tell me more about the queue," offer a menu before diving: "Would you like me to discuss what kind of queue and why, or talk about scalability?" This shows scope discipline and lets the interviewer point at the part they want to hear.

Don't sweep shallowly across the whole product — narrow to one or two features. Don't burn ten minutes on OAuth 2.0 in a private-messaging design. Math is used with purpose ("QPS is 100k, so we'll need to scale app servers since each handles ~30k") and never done before API and schema.

### 2.5. Handle Disagreement at the Assumption Level

Disagreements usually stem from different assumptions. Neutralize by addressing the root, not the surface claim. *"We can A/B test location-update frequency and monitor customer feedback"* deflates an argument better than insisting the original number was right. Keep a backbone — back each stance with strong justifications — but don't make the interviewer look bad.

## 3. Common Red Flags

Both books converge on the same list:

- Jumping to a solution before clarifying scope.
- Buzzword answers without internals (saying "use Redis" without saying why).
- Not asking clarifying questions.
- Not understanding even after hints.
- Designs that fail the stated requirement even after pointers.
- Recapping the whole interview as a monologue without checking direction.
- Going silent when stuck instead of thinking out loud.
- Over-studied trivia (e.g., naming EdgeRank components for a Facebook feed) that complicates the conversation rather than clarifying it.

## 4. The Interviewer's Leveling Rubric

Liu gives candidates a window into how the rubric works. Level terminology is company-agnostic:

| Level | Years | Typical title |
|---|---|---|
| L2 | 2–5 | Mid-level engineer |
| L3 | 5–10 | Senior engineer |
| L4 | 10+ | Staff engineer |

The same four-tier structure ("No Hire / L2 / L3 / L4") repeats across every step of the framework. The rising axis is consistent:

- Less guidance needed.
- More trade-offs surfaced proactively.
- More tying of decisions back to requirements.
- More awareness of what *not* to include — cost-awareness, removing unnecessary components.
- Proactive listing of all critical trade-offs *and* alternatives in case requirements change.

A candidate targeted at L3 who performs at L2 may be down-leveled. A candidate targeted at L4 who performs at L2 or below is likely rejected. Liu observes that junior candidates often outperform seniors because they prepare harder.

**No Hire signals** are also consistent: no clarifying questions, no understanding after hints, buzzword answers without internals, designs that fail the requirement even after pointers.

## 5. The "Jimmy" Archetype

Xu introduces "Jimmy" as the kid who blurts out an answer fast. Jimmy is the behavior to avoid: rushing to a solution before scope is clear. The most valuable skill is asking the right questions — features in scope, current scale, anticipated growth, the company's tech stack, existing services to leverage.

Liu's golden question — *"What is the problem I am trying to solve?"* — is the same idea phrased as a self-check.

## Sources

- [Liu Ch 3: Interviewer's Perspective](software/system-design-interview/books/system-design-interview-fundamentals/ch03_interviewers_perspective.md)
- [Liu Ch 4: Communication Tactics](software/system-design-interview/books/system-design-interview-fundamentals/ch04_communication_tactics.md)
- [Xu Ch 3: A Framework for System Design Interviews](software/system-design-interview/books/system-design-interview-insiders-guide/ch03_framework_for_system_design_interviews.md)
