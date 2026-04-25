# Ch 28: Creating Tools for Procedural Storytelling

## Table of Contents

- [1. Scope and What Tools Do](#1-scope-and-what-tools-do)
- [2. Authoring Phases](#2-authoring-phases)
- [3. Importing Content](#3-importing-content)
- [4. Planning a New Tool](#4-planning-a-new-tool)
- [5. As You're Building](#5-as-youre-building)
- [6. Testing and Iteration](#6-testing-and-iteration)

## 1. Scope and What Tools Do

Procedural storytelling tools support systems where authored data + metadata flow through a runtime that decides *how* and *in what order* to show content. Covers text adventures, dungeon generators with narrative rooms, storylet games like *Fallen London*, and heavy text-generation systems with large corpora.

## 2. Authoring Phases

- **The first five minutes** — a new system needs primer content before anything is playable. For studios this matters less; for platforms or non-professional users it's critical. *Inform*'s default library compiles to a playable first room instantly. *Spirit AI's Character Engine* ships default projects with rudimentary dialogue. *Twine* and *Texture* are playable the moment the first link exists.
- **Developing structure** — Short builds a linear skeleton first, then adds branches and variants. In *Twine*, that means scene-start/scene-end nodes with content added later. Quality-based narrative tools (StoryNexus) make this harder because no explicit model of narrative content exists.
- **Matching fiction to mechanics** — when predefined mechanical slots need flavourful text (Earth/Air/Water/Fire versions of clothing, Kindness/Cunning/Humor relationship advances), writers burn out. Tools can track outstanding slots and assign them in *random* order so writers don't drown in one category. Better: tools can propose prompts. For *Fallen London*, Short wrote a generative grammar that invented storylet premises tied to player stats: *"You keep a watchful vigil on your mark's home to gain an introduction to your mark's relatives, at the risk of going mad."* Three prompts at a time; usually at least one gives a seed. Research also suggests writers produce more inventive text when prompted with images rather than words.
- **Accretive/sculptural writing** — play the partial game until a better response suggests itself, then add it in place. Puts the author in the player's mindset. Tools that support this:
  - Tight play/replay cycles with preserved random seeds (*Inform*).
  - Ability to duplicate the current running state and attach new content to it. *Alabaster* (multi-author) included an in-game feature: if *ASK (THE NPC) ABOUT LILITH* had no answer, the game switched to authoring mode and prompted the player/author to fill in a response.
- **Adding variety** — elaborating *"I love chocolate cake"* → *"I [love/hate/feel ambivalent about] [chocolate cake/mushroom omelets]"*. Two traps:
  1. **Over-elaborating rarely-seen content** — a variant seen in 5 % of playthroughs doesn't deserve hundreds of options. Tools can highlight high-traffic content via static analysis or automated-play statistics.
  2. **Variants reducing average quality** — *"apple spice cake with goat cheese frosting"* is delicious; adding more generic options dilutes the average toward *"vanilla cake with buttercream frosting"*. Real-time sample generation lets the author see whether new variants are helping.

## 3. Importing Content

- **Crowd-sourced models** — Scheherazade (Georgia Tech) asks Mechanical Turk workers for short stories about familiar scenarios (trip to the movies, bank robbery) to build action models. Jeff Orkin's *Restaurant Game* paired strangers online, one as waiter and one as customer, and mined the results including outlier behaviour (a customer trying to steal the microwave). Gabriella Barros and others use Wikipedia-like sources to fill characters and situations in templates.
- **Import-and-curate workflow** — for a past project Short needed NPC fallback remarks. Imported a few hundred proverbs, culled culture-specific or offensive ones, tagged by theme (*wealth*, *love*) and valence (positive/negative), then deployed as situation appropriate. Supporting import often just requires large paste fields; more sophisticated tooling can pull from DBpedia, auto-clean, and suggest tags using keywords, regex, or ML classifiers.
- **Refactoring** — corpus wrong size, metadata tags doing overlapping work, variables pulling weight in only a handful of places. Search/replace and move operations become essential.

## 4. Planning a New Tool

- **Pick an aesthetic**:
  - What experiences do you want to facilitate?
  - What would count as good quality?
  - Is output allowed to look generated, or must it read as human-created?
  - Are humorous incongruities desirable or to be avoided?
- **Know the users** — yourself vs others; paid vs volunteers; novice vs expert at both building and playing this kind of project. Publishing-platform tools only work if authors are motivated enough to learn them. In-house tools can afford to be clunky — Christine Love's *Ladykiller in a Bind* timed-dialogue tool is unsuitable for anyone but her, and exactly right for her.
- **Mirror the user's creative terminology** — interactive narrative is cognitively heavy; holding the whole branching structure in your head is hard. Meet authors in their own paradigm.

## 5. As You're Building

- **Don't design only for small datasets** — what works in a prototype rarely scales.
- **Anticipate the Founder Principle** — the first significant works shape what people build with the tool for years. *Adventure* locked text adventures into underground dungeons and light puzzles. Visual novels adopt anime style because anime visual novels came first. Tools meant for many genres should ship many example projects in very different styles — the *Inform 7* manual shipped hundreds of playable code examples on purpose.
- **Don't build GUI tools too soon** — GUIs lock you into anticipated data structures. Start with extensible XML/JSON or a DSL. If you must have a GUI, support free-text custom tags so authors can add hooks unsupported by the GUI.
- **Accommodate hacks** — there will always be some one-off behaviour you didn't plan for (Easter eggs, one-scene-only effects). Allow arbitrary tags or hooks outside the normal structure.
- **Beware complexity cost** — adding a whole new subsystem costs authoring friction. If a handful of hacks covers it, live with them; more moving parts = more author overhead = less total content.
- **Collect feedback in writers' workshops** — Short's team at Spirit runs writing-workshop-style sessions focused on aesthetics and blockers rather than testing. Authors often don't raise tool issues; they assume they're "being stupid" and there must be a solution they're missing. The workshops draw those issues out.

## 6. Testing and Iteration

- **No tool is ready until a sizeable project has been built in it** — ideally two or three.
- **Port related work** — port existing projects from another system. Short ported *Galatea* from Inform 6 to Versu and to Character Engine; pieces from Inform 6 to Inform 7. The interactive fiction community used *Cloak of Darkness* as a standard port target to expose strengths and weaknesses across systems. Porting produces a sizeable corpus quickly and highlights both gaps and unexpected wins.
- **Budget ongoing iteration** — tools are never done. Many studios assume once the initial spec ships, no more work is needed and then find themselves years later with a tool that must be scrapped and rebuilt. *Inform 7* has been under development for two decades and users still propose improvements.
- **Use the tool to reinforce good design** — as you build several projects, you learn which idioms work; bake those into the tool.
- **Let the tool be clever** — AI is rare inside the tool itself. Computational-creativity and mixed-initiative research both explore how computers can add to a human-authored design. Mike Cook's **Danesh** analyses the expressive range of procedural generators so authors can tune their variety.
- **Expect forgetful users on distributed teams** — flow state with the whole project in your head is rare and brittle; design for revisits.
- **Help users test their work** — full QA can never cover every branch. Automated tools can answer:
  - Are there dead ends where the engine runs out of viable content?
  - Is any content unreachable or very rarely reached?
  - How long is an average playthrough relative to total content size?
- **Let users define their own tests and metrics** — *Inform* supports user-defined test command sequences. Visualise structure and outcomes carefully; pure branching visualisations hide the forest in thousands of trees for the games this book describes.
