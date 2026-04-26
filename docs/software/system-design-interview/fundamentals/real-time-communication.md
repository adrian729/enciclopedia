# Real-Time Communication

> Liu's chapter (5.04) is the protocol comparison; Xu applies the same comparison inside the Chat System chapter (Ch 12). They agree: WebSocket is the bidirectional default, and the stateful nature of WebSocket connections requires a proxy farm in front, not a load balancer.

## Table of Contents

- [1. The Receive-Side Problem](#1-the-receive-side-problem)
- [2. Protocol Comparison](#2-protocol-comparison)
- [3. WebSocket Architecture](#3-websocket-architecture)
  - [3.1. Statefulness](#31-statefulness)
  - [3.2. Proxy Farm Pattern](#32-proxy-farm-pattern)
  - [3.3. Heartbeat and Disconnect Detection](#33-heartbeat-and-disconnect-detection)
  - [3.4. Thundering Herd on Server Failure](#34-thundering-herd-on-server-failure)
- [4. Choosing a Protocol](#4-choosing-a-protocol)
- [Sources](#sources)

## 1. The Receive-Side Problem

HTTP is client-initiated: the client asks, the server responds. To deliver a server-pushed message (a chat message, a notification, a real-time update) the system needs another mechanism.

## 2. Protocol Comparison

| Technique | Direction | How it works | Drawbacks |
|---|---|---|---|
| Short polling | Client → Server | Client periodically asks "anything new?" | Wasteful — most answers are "no". |
| Long polling | Client → Server (held) | Client opens a request; server holds it until a message arrives or a timeout | Sender and receiver may hit different servers; can't tell if client disconnected. |
| Server-Sent Events (SSE) | Server → Client | Persistent HTTP connection; server pushes events | Unidirectional only. |
| WebSocket | Bidirectional | Persistent TCP connection upgraded from HTTP, both sides push | Stateful — requires careful server-side connection management. |

Both authors converge on WebSocket as the default for chat, presence, and any low-latency two-way flow. SSE is the right choice for one-way streams (live scores, server logs).

## 3. WebSocket Architecture

### 3.1. Statefulness

A WebSocket connection is identified by the TCP four-tuple `(client IP, client port, server IP, server port)` — see [Networking & DNS](fundamentals/networking-and-dns.md). The connection is bound to a *specific physical server*. It cannot be load-balanced at the request level the way HTTP can.

This makes WebSocket servers explicitly stateful — Xu calls out the statefulness as a feature of the problem, not a design choice. The tradeoff is operational: connection draining, deploys, and failover all need handling.

### 3.2. Proxy Farm Pattern

The standard architecture: a load balancer hands the client an endpoint of a **WebSocket proxy farm**. The connection terminates at one specific proxy server. Service discovery (Apache ZooKeeper, Consul) tells the LB which proxies are alive, what their capacity is, and where to route the next client (often by geographic proximity).

### 3.3. Heartbeat and Disconnect Detection

TCP doesn't reliably notify when a peer goes silent. Heartbeat pings — Xu's chat system uses 5-second beats with a 30-second grace window — let each side detect dead connections and reconnect. Liu's variant: a `buffer_seconds` timeout fits the freshness SLO of the application.

### 3.4. Thundering Herd on Server Failure

When a WebSocket server dies, all its clients disconnect simultaneously and reconnect to the survivors — a thundering herd. Mitigations:

- **Right-size the proxy fleet** so a single failure's blast radius is bounded.
- **Stagger reconnects** with client-side jitter (random backoff between 0 and N seconds).
- **Provision spare capacity** on every proxy for absorbing reconnect spikes.

Server sizing is the trade-off lever between blast radius and operational cost.

## 4. Choosing a Protocol

| Use case | Recommended protocol |
|---|---|
| Real-time chat, multiplayer games | WebSocket |
| Notifications when sender doesn't expect a reply | SSE or WebSocket |
| Live updates with infrequent traffic (e.g., Google Drive sync) | Long polling — Xu's Ch 15 picks this for low-throughput unidirectional flows |
| Periodic UI refresh that doesn't need to be instant | Short polling or HTTP request on user action |
| One-shot status checks | Plain HTTP |

The Google Drive choice (long polling, not WebSocket) is a useful counter-point: the traffic is one-way, infrequent, and bursty in the wrong direction (server-pushed only) — Xu picks long polling explicitly because no bursts of data need to arrive at the same moment.

## Sources

- [Liu Ch 5.04: Real-Time Data Updates](software/system-design-interview/books/system-design-interview-fundamentals/ch05_04_realtime_data_updates.md)
- [Xu Ch 12: Design a Chat System](software/system-design-interview/books/system-design-interview-insiders-guide/ch12_design_a_chat_system.md) (protocol comparison and WebSocket choice)
- [Xu Ch 15: Design Google Drive](software/system-design-interview/books/system-design-interview-insiders-guide/ch15_design_google_drive.md) (long-polling rationale)
