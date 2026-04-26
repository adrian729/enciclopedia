# API Design & API Gateway

> Liu's Ch 5.02 covers API design as a contract; Liu's Ch 5.19 covers the API gateway as the natural home for cross-cutting concerns. Xu doesn't have dedicated chapters but defines APIs in every product design.

## Table of Contents

- [1. Why the API Matters](#1-why-the-api-matters)
- [2. The Three Things That Matter](#2-the-three-things-that-matter)
  - [2.1. Signature Name](#21-signature-name)
  - [2.2. Inputs](#22-inputs)
  - [2.3. Outputs](#23-outputs)
- [3. Defaults](#3-defaults)
  - [3.1. Idempotency](#31-idempotency)
  - [3.2. Server-Generated Where Sensitive](#32-server-generated-where-sensitive)
  - [3.3. Pagination and Thumbnails](#33-pagination-and-thumbnails)
- [4. The API Gateway](#4-the-api-gateway)
- [Sources](#sources)

## 1. Why the API Matters

The API is a detailed contract; without it, deep-dive discussions get hand-wavy. Both books treat API design as a checkpoint in the framework — Liu makes it Step 2 of the six-step process, Xu folds it into Step 2 of the four-step process.

The API also drives QPS calculations (which need a *specific* call to multiply by) and the schema (which the API operates on).

## 2. The Three Things That Matter

### 2.1. Signature Name

A descriptive verb-noun. `request_ride`, `upload_photo`, `get_feed`.

### 2.2. Inputs

The **everything-counts** rule: don't add unjustified parameters, don't omit required ones, don't use vague or nonsensical values.

- A client-generated `photo_id` smells wrong — IDs sensitive to clock skew or tampering should be server-generated.
- A `friend_name` instead of `friend_user_id` introduces ambiguity (homonyms, name changes).
- RESTful and protobuf details are distractions unless the interviewer explicitly asks.

### 2.3. Outputs

Most candidates forget this; Liu emphasizes it loudly because the output shape is often as design-shaping as the input.

The canonical example: `request_ride` returning `{ driver_ids: [1, 2] }` lets the user pick a driver and introduces concurrency at the API boundary. Returning `{ driver_id: 1 }` and letting the server assign sidesteps the race entirely. Same UX, dramatically simpler tech.

Collection responses imply pagination and thumbnails — call them out proactively.

## 3. Defaults

### 3.1. Idempotency

Default to idempotent APIs where achievable. `update_quantity(order, 2)` (set the quantity to 2) is idempotent — calling it twice doesn't double anything. `decrease_quantity(order, 1)` (decrement by 1) is *not* — calling it twice decrements by 2.

Idempotent APIs simplify retry logic, make at-least-once delivery safe, and reduce the need for client-side dedup.

### 3.2. Server-Generated Where Sensitive

Anything sensitive to client clock skew or tampering should be server-generated:

- IDs (use [Snowflake](fundamentals/id-generation.md))
- Timestamps (a chat system uses server-generated millisecond timestamps for ordering — Liu Ch 6.08)
- Audit fields (`created_by`, `updated_at`)

Client-supplied values for these fields are a red flag.

### 3.3. Pagination and Thumbnails

For collection endpoints, raise pagination proactively:

- Page size limit.
- Cursor-based vs offset-based pagination (cursor is the modern default; doesn't break under inserts).
- Thumbnails (downsized images) for clients on mobile networks.

## 4. The API Gateway

An **API gateway** sits in front of microservices, has its own IP, and is the natural home for cross-cutting concerns:

- **Rate limiting** — see [Rate Limiter case study](case-studies/rate-limiter.md). The gateway has visibility into all incoming requests and is a natural enforcement point.
- **IP blocklist** — geographic blocking, abuse mitigation.
- **TLS termination** — backend services receive plain HTTP from a trusted network.
- **Authentication** — verify tokens (OAuth) before forwarding to downstreams.
- **Request routing** — map external paths to internal services.
- **Response transformation** — combine multiple internal responses into one external one (BFF pattern).

In the deep-dive, candidates often place a rate limiter, auth, and TLS termination on a single component. Naming that component the API gateway is a stronger signal than describing each function as a separate microservice in front of the others.

## Sources

- [Liu Ch 5.02: API Design](software/system-design-interview/books/system-design-interview-fundamentals/ch05_02_api_design.md)
- [Liu Ch 5.19: API Gateway](software/system-design-interview/books/system-design-interview-fundamentals/ch05_19_api_gateway.md)
