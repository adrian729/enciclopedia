# Ch 3: Modularity

## Table of Contents

- [1. Modularity Versus Granularity](#1-modularity-versus-granularity)
- [2. Defining Modularity](#2-defining-modularity)
- [3. Cohesion](#3-cohesion)
- [4. Coupling](#4-coupling)
- [5. Core Metrics: Abstractness and Instability](#5-core-metrics-abstractness-and-instability)
- [6. Distance from the Main Sequence](#6-distance-from-the-main-sequence)
- [7. Connascence](#7-connascence)
- [8. From Modules to Components](#8-from-modules-to-components)

- **Modularity is an *implicit* architecture characteristic** — no requirements document asks for it, but sustainable code bases need the order it imposes. Software systems, like physical ones, tend toward entropy unless an architect actively expends energy to preserve structure.

> *"95% of the words written about software architecture are spent extolling the benefits of 'modularity' and little, if anything, is said about how to achieve it."* — Glenford J. Myers

## 1. Modularity Versus Granularity

- **Modularity** — *breaking a system apart* into smaller pieces (e.g., monolith → microservices). About logical separation.
- **Granularity** — *the size of those pieces*; how big a service or component should be.

> *"Embrace modularity, but beware of granularity."* — Mark Richards

- **Granularity is where trouble starts** — wrong-sized pieces produce coupled antipatterns: **Spaghetti Architecture**, **Distributed Monoliths**, and the famous **Big Ball of Distributed Mud**. The cure is paying attention to coupling between services and components.

## 2. Defining Modularity

- **Working definition** — *modularity* is a logical grouping of related code: classes in OO, functions in functional/structured, or any package/namespace. It's logical, not necessarily physical.
- **Why packaging matters to architects** — tightly coupled packages resist reuse and resist later restructuring of the architecture.
- **Namespace** — a unique, fully qualified name that disambiguates assets (the internet is the canonical example). Most languages combine modules with namespaces (Java `package`, .NET `namespace`).
- **Java history sidebar** — Java 1.0 forced package directories to match filesystem directories so the OS would prevent name collisions. JAR files (Java 1.2) broke this guarantee, leading to a decade of classpath war stories.
- **Pre-OO origins** — after Dijkstra's *Go To Statement Considered Harmful* (1968), structured languages (Pascal, C) lacked logical grouping. The short-lived **modular languages** of the mid-1980s (Modula, Ada) introduced modules; OO languages absorbed them as packages/namespaces.

## 3. Cohesion

- **Cohesion** — the extent to which a module's parts belong together. An ideally cohesive module cannot be split without forcing extra coupling between the resulting pieces.

> *"Attempting to divide a cohesive module would only result in increased coupling and decreased readability."* — Larry Constantine

- **Cohesion levels (best to worst):**

| Level | Meaning |
|---|---|
| **Functional** | Every part is related; the module contains everything it needs to function |
| **Sequential** | One module's output feeds the next module's input |
| **Communicational** | Modules form a chain, each contributing to a shared output (e.g., add DB record → email notification) |
| **Procedural** | Modules must execute in a particular order |
| **Temporal** | Related only by timing (e.g., system-startup initialization tasks) |
| **Logical** | Data is logically related but not functionally (e.g., Java's `StringUtils` static helpers) |
| **Coincidental** | Elements share only a source file — the worst form |

- **Cohesion is subjective** — should `get/cancel customer orders` live in `Customer Maintenance` or split into `Order Maintenance`? Depends on growth expectations, the rest of the order behavior, and how much knowledge the split would require crossing the boundary.
- **LCOM (Lack of Cohesion in Methods)** — the Chidamber & Kemerer structural metric for cohesion. Roughly: *the sum of sets of methods not shared via sharing fields*. A class with private fields `a` and `b`, where most methods touch only one or the other, scores high LCOM — those field/method pairs could each become their own class.
- **LCOM caveat** — only finds *structural* lack of cohesion, never *logical* lack. Reflects the Second Law of Software Architecture: *why* matters more than *how*.

## 4. Coupling

- **Two foundational metrics from Yourdon & Constantine's *Structured Design* (1979):**
  - **Afferent coupling** — *incoming* connections to a code artifact (component, class, function). Mnemonic: *a* before *e*, like *incoming* before *outgoing*.
  - **Efferent coupling** — *outgoing* connections from the artifact to others. Mnemonic: *e* in *efferent* matches *e* in *exit*.
- **Why the bad names?** Yourdon and Constantine borrowed mathematical symmetry over clarity; the metrics should arguably have been called *incoming* and *outgoing*. Tooling exists for nearly every platform to measure both.

## 5. Core Metrics: Abstractness and Instability

Robert C. Martin's derived metrics, applicable to most OO languages.

- **Abstractness** — ratio of abstract artifacts (interfaces, abstract classes) to concrete ones. A 5,000-line `main()` method has abstractness near 0; an over-abstracted code base full of `AbstractSingletonProxyFactoryBean`-style hierarchies sits near 1. Formula: `A = Σm^a / (Σm^c + Σm^a)`.
- **Instability** — ratio of efferent coupling to total coupling: `I = C^e / (C^e + C^a)`. Measures *volatility*: a class with many outgoing calls breaks easily when any callee changes.
- Both metrics fall between 0 and 1.

## 6. Distance from the Main Sequence

- **Distance from the Main Sequence** — a holistic structural metric derived from Abstractness and Instability: `D = A + I - 1`.
- **The main sequence** is the idealized line `A + I = 1` on the Abstractness-vs-Instability graph. Classes near the line are well balanced.
- **Zone of Uselessness** (upper-right) — too abstract to be useful; nobody knows how to wire it up.
- **Zone of Pain** (lower-left) — too concrete, too coupled; brittle and hard to maintain.
- **Use cases** — analyzing code bases, preparing for migrations, assessing technical debt.
- **Limit of metrics** — even structural metrics need interpretation. Cyclomatic Complexity, for example, can't tell *essential* complexity (the problem is hard) from *accidental* complexity (the code made it harder than necessary). Establish baselines and apply judgment.

## 7. Connascence

From Meilir Page-Jones's *What Every Programmer Should Know about Object-Oriented Design* (1996), repopularized by Jim Weirich.

- **Connascence definition** — two components are *connascent* if changing one would force the other to change to keep the system correct. It's a *vocabulary* for kinds of coupling, not a metric.
- **Two top-level categories:** *static* (source-code coupling) and *dynamic* (runtime coupling).

### 7.1. Static Connascence

| Type | Meaning |
|---|---|
| **Connascence of Name** | Components must agree on the name of an entity. Most common, most desirable — modern refactoring tools rename safely across a code base |
| **Connascence of Type** | Components must agree on the type of an entity (statically typed languages, plus opt-ins like Clojure Spec) |
| **Connascence of Meaning** (a.k.a. *Convention*) | Components must agree on what particular values mean. Classic case: hard-coded `int TRUE = 1; int FALSE = 0` |
| **Connascence of Position** | Components must agree on order. `updateSeat("14D", "Ford, N")` is type-correct but semantically swapped |
| **Connascence of Algorithm** | Components must agree on an algorithm — e.g., a security hash that must produce identical output on client and server |

### 7.2. Dynamic Connascence

| Type | Meaning |
|---|---|
| **Connascence of Execution** | Order of execution matters (`email.send()` before `email.setSubject(...)` is broken) |
| **Connascence of Timing** | Timing matters — race conditions between threads |
| **Connascence of Values** | Several values must change together (rectangle corners; transactions across distributed databases) |
| **Connascence of Identity** | Multiple components must reference the *same* entity — e.g., a shared distributed queue |

### 7.3. Connascence Properties

- **Strength** — how hard the coupling is to refactor away. Prefer *static* over *dynamic* (static is detectable by source analysis and easy to fix). Refactoring example: turn a magic value (Connascence of Meaning) into a named constant (Connascence of Name).
- **Locality** — how proximal the coupled modules are. Strong connascence inside the same module is fine; strong connascence across module boundaries is a code smell. This is the same insight **DDD** encodes as the **bounded context** — limit implementation coupling to a narrow scope.
- **Degree** — the *size of impact*: how many classes/modules a change ripples through. Small degree of strong connascence may be tolerable; degrees grow as code bases grow.

> **Page-Jones's three modularity guidelines** —
> 1. Minimize overall connascence by breaking the system into encapsulated elements.
> 2. Minimize remaining connascence that crosses encapsulation boundaries.
> 3. Maximize connascence within encapsulation boundaries.

> **Jim Weirich's two rules** —
> - **Rule of Degree:** convert strong forms of connascence into weaker ones.
> - **Rule of Locality:** as distance between elements increases, use weaker forms of connascence.

- **Why learn it?** Same reason as design patterns: connascence gives architects a precise shared vocabulary. *"Don't add a magic string in the middle of a method"* becomes *"You have Connascence of Meaning; refactor it to Connascence of Name."*

## 8. From Modules to Components

- The book uses **module** as the generic term for "a bundle of related code"; most architects call these **components**, the building blocks of software architecture.
- The concept is as old as computer science, yet teams still struggle to do it well. Component-based thinking and deriving components from problem domains are covered in Chapter 8 — but first the book turns to **architecture characteristics and their scope** (Chapters 4–7).
