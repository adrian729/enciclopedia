# Ch 21: Java

## Table of Contents

- [1. Framing](#1-framing)
- [2. How to approach Java questions](#2-how-to-approach-java-questions)
- [3. final keyword](#3-final-keyword)
- [4. finally keyword](#4-finally-keyword)
- [5. finalize method](#5-finalize-method)
- [6. Overloading vs. Overriding](#6-overloading-vs-overriding)
- [7. Collection Framework](#7-collection-framework)

## 1. Framing

- **This chapter is about language and syntax questions** — distinct from the Java-implemented algorithm problems elsewhere in the book.
- **Less common at bigger companies** — they prefer testing aptitude over language trivia and have resources to train on a specific language. More common at other companies.

## 2. How to approach Java questions

- **Best preparation is learning Java inside and out** — but if stumped, a structured fallback approach exists.
- **Three-step fallback**:
  1. **Create an example of the scenario** and ask how things should play out.
  2. **Ask how other languages would handle the scenario.**
  3. **Consider how you'd design this situation** as the language designer — what are the implications of each choice?
- **Derivation beats recall** — an interviewer may be equally or more impressed if you derive the answer than if you knew it automatically. Don't bluff; say "I'm not sure I can recall the answer, but let me see if I can figure it out."

## 3. final keyword

Meaning depends on what `final` is applied to:

| Applied to | Meaning |
|------------|---------|
| **Variable** | The value cannot be changed once initialized. |
| **Method** | The method cannot be overridden by a subclass. |
| **Class** | The class cannot be subclassed. |

## 4. finally keyword

- **Used with `try`/`catch`** — guarantees a section of code executes even if an exception is thrown.
- **Execution order** — the `finally` block runs after `try` and `catch` blocks, but **before control transfers back to its origin** (e.g., before the function's `return` actually returns).
- **`catch` with return + finally** — in the chapter's traced example, the `catch` block executes fully (including its own function call inside the `return` statement), then `finally` runs, then the function actually returns. Output sequence illustrates this: `start bar`, `start try`, `catch`, `lem`, `finally`, `return from lem | returned from catch`, `end bar`.

## 5. finalize method

- **Called by the garbage collector** just before destroying an object.
- **Overridable** from the `Object` class to define custom behavior during garbage collection (e.g., close open files, release resources).
- **Signature** — `protected void finalize() throws Throwable { ... }`.

## 6. Overloading vs. Overriding

| Term | Definition |
|------|------------|
| **Overloading** | Two methods have the **same name but differ in the type or number of arguments** (e.g., `computeArea(Circle c)` and `computeArea(Square s)`). |
| **Overriding** | A method shares the **same name and function signature** as another method in its superclass. |

- **Worked example** — abstract `Shape` with `printMe()` and abstract `computeArea()`; `Circle extends Shape` overrides both; `Ambiguous extends Shape` overrides only `computeArea()`. Iterating over a `Shape[]` of a `Circle` and an `Ambiguous` prints:
  - `I am a circle.` / `78.75` — `Circle` overrode `printMe()`.
  - `I am a shape.` / `10.0` — `Ambiguous` left `printMe()` as-is.

## 7. Collection Framework

- **Widely used throughout the book** — be very comfortable with the syntax below before an interview.

| Class | Purpose | Notes |
|-------|---------|-------|
| **ArrayList** | Dynamically resizing array that grows as you insert elements. | `ArrayList<String> myArr = new ArrayList<String>(); myArr.add("one");` |
| **Vector** | Very similar to an `ArrayList`, except that it is **synchronized**. Syntax is almost identical. | `Vector<String> myVect = new Vector<String>();` |
| **LinkedList** | Java's built-in linked list class. Rarely comes up in interviews, but useful to study for its **iterator syntax**. | `Iterator<String> iter = myLinkedList.iterator(); while (iter.hasNext()) { ... }` |
| **HashMap** | Widely used in interviews and in the real world. | `HashMap<String, String> map = new HashMap<String, String>(); map.put("one", "uno");` |
