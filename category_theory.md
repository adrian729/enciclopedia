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
    - [3.4.4. Epimorphisms, Monomorphisms and Isomorphisms](#344-epimorphisms-monomorphisms-and-isomorphisms)
  - [3.5. Monoid](#35-monoid)
  - [3.6. Kleisli Category](#36-kleisli-category)
    - [3.6.1. Arrows: Embellished Functions](#361-arrows-embellished-functions)
    - [3.6.2. Composition](#362-composition)
    - [3.6.3. Identity](#363-identity)
  - [3.7. Monad](#37-monad)
  - [3.8. Universal Constructions](#38-universal-constructions)
    - [3.8.1. Terminal Object](#381-terminal-object)
    - [3.8.2. Initial Object](#382-initial-object)

<a id="1-what-is-a-category"></a>

## 1. What is a Category?

<a id="11-abstraction"></a>

### 1.1. Abstraction

- **objects**: primitive for category theory (no properties or anything).
- **arrows or morphisms**: other primitive. Goes from one object to another (start - end).

**Example:**

```
f: a -> b
```

- objects `a` and `b`
- `f` arrow/morphism from `a` to `b`

<a id="12-category"></a>

### 1.2. Category

A collection of `objects`, and for each pair of objects 0 or more `arrows` between one and another or from one object to itself.

<a id="13-composition"></a>

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

<a id="14-identity"></a>

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

<a id="15-associativity"></a>

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

<a id="16-example-category-theory-in-programming"></a>

### 1.6. Example: category theory in programming

An example of category in programming: `types` and `methods`.

The `types` are the objects and the `methods` the arrows or functions.

We can see `types` as `sets of values` and `methods` as `functions` between sets.

When working with category theory, we need to forget the properties of sets and functions. We are building an abstraction on top of it, all we care about is `objects` and `arrows`.

<a id="2-functions"></a>

## 2. Functions

<a id="21-what-are-functions"></a>

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

---

**Definition: injective function**

If a function does NOT collapse, it is injective.

For all <code>x<sub>1</sub></code> <code>x<sub>2</sub></code>: <code>f x<sub>1</sub> != f x<sub>2</sub></code>.

---

---

**Definition: surjective function**

If the `image` of a function covers all the `codomain`, then it is `surjective`.

For all `y` in the `codomain`, there exists an `x` in the domain where `y = f x`

---

So, if a function is `injective` and `surjective`, it is an `isomorphism` (another definition for it).

**The Problem!**

This definitions work with sets. The issue is that in `category theory` we can't talk in terms of the elements of a category to define its properties!

<a id="22-functions-in-category-theory"></a>

### 2.2. Functions in Category Theory

<a id="221-epic-morphisms-epimorphism"></a>

#### 2.2.1. Epic Morphisms: Epimorphism

Having `f :: a -> b`,

For all objects `c` and all morphisms <code>g<sub>1</sub></code>, <code>g<sub>2</sub> :: b -> c</code>,

if <code>g<sub>1</sub>∘f = g<sub>2</sub>∘f</code>,

then <code>g<sub>1</sub> = g<sub>2</sub></code>

---

Analog to `surjective` functions for category theory.

<a id="222-monic-morphisms-monomorphism"></a>

#### 2.2.2. Monic Morphisms: Monomorphism

Having `f :: a -> b`,

For all objects `z` and all morphisms <code>h<sub>1</sub></code>, <code>h<sub>2</sub> :: z -> a</code>,

if <code>f∘h<sub>1</sub> = f∘h<sub>2</sub></code>,

then <code>h<sub>1</sub> = h<sub>2</sub></code>

---

Analog to `injective` functions for category theory.

<a id="223-disclaimer-isomorphism-in-category-theory"></a>

#### 2.2.3. Disclaimer: isomorphism in category theory

For sets, if a function is `injective` and `surjective`, then we can say it is an `isomorphism`.

The same can't be said for a category if it is a `monomorphism` and an `epimorphism`!

That is not enough to say it is an `isomorphism`!

<a id="224-haskell-objects-and-function-examples"></a>

#### 2.2.4. Haskell objects and function examples

- `void`: type in haskell that represents _nothing_
- `absurd :: void -> a`
- `unit`: `() :: ()` in haskell.
- `unit :: a -> ()`: haskell unit function (gets anything, returns unit)
- `() -> a`: since it's pure functions, for each element `a` we need a different function
  - f.e. `one :: () -> 1`, `two :: () -> 2`, `three :: () -> 3`, etc
  - f.e. `True :: () -> true`, `False :: () -> false`

<a id="3-categories"></a>

## 3. Categories

<a id="31-zero"></a>

### 3.1. Zero

Category with no objects.

It fulfills the conditions because "for every pair of objects there is an arrow", since there are no objects (or arrows) it fullfils.

<a id="32-one-object"></a>

### 3.2. One object

Category with one object.

Will have a single object, and a single arrow, the identity `Id: a -> a`.

<a id="33-graph-more-objects"></a>

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

<a id="34-orders"></a>

### 3.4. Orders

In a category that is an order, arrows don't represent functions, they represent relations.

`f: a -> b` means `a` less or equal to `b`, `a ≤ b`

Depending on which conditions they fulfill we can have different types of order.

<a id="341-pre-order"></a>

#### 3.4.1. Pre-Order

Order that satisfies just the minimum of conditons:

**Reflexibity**

`a ≤ a` (Identity)

**Composition (Transitivity)**

So if `a ≤ b` and `b ≤ c`,
<br>
then `a ≤ c`

**Associativity**

If `a ≤ b`, `b ≤ c`, and `c ≤ d`,
<br>
then `(a ≤ b) ≤ c` is the same as `a ≤ (b ≤ c)`

A `category` which is a `pre-order` is called a `thin category`.

**Definition 2**

`C` is a `pre-order category`
<br>
_if, and only if_, for **all** objects `a`, `b` of `C`,
<br>
there is **at most** one morphism `f: a -> b`.

---

##### hom-set

The set of arrows between any two objects is called the `hom-set`.

A `thin category` is one in which every `hom-set` is either an `empty set` or a `singleton set`.

A `hom-set` for example from `a` to `b` is represented as `C(a, b)`.

<a id="342-partial-order"></a>

#### 3.4.2. Partial-Order

A `partial-order` is a `pre-order` that also satisfies **Antisymmetry**:

If `a ≤ b` and `b ≤ a`, then `a = b`.

This means there are no loops between distinct objects.

<a id="343-total-order"></a>

#### 3.4.3. Total-Order

A `total-order` (or _linear order_) is a `partial-order` in which there is an **arrow** between any two objects: every pair of objects is comparable.

For any two objects `a` and `b`, either `a ≤ b` or `b ≤ a`.

<a id="344-epimorphisms-monomorphisms-and-isomorphisms"></a>

#### 3.4.4. Epimorphisms, Monomorphisms and Isomorphisms

In previous sections it was said that `isomorphism` in **category theory** is a bit different than when talking about **sets**.

Having a morphism that is both `monic` (monomorphism) and `epic` (epimorphism) is not enough to be an `isomorphism` (invertible).

Now we can show an example!

In a `thin category` (preorder), since there is at most one arrow between any two objects, every arrow is both **monic** and **epic**.

However, an arrow `f: a -> b` is an **isomorphism** only if there is an inverse `g: b -> a`. This would require `a ≤ b` and `b ≤ a`.

- In a general **pre-order**, we might have cycles between distinct objects that are isomorphic.
- In a **partial-order**, due to antisymmetry (`a ≤ b` and `b ≤ a` implies `a = b`), the only isomorphisms are the identity arrows (from an object to itself).

Therefore, in a partial order, a morphism `a -> b` where `a != b` is a `monomorphism` and an `epimorphism`, but **not** an `isomorphism`!

<a id="35-monoid"></a>

### 3.5. Monoid

Any category that consists of a `single object` and as many arrows, is called a `monoid`.

A `monoid` will have `reflexibity` (identity), `composition` (single element, all arrows will be composable), and `associativity`.

The `hom-set` of a `monoid` **M** can be represented as `M(m, m)`.

**Examples of monoids**

- Multiplication of integers
- Addition of integers
- Concatenating strings
- Appending lists

<a id="36-kleisli-category"></a>

### 3.6. Kleisli Category

A **Kleisli category** is a category based on another existing category (like the category of types and functions in programming), but where the arrows have a special modification or "embellishment".

In our programming example (Section 1.6), we had:

- **Objects**: Types.
- **Arrows**: Functions `a -> b`.

In a **Kleisli category**, we keep the same objects, but redefine the arrows and their composition.

<a id="361-arrows-embellished-functions"></a>

#### 3.6.1. Arrows: Embellished Functions

The arrows in a Kleisli category from object `a` to object `b` correspond to functions `a -> M(b)` in the underlying category, where `M` represents some "embellishment" or "wrapper".

**Example: The Writer Category**

Imagine functions that return a value but also write to a log (a string). Strings form a **Monoid** (Section 3.5) with concatenation and an empty string.

- Standard function: `Number -> Number`
- Embellished function: `Number -> (Number, String)`

Here, the arrow from `Number` to `Number` in the Kleisli category is actually implemented as a function returning a pair.

<a id="362-composition"></a>

#### 3.6.2. Composition

Standard function composition (`g ∘ f`) doesn't work because the types don't match.

- `f: a -> (b, String)`
- `g: b -> (c, String)`

The output of `f` is `(b, String)`, but the input of `g` expects just `b`.

In a Kleisli category, we define a new composition operator (often called the "fish" operator `>=>`) that handles the "wrapping":

`g >=> f` applied to `a`:

1. Execute `f(a)` to get `(b, s1)`.
2. Pass `b` to `g` to get `(c, s2)`.
3. Combine the logs using the Monoid operation (concatenation) and return `(c, s1 + s2)`.

<a id="363-identity"></a>

#### 3.6.3. Identity

The identity arrow for an object `a` must be a function `a -> (a, String)` that doesn't change the value and produces an "empty" log (the Monoid identity).

- `id: a -> (a, "")`

This structure (Objects, Embellished Arrows, Special Composition, Identity) forms a valid Category known as the Kleisli Category.

<a id="37-monad"></a>

### 3.7. Monad

A **Monad** is the structure that makes a Kleisli category work. It is defined by the three things we already saw in Section 3.6: the embellishment `M` (Section 3.6.1), the Kleisli composition (Section 3.6.2), and the identity (Section 3.6.3).

Since a Kleisli category is a category, it must satisfy the category laws (Sections 1.3–1.5). These are the **Monad laws**:

- **Associativity** (Section 1.5): composing three embellished arrows with `>=>` must give the same result regardless of grouping: `(f >=> g) >=> h = f >=> (g >=> h)`.
- **Identity** (Section 1.4): composing any embellished arrow with the identity from Section 3.6.3 must return the same arrow: `id >=> f = f` and `f >=> id = f`.

<a id="38-universal-constructions"></a>

### 3.8. Universal Constructions

<a id="381-terminal-object"></a>

#### 3.8.1. Terminal Object

A **terminal object** in a category is an object that has a unique arrow coming from any other object.

Not all categories have a terminal object.

**condition 1**

For all object `a`,
<br>
there _exists_ an `f: a -> ()`

**condition 2**

For every two functions,
<br>
if `f: a -> ()`, `g: a -> ()`
<br>
then `f = g`

<a id="382-initial-object"></a>

#### 3.8.2. Initial Object

An **initial object** in a category is an object that has a unique outgoing arrow to every object.

**condition 1**

For all object `a`,
<br>
there **exists** an `f: void -> a`

**condition 2**

For every two functions,
<br>
if `f: void -> a`, `g: void -> a`
<br>
then `f = g`
