# Content Delivery Network (CDN)

> A CDN caches static content at geographically distributed nodes. Both books cover it; Liu pushes back harder against trivializing it ("just use a CDN") and lists the deep-dive questions to expect.

## Table of Contents

- [1. What a CDN Is](#1-what-a-cdn-is)
- [2. Benefits](#2-benefits)
- [3. The Read-Through Pattern](#3-the-read-through-pattern)
- [4. Considerations](#4-considerations)
- [5. Cost vs In-House Storage](#5-cost-vs-in-house-storage)
- [Sources](#sources)

## 1. What a CDN Is

A geographically distributed cache for static assets — images, video segments, CSS, JavaScript. Edges sit close to users; the origin (in-house storage or object store) sits far away. Routing is via [anycast](fundamentals/networking-and-dns.md): multiple edges share an IP, and each internet router forwards to the nearest one.

## 2. Benefits

- **Latency** — proximity. Tens of milliseconds saved for users far from the origin.
- **Bandwidth** — traffic absorbed at the edge never hits the origin's pipe.
- **Availability** — multi-region redundancy by default; cross-CDN failover is a real option for global services.

## 3. The Read-Through Pattern

The standard read pattern is read-through: edge looks up the asset, on miss fetches from origin, caches it, returns to the client. The TTL determines how long the cached copy is served before the edge re-checks.

## 4. Considerations

Liu lists the deep-dive questions a senior candidate proactively raises:

- **What is worth caching?** Not every static asset deserves the cost.
- **What happens on a miss?** Latency to origin; thundering-herd risk if many edges miss the same asset simultaneously.
- **How are nodes updated?** Vendor-specific invalidation APIs (signals to purge a URL) or **URL versioning** like `image.png?v=2`. URL versioning sidesteps the invalidation problem entirely — old URLs stay cached, new versions get fresh URLs.
- **How is content prepopulated?** Netflix predicts regional demand and pushes encoded content to edges before viewing peaks. Without prepopulation, the first viewer in each region pays the cold-cache penalty.
- **TTL tuning.** Long TTL = high hit rate, slower invalidation. Short TTL = freshness, more origin traffic.
- **Fallback when the CDN is down.** Either fail to direct origin (capacity-bound) or serve a degraded experience.

## 5. Cost vs In-House Storage

Xu's YouTube design makes the cost trade-off explicit: serving every video through CDN costs ~$150,000/day at AWS CloudFront pricing for a YouTube-scale catalog. The optimization is to exploit the **long-tail viewing pattern** — popular videos go through CDN; unpopular videos serve from in-house storage where the marginal cost per view is much lower. The hot/cold split mirrors the [cold storage](fundamentals/observability-security-cold-storage.md) pattern.

## Sources

- [Liu Ch 5.20: CDN](software/system-design-interview/books/system-design-interview-fundamentals/ch05_20_cdn.md)
- [Xu Ch 1: Scale From Zero to Millions of Users](software/system-design-interview/books/system-design-interview-insiders-guide/ch01_scale_zero_to_millions.md) (CDN section)
- [Xu Ch 14: Design YouTube](software/system-design-interview/books/system-design-interview-insiders-guide/ch14_design_youtube.md) (CDN cost optimization)
