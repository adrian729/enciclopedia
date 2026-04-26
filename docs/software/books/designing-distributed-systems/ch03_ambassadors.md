# Ch 3: Ambassadors

## Table of Contents

- [1. Pattern Definition](#1-pattern-definition)
- [2. Sharding a Service](#2-sharding-a-service)
  - [2.1. Sharding Ambassador Proxy](#21-sharding-ambassador-proxy)
  - [2.2. Hands-On: Sharded Redis](#22-hands-on-sharded-redis)
- [3. Service Brokering](#3-service-brokering)
- [4. Experimentation and Request Splitting](#4-experimentation-and-request-splitting)

## 1. Pattern Definition

- **Ambassador pattern** — a single-node, two-container pairing where an *ambassador container* brokers all interactions between the *application container* and the outside world; both are co-scheduled on the same machine in a symbiotic group.
- **Value of the pattern** — separation of concerns produces modular, reusable containers; the ambassador can be paired with many different applications, and is built once but reused many times, raising consistency and quality.
- **Localhost contract** — the application always connects to "the service" on localhost, unaware of the real topology; the ambassador owns all environment- and topology-specific logic.

## 2. Sharding a Service

### 2.1. Sharding Ambassador Proxy

- **Sharding** — splitting a storage layer into multiple disjoint pieces, each hosted on a separate machine, when data outgrows a single node.
- **Retrofit problem** — existing client code expects to talk to a single backend, so wiring it to a sharded service is painful; environment differences (one shard in dev, many in prod) compound the issue.
- **Sharding ambassador proxy** — an ambassador container that exposes what looks like a single storage backend on localhost, then routes each request to the correct shard and returns the result; the application stays oblivious to sharding.
- **Server-side vs. client-side ambassador** — sharding logic can live in a stateless load balancer in front of the shards (a "distributed ambassador as a service") or in a client-side ambassador; the choice depends on team boundaries and whether you control the sharded service code or only deploy off-the-shelf.

### 2.2. Hands-On: Sharded Redis

- **Demo summary** — deploys three Redis shards via a Kubernetes `StatefulSet` (giving each replica a stable DNS name like `sharded-redis-0.redis`), then runs Twitter's open source `twemproxy` as the ambassador container in the application's pod, listening on `127.0.0.1:6379` and fanning requests across the shards via a `ConfigMap`-mounted config.

## 3. Service Brokering

- **Portability problem** — the same application must run across public cloud, private cloud, and physical datacenters where the same dependency (e.g., MySQL) is provisioned differently — SaaS in one environment, a freshly spun-up VM or container in another.
- **Service discovery** — the process of inspecting the environment to locate the appropriate instance of a dependency to connect to.
- **Service broker** — the component that performs service discovery and links the application to the discovered service.
- **Service broker ambassador** — an ambassador implementation of the service broker; the app connects to the dependency on localhost, and the ambassador introspects the environment and brokers the real connection, isolating environment-specific logic from application logic.

## 4. Experimentation and Request Splitting

- **Request splitting** — sending some fraction of traffic to an alternative implementation of a service instead of the main production version, typically to test a new beta version's reliability and performance.
- **Tee-ing traffic** — duplicating requests so they hit both the production system and an undeployed version; the production response is returned to the user and the experimental response is discarded, simulating production load on the new version with no user-visible risk.
- **Request-splitting ambassador** — the application connects to localhost; the ambassador receives requests, proxies them to production and experimental backends, and returns the production response to the caller, keeping each container's code slim and reusable.
- **Hands-On: 10% experiments with nginx** — uses an `nginx` ambassador container with an `upstream` block weighting `web` at 9 and `experiment` at 1 (90/10 split), and `ip_hash` to pin each user to a single backend so they get a consistent experience instead of flip-flopping; deployed via a Kubernetes `ConfigMap` alongside the application pod.
- **Tradeoff: ambassador vs. standalone microservice** — request splitting can also live as a separate microservice in front of the app; that adds an extra service to maintain, scale, and monitor, so it pays off only when experimentation is a long-standing architectural component — for occasional use, the client-side ambassador is lighter weight.
