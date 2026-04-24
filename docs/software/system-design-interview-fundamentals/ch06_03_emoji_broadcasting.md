# Ch 6.03: Emoji Broadcasting

## Table of Contents

- [1. Requirements](#1-requirements)
- [2. API](#2-api)
- [3. High-Level Design](#3-high-level-design)
- [4. Schema](#4-schema)
- [5. End-to-End Flow](#5-end-to-end-flow)
- [6. Deep Dives](#6-deep-dives)

## 1. Requirements

- **Prompt** — design emoji broadcasting for Facebook Live. When a watcher taps an emoji, fan it out to all watchers of the stream
- **Scope narrowed to**:
  - Emoji briefly appears on each watcher's viewport then disappears (collective emotional experience)
  - **Predefined emoji set**
  - Anyone can watch; all users treated the same
  - **No offline replays**
  - No coordination between the emoji press and a specific stream frame (users are at different stream positions anyway) — send as fast as possible
- **Assumptions** agreed with interviewer:
  - **100M DAU** worldwide
  - Must support **celebrity streams with tens of millions of concurrent watchers**
  - Freshness is critical — out-of-context emoji is a bad UX
  - Durability unimportant; occasional loss acceptable, but aim to deliver as many as possible

## 2. API

```
watch_stream(user_id, stream_id) → websocket_address
send_emoji(user_id, stream_id, emoji_id) → status
display_emoji(emojis)   // client-side callback
```

- `watch_stream` returns a WebSocket address the client then connects to
- `send_emoji` `SUCCESS` = server received and is fanning out (not delivered to all watchers)
- `display_emoji` is invoked on the watcher's client to render on the viewport

## 3. High-Level Design

- **WebSocket servers** maintain stateful connections to watchers and stream video to them (unidirectional server→client for this design)
- **Stream service** accepts `send_emoji` and pushes to an **emoji queue** (async; high write throughput expected)
- **Fan-out service** consumes the queue, reads from **connection storage** to find which WebSocket servers host watchers of the stream, and forwards the emoji
- **Connection storage** maps `stream_id` → list of `websocket_server_id`, updated when watchers join/leave

## 4. Schema

**Emoji queue** — `user_id` omitted (we don't display who sent it)

| Stream Id | Emoji Id |
|---|---|

**Connection storage**

```
stream_id → [websocket_server_id]
```

**WebSocket server (in-memory)** — lifecycle tied to the stateful TCP connection on the physical machine

```
stream_id → [connection]   // connection = IP + port
```

## 5. End-to-End Flow

- **`watch_stream`**: client → WebSocket server adds connection to `stream_id → [connection]`; if this is the first connection for that `stream_id` on this server, WebSocket server updates connection storage to include its `websocket_server_id` for the stream. On disconnect, remove from local list; if the list becomes empty, remove `websocket_server_id` from connection storage for that stream
- **`send_emoji`**: client → stream service → emoji queue → fan-out service → reads connection storage for `[websocket_server_id]` → forwards to each target server → each server iterates local `[connection]` for the `stream_id` and pushes to watchers

## 6. Deep Dives

### 6.1 Fan-out Factor (Thundering Herd)

- **Scenario** — tens of millions of concurrent watchers; if all tap at once (e.g., Michael Jordan buzzer-beater), potential **10M QPS** briefly, and 10M emojis × 10M watchers is unusable even if delivered (device freeze, screen cover-up)

| Option | Upside | Downside |
|---|---|---|
| **Just let it fan out** (scale stream service + queue by sharding; fan-out micro-batches) | None beyond simplicity | Backlog delay; device overwhelm; 10M emojis on screen useless |
| **Client-side sampling** — probability of going through scales with concurrent watcher count (e.g., 0.01% at 10M; 99.9% at 10 watchers) | Cuts emoji QPS massively; predictable traffic per stream; accuracy matters less at scale due to overlap | Not every tap is sent |
| **Fan-out service sampling** — micro-batch every second to aggregated `(stream_id, emoji_id) → count`; UI renders an **"emoji confetti"** when count is high (e.g., count≥20 shows confetti, regardless of whether actual count is 20 or 1,000) | Reduces WebSocket fan-out; better UX under load | Requires UI collaboration |

- **Conclusion** — **combine options 2 and 3**. Option 2 reduces stream-service/queue throughput; option 3 reduces WebSocket fan-out and improves UX

### 6.2 Connection Storage: Keep It or Broadcast to All?

- **Math**: 30% of 100M DAU concurrent = 30M WebSocket connections. At 250k connections/server → **120 WebSocket servers**. Without connection storage, every emoji fans out to all servers even if only 1 hosts a watcher

| Option | Upside | Downside |
|---|---|---|
| **Always fan-out to all WebSocket servers** | No connection storage to maintain | Huge waste on long-tail streams (1 watcher → 120 servers per emoji) |
| **Use connection storage** | Fan-out only to servers actually hosting watchers (often 1–3 vs. 120) | Write QPS as connections open/close; slight read overhead per fan-out |

- **Conclusion** — **use connection storage**; the long-tail distribution makes the saving dominate the maintenance cost

### 6.3 Globally Distributed User Base

- **Scenario** — 3 regions. Each region already has a regional connection storage; question is how regions coordinate on which other regions watch a given stream

| Option | Upside | Downside |
|---|---|---|
| **Forward each emoji to all 3 regions** | Simple; no global connection store | Wasted forwarding when a region has no watchers of that stream |
| **Global region connection store** (`stream_id → [region_id]`, replicated across regions) | Forward only to regions with watchers | Cross-region update broadcast complexity; expensive and unreliable |

- **Conclusion** — **option 1** for regions, opposite of the intra-region decision. Fan-out factor is 3 (not 120), and probability that a region hosts a watcher is far higher than for a single server (a region contains many servers). Global coordination complexity outweighs the savings

### 6.4 Connection Store Read Path (Data Store Choice)

- **Math**: at 10M emoji peak, batch 1,000 → 100,000 chunks; batch keys per chunk → **10k QPS** read on the connection store

| Option | Upside | Downside |
|---|---|---|
| **Durable key-value store** (list of `websocket_server_ids` per key) | Durable; survives store failure without rebuilding from 120+ servers | 10k QPS on disk is hard; likely needs sharding; 5ms disk read |
| **Cache with periodic backup** | Handles 10k QPS; efficient key-value blob reads; stale backup on failure is tolerable | Rebuild complexity; invalidation on writes; inconsistency on stale backup (emojis lost or sent to disconnected users) |
| **Durable store + read-through cache** | DB as source of truth; cache absorbs reads | Invalidation complexity; occasional cache misses with unpredictable latency |

- **Conclusion** — **option 2**. Connections are already inconsistent due to disconnects, so the cache's stale-backup tradeoff is acceptable. Can incrementally upgrade to option 3 later if inconsistency cost is too high

### 6.5 WebSocket Load Balancing

- Even worst case: an emoji may need to fan out to every WebSocket server for a stream if each hosts at least one watcher

| Option | Upside | Downside |
|---|---|---|
| **Assign by `stream_id`** (stream pinned to a WebSocket server) | Fan-out to 1 server in the simple case | Stateful → harder to scale; hot streams need **micro-sharding** (fan-out to all micro-shards of the stream) |
| **Round robin** (new connection → next available server) | Stateless; scales by adding servers | Fan-out must target all servers hosting the stream (via connection store) |

- **Conclusion** — **round robin**. For popular videos micro-shards force fan-out anyway, so stateful pinning adds no value. For smaller scales where no stream needs multiple servers, option 1 is preferable and removes connection-store complexity

### 6.6 Stream Replay

- Replay requires mapping each emoji to a point in the stream's timeline

| Option | Upside | Downside |
|---|---|---|
| **Client clock, per-emoji relative timestamp** | Stored at the exact frame the user clicked on | Still need sampling to avoid flooding replay; malicious client timestamps |
| **Stream-service clock on receive** | Prevents malicious timestamps | Same flooding issues; less aligned to user's intended frame |
| **Fan-out service clock** — persist `(stream_id, time_slice) → [emoji_id]` (already computed post-sampling) | Reuses existing infrastructure; no extra capture pipeline | Fan-out service must coordinate with streaming service for best-effort relative timestamp; may drift from user's intention |

- **Conclusion** — **option 3**. Reuses the fan-out work already done; interviewer notes this is close to the production design
