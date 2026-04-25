# Ch 4: Adapting Content to Player Choices

## Table of Contents

- [1. Why Adapt at All](#1-why-adapt-at-all)
- [2. Choosing What to Make Adaptive](#2-choosing-what-to-make-adaptive)
- [3. Combining Bits and Creating Bits](#3-combining-bits-and-creating-bits)
- [4. Papering Over the Seams](#4-papering-over-the-seams)
- [5. Working Process and Big Picture](#5-working-process-and-big-picture)

## 1. Why Adapt at All

- **Drive tech from creative goals** — the fact that you *could* generate something doesn't mean you should. Identify the creative goal first.
- **Typical reasons for procgen** — infinite worlds (*Elite*, *No Man's Sky*), deep possibility space (*Dwarf Fortress*), replayability (*Spelunky*, roguelikes), evocative randomness (Twitter bots).
- **Horneman's reason** — adapting games and stories to player choices and dynamic state, especially in open worlds where you can't predict where or when the player will engage with a given story beat.
- **Mixed content is unavoidable** — high execution quality usually forces a blend of pre-created and generated content, and that mix is where the hard problems live.

## 2. Choosing What to Make Adaptive

- **Identify the part that ties content to context** — that is the piece to abstract out so the rest can adapt.
- **Objective-text templates** — *"Search for the witch in the %location%"* with `%location%` filled from the actual mission location. Tools like Kate Compton's **Tracery**, James Ryan's **Expressionist**, and Bruno Dias's **Improv** are more sophisticated versions of the same substitution idea. Gendered languages make this harder; speech is the hardest medium because text-to-speech is still weak.
- **Mission givers per setting** — create a weary explorer in the forest tavern and a mysterious traveler in the desert oasis; activate the one that matches the player's location. Simple, no complex tech, still counts as procedural storytelling.
- **Generalise where cheap** — any tavern owner could be a mission giver; teaching the computer what a mission giver *is* makes missions more adaptable. But generalising trades specificity — sometimes the story needs *this* ring for *this* wizard.
- **Adaptive content we've already normalised** — *Overwatch*'s Play-of-the-Game highlight intro adapts to the player's hero, skin, and intro type. A 3D renderer is itself a procedural animation/image generator; we just stopped calling it that.
- **Story daemons** — invisible entities that inject story beats independent of spatial triggers. Horneman's **Creepifier** (2016) is a dread-building daemon modelled on *Left 4 Dead*'s AI Director: a "creep clock" ticks each turn, and when it fires the daemon picks a creep block matching the current location's tags and injects it into the description (*"You hear a scurrying noise behind the walls"*). Can inject new player options, visual effects, music. Companion NPCs can be implemented as daemons that interact with other daemons.

## 3. Combining Bits and Creating Bits

- **Tag-based content selection** — the *Mainframe* ProcJam 2015 game (Horneman & Liz England) used `<injectOption tags="search, electrical"/>` to pull a scene matching those tags. Simple, powerful; compare with Valve's rule-based dialogue selection and Irrational Games' gameplay pattern-matching. In an unreleased 2011 action-RPG, rooms in a hand-designed dungeon map were declared with tags (*"spooky, corridor, jungle, exit to the east"*) and the engine matched them against a pre-authored room library.
- **Must-have vs. nice-to-have tags** — required tags guarantee the system can fall back when a perfect match doesn't exist.
- **Avoid asking for content you don't have** — automated testing catches missing combinations; tools that show where the content is thin let you fill the right buckets.
- **Implicit vs. explicit context** — implicit: the writer knows the situations a line can appear in but nothing enforces it (one of the hardest problems in game writing). Explicit: the author declares which contexts a piece fits. Explicit gives control but still requires thinking through permutations, and nuance in text is near-infinite.
- **Weighting** — as in NPC barks, the remarkable content should fire less often than the highly reusable stuff so repetition doesn't flatten the experience.

## 4. Papering Over the Seams

- **Transitions are where quality lives** — NPC remarks between missions need to reference what just happened, what's coming, branch-specific outcomes (*"You convinced the witch to give you her monster-killing potion? Excellent!"* vs. *"You didn't get the witch's potion? Well, you can still kill the monsters…"*).
- **Solution 1: remove transitions entirely** — *Dwarf Fortress* uses functional, non-flowing text (*"Endok sketches pictures of stacked leather. Endok has begun a mysterious constriction."*). Efficient but less immersive.
- **Solution 2: modularise into storylets** — *Fallen London* intentionally cuts connections between story beats and lets the player imagine the links. Valid artistic choice, but discards the causal glue that makes "the king died, and then the queen died of grief" different from "the king died. The queen died." Connections between events are the key to story.
- **Control over specificity** — keep main missions hand-authored and specific, let side missions be more generated, and always mix a few hand-authored side missions in. Never be locked into all-procedural.

## 5. Working Process and Big Picture

- **Procgen changes how teams work** — content creators lose direct control; tools replacing their familiar ones are often less sophisticated. Expect anxiety.
- **Non-linear progress** — static content (rocks) scales linearly: 30% of work = 30% of rocks in-game. Programming is the opposite: 90% of effort can show nothing on-screen. Procgen sits between — a tweak to one algorithm or a data change can transform the game overnight, or everything looks bland until the system flips into place. Needs active project-management attention.
- **Missing workflows** — graybox and level-metrics disciplines don't yet have procgen equivalents. How to test content in all contexts? How to judge *enough*? Unsolved.
- **Not one problem, a thousand solutions** — procedural storytelling is not a technical problem to be solved the way 3D rendering has been. It is an art, not a science; you cannot "solve" storytelling in games.
- **Top-down vs. bottom-up** — millennia of storytelling assume precise control over the audience's time, space, and point of view. Games break those assumptions. Top-down techniques (branching, non-linearity) break the authored experience into bits; bottom-up systems (simulations) grow stories from rules. Neither side generates what the other does, and no one has mastered combining them. Horneman's running joke: the three core tools of storytelling in games are cut-scenes, invisible boxes, and environmental storytelling — and it turned out not to be a joke. Progress lies in combining pre-created, generated, and systemic content based on dynamic context.
