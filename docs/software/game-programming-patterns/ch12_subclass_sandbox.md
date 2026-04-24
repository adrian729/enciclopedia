# Ch 12: Subclass Sandbox

## Table of Contents

- [1. The Problem](#1-the-problem)
- [2. The Pattern](#2-the-pattern)
- [3. When to Use It](#3-when-to-use-it)
- [4. Design Decisions](#4-design-decisions)
- [5. Keep in Mind](#5-keep-in-mind)

## 1. The Problem

- **Many subclasses, each touching everything** — e.g., a superhero game with hundreds of `Superpower` subclasses. They'll play sounds, spawn effects, move entities, poke physics, talk to AI. Every corner of the engine is fair game
- **Four consequences when each subclass is free to call into the engine directly**:
  - **Redundant code** — a freeze ray, heat ray, and Dijon mustard ray all overlap. Uncoordinated authors duplicate work
  - **Pervasive coupling** — gameplay subclasses dig into internal rendering layers never meant to be exposed; every engine subsystem ends up linked to every power
  - **Brittle under change** — whenever an engine subsystem changes, random superpower code breaks. Graphics and audio programmers shouldn't also have to be gameplay programmers
  - **No invariants** — if every power calls the sound engine directly, there's no single place to enforce queueing or prioritization
- **Goal** — give each gameplay author a curated toolkit of primitives, not raw access to the engine

## 2. The Pattern

- **A base class defines an abstract sandbox method and several provided operations**
- **The sandbox method** — `protected virtual` and abstract. Subclasses must override it; this is where their behavior goes
- **The provided operations** — `protected` (often non-virtual) methods on the base class that the sandbox method calls to get things done. `protected` signals "for subclasses only"
- **To create a new subclass**: inherit from the base, override the sandbox method, implement it by calling the provided operations
- **Result**: a shallow, wide class hierarchy — one base with many direct subclasses. Coupling to the engine lives in one place (the base), and the numerous subclasses couple only to the base

## 3. When to Use It

- **A very common pattern** — often lurking unnoticed. If you have a `protected` non-virtual method, you're probably already doing something like this
- **Good fit when**:
  - You have a base class with a number of derived classes
  - The base class can provide all the operations a derived class may need
  - There's behavioral overlap between subclasses you'd like to share
  - You want to minimize coupling between derived classes and the rest of the program

## 4. Design Decisions

### 4.1. What operations should be provided?

- **Minimal end** — base class provides nothing; subclass calls the outside world directly. Barely counts as using the pattern
- **Maximal end** — base class provides every operation a subclass could need. Subclass source files `#include` only the base class
- **The tradeoff** — more provided operations means less subclass coupling but a fatter base class. You're centralizing coupling, not eliminating it
- **Rules of thumb**:
  - An operation used by only one or two subclasses adds complexity for everyone and benefits few — may not be worth it
  - Operations that don't modify state are "safer" to let subclasses call directly (but beware multi-threading and deterministic online games)
  - State-modifying calls are better wrapped as provided operations — the coupling is more visible
  - A pure-forwarding operation (one line to an engine call) looks useless, but can still earn its keep by encapsulating a private field the subclass shouldn't touch

### 4.2. Provide methods directly, or via helper objects?

- **Problem**: the base class accrues methods and bloats
- **Solution**: move groups of related methods to helper classes (e.g., `SoundPlayer`), and have the base class expose a getter for them
- **Wins**:
  - Fewer methods in the base class
  - Helper-class code is easier to maintain than core base-class code
  - Coupling narrows — the base class depends on `SoundPlayer`, not on every audio detail

### 4.3. How does the base class get the state it needs?

| Approach | Upside | Downside |
|---|---|---|
| Pass to base constructor | Guaranteed initialization | Every derived class has to forward the argument; private state leaks into subclass constructors |
| Two-stage init (constructor + `init`) | Derived classes don't see the state | Easy to forget the `init` call — wrap in a factory function to prevent that |
| Make the state static | No per-instance memory; one `init` for the whole class | Shares singleton's problems — shared mutable state across all instances |
| Service Locator | Base pulls what it needs on demand | Adds a service-locator dependency |

## 5. Keep in Mind

- **Base classes accrete code** — this pattern is especially prone to it. The base ends up coupled to every system any subclass needs, and subclasses are intimately tied to the base. That spiderweb makes changing the base risky — the **brittle base class problem**
- **Flip side**: most coupling has moved up into the base, so the subclasses themselves are cleanly isolated. That's where most of your behavior lives, so the bulk of the codebase becomes easier to maintain
- **If the base turns into a "giant bowl of code stew"** — pull provided operations into separate classes the base can delegate to. The **Component** pattern can help
- **A data-driven alternative** — when subclasses proliferate, consider encoding their behavior in data instead (**Type Object**, **Bytecode**, **Interpreter GoF**). Subclass Sandbox fits better when behavior is genuinely complex and imperative
- **See also**:
  - The **Update Method** pattern's `update()` is often also a sandbox method
  - **Template Method GoF** is the role reversal — there, the derived class provides primitives and the base class provides the high-level method; here it's the opposite
  - Can be seen as a variation of **Facade GoF** — the base class acts as a facade hiding the engine from its subclasses
