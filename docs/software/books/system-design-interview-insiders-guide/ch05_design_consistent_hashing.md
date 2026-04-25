# Ch 5: Design Consistent Hashing

## Table of Contents

- [1. The Rehashing Problem](#1-the-rehashing-problem)
- [2. Consistent Hashing Defined](#2-consistent-hashing-defined)
- [3. Hash Space and Hash Ring](#3-hash-space-and-hash-ring)
- [4. Mapping Servers and Keys](#4-mapping-servers-and-keys)
- [5. Server Lookup](#5-server-lookup)
- [6. Adding and Removing Servers](#6-adding-and-removing-servers)
- [7. Two Issues in the Basic Approach](#7-two-issues-in-the-basic-approach)
- [8. Virtual Nodes](#8-virtual-nodes)
- [9. Finding Affected Keys](#9-finding-affected-keys)
- [10. Benefits and Real-World Use](#10-benefits-and-real-world-use)

## 1. The Rehashing Problem

- **Naive distribution** — `serverIndex = hash(key) % N` where `N` is server-pool size; works fine when `N` is fixed and data is evenly distributed
- **Failure mode** — when a server is added or removed, `N` changes, so almost every key maps to a different server even though the hash itself didn't change
- **Cache-miss storm** — if server 1 of 4 goes offline, most keys (not just those on server 1) get redistributed and clients hit the wrong servers, causing a storm of cache misses

## 2. Consistent Hashing Defined

> **Consistent hashing (Wikipedia)** — a special kind of hashing such that when a hash table is re-sized and consistent hashing is used, only `k/n` keys need to be remapped on average, where `k` is the number of keys and `n` is the number of slots. In contrast, traditional hash tables remap nearly all keys when slot count changes.

## 3. Hash Space and Hash Ring

- **Hash space** — assume SHA-1 as the hash function; SHA-1's output range is `0` to `2^160 - 1`
- **Hash ring** — connect both ends of the linear hash space so the maximum value wraps around to `0`, forming a circle

## 4. Mapping Servers and Keys

- **Hash servers** — using the same hash function `f`, servers are placed on the ring by hashing their IP or name
- **Hash keys** — cache keys are hashed onto the same ring (no modular operation, unlike the rehashing approach)

## 5. Server Lookup

- **Clockwise rule** — to find the server for a key, walk clockwise from the key's position on the ring until you hit a server; that server owns the key
- **Example** — with 4 servers placed on the ring, `key0 → server 0`, `key1 → server 1`, `key2 → server 2`, `key3 → server 3` simply by following the clockwise lookup

## 6. Adding and Removing Servers

- **Add a server** — only keys between the new server and its anticlockwise neighbor are remapped; all other keys stay put. Example: adding server 4 only relocates `key0` (now the first server clockwise from `key0`'s position); `key1`, `key2`, `key3` remain unaffected
- **Remove a server** — only keys owned by that server are remapped to the next server clockwise. Example: removing server 1 forces only `key1` to move to server 2; the rest are untouched

## 7. Two Issues in the Basic Approach

- **Origin** — algorithm introduced by Karger et al. at MIT
- **Unequal partitions** — a partition is the hash space between adjacent servers; with arbitrary placement, partitions can be very small or very large. Removing `s1` may double `s2`'s partition relative to `s0` and `s3`
- **Non-uniform key distribution** — depending on where servers land on the ring, most keys can pile onto one server (e.g., server 2) while others (server 1, server 3) hold no data

## 8. Virtual Nodes

- **Definition** — each real server is represented by multiple virtual nodes (also called replicas) on the ring; e.g., `s0_0, s0_1, s0_2` and `s1_0, s1_1, s1_2` instead of `s0` and `s1`
- **Why it helps** — each server now owns multiple partitions scattered around the ring, balancing load
- **Lookup** — same clockwise walk; the first virtual node encountered identifies the real server (e.g., reaching `s1_1` means the key belongs to server 1)
- **Standard-deviation tradeoff** — more virtual nodes → smaller standard deviation → more balanced distribution. Online experiments show ~10% of mean with 100 virtual nodes and ~5% with 200; more virtual nodes cost more memory to track, so the count is a tunable tradeoff

## 9. Finding Affected Keys

- **Adding a server** — affected range starts at the new node and moves anticlockwise to the previous server on the ring; keys between those two positions are redistributed to the new node. Example: adding `s4` redistributes keys located between `s3` and `s4` to `s4`
- **Removing a server** — affected range starts at the removed node and moves anticlockwise until the next server; those keys redistribute to the next clockwise server. Example: removing `s1` moves keys between `s0` and `s1` to `s2`

## 10. Benefits and Real-World Use

- **Minimal redistribution** — only a fraction of keys move when servers are added or removed, eliminating cache-miss storms
- **Easy horizontal scaling** — data spreads more evenly across servers, so adding capacity is straightforward
- **Mitigates hotspot keys** — heavy access to a single shard (e.g., Katy Perry, Justin Bieber, Lady Gaga all on the same shard) is smoothed because virtual nodes spread the load
- **Real-world systems** — partitioning component of Amazon's Dynamo database, data partitioning in Apache Cassandra, Discord chat application, Akamai content delivery network, Maglev network load balancer
