# Ch 9: Design a Web Crawler

## Table of Contents

- [1. Purpose and Use Cases](#1-purpose-and-use-cases)
- [2. Requirements and Scale](#2-requirements-and-scale)
- [3. Characteristics of a Good Crawler](#3-characteristics-of-a-good-crawler)
- [4. High-Level Components](#4-high-level-components)
- [5. Crawler Workflow](#5-crawler-workflow)
- [6. DFS vs BFS](#6-dfs-vs-bfs)
- [7. URL Frontier](#7-url-frontier)
- [8. HTML Downloader](#8-html-downloader)
- [9. Robustness](#9-robustness)
- [10. Extensibility](#10-extensibility)
- [11. Detect and Avoid Problematic Content](#11-detect-and-avoid-problematic-content)
- [12. Additional Talking Points](#12-additional-talking-points)

## 1. Purpose and Use Cases

- **Web crawler** — a robot/spider that starts from seed URLs, downloads pages, extracts links, and follows them to collect new content; the engine behind every search index
- **Search engine indexing** — the most common use case (e.g., Googlebot builds Google's local index)
- **Web archiving** — preserving sites for the future, e.g., the US Library of Congress and the EU Web Archive
- **Web mining** — extracting knowledge at scale, e.g., financial firms crawling shareholder meetings and annual reports
- **Web monitoring** — detecting copyright/trademark infringement, e.g., Digimarc scanning for pirated works

## 2. Requirements and Scale

- **Clarify scope first** — purpose (search indexing), scale (1B pages/month), content type (HTML only), freshness (recrawl new/edited pages), retention (5 years), dedupe policy (ignore duplicate content)
- **Back-of-envelope** — 1B pages/month → ~400 QPS, peak 800 QPS; avg page 500 KB → 500 TB/month; 5 years → 30 PB total storage

## 3. Characteristics of a Good Crawler

- **Scalability** — billions of pages exist, so crawling must be heavily parallelized
- **Robustness** — must survive bad HTML, unresponsive servers, crashes, malicious links, and other web traps
- **Politeness** — must throttle requests to a single host to avoid acting like a DoS attack
- **Extensibility** — new content types (images, PDFs, video) should plug in without redesigning the system

## 4. High-Level Components

- **Seed URLs** — starting points; pick by locality (per-country popular sites) or by topic (shopping, sports, healthcare) to cover the URL space broadly
- **URL Frontier** — FIFO queue of URLs still to download; the boundary between "to crawl" and "already crawled"
- **HTML Downloader** — fetches pages over HTTP using URLs from the Frontier
- **DNS Resolver** — translates hostnames to IPs (e.g., `www.wikipedia.org` → `198.35.26.96`)
- **Content Parser** — parses and validates downloaded pages; runs as a separate component because doing it on the crawler would slow downloads
- **Content Seen?** — dedupe check against previously stored pages; ~29% of the web is duplicate content, so comparing **hash values** (not character-by-character) is essential for speed
- **Content Storage** — most HTML on disk (data set is too big for RAM); popular content kept in memory for low-latency access
- **URL Extractor** — pulls links from HTML; converts relative paths to absolute URLs (e.g., prepend `https://en.wikipedia.org`)
- **URL Filter** — drops blacklisted sites, error links, and unwanted file extensions/content types
- **URL Seen?** — tracks URLs already visited or already in the Frontier to prevent re-crawling and infinite loops; implemented with a **bloom filter** or hash table
- **URL Storage** — persists already-visited URLs

## 5. Crawler Workflow

1. Add seed URLs to URL Frontier
2. HTML Downloader pulls URLs from Frontier
3. Resolves IPs via DNS Resolver and downloads pages
4. Content Parser parses and checks for malformed HTML
5. Pass parsed content to Content Seen?
6. If already stored, discard; otherwise hand off to Link Extractor
7. Link Extractor pulls outgoing links
8. Links go through URL Filter
9. Filtered links go to URL Seen?
10. If already known, drop them
11. Otherwise add new URLs back into the URL Frontier

## 6. DFS vs BFS

- **Web as directed graph** — pages are nodes, hyperlinks are edges; crawling = graph traversal
- **DFS rejected** — depth can be effectively unbounded, so DFS is unsuitable
- **BFS via FIFO queue** — standard choice, but has two problems on the raw web:
  - **Host concentration** — most links on a page point back to the same host (e.g., all internal Wikipedia links), flooding that host with parallel requests ("impolite")
  - **No prioritization** — vanilla BFS treats every URL equally, ignoring page rank, traffic, and update frequency

## 7. URL Frontier

- **Politeness** — avoid bombarding a host; rule of thumb is one page at a time per host with a delay between requests
- **Politeness design** — a **queue router** routes URLs into per-host FIFO queues (b1…bn), a **mapping table** maps host → queue, a **queue selector** assigns each worker thread to one queue, and each **worker thread** downloads sequentially from that single host
- **Priority** — not all URLs are equal (Apple home page outranks an Apple forum post)
- **Prioritizer** — computes URL priority by **PageRank**, traffic, update frequency, etc.
- **Priority design** — multiple priority queues (f1…fn); the queue selector picks higher-priority queues with higher probability
- **Two-module frontier** — **front queues** manage prioritization, **back queues** manage politeness
- **Freshness** — the web changes constantly, so periodically recrawl; optimize by recrawling based on observed update history and prioritizing important pages
- **Storage** — frontier can hold hundreds of millions of URLs; pure RAM is not durable/scalable, pure disk is too slow, so use a **hybrid**: bulk on disk, in-memory enqueue/dequeue buffers flushed periodically

## 8. HTML Downloader

- **Robots.txt (Robots Exclusion Protocol)** — standard for sites to declare which paths crawlers may fetch; the crawler must check it before crawling, and the file is cached and refreshed periodically to avoid repeated downloads
- **Distributed crawl** — partition the URL space across multiple servers, each running multiple downloader threads
- **Cache DNS Resolver** — DNS calls take 10–200 ms and are often synchronous (blocking other threads); a local DNS cache (domain→IP) refreshed by cron jobs removes this bottleneck
- **Locality** — place crawl servers (and caches, queues, storage) geographically close to target hosts to reduce download time
- **Short timeout** — set a maximum wait so a slow/unresponsive host doesn't stall a worker; abort and move on

## 9. Robustness

- **Consistent hashing** — distributes load across downloaders and lets servers be added/removed with minimal data movement (see Ch 5)
- **Save crawl states and data** — persist progress so a disrupted crawl can resume from saved state instead of restarting
- **Exception handling** — large-scale crawls hit constant errors; the system must catch and continue rather than crash
- **Data validation** — guard against system errors caused by malformed/unexpected input

## 10. Extensibility

- **Plug-in modules** — new content types attach to the existing pipeline as separate modules
- **Examples** — a **PNG Downloader module** for image files; a **Web Monitor module** for copyright/trademark monitoring

## 11. Detect and Avoid Problematic Content

- **Redundant content** — ~30% of pages are duplicates; detect with hashes/checksums
- **Spider trap** — a page that traps the crawler in an infinite loop (e.g., `www.spidertrapexample.com/foo/bar/foo/bar/...`); mitigations include capping URL length and manually blacklisting offenders, since no general algorithm exists
- **Data noise** — ads, code snippets, spam URLs add no value; filter them out where possible

## 12. Additional Talking Points

- **Server-side rendering** — pages that build links via JavaScript/AJAX won't yield links from raw HTML; render dynamically before parsing
- **Filter unwanted pages** — an anti-spam component preserves storage and crawl budget by dropping low-quality and spam pages
- **Database replication and sharding** — improve data-tier availability, scalability, and reliability
- **Horizontal scaling** — hundreds to thousands of downloader servers for large crawls; keep them stateless
- **Availability, consistency, reliability** — core large-system concerns covered in Ch 1
- **Analytics** — collecting and analyzing crawl data is essential for fine-tuning the system
