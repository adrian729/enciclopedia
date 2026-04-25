# Ch 20: Poetry Generation

## Table of Contents

- [1. Context and Examples](#1-context-and-examples)
- [2. Why Generated Poetry Is Hard](#2-why-generated-poetry-is-hard)
- [3. Domain Knowledge over Computer Science](#3-domain-knowledge-over-computer-science)
- [4. Generation Pipeline in A House of Many Doors](#4-generation-pipeline-in-a-house-of-many-doors)
- [5. Player Control as a Design Principle](#5-player-control-as-a-design-principle)
- [6. Embracing Badness](#6-embracing-badness)

## 1. Context and Examples

- **Source project** — Tuffs's RPG *A House of Many Doors* generates poems shown in-game as four-line "extracts" from a larger piece. Each attempts a single overarching theme (a horn, a horse, a politician). Sample outputs include "Tales of the Lunatic Horn of Pride" (dramatic verse), "Hunting with the Magnificent Horse" (heroic epic), and "The Dancing of the Politician" (satire).
- **Honest verdict** — they are "all pretty bad. Just not very good at all."

## 2. Why Generated Poetry Is Hard

- **Uncanny lexis** — analogous to the uncanny valley. CGI can produce beautiful trees but struggles with human faces; generators handle rocks and continents tolerably but stumble on language because brains are "finely tuned word tools" and humans immediately notice flaws. Familiarity breeds difficulty.
- **Neural networks vs procedural generation** — a Google neural-net poetry sample is far more impressive as AI (it learns grammar rather than being programmed to obey rules), but the resulting poems are not better than procedurally generated ones in literary quality. "My proc gen poems are bad. But not that bad."

## 3. Domain Knowledge over Computer Science

- **Author background matters** — Tuffs is an English literature graduate, not a computer scientist. He categorized the word database by rhyme, lexical category, meaning, *and* number of syllables.
- **Meter as a priority** — without stress detection, syllable counts alone gave poems an approximation of cadence. He suspects a CS-first approach would have skipped this entirely. Real-world knowledge of the domain "can cause you to totally reevaluate your approach"; if no degree is on hand, a week or two of intense research will do.

## 4. Generation Pipeline in A House of Many Doors

- **Origin story** — poetry was originally just a flavor wrapper for XP: spend "memories" (e.g., A Moment of Melancholy, a Horrifying Ordeal) to "write a poem," with only a generated title and the rest left to imagination. After casual mention during the Kickstarter caught fire, full poem generation became necessary.
- **Genre first, then title, then everything else** — opposite of how real poems are written, but it ended up working. Spending Breathtaking Spectacles produces a heroic epic; the title is collated from genre-appropriate words ("magnificent" + "horse"), then the body is generated from those.
- **Themed word selection with weighted variance** — synonyms of the title nouns (`stallion`, `pony` for `horse`) get high probability; loosely related but non-synonym words (`lance`) get lower probability; genre-relevant unrelated words (`sword`, `hero` for epics) get a smaller chance; and a "very small chance of totally random deviation (just for fun)" remains.
- **Line templates** — once the key nouns/verbs/adjectives are chosen, the system fills line templates ("With ___ as ___ as your ___"). Template choice is weighted by genre and by the grammatical construction of preceding lines, with a small random-deviation chance again.
- **Database scale** — almost 10,000 words categorized by synonyms, rhymes, syllable counts, and genre weighting. The system "can spit out more poems than there are atoms in the universe."
- **Future direction** — categorize words by **metric feet** as well as syllables to enforce stressed/unstressed patterns and "ruthlessly administered iambic pentameter in the Shakespearean vein," since "almost anything in iambic pentameter sounds nice and literary."

## 5. Player Control as a Design Principle

- **Player as participant, not button-pusher** — in *A House of Many Doors* the player earns a memory resource and chooses what genre to spend it on (epic saga, melancholic lament, satire, romance, dream vision). Even though code does the heavy lifting, the player feels involved in shaping the result.
- **General principle** — the best world builders let players tweak parameters (world size, demographics, magic system in *Dwarf Fortress*); this turns generation from a one-time party trick into an ongoing experiment. Sliders that visibly alter rainfall make players appreciate the simulation depth they would otherwise never notice.
- **Author's regret** — he wishes he had let players choose the *subject* of the poem ("a politician") rather than only the genre, but development was too far along.

## 6. Embracing Badness

- **All computer-generated poems will be bad** — even with metric-feet improvements, uncanny lexis ensures stilted output (until robot overlords arrive).
- **Closing rule** — embrace badness as long as it is funny or interesting. The aim is **funny-bad** rather than **frustrating-bad**.
