# Appendix: Advanced Concepts

## Table of Contents

- [1. Scope](#1-scope)
- [2. Probabilistic Data Structures](#2-probabilistic-data-structures)
- [3. Recommendation and Ranking](#3-recommendation-and-ranking)
- [4. Document and Web Search Ranking](#4-document-and-web-search-ranking)
- [5. Collaborative Editing](#5-collaborative-editing)
- [6. Trending Detection](#6-trending-detection)

## 1. Scope

- **Rarely required in a system-design interview** — the book recommends optimizing fundamentals first and using these only if the question naturally pulls them in
- **Know when and why, not the algorithm in depth** — pattern-matching these to problems is the real skill

## 2. Probabilistic Data Structures

| Structure | Problem it solves | Use case |
|---|---|---|
| **HyperLogLog** | Approximate unique count with minimal memory, using the intuition that leading-bit patterns correlate with how many distinct values have been seen (e.g., a bit-pattern `100` suggests you've seen ~8 numbers) | Count unique site/post visitors |
| **Count-Min Sketch** | Maintain a key→count map that exceeds memory by trading accuracy for space | Near-real-time top-K |
| **Bloom Filter** | Fast, space-efficient membership test. Can return false positives but never false negatives — if it says "not present", it isn't; if it says "present", verify against the real source | Skip disk seeks when asking "does this ID exist?"; second-degree connection checks in graph dbs; skip already-crawled URLs |

## 3. Recommendation and Ranking

- **Collaborative Filtering** — find what similar users liked; the engine for "users like you also bought". Applies to Netflix recommendations and Amazon's "customers also bought"
- **EdgeRank** — Facebook's feed-ranking algorithm combining three signals: **user affinity** (closer users rank higher), **content weight** (more activity on the post), **time decay** (older posts rank lower). Applies to designing Instagram, Twitter, News Feed

## 4. Document and Web Search Ranking

- **TF / IDF** — relevance for full-text search. TF (term frequency) = how often the term appears in a document; IDF (inverse document frequency) = how rare the term is across all documents. More frequent *in the document* and rarer *across the corpus* → higher score. Example: searching "interview" across `A: "please study system design"` and `B: "please study system design interview"` → B scores higher because "interview" appears in B but not A
- **Page Rank** — webpage relevance for a search engine. Intuition: if many other websites link to a page, the page is popular. Weight is propagated — higher-weighted referring sites contribute more. Applies to website search-engine designs

## 5. Collaborative Editing

- **Operational Transform (OT)** — automatically resolve document-collaboration conflicts when multiple users edit simultaneously. Applies to Google Docs design

## 6. Trending Detection

- **Z-Score** — measure how many standard deviations an activity rate is from the mean. A video averaging 5 views/day (σ=1) viewed 100 times in the last hour is clearly trending. Applies to "design a trending topic" questions
