# Ch 27: Meaning

## Table of Contents

- [1. Meaning in Games](#1-meaning-in-games)
- [2. Meaninglessness in Games](#2-meaninglessness-in-games)
- [3. Designer and Player Meaning](#3-designer-and-player-meaning)
- [4. Meaning in Qualitative PCG: URR](#4-meaning-in-qualitative-pcg-urr)
- [5. Conclusion](#5-conclusion)

## 1. Meaning in Games

- **Meaning is created through connection** — in games (and any work of art) meaning arises when elements link to each other: a phrase that recalls an earlier line, a logo seen previously, a boss whose visual design echoes earlier enemies. Without such links, content is mere background — important, but not *meaningful* because it could be swapped out without changing the message.
- **Lore as a common vehicle** — optional textual content that fleshes out a world rather than gating mechanical success. Procedural games handle lore in distinct ways:
  - **Tales of Maj'Eyal** — scattered lore that aggregates into a body of data; the apparent story can morph as more information is acquired.
  - **Dungeon Crawl Stone Soup** — draws on classical mythologies (Greek, Egyptian, Jewish, Hindu) to position monsters, hinting at their behavior via mythic origins.
  - **The Binding of Isaac** — fragments of story surface gradually across many playthroughs, retroactively reframing grotesque monsters and body horror as a deeper narrative about (interpretations vary) religion, child abuse, parenting, and imaginary worlds.
- **The lore "deal" with the player** — players must be persuaded that there is enough meaning to merit their time. A generator that emitted *Souls*-style cryptic utterances without an underlying coherent narrative would be quickly seen through: signifiers of meaning that signify nothing destroy investment.
- **Lore can also undermine meaning** — citing **Erik Champion**'s *Critical Gaming: Interactive History and Virtual Heritage*, the *Elder Scrolls* world described in books and NPC dialogue is "almost infinitely richer" than the world the player can actually interact with; the gap reminds the player of the artificiality and limits of the game space.
- **Meaning is a balance** — a meaningful world must feel "hermetically sealed," giving out the right amount of information: enough to make elements cohere, not so much that it advertises what isn't there.

## 2. Meaninglessness in Games

- **Two characteristic failure modes in PCG** — the **unnecessary item** and the **mostly uninteresting map**.
- **The meaningless item** — when items are linearly ranked and decisions like "Weapon A vs. Weapon B in Context C" rarely arise, acquiring a strictly inferior item is an effectively meaningless moment. Meaninglessness here is *emergent*, not inherent: the same Weapon A would have been deeply meaningful at the start of a run. This is most marked in the **Angband** family, where late-game item decisions become impossible without ignoring most of the loot.
- **Why PCG amplifies the problem** — randomized item statistics mean only a small portion will be relevant to any given character. Some games "tilt" generation toward the player's strengths and weaknesses to raise the share of meaningful drops, but procedural elements without meaning to the current run cannot be eliminated.
- **The mostly uninteresting map** — on large procedural terrains, much of the space exists only to separate points of interest (settlements, dungeons, events). Ambient additions (weather, flora, fauna, random events) — including those used in **URR** — can mitigate the dead air without filling it.
- **Granularity of interest** — the author's term for the *volume of present content that is actually intriguing, relevant, and meaningful to a player*.

  | Granularity | Player experience |
  |---|---|
  | **High** | Points of interest are closely packed; consistent high engagement |
  | **Low** | Large stretches of filler between interesting moments; sinusoidal rhythm — rest then intensity, each made stronger by the contrast |

- **Low granularity is not automatically worse** — *No Man's Sky* explicitly accepts that many planets and regions will be uninteresting and recasts that as a positive: bland worlds make the unique worlds stand out, and exploration plus sharing of interesting finds becomes the central activity.
- **Takeaway** — meaninglessness is hard to avoid in PCG and is often best treated as contrast that highlights meaning, rather than a flaw to be eliminated.

## 3. Designer and Player Meaning

- **Two channels of meaning** — meaning can be *placed by the designer and recognized by the player*, or *projected onto unintended elements by the player*.
- **Fixed content as anchors** — many PCG games place a database of fixed content first (or with priority) and let procedural systems work around it. Examples: fixed bosses and characters in **Ancient Domains of Mystery** and **Tales of Maj'Eyal**, and **Spelunky**'s long chain of secret actions to reach the final boss (specific items, locating an area, dying in a particular place). This gives designers authored points of meaning while the bulk of content remains procedural; the constraint is that surrounding generation must always accommodate the fixed pieces.
- **Vaults — handmade optional segments** — a related-but-distinct system: hand-authored content embedded inside procedural areas. **Dungeon Crawl Stone Soup** **vaults** range from unique gameplay challenges to thematic vignettes (a shrine to a bloodthirsty god strewn with sacrifices, or the "tragic and rather amusing" tale of the deceased bakers). They are typically non-essential, appear only on some playthroughs, and develop background rather than the immediate narrative.
- **Player-assigned meaning** — players regularly read meaning into events the designer never intended: AI behavior interpreted as smarter than it is; the sudden discovery of a powerful weapon in an otherwise unlucky run becoming a defining moment.
- **YASD / YAVP narratives** — "Yet Another Stupid Death" and "Yet Another Victory Post" forum posts are player-authored stories that retroactively assign narrative meaning to permadeath roguelike runs whose key events were entirely procedural.
- **Self-imposed challenges as meaning** — risk-for-reward play, **Dungeon Crawl Stone Soup**'s 15 runes (3 needed to win; more = more prestige), and **NetHack**'s **conducts** (e.g., the vegetarian conduct, forbidding the character from eating meat) are ways players add weight to a particular run. Such practices are rare around non-procedural games (compared to speed running or high scores), but ubiquitous around roguelikes — anchors that "undermin[e] the popular idea that randomness is necessarily devoid of any deeper importance."

## 4. Meaning in Qualitative PCG: URR

- **URR (Ultima Ratio Regum) hinges on meaning** — the author's own game treats meaning not as decoration but as the central design pillar.
- **Chains of meaning** — the foundational idea: "Nothing (or at least, very little) is intended to appear in the world that is only related to itself, or only related to one other element." Every generated element ties into others.
- **Procedural flora and fauna with cross-links** — large databases with options that enable/disable each other model wildlife and plant spread, so each region has its own animal and plant set, each with a procedurally generated image and name. They orient the player and add variety as the player travels — and, crucially, they propagate elsewhere: book covers depict local animals; healers discuss local plants' regenerative properties; foreigners speak of the national animal or plant of their homeland.
- **Shared aesthetics across cultures and religions** — every secular culture's artifacts share a geometric form (squares, octagons, circles) reproduced from chairs to shop signs to city layouts to floor tilings; every religion's items share particular color sets across vestments, altars, prayer mats, and holy books, with some bleeding between culture and religion.
- **Show, don't tell** — the game never says "this is the coat of arms of House B" — it presents the world and lets the player infer that nothing is disconnected and meaning is there to be found.
- **Meaning as the core gameplay loop** — the player's central objective is uncovering a global conspiracy. Clues sit in the corner of a painting, a particular line of a particular novel, a chest in a mercenary's quarters, a stained-glass window, a piece of poetry. The interwoven generation lets the player track them: a novel containing a clue might be mentioned by philosophers, influence opinion on a recent war, be sold in translation abroad, or be named after a local animal — all of which help the player home in on a copy.
- **Discovering meaning combines designer- and player-led meaning** — the systems author shared meanings; the player must identify, connect, and extrapolate from them.
- **Spoilers comparison** — many classic roguelikes are so complex that players play "with spoilers," consulting wikis on first encounter with a monster, item, or decision. Designers clearly intended these decisions to be made *without* full information; **NetHack** is popularly considered nearly impossible to complete unspoiled.
- **NetHack knowledge vs. URR knowledge** — comparison:

  | | NetHack knowledge | URR knowledge |
  |---|---|---|
  | Scope | Applies across all playthroughs (Medusa always petrifies on line of sight) | Applies only within a single playthrough |
  | Wiki value | High — knowledge transfers | Almost none — only the meta-knowledge that *one is meant to acquire knowledge* transfers |
  | Effect on game mechanic | Spoilers can short-circuit the intended discovery metagame | "Discovering meaning as a game mechanic" is preserved even with spoilers |

## 5. Conclusion

- **Meaning and randomness are not opposed** — fixed markers around which procedural content is generated supply unchanging meaning; deeply interconnected procedural systems that "do nothing in isolation" supply per-playthrough meaning unique to each run.
- **A new mechanic space** — these techniques enable game mechanics centered on discovery, understanding, and problem solving, similar to puzzle and adventure games but replayable across arbitrarily many playthroughs; even riddles and puzzles whose distributed-yet-connected elements should be indistinguishable from handmade ones.
- **Designer mindset shift** — meaning in PCG requires moving beyond the model of "random" generation that distributes affordances without regard to their connections, and instead distributing moments of meaning within the randomness so that stories, backgrounds, and entire mechanics can be built from them.
