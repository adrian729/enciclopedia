# Ch 7: Applying Functional Programming in Practice

## Table of Contents

- [1. Handling Collections in Data Processing](#1-handling-collections-in-data-processing)
- [2. Handling JSON with Algebraic Data Types](#2-handling-json-with-algebraic-data-types)

## 1. Handling Collections in Data Processing

### 1.1. Map, Filter, and Fold Are Almost Enough

- **Most collection problems reduce to three operations** — despite infinitely many data-processing problems, the vast majority boil down to transforming elements (`map`), selecting elements (`filter`), and accumulating results (`fold`). Composing these three covers most real-world collection processing in e-commerce, mobile, and web applications
- **Dataflow programming with pipelines** — a collection flows through a sequence of stages (filter, then map, then fold) connected by the pipe operator `|>`, producing readable left-to-right data transformations. For example, calculating the total price of electronic products becomes: filter by type, map to price, fold with addition
- **Specialized functions extend the core three** — practical applications benefit from additional reusable functions (find, sort, take, etc.) that can themselves be implemented in terms of map, filter, and fold

### 1.2. Retrieving Single Elements

- **`find` extracts the first matching element** — given a predicate, `find` returns the first element satisfying it from an ordered collection, enabling queries like "first product cheaper than 1000." For unordered collections, the semantics shifts to returning *some* matching element
- **`contains` checks for existence** — a higher-order function that returns `true` if any element satisfies a predicate, implemented by checking whether the filtered list is non-empty

### 1.3. Ordering Collection Elements

- **`sort` with a comparison function** — `List.sort` takes a comparison function and returns a sorted list, allowing custom orderings (e.g., products sorted low-to-high by price using `Stdlib.compare` on the price field)
- **`reverse` via fold** — list reversal can be expressed using `List.fold_right`, illustrating how fold serves as a general-purpose list-building primitive

### 1.4. Retrieving Collection Parts

- **`take` extracts the first n elements** — useful for "top N" queries, such as showing the two cheapest products after sorting. Implemented recursively: base case returns empty list, recursive case prepends the head and takes n-1 from the tail
- **`take_while` extracts elements until a predicate fails** — a more general variant that keeps taking elements as long as they satisfy a predicate and stops at the first non-matching element, enabling queries like "all products under 1000 from cheapest up"

### 1.5. Domain-Specific Language for Collections

- **Collection functions form a DSL** — the list datatype plus the suite of higher-order functions (map, filter, fold, find, sort, take, take_while, etc.) together constitute a domain-specific language for collection processing, built on top of OCaml
- **Collections as single units** — the DSL lets you treat an entire collection as one conceptual unit rather than working with individual elements, raising the abstraction level
- **Shared interface enables composition** — all these functions accept and return lists, so they compose naturally into dataflow pipelines. This same approach transfers to other languages (Swift, Kotlin, JavaScript, Java), producing readable and reusable code

## 2. Handling JSON with Algebraic Data Types

### 2.1. Representing JSON as an Algebraic Data Type

- **JSON maps naturally to an algebraic data type** — JSON's hierarchical, multi-case structure (null, string, int, float, bool, array, object) is a textbook fit for an algebraic data type with seven constructors. Arrays are represented as `json list` and objects as `(string * json) list` (a list of key-value pairs)
- **Recursive structure** — because JSON arrays and objects can contain any JSON value, the type definition is recursive, mirroring the recursive nature of JSON itself

### 2.2. Pretty Printing JSON

- **Pattern matching drives serialization** — `json_to_string` matches on each data constructor and converts it to its string representation: `Null` becomes `""`, primitives use built-in conversion functions (`string_of_int`, `string_of_bool`, etc.), arrays and objects recursively serialize their elements and join them with commas
- **Recursive structure, recursive processing** — since JSON is a recursive data type, the pretty-print function is naturally recursive, calling itself on nested values

### 2.3. Extracting Fields from JSON

- **`member` retrieves a field by name** — takes a field name and a JSON value; if the value is an `Object`, it looks up the key and returns the associated JSON value; for all other constructors, it returns `Null`. This enables field extraction chained with the pipe operator: `movie |> member "actors" |> json_to_string`

### 2.4. Higher-Order Functions on JSON

- **`json_array_map` transforms array elements** — applies a function to each element of a JSON array, producing a new JSON array. Enables transformations like converting detailed actor records into compact summary strings
- **`json_array_filter` selects array elements** — filters a JSON array by a predicate, such as selecting only major characters from an actors list
- **`json_object_map` transforms key-value pairs** — maps each key-value pair in a JSON object to a new pair, enabling selective field transformations (e.g., compacting the actors field while leaving other fields unchanged)
- **`json_object_filter` selects key-value pairs** — filters a JSON object's fields by a predicate, such as excluding a specific field like `is_on_netflix`
- **Algebraic data types make DSLs easy** — the combination of an algebraic data type with higher-order functions yields a concise DSL for representing and manipulating JSON at a high level of abstraction. This pattern generalizes: functional programming with algebraic data types is exceptionally well-suited for building DSLs over hierarchical data structures
