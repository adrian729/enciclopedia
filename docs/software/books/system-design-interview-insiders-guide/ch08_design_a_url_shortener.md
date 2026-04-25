# Ch 8: Design a URL Shortener

## Table of Contents

- [1. Problem and Use Cases](#1-problem-and-use-cases)
- [2. Back-of-the-Envelope Estimation](#2-back-of-the-envelope-estimation)
- [3. API Endpoints](#3-api-endpoints)
- [4. URL Redirecting](#4-url-redirecting)
- [5. 301 vs 302 Redirect](#5-301-vs-302-redirect)
- [6. Data Model](#6-data-model)
- [7. Hash Value Length](#7-hash-value-length)
- [8. Hash + Collision Resolution](#8-hash--collision-resolution)
- [9. Base 62 Conversion](#9-base-62-conversion)
- [10. Approach Comparison](#10-approach-comparison)
- [11. URL Shortening Flow](#11-url-shortening-flow)
- [12. URL Redirecting Flow](#12-url-redirecting-flow)
- [13. Additional Considerations](#13-additional-considerations)

## 1. Problem and Use Cases

- **Goal** — design a service like tinyurl that turns a long URL into a much shorter alias which redirects back to the original
- **Core use cases** — URL shortening (long → short), URL redirecting (short → long), plus high availability, scalability, and fault tolerance
- **Constraints** — shortened URL as short as possible; alphabet `[0-9, a-z, A-Z]`; assume short URLs cannot be deleted or updated

## 2. Back-of-the-Envelope Estimation

- **Write rate** — 100 million URLs/day → ~1,160 writes/second
- **Read rate** — 10:1 read-to-write ratio → ~11,600 reads/second
- **Records over 10 years** — 100M × 365 × 10 = 365 billion records
- **Storage** — average URL ~100 bytes → 365 billion × 100 bytes = 365 TB over 10 years

## 3. API Endpoints

- **Shorten** — `POST api/v1/data/shorten` with `{longUrl: longURLString}` returns the shortURL
- **Redirect** — `GET api/v1/shortUrl` returns the longURL for HTTP redirection
- **Style** — REST endpoints handle the two-way mapping between long and short URLs

## 4. URL Redirecting

- **Server behavior** — receive a tinyurl request, look up the long URL, and respond with an HTTP 301 redirect
- **Naive storage** — a hash table mapping `<shortURL, longURL>` works conceptually: `longURL = hashTable.get(shortURL)`, then redirect

## 5. 301 vs 302 Redirect

| Redirect | Meaning | Browser behavior | Best when |
|---|---|---|---|
| **301** | Permanently moved | Caches the response; subsequent requests skip the shortener and go straight to the long URL | Reducing server load |
| **302** | Temporarily moved | Subsequent requests still hit the shortener first, then redirect | Tracking analytics like click rate and source |

## 6. Data Model

- **Why not a hash table** — fine as a starting point but infeasible in production: memory is limited and expensive
- **Relational DB** — store `<shortURL, longURL>` mappings; a simple table has three columns: `id`, `shortURL`, `longURL`
- **Hash function requirements** — every longURL maps to one hashValue, and every hashValue maps back to one longURL

## 7. Hash Value Length

- **Alphabet** — `[0-9, a-z, A-Z]` = 10 + 26 + 26 = 62 characters
- **Length calculation** — find smallest n such that `62^n ≥ 365 billion`. At n = 7, `62^7 ≈ 3.5 trillion`, well above 365 billion
- **Result** — hashValue length is 7

## 8. Hash + Collision Resolution

- **Idea** — apply a known hash (CRC32, MD5, SHA-1) and take the first 7 characters
- **Problem** — even CRC32 produces more than 7 characters; truncating to 7 causes collisions
- **Resolution** — recursively append a predefined string until no collision is found in the database
- **Cost** — each request requires DB lookups to test for collision; a **bloom filter** (space-efficient probabilistic set membership test) can speed up the existence check

## 9. Base 62 Conversion

- **Idea** — convert a unique numeric ID into its base 62 representation, since there are 62 valid output characters
- **Mapping** — `0–9` → `0–9`, `10` → `a`, ..., `35` → `z`, `36` → `A`, ..., `61` → `Z`
- **Example** — `11157₁₀ = 2 × 62² + 55 × 62¹ + 59 × 62⁰ = [2, 55, 59] → [2, T, X]`, giving short URL `https://tinyurl.com/2TX`
- **Coordination need** — requires a distributed unique ID generator (see Ch 7) to supply globally unique numeric IDs

## 10. Approach Comparison

| | Hash + collision resolution | Base 62 conversion |
|---|---|---|
| Fixed length | Yes (7 chars) | No — length grows with ID |
| Needs unique ID generator | No | Yes |
| Generation cost | DB lookups to detect collisions (mitigated by bloom filter) | Single base 62 conversion, no collision check |

## 11. URL Shortening Flow

- **Approach chosen** — base 62 conversion for simplicity and predictable behavior
- **Step 1** — `longURL` is the input
- **Step 2** — check the database for an existing entry; if present, fetch and return the existing shortURL (idempotent)
- **Step 3** — if new, the unique ID generator (Ch 7) produces a globally unique primary key
- **Step 4** — convert the ID to a shortURL via base 62 conversion
- **Step 5** — insert a new row with `id`, `shortURL`, and `longURL`
- **Concrete example** — input `https://en.wikipedia.org/wiki/Systems_design`, ID generator returns `2009215674938`, base 62 conversion yields shortURL `zn9edcu`

## 12. URL Redirecting Flow

- **Caching** — because reads dominate writes, `<shortURL, longURL>` mappings are cached to improve performance
- **Step 1** — user clicks a short URL like `https://tinyurl.com/zn9edcu`
- **Step 2** — load balancer forwards the request to a web server
- **Step 3** — if the shortURL is in cache, return the longURL directly
- **Step 4** — on cache miss, fetch from the database; if absent, the shortURL is likely invalid
- **Step 5** — return the longURL to the user

## 13. Additional Considerations

- **Rate limiter** — protect against malicious clients flooding shorten requests by filtering on IP or other rules (see Ch 4)
- **Web server scaling** — the web tier is stateless, so adding/removing servers is straightforward
- **Database scaling** — apply replication and sharding as standard horizontal techniques
- **Analytics** — integrate to capture click counts, timing, and click sources for business insight
- **Availability, consistency, reliability** — core concerns for any large system, covered in detail in Ch 1
