# Ch 9: Linked Lists

## Table of Contents

- [1. Why linked lists stump candidates](#1-why-linked-lists-stump-candidates)
- [2. Creating a Linked List](#2-creating-a-linked-list)
- [3. Deleting a Node from a Singly Linked List](#3-deleting-a-node-from-a-singly-linked-list)
- [4. The "Runner" Technique](#4-the-runner-technique)
- [5. Recursive Problems](#5-recursive-problems)

## 1. Why linked lists stump candidates

- **No constant-time access** — unlike arrays, you cannot jump to an index; every traversal is linear.
- **Heavy reliance on recursion** — many standard linked list problems are naturally recursive, which trips candidates up.
- **Low question variety** — most linked list problems are variants of a small set of well-known questions, so preparation pays off.
- **Fundamentals matter** — problems rely so heavily on core mechanics that you must be able to implement a linked list from scratch.

## 2. Creating a Linked List

- **Starting point** — a basic singly linked list built from a `Node` class with a `next` pointer and an `int data` field.
- **`appendToTail(int d)`** — creates a new `Node(d)` called `end`, walks a pointer `n` from `this` until `n.next == null`, then sets `n.next = end`.
- **Singly vs. doubly** — when discussing a linked list in an interview, you must understand and clarify whether it is **singly linked** or **doubly linked**.

## 3. Deleting a Node from a Singly Linked List

- **Basic procedure** — given a node `n`, find the previous node `prev` and set `prev.next = n.next`.
- **Doubly linked case** — also set `n.next.prev = n.prev` to keep the back-pointer chain intact.
- **Two things to remember** — (1) check for the **null pointer** and (2) update the **head or tail pointer** as necessary.
- **Manual memory management** — in C, C++, or similar languages, also consider whether the removed node should be deallocated.
- **Sample `deleteNode(head, d)`** — if `head.data == d`, return `head.next` (head moved); otherwise iterate, and when `n.next.data == d` set `n.next = n.next.next` and return the unchanged head.

## 4. The "Runner" Technique

- **Definition** — iterate the list with **two pointers simultaneously**, one ahead of the other by either a fixed amount or by a variable step (e.g., hopping multiple nodes per slow-pointer step).
- **Also called** — the *second pointer* technique.
- **Worked example — weaving a list** — given `a₁ → a₂ → … → aₙ → b₁ → b₂ → … → bₙ`, rearrange into `a₁ → b₁ → a₂ → b₂ → … → aₙ → bₙ` without knowing the length (only that it is even).
- **Weaving procedure** — move pointer `p1` two steps for every one step of `p2`; when `p1` reaches the end, `p2` sits at the midpoint. Then reset `p1` to the front and iterate: `p2` selects an element and inserts it after `p1`.

## 5. Recursive Problems

- **Frequent fit** — many linked list problems are easier to solve recursively; if an iterative approach stalls, try recursion.
- **Space cost** — recursive algorithms take at least `O(n)` space, where `n` is the depth of the recursive call.
- **Iterative equivalence** — every recursive algorithm *can* be implemented iteratively, although the iterative version may be much more complex.
- **Deferred depth** — recursion is covered in detail in a later chapter.
