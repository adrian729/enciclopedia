# Ch 15: Write The Comments First

## Table of Contents

- [1. Delayed Comments Are Bad Comments](#1-delayed-comments-are-bad-comments)
- [2. The Comments-First Approach](#2-the-comments-first-approach)
- [3. Comments as a Design Tool](#3-comments-as-a-design-tool)
- [4. Early Comments Are Fun and Cheap](#4-early-comments-are-fun-and-cheap)

## 1. Delayed Comments Are Bad Comments

- **Procrastination spirals** — once you delay writing comments, it's easy to keep delaying. The backlog grows, the task becomes more daunting, and it never gets done
- **Mental checkout** — even if you do go back, the design decisions are no longer fresh. You skim the code, repeat what the code already says, and miss the deeper reasoning that comments should capture
- **"Code is still changing" excuse** — developers rationalize delay by saying comments will need rewriting, but this saves very little time (see section 4) and guarantees worse documentation

## 2. The Comments-First Approach

- **Write comments before code** — for a new class, start with the class interface comment, then method signatures with interface comments, then instance variable declarations with comments, and finally fill in method bodies
- **Iterate on the comments** — adjust the interface comments until the abstraction feels right before writing implementation code
- **No backlog** — when the code is done, the comments are already done. There is never a pile of undocumented code waiting for attention
- **Better comments result** — design decisions are fresh in your mind while writing, so it's easy to record the reasoning behind them rather than just restating the code

## 3. Comments as a Design Tool

- **Comments capture abstractions** — abstractions are fundamental to good design, and comments are the only way to fully describe them. Writing them first forces you to identify the essence of each module or variable before coding
- **Canary for complexity** — if an interface comment must be long and complicated to fully describe a method, the method's interface is too complex. Short, complete interface comments signal a deep module; long ones signal a shallow one
- **Compare interface to implementation** — if the interface comment must describe all major implementation features, the method is shallow. This comparison is a quick litmus test for module depth

> **Red Flag: Hard to Describe** — if you find it difficult to write a simple yet complete comment for a method or variable, that indicates a problem with the design of the thing you are describing

- **Comments only work as a complexity indicator when they are complete and clear** — a cryptic or incomplete comment can't serve as a reliable measure of interface depth

## 4. Early Comments Are Fun and Cheap

- **Writing comments early is enjoyable** — the early design phase (fleshing out abstractions and structure) is one of the most creative parts of programming. Comments are how you record and test design quality during this phase
- **Simplicity as pride** — finding a design that can be expressed completely and clearly in the fewest words is satisfying. Simpler comments = better design
- **Cost is negligible** — typing code and comments together is roughly 10% of total development time; comments alone are perhaps 5%. Delaying saves only a fraction of that 5%
- **May actually save time overall** — writing comments first stabilizes abstractions earlier, reducing code churn. Writing code first means abstractions evolve during implementation, requiring more revisions
