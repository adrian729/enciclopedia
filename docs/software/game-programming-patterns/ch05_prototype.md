# Ch 5: Prototype

## Table of Contents

- [1. The Problem](#1-the-problem)
- [2. The Pattern](#2-the-pattern)
- [3. How Well Does It Work?](#3-how-well-does-it-work)
- [4. Alternatives in Class-Based Languages](#4-alternatives-in-class-based-languages)
- [5. The Prototype Language Paradigm](#5-the-prototype-language-paradigm)
- [6. Prototypes for Data Modeling](#6-prototypes-for-data-modeling)

## 1. The Problem

- **Parallel class hierarchy** — imagine a Gauntlet-style game with `Ghost`, `Demon`, `Sorcerer` subclasses of `Monster`, each spawned by its own `GhostSpawner`, `DemonSpawner`, etc. A factory class per monster class is boilerplate-heavy redundant duplication
- **Goal** — spawn monsters of varying types without a spawner subclass for every monster subclass

## 2. The Pattern

- **Key idea** — an object can spawn other objects similar to itself. Any monster can act as a *prototypal* monster used to generate copies
- **`clone()` method** — add an abstract `clone()` to the base class; each subclass returns a new object identical in class and state to itself
- **Single Spawner class** — holds one hidden prototype instance and calls `prototype_->clone()` to produce new monsters. *Design Patterns* cites Ivan Sutherland's 1963 Sketchpad as one of the first examples of this pattern in the wild
- **Clones state, not just class** — a spawner built around a fast ghost prototype produces fast ghosts; a weak-ghost prototype yields weak ghosts. Prototype state parameterizes the spawner for free

## 3. How Well Does It Work?

- **Saves the spawner hierarchy** — no separate spawner class per monster
- **But** — you still have to implement `clone()` in every monster class, which is about as much code as the spawners were
- **Semantic ratholes** — deep clone vs. shallow clone: if a demon holds a pitchfork, does cloning the demon clone the pitchfork? No single right answer
- **Contrived premise** — the pattern assumes a separate class per monster kind, which modern engines avoid. Component and Type Object patterns are the contemporary go-tos for modeling different entity kinds without a class per kind

## 4. Alternatives in Class-Based Languages

- **Spawn functions** — a free function like `spawnGhost()` that returns a `new Ghost()`; the single `Spawner` class stores a function pointer. Less boilerplate than a whole spawner class
- **Templates** — `template <class T> class SpawnerFor : public Spawner { Monster* spawnMonster() { return new T(); } }`. The non-templated base `Spawner` lets callers work with any monster type without themselves becoming templates
- **First-class types** — in dynamically-typed languages (JavaScript, Python, Ruby) classes are regular objects; pass the monster class itself to the spawner. C++ lacks first-class types, hence the gymnastics above

## 5. The Prototype Language Paradigm

- **Self** — Dave Ungar and Randall Smith's 1980s language. Object-oriented but classless: state *and* behavior both live on the object itself, erasing the class/instance distinction
- **Delegation** — instead of inheritance, failed property lookups on an object are delegated to its *parent* (just a reference to another object). Parents can themselves be swapped at runtime — *dynamic inheritance*
- **Cloning instead of instantiation** — since there are no classes, you build one object in the shape you want and clone it to make more. Every object supports Prototype automatically
- **Nystrom's verdict on prototype languages** — he built a prototype-based language called Finch to learn, found it wasn't fun to program in. The language was simple to implement but punted complexity onto the user; he missed the structure classes give. Self programmers reportedly reached the same conclusion
- **Legacy** — the VM techniques invented to make Self fast (JIT, GC, dispatch optimization) are what now power mainstream dynamic languages
- **JavaScript** — Brendan Eich took direct inspiration from Self, but JavaScript in practice resembles class-based languages more than prototypal ones. Cloning is absent; `Object.create()` (ECMAScript 5) is the closest. The `new` operator + constructor function + methods on `.prototype` effectively reintroduces the class/instance split

## 6. Prototypes for Data Modeling

- **Data is growing** — modern game code is an engine driving content defined in data files. At scale, data has the same organizational problems as code: duplication, maintenance, cross-cutting edits
- **Delegation in data** — let a data entity reference another via a `"prototype"` field; missing properties are looked up on that prototype. Basic single delegation, big wins
- **Example** — three goblin variants (grunt, wizard, archer) share health/resists/weaknesses. Instead of repeating those fields, `wizard` and `archer` list `"prototype": "goblin grunt"` and only declare what they add (`spells`, `attacks`)
- **No abstract base needed** — rather than invent a fourth "base goblin" prototype, pick the simplest concrete goblin and delegate to it. Natural for one-off special entities
- **Fits unique items and bosses** — the Sword of Head-Detaching is just a `longsword` prototype with a `damageBonus`. Designers get concise variation without schema ceremony
