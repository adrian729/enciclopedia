# Ch 5.17: Cold Storage

## Table of Contents

- [1. Why Cold Storage](#1-why-cold-storage)
- [2. When to Bring It Up](#2-when-to-bring-it-up)

## 1. Why Cold Storage

- **Data growth is inevitable** — as long as you have users, data keeps growing; performance degrades over time and storage eventually runs out of memory
- **Access pattern skew** — for most applications, recent data is accessed more frequently than past data
- **Hot to cold migration** — move infrequently accessed data from **hot storage** to **cold storage** to exploit that skew
- **Trade-off** — cold storage is less performant and less available, but cheaper to maintain; complexity comes from moving data between tiers

## 2. When to Bring It Up

- **Interviewer asks about unbounded data growth** — proposing to separate infrequently accessed data into cold storage is a direct answer
- **Verify constraints still hold** — after moving data to cold storage, confirm that performance constraints from the requirements are still satisfied
