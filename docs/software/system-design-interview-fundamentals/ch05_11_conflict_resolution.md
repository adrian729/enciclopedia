# Ch 5.11: Conflict Resolution

## Table of Contents

- [1. Why Conflicts Arise](#1-why-conflicts-arise)
- [2. Last Write Wins](#2-last-write-wins)
- [3. Conflict-Free Replicated Data Type (CRDT)](#3-conflict-free-replicated-data-type-crdt)
- [4. Keep Records of the Conflict](#4-keep-records-of-the-conflict)
- [5. Custom Conflict Resolution](#5-custom-conflict-resolution)

## 1. Why Conflicts Arise

- **Source** — multiple writers hit the same key on different nodes simultaneously under leaderless or leader-leader replication; the system must decide whose write sticks
- **Analogy** — like a git merge: two engineers branch from the same code and both modify it; reconciling the edits is non-trivial
- **Goal** — resolution strategy must continue to deliver a good end-user experience for the specific application

## 2. Last Write Wins

- **Mechanism** — attach a timestamp to each write; on conflict, the write with the latest timestamp wins
- **Lossy** — the "losing" write disappears
- **Clock-skew caveat** — a later wall-clock timestamp isn't guaranteed to be causally later from the same user's perspective
- **When to use** — practical and simple for many applications where occasional losses are acceptable

## 3. Conflict-Free Replicated Data Type (CRDT)

- **Mechanism** — each node tracks its own count plus the counts of other nodes; nodes replicate their tallies to each other, and any node can compute the total by summing across nodes
- **Example** — a global distributed counter across `node_1`, `node_2`, `node_3`: writes to `node_1` increment only `node_1`'s count; `node_1` asynchronously replicates that count to the others; each node sums its view to answer a read
- **Advantage** — any node can serve reads (high availability), read latency stays low (no scatter-gather across all nodes)
- **Disadvantage** — broadcasting complexity; the total is **eventually consistent** under async replication
- **Other uses** — resolving Google Docs operations. Useful in interview questions about distributed counters or Google Docs

## 4. Keep Records of the Conflict

- **Mechanism** — don't resolve automatically; persist all conflicting values, and let the application decide on read
- **Example** — `node_1` has `"animal": "dog"` and `node_2` has `"animal": "cat"`; on reconciliation, the key holds `["dog", "cat"]` and the application chooses what to do
- **Advantage** — not lossy; retains all the conflicting information
- **Disadvantage** — every subsequent reader now has to handle conflict-resolution logic

## 5. Custom Conflict Resolution

- **Domain-specific resolution** — pick a strategy that fits the application semantics
- **Example: manual merge** — a code merge conflict in source control isn't resolved by the system; the engineer resolves it by hand, because automatic code merging is too risky
