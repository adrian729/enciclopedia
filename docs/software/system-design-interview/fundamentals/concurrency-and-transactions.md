# Concurrency & Transactions

> Liu's chapter is the deep reference (single-thread vs micro-batch vs sharded-serial, pessimistic vs optimistic locking, write skew, distributed transactions). Xu doesn't cover concurrency as its own topic but applies the patterns inside specific case studies (rate limiter Lua scripts, news feed counters). Concurrency is one of the strongest interview signals because most candidates avoid it.

## Table of Contents

- [1. Why Concurrency Matters in the Interview](#1-why-concurrency-matters-in-the-interview)
- [2. Canonical Examples](#2-canonical-examples)
- [3. Serialization Strategies](#3-serialization-strategies)
- [4. Pessimistic vs Optimistic Locking](#4-pessimistic-vs-optimistic-locking)
- [5. Write Skew and Phantom Data](#5-write-skew-and-phantom-data)
- [6. Distributed Transactions](#6-distributed-transactions)
  - [6.1. Two-Phase Commit](#61-two-phase-commit)
  - [6.2. Blob + Metadata Pattern](#62-blob--metadata-pattern)
  - [6.3. Database + Queue Pattern](#63-database--queue-pattern)
  - [6.4. The Generic Frame](#64-the-generic-frame)
- [7. Reframing the Product](#7-reframing-the-product)
- [Sources](#sources)

## 1. Why Concurrency Matters in the Interview

Concurrency is a strong signal precisely because most candidates avoid it. Surfacing it proactively — "two threads can both read `x=1`, both increment, both persist `x=2`, so we lost an update" — is a Level-3 / Level-4 tell.

## 2. Canonical Examples

Recurring across designs:

- **Global counter** — two threads read `x=1`, both increment, both persist `x=2`. Lost update.
- **Ridesharing match** — two riders both get assigned the same driver if dispatch isn't serialized.
- **Ticket booking** — two customers buy the last seat.
- **Meeting-room scheduling** — two organizers reserve overlapping slots.

## 3. Serialization Strategies

Three options on a spectrum, from simplest to most scalable:

| Strategy | Throughput | Freshness | When to use |
|---|---|---|---|
| Single-thread | Low | Live | Low-QPS critical path; admin operations. |
| Single-thread micro-batch | Medium | ~1 batch interval stale | Aggregation, dispatch, top-K. Amortizes I/O. |
| Sharded serial | High | Live per shard | Independent partitions (per-driver, per-room, per-key). |

Liu's ridesharing case study uses sharded serial: each geographic dispatcher serializes per-region matches.

## 4. Pessimistic vs Optimistic Locking

**Pessimistic** locking acquires a lock before the transaction. Write locks block both readers and writers; read locks allow concurrent reads but block writers. Preferred when QPS is low and correctness is critical (banking).

**Optimistic** locking uses a monotonically increasing version number (an **eTag**) checked at commit time. Two readers at `v1` race; one commits to `v2`, the second's commit fails because the expected version doesn't match. The second retries. Avoids lock overhead, but **retry storms under contention** bubble up as poor UX.

Lock scope: database, table, row, in-memory data structure. The narrower the scope, the less blocking — but harder to reason about.

## 5. Write Skew and Phantom Data

The hard case is when the resource to lock *doesn't exist as a row*. Example: booking a continuous time range on a calendar — there's no row to lock for "9:00 to 10:30 on Tuesday" until you insert it. Two clients can both check "is the slot free?" (yes), both insert, and both succeed.

Mitigations:

- **Scope up** to a broader row that does exist (lock the whole calendar day).
- **Predicate locks** if the database supports them.
- **Materialize the data** — restrict bookings to fixed 30-minute blocks, so each block is a row that *can* be locked. This changes the product requirement.

## 6. Distributed Transactions

A distributed transaction touches more than one data source, and the complexity is what happens on partial commit.

### 6.1. Two-Phase Commit

Coordinator asks every participant to **prepare** (vote yes or no without committing). If all vote yes, coordinator sends **commit**; otherwise **abort**. Prevents inconsistency but the coordinator is a SPOF — a downed coordinator with participants in the prepared state leaves the system unavailable until it returns.

Used when correctness must be guaranteed end-to-end (money transfer between two banks).

### 6.2. Blob + Metadata Pattern

Common for systems that store a binary asset and a metadata record. Persist the blob first (producing a URL); then persist metadata pointing to it. A failed metadata write leaves an **unreferenced blob** that a background cleanup can reap.

Used in: photo upload, video upload (Xu Ch 14), [Cloud File Storage](case-studies/cloud-file-storage.md). It works because the user-visible state (metadata) is the only thing that needs to be transactional; orphan blobs are a background-cleanup problem, not a correctness problem.

### 6.3. Database + Queue Pattern

Insert a row and enqueue a message in one logical operation. Some databases offer transactional outboxes; otherwise, write the row first and let a reconciliation job catch any dropped enqueues. Acceptable when the failure rate is low and reconciliation is cheap.

### 6.4. The Generic Frame

Liu's abstraction for any A/B distributed transaction:

1. Call A then B.
2. Call B then A.
3. Both concurrently.
4. Both via a coordinator (2PC).
5. Both transactionally (if a single store covers both).

For each option, walk through what happens on partial failure. The right answer is whichever leaves the system in a state cleanup can fix.

## 7. Reframing the Product

When concurrency gets hairy, ask whether the product requirement can change. Liu's ridesharing example: instead of fanning a ride request to three drivers and resolving the acceptance race, redesign so the backend auto-assigns one driver. The user gets the same UX — they don't pick the driver in either case — and the technical complexity collapses.

Materializing 30-minute booking blocks (Section 5) is the same move. Concurrency-as-a-product-decision is a senior-level signal.

## Sources

- [Liu Ch 5.05: Concurrency and Transactions](software/system-design-interview/books/system-design-interview-fundamentals/ch05_05_concurrency_and_transactions.md)
- [Liu Ch 5.16: Distributed Transaction](software/system-design-interview/books/system-design-interview-fundamentals/ch05_16_distributed_transaction.md)
