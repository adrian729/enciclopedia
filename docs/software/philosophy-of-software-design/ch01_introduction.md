# Ch 1: Introduction

## Table of Contents

- [1. Core Premise](#1-core-premise)
- [2. Two Approaches to Fighting Complexity](#2-two-approaches-to-fighting-complexity)
- [3. Design is Continuous](#3-design-is-continuous)
- [4. How to Use This Book](#4-how-to-use-this-book)

## 1. Core Premise

- **Greatest limitation in software** — our ability to understand the systems we create, not physical constraints or coordination skill
- **Complexity accumulates** — as features are added, subtle dependencies form between components, making it harder to keep all relevant factors in mind when modifying the system
- **Tools aren't enough** — good tools help manage complexity, but to build larger and more powerful systems we must find ways to make the software itself simpler
- **Two goals of this book** — (1) describe the nature of software complexity: what it means, why it matters, how to recognize it; (2) present higher-level, philosophical techniques (e.g., "classes should be deep," "define errors out of existence") for minimizing complexity during development

## 2. Two Approaches to Fighting Complexity

| Approach | How |
|----------|-----|
| **Eliminate** | Make code simpler and more obvious — remove special cases, use identifiers consistently |
| **Encapsulate** | Hide complexity via **modular design** — divide the system into independent modules so a developer can work on one without understanding the internals of others |

## 3. Design is Continuous

- **Waterfall fails for software** — software is too complex to fully visualize upfront. Problems surface during implementation when the design is already frozen, so developers patch around them instead of redesigning, causing complexity to explode
- **Incremental/agile works** — design a small subset, implement, evaluate, fix problems, then add more features. Early problems are caught while the system is still small, and later features benefit from lessons learned
- **Software is malleable** — unlike physical systems (e.g., you can't change the number of towers on a bridge mid-construction), software can absorb major design changes during implementation, which is what makes incremental development feasible
- **Design is never done** — developers should always be thinking about design and planning time for improvements, not just new features

## 4. How to Use This Book

- **Red flags** — recurring signs that code is more complicated than it needs to be. When you spot one, stop and try alternative designs until the flag goes away. The more alternatives you explore, the more you learn
- **Code reviews** — the best context to apply the book's principles, because it's easier to see design problems in someone else's code than in your own
- **Moderation** — every principle has limits; taking any design idea to its extreme leads to a bad place. Good design is a balance between competing approaches
- **Applicability** — examples are Java/C++, but the concepts apply to any language and any module type (functions, subsystems, network services)
