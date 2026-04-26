# Concurrency & Transactions

> Liu's chapter is the deep reference (single-thread vs micro-batch vs sharded-serial, pessimistic vs optimistic locking, write skew, distributed transactions). Xu Vol 1 doesn't cover concurrency as its own topic but applies the patterns inside specific case studies (rate limiter Lua scripts, news feed counters). Xu Vol 2 leans on the patterns heavily — TC/C and Saga in [Digital Wallet](case-studies/digital-wallet.md), idempotency keys in [Hotel Reservation](case-studies/hotel-reservation.md) and [Payment System](case-studies/payment-system.md), event sourcing in wallet/payment/[Stock Exchange](case-studies/stock-exchange.md), exactly-once-via-offset in [Ad-Click Aggregation](case-studies/ad-click-aggregation.md). Concurrency is one of the strongest interview signals because most candidates avoid it.

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
  - [6.5. Try-Confirm/Cancel (TC/C)](#65-try-confirmcancel-tcc)
  - [6.6. Saga](#66-saga)
  - [6.7. Event Sourcing + CQRS](#67-event-sourcing--cqrs)
- [7. Idempotency Keys as Primary Keys](#7-idempotency-keys-as-primary-keys)
- [8. Double-Entry Ledger](#8-double-entry-ledger)
- [9. Exactly-Once via Offset Transactions](#9-exactly-once-via-offset-transactions)
- [10. Reframing the Product](#10-reframing-the-product)
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

### 6.5. Try-Confirm/Cancel (TC/C)

A 2PC alternative that's database-agnostic — the "undo" lives in application code, not the DB. Two **independent** local transactions per participant: phase 1 *Try* reserves resources, phase 2 *Confirm* finalizes or *Cancel* reverses via business-logic compensation.

For a transfer `A → $1 → C`, the only correct Try-phase choice is `Try: A=-$1, C=NOP`; `Confirm: A=NOP, C=+$1`; `Cancel: A=+$1, C=NOP`. Crediting C in Try risks somebody draining C before Cancel can reclaim the funds; touching both accounts in Try creates concurrency complications.

**Unbalanced state is expected.** At the end of Try, $1 is missing — debited from A, not yet credited to C. TC/C exposes the intermediate state; that's fine as long as the full sequence completes.

A **phase status table** (typically co-located with the debit account's DB) records `(transaction_id, try_status_per_db, second_phase_name, second_phase_status, out_of_order_flag)` so TC/C can resume after a coordinator restart. Out-of-order execution — a Cancel arriving before its Try — is handled by leaving the out-of-order flag; a later-arriving Try checks the flag and fails immediately.

### 6.6. Saga

The de-facto standard for cross-microservice transactions. Order all operations in a linear sequence of independent local transactions; on failure at step `k`, run **compensating transactions** for steps `k-1, k-2, …, 1` to roll back.

Two coordination styles:

- **Choreography** — services subscribe to each other's events; fully decentralized; hard to reason about as the service count grows.
- **Orchestration** — single coordinator drives the order; preferred for [digital wallet](case-studies/digital-wallet.md) and [payment system](case-studies/payment-system.md).

**TC/C vs Saga:**

| Dimension | TC/C | Saga |
|---|---|---|
| Compensating action | In Cancel phase | In rollback phase |
| Operation execution order | Any | Linear |
| Parallel execution | Yes | No |
| Partial inconsistent state visible | Yes | Yes |

Pick Saga if you're following microservice trends or have few services with no strict latency need. Pick TC/C if latency is tight and parallelism wins.

### 6.7. Event Sourcing + CQRS

Persist the immutable sequence of state-changing facts; derive state by replay. Four core terms:

- **Command** — intent from outside ("transfer $1 A→C").
- **Event** — validated past-tense fact ("transferred $1 A→C").
- **State** — current materialized view (`account → balance`).
- **State Machine** — validates Commands → emits Events; applies Events → mutates State. Must be **deterministic** (no random numbers, no external I/O during apply); replay must yield identical State.

**CQRS (Command-Query Responsibility Segregation)** publishes Events, not State. One writer State Machine and many read-only State Machines build different views (current balance, hourly window for double-charge investigation, audit trail) — eventually consistent.

This is the **only** pattern that satisfies *reproducibility*: replay the Event log from start (or from a snapshot) to reconstruct any historical balance, verify correctness after a code change, or test new code by re-running events. State-only stores cannot answer "why is this balance what it is."

The generic mechanism is shared across [Digital Wallet](case-studies/digital-wallet.md), [Payment System](case-studies/payment-system.md), and [Stock Exchange](case-studies/stock-exchange.md); each case study covers its own workload-specific motivation (mmap+Raft for wallet, sequencer + deterministic matching engine for exchange, append-only payment-state log for retry/resume in payments).

## 7. Idempotency Keys as Primary Keys

The universal double-write defense. Client generates a UUID (cart ID, `reservation_id`, message offset) and sends it with the request — typically as `<idempotency-key: key_value>` in an HTTP header (Stripe, PayPal). Server uses the key as the **primary key** of the relevant table; the unique constraint rejects duplicate inserts and the system returns the original status.

Decomposition: **exactly-once = at-least-once (via retry) + at-most-once (via idempotency)**.

Defends against:

- User double-clicks "pay" or "book."
- Network retry after the server succeeded but the response was lost in transit.
- Concurrent in-flight requests with the same key — only one is processed; the others receive `429 Too Many Requests`.
- Crash-redo across reservation, payment, and ad pipelines.

Pick a natural pre-submit identifier when one exists: the **shopping-cart ID** in [Payment System](case-studies/payment-system.md), the **`reservation_id`** in [Hotel Reservation](case-studies/hotel-reservation.md), the **partition offset** in [Ad-Click Aggregation](case-studies/ad-click-aggregation.md). When the third party doesn't offer idempotency, wrap your own — payment systems map a UUID nonce to a PSP token and check the token before re-charging.

## 8. Double-Entry Ledger

Every transfer posts to two accounts with equal magnitude — debit one, credit the other — so the sum across all entries is exactly zero. "One cent lost means someone else gains a cent." End-to-end traceability falls out for free; auditors can reconstruct any account's history by filtering the ledger.

Two practical conventions money math depends on:

- **Amount as string, not double.** Doubles cause precision/serialization rounding errors. Values can be huge (Japan's GDP ≈ 5 × 10¹⁴ yen) or tiny (1 satoshi = 10⁻⁸ BTC). Parse to numeric only at the display/calculation boundary.
- **Running balance derives from the ledger.** Never modify a balance directly; insert ledger entries and recompute. Combined with [event sourcing](#67-event-sourcing--cqrs), this gives both reproducibility and audit.

Used in [Payment System](case-studies/payment-system.md). Square's engineering blog is the canonical industry reference.

## 9. Exactly-Once via Offset Transactions

The naive recipe — process events, write the offset back to durable storage, ack downstream — has two failure windows:

- **Save offset *before* downstream ack** → crash after the save means the un-acked events are skipped forever.
- **Save offset *after* downstream ack** → crash before the save means the events get redelivered on restart.

The fix: **wrap the offset commit and the downstream ack in a single distributed transaction**. Either both succeed or both roll back. On partial failure, the consumer restarts from the last committed offset and replays whatever wasn't acked.

This is how [Ad-Click Aggregation](case-studies/ad-click-aggregation.md) gets billing-grade exactly-once semantics on top of Kafka. End-of-day reconciliation against the raw event log catches very late events that watermarks missed.

## 10. Reframing the Product

When concurrency gets hairy, ask whether the product requirement can change. Liu's ridesharing example: instead of fanning a ride request to three drivers and resolving the acceptance race, redesign so the backend auto-assigns one driver. The user gets the same UX — they don't pick the driver in either case — and the technical complexity collapses.

Materializing 30-minute booking blocks (Section 5) is the same move. Concurrency-as-a-product-decision is a senior-level signal.

## Sources

- [Liu Ch 5.05: Concurrency and Transactions](software/system-design-interview/books/system-design-interview-fundamentals/ch05_05_concurrency_and_transactions.md)
- [Liu Ch 5.16: Distributed Transaction](software/system-design-interview/books/system-design-interview-fundamentals/ch05_16_distributed_transaction.md)
- [Vol 2 Ch 6: Aggregate Ad Click Events](software/system-design-interview/books/system-design-interview-vol2/ch06_aggregate_ad_click_events.md) — exactly-once via offset transactions.
- [Vol 2 Ch 7: Hotel Reservation System](software/system-design-interview/books/system-design-interview-vol2/ch07_hotel_reservation_system.md) — idempotency key as primary key, optimistic locking.
- [Vol 2 Ch 11: Payment System](software/system-design-interview/books/system-design-interview-vol2/ch11_payment_system.md) — idempotency keys, double-entry ledger, Saga.
- [Vol 2 Ch 12: Digital Wallet](software/system-design-interview/books/system-design-interview-vol2/ch12_digital_wallet.md) — TC/C, Saga, Event Sourcing + CQRS.
- [Vol 2 Ch 13: Stock Exchange](software/system-design-interview/books/system-design-interview-vol2/ch13_stock_exchange.md) — Event Sourcing for crash recovery.
