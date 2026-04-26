# Back-of-the-Envelope Estimation

> Both books spend a chapter on numerical fluency, framed by Jeff Dean's working definition: estimates built from thought experiments and common performance numbers, used to get a feel for which designs will meet requirements. Liu provides QPS and storage formulas; Xu provides the capacity and latency tables. They are complementary.

## Table of Contents

- [1. When to Calculate](#1-when-to-calculate)
- [2. Liu's QPS Formula](#2-lius-qps-formula)
- [3. Liu's Storage Formula](#3-lius-storage-formula)
- [4. The Six-Step Calculation Technique](#4-the-six-step-calculation-technique)
- [5. Xu's Capacity Foundations](#5-xus-capacity-foundations)
  - [5.1. Powers of Two](#51-powers-of-two)
  - [5.2. Latency Numbers Every Programmer Should Know](#52-latency-numbers-every-programmer-should-know)
  - [5.3. Availability Nines](#53-availability-nines)
- [6. Worked Example — Twitter (Xu)](#6-worked-example--twitter-xu)
- [7. Common Mistakes](#7-common-mistakes)
- [Sources](#sources)

## 1. When to Calculate

**After API and schema, not before** (Liu's most-emphasized sequencing rule). QPS is per-API; storage is per-schema. Calculating either upfront forces guesswork.

A calculated 10⁸ QPS against a single machine's ~10⁶ capacity *identifies* a scaling problem — that's the value of doing the math. Calculating 6 PB/day and moving on without doing anything with the number is worthless.

## 2. Liu's QPS Formula

```
QPS = (DAU × % making query × queries per user per day × scaling factor) ÷ 100,000
```

The denominator is the ~86,400 seconds in a day, rounded for mental math. Dividing by 100k just subtracts 5 from the power of 10.

The **scaling factor** captures worst-case spikes — ridesharing on weekend nights runs 5–10× average; concert-end can go 10×. The worst case is the number to design for.

## 3. Liu's Storage Formula

```
Storage = DAU × % × queries × data size per query × replication factor × time horizon
```

Replication factor is typically 3. Time horizon is usually 1–5 years.

## 4. The Six-Step Calculation Technique

Mechanical and consistent:

1. Convert everything to scientific notation. Every comma shifts the exponent by 3.
2. Group the 10s.
3. Group other numbers.
4. Compute.
5. Convert to readable units via the conversion table (3=K, 6=M, 9=B/G, 12=T, 15=P).
6. **Do something with the number.**

## 5. Xu's Capacity Foundations

### 5.1. Powers of Two

Getting the unit wrong corrupts every estimate by orders of magnitude. The minimum ladder:

| Power | Approx. value | Unit |
|---|---|---|
| 2¹⁰ | ~10³ | KB |
| 2²⁰ | ~10⁶ | MB |
| 2³⁰ | ~10⁹ | GB |
| 2⁴⁰ | ~10¹² | TB |
| 2⁵⁰ | ~10¹⁵ | PB |

Liu's mnemonic for powers of 10: 3=Kudos, 6=Monkeys, 9=Grapes, 12=Tents, 15=Pizzas.

### 5.2. Latency Numbers Every Programmer Should Know

Jeff Dean's 2010 numbers, still directionally correct:

- L1 cache reference: ~0.5 ns
- Branch misprediction: ~5 ns
- L2 cache reference: ~7 ns
- Mutex lock/unlock: ~25 ns
- Main memory reference: ~100 ns
- Compress 1 KB with Zippy: ~3 µs
- Send 1 KB over 1 Gbps network: ~10 µs
- Read 4 KB from SSD: ~150 µs
- Read 1 MB sequentially from memory: ~250 µs
- Round trip within same datacenter: ~500 µs
- Read 1 MB sequentially from SSD: ~1 ms
- Disk seek: ~10 ms
- Read 1 MB sequentially from disk: ~20 ms
- Send packet CA → Netherlands → CA: ~150 ms

Operational rules of thumb: memory is fast, disk is slow, random disk seeks should be engineered out, simple compression is cheap, and cross-region transfer is meaningfully slower than intra-region.

### 5.3. Availability Nines

| Nines | Downtime per year |
|---|---|
| 99% | ~3.65 days |
| 99.9% | ~8.76 hours |
| 99.99% | ~52.6 minutes |
| 99.999% | ~5.26 minutes |

Codified in **SLA** contracts; major cloud providers set SLAs at 99.9% or above. Frame durability ("eleven 9s") in user impact rather than memorized counts.

## 6. Worked Example — Twitter (Xu)

Assumptions:
- 300M MAU
- 50% daily-active → DAU = 150M
- 2 tweets per user per day
- 10% of tweets contain media
- 5-year retention
- Average tweet sizes: `tweet_id` 64 B, `text` 140 B, `media` 1 MB

QPS:
- Tweets per second = 150M × 2 / 86,400 ≈ **3,500 QPS**
- Peak QPS (2× factor) ≈ **7,000 QPS**

Storage:
- Daily media storage = 150M × 2 × 10% × 1 MB = **30 TB/day**
- 5-year media storage ≈ **55 PB**

The point is process over precision: round aggressively, write down assumptions, label units, and rehearse the common asks (QPS, peak QPS, storage, cache size, server count) until they come out fluently.

## 7. Common Mistakes

- Calculating before the API and schema are nailed (Liu's sequencing rule).
- Spending too long on the math.
- Confusing GB with TB — a 1,000× error.
- Calculating numbers that don't drive a decision (bandwidth for a lightweight heartbeat service).
- Doing the math but not stating what it implies for the design.

## Sources

- [Liu Ch 5.01: Back-of-the-Envelope Math](software/system-design-interview/books/system-design-interview-fundamentals/ch05_01_back_of_envelope_math.md)
- [Liu Appendix: Numbers and Capacity](software/system-design-interview/books/system-design-interview-fundamentals/appendix_1_numbers_and_capacity.md)
- [Xu Ch 2: Back-of-the-Envelope Estimation](software/system-design-interview/books/system-design-interview-insiders-guide/ch02_back_of_envelope_estimation.md)
