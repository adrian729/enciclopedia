# Ch 5.23: Service Discovery and Request Routing

## Table of Contents

- [1. Load Balancing](#1-load-balancing)
- [2. Shard Discovery](#2-shard-discovery)
- [3. Client Routing Strategies](#3-client-routing-strategies)

## 1. Load Balancing

- **Purpose** — distribute load across a pool of functionally equivalent servers
- **Algorithms** — round-robin, or health-aware routing that monitors CPU / memory / bandwidth and forwards to the least-utilized host
- **Don't over-invest in the interview** — load balancing is generic to all questions; only dig in if the design is materially affected

## 2. Shard Discovery

- **Purpose** — when you've sharded a database, a request must be routed to the right shard; shard discovery maps request attributes to a shard and a specific node
- **Shard is logical** — a shard is a logical concept and can contain many nodes; shard discovery may return multiple nodes in case one is down
- **Signature** — returns a single node or multiple (for failover):
  - `get_node(request_attribute) → (node_id, private_ip)`
  - `get_node(request_attribute) → (node_id, [private_ip])`
- **Mapping storage** — typically in a coordination service like **ZooKeeper**. Example mapping for keys 1–100 across 3 shards × 3 nodes:

| Key range | Shard | Nodes |
|---|---|---|
| 1–33 | 1 | (node_1, ip_1), (node_2, ip_2) |
| 34–66 | 2 | (node_2, ip_2), (node_3, ip_3) |
| 67–100 | 3 | (node_1, ip_1), (node_3, ip_3) |

## 3. Client Routing Strategies

| Option | Mechanism | Advantage | Disadvantage |
|---|---|---|---|
| **Central service** | Client calls ZooKeeper (or similar) on every request | Simple — one place owns the mapping | Extra hop adds latency; central service becomes a scale bottleneck |
| **Node-aware client** | Client fetches the mapping at startup and caches it | Lower request latency — no discovery hop | Config drift until the update propagates; consistency suffers if pushes lag |

- **When latency matters, prefer node-aware** — accept occasional routing to a stale node when the config changes, at the cost of managing client-side updates
