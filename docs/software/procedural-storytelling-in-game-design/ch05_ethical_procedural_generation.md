# Ch 5: Ethical Procedural Generation

## Table of Contents

- [1. Generators Encode Values](#1-generators-encode-values)
- [2. Pulling Data from the World](#2-pulling-data-from-the-world)
- [3. Letting the World Talk Back](#3-letting-the-world-talk-back)
- [4. How We Talk About Procgen](#4-how-we-talk-about-procgen)

## 1. Generators Encode Values

- **Every generator is a little digital apprentice** — it encodes what you think a good dungeon, story, or palette looks like, and unpacks that opinion in every player's home. Some of the encoded ideas are deliberate, many are accidental.
- **Accidents are hard to spot** — the system produces so much content you can't review it all; bias surfaces only on specific inputs.
- **Graveyard example** — templating `"#NAME and #NAME, reunited in love once again, #YEAR"` with two separate male/female name lists silently guarantees the graveyard shows only heterosexual couples. The problem isn't the feature itself (that may be the authorial intent); the problem is not knowing what message your generator is broadcasting.
- **Rule of thumb** — don't introduce distinctions that don't mean anything in your game. If gender doesn't affect mechanics, don't encode it. Fewer variables = fewer accidental features.
- **No hard fix** — stay critical, expect surprises, be ready to repair mistakes. Every surprise is a learning experience.

## 2. Pulling Data from the World

- **External knowledge sources amplify risk** — Wikipedia, **ConceptNet**, live Google queries, and similar sources import the messiness of the real world into your generator.
- **Argument Champion (2012)** — debate game using ConceptNet to leap between topics (schools → computers → keyboards → pianos). Polysemy breaks things (the "keyboard" shifts meaning mid-chain); outright offensive "facts" lurk in the database (*"women are sluts"* appears in ConceptNet for "woman").
- **Why users blame the game** — when software seems intelligent, humans treat its mistakes as genuine statements, not accidents. The system becomes responsible for what it says, full stop.
- **Banlists** — Darius Kazemi (Ch 2) maintains banlists that filter generator output; the principle is "better to accidentally filter too much than too little". Even the original *Elite* (1984) tweaked its star-name generator to avoid producing rude letter combinations.
- **A Rogue Dream (2013)** — Cook's 7-Day Roguelike that used **Google milking** (Tony Veale's coinage): reverse-engineering question language in Google autocomplete to extract folk knowledge. *"Why do cats hate …"* → "water"; *"Why do cats eat …"* → "grass". Cats avoid water droplets and eat grass in the resulting dungeon.
- **Where it broke** — folk knowledge includes stereotypes, rumours, and hate speech. Priest's powers included *"abuse child"*; typing *"man"* made the enemies *"women"*; typing *"Muslim"* gave abilities that included *"kill"*. Weeks of filtering couldn't salvage it. Cook abandoned the project; now it serves as a warning.

## 3. Letting the World Talk Back

- **Tay (Microsoft, 2016)** — Twitter bot that learned from users. Taken offline within hours after being trained into a mimic for hate speech and nonsense. Lesson for procgen: the moment real people can feed input into your generator, the generator inherits their worst impulses.
- **Where this shows up in games** — mod tools that let players edit procgen data lists (*Stellaris*); Twitch-chat-driven inputs to a streamer's game. Modding at least lets the player choose what to install; broadcast inputs don't.
- **Restrict input to limit damage** — constrain text input to a small vocabulary, replace freeform drawing with snapping shapes. People will still try to game it, but restrictions make your generator safer without forbidding experimentation.
- **Who gets blamed** — not the users. Once bad patterns appear, the audience attributes them to the software (and its authors), not to whoever taught it.

## 4. How We Talk About Procgen

- **Marketing language leaks meaning** — *"a new gaming experience every time"* (Diablo design doc), *"limitless gameplay"*, *"infinite replayability"*, *"endless variety"*. These are euphemisms for shuffling a deck. Experienced players translate automatically; newcomers inherit the hype as literal promise.
- **Big-number marketing** — *Borderlands* (2009) made its 17.5 million guns a Guinness World Record. Most of those differ by a single damage point; mathematically distinct, perceptually the same (see Ch 1's 10,000 Bowls of Oatmeal / perceptual uniqueness).
- **Spelunky's quiet version** — the loading line *"the walls are shifting"* promises exactly what it delivers: levels are being shuffled, not invented from scratch. Small language choice, fits the theme, avoids overselling.
- **Lean into what your generator is actually good at** — if it produces a lot of rubbish, the rare gems become the hook (rarity and surprise). Don't promise uniqueness you aren't delivering.
- **The future** — procgen is still a pioneering field. The precedents set now (ethical concerns included) will frame how the next wave of practitioners think about the craft.
