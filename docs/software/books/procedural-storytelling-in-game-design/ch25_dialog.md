# Ch 25: Dialog

## Table of Contents

- [1. The Problem](#1-the-problem)
- [2. Rules and Criteria](#2-rules-and-criteria)
- [3. Automatic Triggers and Memory](#3-automatic-triggers-and-memory)
- [4. Repartee and Complex Responses](#4-repartee-and-complex-responses)
- [5. Data-Driven Context and Usability](#5-data-driven-context-and-usability)
- [6. Data Structures and Optimisation](#6-data-structures-and-optimisation)
- [7. Authoring Tools](#7-authoring-tools)
- [8. Takeaways](#8-takeaways)

## 1. The Problem

- **Context** — *Left 4 Dead* characters call tactical information, react to teammates, and die at any time. Dialog had to pick the best line from thousands based on world state, without relying on fixed location triggers because the AI Director randomises encounters.
- **State-machine dialog explodes** — every new world fact (village destroyed, dragon freed, sword equipped) multiplies branching conditions in giant nested `if` statements. Writers end up dependent on programmers to discover available state.
- **Need** — track world state uniformly, select the best line from a big database, remember what was said. Treat dialog as a system of **general rules with increasingly specific exceptions**.

## 2. Rules and Criteria

- **Every rule** has **criteria** (facts that must be true) and a **response** (line, animation, callback).

```
rule Voc_Grenadier_CallForMedic
{
  criteria { Event=OnVocalizeKey ; LookingAt=Medic ; SpeakingCharacter=Grenadier }
  response { Grenadier_Medic_Call // "hey doc, come help me" }
}
```

- **Vocalize()** iterates rules, keeps matches, picks the one with the **most criteria** (most specific). A generic "stand on that capture point" line falls back when no A/B/C-specific rule exists.
- **Works for game events too** — reaching full charge on a special attack fires `OnFullyCharged`; the rule with the matching speaker produces the line.

## 3. Automatic Triggers and Memory

- **Tags on world objects** — a simple string field on each actor (cats tagged `cat`, barrels `barrel`). A periodic timer fires `onSee` events with the object under the character's gaze, so NPCs appear to spontaneously notice things.
- **Said-once flags** — rule callbacks set `this.SaidOnce := true` to stop repetition. Callbacks run after the line finishes.
- **Character memory** — an associative array per character that callbacks can increment. Running gags are just numbered rules:

```
rule Fred_LookingAt_Barrel_0
  criteria { Event=onSee; LookingAt=Barrel; SpeakingCharacter=Fred; speaker.BarrelsSeen=0 }
  response "I wonder what's in this barrel."
  callback { speaker.BarrelsSeen += 1 }

rule Fred_LookingAt_Barrel_1
  response "I heard these barrels store vast quantities of marinara sauce."

rule Fred_LookingAt_Barrel_2
  response "All this sauce and no pasta in sight."
```

- **Global state** — the world itself has a context dictionary (`global.DragonFreed=true`) so rules can test quest state, weather, etc.

## 4. Repartee and Complex Responses

- **Send follow-up events** — a callback calls `SendFollowupEvent(target:Jane, event:onReply, PreviousLine:Fred_Comment_Barrel1)`. Jane's rulebook matches and she replies, whose callback fires another event back at Fred. Stringing lines together is just adding rules; `target:Self` lets a character split a monologue.
- **target:Anyone** — broadcast a reply request to everyone nearby; the most-specific rule wins, so Jane, Pierre, or Kim can answer depending on the moment.
- **Complex responses** — the `response` field can be a list with replay policies (random, round-robin with reset, say-once). Round-robin is perfect for stealth barks where five `OnSawPlayer` lines will inevitably be cycled.

## 5. Data-Driven Context and Usability

- **Writers invent context keys** — a callback like `speaker.CatsSeen += 1` creates the key on demand; writers don't need programmer support to build new running gags.
- **Why the flat-dictionary model helps writers** — a naive code approach hides state across dozens of classes with different owners. A flat merged dictionary (function params + speaker state + memory + global state) is discoverable by key lookup, enables serendipity (a `TotalFruitPurchased` counter for one vendor can suddenly be used by a different character two towns over), and self-documents when you print it out. The *Left 4 Dead* writers used this diagnostic as their primary index.

## 6. Data Structures and Optimisation

- **Definitions**:
  - **Context** — a single key-value pair (`PlayerHealth:72`). Prefer numeric values for performance; intern strings to symbols or hashes.
  - **Query** — a merged vector of contexts built at lookup time.
  - **Criterion** — a comparison on a context (`PlayerHealth > 50`).
  - **Rule** — a list of criteria; most-criteria wins when multiple match.
  - **Response** — line/animation to play + writebacks to character/world memory + follow-up events.
- **Algorithm**: build query → test every rule → pick highest-scoring match.
- **Optimisations**:
  1. Sort criteria within each rule and contexts within each query by key; march two pointers in parallel, reject early.
  2. Don't literally merge the source vectors; keep function/speaker/memory/global separate and walk them in parallel.
  3. Partition the rules database hierarchically on a common criterion (e.g. `SpeakingCharacter`) — a nested table per speaker massively narrows the search.
  4. Level-scope rules — store per-level rules inside the level asset; load/evict with the level.
  5. Sort rules within each partition by number of criteria, descending; stop testing once a match with more criteria than any remaining rule is found.

## 7. Authoring Tools

- **Direct script** — simplest, unwieldy past a few hundred rules.
- **Spreadsheets** — familiar, sortable, easy to add rows. Downside: one column per possible criterion bloats quickly; context writebacks are awkward.
- **Relational database front-end** — Campo Santo's *Firewatch* tool unified rules, localisation status, VO recording status, and content files. Big investment. Criterion storage is awkward either way (many columns or a free-form TEXT field that's hard to search).
- **Rulebook-style natural language** — Inform 7's syntax for increasingly specific exceptions: *"A cat behavior rule when the cat can touch the catnip: say 'The cat frolics with the catnip…'"*. Unwieldy at scale but the idea adapts.
- **Always ship debug visualisation** — print every query with origins, all rules tested, and pass/fail reasons. Saves hours.

## 8. Takeaways

1. Keep it simple. The whole apparatus is a rule-matching engine (a production system).
2. Queries are flat key-value dictionaries.
3. Throw *every* available fact into every query. New rules for new specific circumstances shouldn't need programmer support.
4. Responses can trigger follow-up queries on other characters → back-and-forth conversation.
5. Responses can write back to character or global memory.
6. Context names are arbitrary — writers invent new ones by writing to unused keys.
7. Rules are additive — start with general `OnBark` fallbacks and layer specific exceptions.
8. Because rules are additive, new characters, scenarios, and quests can be loaded purely as data.

Most of all: keep it simple.
