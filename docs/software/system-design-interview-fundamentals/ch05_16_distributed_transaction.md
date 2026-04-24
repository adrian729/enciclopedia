# Ch 5.16: Distributed Transaction

## Table of Contents

- [1. The Core Problem](#1-the-core-problem)
- [2. Money Transfer and 2PC](#2-money-transfer-and-2pc)
- [3. Blob Storage and Metadata Storage](#3-blob-storage-and-metadata-storage)
- [4. Third Party Data Source](#4-third-party-data-source)
- [5. Database and Queue](#5-database-and-queue)
- [6. Cache and Storage Update](#6-cache-and-storage-update)
- [7. Abstract Design Choices](#7-abstract-design-choices)

## 1. The Core Problem

- **Distributed transaction** — a transaction involving more than one data source; complexity appears when a subset of sources successfully commits while the other subset fails
- **Comes up often** — it's something the interviewer may ask about or something you'll want to address yourself; you don't need to jump into it during high-level design, but be ready to handle it in deep dive

## 2. Money Transfer and 2PC

- **Setup** — consider pseudocode that adds `amount` to `to_user_database` then removes `amount` from `from_user_database`
- **Failure mode** — if `add_amount` commits successfully but `remove_amount` fails (e.g., `from_user` no longer has enough balance, or `from_user_database` is unavailable), the system is left in an inconsistent state where money has been credited but not debited
- **2-phase commit (2PC)** — a system can write to multiple sources with a **prepare** phase and a **commit** phase; once both sources agree they can commit, the coordinator pushes the 2nd-phase commit until it goes through
- **Why not 1 phase** — if one source commits and the other decides it can't, the system is inconsistent
- **2PC weakness** — if the coordinator is down, the service becomes unavailable

## 3. Blob Storage and Metadata Storage

- **Setup** — uploading a photo plus its metadata to two separate systems
- **Naive failure mode** — persist metadata first, then photo: if the photo commit fails, you have a metadata row with no photo blob
- **2PC coordinator option** — possible, but increases complexity and throughput cost; sometimes you don't control the service (e.g., Amazon S3)
- **Recommended approach** — persist to the blob store first, get the URL, then store the URL in metadata. If the metadata save fails, you're left with an **unreferenced blob**
- **Cleanup options** — run a background cleanup job to clear unreferenced blobs, or leave them alone for more data and cost in exchange for less complexity (no background job)

## 4. Third Party Data Source

- **Setup** — in some designs, you will have a service where you don't control the API contract and design, yet you need to make a distributed transaction with it

## 5. Database and Queue

- **Setup** — write to a database first, then emit an event to a queue to be processed asynchronously; the insertion into the queue can fail and the event can be lost
- **E-commerce example** — create a record for the order placed and enqueue an asynchronous fulfillment workflow; if the queue insertion fails, the order can be stuck unfulfilled

**Solution 1: Database Queue**

- Some databases support a post-processing queue where saving the record and inserting into the queue is transactional
- Not available when the database doesn't come with queue support

**Solution 2: Let It Be**

- Failure rate into the queue may be so low that occasional event loss is acceptable
- Pair with a background job that periodically checks for unprocessed records
- Viability depends on whether end-user impact of occasional loss is acceptable (e.g., an email notification about checkout success may tolerate rare loss)

## 6. Cache and Storage Update

- **Write-through cache** — a request to update a record updates the cache and the store at the same time; one of the two can fail
- **Worst-case failure** — cache updated but underlying store not updated — the cache serves a value that was never persisted to disk
- **Implication** — write-through cache can be quite challenging for this reason

## 7. Abstract Design Choices

- **Framework** — given Service A and Service B, think about design choices abstractly and, for each, walk through what happens on partial failure

| Option | Description |
|---|---|
| **Option 1** | Call A then B |
| **Option 2** | Call B then A |
| **Option 3** | Call A and B concurrently |
| **Option 4** | Call A and B with a coordinator |
| **Option 5** | Make A and B transactional |

- **Interview use** — when asked about distributed transaction complexity, bring up 2 to 3 options and walk through them with the interviewer; for each option, reason about what happens on partial failure and how the end-user experiences it
