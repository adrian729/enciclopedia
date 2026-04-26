# Web Crawler

> Xu's Ch 9 only. The interesting components are the **URL Frontier** (politeness + priority queues), deduplication (29% of the web is duplicate), and robustness against spider traps.

## Table of Contents

- [1. Requirements](#1-requirements)
- [2. The Search Strategy — BFS, Not DFS](#2-the-search-strategy--bfs-not-dfs)
- [3. Components](#3-components)
- [4. URL Frontier](#4-url-frontier)
  - [4.1. Politeness](#41-politeness)
  - [4.2. Priority](#42-priority)
- [5. Deduplication](#5-deduplication)
- [6. Robustness](#6-robustness)
- [7. Trade-offs](#7-trade-offs)
- [Sources](#sources)

## 1. Requirements

- Discover and fetch pages on the web at scale.
- Honor `robots.txt`.
- Avoid re-crawling unchanged content.
- Respect host bandwidth (politeness).
- Prioritize important or fast-changing pages.

## 2. The Search Strategy — BFS, Not DFS

DFS goes unbounded depth in a single subtree before exploring siblings; on the web, that means descending into one host's deep content before crawling any other site. **BFS** explores breadth-first — but most outgoing links from a page point back to the *same host*, which means naive BFS still concentrates traffic on one host. The **politeness** mechanism in the URL Frontier fixes this.

## 3. Components

```
Seed URLs
   ↓
URL Frontier ← URL Filter ← URL Extractor
   ↓                              ↑
HTML Downloader (with DNS cache)
   ↓
Content Parser
   ↓
"Content Seen?" Deduplicator → Content Storage
   ↓
URL Extractor → "URL Seen?" Tracker (bloom filter or hash table)
                            ↓
                       URL Filter → URL Frontier
```

Each box is independently scaled and runs over consistent-hashed pools of workers.

## 4. URL Frontier

The **URL Frontier** is a FIFO queue of URLs to download — but with two structural refinements that make crawling polite and prioritized.

### 4.1. Politeness

One page at a time per host, with a delay between fetches. Implemented via **per-host queues**: each host has its own queue, and the downloader pulls from one host's queue at a time, then sleeps before fetching another from the same host. Hosts with many pending URLs get serviced in round-robin without overwhelming any single host.

### 4.2. Priority

Higher-PageRank or more-frequently-updated URLs go first. Implemented via **priority queues** that feed the per-host queues. The classifier upstream of the priority queue decides where to put new URLs.

## 5. Deduplication

Two distinct dedup steps:

- **URL dedup** — has this URL already been seen? Bloom filter (probabilistic, low memory) or hash table (exact, more memory).
- **Content dedup** — has this *content* already been seen? Hash the page content; compare hashes (not characters). 29% of the web is duplicate content, per Xu — without content dedup, the index is bloated and crawl bandwidth wastes on copies.

## 6. Robustness

- **Robots.txt** must be honored. Cached per host with reasonable TTL.
- **DNS resolution** is a 10–200 ms blocking call; a local **DNS cache** shaves it for repeat hosts.
- **Spider traps** — pages that generate infinite URLs (a calendar with `?date=` parameters, an infinite paginator). No general algorithm exists; mitigations are pragmatic: cap URL length, blacklist domains by hand, set per-host crawl quotas.
- **Persisted crawl state** — restart from where you left off, not from scratch.
- **Consistent hashing** across downloaders — when a downloader dies, only its assigned hosts are reassigned. See [Sharding & Consistent Hashing](fundamentals/sharding-and-consistent-hashing.md).
- **Exception handling and data validation** — every component fails sometimes; the pipeline must tolerate it without dropping the whole crawl.

## 7. Trade-offs

- **Bloom filter vs hash table for "URL Seen?"** — bloom filter has false positives (URL marked seen when it wasn't); hash table is exact but uses more memory. At web scale, false-positive rate of 0.1% is acceptable.
- **Crawl freshness vs cost** — re-crawling daily costs 365× annually; weekly costs 52×. Most pages change rarely; smarter scheduling (re-crawl high-change-rate pages more often) cuts cost significantly.
- **Politeness aggression** — too polite means slow crawls; too aggressive means hosts block the crawler. Per-host adaptive backoff is the production answer.

## Sources

- [Xu Ch 9: Design a Web Crawler](software/system-design-interview/books/system-design-interview-insiders-guide/ch09_design_a_web_crawler.md)
