# Summary of Design Principles and Red Flags

## Table of Contents

- [1. Design Principles](#1-design-principles)
- [2. Red Flags](#2-red-flags)

## 1. Design Principles

> **Design Principle: Complexity is incremental** — you have to sweat the small stuff. Each tiny bit of complexity seems harmless on its own, but they accumulate into an unmanageable whole

> **Design Principle: Working code isn't enough** — introducing unnecessary complexity to get something working quickly is not acceptable; design quality matters alongside correctness

> **Design Principle: Make continual small investments to improve system design** — take a strategic approach: spend a little extra time with each change to improve the overall structure rather than just patching in features

> **Design Principle: Modules should be deep** — the best modules provide powerful functionality behind a simple interface. The ratio of interface complexity to functionality is what matters

> **Design Principle: Interfaces should be designed to make the most common usage as simple as possible** — optimize the interface for the frequent case; rare cases can require more effort from the caller

> **Design Principle: It's more important for a module to have a simple interface than a simple implementation** — push complexity into the implementation where it is hidden, rather than exposing it through the interface where every caller must deal with it

> **Design Principle: General-purpose modules are deeper** — a general-purpose interface covers more use cases with fewer methods, making the module deeper and more reusable than a special-purpose design

> **Design Principle: Separate general-purpose and special-purpose code** — keep general-purpose logic in lower layers and special-purpose logic in higher layers; mixing them creates complexity and limits reusability

> **Design Principle: Different layers should have different abstractions** — if adjacent layers have similar abstractions, it is a sign that the class decomposition is not clean. Each layer should add meaningful transformation

> **Design Principle: Pull complexity downward** — it is better for a module's implementer to handle complexity than to push it onto the module's users, because the implementer handles it once while users handle it repeatedly

> **Design Principle: Define errors (and special cases) out of existence** — redesign APIs so that error conditions cannot arise in the first place, rather than forcing every caller to handle them

> **Design Principle: Design it twice** — before settling on a design, consider at least two alternatives. Comparing options reveals the strengths and weaknesses of each and often leads to a better result

> **Design Principle: Comments should describe things that are not obvious from the code** — if a comment merely restates what the code says, it adds no value; comments should capture the designer's intent, rationale, and non-obvious constraints

> **Design Principle: Software should be designed for ease of reading, not ease of writing** — code is read far more often than it is written. Invest extra effort at write time to save time for all future readers

> **Design Principle: The increments of software development should be abstractions, not features** — build systems by designing clean abstractions one at a time, rather than hacking in one feature after another

## 2. Red Flags

> **Red Flag: Shallow Module** — the interface for a class or method isn't much simpler than its implementation. The module provides little benefit because callers must understand almost as much as the implementer

> **Red Flag: Information Leakage** — a design decision is reflected in multiple modules. Changes to that decision will require modifying all of them, creating tight coupling

> **Red Flag: Temporal Decomposition** — the code structure is based on the order in which operations are executed, not on information hiding. This scatters related knowledge across multiple modules

> **Red Flag: Overexposure** — an API forces callers to be aware of rarely used features in order to use commonly used features. The common case should be simple, with rare options hidden behind defaults

> **Red Flag: Pass-Through Method** — a method does almost nothing except pass its arguments to another method with a similar signature. It adds a layer without adding value, creating unnecessary complexity

> **Red Flag: Repetition** — a nontrivial piece of code is repeated over and over. Each copy creates a maintenance liability because all copies must be found and updated together

> **Red Flag: Special-General Mixture** — special-purpose code is not cleanly separated from general-purpose code. The tangling makes the general-purpose code harder to reuse and the special-purpose code harder to understand

> **Red Flag: Conjoined Methods** — two methods have so many dependencies that it's hard to understand the implementation of one without understanding the implementation of the other. They should likely be merged or restructured

> **Red Flag: Comment Repeats Code** — all of the information in a comment is immediately obvious from the code next to it. Such comments add clutter without value

> **Red Flag: Implementation Documentation Contaminates Interface** — an interface comment describes implementation details not needed by users of the thing being documented. This couples callers to the implementation

> **Red Flag: Vague Name** — the name of a variable or method is so imprecise that it doesn't convey much useful information. Good names are specific enough to tell the reader what the entity does or holds

> **Red Flag: Hard to Pick Name** — difficulty finding a precise and intuitive name for an entity often indicates that the entity itself is not well-defined or is trying to do too much

> **Red Flag: Hard to Describe** — if the documentation for a variable or method must be long to be complete, the underlying design may be too complex. A clean abstraction should be easy to describe concisely

> **Red Flag: Nonobvious Code** — the behavior or meaning of a piece of code cannot be understood easily. Code should be structured so that its intent is apparent without requiring deep analysis
