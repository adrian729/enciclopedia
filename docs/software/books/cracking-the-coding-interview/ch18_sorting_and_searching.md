# Ch 18: Sorting and Searching

## Table of Contents

- [1. Framing](#1-framing)
- [2. Common sorting algorithms](#2-common-sorting-algorithms)
- [3. Merge Sort](#3-merge-sort)
- [4. Quick Sort](#4-quick-sort)
- [5. Radix Sort](#5-radix-sort)
- [6. Searching algorithms](#6-searching-algorithms)

## 1. Framing

- **Many problems are tweaks of known algorithms** — run through the sort catalog and see which one fits particularly well.
- **Leverage constraints** — e.g., "sort a very large array of `Person` objects by age" signals a small value range, making **bucket sort** (or **radix sort**) a candidate with buckets of 1 year each for `O(n)` runtime.
- **Most commonly used in interviews** — Merge Sort, Quick Sort, and Bucket Sort.

## 2. Common sorting algorithms

| Algorithm | Runtime (avg / worst) | Memory | How it works |
|-----------|-----------------------|--------|--------------|
| **Bubble Sort** | `O(n²)` / `O(n²)` | `O(1)` | Sweep the array; swap each out-of-order adjacent pair. Repeat sweeps until sorted. |
| **Selection Sort** | `O(n²)` / `O(n²)` | `O(1)` | The "child's algorithm": linear-scan for the smallest, swap to front; then the second smallest; repeat. Simple but inefficient. |
| **Merge Sort** | `O(n log n)` / `O(n log n)` | Depends | Divide array in half, sort each half, merge. The "merge" does the heavy lifting. |
| **Quick Sort** | `O(n log n)` / `O(n²)` | `O(log n)` | Pick a random partition element; place smaller elements before it and larger after via swaps. Recurse. Worst case when the partition is far from the median. |
| **Radix Sort** | `O(kn)` | — | For integers (and some other types): sort by each digit in turn, grouping by digit value. |

## 3. Merge Sort

- **Divide and conquer** — recursively split until subarrays are single elements, then merge.
- **Merge step** — copy the target segment into a **helper** array, then iterate with `helperLeft` and `helperRight` pointers, copying the smaller element back into the target.
- **Only remaining left-half elements need copying back** at the end — the right-half leftovers are already in place in the target array.

## 4. Quick Sort

- **Partition around a pivot** — all smaller elements come before, all greater come after, via a series of swaps.
- **Recursion** — apply the same partition to each side; repeated partitioning eventually sorts the array.
- **Worst-case `O(n²)`** — because the chosen partition element is not guaranteed to be near the median.

## 5. Radix Sort

- **Exploits bounded bit-width** — integers have a finite number of digits/bits, so digit-by-digit grouping works.
- **Process** — sort by the first digit (e.g., grouping all 0s together), then within each group sort by the next digit, and so on until all digits are processed.
- **Beats comparison sorts' `O(n log n)` bound** — runs in `O(kn)` where `n` is element count and `k` is the number of passes. Comparison sorts cannot do better than `O(n log n)` on average.

## 6. Searching algorithms

- **Binary search** is the canonical searching algorithm to know.
- **How it works** — compare `x` to the midpoint of a sorted array; if `x` is smaller, search the left subarray, else the right; repeat until found or the subarray has size 0.
- **Implementation detail warning** — getting the plus-ones and minus-ones right is harder than it looks. Both iterative and recursive forms are worth studying.
- **Think beyond binary search** — searching can also use a **binary tree** traversal or a **hash table** lookup; don't limit yourself to binary search when another structure fits.
