# Ch 14: Design YouTube

## Table of Contents

- [1. Requirements and Scope](#1-requirements-and-scope)
- [2. Back-of-the-Envelope Estimation](#2-back-of-the-envelope-estimation)
- [3. High-Level Architecture](#3-high-level-architecture)
- [4. Video Uploading Flow](#4-video-uploading-flow)
- [5. Video Streaming Flow](#5-video-streaming-flow)
- [6. Video Transcoding](#6-video-transcoding)
- [7. DAG Programming Model](#7-dag-programming-model)
- [8. Transcoding Architecture](#8-transcoding-architecture)
- [9. Speed Optimizations](#9-speed-optimizations)
- [10. Safety Optimizations](#10-safety-optimizations)
- [11. Cost-Saving Optimizations](#11-cost-saving-optimizations)
- [12. Error Handling](#12-error-handling)
- [13. Wrap-Up Topics](#13-wrap-up-topics)

## 1. Requirements and Scope

- **Target features** — fast video upload, smooth streaming, ability to change quality, low infrastructure cost, high availability/scalability/reliability, mobile + web + smart TV support
- **Scale agreed in interview** — 5M DAU, encryption required, max video size 1GB, leverage existing cloud infrastructure (Amazon, Google, Microsoft)
- **Why leveraging cloud is okay** — building blob storage and CDN from scratch is enormously expensive; even Netflix uses AWS and Facebook uses Akamai's CDN. Choosing the right technology beats explaining how to rebuild it

## 2. Back-of-the-Envelope Estimation

- **Storage** — 5M users × 10% upload × 300 MB avg = 150 TB/day
- **CDN cost** — using AWS CloudFront at $0.02/GB (US): 5M × 5 videos × 0.3 GB × $0.02 = **$150,000/day**, motivating the cost-saving section
- **Implication** — CDN egress is the dominant cost; reducing it is a major design goal

## 3. High-Level Architecture

- **Three components**
  - **Client** — browser, mobile app, smart TV
  - **CDN** — stores and streams videos to viewers
  - **API servers** — handle everything except video streaming (feed, upload URL generation, metadata DB/cache, signup, etc.)

## 4. Video Uploading Flow

- **Components added for upload** — load balancer, API servers, **Metadata DB** (sharded + replicated), **metadata cache**, **Original storage** (BLOB storage for raw videos), **Transcoding servers**, **Transcoded storage** (BLOB), CDN, **Completion queue**, **Completion handler** (workers consuming the queue)
- **BLOB definition** — "A Binary Large Object (BLOB) is a collection of binary data stored as a single entity in a database management system"
- **Two parallel processes**
  - **Flow a (upload video)** — video → original storage → transcoding servers fetch and transcode → in parallel: (3a) transcoded video lands in transcoded storage and is distributed to CDN; (3b) completion event goes to the completion queue; completion-handler workers consume events and update metadata DB and cache → API servers tell the client the video is ready
  - **Flow b (update metadata)** — client also sends file name, size, format, etc. to API servers, which update the metadata cache and DB

## 5. Video Streaming Flow

- **Streaming vs downloading** — streaming continuously feeds bytes so playback can start immediately; downloading copies the entire file before playback
- **Streaming protocols** — MPEG-DASH (Dynamic Adaptive Streaming over HTTP), Apple HLS (HTTP Live Streaming), Microsoft Smooth Streaming, Adobe HTTP Dynamic Streaming (HDS); each supports different encodings and players
- **Edge delivery** — videos are streamed from the CDN edge server closest to the viewer, minimizing latency

## 6. Video Transcoding

- **Why transcode** — raw video is huge (HD at 60fps ≈ hundreds of GB/hour); devices/browsers support different formats; deliver high resolution to fast networks and lower resolution to slow ones; switch quality automatically as network changes
- **Encoding format anatomy**
  - **Container** — like a basket holding video, audio, and metadata; identified by extension (.avi, .mov, .mp4)
  - **Codecs** — compression/decompression algorithms reducing size while preserving quality. Common codecs: H.264, VP9, HEVC

## 7. DAG Programming Model

- **Why DAG** — different creators need different processing (watermarks, custom thumbnails, varying resolutions); a **directed acyclic graph (DAG)** model defines tasks as stages that run sequentially or in parallel, mirroring Facebook's streaming video engine (SVE)
- **Typical DAG tasks**
  - **Inspection** — verify quality, detect malformed video
  - **Video encodings** — produce versions for different resolutions, codecs, bitrates
  - **Thumbnail** — uploaded by user or auto-generated
  - **Watermark** — image overlay carrying identifying info

## 8. Transcoding Architecture

- **Six components** — preprocessor, DAG scheduler, resource manager, task workers, temporary storage, encoded video output
- **Preprocessor responsibilities**
  - **Video splitting** — split the stream into Group of Pictures (GOP) chunks. A **GOP** is a chunk of frames in a specific order forming an independently playable unit (a few seconds long)
  - **GOP for old clients** — handle splitting server-side when old mobile/browser clients can't
  - **DAG generation** — build the DAG from configuration files written by client programmers
  - **Cache data** — store GOPs and metadata in temporary storage so failed encodings can retry from persisted data
- **DAG scheduler** — splits the DAG into stages of tasks and pushes them onto the resource manager's task queue (e.g., stage 1: split into video/audio/metadata; stage 2: video encoding + thumbnail + audio encoding)
- **Resource manager** — manages efficient allocation via three queues plus a scheduler:

| Queue | Purpose |
|---|---|
| **Task queue** | Priority queue of tasks waiting to run |
| **Worker queue** | Priority queue of worker utilization info |
| **Running queue** | Currently running task/worker bindings |

- **Resource manager loop** — task scheduler picks highest-priority task → picks optimal worker → instructs worker to run → records binding in running queue → removes once done
- **Task workers** — execute the DAG-defined tasks (different workers may run different tasks)
- **Temporary storage** — tiered: in-memory cache for small frequently-accessed metadata; BLOB storage for video/audio data; freed once processing completes
- **Encoded video** — final output, e.g., `funny_720p.mp4`

## 9. Speed Optimizations

- **Parallelize uploads via GOP chunking** — splitting upload into GOP-aligned chunks enables fast resumable uploads on failure; client-side splitting improves upload speed
- **Geo-distributed upload centers** — set up upload centers globally (e.g., North America, Asia) using CDN edges; reduces upload latency vs a single origin
- **Parallelism via message queues** — without a queue, encoding waits for download to complete; introducing a message queue between modules decouples them so encoding runs in parallel with whatever upstream events are available

## 10. Safety Optimizations

- **Pre-signed upload URLs** — client requests a pre-signed URL from API servers; the URL grants permission to upload to a specific object in storage. Term comes from Amazon S3; Microsoft Azure calls it "Shared Access Signature"
- **Copyright protection** — three options
  - **Digital rights management (DRM)** — Apple FairPlay, Google Widevine, Microsoft PlayReady
  - **AES encryption** — encrypt the video with an authorization policy; decrypted only on authorized playback
  - **Visual watermarking** — image overlay with logo/company name

## 11. Cost-Saving Optimizations

- **Long-tail observation** — YouTube viewing follows a long-tail distribution: a few popular videos dominate views, most others have very few viewers
- **Optimizations exploiting the long tail**
  1. **CDN only for popular videos** — serve unpopular videos from in-house high-capacity storage servers
  2. **Encode on-demand** — for short or unpopular videos, skip pre-encoding many versions
  3. **Regional distribution** — only push videos to CDN regions where they're popular
  4. **Build your own CDN + ISP partnerships** — like Netflix; partnering with ISPs (Comcast, AT&T, Verizon) places content close to users and reduces bandwidth charges; only sensible for very large streamers

## 12. Error Handling

- **Recoverable errors** — retry a few times; if still failing and judged non-recoverable, return an error code
- **Non-recoverable errors** — e.g., malformed video; stop the running tasks and return an error code
- **Per-component playbook**
  - **Upload error** — retry
  - **Split video error** — older clients fall back to server-side splitting
  - **Transcoding error** — retry
  - **Preprocessor error** — regenerate the DAG
  - **DAG scheduler error** — reschedule the task
  - **Resource manager queue down** — use a replica
  - **Task worker down** — retry on a new worker
  - **API server down** — stateless, redirect to another
  - **Metadata cache down** — replicated; bring up a new node
  - **Metadata DB master down** — promote a slave
  - **Metadata DB slave down** — read from another slave; replace failed node

## 13. Wrap-Up Topics

- **Scale the API tier** — stateless, horizontally scalable
- **Scale the database** — replication and sharding
- **Live streaming** — shares uploading/encoding/streaming with VOD but has higher latency requirements (different protocol), lower parallelism (small real-time chunks), and stricter error handling (slow recovery is unacceptable)
- **Video takedowns** — videos violating copyright, pornography rules, or other laws must be removable; some caught at upload, some by user flagging
