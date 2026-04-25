# Ch 14: Mathematics and Probability

## Table of Contents

- [1. Prime numbers](#1-prime-numbers)
- [2. Checking for primality](#2-checking-for-primality)
- [3. Sieve of Eratosthenes](#3-sieve-of-eratosthenes)
- [4. Probability basics](#4-probability-basics)
- [5. Independence and mutual exclusivity](#5-independence-and-mutual-exclusivity)
- [6. Things to watch out for](#6-things-to-watch-out-for)

Most interview "brain teaser" math problems are actually rooted in mathematics or computer science rules; knowing those rules lets you solve or validate the answer methodically instead of guessing.

## 1. Prime numbers

- **Prime factorization** — every positive integer decomposes into a product of primes, e.g. `84 = 2² * 3¹ * 5⁰ * 7¹ * 11⁰ * 13⁰ * 17⁰ * …`. Many exponents are zero.
- **Divisibility rule** — for `x\y` (x divides y), every prime in x's factorization must appear in y's factorization with an equal-or-greater exponent. If `x = 2^j0 * 3^j1 * 5^j2 * …` and `y = 2^k0 * 3^k1 * 5^k2 * …`, then `x\y` iff `ji <= ki` for all i.
- **GCD** — `gcd(x, y) = 2^min(j0,k0) * 3^min(j1,k1) * 5^min(j2,k2) * …` (min of exponents).
- **LCM** — `lcm(x, y) = 2^max(j0,k0) * 3^max(j1,k1) * 5^max(j2,k2) * …` (max of exponents).
- **Identity** — `gcd * lcm = xy`, because `min(j, k) + max(j, k) = j + k`.

## 2. Checking for primality

- **Naive** — iterate `i` from 2 through `n-1`, return false if any `n % i == 0`. O(n) divisibility checks.
- **Improved** — iterate only up to `sqrt(n)`. For any divisor `a > sqrt(n)` there is a complementary divisor `b = n/a < sqrt(n)` that would already have been found; checking past the square root is redundant.
- **Further improvement** — you only actually need to check divisibility by *prime* numbers, which motivates generating a prime list via the Sieve of Eratosthenes.

## 3. Sieve of Eratosthenes

- **Idea** — all non-prime numbers are divisible by some prime number. Start with all numbers up to `max` marked prime; repeatedly pick the next non-crossed number and cross off all its multiples (by 2, 3, 5, 7, 11, …). What remains is the list of primes from 2 through `max`.
- **Cross-off start point** — when crossing off multiples of `prime`, start at `prime * prime`. Any smaller multiple `k * prime` with `k < prime` was already crossed off in a prior iteration (as a multiple of one of `k`'s prime factors).
- **Space optimization** — storing only odd numbers halves the array size.

## 4. Probability basics

Two events A and B can be visualized as overlapping circles in a Venn diagram; the overlap is the event `{A and B}`.

- **P(A and B)** — `P(A and B) = P(B given A) * P(A)`. Example: picking a number 1–10, odds it's *even and* `<= 5` equals `P(even | x<=5) * P(x<=5) = (2/5) * (1/2) = 1/5`.
- **P(A or B)** — `P(A or B) = P(A) + P(B) - P(A and B)`. You subtract the intersection because adding the two regions would double-count it. Example: `P(even or x<=5) = 1/2 + 1/2 - 1/5 = 4/5`.

## 5. Independence and mutual exclusivity

- **Independence** — A and B independent means one occurring tells you nothing about the other. Then `P(A and B) = P(A) * P(B)`, because `P(B given A) = P(B)`.
- **Mutual exclusivity** — if one event occurs the other cannot. Then `P(A and B) = 0`, so `P(A or B) = P(A) + P(B)`.
- **Not interchangeable** — the concepts are *entirely different*. Two events with non-zero probability can never be both independent and mutually exclusive: mutual exclusivity means A happening tells you B absolutely did not happen (strong dependence), which contradicts independence.
- **Zero-probability edge case** — if one or both events have probability zero, they are both independent *and* mutually exclusive (provable directly from the formulas).

## 6. Things to watch out for

1. **Float vs. double precision** — be careful with the difference in precision between floats and doubles.
2. **Don't assume integer types** — don't assume a value (e.g. the slope of a line) is an `int` unless you've been told so.
3. **Don't assume independence or mutual exclusivity** — unless specified, do not blindly multiply or add probabilities.
