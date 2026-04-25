# Ch 7: Designing for Narrative Momentum

## Table of Contents

- [1. The Narrative Slump](#1-the-narrative-slump)
- [2. Only Forwards Design](#2-only-forwards-design)
- [3. ink and the Weave Structure](#3-ink-and-the-weave-structure)
- [4. Knowledge as an Acyclic Directed Graph](#4-knowledge-as-an-acyclic-directed-graph)
- [5. Rules for Momentum](#5-rules-for-momentum)

## 1. The Narrative Slump

- **Raymond Chandler's rule** — *"When in doubt, have a man come through the door with a gun in his hand."* Games have over-internalised this; henchmen keep spawning. Yet games still suffer the opposite problem: the story stalls, Nathan Drake stares into space, the game waits for the player to cue the next line.
- **Games compound the problem** — built on loops and repetition, not surprise and escalation. Players drive without knowing what they're supposed to do, can fail at every turn, and are free to waste time doing nothing. Philip Marlowe never does that.
- **Momentum is velocity × mass** — importance multiplied by rate of change. If the world only reacts to the player's inputs, its momentum is whatever the player puts in.

## 2. Only Forwards Design

- **Action games use cinema's trick** — worlds that look open are actually corridors with one-directional valves (mudslides, lifts, helicopter drops) keeping the player in drive. Naughty Dog's waist-high walls signal a coming ambush; reused levels get flooded or reversed.
- **CYOA books** — acyclic directed graphs that branch and rejoin but always flow forwards. Fighting Fantasy (Livingstone & Jackson) added hidden side paths coded as rules (*"add 7 to the current paragraph number to use the gold key on a paragraph beginning with 'Red'"*), leading players to read the books out of order to reverse-engineer the puzzles.
- **Backtracking kills the world** — once you allow revisiting and dialogue-farming, locations become frozen-in-time waxwork museums: shopfronts without shops, bartenders polishing one mug forever, villagers wringing hands about the werewolf nobody fights. The problem scales badly.

## 3. ink and the Weave Structure

- **80 Days** — players see ~3% of 750,000 words per playthrough. Design ethos: *"only forwards, whichever way you want"*. The time-limited premise justifies no backtracking and makes "failing" a scenario an active choice pushing forward.
- **Weave** — the core structure in Inkle's **ink** mark-up language. Text and options flow top-to-bottom. Options marked with `*` lead to branches that rejoin at gather points (`-`); whatever the player picks, flow falls to the end.
- **Paragraph labels as conditionals** — each label (e.g. `zany`, `dull`) can be set only in one place in the entire script, and once set can never be unset. That makes `london.zany` a reliable test no matter how long the script grows. Intrinsically only-forwards.
- **Sequences and loops** — braced alternatives (`{first time|later visits}`) advance on each visit and can't be reset. Options default to once-only; `+` marks a reusable option (e.g. "Leave"). The *Sorcery!* hub pattern: choices unlock as discovered, each exhausts itself, the `Leave` option bounces the flow onward. If a player re-enters an emptied *Sorcery!* location, the text is reduced to a sentence or skipped.

## 4. Knowledge as an Acyclic Directed Graph

- **Heaven's Vault** — archaeology-adventure with 3D environments unlocked in any order. Early playtests looked like a Roomba executing its program: hoover up all interaction hotspots in a room, move on. The game needed to be *about understanding the world*, not manipulating it.
- **Knowledge chains** — knowledge starts vague and becomes more specific. Two rules: (1) once a fact is learned it can never be unlearned; (2) learning a fact automatically learns all preceding facts. Example chain: *Going around the world → Got 80 days → It's a bet* — discovering the bet for-free learns the 80-day target.
- **The `between` test** — script lines are gated by knowledge *intervals*, not single states:

```
* {between(GOING_AROUND_WORLD, ITS_A_BET)}
  I asked Monsieur Fogg if there was anywhere particular in the world...
```

- **Why intervals** — the test asks "does the player know enough for this to make sense, but not so much that it's redundant?" Future-proof: inserting new states mid-chain doesn't break existing checks because only the interval endpoints matter.
- **Knowledge webs** — chains can branch and rejoin like CYOA graphs. *Heaven's Vault* has over 1,500 knowledge states across ~700 chains, some 10 states long, some single-state (glorified Booleans that may be extended later without breaking anything).
- **Writing workflow** — lay out the knowledge map, then write content, then mark content with minimum (unlock) and maximum (redundancy) requirements. The map is static; the writer doesn't need to think through flow, order, or cause and effect while drafting.

## 5. Rules for Momentum

- **Rule One** — no line of dialogue, action, or scene is allowed unless the player's current knowledge lies between an unlock state and a reward state. Most locations have multiple unlock states and reward states, so scenes trigger in varied contexts and with varied outcomes.
- **Rule Two** — every scene (and a decent share of dialogue beats) must move something in the knowledge model forwards. Gate everything this way and, so long as the player has *anything* to do, doing it produces progress. Velocity is guaranteed.
- **Automated testing possible** — bots can bash through content to check for dead ends; coherence remains a human problem.
- **Dialogue as the inexhaustible resource** — players can only open so many cupboards. A dedicated active-everywhere conversation button pulls from the script based on the current knowledge model, letting companions talk about what's just happened. The Roomba loop becomes a detective loop: interact, walk, discuss, deduce, repeat. Discussion-as-momentum is rare in games but natural to Chandler.
- **Closing thesis** — narrative momentum is the tension between what is happening and what is about to happen. A formal knowledge model adds a second axis of progression that keeps working even when the player is standing still. You can't stop them putting the controller down; you can invite them to take one more step.
