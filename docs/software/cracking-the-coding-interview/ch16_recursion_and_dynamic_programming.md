# Ch 16: Recursion and Dynamic Programming

## Table of Contents

- [1. Recognizing recursive problems](#1-recognizing-recursive-problems)
- [2. How to approach recursive problems](#2-how-to-approach-recursive-problems)
- [3. Bottom-up vs. top-down recursion](#3-bottom-up-vs-top-down-recursion)
- [4. Dynamic programming](#4-dynamic-programming)
- [5. Recursive vs. iterative solutions](#5-recursive-vs-iterative-solutions)

## 1. Recognizing recursive problems

- **Built from sub-problems** — a good hint that a problem is recursive is that it can be built off of sub-problems.
- **Common phrasings** — problems starting with "Design an algorithm to compute the nth …", "Write code to list the first n …", or "Implement a method to compute all …" are often (though not always) good candidates for recursion.
- **Practice makes perfect** — the more recursive problems you solve, the easier recognition becomes.

## 2. How to approach recursive problems

- **Solutions built off sub-problems** — by definition, a recursive solution is built off solutions to sub-problems. Often this means computing `f(n)` by adding something to, removing something from, or otherwise changing the solution for `f(n-1)`; sometimes the transformation is more complex.
- **Consider both directions** — always consider both **bottom-up** and **top-down** recursive solutions.
- **Base Case and Build** — the approach from Chapter 6 works well for recursive problems.

## 3. Bottom-up vs. top-down recursion

| Style | Idea |
|-------|------|
| **Bottom-Up Recursion** | Solve a simple base case (e.g. a list with one element), then figure out how to solve two elements, then three, and so on — each case *built* off the previous. Often the most intuitive. |
| **Top-Down Recursion** | Divide the problem for case N into sub-problems. Can be more complex but is sometimes necessary. **Watch for overlap** between the cases. |

## 4. Dynamic programming

- **Rarely asked in interviews** — DP problems are too difficult for a 45-minute interview; even good candidates generally do poorly on them, so they're not a good evaluation technique.
- **Treat DP as recursion plus caching** — approach a DP problem much the same way as a recursion problem; the only difference is that intermediate results are "cached" for future calls.
- **Naive Fibonacci is O(2ⁿ)** — the recursive definition `fib(i) = fib(i-1) + fib(i-2)` makes two recursive calls per invocation, giving exponential runtime; on a standard desktop, seconds-to-compute grows steeply past ~n = 40.
- **Cached Fibonacci is O(N)** — store each `fib[i]` in an array and return the cached value when available:

```java
int[] fib = new int[max];
int fibonacci(int i) {
    if (i == 0) return 0;
    if (i == 1) return 1;
    if (fib[i] != 0) return fib[i]; // Return cached result.
    fib[i] = fibonacci(i - 1) + fibonacci(i - 2); // Cache result
    return fib[i];
}
```

- **Speedup is dramatic** — the naive version can take over a minute to generate the 50th Fibonacci number; the cached version generates the 10,000th in fractions of a millisecond (though with plain `int` it would overflow much earlier).
- **Implementation tip** — write a DP problem first as a normal recursive solution, then add the caching step.

## 5. Recursive vs. iterative solutions

- **Recursion costs stack space** — each recursive call adds a layer to the stack; an algorithm with O(n) recursive calls uses O(n) memory.
- **All recursion can be rewritten iteratively**, though the iterative version is sometimes much more complex.
- **Discuss the trade-off** — before diving into recursive code, ask how hard it would be to write iteratively and discuss the trade-offs with your interviewer.
