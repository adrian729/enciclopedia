# Ch 9: Ownership Election

## Table of Contents

- [1. The Ownership Problem](#1-the-ownership-problem)
- [2. When You Don't Need Master Election](#2-when-you-dont-need-master-election)
- [3. Building Blocks: Consensus Stores](#3-building-blocks-consensus-stores)
- [4. Distributed Locks](#4-distributed-locks)
- [5. Long-Lived Ownership via Leases](#5-long-lived-ownership-via-leases)
- [6. Handling Concurrent Data Manipulation](#6-handling-concurrent-data-manipulation)
- [7. Hands-On Exercises](#7-hands-on-exercises)

## 1. The Ownership Problem

- **Ownership** — a specific process owns a specific task (e.g., a particular shard of a sharded keyspace); only one actor may act on that task at a time.
- **Single-server ownership is easy** — a single application can use in-process locks, but a single instance limits scalability (no replication) and reliability (failure means downtime).
- **Distributed ownership** — when ownership must persist across replicas, you need a protocol so that exactly one replica is the master at any moment, and a new master is elected if the current one fails.
- **Master election** — the term used throughout the chapter for the process of selecting (and re-selecting) the owner replica; often the most complicated and most important part of designing a reliable distributed system.

## 2. When You Don't Need Master Election

- **Singleton pattern** — run a single replica; it implicitly owns everything without election. Simpler to build and deploy at the cost of downtime.
- **Orchestrator-provided guarantees** — a singleton on Kubernetes gets automatic restart on crash, automatic restart on failed health check, and rescheduling onto another machine if its node fails.
- **Uptime estimate** — a container that crashes once a day and restarts in a few seconds gives roughly three to four nines (2 s of downtime/day ~= 99.99%); whole-machine failure plus a ~5-minute reschedule yields ~two nines if every machine fails daily.
- **Deployment is the dominant cost** — a singleton cannot run old and new versions concurrently; a 2-minute daily upgrade caps you at two nines, an hourly upgrade drops below one nine. Pre-pulling images speeds this up but adds complexity.
- **When singletons are fine** — background asynchronous processing and other workloads where simplicity beats high availability; reach for master election only when four+ nines really matter.

## 3. Building Blocks: Consensus Stores

- **Two paths to master election** — implement a distributed consensus algorithm yourself (Paxos, RAFT) or build on a key-value store that has already implemented one. Rolling your own is akin to implementing locks on top of assembly-code compare-and-swap instructions — an academic exercise, not production work.
- **Distributed key-value stores** — etcd, ZooKeeper, and consul provide a replicated reliable store plus the primitives needed to build locking and election abstractions.
- **Compare-and-swap (CAS)** — atomic primitive that writes a new value for a key only if the current value matches the expected value; returns false on mismatch, error if the key is missing but a non-null current value was supplied.
- **Time-to-live (TTL)** — the store can attach an expiry to a key so it auto-clears once the TTL elapses. CAS plus TTL is sufficient to build the synchronization primitives the rest of the chapter needs.

## 4. Distributed Locks

- **Mutex over a key-value store** — model the in-memory mutual exclusion lock by treating a named key as the lock; CAS `"1"` over `"0"` to acquire, CAS `"0"` over `"1"` to release.
- **First-acquire bootstrap** — if the key doesn't yet exist, fall back to CAS-ing `"1"` against a non-existent value so the very first caller can claim the lock.
- **Blocking acquire via watches** — naive sleep-poll always wastes up to the poll interval after release; key-value stores expose `waitForChanges` so the locker can block until the key changes instead of polling.
- **Crash safety needs TTL** — if a holder dies mid-critical-section there is no one to release; writing the lock with a TTL guarantees auto-release after the timeout.
- **Watchdog timer** — when acquiring a TTL lock, set a watchdog that crashes the process if the TTL elapses before `unlock` is called, so work never outlives its lock.
- **TTL introduces a stale-unlock bug** — Process-1's TTL expires, Process-2 takes the lock, then Process-1's late `unlock` releases someone else's lock and Process-3 grabs it; now two replicas believe they are owner.
- **Resource version fix** — every store write returns a *resource version*; record it on lock and require both expected value and matching resource version on unlock so a stale holder can't release a successor's lock.

## 5. Long-Lived Ownership via Leases

- **Why locks aren't enough** — some roles (e.g., the active Kubernetes scheduler in an HA deployment) must remain owner for the lifetime of the process, not just a short critical section.
- **Long TTL is wrong** — extending the lock TTL to a week means a week of unavailability if the holder dies; the system needs faster failover than that.
- **Renewable lock (lease)** — extend the basic lock with a `renew()` operation that CAS-updates the same value with a fresh TTL, so the holder keeps ownership as long as it keeps renewing.
- **Renew at TTL/2** — a background thread renews every `ttl/2` seconds, leaving margin for clock skew and scheduling jitter so the lease doesn't accidentally expire.
- **`handleLockLost()`** — the renewal loop must define what to do when renewal fails; in a container orchestrator the cleanest action is to terminate the process and let the orchestrator restart it as a secondary waiting for the lease.

## 6. Handling Concurrent Data Manipulation

- **Two-master windows still exist** — even with TTL leases, an over-scheduled CPU stall can leave a stale holder briefly believing it owns the lock after another replica has already taken over.
- **Local pre-check** — `isLocked()` verifies the lock is still held and that current time is below `lockTime + 0.75 * ttl` before running guarded code; reduces but does not eliminate the window.
- **Server-side double-check** — the called service consults the lock store on each request and rejects writes from a replica that is no longer the recorded owner; the lock store records the owner's hostname for this purpose.
- **Reordered-request hazard** — an in-flight request `R1` from a former master may arrive after that replica re-acquires ownership, so a naive owner-only check still admits a stale request whose successor's `R2` already executed.
- **Resource version on every request** — attach the lock's resource version to each request `(R1, Version1)`; the receiver validates both current owner and version, rejecting requests whose version no longer matches.

## 7. Hands-On Exercises

- **Deploying etcd** — install Helm, run the etcd operator chart, then declare a `Cluster` custom resource with `size: 3` to provision a three-replica etcd cluster on Kubernetes.
- **Operators** — an in-cluster program that creates, scales, and maintains a specific application via a desired-state API; the etcd operator manages etcd itself.
- **Locks in etcd** — create a key `my-lock` with value `unlocked`, then use `etcdctl set --swap-with-value` so Alice's CAS succeeds while Bob's fails until Alice writes `unlocked` back.
- **Leases in etcd** — use `etcdctl mk --ttl=10` so absence of the key means unlocked; the holder reasserts the value with `set --ttl=10 --swap-with-value` before each TTL elapses to extend the lease.
