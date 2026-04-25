# Ch 12: Bit Manipulation

## Table of Contents

- [1. Why bit manipulation matters](#1-why-bit-manipulation-matters)
- [2. Bit manipulation by hand](#2-bit-manipulation-by-hand)
- [3. Operator tricks](#3-operator-tricks)
- [4. Bit facts and tricks](#4-bit-facts-and-tricks)
- [5. Common bit tasks](#5-common-bit-tasks)

## 1. Why bit manipulation matters

- **Used in a variety of problems** — sometimes the question explicitly calls for bit manipulation; sometimes it's a useful technique to optimize code.
- **Be comfortable doing it by hand and with code** — interviewers expect both.
- **Easy to make little mistakes** — test your code thoroughly after writing it, or even while writing it.

## 2. Bit manipulation by hand

- **If you have the oh-so-common fear of bit manipulation**, practice by working operations through as base-10 numbers first, then apply the same process to binary.
- **Assume four-bit numbers** for practice; use the Windows calculator in **View > Programmer** mode to experiment with AND, XOR, and shifting.
- `^` denotes **XOR**; `~` denotes **NOT (negation)**.

## 3. Operator tricks

Shortcuts for recognizing common patterns:

| Expression | Equivalent / Result |
|------------|---------------------|
| `0110 + 0110` | Same as `0110 * 2`, same as shifting `0110` left by 1 |
| `0011 * 0100` | Multiplying `0011` by 4; `2ⁿ` multiplication just shifts left by n |
| `a ^ (~a)` | Always a sequence of **1s** — XORing a bit with its own negated value always gives 1 |
| `x & (~0 << n)` | **Clears the n rightmost bits of x** — `~0` is a sequence of 1s; shifted left by n gives 1s followed by n zeros, and ANDing with x clears the low n bits |

## 4. Bit facts and tricks

Understand *why* each of these is true rather than memorizing. They hold bit-by-bit — what happens on one bit never impacts the other bits, so if a statement is true for a single bit, it's true for a sequence of bits.

| XOR | AND | OR |
|-----|-----|----|
| `x ^ 0s = x` | `x & 0s = 0` | `x \| 0s = x` |
| `x ^ 1s = ~x` | `x & 1s = x` | `x \| 1s = 1s` |
| `x ^ x = 0` | `x & x = x` | `x \| x = x` |

## 5. Common bit tasks

These operations are very important to know, but **do not simply memorize** — memorizing leads to mistakes impossible to recover from. Understand *how* to implement them so you can derive these and related bit methods.

- **Get Bit** — shift `1` over by `i` bits to create a mask like `00010000`, AND with `num`; if result is nonzero, bit `i` is 1.
  - `return ((num & (1 << i)) != 0);`
- **Set Bit** — shift `1` over by `i` bits, OR with `num`; only the bit at position `i` changes because the other mask bits are zero.
  - `return num | (1 << i);`
- **Clear Bit** — create the reverse of a `setBit` mask (like `11101111`) by negating `(1 << i)`, then AND with `num`.
  - `int mask = ~(1 << i); return num & mask;`
- **Clear bits MSB through i (inclusive)** — `int mask = (1 << i) - 1; return num & mask;`
- **Clear bits i through 0 (inclusive)** — `int mask = ~((1 << (i+1)) - 1); return num & mask;`
- **Update Bit** — merges setBit and clearBit. Clear bit `i` with a mask like `11101111`, shift the intended value `v` left by `i`, then OR.
  - `int mask = ~(1 << i); return (num & mask) | (v << i);`
