# Ch 5.08: Cache Strategies

## Table of Contents

- [1. What Cache Is and Why to Use It](#1-what-cache-is-and-why-to-use-it)
- [2. Cache Hit Rate and What You Cache](#2-cache-hit-rate-and-what-you-cache)
- [3. Write Strategies](#3-write-strategies)
- [4. Cache Invalidation](#4-cache-invalidation)
- [5. Cache Eviction](#5-cache-eviction)
- [6. Failure Scenarios and Redundancy](#6-failure-scenarios-and-redundancy)
- [7. Data Structure](#7-data-structure)
- [8. Thundering Herd on Cold Cache](#8-thundering-herd-on-cold-cache)

## 1. What Cache Is and Why to Use It

- **Definition** — volatile storage that improves query efficiency; data is lost when the cache goes down, unlike a database
- **Three benefits** — latency (memory is ~100× faster than disk), throughput (more work in the same time on a single core), bandwidth (data closer to the user; CDNs are a form of cache)
- **Justify, don't hand-wave** — cache costs maintenance and complexity; candidates who throw it in front of every database without a reason get dinged. Tie the need to a non-functional requirement: e.g., sub-20 ms latency with 100k read QPS
- **Latency gain depends on the target** — reducing 5 ms → 0.1 ms is pointless if the requirement is 500 ms; meaningful if the requirement is 20 ms

## 2. Cache Hit Rate and What You Cache

- **Cache Hit Rate = Hits / (Hits + Misses)** — if the rate is low, the cache costs money without adding value
- **Always state what's cached** — "put a cache in front of the database" is hand-wavy. The key, value, and invalidation strategy need to be explicit
- **Details change the hit rate dramatically** — for a search service with documents "System Design Interview" and "Coding Interview":

| Option | Example | Speed | Hit rate |
|---|---|---|---|
| Cache full search query | `"My OR Design" → [1]` | Fast key-value lookup | Poor — free-text queries rarely repeat |
| Cache per-token | `"Design" → [1]`, `"Interview" → [1, 2]` | Requires tokenization + combine | Much better — tokens repeat |

- **Applies beyond key-value stores** — if the cache is a trie, talk about what's in each node; if a queue, talk about what event is queued; read/write access patterns still need to be justified

## 3. Write Strategies

| Strategy | How it writes | Advantage | Disadvantage |
|---|---|---|---|
| **Write-Through** | Synchronously to cache AND data store | Data exists in both | Higher write latency, lower availability, atomicity not guaranteed (see distributed transaction) |
| **Write-Back** | To cache first, data store later | Lowest write latency; data immediately readable | Data loss if cache fails before persisting |
| **Write-Around** | To data store only; cache populated on read miss | Durable (disk first); no cache-failure loss | First read is slow; cache warm-up complexity |

- **Read-through companion** — with write-around, reads that miss fetch from the database and populate the cache
- **Prefer delete over update on cache invalidation** — two concurrent database updates (A, B) don't guarantee A hits cache before B in a distributed system; deleting the key is idempotent and avoids ordering issues

## 4. Cache Invalidation

> "There are only two hard things in Computer Science: cache invalidation and naming things." — Phil Karlton

- **Option 1: Listener on source values** — a pub/sub or post-commit listener invalidates the key on change. Freshest data. Expensive to build when there are many dependencies
- **Option 2: Periodic recomputation job** — recompute the materialized value on a schedule. Simpler than listeners; the value is always present on read. Data is stale between runs; wastes work for infrequently queried values
- **Option 3: Cache a lower layer and fan-in on read** — cache only part of the computation; mix cached and live data on read. Trades slightly higher read latency for simpler invalidation. Common for Netflix recommendations and News Feed where signals change often
- **Option 4: TTL (time-to-live)** — entry expires after a set duration. Short TTL = more misses; long TTL = staler data. DNS uses TTL because sending invalidation to every browser is impractical
- **Materialized values don't have to be in memory** — the same invalidation problem applies to disk-persisted materialized fields

## 5. Cache Eviction

- **Why needed** — cache memory is expensive and limited; you can't keep everything
- **Goal** — minimize memory used while keeping the hit rate high. Evicting a hot key regresses average latency by forcing disk reads
- **Least Recently Used (LRU)** — evict values not accessed/updated recently. Works when recency predicts future access; fails for cyclical queries (data returns after a long gap)
- **Least Frequently Used (LFU)** — evict values with the lowest access count. Works when frequency predicts future access; fails for stocks that were active yesterday and went quiet today
- **Custom eviction** — use domain knowledge to predict future hit rate. E.g., a concert venue's data stays hot the day before the event and is evicted after
- **Right answer is query-pattern dependent** — ask the interviewer, make assumptions, pick the fit

## 6. Failure Scenarios and Redundancy

- **Unlike databases, a crashed cache loses all data** — requests that previously hit the cache now flood the database and can cause a thundering herd
- **Option 1: Periodic snapshot** — serialize the cache to a backup file every N seconds. Fast writes; data may be minutes stale; restoring takes time to decompress
- **Option 2: Write-ahead log (WAL)** — append to disk log before writing to cache. Most up-to-date on recovery; slower writes; long WAL replay. Combine with periodic snapshots to replay only from the latest snapshot
- **Option 3: No backup** — accept the data loss when data is transient (e.g., driver-location updates that are overwritten every few seconds)
- **Option 4: Replication** — same pros and cons as database replication; a failed leader can be rebuilt from replicas, reads can failover to a replica

## 7. Data Structure

- **Cache isn't always a key-value store** — any in-memory structure counts: a trie for type-ahead, a quadtree for location queries
- **Same considerations apply** — if the in-memory structure dies, how is it rebuilt? What's the failover? Treat in-memory app-server data the same way you'd treat a cache

> **Warning** — candidates often think a cache directly improves bandwidth. Streaming YouTube or Netflix is usually network-bound; putting a cache server next to the database in the same data center doesn't help if the bottleneck is the network to the user. That's why CDNs move data physically closer to the user.

## 8. Thundering Herd on Cold Cache

- **Problem** — many simultaneous requests miss a cold cache and all hit the underlying data source at once, bringing it down
- **Cache blocking** — only one request fetches from the data source; the rest wait for the cache to warm up
- **Timeout trade-off** — if the single fetcher fails, the rest wait forever. A timeout lets the next request retry. Longer timeout = more waiting on failure; shorter timeout = more load on the data source when something goes wrong
