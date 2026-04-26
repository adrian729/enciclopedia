# Ch 6: Sharded Services

## Table of Contents

- [1. Pattern Definition](#1-pattern-definition)
- [2. Sharded Caching](#2-sharded-caching)
  - [2.1. Why Shard a Cache](#21-why-shard-a-cache)
  - [2.2. Cache Criticality and Hit Rate](#22-cache-criticality-and-hit-rate)
  - [2.3. Replicated, Sharded Caches](#23-replicated-sharded-caches)
  - [2.4. Hands-On: Sharded Memcache](#24-hands-on-sharded-memcache)
- [3. Sharding Functions](#3-sharding-functions)
  - [3.1. Selecting a Key](#31-selecting-a-key)
  - [3.2. Consistent Hashing](#32-consistent-hashing)
  - [3.3. Hands-On: Consistent HTTP Sharding Proxy](#33-hands-on-consistent-http-sharding-proxy)
- [4. Beyond Caches](#4-beyond-caches)
  - [4.1. Sharded, Replicated Serving](#41-sharded-replicated-serving)
  - [4.2. Hot Sharding Systems](#42-hot-sharding-systems)

## 1. Pattern Definition

- **Sharded service** — unlike a replicated service where every replica can serve every request, each replica (a *shard*) serves only a subset of requests; useful when the working set is too large for a single machine.
- **Root** — the load-balancing node in front of the shards; it inspects each request and routes it to the appropriate shard or shards.
- **Replicated vs. sharded** — replicated services are typically stateless and scale for redundancy and request volume; sharded services are typically stateful and scale because the *state itself* is too large for one machine.

## 2. Sharded Caching

- **Sharded cache** — a cache placed between users and the frontend implementation, partitioned so each shard owns a disjoint slice of the keyspace.

### 2.1. Why Shard a Cache

- **Memory utilization argument** — given a 200 GB result set, 1,000 RPS demand, and cache nodes that each hold 10 GB and serve 100 RPS, ten *replicated* caches still serve the RPS but each holds the same 10 GB, covering only 5% of the data. Ten *sharded* caches serve the same RPS but each holds a unique 10 GB, covering 50% — a tenfold gain in working-set coverage because each key lives in only one shard.

### 2.2. Cache Criticality and Hit Rate

- **Hit rate** — the percentage of requests served from cache; determines the overall capacity and latency of the system, not just the cache itself.
- **Sharded caches are fragile** — because each user always maps to the same shard, losing a shard means that user permanently misses cache until the shard is restored, unlike a replicated cache where any replica can answer.
- **Capacity sizing under cache failure** — a backend rated for 1,000 RPS fronted by a 50%-hit cache appears to do 2,000 RPS, but should be rated at ~1,500 RPS so the system survives losing half the cache replicas.
- **Latency contribution** — a 25%-hit cache returning in 10 ms in front of a 100 ms backend yields 77.5 ms average latency; cache loss won't drop request volume but can cause queue buildup and timeouts. Load-test with and without the cache.
- **Rollouts cost capacity** — deploying a new sharded-cache version temporarily loses capacity; replicating shards is the mitigation.

### 2.3. Replicated, Sharded Caches

- **Replicated, sharded service** — implement each shard as a small replicated service rather than a single server; combines Chapter 5's pattern with the sharded pattern.
- **Benefits** — shards survive individual failures, peak-time rollouts become safe (assuming over-provisioning), and each shard can scale independently in response to its own load — the foundation for hot sharding.

### 2.4. Hands-On: Sharded Memcache

- **Demo** — deploy `memcached` as a Kubernetes `StatefulSet` with a headless `Service` to give each replica a stable DNS name (`memcache-0.memcache`, etc.), then front it with `twemproxy` (nutcracker) configured for `fnv1a_64` hashing and `ketama` (consistent) distribution. Two routing options shown: `twemproxy` as an *ambassador* sidecar inside each consumer pod, or as a separate replicated *shard router* service (less complexity per consumer, but adds a network hop and must itself be scaled).

## 3. Sharding Functions

- **Sharding function** — `Shard = ShardingFunction(Req)`; maps a request to one of N shards. Commonly built from a hash function and the modulo operator: `Shard = hash(Req) % N`.
- **Required properties** — *determinism* (same input always yields the same shard, so a request consistently hits the same cache) and *uniformity* (outputs spread evenly across shards, so load is balanced).

### 3.1. Selecting a Key

- **Hashing the whole request is wrong** — request time and client IP would force two functionally identical requests to different shards, destroying the cache.
- **Too general** — `shard(request.path)` groups requests that should differ; a French and an English user asking for the same path would land on the same shard and one might receive the other's localized response.
- **Too specific** — `shard(request.ip, request.path)` splits two French IPs across different shards even though they should share results.
- **Right level** — `shard(country(request.ip), request.path)` derives a coarse attribute from the IP so all French requests for a path share a shard, while US requests use a different one. Picking the right key requires understanding which request attributes actually change the response.

### 3.2. Consistent Hashing

- **The re-sharding problem** — switching `hash(Req) % 10` to `hash(Req) % 11` remaps a large fraction of keys to new shards; for a cache, this approximates a complete cache failure as the miss rate spikes until shards are repopulated.
- **Consistent hashing function** — guaranteed to remap only roughly *# keys / # shards* when the shard count changes (e.g., scaling 10→11 shards remaps under 10% of keys instead of nearly all of them).

### 3.3. Hands-On: Consistent HTTP Sharding Proxy

- **Demo** — use nginx as the sharding proxy: an `upstream` block lists the shard backends and uses `hash $request_uri consistent` to key on the full request URI with a consistent hash. The URI (path + query + fragment) is a good general-purpose key; cookies or locale must be added if the service customizes by user or region.

## 4. Beyond Caches

### 4.1. Sharded, Replicated Serving

- **Sharded, replicated serving** — sharding applies to any service whose state outgrows one machine, not just caches. The shard key may come from user context rather than the HTTP request.
- **Multi-player game example** — a virtual world too large for one machine is sharded by player location, since players far apart in the world rarely interact; all players in a region land on the same set of servers.

### 4.2. Hot Sharding Systems

- **Hot shard** — load on a sharded cache is ideally even, but organic traffic skew (e.g., one photo going viral) often drives disproportionate load to a single shard.
- **Hot sharding** — with replicated shards plus autoscaling, a hot shard gets more replicas while cold shards can be co-located on fewer machines; the system rebalances dynamically as traffic patterns shift, e.g., replicating a hot Shard A onto a second machine while collapsing Shards B and C onto one.
