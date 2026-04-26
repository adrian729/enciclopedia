# Search Autocomplete

> Xu's Ch 13 only — Liu doesn't cover prefix search as a case study. The interesting part is the **trie** with cached top-k completions at every node, plus the data pipeline that rebuilds the trie weekly.

## Table of Contents

- [1. Requirements](#1-requirements)
- [2. Why Not SQL LIKE](#2-why-not-sql-like)
- [3. The Trie](#3-the-trie)
- [4. Optimizations](#4-optimizations)
  - [4.1. Cap Prefix Length](#41-cap-prefix-length)
  - [4.2. Cache Top-K at Every Node](#42-cache-top-k-at-every-node)
- [5. Data-Gathering Pipeline](#5-data-gathering-pipeline)
- [6. Sharding by First Letter](#6-sharding-by-first-letter)
- [7. Delete Filter](#7-delete-filter)
- [8. Trade-offs](#8-trade-offs)
- [Sources](#sources)

## 1. Requirements

- Type-ahead suggestions with sub-100 ms latency.
- Suggestions ranked by popularity.
- Must scale to a search-engine-sized query log.

## 2. Why Not SQL LIKE

`SELECT term FROM queries WHERE term LIKE 'tw%' ORDER BY frequency DESC LIMIT 5` does work, but it's too slow at scale — the query touches potentially millions of rows for every prefix. The 100 ms budget rules it out.

A specialized data structure is needed.

## 3. The Trie

A **trie** (prefix tree) stores strings character-by-character. Each node represents a prefix; descendants extend it. To suggest completions for "tw", walk two edges (`t` then `w`) and the subtree below contains every term starting with "tw".

For ranking, store **frequency on each terminal node** (or each node, depending on representation). Top-k completions are the highest-frequency terms in the subtree.

See [Full-Text Search](fundamentals/full-text-search.md) for the contrast between trie (prefix) and reverse index (full-text).

## 4. Optimizations

### 4.1. Cap Prefix Length

Cap at ~50 characters. Beyond that, the search degrades into a much smaller subtree where the lookup is cheap anyway. This makes worst-case lookup time O(1) — the depth is bounded.

### 4.2. Cache Top-K at Every Node

The naive approach is "walk the subtree, sort by frequency, take top 5." On dense subtrees (popular prefix like "the"), this is too slow.

The optimization: **store the top-k completions at every node**. Lookup becomes O(1) — walk to the node for the prefix, return its cached list.

Trade-off: writes (recomputing top-k as new queries arrive) become expensive. The system side-steps this by **rebuilding the trie weekly** in batch and atomically swapping the new trie in.

## 5. Data-Gathering Pipeline

```
Search queries (real-time stream)
   ↓
Analytics logs (object store)
   ↓
Aggregators (batch — daily or weekly)
   ↓
Workers (build new trie)
   ↓
Trie cache (atomic swap)
   Trie DB (durable copy)
```

Weekly rebuild is fine because the popularity ranking doesn't change much in a week — the long tail is stable. Real-time updates are reserved for edge cases (trending events, new product launches) and applied as overlays.

See [Async, Batch, Stream](fundamentals/async-batch-stream.md) for the batch pattern.

## 6. Sharding by First Letter

Partition the trie by the **first letter** of the prefix:

| Shard | Prefixes |
|---|---|
| Shard A | a, b, c, d, e |
| Shard B | f, g, h, i |
| ... | ... |

Rebalance by **historical query distribution** — far more queries start with "c" than "x", so the "c" shard handles disproportionately more traffic. The shard-to-letter mapping is chosen to even out *traffic*, not letter count.

## 7. Delete Filter

A filter sits in front of the cache to remove offending suggestions before they reach the user. The filter is updated when:

- Moderation flags a term.
- A new offensive term enters the popularity rankings.
- A trademark holder requests removal.

The filter is small enough to fit in memory and is applied on every lookup.

## 8. Trade-offs

- **Weekly rebuild vs real-time** — weekly is cheap and accurate enough for the long tail; real-time costs more and matters only for trending terms. Lambda architecture (both lanes) is the right answer when both are needed.
- **Trie depth cap vs completeness** — capping at 50 chars sacrifices a tiny minority of long queries; in practice, no one types 50-char queries.
- **Top-k per node vs per query** — per-node uses more memory but makes queries trivial; per-query uses less memory but does more work per request.

## Sources

- [Xu Ch 13: Design a Search Autocomplete System](software/system-design-interview/books/system-design-interview-insiders-guide/ch13_design_a_search_autocomplete.md)
