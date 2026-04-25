# Ch 14: Procedural Enemy Waves

## Table of Contents

- [1. What Wave Spawning Is For](#1-what-wave-spawning-is-for)
- [2. Method 1: Spawn by Timer](#2-method-1-spawn-by-timer)
- [3. Method 2: Spawn on Completion](#3-method-2-spawn-on-completion)
- [4. Method 3: Continuously Escalating Total](#4-method-3-continuously-escalating-total)
- [5. Method 4: Hitpoint Progression](#5-method-4-hitpoint-progression)
- [6. Method Comparison](#6-method-comparison)
- [7. Closing Thoughts](#7-closing-thoughts)

## 1. What Wave Spawning Is For

- **Waves and "adds"** — PvE games regularly throw groups of enemies at the player either as distinct waves or as individual additions ("adds") joining a fight in progress; sometimes triggered events, sometimes whole levels built around fighting waves.
- **Blizzard examples cited**:
  - **StarCraft 2: Wings of Liberty — "Mar Sara 3: Zero Hour"** — survive 20 minutes of attacks; called a **holdout** mission.
  - **World of Warcraft — Gluth in Naxxramas** — boss spawns zombies every 10 seconds.
  - **Diablo III — Cursed Chests** — exactly one minute, monsters spawn continuously, spawn rate scales with kill rate; killing 100+ monsters grants extra reward.
- **Four methods compared in this chapter** — Spawn by Timer, Spawn on Completion, Continuously Escalating Total, Hitpoint Progression.

## 2. Method 1: Spawn by Timer

- **Algorithm** — each wave has a scheduled mission time; when the clock passes that time, the wave spawns regardless of what the player is doing.
- **Best fit** — testing whether the player has reached a target level of mechanical proficiency when the player's power level is fixed and consistent across the audience.
- **Snowball risk** — if the designer expects 15 s/wave but the player needs 18–19 s, leftover enemies stack on the next wave, then the wave after that, until the player is overwhelmed; equally, slightly stronger players blow through every wave and get bored.
- **StarCraft holdouts** — fitting use case because player power on a given mission is well known and the goal is strategic competence.
- **Two responses to fast players** — wait for the timer (simpler, rewards finishing early, risks dead air) or fall through to the next wave immediately (effectively merging with Spawn on Completion; watch for incentives to drag fights out via regen/cooldowns).

## 3. Method 2: Spawn on Completion

- **Algorithm** — the next wave triggers only when no enemies from the previous wave are alive.
- **Best fit** — keeping a minimum performance bar while staying somewhat adaptive; struggling on one wave doesn't poison the next.
- **WoW "Battle for Mount Hyjal"** — 10 waves per cycle followed by a boss; balances minimum-skill gating with continuous engagement.
- **Multi-vector testing** — separate waves can probe different player strengths (e.g., a spaceship game testing missiles, lasers, then shields); weak vectors hurt locally without sinking the run.
- **Drag-the-last-enemy exploit** — players may keep one monster alive to recover health, resources, and cooldowns; a partial fix is to OR this method with a Spawn-by-Timer fallback, accepting a controlled dose of snowball risk in exchange.
- **Tension and release** — wave structure is visible to the player, allowing alternating high-tension and breather phases.

## 4. Method 3: Continuously Escalating Total

- **Algorithm** — at any time `t`, a minimum live-enemy count is required; each tick, if fewer enemies are alive than the current threshold, more spawn until the threshold is met. The threshold grows over time.
- **End condition cannot be "kill them all"** — the fight must end on time limit or kill total instead, since the spawner refills.
- **Best fit** — dramatic arcs, bonus levels, and contexts where the player's true power level is hard to estimate; the player measures progress against themselves over runs.
- **Diablo III Cursed Chests** — one-minute window, faster kills produce faster spawns, the goal is "how many enemies can you defeat" rather than survival or victory.
- **Completion-criterion interaction with player power** — important design knob:

| Completion criterion | Effect of stronger player |
|---|---|
| Time-limited | Cannot finish faster |
| "Kill X enemies" | Finishes faster |
| "How far can you get" | Takes longer (more progression to chew through) |

- **Caution** — sustained escalation is mentally exhausting; not suitable for long stretches of play.

## 5. Method 4: Hitpoint Progression

- **Algorithm** — each wave has a percentage threshold; when the previous wave's summed current HP / summed max HP drops below that threshold, the next wave spawns. Spawning happens while the previous wave is still alive, producing a continuous stream.
- **Adaptive by construction** — strong players trigger waves faster, weak players slower; dramatic encounter pacing without overwhelming under-leveled players.
- **Best fit** — large variance in player power due to skill or progression, where the goal is a fun, dramatic fight for the widest audience.
- **Tradeoff** — because the rate auto-adjusts, this method cannot be used to test or measure player performance.
- **Like Spawn on Completion** — designers can craft individual waves that are challenging, thematic, or vector-specific, while the adaptive trigger prevents under-power players from being run over.

## 6. Method Comparison

| Method | Trigger | Adaptive? | Best for | Watch out for |
|---|---|---|---|---|
| **Spawn by Timer** | Elapsed time | No | Testing mechanical skill at known fixed power level; precisely designed pacing | Snowballing under weaker players; boredom under stronger players |
| **Spawn on Completion** | Previous wave fully defeated | Mild | Minimum-bar gating with engagement; multi-vector testing; tension/release | Players dragging out the last enemy to recover; mitigated by combining with timer |
| **Continuously Escalating Total** | Live-enemy count below time-indexed threshold | Self-pacing intensity | Dramatic arcs, bonus events, measuring players against themselves over runs | Mentally exhausting in long sessions; pick the right end criterion (time / kill count / "how far") |
| **Hitpoint Progression** | Previous wave's HP fraction below threshold | Most adaptive of the four | Wide-variance audiences; dramatic, continuous combat | Useless for measuring player power |

## 7. Closing Thoughts

- **Small spawn-rule changes shift player experience drastically** — the four methods differ on intensity, challenge, pacing, exploitation resistance, and balance; pick or combine techniques on the basis of the gameplay's specific needs.
- **These four are illustrative, not exhaustive** — wave spawning has many more possibilities; the chapter offers them as adaptable starting points.
