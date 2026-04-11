# Ch 2: The Nature of Complexity

## Table of Contents

- [1. Complexity Defined](#1-complexity-defined)
- [2. Symptoms of Complexity](#2-symptoms-of-complexity)
- [3. Causes of Complexity](#3-causes-of-complexity)
- [4. Complexity is Incremental](#4-complexity-is-incremental)

## 1. Complexity Defined

- **Complexity** — anything related to the structure of a software system that makes it hard to understand and modify
- **Cost/benefit framing** — in a complex system, even small improvements take a lot of work; in a simple system, large improvements come cheaply
- **It's relative to the developer**, not the system's size — a large system that's easy to work on is not complex; a small system that's hard to modify is
- **Weighted by usage** — overall complexity = each part's complexity weighted by how often developers touch it (`C = Σ(cp × tp)`). A gnarly module nobody touches barely matters; a mildly confusing module everyone edits daily dominates
- **Complexity is in the reader's eye** — if others find your code complex, it is complex. Your familiarity with it doesn't count

## 2. Symptoms of Complexity

| Symptom | What it looks like |
|---------|-------------|
| **Change amplification** | A seemingly simple change requires modifications in many different places. E.g., a banner color hardcoded in every page instead of stored in one shared variable |
| **Cognitive load** | A developer must hold too much context to complete a task — many API methods, global variables, implicit conventions, cross-module dependencies. Note: more lines of code can be *simpler* if it reduces what you need to keep in your head |
| **Unknown unknowns** | It's not obvious what code needs to change or what information you're missing. You don't know what you don't know — bugs surface only after the fact |

- **Unknown unknowns are the worst** — change amplification is tedious but at least you know what to touch; cognitive load is expensive but at least you know what to learn. With unknown unknowns, there's no way to discover the problem until something breaks
- **Goal: obviousness** — the antidote to all three symptoms. In an obvious system, a developer can quickly guess what to do, and be right

## 3. Causes of Complexity

| Cause | What it means | Leads to |
|-------|-------------|----------|
| **Dependencies** | A piece of code can't be understood or modified in isolation — changing it requires understanding or changing other code too (e.g., sender/receiver in a protocol, method signatures and all their callers) | Change amplification, cognitive load |
| **Obscurity** | Important information is not obvious — the relationship between pieces of code is hidden (e.g., a status enum that requires a matching entry in a separate string table, but nothing makes that connection visible) | Unknown unknowns, cognitive load |

- **Dependencies can't be eliminated**, only minimized — every API creates dependencies. The goal is to make them few, simple, and obvious. Replacing a non-obvious dependency (color hardcoded everywhere) with an obvious one (shared variable with a searchable name) is a win even though a dependency still exists
- **Obscurity sources** — generic variable names, missing units in docs, inconsistent naming that hides patterns, undocumented relationships between components
- **Needing lots of documentation = design smell** — the need for extensive documentation is often a red flag that the design isn't quite right. A clean design makes most things self-evident; the best way to reduce obscurity is by simplifying the system design

## 4. Complexity is Incremental

- **No single catastrophic error** — complexity accumulates in hundreds of small chunks: a dependency here, an obscurity there. Each one is easy to justify ("this little bit won't matter")
- **Hard to reverse** — once accumulated, fixing one dependency or obscurity doesn't visibly improve things, which discourages cleanup
- **Zero tolerance** — the only defense is refusing to accept "just a little" complexity with every change, because that's exactly how it grows
