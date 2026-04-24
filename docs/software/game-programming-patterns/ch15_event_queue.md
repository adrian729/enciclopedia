# Ch 15: Event Queue

## Table of Contents

- [1. The Problem](#1-the-problem)
- [2. The Pattern](#2-the-pattern)
- [3. When to Use It](#3-when-to-use-it)
- [4. Building the Queue (Sample Code)](#4-building-the-queue-sample-code)
- [5. Design Decisions](#5-design-decisions)
- [6. Keep in Mind](#6-keep-in-mind)
- [7. Related Patterns](#7-related-patterns)

## 1. The Problem

Motivated by a synchronous `Audio::playSound(id, volume)` API called from all over the codebase.

- **Problem 1: API blocks the caller** — `playSound()` doesn't return until the sound is actually playing. Loading a sound from disc freezes the rest of the game for several frames
- **Problem 2: requests can't be processed in aggregate** — two enemies wailing in the same frame sum their identical waveforms into one sound at double volume. Boss fights exceed the hardware channel limit and sounds get cut off. The API sees each `playSound()` call through a pinhole
- **Problem 3: requests are processed on the wrong thread** — synchronous calls run on the caller's thread, so the audio code is hammered concurrently by rendering, AI, and gameplay threads while the dedicated audio thread sits idle
- **Common theme** — the engine treats each call as "drop everything and play this right now." Immediacy is the problem. Fix it by decoupling receiving a request from processing it

## 2. The Pattern

> A **queue** stores a series of **notifications** or **requests** in first-in, first-out order. Sending a notification enqueues the request and returns. The request processor processes items from the queue at a later time. Requests can be handled directly or routed to interested parties. This decouples the sender from the receiver both statically and **in time**.

- **GUI event loops** are the canonical example: the OS fills a queue with user input, and `getNextEvent()` pulls the oldest one when the app is ready
- **Central event bus** — a game-wide queue used as the backbone for decoupled high-level communication (e.g., combat system posts "enemy died" events; tutorial engine registers to receive them). Similar in spirit to AI **blackboard systems**

## 3. When to Use It

- **Only when you need to decouple in time.** If you just need to decouple *who* receives a message from the sender, Observer or Command are simpler
- **Push/pull mismatch** — sender A naturally pushes, receiver B naturally pulls at a convenient moment in its own cycle. A queue is the buffer between them
- **Queues give control to the receiver** — delay, aggregate, or discard. The cost: the sender loses control and can't get a response. Poor fit when the sender needs a reply

## 4. Building the Queue (Sample Code)

Three refinements applied in order to the audio engine:

- **Reify the request** — a `PlayMessage { SoundId id; int volume; }` struct captures a pending call so it can be stored and processed later
- **Plain array backing store** — preferred over fancy data structures: no dynamic allocation, no bookkeeping overhead, cache-friendly contiguous memory. Size the array to cover the worst case
- **`playSound()` just appends; `update()` drains** — called from the main loop or a dedicated audio thread (this is the Update Method pattern)
- **Ring buffer** — a queue that leaves the array in place. Terms:
  - **head** — oldest pending request; where the processor reads
  - **tail** — one past the newest; where the next enqueue writes. Half-open range so head == tail means empty
  - Wrap both pointers modulo array size; unused cells at the front get reused as the tail wraps around. No shifting, no allocation, still cache-friendly
  - A growable array with doubling still gives constant amortized enqueue if the fixed cap is unacceptable
- **Aggregating requests** — on enqueue, scan pending requests for a matching `SoundId` and merge (keep the louder volume). Solves the "same sound twice = double loud" bug
  - Tradeoff: processing on enqueue puts O(n) cost on the caller; a hash table keyed on `SoundId` gives O(1). Aggregating in `update()` instead shifts the burden
  - The aggregation window equals the queue's fill depth — lag lets more requests batch together, which can visibly affect behavior
- **Spanning threads** — with sender and receiver decoupled and the queue encapsulated, make `playSound()` and `update()` thread-safe. `playSound()` does tiny work and can lock briefly; `update()` waits on a condition variable instead of spinning

## 5. Design Decisions

### 5.1. What goes in the queue?

| Kind | Describes | Typical listeners | Scope |
|------|-----------|-------------------|-------|
| **Event / notification** | Something that already happened ("monster died") | Multiple | Broader, often global. Asynchronous cousin of Observer |
| **Message / request** | Something we want to happen ("play sound") | Typically one (async API to a service) | Narrower. Akin to Command, or a service locator |

### 5.2. Who can read from the queue?

- **Single-cast** — one reader owns the queue. Natural when the queue is an implementation detail of a class's public API (as in the audio example). Most encapsulated; avoids contention between listeners
- **Broadcast** — every listener sees every event, like most GUI event systems. Events are dropped when no listener is registered; typically needs filtering so listeners see only relevant events
- **Work queue** — multiple listeners, but each item goes to exactly one of them. Common for parceling jobs to a pool of threads. Requires scheduling (round robin, random, or prioritized)

### 5.3. Who can write to the queue?

Pattern supports all of: one-to-one, one-to-many ("fan-out"), many-to-one ("fan-in"), many-to-many.

- **Single writer** — closest to synchronous Observer. Listeners implicitly know the source
- **Multiple writers** — `playSound()` is public, anyone calls it. Easier to create feedback loops, and listeners usually need the sender's identity packed into the event

### 5.4. Lifetime of queued objects

With a queue, the message outlives the enqueuing call, so ownership matters in non-GC languages:

- **Pass ownership** — queue takes the message on enqueue, receiver takes it on dequeue and frees it (`unique_ptr<T>`)
- **Share ownership** — message lives as long as anything references it (`shared_ptr<T>`)
- **Queue owns it** — messages live inside the queue itself; sender asks the queue for a fresh slot and fills it in. The backing store is effectively an Object Pool

## 6. Keep in Mind

- **A central event queue is a global variable** — wraps shared state in a protocol but carries all the dangers of globals
- **The world can change under you** — an "entity died" event may be processed many frames later, by which time the entity is deallocated and its surroundings have moved. Queued events must capture all ephemeral data the receiver will need; they tend to be heavier than synchronous notifications
- **Feedback loops** — A's event triggers B's event which triggers A's event. In synchronous systems the stack overflows fast; in a queue the asynchrony unwinds the stack and spurious events silently slosh forever. Common rule: don't send events from inside an event handler. Add debug logging to the event system

## 7. Related Patterns

- **Observer** — event queues are the asynchronous cousin
- **Message queue / publish-subscribe (pubsub)** — same idea, typically applied to distributed systems rather than in-process
- **State / finite state machine** — async input streams feed naturally into queues. Many state machines, each with its own queue (**mailbox**), reinvent the **actor model** of computation
- **Go's channel** — a built-in event/message queue
