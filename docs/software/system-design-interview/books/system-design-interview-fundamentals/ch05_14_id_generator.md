# Ch 5.14: ID Generator

## Table of Contents

- [1. Why ID Generation Matters](#1-why-id-generation-matters)
- [2. Strategy Comparison](#2-strategy-comparison)
- [3. UUID](#3-uuid)
- [4. Auto Increment](#4-auto-increment)
- [5. Auto Increment on Multiple Machines](#5-auto-increment-on-multiple-machines)
- [6. Strongly Consistent and Fault Tolerant](#6-strongly-consistent-and-fault-tolerant)
- [7. Distributed Roughly Sorted ID (Snowflake)](#7-distributed-roughly-sorted-id-snowflake)
- [8. Offline Generation](#8-offline-generation)
- [9. Custom ID](#9-custom-id)

## 1. Why ID Generation Matters

- **Sometimes a system design question in itself** — otherwise, ID generators are tools you pick for the use case
- **Match generator to requirement** — not every system needs ordered, unique, globally-coordinated 64-bit IDs; use the right generator for the correct use case

## 2. Strategy Comparison

| Strategy | Ordered? | Coordination | Size | Throughput | When to use |
|---|---|---|---|---|---|
| **UUID** | No | None (independent) | 128-bit | Very high | Any time order/size aren't issues |
| **Auto Increment (single DB)** | Yes | Single DB | Small | Limited by one machine | Small-scale apps |
| **Auto Increment (multi DB)** | Not globally ordered | Configured (e.g., odd/even) | Small | Higher than single | Medium-scale, quick scale-up |
| **Strongly Consistent (ZooKeeper)** | Strictly | Leader-follower quorum | 64-bit | Low (quorum cost) | Fencing tokens, Snowflake machine IDs |
| **Snowflake (roughly sorted)** | Roughly | None (ZooKeeper only for machine ID) | 64-bit | Very high | Tweets, Discord messages |
| **Offline generation** | Custom | Pre-generated pool | Any | Low-latency lookup | TinyURL, short unique codes |
| **Custom** | Depends | Depends | Depends | Depends | When requirements are loose |

## 3. UUID

- **UUID v1** — uses MAC address + timestamp for effective uniqueness
- **Pros** — any server generates independently with no coordination; effectively unique (collision chance is negligible)
- **Cons** — unordered; 128 bits may be too large for some storage/index use cases

## 4. Auto Increment

- **Mechanism** — databases like MySQL assign the next sequential integer on insert
- **Pros** — guaranteed ordering and uniqueness; simple (just use the database)
- **Cons** — not horizontally scalable (single instance); not fault-tolerant (single point of failure)
- **Use** — small-scale applications

## 5. Auto Increment on Multiple Machines

- **Mechanism** — partition the ID space across machines; canonical example is Flickr using one server for odd numbers and another for even
- **Pros** — simple way to multiply throughput
- **Cons** — inflexible to reconfigure; adding a third machine means re-partitioning everything into multiples of 3

## 6. Strongly Consistent and Fault Tolerant

- **Mechanism** — linearizable systems like **ZooKeeper** emit monotonically increasing 64-bit integers via `zxid`
- **Pros** — ordered, unique, fault-tolerant, 64-bit
- **Cons** — leader-follower quorum caps throughput; ZooKeeper cluster maintenance adds complexity
- **Use** — fencing tokens for distributed locks; assigning Snowflake machine IDs at boot

## 7. Distributed Roughly Sorted ID (Snowflake)

- **Source** — originally published by Twitter
- **Layout (64 bits)**:

| Segment | Bits | Source |
|---|---|---|
| Timestamp | — | Millisecond precision on the generating host |
| Machine ID | 10 | Assigned by ZooKeeper on boot; 1024 machines max |
| Sequence | 12 | Incremented per-ID on the host; 4096 IDs per millisecond per machine |

- **Pros** — roughly ordered and unique; high throughput; no per-ID coordination; 64-bit; horizontally scalable by adding machines
- **Cons** — not perfectly ordered across machines (ties aren't resolvable); library complexity required on every host
- **Use** — Twitter tweet IDs; Discord message-table cluster index

## 8. Offline Generation

- **Mechanism** — pre-generate a pool of IDs offline, hand them out at request time
- **Pros** — low request-time latency; supports unusual formats (short strings, custom sequences)
- **Cons** — need to forecast demand — run out and you need a fallback; over-generate and you waste storage
- **Use** — TinyURL's shortened URL codes, where retries on duplicate generation would be costly

## 9. Custom ID

- **Not every ID needs to be ordered, unique, or fixed-size** — it can be a string, integer, bigint, timestamp, or hash
- **Clarify the requirement** — ask the interviewer what properties the ID actually needs. Snowflake's segment layout can also be reconfigured for the use case
