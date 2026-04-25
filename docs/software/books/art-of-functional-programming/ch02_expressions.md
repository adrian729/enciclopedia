# Ch 2: Expressions – Building Blocks of Functional Programs

## Table of Contents

- [1. Everything is an Expression](#1-everything-is-an-expression)
- [2. The Power of Combination](#2-the-power-of-combination)
- [3. Syntax of Expressions](#3-syntax-of-expressions)
- [4. Parsing](#4-parsing)
- [5. Types of Expressions](#5-types-of-expressions)
- [6. Values of Expressions](#6-values-of-expressions)
- [7. Names as Abstraction](#7-names-as-abstraction)

## 1. Everything is an Expression

- **Two worlds in imperative languages** — John Backus observed that imperative languages split their elements into *expressions* (constructs that evaluate to values: `1 + 2`, `true || false`) and *statements* (commands that perform side effects: variable assignments, if-statements, loops). This split is the root cause of limited composability in imperative code
- **FP eliminates statements entirely** — there are no variable assignments, no if-statements, no for/while loops. Instead, values are passed via function arguments and return values, conditionals are expressions that produce results, and repeated computation uses recursion. This means every piece of an FP program evaluates to a value and can be composed with any other piece
- **If as an expression** — `if e1 then e2 else e3` evaluates to a value, not a side effect. The `else` branch is mandatory because the whole construct must produce a result regardless of the condition — unlike imperative `if` where the else branch can be omitted since it just controls flow

## 2. The Power of Combination

- **Lego analogy** — primitive expressions (literals like `1`, `true`) combine into compound expressions, which combine into larger expressions, without limit. The power comes from the fact that any expression can appear anywhere another expression is expected
- **Expressions compose, statements don't** — because `if` is an expression in FP, you can use it directly as an operand: `(if 1 > 2 then 0 else 42) + 1`. In imperative languages where `if` is a statement, this is impossible — you'd need a temporary variable and multiple lines. This is a small example, but it illustrates a fundamental advantage: FP's exclusive reliance on expressions unlocks unlimited composability

## 3. Syntax of Expressions

- **BNF notation** — a concise formal grammar for specifying which input strings are valid programs. OCaml's expression grammar includes: number literals, unary operator applied to an expression, binary operator between two expressions, and `if-then-else` with three sub-expressions. These few rules specify the syntax of some of the OCaml expressions
- **Hierarchical tree structure** — every expression has a tree structure derived from applying syntactic rules. E.g., `1 + 2 * 3` produces a tree where `*` binds tighter than `+`, making `2 * 3` the right operand of `+`. This tree structure is what the compiler actually works with, not the flat string
- **Natural language analogy** — just as English builds sentences from words via grammar rules (nouns → noun phrases → sentences), programming languages build expressions from literals and operators via syntactic rules. The BNF rules for OCaml expressions play the same role as grammar rules in English

## 4. Parsing

- **Two-stage process** — mirrors how humans recognize English phrases:
  1. **Lexing (word recognition)** — scan the character sequence left-to-right, grouping characters into tokens (literals, operators, keywords). Fails on unrecognizable tokens, e.g., `1xyz` → "Invalid literal" — analogous to encountering a nonsense word like "qpr" in English
  2. **Parsing (structure recognition)** — verify that tokens are arranged according to grammar rules by building a parse tree. Fails on invalid arrangements, e.g., `1 +` → "Syntax error" because the binary operator is missing its right operand — analogous to "baby cute cat" violating English word-order rules
- **Abstract syntax tree (AST)** — a compact tree that captures an expression's essential structure, stripping away concrete details like whitespace, parentheses, and keywords. The compiler relies on the AST to further analyze expressions, such as type checking or code generation into bytecode or native code

## 5. Types of Expressions

- **Syntactic validity isn't enough** — `1 + true` is syntactically valid (matches the `expr binop expr` rule) but semantically nonsensical because `+` expects two numbers. Just like "cute table cat" passes English grammar rules but makes no real-world sense

| Typing approach | How it works | Trade-off |
|-----------------|-------------|-----------|
| **Dynamic typing** (JavaScript, PHP) | Type checking happens at runtime only. `1 + true` executes — JS silently coerces `true` to `1` and returns `2` | Maximum flexibility, but type errors hide until execution, sometimes surfacing as hard-to-debug runtime crashes in production |
| **Static typing** (OCaml, Haskell) | A type checker runs at compile time before the program ever executes. `1 + true` is rejected immediately | Less flexible, but catches an entire class of common mistakes (type mismatches) before the code ever runs |

- **Type inference** — OCaml's type checker doesn't require explicit type annotations. It infers types by propagating them up the AST from leaves to root using recursive rules (e.g., `int + int → int`, `int > int → bool`). This gives the safety of static typing without the verbosity of writing types everywhere
- **If expression typing** — the condition must be `bool`; both branches must have the *same* type; the result type equals the branch type. This prevents subtle bugs where one branch returns a number and the other a string
- **Layered validation** — the parser reduces all input strings to syntactically valid expressions; the type checker further reduces those to type-correct expressions. Only expressions passing *both* layers are compiled. This two-layer funnel catches progressively subtler errors

## 6. Values of Expressions

- **Syntax vs. semantics** — syntax defines which character combinations form valid programs; semantics defines their *meaning*. The string `12 + 34` is syntax; the number `46` is semantics. Understanding this distinction is fundamental when learning any programming language or debugging errors

| Language class | How values are produced |
|----------------|----------------------|
| **Interpreted** (JavaScript, Python) | An interpreter walks the AST recursively, evaluating from leaves upward — primitive nodes return their values, operator nodes combine their children's values |
| **Compiled** (OCaml, Haskell, Java) | A code generator translates the AST into bytecode or native machine code; a bytecode runner or the CPU executes it. OCaml provides both `ocamlc` (bytecode) and `ocamlopt` (native code) |

- **Recursive evaluation** — both interpretation and type inference follow the same recursive pattern over the AST. This is no coincidence: expressions have hierarchical structure, so any algorithm that processes them naturally recurses over that structure

## 7. Names as Abstraction

- **`let` binding is not variable assignment** — in imperative languages, a variable names a memory cell whose content changes over time via assignment. In FP, `let pi = 3.14` permanently associates the name `pi` with the value `3.14` — it creates an *abstraction*, a self-contained conceptual unit that cannot be mutated. Attempting `pi = pi + 1` in OCaml is a boolean comparison (evaluating to `false`), not an update
- **Chunking** — naming mirrors how humans build knowledge hierarchically: "giving" → "trading" → "buying/selling" → "market" → "economy." Each name compresses a complex concept into a single unit that can participate in higher-level reasoning. FP's `let` binding works the same way — once `circle_area` is defined, you think of it as one concept, not as the arithmetic it expands to
- **`let ... in` for local scope** — `let radius = 2.0 in pi *. radius *. radius` limits the name `radius` to the enclosing expression only, invisible outside. `let ... in` is itself an expression (it evaluates to a value) and can be arbitrarily nested, allowing you to build up local abstractions within any computation
