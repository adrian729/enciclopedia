# Ch 22: Procedural Characters in State of Decay 2

## Table of Contents

- [1. Why Generate Characters at All](#1-why-generate-characters-at-all)
- [2. Two Failure Modes — Blandness and Contradictions](#2-two-failure-modes--blandness-and-contradictions)
- [3. Contradiction Winnowing with Tags](#3-contradiction-winnowing-with-tags)
- [4. Identity, Culture, and Naming](#4-identity-culture-and-naming)
- [5. Order-of-Operations Regrets](#5-order-of-operations-regrets)

## 1. Why Generate Characters at All

- **State of Decay's permadeath** — core feature. Yet players of the original often restarted to recover lost bespoke starters, so permadeath meant less than intended.
- **The sequel doubled down** — making deaths meaningful required a near-infinite supply of characters players could actually care about.
- **The original's "random" characters were an illusion** — only names were random; life history, skills, quirks, and appearance were hand-authored per character, a few hundred in total.
- **Requirements** — unique, authentic, relatable, random-feeling without being random. Otherwise deaths are empty.

## 2. Two Failure Modes — Blandness and Contradictions

- **Blandness** — every character reads as "Generic Human Number Five" and no individual's death matters. Easy to fix by dialling up distinctive features — but then contradictions multiply.
- **Contradictions** — traits that seem like they couldn't belong to the same person. In hand-authored fiction, contradictions can be made to work; in procgen, players read them as "the random generator made something dumb". The bar for believability is higher for procedural content.
- **Strategy — some characters must shine** — the team couldn't make every character a movie star; they aimed for a handful per player, with supporting backstory easy to surface.

## 3. Contradiction Winnowing with Tags

Gameplay stats (health, stamina, skills) derive from a central set of **traits**. Traits are always written in **first person** and mostly offer a story or opinion rather than a plain description — giving characters a voice and something to talk about.

- **Breadcrumbs back to the story** — nicknames derived from traits (a character who slept in trees to avoid zombies might be *"Squirrel"*); skill specialisations and hero bonuses catch the eye and lead the player to the trait that explains them.
- **Tags on traits** — each trait has arbitrary tags with rules for co-occurrence. The **career** tag can only appear once per character, so applying `firefighter` eliminates every other career trait.
- **Mutually exclusive tag pairs** — `active` vs. `inactive` (after a tester spotted a marathon-running couch potato). Any trait sounding physically energetic gets `active`; sedentary traits get `inactive`; the two tags cull each other.
- **Repurposing the system** — a request to cap starting characters to low-level skills was solved with an invisible `beginner` trait applied at spawn and an `advanced` tag on advanced-skill traits, set mutually exclusive.
- **Hierarchical trait tree** — traits are organised in nested groups so a tag can be dropped on a subgroup instead of per-trait. Adding the `advanced` tag became drag-and-drop on subgroups rather than editing thousands of traits.
- **No need to anticipate everything** — throughout development, testers reported new contradictory pairs; each fix was a couple of new tags plus an exclusion rule.

## 4. Identity, Culture, and Naming

Name + appearance + gender + voice had to line up believably. Pooling all identity features into one random draw produced "awareness-free" mishmashes; the standard for representation was stricter than for reality.

- **Weighted combinations** — most characters matched a common set (a male voice with Spanish words, a Latino appearance, Spanish first/last name, Mexican nickname); rare exceptions were allowed so characters could step across.
- **Go highly specific** — treating cultures as monoliths alienates familiar players. India is internally as diverse as Europe; the team started with *one region* of India and researched the most common names there, vetting with advisors from that region.
- **Cross-culture nickname mistake** — Microsoft localisation's Spain translator red-penned their Spanish nicknames as "not real"; Mexico translator confirmed them as authentic. The list was Mexican, not generic Spanish. Fix: copy nicknames to a Mexico-specific list, remove from the general pool.
- **Seu lin (Lao)** — informal nicknames unrelated to the given name, used almost exclusively in place of a first name. Fit an independent nickname slot already in the data structure. One team member's own seu lin (*Poo*) couldn't ship because it would register as parody in English even with best intentions.
- **Ethiopian names + Old Testament** — the Ethiopian advisor rejected the first English/Ethiopian mix until the team added the Old Testament name list (*Abraham, Isaac, Ishmael*). Characters began to feel like his friends and family. The flexible weighted-list design let this get added in minutes rather than hours of rewriting.
- **English given names on many cultural backgrounds** — reflects how families converge on the same first-name list after a generation or two in the US while last names stay distinctive.
- **Why procgen helped diversity** — a single developer can't keep track of every bias. Setting goals and automating from them removed a kind of human error — though new mistakes in content still propagate naively through the system.

## 5. Order-of-Operations Regrets

- **The bug** — voice was being selected before age; teenagers spoke in cracked, gravelly voices. Voice moved to near-last to depend on age, gender, and culture.
- **14 voices, every role** — the sequel eliminated the ubiquitous radio character (*Lily Ritter* in the original, whom players wanted dead) so every character could play every role. That doubled voice count and broke the budget for late-development mission VO.
- **Constrained last choice = disaster** — when a mission demands lines recorded only for voices A, D, R, Q, and the generator has already committed to young + female + culture X with no eligible voice left, it falls back to a random voice and the line is missing. Earlier choices being hard to trace made debugging painful.
- **Two things the team would do differently** (hindsight):
  - **Unify all features under a single tag/exclusion system** (like traits) so age, gender, voice, appearance all winnow each other. Age-specific traits like *arthritis* or *college freshman* wouldn't need their own parallel subcategories.
  - **Add backtracking** — when the generator exhausts options for one feature, undo a previous choice and try again instead of falling back randomly. Guarantees a match if one exists; leaves only fundamentally broken constraint sets as bugs, which are easy to diagnose.
- **Core lesson** — early choices must be free to constrain later choices. People are weird, complex, and each starts from a different place in fashioning their identity; procgen characters feel human when they go through a similar process and use their own voices.
