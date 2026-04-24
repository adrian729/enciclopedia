# Ch 5.13: Resilience Patterns

## Table of Contents

- [1. Timeout](#1-timeout)
- [2. Exponential Backoff](#2-exponential-backoff)
- [3. Buffering](#3-buffering)
- [4. Sampling](#4-sampling)
- [5. Fail to Open](#5-fail-to-open)

## 1. Timeout

- **You can't detect true failure in a distributed system** — a missing response may be network congestion, a slow server, slow dependencies, or a dead host; the client must not block forever or it burns its own resources waiting
- **Timeout converts uncertainty into a decision** — mark the request as a timeout failure so the client can move on (e.g., retry)
- **Core trade-off** — a longer timeout wastes resources when a service is genuinely down; a shorter one risks giving up on a response that would have arrived moments later (and then retrying, possibly timing out again)
- **Example** — processing takes 1 minute but timeout is 50 seconds: you wasted 50 seconds and must retry, when waiting 10 more seconds would have returned the result. Conversely, if the service is truly dead, you only waited 50 seconds
- **Ideal vs reality** — ideally the timeout equals the request's processing time, but you never know that number up front
- **End-user angle** — in an interview, discuss how timeout affects user experience; a long timeout in a ridesharing service makes the user wait before seeing "please try again," which is frustrating
- **Other uses** — service discovery uses timeouts to decide which hosts are still available (adding/removing machines from shards); leader-health checks use timeouts to decide when to elect a new leader; longer timeout = slower failure detection, shorter timeout = falsely declaring a live node unavailable

## 2. Exponential Backoff

- **When to use** — downstream errors that may go away on their own: server busy from a traffic spike, a bug about to be rolled back, transient network congestion causing a timeout
- **Retry without backoff snowballs** — frequent retries pile more requests on an already-struggling downstream
- **Exponential backoff with maximum retry** — wait progressively longer between retries, and stop after a cap; hitting the cap usually means the failure is real and manual intervention is needed
- **Tuning trade-off** — a bigger backoff delays processing but eases pressure on the downstream; a smaller backoff recovers faster when the service is back, at the cost of more load on the downstream
- **Interview signal** — raise this when discussing temporary first or third-party downstream failures

## 3. Buffering

- **Used for throughput problems** — each client-to-datastore request carries non-trivial overhead: TCP connection setup, load balancer, internal RPC calls, disk IO, etc.
- **Batch to amortize overhead** — instead of sending one data point at a time, wait a second and collect hundreds of points before sending them in a single request (e.g., emitting metrics data)
- **Trade-off: throughput vs freshness** — the longer you wait, the less overhead per request, but data arrives staler; if freshness is an important non-functional requirement, tune the buffer size accordingly

## 4. Sampling

- **When accuracy can be traded for performance** — if the interviewer agrees complete accuracy isn't required, reducing the amount of data processed reduces compute and storage
- **Interview prompt** — when discussing high QPS or storage bottlenecks, look for places where less data still yields a good user experience
- **Reduce storage — ridesharing route example** — the driver's phone sends a location update every 5 seconds; instead of persisting every one, sample a fraction. You cut QPS and storage by that same fraction; the ride-path replay loses some granularity, which riders typically don't need in detail
- **Reduce computation — recommendations example** — when finding similar users for a recommendation, don't search the whole user base; narrow the search space to a sample. Works when the sample is large enough to be statistically significant

## 5. Fail to Open

- **The idea** — standard failure talk (redundant storage/service, election, manual failover) still costs real time and isn't always smooth. "Fail to open" means keeping the user experience *perceived as available* with a backup behavior, even when the ideal path is broken
- **Interview approach** — offer options, discuss trade-offs, and pick one that preserves a good user experience
- **Faulty Payment Processor** — e-commerce checkout: if the payment processor is down, let the order through and collect the money later instead of dropping the order and losing revenue. Trade-off: risk of not collecting later (fraud, expired payment) vs much better checkout availability
- **Faulty Storage** — when a storage node is down, stash the write on another node temporarily; when the original is back, the holder transfers the data over. Seen in Cassandra **hinted handoff** and in consistent hashing where a neighboring node takes the write. Trade-offs: inconsistency (Cassandra hinted handoff), extra load (consistent hashing)
- **Faulty Price Estimate** — ridesharing price calculator is down: call a backup service using similar historical data, or return the baseline price without the surge multiplier. Trade-off: preserves availability at the cost of revenue loss from the missing surge multiplier
