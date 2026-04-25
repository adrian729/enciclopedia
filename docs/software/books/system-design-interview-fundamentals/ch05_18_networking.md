# Ch 5.18: Networking

## Table of Contents

- [1. Why Networking Matters in the Interview](#1-why-networking-matters-in-the-interview)
- [2. IP and Port](#2-ip-and-port)
- [3. Domain Name System (DNS)](#3-domain-name-system-dns)
- [4. How to Route to the Closest Region](#4-how-to-route-to-the-closest-region)
- [5. OSI Model](#5-osi-model)

## 1. Why Networking Matters in the Interview

- **Scope is generalist, not specialist** — unless interviewing for a networking role, trivia is not asked; core concepts are needed to give the right level of detail on scalability
- **Where networking shows up** — geo-sharding, data-center failover, CDN routing, "describe how the internet works" prompts, and WebSocket deep dives
- **Hand-wavy answers are visible** — saying "the client routes to the closest CDN" or "when the data center is down, requests go elsewhere" is acceptable only if you can unpack the routing mechanism when pressed

## 2. IP and Port

- **IP = home address of a device on the internet** — a server has an IP; a device can expose many ports as entry points; a request specifies both IP and port to reach a listener
- **TCP connection = 4-tuple** — `client_ip, client_port, server_ip, server_port`
- **Path of a browser request** — client → ISP → series of routers ("the internet") → server IP; responses traverse the internet back to the client
- **Default ports hide from the user** — HTTPS defaults to 443, HTTP defaults to 8080, so typing `https://www.google.com` requires no explicit port

> **Reminder** — When you enter `https://www.google.com`, the browser asks DNS servers which IP the domain belongs to. Because the protocol is HTTPS, the server uses default port 443, so the user doesn't have to specify it. HTTP's default port is 8080.

- **Where IP/port/router knowledge unlocks deep dives**:
  - **Geo-sharding** — multiple data centers accept the same request; you must explain how it reaches the right one
  - **Data center failover** — when the primary is down, requests must stop hitting the failed IP and go to a healthy region
  - **CDN** — same problem: route to the closest CDN node for a given CDN domain
  - **Describing how the internet works** — interviewer probes for basic literacy
  - **WebSocket** — how client/server communicate over a persistent connection and what happens when the connection drops

## 3. Domain Name System (DNS)

- **DNS converts domain to IP** — `google.com` is human-readable, but routing needs an IP; the browser asks a DNS server and caches the result with a TTL
- **Rarely the main topic** — not unique to any one question, but useful for "what happens when you enter www.google.com" or "the website is down, debug it"
- **DNS round robin** — load balance by returning multiple IPs for a service to improve redundancy and availability
- **DNS round-robin caveat** — browsers cache DNS responses; the server has no direct control over client-side cache, so a downed IP can still be hit from a stale cache. Still worth mentioning as a fault-tolerance option

## 4. How to Route to the Closest Region

- **Goal** — improve availability and performance via geo-distributed edges and servers; applies to edge servers, CDNs, and data centers
- **Two routing questions to answer**:
  1. How a request routes to the nearest data center
  2. What happens when a region is down — how does the system reroute to a healthy data center or edge

### 4.1. Option 1: DNS Routing

- **Mechanism** — the DNS server inspects the client's IP and returns the closest server IP; if a server IP is down, DNS can be configured to return another IP even if farther away
- **Advantages** — performance (closest IP) and availability (failover to another IP)
- **Disadvantages** — complex DNS logic to choose the optimal IP; clients cache domain→IP mappings with a TTL, so a downed IP can keep getting hit from the browser cache, and the server has no control over that cache

### 4.2. Option 2: Edge Router (Anycast)

- **Mechanism** — servers keep static IPs, but multiple edge routers share a single **anycast** IP; multiple edges are assigned the same IP
- **How the right edge is chosen** — as a request traverses internet routers, each router forwards toward the most optimal next hop for that IP (like a shortest-path graph where each node knows its best outgoing edge)
- **Edge → data center step** — once the request reaches the edge router, it forwards to the most optimal data center; the edge router continuously monitors data-center health, preferring closer and healthier targets
- **Private backbone advantage** — the network between edge servers and data centers is usually company-owned, so it is far more efficient than the public internet

## 5. OSI Model

- **Interview focus** — not packet trivia; know which commonly-mentioned terms belong in which layer. For generalist interviews, **Layer 7** and **Layer 4** are the most important
- **Avoid confusing layers** — TCP and HTTP are not the same thing; they solve different problems at different layers

### 5.1. Layer 7: Application

| Protocol | Role in the interview |
|---|---|
| **HTTP** | Know common verbs and status codes and when to use them; don't over-index unless asked |
| **DNS** | Domain-to-IP resolution (see section 3) |
| **SMTP, FTP, SSH, SOAP** | Occasionally relevant; not deeply expected unless you have prior expertise |

### 5.2. Layer 4: Transport Layer

- **Role** — node-to-node communication and control flow
- **Two protocols that matter** — TCP and UDP

| Protocol | Guarantees | Connection model | Typical use |
|---|---|---|---|
| **UDP (User Datagram Protocol)** | No acknowledgment, no ordering | One-to-many capable (broadcasting) | Video streaming, voice/video chat, heartbeats, broadcasting |
| **TCP (Transmission Control Protocol)** | Acknowledgment per request, ordered packets via sequence numbers from the handshake | One-to-one only | Most web applications needing reliable data transfer |

- **UDP trade-off** — more performant by skipping TCP's overhead, at the cost of packet loss and ordering issues; choose it when the application tolerates those downsides
- **TCP default** — most connections in a system design interview are TCP unless the use case can absorb UDP's cons
