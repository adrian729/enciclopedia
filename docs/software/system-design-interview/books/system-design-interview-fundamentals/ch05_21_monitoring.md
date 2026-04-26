# Ch 5.21: Monitoring

## Table of Contents

- [1. Why Monitor](#1-why-monitor)
- [2. Core Metrics](#2-core-metrics)
- [3. Interview Guidance](#3-interview-guidance)

## 1. Why Monitor

- **Reality ≠ ideal** — systems don't auto-adjust perfectly to changing load; someone or something has to notice and react
- **Signal to bring up in the interview** — an on-call-aware candidate names the metrics worth tracking for this specific system

## 2. Core Metrics

| Metric | What it tells you | When it spikes |
|---|---|---|
| **Latency** | End-user experience degradation | Check downstream dependencies first; if clean, the service itself is the problem |
| **QPS** | Traffic trend; rogue internal callers | Plan capacity for future growth; spot inefficient callers making redundant queries |
| **Error rate** | Reliability after deploys | On-call investigates; watch overall and per-endpoint rates during feature launches |
| **Storage** | Data-growth runway | Forecast so databases don't hit the storage ceiling |
| **Product-specific event counts** | Business-level health | Below |

## 3. Interview Guidance

- **Monitor what you expect to happen** — a cron job should emit a "ran successfully" event; if no event arrives in time, fire an alarm
- **Product-specific signals**:
  - **E-commerce** — sudden drop in orders processed
  - **Ridesharing** — backlog of the request queue; a full queue means riders are waiting
- **Point is situational awareness, not a laundry list** — don't recite every metric big companies track; name the metrics relevant to the system you're designing
