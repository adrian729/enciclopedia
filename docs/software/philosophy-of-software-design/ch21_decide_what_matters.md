# Ch 21: Decide What Matters

## Table of Contents

- [1. The Core Idea](#1-the-core-idea)
- [2. How to Decide What Matters](#2-how-to-decide-what-matters)
- [3. Minimize What Matters](#3-minimize-what-matters)
- [4. How to Emphasize Things That Matter](#4-how-to-emphasize-things-that-matter)
- [5. Mistakes](#5-mistakes)
- [6. Thinking More Broadly](#6-thinking-more-broadly)

## 1. The Core Idea

- **Separating what matters from what doesn't** — one of the most important elements of good software design. Structure the system around the things that matter; minimize the impact of everything else
- **Things that matter** — should be emphasized and made more obvious
- **Things that don't matter** — should be hidden as much as possible
- **This principle unifies many earlier concepts** — module interfaces reflect what matters to users (hiding what doesn't); variable names convey the most important aspects; performance-critical paths are designed around what matters most

## 2. How to Decide What Matters

- **Look for leverage** — situations where one piece of knowledge solves many problems or where one design decision unlocks multiple benefits. A general-purpose interface for text editing (insert/delete with positions) has more leverage than specialized methods (e.g., backspace), because it covers more use cases with less surface area
- **Invariants provide leverage** — once you know an invariant for a variable or structure, you can predict how it will behave in many different situations without checking special cases
- **When in doubt, hypothesize** — sometimes it's not obvious what matters most, especially for less experienced developers. Make a hypothesis ("I think X is what matters here"), build under that assumption, and evaluate. If the hypothesis was wrong, the specific failure will teach you more than abstract reasoning
- **Use "design it twice"** — comparing alternatives forces you to articulate what's important about each, revealing what truly matters

## 3. Minimize What Matters

- **Fewer things that matter = simpler system** — minimize the number of parameters needed to construct an object, provide sensible defaults, hide information inside modules so it doesn't matter to callers
- **Mask exceptions at low levels** — if an exception can be handled internally, callers never need to know it exists
- **Compute configuration automatically** — if the system can determine a good value on its own, don't force users or admins to provide it

## 4. How to Emphasize Things That Matter

| Technique | How it works |
|-----------|-------------|
| **Prominence** | Put important things where they're likely to be seen — interface docs, parameter names, heavily-used methods |
| **Repetition** | Key ideas should appear over and over; if an idea keeps surfacing, it's probably central |
| **Centrality** | The things that matter most should be at the heart of the system, determining the structure around them. Device driver interfaces in an OS are a good example: hundreds or thousands of drivers all depend on this central abstraction |

- **The converse is also true** — if an idea appears everywhere or shapes the structure around it, that's a signal that it matters
- **Things that don't matter should be de-emphasized** — hidden as much as possible, rarely encountered, not influencing the overall structure

## 5. Mistakes

| Mistake | Effect | Example |
|---------|--------|---------|
| **Treating too many things as important** | Clutters the design with unimportant details, increases cognitive load | Java I/O forcing developers to be aware of buffered vs. unbuffered I/O; shallow classes with complex interfaces for minimal functionality |
| **Failing to recognize what's important** | Important information is hidden or unavailable, leading to unknown unknowns | Key design decisions buried in implementation rather than surfaced in interfaces; important functionality requiring users to discover it on their own |

## 6. Thinking More Broadly

- **Applies beyond software** — the skill of focusing on what's most important transfers to technical writing (identify key concepts up front, structure around them) and to life in general (identify what matters most to you and spend your energy on those things)
- **"Good taste"** — the phrase describes the ability to distinguish what is important from what isn't. Having good taste is an important part of being a good software designer
