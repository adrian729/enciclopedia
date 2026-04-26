# Ch 7: Design a Unique ID Generator in Distributed Systems

## Table of Contents

- [1. Problem and Requirements](#1-problem-and-requirements)
- [2. Why auto_increment Fails](#2-why-auto_increment-fails)
- [3. Candidate Approaches](#3-candidate-approaches)
- [4. Twitter Snowflake](#4-twitter-snowflake)
- [5. Snowflake Section Details](#5-snowflake-section-details)
- [6. Additional Considerations](#6-additional-considerations)

## 1. Problem and Requirements

- **Goal** — generate globally unique IDs in a distributed environment, since one DB server is too small and coordinating uniqueness across many DBs is hard
- **Clarified requirements** — IDs must be unique, numerical only, fit in 64 bits, ordered by date (later in the day > earlier same day, but not necessarily +1 increments), with throughput of 10,000+ IDs per second

## 2. Why auto_increment Fails

- **Single DB ceiling** — relational `auto_increment` works on one server but cannot be relied on across many databases without coordination delays
- **Distributed environment** — needs an approach that produces unique, time-sortable IDs without a global lock

## 3. Candidate Approaches

| Approach | How it works | Pros | Cons |
|---|---|---|---|
| **Multi-master replication** | Use DB `auto_increment` but step by `k` (number of DB servers) so each server emits a disjoint sequence | Reuses familiar DB feature | Hard to scale across data centers; IDs do not go up with time across servers; doesn't scale on add/remove |
| **UUID** | 128-bit number generated independently per web server; collision probability is ~50% only after 1B IDs/sec for 100 years | Simple, no coordination, scales with web servers | 128 bits exceeds 64-bit limit; not time-sorted; can be non-numeric |
| **Ticket server** | Centralized DB with `auto_increment` (Flickr's design) hands out IDs | Numeric IDs; easy for small/medium scale | Single point of failure; multiple ticket servers reintroduce sync challenges |
| **Twitter snowflake** | Divide a 64-bit ID into sections (timestamp + datacenter + machine + sequence) | Meets all requirements: 64-bit, numeric, time-sorted, scalable | More complex; depends on synchronized clocks |

## 4. Twitter Snowflake

- **Divide and conquer** — instead of generating an ID monolithically, partition 64 bits into sections that each carry distinct meaning
- **64-bit layout** — 1 sign bit, 41 bits timestamp, 5 bits datacenter ID, 5 bits machine ID, 12 bits sequence number
- **Why it satisfies the spec** — timestamp first means IDs are sortable by time; datacenter+machine bits ensure uniqueness across nodes; sequence covers same-millisecond bursts

## 5. Snowflake Section Details

- **Sign bit (1 bit)** — always 0; reserved for future use such as distinguishing signed vs unsigned numbers
- **Timestamp (41 bits)** — milliseconds since a custom epoch (Twitter default `1288834974657` = Nov 04, 2010, 01:42:54 UTC). Because timestamps grow with time, IDs are sortable by time
- **Timestamp lifespan** — `2^41 - 1` ms ≈ 69 years; using a custom epoch close to today maximizes runway. After 69 years a new epoch or migration is needed
- **Datacenter ID (5 bits)** — `2^5 = 32` datacenters; chosen at startup and effectively fixed (changes risk ID conflicts)
- **Machine ID (5 bits)** — `2^5 = 32` machines per datacenter; also fixed at startup
- **Sequence number (12 bits)** — `2^12 = 4096` combinations; reset to 0 every millisecond and incremented per ID generated within the same millisecond on the same machine. Caps a single machine at 4096 IDs/ms

## 6. Additional Considerations

- **Clock synchronization** — snowflake assumes generators share a clock; multi-core or multi-machine setups can drift. Network Time Protocol (NTP) is the standard mitigation, though out of scope here
- **Section length tuning** — fewer sequence bits with more timestamp bits suits low-concurrency, long-lived applications; the partition can be retuned for the workload
- **High availability** — an ID generator is mission-critical and must itself be highly available
