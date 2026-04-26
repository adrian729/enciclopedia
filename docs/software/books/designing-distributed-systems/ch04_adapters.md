# Ch 4: Adapters

## Table of Contents

- [1. Pattern Definition](#1-pattern-definition)
- [2. Monitoring](#2-monitoring)
  - [2.1. Hands-On: Prometheus](#21-hands-on-prometheus)
- [3. Logging](#3-logging)
  - [3.1. Hands-On: Fluentd](#31-hands-on-fluentd)
- [4. Health Monitoring](#4-health-monitoring)
  - [4.1. Hands-On: MySQL Health Adapter](#41-hands-on-mysql-health-adapter)

## 1. Pattern Definition

- **Adapter pattern** — a single-node pattern where an *adapter container* modifies the interface of the *application container* so it conforms to a predefined interface expected by the surrounding system (e.g., a uniform monitoring API or a convention that logs always go to `stdout`).
- **Heterogeneity problem** — real applications mix in-house code, vendor-supplied components, and off-the-shelf binaries written in many languages with different conventions for logging, monitoring, and metrics; common operational tooling needs a single interface to consume.
- **Adapter vs. modifying the app container** — when you own the application, modifying it directly is fine; when reusing a third-party container, deriving and maintaining a patched image is more expensive than running an adapter alongside it, and an external adapter can be shared and reused — a modified image cannot.
- **Resource isolation benefit** — running the adapter as its own container gives it dedicated CPU and memory, so a misbehaving adapter (e.g., a runaway monitoring exporter) cannot starve the user-facing service.

## 2. Monitoring

- **Standardization gap** — `syslog`, Windows ETW, JMX, and many others are all "standard" monitoring interfaces but differ in protocol and push-vs-pull style; a single monitoring stack expects one interface across all apps.
- **Adapter role for monitoring** — the application container exposes whatever monitoring interface it natively offers; the adapter container transforms it into the format the general-purpose monitoring system expects.
- **Decoupling benefit** — rolling out new versions of the application doesn't force a rollout of the monitoring adapter (and vice versa), and the same adapter can be reused across many application containers, sometimes maintained by the monitoring system's authors rather than the app's developers.

### 2.1. Hands-On: Prometheus

- **Prometheus** — an open source monitoring aggregator that collects metrics from every container via a specific `metrics` API, stores them in a time-series database, and provides visualization and a query language on top.
- **Demo summary** — many programs (e.g., Redis) don't natively expose Prometheus's metrics format, so a Kubernetes pod combines the stock `redis` image with the open source `oliver006/redis_exporter` adapter container; the result is a Prometheus-monitorable Redis with no custom code.

## 3. Logging

- **Logging heterogeneity** — apps split logs across debug/info/warning/error files, or write to `stdout`/`stderr`; containerized environments expect `stdout` because that's what `docker logs` and `kubectl logs` surface.
- **Structured-data drift** — log libraries (e.g., Java's built-in logger vs. Go's `glog`) format timestamps and structured fields differently, so a downstream aggregator can't rely on a single schema.
- **Adapter role for logging** — the adapter redirects file-based logs to `stdout` and transforms diverse formats into a single structured representation that the log aggregator can consume, normalizing a heterogeneous fleet into a homogeneous interface.

### 3.1. Hands-On: Fluentd

- **fluentd** — a popular open source logging agent whose key strength is a rich set of community-supported plugins for normalizing many input formats into a common event stream.
- **Redis SLOWLOG demo** — Redis's `SLOWLOG` command lists recent queries that exceeded a time threshold but is only retrievable live on the server; pairing the `redis` container with a `fluentd` adapter running the `fluent-plugin-redis-slowlog` plugin (configured against `localhost:6379` since the containers share a network namespace) turns slow-query history into persistent, queryable logs.
- **Apache Storm demo** — same shape: a `fluentd` adapter with the `fluent-plugin-storm` plugin polls Storm's RESTful API on `localhost:8080` and converts it into a queryable time-series log so problems can be debugged retrospectively.

## 4. Health Monitoring

- **Why richer health checks** — orchestrators provide simple "process running" / "port listening" checks, but operators often want to actually run a representative query against the database to determine real health.
- **Adapter for health checks** — instead of patching the off-the-shelf database container, ship an adapter container holding the health-check shell script (or HTTP server); it shares the network namespace with the database, the orchestrator points its health probe at the adapter, and a failure triggers automatic restart of the database.
- **Versioning win** — the script lives in its own container, so it's versioned and shipped independently of the database image.

### 4.1. Hands-On: MySQL Health Adapter

- **Demo summary** — a small Go program (`brendanburns/mysql-adapter`) takes `--user`, `--password`, `--database`, and `--query` flags, connects to MySQL on localhost, and exposes an HTTP handler that returns 200 OK if the test query succeeds and 500 with the error otherwise; the pod runs the unmodified `mysql` image alongside this adapter, and Kubernetes uses the adapter's HTTP endpoint as the database's health check.
- **Modularity payoff** — anyone could bake health-checking into a custom MySQL image, but a shared adapter container can be reused across teams; users without deep MySQL expertise can adopt someone else's well-tuned health adapter, turning design patterns into a vehicle for community knowledge sharing.
