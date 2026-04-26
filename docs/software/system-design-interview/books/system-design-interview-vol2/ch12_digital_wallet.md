# Ch 12: Digital Wallet

## Table of Contents

- [1. Problem and Scope](#1-problem-and-scope)
- [2. Design Evolution Overview](#2-design-evolution-overview)
- [3. In-Memory Sharding](#3-in-memory-sharding)
- [4. Distributed Transactions](#4-distributed-transactions)
  - [4.1. Two-Phase Commit (2PC)](#41-two-phase-commit-2pc)
  - [4.2. Try-Confirm/Cancel (TC/C)](#42-try-confirmcancel-tcc)
  - [4.3. Saga](#43-saga)
  - [4.4. TC/C vs Saga](#44-tcc-vs-saga)
- [5. Event Sourcing](#5-event-sourcing)
- [6. High-Performance Event Sourcing](#6-high-performance-event-sourcing)
- [7. Reliability with Raft](#7-reliability-with-raft)
- [8. Distributed Event Sourcing](#8-distributed-event-sourcing)

## 1. Problem and Scope

- **Digital wallet** — backend that lets users store money in a per-user balance and transfer it directly to another wallet on the same platform (e.g., PayPal), avoiding bank-to-bank fees and latency.
- **Functional scope** — only cross-wallet balance transfer between two wallets; no FX, no other features.
- **Non-functional requirements** — 1,000,000 TPS, 99.99% availability, transactional guarantees for correctness, and **reproducibility** so historical balances can be reconstructed by replaying data from the beginning.
- **Why reproducibility over reconciliation alone** — comparing internal records to bank statements only flags discrepancies; it cannot explain *how* a difference was generated. Replay can.
- **Node-count math** — each transfer is two operations (debit + credit), so 1M TPS needs ~2M per-node TPS. At 1,000 TPS/node → 2,000 nodes; at 10,000 TPS/node → 200 nodes; design goal is to push per-node TPS up to lower hardware cost.
- **Amount as string, not double** — avoids floating-point precision loss in money math (rationale carried over from Ch 11 Payment System).

## 2. Design Evolution Overview

- The chapter walks through three designs, each fixing the prior one's limitation:
  1. **In-memory sharding (Redis)** — fast but no atomicity across nodes.
  2. **Distributed transactions on relational DBs (2PC, TC/C, Saga)** — atomic but no audit trail.
  3. **Event Sourcing + CQRS** — adds reproducibility, then optimized via local files, Raft replication, and sharding for 1M TPS.

## 3. In-Memory Sharding

- **Data model** — `<user, balance>` map; one Redis cluster shards user accounts across nodes via `accountID.hashCode() % partitionNumber`.
- **Sharding metadata** — number of partitions and Redis node addresses kept in **Zookeeper** as highly-available config storage.
- **Wallet service** — stateless service that receives a transfer command, validates it, and updates two account balances on (typically) two different Redis nodes.
- **Failure mode** — if the wallet service crashes after the debit but before the credit, the transfer is incomplete. Two updates aren't atomic, so the design fails the correctness requirement.

## 4. Distributed Transactions

- **Why relational DBs replace Redis** — to make multi-node updates atomic, each shard must be a transactional database, not just a key-value store.
- **Two flavors of distributed transactions** — **low-level** (database-driven, e.g., 2PC via X/Open XA) and **high-level** (application-driven via compensation, e.g., TC/C, Saga).

### 4.1. Two-Phase Commit (2PC)

- **2PC** — coordinator (the wallet service) does normal reads/writes against locked DBs, then asks all DBs to *prepare*; if all answer yes, it tells them to *commit*, otherwise *abort*.
- **Both phases share one transaction** — locks are held the entire time across all participants.
- **Drawbacks** — long-held locks kill performance; the coordinator is a single point of failure; requires DB-level support for the prepare protocol (XA).

### 4.2. Try-Confirm/Cancel (TC/C)

- **TC/C** — compensating transaction in two **independent** local transactions: phase 1 *Try* reserves resources; phase 2 *Confirm* finalizes or *Cancel* reverses via business-logic undo.
- **Database-agnostic** — works on any DB that supports local transactions; the "undo" lives in application code, not the DB.
- **Valid Try-phase choice for `A → $1 → C`** — only `Try: A=-$1, C=NOP`; `Confirm: A=NOP, C=+$1`; `Cancel: A=+$1, C=NOP`. Choices that credit C in the Try phase risk somebody draining C before Cancel can reclaim the funds; choices that touch both accounts in Try create concurrency complications.
- **Unbalanced state is expected** — at the end of Try, $1 is missing (debited from A, not yet credited to C). TC/C exposes intermediate state to the application; this is fine as long as the full sequence completes.
- **Phase status table** — persisted in a transactional DB (typically co-located with the debit account's DB) recording transaction ID, Try-phase status per DB, second-phase name (`Confirm`/`Cancel`), second-phase status, and an out-of-order flag. Survives wallet-service restarts so TC/C can resume.
- **Out-of-order execution** — a node may receive a Cancel before its Try due to network reordering. Mitigation: the Cancel leaves an out-of-order flag; a later-arriving Try checks the flag and fails immediately.

### 4.3. Saga

- **Saga** — de-facto standard for microservices; orders all operations in a linear sequence of independent local transactions. On failure, rolls back from the failing operation back to the first using compensating transactions.
- **Coordination styles** — **choreography** (services subscribe to each other's events, fully decentralized; hard to reason about with many services) or **orchestration** (single coordinator drives the order; preferred for digital wallets).

### 4.4. TC/C vs Saga

| Dimension | TC/C | Saga |
|---|---|---|
| Compensating action | In Cancel phase | In rollback phase |
| Central coordination | Yes | Yes (orchestration mode) |
| Operation execution order | Any | Linear |
| Parallel execution | Yes | No |
| Partial inconsistent state visible | Yes | Yes |
| Logic location | Application | Application |

- **When to pick which** — Saga if following microservice trends or with few services and no strict latency need; TC/C if latency-sensitive with many services (parallelism wins).

## 5. Event Sourcing

- **Motivation** — auditors ask: balance at any time? historical correctness? logic correctness after a code change? Storing only current state can't answer these.
- **Event Sourcing** — a Domain-Driven Design technique: persist the immutable sequence of state-changing facts, derive state by replay.
- **Four core terms** — **Command** (intent from outside, e.g., "transfer $1 A→C"), **Event** (validated fact in past tense, e.g., "transferred $1 A→C"), **State** (current map of `account → balance`), **State Machine** (validates Commands → emits Events; applies Events → mutates State).
- **Two FIFO queues** — Commands and Events both go through ordered queues (Kafka is a typical choice); ordering is essential.
- **State Machine must be deterministic** — no random numbers, no external I/O during apply; replay must yield identical State.
- **Reproducibility** — replay the immutable Event log from the start (or from a snapshot) to reconstruct historical balance, verify correctness, or test new code by re-running events.
- **CQRS (Command-Query Responsibility Segregation)** — instead of publishing State, publish all Events; one writer State Machine and many read-only State Machines that build different views (current balance, hourly window for double-charge investigation, audit trail). Read views are eventually consistent.

## 6. High-Performance Event Sourcing

- **Local file-based Command/Event store** — write append-only files on local disk instead of remote Kafka; sequential disk writes are very fast and according to ACM Queue can outpace random memory access in some cases.
- **mmap** — maps the append-only file into memory so the OS caches recent content; gives in-memory speed for reads and disk durability for writes simultaneously.
- **File-based State** — replace the remote relational DB with **SQLite** (file-based RDBMS) or **RocksDB** (LSM-tree key-value store optimized for writes with caching for reads).
- **Snapshot** — periodic immutable dump of current State to a file (often stored in HDFS); on recovery, the State Machine loads the latest snapshot and replays only events after it. Finance teams typically demand a 00:00 snapshot for daily verification.
- **Tradeoff** — local files make a node stateful and a single point of failure; addressed by replication next.

## 7. Reliability with Raft

- **Only Events need strong durability** — State and snapshots can be regenerated from Events. Commands can't be relied on (Event generation may be non-deterministic with I/O), so Events are the single source of truth that must never be lost.
- **Raft consensus** — replicates the append-only Event list across nodes with no data loss and identical ordering; tolerates failures as long as a majority is up (3-of-5, 2-of-3).
- **Roles** — Leader (receives Commands, replicates), Follower, Candidate (during election).
- **Failure handling** — leader crash triggers automatic re-election from the remaining healthy nodes; client retries unacknowledged Commands against the new leader. Follower crash is handled by Raft's indefinite retry until restart or replacement.
- **Effect on Event Sourcing** — leader takes Commands → Events → appends locally → Raft replicates to followers → all nodes (leader + followers) apply Events to local State, guaranteeing identical State across the cluster.

## 8. Distributed Event Sourcing

- **Two remaining limitations of a single Raft group** — CQRS request/response is not real-time (clients pull); a single Raft group can't sustain 1M TPS.
- **Pull → push** — adding a reverse proxy between client and Event Sourcing nodes lets the read-only State Machine push execution status back to the proxy as soon as it sees the Event, giving clients a real-time feel.
- **Sharding by hash** — partition data by hash of key (e.g., mod 2 for two partitions), each partition is its own Raft group; cross-partition transfers reuse TC/C or Saga on top.
- **End-to-end Saga happy path** — coordinator records the transfer in the Phase Status Table; sends `A-$1` to Partition 1's Raft leader → command list → validated → Event → Raft sync → State updated → CQRS read path pushes success back; coordinator marks Partition 1 done; sends `C+$1` to Partition 2; same flow; coordinator marks transaction complete.
- **Final architecture combines all layers** — sharded Raft groups for scale, Event Sourcing for reproducibility, mmap-backed local files for low latency, Saga/TC/C for cross-partition atomicity, and CQRS push for real-time responses.
