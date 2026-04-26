# Observability, Security, and Cold Storage

> A bundle of three smaller topics that share the property of being almost-always-relevant in a deep dive but never the central question. Liu has a chapter on each (5.21 monitoring, 5.12 + Appendix 3 security, 5.15 data transfer, 5.17 cold storage); Xu covers monitoring inside Ch 1 and revisits cold storage in YouTube and Google Drive.

## Table of Contents

- [1. Monitoring](#1-monitoring)
  - [1.1. Three Tiers of Metrics](#11-three-tiers-of-metrics)
  - [1.2. The Core Four](#12-the-core-four)
- [2. Security](#2-security)
  - [2.1. API Security Is the Exception](#21-api-security-is-the-exception)
  - [2.2. TLS](#22-tls)
  - [2.3. OAuth and Token Refresh](#23-oauth-and-token-refresh)
- [3. Data Transfer](#3-data-transfer)
  - [3.1. Encoding, Transcoding, Compression, Codec](#31-encoding-transcoding-compression-codec)
  - [3.2. Lossless vs Lossy](#32-lossless-vs-lossy)
  - [3.3. Adaptive Bit Rate](#33-adaptive-bit-rate)
  - [3.4. Rsync — Send Only What Changed](#34-rsync--send-only-what-changed)
- [4. Cold Storage](#4-cold-storage)
- [Sources](#sources)

## 1. Monitoring

Naming metrics worth tracking for the *specific design* signals on-call awareness — interviewers want to see that you'd know if the system was failing in production.

### 1.1. Three Tiers of Metrics

Xu's framing:

- **Host** — CPU, memory, disk I/O, network. Where the box is unhealthy.
- **Aggregated** — database tier, cache tier performance. Where the cluster is unhealthy.
- **Business** — DAU, retention, revenue, conversion. Where the *product* is unhealthy.

A well-instrumented system has dashboards at all three.

### 1.2. The Core Four

Liu's list of metrics worth having for any service:

- **Latency** (p50, p95, p99 — never just average).
- **QPS** (current and peak).
- **Error rate** (% of requests failing, broken down by error class).
- **Storage runway** (how long until the disk fills).

Plus product-specific signals: order drops, queue backlog, message-delivery success rate, location-update lag.

The point isn't reciting every metric — it's knowing which ones the on-call would actually look at when paged.

## 2. Security

### 2.1. API Security Is the Exception

Security rarely drives a generalist design, but **API security** is the exception. Both authors recommend thinking through, for each API, *the worst thing a malicious user could do*:

- `transfer_money(amount, user_id, to_user_id)` — a client setting `user_id` to someone else's ID drains their account unless validated server-side. Authentication tokens, not client-supplied user IDs.
- `upload_photo(bytes)` — must defend against malicious bytes (SVG with embedded scripts, polyglot files, decompression bombs).
- `request_ride(...)` — must defend against phantom rides (credit-card-stolen-account spamming requests).

The signal is *naming the worst case proactively*, not memorizing OWASP categories.

### 2.2. TLS

Mitigates man-in-the-middle attacks. The interviewer rarely quizzes the key-exchange steps in detail; what matters is knowing TLS terminates somewhere (often at the [API gateway](fundamentals/api-design-and-gateway.md)) and that backend traffic on a private network may run plaintext.

### 2.3. OAuth and Token Refresh

OAuth-style tokens with **periodic refresh** limit the blast radius of a compromised credential. A leaked access token expires within minutes; the refresh token is held more securely and can be revoked when compromise is detected. The pattern shows up in any system that issues credentials to clients (mobile apps, third-party integrations).

## 3. Data Transfer

### 3.1. Encoding, Transcoding, Compression, Codec

Liu draws sharp distinctions:

- **Encoding** — raw → JPEG (or any specific format).
- **Transcoding** — format → format (e.g., AVI → MP4).
- **Compression** — any size reduction (lossless or lossy).
- **Codec** — the algorithm (H.264, VP9, HEVC).

Using the right term in an interview signals familiarity with the domain.

### 3.2. Lossless vs Lossy

| Type | Example | Ratio | Recoverable? |
|---|---|---|---|
| Lossless | Run-Length Encoding (`AAAABBBBBBBBBBBBBBBAAA` → `4A15B3A`) | ~2× | Yes |
| Lossy | JPEG chroma subsampling | ~20× | No |

Compression costs CPU. The choice between client-side and server-side compression depends on which side has spare cycles and which side is bandwidth-constrained.

### 3.3. Adaptive Bit Rate

ABR dynamically adjusts video quality to available bandwidth. A pre-encoded ladder (e.g., 240p, 480p, 720p, 1080p, 4K) is served per-segment based on the client's measured bandwidth and buffer health. Used by every modern video service.

### 3.4. Rsync — Send Only What Changed

Hash 2,048-byte chunks of the file with MD5; transmit only the chunks whose hashes differ from the destination. A **rolling hash** lets the sender recompute chunk hashes by moving one byte forward at head and tail, so insertions and deletions don't force re-hashing the whole file.

Used in [Cloud File Storage](case-studies/cloud-file-storage.md) (Dropbox / Google Drive style "delta sync") to keep upload cost proportional to *changes*, not file size.

## 4. Cold Storage

Recent data is accessed more often than old data — the access distribution is heavily skewed. Moving infrequently-accessed data from **hot storage** (low-latency, expensive) to **cold storage** (high-latency, cheap) exploits that skew.

Xu uses cold storage in two designs:

- **YouTube** — popular videos go through CDN; unpopular videos serve from in-house cold storage where the marginal cost per view is much lower than CDN egress.
- **Google Drive** — files not opened in months move to cold tiers (S3 Glacier, etc.); recall takes minutes but storage is ~10× cheaper.

Liu's framing: cold storage is the **direct answer to unbounded-data-growth prompts**. When the interviewer asks "what about old data?", the answer is almost always "tier it." The trade-off is performance/availability for cost; the complexity is the migration logic between tiers.

## Sources

- [Liu Ch 5.12: Security](software/system-design-interview/books/system-design-interview-fundamentals/ch05_12_security.md)
- [Liu Ch 5.15: Data Transfer](software/system-design-interview/books/system-design-interview-fundamentals/ch05_15_data_transfer.md)
- [Liu Ch 5.17: Cold Storage](software/system-design-interview/books/system-design-interview-fundamentals/ch05_17_cold_storage.md)
- [Liu Ch 5.21: Monitoring](software/system-design-interview/books/system-design-interview-fundamentals/ch05_21_monitoring.md)
- [Liu Appendix: Security Considerations](software/system-design-interview/books/system-design-interview-fundamentals/appendix_3_security.md)
- [Xu Ch 1: Scale From Zero to Millions of Users](software/system-design-interview/books/system-design-interview-insiders-guide/ch01_scale_zero_to_millions.md) (logging/metrics section)
