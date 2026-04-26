# Chat System

> Both books cover this. Xu's Ch 12 is the deeper architecture (WebSocket, stateful chat servers, multi-device sync, presence). Liu's Ch 6.08 emphasizes the storage choice (Cassandra for write-heavy workload) and concurrency (server-generated millisecond timestamps for ordering).

## Table of Contents

- [1. Requirements](#1-requirements)
- [2. Protocol Choice — WebSocket](#2-protocol-choice--websocket)
- [3. Stateful Chat Servers](#3-stateful-chat-servers)
- [4. Storage](#4-storage)
- [5. Message Ordering](#5-message-ordering)
- [6. Multi-Device Sync](#6-multi-device-sync)
- [7. Group Chat](#7-group-chat)
- [8. Online Presence](#8-online-presence)
- [9. Trade-offs](#9-trade-offs)
- [Sources](#sources)

## 1. Requirements

- One-to-one chat.
- Group chat (small to medium groups).
- Online/offline presence.
- Multi-device sync — same user logged in on phone and desktop.
- Message history with retention.
- Low latency for active users; durability for stored messages.

## 2. Protocol Choice — WebSocket

Both books pick WebSocket — bidirectional, persistent, works through firewalls on ports 80/443. See [Real-Time Communication](fundamentals/real-time-communication.md) for the protocol comparison.

The alternatives (polling, long polling, SSE) all have drawbacks for chat: polling wastes bandwidth, long polling can route sender and receiver to different servers without coordination, SSE is unidirectional.

## 3. Stateful Chat Servers

Each client holds a persistent WebSocket to *one specific* chat server (the four-tuple TCP binding — see [Networking & DNS](fundamentals/networking-and-dns.md)). The server is stateful: the connection lives there until the client disconnects.

Service discovery (Apache ZooKeeper) recommends the best chat server based on geography and capacity — see [Service Discovery & Load Balancing](fundamentals/service-discovery-and-load-balancing.md).

Trade-offs from statefulness:

- **Deploys** — graceful drain (close new connections, wait for existing ones).
- **Failover** — clients reconnect; thundering herd is bounded by fleet size.
- **Routing for delivery** — to send Alice's message to Bob, the system needs to know which chat server holds Bob's connection. A presence/routing layer (often the same gossip-based service-discovery system) tracks this.

## 4. Storage

Chat messages are an explicit write-heavy workload. Both books pick a wide-column / KV store:

- **Liu** picks Cassandra (write-optimized, no edits/deletes in the agreed scope, partitioned by user pair or chat room).
- **Xu** notes that Facebook Messenger uses HBase, Discord uses Cassandra. The reasoning is the same: horizontal scalability, low-latency writes, proven production use.

The schema is partitioned by `(chat_id, message_timestamp)` so messages for one chat are co-located.

## 5. Message Ordering

The receiver must see messages in some sensible order. The interesting question is *which clock*:

- **Client clock** — easy to skew; two clients with mismatched system time produce out-of-order messages.
- **Server clock** — single source of truth at the chat server.

Liu's pick: **server-generated millisecond timestamps**. Rare collisions when two messages get the same millisecond are acceptable because **concurrent messages have no semantic relationship to each other** — there's no "right" order between two simultaneous, unrelated sends.

[Snowflake IDs](fundamentals/id-generation.md) are an alternative — time-sortable across the cluster with explicit tie-breaking via the sequence bits.

## 6. Multi-Device Sync

A user logged in on phone and desktop wants the same view of every conversation. Pattern:

- Each device tracks `cur_max_message_id` for each conversation.
- On reconnect or open, fetch all messages with ID > `cur_max_message_id`.
- Update local state.

Vector clocks are an alternative for tracking divergence across devices, but `cur_max_message_id` is simpler and suffices for this use case.

## 7. Group Chat

Group chat fans out a message to each recipient's inbox at write time:

```
Send to group(N members)
   ↓
For each member: append message to their inbox queue
```

Cheap for groups capped at ~100. WeChat caps at 500, which is still manageable. For "channels" with 100,000+ members (Discord, Slack), the design changes — fanout becomes too expensive, and members fetch on read instead, which is a [News Feed](case-studies/news-feed.md)-style hybrid.

## 8. Online Presence

A heartbeat protocol — Xu's chat system uses 5-second heartbeats with a 30-second grace window — keeps the presence view fresh. Status changes are broadcast via **publish-subscribe** channels per friend pair: when Alice goes online, Bob and Carol (her friends) get notified.

Bounded fanout works for friend lists (a few hundred friends) but doesn't scale to 100,000-member groups, where status is fetched lazily on entry instead.

## 9. Trade-offs

- **Statelessness vs statefulness** — chat servers are intentionally stateful (WebSocket binding). The design embraces it; service discovery routes around it.
- **Server clock vs Snowflake** — server clock is simpler; Snowflake handles cross-cluster ordering more robustly. Either is acceptable.
- **Presence accuracy vs fanout cost** — 5-second heartbeat is a balance. Faster gives more accurate presence, more network cost.
- **Group fanout-on-write vs fanout-on-read** — write for small groups, read for huge channels. The threshold is the same kind of decision as the [News Feed](case-studies/news-feed.md) celebrity threshold.

## Sources

- [Xu Ch 12: Design a Chat System](software/system-design-interview/books/system-design-interview-insiders-guide/ch12_design_a_chat_system.md)
- [Liu Ch 6.08: Chat Application](software/system-design-interview/books/system-design-interview-fundamentals/ch06_08_chat_application.md)
