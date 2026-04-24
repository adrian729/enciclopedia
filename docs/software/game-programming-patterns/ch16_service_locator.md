# Ch 16: Service Locator

## Table of Contents

- [1. The Problem](#1-the-problem)
- [2. The Pattern](#2-the-pattern)
- [3. When to Use It](#3-when-to-use-it)
- [4. Building a Locator (Sample Code)](#4-building-a-locator-sample-code)
- [5. Design Decisions](#5-design-decisions)
- [6. Keep in Mind](#6-keep-in-mind)
- [7. Related Patterns](#7-related-patterns)

## 1. The Problem

- **Pervasive systems** — memory allocators, logging, random numbers, audio: services needed all over the codebase. Physics plays crash sounds, AI fires rifle shots, UI plays menu beeps
- **Naive access couples everyone to the implementation** — calling `AudioSystem::playSound(...)` directly as a static class or `AudioSystem::instance()->playSound(...)` as a Singleton GoF ties every call site to the concrete `AudioSystem` class *and* to the particular access mechanism
- **Phone book analogy** — instead of giving every caller your real address, list a lookup name. People find you by name; when you move, you just update the directory. The Service Locator is that phone book: it decouples callers from both **who** the service is (concrete type) and **where** it lives (how to reach the instance)

## 2. The Pattern

> A **service** class defines an abstract interface to a set of operations. A concrete **service provider** implements this interface. A separate **service locator** provides access to the service by finding an appropriate provider while hiding both the provider's concrete type and the process used to locate it.

## 3. When to Use It

- **Use sparingly.** Anything globally accessible courts the same problems as Singleton GoF
- **First try passing the object directly** — simple, makes coupling obvious, covers most needs
- **Use a locator when passing is gratuitous or makes code harder to read**:
  - Systems that shouldn't belong in a module's public API (logging, memory management — rendering parameters shouldn't include a logger)
  - Facilities that are fundamentally singular and ambient (one audio device, one display) — plumbing them through ten call layers is noise

## 4. Building a Locator (Sample Code)

- **The service** — an abstract interface, e.g., `class Audio { virtual void playSound(int); virtual void stopSound(int); virtual void stopAllSounds(); };`. No implementation bound to it
- **The service provider** — a concrete subclass like `ConsoleAudio` implementing the interface with real platform calls
- **The simple locator** — a class with `static Audio* getAudio()` and `static void provide(Audio*)`. Startup code news up `ConsoleAudio` and calls `Locator::provide(audio)`. Callers only see the abstract `Audio` interface
- **Dependency injection** — jargon for: outside code injects the dependency instead of the locator constructing it. The locator class itself is never coupled to the concrete provider
- **Decoupling bonus** — the service class doesn't know it's being accessed through a locator. That lets the pattern apply to classes not designed around it, unlike Singleton GoF which shapes the service class itself
- **Null service** — if nothing has registered a provider, `getAudio()` returning `NULL` will crash callers. The author notes this required-call-order problem is sometimes called **temporal coupling**. Fix by defining a `NullAudio` provider whose methods do nothing, defaulting the locator to it (via an `initialize()` call) and falling back to it if `provide()` is given `NULL`. Returning the service by reference rather than pointer signals to callers that the result is never null
  - Also useful as a deliberate off-switch during development (disable audio by simply not registering a real provider — saves memory, CPU, and eardrums when debugging)
- **Logging decorator** — another provider, e.g., `LoggedAudio`, wraps an existing `Audio` and logs each call before forwarding to the inner provider. Swap it in with `Locator::provide(new LoggedAudio(Locator::getAudio()))`. This is the Decorator GoF pattern; lets you selectively log one subsystem at a time and ship the game with no logging at all. Stacks cleanly with the null service

## 5. Design Decisions

### 5.1. How is the service located?

| Approach | Speed | Flexibility | Downside |
|----------|-------|-------------|----------|
| **Outside code registers it** | Fast (often inlined) | Can swap service even at runtime; locator stays ignorant of construction details (e.g., online-vs-local controller provider that needs an IP address) | Depends on outside init code running first |
| **Bind at compile time** (preprocessor) | Fastest | Compile-time guaranteed available | Must recompile to change; no runtime swap |
| **Configure at runtime** (reflection, config file) | Slowest (locate takes time) | Swap without recompile; non-programmers can reconfigure; one binary supports many configs | Complex — must build config parsing and reflection lookup |

### 5.2. What happens if the service can't be located?

- **Let the user handle it** — return `NULL` and let each call site decide. Each site must check; duplicated error handling across potentially hundreds of call sites; one missed check crashes the game
- **Halt the game** — assert inside the locator. Callers don't need to check; if it fails, it's declared a bug in the locator. On a large dev team, though, one broken registration blocks everyone
- **Return a null service** — the sample's approach. Callers never handle missing services; game keeps running. Downside: can silently hide a real missing registration. Mitigation: have the null service print debug output when used
- **Typical choice** — ship builds usually assert; large teams benefit from a null service during development

### 5.3. What is the scope of the service?

- **Global access** — encourages the whole codebase to share one service; loses control over who uses it
- **Restricted access** (e.g., protected static in a base class) — limits coupling to a branch of the inheritance tree; risks duplicated locator code across unrelated classes
- **Guideline** — limit scope to a domain if the service belongs to one (network service used only by online classes); keep globals only for truly cross-cutting services like logging

## 6. Keep in Mind

- **Deferred dependency wiring** — the locator is a dependency that's resolved at runtime. Flexibility bought at the cost of harder-to-read dependencies
- **Service must actually be locatable** — unlike a Singleton or static class, lookup can fail. The null service is one strategy to guarantee something valid comes back
- **Service can't know who's calling it** — because any code may access the locator, the service must work in any context. Classes whose correctness depends on being called only at a certain point in the game loop are a bad fit
- **Worst-case** — used poorly, a service locator has all the downsides of Singleton GoF plus worse runtime performance

## 7. Related Patterns

- **Singleton GoF** — sibling pattern; compare both for fit. Locator is a more flexible, configurable cousin
- **Component** — Unity's `GetComponent()` uses this pattern alongside the Component pattern
- **XNA** — Microsoft's XNA framework has the pattern built into its core `Game` class via a `GameServices` object that registers and locates services of any type
