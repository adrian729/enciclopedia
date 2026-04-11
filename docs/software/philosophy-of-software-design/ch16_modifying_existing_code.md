# Ch 16: Modifying Existing Code

## Table of Contents

- [1. Stay Strategic](#1-stay-strategic)
- [2. Maintaining Comments: Keep Them Near the Code](#2-maintaining-comments-keep-them-near-the-code)
- [3. Comments Belong in the Code, Not the Commit Log](#3-comments-belong-in-the-code-not-the-commit-log)
- [4. Maintaining Comments: Avoid Duplication](#4-maintaining-comments-avoid-duplication)
- [5. Maintaining Comments: Check the Diffs](#5-maintaining-comments-check-the-diffs)
- [6. Higher-Level Comments Are Easier to Maintain](#6-higher-level-comments-are-easier-to-maintain)

## 1. Stay Strategic

- **Tactical mindset when modifying code** — developers tend to ask "what is the smallest change I can make?" This introduces special cases, dependencies, and complexity with every modification
- **Design as if you knew from the start** — after each change, the system should look as though it was designed with that change in mind from the beginning. This requires resisting quick fixes and considering whether the current design still fits
- **Investment mindset** — spend a little extra time refactoring during each change. You'll recoup the cost through a cleaner system that's faster to work with later
- **If you're not making the design better, you're probably making it worse** — even if a particular change doesn't require refactoring, look for nearby design imperfections you can fix while you're in the code
- **Pragmatic limits** — sometimes a 3-month refactoring isn't feasible against a tight deadline. In those cases, look for a middle path (an almost-as-clean approach doable in days), or schedule time to come back. Every organization should budget a fraction of effort for cleanup

## 2. Maintaining Comments: Keep Them Near the Code

- **Proximity = visibility** — the best way to ensure comments get updated is to place them close to the code they describe. Developers will see them when modifying nearby code and update them naturally
- **Interface comments next to the method body** — in languages with separate header files (C/C++), placing interface comments in the `.h` file puts them far from the implementation. Developers won't see them when changing the method body. IDEs and doc tools (Doxygen, Javadoc) can surface comments regardless of placement, so optimize for the developer editing the code
- **Spread implementation comments throughout the method** — don't lump all comments at the top. Push each comment down to the narrowest scope that covers the relevant code. A high-level strategy comment at the top is fine, but phase-by-phase details belong next to the code for each phase
- **Distance and abstraction** — the farther a comment is from the code it describes, the more abstract it should be, reducing the chance that code changes will invalidate it

## 3. Comments Belong in the Code, Not the Commit Log

- **Commit messages are hard to find** — developers who need context about a subtle bug fix or design decision are unlikely to think of scanning the revision history, and even if they do, finding the right message is tedious
- **Document rationale in the code** — if a commit message explains why a change was made (e.g., a subtle bug it fixes), put that information in a code comment. Otherwise a future developer may undo the change and reintroduce the bug
- **Duplicating to commit log is fine** — just make sure the primary location is the code itself, where developers will actually encounter it

## 4. Maintaining Comments: Avoid Duplication

- **Document each design decision exactly once** — duplication makes it harder to find and update all copies. Pick the most natural single location (e.g., a variable's declaration for behavior that affects multiple usage sites)
- **Use cross-references for secondary locations** — add short comments like "See the comment in xyz for an explanation" rather than repeating the documentation. If the reference becomes stale, the staleness is self-evident and fixable
- **Don't redocument another module's decisions** — don't put comments before a method call explaining what the called method does. Readers can look at the method's own interface comment; good IDEs surface it automatically
- **Reference external documentation** — if a protocol (e.g., HTTP) or feature is already documented elsewhere (spec, user manual, web), don't repeat it. Add a short comment with a URL or pointer instead

## 5. Maintaining Comments: Check the Diffs

- **Pre-commit scan** — before committing, review all changes and verify that each one is properly reflected in the documentation. This also catches stale TODOs and leftover debugging code

## 6. Higher-Level Comments Are Easier to Maintain

- **Abstract comments survive code changes** — higher-level comments that describe overall behavior or intent are not affected by minor code edits, only by changes in overall behavior
- **The most useful comments are also the easiest to maintain** — comments that don't simply repeat the code (i.e., the ones developers actually need) tend to be abstract enough that they rarely go stale
