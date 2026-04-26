# News Feed (Instagram-style)

> Both books cover this. Xu's Ch 11 is the canonical illustration of **fanout**; Liu's Ch 6.04 frames Instagram around the same hybrid fan-out + fan-in pattern, with extra emphasis on celebrities as a long-tail distribution. The two designs converge.

## Table of Contents

- [1. Requirements](#1-requirements)
- [2. The Central Question — Fanout](#2-the-central-question--fanout)
- [3. Strategy Comparison](#3-strategy-comparison)
- [4. The Hybrid](#4-the-hybrid)
- [5. Architecture](#5-architecture)
- [6. The Multi-Layer Cache](#6-the-multi-layer-cache)
- [7. Replication and Geo-Distribution](#7-replication-and-geo-distribution)
- [8. The "Do Nothing" Move](#8-the-do-nothing-move)
- [Sources](#sources)

## 1. Requirements

- Users post content (photo, text, video).
- Followers see new posts in their feed.
- Read latency: low (feed should load instantly on app open).
- Some users have millions of followers (celebrities); some users have a handful.

## 2. The Central Question — Fanout

When a user posts, how do followers' feeds get the new post?

- **Fanout on write (push)** — at post time, write the new post into every follower's feed cache.
- **Fanout on read (pull)** — at feed-read time, query the followed users' recent posts and merge.

## 3. Strategy Comparison

| | Fanout on write (push) | Fanout on read (pull) |
|---|---|---|
| When feed is built | Pre-computed at write time | On-demand at read time |
| Read latency | Fast — feed already cached | Slow — must aggregate at read time |
| Inactive users | Wastes compute pre-building feeds they won't read | Efficient — no work until they log in |
| Hot-key problem | Yes — celebrities cause expensive fanouts | No — data isn't pushed |

Pure push falls over for celebrities (one post fans out to millions of follower caches). Pure pull falls over for active users on a normal-sized network (every feed open queries N friends' posts).

## 4. The Hybrid

Both books land on the same answer:

- **Push** for the majority — non-celebrity users with reasonable follower counts. Their followers' feeds are pre-computed at write time; reads are fast.
- **Pull** for celebrities — millions-of-followers users. Their posts are *not* fanned out at write; instead, every reader's feed read includes a pull from the followed celebrities' recent-posts list.

Celebrity threshold is a tunable parameter (e.g., 10,000 followers). [Consistent hashing](fundamentals/sharding-and-consistent-hashing.md) on user IDs balances the fanout service load.

## 5. Architecture

```
Post API
   ↓
Fanout Service (looks up follower IDs from social graph DB)
   ↓
   ├─ Non-celebrity post: fanout-on-write to N follower feed caches
   └─ Celebrity post: store post; do not fanout

Feed Read API
   ↓
Feed Builder
   ├─ Pulls non-celebrity posts from user's pre-built feed cache
   ├─ Pulls celebrity posts from followed celebrities' recent-posts list
   └─ Merges, ranks, returns to client
```

The fanout service applies user settings (mutes, audience filters) and writes `<post_id, user_id>` rows into the feed cache.

## 6. The Multi-Layer Cache

Xu's News Feed deep dive uses five caches tuned per access pattern. See [Caching](fundamentals/caching.md):

| Cache | Holds |
|---|---|
| News feed cache | Ordered list of post IDs per user |
| Content cache | Full post content by post ID |
| Social graph cache | Friend / follower lists |
| Action cache | Like, comment, share counts |
| Counter cache | Aggregated view counts |

Media is served from a [CDN](fundamentals/cdn.md). The feed render hydrates from the caches and CDN in parallel.

## 7. Replication and Geo-Distribution

Liu's Ch 6.04 emphasizes geo-distribution: feed storage is replicated cross-region for both latency (read locally) and durability. Async cross-region replication is the standard pick — eventual consistency is acceptable for a feed.

## 8. The "Do Nothing" Move

Liu calls out a senior-level pattern: when something *can* go wrong but rarely does and the user impact is mild, do nothing. Instagram's example is **duplicate posts on celebrity promotion** — under a race, a celebrity's post might briefly appear twice in some feeds. The user notices for a second; the cost of preventing it (distributed locks across millions of followers) is enormous. Do nothing; let it self-correct.

This is the same logic as the rate limiter's 1% inaccuracy tolerance — naming it as a deliberate design choice signals seniority.

## Sources

- [Xu Ch 11: Design a News Feed System](software/system-design-interview/books/system-design-interview-insiders-guide/ch11_design_a_news_feed_system.md)
- [Liu Ch 6.04: Instagram](software/system-design-interview/books/system-design-interview-fundamentals/ch06_04_instagram.md)
