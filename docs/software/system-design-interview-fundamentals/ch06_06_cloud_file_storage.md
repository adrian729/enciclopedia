# Ch 6.06: Cloud File Storage

## Table of Contents

- [1. Requirements](#1-requirements)
- [2. API](#2-api)
- [3. High-Level Design](#3-high-level-design)
- [4. Schema](#4-schema)
- [5. End-to-End Flow](#5-end-to-end-flow)
- [6. Deep Dives](#6-deep-dives)

## 1. Requirements

- **Prompt** — design cloud file storage where users store and organize files into folders (Google Drive style list view)
- **Scope narrowed to**: upload files, create folders within folders, view folder contents, download files. Thumbnails, search, labeling, sharing, permissions, click-into-file UX, and sorting are tabled
- **Assumptions** agreed with interviewer:
  - **100M DAU** in North America
  - Up to **50 GB per user**, no pricing tiers
  - Thousands of folders/files per folder is plausible
  - File size up to **1 GB**; common range **1 KB – 1 MB**
  - Read-to-write ratio **~20:1** (every upload triggers a page visit)
  - **Consistency** important across devices; **durability** important (data loss = terrible UX); **integrity** (no corruption) important
  - Fetch latency ~**300–400 ms p99**

## 2. API

```
add_folder(user_id, folder_id, name) → status
add_file(user_id, folder_id, file_bytes) → status
view_folder_items(user_id, folder_id, offset) → [folder_item]
download_file(user_id, file_url) → file_bytes
```

- `folder_item` is either a file or a folder
- `view_folder_items` paginates with an **offset**; page size is a constant; sorted by `created_at`

## 3. High-Level Design

- **Directory service** — thin pass-through for folder/file metadata reads and writes
- **Metadata storage** — folder and file tables
- **File blob storage** — stores raw file bytes; generates a `file_url` on write
- **Download service** — pass-through to file blob storage

## 4. Schema

**File Bytes Table** (blob storage)

| File ID | File Bytes |
|---|---|

**Folder Table** (metadata storage)

| User ID | Folder ID | Parent Folder ID | Created At | Folder Name |
|---|---|---|---|---|

**File Table** (metadata storage)

| User ID | File ID | Parent Folder ID | File Name | Created At | File URL |
|---|---|---|---|---|---|

## 5. End-to-End Flow

- **`add_folder`** — directory service writes to folder table
- **`add_file`** — bytes persisted to blob storage first → generated `file_url` saved to file table
- **`view_folder_items`** — directory service fetches folders + files by `parent_folder_id`, sorts by `created_at`, paginates by offset
- **`download_file`** — `file_url` fetched from blob storage through download service

## 6. Deep Dives

### 6.1 Normalized vs Denormalized Schema

| Option | Upside | Downside |
|---|---|---|
| Normalized (separate folder and file tables) | Clean entity separation | Requires union at read time |
| Denormalized (folder_file table with `type` column) | No union needed on `view_folder_items` | Entity strongly coupled to UI wireframe; worse extensibility |

- **Conclusion** — start with **normalized** (option 1); switch to denormalized if performance becomes an issue

### 6.2 Secondary Indexing

- **Query pattern** — primary key is `file_id`/`folder_id`, but reads filter by `parent_folder_id` and sort by `created_at`

| Option | Upside | Downside |
|---|---|---|
| Full table scan | Fast write | Slow read |
| Secondary index on `parent_folder_id` | Faster filter read | Slower write |
| Secondary index on `(parent_folder_id, created_at)` | Efficient top-N pagination (sorted within folder) | Slowest write |

- **Conclusion** — **option 3**, since reads dominate writes

### 6.3 Database Choice (cross-row transactions)

- **Added requirement** — support adding multiple files in one request; interviewer wants **all-or-nothing** (roll back partial success)

| Option | Upside | Downside |
|---|---|---|
| Wide column store | Write-optimized | LSM, no cross-row transactions; leaderless (Cassandra) has lossy writes |
| Document store | Simple blob model | No join/union on `parent_folder_id`; must union in application |
| **Relational (MySQL)** | Strong transactions, join/union, B-Tree fits read-heavy | Harder to scale writes |

- **Conclusion** — **relational database** like MySQL

### 6.4 Out-of-Sync Files Across Sessions

| Option | Upside | Downside |
|---|---|---|
| Pessimistic lock on the file | No concurrent modification | Only one person can edit at a time |
| **Optimistic lock** (version number) | Concurrent edits allowed | Retry storms in high concurrency |
| Display both versions on conflict | Keeps both edits | Branching divergence confuses users |

- **Conclusion** — **optimistic lock** plus an explicit conflict message ("Another user has already updated the file, here are the conflicts…")

### 6.5 File Upload Bandwidth

- **Scenario** — non-trivial file modification; passing the whole file every time is wasteful

| Option | Upside | Downside |
|---|---|---|
| Pass the whole file | Simplest | Re-sends unchanged bytes |
| **Pass chunks (rsync)** | Minimal bytes when files are similar | Checksum overhead when files are completely different |
| Lossless compression (e.g., run-length encoding) | Fewer bytes | Encode/decode CPU cost |

- **Conclusion** — **chunked diff (rsync-style)** as primary; add lossless compression if CPU overhead is acceptable; A/B test

### 6.6 Scale It Up (sharding the relational DB)

- **Math** — 100M DAU × 2 visits × 1.5 peak = **3×10⁸ QPD** → ~**3,000 read QPS**, writes a fraction. At 300–500 QPS per DB, need ~10 shards
- **Cache** is rejected first: strong consistency requirement makes cache invalidation on write the same cost as writing to the DB

| Option | Upside | Downside |
|---|---|---|
| Shard by `parent_folder_id` | Same-shard reads for a folder | Hot shard on home directory (`parent_folder_id = 0`) |
| Shard by `user_id` | No folder-0 hotspot | Superuser hotspot |
| Shard by `folder_id` | No folder or user hotspot | Scatter-gather when fetching by `parent_folder_id` |
| **Shard by `(user_id, parent_folder_id)`** | Single-shard read per folder; distributes superusers across nodes | Hotspot only if a superuser crams one folder |

- **Conclusion** — **shard by `(user_id, parent_folder_id)`**; monitor for the narrow case where a power user stuffs one folder

### 6.7 Folder Deletion

- **Requirement** — permanently delete files within a deleted folder

| Option | Upside | Downside |
|---|---|---|
| Recursive synchronous delete | Immediate reflection | Unpredictable duration for large folders; can time out or overload DB; irreversible |
| **Mark and sweep** (add `status` column: ACTIVE/TRASH) | Soft delete; schedule sweeps off-peak; undo possible; archive option | Extra storage until swept |

- **Conclusion** — **mark and sweep**
