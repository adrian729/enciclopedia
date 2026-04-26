# Ch 5.02: API Design

## Table of Contents

- [1. Idempotency](#1-idempotency)
- [2. Client vs Server Generated Data](#2-client-vs-server-generated-data)
- [3. Efficiency](#3-efficiency)
- [4. Correctness](#4-correctness)
- [5. Focus on the Core](#5-focus-on-the-core)

## 1. Idempotency

- **Definition** — calling the API multiple times with the same input produces the same end state; retries don't compound effects
- **Example** — to decrease an order quantity from 3 to 2:

| API | Idempotent? | Behavior on repeat |
|---|---|---|
| `decrease_quantity(order, 1)` | No | Each retry decrements by 1 (2 → 1 → 0 → …) |
| `update_quantity(order, 2)` | Yes | State stays at 2 regardless of call count |

- **Why prefer idempotency** — system and user retries are common; non-idempotent APIs produce unwanted behavior on accidental repeats
- **Not always achievable** — a "place order" API can't know whether two identical orders are a mistake or a genuine double purchase; warning the user about duplicates is a UX mitigation, not idempotency

## 2. Client vs Server Generated Data

- **Default: server generates** — for fields like timestamps, generate them on the server, not the client
- **Two reasons** — client clocks may drift out of sync; a malicious client can tamper with fields it controls

## 3. Efficiency

- **Don't return unbounded collections** — a news-feed API shouldn't return every feed for the user
- **Paginate** — return a page at a time; pagination is the default mental model for any list response

## 4. Correctness

- **Signature must match the task** — the name reflects what the API actually does
- **Inputs and outputs must satisfy the requirement** — walk through the agreed functional requirement against the contract before moving on

## 5. Focus on the Core

- **Three things matter** — input parameters, output response, signature name
- **REST / protobuf is a distraction** — unless the interviewer explicitly asks for a RESTful design, don't elaborate on HTTP verbs, status code mappings, or protobuf schemas; it's time wasted
