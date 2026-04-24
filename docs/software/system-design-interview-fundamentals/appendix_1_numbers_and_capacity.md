# Appendix: Numbers and Capacity

## Table of Contents

- [1. Number Conversions](#1-number-conversions)
- [2. Mnemonic for Scientific Notation](#2-mnemonic-for-scientific-notation)
- [3. Single-Machine Capacity Numbers](#3-single-machine-capacity-numbers)
- [4. Capacity-Adjustment Factors](#4-capacity-adjustment-factors)
- [5. Math Number Assumptions](#5-math-number-assumptions)
- [6. Product Math Assumptions](#6-product-math-assumptions)

## 1. Number Conversions

| Raw Number | Scientific Notation | Query Units | Memory Units |
|---|---|---|---|
| 1,000 | 1 × 10³ | Thousand | KB |
| 1,000,000 | 1 × 10⁶ | Million | MB |
| 1,000,000,000 | 1 × 10⁹ | Billion | GB |
| 1,000,000,000,000 | 1 × 10¹² | Trillion | TB |
| 1,000,000,000,000,000 | 1 × 10¹⁵ | Quadrillion | PB |

## 2. Mnemonic for Scientific Notation

- Use a memorable phrase to map the exponent to the unit. The book suggests:

| Exponent | Mnemonic |
|---|---|
| 3 | Kudos |
| 6 | Monkeys |
| 9 | Grapes |
| 12 | Tents |
| 15 | Pizzas |

- **Scientific notation → natural units**: `6 × 10⁷ queries` = `60 million queries` = `60 MB` (for bytes); `3 × 10¹² queries` = `3 trillion queries` = `3 TB` (for bytes)
- **Natural units → scientific notation**: `80 billion` = `10⁹ × 80` = `8 × 10¹⁰`; `700 trillion queries` = `7 × 10¹⁴`
- **Round to the nearest multiple of 3** when the exponent isn't a clean multiple (e.g., for 13, round down to 12 → `10 × trillion` → `10 × TB`)

## 3. Single-Machine Capacity Numbers

These are rough intuition numbers, not authoritative benchmarks — use your own if you prefer, but always explain the reasoning.

| Resource | Low | Medium | High |
|---|---|---|---|
| Database Read QPS | 100 | 200 | 500 |
| SSD Read QPS | 1,000 | 3,000 | 10,000 |
| Memory Read QPS | 10,000 | 30,000 | 100,000 |
| Bandwidth | 10 Gbps | 15 Gbps | 25 Gbps |
| Database | 512 GB | 8 TB | 64 TB |
| Memory | 64 GB | 256 GB | 1 TB |
| Connections | 50,000 | 200,000 | 1,000,000 |

> **Warning** — bandwidth is measured in **bits** per second, not bytes per second. Divide by 8 (or approximate by 10) to convert to bytes per second.

## 4. Capacity-Adjustment Factors

QPS numbers above assume a single thread. Shift your estimate based on (non-exhaustive):

- **Size of payload** into or out of memory / database
- **Amount of data** in the datastore
- **Complexity of the query**
- **Database selections** (LSM vs B-Tree)

## 5. Math Number Assumptions

Rough approximations for back-of-the-envelope math.

**Datastore Latency**

| Storage | Latency |
|---|---|
| Fetching 1 MB from disk | Disk seek: 2 ms + Read 1 MB sequentially on disk: 1 ms → **Total: 3 ms** |
| Fetching 1 MB from SSD | SSD random read: 15 μs + Reading 1 MB sequentially from SSD: 200 μs → **Total: 0.2 ms** |
| Fetching 1 MB from memory | Memory reference: 100 ns + Reading 1 MB sequentially from memory: 10 μs → **Total: 0.01 ms** |

- Latency to fetch 1 MB = fixed seek cost + sequential read cost

**Network Latency**

| Distance | Latency |
|---|---|
| California to the Netherlands | 150 ms |
| California to Virginia | 60 ms |
| Inter Datacenter | 0.5 ms |

**Images**

| Quality | Size | Examples |
|---|---|---|
| Low | 10 KB | Thumbnail, small website images |
| Medium | 100 KB | Website photos |
| High | 2 MB | Phone camera photos |
| Ultra High | 20 MB | RAW photographer image |

**Video**

| Quality | 1-Minute Storage | Examples |
|---|---|---|
| Low | 30 MB | 480p video |
| Medium | 90 MB | 1080p video |
| High | 500 MB | 4k video |

**Audio**

| Quality | 1-Minute Storage | Examples |
|---|---|---|
| Low | 700 KB | Low quality Mp3 |
| High | 2.5 MB | High quality Mp3 |

**Storage Data Type**

| Type | Memory |
|---|---|
| Boolean | 1 Bit |
| Char | 1 Byte |
| Int | 4 Bytes |
| Timestamp | 4 Bytes |
| BigInt | 8 Bytes |

## 6. Product Math Assumptions

Useful intuition for "reasonable" user-count numbers when the interviewer asks you to assume them (an off-the-chart number is alarming — e.g., 1 trillion DAU on Facebook or 100 DAU on Uber).

| 2021 Numbers | Value |
|---|---|
| World population | 8 billion |
| US population | 300 million |
| Facebook MAU | 3 billion |
| Instagram MAU | 1 billion |
| Uber MAU | 100 million |
| Google searches per day | 5.6 billion |

- MAU = Monthly active users
