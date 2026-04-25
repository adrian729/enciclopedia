# Ch 18: Story and Plot Generation

## Table of Contents

- [1. Scope and Approach](#1-scope-and-approach)
- [2. Grammars and Story Grammars](#2-grammars-and-story-grammars)
- [3. Game World Model](#3-game-world-model)
- [4. Story Model](#4-story-model)
- [5. Rule Design](#5-rule-design)
- [6. Game World Simulation](#6-game-world-simulation)
- [7. Metric-Guided Generation](#7-metric-guided-generation)

## 1. Scope and Approach

- **Stories in games take many forms** — narrated, environmental, cut scenes, dialogue, quests, mechanics, AI, simulation. *Façade* and *Left 4 Dead* track drama and tension; *Dwarf Fortress* and **Crusader Kings 2** rely on simulation to surface emerging causal sequences that feel like a grand narrative.
- **Chapter focus** — sequential, episodic stories (like RPG quests or TV episodes) generated from character relationships and attributes via a **story grammar**, where each story can also feed back and modify the world.
- **Why grammars** — relatively simple to author, understand, and implement. Tradeoff: outputs are highly structured and risk feeling repetitive.

## 2. Grammars and Story Grammars

- **Grammar** — a vocabulary of symbols plus rules that construct "valid" outputs. Sentence grammars validate sentences; here, they construct valid stories.
- **Rewrite rules** — formal `A → B` rules where the left-hand pattern, if present, can be replaced by the right-hand symbols. With rules `A → C`, `A → B`, `B → CC`, generation eventually terminates; adding `C → A` makes it expand infinitely.
- **Story symbols** — nothing forces symbols to be letters; they can be story events. A toy quest grammar uses `[Journey]`, `[Encounter]`, `[Discovery]` and rules like `[Journey] → [Journey][Encounter]` to build sidequest skeletons.
- **Layering for concreteness** — secondary rules expand abstract symbols into concrete events (`[Encounter] → [Fight a goblin]`, `[Discovery] → [Find gold]`). Generation proceeds by repeatedly applying valid random rules until none apply or a cap is reached.
- **Limitation of pure grammars** — a self-contained grammar has no meaningful link to the game world. Since stories are about character conflict, the grammar must operate on *both* a story representation *and* a representation of the social world, with rules that match and mutate both.

## 3. Game World Model

- **Social network representation** — characters as nodes in a directed graph, edges as one-directional relationships. Each character has a unique ID and a set of attribute key–value pairs (e.g., name, age); each edge has its own keys (e.g., trust, friendship).
- **Directed edges matter** — what A feels toward B need not equal what B feels toward A.
- **Dynamic world** — attributes and relations must change over time, since story interest comes from change. Static worlds are the common complaint about branching narratives.
- **Worked example** — a Western-flavored social world with three NPCs (Ennio, Miller, Clint) and the player. Attributes: name, bullets, money, gambling skills. Relations: money owed, trust, affection.

## 4. Story Model

- **Story as a directed graph** — nodes are story content fragments; edges are branches the player can choose. The actual experienced story is a path from a start node to a terminal node.
- **Graph grammar, not string grammar** — because rules rewrite graph nodes with new graph pieces rather than rewriting symbols in a string.

## 5. Rule Design

- **Two rule categories** — Initial Rewrite Rules (IRRs) build the basic story skeleton; Secondary Rewrite Rules (SRRs) expand and complicate that skeleton. One IRR is applied first, then several SRRs. A complete story exists at every step.
- **IRRs match world patterns** — design question: "What interesting stories arise from possible patterns in our social graph?" Example pattern: character X has money < 5 and owes more than 5 to Y → seed a story where X plays poker against the player and takes the winnings to Y. This pattern matches Clint and Ennio.
- **Keep IRR patterns small** — searching arbitrary subgraph patterns is NP-hard, so two-character patterns are far cheaper. Simple patterns also occur more often in the world; large complex patterns rarely match anything.
- **Secondary rewrite rules expand events** — SRRs match story events plus world patterns and rewrite individual events into richer ones. Example: a poker event plus a third character Y with high enough trust in X → Y helps X cheat at poker and rob the player. Further SRRs let the player notice cheating (via affection or gambling skill) and confront cheaters at gunpoint, branching into duels or surrenders.
- **Reusability is the point** — the same gunfight SRRs that escalate a card game also work for desert wagon robberies or sharpshooting contests. There should always be many more SRRs than IRRs.
- **Application strategy** — collect all valid SRRs, pick one at random, apply, repeat for a fixed number of iterations. Continuous application until exhaustion is risky: poorly designed SRRs can apply infinitely. Always cap rule applications.

## 6. Game World Simulation

- **Stories must affect the world** — without postconditions, generated stories are inert. Extend the story model with **preconditions** (world facts required for an event) and **postconditions** (changes the event makes to the world).
- **Branch on outcomes** — the IRR `X takes winnings to Y` only fires if X actually won; otherwise branch to "X leaves defeated." Cheating reduces trust toward the cheater. These hooks let similar story templates feel different because the world keeps changing underneath them.
- **Validation pass** — sweep generated stories to assert each event's preconditions hold given the cumulative postconditions of earlier events.

## 7. Metric-Guided Generation

- **Selective SRR application** — instead of picking randomly among valid SRRs, score them by features the designer wants. Prioritize SRRs that add player-choice branches, that add gunfighting events for a Western mood, or that avoid character death (it is "morbidly easy to end in Shakespeare-like scenarios where all characters have murdered each other").
- **Causality across stories** — track postconditions of each story the player experienced; prioritize SRRs whose preconditions are satisfied by the player's prior actions. If the player burned through their bullets in a duel last episode, prioritize a holdup story where they cannot defend themselves. The story templates may be similar but the context is dynamic and player-sensitive.
- **Closing observation** — story generation lets authors design the rules and structures that shape player stories rather than scripting one fixed story, aligning with criticism that players have minimal effect on game narratives.
