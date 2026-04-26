# Ch 5.05: Concurrency and Transactions

## Table of Contents

- [1. Definition and Why It Matters](#1-definition-and-why-it-matters)
- [2. Canonical Interview Examples](#2-canonical-interview-examples)
- [3. Serialization Strategies](#3-serialization-strategies)
- [4. Pessimistic Locking](#4-pessimistic-locking)
- [5. Lock Scope and Data Structures](#5-lock-scope-and-data-structures)
- [6. Write Skew With Phantom Data](#6-write-skew-with-phantom-data)
- [7. Optimistic Locking](#7-optimistic-locking)
- [8. Change Product Requirement to Simplify](#8-change-product-requirement-to-simplify)
- [9. How to Pick a Concurrency Strategy](#9-how-to-pick-a-concurrency-strategy)

## 1. Definition and Why It Matters

- **Concurrency** — happens when more than one thread is trying to access and modify the same resource
- **Why it's a strong signal in interviews** — most candidates avoid the topic, yet it's common in daily engineering work; demonstrating competence here is perceived strongly by interviewers
- **When to raise it** — any data source that can be read or modified by multiple requests has potential concurrency problems; affects correctness and reliability, and if unaddressed leads to unhappy customers
- **Core of certain questions** — meeting scheduling and ticket booking systems are fundamentally concurrency problems

## 2. Canonical Interview Examples

- **Global counter** — classic read-modify-write problem: two threads read `x=1` simultaneously, both increment, both persist `x=2`; final result is 2 instead of 3
- **Ridesharing match** — matcher reads the same driver list from the location service as another request, so the same driver gets assigned to multiple riders
- **Ticket booking** — two users must not be allowed to book the same seat, or two people show up at the event for one seat
- **Meeting scheduling** — a room must not get double-booked for overlapping `from_time`/`to_time` ranges

## 3. Serialization Strategies

- **Single thread** — insert requests into a queue and process them one by one; no concurrency issues, but throughput is potentially poor. Acceptable when QPS is very low
- **Single thread micro batch** — batch multiple requests together and solve them in one pass (e.g., fetch a list of driver locations and run the matching algorithm for multiple riders and drivers at once); amortizes expensive operations like disk IO across many requests. Trade-off: freshness suffers because you wait to buffer up requests
- **Partition into multiple serial processing** — shard the application by a request attribute and process each shard serially. Throughput scales with number of shards since each shard is mutually exclusive. Trade-offs: complexity of maintaining the sharding mapping, and cross-shard consideration (if the user experience benefits from wider search space) incurs cross-node call overhead

## 4. Pessimistic Locking

- **Definition** — acquire a lock to access and write to a resource before the transaction runs; lock has varying granularity across entities
- **Write lock (exclusive)** — holder blocks other transactions from writing *and* reading; very safe but limits both read and write throughput
- **Read lock (shared)** — holder allows others to read but not modify; internally creates a local copy for readers while the transaction modifies an intermediate copy; improves read throughput but both lock types still limit write throughput
- **When to prefer** — read/write queries are low and correctness is critical; simplicity of reasoning about correctness is the main advantage

| Aspect | Pessimistic | Optimistic |
|---|---|---|
| Mechanism | Acquire lock before transaction | Version number (eTag) checked on commit |
| Best for | Low QPS, correctness critical | High throughput, low contention |
| Failure mode | Deadlocks, rogue thread holds lock → timeout needed | Retries pile up under high contention, poor UX |
| Throughput | Limited (both reads and writes can block) | Higher (no lock acquisition overhead) |

- **Disadvantages** — in highly concurrent environments, throughput is limited since read and write locks block writes; deadlocks can appear as the app grows; a rogue thread holding the lock stalls others and a timeout is needed to release

## 5. Lock Scope and Data Structures

- **Database lock** — one transaction per database; extremely low throughput
- **Table-based lock** — one transaction per table at a time; very low throughput, but higher than DB-level
- **Row-level lock** — one transaction per row; much better throughput since multiple rows can be accessed in parallel; still problematic if many concurrent transactions hit one row
- **Locks on in-app data structures** — concurrency control is also needed for in-memory structures (quadtree, trie, concurrent queue) when correctness matters to the end-user
- **Queue data structure** — either lock the whole queue (no insertion during consumption) or use two locks (one for insertion, one for consumption); relevant for rate limiter rolling windows
- **Tree data structure** — lock hierarchically: locking a subtree blocks access to that subtree. Useful for a quadtree in ridesharing (lock a region); complexity arises when acquiring a lock on an ancestor of an already-locked subtree. Limiting locks to a particular height level is one simplification
- **Other data structures** — any highly concurrent custom structure where correctness matters should be raised as a potential issue

## 6. Write Skew With Phantom Data

- **Problem** — sometimes you need to lock resources that don't logically exist in any table or structure (e.g., booking a room with a continuous time range, where a `Room` table exists but no records for arbitrary time slots). Two threads checking availability of a range cause a read-modify-write issue
- **Scope up to lock** — find a resource that is a superset of the granular resources you're trying to lock (e.g., lock the whole meeting room row instead of the specific time range)
- **Predicate lock** — locks based on queries; traverse all predicate locks to detect overlap. Highly inefficient with many locks
- **Materialize data** — create data to lock on (e.g., agree with the interviewer to restrict bookings to 30-minute blocks, create records for those blocks, then treat it like ticket booking). Changes product requirement, and you need a plan to keep materializing new time slots over time

## 7. Optimistic Locking

- **Mechanism** — transaction verifies no other thread updated the resource before committing, using a monotonically increasing version number (a.k.a. eTag) attached to the resource
- **Flow** — two threads read `x` at `v1`; one commits, bumping to `v2`; when the second tries to commit with `v1`, the database sees it's outdated and fails the request. The client reloads `v2` and retries
- **Advantage** — no waiting on locks; threads apply business logic freely; higher throughput without lock acquisition/release overhead
- **Disadvantage** — in highly contended resources many failures and retries occur; these can bubble up to end-users as poor UX

## 8. Change Product Requirement to Simplify

- **Reframe instead of tunnel-visioning** — step back and ask *why* you're doing something the obvious way
- **Global counter example** — instead of a distributed database with shared memory, keep a log and run a batch job; longer delay but may be acceptable for the requirement
- **Ridesharing example** — if riders picking their own driver creates concurrency, change the requirement so the system assigns the driver; simpler UX *and* simpler tech. Technical complexity often results from product complexity — rethink the product experience

## 9. How to Pick a Concurrency Strategy

- **Brainstorm multiple options** — for a generalist interview, the tactics above are enough; deep distributed-lock or DB-transaction expertise turns it into a domain-focused interview
- **Discuss pros and cons against the design requirements** — focus on what the end-user would experience, not generic trade-offs
- **Interviewer is looking for** — ability to present options and trade-offs, not an instant best solution
