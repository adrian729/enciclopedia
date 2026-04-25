# Ch 8: Arrays and Strings

## Table of Contents

- [1. Scope](#1-scope)
- [2. Hash Tables](#2-hash-tables)
- [3. ArrayList (Dynamically Resizing Array)](#3-arraylist-dynamically-resizing-array)
- [4. StringBuffer](#4-stringbuffer)

## 1. Scope

- **Assumed knowledge** — the chapter skips array/string basics and focuses on common techniques and issues with these data structures.
- **Interchangeable questions** — a problem stated as an array question may equally be asked as a string question, and vice versa.

## 2. Hash Tables

- **Definition** — a data structure that maps keys to values for highly efficient lookup, built on an underlying array plus a *hash function*.
- **Core mechanic** — inserting a key-value pair calls the hash function to convert the key to an integer, which becomes the array index where the object is stored.
- **Collisions** — in the naive version, two distinct keys can hash to the same index and overwrite each other unless the array is sized to hold every possible key.
- **Chaining fix** — use a smaller array and store objects in a **linked list at index `hash(key) % array_length`**; lookup searches that linked list for the key.
- **BST alternative** — implement the hash table on top of a balanced **binary search tree** for guaranteed `O(log n)` lookup and lower up-front space (no large array pre-allocation).
- **Interview priority** — one of the most common interview data structures; practice both *implementing* and *using* them, because the need for a hash table is often implicit, not stated.

**Java usage example** — a `HashMap<Integer, Student>` populated by iterating `students` and calling `map.put(s.getId(), s)`.

## 3. ArrayList (Dynamically Resizing Array)

- **Definition** — an array that resizes itself as needed while still providing `O(1)` access.
- **Typical implementation** — when the underlying array is full, allocate a new array of **double the size** and copy elements over.
- **Amortized cost** — each doubling is `O(n)`, but doublings are rare enough that the amortized insertion time remains `O(1)`.

## 4. StringBuffer

- **Problem with naive concatenation** — repeatedly doing `sentence = sentence + w` copies the whole accumulated string on every iteration.
- **Cost analysis** — iteration k copies `k*x` characters; total work is `x + 2x + ... + nx`, which reduces to `O(xn²)` (since `1 + 2 + ... + n = n(n+1)/2`, i.e. `O(n²)`).
- **`StringBuffer` fix** — internally keeps an array of the appended strings and only copies them into a final string when `toString()` is called, avoiding the quadratic copy.
- **Usage pattern** — construct a `StringBuffer`, loop and call `sentence.append(w)`, then return `sentence.toString()`.
- **Recommended exercise** — implement your own `StringBuffer` to practice strings, arrays, and general data structures.
