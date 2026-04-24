# Ch 1: Architecture, Performance, and Games

## Table of Contents

- [1. What Software Architecture Is](#1-what-software-architecture-is)
- [2. Decoupling](#2-decoupling)
- [3. The Cost of Architecture](#3-the-cost-of-architecture)
- [4. Performance vs. Flexibility](#4-performance-vs-flexibility)
- [5. Prototyping and Throwaway Code](#5-prototyping-and-throwaway-code)
- [6. Striking a Balance](#6-striking-a-balance)
- [7. Simplicity](#7-simplicity)
- [8. Parting Advice](#8-parting-advice)

## 1. What Software Architecture Is

- **Architecture is about organizing code, not writing it** — this book is about the code *between* graphics, AI, physics, and audio, not those systems themselves
- **A good design is one that makes change easy** — the measure of architecture is how easily it accommodates change. If no one is touching the code, its design is irrelevant
- **Good design feels anticipatory** — when you make a change, it's as if the entire program was crafted in anticipation of it: a few choice function calls slot in without rippling through the rest
- **Programming flow** — understand existing code → solve the problem → code the solution → clean up for the next reader. Loading code into your head is often the most time-consuming step

## 2. Decoupling

- **Coupling defined** — two pieces of code are coupled if you can't understand one without understanding the other. Decoupling lets you reason about either side independently
- **Why it matters** — architecture's key goal is to **minimize the amount of knowledge you need in-cranium before you can make progress**. Less to load into your head = faster change
- **Second definition** — decoupled code means a change to one piece doesn't force a change to another. Changes ripple less across the codebase

## 3. The Cost of Architecture

- **Good architecture is not free** — every feature must be integrated gracefully, and the design must be maintained across thousands of small changes ("like gardening — weed and prune")
- **Speculative flexibility is dangerous** — every abstraction or extension point bets that future-you will need it. When the bet is wrong, it's just more code to maintain
- **YAGNI** — "You aren't gonna need it": a mantra against the urge to speculate about future needs
- **Over-architected codebases** — interfaces, abstract base classes, virtual methods, plug-ins everywhere. Tracing real behavior takes forever, and the abstraction layers themselves fill your mental scratch disk. This is what turns people against design patterns

## 4. Performance vs. Flexibility

- **Architecture tends to slow code down** — virtual dispatch, interfaces, pointers, and messages all have runtime cost
- **Flexibility and performance are opposite assumptions** — architecture removes assumptions so code works with more cases; optimization adds assumptions ("never more than 256 enemies → pack ID in one byte") to go fast
- **Spectrum of dispatch**:

  | Mechanism | Decision point | Flexibility | Runtime cost |
  |-----------|---------------|-------------|--------------|
  | Concrete method call | Author time | Low | None |
  | Template instantiation (C++) | Compile time | Medium | None |
  | Virtual / interface | Runtime | High | Some |

- **Pragmatic compromise** — keep code flexible while the design is still settling, then tear out abstraction later to reclaim performance. *"It's easier to make a fun game fast than it is to make a fast game fun."*

## 5. Prototyping and Throwaway Code

- **Slapdash code has its place** — prototyping is writing code "just barely functional enough to answer a design question". Legitimate when you're exploring, especially early in a game's life
- **The catch: you must actually throw it away** — the trap is a boss saying "that prototype is great, just clean it up a bit and ship it". Unmaintainable code ships, and you're stuck with it
- **Defense** — ensure stakeholders know throwaway code is unmaintainable. One trick: write prototypes in a different language than the real game, so they *have* to be rewritten

## 6. Striking a Balance

- **Three competing forces, all about "speed"**:

  1. **Long-term development speed** — clean architecture makes future changes cheap
  2. **Runtime speed** — the game itself has to execute fast
  3. **Short-term development speed** — today's feature has to land today

- **They pull against each other** — clean architecture costs effort per change; optimization calcifies code and resists future change; rushing features accrues hacks that sap later productivity
- **No right answer, only tradeoffs** — this is the source of the craft. Like chess, the interlocking constraints are what make software architecture worth mastering

## 7. Simplicity

- **Simplicity is the best lever against all three forces** — clean, direct code is easier to load into your head, easier to change, and often runs fast because there's less to execute
- **Simple ≠ quick to write** — a simple solution is a *distillation* of code, not an accretion. It takes more effort, not less ("I would have written a shorter letter, but I did not have the time." — Pascal)
- **Novice trap** — churning out conditionals, one per observed use case. The resulting code is brittle and collapses on inputs the author didn't imagine
- **Elegant solutions are general** — a small piece of logic that covers a large space of use cases. Finding it is pattern-matching: seeing past the examples to the hidden order underneath

## 8. Parting Advice

- **Abstract only when confident the flexibility is needed** — don't waste time decoupling code that won't need to change
- **Design for performance throughout, but defer low-level optimization** — ship-breaking performance problems should be caught early; bit-twiddling waits until late
- **Move fast on design exploration, but don't leave a mess** — you'll have to live in the codebase afterward
- **Don't polish code you're going to throw away** — "rock stars trash hotel rooms because they know they're going to check out the next day"
- **If you want to make something fun, have fun making it**
