# Ch 5.15: Data Transfer (Compression and Filtering)

## Table of Contents

- [1. When to Reach for Compression](#1-when-to-reach-for-compression)
- [2. Lossless vs Lossy](#2-lossless-vs-lossy)
- [3. Compression Efficiency](#3-compression-efficiency)
- [4. Quality of File](#4-quality-of-file)
- [5. Computing Time](#5-computing-time)
- [6. Device Compatibility](#6-device-compatibility)
- [7. Compressed File Usage](#7-compressed-file-usage)
- [8. Pass Only Needed Data](#8-pass-only-needed-data)

## 1. When to Reach for Compression

- **Bandwidth bottleneck** — if too much data is passing through the wire, consider compression; the goal in an interview is to articulate what you're trying to achieve and the considerations/implications, not to recite codec internals
- **Compression is niche** — different algorithms fit different file types with different efficiency; interviewers rarely dig deep unless you have domain experience

> **Warning** — many people confuse compression, encoding, transcoding, and codec.

| Term | Definition |
|---|---|
| **Encoding** | Compressing raw data into an encoding format (e.g., RAW image → JPEG) |
| **Transcoding** | Converting one encoded format into another (e.g., JPEG → different aspect ratios) |
| **Compression** | Reducing the size of a piece of information; can be achieved through encoding and transcoding |
| **Codec** | The actual algorithm used to compress and uncompress data (e.g., H264 for videos) |

## 2. Lossless vs Lossy

- **Lossless compression** — looks for file patterns to produce another representation requiring less memory; the original file is always recoverable
- **Lossy compression** — the original file can never be recovered
- **They co-exist** — e.g., an image can be permanently lossy-compressed into JPEG for use by other software/users, then further lossless-encoded for efficient database storage (software can't use it directly without decompression)

| Aspect | Lossless | Lossy |
|---|---|---|
| Original recoverable? | Yes | No |
| Typical image ratio | ~2 | Heavily depends on encoding (e.g., JPEG ~20) |
| Example algorithm | Run-Length Encoding (RLE) | Chroma subsampling |

- **Run-Length Encoding (RLE)** — lossless; stores runs instead of individual characters. `AAAABBBBBBBBBBBBBBBAAA` (22 chars) becomes `4A15B3A`; always rebuildable. Efficiency depends on pattern — `ABABAB` becomes `1A1B1A1B1A1B`, potentially worse. Used in images like JPEG
- **Chroma Subsampling** — lossy; models image tiles by combining luma and chroma, preserves luma while compressing chroma. Adjacent chroma pairs share the same color after compression, so the original pair cannot be recreated from a single color

## 3. Compression Efficiency

- **Compression Ratio = Uncompressed Size / Compressed Size** — higher is better. A 10 MB file compressed to 1 MB = ratio of 10
- **Typical ratios** — lossless image compression ~2; lossy heavily depends on encoding. An iOS HEIF photo (~2 MB) encoded to JPEG (~100 KB) for Instagram gives a ratio of ~20

## 4. Quality of File

- **Quality is context-dependent** — for images, videos, and audio, it is end-user perception of quality; lossy compression trades quality for size
- **JPEG strengths/weaknesses** — efficient lossy compression like JPEG has minimal impact on end-user perception for natural photographic images, but isn't as good for synthetic images like web graphics (use PNG and vector graphics instead)
- **Monitor end-user experience** — you don't need to be a compression-algorithm expert, but you should discuss how you'd verify compression doesn't worsen the user experience

## 5. Computing Time

- **Compression costs compute** — especially for videos; encoding some videos may take as long as the video itself
- **More efficient = slower** — more thorough pattern discovery raises processing time
- **Client vs server trade-off** — processing cost influences whether compression runs on client or server; the backend challenge is whether there are enough machines to process all files since compression can be compute-heavy

## 6. Device Compatibility

- **Backend must encode multiple formats** — some mobile clients and applications only handle certain encodings; the mapping of device to encoding is niche but the system must support several

| Media | Encodings / Variants |
|---|---|
| **Video** | H264, VP9 codecs; resolutions 480p, 720p, 1080p |
| **Image** | JPEG; aspect ratios 1:1, 3:2, 4:3, 16:9; dimensions such as 1080×1080, 1280×720 |
| **Audio** | MP3, OGG; qualities like 160 KBPS, 320 KBPS |

## 7. Compressed File Usage

- **Dimension and aspect ratio** — proliferation of tablets, phones, and web clients means many screen sizes, aspect ratios, and resolutions; responsive browsers add demand for varied image and video dimensions
- **Quality encoding via ABR** — for clients with low bandwidth (e.g., Facebook's global audience), use **adaptive bit rate (ABR)** to dynamically adjust compression quality to fit available bandwidth

## 8. Pass Only Needed Data

- **Tactic for bandwidth bottlenecks** — only send what's actually needed rather than the full payload

### 8.1. Filtering

- **Server-side field selection** — for e-commerce products with heavy metadata, let the client specify the fields it wants and return only those
- **Trade-off** — better bandwidth at the expense of client complexity to specify the filtering scheme

### 8.2. Pass Chunk Delta with Rsync

- **Send only deltas** — instead of passing whole objects, pass incremental changes when the use case allows
- **Rsync approach** — each 2,048-byte chunk is hashed with a function like MD5 into 128 bits (16 bytes), drastically reducing compared data

**How rsync works:**

1. **Step 1** — compare the first chunk's checksum; if identical, move on
2. **Step 2** — detect that the new chunk is different
3. **Step 3** — calculate the next hash by moving one byte forward at head and tail (**rolling hash**); to compute chunk 2, remove 1 and add 2 without recalculating the overlapping blocks
4. **Transmit only new chunks** — when a new chunk is detected, only that chunk is passed; for matching blocks, move on

- **Overhead caveat** — passing checksums to compare has cost; if the files are completely different, it's better to copy the new bytes directly. Use rsync when files are similar
