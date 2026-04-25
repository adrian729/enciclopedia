# Ch 3: Building Abstractions with Functions

## Table of Contents

- [1. Lambda Calculus – Foundation of Functional Programming](#1-lambda-calculus--foundation-of-functional-programming)
- [2. Function Abstraction and Application in OCaml](#2-function-abstraction-and-application-in-ocaml)
- [3. Currying and Partial Application](#3-currying-and-partial-application)
- [4. Recursive Functions](#4-recursive-functions)
- [5. Higher-Order Functions](#5-higher-order-functions)

## 1. Lambda Calculus – Foundation of Functional Programming

### 1.1. Lambda Expressions

- **Lambda calculus** — an idealized bare-bones functional programming language invented by Alonzo Church, serving as the theoretical foundation for all functional programming languages. Strip away every non-essential feature from OCaml or Haskell and what remains is essentially lambda calculus
- **Three construction rules** — every lambda expression is built from exactly three forms: a variable (`x`, `y`), a function abstraction (`λx. e`, declaring a function of one argument), or a function application (`e1 e2`, applying one expression to another). Despite this extreme minimalism, lambda calculus is as powerful as any general-purpose language — it can encode numbers, booleans, pairs, lists, and more via Church encoding

### 1.2. Lambda Reduction

- **Reduction as execution** — running a lambda calculus program means reducing its expression until no further reduction is possible; the fully reduced form is the program's value
- **Redex (reducible expression)** — a function application `(λx. e1) e2` can be reduced by substituting `x` with `e2` in `e1`. A variable or a function abstraction alone is already fully reduced
- **Non-termination is possible** — some lambda expressions never reach a fully reduced form, e.g., `(λx. x x)(λx. x x)` reduces to itself endlessly. This mirrors how programs in any language can loop forever

### 1.3. Functions as First-Class Citizens

- **No distinction between variables and functions** — in lambda calculus, both are expressions. Functions can be passed as arguments to other functions or returned from them, just like numbers or strings. This property is called being a *first-class citizen*
- **Imperative languages treat functions as second-class** — in languages like C or Java, functions cannot be stored in variables, passed as arguments, or returned from other functions in the same way values can. This limits composability
- **Foundation for higher-order functions** — treating functions as first-class citizens is the enabler for higher-order functions, a hallmark of functional programming

### 1.4. Currying

- **Multi-argument functions via nesting** — lambda calculus only supports single-argument functions, yet multi-argument functions are represented as nested chains of single-argument functions: `λx.λy. f x y`. This technique is called *currying*, named after logician Haskell Brooks Curry
- **Partial application** — because a multi-argument function is really a chain, you can apply it to fewer arguments than expected and obtain a new function with the remaining parameters. For example, applying `λx.λy. f x y` to just `u` yields `λy. f u y`, a specialized unary function

### 1.5. Reduction Strategies

- **Call-by-value (strict)** — evaluate the argument fully before substituting it into the function body. Used by OCaml, Java, C, Python, and most mainstream languages
- **Call-by-name (non-strict)** — substitute the argument expression as-is into the function body without evaluating it first. Used by Haskell

| Strategy | Behavior with unused argument | Behavior with undefined argument |
|----------|-------------------------------|----------------------------------|
| **Call-by-value** | Evaluates the argument anyway, wasting work or triggering errors (e.g., `(fun x -> 42)(1/0)` raises `Division_by_zero` in OCaml) | Non-termination — the runtime tries to evaluate the undefined argument forever |
| **Call-by-name** | Skips evaluation entirely since the argument is never needed (e.g., `(\x -> 42)(1/0)` returns `42` in Haskell) | May still terminate if the function body does not use the argument |

- **Confluence** — when both strategies terminate on the same expression, they always produce the same result. They differ only in evaluation order and in whether they terminate when undefined subexpressions are present

## 2. Function Abstraction and Application in OCaml

### 2.1. Function Declaration

- **`fun` keyword** — the OCaml equivalent of lambda `λ`. `fun x -> x *. x` declares an anonymous function (also called a *lambda function* or *arrow function*) that takes `x` and returns its square
- **Functions are expressions** — a function evaluates to a function value, just like `42` evaluates to an integer value. This is what it means for functions to be first-class citizens in OCaml, unlike Java where functions do not evaluate to values
- **Named functions via `let`** — since functions are normal expressions, `let square = fun x -> x *. x` binds a name to a function value. OCaml provides syntactic sugar: `let square x = x *. x`

### 2.2. Function Application

- **Juxtaposition syntax** — identical to lambda calculus: place the function and its argument side by side separated by a space, e.g., `square 2.` evaluates to `4.`
- **OCaml uses call-by-value** — the argument is always evaluated before substitution into the function body, matching the behavior of most mainstream languages
- **Haskell uses call-by-name** — the argument is substituted unevaluated, meaning it is only computed if actually needed. This can avoid errors on unused arguments but may duplicate work when an argument is used more than once

### 2.3. Function Types

- **Type signature `t1 -> t2`** — every function has a type describing its input and output. `square` has type `float -> float`. OCaml infers function types automatically through type inference, so explicit annotations are rarely needed
- **Nested function types** — `t1` or `t2` can themselves be function types, e.g., `int -> (bool -> string)` describes a function that takes an integer and returns a function from boolean to string. These nested types arise naturally from currying and higher-order functions
- **Types as contracts** — examining a function's type reveals its public contract (what it accepts and returns), which is often half the battle toward understanding what the function does

### 2.4. Functions as Black Box Abstractions

- **Abstraction over computation** — defining and naming a function like `square` creates a reusable building block capturing a general method of computation, not just a specific result
- **Composition** — named functions compose into larger functions (e.g., `circle_area r = pi *. (square r)`), just as built-in operators compose. From the client's perspective, the internal implementation is irrelevant — the function is a *black box*
- **Stepwise construction** — the central discipline of functional programming is recognizing opportunities to abstract computations into named functions, then composing those functions into progressively more complex programs

## 3. Currying and Partial Application

### 3.1. Multi-Argument Functions in OCaml

- **Syntactic sugar hides currying** — `let rectangle_area w h = w *. h` looks like a two-argument function but is actually syntactic sugar for `let rectangle_area = fun w -> fun h -> w *. h`, a chain of two single-argument functions
- **Right-associative `->` in types** — the type `int -> int -> int` is equivalent to `int -> (int -> int)`, meaning the function takes one integer and returns a function that takes another integer and returns an integer. OCaml's `+` operator, accessed as `(+)`, has exactly this type

### 3.2. Partial Application

- **Applying fewer arguments than expected** — because multi-argument functions are curried chains, applying `rectangle_area` to just one argument (e.g., `rectangle_area 2.`) yields a new unary function that computes the area for a fixed width of 2.0
- **Free function derivation** — partial application lets you derive specialized functions from general ones without writing new code: `let inc = (+) 1` creates an increment function from the addition operator; `let double = ( * ) 2` creates a doubling function from multiplication
- **Two-step view of application** — `rectangle_area 2.5 3.5` is more accurately read as `(rectangle_area 2.5) 3.5`: first apply to `2.5` to get a unary function, then apply that function to `3.5`. This mental model guides argument ordering decisions when designing multi-argument functions

## 4. Recursive Functions

### 4.1. Recursion Replaces Loops

- **No for/while in FP** — functional programming has no loop statements. Instead, repeated computation is expressed via *recursive functions* — functions that call themselves. The `rec` keyword marks a recursive function in OCaml
- **Mathematical definitions translate directly** — `sum(n) = 0` for `n = 0`, `n + sum(n-1)` for `n > 0` becomes `let rec sum n = if n <= 0 then 0 else n + sum (n-1)` in OCaml, a direct one-to-one translation
- **Stack overflow risk** — each recursive call pushes a frame onto the call stack to remember where to return. For naive recursion on large inputs (e.g., `sum 1000000`), the chain of deferred calculations grows linearly with `n` until the stack limit is exceeded

### 4.2. Tail-Recursive Functions

- **Tail recursion** — a recursive function is *tail-recursive* when its recursive call is the very last operation, with no additional computation wrapping it. `sum_iter (s + c) (c + 1) n` is tail-recursive because nothing is added to the result of the recursive call
- **No deferred calculations** — unlike naive recursion which builds up a chain like `5 + (4 + (3 + ...))`, a tail-recursive function carries its running result in an accumulator argument, so each step completes fully before the next begins
- **Constant stack usage** — because there is nothing to return to, the runtime does not need to push stack frames. `sum_iter 0 1 1000000` succeeds where `sum 1000000` overflows
- **Readability trade-off** — tail-recursive versions require extra accumulator arguments and are harder to read. For small inputs where stack overflow is not a concern, the naive recursive version is usually preferable

### 4.3. Tail-Recursion Optimization

- **Compiler support** — most functional languages such as OCaml and Haskell support *tail-recursion optimization*, meaning a tail-recursive function is executed without using a call stack. This makes recursion a viable replacement for loops — these languages do not need special-purpose loop constructs like `for` and `while`
- **Imperative languages lack this** — Java and most non-functional languages do not optimize tail calls. Any recursive function in Java pushes frames regardless of tail position, which is why those languages need dedicated `for`/`while` constructs for safe looping
- **Recursion as the universal loop** — with tail-recursion optimization, functional languages need no special loop constructs. An infinite tail-recursive function (e.g., `let rec endless () = print_endline "Hi recursion"; endless()`) runs forever without stack overflow in OCaml but crashes in Java

## 5. Higher-Order Functions

### 5.1. Summation as a Higher-Order Function

- **Higher-order function** — a function that accepts other functions as arguments or returns a function as its result. This is possible because functions are first-class citizens
- **Generalizing the summation pattern** — instead of writing separate functions for summing integers, summing squares, etc., a single higher-order function `sum term m n` accepts a `term` function that produces each element of the sum, plus bounds `m` and `n`. Different `term` functions yield different summations
- **Partial application for concise definitions** — `let sum_integers = sum (fun i -> i)` and `let sum_squares = sum (fun i -> i * i)` are defined by partially applying `sum` with just the term function, avoiding redundant bound parameters

### 5.2. Accumulation as a Higher-Order Function

- **Summation and product share a pattern** — both accumulate terms produced by a function within an interval; they differ only in the combining operation (`+` vs `*`) and initial value (`0` vs `1`)
- **`accumulate` factors out the common pattern** — `accumulate combiner init term m n` takes a binary combining function, an initial value, a term-producing function, and a range. Both `sum` and `product` become special cases: `let sum = accumulate (+) 0` and `let product = accumulate ( * ) 1`

### 5.3. Climbing the Abstraction Hierarchy

- **From concrete to general** — the progression goes: `sum_integers` / `sum_squares` (concrete) -> `sum` (general summation) -> `accumulate` (general accumulation). Each step upward captures a more general computation pattern, and every function below can be derived from the one above
- **Code reuse** — `accumulate` alone can express `sum`, `product`, `sum_integers`, `product_integers`, and any other accumulation-based computation, eliminating duplication
- **High-level vs. low-level thinking** — with `accumulate` available, solving "compute 1^3 + 2^3 + ... + n^3" becomes a matter of configuring parameters (`accumulate (+) 0 (fun x -> x * x * x) 1`) rather than manually writing recursion cases. The implementation details of `accumulate` are irrelevant at this abstraction level, freeing mental effort for the problem at hand
