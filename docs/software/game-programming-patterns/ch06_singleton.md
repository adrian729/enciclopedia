# Ch 6: Singleton

## Table of Contents

- [1. An Anti-Pattern Chapter](#1-an-anti-pattern-chapter)
- [2. The Pattern](#2-the-pattern)
- [3. Why We Use It](#3-why-we-use-it)
- [4. Why We Regret Using It](#4-why-we-regret-using-it)
- [5. Solves Two Problems Even When You Have One](#5-solves-two-problems-even-when-you-have-one)
- [6. Lazy Initialization Takes Control Away From You](#6-lazy-initialization-takes-control-away-from-you)
- [7. What To Do Instead](#7-what-to-do-instead)
- [8. What's Left for Singleton](#8-whats-left-for-singleton)

## 1. An Anti-Pattern Chapter

- **Anomaly chapter** — every other chapter shows how to use a pattern; this one shows how *not* to
- **Overused in games** — the Gang of Four stressed the Singleton GoF pattern should be used sparingly; that message was largely lost in translation to the game industry
- **Root cause** — when the industry moved from C to OOP, "how do I get an instance?" was the recurring frustration. Singletons (i.e. globals) were the easy way out

## 2. The Pattern

- **GoF definition** — *"Ensure a class has one instance, and provide a global point of access to it."* Two problems glued together by "and"
- **Restricting to one instance** — useful when the class wraps external global state (e.g. an async file system wrapper where multiple instances couldn't coordinate pending operations)
- **Global point of access** — the class exposes a static `instance()` method so any module (logging, content loading, save system) can reach the one instance
- **Classic C++ implementation** — private constructor, static `instance_` pointer, lazy init inside `instance()`
- **Modern C++11** — a local `static` inside `instance()` is guaranteed thread-safe for initialization (the class's own methods are a separate question)

## 3. Why We Use It

- **No instance if unused** — lazy initialization saves memory and CPU if the game never asks for it
- **Initialized at runtime, not at static-init time** — static member variables are initialized by the compiler before `main()`, so they can't use info known only once the program is running (e.g. config loaded from a file) and can't reliably depend on each other (compiler doesn't guarantee ordering). Lazy init sidesteps both
- **One singleton can depend on another** — as long as there are no circular dependencies
- **Subclassable** — a `FileSystem` abstract base can return a `PS3FileSystem` or `WiiFileSystem` from `instance()` based on a compiler switch. The whole codebase uses `FileSystem::instance()` without being coupled to platform code

## 4. Why We Regret Using It

- **It's a global variable** — a singleton *is* global state, just encapsulated in a class. It inherits every downside of globals
- **Harder to reason about code** — a function that touches global state forces you to grep the whole codebase to understand what might mutate it. "You don't really hate global state until you've had to grep a million lines of code at three in the morning"
- **Encourages coupling** — a new team member told to "make boulders play sounds on impact" will `#include` the globally visible `AudioPlayer` and couple physics to audio. Restricting access is how you control coupling
- **Not concurrency-friendly** — globals are shared memory every thread can poke at without knowing what others are doing. Deadlocks, race conditions, thread-sync bugs follow
- **Pure functions** — functions that don't touch global state are easier to reason about, easier to optimize, and enable techniques like memoization. Haskell enforces purity for these reasons
- **Placebo, not cure** — Singleton solves none of the problems globals cause, because a singleton *is* global state

## 5. Solves Two Problems Even When You Have One

- **The "and" is suspicious** — ensuring single instantiation and providing global access are separate concerns. Most uses only want convenient access
- **Logger example** — you Singleton-ify `Log` to avoid passing it around. Deep in development the log file becomes unreadable and you want separate loggers per domain (UI, audio, online, gameplay) — but single-instantiation is now baked into every `Log::instance().write(...)` call site in the codebase
- **Cost of change** — fixing both the class *and* every call site. Worse if `Log` lives in a shared library across multiple games

## 6. Lazy Initialization Takes Control Away From You

- **Games are not desktop PCs** — initializing a subsystem may allocate memory and load resources. If audio lazy-initializes the first time a sound plays, it will likely do so mid-action, causing dropped frames
- **Heap layout matters** — games control heap layout to avoid fragmentation; you need to know *when* a subsystem grabs its memory so you know *where* it lands
- **Common workaround** — skip lazy init; use a `static FileSystem instance_` member. But this strips away the features that made Singleton better than a raw global: no polymorphism, must be constructible at static-init time, can't free the memory
- **At that point it's a static class** — so why not drop `instance()` and use static functions directly? `Foo::bar()` is simpler than `Foo::instance().bar()` and honest about the static memory

## 7. What To Do Instead

### 7.1. See if you need the class at all

- **Manager disease** — `Monster`, `MonsterManager`, `Particle`, `ParticleManager`, `ManagerManager`. Often reflects unfamiliarity with OOP
- **Move behavior onto the class it helps** — a `BulletManager` that tracks `isOnScreen()` and `move()` for a dumb `Bullet` struct should just be collapsed into `Bullet`. OOP is about objects taking care of themselves

### 7.2. Single instantiation without global access

- **Runtime assert** — a public constructor that `assert`s a static `instantiated_` flag is false, flips it true, and resets in the destructor. Enforces single instance without granting global visibility
- **Tradeoff** — check is runtime-only; the real Singleton enforces single instantiation at compile time by its very structure

### 7.3. Convenient access without globals

- **Pass it in** — the simplest and often best answer. "Dependency injection" in one common sense. A `context` parameter for rendering, for example. Not everything belongs in the signature though (logging is the textbook *cross-cutting concern*; aspect-oriented programming was designed for these)
- **Get it from the base class** — with a shallow `GameObject` hierarchy, put a `protected getLog()` on the base. Only derived game objects reach the `Log`; nothing else in the codebase can. Connects to the Subclass Sandbox pattern
- **Get it from something already global** — most codebases have *one* unavoidable global like `Game` or `World`. Piggyback other systems on it: `Game::instance().getAudioPlayer()`. Reduces N singletons to one. Purists cite the Law of Demeter; Nystrom claims this is still better than a giant pile of singletons. If the architecture later supports multiple `Game` instances, the subsystems don't notice
- **Hybrid** — code that already knows about `Game` goes through it; unrelated code uses one of the other options
- **Service Locator** — a dedicated class whose sole job is to provide global access to services. Its own chapter later in the book

## 8. What's Left for Singleton

- **Nystrom has never used the full Gang of Four implementation in a game**
- **For single instantiation** — a static class, or a runtime-checked static flag
- **Related patterns** — Subclass Sandbox gives derived classes shared state without globals; Service Locator provides globally reachable objects with more flexibility than Singleton
