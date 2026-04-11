# Ch 6: Dataflow Programming with Functions

## Table of Contents

- [1. List-based Dataflow Programming](#1-list-based-dataflow-programming)
- [2. Stream-based Dataflow Programming](#2-stream-based-dataflow-programming)

## 1. List-based Dataflow Programming

### 1.1. The Dataflow Programming Paradigm

- **Programs as directed graphs** — dataflow programming models programs as directed graphs where nodes are operations (accept inputs, produce outputs) and directed edges send one node's output as the next node's input. Originated from Bert Sutherland's Ph.D. thesis "The on-line graphical specification of computer procedures"
- **Advantages over textual representation** — the dataflow style makes program structure visible (how building blocks compose) and enables automatic parallel execution based on data dependencies, with no extra effort from the programmer
- **Reusable component libraries** — the paradigm encourages creating general-purpose components that can be mixed and matched to solve problems not envisioned by their creators, saving development time compared to implementing from scratch

### 1.2. Functions as Dataflow Components

- **Pure functions behave like dataflow components** — because functions in FP always return the same output for the same input and have no side effects, they naturally act as processing nodes that accept input and produce output. When functions share a common data format (e.g., lists), they compose in the dataflow style
- **map, filter, and fold as components** — each higher-order function serves a distinct role in a dataflow pipeline:

| Component | Dataflow role | Configurable parameter |
|-----------|--------------|----------------------|
| **map** | Transforms each element of the input signal to a new value in the output signal | Mapping function `f` |
| **filter** | Passes through only elements satisfying a condition | Predicate `p` |
| **fold** | Accumulates an input signal into a single value | Initial value and accumulation function |

- **Composing a pipeline** — to compute the sum of squares of even numbers in `[a, b]`, decompose into stages: enumerate integers, filter evens, map to squares, fold with `(+)`. Each stage is a reusable component; the list serves as the universal interface connecting them

### 1.3. The Pipe Operator

- **Problem with nested calls** — writing `List.fold_left (+) 0 (List.map square (List.filter even (enumerate_integers a b)))` reverses the logical left-to-right flow of data, making the code hard to read
- **Pipe operator `|>`** — defined as `x |> f = f x`, it lets data flow left-to-right to match the dataflow diagram: `enumerate_integers a b |> List.filter even |> List.map square |> List.fold_left (+) 0`
- **zipWith as a multi-input component** — `zipWith` acts as a dataflow component accepting two input signals. For example, a prime-counting program uses `zipWith` to pair index labels with filtered primes

### 1.4. Rule of Composition

- **Unix philosophy parallel** — Eric Steven Raymond's "rule of composition" from *The Art of Unix Programming* states: favor small, independent programs that do one thing well, with plain text as the universal interface. The Unix pipe `|` connects programs the same way OCaml's `|>` connects functions
- **FP mirrors Unix success** — `map`, `filter`, `fold`, and `zipWith` are small, independent functions that each do one thing well. Lists serve as the shared interface that makes them composable. The rule of composition is a part of what makes the Unix operating system so successful, and FP harnesses that same power

## 2. Stream-based Dataflow Programming

### 2.1. Limitations of List-based Dataflow

- **Lists are finite** — in OCaml (a strict language), attempting `let rec naturals_from n = n :: naturals_from (n + 1)` causes a stack overflow because the `::` constructor eagerly evaluates both arguments. This means list-based dataflow cannot represent infinite sequences
- **Finite workarounds are inefficient** — constraining the range (e.g., `first_prime_between a b`) works but enumerates and checks every element in the range even when only the first match is needed

### 2.2. Delaying Evaluation

- **Thunks** — wrapping an expression in a zero-argument function (`fun () -> fib 40`) delays its evaluation until the thunk is applied. This is the fundamental mechanism for controlling when computation happens
- **`lazy` and `Lazy.force`** — OCaml's built-in `lazy` keyword delays evaluation and `Lazy.force` triggers it. Unlike thunks, `lazy` includes memoization: the first `Lazy.force` computes and caches the result; subsequent calls return the cached value instantly

### 2.3. Streams as Delayed Lists

- **Stream type definition** — `type 'a stream = Cons of 'a * 'a stream Lazy.t` — a stream is a pair of a head value (available immediately) and a lazily-evaluated tail that promises to produce the next stream element on demand
- **No empty stream** — unlike lists, streams have no `Nil` case because they can represent infinite sequences where there is always a next element
- **Selectors** — `stream_hd (Cons (h, _)) = h` returns the head; `stream_tl (Cons (_, t)) = Lazy.force t` forces the tail to evaluate, producing the next element
- **Infinite sequences without overflow** — `let rec naturals_from n = Cons (n, lazy (naturals_from (n+1)))` succeeds because `lazy` delays the recursive call. The stream produces elements on demand rather than all at once
- **Inspecting streams** — `stream_take n s` forces exactly `n` elements from the stream into a finite list, giving controlled access to an otherwise unbounded sequence

### 2.4. Higher-Order Functions on Streams

- **stream_map** — applies a mapping function to each stream element, using `lazy` to delay recursive processing of the tail: `stream_map f s = Cons (f (stream_hd s), lazy (stream_map f (stream_tl s)))`. Unlike `List.map`, input and output signals may have infinite elements
- **stream_filter** — produces a new stream containing only elements satisfying a predicate. It keeps requesting the next element from the input stream until it finds one that passes. If no such element exists, `stream_filter` never returns
- **stream_zipWith** — the stream version of `zipWith`, combining two streams element-wise with a binary function. It transparently handles synchronization by waiting until both input streams can provide elements before producing output

### 2.5. Stream-based Dataflow in Practice

- **Composing stream components** — `stream_hd`, `stream_tl`, `stream_map`, `stream_filter`, and `stream_zipWith` compose in the same dataflow style as their list counterparts, with streams as the shared interface
- **Incremental computation** — the key efficiency advantage of streams: `first_prime_greater_equal n = naturals_from n |> stream_filter is_prime |> stream_hd` generates candidates one at a time and stops as soon as the filter finds a prime, rather than enumerating and checking an entire range
- **Three benefits of stream-based dataflow** — programs are constructed by composing components; signals can contain infinitely many elements; computation is done incrementally (on demand)

### 2.6. Infinite Lists in Non-strict Languages

- **Haskell lists are already lazy** — in Haskell, `naturals_from n = n : naturals_from (n+1)` works without a special stream type because Haskell is non-strict: it does not evaluate `naturals_from (n+1)` until the value is needed, achieving the same effect as OCaml's `lazy` keyword
- **Strict vs non-strict trade-offs** — non-strict semantics (Haskell) let ordinary lists act as streams, but make it harder to reason about space and time usage. Strict semantics (OCaml) require explicit `lazy`/stream types for infinite data but make performance characteristics more predictable
