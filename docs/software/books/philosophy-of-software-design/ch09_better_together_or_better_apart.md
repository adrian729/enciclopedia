# Ch 9: Better Together Or Better Apart?

## Table of Contents

- [1. The Fundamental Question](#1-the-fundamental-question)
- [2. Costs of Subdivision](#2-costs-of-subdivision)
- [3. Indicators That Code Belongs Together](#3-indicators-that-code-belongs-together)
- [4. Bring Together: Shared Information](#4-bring-together-shared-information)
- [5. Bring Together: Simpler Interface](#5-bring-together-simpler-interface)
- [6. Bring Together: Eliminate Duplication](#6-bring-together-eliminate-duplication)
- [7. Separate General-Purpose From Special-Purpose](#7-separate-general-purpose-from-special-purpose)
- [8. Example: Cursor and Selection](#8-example-cursor-and-selection)
- [9. Example: Separate Logging Class](#9-example-separate-logging-class)
- [10. Example: Editor Undo Mechanism](#10-example-editor-undo-mechanism)
- [11. Splitting and Joining Methods](#11-splitting-and-joining-methods)
- [12. A Different Opinion: Clean Code](#12-a-different-opinion-clean-code)

## 1. The Fundamental Question

- **Together or apart?** — given two pieces of functionality, should they live in the same place or be separated? This applies at every level: functions, methods, classes, and services
- **Goal** — reduce overall system complexity and improve modularity; the answer is whichever structure achieves that

## 2. Costs of Subdivision

- **More components = harder to track** — each subdivision adds interfaces, and every new interface adds complexity
- **Management overhead** — code that used one object now may need to manage several
- **Separation harms visibility** — related code ends up farther apart (different methods, classes, or files), making it harder to see together; if the pieces are truly independent this is fine, but if there are dependencies, developers end up flipping back and forth or, worse, not realizing dependencies exist
- **Duplication** — code that existed once may need to be replicated in each subdivided component

## 3. Indicators That Code Belongs Together

| Signal | Meaning |
|--------|---------|
| **Shared information** | Both pieces depend on the same knowledge (e.g., the syntax of a document format) |
| **Used together** | Anyone using one piece is likely to use the other (must be bidirectional to be compelling) |
| **Conceptual overlap** | Both fall under a simple higher-level category (e.g., "string manipulation", "network communication") |
| **Hard to understand alone** | You can't understand one piece without looking at the other |

## 4. Bring Together: Shared Information

- **HTTP server example** — reading a request from a socket and parsing it were in separate classes, but both needed detailed knowledge of the HTTP format (e.g., the reader had to parse headers to find the content length). Combining them removed duplicated knowledge and made the code shorter and simpler

## 5. Bring Together: Simpler Interface

- **Combining removes intermediate interfaces** — when modules each implement part of a solution, merging them eliminates the glue interfaces between them
- **Automatic behavior** — combining can let features work by default. If `FileInputStream` and `BufferedInputStream` were one class with buffering on by default, most users would never need to know buffering exists

## 6. Bring Together: Eliminate Duplication

> **Red Flag: Repetition** — if the same piece of code (or code that is almost the same) appears over and over again, that's a red flag that you haven't found the right abstractions.

- **Factor into a method** — extract the repeated snippet into a shared method; most effective when the snippet is long and the method's signature is simple
- **Restructure so it runs once** — reorganize control flow so the duplicated logic executes in only one place (e.g., use `goto` to a shared cleanup block at the end of a function for multiple error-return points)

## 7. Separate General-Purpose From Special-Purpose

- **General-purpose mechanisms should stand alone** — don't embed use-case-specific code in a general-purpose module; it creates information leakage and couples the mechanism to one caller
- **Pull special-purpose code upward** — lower layers should be general-purpose; upper layers specialize. If a class mixes both, split it into a general-purpose base and a special-purpose layer on top

> **Red Flag: Special-General Mixture** — when a general-purpose mechanism also contains code specialized for a particular use of that mechanism. This makes the mechanism more complicated and creates information leakage between the mechanism and the particular use case: future modifications to the use case are likely to require changes to the underlying mechanism as well.

- **Nuance** — "separate general from special" applies within the same mechanism. It is fine to combine special-purpose code for one mechanism with general-purpose code for another (e.g., the text class is a general-purpose text mechanism but contains special-purpose undo code for text modifications, because that code is closely related to text operations)

## 8. Example: Cursor and Selection

- **Tempting to combine** — the insertion cursor always sits at one end of the selection, and they are often manipulated together (click-drag sets both; text insertion deletes selection then inserts at cursor)
- **Combined object was worse** — higher-level code still needed to treat cursor and selection as distinct entities; the combined object was harder to implement (stored a boolean for "which end is the cursor" instead of a direct position)
- **Separated objects were simpler** — a general-purpose `Position` class (line + character) was introduced; selection = two `Positions`, cursor = one `Position`. Both usage and implementation became cleaner, and `Position` found reuse elsewhere

## 9. Example: Separate Logging Class

- **Separate `NetworkErrorLogger` class added complexity for no benefit** — each logging method was shallow (one line of code, heavy documentation), called from only one place, and tightly coupled to its call site (readers had to flip between the two)
- **Better: inline the log statement** — placing the logging directly at the error site removes an unnecessary interface and keeps related information together

## 10. Example: Editor Undo Mechanism

- **Problem with undo in the text class** — students put the entire undo mechanism (general-purpose history management + special-purpose handlers for text, selection, cursor) inside the text class; this caused information leakage, awkward cross-module callbacks, and made adding new undoable entities require changes to the text class
- **Better design: separate `History` class** — a general-purpose `History` class manages a list of `Action` objects (each with `undo()`/`redo()` methods) and knows nothing about what the actions do

| Responsibility | Where it lives |
|---------------|---------------|
| **General undo mechanism** (manage action list, walk it during undo/redo) | `History` class |
| **Specific action logic** (what to undo/redo for text, selection, cursor) | Action subclasses in the relevant modules |
| **Grouping policy** (which actions form one user-level undo step) | High-level UI code, using `History.addFence()` |

- **Key insight** — separating general-purpose undo infrastructure from special-purpose action handlers let each part be understood and extended independently

## 11. Splitting and Joining Methods

- **Length alone is not a reason to split** — methods containing hundreds of lines of code are fine if they have a simple signature and are easy to read; splitting them into small pieces adds interfaces and separates related code
- **Don't split too eagerly** — developers tend to over-subdivide methods; each split adds an interface and scatters related logic

> **Red Flag: Conjoined Methods** — it should be possible to understand each method independently. If you can't understand the implementation of one method without also understanding the implementation of another, that's a red flag.

- **Two valid reasons to split a method:**

| Split type | When it makes sense |
|-----------|-------------------|
| **Extract a subtask** (parent calls child) | The subtask is cleanly separable, general-purpose, and the parent doesn't need to know the child's implementation (and vice versa) |
| **Divide into peers** (both visible to callers) | The original method had an overly complex interface because it did multiple unrelated things; each resulting method is simpler and most callers need only one of them |

- **When to join methods** — joining can replace two shallow methods with one deep method, eliminate duplication, remove dependencies or intermediate data structures, improve encapsulation, or simplify the interface
- **Decision rule** — pick the structure that results in the best information hiding, the fewest dependencies, and the deepest interfaces

## 12. A Different Opinion: Clean Code

- **Robert Martin's position** — functions should be extremely short; even 10 lines is too long. Blocks within `if`/`else`/`while` should be one line (a function call). Indent level should not exceed one or two
- **Ousterhout's disagreement** — once a function is down to a few dozen lines, further shrinking has little readability benefit. Breaking it up further creates more interfaces, more functions to learn, and conjoined methods that can't be understood independently
- **Depth matters more than length** — make functions deep first, then make them short enough to read easily. Don't sacrifice depth for length
