# Ch 13: Comments Should Describe Things that Aren't Obvious

## Table of Contents

- [1. Guiding Principle](#1-guiding-principle)
- [2. Comment Conventions](#2-comment-conventions)
- [3. Don't Repeat the Code](#3-dont-repeat-the-code)
- [4. Two Levels of Detail](#4-two-levels-of-detail)
  - [4.1. Lower-Level Comments Add Precision](#41-lower-level-comments-add-precision)
  - [4.2. Higher-Level Comments Enhance Intuition](#42-higher-level-comments-enhance-intuition)
- [5. Interface Documentation](#5-interface-documentation)
  - [5.1. Class Interface Comments](#51-class-interface-comments)
  - [5.2. Method Interface Comments](#52-method-interface-comments)
- [6. Implementation Comments: What and Why, Not How](#6-implementation-comments-what-and-why-not-how)
- [7. Cross-Module Design Decisions](#7-cross-module-design-decisions)

## 1. Guiding Principle

- **Comments should describe things that aren't obvious from the code** — the reason comments exist is to capture information that was in the developer's mind but cannot be represented in a programming language: boundary-condition semantics, design rationale, ordering constraints, high-level abstractions
- **Developers should understand a module's abstraction without reading its implementation** — the only way to achieve this is through comments that supplement externally visible declarations

## 2. Comment Conventions

- **Adopt and follow a convention** — consistency makes comments easier to read and ensures you actually write them. Use language-specific tools (Javadoc, Doxygen, godoc) when available
- **Four categories of comments:**

| Category | Where it lives | What it describes |
|----------|---------------|-------------------|
| **Interface** | Before a class/method/function declaration | The abstraction: behavior, arguments, return values, side effects, exceptions, preconditions |
| **Data structure member** | Next to a field/variable declaration | What the variable represents, units, invariants, ownership |
| **Implementation** | Inside a method body | How the code works internally (use sparingly) |
| **Cross-module** | Wherever the dependency is most visible | Design decisions that span multiple modules |

- **Comment everything by default** — it's easier to comment every class, method, and class variable than to spend energy deciding which ones "don't need it." Truly obvious declarations (e.g., trivial getters) are rare

## 3. Don't Repeat the Code

- **Same-level-of-detail comments are useless** — if a reader could write the comment just by looking at the code next to it, the comment adds nothing (e.g., `// Add a horizontal scroll bar` next to `new JScrollBar(JScrollBar.HORIZONTAL)`)
- **Don't echo the entity name** — comments that merely rearrange the words from the method/variable name into a sentence provide zero new information

> **Red Flag: Comment Repeats Code** — if the information in a comment is already obvious from the code next to it, the comment isn't helpful. A telltale sign is when the comment uses the same words that make up the name of the entity being described.

- **Use different words** — pick words that provide additional information about the meaning: units, boundary behavior, implications, the "why." For example, instead of `// The horizontal padding`, write `// Blank space on left and right of each text line, in pixels`

## 4. Two Levels of Detail

### 4.1. Lower-Level Comments Add Precision

- **Precision fills in what declarations leave out** — names and types are inherently imprecise. Comments on variables and parameters should clarify:
  - Units (pixels, bytes, seconds)
  - Boundary conditions (inclusive vs. exclusive)
  - Null semantics (what does a null value imply?)
  - Ownership and cleanup responsibility
  - Invariants (e.g., "this list always contains at least one entry")
- **Focus on what the variable represents (nouns), not how it's manipulated (verbs)** — a comment describing what the variable means is shorter, more stable, and more useful than one that mirrors the code paths that set it
- **"The code" means the adjacent code, not the entire application** — a reader should not have to scan all usages of a variable to understand its declaration

### 4.2. Higher-Level Comments Enhance Intuition

- **Abstraction over detail** — implementation comments inside methods should describe the overall intent and structure, not repeat the logic line by line
- **Good example:** `// Try to append the current key hash onto an existing RPC to the desired server that hasn't been sent yet.` — this single sentence explains the purpose of an entire loop; readers can then map individual conditions to that purpose
- **Bad example:** a comment that re-describes each condition in the `if` statement adds nothing a reader can't see
- **Ask three questions:** What is this code trying to do? What is the simplest thing I can say that explains everything here? What is the most important thing about this code?

## 5. Interface Documentation

### 5.1. Class Interface Comments

- **Describe the abstraction, not the implementation** — a class comment should explain what the class does for its users: overall capability, what each instance represents, and any limitations (e.g., single-threaded)
- **Omit internal details** — names of internal RPCs, private configuration parameters, and data structures belong in implementation comments, not in the interface

> **Red Flag: Implementation Documentation Contaminates Interface** — this occurs when interface documentation, such as that for a method, describes implementation details that aren't needed in order to use the thing being documented.

### 5.2. Method Interface Comments

- **What a method comment must cover:**
  - High-level behavior as perceived by the caller (the abstraction)
  - Each argument and return value, with precise constraints and dependencies
  - Side effects (anything that affects future system behavior beyond the return value)
  - Exceptions that can emanate from the method
  - Preconditions that must hold before invocation
- **Shallow-class detector** — if the interface comment must also describe the implementation, the class or method is shallow. Writing comments can therefore serve as a design quality check

## 6. Implementation Comments: What and Why, Not How

- **Most short methods need no implementation comments** — the code plus the interface comment is enough
- **For longer methods, comment each major block** — provide a high-level (more abstract) description of what the block does, not how (e.g., `// Phase 1: Scan active RPCs to see if any have completed`)
- **For loops, describe what each iteration accomplishes** — but only for longer or complex loops where the purpose isn't self-evident
- **Document the "why"** — if code exists because of a tricky edge case or a bug fix, explain the reason. Reference a bug tracker ID instead of duplicating all details
- **Local variables rarely need comments** — good names and small scope are usually sufficient. Add a comment only when the variable is used across a large span of code

## 7. Cross-Module Design Decisions

- **The challenge** — real systems have design decisions (e.g., network protocol rules, error-handling strategies) that affect multiple classes. These are often complex, subtle, and a frequent source of bugs
- **Place docs where they'll be found** — if there's a natural central location (e.g., an enum declaration that every new value must touch), put the cross-module instructions there
- **`designNotes` file approach** — for decisions with no obvious central location, maintain a single file with labeled sections for each cross-module topic. Reference it from each relevant piece of code with a short pointer comment (e.g., `// See "Zombies" in designNotes`). Trade-off: single source of truth, but the documentation is distant from the code it describes
- **"Obvious" is from the reader's perspective** — if a code reviewer says something is not obvious, it is not obvious. Don't argue; clarify with better comments or better code
