# Ch 8: Conclusion

## Table of Contents

- [1. Core Takeaways](#1-core-takeaways)
- [2. Where to Go from Here](#2-where-to-go-from-here)

## 1. Core Takeaways

- **Abstraction is FP's greatest strength** — functions abstract over specific values (a `square` function computes the square of *any* number, not just one). First-class functions elevate this further: higher-order functions like `accumulate`, `map`, `filter`, and `fold` abstract over entire computation patterns, not just values
- **Composition is what makes FP scale** — large programs are built by composing smaller ones. Three properties make this work in FP: (1) everything is an expression, so smaller expressions combine freely into larger ones; (2) functions are pure, always returning the same output for the same input; (3) data is immutable, so functions construct new data rather than mutating existing state
- **Dataflow composition via shared interfaces** — functions that agree on a shared data structure (e.g., lists) can be connected in a dataflow pipeline. This is why `map`, `filter`, and `fold` compose so naturally: lists serve as the common interface between stages
- **Big ideas are simple ideas** — David Ogilvy, credited as "Father of Advertising," used to say that "big ideas are usually simple ideas." Many big ideas in FP — first-class functions, higher-order functions, pure functions, immutable data, currying, and partial application — might look scary at first but are inherently simple

## 2. Where to Go from Here

- **Apply FP to your own projects** — most mainstream languages (Kotlin, Java, JavaScript, Swift, Python, Scala) already support functional programming, so the concepts from this book transfer directly
- **Recommended reading for deeper understanding**:

| Book | Authors | Focus |
|------|---------|-------|
| *Structure and Interpretation of Computer Programs* (SICP) | Harold Abelson and Gerald Jay Sussman, with Julie Sussman | Functional way of thinking |
| *Thinking Functionally with Haskell* | Richard Bird | Functional way of thinking |
| *Real-world OCaml* | — | Practical OCaml |
| *Real World Haskell* | — | Practical Haskell |

- **Fundamentals transcend languages** — the fundamentals discussed in the book remain valid regardless of which programming language you use. Mastery lies in the balancing act between striving to grasp the fundamental principles and applying them to real-world problems pragmatically
