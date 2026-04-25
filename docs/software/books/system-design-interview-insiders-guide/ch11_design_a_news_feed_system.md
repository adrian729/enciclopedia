# Ch 11: Design a News Feed System

## Table of Contents

- [1. Requirements and Scope](#1-requirements-and-scope)
- [2. APIs](#2-apis)
- [3. Two Flows: Publishing and Building](#3-two-flows-publishing-and-building)
- [4. Feed Publishing Components](#4-feed-publishing-components)
- [5. Fanout: On Write vs On Read](#5-fanout-on-write-vs-on-read)
- [6. Hybrid Fanout Strategy](#6-hybrid-fanout-strategy)
- [7. Fanout Service Steps](#7-fanout-service-steps)
- [8. News Feed Retrieval](#8-news-feed-retrieval)
- [9. Cache Architecture](#9-cache-architecture)
- [10. Scalability Talking Points](#10-scalability-talking-points)

## 1. Requirements and Scope

- **News feed defined** — Facebook's term: "the constantly updating list of stories... status updates, photos, videos, links, app activity, and likes from people, pages, and groups that you follow"; the same shape applies to Twitter timeline, Instagram feed, etc.
- **Platform** — both mobile and web
- **Core features** — publish a post; view friends' posts on the feed page
- **Ordering** — reverse chronological (no scoring) to keep design simple
- **Friend cap** — 5,000 per user
- **Traffic** — 10M DAU
- **Media** — feed contains text plus images and videos

## 2. APIs

- **Feed publishing API** — `POST /v1/me/feed` with `content` (post text) and `auth_token` (authentication)
- **News feed retrieval API** — `GET /v1/me/feed` with `auth_token`

## 3. Two Flows: Publishing and Building

- **Feed publishing** — when a user posts, data is written to cache and database, and the post is propagated to friends' news feeds
- **News feed building** — for retrieval, aggregate friends' posts in reverse chronological order

## 4. Feed Publishing Components

- **User** — browser or mobile app submitting `/v1/me/feed?content=Hello&auth_token=...`
- **Load balancer** — distributes traffic to web servers
- **Web servers** — route to internal services and enforce **authentication** (only valid `auth_token`) and **rate limiting** (cap posts per period to block spam/abuse)
- **Post service** — persists the post in DB and cache
- **Fanout service** — pushes new content to friends' news feeds; news feed data is stored in cache for fast retrieval
- **Notification service** — informs friends that new content is available, including push notifications

## 5. Fanout: On Write vs On Read

- **Fanout** — the process of delivering a post to all of a user's friends; two competing models

| | Fanout on write (push) | Fanout on read (pull) |
|---|---|---|
| When feed is built | Pre-computed at write time | On-demand at read time |
| Read latency | Fast — feed already in cache | Slow — must aggregate at request time |
| Inactive users | Wastes compute pre-building feeds they never read | Efficient — no work until they log in |
| Hotkey problem | Yes — users with many friends/followers cause expensive fanouts | No — data isn't pushed |

## 6. Hybrid Fanout Strategy

- **Hybrid approach** — get the benefits of both models while avoiding their pitfalls
- **Push for the majority** — use fanout on write so most users get fast reads from a pre-computed cache
- **Pull for celebrities** — users with massive follower counts let followers pull on-demand, avoiding a write-side overload (the **hotkey problem**)
- **Consistent hashing** — used to mitigate the hotkey problem by distributing requests/data more evenly

## 7. Fanout Service Steps

1. **Fetch friend IDs** from a **graph database**, which is well-suited for friend relationships and friend recommendations
2. **Get friends info from user cache** and filter by user settings — e.g., muted friends are excluded, and posts shared with specific subsets are hidden from the rest
3. **Send friends list and new post ID to the message queue**
4. **Fanout workers** pull from the queue and write to the **news feed cache**, modeled as a `<post_id, user_id>` mapping table; only IDs are stored to keep memory small, with a configurable size limit since users rarely scroll thousands of posts (cache miss rate stays low)
5. **Store `<post_id, user_id>`** in the news feed cache

## 8. News Feed Retrieval

- **Media in CDN** — images and videos are served from a CDN for fast delivery
- **Retrieval flow**:
  1. User sends `/v1/me/feed`
  2. Load balancer routes to web servers
  3. Web servers call the news feed service
  4. News feed service fetches a list of post IDs from the news feed cache
  5. News feed service hydrates the feed by fetching full user and post objects from **user cache** and **post cache** (a feed needs username, profile picture, post content, post image, etc., not just IDs)
  6. Fully hydrated feed returned as JSON for client rendering

## 9. Cache Architecture

The cache tier is split into five layers, each tuned for its access pattern:

- **News Feed** — IDs of news feed entries
- **Content** — post data; popular content kept in a hot cache
- **Social Graph** — user relationship data
- **Action** — likes, replies, and other per-user post actions
- **Counters** — like, reply, follower, following counts

## 10. Scalability Talking Points

- **Scaling the database** — vertical vs horizontal scaling, SQL vs NoSQL, master-slave replication, read replicas, consistency models, database sharding
- **Keep web tier stateless**
- **Cache data as much as you can**
- **Support multiple data centers**
- **Loose-couple components with message queues**
- **Monitor key metrics** — e.g., QPS during peak hours and latency while users refresh their news feed
