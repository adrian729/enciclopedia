# Service Discovery & Load Balancing

> Liu's Ch 5.23 separates two related but distinct problems: load balancing (which healthy node within a pool) and shard discovery (which shard, then which node). Xu introduces the load balancer in his scaling-evolution chapter and reuses it in nearly every design.

## Table of Contents

- [1. Two Problems, One Concept](#1-two-problems-one-concept)
- [2. Load Balancing](#2-load-balancing)
  - [2.1. Round-Robin](#21-round-robin)
  - [2.2. Health-Aware](#22-health-aware)
  - [2.3. Layer 4 vs Layer 7](#23-layer-4-vs-layer-7)
- [3. Shard Discovery](#3-shard-discovery)
- [4. Client Routing — Central vs Node-Aware](#4-client-routing--central-vs-node-aware)
- [5. Statelessness Enables Both](#5-statelessness-enables-both)
- [Sources](#sources)

## 1. Two Problems, One Concept

Service discovery handles two related questions:

1. **Which healthy node within this pool should serve this request?** (load balancing)
2. **Which shard does this key live on, and which node is the current owner of that shard?** (shard discovery)

Both are a mapping from a request to a backend. The answers are usually maintained in different stores.

## 2. Load Balancing

The load balancer is the public entry point. Clients hit its IP; backends sit on private IPs behind it. New backends join the pool seamlessly; failed backends are removed from rotation.

### 2.1. Round-Robin

Simplest. Each new request goes to the next backend in order. Fine when backends are identical and stateless, and request cost is uniform.

### 2.2. Health-Aware

The LB checks each backend periodically (HTTP health check, TCP ping). Unhealthy backends drop out of rotation. Variants:

- **Least-connections** — route to the backend with the fewest active connections.
- **Latency-aware** — route to the lowest-latency backend.
- **Sticky sessions** — bind a client to a backend by cookie or hash. Adds operational pain on scale-out and failure; both books recommend avoiding it via [statelessness](fundamentals/scaling-evolution.md).

### 2.3. Layer 4 vs Layer 7

A **Layer 4** (TCP) load balancer is faster but can't read application content. A **Layer 7** (HTTP) load balancer can route by URL path, header, or cookie — useful for canary deploys and request-aware routing. See [Networking & DNS](fundamentals/networking-and-dns.md) for the OSI primer.

## 3. Shard Discovery

For sharded data, the request must first pick a shard, then pick a node within the shard. The mapping is typically stored in **ZooKeeper** (or etcd, Consul):

```
shard_for(request_attribute) → shard_id
nodes_for(shard_id) → [node_a, node_b, node_c]
```

The mapping changes when shards split, when nodes are added/removed, or when an outage promotes a follower to leader. The discovery service is the source of truth.

For consistent-hashing-based partitioning (see [Sharding & Consistent Hashing](fundamentals/sharding-and-consistent-hashing.md)), the mapping is computed by walking the ring rather than looked up — but the ring's membership *itself* is stored centrally.

## 4. Client Routing — Central vs Node-Aware

Two ways to put the discovery information in the client's hands:

| Approach | How it works | Trade-off |
|---|---|---|
| Central service | Client asks the discovery service for the right node on every request, or per session | Simple; extra hop adds latency. |
| Node-aware client | Client fetches the mapping at startup and caches it locally | Lower latency; risk of config drift when the mapping changes mid-session. |

Cassandra-style systems use node-aware clients with periodic refresh. Service-mesh proxies (Envoy, Linkerd) sit alongside the client and absorb the discovery logic, making it look like a central service from the client's view but with a local fast path.

## 5. Statelessness Enables Both

Both load balancing and node-aware shard routing depend on the backends being stateless or, at least, on per-user state being externalized. Sticky sessions (binding a client to one backend forever) defeat the load balancer's ability to redistribute on failure or scale.

The exceptions are intentionally stateful — chat servers (WebSocket-bound clients), presence servers — and the discovery layer is what maps clients to those specific stateful backends. Xu's chat system uses ZooKeeper for chat-server selection by geography and capacity.

## Sources

- [Liu Ch 5.23: Service Discovery and Routing](software/system-design-interview/books/system-design-interview-fundamentals/ch05_23_service_discovery.md)
- [Xu Ch 1: Scale From Zero to Millions of Users](software/system-design-interview/books/system-design-interview-insiders-guide/ch01_scale_zero_to_millions.md) (load balancer section)
- [Xu Ch 12: Design a Chat System](software/system-design-interview/books/system-design-interview-insiders-guide/ch12_design_a_chat_system.md) (ZooKeeper for chat-server discovery)
