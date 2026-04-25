# Ch 4: Modules Should Be Deep

## Table of Contents

- [1. Modular Design](#1-modular-design)
- [2. Interfaces: Formal and Informal](#2-interfaces-formal-and-informal)
- [3. Abstractions](#3-abstractions)
- [4. Deep Modules](#4-deep-modules)
- [5. Shallow Modules](#5-shallow-modules)
- [6. Classitis](#6-classitis)
- [7. Java and Unix I/O Compared](#7-java-and-unix-io-compared)

## 1. Modular Design

- **Modular design** — decomposing a system into relatively independent modules (classes, subsystems, services) so that developers only face a small fraction of the total complexity at a time
- **Independence is ideal but unattainable** — modules must call each other, creating dependencies. The goal is to minimize those dependencies, not eliminate them
- **Interface vs. implementation** — every module has an interface (what it does) and an implementation (how it does it). Developers using a module should only need to know its interface, not its implementation
- **Best modules** — those whose interfaces are much simpler than their implementations. A simple interface minimizes the complexity imposed on the rest of the system and allows the implementation to change without affecting other modules

## 2. Interfaces: Formal and Informal

- **Formal interface** — the parts explicitly specified in code and enforced by the language: method signatures, parameter types, return types, exceptions, public variables
- **Informal interface** — high-level behavior, usage constraints, side effects, ordering requirements. Can only be communicated through comments/documentation and cannot be compiler-checked
- **Informal parts are usually larger** — for most interfaces, the informal aspects (behavioral contracts, preconditions) are more complex than the formal aspects (type signatures)
- **Clear interfaces eliminate unknown unknowns** — a well-specified interface tells developers exactly what they need to know, reducing the chance they'll miss something critical

## 3. Abstractions

- **Abstraction** — a simplified view of an entity that omits unimportant details, making it easier to reason about complex things
- **Each module's interface is an abstraction** — it presents the module's functionality while hiding implementation details
- **Too much detail** — including unnecessary detail in an abstraction increases cognitive load without adding value
- **Too little detail (false abstraction)** — omitting details that users actually need creates obscurity; the abstraction appears simple but is misleading because callers must look behind it to use it correctly
- **The key design skill** — understanding what is truly important and minimizing the amount of information that callers need to know

## 4. Deep Modules

- **Deep module** — provides powerful functionality behind a simple interface. Visualized as a rectangle: narrow top edge (simple interface), large area (lots of functionality)
- **Cost vs. benefit** — a module's interface is its cost (complexity imposed on the system); its functionality is its benefit. Deep modules maximize benefit while minimizing cost
- **Unix I/O as the canonical example** — five system calls (`open`, `read`, `write`, `lseek`, `close`) hide hundreds of thousands of lines of implementation dealing with disk layout, caching, permissions, scheduling, and multiple device types. The interface has remained stable for decades while implementations evolved radically
- **Garbage collection** — a deep module with effectively no interface at all. It works invisibly, actually shrinking the system's total interface by eliminating the need for manual memory-freeing APIs

## 5. Shallow Modules

- **Shallow module** — its interface is complex relative to the functionality it provides, so it doesn't hide much complexity. Example: a linked-list class whose interface is nearly as complex as its implementation
- **Extreme example** — a method like `addNullValueForAttribute(String attribute)` that simply calls `data.put(attribute, null)`. The method offers no abstraction (callers still need to know about `data`), the documentation is longer than the code, and invoking it takes more keystrokes than doing the operation directly

> **Red Flag: Shallow Module** — a module whose interface is complicated relative to the functionality it provides. The benefit of not learning internals is negated by the cost of learning the interface. Small modules tend to be shallow.

## 6. Classitis

- **Classitis** — the mistaken belief that "classes are good, so more classes are better," leading to systems with many tiny, shallow classes
- **Root cause** — conventional wisdom that classes should be small and methods should be short (e.g., "nothing longer than N lines"). This advice optimizes for the wrong metric
- **System-level harm** — individually simple classes accumulate a large number of interfaces, creating tremendous complexity at the system level. Each class contributes little functionality, and boilerplate code inflates the codebase

## 7. Java and Unix I/O Compared

| Aspect | Java I/O (classitis) | Unix I/O (deep) |
|--------|---------------------|-----------------|
| **Opening a file** | Requires creating three separate objects (`FileInputStream`, `BufferedInputStream`, `ObjectInputStream`) | Single `open()` call returns a file descriptor |
| **Buffering** | Must be explicitly requested via a separate class; forgetting it causes silent performance bugs | (Not discussed at the syscall level) |
| **Sequential access** | No special default | Made the default; random access available via `lseek` but you don't need to know about it unless you need it |
| **Design philosophy** | Exposes every option as a separate class, forcing users to learn rarely-needed features | Makes the common case simple; rarely-needed features exist but don't increase cognitive load for typical use |

- **Design the common case to be simple** — if almost everyone needs buffering, provide it by default. Offer a way to disable it for rare cases, but keep that mechanism separate so most users never encounter it
- **Effective complexity** — if an interface has many features but most developers only use a few, the real complexity is just the commonly used subset
