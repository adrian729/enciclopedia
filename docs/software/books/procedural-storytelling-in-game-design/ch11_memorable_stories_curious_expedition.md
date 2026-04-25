# Ch 11: Memorable Stories from Simple Rules in Curious Expedition

## Table of Contents

- [1. The Game](#1-the-game)
- [2. Three Layers of Abstraction](#2-three-layers-of-abstraction)
- [3. One Event, Many Interpretations](#3-one-event-many-interpretations)
- [4. Apples in NetHack — Suspension of Disbelief](#4-apples-in-nethack--suspension-of-disbelief)
- [5. Emergent Story Arcs](#5-emergent-story-arcs)

## 1. The Game

- **The Curious Expedition** — Maschinen-Mensch debut (Berlin, 2014). Gather Victorian-era party members and supplies, explore uncharted Perlin-generated terrain, plan routes turn by turn across a slowly uncovered map. Each tile = a day; legs take weeks. Stories of triumph, hubris, exploitation, and death.
- **Diary screen** — procedural text scenes with multiple-choice actions, usually compromises among scarce resources, tense character dynamics, and questionable morals.

## 2. Three Layers of Abstraction

- **World layer** — the diary triggers from point-of-interest interactions (villages, missions, shrines, pyramids, merchants, forsaken camps) or from catastrophic checks per turn (wounds infected, sickness, running out of **sanity** — the trek's main resource). Some events freeze the trek; some defer until arrival at a destination to avoid confusing interruption.
- **Event layer** — declarative text syntax. A minimal event:

```
{ id: evt-basic-example
  sanity: +20
  text: I suddenly felt better. }
```

Events can reference other events (like a cookbook of ingredients). The `evt-nightRest-sanityLow` event picks one of ~50 sub-events that meets its requirements (`reqSanity: 20..50`) and runs it. `charEffects` finds *N* trek members matching tags (`+humanoid -special`) and substitutes `$name`, `$he`, etc. into the text — *"A discussion between Richard Wellington and Akulta grew into an argument"*, with per-character action buttons *"Arrest Richard Wellington" / "Arrest Akulta"*.

- **Sentence layer** — text supports inline word randomisation:

```
"[He|She] suggested that we should set up camp here. I [hated|agreed with] the idea.
 We would stay here [for now|until I felt like moving on again]."
```

- **Avoid synonym-only variation** — synonyms balloon localisation work without enriching events. Tonal or contradictory variations (glad vs. angry about the same decision) are more memorable so long as they don't negate the sentence's point.

## 3. One Event, Many Interpretations

- **The "trek member falls in love with a villager" event** — players retell this one most. Different trek members + pronoun variations produced wildly different tones:
  - a British soldier falling in love with a woman from the tribe
  - a bearded sailor falling in love with a man of the tribe
  - a missionary falling in love with a woman of the tribe
- **Same mechanics, different taboos** — the system touched different emotional registers by permutation, making each recounting feel personal.

## 4. Apples in NetHack — Suspension of Disbelief

- **Apples killing players in NetHack** — hundreds of deaths, choking on apples. Djemili assumed the code must be elaborate; looking up the 1987 source, the relevant logic was a handful of lines:

```c
if (food) {
  You("choke over your %s.", foodword(food));
  if (food->oclass == COIN_CLASS) {
    killer = "a very rich meal";
  } else { ...
```

- **Players co-produce the simulation** — they fill in depth that isn't there. As long as the system stays consistent, players happily cooperate in making the world believable. *Curious Expedition* relies on the same gift.

## 5. Emergent Story Arcs

- **Sample sequence** — low sanity → coca leaves → Marie-Elise Alexandre has a psychotic episode and gains the superstitious trait → at night, a vulture bothers her (event only fires because of the trait) → player refuses to waste ammo → Marie-Elise loses loyalty, is marked angry → later she starts a fight with the scout (triggered by her angry mood) → the player chastises her → she runs off into the jungle → many days later, she steps out of the woods with food and asks to rejoin.
- **No "storyline" system** — no component was dedicated to long-term arcs. Each event simply triggered when its requirements matched and its effects enabled or disabled others. A shared vocabulary of hooks (traits, moods, resources, character pools) was enough to produce consistent, interactive arcs.
- **Not every chain is memorable** — characters die, leave, or ignore threads; players are never forced to see a thread through. When a chain does land, it feels uniquely personal, and that is where procedural storytelling feels truly magical.
