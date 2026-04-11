# Ch 17: Consistency

## Table of Contents

- [1. Why Consistency Matters](#1-why-consistency-matters)
- [2. Examples of Consistency](#2-examples-of-consistency)
- [3. Ensuring Consistency](#3-ensuring-consistency)
- [4. Taking It Too Far](#4-taking-it-too-far)

## 1. Why Consistency Matters

- **Cognitive leverage** — once you learn how something is done in one place, you can immediately understand other places that use the same approach. Without consistency, each situation must be learned separately
- **Fewer mistakes** — in an inconsistent system, two situations may look alike but behave differently, leading to incorrect assumptions. Consistency makes pattern-based reasoning safe
- **Speed** — developers work more quickly when they can rely on familiar patterns instead of analyzing every case from scratch
- **Investment mindset** — consistency requires upfront work (defining conventions, building automated checkers, studying existing code, thorough code reviews) but the payoff is code that is more obvious, allowing developers to work faster with fewer bugs

## 2. Examples of Consistency

| Level | Example |
|-------|---------|
| **Names** | Using names in a consistent way across the codebase (see Ch 14) makes code predictable and searchable |
| **Coding style** | Style guides (indentation, brace placement, naming, commenting) make code easier to read and reduce certain kinds of errors |
| **Interfaces** | An interface with multiple implementations is inherently consistent — understanding one implementation tells you the features any other must provide |
| **Design patterns** | Generally-accepted solutions (e.g., MVC) let teams proceed faster, produce more reliable code, and make the system more obvious to readers already familiar with the pattern |
| **Invariants** | A property that is always true (e.g., every line ends with a newline) eliminates special cases and makes it easier to reason about behavior |

## 3. Ensuring Consistency

- **Document conventions** — write down the most important conventions (coding style, project-wide rules) and place them somewhere visible (e.g., project wiki). Encourage new members to read the document and existing members to review it periodically
- **Document local conventions in the code** — for invariants and module-specific conventions, put the documentation in an appropriate spot in the source code. If conventions aren't written down, others won't follow them
- **Enforce with automated tools** — checkers that run before commit are the most reliable way to enforce conventions. A pre-commit script that catches violations (e.g., wrong line-termination characters) instantly eliminates recurring problems and trains new developers
- **Code reviews** — another enforcement opportunity. Nit-picky reviewers accelerate the team's learning of conventions and keep the codebase clean
- **"When in Rome, do as the Romans do"** — the most important convention. When working in existing code, study how it's structured (declaration order, naming style, patterns) and follow the same approach. Before making a design decision, check whether a similar decision was made elsewhere and mimic it
- **Don't change existing conventions** — having a "better idea" is not sufficient reason to introduce inconsistency. The value of consistency almost always outweighs the value of one approach over another. Only change a convention if (1) you have significant new information that wasn't available when it was established, and (2) the new approach is so much better that it's worth updating all existing uses. After migrating, no trace of the old convention should remain

## 4. Taking It Too Far

- **Dissimilar things should look different** — consistency means similar things are done similarly *and* dissimilar things are done differently. Forcing unrelated concepts into the same pattern (e.g., reusing a variable name for something semantically different, or shoehorning a problem into an ill-fitting design pattern) creates confusion
- **Confidence depends on honesty** — consistency only works when developers can trust that "if it looks like an *x*, it really is an *x*." Overzealous consistency destroys that trust
