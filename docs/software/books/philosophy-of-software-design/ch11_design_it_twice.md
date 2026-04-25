# Ch 11: Design it Twice

## Table of Contents

- [1. The Core Principle](#1-the-core-principle)
- [2. How to Apply It](#2-how-to-apply-it)
- [3. Evaluating Alternatives](#3-evaluating-alternatives)
- [4. Applies at Every Level](#4-applies-at-every-level)
- [5. The Smart-Person Trap](#5-the-smart-person-trap)

## 1. The Core Principle

- **Design it twice** — before committing to a design, consider at least two fundamentally different approaches for each major decision. Your first idea is unlikely to be the best one, and comparing alternatives reveals strengths and weaknesses you'd otherwise miss
- **Radically different alternatives** — don't pick two similar approaches; the further apart they are, the more you learn about the design space. Even if you're certain one approach is correct, sketch a second anyway to test that certainty

## 2. How to Apply It

- **Rough sketches, not full designs** — you don't need to pin down every detail; outline a few of the most important methods or structural choices for each alternative
- **List pros and cons** — after roughing out alternatives, explicitly compare them. The best choice may be one of the alternatives, or a hybrid that combines the best features of several
- **When nothing looks good** — if all alternatives feel awkward, use their specific weaknesses to drive a new design. Identifying what's wrong with each option often reveals the right abstraction (e.g., a text editor class where both line-oriented and character-oriented APIs are clumsy may point toward a range-oriented API that eliminates the problems of both)
- **Low time cost** — for a class-sized module, exploring alternatives might take an hour or two, which is negligible compared to the days or weeks of implementation and pays back in a significantly better design

## 3. Evaluating Alternatives

- **Ease of use for callers** — the most important criterion for an interface is how simple it makes life for higher-level code
- **Simplicity of the interface** — fewer concepts and methods means less cognitive load
- **Generality** — a more general-purpose interface tends to be more reusable and longer-lived
- **Performance** — some interfaces enable more efficient implementations (e.g., a character-at-a-time API forces many small calls, which can be significantly slower)

## 4. Applies at Every Level

- **Interfaces** — choose between alternative APIs for a module
- **Implementations** — once the interface is set, explore different internal data structures and algorithms (e.g., linked list vs. gap buffer for a text class)
- **System-level** — use the same approach when decomposing a system into major modules or choosing features for a user interface

## 5. The Smart-Person Trap

- **First-idea bias** — smart people often develop a habit of going with their first idea because it was always good enough in school. As problems get harder, this habit becomes a liability
- **Not a sign of weakness** — needing multiple iterations doesn't mean you're not smart; it means the problem is genuinely hard. Large software design is always in that category
- **Skill-building effect** — repeatedly devising and comparing alternatives trains your design intuition, making it progressively easier to spot bad designs and converge on good ones
