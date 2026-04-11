# Ch 4: Compound Data Types

## Table of Contents

- [1. Tuples](#1-tuples)
- [2. Pattern Matching](#2-pattern-matching)
- [3. Immutability](#3-immutability)
- [4. Lists](#4-lists)
- [5. Algebraic Data Types](#5-algebraic-data-types)
- [6. Algebraic Data Types vs. Classes](#6-algebraic-data-types-vs-classes)

## 1. Tuples

- **Grouping data into compound objects** — primitive types (integers, floats, booleans, strings) are often insufficient for modeling real-world concepts. Tuples let you glue multiple values into a single compound data object, so you can treat something like a 2D point as one concept instead of tracking separate `x` and `y` variables
- **Construction syntax** — values are placed in parentheses separated by commas: `(42, "Hi FP")`. Order matters — `("Hi FP", 42)` is an entirely different tuple
- **Heterogeneous elements** — a tuple can contain elements of different types. The pair `(42, "Hi FP")` has type `int * string` (read "int cross string")
- **Fixed arity** — tuples have a fixed number of elements, making them ideal when the count is known in advance (e.g., a 2D point always has exactly two coordinates)
- **Nesting** — tuples can contain other tuples: `(1, (2, "FP"))`. The Scheme language exploits this to represent lists as chains of nested pairs: `(1, (2, (3, (4, nil))))`
- **Returning multiple values** — tuples are a natural way for a function to return more than one result, e.g., `let div_mod x y = (x / y, x mod y)` returns both the quotient and remainder as a pair

## 2. Pattern Matching

- **Decomposing compound data** — pattern matching (`match ... with`) destructures tuples (and other compound types) into their components, binding each part to a name for use in the function body
- **Tuple patterns in `match`** — `match p with | (x, y) -> ...` binds the first element of pair `p` to `x` and the second to `y`, enabling coordinate access for operations like point translation
- **Multiple simultaneous patterns** — instead of nesting two `match` expressions, OCaml allows matching multiple values at once: `match p1, p2 with | (x1, y1), (x2, y2) -> ...`, which is cleaner and more readable
- **Syntactic sugar in `let` and `fun`** — OCaml allows pattern matching directly in function parameters: `let distance_point (x1, y1) (x2, y2) = ...`, avoiding explicit `match` expressions entirely

## 3. Immutability

- **Data cannot be changed after construction** — in functional programming, all data is immutable. Once a tuple like `(2., 1.)` is created, its values can never be modified. This contrasts sharply with imperative programming where objects are routinely mutated in place
- **New data from old** — instead of modifying a point's coordinates, `translate_point (x, y) dx dy` constructs an entirely new point `(x +. dx, y +. dy)`. This "create new, never mutate" pattern is fundamental to the functional style
- **Easier reasoning** — with immutable data, you know exactly what a value contains just by looking at its construction. Mutable data requires tracing its entire change history to determine the current state
- **Thread safety** — immutable data is inherently safe to share across threads because no thread can alter it, eliminating an entire class of concurrency bugs

## 4. Lists

### 4.1. Construction and Destruction

- **Two constructors** — OCaml lists are built from `[]` (nil, the empty list) and `::` (cons, which prepends an element to an existing list). `1::(2::(3::[]))` is the fully explicit form; `[1; 2; 3]` is syntactic sugar
- **Singly linked list** — internally, an OCaml list is a singly linked chain of cons cells, with `[]` signaling the end. This structure means prepending to the front is O(1) but accessing the n-th element requires traversing n links
- **Pattern matching for access** — since only the head is directly accessible, `match l with | [] -> ... | hd :: tl -> ...` is the standard way to decompose a list. `hd` binds the first element; `tl` binds the remaining list
- **Recursive construction** — building lists follows the same recursive pattern: `let rec enumerate_integers a b = if a > b then [] else a :: enumerate_integers (a + 1) b` constructs a list by consing each element onto the result of the recursive call

### 4.2. List Operations

- **Recursive traversal** — operations like `nth`, `length`, and `append` all follow the pattern of matching on `[]` (base case) and `hd :: tl` (recursive case), using `[]` as the recursion terminator
- **`length`** — returns 0 for an empty list, otherwise 1 plus the length of the tail: `let rec length l = match l with | [] -> 0 | hd :: tl -> 1 + length tl`
- **`append`** — concatenates two lists by recursively consing elements from the first list onto the second: `let rec append l1 l2 = match l1 with | [] -> l2 | x :: xs -> x :: append xs l2`. OCaml's built-in `@` operator does the same thing

### 4.3. Immutable Lists vs. Mutable Arrays

- **No in-place updates** — to "change" the first element of `[1; 2; 3]` to `4`, you construct a new list: `4 :: (List.tl l)`. The original list is untouched
- **Mutable arrays cause aliasing bugs** — in Java, `int[] b = a; b[0] = 42;` silently modifies `a` as well because both names refer to the same mutable memory. Immutable lists eliminate this entire class of bugs
- **Functional style is closer to mathematics** — a function that reverses a list constructs a new list with elements in reverse order, always producing the same output for the same input. The imperative version swaps elements in place, mutating the input directly

### 4.4. Lists as Generic Containers

- **Parameterized type `'a list`** — the type variable `'a` means a list can hold elements of any type: `int list`, `string list`, `(float * float) list`, or even lists of functions
- **Generic programming** — functions like `length : 'a list -> int` and `@ : 'a list -> 'a list -> 'a list` work on any list regardless of element type, avoiding the need to write separate implementations for each concrete type

## 5. Algebraic Data Types

### 5.1. Product and Sum Types

- **Two ways to build compound types** — *product types* (combination) group values together, like `int * string`. *Sum types* (alternation) define a type as a set of alternatives, like a list being either `[]` or `hd :: tl`
- **Algebraic data types blend both** — they combine product and sum types into a single mechanism. The term "algebraic" refers to this combination of sum and product

### 5.2. Defining Algebraic Data Types

- **Data constructors** — each alternative in the type is a named constructor that may carry zero, one, or multiple pieces of data: `type shape = Circle of float | Rectangle of float * float`
- **Recursive definitions** — an algebraic data type can reference itself, making it ideal for recursive structures: adding `ComplexShape of shape list` lets shapes contain other shapes
- **Pattern matching deconstructs values** — `match s with | Circle r -> ... | Rectangle (w, h) -> ...` handles each variant, with the compiler warning if any case is missing

### 5.3. Parameterized Algebraic Data Types

- **Type variables for genericity** — algebraic data types can be parameterized over type variables, creating generic containers. A binary tree becomes `type 'a bin_tree = Leaf | Node of 'a bin_tree * 'a * 'a bin_tree`, holding elements of any type
- **Generic functions over parameterized types** — functions like `size : 'a bin_tree -> int` work for trees of integers, strings, or any other type, just as `length` works for any list
- **Multiple type parameters** — the `either` type is parameterized over two type variables: `type ('a, 'b) either = Left of 'a | Right of 'b`. By convention, `Right` holds the correct value and `Left` holds an error

### 5.4. Built-in Types as Algebraic Data Types

OCaml defines several core types as algebraic data types internally:

| Type | Definition | Purpose |
|------|-----------|---------|
| **`bool`** | `True \| False` | Two-valued logic (used as `true`/`false` in code) |
| **`'a list`** | `[] \| :: of 'a * 'a list` | Singly linked sequence of elements |
| **`'a option`** | `None \| Some of 'a` | Represents presence or absence of a value — used when a function might not return a meaningful result (e.g., `list_max` returns `None` for an empty list, `Some 3` for `[1; 2; 3]`) |

- **`option` vs. `either`** — both model two-outcome situations, but `option` carries no data in the `None` case while `either` allows attaching information (like an error message) to the `Left` case

## 6. Algebraic Data Types vs. Classes

### 6.1. The Expression Problem

- **Classes excel at adding new representations** — adding a `Triangle` subclass to a `Shape` hierarchy requires no changes to `Shape`, `Circle`, or `Rectangle`. Each class encapsulates its own behavior
- **Classes struggle with new operations** — adding a `perimeter` method means modifying the base class declaration and every existing subclass, which is expensive when subclasses are distributed across a codebase
- **Algebraic data types excel at adding new operations** — writing a new `perimeter : shape -> float` function uses pattern matching to handle each variant, with no changes to existing functions like `area`
- **Algebraic data types struggle with new representations** — adding a `Triangle` constructor forces updates to every function that pattern-matches on `shape`, since they must all handle the new case

| Dimension | Classes + Inheritance | Algebraic Data Types + Pattern Matching |
|-----------|----------------------|----------------------------------------|
| **Add new data variant** | Easy — add a subclass | Hard — must update all existing functions |
| **Add new operation** | Hard — must modify base class and all subclasses | Easy — write a new function with pattern matching |

- **The expression problem** — computer scientist Philip Wadler named this fundamental tension: can a data abstraction make it easy to add both new representations *and* new operations while retaining static type safety? As of today, no definitive solution exists
- **Practical guideline** — use classes and inheritance when you expect to add new data representations frequently; use algebraic data types and pattern matching when you expect to add new operations frequently. Many languages (OCaml included) support both for this reason
