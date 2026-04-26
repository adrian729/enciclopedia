# Ch 5.22: Full-Text Search

## Table of Contents

- [1. When Full-Text Search Comes Up](#1-when-full-text-search-comes-up)
- [2. Text-to-Token Pipeline](#2-text-to-token-pipeline)
- [3. Indexing (Reverse Index)](#3-indexing-reverse-index)
- [4. N-Gram](#4-n-gram)
- [5. Search Query](#5-search-query)
- [6. Ranking](#6-ranking)
- [7. Data Source and Indexing Pipeline](#7-data-source-and-indexing-pipeline)

## 1. When Full-Text Search Comes Up

- **Common in many system-design questions** — searching images by label, tweets by text, chat history by message; sometimes a full interview question on its own
- **Requirements drive the infrastructure** — freshness (index every day vs every minute) and search latency (cache aggressively vs accept disk hits) are the main knobs
- **Intuition beats memorization** — enough high-level knowledge to ask informed domain questions; deep NLP only if interviewing in that specialty

## 2. Text-to-Token Pipeline

Before indexing a document, the system tokenizes the string through these stages:

| Step | What it does | Example |
|---|---|---|
| **Normalize** | Lowercase and strip special characters | `"System-Design!"` → `"system design"` |
| **Tokenize** | Split into tokens | `"system design"` → `["system", "design"]` |
| **Remove stop words** | Drop words appearing in every document | `["the", "for"]` removed |
| **Stemming** | Reduce to word stems | `"studying"` → `"study"` |

> **Reminder** — these are common English-NLP steps. Stemming is English-specific; case sensitivity may matter for some queries. Ask the interviewer about domain requirements rather than blindly running the whole pipeline.

## 3. Indexing (Reverse Index)

- **Reverse index** — for each token, store the list of documents containing it (the **posting list**)
- **Efficient lookup** — searching `"design"` hits one key and returns the matching document IDs in sorted order
- **Sort key on posting list** — by doc ID or by ranking score, depending on how results are served

## 4. N-Gram

- **Motivation** — some token pairs have meaning only together (`"system design"`, `"San Francisco"`)
- **2-gram example** — index bigrams alongside unigrams so a `"system design"` query hits one entry instead of intersecting two posting lists
- **Trade-off** — extra storage because more keys exist

## 5. Search Query

- **Clarify the operators** — `"system design"` could mean literal phrase, `AND`, `OR`, wildcard, or `NOT`; ask the interviewer what expressions the system must support
- **Merge k sorted posting lists** — multi-term queries combine sorted lists using the standard k-way merge algorithm

## 6. Ranking

- **Sorting key is the ranking factor** — if the posting list is already sorted by the ranking score, retrieval is free
- **Time-varying scores** — when rank changes over time (e.g., recency decay), plan for re-scoring or re-sorting post-retrieval
- **TF-IDF** — a canonical document-search ranking algorithm; see Appendix: Advanced Concepts

## 7. Data Source and Indexing Pipeline

- **Profile the source** — how frequently data arrives, what structure it has, where it's stored
- **Freshness drives architecture choice**:
  - Real-time → **stream processing**
  - Periodic → **batch**
  - Both → **Lambda architecture** (see Ch 5.09)
- **MapReduce** — the classical batch pattern for building reverse indices
