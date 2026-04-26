# Metrics Monitoring and Alerting

> Vol 2 only — neither Liu nor Xu Vol 1 covers a full monitoring system. The interesting trade-offs are **pull vs push** for collection, **time-series DB choice** (purpose-built TSDBs win over relational/NoSQL), and **delta-of-delta encoding + downsampling** to keep PB-scale time series affordable. Per Facebook research, **≥85% of operational queries hit data from the last 26 hours** — exploit hot-data dominance everywhere.

## Table of Contents

- [1. Requirements](#1-requirements)
- [2. Time-Series Data Model](#2-time-series-data-model)
- [3. Storage Choice](#3-storage-choice)
- [4. High-Level Design](#4-high-level-design)
- [5. Pull vs Push Collection](#5-pull-vs-push-collection)
- [6. Transmission Pipeline](#6-transmission-pipeline)
- [7. Aggregation Locations](#7-aggregation-locations)
- [8. Storage Optimization](#8-storage-optimization)
- [9. Alerting](#9-alerting)
- [10. Visualization](#10-visualization)
- [Sources](#sources)

## 1. Requirements

Internal (not SaaS) monitoring + alerting; out of scope: log monitoring (handled by ELK), distributed tracing, business metrics.

- Scale: 100M DAU; 1,000 server pools × 100 machines × 100 metrics ≈ **10M metrics**.
- Tiered retention: raw 7 days, 1-min resolution 30 days, 1-hour resolution 1 year.
- Alert channels: email, phone, PagerDuty, webhooks.
- Non-functional: scalability, low query latency for dashboards/alerts, reliability (don't miss critical alerts), flexibility for new tech.

## 2. Time-Series Data Model

A **time series** is a value stream uniquely identified by `(metric_name, set of <key:value> labels)`, with an array of `<value, timestamp>` pairs.

Labels enable aggregation — e.g., compute average `CPU.load` for `region=us-west` by filtering on labels. The **line protocol** (Prometheus, OpenTSDB) is `<metric> <labels> <timestamp> <value>` per line.

**Low-cardinality labels** matter — InfluxDB best practice: each label should have a small set of possible values; high cardinality breaks indexes.

## 3. Storage Choice

Why not general-purpose DBs:

- Relational DBs aren't optimized for time-series ops (rolling moving average is gnarly nested SQL); they choke under constant heavy writes and need an index per tag.
- NoSQL (Cassandra, Bigtable) can technically work but requires deep internal knowledge to design a scalable schema.

**Purpose-built TSDBs** use far fewer servers, expose time-series-friendly query languages, and bake in retention/aggregation. Notable: OpenTSDB (Hadoop/HBase-based, complex to run), MetricsDB (Twitter), Amazon Timestream, **InfluxDB** and **Prometheus** (the two most popular). InfluxDB on 8 cores / 32 GB RAM handles **>250,000 writes/sec**.

**Access pattern** — write-heavy and constant; read-heavy and **spiky** (visualization + alerting bursts).

## 4. High-Level Design

```
Sources → Collector → [Kafka] → TSDB → Query Service ──┬──> Visualization
                                                       └──> Alerting
```

- **Metrics source** — application servers, DBs, message queues.
- **Metrics collector** — gathers data and writes to TSDB.
- **TSDB** — stores time series with label indexes; often via custom query language.
- **Query service** — thin wrapper over TSDB; can be skipped if the TSDB exposes a good native interface.
- **Alerting system** — dispatches to channels.
- **Visualization** — dashboards.

## 5. Pull vs Push Collection

**Pull** — dedicated collectors poll each service's `/metrics` HTTP endpoint on a schedule. **Service discovery** (etcd, ZooKeeper) feeds collectors the live endpoint list so new servers aren't missed.

**Multiple collectors** — at scale a single collector can't handle thousands of servers; use a pool with **consistent hashing** so each metrics source maps to exactly one collector (no duplicate pulls). See [Sharding & Consistent Hashing](fundamentals/sharding-and-consistent-hashing.md).

**Push** — a long-running collection agent on each server pushes metrics to the collector cluster. Agent may aggregate (e.g., counters per minute) and buffer locally on rejection. Auto-scaling collector cluster behind a load balancer prevents fall-behind. Caveat: in auto-scaling groups, locally-buffered metrics may be lost when servers rotate out before the collector drains.

| Dimension | Pull wins | Push wins |
|---|---|---|
| Easy debugging | `/metrics` viewable on demand | — |
| Health check | Pull failure = clear server-down signal | Missing push could be a network issue |
| Short-lived jobs | — | Batch jobs may finish before being pulled (workaround: push gateways) |
| Firewalls / multi-DC | All endpoints must be reachable | LB + auto-scaling can accept from anywhere |
| Performance | TCP | UDP, lower latency |
| Data authenticity | Endpoints pre-configured | Anyone can push (mitigate via whitelisting / auth) |

Real world: Prometheus pulls; CloudWatch and Graphite push. Large orgs often support both — especially with serverless where agent install isn't possible.

## 6. Transmission Pipeline

- **Auto-scaling collector cluster** — required regardless of pull/push to handle volume.
- **Add Kafka between collector and TSDB** — protects against TSDB unavailability by buffering writes; decouples ingestion from storage; lets stream-processing engines (Storm, Flink, Spark) consume in parallel. See [Async, Batch, Stream](fundamentals/async-batch-stream.md) and [Queues & Messaging](fundamentals/queues-and-messaging.md).
- **Kafka partitioning strategy** — partition by metric name so consumers can aggregate by metric; further partition by tag/label; categorize and prioritize so critical metrics process first.
- **Kafka alternative — Facebook's Gorilla** is an in-memory TSDB designed to remain available for writes through partial network failures, arguably as reliable as a Kafka buffer without the operational burden.

## 7. Aggregation Locations

| Location | Trade-off |
|---|---|
| **Collection agent** (client-side) | Only simple aggregations (minute-bucketed counters before send) |
| **Ingestion pipeline** (pre-storage, Flink-style) | Slashes write volume; loses raw-data precision and complicates late-arriving events |
| **Query side** (post-storage) | No precision loss, full flexibility; queries run over the full dataset and are slower |

## 8. Storage Optimization

- **Delta-of-delta encoding** — store value deltas with one base instead of full values. Timestamps `1610087371, 1610087381, …` become `1610087371, 10, 10, 9, 11`, dropping per-point timestamp from 32 bits to ~4 bits.
- **Compression** — built into good TSDBs; combines with delta encoding for major savings.
- **Downsampling** — convert high-resolution to low-resolution as data ages. Tier: raw 7 days, 1-min 30 days, 1-hour 1 year. Six 10-second `cpu` samples (10, 16, 20, 30, 20, 30) roll up to two 30-second averages (19, 25).
- **Cold storage** — inactive data moves to cheap cold tiers. See [Observability, Security, Cold Storage](fundamentals/observability-security-cold-storage.md).

## 9. Alerting

**Alert rules** in YAML:

```yaml
instance_down:
  expr: up == 0
  for: 5m
  labels:
    severity: page
```

**Flow** — alert manager fetches rules from cache → polls query service at the rule's interval → on threshold violation creates an alert event → events filtered/merged/deduped → eligible alerts pushed into Kafka → alert consumers fan out to email/SMS/PagerDuty/HTTP webhooks.

**Alert store** — a KV DB like **Cassandra** that tracks each alert's state (`inactive / pending / firing / resolved`); guarantees at-least-once notification.

**Alert manager** — filtering, merging duplicates within an instance, retry on failed sends, access control.

**Build vs buy** — many off-the-shelf alerting systems integrate tightly with TSDBs and notification channels; justifying a custom build is hard at senior interview level.

## 10. Visualization

Dashboards show metrics across timeframes (server requests, memory/CPU, page load time, traffic, logins) plus current alerts. Quality visualization is hard to build; **Grafana** integrates with most popular TSDBs and is the standard recommendation. Most off-the-shelf options eliminate the need for a custom layer.

## Sources

- [Vol 2 Ch 5: Metrics Monitoring and Alerting System](software/system-design-interview/books/system-design-interview-vol2/ch05_metrics_monitoring_alerting.md)
