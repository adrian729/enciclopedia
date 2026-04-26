# Ch 5: Replicated Load-Balanced Services

## Table of Contents

- [1. Pattern Definition](#1-pattern-definition)
- [2. Stateless Services](#2-stateless-services)
  - [2.1. Readiness Probes](#21-readiness-probes)
  - [2.2. Hands-On: Replicated Service in Kubernetes](#22-hands-on-replicated-service-in-kubernetes)
- [3. Session Tracked Services](#3-session-tracked-services)
- [4. Application-Layer Refinements](#4-application-layer-refinements)
  - [4.1. Caching Layer](#41-caching-layer)
  - [4.2. Rate Limiting](#42-rate-limiting)
  - [4.3. SSL Termination](#43-ssl-termination)
  - [4.4. Hands-On: Caching and SSL](#44-hands-on-caching-and-ssl)

## 1. Pattern Definition

- **Replicated load-balanced service** — the simplest distributed pattern: a scalable number of identical servers behind a load balancer that distributes traffic round-robin or with session stickiness; every replica can serve every request.

## 2. Stateless Services

- **Stateless service** — a service that requires no saved state to operate correctly; in the simplest cases even individual requests from one user can be routed to different instances. Examples: static content servers and middleware that aggregates responses from backend systems.
- **Why two replicas minimum** — a "three-nines" SLA (99.9% availability) allows only 1.4 minutes of downtime per day; with a single instance, every rollout must finish inside that budget. With continuous delivery (e.g., hourly pushes), a single-instance rollout would have to complete in 3.6 seconds. Two replicas behind a load balancer make rollouts and crashes invisible to users.
- **Horizontal scaling** — handling more users by adding more replicas; the load-balanced replicated serving pattern is the mechanism that makes this work.

### 2.1. Readiness Probes

- **Readiness probe** — distinct from a health probe: a health probe tells the orchestrator when to restart, a readiness probe tells the load balancer when an instance is *ready to serve user requests*. Containers may be alive but not yet ready (loading plugins, connecting to a database, downloading serving files). Build a dedicated URL into the application that implements the readiness check.

### 2.2. Hands-On: Replicated Service in Kubernetes

- **Demo** — deploy `brendanburns/dictionary-server` (a NodeJS dictionary server that downloads ~8 MB of data before reporting ready) as a Kubernetes `Deployment` with three replicas, an HTTP `readinessProbe` on `/ready`, and a `Service` object as the load balancer providing a stable name independent of any specific replica.

## 3. Session Tracked Services

- **Session tracked services** (a.k.a. session affinity) — an adaptation of the stateless pattern where all requests from a single user are routed to the same replica. Used when caching per-user data in memory raises the hit rate, or when an interaction is long-running and carries state between requests.
- **IP-based session tracking** — typical implementation hashes source and destination IP to pick the replica; works inside a cluster but breaks across NAT for external users, where cookie- or header-based application-level tracking is preferred.
- **Consistent hashing function** — special hash used so that scaling the replica count up or down only remaps a small fraction of users to a different replica, instead of reshuffling almost everyone.

## 4. Application-Layer Refinements

- **Application-layer replication** — knowing the protocol (typically HTTP) lets the load-balancing tier do more than blind TCP/IP forwarding. Caching, rate limiting, and SSL termination all live in this tier.

### 4.1. Caching Layer

- **Caching web proxy** — an HTTP server in front of the stateless backend that holds prior responses in memory; identical requests from different users are served from the cache, sparing the backend. Book uses Varnish.
- **Sidecar caching disadvantage** — deploying the cache as a sidecar next to each web server forces the cache to scale at the same rate as the application; every page is duplicated across every replica, shrinking the working set in memory and dropping the **hit rate** (fraction of requests served from cache).
- **Separate caching tier** — prefer few large cache replicas (e.g., two with 5 GB each) over many small ones (ten with 1 GB each). Web servers stay numerous and small to use multiple cores in single-threaded runtimes like NodeJS, while caches stay few and fat to maximize unique pages held in memory.
- **Caching breaks IP-based session tracking** — once requests pass through a small set of caches, the backend sees only the caches' IPs; affinity must move to cookies or HTTP headers, otherwise some web replicas may receive no traffic at all.

### 4.2. Rate Limiting

- **Rate limiting** — denial-of-service defense added at the caching layer; protects against both deliberate attacks and accidents (a misconfigured client, an SRE running a load test against production). Varnish's `throttle` module limits by IP, request path, and login state.
- **Anonymous vs. logged-in limits** — keep anonymous limits low and force login for higher quotas; login provides auditing for unexpected load and forces attackers to obtain multiple identities.
- **Surfacing the limit** — when limits are hit return HTTP `429`; expose remaining quota in a header (no standard exists, but variations of `X-RateLimit-Remaining` are common) so well-behaved clients can self-throttle.

### 4.3. SSL Termination

- **SSL termination** — terminating HTTPS at an edge layer before traffic reaches caches and backends. Each layer (edge, internal services) should use its own certificate so layers can roll out independently. Varnish cannot terminate SSL, so an additional replicated `nginx` tier sits in front: nginx terminates HTTPS and proxies plaintext to Varnish, which forwards to the application.

### 4.4. Hands-On: Caching and SSL

- **Demo** — extend the dictionary service into a three-tier replicated serving stack on Kubernetes: a Varnish `Deployment` (configured via `ConfigMap`, backed by a `Service`) caches responses from the dictionary backend, and a replicated nginx `Deployment` in front of Varnish loads a TLS certificate from a `Secret` to terminate HTTPS, exposed externally via a `LoadBalancer`-type `Service`.
