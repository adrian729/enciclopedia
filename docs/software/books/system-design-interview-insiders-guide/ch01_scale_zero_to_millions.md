# Ch 1: Scale From Zero to Millions of Users

## Table of Contents

- [1. Single Server Setup](#1-single-server-setup)
- [2. Database Tier](#2-database-tier)
- [3. Vertical vs Horizontal Scaling](#3-vertical-vs-horizontal-scaling)
- [4. Load Balancer](#4-load-balancer)
- [5. Database Replication](#5-database-replication)
- [6. Cache](#6-cache)
- [7. Content Delivery Network (CDN)](#7-content-delivery-network-cdn)
- [8. Stateless Web Tier](#8-stateless-web-tier)
- [9. Multiple Data Centers](#9-multiple-data-centers)
- [10. Message Queue](#10-message-queue)
- [11. Logging, Metrics, Automation](#11-logging-metrics-automation)
- [12. Database Scaling: Sharding](#12-database-scaling-sharding)
- [13. Scaling Checklist](#13-scaling-checklist)

## 1. Single Server Setup

- **Starting point** — web app, database, and cache all run on a single server; everything is co-located before traffic justifies separation
- **Request flow** — user resolves the domain (e.g., `api.mysite.com`) via DNS — usually a paid 3rd-party service — gets back an IP, sends an HTTP request to the web server, and receives an HTML page or JSON response
- **Traffic sources** — web app (server-side languages for logic, HTML/JS for presentation) and mobile app (HTTP + JSON API responses)

## 2. Database Tier

- **Why separate** — once a single server isn't enough, splitting web tier and data tier lets each scale independently
- **Relational (RDBMS / SQL)** — MySQL, Oracle, PostgreSQL; tables and rows; supports joins; the default for most apps because of 40+ years of maturity
- **Non-Relational (NoSQL)** — CouchDB, Neo4j, Cassandra, HBase, DynamoDB; four families: key-value, graph, column, document; joins generally not supported
- **When NoSQL fits** — super-low latency requirements, unstructured or non-relational data, simple serialize/deserialize workloads (JSON/XML/YAML), or massive data volumes

## 3. Vertical vs Horizontal Scaling

| | Vertical (scale up) | Horizontal (scale out) |
|---|---|---|
| Method | Add CPU/RAM to one server | Add more servers to the pool |
| Best for | Low traffic, simplicity | Large-scale apps |
| Hard limit | Yes — finite hardware ceiling | No |
| Failover | None — one server, one point of failure | Built-in via redundancy |

- **Why horizontal wins at scale** — vertical scaling has a hardware ceiling and no redundancy; if the single server dies, the site dies with it

## 4. Load Balancer

- **Function** — evenly distributes incoming traffic across web servers in a load-balanced set
- **Public vs private IPs** — clients hit the load balancer's public IP; web servers sit behind it on private IPs (only reachable inside the network) for security
- **Failover** — if a server goes offline, traffic routes to the rest; a healthy server is added to rebalance load
- **Elasticity** — when traffic grows, just add more servers to the pool; the load balancer picks them up automatically

## 5. Database Replication

- **Master/slave model** — master handles writes; slaves hold copies and serve reads. Most apps are read-heavy, so slaves typically outnumber masters
- **Benefits** — better performance (parallel reads across slaves), reliability (data survives a regional disaster), high availability (other replicas serve traffic if one fails)
- **Slave failure** — reads are redirected to a healthy slave; if no slaves remain, reads temporarily go to the master. A replacement slave is provisioned to take over
- **Master failure** — a slave is promoted to be the new master and writes resume there. In production this is non-trivial: the promoted slave's data may not be fully up to date, so recovery scripts run to fill the gap. Multi-master and circular replication exist as alternatives but are more complex (out of scope)

## 6. Cache

- **Purpose** — temporary in-memory store for expensive or frequent data; subsequent requests skip the database
- **Cache tier** — a separate layer between web tier and database; faster than the DB, scales independently, reduces DB load
- **Read-through cache** — web server checks the cache first; on a hit, returns immediately. On a miss, queries the DB, populates the cache, then returns to the client
- **When to use** — data that is read frequently but modified infrequently. The cache is never the source of truth: memory is volatile and a cache restart wipes everything, so important data must be persisted in the DB
- **Expiration policy** — too short reloads from DB too often; too long serves stale data
- **Consistency** — cache and DB updates aren't atomic; cross-region scaling makes this harder. See "Scaling Memcache at Facebook"

> **Single Point of Failure (SPOF)** — a part of a system that, if it fails, stops the entire system. A single cache server is a SPOF; mitigate with multiple cache servers across data centers and overprovisioned memory

- **Eviction policy** — once full, items are evicted to make room. **LRU** (Least Recently Used) is most common; **LFU** (Least Frequently Used) and **FIFO** also used

## 7. Content Delivery Network (CDN)

- **Definition** — a network of geographically dispersed servers caching static content (images, video, CSS, JS)
- **How it works** — user request goes to the nearest CDN edge; on miss, edge fetches from origin (web server or S3), caches with a TTL header, serves to subsequent users until TTL expires
- **Latency principle** — closer edge = faster load. Users in LA hit a SF edge faster than users in Europe would
- **Considerations**
  - **Cost** — pay for data transfer; don't CDN-cache infrequently used assets
  - **TTL tuning** — too long = stale, too short = repeated origin fetches
  - **Fallback** — clients should detect CDN outage and fetch from origin
  - **Invalidation** — use CDN-vendor APIs, or version the URL (e.g., `image.png?v=2`)

## 8. Stateless Web Tier

- **Stateful server** — remembers a client's session/profile data locally across requests, so every request from that client must come back to the same server. The load balancer enforces this with **sticky sessions**, which adds overhead and makes adding/removing servers and handling failures harder
- **Stateless server** — keeps no per-client state; session data lives in a shared persistent store (RDBMS, NoSQL, Memcached/Redis), so any web server can serve any request
- **Why stateless wins** — simpler, more robust, easier to scale; the book picks NoSQL as the shared store because it's easy to scale
- **Autoscaling** — automatically adds/removes web servers based on traffic load. Only feasible once state has been externalized out of the web tier

## 9. Multiple Data Centers

- **GeoDNS routing** — a DNS service that resolves a domain to different IPs based on the user's location. Users are routed to the closest data center, splitting traffic (e.g., x% US-East, 100−x% US-West)
- **Outage handling** — if one data center goes offline, all traffic is redirected to a healthy one (e.g., 100% to US-East when US-West is down)
- **Challenges**
  - **Traffic redirection** — GeoDNS or similar tools to route to the right DC
  - **Data synchronization** — replicate across DCs so failover traffic can find its data; Netflix uses asynchronous multi-region replication
  - **Test and deployment** — automated, location-aware deployment tools to keep DCs consistent

## 10. Message Queue

- **Definition** — a durable, in-memory component that supports asynchronous communication. It buffers requests between services that produce and consume them
- **Producers/publishers** post messages onto the queue; **consumers/subscribers** connect to the queue and perform the work the messages describe
- **Decoupling benefit** — the producer can keep posting when the consumer is unavailable; the consumer can keep draining the queue when the producer is unavailable. This is what makes the queue a building block for scalable, failure-resilient systems
- **Independent scaling** — producer and consumer scale separately; when the queue grows, add more workers, when it's idle, reduce them
- **Example** — photo customization (cropping, sharpening, blurring) takes time. Web servers publish photo-processing jobs to the queue; dedicated photo workers consume them asynchronously, so the user-facing request doesn't block

## 11. Logging, Metrics, Automation

- **Logging** — monitor error logs per server, or aggregate to a centralized service for searchable diagnostics
- **Metrics** — three useful tiers
  - **Host-level** — CPU, memory, disk I/O
  - **Aggregated** — performance of the database tier, cache tier, etc.
  - **Business** — daily active users, retention, revenue
- **Automation** — CI verifies every check-in to detect problems early; automate build, test, and deploy to compound developer productivity

## 12. Database Scaling: Sharding

- **Vertical DB scaling** — bigger box (RDS offers up to 24 TB RAM); Stack Overflow ran on a single master in 2013 with 10M+ monthly visitors. Hits hardware limits, SPOF risk, and high cost
- **Horizontal DB scaling (sharding)** — split a large DB into smaller shards; each shard shares the schema but holds unique data
- **Sharding key (partition key)** — one or more columns that determine routing. Example: `user_id % 4` selects shard 0–3
- **Choosing a key** — must distribute data evenly to avoid hot shards
- **Resharding** — required when a shard runs out of space (rapid growth) or when uneven data distribution causes one shard to exhaust faster than others. Resharding means updating the sharding function and moving data around; **consistent hashing** (Ch 5) is a commonly used technique to solve this problem
- **Celebrity / hotspot key problem** — excessive access to one shard (Katy Perry, Justin Bieber, Lady Gaga on the same shard) overloads it; mitigation may require a dedicated shard per celebrity, possibly further partitioned
- **Join and de-normalization** — cross-shard joins are hard; de-normalize so queries hit a single table
- **NoSQL offload** — move some non-relational features to a NoSQL store to reduce RDBMS load

## 13. Scaling Checklist

The chapter closes with a recap of techniques to reach millions of users. Each bullet ties back to a section above:

- **Keep web tier stateless** — store session and user state in a shared persistent store, so any web server can handle any request and autoscaling becomes trivial (§8)
- **Build redundancy at every tier** — eliminate single points of failure: multiple web servers behind a load balancer, replicated databases, multiple cache servers, multiple data centers (§4–5, §6, §9)
- **Cache data as much as you can** — keep frequent or expensive results in a fast in-memory layer to reduce database load and latency (§6)
- **Support multiple data centers** — geo-route users to the closest data center for lower latency, and survive a regional outage by failing traffic over to a healthy one (§9)
- **Host static assets in CDN** — push images, video, CSS, JS to edge servers near the user; web servers serve only dynamic content (§7)
- **Scale your data tier by sharding** — split the database horizontally across shards keyed by a partition key, since vertical scaling has a hardware ceiling (§12)
- **Split tiers into individual services** — decouple components (web, cache, DB, CDN, queue, photo workers) so each can be scaled or redeployed independently (§10)
- **Monitor your system and use automation tools** — logging, metrics at host/aggregated/business levels, CI, and automated build/test/deploy keep a complex system observable and shippable (§11)
