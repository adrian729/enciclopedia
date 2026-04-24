# Appendix: System Design Framework Cheat Sheet

## Table of Contents

- [1. The 6-Step Framework](#1-the-6-step-framework)
- [2. Non-Functional Cheat Sheet](#2-non-functional-cheat-sheet)
- [3. Deep Dive Cycle](#3-deep-dive-cycle)

## 1. The 6-Step Framework

| Step | Activity | Time (40-min interview) |
|---|---|---|
| **1a** | Gather Requirements — Functional | 2–3 min |
| **1b** | Gather Requirements — Non-Functional | 3–5 min |
| **2** | Define API | 3–5 min |
| **3** | Define High-Level Diagram | 5–7 min |
| **4** | Define Schema and Data Structures | 5–7 min |
| **5** | Summarize End-to-End Flow | 2–3 min |
| **6** | Deep Dives | 15–20 min |

## 2. Non-Functional Cheat Sheet

| Data Distribution | Performance Constraint |
|---|---|
| Scale numbers | Consistency and availability |
| Distribution of storage and query | Response time |
| Geo distribution of users | Latency |
| | Accuracy |
| | Freshness |
| | Durability |

## 3. Deep Dive Cycle

1. Identify the most important discussion point
2. Come up with options
3. Discuss the trade-offs
4. Conclude with one solution
5. Active discussion with the interviewer
6. Go to Step 1
