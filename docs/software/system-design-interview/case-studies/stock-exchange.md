# Stock Exchange

> Vol 2 only — neither Liu nor Xu Vol 1 covers exchanges. The chapter is the **latency outlier** of the book: millisecond round-trip with a focus on **99th-percentile latency** at 215K peak QPS. The killer move is **single-server design** with `mmap` over `/dev/shm` as the message bus — gateway, order manager, sequencer, and matching engine all on one machine, communicating via shared memory, with a single-threaded `while(true)` polling loop pinned to a fixed CPU core. Modern exchanges hit **tens of microseconds** end-to-end this way. Determinism is the contract: same input order sequence → identical execution sequence on replay. ES+CQRS generic mechanics live in [Concurrency & Transactions §6.7](fundamentals/concurrency-and-transactions.md#67-event-sourcing--cqrs).

## Table of Contents

- [1. Requirements](#1-requirements)
- [2. Domain Concepts](#2-domain-concepts)
- [3. Three Flows](#3-three-flows)
- [4. Order Book Data Structure](#4-order-book-data-structure)
- [5. Latency Optimization](#5-latency-optimization)
- [6. Event Sourcing in the Exchange](#6-event-sourcing-in-the-exchange)
- [7. High Availability](#7-high-availability)
- [8. Determinism](#8-determinism)
- [9. Market Data Distribution](#9-market-data-distribution)
- [10. Network Security](#10-network-security)
- [Sources](#sources)

## 1. Requirements

Electronic stock exchange that matches buyers and sellers; this design supports stocks only with limit orders.

- Functional: place new limit order, cancel order, view real-time order book, receive matched trades; risk checks (e.g., max 1M shares of AAPL/user/day); wallet integration to withhold funds for resting orders.
- Non-functional: **99.99% availability** (downtime in seconds harms reputation), **millisecond round-trip with focus on 99th-percentile latency**, KYC + DDoS protection.
- Scale: 100 symbols, ~tens of thousands of concurrent users, ~1B orders/day. With NYSE's 6.5h trading window: **~43,000 QPS average, ~215,000 peak** (5× for open/close bursts).
- Reference: NYSE trades billions of matches/day; HKEX ~200B shares/day.

**Workload-specific ES motivation:** orders pass through many state transitions; the immutable event log is the golden source of truth, and replay reconstructs any historical state — essential for crash recovery in a system that cannot afford to drop trades.

## 2. Domain Concepts

- **Broker** — intermediary (Schwab, Robinhood, Fidelity) that gives retail clients a UI to place trades and view market data.
- **Institutional clients** — pension funds (rare large trades, need order splitting), market-making hedge funds (need ultra-low latency for commission rebates).
- **Limit order** — buy/sell at a fixed price; may not match immediately and may be partially filled.
- **Market order** — no price; executes immediately at prevailing price; sacrifices cost for guaranteed execution.
- **Market data levels** — **L1** = best bid/ask + quantities; **L2** = multiple price levels; **L3** = price levels plus per-order queued quantity.
- **Candlestick** — open/close/high/low for an interval (1m, 5m, 1h, 1d, 1w, 1mo).
- **FIX protocol** — vendor-neutral securities-transaction protocol from 1991; pipe-delimited tag=value format used between brokers and exchanges.

## 3. Three Flows

Three flows share components but with different latency budgets — **trading flow** (critical path), **market data flow** (publishing to subscribers), **reporter flow** (compliance, settlements; latency-tolerant).

**Critical path** — `client gateway → order manager → sequencer → matching engine`. Even logging is removed from this path to save microseconds.

- **Client gateway** — input validation, rate limiting, authentication, normalization, routing. Lightweight by design. Different gateway types serve retail vs institutional clients (e.g., **colocation engine** runs broker software on a server rented inside the exchange's data center; latency = speed-of-light over cable length).
- **Order manager** — orchestrates risk checks, wallet fund verification, sends order to sequencer, receives executions back, returns fills. Manages tens of thousands of state-transition cases — Event Sourcing is a natural fit.
- **Sequencer** — stamps every incoming order and outgoing execution pair with a sequential ID. Inbound and outbound sequencers each maintain their own monotonic sequence. Provides **timeliness/fairness**, **fast recovery/replay**, **exactly-once** guarantees. Functions as a message queue and event store; Kafka could fill the role but its latency is too high and unpredictable for an exchange.
- **Matching engine (cross engine)** — maintains the order book per symbol, matches buys against sells emitting two executions per match (one per side), streams executions to the market data publisher. Must be **deterministic**.

**Market data flow** — Market Data Publisher (MDP) reconstructs order books and candlestick charts from the execution stream → data service persists to specialized real-time analytics storage (e.g., **KDB** in-memory columnar DB) → exposes feeds for brokers.

**Reporter flow** — builds compliance, tax, settlement, and trading-history reports by joining inbound orders (full details) with outbound executions (just order ID, price, qty, status). Latency-tolerant; accuracy and compliance dominate.

## 4. Order Book Data Structure

Requirements: O(1) for placing, canceling, executing; constant-time lookup for volume at/between price levels; fast best-bid/ask query; ability to iterate price levels.

**Structure:**

```
OrderBook
  ├─ Book<Buy>:  Map<Price, PriceLevel>
  └─ Book<Sell>: Map<Price, PriceLevel>

PriceLevel
  ├─ limitPrice
  ├─ totalVolume
  └─ doubly-linked list of orders

(top-level) Map<OrderID, Order>   ← O(1) cancel by jumping straight to the linked-list node
```

**O(1) operations** — place = append to tail of `PriceLevel`; match = remove from head; cancel = `orderMap` lookup → unlink from doubly-linked list.

**Candlestick** — `{openPrice, closePrice, highPrice, lowPrice, volume, timestamp, interval}`; `CandlestickChart` is a `LinkedList<Candlestick>`.

**Memory optimizations** — pre-allocated **ring buffers** to avoid allocations; cap in-memory candlesticks and persist the rest to disk.

## 5. Latency Optimization

`Latency = Σ execution time along critical path`. Reduce by shortening the path or each task's time (eliminate network/disk, optimize code).

| Design | Latency |
|---|---|
| Naive multi-server | ~500μs per network hop + tens of ms for sequencer disk persistence → tens of ms total |
| **Single-server with mmap** | **Tens of microseconds** end-to-end |

**Single-server design** — gateway, order manager, sequencer, matching engine on one machine; communicate via `mmap(2)` over a file in `/dev/shm` (memory-backed filesystem). No disk access at all; sub-microsecond message sends.

**Application loop** — single-threaded `while(true)` polling loop pinned to a fixed CPU core. No context switches, no locks, no contention → very low p99. Tradeoff: each task must be carefully bounded so it doesn't starve subsequent tasks.

**mmap message bus** — lets components communicate as low-latency microservices inside one server.

## 6. Event Sourcing in the Exchange

**Why event sourcing fits** — the immutable log is the golden source of truth, and replay reconstructs any historical state. The generic ES+CQRS mechanism lives in [Concurrency & Transactions §6.7](fundamentals/concurrency-and-transactions.md#67-event-sourcing--cqrs).

**mmap event store as message bus** — Pub-Sub-like. Gateway encodes orders as **FIX over Simple Binary Encoding (SBE)** for compact fast encoding, publishes `NewOrderEvent`. Matching engine (with embedded order manager) validates and matches; on match, publishes `OrderFilledEvent`. MDP and reporter subscribe.

**Order manager as embedded library** — instead of a centralized service (which would add network hops), each consuming component has its own copy; event sourcing guarantees identical state across replicas.

**Sequencer reduced** — with one shared event store, the sequencer just stamps a `sequence` field on each event and writes to the store; **single writer** to avoid lock contention. It pulls from per-component ring buffers, stamps, and forwards. Backup sequencers stand by for HA.

## 7. High Availability

**4 nines target** — 99.99% allows only 8.64 seconds of downtime per day; needs near-instant recovery.

- **Hot-warm matching engine** — primary processes events normally; warm secondary processes the same event stream but suppresses outbound publishes. On primary failure, warm takes over instantly; on warm restart, it rebuilds state by replaying the event store. Health detection via heartbeats.
- **Cross-data-center replication** — single-server hot-warm doesn't survive datacenter outages; replicate the entire event store to warm servers in other cities. **Reliable UDP** (e.g., **Aeron**) broadcasts events to many warm servers efficiently.
- **Stateless services scale horizontally** — client gateway just adds servers.
- **Failover decisions** — guard against false alarms and bug-driven cascading failures (a bug that downed primary may also down warm). Practical advice: start with **manual failover** until enough operational signal is gathered; **chaos engineering** to surface edge cases.
- **Leader election with Raft** — 5-node cluster needs majority (3) to commit. Term numbers prevent stale leaders. See [CAP, Consensus & Conflict Resolution](fundamentals/cap-consensus-and-conflict-resolution.md).
- **RTO** must be seconds → automatic failover with service prioritization and a degradation strategy. **RPO** must be near-zero → Raft's replicated log gives strong consistency so a new leader can serve immediately.

## 8. Determinism

- **Functional determinism** — same event order in → same execution sequence out; guaranteed by the sequencer + event sourcing combination. Wall-clock times don't matter, order does — replay/recovery becomes much faster because timestamps don't gate processing.
- **Latency determinism** — every trade should experience nearly the same latency; measured via 99th (or 99.99th) percentile latency, often with **HdrHistogram**.
- **Common p99 spike causes (Java)** — JVM safe points: **HotSpot stop-the-world GC**, code deoptimization, debug operations like stack-trace dumps; all freeze threads. The critical path therefore avoids JVM features that trigger safe points.

## 9. Market Data Distribution

- **MDP scaling** — tiered service (retail gets 5 L2 levels free, more levels are paid); memory bounded by capping candlesticks per symbol and offloading older to disk.
- **Ring buffers** — fixed-size circular queue with pre-allocated slots; lock-free single-producer/multi-consumer; **padding** keeps the sequence number off shared cache lines to avoid false sharing.
- **Distribution fairness** — if the publisher delivers in subscriber-connection order, smart clients race to be first when the market opens. Mitigation: assign random delivery order, or use **multicast**.
- **Multicast** — one source to many subnets simultaneously; pairs with reliable UDP plus retransmission for lost datagrams.
- **Colocation** — exchanges sell rack space inside the matching-engine data center; latency is the cable length itself. Considered a paid VIP service, not a fairness violation.

## 10. Network Security

DDoS defenses for the public market data interface:

- Isolate public services from private trading services so attacks don't touch core clients; serve public data from read-only replicas.
- Cache infrequently-changing data so most queries miss the database.
- Harden URLs: prefer `/data/recent` (cacheable at CDN) over `/data?from=123&to=456` (attackers vary query strings to bypass cache).
- Maintain effective safelist/blocklist via network gateway products.
- Apply rate limiting at the edge. See [Rate Limiter](case-studies/rate-limiter.md).

**KYC** — required before opening accounts for legal compliance.

**Single-server is the modern norm** for large exchanges — many run nearly everything on one gigantic server (or one process) to chase microsecond latency. Cryptocurrency exchanges increasingly deploy on cloud infrastructure, and DeFi AMM (Automatic Market Making) projects skip order books entirely.

## Sources

- [Vol 2 Ch 13: Stock Exchange](software/system-design-interview/books/system-design-interview-vol2/ch13_stock_exchange.md)
