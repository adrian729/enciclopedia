# Cloud File Storage (Google Drive / Dropbox)

> Both books cover this. Xu's Ch 15 is the full design (delta sync, block servers, ACID metadata, long polling). Liu's Ch 6.06 emphasizes **why MySQL** for metadata (cross-row transactions, joins on `parent_folder_id`) and the blob-then-metadata pattern as a 2PC alternative. Distinct from [Object Storage (S3-like)](case-studies/object-storage.md), which is the immutable-objects-with-versioning problem; this page is about **mutable file sync** with delta-based bandwidth savings.

## Table of Contents

- [1. Requirements](#1-requirements)
- [2. The Pivotal Idea — Delta Sync](#2-the-pivotal-idea--delta-sync)
- [3. Strong Consistency for Metadata](#3-strong-consistency-for-metadata)
- [4. Storage Choice — MySQL](#4-storage-choice--mysql)
- [5. Architecture](#5-architecture)
- [6. Metadata Schema](#6-metadata-schema)
- [7. Concurrency — Optimistic Locking](#7-concurrency--optimistic-locking)
- [8. Distributed Transaction — Blob, Then Metadata](#8-distributed-transaction--blob-then-metadata)
- [9. Notification — Long Polling](#9-notification--long-polling)
- [10. Storage Optimization](#10-storage-optimization)
- [11. Failure Handling](#11-failure-handling)
- [Sources](#sources)

## 1. Requirements

- Sync files across devices reliably with low bandwidth.
- Strong consistency on metadata — clients must see the same view of a file.
- Low-bandwidth re-upload when only part of a file changes.
- Folder operations (move, rename) atomic.

## 2. The Pivotal Idea — Delta Sync

Files are split into **blocks** (Dropbox's reference uses 4 MB max). Each block has a content hash stored in the metadata DB.

When a file changes:

1. Compute the new block list.
2. Compare hashes to the existing block list.
3. Only re-upload the blocks that differ.

Each block is **compressed** (per file type, since text compresses well and JPEG doesn't) and **encrypted**. The bandwidth cost is proportional to *changes*, not file size.

See [rsync](fundamentals/observability-security-cold-storage.md) for the underlying technique.

## 3. Strong Consistency for Metadata

Unlike chat or news feed, file storage demands **strong consistency**. If two clients open the same file, they must see the same content. Eventual consistency would mean one client could read stale metadata pointing at old blocks.

The system is **CP**, not AP. See [CAP, Consensus & Conflict Resolution](fundamentals/cap-consensus-and-conflict-resolution.md).

## 4. Storage Choice — MySQL

Liu's emphasis: **why a relational store, not Cassandra**.

- **Cross-row transactions matter.** Moving a folder changes `parent_folder_id` for many child files atomically. A wide-column store can't easily express that.
- **Joins and unions on `parent_folder_id`** are the dominant query pattern (rendering a folder's contents). Cassandra would force denormalization or scatter-gather.
- **ACID guarantees** are native in MySQL/PostgreSQL.

The blobs themselves go to an object store (S3, GCS) — those are write-once, read-many, and don't need ACID.

## 5. Architecture

```
Client (Desktop / Mobile / Web)
   ↓
Load Balancer
   ↓
Web Servers (stateless)
   ↓                        ↓
Notification Service    Block Servers ← orchestrate chunk/compress/encrypt/upload
   ↓                        ↓
Metadata DB (MySQL)    Cloud Storage (S3, with cross-region replication)
   ↓
Cache (Redis) for hot metadata
```

**Block servers** are the interesting middle layer: they handle the chunk/compress/encrypt pipeline so the web servers don't have to.

## 6. Metadata Schema

Xu's tables:

| Table | Holds |
|---|---|
| `User` | Account info |
| `Device` | Devices per user, with `push_id` for notifications |
| `Namespace` | Each user's root directory |
| `File` | File metadata; points to latest version |
| `File_version` | Read-only history of versions |
| `Block` | Block hashes that comprise each version |

Versioning by separating `File` (mutable, latest) from `File_version` (immutable, historic) keeps the schema clean.

## 7. Concurrency — Optimistic Locking

Two clients editing the same file at once must not silently overwrite each other. Liu picks **optimistic locking** with an explicit conflict message:

- Each version has an eTag.
- Client uploads a new version, asserting the previous eTag.
- If the asserted eTag doesn't match (someone else committed), the upload fails with a clear conflict response.
- Client decides — keep both versions, overwrite, or merge.

See [Concurrency & Transactions](fundamentals/concurrency-and-transactions.md). Pessimistic locking would block all editors when one is editing; for collaborative editing UX, optimistic-with-explicit-conflict is the right pattern.

## 8. Distributed Transaction — Blob, Then Metadata

Uploading a new version is two writes — to S3 and to the metadata DB. Liu's approach (cheaper than 2PC):

1. **Upload blob to S3 first.** S3 returns a URL.
2. **Write metadata** pointing to the new blob.
3. **If metadata write fails**, the blob is unreferenced. A background cleanup job reaps unreferenced blobs.

The user-visible state (metadata) is the only thing that needs to be transactional. Orphaned blobs are a background-cleanup problem, not a correctness problem.

See [Concurrency & Transactions](fundamentals/concurrency-and-transactions.md) for the pattern.

## 9. Notification — Long Polling

When a file changes, other devices need to know. Xu picks **long polling**:

- Clients open a long-poll request to the notification service.
- The service holds the connection until a change matters for that client.
- Sends the change reference; client closes and re-opens.

Why not WebSocket? Traffic is **one-way (server → client)**, **infrequent**, and **doesn't burst** — long polling fits all three. WebSocket adds operational cost without benefit. See [Real-Time Communication](fundamentals/real-time-communication.md).

## 10. Storage Optimization

- **Block-level deduplication.** If two users upload the same file (a viral PDF, a popular installer), the blocks have the same hashes. The system stores the block once, multiple File entries point to it. Saves storage proportional to duplication.
- **Smart backup strategies.** Recent versions in hot storage; old versions in cold storage. See [cold storage](fundamentals/observability-security-cold-storage.md).
- **Compression** per file type — text compresses well, already-compressed media doesn't.

## 11. Failure Handling

| Component | Mitigation |
|---|---|
| Web server outage | Load balancer redirects to healthy peers |
| DB outage | Master/slave promotion (see [Replication](fundamentals/replication.md)) |
| Storage outage | S3 cross-region replication for durability |
| Notification service outage | Clients fall back to periodic polling |
| Whole region outage | Cross-region storage + DC-level failover |

Graceful degradation everywhere: a degraded experience beats an outage.

## Sources

- [Xu Ch 15: Design Google Drive](software/system-design-interview/books/system-design-interview-insiders-guide/ch15_design_google_drive.md)
- [Liu Ch 6.06: Cloud File Storage](software/system-design-interview/books/system-design-interview-fundamentals/ch06_06_cloud_file_storage.md)
