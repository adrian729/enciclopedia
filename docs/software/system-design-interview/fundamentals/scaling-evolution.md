# Scaling Evolution

> Xu's first chapter walks an architecture from a single server to a system serving millions of users, adding one technique per step. Every primitive introduced here returns later as a building block in the case studies. Liu's book doesn't have an equivalent narrative — he treats each primitive in isolation — so this page is mostly Xu's tour, with Liu's emphasis added where helpful.

## Table of Contents

- [1. The Single Server](#1-the-single-server)
- [2. Separating Web Tier from Data Tier](#2-separating-web-tier-from-data-tier)
- [3. Vertical vs Horizontal Scaling](#3-vertical-vs-horizontal-scaling)
- [4. Load Balancer](#4-load-balancer)
- [5. Database Replication](#5-database-replication)
- [6. Cache](#6-cache)
- [7. CDN](#7-cdn)
- [8. Statelessness](#8-statelessness)
- [9. Multiple Data Centers](#9-multiple-data-centers)
- [10. Message Queues](#10-message-queues)
- [11. Logging, Metrics, Automation](#11-logging-metrics-automation)
- [12. Database Scaling](#12-database-scaling)
- [13. Closing Checklist](#13-closing-checklist)
- [Sources](#sources)

## 1. The Single Server

Web app, database, and cache all on one box. Once it's no longer enough, the first split is the data tier.

## 2. Separating Web Tier from Data Tier

Each tier scales independently. The data tier is a choice between a relational store (MySQL, PostgreSQL — mature, supports joins) and a NoSQL store (Cassandra, DynamoDB — better for super-low latency, unstructured data, simple serialize/deserialize workloads, or massive volume). See [Databases, Schema, Indexing](fundamentals/databases-schema-indexing.md) for category reasoning.

## 3. Vertical vs Horizontal Scaling

Vertical scaling (more CPU/RAM per box) is simple but capped by hardware and lacks failover. Horizontal scaling (more servers) is the route to large systems.

## 4. Load Balancer

Clients hit the load balancer's public IP; servers sit behind it on private IPs. When a server fails, traffic routes to the rest. New servers join the pool seamlessly. See [Service Discovery & Load Balancing](fundamentals/service-discovery-and-load-balancing.md).

## 5. Database Replication

Master takes writes, slaves serve reads. If a slave dies, traffic routes elsewhere; if the master dies, a slave is promoted, with recovery scripts handling whatever data the slave hadn't yet replicated. See [Replication](fundamentals/replication.md) for the full taxonomy (leader-follower, leader-leader, leaderless).

## 6. Cache

Temporary in-memory store that absorbs expensive or repeated reads. Xu's introductory pattern is **read-through**: web server checks cache first, queries DB on miss, populates the cache, returns to the client. He flags **Single Point of Failure (SPOF)** — a part that, if it fails, stops the entire system — as a risk to mitigate by replicating cache servers across data centers and overprovisioning memory. See [Caching](fundamentals/caching.md) for write strategies, invalidation, eviction, and thundering herd.

## 7. CDN

Static assets (images, video, CSS, JS) are pushed to geographically dispersed edges. The closer the edge, the faster the load. See [CDN](fundamentals/cdn.md).

## 8. Statelessness

The unlock for autoscaling: by externalizing per-user state into a shared store (RDBMS, NoSQL, Memcached, Redis), any web server can handle any request, and the load balancer no longer needs sticky sessions. Sticky sessions add overhead and make adding/removing servers and handling failures harder.

The exceptions are *intentionally* stateful: chat servers (WebSocket-bound clients) and presence servers. Xu calls out this statefulness as a feature of the problem, not a design choice.

## 9. Multiple Data Centers

Improves latency and survives regional outages. Users are routed to the closest DC via **GeoDNS**; on failure, traffic redirects to a healthy DC. Three challenges:

1. Traffic redirection.
2. Cross-DC data synchronization (Netflix uses asynchronous multi-region replication).
3. Consistent automated deployment across DCs.

## 10. Message Queues

Decouple producers and consumers via durable asynchronous buffering. The producer can post when the consumer is unavailable, and vice versa. Xu's example: web servers publish photo-processing jobs; dedicated photo workers drain the queue asynchronously so the user-facing request doesn't block. See [Queues & Messaging](fundamentals/queues-and-messaging.md).

## 11. Logging, Metrics, Automation

Three tiers of metrics:

- **Host** — CPU, memory, disk I/O.
- **Aggregated** — database tier, cache tier performance.
- **Business** — DAU, retention, revenue.

CI plus automated build/test/deploy keeps complex systems shippable. See [Observability, Security, Cold Storage](fundamentals/observability-security-cold-storage.md).

## 12. Database Scaling

Vertical scaling has hard ceilings (Xu's example: AWS RDS at 24 TB RAM). Horizontal scaling = **sharding**. Each shard shares the schema but holds unique data; a sharding key (e.g., `user_id % 4`) routes queries. Three issues:

1. **Resharding** — handled with consistent hashing.
2. **Hotspot keys** — the celebrity problem (Katy Perry, Justin Bieber, Lady Gaga ending up on the same shard).
3. **Cross-shard joins** — mitigated by de-normalization.

See [Sharding & Consistent Hashing](fundamentals/sharding-and-consistent-hashing.md).

## 13. Closing Checklist

Xu's distilled rules — every later chapter applies them:

- Keep the web tier stateless.
- Build redundancy at every tier.
- Cache aggressively.
- Support multiple data centers.
- Host static assets in a CDN.
- Shard the data tier.
- Split tiers into individual services.
- Monitor with automation.

## Sources

- [Xu Ch 1: Scale From Zero to Millions of Users](software/system-design-interview/books/system-design-interview-insiders-guide/ch01_scale_zero_to_millions.md)
- [Liu Ch 5.03–5.23](software/system-design-interview/books/system-design-interview-fundamentals/book_summary.md) (parallel coverage of individual primitives, treated topic-by-topic rather than as an evolution)
