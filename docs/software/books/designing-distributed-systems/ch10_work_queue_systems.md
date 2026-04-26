# Ch 10: Work Queue Systems

## Table of Contents

- [1. What a Work Queue Is](#1-what-a-work-queue-is)
- [2. Reusable Container Architecture](#2-reusable-container-architecture)
- [3. The Source Container Interface](#3-the-source-container-interface)
- [4. The Worker Container Interface](#4-the-worker-container-interface)
- [5. The Shared Work Queue Manager](#5-the-shared-work-queue-manager)
- [6. Dynamic Scaling of Workers](#6-dynamic-scaling-of-workers)
- [7. The Multi-Worker Pattern](#7-the-multi-worker-pattern)
- [8. Hands-On: Video Thumbnailer](#8-hands-on-video-thumbnailer)

## 1. What a Work Queue Is

- **Work queue** — the simplest form of batch processing: a batch of fully independent work items that can each be processed without interaction with the others.
- **Goal** — ensure each item is processed within a target time; scale workers up or down so the queue keeps pace with arrivals.
- **Why this pattern is illustrative** — most of the queue's machinery is independent of what the work actually does, so much of it can be packaged as reusable distributed-system infrastructure.

## 2. Reusable Container Architecture

- **Library containers** — generic, reusable containers that implement the work-queue plumbing; users supply only the application-specific containers.
- **Two interface points** — the *source container* surfaces work items to be processed, and the *worker container* knows how to process one item.
- **Source container as ambassador** — an instance of the ambassador pattern: the generic queue manager is the application container, and the source container ambassadors out to the real-world queue (cloud storage listing, network share, Kafka or Redis topic, etc.).
- **Generic source implementations exist** — although the ambassador is application-specific in role, common backends (cloud blob listings, file shares, pub/sub queues) ship as off-the-shelf source containers that users just configure.

## 3. The Source Container Interface

- **HTTP REST API** — the easiest and de-facto interface between the queue manager and its source ambassador; runs on `localhost` inside the same container group.
- **Endpoints** — `GET /api/v1/items` returns an `ItemList` of all item names; `GET /api/v1/items/<item-name>` returns a single `Item` whose `data` field carries the per-item payload.
- **Always version your API** — `v1` in the path is cheap up front and very expensive to retrofit, so the book treats versioning as a default best practice even when no `v2` is foreseen.
- **No completion endpoint** — the source intentionally doesn't track which items are done; the manager owns completion bookkeeping so the source stays minimal.

## 4. The Worker Container Interface

- **One-shot, out-of-group worker** — unlike the source, the worker is started in its own container group via the orchestrator and receives exactly one invocation per item over its lifetime.
- **File-based API** — the worker reads its work from a file path supplied via the `WORK_ITEM_FILE` environment variable; in Kubernetes this is implemented by mounting a `ConfigMap` carrying the item's `data` field.
- **Why file-based, not HTTP** — only one call per worker is needed, and a remote HTTP endpoint would have to defend against malicious or accidental injection from other cluster users; a file scoped to the container avoids both concerns.
- **Generic worker example** — a container that downloads an input file from cloud storage, runs a user-supplied shell script over it, and uploads the result; only the script changes per use case, file plumbing is shared.

## 5. The Shared Work Queue Manager

- **Core algorithm** — repeatedly: list source items, list outstanding `Job` objects for this queue, diff to find unprocessed items, create a Kubernetes `Job` per missing item that runs the worker container.
- **Lean on the orchestrator** — Kubernetes `Job` reliably runs the worker to completion even across machine failure, so the manager doesn't need its own durable storage for in-flight work.
- **Job annotations as state** — each `Job` is annotated with the item it processes, letting the manager tell which items are in flight and which have succeeded or failed without a separate database.
- **Reference implementation** — a small Python loop using the Kubernetes client: build a `V1Job` for each missing item with `restart_policy: Never` and create it via `BatchV1Api.create_namespaced_job`, sleeping 10 seconds between sweeps.

## 6. Dynamic Scaling of Workers

- **Bursty default behavior** — processing every item the moment it arrives can spike resource use; if you don't have enough mixed workloads to even out the bursts, you over-provision to cover idle time.
- **Cap parallelism to flatten load** — limiting the number of concurrent `Job` objects bounds resources, at the cost of higher per-item latency under heavy load.
- **Steady-state must beat arrival rate** — if average processing time exceeds average arrival time, the backlog grows without bound and latency goes to infinity.
- **Interarrival time** — the average gap between new work items, computed as items per long window (e.g., 24 hours); compare against average per-item processing time divided by parallelism.
- **Three regimes** — arrival 1/min and processing 30s yields slack to absorb bursts; arrival 1/min and processing 1 min is balanced but cannot absorb sustained spikes; arrival 1/min and processing 2 min always loses ground.
- **Autoscaling rule of thumb** — increase parallelism so effective processing time stays below interarrival time; scale down only until effective processing time reaches roughly 90% of interarrival time, preserving a safety margin.

## 7. The Multi-Worker Pattern

- **Multi-worker pattern** — a specialization of the adapter pattern: a wrapper container exposes the single worker interface but delegates the actual work to a composed group of reusable worker containers.
- **Composable processing pipelines** — example: detect faces, tag identities, then blur faces — each stage is its own reusable container, so the next pipeline (e.g., detect cars, blur them) reuses the blurring container instead of rebuilding a bespoke worker.
- **Outcome** — increased code reuse and reduced effort for batch-oriented distributed system designers, while keeping the single-call worker contract intact.

## 8. Hands-On: Video Thumbnailer

- **Demo setup** — a Node.js source container lists `*.mp4` files on an NFS share via `MEDIA_PATH` and serves them through the source API; the worker uses the `jrottenberg/ffmpeg` image to run `ffmpeg -i ${INPUT_FILE} -frames:v 100 thumb.png`, emitting one PNG every 100 frames as the video's thumbnails.
