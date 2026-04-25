# Ch 2: The Six-Step Framework

## Table of Contents

- [1. The Framework at a Glance](#1-the-framework-at-a-glance)
- [2. Step 1: Gather Requirements](#2-step-1-gather-requirements)
- [3. Step 2: Define API](#3-step-2-define-api)
- [4. Step 3: High-Level Diagram](#4-step-3-high-level-diagram)
- [5. Step 4: Data Model and Schema](#5-step-4-data-model-and-schema)
- [6. Step 5: End-to-End Flow](#6-step-5-end-to-end-flow)
- [7. Step 6: Deep Dive Design](#7-step-6-deep-dive-design)

## 1. The Framework at a Glance

- **Why a framework** — an unstructured interview is hard to follow for both sides; in a 40-minute slot the steps and timings must fit
- **Top-down flow** — requirements → API → high-level diagram → schema → end-to-end flow → deep dives; starting from the middle loses the big picture
- **Suggested timing** (40-minute interview):

| Step | Timing |
|---|---|
| 1. Gather Requirements (functional) | 2 min |
| 1. Gather Requirements (non-functional) | 3–5 min |
| 2. Define API | 3–5 min |
| 3. High-Level Diagram | 5–7 min |
| 4. Schema and Data Structure | 5–7 min |
| 5. End-to-End Flow | 2–3 min |
| 6. Deep Dives | 15–20 min |

> **Warning** — do back-of-the-envelope calculations *after* API and schema are finalized, not upfront; you can't calculate QPS without knowing which API, or storage without knowing schema. Prefer doing the math inside the deep dive, where the numbers *justify* a scalability discussion.

## 2. Step 1: Gather Requirements

- **Purpose** — test your ability to clarify an open-ended, ambiguous problem and lock in shared assumptions with the interviewer
- **Functional requirements = user stories** — act as a PM: ask *who is it for and why*, not just *what features*. Narrow to 1–2 features and get the interviewer's buy-in; too many features force a breadth-only session
- **Clarify terminologies** — for a "Netflix recommendations" feature, drill into what a recommendation contains and what ranking signals feed it; don't over-engineer the ML model unless that's the interview
- **Non-functional = scale + performance constraints** — the area that makes the design unique and engineering-focused; spend more time here
- **Scale questions to ask** — how many active users, how are they distributed globally, what scenarios drive **high QPS** (e.g., concert-end for ridesharing, royal wedding for livestream), what scenarios drive **high storage/bandwidth** (super users, large files, peak hours)
- **Performance constraints** — availability vs consistency (frame as user experience, not "AP vs CP"), accuracy (different from consistency — eventual consistency is eventually *accurate*), response time / latency, freshness, durability

> **Reminder** — Response Time = Latency + Processing Time. Response Time = time between client sending the request and receiving the response. Latency = time the request waits before being processed. Processing Time = time to process the request. For most simple pass-through APIs, Response Time ≈ Latency.

- **Freshness categories** — **real-time** (stock trader, delay causes wrong trades), **near real-time** (Facebook Live, few-second delay acceptable), **batch process** (static-site web crawler, hours-to-days is fine)
- **Durability in 9s** — "nine 9s" = 99.999999999% (0.000000001% loss per year). Don't memorize the exact number of 9s; frame it as impact on the end user (life photos = high, old chats = medium, driver location snapshot = low)

## 3. Step 2: Define API

- **Purpose** — a detailed contract between client and backend; without it, discussions get hand-wavy and incomplete
- **Three parts**: API signature, input parameters, output response. Most candidates forget to define the output
- **Signature** — use a readable name like `request_ride`, not `rides` or `fetch`. Don't elaborate on REST/protobuf unless the interviewer asks — candidates lose 7+ minutes on RESTful design that interviewers don't care about
- **Input rule: everything counts.** Don't add parameters you can't justify (distracting), don't omit ones the requirement needs (missing photo bytes, pickup location, user ID for feed), don't put vague ones (ambiguous time granularity) or nonsensical ones (client-generated `photo_id` or `timestamp`, `friend_name` instead of `friend_user_id`)
- **Output matters as much as input** — must satisfy the requirement (include sorted folders+files if that was agreed), and the data structure changes the design:

| Response | Implication |
|---|---|
| `{ driver_ids: [1, 2] }` | User picks a driver; need to handle concurrency when multiple riders pick the same driver |
| `{ driver_id: 1 }` | Server assigns; no concurrency issue at the API boundary |

- **Response codes** — HTTP codes are a useful reference but don't map 1:1; define what *your* SUCCESS means (request accepted vs. fully processed)
- **Intuition on inefficiencies** — collections in the response (feed list, photo list) suggest pagination and thumbnails; call this out proactively

## 4. Step 3: High-Level Diagram

- **Purpose** — set foundations, show an end-to-end flow that satisfies the requirements
- **Position** — goes *after* API (the API is the diagram's entry point) and *before* schema (you don't know what data stores you need until the flow is drawn)
- **Systematic approach** — for each API: (1) draw the client, (2) draw the next logical blocks from client to the last component, (3) repeat for the next API, connecting to what you already drew. Candidates who "list microservices" tend to miss components
- **Don't add generic boxes** — DNS, auth, logging, deployment, rate limiter are distracting unless unique to the question. Don't add boxes for features you already agreed to drop (payment, fraud, ETA)
- **Don't prematurely optimize** — adding a cache cluster or sharding during the high-level step without justification is hand-wavy. Keep the diagram simple, optimize in deep dive
- **Table interesting discussion points** — when you're tempted to dig in, write the topic on the side ("queue for bursty traffic", "driver-location index", "ride-matching concurrency") and come back during deep dive. Interviewers perceive this as focused and technically aware
- **Logical separation** — one microservice box per responsibility (matching service separate from notification service) for clarity, even if they'd co-host in production
- **Depth-oriented questions** — some prompts (e.g., rate limiter) don't have much high-level structure; finish the bare diagram and go deep

## 5. Step 4: Data Model and Schema

- **Purpose** — concretize the diagram; schema decisions affect performance and downstream discussions (sharding, indexing, caching)
- **Add detail to arrows** — an arrow from match service → location service could mean an unsorted list of driver IDs, a list with scores, or a single driver ID — each implies different downstream work (ranking, score persistence, concurrency)
- **Add detail to queues** — what goes in matters. Enqueuing `raw_video_id` and reading bytes from blob storage is far better than enqueuing the video bytes themselves, which exhausts memory
- **Add detail to databases and caches** — flat table (`driver_id | x | y`) vs table + index (`position_id → driver_ids`) changes query efficiency; explicit schema makes efficiency discussions possible
- **Don't add irrelevant columns** — a ride-status question doesn't need `estimated_cost`, `number_of_rides_taken`, `fraud_status`; focus on columns the agreed requirement needs
- **Table lengthy optimizations** — quick denormalization (join avoidance) is fine inline; sharding and MySQL vs NoSQL debates belong in deep dive, after query patterns are clear
- **Check for nonsensical design** — a `Message Table(user_id, receiver_id, message, timestamp)` fails for group chat because a user and receiver can belong to multiple rooms; always walk through the schema against the requirement

## 6. Step 5: End-to-End Flow

- **Purpose** — before jumping into deep dives, walk each API through the system and confirm it satisfies the requirements; also a checkpoint to add more items to the discussion list
- **Most candidates skip this step** — they jump straight to scalability without confirming a working system, which leaves the interviewer unsure the baseline works
- **Two sub-steps**: (1) trace each API end-to-end, flagging "come back to this" items (possible micro-batches, concurrency); (2) ask the interviewer which discussion point to dig into first

## 7. Step 6: Deep Dive Design

- **Purpose** — identify bottlenecks, propose solutions, discuss trade-offs; this is where seniority shows

> **The System Design Interview Golden Question: "What is the problem I am trying to solve?"** Solution-first thinking (adding a cache, sharding) without stating the problem is the most common failure mode. Concluding that something *isn't* a problem and doesn't need solving is a strong positive signal — you wouldn't shard a 1-QPS startup database in real life either.

- **Magic formula** (6-step loop):

  1. Identify a bottleneck
  2. Come up with options (aim for 2 — one option reveals no problem-solving)
  3. Talk about the trade-offs (tie back to the functional and non-functional requirements)
  4. Pick one solution (take a stance; "right or wrong" matters less than sound reasoning)
  5. Active discussion with the interviewer
  6. Go back to step 1

- **Come up with your own bottlenecks** — there's no real monitoring dashboard or PM in an interview; you set up scenarios where you can shine (a thundering-herd expert frames a concert-end scenario for ridesharing)
- **Categories to mine for discussion points**:
  - **API and interprocess arrows** — latency sensitivity (typeahead needs p95 10 ms; airline booking doesn't), high QPS, bursty/thundering herd, slow/congested network, query optimization (input size, output size, call count), further technical detail (TCP vs UDP, short poll vs WebSocket)
  - **Microservices, queue, databases** — failure scenarios (partial vs complete), high amount of data, deeper dives on any component, design choices between database/queue types
  - **Algorithm, data structure, schema** — look for alternatives (append-only location table → can you store less or optimize the lookup?)
  - **Concurrency** — shared resources accessed simultaneously; mastery in this area separates candidates
  - **Operational issues and metrics** — queue spillover, batch-job success, anything whose silent failure harms users
  - **Security** — overlooked by most candidates; bring up man-in-the-middle, ticket-locking abuse, money-transfer validation even when not asked
- **Handling disagreement** — disagreements usually stem from different assumptions; neutralize by addressing the root (e.g., "to find the right location-update frequency, test and monitor customer feedback"). Read the room — if the interviewer is headstrong, restate your options and trade-offs and ask for questions
- **Priority of discussion** — interview time is limited; favor problems where impact is severe (users churn, money lost, internet saturated). Skip low-impact discussions (bandwidth compression on a low-payload notification, sub-50ms airline checkout, load-balancer algorithm in a photo-storage system)
