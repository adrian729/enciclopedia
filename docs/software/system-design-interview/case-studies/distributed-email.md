# Distributed Email Service (Gmail/Outlook Scale)

> Vol 2 only — neither Liu nor Xu Vol 1 covers email. The killer detail is the **metadata DB choice**: workload analysis shows isolated per-user operations and **82% of read queries hit data younger than 16 days**, which rules out relational (poor at large HTML BLOBs) and pure object storage (no read flags or threading). Large providers ultimately build **custom KV stores** with multi-MB columns, strong consistency, easy incremental backups. Read/unread are **denormalized into separate tables** because NoSQL can't filter on a non-key column efficiently.

## Table of Contents

- [1. Requirements](#1-requirements)
- [2. Email Protocols](#2-email-protocols)
- [3. Distributed Architecture](#3-distributed-architecture)
- [4. Send and Receive Flows](#4-send-and-receive-flows)
- [5. Metadata Database Design](#5-metadata-database-design)
- [6. Search](#6-search)
- [7. Email Deliverability](#7-email-deliverability)
- [8. Scalability and Availability](#8-scalability-and-availability)
- [Sources](#sources)

## 1. Requirements

Gmail/Outlook/Yahoo Mail-scale system. Send/receive, fetch all emails, read/unread filtering, **full-text search** across subject/sender/body, anti-spam, anti-virus. Authentication is out of scope.

- Client transport assumed: HTTP (rather than legacy POP/IMAP/SMTP for the user-facing layer); attachments allowed.
- Scale: 1B users, avg 10 sends + 40 receives/user/day → **100K send QPS**. Metadata avg 50 KB/email → **730 PB/year**. 20% of emails carry ~500 KB attachments → **1,460 PB/year**.
- Storage-heavy by nature, so a distributed DB is required.

## 2. Email Protocols

| Protocol | Role |
|---|---|
| **SMTP** | Standard for **sending** server-to-server |
| **POP** | Downloads to one device, deletes from server (RFC 1939) |
| **IMAP** | Reads remotely, leaves on server, multi-device — most common |
| **HTTPS** | Used by web/mobile clients (e.g., Outlook ActiveSync) |

**MX records** — DNS lookup returns mail-exchanger records ranked by priority. **Attachments** sent inline using **MIME** with **Base64** encoding; provider limits (Outlook 20 MB, Gmail 25 MB).

**Why traditional storage doesn't scale** — old systems used file directories (e.g., **Maildir**) with one file per email. Disk I/O bottlenecks at scale and local files give no HA. The 1960s-era email protocols themselves weren't designed for threading, labels, search, multimedia, or billions of users.

## 3. Distributed Architecture

- **Webmail + Web servers** — stateless servers that handle login, profile, send-email API, folder loading.
- **Real-time servers** — stateful long-lived connections push new emails to online clients. Prefer **WebSocket** with **long polling fallback**. Apache James implements **JMAP over WebSocket** as a real-world example. See [Real-Time Communication](fundamentals/real-time-communication.md).
- **Metadata database** — custom-built at Gmail/Outlook scale (see §5).
- **Attachment store** — object storage (e.g., **Amazon S3**), required because emails carry up to ~25 MB blobs. **Cassandra is rejected** — theoretical 2 GB blob limit, practical limit <1 MB, large blobs break the row cache.
- **Distributed cache (Redis)** — caches recently accessed emails since most reads target recent data; Redis lists fit the inbox model.
- **Search store** — distributed document store using an inverted index. See [Full-Text Search](fundamentals/full-text-search.md).

## 4. Send and Receive Flows

**REST APIs:**

```
POST /v1/messages                                # send
GET /v1/folders                                  # list folders
GET /v1/folders/{folder_id}/messages             # paginated; supports both consecutive and range-based paging
GET /v1/messages/{message_id}
```

**Send flow** — load balancer (rate-limit) → web server validates → **same-domain shortcut**: if recipient is on the same domain, write straight to storage/cache/object store and skip outbound. Otherwise: **outgoing queue** (or error queue on validation failure) → SMTP outgoing workers run spam/virus checks → write to sender's "Sent" folder → SMTP-deliver to recipient's mail server.

**Outgoing queue health** — backlog signals either a down recipient server (use **exponential backoff** retries) or insufficient consumers (scale workers). See [Queues & Messaging](fundamentals/queues-and-messaging.md).

**Receive flow** — incoming SMTP load balancer → SMTP servers (apply email acceptance policy at connection level; bounce invalid early) → large attachments go straight to S3 → messages enter an **incoming queue** that decouples mail-processing workers (spam/virus filtering) from SMTP intake → passing emails written to mail storage/cache/object store → if recipient is online, push via real-time WebSocket; else they fetch via REST when they reconnect.

## 5. Metadata Database Design

**Workload characteristics** — small frequently-read headers vs. larger seldom-read bodies (each email read ~once); operations are isolated per user; **82% of read queries hit data younger than 16 days**; data loss is unacceptable.

**DB option analysis:**

- Relational is bad for >100 KB HTML emails (BLOB search is inefficient).
- Object storage alone (S3) can't support read flags / search / threading.
- **NoSQL** is the leading candidate. Bigtable is what Gmail uses (closed-source). Large providers ultimately build **custom KV stores** with: multi-MB columns, strong consistency, minimized disk I/O, HA + fault tolerance, easy incremental backups.

**Partition by `user_id`** — keeps a user's data on one shard; trade-off: sharing messages across users isn't supported (not a stated requirement).

| Query | Table | Partition key | Clustering key |
|---|---|---|---|
| Folders for a user | `folders` | `user_id` | — |
| Emails in a folder, newest first | `emails_by_folder` | `(user_id, folder_id)` | `email_id` (TIMEUUID for chrono) |
| Get/create/delete a specific email | `emails_by_user`, attachments by `(email_id, filename)` | `user_id` | `email_id` |
| Read vs unread | denormalized into `read_emails` and `unread_emails` | `(user_id, folder_id)` | `email_id` |

**Why denormalize read/unread** — NoSQL only filters efficiently on partition/cluster keys, and `is_read` is neither. Filtering in the app over a whole folder doesn't scale. Maintaining two tables and **moving rows on read** trades write complexity for fast reads at scale.

**Conversation threads** — clients reconstruct threads from headers `Message-Id` (per-message), `In-Reply-To` (parent), and `References` (full chain); the **JWZ algorithm** is the classic implementation.

**Consistency trade-off** — distributed DBs trade consistency vs availability under replication. Email correctness matters more than uptime: each mailbox has a **single primary**, and during failover the mailbox is **paused** rather than served stale — favoring consistency over availability. See [CAP, Consensus & Conflict Resolution](fundamentals/cap-consensus-and-conflict-resolution.md).

## 6. Search

Email search differs from Google search: scoped to one user, sorts by attributes (time, has_attachment, unread) not relevance, demands **near real-time, accurate** indexing. Reads are infrequent (only when the user clicks Search), but writes/reindexes happen on every send/receive/delete — so the workload is **write-heavy on indexing**.

| Feature | Elasticsearch | Custom search engine |
|---|---|---|
| Scalability | Scales somewhat | Easier to optimize for email specifics |
| System complexity | Two systems (datastore + ES) | One system |
| Data consistency | Two copies, hard to keep in sync | Single copy in metadata store |
| Effort | Easy to integrate; large-scale needs a dedicated ES team | Significant engineering investment |

**Elasticsearch path** — partition documents by `user_id`. Reindexing is decoupled via **Kafka** between event-producing services and indexing workers; search requests stay synchronous.

**Custom path** — dominant constraint is **disk I/O** (PB-scale daily ingest, 500K+ emails per heavy user). Use a **Log-Structured Merge-Tree (LSM)**: in-memory level 0, merged to disk levels in sequential writes (same structure behind Bigtable, Cassandra, RocksDB). LSM also lets you separate frequently-changing data (folder/labels) from immutable data (email body) so a folder change doesn't rewrite email bodies.

**Rule of thumb** — Elasticsearch for smaller scale; for Gmail/Outlook scale, embed search natively in the database. Microsoft Exchange's search is the industry reference.

## 7. Email Deliverability

**>50% of all emails are spam** (Statista), so new mail servers default to the spam folder until they earn ISP trust.

**Tactics:**

- Use **dedicated IPs**.
- **Classify** emails by purpose (don't mix marketing and transactional from the same IP, or ISPs flag everything as promotional).
- **Warm up new IPs slowly** (Amazon SES estimates 2–6 weeks).
- **Ban spammers fast** to protect reputation.
- On failure, **retry** with bounded attempts then park in a monitored queue.

**Feedback processing** — set up ISP feedback loops; outcomes are **hard bounce** (invalid recipient — permanent), **soft bounce** (temporary issue), or **complaint** (user reported spam). Use **separate queues** per category.

**Email authentication** — combat phishing/pretexting (93% of breaches per Verizon 2018 DBIR) with **SPF**, **DKIM**, **DMARC**.

## 8. Scalability and Availability

Per-user data access is independent, so most components scale by adding nodes.

**Multi-data-center replication** — data replicated across DCs; users connect to the topologically nearest DC; during a network partition, users can still read messages from a different DC.

**Open follow-ups** — fault tolerance, GDPR + legal intercept, phishing protection, encryption (Gmail's safety stack), attachment deduplication in S3 (the same file sent to many recipients should be stored once; check existence before save).

## Sources

- [Vol 2 Ch 8: Distributed Email Service](software/system-design-interview/books/system-design-interview-vol2/ch08_distributed_email_service.md)
