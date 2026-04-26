# S3-like Object Storage

> Vol 2 only — neither Liu nor Xu Vol 1 covers immutable object stores. The architectural insight is **object immutability** — objects can be replaced or deleted but never edited in place — which buys vast scale and durability. The design separates a **mutable metadata store** (UNIX inode-equivalent) from an **immutable data store** (file-block-equivalent). Distinct from [Cloud File Storage](case-studies/cloud-file-storage.md), which is the Drive/Dropbox delta-sync problem with mutable metadata.

## Table of Contents

- [1. Storage Taxonomy](#1-storage-taxonomy)
- [2. Requirements](#2-requirements)
- [3. High-Level Design](#3-high-level-design)
- [4. Upload and Download Flows](#4-upload-and-download-flows)
- [5. Data Store Internals](#5-data-store-internals)
- [6. Replication vs Erasure Coding](#6-replication-vs-erasure-coding)
- [7. Metadata Store and Listing](#7-metadata-store-and-listing)
- [8. Versioning, Multipart Upload, Garbage Collection](#8-versioning-multipart-upload-garbage-collection)
- [Sources](#sources)

## 1. Storage Taxonomy

| Class | Mutability | Performance | Use case |
|---|---|---|---|
| **Block storage** | Mutable, raw blocks owned by one server | Highest | Databases, VMs |
| **File storage** | Mutable hierarchical files/dirs (NFS/SMB) | Medium | General-purpose |
| **Object storage** | **Immutable** flat namespace, REST API | Low–medium, vast scale, low cost | Cold/archival data (S3, GCS, Azure Blob) |

- **Bucket** — globally-unique logical container; must exist before objects can be uploaded.
- **Object** — payload (any byte sequence) plus metadata (name-value pairs); URI: `s3://bucket-name/object-name`.
- **Versioning** — bucket-level feature that keeps multiple variants of an object so accidental deletes/overwrites can be recovered.
- **SLA example (S3 Standard-IA)** — 11 nines durability across multiple AZs, survives one full AZ destruction, 99.9% availability.

## 2. Requirements

- Functional: bucket creation, object upload/download, versioning, listing.
- Non-functional: 100 PB stored in year one, **6 nines durability** (99.9999%), **4 nines availability** (99.99%), strong storage efficiency.
- Object-size mix: 20% small (<1 MB), 60% medium (1–64 MB), 20% large (>64 MB).
- Capacity: at 40% disk-usage ratio, 100 PB holds ~0.68 billion objects; at ~1 KB metadata per object, ~0.68 TB of metadata.
- IOPS budget: 7200 rpm SATA disk does ~100–150 random seeks/sec → bottleneck for small-object workloads.

## 3. High-Level Design

The architectural insight is **object immutability** — objects can be replaced or deleted but never edited in place. **UNIX inode analogy**: separate metadata store (mutable) from data store (immutable); each independently optimized.

Per LinkedIn research, **~95% of object-storage requests are reads**, justifying read-optimized choices.

```
Client → Load Balancer → API Service → IAM (authn/authz)
                                     → Metadata Store
                                     → Data Store
```

The API service orchestrates RPCs across the three. Metadata and data stores are logical roles; some systems (Ceph Rados Gateway) collapse them into a single object substrate.

## 4. Upload and Download Flows

**Bucket creation** — client `PUT /bucket-to-share` → IAM `WRITE` check → metadata store inserts a bucket row.

**Object upload (7 steps)** — client `PUT /bucket/script.txt` → IAM check → API streams payload to data store → data store returns a UUID → API writes a metadata row `(object_name, object_id, bucket_id)`.

**Logical hierarchy** — buckets are flat; "folders" are simulated by including slashes in the object name (e.g., `bucket-to-share/script.txt`).

**Object download** — IAM `READ` check → metadata lookup translates `(bucket, name)` → UUID → data store fetch by UUID → response body.

**HTTP shape** — uploads use `PUT` with `Content-Length`, `Authorization`, optional `x-amz-meta-*` user metadata headers; downloads use `GET` returning the raw payload. See [API Design & Gateway](fundamentals/api-design-and-gateway.md).

## 5. Data Store Internals

Three subcomponents:

- **Data Routing Service** — stateless, REST/gRPC.
- **Placement Service** — cluster topology + replica placement.
- **Data Nodes** — actual disks.

### Placement and replication

- **Virtual cluster map** — placement service tracks physical topology (datacenter → rack → node) so replicas spread across **failure domains**; data nodes heartbeat continuously, marked "down" after a 15-second grace period.
- **Consensus-backed placement** — run 5 or 7 placement nodes with Paxos or Raft; tolerates `floor(n/2)` failures (e.g., 3 of 7).
- **Replication group lookup** — given an object UUID, placement service returns a deterministic set of (primary + secondaries); typically implemented with consistent hashing so adding/removing nodes doesn't reshuffle everything. See [Sharding & Consistent Hashing](fundamentals/sharding-and-consistent-hashing.md).
- **Three replicas, primary-coordinated** — data router writes to primary; primary replicates to two secondaries before acking; reliability ≈ 1 − 0.0081³ ≈ **6 nines** assuming 0.81% annual disk-failure rate.
- **Consistency vs latency knob** — ack after all 3 replicas (strong, slow), after primary + 1 secondary (medium), or after primary only (weak, fast).

### Small-file packing and object lookup

- **Why not one file per object** — small files waste disk blocks (a <4 KB object still consumes a full 4 KB block) and exhaust the file system's fixed inode table.
- **WAL-style packing** — append many small objects into one large read-write file; once it hits a few-GB threshold, mark it read-only and open a new read-write file. **Modern multi-core servers need one read-write file per core** to avoid serialization on writes.
- **Object lookup table** — local SQLite database on each data node holds `object_mapping(object_id, file_name, start_offset, object_size)`; per-node isolation means no cross-node coordination.
- **RocksDB vs RDBMS** — RocksDB (SSTable) wins on writes; B+ tree RDBMS wins on reads; given write-once/read-many, the relational DB is preferred.

## 6. Replication vs Erasure Coding

**Erasure coding (k+m)** splits an object into k data chunks plus m parity chunks computed via a linear formula; tolerates up to m simultaneous chunk losses. The **(8+4)** example: 8 data + 4 parity = 12 chunks total, all reconstructable as long as ≥8 of 12 are healthy.

| Dimension | Replication (3×) | Erasure Coding (8+4) |
|---|---|---|
| Durability | 6 nines | **11 nines** |
| Storage overhead | 200% | **50%** |
| Compute | None | Parity calc on write, reconstruct on read |
| Write latency | **Low** | Higher — must compute parities |
| Read latency | **Low** | Higher — multi-node fetch |
| Use case | **Latency-sensitive** | Cost-minimizing archival |

**Checksum verification** — append MD5 (or SHA1/HMAC) at end of each object and per file; mismatch triggers reconstruction from another failure domain. Catches in-memory corruption that disk failure detection misses.

The book uses **replication as the primary mechanism**; erasure coding is the cost-optimization alternative. See [Replication](fundamentals/replication.md).

## 7. Metadata Store and Listing

**Two tables** — `bucket(bucket_id, owner_id, ...)` and `object(object_id, bucket_id, object_name, ...)`.

**Bucket table is small** — 1M users × 10 buckets × 1 KB ≈ 10 GB; fits one server, scale reads with replicas.

**Object table sharding** — shard by `hash(bucket_name, object_name)` rather than `bucket_id` (hot bucket) or `object_id` (breaks URI lookups); URI-based queries map to a single shard.

**Three listing query types** — list user's buckets, list one level under a prefix (rolling up deeper paths into common prefixes), recursive list under a prefix.

**Prefixes are not directories** — `s3://mybucket/abc/d/e/f/file.txt` has bucket `mybucket`, object name `abc/d/e/f/file.txt`, prefix `abc/d/e/f/`; rollups happen in application code.

**Sharded paging is hard** — every shard returns a different number of results, each with its own offset; the cursor must encode hundreds of per-shard offsets. Pragmatic solution: denormalize a separate listing table sharded by `bucket_id`; listing performance is intentionally deprioritized in commercial object storage (S3 included).

## 8. Versioning, Multipart Upload, Garbage Collection

**Versioning** — adds an `object_version` column; new uploads insert a new row with a fresh `object_id` and `TIMEUUID` rather than overwriting; current version is the row with the largest `TIMEUUID` for a given `(bucket_id, object_name)`.

**Delete marker** — deleting a versioned object inserts a tombstone row that becomes the current version; subsequent `GET` returns `404 Object Not Found` while older versions remain recoverable.

**Multipart upload flow** — client requests `uploadID` → splits a large file (e.g., 1.6 GB into 8 × 200 MB parts) → uploads each part with the `uploadID`, receiving an `ETag` (MD5 checksum) per part → sends complete request with all part numbers + `ETags` → server reassembles. Parts retry independently and upload in parallel; large objects over flaky networks fail without this.

**Garbage collection sources** — lazy deletes (marked but not removed), orphans (abandoned multipart parts, half-uploaded data), corrupted data (failed checksums).

**Compaction** — GC copies live objects from old read-only files into new files (skipping rows with delete flag set), then transactionally updates `file_name` and `start_offset` in `object_mapping`; batches across many read-only files to avoid creating new small files.

**Replica-aware GC** — for replication, free space on all replicas; for (8+4) erasure coding, free space on all 12 chunks.

## Sources

- [Vol 2 Ch 9: S3-like Object Storage](software/system-design-interview/books/system-design-interview-vol2/ch09_s3_like_object_storage.md)
