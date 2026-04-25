# Ch 18: Code Should be Obvious

## Table of Contents

- [1. What Obviousness Means](#1-what-obviousness-means)
- [2. Things That Make Code More Obvious](#2-things-that-make-code-more-obvious)
- [3. Things That Make Code Less Obvious](#3-things-that-make-code-less-obvious)
- [4. Obviousness as Information](#4-obviousness-as-information)

## 1. What Obviousness Means

- **Obscurity is one of the two main causes of complexity** (alongside dependencies, per Ch 2) — it occurs when important information about a system is not obvious to new developers. Writing obvious code is the direct remedy
- **Quick, correct first guesses** — code is obvious when someone can read it quickly, without much thought, and their first guesses about behavior or meaning turn out to be correct
- **Less time, fewer bugs** — obvious code reduces the effort needed to gather information, which directly lowers the chance of misunderstanding and mistakes
- **Fewer comments needed** — obvious code is self-explanatory, reducing the documentation burden
- **Obviousness is in the reader's eye** — if someone reading your code says it's not obvious, it isn't, regardless of how clear it seems to you. Code reviews are the best way to gauge obviousness

## 2. Things That Make Code More Obvious

- **Good names** (Ch 14) — precise, meaningful names clarify behavior and reduce the need for documentation. Vague or ambiguous names force readers to trace through the code to deduce meaning
- **Consistency** (Ch 17) — when similar things are done in similar ways, readers recognize patterns and draw safe conclusions without analyzing code in detail
- **Judicious use of white space** — formatting affects comprehension. Blank lines between major blocks (especially before comments describing each block) make structure visible. White space within statements (e.g., spaces around operators in a `for` loop) clarifies their structure
- **Comments to compensate for nonobvious code** — when code can't be made obvious through structure alone, comments must fill in the missing information. Put yourself in the reader's position and figure out what would confuse them

## 3. Things That Make Code Less Obvious

- **Event-driven programming** — handler functions are invoked indirectly via function pointers or interfaces, making control flow hard to follow. You can't tell which specific function runs without knowing what was registered at runtime. Mitigate by documenting in each handler's interface comment when it is invoked
- **Generic containers** — types like `Pair` or `std::pair` obscure meaning because elements have generic names (`getKey()`, `getValue()`). Define a specialized class or struct with meaningful field names instead

> **Red Flag: Nonobvious Code** — if the meaning and behavior of code cannot be understood with a quick reading, it is a red flag. Often this means that important information is not immediately clear to someone reading the code

- **Different types for declaration and allocation** — declaring a variable as `List` but allocating an `ArrayList` can mislead readers about performance and thread-safety characteristics. Match the declaration type to the actual type
- **Code that violates reader expectations** — e.g., a constructor that spawns background threads so the application keeps running after `main` returns. When behavior departs from what readers would assume, document it explicitly at the point of use, not just in the interface comment
- **General rule: design for ease of reading, not ease of writing** — generic containers are convenient for the author but confusing for every reader that follows. A few extra minutes defining a specific type pays off in clarity

## 4. Obviousness as Information

- **Nonobvious code = missing information** — when code is hard to understand, it usually means the reader lacks important information (e.g., that a constructor spawns threads, or that `getKey()` returns a term number)
- **Three strategies to make code obvious**:
  1. **Reduce the information needed** — use abstraction and eliminate special cases so there is less to explain
  2. **Leverage existing knowledge** — follow conventions and meet expectations so readers can apply what they already know
  3. **Present information in the code** — use good names and strategic comments to make remaining details explicit
