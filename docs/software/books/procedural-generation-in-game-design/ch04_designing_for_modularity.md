# Ch 4: Designing for Modularity

## Table of Contents

- [1. Modules and Gestalts](#1-modules-and-gestalts)
- [2. Assembly Mechanisms and Gestalt Spaces](#2-assembly-mechanisms-and-gestalt-spaces)
- [3. Three Principles for Enabling Play](#3-three-principles-for-enabling-play)
- [4. Plotting Desirable Gestalts](#4-plotting-desirable-gestalts)
- [5. Inserting Memorable Asymmetry](#5-inserting-memorable-asymmetry)

## 1. Modules and Gestalts

- **Modules and gestalts** — modules are the discrete units; gestalts are the larger structures assembled from them. Gestalts (e.g., dynamic puzzles, dungeon levels, dialog trees) are what players actually encounter and care about.
- **The combinatorial magic** — design a few modules plus an assembly mechanism, and a plethora of gestalts comes for free. Modularity multiplies the designer's work and often produces novel results.
- **Canonical example: RPG equipment** — the modules are individual armor pieces; the assembly mechanism is the player's choice of equipment (constrained by body-part coupling); the gestalt is the entire loadout. Modularity is what gives the system its *play*.
- **Play, defined** — borrowing from Salen and Zimmerman's *Rules of Play*, "the free space of movement within a more rigid structure." In this chapter, play means the range of interesting possibilities prescribed by the system's rules.
- **Scope of this chapter** — modular designs that satisfy two qualities: (1) the assembly mechanism includes some randomness, (2) the gestalt space is too large to craft every gestalt by hand.
- **The modular designer's twofold aim** — craft modules that assemble into desirable gestalts, and design an assembly mechanism to manifest them. Gestalts are out of direct reach, which is what makes the problem hard.

## 2. Assembly Mechanisms and Gestalt Spaces

- **Gestalt space** — the set of all possible gestalts that can be assembled from a given set of modules by a given assembly mechanism. Restated aim: yield a sufficiently large gestalt space with a high proportion of desirable gestalts.
- **No generic desirability metric** — desirability is decided per system (e.g., for RPG equipment, synergistic bonuses) and graded on a spectrum from ideal to unworkable.
- **Null zone** — the region of the gestalt space holding gestalts that cross a threshold of undesirability.
- **Combinatorial growth** — populating a dungeon room with 3 monsters drawn from 5 types yields 35 distinct combinations; with 25 types and 10 monsters chosen, 131,128,140 gestalts. Even modest module counts produce large gestalt spaces.
- **Permutation vs. combination** — a gestalt that cares about order is a permutation; one that doesn't is a combination. (With repetition allowed, both have closed-form formulas; the chapter uses combination-with-repetition for the dungeon example.)
- **How module interactions propagate** — contrived example: a fire imp's attack instantly annihilates a water elemental, so any room containing both is undesirable. 5 of the 35 possible rooms contain both, so this design choice confines those 5 to the null zone. Options: live with the proportion, add a constraint preventing co-spawn, or revisit monster design. The mathematical context enables better decisions.

## 3. Three Principles for Enabling Play

Three principles for designing modules and assembly mechanisms that yield desirable gestalts. Examples come from *Sproggiwood* (Freehold Games, 2014), a roguelike with turn-based grid movement.

### 3.1. Mechanics as Shared Substrates

- **Direct module-to-module relationships are detrimental** — set pieces (two equipment items that each grant a bonus only when the other is worn) tightly couple modules. The pair produces a desirable gestalt but loses a big swath of the gestalt space to the null zone, since neither module assembles meaningfully with anything else.
- **Indirect coupling via mechanics** — instead, define modules in the language of the game's mechanics. Each mechanic acts as a *substrate* the modules act in. Example: a lance that deals bonus damage equal to your movement speed plus boots that increase movement speed by 20% — both speak movement, both compose with any other movement-substrate module.
- **Substrate choice matters** — the more central a mechanic is to gameplay, the more play results from designing modules in its language.
- **Sproggiwood applied** — turn-based movement is central; many traps and monsters constrain or coerce movement on the grid. Modules are traps and monsters; assembly mechanism is the dungeon populator; gestalts are dungeon rooms; a tactically challenging room is desirable.
- **Worked example** — a player who just killed a black jelly faces (1) a jelly puddle that respawns the jelly if not walked over within 7 turns, (2) a frog that yanks the nearest creature adjacent every few turns via its tongue, and (3) a lily pad that teleports anything stepping on it to another lily pad. The three modules combine into a tactically rich gestalt because all are written on the movement substrate.

### 3.2. Orthogonality

- **Orthogonality** — partitioning the design into modules that don't overlap and whose gestalts span the space of gameplay prescribed by the mechanics.
- **Counterfeiting** — when two modules' designs largely overlap, the gestalts containing either module replicate each other's place in the gestalt space, reducing the count of distinct desirable gestalts and muting the thematic resonance of each.
- **Counterfeit example** — a hypothetical purple jelly puddle that spawns two jellies unless walked over within nine turns would counterfeit the existing black jelly puddle (one jelly, seven turns) — virtually identical challenge.
- **Sproggiwood's six jellies** — designed for distinct identities:

| Jelly | Effect |
|---|---|
| Yellow | Puddle causes walkers to slip one tile |
| Blue | Slip puddle that also deals poison damage |
| Red | Explodes in a cross pattern one turn after dying |
| Black | Slip puddle; spawns another jelly if not walked over within 7 turns |
| Purple | Slip puddle; shoots a lightning bolt that triggers other purple puddles |
| Ice | Explodes in a cross pattern and freezes anything it hits |

- **Total orthogonality is hard** — yellow's puddle is subsumed by all the others; red and ice present similar challenges. Some overlap is inevitable when designing thematic monsters and articulating the whole gameplay space is itself difficult. Use orthogonality as a guiding pressure, not a rigid requirement.

### 3.3. Equivalence of Impact

- **Overshadowing module** — one whose impact is so powerful it distorts every gestalt it appears in, flattening dimensionality by compelling so much player action that other modules can't compete. Analogy: other massive bodies on Earth being dwarfed by Earth's gravitational pull.
- **Goal** — most modules should fall within a similar impact range. Both module impact values *and* the assembly mechanism's pairing behavior matter; an outlier module can ruin a gestalt even when the average impact is fine.
- **Sproggiwood example** — the dungeon populator can produce out-of-depth encounters (a difficult monster from a later dungeon in an earlier one). At low player health, the big baddie compels flight regardless of how interesting the rest of the room is.
- **Mitigations** — keep far out-of-depth encounters rare; or pair them with out-of-depth rewards (e.g., a powerful sword guarded by the difficult monster) — still flattens dimensionality but adds a new one that may be worth the trade.

## 4. Plotting Desirable Gestalts

- **The bridging technique** — gameplay in modular procedural systems is emergent and operates at the gestalt level, while designers operate on modules and assembly mechanisms. Envision specific desirable gestalts and work backward to the modules and rules that produce them.
- **Span the spectrum** — imagine both rare gestalts (the story a player excitedly tells friends) and common ones (a savvy strategy a player repeats for minor benefit). Once you have several, interpolate between them to derive modules and an assembly mechanism.
- **Caves of Qud faction system** — the technique was used to design interspecies conflict. The seed gestalt: a player stumbling on a fight between baboons and goats, occasionally for a ridiculous reason matching the game's tone (e.g., a named baboon leader hated by goats for some esoteric reason).
- **Resulting design** — a faction system where animal groups' behavior is modified by the procedural histories of their faction leaders. Each generated leader gets a small backstory with one to three procedurally chosen factions, determining like/dislike, which then governs animal behavior in the leader's zone.
- **Outcome beyond the seed** — animal factions find strange allies; players can share water with leaders to alter reputations with the factions that like or dislike them. Plotting desirable gestalts gave a kernel that pushed the design into unexpected territory.

## 5. Inserting Memorable Asymmetry

- **The pitfall** — neat partitioning into shared-substrate, orthogonal, equivalent-impact modules tends to form elegant *symmetric* systems, but elegance shouldn't be privileged over the player's experience. Lost in systemization, a design can lose its thematic inspirations.
- **Leave room for thematic overrides** — break the play-enabling principles in small, deliberate doses where appropriate; asymmetry can disrupt elegance in memorable, favorable ways.
- **Sproggiwood weapons case** — three classes (freezing, flaming, vampiric) implemented as nearly orthogonal effects on the movement and health substrates, intentionally decoupled from the six player classes so any class could find any weapon. From a play-enabling standpoint, it worked; gestalts like "freezing warrior" and "freezing wizard" played distinctly.
- **The complaint** — players found the weapons "samey" and lifeless. Roguelike weapons traditionally juice up gameplay; the over-systemization stripped that.
- **The fix** — the 2015 mobile release added unique weapons coupled to specific player classes (e.g., the farmer's grappling pitchfork, shot at walls to slide the player along the grid toward the wall). The team lost desirable gestalts but gained thematically resonant weapons.
- **Closing rule** — adherence to play-enabling principles should serve the game's vision; when they conflict, subvert them.
