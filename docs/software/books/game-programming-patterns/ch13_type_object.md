# Ch 13: Type Object

## Table of Contents

- [1. The Problem](#1-the-problem)
- [2. The Pattern](#2-the-pattern)
- [3. When to Use It](#3-when-to-use-it)
- [4. Implementation Notes](#4-implementation-notes)
- [5. Design Decisions](#5-design-decisions)
- [6. Keep in Mind](#6-keep-in-mind)

## 1. The Problem

- **Conceptual kinds versus compiled classes** — a fantasy RPG has many **monster breeds** (dragon, troll, etc.). Each breed fixes starting health and an attack string; many monster instances share a breed
- **The typical OOP answer: subclass per breed** — `Monster` base class with `Dragon`, `Troll`, etc. as subclasses. Each overrides `getAttack()` and passes starting health up to the base constructor
- **Why this breaks down at scale**:
  - Designers want hundreds of breeds; programmers end up writing seven-line subclasses all day
  - Tuning is painful — "change troll health from 48 to 52" turns into a checkout, edit, recompile, check-in cycle
  - Programmers become data monkeys; designers wait on programmers for trivial tweaks
- **What we actually want** — designers creating and tuning breeds without any programmer in the loop, no recompile required

## 2. The Pattern

- **Define a type object class and a typed object class** — e.g., `Breed` and `Monster`. Two classes, no inheritance between breeds
- **Each type object instance represents a different logical type** — one `Breed` instance for "dragon", another for "troll"
- **Each typed object stores a reference to its type object** — each `Monster` holds a `Breed&`. Calls like `getAttack()` forward to the breed
- **Instance-specific data lives in the typed object; shared data/behavior lives in the type object** — current health on the monster, starting health and attack string on the breed
- **Objects referencing the same type object function as if they were the same type** — share behavior like subclassing does, but without baking the types into the class hierarchy
- **New types are just new instances** — instantiate more `Breed` objects, populate from a config file, and you have hundreds of monster kinds defined in data

## 3. When to Use It

- **Use when you need a variety of "kinds" of things** but baking them into the language's type system is too rigid
- **Particularly good when**:
  - You don't know what types you'll need up front (e.g., supporting downloadable content that adds new breeds)
  - You want to modify or add types without recompiling

## 4. Implementation Notes

- **Minimal implementation**: `Breed` holds `health` and `attack` with getters; `Monster` takes a `Breed&` in its constructor, uses it to seed current health, and forwards `getAttack()` to the breed. That's the core of the pattern — everything else is bonus
- **Vtables are Type Object applied to C by the compiler** — a C++ vtable is the breed object; the vtable pointer is the monster's breed reference. You're re-implementing what the compiler does, by hand, at runtime
- **Factory method for construction** — give `Breed` a `newMonster()` method and make `Monster`'s constructor private (with `Breed` as a friend). Calling `someBreed.newMonster()` lets the breed control allocation (custom allocators, object pools) in addition to initialization
- **Sharing attributes via inheritance among type objects**:
  - Give each `Breed` a pointer to a parent breed
  - Define override semantics (e.g., non-zero health overrides; non-null attack string overrides)
  - **Dynamic delegation** — check override at every access; walks the chain each lookup. Slower but respects runtime changes to the hierarchy
  - **Copy-down delegation** — at construction, copy any non-overridden attributes from parent into the child. Fast lookups (just return the field), can drop the parent pointer afterward, but changes to the parent post-construction don't propagate
- **Data file example** — a JSON file defining "Troll", "Troll Archer" (parent: "Troll"), "Troll Wizard" (parent: "Troll"). Zero health on the children inherits from Troll, so tuning Troll tunes all three

## 5. Design Decisions

### 5.1. Is the type object encapsulated or exposed?

- **Encapsulated** (Monster doesn't expose its `Breed`):
  - Hides the pattern's complexity — just an implementation detail of `Monster`
  - Lets the typed object selectively override — e.g., return `"The monster flails weakly"` when health is low, else forward to the breed
  - Requires tedious forwarding methods for everything the breed exposes
- **Exposed** (Monster returns its `Breed`):
  - Outside code can interact with breeds without needing a monster (e.g., calling `breed.newMonster()`)
  - Widens the public API — narrower interfaces are generally easier to maintain

### 5.2. How are typed objects created?

- **Construct the object and pass in its type** — caller controls allocation (stack, pool, custom allocator)
- **Call a "constructor" function on the type object** — type controls allocation, useful for enforcing pool allocation or similar invariants

### 5.3. Can the type change?

- **Fixed type**:
  - Simpler to code and understand — people don't expect "type" to mutate
  - Easier to debug — current breed is the original breed
- **Mutable type** — e.g., monster dies and becomes a zombie breed instead of spawning a fresh zombie:
  - Less object churn — a simple assignment replaces copy/create/delete
  - Must validate assumptions — the existing instance state must be valid under the new type (e.g., current health not exceeding new starting health)

### 5.4. What kind of inheritance is supported?

| Inheritance | Verdict |
|---|---|
| None | Simple; but designers always end up wanting some kind of sharing |
| Single | Sweet spot — easy to implement, easy for non-programmers to reason about. Lookup may walk a chain |
| Multiple | Avoids nearly all duplication in theory; in practice hard to understand and reason about ("Zombie Dragon" — whose attributes win?). Many C++ standards ban it; Java and C# lack it |

## 6. Keep in Mind

- **Type objects have to be tracked manually** — the compiler no longer handles bookkeeping. You're responsible for instantiating breeds, keeping them alive as long as monsters need them, and wiring each monster to a valid breed. Freedom from the compiler comes with the cost of re-implementing what it used to do
- **Harder to define per-type behavior** — overriding a method is replaced by storing a member variable. Great for type-specific data, hard for type-specific behavior. Workarounds:
  - A fixed set of pre-defined behaviors selected by an enum or function pointer in the type object (at which point you're reinventing vtables)
  - Push behavior fully into data with **Interpreter GoF** or **Bytecode**
- **Data-driven trend** — games are limited more by content-authoring throughput than hardware; higher-level/data-driven behavior trades runtime efficiency for designer productivity, and the trade keeps getting more favorable
- **See also**:
  - **Prototype GoF** — addresses the same data-and-behavior-sharing problem differently
  - **Flyweight GoF** — cousin pattern that shares data across instances, but focused on memory savings rather than modeling conceptual "types"
  - **State GoF** — also delegates part of an object's identity. Type Object delegates what the object *is* (invariant); State delegates what it *is right now* (temporal). An object that changes its type object is essentially using Type Object and State together
