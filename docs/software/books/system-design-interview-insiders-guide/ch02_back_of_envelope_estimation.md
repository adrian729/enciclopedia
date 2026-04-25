# Ch 2: Back-of-the-Envelope Estimation

## Table of Contents

- [1. What Back-of-the-Envelope Estimation Is](#1-what-back-of-the-envelope-estimation-is)
- [2. Power of Two](#2-power-of-two)
- [3. Latency Numbers Every Programmer Should Know](#3-latency-numbers-every-programmer-should-know)
- [4. Availability Numbers](#4-availability-numbers)
- [5. Worked Example: Twitter QPS and Storage](#5-worked-example-twitter-qps-and-storage)
- [6. Tips for the Interview](#6-tips-for-the-interview)

## 1. What Back-of-the-Envelope Estimation Is

- **Definition (Jeff Dean)** — estimates built from thought experiments combined with common performance numbers, used to get a feel for which designs will meet requirements
- **Why it matters in interviews** — interviewers may ask candidates to estimate system capacity or performance requirements using a back-of-the-envelope estimation
- **Three foundations** — power of two for data volumes, latency numbers for operation costs, availability numbers for SLA targets

## 2. Power of Two

- **Why** — distributed-system data volumes get huge, but unit conversions still reduce to powers of two; getting the unit wrong throws estimates off by orders of magnitude
- **Byte basics** — a byte is 8 bits; an ASCII character is one byte
- **Reference scale** — 2^10 ≈ 1 KB, 2^20 ≈ 1 MB, 2^30 ≈ 1 GB, 2^40 ≈ 1 TB, 2^50 ≈ 1 PB

## 3. Latency Numbers Every Programmer Should Know

- **Source** — Dr. Jeff Dean's 2010 numbers (still directionally correct even as hardware improves), visualized by a Google engineer for 2020
- **Units** — `1 ns = 10^-9 s`, `1 µs = 10^-6 s = 1,000 ns`, `1 ms = 10^-3 s = 1,000 µs = 1,000,000 ns`
- **Memory is fast, disk is slow** — guides every caching decision; in-memory access is orders of magnitude cheaper than disk I/O
- **Avoid disk seeks if possible** — random disk access dominates many naive designs and should be engineered out
- **Simple compression algorithms are fast** — cheap enough to pay for routinely
- **Compress data before sending it over the internet if possible** — network is the bottleneck, so trading a little CPU for less bandwidth pays off
- **Cross-region transfer is slow** — data centers in different regions add meaningful latency, so multi-region designs must account for it

## 4. Availability Numbers

- **High availability** — the ability of a system to be continuously operational for a desirably long period; expressed as a percentage where 100% means zero downtime
- **SLA (Service Level Agreement)** — formal contract between provider and customer defining the uptime delivered; major cloud providers (Amazon, Google, Microsoft) set SLAs at 99.9% or above
- **Measured in nines** — more nines = less downtime; the more nines, the better

## 5. Worked Example: Twitter QPS and Storage

- **Assumptions** — 300M monthly active users, 50% daily active, 2 tweets/user/day, 10% of tweets contain media, retain data for 5 years
- **DAU** — 300M × 50% = 150M
- **Tweets QPS** — 150M × 2 / 24 / 3600 ≈ 3,500 QPS
- **Peak QPS** — 2 × QPS ≈ 7,000
- **Average tweet size** — `tweet_id` 64 bytes, `text` 140 bytes, `media` 1 MB
- **Daily media storage** — 150M × 2 × 10% × 1 MB = 30 TB/day
- **5-year media storage** — 30 TB × 365 × 5 ≈ 55 PB

## 6. Tips for the Interview

- **Process over precision** — interviewers test problem-solving; the result matters less than how you got there
- **Rounding and approximation** — don't burn time on exact arithmetic; simplify (e.g., `99987 / 9.1` becomes `100,000 / 10`)
- **Write down your assumptions** — keep them visible so you and the interviewer can reference them later
- **Label your units** — "5" is ambiguous; "5 MB" is not; missing units quietly corrupt the rest of the estimate
- **Common asks** — QPS, peak QPS, storage, cache size, server count; rehearse these before the interview so they come out fluently
