# Ch 15: Design Google Drive

## Table of Contents

- [1. Requirements and Scope](#1-requirements-and-scope)
- [2. Back-of-the-Envelope Estimation](#2-back-of-the-envelope-estimation)
- [3. Single-Server Starting Point](#3-single-server-starting-point)
- [4. APIs](#4-apis)
- [5. Scaling Out: Sharding and S3](#5-scaling-out-sharding-and-s3)
- [6. Sync Conflicts](#6-sync-conflicts)
- [7. High-Level Design](#7-high-level-design)
- [8. Block Servers and Delta Sync](#8-block-servers-and-delta-sync)
- [9. Strong Consistency](#9-strong-consistency)
- [10. Metadata Database Schema](#10-metadata-database-schema)
- [11. Upload and Download Flows](#11-upload-and-download-flows)
- [12. Notification Service](#12-notification-service)
- [13. Saving Storage Space](#13-saving-storage-space)
- [14. Failure Handling](#14-failure-handling)
- [15. Wrap-Up Tradeoffs](#15-wrap-up-tradeoffs)

## 1. Requirements and Scope

- **Target features** — upload/download files, sync across devices, file revision history, sharing, and notifications when a file is edited/deleted/shared
- **Constraints agreed in interview** — mobile + web, any file type, files encrypted at rest, max file size 10 GB, 10M DAU
- **Out of scope** — Google Doc-style real-time collaborative editing
- **Non-functional requirements** — reliability (no data loss), fast sync, low bandwidth usage (mobile data plans), scalability, high availability

## 2. Back-of-the-Envelope Estimation

- **Users and storage** — 50M signed-up users × 10 GB free space = **500 PB total**
- **Traffic** — 10M DAU × 2 uploads × 500 KB; 1:1 read/write ratio
- **QPS** — 10M × 2 / 86,400s ≈ 240 upload QPS; peak ≈ 480

## 3. Single-Server Starting Point

- **Setup** — Apache web server + MySQL DB + a `drive/` directory with 1 TB; each user gets a **namespace** (subdirectory) holding their files
- **Why start here** — narrative pedagogy: refresh fundamentals, then iterate. Each file/folder is uniquely identified by `namespace + relative path`

## 4. APIs

- **Three core APIs** — upload, download, list revisions; all require authentication and run over HTTPS (SSL)
- **Upload types**
  - **Simple upload** — for small files
  - **Resumable upload** — for large files prone to network interruption; three steps: send initial request to get a resumable URL, upload data while monitoring state, resume on disturbance
- **Download** — `GET /files/download` with `path` parameter
- **List revisions** — `GET /files/list_revisions` with `path` and `limit`

## 5. Scaling Out: Sharding and S3

- **Storage exhaustion** — single server fills up; first fix is to shard storage by `user_id` across multiple servers
- **Move file storage to Amazon S3** — "industry-leading scalability, data availability, security, and performance"; supports same-region and cross-region replication. Files stored across regions for durability and availability
- **Bucket** — like a folder in a file system
- **Further improvements**
  - **Load balancer** — distributes traffic and reroutes around failed web servers
  - **Web servers** — easy to add/remove behind the LB
  - **Metadata database** — moved off the box; replicated and sharded
  - **File storage** — S3 with cross-region replication

## 6. Sync Conflicts

- **Strategy** — first version processed wins; the late version receives a conflict
- **Resolution** — present both versions to the late user (local copy + latest server version); user can merge or override
- **Real-time co-editing** — keeping a doc synchronized while many users edit simultaneously is hard; out of scope (pointer to differential synchronization references)

## 7. High-Level Design

- **Components**
  - **Block servers** — upload blocks to cloud storage. A file is split into blocks, each with a unique hash stored in the metadata DB; blocks are independent objects in the storage system (S3) and joined in order to reconstruct a file. Max block size 4 MB (Dropbox reference)
  - **Cloud storage** — stores the blocks
  - **Cold storage** — for inactive data not accessed in a long time
  - **Load balancer** — distributes traffic to API servers
  - **API servers** — handle everything except the upload data path: auth, profile, metadata updates
  - **Metadata database** — users, files, blocks, versions; only metadata, not file content
  - **Metadata cache** — cached metadata for fast retrieval
  - **Notification service** — pub/sub-style; pushes events to clients when files change so they can pull the latest changes
  - **Offline backup queue** — buffers change info for offline clients to apply when they reconnect

## 8. Block Servers and Delta Sync

- **Why block servers exist** — re-uploading the entire file on each edit wastes bandwidth
- **Delta sync** — when a file is modified, only modified blocks are synced instead of the whole file, using a sync algorithm
- **Compression** — applied per block; algorithm picked by file type (gzip/bzip2 for text, others for images/video)
- **Block server flow on new file** — split file → compress each block → encrypt → upload to cloud
- **Delta sync example** — if only blocks 2 and 5 changed, only those two are uploaded

## 9. Strong Consistency

- **Requirement** — all clients must see the same view of a file at any moment
- **Cache + DB consistency rules**
  - Replicas and master must hold the same data
  - Invalidate cache on every DB write
- **DB choice** — relational, because **ACID** (Atomicity, Consistency, Isolation, Durability) is native; NoSQL would require ACID to be implemented manually in sync logic

## 10. Metadata Database Schema

- **User** — basic info (username, email, profile photo)
- **Device** — device records including `push_id` for mobile push notifications; one user can have many devices
- **Namespace** — root directory of a user
- **File** — metadata for the latest version of each file
- **File_version** — version history; rows are read-only to preserve revision integrity
- **Block** — block-level info; any version can be reconstructed by joining its blocks in order

## 11. Upload and Download Flows

- **Upload — two parallel paths originating from client 1**
  - **Add file metadata** — client sends metadata → DB stores it with status `pending` → notify notification service → notification service informs other clients (e.g., client 2) that a file is being uploaded
  - **Upload file to cloud storage** — client uploads content to block servers → block servers chunk/compress/encrypt → write to cloud storage → cloud storage triggers upload-completion callback to API servers → status becomes `uploaded` → notification service informs client 2 the file is fully uploaded
- **Edit flow** — same shape as upload
- **Download flow trigger** — file added/edited elsewhere
  - **Online client** — notification service pushes a change notice → client requests metadata via API
  - **Offline client** — change is saved to cache; pulled when client reconnects
- **Download steps** — notification → fetch metadata via API/DB → request blocks from block servers → block servers download from cloud → assemble blocks into the file

## 12. Notification Service

- **Purpose** — propagate any local file mutation to other clients to reduce conflicts
- **Options compared**

| Option | Used by | Notes |
|---|---|---|
| **Long polling** | Dropbox | Chosen — communication is one-way (server → client); notifications are infrequent with no bursts |
| **WebSocket** | — | Better for real-time bidirectional traffic like chat; overkill here |

- **Long polling protocol** — client opens a long poll → on file change, server closes the connection → client must hit the metadata server for the latest changes → after response or timeout, client immediately reconnects to keep the channel open

## 13. Saving Storage Space

- **De-duplicate blocks** — eliminate identical blocks (same hash) at the account level
- **Intelligent backup strategy**
  - **Set a limit** — cap number of stored versions; oldest is replaced when limit is reached
  - **Keep valuable versions only** — heavily edited docs could save 1000+ versions in a short period; weight recent versions more, prune the rest based on experimentation
- **Cold storage tiering** — move data inactive for months/years to cheaper cold storage like Amazon S3 Glacier

## 14. Failure Handling

- **Load balancer failure** — secondary takes over; LBs monitor each other via heartbeat
- **Block server failure** — other servers pick up unfinished/pending jobs
- **Cloud storage failure** — S3 buckets are cross-region replicated; fetch from another region
- **API server failure** — stateless; LB redirects traffic
- **Metadata cache failure** — replicated; bring up a new node
- **Metadata DB**
  - **Master down** — promote a slave; provision a new slave
  - **Slave down** — use another slave for reads; replace the failed one
- **Notification service failure** — every online user holds a long poll connection; per the Dropbox 2012 talk, >1M connections per machine. If a server dies, all those connections are lost and clients must reconnect to a different server — slow because reconnecting all clients at once is hard
- **Offline backup queue failure** — queues are replicated; consumers re-subscribe to the backup queue

## 15. Wrap-Up Tradeoffs

- **Direct client-to-cloud uploads (alternative)** — faster (one transfer instead of two), but requires reimplementing chunking/compression/encryption on every platform (iOS, Android, Web), and putting encryption logic on the client is risky since clients can be hacked or manipulated. Centralizing this in block servers is safer
- **Presence service** — splitting online/offline tracking out of the notification servers would let other services reuse it
- **No perfect solution** — every company's constraints are different; understanding the tradeoffs is what matters
