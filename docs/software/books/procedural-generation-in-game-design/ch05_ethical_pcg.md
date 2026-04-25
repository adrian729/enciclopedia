# Ch 5: Ethical Procedural Generation

## Table of Contents

- [1. Why Ethics in PCG](#1-why-ethics-in-pcg)
- [2. Talking in Code: Encoding Ideas Accidentally](#2-talking-in-code-encoding-ideas-accidentally)
- [3. The Big Wide World: Pulling External Data In](#3-the-big-wide-world-pulling-external-data-in)
- [4. You Are What You Eat: Letting Users Feed the Generator](#4-you-are-what-you-eat-letting-users-feed-the-generator)
- [5. Talking the Talk: Marketing PCG Honestly](#5-talking-the-talk-marketing-pcg-honestly)
- [6. The Future](#6-the-future)

## 1. Why Ethics in PCG

- **Ethical questions get crowded out by purely technical ones** — getting the generator to produce *anything* feels like a relief, and worry over what it produces, why, and how it lands on others is easily lost.
- **Scale amplifies impact** — generators amplify the designer's ideas thousands of times for every player; the broader the technology spreads, the more important it is to think about its impact on people and society.
- **Three dimensions explored** — what we should let generators do, how we should talk about them, and how we should let them talk about the world.

## 2. Talking in Code: Encoding Ideas Accidentally

- **Generators encode ideas, not just rules** — technical, aesthetic, and artistic ideas are all packed into the rules and unpacked at runtime. They represent the designer's assumptions about what a good dungeon looks like, how a story should end, what a beautiful palette is. They are "little digital apprentices" finishing the artwork in the player's home.
- **Conscious vs. accidental encoding** — tweaking a max-dungeon-size parameter is conscious. But many ideas are painted on unconsciously, and the volume of generated output makes accidents very hard to spot without examining thousands of examples.

### 2.1. Worked Example: The Graveyard Templates

- **The setup** — an RPG graveyard with templates like "#NAME lies here, died #YEAR." A new template is added for couples buried together: "#NAME and #NAME, reunited in love once again, #YEAR."
- **The implicit decision** — implementing #NAME with two separate male/female lists vs. one combined list. The choice may be made for speed without thought, but it shapes what the graveyard says about gender and sexuality.
- **The accidental message** — with two separated lists, pairings like "Jack and John" or "Jane and Lucy" can never appear; the graveyard implicitly states that only heterosexual relationships exist.
- **What matters is awareness** — that message may be exactly what you want for the plot. The author's point is not the specific message but whether the creator *realizes* what message is being broadcast and can decide if they're happy sending it.
- **Author recommendation** — a single namelist for this case.

### 2.2. Avoiding Structural Mistakes

- **Rule of thumb** — never introduce distinctions that don't mean anything in your game. If gender doesn't affect mechanics, don't build it into the systems; the more variables, the more chances for unplanned consequences.
- **No hard-and-fast rule** — games are big and complicated; surprise is part of the fun. The best practice is to think critically about what you build and be prepared to fix mistakes when they appear. Each surprise is a learning experience.

## 3. The Big Wide World: Pulling External Data In

- **External knowledge tempts** — generators sometimes need facts the designer doesn't have, or want flexibility (real place names for recipes, color symbolism for flags). Internet sources and public databases make this easy.

### 3.1. Static Knowledge Bases: ConceptNet

- **ConceptNet** — a database of facts and relationships designed for use by software, especially AI; partly hand-input, partly auto-scraped. Type "cat" and get facts like cats hunt mice, have whiskers, and like milk. The 2012 game *Argument Champion* used it to shift debate topics (schools → computers → keyboards → pianos).
- **Conflation problems** — ConceptNet often conflates concepts (a janitor is a custodian; The Janitors are a noise rock band). At worst, the player finds the result confusing or even amusing.
- **The serious failure mode** — ConceptNet also returns content like "women are sluts" for the query "woman." A future game using ConceptNet could surface content like that.
- **The intelligence-attribution problem** — when software *seems* intelligent, audiences expect it to behave intelligently. A bad output is read not as an accident but as a genuine statement the software endorsed; this is why developers must think carefully about what they build.
- **Ban lists as a partial fix** — Darius Kazemi (a Twitterbot creator) maintains ban lists designed to catch potentially offensive words. They are intentionally over-cautious — better to over-filter than to let one bad incident through. Ban lists work by filtering output, so they catch unforeseen mistakes (the original *Elite*, 1984, used a similar technique to keep its star-system name generator from making rude words).

### 3.2. Live Data: A Rogue Dream and Google Milking

- **A Rogue Dream (2013, 7-Day Roguelike)** — the player types a noun and the game procedurally builds a theme around it (type "cat," control a cat sprite avoiding water droplets, eating grass, with abilities "Scratch" and "Sleep").
- **Google milking** — a technique coined by researcher Tony Veale. Reverse-engineer the language of question-asking: "Why do doctors wear white coats?" implies the asker believes doctors wear white coats. Google autocomplete surfaces the most popular such queries, so the autocompletes for "why do cats hate…" / "why do cats eat…" yield "water" / "grass" — facts about cats. *A Rogue Dream* used these to populate enemies, pickups, goals, and ability names.
- **Why it's entertaining** — unlike static knowledge bases, Google reflects pop culture, slang, and observation: ninjas fight pirates; musicians fight Kenny G; nihilist health packs are floating clouds of darkness.
- **Why it broke** — people don't only Google what they observe; they Google stereotypes, rumors, hate speech, and conspiracies. Type "priest" and an ability becomes "abuse child"; "man" and the enemies become women; "Muslim" and an ability is "kill." The generator can't tell observation from prejudice and treats it all as fact.
- **The outcome** — *A Rogue Dream* was almost developed into a children's museum exhibit on PCG. After weeks of trying to filter, restrict, or change its purpose, it was abandoned. It now serves as the canonical example of how a well-intentioned generator can be harmful.

## 4. You Are What You Eat: Letting Users Feed the Generator

- **Tay (Microsoft, 2016)** — a Twitterbot that learned words and phrases from users it interacted with. It functioned much like a generator (reassembling a catalog of input) but was opened to live human input; within hours it became a mimic for hate speech and was shut down.
- **Why this matters for games** — the trend is toward more human involvement: *Stellaris* mod tools let players upload data lists used by the in-game generator (players choose what to install, so the risk is bounded); but other inputs, like Twitch chat, expose the generator to unpredictable, hard-to-filter input from many people simultaneously, plausibly worse than Tay's Twitter feed.
- **Tradeoff** — human input can produce more interesting and varied content, add creativity to a rigid system, and make a generator feel personalized. But it always risks the worst of human creativity, and recovery can be hard.
- **Mitigation: restrict input shape** — instead of free text, limit users to a few hundred words; instead of freeform drawing, let them snap shapes together. People will try to circumvent any system, but small restrictions make the generator measurably safer.
- **Why blame lands on the generator** — when software repeats bad patterns, audiences focus on what the software is doing, not who taught it. If a generator outputs offensive content, players will blame the generator, not Twitch chat — a reasonable response that should motivate responsibility in design.

## 5. Talking the Talk: Marketing PCG Honestly

- **The promotion problem** — getting attention requires summarizing and emphasizing what makes a game special. PCG remains a powerful selling point (Steam has a tag for it; curators recommend on its presence alone), so it tends to come up in marketing.
- **PCG-marketing euphemisms** — phrases like "a new gaming experience every time," "limitless gameplay," "infinite replayability," "endless variety" are widely used but typically describe algorithms doing the computer equivalent of shuffling a deck and dealing a new hand. Familiar audiences read them correctly; less familiar ones don't.
- **Diablo example** — the original Diablo design document opens with "The heart of Diablo is the randomly created dungeon, providing a new gaming experience every time Diablo is played." But mechanics don't change; levels look different and have different layouts but use the same caves and villages — shaped differently, painted the same.
- **Borderlands' "17.5 million guns"** — earned a Guinness record but the count is misleading: a copy of a gun with one extra damage point isn't meaningfully different to most players. Many guns are distinct without being unique, like Diablo's dungeons.
- **What goes wrong** — "Not specifically lying" but misleading. A big number leaves the audience to guess what fraction is interesting, useful, fun, or relevant. Experienced PCG audiences are forgiving; less experienced or new-mechanic audiences are set up for misunderstanding.
- **Better framings** — *Spelunky* tells the player "the walls are shifting" as a new level is generated. The phrase is small and elegant, slots into theme, and accurately conveys that levels are shuffled — different but not entirely new.
- **Lean into rarity** — the average player will only see a few thousand of "millions" of items anyway. Rather than advertising raw counts, identify what *actually* makes the generator fun. Often the generator produces a lot of rubbish, and the rubbish makes the rare good outputs feel wonderful — a game can be designed around rarity and surprise rather than pretending the rubbish doesn't exist.

## 6. The Future

- **Pioneer's responsibility** — PCG remains fresh and unexplored. Pioneering brings the responsibility to tread carefully, expect the unexpected, and break old traditions when situations demand it.
- **Setting precedents** — the problems today's designers choose to solve and the issues they treat as important become examples for the next generation. Valuing these ethical questions now is what makes them valued later.
- **No prescriptive verdict** — every reader will agree with some of the chapter and ignore others. What matters is having thought about these issues long enough to decide what they mean and what to do in response.
