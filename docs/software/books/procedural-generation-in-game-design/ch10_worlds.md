# Ch 10: Worlds

## Table of Contents

- [1. Scope of World Generation](#1-scope-of-world-generation)
- [2. Brief History](#2-brief-history)
- [3. Space vs. System Worlds](#3-space-vs-system-worlds)
- [4. Why Generate Worlds](#4-why-generate-worlds)
- [5. Qualitative Procedural Generation](#5-qualitative-procedural-generation)

## 1. Scope of World Generation

- **What counts as a world** — entire planetary terrain (continents, oceans, deserts, tundra, jungles, mountains), but optionally also climates, flora, fauna, and even larger scales like solar systems and galaxies. The author flags an open challenge: a game that procedurally generates a *universe* with its own algorithmically determined natural laws.
- **Two modeling stances** — top-down generation that places continents and mountain ranges then fills in between, vs. simulation of natural phenomena (rainfall, tectonic plates, weather) from which world structure emerges.
- **Sub-world targets** — generators can also operate at smaller scales (nations, regions, cities, towns, fortresses, districts, individual buildings, building floors). The chapter focuses on the grander end.

## 2. Brief History

- **Defining "world" is fuzzy** — drawing the line between a "world" and a "very large generated space" is hard, so the first generated world is hard to pinpoint.
- **Early markers** — *Akalabeth* (1980) generated worlds from player-supplied seeds; *Elite* (1984) was originally planned with trillions of galaxies but shipped with far fewer; *River Raid* (1982) endlessly scrolled procedural terrain; *Civilization* (1991) generated Earth-like worlds parameterised by land mass, temperature, climate, and age — the first major mainstream game offering an endless volume of planets.
- **Modern landmarks** — *Alpha Centauri* (1999), *Dwarf Fortress* (2006), *Minecraft* (2009), *Cataclysm: Dark Days Ahead* (2013), *No Man's Sky* (2016).
- **More-than-world generators shift topology** — space-scale games (*Faster Than Light*, *Stellaris*, *Aurora 4X*) abandon square or hex grids in favor of node-based networks, since space is mostly void with sparse points of interest.

## 3. Space vs. System Worlds

Two contrasting models of procedural worlds, exemplified by *Civilization* and *Dwarf Fortress*.

| Model | Worlds as **space to act upon** | Worlds as **system to act within** |
|---|---|---|
| **Exemplar** | *Civilization*, *Minecraft* | *Dwarf Fortress*, *Elite*, *UnReal World*, *Europa Universalis*, *Crusader Kings*, *Ultima Ratio Regum* |
| **Starting state** | Largely empty map; player carves it up | Pre-populated with peoples, factions, weather, mythologies |
| **Player relation** | Sandbox: player projects creative or strategic will onto a blank canvas | Slot-in: player inserts into an already-running system and probes its rules |
| **Design focus** | An interesting space to explore and build on | Interlocking nonphysical and physical systems with emergent knock-on effects |
| **Generation emphasis** | Terrain, topography | Social, political, economic, cultural systems alongside terrain |

- **Different rationales, different generators** — the two models produce very different worlds and demand very different generation techniques.

## 4. Why Generate Worlds

Three motivations distinguish procedural worlds from large handcrafted ones:

- **Exploration as game mechanic** — handcrafted worlds offer real exploration only on the first playthrough; procedural worlds keep it fresh every run. Strategy games rely on exploration to find enemies, terrain, and resources; pure-exploration games like *Proteus* make discovery itself the activity; systemic worlds use it to find trade routes and clues (e.g., *Ultima Ratio Regum*).
- **Expansive or complex worlds** — generators produce scales no developer could hand-author: thousands of planets in *No Man's Sky*, the planetary detail of *Dwarf Fortress* and *Ultima Ratio Regum*. Trade-off: not every generated element matches the gameplay value of a handcrafted one, but for sheer volume and explorability nothing rivals generation.
- **Gameplay variation** — a single fixed map quickly reveals dominant strategies; procedural worlds force experimentation. A *Civilization* run on a heavily oceanic map demands naval play even from a player who never builds navies; a *Dwarf Fortress* world missing a key resource forces alternate production routes. Generation nudges players across the full possibility space rather than into rote tactics.

## 5. Qualitative Procedural Generation

The author's own term for his work in *Ultima Ratio Regum*, contrasted with terrain/spatial generation.

> **Qualitative procedural generation** — the procedural creation of cultural practices, social norms, religious beliefs, ways of speaking and behaving, and their physical instantiations within a game world.

- **Show, don't tell, at human scale** — instead of abstracting nation relations into Civilization-style numerical values, let the player walk between two nations' cities and *see* artifacts bleed across the border, hear linguistic exchange, observe patrol density, and how each side's people speak of the other. Only feasible at the single-character scale, not at world-strategy scope.
- **Extends the system model** — qualitative generation builds on the "world as system" approach: many existing systemic generators already model trade or politics, but as numerical relationships rather than as embodied culture.
- **Intersection drives meaning** — a religious belief about the afterlife shapes book-cover colors; a powerful house influences weapon and armor design across a nation; flora and fauna inform family sigils; an ancient war shapes how strangers respond to a player from the resented foe; a city's geography shapes the religions that spring up there. Cross-system links make the world feel layered and discoverable.
- **Combats homogeneity** — most procedural worlds, regardless of size, are populated by AI actors speaking the same language and building similar buildings; qualitative detail counteracts this sameness.
- **Enables new gameplay** — a complex cultural system supports cultural-knowledge-as-skill, espionage gameplay (faking one's origin), informed travel decisions across allied and feuding lands, and dialogue choices grounded in acquired knowledge of each people's dispositions rather than direct exposition.
- **Future direction** — qualitative procedural generation is positioned as a major next step for procedural worlds, both for richness and for novel gameplay forms.
