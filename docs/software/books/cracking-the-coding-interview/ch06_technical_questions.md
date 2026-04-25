# Ch 6: Technical Questions

## Table of Contents

- [1. How to practice a question](#1-how-to-practice-a-question)
- [2. Must-know knowledge](#2-must-know-knowledge)
- [3. Powers of 2 table](#3-powers-of-2-table)
- [4. Language questions](#4-language-questions)
- [5. Five Steps to a Technical Question](#5-five-steps-to-a-technical-question)
- [6. Five Algorithm Approaches](#6-five-algorithm-approaches)
- [7. What good coding looks like](#7-what-good-coding-looks-like)

## 1. How to practice a question

- **Solve it yourself first** — don't read solutions passively; memorizing won't help on new problems. Think about space and time efficiency; ask if you can trade one for the other.
- **Code on paper** — interviews lack syntax highlighting, completion, and compilers. Mimic that by writing solutions on paper.
- **Test on paper** — general cases, base cases, error cases. Practice this in advance.
- **Type paper code as-is into a computer** — you will make mistakes; keep a running list of the kinds of errors you make so you catch them in the real interview.
- **Mock interviews** — CareerCup.com offers mocks with Microsoft/Google/Amazon employees; trading mocks with a friend also works.

## 2. Must-know knowledge

The book's absolute must-have list, split across three buckets. Practice implementing each from scratch.

| Data Structures | Algorithms | Concepts |
|-----------------|------------|----------|
| Linked Lists | Breadth First Search | Bit Manipulation |
| Binary Trees | Depth First Search | Singleton Design Pattern |
| Tries | Binary Search | Factory Design Pattern |
| Stacks | Merge Sort | Memory (Stack vs. Heap) |
| Queues | Quick Sort | Recursion |
| Vectors / ArrayLists | Tree Insert / Find / e.t.c. | Big-O Time |
| Hash Tables | | |

- **Understand use, implementation, and space/time complexity** for every item above.
- **Hash tables are especially important** — they come up frequently across interview questions.

## 3. Powers of 2 table

Useful for computing storage in scalability questions. Commit to memory, or keep this in front of you on a phone screen with a web-based company.

| Power of 2 | Exact Value (X) | Approx. Value | X Bytes into MB, GB, e.t.c. |
|------------|-----------------|---------------|------------------------------|
| 7 | 128 | | |
| 8 | 256 | | |
| 10 | 1,024 | 1 thousand | 1 K |
| 16 | 65,536 | | 64 K |
| 20 | 1,048,576 | 1 million | 1 MB |
| 30 | 1,073,741,824 | 1 billion | 1 GB |
| 32 | 4,294,967,296 | | 4 GB |
| 40 | 1,099,511,627,776 | 1 trillion | 1 TB |

Example use: a hash table mapping every 32-bit integer to a boolean fits in memory on a single machine.

## 4. Language questions

- **Big tech (MS/Google/Amazon)** — language trivia (e.g., "what is a vtable?") is low-priority; focus prep on data structures and algorithms. Still know the main concepts of any language you claim.
- **Smaller and non-software companies** — language questions matter more; start-ups look for their specific language.
- **Check CareerCup.com** for company-specific patterns; if yours isn't listed, pick a similar company as reference.

## 5. Five Steps to a Technical Question

1. **Ask the interviewer questions** to resolve ambiguity.
2. **Design an algorithm.**
3. **Write pseudocode first** — but explicitly tell the interviewer you'll follow it with "real" code, so you aren't lumped with candidates who use pseudocode to dodge real coding.
4. **Write code at a moderate pace.**
5. **Test the code and carefully fix any mistakes.**

### 5.1. Step 1: Ask Questions

- Problems are more ambiguous than they appear — ambiguity resolution can turn a hard problem into an easy one, and is explicitly tested at some companies (especially Microsoft).
- **Good questions** — data types, how much data, what assumptions hold, who the user is.
- **Example** — "design an algorithm to sort a list" becomes "sort an array of ~1M customer ages (integers 0–130)" once questions are asked; solution collapses to a 130-element counting array.

### 5.2. Step 2: Design an Algorithm

While designing, ask:

- What are the space and time complexity?
- What if there's a lot of data?
- Does the design cause other issues (e.g., a modified BST affecting insert/find/delete time)?
- Are the trade-offs right? Which scenarios make them worse?
- Were you told specific facts about the data (ages, already sorted)? Leverage them — interviewers rarely give data for no reason.

**Brute force is acceptable to mention first**, then optimize. The first solution doesn't need to be perfect.

### 5.3. Step 3: Pseudocode

Outlines thinking and reduces mistakes. **Explicitly announce** that real code will follow so you aren't confused with candidates dodging real code.

### 5.4. Step 4: Code

- Don't rush — slow, methodical pacing is faster overall.
- **Use Data Structures Generously** — define your own when useful (e.g., a `Person` class for "find min age"). Signals care about object-oriented design.
- **Don't Crowd Your Coding** — on a whiteboard, start in the upper-left corner, not the middle, so you have room.

### 5.5. Step 5: Test

- **Extreme cases** — 0, negative, null, maximums, minimums.
- **User error** — null or negative input.
- **General cases** — the normal case.
- **Numeric / bit-shifting code** — test while writing, not only at the end.
- **When you find a bug, think deeply about why** — flipping return values to "fix" a failing test creates more bugs and is the mark of the "random fixer" candidate.

## 6. Five Algorithm Approaches

No surefire approach exists; the more you practice, the easier identifying the right one becomes. Approaches can be mixed and matched.

| Approach | What it means |
|----------|---------------|
| **Exemplify** | Write specific examples and derive a general rule from them |
| **Pattern Matching** | Consider which known problems this resembles; adapt their solution |
| **Simplify & Generalize** | Change a constraint (data type, size) to simplify, solve the simpler version, then generalize back |
| **Base Case and Build** | Solve n=1, then n=2 assuming n=1, then n=3 assuming n=1,2, …; often leads to recursive algorithms |
| **Data Structure Brainstorm** | Walk through a list of data structures and try each; hacky but effective |

### 6.1. Exemplify

Example: **angle between clock hands** — pick an example (3:27), draw the clock, derive:

- minute hand vs. 12 o'clock: `360 * m / 60`
- hour hand vs. 12 o'clock: `360 * (h % 12) / 12 + 360 * (m / 60) * (1 / 12)`
- angle between: `(hour angle - minute angle) % 360`
- simplified: `(30h - 5.5m) % 360`.

### 6.2. Pattern Matching

Example: **find min in a rotated sorted array** (e.g., `3 4 5 6 7 1 2`). Two related problems: find-min in unsorted array (not useful), binary search in sorted array (useful). Adapt binary search by comparing mid and right to locate the "reset point"; recurse on the correct half.

### 6.3. Simplify & Generalize

Example: **ransom note from a magazine string.** Simplify by cutting characters (not whole words): count characters in the note, scan the magazine for availability. Generalize back to words by swapping the character-count array for a hash table of word frequencies.

### 6.4. Base Case and Build

Example: **all permutations of a unique-character string** `"abc"`. Know `P("a") = {"a"}`, `P("ab") = {"ab","ba"}`; build `P("abc")` by inserting `c` into every position of every string in `P("ab")`. Generalizes to the recursive rule: permute `s₁…sₙ₋₁`, then insert `sₙ` at every position.

### 6.5. Data Structure Brainstorm

Example: **track the median of numbers stored in an expanding array.** Walk through candidates:

- **Linked list** — bad at access and sorting.
- **Array** — possible if kept sorted, but insertion is expensive.
- **Binary tree** — balanced BST puts median near the top, but with an even element count the median is the average of the middle two and they can't both be at the root.
- **Heap** — winning answer. Keep a max-heap of the smaller half and a min-heap of the bigger half; the roots give the median. Rebalance by popping from one heap and pushing onto the other when sizes diverge.

## 7. What good coding looks like

Five broad properties. Balancing them is an act — you'll trade efficiency for maintainability and vice versa.

- **Correct** — operates correctly on all expected *and* unexpected inputs.
- **Efficient** — both asymptotic (big-O) and practical (constants dropped by big-O can still matter in real life).
- **Simple** — 10 lines beats 100; code should be quick to write.
- **Readable** — another developer can read it; comments where necessary; clever bit-shifting isn't necessarily good.
- **Maintainable** — adaptable to product-lifecycle changes; easy for other developers to maintain.

### 7.1. Use Data Structures Generously

Example: summing polynomial expressions `Ax^a + Bx^b + …`.

- **Bad** — one array of doubles indexed by exponent; breaks on negative/non-integer exponents and wastes space (1000 elements for `x^1000`).
- **Less bad** — two parallel arrays `coefficients[]` and `exponents[]`; fragile, messy, returns two arrays.
- **Good** — define an `ExprTerm` class with `coefficient` and `exponent`; `sum(ExprTerm[], ExprTerm[])` returns `ExprTerm[]`. May be called "over-optimizing," but demonstrates deliberate data-structure design.

### 7.2. Appropriate Code Reuse

Example: compare a binary string to a hex string for value equality. Elegant version uses one `convertToBase(number, base)` method (shared by both inputs) and one `digitToValue(char)` helper, rather than duplicating conversion logic.

### 7.3. Modular

Separate isolated chunks into their own methods — more maintainable, readable, testable.

Example: **swap min and max in an array**. The monolithic version inlines min-scan, max-scan, and swap. The modular version extracts `getMinIndex`, `getMaxIndex`, and `swap` into standalone methods, each testable on its own. The gain compounds as code grows.

### 7.4. Flexible and Robust

- Don't over-assume the input shape (e.g., don't hardcode a 3x3 tic-tac-toe board — write for NxN).
- Use constants instead of magic numbers; use templates / generics where helpful.
- Limit: don't balloon complexity for hypothetical generality — if the simple case is all that's asked, stay simple.

### 7.5. Error Checking

- Validate inputs with ASSERT or if-statements; a careful coder doesn't assume input shape.
- Example — `convertToBase` rejects invalid base (line: `if (base < 2 || (base > 10 && base != 16)) return -1;`) and invalid digits within the loop.
- In an interview, if error checks would be tedious, **write a placeholder comment** indicating you'd fill them in, rather than spending precious time writing them out.
