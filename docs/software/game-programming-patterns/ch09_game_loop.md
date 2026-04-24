# Ch 9: Game Loop

## Table of Contents

- [1. The Problem](#1-the-problem)
- [2. The Pattern](#2-the-pattern)
- [3. When to Use It](#3-when-to-use-it)
- [4. Timing Strategies](#4-timing-strategies)
- [5. Design Decisions](#5-design-decisions)
- [6. Keep in Mind](#6-keep-in-mind)

## 1. The Problem

- **Batch mode programs** — old-style: feed input in, wait, get output, done. Shell scripts fit this mould
- **Event loops** — modern GUI apps sit idle waiting for user input, then dispatch. Blocking on input is fine for a word processor but wrong for games
- **Games never stop moving** — even with no user input, animation plays, effects sparkle, the monster keeps chomping. "Idle" events in a standard event loop are too rudimentary
- **Two factors determine frame rate in a naive loop**: (a) how much work is done per frame, (b) speed of the underlying platform
- **Old fixed-hardware era** — NES/Apple IIe games were coded for one CPU. Running them on faster hardware made them *too fast*. Old PCs had "turbo" buttons to slow the machine down so old games were playable
- **Modern reality** — developers rarely know exactly what hardware the game will run on. The game must adapt

## 2. The Pattern

- **Definition** — a game loop runs continuously during gameplay. Each turn it: processes user input without blocking, updates the game state, and renders the game. It tracks the passage of time to control the rate of gameplay
- **Skeleton**:

  ```
  while (true) { processInput(); update(); render(); }
  ```

- **"Tick" and "frame"** — common names for one crank of the loop
- **Two key jobs** — (1) process input without waiting for it, (2) run the game at a consistent speed despite hardware differences

## 3. When to Use It

- **You will use it** — even if you don't write it. If you use a game engine, the engine owns the loop and calls into your code; with a library, you own the loop and call into the library
- **Even turn-based games need it** — game state waits on the player, but animation and music keep playing during the "wait"

## 4. Timing Strategies

The heart of the chapter: several named approaches to controlling gameplay speed.

- **Run, run as fast as you can** — the simplest loop spins as fast as the machine allows. Fast machine: unplayably fast. Slow machine: crawl. Content-heavy scenes play slower than simple ones. Only virtue: simplicity
- **Take a little nap (fixed time step with synchronization)** — after processing a frame, `sleep()` until the target frame budget (e.g., 16 ms for 60 FPS) is spent. Caps too-fast hardware; saves battery. Does *nothing* for too-slow hardware — if the frame takes longer than the budget, the game slows down
- **Variable / fluid time step** — measure `elapsed` since last frame and pass it to `update(elapsed)`. A bullet scales its position by elapsed time; it crosses the screen in the same real time whether in 20 small steps or 4 big ones. Trade-offs:
  - Adapts to both too-slow and too-fast hardware
  - **Non-deterministic and unstable** — floating-point rounding accumulates differently on different machines (a networked bullet ends up in different places for Fred's fast PC vs. George's grandmother's antique); physics damping is tuned to a specific step and can "blow up" when the step varies (objects launching into the air). Most game developers recommend against it
- **Play catch up (fixed update time step, variable rendering)** — decouple updating from rendering. Keep physics/AI on a fixed step for stability; render whenever possible:

  ```
  previous = now; lag = 0
  while (true) {
    elapsed = now - previous; previous = now; lag += elapsed
    processInput()
    while (lag >= MS_PER_UPDATE) { update(); lag -= MS_PER_UPDATE }
    render()
  }
  ```

  - `MS_PER_UPDATE` is the simulation granularity, not the visible frame rate. Make it short (often faster than 60 FPS) for high-fidelity sims on fast machines, but *greater* than update time on the slowest hardware — otherwise the game can never catch up
  - Safeguard: cap the inner loop to a maximum iteration count so the game slows rather than locking up
  - Result: constant-rate simulation across hardware; the player's window into the game just gets choppier on slow machines

- **Stuck in the middle: residual lag and extrapolation** — `render()` usually happens *between* two updates, so objects appear at a stale position. The leftover `lag` tells us exactly how far between updates we are. Pass `lag / MS_PER_UPDATE` (a value in 0 to <1) to `render()`, which extrapolates object positions forward by that fraction. Bullet at 20 px moving 400 px/frame at 0.5 between frames renders at 220 px — smooth motion
- **Extrapolation is a guess** — the bullet might actually hit an obstacle next update. These corrections are usually less noticeable than the stutter you get without extrapolation

## 5. Design Decisions

- **Do you own the game loop, or does the platform?**

  | Option | Upside | Downside |
  |--------|--------|----------|
  | Platform's event loop | Simple; plays nice with host | Lose control over timing; most app event loops weren't designed for games |
  | Game engine's loop | Don't have to write it; tight loop already tuned | Don't get to write it — lose control if needs don't match |
  | Write it yourself | Total control, tuned to the game | Must interface with platform; explicitly hand off time to frameworks so they don't hang |

- **How do you manage power consumption?**
  - **Run as fast as it can** — typical PC choice; spare cycles go to higher FPS or graphic fidelity. Great experience, big battery drain
  - **Clamp the frame rate** — typical mobile choice; target 30 or 60 FPS and sleep leftover time. "Good enough" gameplay with battery life

- **How do you control gameplay speed?** Summary of the strategies above:

  | Strategy | Simple? | Adapts to slow HW? | Adapts to fast HW? | Deterministic? |
  |----------|---------|--------------------|--------------------|----------------|
  | Fixed step, no sync | Yes | No | No (runs too fast) | Yes |
  | Fixed step with sync | Yes | No (game slows) | Yes | Yes |
  | Variable time step | Moderate | Yes | Yes | No |
  | Fixed update, variable render | Most complex | Yes | Yes | Yes |

## 6. Keep in Mind

- **It's in the hot 10%** — the loop runs every frame; minor bugs or perf issues have large impact. Take care with this code
- **Coordinate with the platform's event loop** — on Windows, `main()` can host the game loop and call `PeekMessage()` (non-blocking) to drain OS events. On the web, the browser's event loop runs the show and the game hooks in via `requestAnimationFrame()`
- **Further reading** — Glenn Fiedler's "Fix Your Timestep" is the classic article; Witters' article is a close runner-up; Unity's loop is detailed in a published illustration
