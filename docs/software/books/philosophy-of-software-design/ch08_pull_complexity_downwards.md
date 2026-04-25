# Ch 8: Pull Complexity Downwards

## Table of Contents

- [1. The Core Principle](#1-the-core-principle)
- [2. Example: Editor Text Class](#2-example-editor-text-class)
- [3. Configuration Parameters](#3-configuration-parameters)
- [4. When It Goes Too Far](#4-when-it-goes-too-far)

## 1. The Core Principle

- **Developer suffers so users don't have to** — when unavoidable complexity exists, the module developer should handle it internally rather than pushing it onto callers; modules have more users than developers, so the pain is multiplied when users bear it
- **Simple interface over simple implementation** — it is more important for a module to have a simple interface than a simple implementation; a harder implementation that produces a clean interface reduces overall system complexity
- **The temptation** — it's easy to solve the simple parts and punt the hard ones to callers (throw an exception, add a configuration parameter); this feels productive but amplifies complexity because many people must now deal with the problem instead of one

## 2. Example: Editor Text Class

- **Line-oriented API pushes complexity up** — students who chose a line-oriented interface (methods to read, insert, and delete whole lines of text) had a simpler implementation, but every caller had to split and join lines for common operations like mid-line insertion or multi-line deletion
- **Character-oriented API pulls complexity down** — `insert(string, position)` and `delete(start, end)` move line-splitting logic into the text class; the implementation is more complex, but the overall system is simpler because the complexity is encapsulated once rather than duplicated across all callers

## 3. Configuration Parameters

- **Configuration parameters push complexity upward** — instead of determining behavior internally, the class exports knobs (cache size, retry count) and forces users or administrators to figure out the right values
- **When parameters seem justified** — users sometimes know more about their domain than low-level code (e.g., request priorities); in those cases, configuration parameters can improve performance
- **Usually avoidable** — in many cases the system can compute a reasonable value itself. E.g., a network protocol can measure response times and derive a retry interval dynamically, rather than making the administrator guess a static value
- **Before exporting a parameter, ask:** "will users (or higher-level modules) be able to determine a better value than we can determine here?" If not, compute a default and eliminate the parameter
- **Configuration parameters = incomplete solution** — each parameter is an admission that the module hasn't fully solved its problem, and the parameter itself adds cognitive load for every user or administrator

## 4. When It Goes Too Far

- **Not all complexity should be pulled down** — pulling complexity downward makes sense only when: (a) it is closely related to the class's existing functionality, (b) it simplifies many callers, and (c) it simplifies the class's interface
- **Counter-example** — adding user-interface knowledge (e.g., a "backspace" method) to the text class doesn't simplify higher-level code much and leaks unrelated information into the text abstraction, causing information leakage rather than a net gain
- **The goal is minimum overall system complexity**, not maximum complexity inside a single module
