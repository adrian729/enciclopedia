# Ch 15: Generating Histories

## Table of Contents

- [1. Why History Is Hard](#1-why-history-is-hard)
- [2. A Model: Entities, Events, Logic, Accounts](#2-a-model-entities-events-logic-accounts)
- [3. Subjectivity — Process vs. Artifact](#3-subjectivity--process-vs-artifact)
- [4. Caves of Qud's Implementation](#4-caves-of-quds-implementation)
- [5. Historical Rationalization](#5-historical-rationalization)
- [6. Questions for Any History Generator](#6-questions-for-any-history-generator)

## 1. Why History Is Hard

- **Codifying relationships into rules** — real histories are tangled webs of people, places, and events; the mechanics are obscured by their complexity.
- **History serves a rhetorical function** — accounts are used to promote cultural narratives, not just to relay facts. Games usually ignore this, even hand-authored ones.
- **A new subfield** — qualitative procedural generation; no canonical solutions yet.

## 2. A Model: Entities, Events, Logic, Accounts

Grinblat frames history as the interplay between **historical entities** (nouns — people, places, objects as bags of properties) and **historical events** (verbs — functions that modify those properties). A generative history system does four things:

1. Model historical entities
2. Model historical events
3. Relate events via an underlying **historical logic**
4. Expose **historical accounts** (alleged results of events) to the player, usually as generated text

- **Events carry the aesthetic** — *Caves of Qud* targets ancient-world biographies (`#character# sieges a city`, `#character# builds a monument`); a high-school generator would have `takes a test`, `goes on a first date`.
- **Logic options**:
  - **Weighted tables** — *Epitaph* (Max Kreminski) lets mastering fire lower foodborne-illness odds and raise forest-fire odds.
  - **Deeper simulation** — *Dwarf Fortress* dwarves act per physical/social rules; newsworthy actions become logged events (the annals in Legends mode). Mirrors how real histories are manufactured: an authority narrativises a subset of events, potentially distorting.

## 3. Subjectivity — Process vs. Artifact

- **Most games adopt a reductive "objective" frame** — *The Elder Scrolls* (especially *Morrowind*) is a notable exception with its heresies; Stephen Lavelle's *Opera Omnia* makes subjectivity the theme, casting the player as a historian cynically building models for a political boss. All games make arguments about history, explicitly or implicitly.
- **History as a process** — the playing-out of rules and relationships that produce the present. Simulate the logic to reproduce it.
- **History as an artifact** — a flattened constituent of the present, engaged with through a contemporary lens. Only historical accounts are accessible; accounts are biased and incomplete. Generate the artifact by reproducing the producing logic, or invent a new logic that yields the same kind of artifact.

## 4. Caves of Qud's Implementation

- **The setting** — thousands of years in the future among the reclaimed ruins of a vast arcology. Inspirations: *Gamma World*, Clark Ashton Smith's Zothique, Gene Wolfe's *Book of the New Sun*, Le Guin, Gibbon's *Decline and Fall*, *Dwarf Fortress*, *ADOM*. Humanity's relationship with history is a main theme.
- **Two scope constraints** — added late in development (limited resources) and had to match an existing handwritten voice. Solution: focus generation on the mythic lives of five **sultans** from a diegetic age called the **sultanate**.
- **Domains as epithets** — each sultan gets an archetypal "domain" (glass, jewels, ice, stars; also might, scholarship, chance), functioning like epic-poetry epithets.
- **Aesthetic — high novelty** — no prescribed narrative arc (no "formative experience", "overcomes obstacle"). Let the generator produce atypical life paths; rely on player **apophenia** (over-perception of patterns) to drive interpretation. Players already have the cultural tapestry of present-day Qud, handwritten lore, and prior player-characters as context.
- **Gospels** — the internal name for historical accounts. Each event manifests a single gospel (text snippet). Gospels appear on **cultural artifacts** (shrines, paintings, engravings) generated dynamically as the player explores. NPCs share them through a reputation-mediated custom called the **water ritual**. The journal sorts collected gospels chronologically so a biography coheres.
- **Historic sites and named items** — places the sultans visit are instantiated during world gen as historic sites; named items left during life events appear at those sites with their historical properties.
- **Generation flow** — instantiate sultan with core properties (name, pronouns, birth year, birth region, location, domain). Resolve a prescribed birth event. Randomly pick an event from the pool, resolve an outcome using sultan state + branching, update sultan + any affected entities, generate a gospel via a Tracery-like replacement grammar. Update global state (current year). Repeat ~12 events. End with a death event if the sultan is still alive.

## 5. Historical Rationalization

- **No intrinsic causality** — events are chosen randomly. The gospels *profess* causes. A `sieges a city` gospel template:

  *"Acting against #injustice#, #sultanName# led an army to the gates of #location#."*

  The `#injustice#` slot looks at the sultan's state for meaningful content (e.g. allied frog factions → *"the persecution of frogs"*). If no suitable cause exists, the event can *create* one by retroactively adding frogs to the sultan's allied factions. The effect causes its own cause — this is the **historical rationalization** the chapter names.
- **Coherence through shared state** — the sultan's state acts as glue. Domains especially: almost every gospel pattern has symbols referencing domains, so the text keeps returning to them.
- **Antixerpur (domain: ice), worked example** — found as a babe with icicles in her hands, assassinates the sultan over a prohibition on encasing things in ice, leads armies to punish bans on ice-related practices, founds a dig site to excavate ancient blocks of ice, wields a frosty hammer named **Frostycus Catsfriend**, devastates cities with icy winds. In gospel 5 she allies with cats; gospel 6 re-uses that alliance to rationalise the Battle of Old Teggash even though the random selection of gospel 6 didn't know about gospel 5. Apophenia supplies the story — perhaps a deal, help for help.
- **Why subvert historical logic** — fits the game's theme: players engage with the past without its original context, so the simulation encodes its own ignorance of its world history.

## 6. Questions for Any History Generator

- In what narrative context will the history be engaged? Process or artifact?
- Who tells the history? What are their biases?
- How do we split history into entities and events?
- What logic relates the events — and what does that logic argue *about* history?

History is threaded everywhere through social life. Turning procedural tools toward it opens a new frontier in meaning-making.
