# Digital Wallet

> Vol 2 only — neither Liu nor Xu Vol 1 covers wallets. The chapter is structured as a **design evolution**: each step fixes the prior one's limitation. **In-memory sharding** is fast but two updates aren't atomic; **distributed transactions** add atomicity but no audit trail; **Event Sourcing + CQRS** finally satisfies **reproducibility** so historical balances can be reconstructed by replaying data from the beginning. The 1M TPS goal is then met with mmap-backed local files, Raft replication, and per-account sharding.
>
> TC/C, Saga, and the generic ES+CQRS mechanism live in [Concurrency & Transactions §6.5–6.7](fundamentals/concurrency-and-transactions.md#65-try-confirmcancel-tcc); this page covers the wallet-specific motivation and optimization.

## Table of Contents

- [1. Requirements](#1-requirements)
- [2. Design Evolution Overview](#2-design-evolution-overview)
- [3. In-Memory Sharding](#3-in-memory-sharding)
- [4. Distributed Transactions](#4-distributed-transactions)
- [5. Event Sourcing for Reproducibility](#5-event-sourcing-for-reproducibility)
- [6. High-Performance Event Sourcing](#6-high-performance-event-sourcing)
- [7. Reliability with Raft](#7-reliability-with-raft)
- [8. Distributed Event Sourcing](#8-distributed-event-sourcing)
- [Sources](#sources)

## 1. Requirements

Backend that lets users store money in a per-user balance and transfer it directly to another wallet on the same platform (e.g., PayPal), avoiding bank-to-bank fees and latency.

- Functional scope: cross-wallet balance transfer between two wallets only; no FX, no other features.
- Non-functional: **1M TPS**, **99.99% availability**, transactional guarantees, and **reproducibility** so historical balances can be reconstructed by replaying data from the beginning.

**Why reproducibility over reconciliation alone** — comparing internal records to bank statements only flags discrepancies; it cannot explain *how* a difference was generated. Replay can.

**Node-count math** — each transfer is two operations (debit + credit), so 1M TPS needs ~2M per-node TPS. At 1,000 TPS/node → 2,000 nodes; at 10,000 TPS/node → 200 nodes. Design goal: push per-node TPS up to lower hardware cost.

**Workload-specific ES motivation:** unlike [Payment System](case-studies/payment-system.md)'s use of event sourcing as a retry-resume log, the wallet uses **full ES + CQRS** to satisfy auditor questions like "balance at any time?", "historical correctness?", "logic correctness after a code change?" — replay is the answer.

**Amount as string, not double** — same rationale as [Payment System §4](case-studies/payment-system.md#4-data-model-and-ledger).

## 2. Design Evolution Overview

| Step | Design | Fixed limitation | New limitation |
|---|---|---|---|
| 1 | In-memory sharding (Redis) | Speed | No atomicity across nodes |
| 2 | Distributed transactions on relational DBs (2PC, TC/C, Saga) | Atomicity | No audit trail / reproducibility |
| 3 | Event Sourcing + CQRS | Reproducibility | Single-node throughput |
| 4 | Local files + mmap + Raft + sharding | 1M TPS | — |

## 3. In-Memory Sharding

Data model: `<user, balance>` map. One Redis cluster shards user accounts via `accountID.hashCode() % partitionNumber`. Sharding metadata (partition count, node addresses) lives in **ZooKeeper** as highly-available config storage.

A stateless wallet service receives a transfer command, validates it, and updates two account balances on (typically) two different Redis nodes.

**Failure mode** — if the wallet service crashes after the debit but before the credit, the transfer is incomplete. Two updates aren't atomic, so the design fails the correctness requirement.

## 4. Distributed Transactions

To make multi-node updates atomic, each shard must be a transactional database, not just a key-value store. Two flavors of distributed transactions:

- **Low-level** (database-driven, e.g., 2PC via X/Open XA).
- **High-level** (application-driven via compensation, e.g., TC/C, Saga).

**2PC drawbacks** — long-held locks kill performance; the coordinator is a single point of failure; requires DB-level support for the prepare protocol.

**TC/C wins on parallelism**; **Saga wins on microservices fit**. Generic mechanics in [Concurrency & Transactions §6.5–6.6](fundamentals/concurrency-and-transactions.md#65-try-confirmcancel-tcc).

**Wallet-specific TC/C example** — for `A → $1 → C`, the only correct Try-phase choice is `Try: A=-$1, C=NOP`; `Confirm: A=NOP, C=+$1`; `Cancel: A=+$1, C=NOP`. Crediting C in Try risks somebody draining C before Cancel can reclaim the funds.

**Phase status table** — co-located with the debit account's DB, recording per-transaction Try-phase status, second-phase name (Confirm/Cancel), second-phase status, out-of-order flag. Survives wallet-service restarts so TC/C can resume.

**Out-of-order execution** — a node may receive a Cancel before its Try due to network reordering. The Cancel leaves an out-of-order flag; a later-arriving Try checks the flag and fails immediately.

**Saga choice** — orchestration over choreography for the wallet (single coordinator, easier to reason about than decentralized event chains).

## 5. Event Sourcing for Reproducibility

State-only stores can't answer the auditor questions above. Event Sourcing — persist the immutable sequence of state-changing facts; derive state by replay — is the only pattern that does.

Four core terms (full treatment in [Concurrency & Transactions §6.7](fundamentals/concurrency-and-transactions.md#67-event-sourcing--cqrs)):

- **Command** — intent from outside, e.g., "transfer $1 A→C."
- **Event** — validated past-tense fact, e.g., "transferred $1 A→C."
- **State** — current map of `account → balance`.
- **State Machine** — validates Commands → emits Events; applies Events → mutates State. **Must be deterministic** — no random numbers, no external I/O during apply; replay must yield identical State.

**Two FIFO queues** — Commands and Events both go through ordered queues (Kafka is a typical choice); ordering is essential.

**CQRS** — instead of publishing State, publish all Events; one writer State Machine and many read-only State Machines build different views (current balance, hourly window for double-charge investigation, audit trail). Read views are eventually consistent.

## 6. High-Performance Event Sourcing

Hitting 1M TPS forces three optimizations:

- **Local file-based Command/Event store** — write append-only files on local disk instead of remote Kafka. Sequential disk writes are very fast — per ACM Queue, can outpace random memory access in some cases.
- **mmap** — maps the append-only file into memory so the OS caches recent content; gives in-memory speed for reads and disk durability for writes simultaneously.
- **File-based State** — replace the remote relational DB with **SQLite** (file-based RDBMS) or **RocksDB** (LSM-tree key-value store optimized for writes with caching for reads).
- **Snapshot** — periodic immutable dump of current State to a file (often stored in HDFS); on recovery, the State Machine loads the latest snapshot and replays only events after it. Finance teams typically demand a 00:00 snapshot for daily verification.

**Tradeoff** — local files make a node stateful and a single point of failure; addressed by replication next.

## 7. Reliability with Raft

**Only Events need strong durability.** State and snapshots can be regenerated from Events. Commands can't be relied on (Event generation may be non-deterministic with I/O), so Events are the single source of truth that must never be lost.

**Raft consensus** — replicates the append-only Event list across nodes with no data loss and identical ordering; tolerates failures as long as a majority is up (3-of-5, 2-of-3). See [CAP, Consensus & Conflict Resolution](fundamentals/cap-consensus-and-conflict-resolution.md).

**Roles** — Leader (receives Commands, replicates), Follower, Candidate (during election).

**Failure handling** — leader crash triggers automatic re-election from remaining healthy nodes; client retries unacknowledged Commands against the new leader. Follower crash is handled by Raft's indefinite retry until restart or replacement.

**Effect on Event Sourcing** — leader takes Commands → Events → appends locally → Raft replicates to followers → all nodes (leader + followers) apply Events to local State, guaranteeing identical State across the cluster.

## 8. Distributed Event Sourcing

Two remaining limitations of a single Raft group:

1. CQRS request/response is not real-time (clients pull).
2. A single Raft group can't sustain 1M TPS.

**Pull → push** — adding a reverse proxy between client and Event Sourcing nodes lets the read-only State Machine push execution status back to the proxy as soon as it sees the Event, giving clients a real-time feel.

**Sharding by hash** — partition data by hash of key (e.g., mod 2 for two partitions); each partition is its own Raft group; cross-partition transfers reuse TC/C or Saga on top.

**End-to-end Saga happy path:**

1. Coordinator records the transfer in the Phase Status Table.
2. Sends `A-$1` to Partition 1's Raft leader → command list → validated → Event → Raft sync → State updated → CQRS read path pushes success back.
3. Coordinator marks Partition 1 done.
4. Sends `C+$1` to Partition 2; same flow.
5. Coordinator marks transaction complete.

**Final architecture** combines all layers — sharded Raft groups for scale, Event Sourcing for reproducibility, mmap-backed local files for low latency, Saga/TC/C for cross-partition atomicity, CQRS push for real-time responses.

## Sources

- [Vol 2 Ch 12: Digital Wallet](software/system-design-interview/books/system-design-interview-vol2/ch12_digital_wallet.md)
