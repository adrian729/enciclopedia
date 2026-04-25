# Ch 18: Dirty Procedural Narrative in We Happy Few

## Table of Contents

- [1. The Game](#1-the-game)
- [2. Player Storytelling as a Superpower](#2-player-storytelling-as-a-superpower)
- [3. Dirty Narrative Techniques](#3-dirty-narrative-techniques)
- [4. Dirty Narrative Is Dangerous](#4-dirty-narrative-is-dangerous)
- [5. Toward Procedurally Generated Story](#5-toward-procedurally-generated-story)

## 1. The Game

- **We Happy Few** — 1964 England after a lost WWII and a four-year German occupation. Everyone takes a happy pill called **Joy**; you, the player, do not. You flee. The world is an archipelago with procedurally arranged islands (numbers vary between the three player-characters because they remember things differently).
- **Where procgen doesn't play** — the three player-characters' major beats are hand-authored cinematics in set sequence and set locations (you meet Ollie in the train station before you can access the Victory Memorial Camp). Encounters are linear Unreal blueprints.
- **Where procgen does play** — the ambient world: letters, journals, graffiti, signs, overheard systemic dialog, NPC greetings and barks. Procedural placement means you don't know which bits a player gets or in what order.

## 2. Player Storytelling as a Superpower

- **Humans are wired to make stories** — Gambler's Fallacy, Conjunction Fallacy, survivorship bias, post hoc ergo propter hoc, No True Scotsman. We'll assemble stories from facts that don't belong together. Epstein suspects there's a Broca's-area-equivalent for stories.
- **Games rarely ask players to work** — players have come to expect any missed narrative to be laid out and explained. Procgen narrative needs to retrain them.
- **A good story still has the normal ingredients** — a character to care about, an opportunity/problem/goal, obstacles or antagonists or flaws, jeopardy (something to lose), and stakes (something to gain). Bits must be told out of order without destroying their emotional value; they can't depend on pacing, suspense, or surprise.

## 3. Dirty Narrative Techniques

"Dirty narrative" demands player interpretation; the more mental work the player does, the more emotionally engaged they become. All of the following are **pull** storytelling — get the audience to ask the question before you answer it. Pushing information pushes players away.

- **Translucent lies** — lies you can see through to the truth *and* which tell you something about the liar. Joy + perpetual smile masks: you see through the "everyone is happy" lie, and you learn the society must be hiding something terrible. (Fun dev history: the masks and drugs came first; the lost war and themes of denial were reverse-engineered from those two mechanics.)
- **Absences** — there are no children in Freedom Town. Adults jump in puddles, play Simon Says, *"if you don't, who will?"* The Garden District has graffiti of children with scratched-out faces; someone mutters *"What am I going to do with all the little shoes?"*. The hidey-hole of one child, Sebastian Dainty, and his parents' increasingly anguished letters after he didn't eat the birthday cake, make the absence concrete. A black hole is invisible, but distorted stars around it tell you it's there.
- **Mysteries** — Foggy Jack, the supposedly fictional monster whose catchphrase *"I'm afraid you've come to the end of your time"* turns up on interrogation reports and engraved cards. Who is he, is he real? Epstein won't say — the monster in shadow is scarier (10 % special effects, 90 % whatever the audience fears most).
- **Inconsistencies** — three overlapping playable characters show the same scenes differently. An Arthur-Sally scene plays at Sally's lab in Arthur's story and at an abandoned playground in Sally's. Sally's answer to *"How could you?"* is flippant in his version and wrenching in hers. Which is the truth? *"It's an odd conceit of games that you can depend on what NPCs are telling you."*
- **Tangents** — NPCs pursuing their own goals let the player infer far more. Two bobbies won't tell you where Dr. Faraday is, but you overhear them talking about Bobby Hickinbotham, assigned to look after her and so guilty about what's been done that he's "gone to the Reform Club to get his arse spanked". That line is a quest hook *and* a worldbuilding statement about a society that institutionalises guilt.
- **All five blur together** — every technique is a flavour of "something should be there but isn't" or "something's there that shouldn't be". The list is a prompt for generating interpretable bits, not a rigid taxonomy.

## 4. Dirty Narrative Is Dangerous

- **Execution-dependent** — if done brilliantly, it's brilliant; less than superb, it becomes sloppy. QA periodically files bugs about "inconsistencies" and "holes" in NPC stories.
- **Why do it anyway** — games have thousands of assets; the real world has billions. In a naturalistic game you need players to fill the spaces between your paltry handful. Clear narrative hand-feeds them and they stop interrogating. Dirty narrative forces them to interrogate, which is the only way your world might convince them it's real.

## 5. Toward Procedurally Generated Story

- **Story doesn't scale** — even a 31-ending CYOA needs 31 stories hand-written. Faction-driven play can *feel* open, but the forks are still hand-written.
- **Procedurally generated lore items** ("X slew the terrible Y") don't automatically produce emotionally engaging backstory. Only some choices are fun (Dorothy in the storm cellar doesn't visit Oz).
- **Order-sensitive story beats** — writers can craft pairs/triples of beats that mean *different but strong* things in different orders:

  ```
  Story 1:   a. Jack cheats on Jill    b. Jill takes a job in another city
  Story 2:   a. Jill takes a job in another city    b. Jack cheats on Jill
  ```

  Both orders yield coherent but different inferences about Jack and Jill.

- **Doesn't generalise to long sequences** — at ten beats, either the connective tissue is strong (one natural order only) or shuffling produces incoherence.
- **Goal isn't great NPC stories** — it's an immersive environment. Each individual story just needs to reveal something about the world (guys cheating is a problem here), and a handful of permutations suffice to give replays new inferences.
- **The gift of irreducibility** — in a game, everything is theoretically knowable. Dirty narrative + procgen means the player can never be sure they have all the facts, their order, or their meaning. No ultimate wiki answer exists. That uncertainty helps suspend disbelief that they're looking into a world instead of pushing electrons.
