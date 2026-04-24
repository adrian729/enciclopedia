# Ch 17: Scalability and Memory Limits

## Table of Contents

- [1. Framing](#1-framing)
- [2. Step-by-step approach](#2-step-by-step-approach)
- [3. A typical system](#3-a-typical-system)
- [4. Dividing up lots of data](#4-dividing-up-lots-of-data)
- [5. Worked example: find documents containing a list of words](#5-worked-example-find-documents-containing-a-list-of-words)

## 1. Framing

- **Scalability questions are not "gotchas"** — no tricks, no fancy algorithms, and usually no distributed-systems coursework required. Any thorough engineer can handle them with practice.
- **What is being evaluated** — not system-design knowledge per se, but the ability to break down a tricky problem and solve it using what you already know. The goal is not to re-architect what companies spent millions on.
- **Poking holes in your own solution** — demonstrates the analysis skill interviewers want.

## 2. Step-by-step approach

The book gives a three-step method that works for many system design problems.

| Step | Name | What to do |
|------|------|------------|
| 1 | **Make Believe** | Pretend all data fits on one machine with no memory limits. How would you solve it? This answer is the general outline. |
| 2 | **Get Real** | Return to the original. How much data fits on one machine? What problems arise when data is split — how does one machine find data on another? |
| 3 | **Solve Problems** | Address each issue from Step 2. The fix may **remove** the issue or merely **mitigate** it. Usually the Step 1 approach is kept (with modifications); occasionally it must be fundamentally altered. |

- **Iterate** — solving Step 2's issues often uncovers new ones; tackle those too.

## 3. A typical system

- **Assume a large system of interconnected machines**, not a super-computer — most web-based companies work this way.
- **Fill in a personal capacity chart before the interview** to ballpark what one machine can store.

| Component | Typical Capacity / Value |
|-----------|--------------------------|
| Hard Drive Space | (fill in) |
| Memory | (fill in) |
| Internet Transfer Latency | (fill in) |

## 4. Dividing up lots of data

When data must be split across machines, four strategies exist.

| Strategy | How it works | Trade-off |
|----------|--------------|-----------|
| **By Order of Appearance** | Fill one machine, then add another. | Never uses more machines than necessary; lookup table can be complex and very large. |
| **By Hash Value** | Store on machine `#[mod(hash(key), N)]`. | No lookup table needed — every machine knows where data is. If a machine overfills, shifting data (expensive) or splitting it (tree-like structure) is required. |
| **By Actual Value** | Use domain knowledge to co-locate related data (e.g., store friends of a Mexican user together to reduce hops). | Can reduce latency by exploiting locality. |
| **Arbitrarily** | Split randomly, maintain a lookup table. | Table may be large, but simplifies the rest of system design and enables better load balancing. |

## 5. Worked example: find documents containing a list of words

Problem: given millions of documents, find all that contain a list of words (complete-word match, any order — "book" does not match "bookkeeper").

- **Clarify first** — is this one-time or repeated? The book assumes repeated calls on the same corpus, so pre-processing is acceptable.

### 5.1. Step 1 — pretend it fits on one machine

- Pre-process each document into a **hash table index** mapping each word to the list of documents containing it.
  - `"books" -> {doc2, doc3, doc6, doc8}`
  - `"many" -> {doc1, doc3, doc7, doc8, doc9}`
- To search `"many books"`, intersect the two value sets → `{doc3, doc8}`.

### 5.2. Step 2 — get real

Millions of documents raise three key concerns:

1. **How to divide the hash table** — by keyword (each machine holds the full doc list for a given word) or by document (each machine holds the keyword map for a subset of docs)?
2. **Cross-machine processing** — processing a document on one machine may require pushing results to other machines. (If divided by document, this step may be unnecessary.)
3. **Locating data** — need a way to know which machine holds a piece of data, plus a place to store that lookup table.

### 5.3. Step 3 — solve problems

- **Divide keywords alphabetically** — each machine controls a contiguous range (e.g., `"after"` through `"apple"`); iterate keywords, filling one machine then moving on.
- **Advantages** — the lookup table only stores ranges, so it is small and simple, and every machine can cache a copy.
- **Disadvantage** — adding new documents/words may trigger expensive keyword shifts.
- **Query execution** — sort the query words, dispatch each machine a lookup request for the strings in its range, have each machine intersect locally, then intersect the per-machine results on the initial machine.
