# Ch 5.07: Sharding

## Table of Contents

- [1. What Sharding Is and Why](#1-what-sharding-is-and-why)
- [2. Vertical vs Horizontal Sharding](#2-vertical-vs-horizontal-sharding)
- [3. Choosing a Sharding Scheme](#3-choosing-a-sharding-scheme)
- [4. Consistent Hashing](#4-consistent-hashing)
- [5. Sharding Non-Row Data Structures](#5-sharding-non-row-data-structures)
- [6. Outlier Keys](#6-outlier-keys)
- [7. Geo-Shards](#7-geo-shards)
- [8. Trade-off Considerations](#8-trade-off-considerations)

## 1. What Sharding Is and Why

- **Definition** — dividing data into smaller chunks across different servers; applies to app servers and caches too, not only storage
- **Throughput** — multiple shards take writes instead of a single shard (works if shards are **share-nothing**)
- **Capacity** — each database's storage cap (e.g., 1 TB) becomes the aggregate `N × cap`
- **Latency** — local shards accept local writes, reducing cross-region round trips; smaller per-shard data also speeds queries
- **Perceived availability** — a failed shard only takes out its partition of users, not the whole app. Overall availability is *not* improved — failure probability rises with more shards — but correlated catastrophic failure is reduced
- **Not the first resort** — before sharding, consider cold storage (storage), compression (bandwidth), batching (QPS); only shard when it's the best fit

## 2. Vertical vs Horizontal Sharding

| Aspect | Vertical Sharding | Horizontal Sharding |
|---|---|---|
| Split by | Columns (migrate some columns into new tables) | Rows (divide rows across shards) |
| When | Database has too many columns or a sparse column | Database has too many rows / too high QPS |
| Advantage | Reduced per-table data, less storage for sparse columns | Reduces burden on a single global shard |
| Disadvantage | Multiple updates per key, joins on read are expensive | Requires choosing a sharding key |
| Interview reality | Rare — most designs don't have enough columns to split | Common — the default for scalability discussions |

## 3. Choosing a Sharding Scheme

- **Always give at least 2 options and discuss trade-offs** — interviewers grade on option generation, not a single "right" answer
- **Hash key** — hash an attribute (e.g., user_id) into `[0, 2^32)` and assign ranges to shards. Good distribution, minimizes hotspots from uneven keys. Bad for range queries because related keys are scattered
- **Range key** — sort keys, assign each range to a shard. Efficient range queries within a shard. Prone to hotspots on writes if the range is time-based (all current writes hit one shard)
- **Example — tweets table** (`tweet_id, user_id, timestamp, tweet_message`):

| Sharding key | `tweet(user_id, msg)` write | `get_tweets_for_user(user, t1, t2)` | `get_all_tweets(t1, t2)` |
|---|---|---|---|
| Shard by timestamp | Hotspot — all writes go to current-time shard | Hits only 1 shard | Hits only 1 shard |
| Shard by `(user_id, timestamp)` | Distributed by user | Hits 1 shard (per user) | Scatter-gather across all shards |

- **Recommendation pattern** — assume one query is rarer, pick the scheme that optimizes the common case, and verbalize the assumption
- **Sharding key ≠ primary/index key** — shard by one attribute, then add primary keys and secondary indices within each shard for local query optimization

## 4. Consistent Hashing

> **Reminder** — candidates treat consistent hashing as a silver bullet. It's not. It has trade-offs based on data distribution, queries, and hot keys.

- **Problem it solves** — plain `hash mod N` causes a rebalancing disaster when nodes are added/removed (key 100 goes to server 0 with 10 servers, server 1 with 11, server 4 with 12 — almost every key moves)
- **What it solves**:
  1. Distributing keys more evenly across shards
  2. Minimizing data migration when servers are added, removed, or fail
- **What it does NOT solve** — a super-hot key still hammers its shard. If 99% of traffic targets one key, that shard is on fire regardless of the ring
- **Algorithm concepts**:
  1. Hash keys live on a circle (e.g., 0 to 2^32)
  2. Each key routes to the next node clockwise on the ring
  3. If a node fails, the next node picks up its keys
  4. Add virtual nodes between real nodes so one failure's load is spread across several successors instead of producing a thundering herd on the single next node
- **Interview rule** — know *when and why* to use consistent hashing; don't retell the algorithm unless it's core to the question

## 5. Sharding Non-Row Data Structures

- **Sharding isn't row-only** — the same reasoning (read pattern, write pattern, data distribution) applies to trees, graphs, and grids
- **Tree** — watch for deep subtrees that grow too big; common for n-ary trees, quadtrees, tries (e.g., prefix queries on a trie can hotspot one branch)
- **Graph** — adjacency queries are common, so think about proximity across shards; used for location and social-graph questions
- **Grid** — 2D arrays; geo-location questions use them. Hotspots can appear in a cell; adjacent-cell queries need good locality

## 6. Outlier Keys

- **Source** — celebrities, enterprise customers, power users generate traffic far above the norm; any scheme puts them on *some* shard, and that shard overheats
- **Option 1: Dedicated shard** — take outliers out of the generic space. Common in enterprise apps with a few huge customers. Cost: per-key configuration complexity
- **Option 2: Shard further** — split the outlier across sub-shards. Reads may still require scatter-gather across sub-shards. Sometimes fine (looking for *any* driver in NYC — one sub-shard is enough)

## 7. Geo-Shards

- **Multi-layer sharding** — a top-level geo-shard (zone) routes users to their region; within each region, shard further
- **Simplifies single-region users** — requests always hit the same shard
- **Social graphs break the simple case** — friends scattered across geo-shards force scatter-gather. Heuristic: friends usually cluster geographically, so group related users by location to minimize cross-shard reads

## 8. Trade-off Considerations

- **Scatter/gather** — reads that hit every shard are slower than single-shard reads. If you shard a driver table by `driver_id` but query by `location_id`, every lookup is a scatter-gather
- **Hotspots** — think about both read and write query patterns. Realistic hotspot examples: time-range sharding on a chat app (current hour is hot), location-ID sharding where one city is densely populated, celebrity posts that are read-heavy
- **Machine hops** — subsequent reads that jump between shards (friend-of-friend social graph). Sharding by primary location often reduces hops because friends cluster geographically
- **No perfect scheme** — interviewers can always construct a hypothetical that breaks any scheme. Your job is to list options, discuss trade-offs, make a recommendation with assumptions, and adapt when the interviewer changes assumptions
