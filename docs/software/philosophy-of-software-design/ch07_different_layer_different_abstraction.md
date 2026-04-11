# Ch 7: Different Layer, Different Abstraction

## Table of Contents

- [1. The Core Principle](#1-the-core-principle)
- [2. Pass-Through Methods](#2-pass-through-methods)
  - [2.1. When Interface Duplication Is OK](#21-when-interface-duplication-is-ok)
- [3. Decorators](#3-decorators)
- [4. Interface vs. Implementation](#4-interface-vs-implementation)
- [5. Pass-Through Variables](#5-pass-through-variables)
  - [5.1. The Context Object Solution](#51-the-context-object-solution)

## 1. The Core Principle

- **Different abstraction at each layer** — in a well-designed system, each layer provides a different abstraction from the layers above and below it; following a single operation through the stack, the abstraction changes at every method call
- **File system example** — top layer: variable-length byte arrays (files); middle layer: fixed-size cached disk blocks; bottom layer: device drivers moving blocks between storage and memory
- **TCP example** — top layer: a reliable byte stream between machines; bottom layer: bounded-size packets delivered on a best-effort basis, some lost or reordered
- **Adjacent layers with similar abstractions = red flag** — it suggests the class decomposition is wrong and that infrastructure is adding complexity without contributing enough functionality to justify it

## 2. Pass-Through Methods

- **Pass-through method** — a method that does little except invoke another method whose signature is similar or identical; it contributes no new functionality
- **Why they're harmful** — they make classes shallower (more interface complexity, no extra capability), create tight coupling between classes (signature changes cascade), and signal confused responsibility boundaries

> **Red Flag: Pass-Through Method** — a method that does nothing except pass its arguments to another method, usually with the same API as the pass-through method. This typically indicates that there is not a clean division of responsibility between the classes.

- **Diagnosis** — ask "exactly which features and abstractions is each class responsible for?" You will usually find overlapping responsibilities
- **Three fixes:**

| Approach | How it works |
|----------|-------------|
| **Expose the lower class directly** | Remove the higher-level class from the call path; callers use the lower class |
| **Redistribute functionality** | Move methods between the two classes so each has a distinct, coherent set of responsibilities |
| **Merge the classes** | If responsibilities can't be disentangled, combine both classes into one |

### 2.1. When Interface Duplication Is OK

- **Dispatchers** — a method that uses its arguments to select one of several other methods to invoke; the signatures match, but the dispatcher provides real functionality (choosing which method handles the task), e.g., a web server routing URLs to handlers
- **Multiple implementations of the same interface** — e.g., different disk drivers in an OS all share the same interface; each provides distinct functionality, reduces cognitive load (learn one interface, use many), and the methods don't invoke each other

## 3. Decorators

- **Decorator (wrapper) pattern** — an object that takes an existing object, provides a similar or identical API, and extends its functionality by delegating to the underlying object's methods
- **Tendency toward shallowness** — decorators introduce a large amount of boilerplate for a small amount of new functionality; they often consist mostly of pass-through methods
- **Overuse risk** — creating a new decorator class for every small feature leads to an explosion of shallow classes (e.g., Java I/O)
- **Alternatives to consider before creating a decorator:**

| Alternative | When it applies |
|-------------|----------------|
| **Add to the underlying class** | The new feature is general-purpose, logically related, or almost always used with the base class (e.g., buffering belongs inside `InputStream`) |
| **Merge with the use case** | The new feature is specialized for one particular use |
| **Merge with an existing decorator** | Produces one deeper decorator instead of multiple shallow ones |
| **Implement as an independent class** | The feature doesn't truly need to wrap the base class (e.g., scrollbars could exist independently of the window) |

## 4. Interface vs. Implementation

- **Interface should differ from implementation** — if the external abstraction closely mirrors the internal representation, the class probably isn't very deep
- **Text editor example** — storing text internally as lines is fine, but exposing a line-oriented API (`getLine`, `putLine`) forces callers to split and join lines for common operations like mid-line insertion or cross-line deletion
- **Character-oriented API is deeper** — `insert(string, position)` and `delete(start, end)` hide the complexity of line splitting/joining inside the text class, making higher-level code much simpler
- **The gap between interface and implementation = the value the class provides** — a wide gap means the class is doing significant work on behalf of its callers

## 5. Pass-Through Variables

- **Pass-through variable** — a variable passed down through a long chain of methods where only a deeply nested method actually uses it; every intermediate method must carry it in its signature
- **Why they're harmful** — intermediate methods must be aware of the variable without benefiting from it, and adding a new pass-through variable requires modifying many signatures across the call chain

| Solution | Trade-off |
|----------|-----------|
| **Shared object** | Store the data in an object already accessible to both the top-level and bottom-level method; but that object may itself be a pass-through variable |
| **Global variable** | Avoids passing data through methods, but prevents running multiple system instances in one process and complicates testing |
| **Context object** | Best general-purpose solution (see below) |

### 5.1. The Context Object Solution

- **Context object** — a single object that holds all application-wide global state (configuration, shared subsystems, performance counters, etc.), one per system instance
- **How it's threaded** — stored as an instance variable in major objects; passed explicitly only in constructors, not through every method call
- **Benefits** — supports multiple system instances in one process, centralizes global state, simplifies testing (tests can swap the context), and adding new global state requires changing only the context constructor/destructor
- **Drawbacks** — variables in the context share the downsides of globals (unclear provenance, non-obvious dependencies); without discipline, the context becomes a grab-bag; thread safety requires care (prefer immutable context variables)
