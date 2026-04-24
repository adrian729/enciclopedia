# Ch 6.08: Chat Application

## Table of Contents

- [1. Requirements](#1-requirements)
- [2. API](#2-api)
- [3. High-Level Design](#3-high-level-design)
- [4. Schema](#4-schema)
- [5. End-to-End Flow](#5-end-to-end-flow)
- [6. Deep Dives](#6-deep-dives)

## 1. Requirements

- **Prompt** — design a public group-chat application (topics span system design, sports, knitting, etc.)
- **Scope narrowed to**: send text messages, read history (scroll up), permanent storage. Images/videos, read receipts, edits/deletes, online status tabled
- **Assumptions** agreed with interviewer:
  - **100M DAU** globally, most in North America
  - **100,000 channels**, long-tail distribution; up to **5,000 users per channel**
  - Bursty traffic at night (hobby chat); max message size **50,000 chars**
  - End-to-end delivery latency target **< 100 ms**
  - Message load time **~200 ms p95**
  - Availability and durability both important; no message corruption

## 2. API

```
send_message(user_id, message, channel_id) → status
read_messages(user_id, channel_id, offset) → [message]
receive_message(channel_id, message)          // server push callback
```

- `message` = text + author + timestamp
- `read_messages` paginates with fixed page size (offset-based) so client doesn't pass size
- `receive_message` is the callback triggered when another user posts

## 3. High-Level Design

- **Chat server** — handles `send_message`, `read_messages`, and maintains **WebSocket** connections for `receive_message`
- **Message queue** — absorbs high write throughput before chat processing
- **Chat processor** — pulls from queue, looks up which chat servers hold WebSocket connections for the channel's recipients, forwards the message
- **Chat storage** — persists messages and channel metadata

## 4. Schema

**Message Queue event**

| User ID | Channel ID | Message | Author | Timestamp |
|---|---|---|---|---|

**Message Table**

| Channel ID | Timestamp | Message | Author |
|---|---|---|---|

**Channel Table**

| Channel ID | Name |
|---|---|

## 5. End-to-End Flow

- **Login / open channel** — client calls `read_messages` for the default channel → chat server fetches latest messages filtered by `channel_id`
- **Send** — message → chat server → message queue → chat processor looks up chat servers holding recipients' WebSockets → `receive_message` pushed to each recipient
- WebSocket-connection lookup is a deep-dive item

## 6. Deep Dives

### 6.1 Channel Concurrency (message ordering)

- **Problem** — two users write to the same channel simultaneously; which ordering is "true"? Per-user consistency is hard because a single user may have multiple sessions

| Option | Upside | Downside |
|---|---|---|
| Per-user version number (client-generated) | Consistent per user | Multiple sessions re-introduce the problem; storage cost |
| Optimistic lock on message write | Consistent ordering | Retry storms make chat unusable under concurrency |
| Pessimistic lock on the channel | Strongly consistent | Only one user writes at a time — terrible UX |
| **Server-generated timestamp as source of truth** | Simple; users rarely notice ordering skew in fast chats | Clock skew across servers (mitigate with periodic clock sync); millisecond-granularity collisions accepted |
| Monotonic distributed ID (e.g., Snowflake) | Unique, roughly ordered | Only roughly ordered; ID order can disagree with attached timestamp |

- **Conclusion** — **server-generated millisecond timestamp (option 4)**. Relaxes per-user consistency: a hard refresh may reorder messages, but concurrent messages have no relationship to each other anyway

### 6.2 Database Choice

- **Access pattern** — write-heavy; reads only when a user opens a channel; reads are "latest N messages for a channel"

| Option | Upside | Downside |
|---|---|---|
| Standard RDBMS (B-Tree) | Well-understood transactions | B-Tree tuned for reads; poor disk locality when fetching a channel's messages (row-oriented storage scatters them) |
| Wide column leader-follower (HBase) | LSM write throughput; column-family locality for a channel; strong consistency via leader | Brief unavailability on leader election |
| **Wide column leaderless (Cassandra)** | LSM write throughput; better availability (no leader election) | Write conflicts (not an issue here since edit/delete is out of scope) |

- **Conclusion** — **Cassandra-style leaderless wide column**. RDBMS ruled out at this scale; leaderless wins on availability and edits/deletes are out of scope so conflicts aren't a concern

### 6.3 Chat Architecture (broadcast vs persist order)

| Option | Upside | Downside |
|---|---|---|
| **Simultaneous fan out to storage and notification** | Low end-to-end latency | Notification may be sent for a message that failed to persist (inconsistency) |
| Write to disk first, then broadcast | Notified messages are guaranteed durable | End-to-end latency includes disk write |

- **Conclusion** — **simultaneous fan out (option 1)** given the < 100 ms target; monitor storage failure rate and retry. Accept rare inconsistency

### 6.4 Read Performance

| Option | Upside | Downside |
|---|---|---|
| Full table scan | No index write cost | Poor read latency |
| **Compound index on `(channel_id, timestamp)`** | Latest-N pagination is efficient | Slower writes |
| Read cache (write-around + read-through, or write-back) | Faster reads | Writes invalidate frequently; write-back risks losing messages before disk |

- **Reminder** — cache isn't a default answer; often the conclusion is "no cache"
- **Conclusion** — **compound index (option 2)**. Writes are notified before disk, so the index's write slowdown is not on the critical path

### 6.5 Real-Time Protocol

| Option | Upside | Downside |
|---|---|---|
| Short polling | Simple HTTP | Many wasted calls when no update |
| Long polling | Fewer wasted calls | Server keeps connections open; timeouts need client retry |
| **WebSocket** | Push on new message; persistent bidirectional connection | Infrastructure complexity to maintain WebSocket fleet |

- **Conclusion** — **WebSocket**

### 6.6 Database Sharding

| Option | Upside | Downside |
|---|---|---|
| Shard by `channel_id` (consistent hashing) | All messages for a channel on one shard | Hotspot on popular channels; storage imbalance |
| Shard by timestamp bucket | Latest messages for all channels in one shard | All writes go to the current-time shard — global hotspot |
| **Shard by `(channel_id, timestamp bucket)`** | Distributes channels; latest-per-channel read efficient | Residual hotspot per popular channel; inactive channel may require hitting multiple time shards |
| Shard by `channel_id + random` | No timestamp hotspot | Scatter-gather on reads; worsens as shards grow |

- **Conclusion** — **`(channel_id, timestamp bucket)`**. Fall back to random sharding only if write throughput truly can't be handled — in practice, if any channel receives 10,000 QPS of writes, nobody can read it anyway
