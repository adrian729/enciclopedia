# Ch 10: Stacks and Queues

## Table of Contents

- [1. Scope](#1-scope)
- [2. Implementing a Stack](#2-implementing-a-stack)
- [3. Implementing a Queue](#3-implementing-a-queue)
- [4. Stack vs. Queue at a glance](#4-stack-vs-queue-at-a-glance)

## 1. Scope

- **Comfort with fundamentals** — like linked list questions, stack and queue problems are much easier if you are comfortable with the ins and outs of the data structure.
- **Difficulty range** — some problems are slight modifications of the base data structure; others impose much more complex challenges.

## 2. Implementing a Stack

- **Ordering** — a stack uses **LIFO (last-in first-out)** ordering. Like a stack of dinner plates, the most recent item added is the first to be removed.
- **Linked list backing** — a stack can be implemented with a linked list; they are essentially the same thing, except a stack usually prevents the user from "peeking" at items below the top node.
- **Core members** — a `Node top` pointer and three operations: `push`, `pop`, and `peek`.
- **`push(item)`** — create `Node t = new Node(item)`, set `t.next = top`, then `top = t`.
- **`pop()`** — if `top != null`, save `top.data`, advance `top = top.next`, and return the saved item; otherwise return `null`.
- **`peek()`** — return `top.data` without modifying the stack.

## 3. Implementing a Queue

- **Ordering** — a queue implements **FIFO (first-in first-out)** ordering. Like a line at a ticket stand, items are removed in the same order they were added.
- **Linked list backing** — a queue can also be implemented with a linked list, with new items added to the **tail**.
- **Core members** — two pointers, `Node first` (head) and `Node last` (tail), plus `enqueue` and `dequeue`.
- **`enqueue(item)`** — if `first == null`, create `last = new Node(item)` and set `first = last`; otherwise append via `last.next = new Node(item)` and advance `last = last.next`.
- **`dequeue()`** — if `first != null`, save `first.data`, advance `first = first.next`, and return the saved item; otherwise return `null`.

## 4. Stack vs. Queue at a glance

| Property | Stack | Queue |
|----------|-------|-------|
| Ordering | LIFO (last-in first-out) | FIFO (first-in first-out) |
| Insert op | `push` | `enqueue` |
| Remove op | `pop` | `dequeue` |
| Pointer(s) | `top` | `first`, `last` |
| Remove from | top of list | head (`first`) |
| Insert at | top of list | tail (`last`) |
| Peek access | top node only | (not shown in intro) |
