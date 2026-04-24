# Ch 4: Observer

## Table of Contents

- [1. The Problem](#1-the-problem)
- [2. How It Works](#2-how-it-works)
- [3. Performance Myths](#3-performance-myths)
- [4. Avoiding Dynamic Allocation](#4-avoiding-dynamic-allocation)
- [5. Lifetime Hazards](#5-lifetime-hazards)
- [6. When Not to Use It](#6-when-not-to-use-it)
- [7. Observers Today and Tomorrow](#7-observers-today-and-tomorrow)

## 1. The Problem

- **Pervasive pattern** — underlies Model-View-Controller. Java ships `java.util.Observer`; C# has the `event` keyword baked into the language
- **Motivating example: achievements** — "Kill 100 Monkey Demons", "Fall off a Bridge", "Complete a Level Wielding Only a Dead Weasel". Achievements are triggered by a wide range of different gameplay behaviors. Naive code would thread achievement calls like `unlockFallOffBridge()` into places like the physics engine's collision resolution
- **What Observer buys you** — *"lets one piece of code announce that something interesting happened without actually caring who receives the notification"*
- **Physics stays clean** — it emits `notify(entity, EVENT_START_FALL)` and doesn't know whether anyone is listening. The achievement system registers to receive those events, checks whether the falling body is the hero standing on a bridge, and unlocks the badge with no involvement from physics
- **Not fully decoupled** — the physics engine still has to decide *which* notifications to send. Architecture aims to make systems *better*, not perfect

## 2. How It Works

- **Observer** — an interface with a single `onNotify(entity, event)` method. Any concrete class implementing it becomes an observer (e.g. `Achievements : public Observer`). Parameters are your choice — pattern name is "Observer", not "ready-made code"
- **Subject** — the thing being observed. Two jobs: hold the list of observers, and send notifications
- **Subject public API** — `addObserver()` and `removeObserver()` let outside code wire up listeners. The subject doesn't need to know the observers' concrete types
- **Subject sends notifications** — `notify()` walks the list and calls `onNotify()` on each observer. Typically `protected` so only subclasses can trigger sends
- **List, not single observer** — supporting many observers keeps them from implicitly coupling (e.g. audio registering would un-register achievements if there were only one slot). Each observer thinks it's alone
- **Observer vs. event systems** — with an **observer** you register on the *thing* that did something interesting. With an **event** you register on an object that represents the *interesting thing that happened* (e.g. `physics.entityFell().addObserver(this)`). Author prefers composing a `Subject` member rather than inheriting `Subject`

## 3. Performance Myths

- **"It's too slow"** — unfounded. Sending a notification is walking a list and calling virtual methods. Cost is negligible outside hot code paths, and no allocation or queuing occurs
- **Confusion with related systems** — Observer gets lumped with "events", "messages", "data binding", some of which *do* queue or allocate. They are different things (see *Event Queue* chapter)
- **It's too *fast*** — Observer is synchronous. The subject blocks until every observer returns. UI programmers' time-worn motto: *"stay off the UI thread"* — push slow work to another thread or work queue
- **Threading caveat** — if an observer grabs a lock the subject holds, you can deadlock. In heavily threaded engines, prefer asynchronous Event Queue

## 4. Avoiding Dynamic Allocation

- **Notification is allocation-free** — it's a plain method call. Allocation only happens when observers are wired up, which is usually rare and front-loaded
- **Linked observers** — thread the list through the observers themselves. `Subject` holds only a `head_` pointer; each `Observer` has a `next_` pointer. No separate collection, no dynamic allocation. `Subject` is made a friend of `Observer` to poke at the list
- **Head-insertion trade-off** — registering at the head is simplest but notifies in *reverse* registration order (register A, B, C → notified C, B, A). Good observer discipline says two observers of the same subject should have no ordering dependency on each other
- **Intrusive list** — this style, where the node data lives inside the observed object, is called *intrusive*. Less flexible but more efficient. Used in the Linux kernel
- **Intrusive limitation** — each observer can belong to only *one* subject's list at a time
- **Pool of list nodes** — to lift that limitation without allocating, use separate list-node objects (pointer to observer + next pointer) drawn from a pre-allocated object pool. Observer can now appear in many subjects at once

## 5. Lifetime Hazards

- **Dangling pointers** — deleting an observer leaves subjects holding pointers into freed memory. Next notification is undefined behavior. *Design Patterns* doesn't mention this issue at all
- **Destroying the subject** — observers still expect notifications that will never come. "They aren't observers at all, really, they just think they are"
- **Three fixes**:
  - Observer unregisters itself in its destructor. Simple, but easy to forget
  - Subject sends a final "dying breath" notification before destruction so observers can react
  - Base `Observer` class automatically unregisters from every subject it observes. Needs pointers in both directions but removes the burden from users
- **Lapsed listener problem** — even with a GC, a subject's observer list keeps observers alive. Zombie UI screens that were dismissed still receive notifications, waste CPU, and may trigger wrong behavior (e.g. playing sounds). Has a Wikipedia article. Lesson: be disciplined about unregistration

## 6. When Not to Use It

- **Hard to trace flow** — the cost of Observer's loose coupling is that the communication graph is dynamic. A static IDE can't show you who gets notified; you have to reason about runtime state
- **Author's guideline** — *"If you often need to think about both sides of some communication in order to understand a part of the program, don't use the Observer pattern to express that linkage. Prefer something more explicit"*
- **Between lumps, not within** — Observer shines when connecting mostly unrelated subsystems (achievements ↔ physics), where you want minimal communication without merging them. It's less useful within a single cohesive feature

## 7. Observers Today and Tomorrow

- **Class-heavy by 1994 standards** — *Design Patterns* came out when OOP was the zeitgeist and programmers were paid by the class. Implementing a whole `Observer` interface just to receive a notification feels heavyweight today
- **Rigidity** — a single class can't use different notification methods for different subjects, which is why subjects usually pass themselves so the observer can disambiguate
- **Function-based observers** — in languages with first-class functions and closures, an observer is just a reference to a method or function. C# events register *delegates* (method references); JavaScript event listeners are usually plain functions. Author: if designing one today, would be function-based even in C++ (member function pointers over `Observer` interfaces)
- **Data binding** — modern frameworks automate the tedious "state changed → update the UI element" loop. Reactive/dataflow programming has chased this for years; data binding is a less ambitious, more practical middle ground
- **Verdict** — data binding is likely too slow/complex for a game engine core, but may creep into UI. The good old Observer pattern is *"dead simple and it works"* — often the two most important criteria
