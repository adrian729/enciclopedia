# Databases, Schema, and Indexing

> Liu's chapter is the more thorough reference, with explicit category reasoning and a deep section on indexing internals. Xu's treatment is shorter (a SQL-vs-NoSQL paragraph in Ch 1, a worked schema in each case study). They agree on the headline rule: choose by access pattern, not by trend.

## Table of Contents

- [1. Schema First, Database Second](#1-schema-first-database-second)
- [2. Normalization vs Denormalization](#2-normalization-vs-denormalization)
- [3. Indexes](#3-indexes)
  - [3.1. What an Index Is](#31-what-an-index-is)
  - [3.2. Primary vs Secondary](#32-primary-vs-secondary)
  - [3.3. Composite Indexes](#33-composite-indexes)
  - [3.4. Geographic Queries](#34-geographic-queries)
- [4. Choosing a Database — Category Reasoning](#4-choosing-a-database--category-reasoning)
- [5. Multiple Databases per Question](#5-multiple-databases-per-question)
- [Sources](#sources)

## 1. Schema First, Database Second

Schemas begin with a logical view — entities, foreign keys, join tables for many-to-many — and defer the database choice until access patterns are clear. Walking the schema against the agreed requirements catches nonsensical designs: a `Message Table(user_id, receiver_id, ...)` fails for group chat where a user and a receiver belong to multiple rooms. Detail belongs on arrows (unsorted driver ID list vs scored list vs single ID), on queues (enqueue `raw_video_id`, not bytes that exhaust memory), and on the table layout (flat table vs indexed table changes efficiency).

## 2. Normalization vs Denormalization

Normalized is the default. Denormalize only when read throughput is the specific bottleneck. The tradeoff: normalization minimizes update anomalies and storage cost; denormalization reduces joins on the read path. Cross-shard joins, in particular, are expensive enough that denormalization is the standard fix — Xu calls this out as the canonical mitigation for "cross-shard join difficulty."

## 3. Indexes

### 3.1. What an Index Is

An index is a sorted auxiliary structure that turns `O(N)` scans into `O(log N)` searches, implemented as a **B-Tree** or as an **LSM** with a **Sorted Strings Table (SST)**. Database indexes are *not* hashmaps — hashmaps are in-memory, while on-disk indexes are sorted structures. Liu emphasizes this because candidates frequently mis-state it.

### 3.2. Primary vs Secondary

A **primary (clustered)** index sorts the main table on disk; a **secondary** index points back into it, trading write cost for read speed. Each additional secondary index slows writes (every insert/update/delete must update every index) and speeds the queries that use it.

### 3.3. Composite Indexes

A composite index on `(col_a, col_b)` is order-sensitive. `(status, location)` is efficient for "all busy drivers in Chicago" but useless for "all drivers in New York" because the prefix `status` isn't bound. The order of columns is chosen to match the dominant query pattern.

### 3.4. Geographic Queries

Two interview-suitable patterns:

- **Geohash with prefix search.** A geohash like `dr5ru` encodes lat/lon hierarchically; `WHERE geohash LIKE 'a%'` returns every cell beginning with `"a"` via a B-Tree prefix scan. Cheap and easy to explain.
- **Reverse index from grid bucket to object IDs.** Each point belongs to a bucket; the index maps `bucket_id → [object_ids]`.

A **QuadTree** is an in-memory data structure (Liu calls it out explicitly), not a database. Google S2 is the production-grade equivalent for spherical geometry but is rarely required at interview depth.

## 4. Choosing a Database — Category Reasoning

"I'll use NoSQL because it scales" is hand-wavy — every competitive database scales. **CAP** (pick two of Consistency, Availability, Partition tolerance) is necessary but not sufficient: MySQL with async-replicated followers isn't strictly "CP" once reads hit followers.

Liu's category map (most-to-least common in interviews):

| Category | Examples | When |
|---|---|---|
| Relational | MySQL, PostgreSQL | Default. ACID, joins, mature ecosystem. |
| Document | MongoDB, Couchbase | Schemaless, nested-object access patterns. |
| Columnar | Redshift, ClickHouse | Analytics, OLAP, range scans on a few columns. |
| Object store | S3, GCS | Blobs (videos, images, large files). |
| Wide-column | BigTable, HBase, Cassandra | Write-heavy, time-series, LSM-friendly access. |
| Reverse-index | Elasticsearch, Solr | Full-text search, aggregations over text. |
| In-memory KV | Redis, Memcached | Cache, session store, leaderboards. |
| Geo-spatial | PostGIS, MongoDB geo | Geographic queries beyond geohash. |
| Strong-consistency coordination | ZooKeeper, etcd | Consensus-backed primitives — fencing tokens, Snowflake machine IDs, leader election (Zab, Paxos, Raft). |

Xu's framing in Ch 1 is the same headline (SQL vs NoSQL) but lighter on categories.

## 5. Multiple Databases per Question

It's normal for one design to use two or three different stores:

- **YouTube** — blob store for video bytes, metadata DB for the video record, KV/cache for hot metadata.
- **Google Drive** — relational metadata DB for ACID file/version state, S3-style blob store for block content.
- **Chat** — wide-column (Cassandra/HBase) for message history, KV for presence, relational for user accounts.

Stating which store handles which entity, and why, is a stronger signal than picking one global database.

## Sources

- [Liu Ch 5.03: Schema, Indexing, Databases](software/system-design-interview/books/system-design-interview-fundamentals/ch05_03_schema_indexing_databases.md)
- [Xu Ch 1: Scale From Zero to Millions of Users](software/system-design-interview/books/system-design-interview-insiders-guide/ch01_scale_zero_to_millions.md) (SQL vs NoSQL section)
- [Xu Ch 6: Design a Key-Value Store](software/system-design-interview/books/system-design-interview-insiders-guide/ch06_design_a_key_value_store.md) (CAP, partitioning, replication on a KV)
