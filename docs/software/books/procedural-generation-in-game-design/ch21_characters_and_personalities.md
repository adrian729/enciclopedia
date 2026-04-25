# Ch 21: Characters and Personalities

## Table of Contents

- [1. Three Kinds of Procedural Character](#1-three-kinds-of-procedural-character)
- [2. Source Projects](#2-source-projects)
- [3. Realization](#3-realization)
- [4. Creation: Designing Trait Vocabularies](#4-creation-designing-trait-vocabularies)
- [5. Recurring Strategies](#5-recurring-strategies)
- [6. Pitfalls](#6-pitfalls)

## 1. Three Kinds of Procedural Character

- **Description** — systems that procedurally create written profiles or descriptions of characters but do not make them interactively meaningful (background flavor in sandboxes, generative art). Often handled with techniques covered elsewhere in the book, e.g., a context-free grammar over a corpus of character traits.
- **Realization** — systems that procedurally choose NPC dialogue and actions in response to the player and world model. The character's *essential traits* are predefined by the writer or chosen during character creation; the system finds the best way to perform those traits at runtime.
- **Creation** — systems that procedurally assemble whole NPC profiles (personality, appearance, loyalties) so the player meets a perennially changing cast. Verges on story generation: simulation-heavy systems like *The Sims* produce emergent stories when conflicting personalities share a household.
- **Chapter scope** — primarily realization and creation.

## 2. Source Projects

- **When in Rome 2** — player must identify and subdue a randomly chosen alien; behavior rules correlate with traits, so observation reveals the alien.
- **Versu** — platform by Richard Evans and Emily Short modeling characters as agents with independent desires; each agent picks the action it most wants from a list given the social situation.
- **Blood & Laurels** — final Versu game, set in a fictional ancient Rome. Story used a preauthored branching structure but each scene was highly procedural — characters could share information, flirt, fight, betray, and poison one another. "A sandbox embedded in a preauthored structure."
- **The Mary Jane of Tomorrow** — train a robot to exhibit traits (enthusiasm, courtesy, particular subject knowledge) and suppress others (ennui). Heavy reliance on text generation to render evolving speech.

## 3. Realization

- **Two-step model** — choose what to say, then how to say it. For non-speaking or non-social characters, this becomes choose what to do and how to do it (in *When in Rome 2* a meat-eating low-gravity alien might steal a salami but have difficulty eating it because of its low strength).
- **Topic-tagged dialogue (Versu)** — characters had unique dialogue tagged with topics; conversation rules transitioned between lines on shared topics. Putting frat-bro Patrick and a 19th-century admiral at the same card table let one's "many dates" story flow into the other's tale of STDs aboard ship — both tagged "sexual behavior" — and players read intentional subtext into a juxtaposition the writers never planned.
- **Layering dialogue features (The Mary Jane of Tomorrow)** — only a dozen or so questions can be asked, but answers are rendered through a grammar reflecting current settings. A favor request expands `[gesture] [consent]`; consent expands `[consent phrase] [final punctuation]`, where `.` marks bored and `!` marks enthusiastic. A flirtatious, enthusiastic, medieval-trained robot answers `The robot crosses her legs. "If thou wishest it, yea!"`; a bored one shrugs and says `"Verily."`
- **Reusable token types** — gesture/tone indicators, social moves (greetings, farewells, compliments, insults), exclamations, names substituted by relationship ("Eunice" / "Dr. Yeung" / "Mom" / "that genius"), and hesitations/framings ("I think…", "I hate to contradict you, but…") that signal personality.
- **Post-construction filters** — Versu's "drunk character" filter rewrote `s` to `sh` for slurred speech; stutters, repetitions, fragmentation, and self-interruption can communicate nervousness, lying, or distress. Filters can autogenerate profanity (the drunk filter mangled "sit"); be ethical and check that altered output is not more offensive than the work warrants.
- **Expressive world hooks** — Versu treated the world model "more like a stage than a fully detailed simulation." Objects existed for expressive use: a vase exists to be smashed in anger; a fireplace affords thoughtful staring, letter-burning, or vicious poking; banquet food can be eaten, criticized, or thrown. Shared props anchor characters in space and signal that interaction is not purely scripted.

## 4. Creation: Designing Trait Vocabularies

- **Why it is game design** — when characters must support different play depending on their strengths, the trait vocabulary becomes the gameplay system. Trait sets need to be:

> **Orthogonal** — traits apply to different aspects of life and combine freely. Height and strength are orthogonal; flirtatious–standoffish and outgoing–shy are not, since "flirtatious and shy" is hard to realize. Better axes: romantic–aromantic paired with outgoing–shy yields four plausible combinations (outgoing romantic flirts; shy romantic daydreams; outgoing aromantic befriends everyone; shy aromantic withdraws).

> **Mechanically Significant** — fictional trait labels abstract away under repetition unless backed by mechanical effects. Mr. Brown (Versu's Byron-like poet) felt flat when given only flowery dialogue; he came alive when his "escalation" tendency became mechanical — maximum offense at insults, doubled warmth at flirtation, sulking at rejection.

> **Easy to Communicate** — complex traits rarely come across. A character "habitually unpleasant to high-ranking men" read as merely surly because most male characters were rich and the player never saw the contrasting cases.

> **Meaningful in Combination** — a system with three emotional styles and three hair colors offers `3 × 3 = 9` combinations, but players experience it as `3 + 3 = 6` because the axes are independent. Mechanical significance helps; so does designing elements that resonate symbolically, where a pair carries meaning the individual elements lacked.

## 5. Recurring Strategies

- **Combining output from several layers (Blood & Laurels poison)** — poison took effect slowly, so the victim went on talking before choking and dying mid-scene. Because the death interlaced with whatever else was happening, the same mechanic produced funny, dark, or sad outcomes depending on the surrounding drama. Instant death would have felt much less rich.
- **Bringing character into every interaction** — juxtapose gameplay-context features (current topic, current feelings about the protagonist) with long-term traits (what kind of person they are). Screenwriters call dialogue without subtext "on the nose"; layering procedural sources produces subtext-feeling content.
- **Concrete layering recipe** — content of the next dialogue beat from prewritten plot needs; emotional content from gameplay-built relationships; text/voice/graphical rendering from long-term traits.
- **Juxtaposing events and interpretation** — players fill narrative gaps. `The robot sighs. "I'd love to,"` reads sarcastic; `The robot grins. "I'd love to,"` reads sincere. A robot poem combining a specific medieval image (`Peasants at the joust / every jaw agape`) with a random proverb (`defeat is ready to spring`) lets the player invent a coherent reading the author never imagined.
- **Callbacks to earlier events** — Versu recorded both the numerical opinion change and a string explaining why, then reused the string later. Fred can later say *"Miss Bates is a fool. She would not stop talking about turtles at supper."* Callbacks make consequence perceivable.

## 6. Pitfalls

- **Overgeneralization** — a behavior set rarely transfers across genres or story lengths. Versu's Regency murder mystery and modern office comedies needed different behaviors: flirting in an office scandalizes a Regency drawing room; office farce wants characters to *over*-interpret signals and start throwing pies, while Regency wants characters to spend time confirming signals before reacting. Multiplying reaction numbers by a scaling factor was insufficient. "A system created for one context may not easily transfer to another."
- **Overrealism** — Versu modeled real-life conversational pragmatics (e.g., respond more to people you have stronger relationships with). Realistic, but when the player walked in on two close friends, the friends acknowledged them briefly and resumed. Players complained, so the team weighted NPCs to always prefer the player; testers reported the result felt "much more realistic." Realism that violates expectations of player centrality fails the game.
- **Untamed simulation** — in an unreleased Versu office comedy, two flirting characters had sex during a strategy meeting in front of coworkers; rules against work-setting intimacy were absent. *Blood & Laurels* solved similar derailments with **scene-by-scene constraints** specifying which characters were allowed to die, leave, or have sex in each scene. Sandboxes and roguelikes can tolerate untamed simulation (dwarfs starve, Sims trap themselves); narrative contexts must prevent simulation from stretching the framework beyond what the author can handle.
