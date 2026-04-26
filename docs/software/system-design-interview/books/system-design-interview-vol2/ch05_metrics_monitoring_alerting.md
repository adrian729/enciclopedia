# Ch 5: Metrics Monitoring and Alerting System

## Table of Contents

- [1. Problem and Scope](#1-problem-and-scope)
- [2. System Components](#2-system-components)
- [3. Time-Series Data Model](#3-time-series-data-model)
- [4. Storage Choice](#4-storage-choice)
- [5. High-Level Design](#5-high-level-design)
- [6. Metrics Collection: Pull vs Push](#6-metrics-collection-pull-vs-push)
- [7. Transmission Pipeline](#7-transmission-pipeline)
- [8. Aggregation Locations](#8-aggregation-locations)
- [9. Query Service](#9-query-service)
- [10. Storage Optimization](#10-storage-optimization)
- [11. Alert System](#11-alert-system)
- [12. Visualization](#12-visualization)

## 1. Problem and Scope

- **Goal** — build an internal (not SaaS) metrics monitoring and alerting system for a large company; out of scope: log monitoring (handled by ELK), distributed tracing, business metrics.
- **Scale** — 100M DAU, 1,000 server pools × 100 machines × 100 metrics ≈ **10M metrics**, 1-year retention.
- **Tiered retention** — raw for 7 days, 1-minute resolution for 30 days, 1-hour resolution for 1 year.
- **Metric examples** — CPU/memory usage, disk consumption, requests/sec, server pool counts, message queue depth.
- **Alert channels** — email, phone, PagerDuty, webhooks (HTTP endpoints).
- **Non-functional requirements** — scalability, low query latency for dashboards/alerts, reliability (don't miss critical alerts), flexibility to integrate new tech later.

## 2. System Components

- **Data collection** — gather metrics from sources.
- **Data transmission** — move metrics from sources to the monitoring system.
- **Data storage** — organize and persist metrics.
- **Alert** — analyze, detect anomalies, fan out notifications.
- **Visualization** — graphs and charts for human pattern recognition.

## 3. Time-Series Data Model

- **Time series** — a value stream uniquely identified by (metric name, set of `<key:value>` labels), with an array of `<value, timestamp>` pairs.
- **Labels enable aggregation** — e.g., compute average `CPU.load` for `region=us-west` by filtering on labels and averaging values.
- **Line protocol** — common input format used by Prometheus and OpenTSDB: `<metric> <labels> <timestamp> <value>` per line.
- **Low-cardinality labels** — InfluxDB best practice: each label should have a small set of possible values; high cardinality breaks indexes.

## 4. Storage Choice

- **Why not general-purpose DBs** — relational DBs aren't optimized for time-series ops (e.g., rolling moving average requires gnarly nested SQL); they choke under constant heavy writes and need an index per tag. NoSQL (Cassandra, Bigtable) can technically work but requires deep internal knowledge to design a scalable schema.
- **Why a dedicated TSDB** — purpose-built engines use far fewer servers, expose time-series-friendly query languages, and bake in retention/aggregation features.
- **Notable TSDBs** — OpenTSDB (Hadoop/HBase-based, complex to run), MetricsDB (Twitter), Amazon Timestream, **InfluxDB** and **Prometheus** (the two most popular per DB-engines). InfluxDB on 8 cores / 32GB RAM handles **>250,000 writes/sec**.
- **Access pattern** — write-heavy and constant; read-heavy and **spiky** (visualization + alerting bursts).
- **Hot data dominance** — Facebook research: **≥85%** of operational queries hit data from the last 26 hours; storage engines that exploit this win.

## 5. High-Level Design

- **Metrics source** — application servers, DBs, message queues.
- **Metrics collector** — gathers data and writes to TSDB.
- **TSDB** — stores time series with label indexes, often via custom query language.
- **Query service** — thin wrapper over TSDB; can be skipped if the TSDB exposes a good native interface.
- **Alerting system** — dispatches to channels.
- **Visualization system** — dashboards.

## 6. Metrics Collection: Pull vs Push

- **Pull model** — dedicated collectors poll each service's `/metrics` HTTP endpoint on a schedule. Service Discovery (etcd, ZooKeeper) feeds collectors the live endpoint list so new servers aren't missed.
- **Multiple collectors** — at scale a single collector can't handle thousands of servers; use a pool with **consistent hashing** so each metrics source maps to exactly one collector (avoiding duplicate pulls).
- **Push model** — a long-running **collection agent** on each server pushes metrics to the collector cluster. Agent may aggregate (e.g., counters per minute) and buffer locally on rejection. Auto-scaling collector cluster behind a load balancer prevents fall-behind.
- **Local buffering caveat** — if servers in an auto-scaling group rotate out, locally buffered metrics may be lost when the collector backs up.

| Dimension | Pull wins | Push wins |
|---|---|---|
| Easy debugging | `/metrics` viewable on demand, even from a laptop | — |
| Health check | Pull failure = clear server-down signal | Missing push could be a network issue |
| Short-lived jobs | — | Batch jobs may finish before being pulled (pull workaround: push gateways) |
| Firewalls / multi-DC | All endpoints must be reachable | LB + auto-scaling can accept from anywhere |
| Performance | TCP | UDP, lower-latency transport |
| Data authenticity | Endpoints pre-configured | Anyone can push (mitigate via whitelisting / auth) |

- **Real-world examples** — Prometheus (pull); CloudWatch, Graphite (push). Large orgs often support both, especially with serverless where agent install isn't possible.

## 7. Transmission Pipeline

- **Auto-scaling collector cluster** — required regardless of pull/push to handle the metric volume.
- **Add Kafka between collector and TSDB** — protects against TSDB unavailability by buffering writes; decouples ingestion from storage; lets stream-processing engines (Storm, Flink, Spark) consume in parallel.
- **Kafka partitioning strategy** — partition by metric name so consumers can aggregate by metric; further partition by tag/label; categorize and prioritize so critical metrics process first.
- **Kafka alternative** — running production Kafka is a serious operational burden; **Facebook's Gorilla** is an in-memory TSDB designed to remain available for writes through partial network failures, arguably as reliable as a Kafka buffer.

## 8. Aggregation Locations

- **Collection agent (client-side)** — only simple aggregations like minute-bucketed counters before send.
- **Ingestion pipeline (pre-storage)** — Flink-style stream processing slashes write volume but loses raw-data precision and complicates late-arriving events.
- **Query side (post-storage)** — no precision loss, full flexibility, but queries run over the full dataset and are slower.

## 9. Query Service

- **Purpose** — decouples TSDB from visualization/alerting clients so either side can change independently; can host a cache layer to relieve TSDB load.
- **Case against** — most industrial visualization/alert tools already have rich plugins for popular TSDBs and a well-chosen TSDB caches well, so a custom query service can be unnecessary abstraction.
- **Custom query languages** — Prometheus and InfluxDB ship their own DSLs because time-series queries are awkward in SQL. Example: an exponential moving average is a deeply nested SQL window query, but in InfluxDB's **Flux** it's `from(...) |> range(...) |> filter(...) |> exponentialMovingAverage(size:-10s)`.

## 10. Storage Optimization

- **Encoding (delta-of-delta)** — store value deltas with one base instead of full values; e.g., timestamps `1610087371, 1610087381, …` become `1610087371, 10, 10, 9, 11`, dropping per-point timestamp from 32 bits to ~4 bits.
- **Compression** — built into good TSDBs; combines with delta encoding for major savings.
- **Downsampling** — convert high-resolution to low-resolution as data ages. Example tier: raw for 7 days, 1-minute for 30 days, 1-hour for 1 year. E.g., six 10-second `cpu` samples (10, 16, 20, 30, 20, 30) roll up to two 30-second averages (19, 25).
- **Cold storage** — inactive, rarely-accessed data moves to cheap cold tiers.

## 11. Alert System

- **Alert rules** — defined in YAML config files (e.g., `instance_down: expr: up == 0, for: 5m, labels: severity: page`); loaded into cache servers.
- **Flow** — alert manager fetches rules from cache → polls query service at the rule's interval → on threshold violation creates an alert event → events filtered/merged/deduped → eligible alerts pushed into Kafka → alert consumers fan out to email/SMS/PagerDuty/HTTP webhooks.
- **Alert store** — a KV DB like **Cassandra** that tracks each alert's state (`inactive / pending / firing / resolved`); guarantees at-least-once notification.
- **Alert manager responsibilities** — filtering, merging duplicates within an instance, retry on failed sends, access control on operations.
- **Build vs buy** — many off-the-shelf alerting systems integrate tightly with TSDBs and notification channels; justifying a custom build (especially at senior interview level) is hard.

## 12. Visualization

- **Dashboards** — show metrics across timeframes (server requests, memory/CPU, page load time, traffic, logins) and current alerts.
- **Build vs buy** — quality visualization is hard to build; **Grafana** integrates with most popular TSDBs and is the standard recommendation. Most off-the-shelf options eliminate the need for a custom layer.
