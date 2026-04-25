# Ch 5.04: Real-Time Data Updates

## Table of Contents

- [1. Use Case](#1-use-case)
- [2. Protocol Comparison](#2-protocol-comparison)
- [3. How to Pick a Protocol](#3-how-to-pick-a-protocol)
- [4. How to Scale WebSockets](#4-how-to-scale-websockets)
- [5. WebSocket Load Balancer](#5-websocket-load-balancer)
- [6. Is the Connection Still Alive?](#6-is-the-connection-still-alive)

## 1. Use Case

- **Why it matters** — many system-design questions push updated data from server to client while the user is online: chat messages arriving, notifications firing, stock-price graphs updating, dashboards refreshing
- **Deep-dive surface** — protocol choice and the mechanics of long-lived connections create multiple opportunities for trade-off discussions

## 2. Protocol Comparison

| Protocol | Connection shape | Best for | Downside |
|---|---|---|---|
| **Short Poll** | Client re-requests periodically | Prototypes; no server-side connection state | Many wasted requests; overloads the server |
| **Long Poll** | Client sends request; server holds open until data or timeout | Server notifies when data ready | Connection-aware complexity |
| **Server-Sent Event (SSE)** | Server holds connection; one-way server→client | Stock price feed, other unidirectional pushes | Client can't push back over the same channel |
| **WebSocket** | Bidirectional TCP connection; stateful | Chat, multiplayer, anything needing two-way push | Stateful connection tied to a machine; reconnect on crash |

## 3. How to Pick a Protocol

- **Skip polling** — short and long polling rarely justify themselves in a scalable system; use them only for quick prototypes
- **WebSocket vs SSE** — WebSocket is bidirectional; SSE only flows server→client. SSE is simpler (uses plain HTTP, no WebSocket server infrastructure). Pick SSE for purely unidirectional events; WebSocket otherwise. Choosing WebSocket for unidirectional is also fine
- **WebSocket is the default for deep dives** — it's the most common real-time protocol, so most scalability discussions focus on it

## 4. How to Scale WebSockets

- **Stateful = different from app-server load balancing** — a WebSocket connection is tied to a specific physical server with an IP and port
- **Don't attach the connection to the app load balancer** — a single load balancer will run out of memory holding millions of connections, and load balancers aren't built to hold long-lived connections
- **Right answer** — a load balancer hands out the endpoint of a **WebSocket proxy farm**; connections terminate at individual WebSocket servers

## 5. WebSocket Load Balancer

- **Per-server connection state** — each WebSocket server tracks its open connections as `(from_ip, from_port, to_ip, to_port)` tuples. The tuple tells the server where to send events
- **Sessions, not users** — a user with multiple devices/tabs has multiple connections; treat each as a session
- **Failure behavior** — if a WebSocket server dies, all its clients reconnect, which can cause a **thundering herd** on the remaining servers
- **Trade-off in server sizing** — more connections per server = bigger thundering herd on failure; fewer connections per server = more servers to operate
- **Broadcast needs a lookup** — to notify a group (e.g., all users in New York), maintain a mapping `user_attribute → [WebSocket servers holding a matching connection]`

## 6. Is the Connection Still Alive?

- **Problem** — clients don't always close gracefully; network interruptions may hide whether the client is still there. A dead connection wastes memory and sends data to nobody
- **Heartbeat/ping** — client sends periodic pings; server stamps the last-ping timestamp. If no ping in `buffer_seconds`, the server considers the connection dead
- **Trade-offs**:
  - Higher ping frequency → better status accuracy, higher server load
  - Larger `buffer_seconds` → less flapping between online/offline, but stale "online" status when a client actually disconnected
- **Application-specific use** — Facebook Chat's online status likely derives from the open connection; notification services must handle unexpected client disconnects as a core case
