# Ch 9: Uncanny Text — Blending Static and Procedural Fiction

## Table of Contents

- [1. Thesis](#1-thesis)
- [2. Southern Monsters](#2-southern-monsters)
- [3. Playful Text in Smaller Projects](#3-playful-text-in-smaller-projects)
- [4. Inheritance from Dwarf Fortress](#4-inheritance-from-dwarf-fortress)
- [5. Tools and the Future](#5-tools-and-the-future)

## 1. Thesis

- **Procedural text explodes meaning** — Snow stumbles into procgen project by project rather than planning for it. It doesn't need to be sophisticated to work; its uncanny quality is the point.
- **Static + procedural together** — in Snow's games the distinction dissolves. Static text gives a fluid structure; procgen text warps with state. Neither is better; the blend is where meaning lives.

## 2. Southern Monsters

- **Semi-autobiographical Twine game** — teenager Cripplefoot in south Arkansas, moderates a paranormal forum, hunts the Boggy Creek Monster in the swamp. Systems model coping with domestic-violence trauma; no explicit "depression meter". The player should feel as helpless as the character.
- **Shower anecdote** — at a convention a player took nine or ten showers in a row. Text shifted each time: *"Oh, the words changed"*, *"Oh, this is getting sad"*. The generator is simple, but surprised a disinterested player.
- **Mood tracking** — numeric mood (0–100 %) collapsed into 1–3 with small randomness, plus a qualitative "current mood" (named after LiveJournal). Both invisible to the player; both shape choice text and generation. The attendee's endless showers set his current mood to *"self-loathing"*.
- **Context-driven eating** — a marshmallow pie is pleasurable unless recent history makes it not. The generator weighs prior mood, the act itself, the aftermath.
- **Most complex generator — cat videos** — picks a genre (sleeping, playing), a paragraph structure, sentence structures, and horizontal context (mentioning snow sets context=snow, later clauses respect it). Example output: *"A lean cat attacks a stuffed fish under a blanket. The cat shreds the fish, spilling cotton everywhere, while someone shrieks off camera. I rewatch the video, again and again, to absorb the scene's warmth."* No tagging, no weighting; iteration is cheap at this scale.

## 3. Playful Text in Smaller Projects

- **Battlecakes (Volcano Bean RPG)** — cupcakes on a quest. Library books are generated from academic-textbook structure × cookbook vocabulary, producing titles like *"Discovering Banana Cake"*, *"Sixty Years of Baking Mysteries"*, *"Ice Cream & Philosophy: The Hidden Connection"*. Word soup limited by per-syllable categorisation plus a syllable cap. The uncanny tone was the point; a shuffled list of funny titles would have been flatter.
- **Jake Elliott's "Playful Text" (Konsoll 2017)** — philosophy of "open, organic possibility spaces" informed by postmodern art, from *Kentucky Route Zero*'s Act IV. Procgen need not be judged only by agency and binary dialogue choices.
- **The Domovoi (2014)** — Twine story of a Soviet folklorist performing a tale about a house spirit. Heavy Twine randomisation: *"even this performance will change — words will be different in your memories than when you first heard them"*. If the storyteller becomes angry, she beats the domovoi with a hammer and narrates nine trauma-reverberation paragraphs chosen at random. The slipperiness enforces the story's theme about memories that continually recontextualise themselves — Snow's PTSD after military discharge.
- **Memory Blocks / Animal Town** — contribution to Priscilla Snow's Twine anthology about memory cards, inspired by *Animal Crossing* letters. Real Animal Crossing uses minimal procgen; *Animal Town* leans into the uncanniness: villagers send randomised replies that barely acknowledge the player's sincere letters. The disconnect becomes funny, touching, a little melancholy — the point.

## 4. Inheritance from Dwarf Fortress

- **Matul Remrit (2010–2013)** — Snow's multimedia fanfiction Let's Play of a single *Dwarf Fortress* v0.31 game. Written in a stilted style imitating the game's uncanny procedural text. DF's raw events (a dwarf's violent tantrum triggered by minor irritations) were given narrative motivation, fixing one canonical reading of the machine's output.
- **Since then** — Snow's career has done the opposite: using procedural text to *complicate* or emphasise meaning in static narrative, not to canonise one reading.

## 5. Tools and the Future

- **Commercial contracts squeeze out procgen** — Snow's worry is that without accessible tools, procedural text stays a hobbyist craft.
- **Wish list** — dialogue tools with procedural-text hooks like **ink** and the **Spirit Character Engine**, easy to pitch to a lead or editor.
- **Voice acting vs. procgen** — live voice is incompatible with procedural text, but even fully voiced games have troves of written environment text (imagine a complex generator for the hundreds of books in *The Elder Scrolls*). Tools are what let these procedural moments exist in practice.
