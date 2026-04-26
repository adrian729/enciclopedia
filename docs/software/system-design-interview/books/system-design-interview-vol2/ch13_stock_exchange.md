# Ch 13: Stock Exchange

## Table of Contents

- [1. Problem and Scope](#1-problem-and-scope)
- [2. Domain Concepts](#2-domain-concepts)
- [3. High-Level Architecture](#3-high-level-architecture)
  - [3.1. Trading Flow](#31-trading-flow)
  - [3.2. Market Data Flow](#32-market-data-flow)
  - [3.3. Reporter Flow](#33-reporter-flow)
- [4. Data Models](#4-data-models)
- [5. Latency Optimization](#5-latency-optimization)
- [6. Event Sourcing in the Exchange](#6-event-sourcing-in-the-exchange)
- [7. High Availability and Fault Tolerance](#7-high-availability-and-fault-tolerance)
- [8. Determinism](#8-determinism)
- [9. Market Data Distribution](#9-market-data-distribution)
- [10. Network Security](#10-network-security)

## 1. Problem and Scope

- **Electronic stock exchange** — system that matches buyers and sellers of securities; this design supports stocks only, with limit orders that can be placed or canceled.
- **Functional requirements** — place new limit order, cancel order, view real-time order book, receive matched trades; risk checks (e.g., max 1M shares of AAPL/user/day); wallet integration to withhold funds for resting orders so users can't overspend.
- **Non-functional requirements** — 99.99% availability (downtime in seconds harms reputation), millisecond round-trip with focus on **99th-percentile latency**, fault tolerance with fast recovery, KYC + DDoS protection.
- **Scale** — 100 symbols, ~tens of thousands of concurrent users, ~1B orders/day. With NYSE's 6.5h trading window: ~43,000 QPS average, ~215,000 peak (5× for open/close bursts).
- **Reference scale points** — NYSE trades billions of matches/day; HKEX ~200B shares/day.

## 2. Domain Concepts

- **Broker** — intermediary (Schwab, Robinhood, Fidelity, etc.) that gives retail clients a UI to place trades and view market data.
- **Institutional clients** — pension funds (rare large trades, need order splitting to minimize market impact), market-making hedge funds (need ultra-low latency for commission-rebate income).
- **Limit order** — buy/sell at a fixed price; may not match immediately and may be partially filled.
- **Market order** — no price; executes immediately at prevailing price; sacrifices cost for guaranteed execution.
- **Market data levels** — **L1** = best bid/ask price + quantities; **L2** = multiple price levels; **L3** = price levels plus per-order queued quantity at each level.
- **Candlestick chart** — open/close/high/low for an interval (1m, 5m, 1h, 1d, 1w, 1mo).
- **FIX protocol** — vendor-neutral securities-transaction protocol from 1991; pipe-delimited tag=value format used between brokers and exchanges.

## 3. High-Level Architecture

- Three flows share components but have different latency budgets: **trading flow** (critical path, tight latency), **market data flow** (publishing to subscribers), **reporter flow** (compliance, settlements; latency-tolerant).

### 3.1. Trading Flow

- **Critical path** — `client gateway → order manager → sequencer → matching engine`; even logging is removed from this path to save time.
- **Client gateway** — input validation, rate limiting, authentication, normalization, routing to the order manager; lightweight by design. Different gateway types serve retail vs. institutional clients (e.g., **colocation engine** runs broker software on a server rented inside the exchange's data center; latency = speed-of-light over cable length).
- **Order manager** — orchestrates risk checks, wallet fund verification, sends order to sequencer, receives executions back from matching engine via sequencer, returns fills to broker. Manages order state transitions (tens of thousands of cases in real systems) — Event Sourcing is a natural fit.
- **Sequencer** — stamps every incoming order and every outgoing execution pair with a sequential ID. Inbound and outbound sequencers each maintain their own monotonic sequence. Provides **timeliness/fairness**, **fast recovery/replay**, and **exactly-once** guarantees. Functions as a message queue and event store; Kafka could be used if its latency were lower and more predictable.
- **Matching engine** (a.k.a. cross engine) — maintains the order book per symbol, matches buys against sells emitting two executions per match (one per side), and streams executions to the market data publisher. Must be **deterministic**: given the same input order sequence, produces the same execution sequence on replay.

### 3.2. Market Data Flow

- **Market Data Publisher (MDP)** — receives execution stream from matching engine, reconstructs order books and candlestick charts, sends to the data service.
- **Data service** — persists to specialized real-time analytics storage (e.g., **KDB** in-memory columnar DB) and exposes feeds for brokers, who relay to their clients.

### 3.3. Reporter Flow

- **Reporter** — builds compliance, tax, settlement, and trading-history reports by joining attributes from incoming orders (full details) with outgoing executions (typically just order ID, price, qty, status). Latency-tolerant; accuracy and compliance dominate.

## 4. Data Models

- **Product** — static metadata per symbol: type, trading symbol, UI symbol, settlement currency, lot size, tick size; rarely changes, highly cacheable.
- **Order** — inbound buy/sell instruction; **Execution (fill)** — outbound matched result. Each match yields two executions (buy + sell sides).
- **Where they live** — critical path keeps orders/executions in memory + sequencer (mmap/shared memory) for fast recovery, archived after market close. Reporter writes them to a database. MDP consumes execution stream to rebuild order book and candlesticks.
- **Order book requirements** — O(1) for placing, canceling, executing; constant-time lookup for volume at/between price levels; fast best-bid/ask query; ability to iterate price levels.
- **Order book structure** — `OrderBook` holds a `Book<Buy>` and `Book<Sell>`, each a `Map<Price, PriceLevel>`. Each `PriceLevel` holds `limitPrice`, `totalVolume`, and a **doubly-linked list** of orders. A top-level `Map<OrderID, Order>` enables O(1) cancel by jumping straight to the linked-list node.
- **O(1) operations** — place = append to tail of `PriceLevel`; match = remove from head; cancel = `orderMap` lookup → unlink from doubly-linked list.
- **Candlestick** — `openPrice`, `closePrice`, `highPrice`, `lowPrice`, `volume`, `timestamp`, `interval`; `CandlestickChart` is a `LinkedList<Candlestick>`.
- **Memory optimizations** — pre-allocated **ring buffers** to avoid allocations; cap in-memory candlesticks and persist the rest to disk.

## 5. Latency Optimization

- **Latency formula** — `Latency = Σ execution time along critical path`; reduce by shortening the path or each task's time (eliminate network/disk, optimize code).
- **Naive multi-server design** — ~500μs network round-trip per hop plus tens of milliseconds for sequencer disk persistence; total in tens of ms — unacceptable as volumes grew.
- **Single-server design** — put gateway, order manager, sequencer, matching engine on one machine; communicate via mmap; modern exchanges hit **tens of microseconds** end-to-end this way.
- **Application loop** — single-threaded `while(true)` polling loop pinned to a fixed CPU core; benefits: no context switches, no locks, no contention → very low p99. Tradeoff: each task must be carefully bounded so it doesn't starve subsequent tasks.
- **mmap message bus** — `mmap(2)` over a file in `/dev/shm` (a memory-backed filesystem) creates inter-process shared memory with no disk access at all; sub-microsecond message sends. Lets components communicate as low-latency microservices inside one server.

## 6. Event Sourcing in the Exchange

- **Why event sourcing fits** — orders pass through many state transitions; immutable event log is the golden source of truth, and replay reconstructs any historical state — essential for an exchange.
- **mmap event store as message bus** — Pub-Sub-like; gateway encodes orders as **FIX over Simple Binary Encoding (SBE)** for compact fast encoding, publishes `NewOrderEvent`; matching engine (with embedded order manager) validates and matches; on match, publishes `OrderFilledEvent`; MDP and reporter subscribe.
- **Order manager as embedded library** — instead of a centralized service (which would add network hops), each consuming component has its own copy; event sourcing guarantees identical state across replicas.
- **Sequencer reduced** — with one shared event store, the sequencer just stamps a `sequence` field on each event and writes to the store; **single writer** to avoid lock contention. It pulls from per-component ring buffers, stamps, and forwards. Backup sequencers stand by for HA.

## 7. High Availability and Fault Tolerance

- **4 nines target** — 99.99% allows only 8.64 seconds of downtime per day; needs near-instant recovery.
- **Hot-warm matching engine** — primary processes events normally; warm secondary processes the same event stream but suppresses outbound publishes. On primary failure, warm takes over instantly; on warm restart, it rebuilds state by replaying the event store. Health detection via heartbeats.
- **Cross-data-center replication** — single-server hot-warm doesn't survive datacenter outages; replicate the entire event store to warm servers in other cities. **Reliable UDP** (e.g., **Aeron**) broadcasts events to many warm servers efficiently.
- **Stateless services scale horizontally** — client gateway just adds servers.
- **Failover decisions** — guard against false alarms and bug-driven cascading failures (a bug that downed primary may also down warm). Practical advice: start with **manual failover** until enough operational signal is gathered; **chaos engineering** to surface edge cases.
- **Leader election with Raft** — 5-node cluster needs majority (N/2+1 = 3) to commit. Followers receive `AppendEntries` from leader; missing heartbeats trigger election timeout → first follower to time out becomes candidate, requests votes via `RequestVote`. Majority wins; split votes restart the election. Term numbers prevent stale leaders.
- **RTO (Recovery Time Objective)** — must be seconds for an exchange → automatic failover with service prioritization and a degradation strategy.
- **RPO (Recovery Point Objective)** — near-zero data loss; Raft's replicated log gives strong consistency across cluster nodes so a new leader can serve immediately.

## 8. Determinism

- **Functional determinism** — same event order in → same execution sequence out; guaranteed by the sequencer + event sourcing combination. Wall-clock times don't matter, order does — replay/recovery becomes much faster because timestamps don't gate processing.
- **Latency determinism** — every trade should experience nearly the same latency; measured via 99th (or 99.99th) percentile latency, often with **HdrHistogram**.
- **Common p99 spike causes (Java)** — JVM safe points: **HotSpot stop-the-world GC**, code deoptimization, debug operations like stack-trace dumps; all freeze threads.

## 9. Market Data Distribution

- **MDP scaling** — tiered service (retail gets 5 L2 levels free, more levels are paid); memory bounded by capping candlesticks per symbol and offloading older to disk.
- **Ring buffers** — fixed-size circular queue with pre-allocated slots; lock-free single-producer/multi-consumer; **padding** keeps the sequence number off shared cache lines to avoid false sharing.
- **Distribution fairness problem** — if the publisher delivers in subscriber-connection order, smart clients race to be first when the market opens. Mitigation: assign random delivery order, or use **multicast**.
- **Multicast** — one source to many subnets simultaneously (vs. **unicast** = one-to-one, **broadcast** = one-to-subnet); pairs with reliable UDP plus retransmission for lost datagrams. Receivers in the same multicast group get data in theory at the same time.
- **Colocation** — exchanges sell rack space inside the matching-engine data center; latency is the cable length itself. Considered a paid VIP service, not a fairness violation.

## 10. Network Security

- **DDoS defenses for the public market data interface**:
  - Isolate public services from private trading services so attacks don't touch core clients; serve public data from read-only replicas.
  - Cache infrequently-changing data so most queries miss the database.
  - Harden URLs: prefer `/data/recent` (cacheable at CDN) over `/data?from=123&to=456` (attackers vary query strings to bypass cache).
  - Maintain effective safelist/blocklist via network gateway products.
  - Apply rate limiting at the edge.
- **KYC** — required before opening accounts for legal compliance.

## Wrap-Up Note

- **Single-server is the modern norm** — many large exchanges run nearly everything on one gigantic server (or one process) to chase microsecond latency; cryptocurrency exchanges increasingly deploy on cloud infrastructure, and DeFi AMM (Automatic Market Making) projects skip order books entirely.
