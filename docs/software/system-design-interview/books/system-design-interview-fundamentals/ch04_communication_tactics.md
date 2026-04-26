# Ch 4: Communication Tactics

## Table of Contents

- [1. Delivery and Presence](#1-delivery-and-presence)
- [2. Driving the Conversation](#2-driving-the-conversation)
- [3. Listening and Two-Way Flow](#3-listening-and-two-way-flow)
- [4. Taking a Stance](#4-taking-a-stance)
- [5. Justifying Your Design](#5-justifying-your-design)
- [6. Handling Disagreement](#6-handling-disagreement)
- [7. Scope and Focus](#7-scope-and-focus)
- [8. Using Math and Technical Detail](#8-using-math-and-technical-detail)
- [9. Avoiding Canned Answers](#9-avoiding-canned-answers)

## 1. Delivery and Presence

- **Improve public speaking** — a system design interview is heavily about how you present yourself; poor pacing or delivery makes the interviewer switch off like people falling asleep in a boring presentation. Invest in pacing, enunciation, modulation, body language, and confidence; engineers over-weight technical skill and forget soft skills matter just as much
- **Show confidence with your justifications** — phrases like "Do you think this design would work?", "What do you think about the solution?", "Am I missing anything?", and "Am I heading in the right direction?" read as indirectly asking for hints and hurt your behavioral score. You shouldn't be designing something you think doesn't work, and the interviewer is there to evaluate your thought process, not share theirs
- **Replacement phrasing** — present what you can think of, then close with "Here are the options and trade-offs I can think of and would pick option 1 because of the assumptions. Is there any direction you would like me to go into?" If the interviewer is satisfied they'll say so; if something is missing they'll bring it up
- **When genuinely stuck** — asking for a hint is fine; the problem is candidates who have reasonable options but still sound unsure

## 2. Driving the Conversation

- **Control the interview** — you do most of the talking and should steer toward areas where you're strongest (e.g., if you're stronger on databases than concurrency control, drive the deep dive toward databases). Having structure makes the presentation stronger
- **But yield when the interviewer redirects** — if they stop your flow and point you at something specific, follow them; they're looking for a particular data point

## 3. Listening and Two-Way Flow

- **Listen to the interviewer** — any system design question can go in infinite directions; sometimes the interviewer lets you talk and sometimes they interject with a direction. If unsure what they're asking, clarify; after answering, confirm you addressed their concern. Not doing this reads as poor listening
- **Don't talk over the interviewer** — driving the interview is a leadership quality, but continuously talking so the interviewer can't speak, or interrupting them mid-sentence, is rude and — more importantly — means you aren't hearing what they're looking for. If you talk over them, it doesn't matter what you say because they won't be listening
- **Scoped response pattern** — when asked "Tell me more about the queue", don't answer with an unrelated tangent ("I'm using Kafka, now back to sharding…"). Instead, offer a menu: "Would you like me to discuss what kind of queue and why, or talk about scalability?" then justify ("Kafka because replay capability is useful for this streaming question in case the aggregator goes down") and check for direction

## 4. Taking a Stance

- **Conclude and make a stance** — when you've listed options and trade-offs, don't leave them in the air with "it really depends on the use cases." Senior engineers must deal with ambiguity and commit; use your agreed-upon assumptions to strengthen the choice ("I'm going to assume users only visit once a day so I'll pick option 2 — is that assumption fine?")
- **Downstream impact** — later designs stack on top of earlier decisions; leaving the design open makes the rest of the interview hard to follow

## 5. Justifying Your Design

- **Articulate your thoughts** — sharing the thought process is the majority of what the interviewer is looking for. Naming the right technology without justification still fails the interview because the choice is contextual to the assumptions you agreed on
- **Justification example** — "I will use a wide-column store" is weak; "I will use a wide-column store because the write-to-read ratio is extremely high with 100k write QPS where I expect an RDBMS to not perform as well; also, based on the time-series nature of the query, wide-column is a better fit because of disk locality" is strong
- **Discussion point with trade-offs** — for each core discussion point, bring up a couple of options, discuss pros and cons, and sell the interviewer on your final choice. Just describing what you'll do makes you sound like you memorized a blog post and haven't considered alternatives; it also fails to show you can handle design dilemmas where no option is strictly better
- **Spewing technical details with an intention** — reciting how WebSocket works isn't impressive on its own; technical knowledge only lands if applied to justify a choice. Frame it as "our requirement is near-instant delivery; options are periodic pull or WebSocket; WebSocket's bidirectional push beats polling's delay" rather than a WebSocket encyclopedia entry

## 6. Handling Disagreement

- **Resolving disagreement** — when the interviewer seems skeptical, they may or may not actually disagree; mishandling this rejects candidates
- **Possibility 1: they propose a solution** — treat it like a colleague proposing an alternative; digest it, produce pros and cons, and rethink your conclusion. It's acceptable to stick with your original choice after trade-off discussion, but staying adamant when you're "wrong" looks bad
- **Possibility 2: they seem to like their solution** — don't get defensive or argumentative; disagreements usually stem from misaligned assumptions. Take a neutral stance and acknowledge where they're coming from. Example (ridesharing driver-location frequency): "I understand your concern is freshness. In practice we can experiment with different update rates through A/B testing and adjust accordingly; for now we can go with a more frequent update"
- **Still keep a backbone** — don't capitulate to everything the interviewer says; back your stance with strong justifications, but don't make the interviewer look bad

## 7. Scope and Focus

- **Keep the requirements simple** — candidates who over-studied (e.g., Facebook EdgeRank signals for affinity/weight/decay) unnecessarily complicate the interview. Better: "I know Facebook uses EdgeRank; for now we'll assume scores are computed and stored, and if we have time we'll revisit updating them — is that OK?"
- **Quality over quantity** — interviews are short. Avoid the trap of listing many requirements in a **hand-wavy** manner; Uber has thousands of engineers and you won't cover everything. Better to narrow ("I am only going to focus on rider and driver matching for now; if we have time we can revisit more requirements") than to sweep the whole product shallowly
- **Focus on the right things** — after clarifying requirements, many technical sub-components compete for airtime. A private messaging design shouldn't burn 10 minutes on OAuth 2.0. Two caveats: (1) if the interviewer explicitly asks for an area, follow them; (2) if the interview is domain-specific (e.g., security), the heart of the problem shifts

## 8. Using Math and Technical Detail

- **Math with a purpose** — back-of-the-envelope calculations aren't a test of algebra; the results must justify a design choice. "QPS is 100k and storage is 20 PB, let me talk about API now" is wasted math. "QPS is 100k, so we'll need to scale app servers since each server handles ~30k QPS" is math used to justify a decision
- **Don't do the math too early** — candidates often calculate right after gathering requirements, before API, high-level diagram, and schema. That's dangerous: you may only be calculating one API's load, and storage estimates are inaccurate without a finalized schema. The math supports decisions like sharding or adding a cache — and if QPS is low, proposing partitioning adds complexity with no benefit

## 9. Avoiding Canned Answers

- **Don't jump into a real-world design** — studying via blogs and tech talks is fine, but don't memorize and retell a design you read somewhere ("I will use Cassandra with Snowflake for ID generation because that's a well-known design"). Apply the fundamentals to the interview's specific requirements and non-functional assumptions; memorized answers are obvious because the candidate isn't flexible when the problem deviates
