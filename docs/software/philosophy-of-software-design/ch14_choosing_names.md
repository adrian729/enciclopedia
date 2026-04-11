# Ch 14: Choosing Names

## Table of Contents

- [1. Why Names Matter](#1-why-names-matter)
- [2. Create an Image](#2-create-an-image)
- [3. Names Should Be Precise](#3-names-should-be-precise)
- [4. Use Names Consistently](#4-use-names-consistently)
- [5. The Go Style Counterpoint](#5-the-go-style-counterpoint)

## 1. Why Names Matter

- **Names are a form of documentation** — good names make code easier to understand, reduce the need for other documentation, and make it easier to detect errors
- **Complexity is incremental** — a single mediocre name won't ruin a system, but software has thousands of variables; choosing good names for all of them has a significant cumulative impact on complexity and manageability
- **Bad names cause real bugs** — in the Sprite operating system, reusing the variable name `block` for both physical disk blocks and logical file blocks caused a six-month debugging ordeal. Distinct names like `fileBlock` and `diskBlock` would have made the error impossible

## 2. Create an Image

- **Goal: paint a picture in the reader's mind** — a good name conveys what the entity is and, just as important, what it is not. Test a name by asking: "If someone saw this in isolation, with no declaration or documentation, how closely could they guess what it refers to?"
- **Names are abstractions** — like other abstractions, the best names focus attention on the most important aspects while omitting less important details. Keep names to two or three words that capture the essence

## 3. Names Should Be Precise

- **Vague names are the most common problem** — names that are too generic (e.g., `getCount()` instead of `getActiveIndexlets()`) force readers to consult documentation to understand what the code does

| Vague name | Problem | Better name |
|------------|---------|-------------|
| `x`, `y` (for character position in file) | Could mean pixel coordinates or anything else | `charIndex`, `lineIndex` |
| `blinkStatus` | "status" is meaningless for a boolean; "blink" doesn't say what blinks | `cursorVisible` |
| `VOTED_FOR_SENTINEL_VALUE` | Says it's special, not what the special meaning is | `NOT_YET_VOTED` |
| `result` (in a void method) | Implies a return value; reveals nothing about what it holds | `mergedLine`, `totalChars` |

> **Red Flag: Vague Name** — if a variable or method name is broad enough to refer to many different things, it doesn't convey much information and the underlying entity is more likely to be misused.

- **Booleans should be predicates** — names like `cursorVisible` let readers guess what `true` means; names like `blinkStatus` do not
- **Too-specific is also wrong** — a parameter named `selection` for a method that operates on any text range misleads readers into thinking it only works on UI selections. A more general name like `range` is better
- **Hard-to-name = design smell** — if you can't find a precise, intuitive, short name for a variable, the variable may not have a clean definition. Consider whether it's trying to represent multiple things and should be split

> **Red Flag: Hard to Pick Name** — if it's hard to find a simple name that creates a clear image of the underlying object, that's a hint the object may not have a clean design.

- **Exception: short loop variables** — `i` and `j` are fine when the loop spans only a few lines and the meaning is obvious from context. The longer the scope, the more descriptive the name should be

## 4. Use Names Consistently

- **Three rules for consistency:**
  1. Always use the common name for the given purpose
  2. Never use that name for anything other than the given purpose
  3. Make sure the purpose is narrow enough that all variables with that name have the same behavior
- **The `block` bug violated rule 3** — the name was used for two different kinds of blocks, creating a false assumption about meaning
- **Distinguish with prefixes** — when multiple variables refer to the same kind of thing (e.g., source and destination block numbers), use a shared root with a distinguishing prefix: `srcFileBlock`, `dstFileBlock`
- **Consistent loop conventions** — always use `i` for outermost loops and `j` for nested loops so readers can make instant, safe assumptions

## 5. The Go Style Counterpoint

- **Go culture favors very short names** — the Go style guide argues that long names obscure what code does, and encourages single-letter variables and reusing short names like `ch` for both "character" and "channel"
- **Ousterhout's response** — ambiguous short names are likely to cause confusion and errors, just like the `block` bug. Readability should be judged by readers, not writers; if people complain that code is cryptic, use longer names
- **One point of agreement** — "The greater the distance between a name's declaration and its uses, the longer the name should be." Short names are fine for tightly scoped variables; long-lived or widely-used variables need descriptive names
