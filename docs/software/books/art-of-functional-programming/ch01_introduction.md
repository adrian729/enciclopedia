# Ch 1: Introduction

## Table of Contents

- [1. Imperative Programming and the Von Neumann Bottleneck](#1-imperative-programming-and-the-von-neumann-bottleneck)
- [2. How Functional Programming Does Better](#2-how-functional-programming-does-better)
- [3. Why Functional Programming Matters](#3-why-functional-programming-matters)

## 1. Imperative Programming and the Von Neumann Bottleneck

- **Imperative paradigm** — models a program as a sequence of commands that mutate state: "first do this, then do that." Even object-oriented code usually implements methods in this imperative style
- **Von Neumann architecture** — CPU + memory + bus; the CPU runs a mechanical fetch-execute cycle over machine instructions that shuttle data between registers and memory. John Backus argued that imperative programming dominates because the paradigm is conceptually tied to this hardware model — the primary concern becomes how to update memory cells in a stepwise manner
- **Low-level nature** — imperative code is fundamentally about updating memory cells step by step. Variables correspond to memory cells, assignment statements (`i = i + 1`) translate to load-add-store sequences on the CPU, and `while` loops map to branch/jump instructions. This means even high-level imperative code (C, Java, Python) is still conceptually tied to the physical machine
- **Limited composition** — because imperative programs are sequences of state-mutating statements, they don't compose or decompose well. A `while` loop is a single monolithic unit — you can't break it into smaller reusable parts or plug it into a larger expression, which makes it hard to build complex programs from simpler ones

## 2. How Functional Programming Does Better

- **Composition from reusable parts** — the sum-of-squares problem that requires a monolithic loop imperatively becomes `(fold (+) 0 . map square) [1..n]` in FP. Only `square`, `(+)`, and `0` are problem-specific; `map`, `fold`, and `.` (function composition) are general-purpose components that can be reused across any program
- **Declarative over imperative** — FP describes *what* the program computes rather than *how* each step mutates state. This reduces cognitive load because you can grasp the program from its structure at a glance, without mentally simulating execution step by step
- **Easy extension** — adding a new requirement (e.g., only sum primes) means plugging in another component: `(fold (+) 0 . map square . filter isPrime) [1..n]`. Imperatively, the same change requires copy-pasting the loop and threading an `if` statement into its body
- **Dataflow perspective** — a functional program can be viewed as a pipeline where the output of one function flows into the input of the next, making the data transformations explicit and the overall structure easy to visualize

## 3. Why Functional Programming Matters

- **Powerful problem-solving tool** — FP can elegantly solve many programming problems in various domains. It excels at applications dealing with hierarchical structures such as JSON and XML, and is well suited to data processing in mobile apps, web apps, or backend services — especially filtering, transforming, and aggregating data. Peter Norvig recommends learning at least one language that emphasizes functional abstraction
- **Sharpens design ability** — even when not used directly at work, learning FP improves one's ability to compose complex programs from simpler ones and define highly reusable abstractions — skills that transfer to any language or paradigm
- **Industry trend toward declarative** — non-functional mainstream languages like Java keep introducing features to write functional code; new languages like Elm, Elixir, Scala, Swift, and Kotlin support FP from the ground up; frameworks like ReactiveX and Akka Streams are built on FP principles. The broader shift is from imperative to declarative across the industry: build systems (Maven/Gradle over Ant), declarative UI, and declarative deployment infrastructure all favor describing *what* over specifying *how*
- **A new way of thinking** — per Alan Perlis: "A language that doesn't affect the way you think about programming is not worth knowing." FP concepts may feel awkward at first — this is normal and expected because you are acquiring a new way of thinking
