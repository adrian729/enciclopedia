# ID Generation

> Both books cover this topic in roughly equal depth. Xu's Ch 7 walks the canonical alternatives and lands on Twitter Snowflake; Liu's Ch 5.14 adds offline pre-generation (TinyURL short codes) and ZooKeeper-style linearizable generators. The two views are complementary.

## Table of Contents

- [1. What an ID Needs](#1-what-an-id-needs)
- [2. The Candidates](#2-the-candidates)
  - [2.1. Single-Database Auto-Increment](#21-single-database-auto-increment)
  - [2.2. Multi-Master Auto-Increment](#22-multi-master-auto-increment)
  - [2.3. UUIDs](#23-uuids)
  - [2.4. Centralized Ticket Server](#24-centralized-ticket-server)
  - [2.5. ZooKeeper-Style Linearizable Generator](#25-zookeeper-style-linearizable-generator)
  - [2.6. Twitter Snowflake](#26-twitter-snowflake)
  - [2.7. Offline Pre-Generated Pool](#27-offline-pre-generated-pool)
- [3. Snowflake in Detail](#3-snowflake-in-detail)
- [4. Decision Guide](#4-decision-guide)
- [Sources](#sources)

## 1. What an ID Needs

Not every system needs the same kind of ID. The questions to ask:

- **Globally unique?** (always)
- **Time-sortable?** (chat messages, news feed posts — yes; URL shortener short codes — no)
- **Fixed bit width?** (Snowflake forces 64-bit; UUIDs are 128-bit)
- **Coordination-free?** (UUIDs and Snowflake yes; auto-increment and ticket server no)
- **High-throughput?** (millions per second across the cluster)

## 2. The Candidates

### 2.1. Single-Database Auto-Increment

Simple, but neither scalable nor fault-tolerant. The DB is a SPOF for ID issuance.

### 2.2. Multi-Master Auto-Increment

Each DB increments by `k` with offset `i` (DB1 emits 1, 4, 7, ...; DB2 emits 2, 5, 8, ...). Multiplies throughput but doesn't scale across data centers and is inflexible — adding a new DB requires re-keying.

### 2.3. UUIDs

128-bit identifiers, coordination-free, effectively unique. Drawbacks:

- 128 bits doesn't fit in 64-bit columns and indexes.
- **Not time-sortable** — successive UUIDs are unrelated.

Fine for opaque tokens, less good for primary keys where ordering matters.

### 2.4. Centralized Ticket Server

A dedicated service hands out monotonic 64-bit integers (Flickr's design). Numeric, ordered, but a SPOF — when the ticket server is down, no one gets new IDs.

### 2.5. ZooKeeper-Style Linearizable Generator

Emits monotonic 64-bit integers via consensus (e.g., ZooKeeper's `zxid`). Used for **fencing tokens** (proving "I am the latest holder of this lock") and as the source of **machine IDs** for Snowflake.

### 2.6. Twitter Snowflake

64-bit ID divided into:

| Bits | Field |
|---|---|
| 1 | Sign bit (always 0) |
| 41 | Timestamp in milliseconds since a custom epoch (~69 years of runway) |
| 10 | Machine ID (5 bits datacenter + 5 bits machine = 1024 machines max, often assigned by ZooKeeper) |
| 12 | Sequence number (4096 IDs per millisecond per machine) |

Putting timestamp first makes IDs **sortable by time**; the machine and sequence bits break ties uniquely. Roughly ordered, unique, high-throughput, horizontally scalable. Used in: Twitter tweet IDs, Discord message-table cluster indexes, and most modern systems that need a unique sortable key.

Liu's note: 1024 machines is a lot but not infinite — ZooKeeper hands out machine IDs and reclaims them when nodes die, so the pool isn't permanently consumed.

### 2.7. Offline Pre-Generated Pool

Pre-compute a pool of unusual-format IDs offline; consumers pull from the pool. **TinyURL's short codes** work this way — the unique-but-short-string format isn't naturally produced by Snowflake, so a generator pre-computes a large pool.

## 3. Snowflake in Detail

Why each field is the size it is:

- **41 bits of millisecond timestamp** = 2⁴¹ ms ≈ 69 years. Pick an epoch in the recent past so the high bits aren't wasted on years that already happened.
- **10 bits of machine ID** = 1024 distinct generators. With one or two generators per service in a fleet, this is plenty.
- **12 bits of sequence** = 4096 unique IDs per millisecond per machine. Total throughput per machine = ~4M IDs/second.

Cluster throughput = 1024 × 4M = ~4 billion IDs/second, which is more than any current real-world system needs. The design has decade-plus headroom.

## 4. Decision Guide

| Need | Pick |
|---|---|
| Opaque token, no ordering, coordination-free | UUID |
| Time-sortable, 64-bit, high-throughput, distributed | Snowflake |
| Sortable from a single source, low scale | Auto-increment |
| Fencing token / lock leadership | ZooKeeper sequence |
| Custom format (short URL codes) | Offline pre-generated pool |

Snowflake is the modern default for any system that needs **unique, time-sortable, 64-bit IDs across distributed nodes**. Both URL shortener (via base-62 conversion of a Snowflake ID — see [URL Shortener](case-studies/url-shortener.md)) and chat message ordering use it.

## Sources

- [Liu Ch 5.14: ID Generator](software/system-design-interview/books/system-design-interview-fundamentals/ch05_14_id_generator.md)
- [Xu Ch 7: Design a Unique ID Generator](software/system-design-interview/books/system-design-interview-insiders-guide/ch07_design_a_unique_id_generator.md)
