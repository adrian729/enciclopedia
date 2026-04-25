# Ch 13: Design a Search Autocomplete System

## Table of Contents

- [1. Requirements and Scope](#1-requirements-and-scope)
- [2. Back-of-the-Envelope Estimation](#2-back-of-the-envelope-estimation)
- [3. High-Level Design](#3-high-level-design)
- [4. Trie Data Structure](#4-trie-data-structure)
- [5. Trie Optimizations](#5-trie-optimizations)
- [6. Data Gathering Pipeline](#6-data-gathering-pipeline)
- [7. Query Service](#7-query-service)
- [8. Trie Operations](#8-trie-operations)
- [9. Storage Sharding](#9-storage-sharding)
- [10. Wrap-Up Topics](#10-wrap-up-topics)

## 1. Requirements and Scope

- **Feature** — search autocomplete (also called typeahead, search-as-you-type, incremental search, or "design top k"); returns matches as the user types
- **Constraints agreed in interview** — match prefix only (not middle), return top 5 suggestions, rank by historical query frequency, no spell-check, English only, lowercase alphabetic only, 10M DAU
- **Non-functional requirements** — fast response (<100ms per Facebook's typeahead article, otherwise stuttering), relevant, sorted by popularity, scalable, highly available

## 2. Back-of-the-Envelope Estimation

- **Per-query data** — assume 4 words × 5 chars = 20 bytes per query (ASCII)
- **Request fanout** — every keystroke sends one request, so typing "dinner" triggers 6 requests (`q=d`, `q=di`, …, `q=dinner`)
- **QPS** — 10M users × 10 queries/day × 20 chars / 86,400s ≈ 24,000 QPS; peak ≈ 48,000
- **New data/day** — 20% of queries are new → 10M × 10 × 20 bytes × 20% = 0.4 GB/day

## 3. High-Level Design

- **Two services**
  - **Data gathering service** — collects user queries and aggregates frequencies in real time (good starting point; not realistic at scale)
  - **Query service** — given a prefix, returns the 5 most-searched terms
- **Naive query** — store `(query, frequency)` table and run `SELECT ... ORDER BY frequency DESC LIMIT 5 WHERE query LIKE 'tw%'`; works on small data, becomes a bottleneck at scale

## 4. Trie Data Structure

- **Why trie** — relational DBs are too slow for top-5-by-prefix queries; **trie** (prefix tree, pronounced "try", from "retrieval") compactly stores strings for fast prefix lookup
- **Structure**
  - Root represents empty string
  - Each node stores a character, has up to 26 children (one per letter)
  - Each tree node represents a single word or a prefix
- **Frequency on nodes** — to support sort-by-popularity, store frequency on each node so we can rank children
- **Naive top-k algorithm** — given prefix `p`, total nodes `n`, children of given node `c`:
  1. Find prefix node — O(p)
  2. Traverse subtree to collect valid descendants — O(c)
  3. Sort and pick top k — O(c log c)
- **Why naive is too slow** — worst case requires traversing the entire subtree below the prefix

## 5. Trie Optimizations

- **Limit prefix length** — users rarely type queries longer than ~50 chars, so prefix lookup becomes O(small constant) ≈ O(1)
- **Cache top-k at every node** — store top 5 most-frequent queries directly on each prefix node (e.g., node `be` stores `[best:35, bet:29, bee:20, be:15, beer:10]`). Trades space for time
- **Resulting complexity** — O(1) to find prefix node + O(1) to return cached top-k = O(1) overall

## 6. Data Gathering Pipeline

- **Why not real-time** — billions of queries/day; updating the trie on each query slows the query service, and top suggestions don't change much hour-to-hour
- **Pipeline components**

| Component | Role |
|---|---|
| **Analytics Logs** | Append-only, unindexed raw query logs |
| **Aggregators** | Reduce raw logs into aggregated frequency data; interval depends on use case (real-time for Twitter, weekly for many Google keywords) |
| **Aggregated Data** | Table of `(query, time, frequency)` summarizing aggregation periods |
| **Workers** | Async servers that build the trie from aggregated data and write to Trie DB |
| **Trie Cache** | Distributed in-memory cache holding the trie for fast reads; takes weekly snapshots |
| **Trie DB** | Persistent storage for the trie |

- **Trie DB options**
  - **Document store** (e.g., MongoDB) — serialize the weekly trie snapshot
  - **Key-value store** — every prefix becomes a key, node data becomes the value (hash-table form of the trie)

## 7. Query Service

- **Improved flow** — request → load balancer → API server → API server reads trie data from Trie Cache → builds suggestions; on cache miss, replenish from Trie DB so subsequent same-prefix requests hit the cache
- **Lightning-fast optimizations**
  - **AJAX request** — fetch suggestions without refreshing the page
  - **Browser caching** — Google sends `Cache-Control: private, max-age=3600`, caching suggestions in the browser for 1 hour. `private` means single-user (no shared cache); `max-age=3600` is the TTL in seconds
  - **Data sampling** — log only 1 of every N requests to cut storage and processing cost at scale

## 8. Trie Operations

- **Create** — workers build the trie from aggregated analytics data
- **Update**
  - **Option 1 (preferred)** — rebuild the trie weekly and atomically swap it in
  - **Option 2** — update individual nodes directly. Slow because all ancestors up to the root must also be updated (each ancestor caches top-k of children). Acceptable only for small tries. Example: changing "beer" from 10 to 30 cascades the value up through every ancestor that previously cached "beer"
- **Delete** — to remove hateful, violent, sexually explicit, or dangerous suggestions, add a filter layer in front of the Trie Cache. The filter rules are flexible; offending entries are removed from the database asynchronously so the next rebuild excludes them

## 9. Storage Sharding

- **Naive sharding by first character** — split queries A–M and N–Z across two servers; up to 26 shards possible. Add a second/third sharding level (e.g., `aa-ag`, `ah-an`) to go beyond 26 servers
- **Imbalance problem** — many more queries start with 'c' than 'x', creating uneven shards
- **Smarter sharding** — analyze historical distribution and group letters so each shard carries comparable load (e.g., one shard for `s` and another for `u`–`z` combined). A **shard map manager** maintains a lookup database mapping prefixes to shards

## 10. Wrap-Up Topics

- **Multi-language support** — store Unicode characters in trie nodes (Unicode covers all writing systems, modern and ancient)
- **Per-country tries** — different countries have different popular queries; build separate tries per country and serve them from CDNs to reduce latency
- **Real-time/trending queries** — original design fails because workers run weekly and trie rebuild is slow. Mitigations (full design out of scope):
  - Reduce working set by sharding
  - Reweight ranking model to favor recent queries
  - Use stream processing — Apache Hadoop MapReduce, Spark Streaming, Storm, Kafka — to handle continuous data flow
