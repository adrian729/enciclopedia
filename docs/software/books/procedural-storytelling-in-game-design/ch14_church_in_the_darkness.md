# Ch 14: Heavily Authored Dynamic Storytelling in Church in the Darkness

## Table of Contents

- [1. The Game and Its Premise](#1-the-game-and-its-premise)
- [2. Motivations and Inspirations](#2-motivations-and-inspirations)
- [3. Core Narrative Systems](#3-core-narrative-systems)
- [4. Player Choices and Endings](#4-player-choices-and-endings)
- [5. Why Build It This Way](#5-why-build-it-this-way)

## 1. The Game and Its Premise

- **Church in the Darkness** — top-down action infiltration set inside a 1970s religious cult whose story changes every playthrough. The cult is the **Collective Justice Mission**, as strongly socialist as it is Christian, led by **Isaac and Rebecca Walker**, relocated to **Freedom Town** in jungle-covered Battuela.
- **The player** — Vic, an ex-cop sent by his sister Stella to find her son Alex, a cult member.
- **Central mystery** — is this cult merely radical or genuinely apocalyptic? The nature of the cult is randomised each playthrough, making the player a detective in a mystery where they don't even know if a murder will happen.

## 2. Motivations and Inspirations

- **Cults are hard to see from outside** — and from inside, they're not cults at all. No one joins a cult on purpose; members are often strong-willed idealists. Many groups with cult-like properties do no harm.
- **Mystery + procgen** — mystery solves once, so for replayable mystery the answer must change. Rouse wanted a specific story, not a general procgen engine.
- **Real-world research** — 1970s outsider movements, cult tactics: remote jungle compounds (conveniently confined play space), fearful members (lets most NPCs be simple fear/flee responders), loudspeaker propaganda (perfectly suited to an action game, especially when PA announcements inaccurately report the player's recent actions — a real-world disinformation tactic). Most cult propaganda contains genuinely noble content (helping addicts, fighting poverty); the "something slightly off" creates the design's ambiguity.
- **Game inspirations**:
  - **Clue** — replayable murder mystery, but doesn't feel like a story.
  - **Murder on the Zinderneuf (1983)** — a Madlibs system of pre-written scripts with character slots, eight detectives, "Red Herring" characters (which Paul Reiche III noted had to be *obviously* herring-like or players got confused). Key lesson: procedural mysteries need to be made fair enough that players have a chance.
  - **Blade Runner (1997)** — simulation that could kill any character at any time and randomised who was a replicant, yielding 40+ endings. Executive producer Louis Castle: "it was actually almost impossible to get the same game experience even if you loaded an old save game." Most players never noticed the procgen, which is a triumph and a problem — players play differently when they *know* a game responds to them. *The Walking Dead* telegraphs choice mattering, so players adjust their play accordingly.

## 3. Core Narrative Systems

- **Discrete starting states, not fine-grained simulation** — the cult leaders' personalities randomise across a handful of discrete starting states. The team deliberately avoided a rich-trait simulation that produced subtle results no one would notice. "Simulation rich, understanding poor" is a real risk.
- **Bespoke dialog per state** — with few enough states, custom lines can be written for each. Additional noise randomises specific story beats for flavour.
- **Replay shortcuts** — on replays, players choose whether to resume the previous story state, pick one they haven't finished, or go fully random. Players often want to build on prior knowledge.
- **Randomised spatial and gameplay layout** — player spawns at a random perimeter point; core character locations move each playthrough; resource locations and guard layouts randomise. A fully regenerated map was cut early for scope.
- **Three delivery channels**:
  - **PA system** — random banks + a non-random "spine" of dialog that advances in stages and is the only place the leaders converse with each other.
  - **Documents in desks** — maps are always found in an order of increasing detail regardless of which desk a player searches. Narrative documents sort into sets: (a) Alex's story, found in a set order but varying by scenario; (b) other characters' stories, each with internal order but inter-set order randomised, and not all sets appear per game; (c) randomly sprinkled flavour notes. The desk-population system became one of the game's most complex.
  - **Side characters** — heavily authored RPG-style NPCs who share points of view, move locations, and adjust dialog based on the leaders' current disposition and the player's actions.

## 4. Player Choices and Endings

- **Exploration is a choice** — how many NPCs to find, whether to approach Isaac and Rebecca directly, how thoroughly to hunt documents, and how many replays to attempt.
- **Infiltration style matters narratively** — lethal vs. non-lethal, undetected vs. frequently spotted. Lethal play draws more aggressive guards, quicker execution on capture, and some characters refuse to help murderers. Detection consequences reset after escape so players don't sink into a feedback loop.
- **Alex encounter** — the only required objective is to find Alex and start a conversation. His dialog depends on scenario + your play so far. From there: leave him, persuade him to follow, or force him out.
- **Optional leader confrontation** — finding the preachers is encouraged, not required. An algorithm places them far from Alex and the player only after specific narrative progress. Players who investigate more gather better evidence to decide whether to assassinate the leaders or leave.
- **Chapter Titles system** — on-screen Roman-numeral chapter headings (*"I. Down in the Jungle"*, *"II. They Know You"*, *"III. Exodus"*) anchor the arc across a gameplay-heavy game. The end sequence displays the player's chapter list to reinforce that their choices told a specific story.
- **Three-chunk endings** — (1) what happened to Alex, (2) how Freedom Town reacted to the player's actions, (3) a longer-term epilogue. The permutation count was complex enough to be coded rather than authored in level logic; Rouse admits he doesn't know exact counts and usually says "more than 20".

## 5. Why Build It This Way

- **Self-conscious about "small" procgen** — the tech complexity is dwarfed by more ambitious generative systems. Scope was one reason; another is intent.
- **Narrative chosen to fit the story, not vice versa** — the goal was to let players explore *the same cult from different angles* by making the cult itself change, so different playthrough choices come from different genuine contexts, not "trying to see all the content".
- **Closing thesis** — procedural narrative should exist because it's the best way to tell the story you want to tell, not to build an impressive tech demo.
