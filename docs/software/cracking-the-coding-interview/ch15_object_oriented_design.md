# Ch 15: Object-Oriented Design

## Table of Contents

- [1. What OOD questions test](#1-what-ood-questions-test)
- [2. Four-step approach](#2-four-step-approach)
- [3. Design patterns in scope](#3-design-patterns-in-scope)
- [4. Singleton pattern](#4-singleton-pattern)
- [5. Factory Method pattern](#5-factory-method-pattern)

## 1. What OOD questions test

- **Sketch classes and methods** — OOD questions ask the candidate to lay out the classes and methods to implement a technical problem or a real-life object (e.g. a coffee maker, a restaurant).
- **Insight into coding style** — these questions are believed to reveal how the candidate writes elegant, maintainable code, not whether they can recite design patterns.
- **Red flag on poor answers** — poor performance on this type of question may raise serious red flags.

## 2. Four-step approach

A single approach works whether the target is a physical item or a technical task.

| Step | Purpose |
|------|---------|
| **1. Handle Ambiguity** | Resolve vagueness by asking clarifying questions |
| **2. Define the Core Objects** | Identify the main entities in the system |
| **3. Analyze Relationships** | Work out how those objects relate to each other |
| **4. Investigate Actions** | Trace the key behaviors and refine the design |

### 2.1. Step 1: Handle Ambiguity

- **OOD questions are intentionally vague** to test whether the candidate will ask clarifying questions; a developer who builds without clarifying wastes company time and money.
- **Ask who will use it and how.** Optionally walk through the **"six Ws"**: who, what, where, when, how, why.
- **Example — coffee maker** — "industrial machine serving hundreds of customers with ten product types" vs. "simple machine for the elderly making only black coffee" produce radically different designs.

### 2.2. Step 2: Define the Core Objects

- **List the main entities.** Example — a restaurant's core objects might be `Table`, `Guest`, `Party`, `Order`, `Meal`, `Employee`, `Server`, `Host`.

### 2.3. Step 3: Analyze Relationships

Work out membership, inheritance, and cardinality (many-to-many vs. one-to-many).

Example relationships for the restaurant:

- `Party` should have an array of `Guests`.
- `Server` and `Host` inherit from `Employee`.
- Each `Table` has one `Party`, but each `Party` may have multiple `Tables`.
- There is one `Host` for the `Restaurant`.

**Watch for incorrect assumptions** — e.g. a `Table` might actually serve multiple `Parties` at "communal tables"; talk to the interviewer about how general-purpose the design should be.

### 2.4. Step 4: Investigate Actions

- **Trace key actions** to refine the design; you may realize some objects are missing and need to update the design.
- **Example flow** — a `Party` walks into the `Restaurant`, a `Guest` requests a `Table` from the `Host`; the `Host` looks up the `Reservation` and assigns a `Table` if one exists, else appends the `Party` to the end of the list; when a `Party` leaves, the `Table` is freed and assigned to a new `Party` in the list.

## 3. Design patterns in scope

- **Interviews test capabilities, not knowledge** — so design patterns are mostly out of scope for an interview.
- **Two patterns worth knowing** — **Singleton** and **Factory Method** are especially useful for interviews.
- **Further learning** — the book recommends picking up a dedicated design patterns book to go deeper.

## 4. Singleton pattern

- **Purpose** — ensures a class has only one instance and provides a single access point to it. Useful for a "global" object that must exist exactly once (e.g. a `Restaurant`).
- **Typical implementation** — a `private static` instance field plus a `public static getInstance()` method that lazy-initializes the instance on first call:

```java
public class Restaurant {
    private static Restaurant _instance = null;
    public static Restaurant getInstance() {
        if (_instance == null) {
            _instance = new Restaurant();
        }
        return _instance;
    }
}
```

## 5. Factory Method pattern

- **Purpose** — offers an interface for creating an instance of a class, with its subclasses deciding which class to instantiate.
- **Two implementation styles** —
  - **Abstract Creator** — Creator class is abstract and does not implement the Factory method; subclasses implement it.
  - **Concrete Creator with type parameter** — Creator is a concrete class whose Factory method takes a parameter indicating which class to instantiate.
- **Example** — `CardGame.createCardGame(GameType type)` returns a `PokerGame` for `GameType.Poker`, a `BlackJackGame` for `GameType.BlackJack`:

```java
public class CardGame {
    public static CardGame createCardGame(GameType type) {
        if (type == GameType.Poker) {
            return new PokerGame();
        } else if (type == GameType.BlackJack) {
            return new BlackJackGame();
        }
        return null;
    }
}
```
