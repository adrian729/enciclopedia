# Ch 12: Design a Chat System

## Table of Contents

- [1. Requirements and Scope](#1-requirements-and-scope)
- [2. Client-Server Communication Protocols](#2-client-server-communication-protocols)
- [3. High-Level Architecture](#3-high-level-architecture)
- [4. Storage Choices](#4-storage-choices)
- [5. Data Models and Message ID](#5-data-models-and-message-id)
- [6. Service Discovery](#6-service-discovery)
- [7. 1-on-1 Message Flow](#7-1-on-1-message-flow)
- [8. Multi-Device Synchronization](#8-multi-device-synchronization)
- [9. Group Chat Flow](#9-group-chat-flow)
- [10. Online Presence](#10-online-presence)
- [11. Wrap-Up Topics](#11-wrap-up-topics)

## 1. Requirements and Scope

- **Target app** — Facebook-Messenger-style chat with 1-on-1 chat, small group chat (max 100 members), online presence, multi-device support, push notifications
- **Scale** — 50 million DAU; text-only messages up to 100,000 characters; chat history stored forever
- **Why scoping matters** — chat apps split into very different categories (1-on-1 like WhatsApp, group-focused like Slack, low-latency voice like Discord); the design changes drastically per category, so clarify before designing

## 2. Client-Server Communication Protocols

- **Sender side uses HTTP** — clients open an HTTP connection (with `keep-alive` to reduce TCP handshakes) and post messages to the chat service; this is what Facebook used originally
- **Receiver side is harder** — HTTP is client-initiated, so the server cannot push. Three techniques simulate server-initiated delivery:

| Technique | How it works | Drawbacks |
|---|---|---|
| **Polling** | Client periodically asks server if messages exist | Costly; most answers are "no"; wastes server resources |
| **Long polling** | Client holds connection open until messages arrive or timeout, then reconnects | Sender/receiver may hit different stateless servers; server can't tell if client disconnected; still inefficient for low-traffic users |
| **WebSocket** | Client-initiated, bidirectional, persistent connection upgraded from HTTP; uses ports 80/443 so works through firewalls | Persistent connections require careful server-side connection management |

- **Choice** — WebSocket on both sides (sender and receiver) since it is bidirectional, simplifies the design, and works through firewalls

## 3. High-Level Architecture

- **Three categories of components** — stateless services, stateful services, third-party integration
- **Stateless services** — login, signup, user profile, etc. Sit behind a load balancer; can be monolith or microservices. Service discovery is the one stateless service worth deep-diving
- **Stateful service** — the chat service is stateful because each client holds a persistent WebSocket connection to a specific chat server and normally does not switch as long as that server is alive
- **Third-party integration** — push notifications are critical; they alert users of new messages even when the app is not running (see Ch 10)
- **Why not a single server** — at 1M concurrent users with ~10K memory per connection (~10GB), it physically fits on one box, but a single server is a SPOF and a deal-breaker; fine to start with one but explicitly call it a starting point
- **Final components** — chat servers (real-time messaging), presence servers (online/offline), API servers (login/signup/profile), notification servers (push), key-value store (chat history)

## 4. Storage Choices

- **Two data types** — generic data (user profile, settings, friends list) goes in a relational DB with replication and sharding; chat history goes in a key-value store
- **Chat history read/write pattern**
  - Enormous volume — Facebook Messenger and WhatsApp process 60 billion messages/day
  - Only recent chats are read frequently
  - Random access still needed (search, mentions, jump to specific message)
  - 1:1 read/write ratio for 1-on-1 chat
- **Why key-value stores** — easy horizontal scaling, very low latency, handle the long tail of data better than relational indexes, and proven in production (Facebook Messenger uses HBase, Discord uses Cassandra)

## 5. Data Models and Message ID

- **Message table for 1-on-1** — primary key is `message_id`, which decides ordering (cannot use `created_at` since two messages can share a timestamp)
- **Message table for group chat** — composite primary key `(channel_id, message_id)`; `channel_id` is the partition key because all queries operate within a channel
- **Message ID requirements** — must be unique and sortable by time (newer rows have higher IDs)
- **Generation options**
  - MySQL `auto_increment` — works in SQL but not in NoSQL
  - Global 64-bit generator like Snowflake (Ch 7)
  - Local sequence number — unique only within a group/channel, which is sufficient since ordering only matters within a channel; easier to implement than global IDs

## 6. Service Discovery

- **Role** — recommend the best chat server for a client based on geography, server capacity, etc.; Apache Zookeeper is the typical implementation
- **Login flow** — user logs in → load balancer hits API servers → after auth, service discovery picks the best chat server (e.g., server 2) and returns its info → client opens a WebSocket to that chat server

## 7. 1-on-1 Message Flow

- **Steps** — User A sends to chat server 1 → chat server 1 fetches a message ID from the ID generator → puts message in the message sync queue → message is persisted to the key-value store
- **Delivery** — if User B is online, message is forwarded to chat server 2 (where B is connected) and then to B over WebSocket; if B is offline, a push notification is sent from PN servers

## 8. Multi-Device Synchronization

- **Problem** — same account logged in on multiple devices (phone + laptop), each with its own WebSocket connection to a chat server
- **Solution: `cur_max_message_id`** — each device tracks the latest message ID it has seen
- **New-message rule** — a message is new for a device if recipient ID matches the logged-in user AND the message ID in the KV store is greater than `cur_max_message_id`
- **Result** — every device independently fetches what it has missed from the KV store

## 9. Group Chat Flow

- **Copy to per-recipient inboxes** — sender's message is copied into each group member's message sync queue (think of it as an inbox per recipient)
- **Why this works for small groups** — each client only checks its own inbox, simplifying sync; copying per recipient is cheap when groups are small. WeChat uses this approach with a 500-member cap
- **Why it does not scale** — for large groups, one copy per member is too expensive
- **Recipient side** — each user's inbox holds messages from many different senders, all in one place

## 10. Online Presence

- **Login** — after WebSocket is established, presence server saves user status and `last_active_at` in the KV store; the green dot appears
- **Logout** — explicit logout flips the status to offline in the KV store
- **Disconnection problem** — naively flipping to offline on every disconnect causes bad UX (e.g., status flickering when going through a tunnel)
- **Heartbeat mechanism** — client sends a heartbeat every few seconds; if no heartbeat arrives within x seconds (e.g., 30s), user is marked offline. Example: 5s heartbeats, 30s grace
- **Online status fanout** — uses publish-subscribe; each friend pair has a channel (A-B, A-C, A-D); A publishes status changes to all its channels and subscribed friends receive them via WebSocket
- **Large-group limit** — fanout doesn't scale to 100,000-member groups (each change creates 100,000 events). Mitigation: fetch online status only when entering a group or manually refreshing

## 11. Wrap-Up Topics

- **Media files** — supporting photos/videos requires compression, cloud storage, and thumbnails since media is much larger than text
- **End-to-end encryption** — only sender and recipient can read messages; WhatsApp implements this
- **Client-side message caching** — reduces data transfer between client and server
- **Geo-distributed cache** — Slack built an edge cache (Flannel) to speed up channel/user data load times
- **Error handling**
  - **Chat server failure** — Zookeeper assigns clients a new chat server to reconnect to
  - **Message resend** — retries and queueing handle transient delivery failures
