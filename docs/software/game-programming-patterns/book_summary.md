# Game Programming Patterns: Summary

> **Read time: ~15–30 minutes.** This page is a single-sitting narrative summary of the book's key ideas. For a detailed chapter-by-chapter reference with the author's definitions and concrete examples, see the chapter entries in the sidebar.

## Table of Contents

- [1. Thesis: Architecture is About Change](#1-thesis-architecture-is-about-change)
- [2. The Three Speeds and Their Tradeoffs](#2-the-three-speeds-and-their-tradeoffs)
- [3. Decoupling: The Book's Core Move](#3-decoupling-the-books-core-move)
  - [3.1. Command: Reify the Call](#31-command-reify-the-call)
  - [3.2. Observer: Announce Without Addressing](#32-observer-announce-without-addressing)
  - [3.3. Event Queue: Decouple in Time](#33-event-queue-decouple-in-time)
  - [3.4. Component: Slice the Monolithic Entity](#34-component-slice-the-monolithic-entity)
  - [3.5. Service Locator: A Phone Book for Subsystems](#35-service-locator-a-phone-book-for-subsystems)
- [4. Behavior as Data](#4-behavior-as-data)
  - [4.1. Type Object: Kinds Without Classes](#41-type-object-kinds-without-classes)
  - [4.2. Bytecode: A Sandboxed Little Language](#42-bytecode-a-sandboxed-little-language)
  - [4.3. Prototype: Cloning and Data Delegation](#43-prototype-cloning-and-data-delegation)
  - [4.4. Subclass Sandbox: A Curated Toolkit](#44-subclass-sandbox-a-curated-toolkit)
- [5. The Game Loop and Its Extensions](#5-the-game-loop-and-its-extensions)
  - [5.1. Game Loop: Timing Strategies](#51-game-loop-timing-strategies)
  - [5.2. Update Method: One Frame at a Time](#52-update-method-one-frame-at-a-time)
  - [5.3. Double Buffer: Hiding Work in Progress](#53-double-buffer-hiding-work-in-progress)
  - [5.4. State: Finite State Machines and Beyond](#54-state-finite-state-machines-and-beyond)
- [6. Working With the Hardware](#6-working-with-the-hardware)
  - [6.1. Data Locality: Data Layout is Performance](#61-data-locality-data-layout-is-performance)
  - [6.2. Object Pool: Memory Without Fragmentation](#62-object-pool-memory-without-fragmentation)
  - [6.3. Spatial Partition: Neighbors in Log Time](#63-spatial-partition-neighbors-in-log-time)
  - [6.4. Dirty Flag: Defer the Work](#64-dirty-flag-defer-the-work)
  - [6.5. Flyweight: Sharing What's Duplicated](#65-flyweight-sharing-whats-duplicated)
- [7. The Pattern to Use Sparingly: Singleton](#7-the-pattern-to-use-sparingly-singleton)
- [8. Key Takeaways](#8-key-takeaways)

## 1. Thesis: Architecture is About Change

Nystrom opens with a deceptively simple claim: software architecture is *about change*. The measure of a design is not how elegant it looks on the whiteboard, but how easily it accommodates modification. If no one is ever going to touch the code — either because it is perfect or because it is so repellent nobody will open their editor — its design is irrelevant. Architecture only exists because programs get edited, and programmers spend far more time *understanding* existing code than writing new code. The single biggest lever an architect has is to reduce the volume of code a programmer must load into their head before they can make progress.

That lever is **decoupling**. Nystrom's working definition: two pieces of code are coupled if you cannot understand one without understanding the other. Decouple them, and either half can be reasoned about independently. A secondary definition: a change on one side does not force a change on the other. Both definitions share a single goal — "minimize the amount of knowledge you need to have in-cranium before you can make progress." A great deal of this book, and a large chunk of *Design Patterns* before it, is about exactly that.

This book is not about graphics, physics, audio, or AI. It is about the code *between* all of that — how the pieces hang together, what conventions let a team keep shipping, and which patterns hold up in the peculiar crucible of game development.

## 2. The Three Speeds and Their Tradeoffs

Good architecture has a cost. Every abstraction is code that must be written, debugged, and maintained. Every extension point is a bet that future-you will need that flexibility, and bets sometimes lose. Overzealous architecting yields codebases bristling with interfaces, virtual methods, and plug-in systems where tracing a single behavior takes forever — the layers of abstraction themselves end up "filling your mental scratch disk." This is what turns people against design patterns. The mantra **YAGNI** — "You aren't gonna need it" — exists to fight the urge to speculate about hypothetical future needs.

Nystrom frames the tension as three competing forces, all of which he calls forms of "speed":

1. **Long-term development speed** — clean architecture makes future changes cheap.
2. **Runtime speed** — the game itself must execute fast.
3. **Short-term development speed** — today's feature has to land today.

These pull against each other. Maintaining clean architecture demands careful effort on every change. Optimization calcifies the codebase; highly tuned code is inflexible and resists further edits. Rushing features accrues hacks, bugs, and inconsistencies that sap next quarter's productivity. There is no right answer, only tradeoffs. Nystrom argues this is the source of the craft rather than a reason for despair: like chess, the intertwined constraints are what make the discipline worth mastering.

Two related observations shape the rest of the book. First, **performance is about assumptions** — the practice of optimization thrives on concrete limitations ("never more than 256 enemies" lets you pack an ID into one byte). Flexibility is the opposite: architecture earns its keep by *removing* assumptions so code can work with more cases. Second, **simplicity is the best lever** against all three forces. Simple code is easier to load into your head, easier to change, and often runs fast because there is less of it. But simple is not quick to write: a simple solution is a *distillation* of code, not an accretion. "I would have written a shorter letter, but I did not have the time."

## 3. Decoupling: The Book's Core Move

A handful of the book's patterns are essentially different shapes of the same idea — replacing a direct call with a more indirect mechanism so that the caller and callee no longer need to know about each other. These appear across all five of the book's sections, and they form the backbone of what Nystrom recommends.

### 3.1. Command: Reify the Call

A **command** is a reified method call — a method call wrapped in an object you can store in a variable, pass to a function, queue, or log. The Gang of Four defined it as "encapsulate a request as an object, thereby letting users parameterize clients with different requests, queue or log requests, and support undoable operations," and gave an alternate slugline: *"Commands are an object-oriented replacement for callbacks."* The tell-tale signature of the pattern is an interface with a single method that returns nothing — typically `execute()`.

Commands solve several concrete game problems. They enable configurable input: instead of hard-wiring `BUTTON_X` to `jump()`, the handler stores a `Command*` per button, and rebinding is a pointer assignment. Once the command carries its target as a parameter (`execute(GameActor&)`), one `JumpCommand` instance can drive any character — AI and the input handler can both emit the same command stream, making demo mode a matter of swapping who is pulling commands from the queue. Serializable commands pushed over a network give you multiplayer for free.

Commands also give a natural home to **undo and redo**. Add a `virtual void undo() = 0` to the interface; each command captures the pre-change state in `execute()` and restores it in `undo()`. A single-level undo keeps the last command; a multi-level undo keeps a list and a "current" pointer, advancing on execute and rewinding on undo. Nystrom notes that games rarely need user-facing redo, but often need **replay** — recording the per-frame commands every entity performed, then re-simulating them instead of snapshotting full game state.

### 3.2. Observer: Announce Without Addressing

The Observer pattern "lets one piece of code announce that something interesting happened without actually caring who receives the notification." Its motivating example in the book is achievements: "Fell off a Bridge" is triggered by physics, "Defeated the Foo without taking damage" by combat. Without Observer, achievement-specific calls thread into every subsystem. With it, physics emits `notify(entity, EVENT_START_FALL)` and does not know whether anyone is listening; the achievement system registers to receive falls and unlocks the badge on its own.

A **subject** holds a list of observers, exposes `addObserver` / `removeObserver`, and has a protected `notify()` that walks the list. An **observer** implements a single `onNotify(entity, event)` method. Supporting a list (not a single slot) keeps observers from implicitly interfering with each other.

Nystrom rebuts the usual criticisms. "Observer is too slow" is unfounded — a notification is a list walk and a virtual call, with no allocation or queuing (Observer is routinely lumped in with event systems that *do* queue). The legitimate complaint is that Observer is too *fast*: it is synchronous, and a subject blocks until every observer returns, which invites lock-order deadlocks on heavily threaded engines.

To avoid dynamic allocation on registration, the observer list can be **intrusive** — thread the list through the observers themselves via a `next_` pointer. The Linux kernel uses this style. The limitation is that each observer can only belong to one subject's list; a pool of separate list-nodes lifts that limitation without allocation.

The dangerous-bug category of Observer is **lifetime**. Deleting an observer leaves dangling pointers in subjects; destroying a subject leaves observers expecting notifications that will never come. Three fixes: observers unregister in their destructor; subjects send a "dying breath" notification; or a base `Observer` class automatically unregisters from every subject it is subscribed to. Even under garbage collection, the **lapsed listener problem** keeps dismissed UI screens alive, wasting CPU and triggering sounds they should no longer play — a Wikipedia-worthy footgun.

Nystrom's guideline: use Observer *between lumps* of code you want kept mostly unrelated, not *within* a single cohesive feature. If you routinely need to think about both sides of a linkage to understand a part of the program, use something more explicit.

### 3.3. Event Queue: Decouple in Time

A queue stores notifications or requests in first-in, first-out order. Senders enqueue and return; processors drain at their convenience. Event Queue is the asynchronous cousin of Observer — it decouples not only *who* receives a message from the sender, but *when* the message is processed.

The motivating example is an `Audio::playSound()` API with three problems: it blocks the caller (loading a sound off disc freezes the game), it cannot aggregate requests (two enemies wailing the same waveform sum to double volume), and it runs on the wrong thread (the audio thread sits idle while render and AI threads hammer the API). All three dissolve when `playSound()` enqueues a `PlayMessage { SoundId; int volume; }` and an `update()` call on the audio thread drains the queue — aggregating identical sounds in the process.

Nystrom's implementation note: prefer a plain fixed-size array over fancy data structures — no dynamic allocation, no bookkeeping, cache-friendly. A **ring buffer** leaves the array in place and wraps head and tail modulo the array size; a growable array with doubling gives amortized constant-time enqueue if a fixed cap is unacceptable.

The design decisions break down by what goes in (events describe something that happened; messages describe something we want to happen), who reads (single-cast, broadcast, or work queue), who writes, and who owns the queued objects. The central warning: a global event queue is a global variable wrapped in a protocol; it carries every danger of globals. The queued object outlives the call, so the world can change under it — an "entity died" event may be processed many frames later, by which time the entity is deallocated and its surroundings have moved. And feedback loops silently spin forever instead of overflowing the stack, so a common rule is "don't send events from inside an event handler."

Use Event Queue only when you actually need to decouple in time. If you just need to decouple who receives from who sends, Observer or Command are simpler.

### 3.4. Component: Slice the Monolithic Entity

The pattern is announced as: "a single entity spans multiple domains; to keep the domains isolated, the code for each is placed in its own component class, and the entity is reduced to a simple container of components." Without it, a hero class accrues input, physics, rendering, animation, sound, and AI code into a 5,000-line dumping ground. Worse, cross-domain conditionals like `if (collidingWithFloor() && getRenderState() != INVISIBLE)` force every programmer to understand every domain just to make a change, and domain-parallel threads cannot run cleanly on such a class without inviting deadlocks. Inheritance cannot carve the monolith up cleanly — the "Deadly Diamond" of multiple inheritance or state pushed up into the base class are the usual traps.

Composition over inheritance is the explicit alternative: two entity kinds share code by both owning an instance of the same component class. Once components are behind abstract interfaces (a `PlayerInputComponent` and a `DemoInputComponent` both satisfying `InputComponent`), the entity class has nothing hero-specific about it and can be renamed to `GameObject`. New entity types are then built by injecting different combinations of components.

Components within a single entity still need to coordinate. Nystrom lists three mechanisms, typically used together:

| Mechanism | Coupling | Good for |
|-----------|----------|----------|
| Modify shared state on the container | Low | Basics every object has: position, size, velocity |
| Direct reference between components | Tighter, but scoped | Closely related pairs: animation ↔ rendering, physics ↔ collision |
| Messaging through the container | Loosest | Fire-and-forget cross-domain notifications |

The messaging form makes the container a **Mediator** in the Gang of Four sense, broadcasting to all components via a `receive(message)` method. Feedback loops are the hazard to watch.

A more extreme variant is the **entity component system (ECS)**, where the entity is just an ID and components live in separate collections keyed by that ID. Nystrom returns to this design in the Data Locality chapter as the natural shape for cache-friendly updates.

### 3.5. Service Locator: A Phone Book for Subsystems

A **service** class defines an abstract interface to a set of operations; a concrete **service provider** implements it; the **service locator** hides both the provider's concrete type and the process used to locate it. Callers see the abstract interface; the locator manages the wiring.

Nystrom's analogy is a phone book. Instead of giving every caller your real address, you list a lookup name. People find you by the name; when you move, you just update the directory. That decouples callers from *who* the service is and *where* it lives.

A simple locator has `static Audio* getAudio()` and `static void provide(Audio*)`. Startup code instantiates the concrete `ConsoleAudio` and registers it. The locator class itself never mentions the concrete type — the coupling stays at the registration site. Two refinements earn their keep. A **null service** (a `NullAudio` that silently does nothing) eliminates the required-call-order hazard Nystrom calls **temporal coupling**, and doubles as a development off-switch for disabling a subsystem. A **logging decorator** — a provider that wraps an existing provider and logs each call before forwarding — lets you selectively trace one subsystem without shipping logging in the release build.

Service Locator shares Singleton's drawbacks (globally reachable state, dynamic wiring, opacity about who uses what) and adds a runtime lookup cost. Nystrom's advice: use sparingly. First try passing the object directly; use a locator only when passing would be gratuitous — for logging, memory management, audio, and other cross-cutting or ambient subsystems that should not appear in every function signature.

## 4. Behavior as Data

Modern games are bottlenecked less by CPU cycles than by content-authoring throughput. Four patterns push behavior out of compiled code and into data that designers can edit without a programmer in the loop.

### 4.1. Type Object: Kinds Without Classes

An RPG has many monster breeds — dragon, troll, and so on. The typical OOP answer is one subclass per breed, each overriding `getAttack()` and passing starting health up to the base constructor. That works for five breeds; it does not work for the hundreds a designer wants, and every health-tweaking iteration turns into a checkout-edit-recompile cycle that makes programmers into data monkeys.

Type Object breaks the class/instance relationship in two: define a **type object class** and a **typed object class**. Each type object instance represents a different logical type (one `Breed` for "dragon", another for "troll"). Each typed object (a `Monster`) holds a reference to its type object and forwards type-specific calls. Instance-specific data (current health) lives on the typed object; shared data and behavior (starting health, attack string) live on the type object. New types are new *instances*, populated from a data file, and designers can add hundreds of breeds without a programmer.

Nystrom points out that C++ vtables are Type Object applied to C by the compiler — a vtable is a type object, the vtable pointer is the breed reference. Type Object is, in effect, re-implementing what the compiler did, by hand, at runtime. Inheritance among type objects adds a twist: type objects themselves can inherit, via **dynamic delegation** (walk the chain at every access) or **copy-down delegation** (at construction, copy non-overridden attributes into the child — faster lookups, but changes to the parent post-construction do not propagate).

The pattern's main weakness is type-specific *behavior* — overriding a method becomes storing a member variable. Workarounds include a fixed set of pre-defined behaviors selected by an enum, or pushing behavior into data via Bytecode.

### 4.2. Bytecode: A Sandboxed Little Language

When huge swaths of game behavior must be tweakable — spells, AI scripts, mod content — encoding them in C++ is painful. Every change needs an engineer, a recompile, and a patch; and shipping behavior as compiled C++ gives mods full trust over the engine, with platform restrictions (many consoles and iOS forbid executing loaded or generated machine code) foreclosing that option anyway.

The Gang of Four's **Interpreter** pattern is the obvious alternative, but it is too slow for anything but toy uses: a sprawling fractal of expression objects evaluated recursively, hammered by pointer chasing and virtual dispatch. Machine code sits at the other extreme — dense, linear, fast — but is a security nightmare and often platform-forbidden. **Bytecode** is the compromise: define a synthetic instruction set and ship an emulator (a virtual machine) for it.

The interpreter is, at its core, a loop over a switch statement — read a byte, dispatch, advance. A stack machine handles expression composition elegantly: instructions pop operands off an internal value stack and push results back; a `LITERAL` instruction embeds its value in the byte stream. A bytecode sandbox falls out of the design almost for free — the bytecode can only do what its instructions allow, stack size is bounded, and execution time can be capped by counting instructions in the interpreter loop.

Key design decisions:

- **Stack-based vs. register-based**: JVM, .NET, and Nystrom's own Wren are stack-based; Lua (as of 5.1) is register-based. Stack-based is simpler to implement and generate code for.
- **Value representation**: tagged variants (enum + union) are the standard for dynamic languages; untagged unions are compact and fast but unsafe.
- **Front-end**: authoring in raw bytecode defeats the purpose. Text-based languages require a parser; graphical authoring tools can prevent invalid programs by construction.

Nystrom's warnings: this is the most complex pattern in the book — reach for it with care. And little languages grow like vines; you will end up with an accidental full language shaped like a shanty town. Keep a short leash, or commit to building a real language deliberately.

### 4.3. Prototype: Cloning and Data Delegation

The Gang of Four's Prototype pattern proposes that an object can spawn other objects similar to itself — add a `clone()` method to the base class, and a single spawner holds one prototype instance and calls `prototype_->clone()`. Nystrom's verdict on the textbook use is lukewarm: the pattern trades a hierarchy of spawner classes for the burden of implementing `clone()` in every monster class, and modern engines avoid per-kind subclasses anyway.

Where Prototype shines, Nystrom argues, is in **data modeling**. Let a data entity reference another via a `"prototype"` field; missing properties are looked up on that prototype. Three goblin variants — grunt, wizard, archer — can share health, resists, and weaknesses by declaring `"prototype": "goblin grunt"` and only listing what they add. One-off bosses and unique items (the Sword of Head-Detaching) are just the base item's prototype with a tweak. Designers get concise variation without schema ceremony.

The detour through the **Self** programming language is Nystrom's aside on why class-free languages, despite their elegance, tend to punt complexity onto the programmer. JavaScript descends directly from Self but in practice uses `new`, constructor functions, and `.prototype` methods to reintroduce an effectively class-based split.

### 4.4. Subclass Sandbox: A Curated Toolkit

When you already need many subclasses — say, a superhero game with hundreds of `Superpower` subclasses, each wanting to play sounds, spawn effects, and move entities — giving each subclass raw access to the engine invites four failures: redundant code across uncoordinated authors, pervasive coupling into internal engine layers, brittleness under engine change, and no place to enforce invariants like sound prioritization.

Subclass Sandbox inverts the arrangement: the base class defines an **abstract sandbox method** subclasses must override, plus a set of **provided operations** (protected, often non-virtual) that subclasses call to get things done. Gameplay authors compose behavior from the provided toolkit; engine coupling lives in one place — the base. The resulting class hierarchy is shallow and wide.

The risk is the **brittle base class problem** — the base ends up coupled to every engine system any subclass needs, and changes to it ripple through every subclass. Nystrom's mitigations: pull groups of related provided methods into separate helper classes the base delegates to (a `SoundPlayer` getter rather than six audio methods), and in the limit consider Component or Type Object when the behavior is better modeled as data than as imperative code.

The pattern is a role reversal of the Gang of Four's **Template Method**: there, the derived class provides primitive operations and the base provides the high-level template; in Subclass Sandbox, the base provides the primitives and the derived class provides the high-level method.

## 5. The Game Loop and Its Extensions

Games never stop moving. Even with no user input, animation plays, effects sparkle, the monster keeps chomping. Four patterns form the control backbone.

### 5.1. Game Loop: Timing Strategies

A game loop runs continuously during gameplay: each turn, process user input without blocking, update the game state, and render. It tracks the passage of time to control the rate of gameplay, and it solves two coupled problems — processing input without waiting, and running at a consistent speed despite hardware differences. Even turn-based games need one, because animation and music keep playing during the player's "wait."

The chapter's heart is a taxonomy of timing strategies:

- **Run as fast as you can** — the simplest loop just spins. Fast machines make the game unplayably fast (the old "turbo button" era); slow machines crawl. Only virtue: simplicity.
- **Fixed time step with synchronization** — after processing a frame, `sleep()` until the target frame budget is spent. Caps too-fast hardware and saves battery, but does nothing for too-slow hardware.
- **Variable time step** — measure elapsed time each frame and pass it to `update(elapsed)`. Motion scales with elapsed time, adapting to both fast and slow hardware. Trade-off: non-deterministic and unstable. Floating-point rounding accumulates differently on different machines (a networked bullet ends up in different places for Fred's fast PC vs. George's grandmother's antique); physics damping is tuned to a specific step and can "blow up" when the step varies. Most game developers recommend against it.
- **Fixed update time step, variable rendering** — decouple updating from rendering. Keep physics on a fixed step for stability; render whenever possible. The core loop accumulates `lag` each frame and runs as many fixed-step updates as fit before rendering. This is the approach Nystrom recommends for serious games.

The residual `lag` between updates enables **extrapolation**: pass `lag / MS_PER_UPDATE` to `render()`, which advances object positions forward by that fraction for smooth motion. The extrapolation is a guess — the bullet might actually hit an obstacle next update — but is usually less noticeable than the stutter without it.

Power management is a second axis. PC games typically burn spare cycles on higher FPS and fidelity; mobile games clamp the frame rate to 30 or 60 FPS and sleep through the remainder for battery life.

### 5.2. Update Method: One Frame at a Time

Every entity must animate across frames, not within one — a `while(true)` loop that patrols a skeleton left-then-right never yields control, so the player never sees motion. Behavior must advance one frame at a time and return.

The pattern: the game world maintains a collection of objects; each object implements an `update()` method that simulates one frame of its behavior; each frame, the game updates every object. An abstract `update()` hides concrete entity types from the loop, and calling it on every object each frame makes them appear to behave concurrently.

Variables that were implicit in the original control flow (a local `patrollingLeft` boolean, a lightning timer) must now be fields on the entity, because execution position is lost every return. The State pattern often helps. Languages with lightweight concurrency (generators, coroutines, fibers) can avoid this cost by pausing and resuming behavior in a straight-line imperative form; Nystrom notes Bytecode as another escape hatch.

Nystrom flags several pitfalls. Objects are simulated each frame but are not truly concurrent — if A precedes B in the update list, A sees B's previous state while B sees A's new state. True parallelism would need Double Buffer so both see the previous frame. Modifying the object list during iteration breaks loops: additions can let new objects act in their spawn frame (fix: cache the count at loop start); removals shift indices (fix: walk backwards or defer). And iterating over inactive objects wastes cycles and cache lines — the more inactive objects you carry, the more a separate active-only collection earns its keep.

Together with Game Loop and Component, Update Method forms what Nystrom calls "a trinity that often forms the nucleus of a game engine."

### 5.3. Double Buffer: Hiding Work in Progress

Computers are sequential, but users need to see operations as instantaneous. The canonical case is rendering: if game code writes to the framebuffer while the video driver reads it, the driver can race past the renderer and the user sees half of something drawn — the bottom half looks "torn off."

A **buffered class** encapsulates a piece of incrementally-modified state and makes outside code see every edit as a single atomic change. It holds two instances — a *current* buffer and a *next* buffer. Reads go to current; writes go to next; when writes complete, a swap instantly exchanges them. Nystrom's analogy is two stages, one lit for the audience (current) and one dark where stagehands set up the next scene (next). At the transition, the lights switch. The audience never sees the work.

Beyond graphics, the pattern solves subtle sequential-update bugs. A stage of actors where each `update()` can `slap()` another — and the receiver notices only via a `slapped_` flag — propagates slaps through the chain in one frame if actors happen to be ordered front-to-back, but stalls for several frames if ordered back-to-front. The fix is finer-grained buffering: two flags per actor (`currentSlapped_`, `nextSlapped_`), and the stage loops twice per frame — once to update, once to swap. Regardless of array order, a slap is seen exactly one frame after it was delivered, and all actors appear to update simultaneously.

The two main design decisions are *how* to swap (pointer swap: fast but data on "next" is two frames old; data copy: slow but only one frame old, and required when a fixed framebuffer address is imposed by the driver) and the *granularity* (one monolithic pair vs. a pair per object). A clever static-index optimization — a single global `current_` index that every distributed buffer reads — gives the speed of a monolithic swap with the layout of a distributed one.

### 5.4. State: Finite State Machines and Beyond

Input handling for a heroine who can jump, duck, and dive-attack breaks when mutually exclusive flags (`isJumping_`, `isDucking_`) tangle with nested conditionals and every new move reintroduces an old bug. The hint is that the flags *should* be mutually exclusive — an enum, not a pile of booleans.

A **finite state machine** formalizes the cure: a fixed set of states, exactly one current state at a time, inputs that drive transitions to next states. This keeps invalid combinations unrepresentable. The textbook enum-plus-switch implementation works until state-specific data starts leaking into the owning object (a `chargeTime_` that is only meaningful while ducking nonetheless lives on the heroine).

The Gang of Four's **State pattern** moves both behavior and data into per-state classes. Each state implements a `HeroineState` interface; the heroine holds a `HeroineState* state_` and forwards `handleInput()` and `update()` to it. State transitions are now pointer swaps, and per-state data lives where it belongs. Static state instances suffice when a state has no fields (a Flyweight); stateful states need per-FSM allocation.

**Enter and exit actions** are a small but important refinement: a `enter()` method on the new state and an `exit()` on the old one run automatically on transition, consolidating setup code that would otherwise be duplicated across every incoming or outgoing transition.

FSMs have a ceiling — they are not Turing-complete and eventually hit it. Nystrom covers three extensions for the limits:

- **Concurrent state machines** split orthogonal axes (action vs. equipment) into two machines that coexist, avoiding the *n × m* state explosion of one combined machine.
- **Hierarchical state machines** let a state have a superstate; inputs the substate does not handle roll up the chain, the way method overrides fall back to a base class. Standing, walking, and running can all share jump-on-B via an `OnGroundState` superstate.
- **Pushdown automata** replace the state reference with a *stack*. Pushing a `FiringState` when fire is pressed, then popping it when the animation ends, automatically restores whatever state the heroine was in before — standing, running, jumping, or ducking — without a combinatorial explosion of firing-while-X states.

## 6. Working With the Hardware

The final four patterns (plus Flyweight, a GoF pattern Nystrom repositions) concern physical reality: caches, memory, and the cost of asking "what's near here?"

### 6.1. Data Locality: Data Layout is Performance

Modern CPUs have caches because main memory is roughly a hundred times slower than registers. When data is fetched from RAM, the CPU pulls a whole contiguous chunk — a **cache line** (~64–128 bytes). A **cache hit** reuses data already pulled; a **cache miss** stalls the CPU for hundreds of cycles. Two programs doing identical work can differ 50× in speed based on cache miss patterns alone.

The pattern: organize data structures so the things you process next are next to each other in memory, maximizing reuse of each cache line. Three techniques:

- **Contiguous arrays** — store components directly in flat arrays (`AIComponent[]`, `PhysicsComponent[]`), one per type, and walk them in memory order. An array of pointers to entities holding pointers to components forces two cache misses per element per frame; flat arrays eliminate both. Nystrom's reported test: the update loop became 50× faster. The heuristic is "look for `->` operators you can eliminate."
- **Packed data** — keep active objects at the front of the array, inactive at the back, and loop only over the active count. Swapping on activation/deactivation is two assignments, far cheaper than iterating through the inactives' cache lines and paying branch-prediction penalties on an `isActive` check.
- **Hot/cold splitting** — split a struct into fields used every frame (hot: animation, energy, goal position) and fields rarely used (cold: loot drop table). The hot piece stays in the packed array; the cold piece lives elsewhere, pointer-referenced. In real games, deciding what is hot vs. cold is "between a black art and a rathole."

Polymorphism and data locality are in tension. Virtual method calls mean pointer hops; interfaces mean cache-unfriendly indirection. In cache-optimized code paths, Nystrom suggests avoiding subclassing, using separate arrays per concrete type, or accepting the pointer-array form only when the loop is not hot. The Component pattern is the natural companion — splitting entities by domain gives each domain's update a cache-friendly array to walk.

### 6.2. Object Pool: Memory Without Fragmentation

Allocating and freeing constantly is deadly on consoles and mobile: memory is scarce, compacting memory managers are rarely available, and allocation can be slow. **Fragmentation** — the heap accumulating small gaps that no allocation can fit — is a common failure mode of console soak tests, which run games for days in demo mode to certify stability.

An **object pool** preallocates a contiguous block of same-typed objects at startup and hands them out internally. Each object supports an "in use" query. Creation asks the pool for a free object; destruction flips it back. No heap activity after construction. For particles, enemies, visual effects, or currently-playing sounds — anything frequently created and destroyed — this is the canonical answer.

The naive implementation scans linearly for a free slot (O(n)). A **free list** improves on that by threading a singly-linked list through the dead objects themselves — since an inactive particle's position and velocity fields are irrelevant, a `union` reuses that memory for a `next` pointer. O(1) creation and destruction, zero extra memory for the list.

Nystrom catalogues strategies for a full pool: prevent it by tuning size (for gameplay-critical objects), fail silently (one missing sparkle on a full screen is fine), forcibly kill an existing object (for sounds — replace the quietest), or grow the pool. Slot size is fixed, so all slots must be large enough for the largest object; when sizes vary widely, use separate pools per size class. And reused objects are not auto-cleared — discipline every init path, because the previous occupant was the same type, and "almost correct" stale data is harder to debug than zero.

Object Pool versus Flyweight: both keep a collection of reusable objects. Flyweight shares one instance *simultaneously* across many owners; Object Pool reuses an object *over time*, one owner at a time.

### 6.3. Spatial Partition: Neighbors in Log Time

Games constantly ask "what's near this location?" — for physics collisions, audio falloff, AI target selection. A naive pairwise check is O(n²), which collapses to a frame budget with a few hundred RTS units. The underlying problem: the object array has no spatial order, so finding neighbors means scanning everyone.

The pattern is to store objects in a **spatial data structure** organized by position, so that near-location queries are efficient, and to update the structure when objects move. Nystrom's sample is the simplest form: a **fixed grid**. Superimpose a grid of cells; each cell is a doubly-linked list of units within it; collisions are resolved cell-by-cell. Moving a unit between cells is unlinking and relinking a few pointers. For attack ranges crossing cell boundaries, check half the eight neighbors (otherwise each pair is processed twice).

Design decisions:

- **Hierarchical vs. flat**: a flat grid is simple and constant-memory, but degenerates when objects clump. Hierarchical structures (**BSP**, **k-d tree**, **bounding volume hierarchy**) subdivide adaptively. A **quadtree** (or **octree** in 3D) is a hybrid: fixed half-splitting boundaries that subdivide only when a square's population crosses a threshold — cheap incremental updates and balanced queries.
- **Object-dependent vs. independent**: object-independent structures (fixed grid) are cheap to update; object-dependent structures (BSP, k-d tree, BVH) pick boundaries to balance object counts, giving consistent query performance but best computed on a whole set at once — used mostly for static geometry.

Common structures have 1D analogues worth knowing: a grid is persistent bucket sort; BSP / k-d / BVH are variants of binary search tree; quadtree and octree are tries.

Spatial Partition is a memory-for-speed trade. The bookkeeping cost of moving objects between partitions is real — "like a hash table whose keys change spontaneously" — and is worth paying only once `n` and the query volume are large enough.

### 6.4. Dirty Flag: Defer the Work

A scene graph stores each object's transform as a local offset from its parent; the renderer needs the composed **world transform** each frame. Computing it on the fly every frame wastes work on static geometry, but caching eagerly is worse: if the ship, crow's nest, pirate, and parrot all move in one frame, recomputing the parrot after each parent change does the work four times when only the last value is consumed.

A **dirty flag** tracks when derived data is out of sync with primary data. It is set on any primary-data change and checked when the derived data is read: recompute only if dirty. For the scene graph, `setTransform` sets the flag without recursing into children; `render()` threads a dirty parameter down the tree, OR-ing in each node's flag, so each affected world transform is recomputed exactly once per frame.

The pattern applies to both **calculation** (expensive math) and **synchronization** (derived data lives on disk or over a network — transport is what's expensive, e.g., a document editor's unsaved-changes dot, which is a literal dirty flag visualized). Three strategies for *when* to clean the flag trade off visible pauses, predictability, and redundancy:

| Strategy | Upside | Downside |
|----------|--------|----------|
| When the result is needed | Avoids work if never consumed | Visible pause when the user asks |
| At well-defined checkpoints | Hide behind loading screens | Player may never reach checkpoint |
| In the background (timer) | Smooth, tunable cost | Redundant work; requires async support |

Dirty Flag's two dangers: forgetting to set the flag somewhere — "cache invalidation is notoriously hard," and one missed mutation leaves stale derived data — and deferring work that then lands at a bad moment. Funnel mutations through a narrow API to mitigate the first; bound deferral to mitigate the second.

### 6.5. Flyweight: Sharing What's Duplicated

A forest with thousands of trees cannot afford a full mesh, bark texture, leaf texture, position, and tuning parameters per tree — too much memory, too much bus bandwidth each frame. Most of those thousands look similar; mesh and textures are identical across instances.

Flyweight splits the object into two kinds of state:

| Kind | Gang of Four term | Tree example |
|------|-------------------|--------------|
| Shared across instances | **Intrinsic** state | Geometry, textures |
| Unique to each instance | **Extrinsic** state | Position, scale, tint |

One `TreeModel` holds the intrinsic state; each `Tree` instance keeps the extrinsic state plus a pointer to the shared model. Instanced rendering APIs (Direct3D, OpenGL) extend the same split to the GPU: a single common data blob plus a list of per-instance parameters, one draw call for the whole forest. Nystrom notes that Flyweight may be the only Gang of Four pattern with actual hardware support, since the graphics card implements it directly.

The pattern applies beyond the obvious case. A tile-based ground can model terrain as a `Terrain` class with movement cost, wetness, and texture — one instance per terrain type — and the world as a grid of pointers to those instances. All terrain state is intrinsic; the pattern replaces the usual enum-plus-switch with code that is both more expressive and, in Nystrom's measurement, no slower (often faster, depending on memory layout).

**Flyweights are almost always immutable** — since the same object appears in multiple contexts, any mutation would be observable everywhere at once. The memory savings should not become a behavioral surprise.

## 7. The Pattern to Use Sparingly: Singleton

Every other chapter in the book explains how to use a pattern. Nystrom's chapter on **Singleton** explains how *not* to use it. The Gang of Four's definition — "ensure a class has one instance, and provide a global point of access to it" — fuses two separate problems with an "and," and the game industry, moving from C to OOP in the early 2000s, largely ignored the caveat that Singleton should be used sparingly.

Nystrom's core complaint: a Singleton is a global variable, just encapsulated in a class. It inherits every drawback of globals. "You don't really hate global state until you've had to grep a million lines of code at three in the morning." It encourages coupling — a new team member will `#include` the globally visible `AudioPlayer` and couple physics to audio where passing the object in would have made the dependency obvious. It is hostile to concurrency. And lazy initialization, often cited as Singleton's advantage, takes control of *when* memory is allocated away from the game — disastrous on consoles where heap layout is curated to avoid fragmentation.

Worse, Singleton "solves two problems even when you have one." If you Singleton a `Log` for convenient access and later want per-domain loggers, the single-instantiation decision is now baked into every `Log::instance().write(...)` call site in the codebase.

The chapter's alternatives — "What to Do Instead":

1. **See if you need the class at all.** Manager disease (`Particle`, `ParticleManager`, `ManagerManager`) often reflects unfamiliarity with OOP. Move behavior onto the class it serves.
2. **Single instantiation without global access.** A constructor that `assert`s a static `instantiated_` flag is false, flips it true, and resets on destruct — enforces uniqueness without granting global visibility.
3. **Convenient access without globals.** Pass the object in (dependency injection); give the base class a protected accessor (tying to Subclass Sandbox); or piggyback services on the one `Game` or `World` instance most codebases already have (`Game::instance().getAudioPlayer()`). If global access really is needed, use a Service Locator, which is at least more flexible.

Nystrom notes he has never used the full Gang of Four Singleton in a game.

## 8. Key Takeaways

- **Architecture's job is to reduce how much code you must load into your head before you can make progress.** Every other recommendation in the book serves this goal.
- **Decoupling is the single most reused technique.** Command, Observer, Event Queue, Component, and Service Locator are five shapes of replacing a direct call with an indirect one so the caller and callee no longer need to know about each other.
- **Balance three "speeds":** long-term development speed, runtime speed, and short-term development speed. They pull against each other; there is no right answer, only tradeoffs.
- **Simplicity is the best lever on all three speeds.** A simple solution is a distillation of code, not an accretion; it takes more effort to write, not less.
- **Move behavior into data when content-authoring throughput is the bottleneck.** Type Object, Bytecode, and data-driven Prototype let designers iterate without programmers. Bytecode is the most complex pattern in the book — reach for it with care.
- **The game loop is a control pattern with performance consequences.** Decouple updating from rendering; keep physics on a fixed step and render whenever possible; extrapolate to hide residual lag.
- **Data layout is performance.** Caches reward contiguous, domain-sliced arrays walked in order. Pointer chasing, polymorphism in hot paths, and flag-and-skip loops all fight the hardware. A 50× speedup is possible from layout alone.
- **Object Pool beats heap fragmentation; Spatial Partition beats O(n²) proximity queries.** Both are memory-for-speed trades worth only their weight in large `n`.
- **Dirty Flag defers expensive derivation until it is actually needed.** Its hazards are missed invalidations and deferred work that lands at the wrong moment.
- **Singleton is the pattern to temper.** It is a global variable wrapped in a class and carries all of globals' costs. Prefer passing objects, or if access truly must be ambient, use Service Locator — ideally with a null service and a logging decorator.
- **Flyweight splits shared intrinsic state from unique extrinsic state.** Flyweights are almost always immutable; their memory sharing should not become behavior.
- **Most of the craft is in knowing when *not* to apply a pattern.** Speculative flexibility is as costly as none at all. YAGNI.
