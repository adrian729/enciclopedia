# Ch 19: Choosing the Appropriate Architecture Style

## Table of Contents

- [1. Shifting "Fashion" in Architecture](#1-shifting-fashion-in-architecture)
- [2. Decision Criteria](#2-decision-criteria)
- [3. Core Determinations](#3-core-determinations)
- [4. Monolith Case Study: Silicon Sandwiches](#4-monolith-case-study-silicon-sandwiches)
- [5. Distributed Case Study: Going, Going, Gone](#5-distributed-case-study-going-going-gone)

## 1. Shifting "Fashion" in Architecture

- **It depends** — the canonical answer to "which style?" Choosing an architecture style is the culmination of trade-off analysis across architecture characteristics, domain considerations, strategic goals, and organizational factors.
- **Observations from the past** — new styles arise as fixes for the pain points of older ones (e.g., the rethink of code reuse after architects observed its negative trade-offs).
- **Changes in the ecosystem** — chaotic and unpredictable; nobody knew Kubernetes a few years ago, and in a few more years it may be replaced by something not yet written.
- **New capabilities** — new paradigms (not just new tools) shift architecture. Containers like Docker were "evolutionary" yet had outsized impact on architects, tools, and engineering practices.
- **Acceleration** — the ecosystem changes faster every cycle; generative AI is the current standout example.
- **Domain changes** — businesses evolve, merge, pivot; the domains we write software for shift continuously.
- **Technology changes** — organizations chase technological changes that have clear bottom-line benefits.
- **External factors** — licensing cost, vendor pricing, and other peripheral pressures can force migration even when teams are happy with a tool.

## 2. Decision Criteria

Only choose an architecture style when you have sufficient knowledge of the following factors:

- **The domain** — understand the major aspects of the business domain, especially those that impact operational architecture characteristics. Business analysts can fill gaps.
- **Architecture characteristics that impact structural decisions** — perform an architecture characteristics analysis. Most generic styles can implement any domain; the *real* difference between styles is how well each supports specific characteristics. The Part II star charts compare characteristics, not domains, for that reason.
- **Data architecture** — collaborate with data developers on databases and schemas, especially when integrating with an existing data architecture.
- **Cloud deployments** — on-prem versus cloud trade-offs differ sharply. Storage volumes and data movement (which can incur significant cost) are key concerns. The cloud commoditizes capabilities once seen as "almost magical" (elasticity, scalability) into config parameters.
- **Organizational factors** — vendor cost can rule out an otherwise ideal design; planned mergers/acquisitions push architects toward open solutions and integration architectures.
- **Knowledge of process, teams, and operational concerns** — the SDLC, architect–operations interaction, and QA maturity all matter. Microservices presents difficulties for organizations lacking Agile engineering maturity.
- **Domain/architecture isomorphism** — *isomorphism* (Greek *isos* "equal" + *morph* "shape") names the generic shape of an architecture and how its components depend on each other.
  - **Layered vs. modular monolith** — separation by layers vs. by domains is visible in the isomorphic drawing.
  - **Monolith vs. distributed** — distribution of core components shows the macro-level structure.
  - **Topology fit** — microkernel suits customizability (plug-ins); space-based suits a domain like genome analysis (many discrete operations and processors).
  - **Topology mismatch** — highly scalable systems struggle with large monoliths (coupling); highly coupled domains (e.g., a multipage insurance form where each page depends on prior context) fit poorly with decoupled microservices and better with intentionally coupled service-based architecture.

## 3. Core Determinations

After accounting for those factors, the architect must answer:

- **Monolith versus distributed?** — does a single set of architecture characteristics suffice (monolith), or do different parts need different sets (distributed)? **Architecture quantum** (Ch 7) is the tool for this determination.
- **Where should data live?** — monoliths typically assume one relational DB; distributed forces decisions about which services persist data and how data flows through workflows. Iterate on structure *and* behavior.
- **Synchronous or asynchronous communication?** — sync is more convenient but trades off scalability/reliability; async buys performance and scale at the price of synchronization, deadlocks, race conditions, and debugging headaches. Default to synchronous; use asynchronous only when necessary.
- **Output of the design process** — an *architecture topology* (chosen style plus any hybridizations), Architectural Decision Records (ADRs) for the highest-effort parts, and architecture fitness functions to protect important principles and operational characteristics.

## 4. Monolith Case Study: Silicon Sandwiches

- **Context recap** — characteristics analysis (Ch 5) showed a single quantum sufficed; simple app, modest budget, monolith appealing. Two component designs existed: domain-partitioned and technically partitioned.

### 4.1. Modular Monolith

- **Topology** — domain-centric components, single relational database, single web UI (with mobile-friendly design), deployed as one quantum.
- **Future-proofing** — separate database tables/assets along the same domain lines as components, easing later migration to a distributed architecture.
- **Customizability** — since the style itself doesn't handle it, design an `Override` endpoint where developers upload customizations; every domain component must reference `Override` for each customizable characteristic. An architectural fitness function is well-suited to enforce that linkage.

### 4.2. Microkernel

- **Topology** — core system contains domain components and a single relational database; each customization is a plug-in. A common plug-in set (with its own DB) plus local plug-ins (each with its own data) keep plug-ins decoupled.
- **Backends for Frontends (BFF) pattern** — the API layer becomes a thin microkernel adapter. The backend serves generic data; each BFF (e.g., iOS BFF) tailors format, pagination, latency to its frontend, enabling rich UIs and easy expansion to new device types.
- **Synchronous communication** — adequate, since neither extreme performance nor elasticity is required and operations are short.

| Aspect | Modular Monolith | Microkernel |
|---|---|---|
| Customization mechanism | `Override` endpoint referenced by every domain component | Plug-ins (common set + local set) |
| Data | Single relational DB; tables aligned to domains for future split | Core relational DB + per-plug-in data stores |
| API surface | Single web UI | API layer with BFF adapters per frontend |
| Best fit | Simple app, single quantum, low budget | Customizability is a primary architecture characteristic |

## 5. Distributed Case Study: Going, Going, Gone

- **Why distributed** — component analysis (Ch 8) showed different parts need different characteristics (auctioneer vs. bidder availability/scalability). Requirements explicitly demand scale, elasticity, performance, and fine-grained customization.
- **Style choice — microservices over event-driven** — both fit, but microservices better supports varying operational characteristics across components. Event-driven typically separates pieces by orchestrated/choreographed communication, not by characteristics.
- **Addressing weak points by design** — microservices is naturally scalable but can develop performance issues from too much orchestration or aggressive data separation; design around them.
- **Three user interfaces** — `Bidder` (many), `Auctioneer` (one per auction), `Streamer` (read-only video and bid stream, optimized because no updates needed).
- **Services and roles:**

| Service | Responsibility |
|---|---|
| `Bid Capture` | Captures online bidder entries; async forward to `Bid Tracker`; no persistence (conduit) |
| `Bid Streamer` | Streams bids back to participants; high-performance read-only |
| `Bid Tracker` | Unifies bids from `Bid Capture` and `Auctioneer Capture`; orders in near real time; both inbound connections async (queues as buffers for differing flow rates) |
| `Auctioneer Capture` | Captures auctioneer bids (separate from `Bid Capture` because architecture characteristics differ) |
| `Auction Session` | Manages individual auction workflow |
| `Payment` | Third-party payment provider invoked after `Auction Session` completes |
| `Video Capture` | Captures the live auction video stream |
| `Video Streamer` | Streams video to online bidders |

- **Mixed sync/async** — async chosen primarily to absorb variation in operational characteristics. Example: `Payment` processes one new payment per 500 ms; if many auctions end simultaneously, sync calls would time out. Message queues add reliability to the fragile path.
- **Five resulting quanta** — `Payment`, `Auctioneer`, `Bidder`, `Bidder Streams`, `Bid Tracker`. Quantum analysis at component design made service, data, and communication boundaries easier to identify.
- **Least-worst trade-offs** — not the "correct" or only design, but the one with the least worst trade-offs; intelligent use of events and messages provides a foundation for future expansion.
