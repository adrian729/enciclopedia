# Category Theory

## Table of Contents

- [1. What is a Category?](#1-what-is-a-category)
  - [1.1. Abstraction](#11-abstraction)
  - [1.2. Category](#12-category)
  - [1.3. Composition](#13-composition)
  - [1.4. Identity](#14-identity)
  - [1.5. Associativity](#15-associativity)
  - [1.6. Example: category theory in programming](#16-example-category-theory-in-programming)
- [2. Functions](#2-functions)
  - [2.1. What are functions?](#21-what-are-functions)
  - [2.2. Functions in Category Theory](#22-functions-in-category-theory)
    - [2.2.1. Epic Morphisms: Epimorphism](#221-epic-morphisms-epimorphism)
    - [2.2.2. Monic Morphisms: Monomorphism](#222-monic-morphisms-monomorphism)
    - [2.2.3. Disclaimer: isomorphism in category theory](#223-disclaimer-isomorphism-in-category-theory)
    - [2.2.4. Haskell objects and function examples](#224-haskell-objects-and-function-examples)
- [3. Categories](#3-categories)
  - [3.1. Zero](#31-zero)
  - [3.2. One object](#32-one-object)
  - [3.3. Graph (more objects)](#33-graph-more-objects)
  - [3.4. Orders](#34-orders)
    - [3.4.1. Pre-Order](#341-pre-order)
    - [3.4.2. Partial-Order](#342-partial-order)
    - [3.4.3. Total-Order](#343-total-order)

## 1. What is a Category?

### 1.1. Abstraction

- **objects**: primitive for category theory (no properties or anything).
- **arrows or morphisms**: other primitive. Goes from one object to another (start - end).

**Example:**

```
f: a -> b
```

- objects `a` and `b`
- `f` arrow/morphism from `a` to `b`

### 1.2. Category

Bunch of `objects`, and for each pair of objects 0 or more `arrows` between one and another or from one object to itself.

### 1.3. Composition

If we have:

```
f: a -> b
```

```
g: b -> c
```

then an arrow exists from `a` to `c` called `g after f`.

```
g∘f: a -> c
```

And `g∘f` is identical to the **composition** of `f` and `g`.

\* _There can be any number of other arrows `a -> c`, but if `f: a -> b` and `g: b -> c` then `g∘f` EXISTS._

### 1.4. Identity

For every object `a`, there EXISTS an arrow from it to itself, the `identity`.

<code>
id<sub>a</sub>: a -> a
</code>

 <br>

Having `f: a -> b`

---

**left identity**

<code>
id<sub>b</sub>∘f: a -> b -> b
</code>

<br>

where <code>id<sub>b</sub>∘f = f</code>

---

**right identity**

<code>
f∘id<sub>a</sub>: a -> a -> b
</code>

<br>

where <code>f∘id<sub>a</sub> = f</code>

### 1.5. Associativity

Having

```
f: a -> b
g: b -> c
h: c -> d
```

We can say that `h∘(g∘f)` and `(h∘g)∘f` are isomorphic

```
h∘(g∘f) = (h∘g)∘f = h∘g∘f
```

### 1.6. Example: category theory in programming

An example of category in programming: `types` and `methods`.

The `types` are the objects and the `methods` the arrows or functions.

We can see `types` as `sets of values` and `methods` as `functions` between sets.

When working with category theory, we need to forget the properties of sets and functions. We are building an abstraction on top of it, all we care about is `objects` and `arrows`.

## 2. Functions

### 2.1. What are functions?

(We will start focusing on mapping sets into each other to make it easier).

Functions are defined in mathematics as special kinds of relations between elements.

**Concepts**

- `Domain` of the function: set of elements the function goes from.
- `Codomain`: set of elements the function goes to.
  - `Image`: subset of the `codomain` obtained by mapping the whole `domain`.
- `Directionality`: Functions have `direction`, mapping from their `domain` to their `codomain`.

---

**Definition: inverse of a function, isomorphism**

`f :: a -> b` is `invertible`

if there exists a function 

`g :: b -> a`

where

<code>
  g∘f = id<sub>a</sub>
  <br>
  f∘g = id<sub>b</sub>
</code>

<br>

An `invertible` function is called an `isomorphism`.

`Isomorphisms` or `invertible functions` are `symmetric`.

---

Reasons some (or most) functions are not `isomorphisms`:

- The function collapses (several elements from the `domain` map to the same element in the `codomain`).
- Not all elements of the `codomain` are part of the `image` of the `domain` (_the `codomain` is "bigger" than the `domain`_). 

___

**Definition: injective function**

If a function does NOT collapse, it is injective.

For all <code>x<sub>1</sub></code> <code>x<sub>2</sub></code>: <code>f x<sub>1</sub> !=  f x<sub>2</sub></code>.

---

---

**Definition: surjective function**

If the `image` of a function covers all the `codomain`, then it is `surjective`.

For all `y` in the `codomain`, there exists an `x` in the domain where `y = f x`

---

So, if a function is `injective` and `surjective`, it is an `isomorphism` (another definition for it).

**The Problem!**

This definitions work with sets. The issue is that in `category theory` we can't talk in terms of the elements of a category to define its properties!

### 2.2. Functions in Category Theory

#### 2.2.1. Epic Morphisms: Epimorphism

Having `f :: a -> b` and `g :: b -> c`,

For all objects `c` and all morphisms <code>g<sub>1</sub></code>, <code>g<sub>2</sub> :: b -> c</code>,

if <code>g<sub>1</sub>∘f = g<sub>2</sub>∘f</code>,

then <code>g<sub>1</sub> = g<sub>2</sub></code>

---

Analog to `surjective` functions for category theory.


#### 2.2.2. Monic Morphisms: Monomorphism

Having `f :: a -> b` and `h :: z -> a`

For all objects `z` and all morphisms <code>h<sub>1</sub></code>, <code>h<sub>2</sub> :: z -> a</code>,

if <code>f∘h<sub>1</sub> = f∘h<sub>2</sub></code>,

then <code>h<sub>1</sub> = h<sub>2</sub></code>

---

Analog to `injective` functions for category theory.

#### 2.2.3. Disclaimer: isomorphism in category theory

For sets, if a function is `injective` and `surjective`, then we can say it is an `isomorphism`.

The same can't be said for a category if it is a `monomorphism` and an `epimorphism`!

That is not enough to say it is an `isomorphism`!

#### 2.2.4. Haskell objects and function examples

- `void`: type in haskell that represents _nothing_
- `absurd :: void -> a`
- `unit`: `() :: ()` in haskell.
- `unit :: a -> ()`: haskell unit function (gets anything, returns unit).
- `() -> a`: since it's pure functions, for each element `a` we need a different function.
  - f.e. `one :: () -> 1`, `two :: () -> 2`, `three :: () -> 3`, etc..
  - f.e. `True :: () -> true`, `False :: () -> false`

## 3. Categories

### 3.1. Zero

Category with no objects.

It fulfills the conditions because "for every pair of objects there is an arrow", since there are no objects (or arrows) it fullfils.

### 3.2. One object

Category with one object.

Will have a single object, and a single arrow, the identity `Id: a -> a`.

### 3.3. Graph (more objects)

After one object, we can start adding objects and arrows.

But is any graph a category? No it is not, but we can transform any graph into a category by adding arrows:

1. Add the `Identity` arrows for each object.
2. Adding composition arrows:
<br>
If we have `f: a -> b` and `g: b -> c`,
<br>
there should exist an arrow `g∘f: a -> c`
3. Adding the composition arrows of the compositions we just added (and keep going for the new arrows generated, until all compositions are satisfied).

With this we create a `free category` from the graph (only following the rules to satisfy the definition of category).

### 3.4. Orders

In a category that is an order, arrows don't represent functions, they represent relations.

`f: a -> b` means `a` less or equal to `b`, `a ≤ b`

Depending on which conditions they fulfill we can have different types of order.

#### 3.4.1. Pre-Order

Order that satisfies just the minimum of conditons:

**Reflexibity**

`a ≤ a` (Identity)

**Composition**

So if `a ≤ b` and `b ≤ c`,
<br>
then `a ≤ c`

**Associativity**

If `a ≤ b`, `b ≤ c`, and `c ≤ d`,
<br>
then `(a ≤ b) ≤ c` is the same as `a ≤ (b ≤ c)`

A `pre-order` is the same as a `thin category`.

The set of arrows between any two objects is called the `hom-set`.

It's a set of arrows. A `thin category` is one in which every `hom-set` is either an `empty set` or a `singleton set`.


#### 3.4.2. Partial-Order


#### 3.4.3. Total-Order

