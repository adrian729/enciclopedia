# Ch 8: Distributed Email Service

## Table of Contents

- [1. Problem and Scope](#1-problem-and-scope)
- [2. Email Protocols and Traditional Servers](#2-email-protocols-and-traditional-servers)
- [3. Distributed Architecture](#3-distributed-architecture)
- [4. Sending and Receiving Flows](#4-sending-and-receiving-flows)
- [5. Metadata Database Design](#5-metadata-database-design)
- [6. Search](#6-search)
- [7. Email Deliverability](#7-email-deliverability)
- [8. Scalability and Availability](#8-scalability-and-availability)

## 1. Problem and Scope

- **Distributed email service** — Gmail/Outlook/Yahoo Mail-scale system supporting send/receive, fetch all emails, read/unread filtering, full-text search across subject/sender/body, anti-spam, and anti-virus. Authentication is out of scope.
- **Client transport assumed** — HTTP between client and server (rather than legacy POP/IMAP/SMTP for the user-facing layer); attachments allowed.
- **Scale** — 1B users, avg 10 sends + 40 receives/user/day → **100,000 send QPS**; metadata avg 50 KB/email → **730 PB/year metadata**; 20% of emails carry ~500 KB attachments → **1,460 PB/year of attachments**. Storage-heavy by nature, so a distributed DB is required.
- **Non-functional requirements** — reliability (no data loss), availability (replicated, survives partial failure), scalability (no degradation with growth), flexibility/extensibility (custom protocols are likely needed because POP/IMAP are too limited for modern features).

## 2. Email Protocols and Traditional Servers

| Protocol | Role |
|---|---|
| **SMTP** | Standard for **sending** mail server-to-server |
| **POP** | Downloads to one device and **deletes from server** (RFC 1939) — must download the whole message |
| **IMAP** | Reads remotely, leaves mail on server, multi-device, only fetches headers until a message is opened — most common for individual accounts |
| **HTTPS** | Not technically email, but used by web/mobile clients (e.g., Outlook ActiveSync) |

- **MX records** — DNS lookup returns mail-exchanger records ranked by priority (lower number first, e.g., `gmail-smtp-in.l.google.com` priority 5, then `alt1.…` priority 10); senders try in priority order.
- **Attachments** — sent inline using **MIME** with **Base64** encoding; provider limits e.g. Outlook 20 MB, Gmail 25 MB.
- **Traditional flow (Alice → Bob)** — Alice's client SMTPs the email to her Outlook server; Outlook DNS-resolves Gmail's MX; Outlook SMTPs to Gmail; Gmail stores it; Bob's client fetches via IMAP/POP.
- **Why traditional storage doesn't scale** — old systems used file directories (e.g., **Maildir**) with one file per email. Disk I/O becomes the bottleneck at scale, and local files give no HA. Email protocols themselves date from the 1960s and weren't designed for threading/labels/search/multimedia or billions of users.

## 3. Distributed Architecture

- **Webmail + Web servers** — browser clients hit stateless web servers that handle login, profile, send-email API, folder loading, etc.
- **Real-time servers** — stateful long-lived connections that push new emails to online clients. Prefer **WebSocket** with **long polling fallback** for browser-compat. Apache James implements **JMAP over WebSocket** as a real-world example.
- **Metadata database** — stores subject, body, from/to, flags. Custom-built at Gmail/Outlook scale.
- **Attachment store** — object storage (e.g., **Amazon S3**), required because emails carry up to ~25 MB blobs. **Cassandra is rejected**: theoretical 2 GB blob, practical limit <1 MB, and large blobs break the row cache.
- **Distributed cache (Redis)** — caches recently accessed emails since most reads target recent data; Redis lists fit the inbox model and scale easily.
- **Search store** — distributed document store using an **inverted index** for full-text search.

## 4. Sending and Receiving Flows

- **Email REST APIs (HTTP)** — `POST /v1/messages` (send), `GET /v1/folders` (list folders; default set per RFC 6154: All, Archive, Drafts, Flagged, Junk, Sent, Trash), `GET /v1/folders/{folder_id}/messages` (paginated — must support both consecutive and range-based paging for random checkpoint access), `GET /v1/messages/{message_id}`.
- **Send flow** — load balancer (rate-limit) → web server validates (size limit etc.); **same-domain shortcut**: if recipient is on the same domain, write straight to storage/cache/object store and skip outbound. Otherwise message goes to an **outgoing queue** (or **error queue** on validation failure); SMTP outgoing workers run spam/virus checks, write to the sender's "Sent" folder, then SMTP-deliver to the recipient's mail server.
- **Outgoing-queue health monitoring** — backlog signals either a down recipient server (use **exponential backoff** retries) or insufficient consumers (scale workers).
- **Receive flow** — incoming SMTP load balancer → SMTP servers (apply email acceptance policy at connection level; bounce invalid early); large attachments go straight to S3; messages enter an **incoming queue** that decouples mail-processing workers (spam/virus filtering) from SMTP intake; passing emails are written to mail storage/cache/object store; if recipient is online, push via real-time WebSocket server, else they fetch via REST when they reconnect.

## 5. Metadata Database Design

- **Workload characteristics** — small frequently-read headers vs. larger seldom-read bodies (each email read ~once); operations are isolated per user; **82% of read queries hit data younger than 16 days**; data loss is unacceptable.
- **DB option analysis** — **relational** is bad for the >100 KB HTML emails (BLOB search is inefficient); **object storage alone** (S3) can't support read flags / search / threading; **NoSQL** is the leading candidate. Bigtable is what Gmail uses (closed-source). Large providers ultimately build **custom KV stores** with these properties: support multi-MB columns, strong consistency, minimized disk I/O, HA + fault tolerance, easy incremental backups.
- **Partitioning** — `user_id` as partition key keeps a user's data on one shard; trade-off: sharing messages across users isn't supported, but it's not a stated requirement.

| Query | Table | Partition key | Clustering key |
|---|---|---|---|
| Folders for a user | `folders` | `user_id` | — |
| Emails in a folder, newest first | `emails_by_folder` | `(user_id, folder_id)` composite | `email_id` (TIMEUUID for chrono order) |
| Get/create/delete a specific email | `emails_by_user`, attachments by `(email_id, filename)` | `user_id` | `email_id` |
| Read vs unread | denormalized into **`read_emails`** and **`unread_emails`** tables | `(user_id, folder_id)` | `email_id` |

- **Why denormalize read/unread** — NoSQL only filters efficiently on partition/cluster keys, and `is_read` is neither. Filtering in the app over a whole folder doesn't scale. Maintaining two tables and **moving rows on read** trades write complexity for fast reads at scale.
- **Conversation threads (bonus)** — clients reconstruct threads from headers `Message-Id` (per-message), `In-Reply-To` (parent's Message-Id), and `References` (full chain); the **JWZ algorithm** is the classic implementation.
- **Consistency trade-off** — distributed DBs trade consistency vs availability under replication. Email correctness matters more than uptime: each mailbox has a **single primary**, and during failover the mailbox is **paused** rather than served stale — favoring consistency over availability.

## 6. Search

- **Email search vs Google search** — scoped to one user's mailbox, sorts by attributes (time, has_attachment, unread) not relevance, and demands **near real-time, accurate** indexing. Reads are infrequent (only when the user clicks Search), but writes/reindexes happen on every send/receive/delete — so the workload is **write-heavy on indexing**.

| Feature | Elasticsearch | Custom search engine |
|---|---|---|
| Scalability | Scales somewhat | Easier to optimize for email specifics |
| System complexity | Two systems (datastore + ES) | One system |
| Data consistency | Two copies, hard to keep in sync | Single copy in metadata store |
| Data loss risk | None (rebuild ES from primary) | None |
| Effort | Easy to integrate; large-scale needs a dedicated ES team | Significant engineering investment |

- **Elasticsearch path** — partition documents by `user_id` to colocate a user's index. Reindexing is decoupled via **Kafka** between event-producing services and indexing workers; search requests stay synchronous. Most popular search engine as of June 2021.
- **Custom engine path** — dominant constraint is **disk I/O** (PB-scale daily ingest, 500K+ emails per heavy user). Use a **Log-Structured Merge-Tree (LSM)**: in-memory level 0, merged to disk levels in sequential writes — same structure behind Bigtable, Cassandra, RocksDB. LSM also lets you separate frequently-changing data (folder/labels) from immutable data (email body) so a folder change doesn't rewrite email bodies.
- **Rule of thumb** — Elasticsearch for smaller scale; for Gmail/Outlook scale, embed search natively in the database. Microsoft Exchange's search is cited as a reference.

## 7. Email Deliverability

- **Reputation problem** — **>50% of all emails are spam (Statista)**, so new mail servers default to the spam folder until they earn ISP trust.
- **Deliverability tactics** — use **dedicated IPs**; **classify** emails by purpose (don't mix marketing and transactional from the same IP, or ISPs flag everything as promotional); **warm up new IPs slowly** (Amazon SES estimates 2–6 weeks); **ban spammers fast** to protect reputation; on failure, **retry** with bounded attempts then park in a monitored queue.
- **Feedback processing** — set up ISP feedback loops; outcomes are **hard bounce** (invalid recipient — permanent), **soft bounce** (temporary issue, e.g., ISP busy), or **complaint** (user clicked "report spam"). Use **separate queues** per category so they're handled independently.
- **Email authentication** — combat phishing/pretexting (93% of breaches per Verizon's 2018 DBIR) with **SPF**, **DKIM**, and **DMARC**; legit Gmail headers show all three passing for the sender domain.

## 8. Scalability and Availability

- **Horizontal scalability is natural** — per-user data access patterns are independent, so most components scale by adding nodes.
- **Multi-data-center replication** — data replicated across DCs; users connect to the topologically nearest DC; during a network partition, users can still read messages from a different DC.
- **Open follow-ups for the interview wrap-up**:
  - **Fault tolerance** — node failures, network issues, event delays.
  - **Compliance** — **GDPR** for EU PII; **legal intercept** capability.
  - **Security** — phishing protection, safe browsing, proactive alerts, account safety, confidential mode, encryption (Gmail's safety stack).
  - **Optimizations** — deduplicate attachments in S3 (the same file sent to many recipients should be stored once; check existence before save).
