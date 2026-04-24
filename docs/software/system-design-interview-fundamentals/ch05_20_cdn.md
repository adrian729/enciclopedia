# Ch 5.20: Content Delivery Network

## Table of Contents

- [1. What a CDN Is](#1-what-a-cdn-is)
- [2. Improve Latency](#2-improve-latency)
- [3. Reduce Bandwidth](#3-reduce-bandwidth)
- [4. Better Availability with Redundancy](#4-better-availability-with-redundancy)
- [5. CDN Considerations](#5-cdn-considerations)

## 1. What a CDN Is

- **Geographically distributed nodes delivering content efficiently** — caches static content such as images, videos, and static files
- **Read-through cache pattern** — a request for a static file is routed to the most optimal CDN via **anycast**; on a miss, the CDN fetches from the origin server and stores the file; on a hit, the CDN returns the file directly to the client

## 2. Improve Latency

- **Content sits closer to the user** — physical proximity reduces round-trip latency versus reaching the origin server

## 3. Reduce Bandwidth

- **CDN absorbs traffic that would otherwise hit main servers and routers** — significantly less data flows through the origin
- **Cost saving** — shorter distance to transfer bytes to the client lowers bandwidth costs on the origin path

## 4. Better Availability with Redundancy

- **Multi-region redundancy** — distribute CDN nodes across geographies with multiple replicas
- **Failover between CDNs** — if one CDN request fails, route to another

## 5. CDN Considerations

- **Don't trivialize CDNs in a deep dive** — "CDNs are closer to the user, so it's great" is not enough; raise challenges that relate to the question you're solving
- **Discussion points worth raising**:

| # | Question |
|---|----------|
| 1 | CDNs cost money — what static data is worth storing? |
| 2 | What happens on a CDN cache miss? How is the request routed? |
| 3 | With many CDN nodes, how is the network kept updated? |
| 4 | How do you prepopulate static content in a CDN? |
| 5 | If a CDN node fails, what should happen? |
| 6 | Does data differ between different regional CDNs? |
| 7 | CDNs are a cache — what cache considerations apply? |

- **Answers depend on the application** — e.g., Netflix predicts what a region may watch and warms up the regional CDN; how often to run warm-ups opens another layer of complexity worth discussing
- **Purpose in the interview** — raising essential discussion points demonstrates depth of knowledge on a topic most candidates treat superficially
