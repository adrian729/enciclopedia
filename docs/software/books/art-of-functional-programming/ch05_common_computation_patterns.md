# Ch 5: Common Computation Patterns

## Table of Contents

- [1. The map Function](#1-the-map-function)
- [2. The filter Function](#2-the-filter-function)
- [3. The fold Function](#3-the-fold-function)
- [4. The zip Function](#4-the-zip-function)

## 1. The map Function

### 1.1. map on Lists

- **Factoring out a common pattern** — functions like `square_list` and `cube_list` share identical structure (recurse over list, transform each head), differing only in the transformation applied. Extracting that shared shape into a higher-order `map` function lets each specific case become a one-liner: `let square_list = map (fun x -> x * x)`
- **map as element replacement** — `map f l` replaces each element `e` in list `l` with `f e`, producing a new list of the same length. This lets you treat the transformation of an entire sequence as a single conceptual unit rather than thinking element-by-element
- **Type signature** — `List.map: ('a -> 'b) -> 'a list -> 'b list` — the function `f` can change the element type, so the output list may have a different type than the input

### 1.2. map on Trees

- **Generalizing beyond lists** — map applies naturally to any hierarchical data structure whose nodes hold elements of the same type, such as a binary tree defined as `type 'a bin_tree = Leaf | Node of 'a bin_tree * 'a * 'a bin_tree`
- **map_tree** — recursively applies `f` to each node's value while preserving the tree's shape: `Leaf` maps to `Leaf`, `Node (l, v, r)` maps to `Node (map_tree f l, f v, map_tree f r)`

### 1.3. map on Containers

- **Container abstraction** — lists, binary trees, and `option` are all containers (data structures that hold elements). A meaningful `map` can often be defined for any container type
- **map on option** — `map_option f o` replaces the value `x` inside `Some` with `f x` and maps `None` to `None`, which is useful for composing operations that may fail. For example, composing `longest_string` (which returns `'a option`) with `Option.map String.length` yields the length of the longest string while transparently propagating the `None` case
- **Structure preservation** — a critical property of `map` is that it applies a function to each element without altering the container's structure. A mapped list has the same length, a mapped tree has the same shape, and a mapped `Some` stays `Some`

### 1.4. map on Domains or Contexts

- **Generalized type pattern** — all map signatures share the form `('a -> 'b) -> 'a context -> 'b context`, where `context` can be `list`, `bin_tree`, `option`, or even abstract concepts like asynchronous computation (`future`)
- **Context-preserving transformation** — just as map on a container must not change the container's structure, map on a domain/context must apply a function to a value without altering the context itself. For example, `Future.map` transforms the eventual value held by a `Future` without changing how the asynchronous computation is carried out

### 1.5. map as a Lifting Function

- **Lifting** — partially applying `map` to a function `f: 'a -> 'b` produces a function `'a context -> 'b context` that "lifts" `f` into a new domain. For instance, `List.map square` lifts the `square` function from integers to integer lists
- **Conceptual unit** — map lets you think about data transformation for an entire structure as one operation, abstracting away the per-element mechanics

## 2. The filter Function

### 2.1. filter on Lists

- **Predicate-based selection** — `filter` accepts a predicate (a function returning `bool`) and a list, keeping only the elements that satisfy the predicate. Functions like `evens` and `positives` are specific cases where the predicate is `even` or `positive`
- **Type signature** — `List.filter: ('a -> bool) -> 'a list -> 'a list` — unlike `map`, the element type does not change; only the list length may shrink
- **Generality beyond lists** — `filter` applies naturally to any collection, such as a set, where elements without particular order can still be selected by a predicate

### 2.2. Composing Predicates

- **Reuse through composition** — instead of writing a new `odd` predicate from scratch, compose existing predicates: `compose not even` produces the `odd` predicate by negating `even`
- **compose function** — `let compose f g x = f (g x)` chains two functions together, enabling concise reuse: `let odds = List.filter (compose not even)`

## 3. The fold Function

### 3.1. fold on Lists

- **Combining elements into a single value** — `fold_right f init l` replaces the empty list `[]` with `init` and each list constructor `::` with the binary function `f`, collapsing the list from right to left into one result
- **Constructor replacement view** — thinking of `fold_right` as substituting constructors makes it easy to derive specific functions: `fold_right (+) 0` sums a list, `fold_right ( * ) 1` multiplies it
- **Subsuming other patterns** — `fold` is powerful enough to express `map`, `filter`, `length`, `any`, and `all` as special cases. For example, `map f l = fold_right (fun x l -> f x :: l) l []`

| Function | Folding function `f` | Initial value `init` |
|----------|---------------------|---------------------|
| `sum_list` | `(+)` | `0` |
| `prod_list` | `( * )` | `1` |
| `any` | `(\|\|)` | `false` |
| `all` | `(&&)` | `true` |
| `length` | `fun x len -> len + 1` | `0` |

- **fold_left vs fold_right** — `fold_left` processes the list from left to right using an accumulator, e.g., `fold_left (-) 0 [1;2;3]` computes `(((0-1)-2)-3) = -6` versus `fold_right (-) 0 [1;2;3]` which computes `(1-(2-(3-0))) = 2`. `fold_left` is tail-recursive, making it more memory-efficient for large lists
- **MapReduce connection** — the higher-order abstractions `map`, `fold`, and `reduce` (fold's name in Python/Java) inspired Google's MapReduce framework and Apache Hadoop for parallel processing of large data sets

### 3.2. fold on Trees

- **Same strategy, different structure** — `fold_tree f init t` replaces `Leaf` with `init` and `Node` with a three-argument function `f`, collapsing the tree into a single value
- **Derived functions from fold_tree** — `sum_tree`, `size` (node count), and `tree_elements` (collect all values into a list) are all specific configurations of `fold_tree`

### 3.3. fold on Other Data Types

- **fold on option** — `fold_option f init o` replaces `None` with `init` and `Some x` with `f x`, collapsing the option into a plain value
- **fold on naturals** — given `type nat = Zero | Succ of nat`, `fold_nat f init n` replaces `Zero` with `init` and each `Succ` with `f`, computing `f(...f(init))` with `f` applied `n` times. This enables conversions like `nat_to_int = fold_nat ((+) 1) 0`
- **Design principle** — whenever you define a recursive data structure, consider designing a `fold` function for it to enable high-level data aggregation without exposing recursion details

## 4. The zip Function

### 4.1. Pairing Elements from Two Lists

- **zip** — takes two lists and returns a list of corresponding pairs: `zip [1;2;3] [4;5;6]` produces `[(1,4); (2,5); (3,6)]`. If the lists have different lengths, extra elements in the longer list are ignored
- **Zipper analogy** — the function is named `zip` because it works like a clothing zipper, interlocking teeth from two sides into one

### 4.2. zipWith — Generalizing zip with a Function

- **zipWith** — accepts a binary function `f` and two lists, producing a new list by applying `f` to corresponding elements: `zipWith (+) [1;2;3] [4;5;6]` yields `[5;7;9]`
- **zip as a special case** — `zip l1 l2 = zipWith (fun x y -> (x, y)) l1 l2`
- **Composing with other patterns** — `zipWith` combines naturally with `map` and `fold` to solve multi-list problems. For example, computing the total absolute difference of adjacent elements: `let total_abs_diff l = List.fold_right (+) (List.map abs (diff l)) 0` where `diff l = zipWith (-) (List.tl l) l`
- **Checking sorted order** — `is_ascending_sorted l` can be expressed as `all (zipWith (<=) l (List.tl l))`, demonstrating how combining zip with fold replaces what would be an explicit recursive traversal

| Pattern | Purpose | Key Parameters |
|---------|---------|---------------|
| **map** | Transform each element independently | Mapping function `f` |
| **filter** | Select elements matching a condition | Predicate `p` |
| **fold** | Collapse a structure into a single value | Binary function `f`, initial value `init` |
| **zip / zipWith** | Combine corresponding elements from multiple lists | Binary function `f` (for zipWith) |
