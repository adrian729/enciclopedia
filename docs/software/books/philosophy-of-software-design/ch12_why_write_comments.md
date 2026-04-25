# Ch 12: Why Write Comments? The Four Excuses

## Table of Contents

- [1. The Four Excuses](#1-the-four-excuses)
  - [1.1. "Good Code is Self-Documenting"](#11-good-code-is-self-documenting)
  - [1.2. "I Don't Have Time"](#12-i-dont-have-time)
  - [1.3. "Comments Get Out of Date"](#13-comments-get-out-of-date)
  - [1.4. "All Comments Are Worthless"](#14-all-comments-are-worthless)
- [2. Benefits of Well-Written Comments](#2-benefits-of-well-written-comments)
- [3. A Different Opinion: Clean Code](#3-a-different-opinion-clean-code)

## 1. The Four Excuses

### 1.1. "Good Code is Self-Documenting"

- **Code can't capture everything** — method signatures express formal aspects of an interface, but informal aspects (high-level behavior, meaning of return values, conditions for calling a method, design rationale) can only be expressed in comments
- **Reading code is not a substitute** — expecting users to read method implementations to understand behavior destroys abstraction. It also pressures developers to write many tiny (shallow) methods, which doesn't actually help because readers must then chase through nested calls
- **Comments complete the abstraction** — without comments, the only abstraction of a method is its declaration, which omits too much essential information (e.g., is the `end` index inclusive or exclusive?). Comments in a human language provide the expressive power to create simple, intuitive descriptions that code syntax cannot

### 1.2. "I Don't Have Time"

- **Investment mindset** — there will always be something that seems higher priority than writing comments. If you allow documentation to be de-prioritized, you'll end up with none
- **Low actual cost** — typing code (excluding design, compiling, testing) is roughly 10% of development time. Even if commenting doubles that typing time, it adds only ~10% to overall effort, which is quickly repaid by easier maintenance
- **Abstraction comments pay for themselves immediately** — top-level class and method comments should be written as part of the design process, where they also serve as a design tool (covered in Ch 15)

### 1.3. "Comments Get Out of Date"

- **Manageable in practice** — large documentation changes only happen when there are large code changes, and the code changes always take more time. Keeping docs close to the corresponding code and avoiding duplication makes updates nearly effortless
- **Code reviews catch staleness** — reviews are a natural mechanism for detecting and fixing comments that have drifted from the code

### 1.4. "All Comments Are Worthless"

- **This excuse has some merit** — most existing comments are mediocre or useless. But the problem is solvable: writing good documentation is not hard once you know how (covered in the following chapters)

## 2. Benefits of Well-Written Comments

- **Capture the designer's knowledge** — comments record information that was in the mind of the original developer but couldn't be expressed in code, from low-level hardware quirks to high-level design rationale. Without them, future developers must re-derive or guess at this knowledge, wasting time and risking bugs
- **Reduce cognitive load** — documentation gives developers the information they need for a change without forcing them to read large amounts of code
- **Eliminate unknown unknowns** — documentation clarifies system structure so developers know what code and information is relevant to any given change
- **Clarify dependencies and remove obscurity** — the two root causes of complexity (from Ch 2) are directly addressed by good documentation

## 3. A Different Opinion: Clean Code

- **Robert Martin's position** — "comments are always failures"; if code were expressive enough, comments would be unnecessary. He advocates replacing comments with well-named methods: instead of commenting a block of code, extract it into a method whose name serves as the comment
- **Ousterhout's disagreement** — comments provide fundamentally different information than code. Code cannot express high-level design rationale, informal interface contracts, or the "why" behind decisions. These things can only be captured in natural language
- **Method names are not a substitute** — Martin's approach produces long, cryptic names like `isLeastRelevantMultipleOfNextLargerPrimeFactor` that convey less information than a well-written comment, and developers end up effectively retyping the documentation (the method name) every time they invoke it
- **Comments are not failures** — well-written comments increase the value of code and play a fundamental role in defining abstractions and managing system complexity
