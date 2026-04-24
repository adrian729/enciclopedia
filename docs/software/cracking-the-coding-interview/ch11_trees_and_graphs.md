# Ch 11: Trees and Graphs

## Table of Contents

- [1. Why these are tricky](#1-why-these-are-tricky)
- [2. Ambiguity to clarify up front](#2-ambiguity-to-clarify-up-front)
- [3. Tree terminology](#3-tree-terminology)
- [4. Tree traversal](#4-tree-traversal)
- [5. Balanced trees](#5-balanced-trees)
- [6. Tries](#6-tries)
- [7. Graph traversal: BFS vs. DFS](#7-graph-traversal-bfs-vs-dfs)

## 1. Why these are tricky

- **Trees and graphs are among the trickiest interview topics** — searching them is more complicated than searching a linearly organized structure like an array or linked list.
- **Worst-case and average-case time can vary wildly** — you must evaluate both aspects of any algorithm on these structures.
- **Implementing from scratch is essential** — fluency with building a tree or graph by hand is expected.

## 2. Ambiguity to clarify up front

Tree/graph questions are ripe for ambiguous details and incorrect assumptions. Always seek clarification on the following issues before coding.

- **Binary tree vs. Binary search tree** — many candidates assume the interviewer means binary *search* tree. Ask. A **binary search tree** imposes the condition that, for all nodes, the left children are less than or equal to the current node, which is less than all the right nodes.
- **Balanced vs. unbalanced** — not every tree is balanced. If unbalanced, describe your algorithm's **average and worst-case time** separately.
- **Balancing is not symmetry** — balancing implies only that **subtree depth does not vary by more than a certain amount**; it does *not* mean the left and right subtrees are the same size.

## 3. Tree terminology

| Term | Definition |
|------|------------|
| **Binary tree** | Tree where each node has up to two children |
| **Binary search tree (BST)** | Binary tree where left children ≤ current node < all right nodes |
| **Full and complete tree** | All leaves are at the bottom and all non-leaf nodes have exactly two children; requires exactly `2ⁿ - 1` nodes, so these are *extremely* rare |

## 4. Tree traversal

- **Be comfortable implementing in-order, post-order, and pre-order traversal** before your interview.
- **In-order traversal** is the most common — visits the left side, then the current node, then the right.
- **Pre-order and other tree traversals are a form of DFS** — the key difference for graphs is you must check whether a node has been visited to avoid infinite loops.

## 5. Balanced trees

- **Red-Black Trees and AVL Trees** — learning to implement a balanced tree may make you a better engineer, but it's **rarely asked in an interview**.
- **Know the runtime of operations on balanced trees** and be **vaguely familiar with how you might balance** one. Implementation details are unnecessary for interview prep.

## 6. Tries

- **A trie is a variant of an n-ary tree** in which characters are stored at each node.
- **Each path down the tree may represent a word** — useful for prefix-based lookups.

## 7. Graph traversal: BFS vs. DFS

Graph traversal is more challenging than tree traversal; **BFS is especially difficult** for most candidates. BFS and DFS are used in different scenarios.

| Aspect | **Depth First Search (DFS)** | **Breadth First Search (BFS)** |
|--------|------------------------------|--------------------------------|
| **How it visits** | From node `r`, iterate through adjacent nodes; for each adjacent `n`, exhaustively search all of `n`'s adjacent nodes before returning to `r`'s other children | Visit each of `r`'s adjacent nodes before searching any of `r`'s "grandchildren" |
| **Typical implementation** | Recursion | Iterative, with a **queue** |
| **Best for** | Visiting every node, or visiting every node until something is found | Finding something near the source when the tree is very large and you want to quit when too far from the origin |
| **Pitfall** | Can be problematic with very large trees — may descend into thousands of ancestors and never search the original node's children | Less intuitive; most interviewees struggle unless already familiar |
| **Intuition** | Natural extension of pre-order tree traversal | Driven entirely by the queue — the rest flows from that fact |

- **Mark nodes visited** — when applying DFS to a graph (not a tree), you must check `node.visited` before recursing or you risk an infinite loop.
- **BFS key implementation detail** — enqueue the root, mark it visited, then loop: dequeue, visit each unvisited neighbor, mark it visited, and enqueue it. If asked to implement BFS, **the key thing to remember is the use of the queue**.
