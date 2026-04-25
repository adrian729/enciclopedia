# Ch 7: State

## Table of Contents

- [1. The Problem](#1-the-problem)
- [2. Finite State Machines](#2-finite-state-machines)
- [3. Enums and Switches](#3-enums-and-switches)
- [4. The State Pattern](#4-the-state-pattern)
- [5. Where Do State Objects Live?](#5-where-do-state-objects-live)
- [6. Enter and Exit Actions](#6-enter-and-exit-actions)
- [7. Extensions to FSMs](#7-extensions-to-fsms)
- [8. When FSMs Are a Good Fit](#8-when-fsms-are-a-good-fit)

## 1. The Problem

- **Heroine input handling** — implement jump, duck, dive-attack, and prevent combinations like air-jumping. Naive code accumulates `isJumping_`, `isDucking_` boolean flags and nested conditionals
- **Every new move breaks an old one** — dive-attack lets you air-jump again; ducking mid-jump standing graphic leaks into a dive. Complex branching + mutable state are the two error-prone code shapes tangled together here
- **Hint** — when flags are mutually exclusive (e.g. `isJumping_` and `isDucking_` should never both be true), you really want an enum

## 2. Finite State Machines

- **FSM gist**:
  - A fixed set of **states** (standing, jumping, ducking, diving)
  - The machine is in **exactly one state at a time** — preventing invalid combos is part of the point
  - A sequence of **inputs/events** arrives (button presses/releases)
  - Each state has **transitions** keyed by input, pointing to a next state. Inputs with no matching transition are ignored
- **From automata theory** — FSMs are the simplest member of the family that also includes the Turing machine
- **Text-adventure analogy** — Zork-style rooms are states, exits are transitions, `"go north"` commands are inputs

## 3. Enums and Switches

- **Replace boolean flags with a single `state_` enum** — `STATE_STANDING`, `STATE_JUMPING`, `STATE_DUCKING`, `STATE_DIVING`. Invalid combinations become unrepresentable
- **Switch on state first, then input** — keeps all code for a single state lumped together (the earlier layout smeared each state across the input branches)
- **Where it breaks down** — adding a charge-up attack while ducking requires a `chargeTime_` field on `Heroine` that's only meaningful in one state, plus update logic in two methods. Data and behavior specific to a state leak into the owning object

## 4. The State Pattern

- **Gang of Four definition** — *"Allow an object to alter its behavior when its internal state changes. The object will appear to change its class."*
- **State interface** — every state-dependent behavior (`handleInput()`, `update()`) becomes a virtual method on a `HeroineState` interface
- **Class per state** — `StandingState`, `DuckingState`, etc. implement the interface; each old `switch` case moves into the matching class
- **State-local data** — `chargeTime_` moves out of `Heroine` and into `DuckingState`, where it's only meaningful. The object model now reflects that data's scope explicitly
- **Delegate from the owner** — `Heroine` holds a `HeroineState* state_`; `handleInput()` and `update()` just forward to it. Changing state means reassigning `state_`
- **Distinguish from Strategy and Type Object** — all three delegate to a subordinate object; the *intent* differs:

  | Pattern | Goal |
  |---------|------|
  | Strategy | Decouple the main class from a portion of its behavior |
  | Type Object | Make many objects behave similarly by sharing a type object |
  | State | Let the main object change its behavior by changing the object it delegates to |

## 5. Where Do State Objects Live?

- **Static states** — if a state has no fields, one instance is enough for all FSMs; store it as a static member (e.g. `HeroineState::standing`). This is the Flyweight GoF pattern. Cheapest option
- **Function-pointer shortcut** — if a state has no fields *and* only one virtual method, replace the class with a plain function and make `state_` a function pointer
- **Instantiated states** — required when a state holds per-FSM data (like `chargeTime_`). Allocate on transition; free the old state carefully (don't delete the state whose method is currently running)
- **Safe swap idiom** — `handleInput()` returns a new state (or `NULL` for "stay"); the `Heroine`'s outer wrapper deletes the old state and swaps in the new one *after* the method returns
- **Nystrom's preference** — static states when possible (no allocation per transition); instantiated when stateful. Dynamic allocation may require Object Pool to avoid fragmentation

## 6. Enter and Exit Actions

- **Problem** — when ducking transitions to standing, the *ducking* state currently sets the standing graphic. Each state isn't fully encapsulated
- **Entry action** — a virtual `enter()` method called on the *new* state after a transition. `StandingState::enter()` sets the standing graphic itself
- **Why it matters** — real state graphs have multiple transitions *into* the same state (lands from jump, lands from dive, releases duck — all end in standing). Entry actions consolidate that duplicated setup in one place
- **Exit action** — symmetric: method called on the state being left, right before the switch

## 7. Extensions to FSMs

- **FSMs aren't Turing complete** — their constraint (fixed states, single current state, hardcoded transitions) is their virtue *and* their limit. Complex game AI will hit the ceiling

### 7.1. Concurrent State Machines

- **Combinatorial explosion** — adding "carrying a gun" doubles every existing state (standing, standing-with-gun, jumping, jumping-with-gun, ...). Two axes of state crammed into one machine need *n × m* states; two separate machines need only *n + m*
- **Fix** — give the heroine two independent state references (`state_` for action, `equipment_` for gear). Delegate inputs to both
- **Interaction** — when states do interact (no firing while jumping, etc.), crude `if` checks on the other machine's state coordinate them. Inelegant but works
- **Input consumption** — a fuller system would let one machine consume an input so the other doesn't also react

### 7.2. Hierarchical State Machines

- **Shared behavior across similar states** — standing, walking, running, sliding all share jump-on-B and duck-on-down. Duplicating across states is wasteful
- **Superstate / substate** — a state can have a superstate; unhandled inputs roll up the chain. Mirrors inherited-method overriding
- **Implementation via class inheritance** — define an `OnGroundState` base that handles jump/duck; `StandingState`, `DuckingState`, etc. inherit and add specifics, falling back to `OnGroundState::handleInput()` for uncovered inputs
- **Alternative implementation** — an explicit stack of states, with the top of the stack as the current state and its superstates beneath; walk down until one handles the input

### 7.3. Pushdown Automata

- **Problem** — plain FSMs have no history. After firing, the heroine should return to whatever state she was in (standing/running/jumping/ducking), but the machine has already forgotten
- **Naive workaround** — a separate firing-while-X state per X, each hardcoded to return to X. Explodes the state count
- **Pushdown automaton** — the state reference becomes a *stack*. Two extra operations beyond plain transition:
  1. **Push** a new state: current state becomes the top of the stack, previous state remains beneath it
  2. **Pop** the topmost state: discards it; the state below becomes current
- **Firing solution** — one `FiringState`. Push it when fire is pressed, pop it when the animation ends. The PDA automatically restores the prior state
- **Distinct from hierarchical FSMs** — both use a stack of states, but the stacks represent entirely different things and solve different problems

## 8. When FSMs Are a Good Fit

- **Scope** — modern AI trends toward behavior trees and planning systems; FSMs alone won't carry complex AI. But they remain an excellent modeling tool when:
  - An entity's behavior changes based on internal state
  - That state divides into a small number of distinct options
  - The entity responds to a stream of inputs/events over time
- **Common uses** — AI (historically), user input handling, menu navigation, text parsing, network protocols, any asynchronous behavior
