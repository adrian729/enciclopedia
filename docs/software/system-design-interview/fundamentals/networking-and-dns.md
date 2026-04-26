# Networking & DNS

> Networking rarely gets deep trivia in interviews, but core concepts unlock geo-sharding, data-center failover, CDN routing, and WebSocket deep dives. Liu's chapter is the more thorough reference; Xu's coverage is mostly inside the scaling-evolution narrative (multi-DC, GeoDNS).

## Table of Contents

- [1. TCP and the Four-Tuple](#1-tcp-and-the-four-tuple)
- [2. DNS](#2-dns)
- [3. Anycast](#3-anycast)
- [4. The Private Backbone](#4-the-private-backbone)
- [5. The OSI Model in Practice](#5-the-osi-model-in-practice)
- [6. Multi-Data-Center Routing](#6-multi-data-center-routing)
- [Sources](#sources)

## 1. TCP and the Four-Tuple

A TCP connection is identified by a four-tuple: `(client IP, client port, server IP, server port)`. This matters in interviews most often for **WebSocket deep dives**: a WebSocket connection is bound to a specific physical server by this tuple, so it cannot be held at the app load balancer; the LB hands out endpoints of a WebSocket proxy farm where connections terminate (see [Real-Time Communication](fundamentals/real-time-communication.md)).

## 2. DNS

DNS converts domain to IP, with TTL caching at every level. **DNS round-robin** is a simple load-balancing mechanism — multiple A records for the same domain — with the caveat that stale client caches can keep hitting a downed IP after the operator rotates the entry. That's why hard failover usually pairs DNS with health-aware load balancing inside the DC.

## 3. Anycast

Multiple edges share one IP; each internet router forwards the packet toward the most optimal next hop based on routing-table cost. The user's request lands at the nearest edge without the client knowing. CDNs use anycast for static-asset routing, and global services use it for the same reason DNS round-robin gets used: simplicity at the cost of fine-grained control.

## 4. The Private Backbone

The network between a CDN edge and the origin data center is typically the company's own private backbone, far more efficient than the public internet. Cross-region transfer over the public internet should be assumed slow (~150 ms transcontinental) compared to the same hop over a private fiber backbone.

## 5. The OSI Model in Practice

Two layers matter for system design:

- **Layer 7 (Application)** — HTTP, DNS, gRPC, WebSocket. Most application-level protocols live here.
- **Layer 4 (Transport)** — TCP for reliable one-to-one (the default for almost everything); UDP for one-to-many broadcasting where packet loss is tolerable (video streaming, heartbeats, DNS queries).

The other layers are interview footnotes. A Layer 4 load balancer (TCP/UDP) is faster but can't read application content; a Layer 7 load balancer can route by URL path or HTTP header.

## 6. Multi-Data-Center Routing

**GeoDNS** routes users to the closest data center. On regional failure, DNS records redirect traffic to a healthy DC. Xu flags three challenges that come with multi-DC:

1. Traffic redirection on outages.
2. Cross-DC data synchronization (asynchronous multi-region replication is the common pattern, e.g., Netflix).
3. Consistent automated deployment across DCs.

For services where DNS-level redirection is too slow, anycast keeps the same public IP and routes packets via BGP convergence to a healthy region.

## Sources

- [Liu Ch 5.18: Networking](software/system-design-interview/books/system-design-interview-fundamentals/ch05_18_networking.md)
- [Xu Ch 1: Scale From Zero to Millions of Users](software/system-design-interview/books/system-design-interview-insiders-guide/ch01_scale_zero_to_millions.md) (multi-DC and GeoDNS sections)
