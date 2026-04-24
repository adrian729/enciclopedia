# Ch 2: Command

## Table of Contents

- [1. The Pattern](#1-the-pattern)
- [2. Configuring Input](#2-configuring-input)
- [3. Directions for Actors](#3-directions-for-actors)
- [4. Undo and Redo](#4-undo-and-redo)
- [5. Commands as Closures](#5-commands-as-closures)
- [6. See Also](#6-see-also)

## 1. The Pattern

- **A command is a reified method call** — a method call wrapped in an object you can store in a variable, pass to a function, queue, or log. "Reify" means "make real" or "first-class"
- **Gang of Four definition** — "Encapsulate a request as an object, thereby letting users parameterize clients with different requests, queue or log requests, and support undoable operations"
- **Alternate Gang of Four slugline** — *"Commands are an object-oriented replacement for callbacks"*
- **Related concepts** — callback, first-class function, function pointer, closure, partially applied function. In languages without closures, Command emulates them
- **Tell-tale signature** — an interface with a single method that returns nothing (e.g. `execute()`) is very likely the Command pattern

## 2. Configuring Input

- **The problem** — input handlers that hard-wire buttons to actions (`if (isPressed(BUTTON_X)) jump();`) cannot be remapped at runtime
- **The fix** — replace each direct call with a `Command` object held in a variable per button. Input handling becomes `buttonX_->execute()`, and rebinding is just reassigning the pointer
- **Base class** — `class Command { virtual void execute() = 0; };` with subclasses like `JumpCommand`, `FireCommand` wrapping the underlying call
- **Null Object** — instead of NULL-checking empty bindings, bind unused buttons to a command whose `execute()` does nothing. This is the Null Object pattern

## 3. Directions for Actors

- **The limitation of simple commands** — if `JumpCommand::execute()` calls a global `jump()`, only the player can jump. The actor is implicitly coupled in
- **Pass the actor in** — change the signature to `execute(GameActor& actor)`. One `JumpCommand` instance can then drive any character
- **Input handler returns commands** — `handleInput()` returns a `Command*` instead of executing it. Separate dispatch code pairs the command with the right actor and runs it. This delay is only possible because the command is reified
- **AI reuses the same interface** — AI modules emit the same `Command` objects the input handler does. Different AIs can be swapped to drive different actors, or even attached to the player for demo mode
- **Think of commands as a stream** — producers (input, AI) push commands; consumers (dispatcher, actor) pull them. Decouples producer from consumer
- **Serializable commands enable multiplayer** — push the stream of commands over the network and replay on the other machine

## 4. Undo and Redo

- **Natural fit** — if a command object can *do* a thing, a small addition lets it *undo* the thing. Adds `virtual void undo() = 0;` to the interface
- **One-shot commands** — for undo, commands are no longer reusable "move something" objects; they're specific concrete moves bound to a target and created per player action (e.g. `new MoveUnitCommand(unit, x, y)`)
- **Remember previous state** — `execute()` captures the pre-change state (e.g. `xBefore_`, `yBefore_`) before mutating; `undo()` restores it
- **Single-level undo** — keep the last command executed. Ctrl-Z calls its `undo()`. Redo re-runs `execute()`
- **Multi-level undo** — keep a list of commands plus a "current" pointer. Execute appends and advances; undo moves the pointer back; redo advances. Choosing a new command after undos discards everything after current
- **Memento comparison** — the Gang of Four's Memento pattern is rarely a good fit here, since commands modify only a small slice of state and snapshotting the whole object wastes memory. Storing just the changed bits is cheaper
- **Persistent data structures** — alternative where each modification returns a new object sharing data with the old; undo is just switching back to the previous reference
- **Replay, not redo** — games rarely need redo, but often need replay. Record the set of commands every entity performed each frame, then re-run the simulation with them instead of snapshotting full game state

## 5. Commands as Closures

- **Why classes in the samples?** — C++ has weak first-class-function support: function pointers are stateless, functors still need a class, and lambdas are awkward with manual memory management
- **In languages with real closures, use them** — a JavaScript `makeMoveUnitCommand(unit, x, y)` that returns a function is the Command pattern
- **Classes still useful even with closures** — when a command has multiple operations (e.g. `execute` + `undo`), mapping it to a single function is awkward. A class also makes the captured state visible, whereas closures can hide it

## 6. See Also

- **Subclass Sandbox** — when many command classes share behavior, a concrete base with helper methods that derived commands compose turns `execute()` into the Subclass Sandbox pattern
- **Chain of Responsibility** — when an object may handle a command itself or pawn it off to a subordinate, especially in hierarchical models, you're in Chain of Responsibility territory
- **Flyweight** — stateless commands like `JumpCommand` waste memory with multiple instances; Flyweight addresses that. (Singletons also work, but *"friends don't let friends create singletons"*)
