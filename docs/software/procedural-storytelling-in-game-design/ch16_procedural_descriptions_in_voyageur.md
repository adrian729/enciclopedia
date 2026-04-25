# Ch 16: Procedural Descriptions in Voyageur

## Table of Contents

- [1. Origins and Premise](#1-origins-and-premise)
- [2. Improv: The Tool](#2-improv-the-tool)
- [3. Filtering and the Filter Stack](#3-filtering-and-the-filter-stack)
- [4. World Models — A Priori vs. A Posteriori](#4-world-models--a-priori-vs-a-posteriori)
- [5. Guardrails and Lessons](#5-guardrails-and-lessons)

## 1. Origins and Premise

- **Emily Short's Parrigues** — a 2015 piece of generative writing, a travelogue guidebook to a fictional medieval country. Inspired Dias to build "an interactive Parrigues".
- **The game** — explore-and-trade in the vein of *Elite*, but with one-way travel. A "descent device" displaces your voyageur ship FTL toward galactic center. You can steer slightly while descending, but every trip is one-way. Name references 19th-century French Canadian canoe voyageurs. Humanity has colonised outward faster than warp travel can keep up, so most colonies are out of regular contact.
- **Why one-way?** — explore-and-trade games collapse into grinding profitable trade routes; one-way travel encourages vagabond play (Sid Meier's *Pirates!* used wind direction for similar effect). Procedural locales don't stand up to revisits; never letting you go back protects that weakness.
- **Emotional tone** — lonely, melancholy. Every place is one you'll never see again. Everyone regards you as exotic and suspicious.

## 2. Improv: The Tool

- **Brief** — text generation from a **grammar** (easy to reason about, syntactic errors traceable to corpus not engine), human- and machine-readable (YAML in source → JSON at compile time), and coherent with a **world state** (don't mention a river in a desert).
- **Shared design with Tracery** — rules have names and lists of possible phrase completions. Improv adds **groups**: phrases under a rule are split into groups, each carrying metadata.
- **Generation loop** — starting from a rule, pick a phrase randomly, expand template slots that reference other rules, recurse until the tree is traversed.
- **Two sources of truth** — grammar + world model. Tracery has only the grammar.
- **World model** — a computer-friendly description of the underlying reality. Example: a Wikipedia sentence about HMS Agamemnon flattens into a nested ontology (Flag: UK; Role: Warship → Ship of the line → Third-rate; Class: Ardent; Era: C18; Propulsion: Sail → Square-rigged; Armament: Cannons).

## 3. Filtering and the Filter Stack

Before picking a phrase, Improv runs **filters** that take (world model, group metadata) and return a salience number or null. Null discards the group; numbers add to the group's **salience score**. High-scoring phrases survive.

- **Soft filtering** — a developer-supplied **culling formula** c = f(m) decides the threshold given the max salience m. *Voyageur* uses `c = m − 10` (empirically tuned; m tends to hover around 30, so it roughly keeps phrases within ~70 % of the maximum). A formula of `c = m` makes the generator rigid; too loose and output goes random.

*Voyageur*'s seven planet-generator filters:

| Filter | What it does |
|---|---|
| **Mismatch** (built-in) | Hard-cull outright contradictions (desert world gets no tundra phrases) |
| **Dryness** (built-in) | Hard-cull phrases already used — Improv needs a memory of used phrases |
| **Full bonus** (built-in) | Bonus for phrases whose tags perfectly match a world-model tag |
| **Unmentioned** (built-in) | Bonus for phrases whose tags haven't yet appeared — bias toward well-rounded descriptions |
| **Tweak** (custom) | Hard-coded per-phrase salience bumps baked into the corpus |
| **Lensing** (custom) | Each planet is "seen through a lens" (culture, biome, etc.); phrases matching the lens gain salience — differentiates similar planets |
| **Bias** (custom) | Bonus for phrases mentioning the planet's special features, prevailing ideology, biome |

The grammar itself is loose: an optional intro (*"Your ship alights …"*) plus loose phrases. A more inter-sentence-aware approach would need something other than a straightforward grammar.

## 4. World Models — A Priori vs. A Posteriori

- **A priori truth** — generate the world model separately (random-tables style), then feed it to the text generator.
- **A posteriori (reincorporation)** — the generator picks a phrase, the phrase's tags are folded back into the world model, subsequent phrases abide by the updated model. Parrigues works this way. Improv supports it with a switch. Corpus frequency drives world frequency: lots of desert writing → lots of desert worlds.
- **What Voyageur actually uses — hybrid**:
  - Planets are seeded with a few basic facts (class, region flavour) before Improv ever runs, because Improv is weak at expressing complex inter-model logic (a city world *must* have a developed non-agrarian economy).
  - Economy balance forced explicit tuning knobs; pure corpus-driven frequency made balancing impractical (reducing availability of one good would have required deleting lines or writing more for other planets).

## 5. Guardrails and Lessons

- **Writing corpora is brutal** — procgen is "200 % of the content for 400 % of the work". Scraped public data (name lists) still needs human vetting; most of the corpus is tiny hand-written fragments.
- **Improv generators are hard to reason about** — even non-ML algorithms written by hand can produce output you can't explain. Tuning is slow: adjust filter mix, generate thousands of samples, collect statistics, check the feel. Maddening.
- **Some phrases fall off the map** — low-frequency gems never surfaced under any filter tuning. The fix was hardcoded salience tweaks per phrase. Could have been done programmatically, but a second automated system would have needed its own tuning. Manual tweaks worked.
- **Two failure modes on a razor's edge**:
  - **Bowls of oatmeal** — too random, lots of variability without meaning.
  - **Brutalist building problem** (Dias's coinage) — too slavish to salience; descriptions surface the model too well, planets "look naked", form follows function too visibly, all farm worlds feel identical.
- **Shaped the game** — *Voyageur* is more ambient and low-agency than originally planned. An intended subgame where players would glean trade information from descriptions died: making descriptions functional enough to guide trading also made them dry enough that players wouldn't read them. Squaring beauty-with-information is left as an exercise.
- **Transferability is limited** — Dias admits the tuning knowledge is particular to *Voyageur*'s content and mechanics.
