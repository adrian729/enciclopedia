# Search

> Liu's Ch 5.22 covers the full-text-search pipeline (tokenization, reverse index, ranking). Xu's Ch 13 covers prefix-search via the **trie** for autocomplete. Different problems with different data structures — both are interview-relevant.

## Table of Contents

- [1. Two Different Problems](#1-two-different-problems)
- [2. Full-Text Search](#2-full-text-search)
  - [2.1. Text-to-Token Pipeline](#21-text-to-token-pipeline)
  - [2.2. Reverse Index](#22-reverse-index)
  - [2.3. N-Grams](#23-n-grams)
  - [2.4. Multi-Term Query](#24-multi-term-query)
  - [2.5. Ranking](#25-ranking)
  - [2.6. Pipeline Architecture](#26-pipeline-architecture)
- [3. Prefix Search via Trie](#3-prefix-search-via-trie)
  - [3.1. The Data Structure](#31-the-data-structure)
  - [3.2. Optimizations](#32-optimizations)
  - [3.3. Sharding the Trie](#33-sharding-the-trie)
- [4. Choosing Between Them](#4-choosing-between-them)
- [Sources](#sources)

## 1. Two Different Problems

| Problem | Data structure | Example |
|---|---|---|
| Find documents that contain words | Reverse index | Search engine, Slack message search |
| Suggest completions for a prefix | Trie | Type-ahead, autocomplete |

The first is *full-text search* (Liu's territory); the second is *prefix search* (Xu's territory). The data structures are not interchangeable.

## 2. Full-Text Search

### 2.1. Text-to-Token Pipeline

Standard preprocessing before indexing:

1. **Normalize** — lowercase, strip punctuation, collapse whitespace.
2. **Tokenize** — split into words (or sub-word units for compound languages).
3. **Remove stop words** — "the", "is", "at" — they don't help the index.
4. **Stem** — "running" → "run", "addressed" → "address". Reduces variants to a canonical form.

The same pipeline runs at index time and at query time.

### 2.2. Reverse Index

The core index is a map from each token to its **posting list** of document IDs:

```
"design" → [doc_3, doc_47, doc_103, ...]
"system" → [doc_1, doc_3, doc_47, ...]
```

A query for `"system design"` intersects the two posting lists.

### 2.3. N-Grams

For phrase queries, n-grams (typically bigrams and trigrams) are indexed alongside unigrams:

```
"system design" → [doc_3, doc_47, ...]
```

This lets `"system design"` hit one entry instead of intersecting two posting lists, at the cost of larger index size. The trade-off depends on the workload.

### 2.4. Multi-Term Query

Combining posting lists is a **k-way merge** problem. With sorted posting lists, the merge is linear in the total list length. Modern engines (Elasticsearch, Lucene) use skip lists and bitmap intersections to accelerate.

### 2.5. Ranking

- **TF-IDF** — Term Frequency × Inverse Document Frequency. TF rises with how often the token appears in a document; IDF rises with how rare the token is in the corpus. Common tokens get low IDF weight; document-specific tokens score highly.
- **PageRank** — extends TF-IDF for the web by propagating weight through inbound links. A page linked by many authoritative pages ranks higher than the same content with no inbound links.
- **Modern rankers** — BM25, learned-to-rank, neural rerankers — extend the same idea with more features.

### 2.6. Pipeline Architecture

Index building follows freshness:

- **Real-time** — stream-process every document as it's created. Highest cost; lowest staleness.
- **Periodic** — batch-rebuild the index every N hours. Cheap; up to N hours stale.
- **Lambda** — both. The hot index serves recent documents; the batch-built index serves the long tail.

See [Async, Batch, Stream](fundamentals/async-batch-stream.md) for the underlying trade-off.

## 3. Prefix Search via Trie

### 3.1. The Data Structure

A **trie** (prefix tree) stores strings character-by-character. Each node represents a prefix; descendants extend the prefix. Looking up "tw" walks two edges — `t` then `w` — and the subtree below contains every string starting with "tw".

For autocomplete, frequency is stored on each node (or each terminal node) so completions can be ranked.

### 3.2. Optimizations

A naive top-k traverse-and-sort is too slow on dense subtrees (a popular prefix can have millions of completions). Two optimizations make Xu's autocomplete sub-100 ms:

1. **Cap prefix length** to ~50 characters. Beyond that, the search degrades to a much smaller subtree.
2. **Cache the top-k completions at every node.** Lookup becomes O(1) instead of "walk the subtree, sort by frequency."

The trade-off: writes (recomputing top-k as queries arrive) become expensive. The chapter side-steps this by rebuilding the trie weekly in batch (see [Async, Batch, Stream](fundamentals/async-batch-stream.md)) and atomically swapping the new version in.

### 3.3. Sharding the Trie

Partition by the **first letter** of the prefix. Rebalance by historical query distribution: more queries start with "c" than "x", so the "c" shard handles more traffic and may be split further; the "x" shard might be merged with another small shard.

A delete filter sits in front of the cache to remove offending suggestions before they reach the user.

## 4. Choosing Between Them

| Need | Pick |
|---|---|
| Find documents matching a query | Reverse index (Elasticsearch, Solr) |
| Type-ahead, prefix completion | Trie (custom or Xu's design) |
| Both (search + autocomplete) | Run both — they're independent systems |

Many production systems run both side-by-side: an Elasticsearch cluster for full-text search and a separate trie service for autocomplete on the search box.

## Sources

- [Liu Ch 5.22: Full-Text Search](software/system-design-interview/books/system-design-interview-fundamentals/ch05_22_full_text_search.md)
- [Xu Ch 13: Design a Search Autocomplete System](software/system-design-interview/books/system-design-interview-insiders-guide/ch13_design_a_search_autocomplete.md)
