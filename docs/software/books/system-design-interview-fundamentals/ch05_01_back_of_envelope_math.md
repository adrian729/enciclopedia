# Ch 5.01: Back-of-the-Envelope Math

## Table of Contents

- [1. Why Do the Math at All](#1-why-do-the-math-at-all)
- [2. When to Skip the Math](#2-when-to-skip-the-math)
- [3. QPS Formula](#3-qps-formula)
- [4. Storage Capacity Formula](#4-storage-capacity-formula)
- [5. Six-Step Calculation Technique](#5-six-step-calculation-technique)
- [6. Common Mistakes](#6-common-mistakes)

## 1. Why Do the Math at All

- **Numbers justify design choices** — a calculated 10⁸ QPS against a single machine's ~10⁶ capacity identifies a scaling problem and lets you propose solutions; conversely, dismissing the need to scale based on a calculated result reflects strong judgment
- **Keeps you from spewing concepts** — if the numbers come out to 10 QPS and you start proposing caching and sharding, it looks bad; scalable solutions need a solid numerical reason
- **Do it *after* API and schema, not upfront** — QPS is tied to a specific API and storage is tied to a specific schema; calculating early forces guesswork and usually misses APIs and tables

## 2. When to Skip the Math

- **Ask the interviewer for QPS and storage directly** — they may just say "assume a lot" (meaning: scale) or hand you the number, saving you time
- **Ask if you can assume you need to scale beyond a single machine** — in most interview contexts it doesn't matter if it's 5 or 50 machines; what matters is that one isn't enough
- **If the interviewer does want math, do it fast and accurately** — many interviewers don't want to watch you do algebra; wasted minutes here are minutes not spent on system discussion

## 3. QPS Formula

- **Query per day (QPD)** — `Daily active users × % of active users making the query × avg queries per user per day × scaling factor`
- **QPS ≈ QPD / 100k** — there are 86,400 seconds per day (24 × 60 × 60), rounded up to 100k for easier math. Mental trick: dividing by 100k just subtracts 5 from the power of 10 (e.g., 10¹¹ / 100k = 10⁶)
- **Design for the worst case** — real systems measure p50/p90/p95/p99; target the QPS that can break your system, not the average
- **Daily Active Users** — ask the interviewer; if only total users are given, assume a percentage are active
- **% of active users making the query** — not all active users perform every action (e.g., on Facebook News Feed most users read, few post; 1%–20% writer-to-reader ratio is a fair assumption)
- **Avg queries per user per day** — apply common sense (1–5 News Feed posts per active user per day is reasonable; 1,000–2,000 raises eyebrows). Follow the interviewer's flow if they override the assumption
- **Scaling factor** — multiply by some factor to capture worst-case scenarios (e.g., ridesharing weekend nights ≈ 5–10× average traffic); the point is to demonstrate awareness of potential bottlenecks, not to multiply numbers

## 4. Storage Capacity Formula

- **Formula** — `Daily active users × % of active users making the query to persist × avg queries per user × data size per query × replication factor × time horizon`
- **Data size per query** — count *all* data (e.g., Instagram post = photo bytes *and* metadata). Don't sum columns precisely to 68 bytes; round to 50 or 100. Appendix 2: Capacity Number helps with assumptions
- **Replication factor** — typically 3 for database backups; the point is to show you've thought about it
- **Time horizon** — usually 1–5 years is fine; in practice, capacity planning is very contextual

## 5. Six-Step Calculation Technique

Worked example: daily active users 200M, 10% post photos, 10 photos per user, 10 MB per photo, replication 3.

- **Step 1: Convert all numbers to scientific notation** — multiplying 200 million by 10 MB directly is error-prone; convert to `A × 10ᵇ` form first. Mental trick: every comma in a number shifts the power of 3 by one (e.g., 10,000 has one comma → 10³ shifted once → 10⁴; 100,000,000 has two commas → 10⁶ shifted twice → 10⁸). Target: produce the notation in under 2 seconds without mistakes
- **Step 2: Group all the 10s together** — 10⁸ × 10⁷ × 10¹ = 10¹⁶
- **Step 3: Group all other numbers together** — 10% × 3 × 2 × 1 = 0.6
- **Step 4: Find the final number** — 0.6 × 10¹⁶ → 6 × 10¹⁵
- **Step 5: Convert to a readable number** — using Appendix 1: Conversion Table, 6 × 10¹⁵ → 6 Petabytes; humans reason in PB, not 10¹⁵
- **Step 6: Do something with the number** — use Appendix 2: Capacity Numbers to reason about scaling (e.g., if each host stores ~1 TB, 6 PB/day requires scaling up servers)

## 6. Common Mistakes

- **Spending too long on the calculation** — of a 40-minute interview, intro and Q&A consume ~10 minutes, leaving 35 for technical. If math eats more than 10 of that, a third of your technical time is algebra, not system design
- **Calculation mistakes** — common slips: confusing GB with TB (magnitude-of-1,000 error), losing a 0 (magnitude-of-10 error). One-off mistakes may not be game-ending but look bad; practice the method to do it quickly and accurately
- **Not doing anything with the result** — calculating 6 PB/day is worthless if you move on without it; the interviewer wants to see how you use the number to identify bottlenecks and propose solutions
- **Calculating unimportant numbers** — spending 2–3 minutes on bandwidth for a lightweight heartbeat service signals poor technical judgment; develop intuition for what matters to the bottleneck
- **Doing the math too soon** — current trend is to calculate right after requirements, before API and schema. QPS is per-API and storage is per-schema; Instagram has `post_feed` and `view_timeline` APIs and both metadata and photo storage — skipping API/schema first leads to missed cases
