# Ch 13: Emergent Narrative in Dwarf Fortress

## Table of Contents

- [1. Emergent Narrative Defined](#1-emergent-narrative-defined)
- [2. Designing Toward It](#2-designing-toward-it)
- [3. Story Flow and Dead Ends](#3-story-flow-and-dead-ends)
- [4. The Player's Role and Exposition](#4-the-players-role-and-exposition)
- [5. Letting Players Finish the Story](#5-letting-players-finish-the-story)

## 1. Emergent Narrative Defined

- **Dwarf Fortress has no authored story** — no hand-written characters or locations, yet players produce an impressive body of cross-media fiction.
- **Emergent narrative** — stories imagined and retold by players recounting their experiences, often embellished, coherent beyond a literal log, but not yet fan fiction.
- **Complexity and procgen alone don't cause it** — complexity can hide what's happening; procgen can produce unintelligible mess. Designing *for* emergent narrative is a deliberate practice.

## 2. Designing Toward It

- **Start from the example story** — produce a plausible player-told snippet and ask "what's the least I can do to generate more of these?"
- **Example snippet**: *"A kobold crept into the workshop and stole Urist's masterpiece scepter. Urist was distraught for days afterward."* Each word loads implications: how are kobolds defined, is there stealth, are items owned, where do names come from, are there skills, are emotions simulated, how compressed is time.
- **Picking which implications matter** — *masterpiece* and *days* are afterthoughts. A prototype worth making right away: a named dwarf crafting an item in a workshop, with mining into a cliff face. Everything else (kobolds, emotional distress, tantrums) comes later. This is exactly how Dwarf Fortress was started.
- **Avoid over-designing simulation** — the exact nature of the scepter rarely matters to a plot beat. Detailed simulation is not automatically narrative; it can swamp players with insignificant facts.
- **But narrative potential needs simulation potential** — an emergent story traverses rapid plot beats; without enough mechanical connections, threads fizzle. Identify mechanics and objects that sit at a nexus of story flow and centre them. A tangle of features thrown into a jar won't shake into a story.

## 3. Story Flow and Dead Ends

- **Research and scholarship — dead end** — the library system doesn't connect to enough time-tested narrative elements. Players can design libraries, assign researchers, copy manuscripts, but research breakthroughs never feed back into labour or industry, so "what happens in the library stays in the library".
- **Engraving — central narrative mechanism** — engravers carve historical events, other dwarves, favourite foods, and feared animals onto walls and items the player chose. Many of the most striking community stories centre on what the last survivor of a fallen fortress chose to engrave: a defiant picture of the demon lord being slain, the fortress's hopeful founding, or the dwarf themselves surrounded by their favourite cheese descending into grief. Connections run physically (through the dwarf + wall + item) and conceptually (historical events, personality traits).
- **Relative dead ends can be salvaged** — book titles are generated from a simple list-and-substitution and bring flavour to the research system without deeper hooks. A "good enough" stopping point is fine provided it doesn't block future extension. But polish is a trade-off: the more you polish, the harder it is to extend later.
- **Use what the player brings** — Dwarf Fortress leans on widely understood fantasy tropes. Which elements of your game will resonate with people who will never play it? Mechanical or aesthetic focus on those elements gives players' retellings a chance to travel.
- **Names and nicknames** — names almost always surface in retold stories; nicknames usually don't. Example analysis underestimates active player abilities. Converting a passive story element into an active player ability strengthens narrative building.

## 4. The Player's Role and Exposition

- **Dwarf Fortress's player role** — "the official will of the fortress". Dwarves retain autonomy; the player induces mining designations (which create spaces), assigns functions and names (which plug them into stories), and chooses most crafted items. Spaces and objects the player created carry more meaning because the player understands their own intentions.
- **Alternative roles** — a single dwarven leader, a personified spirit, a god — each has trade-offs. Bay 12 chose abstract awareness so players can learn about anything happening and dwarves keep control of their own actions, especially free time. Events should surprise the player and the dwarves should feel coherent.
- **Selective exposition** — alerts, announcements, decision windows, subtle indicators let players know a story thread is available. Action (linking two plot beats), observation (a plot beat), and investigation (querying the world) are all valid modes. Ignoring a cue is also a valid mode, and sometimes necessary — it saves the flow of the story being built in the player's mind.
- **Surface the meaningful stuff** — combat deaths go into the main announcement queue (too important to risk missing) *and* into optional verbose combat reports for players who want specifics. Spatial properties surface naturally via display; social and conceptual properties (Why is X talking with Y? What does X believe?) need explicit query support.
- **Legends mode** — Dwarf Fortress prepares threads from hundreds of thousands of generated events and figures. Where the devs failed, modders built tools. Some players play only this way — generating histories and finding stories in the dataset.

## 5. Letting Players Finish the Story

- **Players need the ability to focus and query** — they don't need the ability to act. A simulation could present finished narratives on its own, but that's clumsy. Between the extreme of a fully autonomous narrator and the extreme of players doing whatever they want (which makes systems feel dependent on the storyteller), choose actions and queries that fit the player's role.
- **Multiple roles in one game** — Fortress, Adventurer, and Legends modes let players revisit a situation from different perspectives. When a player's adventurer explores their own old fortress, every room carries their own stories.
- **Players will invent mechanics that don't exist** — that's fine. Emergent narrative leans on players' ability to spin stories from imperfect information. Modding lets them bring their own assets and assumptions; the more ownership they have, the more story connections multiply.
- **Closing thesis** — as long as people are using your game creatively or otherwise edifying or enjoying themselves, the design is working as intended.
