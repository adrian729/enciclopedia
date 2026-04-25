# Ch 25: Generating Rules

## Table of Contents

- [1. Why Rules Are Rarely Generated](#1-why-rules-are-rarely-generated)
- [2. Mix and Match: A Rule Language](#2-mix-and-match-a-rule-language)
- [3. Heuristics and Random Playtesters](#3-heuristics-and-random-playtesters)
- [4. An Open Frontier](#4-an-open-frontier)

## 1. Why Rules Are Rarely Generated

- **Rules as the rarest generated content** — most PCG produces art, audio, worlds, NPCs, or quests; the actual rules players follow are almost never generated, because rules define what the game *is*.
- **Two structural obstacles** — rules don't fit neat templates like dungeons or quests (they are usually one-off bits of executable code), and they are hard to test (a broken ruleset can render the whole game unplayable, and even humans struggle to spot brokenness in their own designs).
- **Rules sit on a spectrum** — in *Sokoban* the rules fully define the game, while in hide-and-go-seek they only set up creative play; this matters because the more the rules *are* the game, the riskier it is to let a generator touch them.

## 2. Mix and Match: A Rule Language

- **Parameter generation as the entry point** — most game designs are "only a few changes away from entirely different game variants" (consider the family of match-3 games); collecting all balancing parameters into one list and generating values for them already produces variants.
- **Build a tiny rules language** — rather than generating code, define a language of components the generator can snap together; the simpler the rule type, the easier the language. Collisions are a good first target: pick two object types and one effect.
- **Generic object names, not gameplay roles** — list "turtle" or "mushroom," not "enemy" or "health," because *what counts as an enemy or a healing item is not known until after the rules are fixed*.
- **Effects as code blocks** — break general events (gain score, die, get a power-up) into discrete effect blocks the generator can attach to a rule.
- **Expand by stacking dimensions** — give collisions two effects (one per object, enabling *PAC-MAN*-ghost-style asymmetric kills), add rules for leaving the screen or pressing a key, and so on.
- **Include "useless" objects deliberately** — add the floor, background objects, and the UI to the object list; generators that only see predictable inputs only emit predictable outputs.

## 3. Heuristics and Random Playtesters

- **Random rule combinations are mostly bad** — pure random selection of rule components will produce many boring or unplayable rulesets; the generator is "not as good a game designer as you."
- **The author already encodes design knowledge** — every object and effect added to the language is an implicit design judgment (the generator wasn't allowed to adjust music volume or delete files); the rules language itself is the first layer of guidance.
- **Heuristics — rules of thumb that filter rulesets** — guidelines the generator believes about *any* ruleset it produces. Example: a *Candy Crush*-style game must have at least one rule that destroys blocks; absent that, the ruleset can be scrapped immediately. Even a heuristic as basic as "Can the player do anything?" cuts a huge percentage of bad designs.
- **Up-front heuristics aren't enough** — like any designer, you can't tell what a ruleset plays like just by reading it, which is why human games are playtested.
- **General Game Playing (GGP)** — research field building AI that can play any game, even an unseen one, by rapidly learning rules; one application is automatic evaluation of generated games. Cutting-edge but a long road.
- **The dumbest agent is still useful** — running a *random* AI player on a generated ruleset 10 times and recording outcomes (completed the game? gained score? touched objects?) yields data. If all 10 random players never died or all finished in under 3 seconds in a *PAC-MAN*-style game, the ruleset is suspect. Random play is a worst-case-scenario probe and a step beyond static heuristics.

## 4. An Open Frontier

- **Rule generation is largely unexplored** — past experiments range from inventing new chess variants to fully automated game designers, but there are few accepted ideas.
- **A basic recipe** — building blocks for rules + heuristics to reject bad ones + a random player to probe gameplay is a starter kit, not a finished method.
- **Why this is exciting** — because no one knows the best approaches yet, untried ideas are likely genuinely untried; new genres may be waiting on the other side of an experiment.
