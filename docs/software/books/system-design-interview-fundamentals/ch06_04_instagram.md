# Ch 6.04: Instagram

## Table of Contents

- [1. Requirements](#1-requirements)
- [2. API](#2-api)
- [3. High-Level Design](#3-high-level-design)
- [4. Schema](#4-schema)
- [5. End-to-End Flow](#5-end-to-end-flow)
- [6. Deep Dives](#6-deep-dives)

## 1. Requirements

- **Prompt** — design an Instagram-style app: users post a photo with a description, follow others, and see a feed ranked from the people they follow
- **Scope narrowed to**: single photo per post, ranking by **timestamp only** (EdgeRank-style affinity/freshness/engagement signals tabled), feed capped at 500 posts, photo capped at 2 MB, support both mobile and web
- **Assumptions** agreed with interviewer:
  - **500M DAU** worldwide
  - **Long-tail follower distribution** — a few celebrities followed by most people
  - Users can follow up to **1,000 users**
  - **Accuracy** of the feed is important — missing posts ruins the experience
  - **Freshness** can tolerate a couple of minutes of delay
  - **Durability** of posts is very important (life events, childhood photos)
  - **Latency** target: **p99 200 ms**

> **Warning** — premature jump into fan-in/fan-out/hybrid reads as memorized. Start simple, identify the problem, then come up with options and trade-offs.

## 2. API

```
post_feed(user_id, photo_byte, description) → status
read_feeds(user_id, offset) → [feed]
load_image(user_id, photo_url) → photo_byte
```

- **Feed object** = `(photo_url, description)`
- **Timestamp** is server-generated to avoid client-clock skew
- **Pagination** via fixed page size; `offset` selects the paginated chunk (most users never scroll past 20–30 posts)
- **Follower table** assumed to exist already

## 3. High-Level Design

- **Post service** accepts `post_feed`, commits bytes to the photo storage, then commits `(photo_url, description)` to feed storage
- **Feed service** serves `read_feeds`: reads follower list, fetches feeds per followee from feed storage, merges, returns
- **Photo storage** is a blob store; `load_image` fetches bytes by `photo_url`
- **CDN optimization** for bandwidth/latency tabled for deep dive

## 4. Schema

**Feed Storage** — one photo per feed (refactor needed if multi-photo later)

| Feed Id | User Id | Photo Url | Description |
|---|---|---|---|

**Photo Storage** — blob store

| Photo Url | Photo blob |
|---|---|

**Follower Storage** — many-to-many

| Follower Id | Followee Id |
|---|---|

## 5. End-to-End Flow

- **`post_feed`**: poster → post service → photo storage (returns `photo_url`) → feed storage commit with `(photo_url, description)`
- **`read_feeds`**: reader → feed service → read follower list → for each followee fetch feeds from feed storage → merge → serve to reader. Flagged as expensive against the 200 ms target
- **`load_image`**: for each returned `photo_url`, fetch bytes from photo storage

## 6. Deep Dives

### 6.1 Optimize for the Feed Read Query

- **Problem** — p99 200 ms read for a user following up to 1,000 users, top 500 posts by timestamp
- **Options**:

| Option | Upside | Downside |
|---|---|---|
| **Fan-Out (on read)** — fetch 500 posts per followee sorted by timestamp, k-list merge to top 500 | Simple; no precompute | 1,000-key disk IO even batched; 500×1,000 = 500,000 posts kept in memory per op |
| **Compute on Write** — on post, fan out `UserId → [Feed]` to each follower's user feed storage | Read is a fast key-value lookup | Celebrity with 10M followers = 10M key updates; becomes complicated if ranking depends on affinity/decay/unfollow |
| **Periodic Update** — recompute each user's list every few minutes | Fast key-value read; no dependency churn | Recomputing for 500M users (many inactive) is extremely expensive; freshness/cost trade-off |
| **Hybrid Fan-Out + Fan-In** — fan out for non-celebrities, fan in at read time for celebrities | Best of both: no mega fan-out, modest fan-in | Complexity of dynamic celebrity threshold; flipping a user across the threshold causes duplicate or missing posts |

- **Conclusion** — **Option 4 (Hybrid)**. A small operations team handles threshold tuning, dedup, and backfill; automate later

### 6.2 Duplicate Posts

- **Scenario** — a non-celebrity becomes a celebrity: posts already fanned out to user feed storage also get fanned in from the feed table, causing duplicates
- **Options**:

| Option | Upside | Downside |
|---|---|---|
| **Do Nothing** | No extra work; promotion is rare; brief duplicates aren't terrible UX | Occasional duplicates visible |
| **Dedupe via k-list merge** | Uses sorted merge already in place | Same post may not be adjacent — other posts can share the timestamp |
| **Dedupe via HashSet** | Reliable dedup | Memory cost to hold all posts |

- **Conclusion** — **Do Nothing**. Event is extremely rare; duplicates are mildly confusing but not frustrating

### 6.3 Global User Base

- **Concern** — global distribution impacts read latency against the 200 ms p99; write fan-out delay across regions is acceptable
- **Options**:

| Option | Upside | Downside |
|---|---|---|
| **Cross-Regional Read** for the regional celebrity shard | Simple; stronger consistency | Cross-globe latency 150–200 ms — unstable against the 200 ms target; worsens with more regions |
| **Cross-Region Replication** — replicate feed storage to each region; read both user feed storage and feed storage locally | Fast local reads; redundancy reinforces durability | Async replication delay (already acceptable); extra storage beyond pure durability redundancy |

- **Conclusion** — **Cross-Region Replication**. Read latency and durability requirements justify the replication complexity

### 6.4 Distributed Transaction (Photo + Feed Write)

- **Problem** — `post_feed` writes both blob store and feed storage; failure of one leaves inconsistency
- **Options**:

| Option | Upside | Downside |
|---|---|---|
| **Photo first, then feed** | Simple sequential 2-step | Feed write failure leaves unreferenced photos → needs background cleanup job |
| **2 Phase Commit (2PC)** | All-or-nothing; no unreferenced photos | Complex on real storage failures; worse throughput |

- **Conclusion** — **Photo-first sequential**. Feed failures are rare and unreferenced-photo storage cost is low; add background cleanup only if monitoring shows it matters

### 6.5 Feed Ads

- **Setup** — Ads team wants to place ads into feeds; candidate owns the API contract
- **Options**:

| Option | Upside | Downside |
|---|---|---|
| **Periodic Refresh of Ads** — materialize ads into user feed storage in background | Fast read from user feed storage | Hard to predict impressions; an advertiser wanting 10 impressions fanned to 10 inactive users wastes inventory |
| **Fan-In on Read** — `get_ads(user_id) → [ad]` called at read time | Simple; no stale materialized ads | Added service call increases latency; stacks up as more internal customers join |

- **Conclusion** — **Fan-In on Read** with a negotiated **latency SLO** between the feed team and ads team, plus a process for additional internal callers. Fall back to a variant of option 1 if the ads team can't meet the SLO

> **Warning** — the design is trivial on its face; the point is to identify latency accumulation risk and demonstrate SLO leadership as happens in real orgs.

### 6.6 Poor Bandwidth

- **Setup** — global users, some on low bandwidth, struggle to upload
- **Options**:

| Option | Upside | Downside |
|---|---|---|
| **Lossy Client-Side Compression** — reduce resolution before upload | Small compute; less bandwidth | Image quality suffers — costly for a photo-based product |
| **Idempotent Resumable Upload** — assign upload ID; resume from offset after disconnect | Upload eventually completes | Added complexity; long upload time |
| **Limit Upload Size** — e.g., cap at 500 KB instead of 2 MB | Fewer bytes on the wire | Frustrating UX — users must edit before uploading |
| **Point of Presence Near Users** — edge server close to user, then internal network | Shortens untrusted network path; more reliable once internal | Not always feasible globally; long-term (e.g., Facebook Aquila) |

- **Conclusion** — **Idempotent Resumable Upload** with a warning to users about slow uploads and optional quality-lowering; consider edge PoP as a long-term investment
