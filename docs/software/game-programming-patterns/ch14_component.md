# Ch 14: Component

## Table of Contents

- [1. The Problem](#1-the-problem)
- [2. The Pattern](#2-the-pattern)
- [3. When to Use It](#3-when-to-use-it)
- [4. How Components Are Wired](#4-how-components-are-wired)
- [5. Component Communication](#5-component-communication)
- [6. Design Decisions](#6-design-decisions)
- [7. Keep in Mind](#7-keep-in-mind)

## 1. The Problem

- **The monolithic entity class** — one class (e.g., a hero `Bjorn`) ends up containing input, physics, rendering, animation, sound, and AI. It becomes a 5,000-line dumping ground only the bravest coders dare touch
- **Coupling across domains** — conditions mixing physics, graphics, and sound (`if (collidingWithFloor() && getRenderState() != INVISIBLE) playSound(...)`) force every programmer to understand every domain just to make a change
- **Concurrency hazard** — modern games distribute work across threads by domain (AI on one core, rendering on another). A single class with `UpdateSounds()` and `RenderGraphics()` methods invites deadlocks and concurrency bugs
- **Inheritance can't carve it up cleanly** — trying to share code via a `GameObject` hierarchy (`Zone`, `Decoration`, `Prop`) runs into the **Deadly Diamond** of multiple inheritance, or pushes unused state up into the base class

## 2. The Pattern

> A single entity spans multiple domains. To keep the domains isolated, the code for each is placed in its own **component class**. The entity is reduced to a simple **container of components**.

- **"Component"** — the author notes the term is overloaded (business software has a different "Component" pattern for decoupled web services). He keeps the name because it is already the common usage in games (XNA, Delta3D)
- **Composition over inheritance** — instead of sharing code by subclassing a common base, two classes share code by both owning an instance of the same component class
- **Restaurant analogy** — monolithic classes are combo meals (a fixed class per combination of features); components are à la carte (pick just the dishes you want). Think software Voltron

## 3. When to Use It

- A class touches multiple domains you want to keep decoupled from each other
- A class is getting massive and hard to work with
- You want to define many kinds of objects that share different capabilities, but inheritance doesn't let you pick reusable parts precisely enough
- Most commonly applied to the core entity class of a game, but useful anywhere the above pressures exist

## 4. How Components Are Wired

- **Extract domains into component classes** — pull input handling into `InputComponent`, physics into `PhysicsComponent`, rendering into `GraphicsComponent`. Each owns its own data (e.g., `Volume` moves into `PhysicsComponent`; sprites move into `GraphicsComponent`)
- **Thin container** — the entity class shrinks to a list of components plus "pan-domain" state (position, velocity) shared across components
- **Hide components behind interfaces** — turn `InputComponent` into an abstract base class; supply a `PlayerInputComponent` for normal play and a `DemoInputComponent` (AI-driven) for demo mode. Physics and graphics don't know the difference
- **The generic `GameObject`** — once Bjorn has no Bjorn-specific code, rename the container to `GameObject` and build every entity type by injecting different combinations of components (a Factory Method à la Gang of Four)
- **Entity component systems** — an extreme variant: the entity is just an ID. Components live in separate collections keyed by that ID, letting you add components to an entity without the entity even knowing. Covered further in the Data Locality chapter

## 5. Component Communication

Perfectly isolated components are an ideal; components in the same entity need to coordinate. These options typically coexist.

| Mechanism | Coupling | Good for |
|-----------|----------|----------|
| Modify container state | Low (components don't know each other) | Basics every object has: position, size, velocity |
| Direct reference between components | Tighter, but scoped | Closely related pairs: animation + rendering, input + AI, physics + collision |
| Messaging through the container | Loosest (coupled only by message values) | Fire-and-forget "less important" communication (audio reacting to a collision) |

- **Shared state via container** — implicit, order-dependent: the original monolithic `update()` was carefully ordered (input → physics → rendering); components inherit that fragile ordering. Worse, state only one component needs gets pushed up into the container, wasting memory on objects that don't use it
- **Direct references** — simple, fast, a free-for-all of method calls. You step back toward the monolithic class, but coupling is limited to component pairs that actually interact
- **Message passing via container** — base `Component` with `receive(message)`; the container has `send(message)` that broadcasts to all its components. The container becomes a **Mediator** (Gang of Four). Beware feedback loops. Can be extended into a queued system (see Event Queue chapter)

## 6. Design Decisions

**What set of components do I need?** Depends on genre and engine size. Bigger engines slice more finely.

**Who assembles the components?**

- **Object creates its own components** — guarantees correctness (never forget to wire one up), but gives up the flexibility of recombining components into new object types
- **Outside code provides the components** — the object becomes a generic container, fully reconfigurable, decoupled even from the concrete component classes. The common and more powerful choice

## 7. Keep in Mind

- **Adds complexity** — each conceptual object becomes a cluster that must be instantiated, initialized, and wired together. Worth it for large codebases; overkill for small ones
- **Level of indirection per access** — get the component from the container before you can do anything. In performance-critical inner loops, pointer chasing can hurt
- **Flip side: cache coherence** — components make it easier to apply the Data Locality pattern, organizing data in the order the CPU wants it
- **Related patterns** — resembles Gang of Four **Strategy**, but components usually hold state that defines what the object *is*, whereas a Strategy is typically a stateless algorithm. A stateless component blurs the line and can be shared across container objects
- **Seen in the wild** — Unity's core `GameObject`, Delta3D's `GameActor` with `ActorComponent`, Microsoft's XNA `Game`/`GameComponent` (at the main-game-object level rather than per entity)
