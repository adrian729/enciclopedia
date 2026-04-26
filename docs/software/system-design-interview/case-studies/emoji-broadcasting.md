# Emoji Broadcasting (Live-Stream Reactions)

> Liu's Ch 6.03 only. The constraint is unusual: **10M emojis per second** in a live stream. The senior-level moves are **client-side sampling** and **aggregated UI rendering** — neither is a tech move; both are product moves.

## Table of Contents

- [1. The Setup](#1-the-setup)
- [2. The Naive Approach](#2-the-naive-approach)
- [3. Two Senior-Level Moves](#3-two-senior-level-moves)
  - [3.1. Client-Side Sampling](#31-client-side-sampling)
  - [3.2. Aggregated UI Rendering](#32-aggregated-ui-rendering)
- [4. Architecture](#4-architecture)
- [5. Cross-Region Coordination](#5-cross-region-coordination)
- [6. Trade-offs](#6-trade-offs)
- [Sources](#sources)

## 1. The Setup

A celebrity goes live to tens of millions of concurrent watchers. Each watcher can tap an emoji button to react. At peak, the system sees **10M emojis per second** — and each emoji must somehow appear on every other watcher's screen.

This is not a typical "send a message to N recipients" problem. The product UX is the **emoji confetti** — a swirl of icons floating up the screen — and that UX is what enables the design.

## 2. The Naive Approach

Send every emoji to every watcher: at 10M emojis/sec × 10M watchers, the fanout is 100T messages/sec. Even with optimal infrastructure, this is unachievable. And the user wouldn't perceive the difference between "exactly 10M emojis" and "lots of emojis."

The naive approach over-engineers the wrong problem.

## 3. Two Senior-Level Moves

### 3.1. Client-Side Sampling

Each client doesn't send every tap to the server. It samples — say, 1 in 10 taps make it to the wire. Server receives ~1M emojis/sec instead of 10M. The aggregate signal is preserved (we know the rate is high) at 10× lower cost.

See [Resilience Patterns — Sampling](fundamentals/resilience-patterns.md) for the underlying technique.

### 3.2. Aggregated UI Rendering

The server doesn't broadcast individual emojis to every watcher. It broadcasts an **aggregated count** every second: "users sent 800K hearts in the last second." Each client renders that count as a swirl of confetti — locally generated icons floating up the screen at the right density.

The user perceives "tons of emojis flying everywhere"; the server only broadcasts a small periodic summary. The actual icon positions and animations are computed locally on each device.

## 4. Architecture

```
Client (sampling on tap → at most 1 in 10 sent)
   ↓
Edge / API gateway (regional)
   ↓
Stream of emoji events (Kafka or similar)
   ↓
Aggregator (windowed: 1-second bucket per stream per region)
   ↓
Broadcast service (push aggregated counts to all watchers)
   ↓
Client (renders confetti at the broadcast rate)
```

**Storage** is minimal — emoji counts are summary statistics, not durable history. A short-lived in-memory window plus a long-term aggregate written to a durable store at coarser granularity.

## 5. Cross-Region Coordination

10M concurrent watchers are distributed across regions. The interesting trade-off:

- **Regional aggregation, regional broadcast.** Each region aggregates its own emojis and broadcasts to its own watchers. Cross-region synchronization is expensive; intra-region is enough for the UX.
- **Cross-region forwarding.** Each emoji event is forwarded to every region's aggregator so the broadcast count is global.

Liu's pick is **cross-region forwarding** — forward each emoji to all three regions because **the intra-region savings of a global connection store don't justify cross-region coordination**. The marginal cost of forwarding events is small relative to the marginal cost of running a global connection store.

## 6. Trade-offs

- **Sampling fidelity.** 1-in-10 sampling means the aggregate rate is approximately right. 1-in-100 would be cheaper but the rate could miss bursts.
- **Aggregation window.** 1-second window means counts update every second. Smaller windows cost more; larger windows feel laggy.
- **Confetti density.** Client-side rendering means the system doesn't need to know exactly which emojis to render — it just needs the *rate*.
- **Storage retention.** Emoji counts are typically transient; a coarse aggregate (per-minute, per-stream) goes to durable storage for analytics.

## Sources

- [Liu Ch 6.03: Emoji Broadcasting](software/system-design-interview/books/system-design-interview-fundamentals/ch06_03_emoji_broadcasting.md)
