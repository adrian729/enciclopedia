# Ch 6: General-Purpose Modules are Deeper

## Table of Contents

- [1. The Spectrum: General vs. Special-Purpose](#1-the-spectrum-general-vs-special-purpose)
- [2. Somewhat General-Purpose](#2-somewhat-general-purpose)
- [3. Text Editor Example](#3-text-editor-example)
  - [3.1. Special-Purpose API](#31-special-purpose-api)
  - [3.2. General-Purpose API](#32-general-purpose-api)
- [4. Generality Leads to Better Information Hiding](#4-generality-leads-to-better-information-hiding)
- [5. Questions to Find the Right Balance](#5-questions-to-find-the-right-balance)
- [6. Push Specialization Upwards (and Downwards)](#6-push-specialization-upwards-and-downwards)
- [7. Example: Editor Undo Mechanism](#7-example-editor-undo-mechanism)
- [8. Eliminate Special Cases in Code](#8-eliminate-special-cases-in-code)

## 1. The Spectrum: General vs. Special-Purpose

- **Over-specialization may be the single greatest cause of complexity in software** — the 2nd edition elevates this to a central thesis: code that is more general-purpose is simpler, cleaner, and easier to understand
- **General-purpose argument** — build a broad mechanism that handles many problems, not just today's. Consistent with the investment mindset (Ch 3), potentially saving future effort
- **Special-purpose argument** — focus on today's needs, avoid speculative features you may never use, refactor later if needed. Consistent with incremental development
- **Both extremes have risks** — too general may include unused facilities and not do a good job of solving today's problem; too special means building just what you need today, but it may require rework when needs change

## 2. Somewhat General-Purpose

- **Sweet spot** — implement the module's *functionality* for your current needs, but design its *interface* to be general enough to support multiple uses
- **Why it works** — a general-purpose interface is typically simpler and deeper than a special-purpose one. Fewer methods, each covering more use cases, means less cognitive load
- **Secondary benefit** — the module may turn out to be reusable. But even if it is only ever used for its original purpose, the simpler interface alone justifies the approach

## 3. Text Editor Example

### 3.1. Special-Purpose API

- **Scenario** — students building a text editor created text-class methods that mirrored UI operations directly: `backspace(Cursor)`, `delete(Cursor)`, `deleteSelection(Selection)`
- **Problems** — (1) large number of shallow methods, each usable in only one context; (2) information leakage between the UI and text class (UI concepts like `Cursor` and `Selection` polluted the text layer); (3) every new UI feature required a new text-class method, tying the two layers together
- **Result** — high cognitive load (many methods to learn), poor separation of concerns, and no reusability

### 3.2. General-Purpose API

- **Better design** — two methods cover all text modification: `insert(Position, String)` and `delete(Position start, Position end)`, plus a position-manipulation helper `changePosition(Position, int numChars)`
- **Backspace implementation** — `text.delete(text.changePosition(cursor, -1), cursor)` -- slightly more code at the call site, but the behavior is explicit and obvious
- **Advantages** — fewer methods to learn, no UI concepts in the text class, new UI features don't require text-class changes, and the class is reusable for non-editor applications (e.g., find-and-replace tools)
- **Less code overall** — the general-purpose API replaces many special-purpose methods with a few general ones, reducing total code even though individual call sites are slightly longer

## 4. Generality Leads to Better Information Hiding

- **Cleaner separation** — the text class no longer knows about backspace keys, selections, or other UI specifics; those details stay encapsulated in the UI class
- **False abstraction exposed** — the original `backspace` method pretended to hide which characters get deleted, but UI developers needed to know this anyway and would read the implementation to verify. Making the deletion logic explicit at the call site is more honest and more obvious
- **When details matter, make them explicit** — hiding information that callers genuinely need creates obscurity, not simplicity. The right question is *who needs to know what, and when*

## 5. Questions to Find the Right Balance

| Question | What it reveals |
|----------|----------------|
| **What is the simplest interface that covers all my current needs?** | If you can reduce the number of methods without reducing capabilities, you're finding more general-purpose methods. But don't add lots of extra arguments just to merge methods -- that's not truly simpler |
| **In how many situations will this method be used?** | A method designed for one specific use (like `backspace`) is a red flag for over-specialization. Try replacing several single-use methods with one general method |
| **Is this API easy to use for my current needs?** | Guards against over-generalization. If callers need lots of boilerplate or loops to use your "simple" API (e.g., single-character insert/delete), the interface lacks the right level of functionality |

## 6. Push Specialization Upwards (and Downwards)

- **Push specialization upward** — top-level application classes are necessarily specialized (they implement specific features). This specialization should not percolate into lower-level classes. The improved text editor API pushed all UI-specific logic (backspace, selection handling) up into the user interface code, leaving only general-purpose operations in the text class
- **Push specialization downward** — sometimes the best approach is to push specialized code into device-specific or platform-specific modules. OS device drivers are a canonical example: the OS defines a general-purpose interface with operations like "read a block" and "write a block," and each device type has its own specialized driver that implements the interface. The core OS never touches device-specific details
- **Both directions reduce complexity** — whether specialization moves up or down, the goal is the same: keep the middle layers general-purpose so they can be understood and reused without knowledge of specific use cases

## 7. Example: Editor Undo Mechanism

- **Problem** — some student projects implemented the entire undo mechanism inside the text class. The text class maintained a list of all undoable changes and automatically added entries whenever text was modified. For changes to the selection, insertion cursor, and view, the UI code invoked additional text-class methods, which then added their own undo entries. Undo/redo was triggered via the text class, which processed entries internally for text changes and called back to the UI for everything else
- **Why it was awkward** — the text class mixed general-purpose undo/redo infrastructure with special-purpose handlers for text, selection, and cursor. This caused information leakage between the text class and the UI, required extra methods in each module to pass undo information back and forth, and meant adding any new undoable entity would require changes to the text class
- **Better design** — extract the general-purpose undo/redo core into a separate `History` class. It defines an inner interface `History.Action` with `undo()` and `redo()` methods. `History` manages a list of actions and walks backwards/forwards through it in response to user requests, calling `undo` and `redo` on each `Action`. It knows nothing about the actions themselves
- **Special-purpose actions stay separate** — each kind of undoable operation is implemented outside `History` as a special-purpose class (e.g., `UndoableInsert`, `UndoableDelete` for text; `UndoableSelection` and `UndoableCursor` for UI state). The text class creates and registers its own action objects; the UI code does the same
- **Fences for grouping** — the `History` class supports fences (via `addFence`) to group related actions so that a single user undo request can reverse a set of changes together (e.g., delete text, restore selection, reposition cursor). The placement of fences is determined by higher-level code, not by `History` itself
- **Three clean categories** — (1) the general-purpose undo/redo mechanism (`History`), (2) the specific action types (each understanding a small number of action kinds), and (3) the grouping policy (high-level UI code). Each category can be implemented without understanding the others
- **Key design decision** — separating the general-purpose part (managing and grouping actions) from the special-purpose parts (individual action implementations), creating a separate class for the general-purpose part and pushing the special-purpose parts into subclasses of `History.Action`
- **Combining code that shares a mechanism is OK** — "separate general-purpose from special-purpose" refers to code related to a particular mechanism. It may make sense to combine special-purpose code for one mechanism with general-purpose code for another in the same class. For example, the text class is general-purpose for text management but includes special-purpose undo code (`UndoableInsert`, `UndoableDelete`) because that code only handles undo operations for text modifications and is closely related to other text functions

## 8. Eliminate Special Cases in Code

- **Over-specialization also appears as special cases** — code riddled with `if` statements for edge conditions is a form of unnecessary specialization at the method level
- **Design the normal case to handle edge cases** — e.g., instead of checking for "no selection" everywhere, represent "no selection" as an empty selection (start == end). The same code path handles both cases with no conditionals
- **Eliminating special cases can also make code more efficient** — as discussed in Ch 20
