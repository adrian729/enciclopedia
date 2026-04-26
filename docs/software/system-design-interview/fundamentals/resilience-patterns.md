# Resilience Patterns

> Liu's Ch 5.13 catalogues the patterns that keep systems usable under partial failure: timeout, exponential backoff, buffering, sampling, fail-to-open. Xu doesn't cover them as a group but applies them in nearly every product design.

## Table of Contents

- [1. Timeout](#1-timeout)
- [2. Exponential Backoff](#2-exponential-backoff)
- [3. Buffering](#3-buffering)
- [4. Sampling](#4-sampling)
- [5. Fail to Open](#5-fail-to-open)
- [6. Hinted Handoff (Storage Variant)](#6-hinted-handoff-storage-variant)
- [Sources](#sources)

## 1. Timeout

Timeouts convert the uncertainty of a missing response into a decision. The trade-off:

- **Too long** — wastes resources on dead services; users feel the latency before the timeout fires.
- **Too short** — gives up on responses that would have arrived; wastes upstream work that did succeed.

The ideal timeout equals the request's actual processing time, but that number is never known up front. In practice, set the timeout based on the p99 of historical latency plus a safety factor.

Timeouts also drive **service discovery and leader-health checks**: a node that doesn't respond to a heartbeat within the timeout is suspected dead, and the protocol takes action.

## 2. Exponential Backoff

When a downstream call fails, retrying immediately makes the problem worse — the downstream is already struggling, and a flood of retries is the fastest way to push it over.

**Exponential backoff** spaces retries progressively: 100 ms, 200 ms, 400 ms, 800 ms, .... Each retry pause doubles. Combined with a **maximum retry cap**, a service that's still failing after the cap signals real failure (escalate to dead-letter, alert, or fall back).

**Jitter** (randomizing each pause within a window) prevents thundering herds: if 1,000 clients all retry at exactly 800 ms, they hammer the recovering downstream simultaneously.

## 3. Buffering

Buffering amortizes per-request overhead. Liu's example: emitting metrics every second instead of per event reduces network and write costs by 1,000× when there are 1,000 events/sec, at the cost of one second of metric staleness.

The trade-off lever is the buffer interval. Big buffer = high throughput, stale output, lost data on crash. Small buffer = fresh, lower throughput, less data lost on crash.

## 4. Sampling

Sampling trades **accuracy** for **performance**. The driver-location-update example: persisting every fifth update cuts QPS and storage by 80%. The trade-off is that the location is up to 5 update intervals stale.

Sampling is appropriate when:

- The aggregate signal matters more than every individual event (telemetry, dashboards, anomaly detection).
- The user-visible output tolerates approximation (heatmaps, user-counts).
- The accuracy requirement is bounded ("within 1%").

Liu's emoji broadcasting case study (Ch 6.03) is the extreme: at 10M emojis/second, **client-side sampling** sends only a fraction to the server, and the server renders **emoji confetti** rather than every individual tap. The user perception is "lots of emojis"; the technical cost is dramatically lower.

## 5. Fail to Open

Keep the user experience perceived-available when the ideal path is broken. The product still works; some non-critical part is degraded.

Liu's examples:

- **Payment processor down** — let the order through and collect later. The customer gets the product; the back office reconciles.
- **Surge price estimator down** — fall back to the **baseline price without the surge multiplier**. The ride still gets booked.
- **Recommendation service down** — show a generic best-sellers list instead of personalized recs.

"Fail to open" inverts the usual circuit-breaker framing: instead of cutting off the request, you serve a degraded version. The right choice depends on whether the missing component is correctness-critical (must block) or value-add (can degrade gracefully).

## 6. Hinted Handoff (Storage Variant)

Cassandra's storage analog of fail-to-open: when a node is down, stash the write on a healthy neighbor and transfer it back when the owner returns. The cluster keeps accepting writes through the failure rather than blocking. See [CAP, Consensus & Conflict Resolution](fundamentals/cap-consensus-and-conflict-resolution.md) for the full mechanism.

## Sources

- [Liu Ch 5.13: Resilience Patterns](software/system-design-interview/books/system-design-interview-fundamentals/ch05_13_resilience_patterns.md)
- [Liu Ch 6.03: Emoji Broadcasting](software/system-design-interview/books/system-design-interview-fundamentals/ch06_03_emoji_broadcasting.md) (sampling at scale)
