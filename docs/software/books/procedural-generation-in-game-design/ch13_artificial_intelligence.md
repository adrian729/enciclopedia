# Ch 13: Artificial Intelligence

## Table of Contents

- [1. Why PCG Games Need a Different AI](#1-why-pcg-games-need-a-different-ai)
- [2. Unpredictability and AI](#2-unpredictability-and-ai)
- [3. Movement and Combat](#3-movement-and-combat)
- [4. Ambient Behavior](#4-ambient-behavior)
- [5. Emergent Phenomena](#5-emergent-phenomena)
- [6. Conversations](#6-conversations)

## 1. Why PCG Games Need a Different AI

- **Not every PCG game needs AI** — exploration games like *Proteus* and *In Ruins* use PCG for the felt experience of discovery; no actors, no AI required.
- **PCG AI must cope with the unforeseen** — handmade-game AI deals with unpredictable player behavior, but PCG AI may have to navigate spaces and gameplay configurations the designers themselves never envisioned, while still producing the intended level of challenge.
- **Chapter scope** — player and designer experience of AI, common requirements, and innovative methods for the subfield's future.

## 2. Unpredictability and AI

- **Why AI uses hidden randomness** — three reasons:
  - **Challenge** — random reactions force players to respond rapidly, raise replayability, and open the door to emergent phenomena from interacting in-game elements.
  - **Exploit resistance** — predictable AI gets gamed; an AI scripted to always dodge grenades can be force-dodged into traps; an always-pursuing AI can be lured. Unpredictability shuts these exploits down.
  - **Balance** — building a game-theory-optimal AI is far easier than building a *fun* opponent; "fun" mixes design, psychology, sociology, and interface concerns that pure optimisation ignores.
- **Designing for fun vs. designing for challenge** — currently one of the most active areas in game AI; harder to code than optimal play, so a common shortcut is to weaken an otherwise-strong AI just enough to feel right.
- **Left 4 Dead's AI Director** — cited as a rare attempt to weigh both player gameplay condition and psychological condition when picking actions.
- **Dungeon Crawl Stone Soup** — bosses pick from a curated spell list (sometimes randomly each turn); unpredictable, and balancing strong/weak options keeps deadly enemies from being game-theory-optimal every turn (which would be more punishing but less interesting).
- **Players over-attribute intent** — early-roguelike monsters used the trivial AI "wander, then pursue when sighted," but players believed the AI was scheming because monsters arriving after a brutal fight stuck in memory while the same monsters arriving at full health were forgotten. A simple AI plus selective memory reads as cunning.

## 3. Movement and Combat

- **Movement and combat dominate game AI** — true in handmade and PCG games alike, but PCG amplifies the design challenge.
- **Terrain is unknowable in advance** — AIs must traverse millions of permutations: wide and narrow alleys, bridges, rivers, traffic, plus terrain types like ice, water, lava, hazards, oceans, mountains, deserts, alien surfaces.
- **Capabilities belong to creatures, not maps** — every creature carries a description of what it can/cannot traverse (e.g., cannot traverse lava, can traverse water); this drives modular monster architectures rather than per-region scripting.
- **Edge cases must be handled** — even a one-in-a-million enclosure of buildings around an AI's spawn must be solvable, or the PCG layer breaks the AI's intended behavior.
- **Combat parallels movement** — AI must reason about weapons, ranges, retreat, flanking, and calling for help against scenarios it cannot have been pre-tuned for; designers must enumerate the *elements* of scenarios so the AI can identify them at runtime.
- **Tight PCG–AI integration is the deciding factor** — low integration produces freezing, dumb defaults, or bizarre choices on unusual maps; high integration makes procedurally placed AIs in procedural spaces feel as competent as handmade-game AIs.

## 4. Ambient Behavior

- **Ambient behavior** — AI actions that continue when the player is not nearby or engaged.
- **Cogmind exemplar** — robotic "species" largely ignore the player and pursue their own routines; the system identifies points of interest per AI when the map generates and builds a unique spatial and temporal schedule for each actor each level.
- **Payoff** — procedurally generated worlds feel "lived in" the moment they exist, achieving a trick previously available only to handmade games with hand-scheduled NPCs.

## 5. Emergent Phenomena

- **Emergent phenomena** — simple behaviors combining into unanticipated complex ones.
- **NetHack as illustration** — *NetHack* contains systems and AI behaviors players can win without ever engaging with.
- **Cursed scroll of genocide / nurses** — a non-cursed scroll wipes out a species; the cursed version *spawns* a ring of that species around the player. Used on "nurses," whose attacks heal the player and can raise max health, the curse becomes a benefit. The interaction between AI behavior and item behavior produces an outcome neither system was designed to produce, and unanticipated outcomes like this are part of what makes PCG-game AI compelling.

## 6. Conversations

- **Speech and conversation generation** — among the most interesting AI applications in PCG; central to *Ultima Ratio Regum (URR)*, where conversation rather than combat or movement carries the gameplay.
- **Two layers** — the PCG of the actual sentences spoken, and the conversation system that decides what can be discussed.

**Dialects** — every culture (roughly 40 per world: feudal nations, tribal nations, nomadic nations, possibly city-states) gets a unique generated dialect built from several elements:

| Element | What it does |
|---|---|
| **Phoneme set** | Selected consonants, vowels, and syllables build all "invented" words for the culture (e.g., *Xonatov, Vonnerto, Toravert* vs. *Kaeltram, Malatrakel, Altrakem*), making cultures audibly distinct |
| **References** | Cultural, historical, political, religious touchstones (terrain, dominant religion, recent history, ideologies, diplomatic relations, aesthetic preferences) shared across speakers of one culture |
| **Greetings, insults, farewells, threats** | Generated set per culture; shapes how distinctive an NPC sounds without altering AI behavior |
| **Sentence complexity** | How much an individual says — terse introduction vs. one padded with national achievements; loquacious NPCs leak more information than taciturn ones |

- **Contrast with handmade games** — conversant characters in even handmade games rarely differ by origin; the *Mass Effect* series is a rare exception. *Elder Scrolls* "rumor" dialogue is cited as the culture-agnostic anti-pattern. *Dwarf Fortress* is the other standout for PCG-driven speech.
- **Conversation system in URR** — players pick from dozens of topics (artworks, history, ideologies, religions, monasteries, travel, animals, books); the question list grows as the player learns. Any newly discovered movement, war, or hermit becomes a topic any NPC can be asked about.
- **PCG response to PCG question** — none of these topics existed before world generation; the system always assembles an appropriate reply, even if that reply is just a procedurally expressed lack of interest.
- **Closing thesis** — the question is "not how many verbs the AI needs, but rather what types and combinations of input it can react to, and what elements of its reaction can be generated and will yield interesting outcomes."
