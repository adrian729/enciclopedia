# Ch 5.03: Schema, Indexing, and Databases

## Table of Contents

- [1. Schema Design](#1-schema-design)
- [2. Normalization vs Denormalization](#2-normalization-vs-denormalization)
- [3. What an Index Is](#3-what-an-index-is)
- [4. Primary vs Secondary Index](#4-primary-vs-secondary-index)
- [5. Common Index Use Cases](#5-common-index-use-cases)
- [6. Composite Index](#6-composite-index)
- [7. Geo Index](#7-geo-index)
- [8. Choosing a Database](#8-choosing-a-database)
- [9. Database Type Comparison](#9-database-type-comparison)

## 1. Schema Design

- **Start with a logical schema, defer the database choice** — clarify entities and relationships first; committing to MySQL vs NoSQL requires knowing access/storage patterns that aren't clear yet
- **Every table has a primary key** — usually a system-generated ID; UUID vs integer vs string rarely matters for the interview unless the question is about ID design (e.g., TinyURL)
- **Foreign keys express relationships** — `folder.user_id (FK)`, `file.folder_id (FK)` for a one-to-many structure
- **Many-to-many needs a join table** — for file labels, a `file_label` table with `(id, file_id FK, label_id FK)` lets you answer both "labels on a file" and "files with a label"
- **Key-value schema as an alternative** — `file_id → [label_id]` answers "labels on file" efficiently but makes "files with label" awkward; keep relational-like abstract schemas by default
- **Walk the schema against the queries** — before moving on, verify the schema can answer the API's read and write requirements

## 2. Normalization vs Denormalization

- **Generally not worth debating in an interview** — it's a generic trade-off; bring it up only when read throughput is the specific bottleneck being discussed
- **Default to normalized** — clean logical separation with well-defined entities; denormalize later as a deep-dive optimization

## 3. What an Index Is

- **Definition** — a sorted auxiliary structure that turns `O(N)` full-table scans into `O(log N)` binary searches
- **Internal implementations** — B-Tree or LSM with **Sorted Strings Table (SST)**; the key property is ordered, on-disk, log-time lookup
- **Performance still degrades with size** — `O(log N)` grows, just far slower than `O(N)`

> **Reminder** — database indexes are not hashmaps. Hashmaps are in-memory; on-disk indexes are sorted structures.

## 4. Primary vs Secondary Index

| Type | Structure | Effect |
|---|---|---|
| **Primary (clustered)** | Sorts the main table on disk by the primary key | Lookup by primary key is fast; inserts may require reshuffling if keys aren't sequential. The clustered index need not be the primary key |
| **Secondary** | Separate sorted table pointing back into the main table | Extra index to optimize non-primary lookups; adds write cost but worth it when read-to-write ratio is high |

## 5. Common Index Use Cases

- **Key / attribute lookup** — `cars(car_id PK, color)`: lookup by `color` is a scan; add an index on `color` to make it a log-time search
- **Range lookup** — `posts(post_id PK, created_time)`: "20 most recent posts" requires sorting without an index; with an index on `created_time`, fetch the top 20 directly from the sorted structure
- **Prefix search** — an index is sorted, so "all strings starting with X" is efficient. Applications: type-ahead (search terms sorted by score), **geohash** (a 9-character geohash; `"a*"` prefix returns all geohashes beginning with `"a"`)
- **Trade-off for type-ahead** — disk-index prefix + sort may be too slow for p95 10ms latency; surface it as an option in deep dive

## 6. Composite Index

- **Multi-column index** — a single index on `(col_a, col_b)`; the order of columns matters
- **Example: driver table** `(driver_id, status, location)`:

| Composite key | Efficient queries | Inefficient queries |
|---|---|---|
| `(status, location)` | "all busy drivers", "all busy drivers in Chicago" | "all drivers in New York" (location sorted only within status) |
| `(location, status)` | "all drivers in Chicago", "all busy drivers in New York" | "all busy drivers" (status sorted only within location) |

- **Applies to NoSQL row keys too** — NoSQL concatenates keys into one row key; the same ordering logic governs what's efficient

## 7. Geo Index

- **Real options are complicated** — R-Tree, kd-tree, 2dsphere, Google S2; interviewers rarely want deep internals
- **Two interview-grade simplifications**:
  - **Geohash + prefix search** — each geohash character narrows the region; prefix search retrieves nested regions
  - **Reverse index `location_id → [object]`** — floor `(longitude, latitude)` into grid buckets (e.g., `(1.11, 2.25)` → `(1, 2)`); no need to store separate range mappings

## 8. Choosing a Database

- **Hand-wavy answers to avoid** — "I'll use NoSQL because it scales", "I'll use Cassandra because it scales at our company". Every competitive database scales; the reason has to be more specific
- **CAP theorem is necessary but not sufficient** — C (all nodes see same data), A (serves traffic), P (survives partitions); you pick two. But **MySQL with async-replicated followers isn't strictly "CP"** once you allow reads from the follower. Use CAP as framing, not as the whole answer

> **Reminder** — CAP theorem: choose 2 of 3. **AC** (no partition, single machine). **CP** (on network split, fail in favor of consistency). **AP** (on network split, continue in favor of availability).

- **Prefer category-level reasoning** — "this workload is transactional with non-trivial joins, so RDBMS" beats "MySQL because it's popular"
- **Multiple databases per question is normal** — e.g., YouTube needs a **blob store** for video bytes and a **metadata store** for the video record
- **Expect follow-up on internals** — if you claim "Cassandra is AP", be ready to explain why; if you claim "HBase suits chat", be ready to defend against MongoDB or MySQL

## 9. Database Type Comparison

| Type | Strengths | Typical use |
|---|---|---|
| **Relational** — MySQL, Postgres | Transactions, joins/unions, ad-hoc indexes, update-in-place; B-Tree indexing favors reads | Default choice unless something points elsewhere; transactional workloads with non-trivial SQL |
| **Document Store** — MongoDB, Amazon DocumentDB | Unstructured data in JSON/XML-like documents; no strict schema | Product catalogs with heterogeneous attributes; otherwise prefer relational when in doubt |
| **Columnar Store** — InfluxDB, Pinot | Data laid out by column; OLAP-friendly; compresses well; append-heavy with batch deletes | Analytics dashboards, time-series metrics |
| **Object Store** — Amazon S3 | Immutable blobs; avoids bloating OLTP tables | Photos/videos (Instagram), log dumps, file storage (PDF/CSV pipelines) |
| **Wide Column Store** — Big Table, HBase, Cassandra | High write throughput; reads fast by row key; LSM indexing; column families stored contiguously | Chat history (Facebook Chat), metrics collection |
| **Reverse Index Store** — Elastic Search, Lucene | Key = term token, value = posting list; supports AND/OR across postings | Search problems |
| **In-Memory Store** — Redis, Memcache | No disk access; trades durability for speed | Driver locations for ride-matching; caching (see caching chapter) |
| **Geo-Spatial Databases** — Google S2, MongoDB Geo Queries | Radius/polygon/shape queries over coordinates | Yelp, Find My Friend |
| **ZooKeeper** — Chubby, ZooKeeper | Strong consistency (linearizable) via consensus; fault-tolerant | Shard manager, configuration manager, leader election |

> **Reminder** — a Quadtree is an in-memory data structure, not a database.

- **Don't argue ACID as a relational-only property** — transactions on a row or document are possible in NoSQL, and NoSQL provides durability via replication
- **Wide column replication varies** — HBase is leader-follower; Cassandra is leaderless and so must deal with conflicting writes at lower consistency; discuss conflict resolution if you pick Cassandra
- **Consensus protocols** (Zab, Paxos, Raft) power ZooKeeper-class systems; interviewers rarely go into the proofs
