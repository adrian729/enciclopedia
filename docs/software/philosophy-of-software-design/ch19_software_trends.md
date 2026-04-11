# Ch 19: Software Trends

## Table of Contents

- [1. Object-Oriented Programming and Inheritance](#1-object-oriented-programming-and-inheritance)
- [2. Agile Development](#2-agile-development)
- [3. Unit Tests](#3-unit-tests)
- [4. Test-Driven Development](#4-test-driven-development)
- [5. Design Patterns](#5-design-patterns)
- [6. Getters and Setters](#6-getters-and-setters)
- [7. Evaluating Trends](#7-evaluating-trends)

## 1. Object-Oriented Programming and Inheritance

- **Private methods and variables** — enforce information hiding by preventing external code from creating dependencies on internal state
- **Interface inheritance** — a parent class defines method signatures without implementations; each subclass provides its own. This provides leverage against complexity by reusing the same interface for multiple purposes (e.g., an I/O interface for both disk files and network sockets)
- **Depth through interface inheritance** — the more implementations an interface has, the deeper it becomes, because the interface must capture essential features while omitting details that differ between implementations. This is the heart of abstraction
- **Implementation inheritance** — a parent class provides default method implementations that subclasses can inherit or override. Reduces change amplification because shared behavior lives in one place instead of being duplicated across subclasses

| Inheritance type | Benefit | Risk |
|------------------|---------|------|
| **Interface inheritance** | Reuses a single interface across many implementations; deepens abstractions | Minimal — aligns naturally with information hiding |
| **Implementation inheritance** | Eliminates duplicated code across subclasses; reduces change amplification | Creates tight coupling between parent and subclasses; instance variables often leak across the hierarchy, forcing developers to understand the whole tree to make changes |

- **Prefer composition over implementation inheritance** — when possible, use small helper classes to provide shared functionality instead of inheriting from a parent. This avoids the dependency web that deep class hierarchies create
- **If using implementation inheritance** — separate state managed by the parent from state managed by subclasses. Subclasses should access parent state only in read-only fashion or through parent methods, applying information hiding within the hierarchy
- **OOP mechanisms don't guarantee good design** — shallow classes, complex interfaces, or exposed internal state still produce high complexity regardless of whether OOP is used

## 2. Agile Development

- **Incremental and iterative development** — agile's core idea of building systems in small iterations aligns with the book's advocacy for incremental design, since it's impossible to visualize the best design up front
- **Risk: tactical programming** — agile's focus on features (not abstractions) and its pressure to ship working software quickly can discourage investment in clean design, leading to rapid accumulation of complexity
- **"Implement minimally now, refactor later"** — this common agile advice argues against an investment approach and encourages a more tactical style of programming, which can result in a rapid accumulation of complexity

> **Design Principle: Increments should be abstractions, not features** — it's fine to defer thinking about an abstraction until a feature needs it, but once you need it, invest the time to design it cleanly and make it somewhat general-purpose

## 3. Unit Tests

- **Unit tests vs. system tests** — unit tests are small, focused, and validate individual methods in isolation; system (integration) tests verify that components work together in a production-like environment
- **Tests enable refactoring** — without a test suite, developers avoid structural changes because bugs go undetected until deployment. With good tests, developers gain confidence to improve the design, knowing the suite will catch regressions
- **Unit tests are especially valuable** — they provide higher code coverage than system tests, making them more likely to uncover bugs introduced by changes
- **Example: Tcl byte-code compiler** — replacing Tcl's interpreter with a byte-code compiler affected almost every part of the engine. The existing unit test suite caught virtually all bugs, with only a single bug surfacing after the alpha release

## 4. Test-Driven Development

- **TDD approach** — write unit tests first (based on expected behavior), then implement code to make each test pass one at a time
- **Problem: TDD encourages tactical programming** — by focusing on making the next test pass, TDD directs attention toward getting specific features working rather than finding the best design. There is no natural moment to step back and think about abstractions
- **Too incremental** — TDD tempts developers to hack in the next feature rather than designing a coherent abstraction. The result tends toward a design that was never intentionally shaped

- **Design abstractions all at once** — once you discover the need for an abstraction, design it completely (or at least its core functions) rather than building it in pieces over time. A holistic design produces pieces that fit together well

- **Exception: bug-fixing** — writing a failing test before fixing a bug is genuinely valuable. It ensures the test actually triggers the bug, confirming the fix is real

## 5. Design Patterns

- **Design patterns** — well-known solutions to common problems (e.g., iterator, observer). They save effort because they encode proven approaches that are hard to improve upon for the situations they target
- **Risk: over-application** — not every problem fits a pattern. Forcing a custom problem into an existing pattern produces worse results than a tailored approach
- **More patterns are not automatically better** — patterns improve a system only when they genuinely fit the situation

## 6. Getters and Setters

- **Purpose** — getter/setter methods wrap access to instance variables, allowing future additions like validation, notification, or constraint enforcement without changing the interface
- **Problem: they violate information hiding** — exposing instance variables (even through wrappers) makes implementation details visible externally, increasing interface complexity
- **Shallow methods** — getters and setters are typically one-liners that add clutter to the interface without meaningful functionality
- **Better approach** — avoid exposing implementation data in the first place. If the internal representation doesn't need to be visible, don't create accessors for it
- **Pattern overuse** — once a pattern like getters/setters is established, developers tend to apply it reflexively, leading to unnecessary proliferation

## 7. Evaluating Trends

- **Challenge every paradigm from the standpoint of complexity** — many proposals sound good on the surface, but under scrutiny some make complexity worse, not better. The litmus test for any software development trend is whether it genuinely helps minimize complexity in large systems
