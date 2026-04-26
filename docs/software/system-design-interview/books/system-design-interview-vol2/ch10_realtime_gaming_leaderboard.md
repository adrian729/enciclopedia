# Ch 10: Real-time Gaming Leaderboard

## Table of Contents

- [1. Problem and Scope](#1-problem-and-scope)
- [2. High-Level Design](#2-high-level-design)
- [3. Storage Options](#3-storage-options)
  - [3.1. Why Relational Fails](#31-why-relational-fails)
  - [3.2. Redis Sorted Sets](#32-redis-sorted-sets)
- [4. Storage Sizing](#4-storage-sizing)
- [5. Cloud vs Self-Managed](#5-cloud-vs-self-managed)
- [6. Scaling Redis: Sharding](#6-scaling-redis-sharding)
- [7. NoSQL Alternative](#7-nosql-alternative)
- [8. Operational Concerns](#8-operational-concerns)

## 1. Problem and Scope

- **Leaderboard** — ranking display showing top competitors plus the requesting user's own position; Marvel Contest of Champions is the reference example.
- **Functional requirements** — show top 10 players, show a specific user's rank, optionally show 4 players above and 4 below the user.
- **Non-functional requirements** — real-time score updates (no batched history), general scalability, availability, reliability.
- **Tournament cadence** — a new leaderboard kicks off every month; previous months go to historical storage.
- **Scoring rule** — 1 point per match win; ties produce equal ranks.
- **Scale** — 5M DAU, 25M MAU, average 10 matches/day per player.
- **QPS estimates** — score updates avg 500/sec, peak 2,500/sec; top-10 fetches avg 50/sec (assuming one fetch per user per day on app open).

## 2. High-Level Design

- **Two services** — **Game Service** validates wins and forwards to **Leaderboard Service**; leaderboard service writes to the leaderboard store and serves rank/top-10 reads directly to clients.
- **Server-authoritative scoring** — clients never write scores directly; client-set scores are vulnerable to **man-in-the-middle attack** where a proxy alters the score in transit.
- **Skip the message queue** — Kafka between game and leaderboard makes sense only if multiple consumers (analytics, push notifications, billing) need the same event stream; not required by the stated requirements.

### API surface

| Endpoint | Purpose |
|---|---|
| `POST /v1/scores` | Internal-only — game server adds points after a win (`user_id`, `points`) |
| `GET /v1/scores` | Top 10 of the current leaderboard |
| `GET /v1/scores/{user_id}` | Specific user's rank and score |

## 3. Storage Options

### 3.1. Why Relational Fails

- **Naive RDBMS schema** — `leaderboard(user_id, score)`; rank computed by `ORDER BY score DESC` and counting rows above.
- **Rank query is a table scan** — to get any single user's rank, sort all rows; over millions of rows this takes tens of seconds, unacceptable for real-time.
- **Caching doesn't help** — scores change continuously, invalidating any cached rank ordering.
- **`LIMIT 10` helps top-10 but not rank** — index + `ORDER BY score DESC LIMIT 10` returns the leaders quickly but still can't answer "what's user X's rank" without scanning.

### 3.2. Redis Sorted Sets

- **Sorted set** — Redis data type where each unique member carries a score; internally a hash table (member → score) plus a skip list (score → member) so all operations are `O(log n)`.
- **Skip list** — sorted linked list augmented with multi-level indexes that skip every other node at each level, giving binary-search-like traversal; chapter cites a 62-node walk reduced to 11 nodes with 5 index levels.
- **Why it beats RDBMS** — elements are kept in order on every insert/update; ranks are read in `O(log n)` instead of requiring a full sort.

### Key Redis commands

| Command | Effect | Cost |
|---|---|---|
| `ZADD` | Insert member or update score | `O(log n)` |
| `ZINCRBY key delta member` | Increment a member's score (auto-creates at 0) | `O(log n)` |
| `ZREVRANGE key 0 9 WITHSCORES` | Top 10 with scores, descending | `O(log n + m)` |
| `ZREVRANK key member` | User's 0-based rank, descending | `O(log n)` |

- **Per-month keys** — `leaderboard_feb_2021` etc.; rolling new sorted set each month, prior month archived.
- **Score-a-point** — `ZINCRBY leaderboard_feb_2021 1 'mary1934'`.
- **Relative window** — for user `Mallow007` at rank 361 wanting ±4 neighbors, run `ZREVRANGE leaderboard_feb_2021 357 365`.

## 4. Storage Sizing

- **Per-entry footprint** — 24-char user_id + 16-bit score ≈ 26 bytes per leaderboard entry.
- **Worst case** — all 25M MAU have at least one win → 26 B × 25M ≈ 650 MB; double to ~1.3 GB to account for skip list + hash overhead, easily fits one Redis instance.
- **CPU/IO** — peak 2,500 updates/sec is well within a single Redis node's envelope.
- **Persistence** — Redis persistence works but cold-start from disk is slow; standard practice is a read replica that gets promoted on primary failure with a fresh replica attached.
- **Supporting MySQL tables** — `user(user_id, display_name)` and `point(user_id, score, timestamp)`; the point table doubles as the source of truth for rebuilding Redis after a cache failure.
- **Optional user-detail cache** — for the top 10, who are read most frequently.

## 5. Cloud vs Self-Managed

- **Self-managed** — own Redis nodes, own MySQL, own API servers; query MySQL alongside Redis to fetch profile fields for display.
- **AWS serverless option** — Amazon API Gateway routes REST endpoints to AWS Lambda functions (`LeaderboardFetchTop10`, `LeaderboardFetchPlayerRank`, `LeaderboardUpdateScore`) which talk to Redis + MySQL.
- **Equivalents** — Google Cloud Functions, Microsoft Azure Functions.
- **Recommendation** — for a greenfield game, lean serverless; auto-scaling and zero infra maintenance outweigh the loss of low-level control.

## 6. Scaling Redis: Sharding

- **When sharding is needed** — at 500M DAU (100× original) the leaderboard reaches ~65 GB and ~250K QPS, beyond a single node.

### Fixed partition

- **Partition by score range** — e.g., 10 shards spanning [1–100], [101–200], …, [901–1000]; top 10 lives entirely in the highest-range shard.
- **Score-to-shard map** — to update a user, look up their current score (cache a `user_id → score` secondary mapping) and route to the right shard; on score crossing a boundary, remove from old shard and update the mapping.
- **Rank computation** — local rank within shard + sum of player counts in higher shards (`info keyspace` returns shard size in `O(1)`).
- **Distribution caveat** — score ranges must be tuned so shards stay roughly balanced.

### Hash partition (Redis Cluster)

- **Hash slots** — 16,384 slots; key's slot is `CRC16(key) % 16384`; nodes own contiguous slot ranges and adding/removing a node moves only the affected slots.
- **Top-10 via scatter-gather** — query all shards in parallel, application-side merges and sorts; latency bounded by slowest shard.
- **Limitations** — large-K results are slow (lots of cross-shard data), tail latency dominated by slowest partition, no straightforward way to compute a single user's global rank.
- **Verdict** — book leans toward fixed partition for leaderboards because rank queries don't naturally fan out.

- **Sizing rule** — write-heavy Redis nodes need ~2× the working-set memory to accommodate snapshot creation under failure; benchmark with `redis-benchmark`.

## 7. NoSQL Alternative

- **Desired NoSQL properties** — write-optimized, efficient sort within a partition by score.
- **Candidates** — DynamoDB (used as the worked example), Cassandra, MongoDB.
- **Initial DynamoDB schema** — partition key `game_name#{year-month}`, sort key `score`; suffers a hot partition because all of the current month's writes hit one node.
- **Write sharding fix** — append `#p{partition_number}` (with `partition_number = user_id % N`) to the partition key; now the month's data is spread across N partitions.
- **Read complexity tradeoff** — top 10 requires scatter-gather across all N partitions and an application-side merge; more partitions = lower per-partition load but higher fan-out.
- **Global secondary index** — keyed by the same sharded partition key with `score` as sort key, so each partition is locally sorted.
- **Percentile rank** — exact rank across N shards is hard; instead, a cron job computes the score distribution per shard and caches percentile cutoffs (e.g., "90th percentile = score < 6500"), so users see "you're top 10–20%" rather than "rank 1,200,001".

## 8. Operational Concerns

- **Tie-breaking with Redis Hash** — store `user_id → last-win-timestamp`; on tied scores, older timestamp ranks higher.
- **User-object cache** — Redis Hash keyed by user_id holding the display object, eliminates a MySQL hop when rendering the top 10.
- **System failure recovery** — replay the MySQL `point` table chronologically with `ZINCRBY` per row to rebuild the Redis sorted set after a cluster-wide failure.
