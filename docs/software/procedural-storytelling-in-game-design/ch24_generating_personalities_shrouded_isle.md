# Ch 24: Generating Personalities in The Shrouded Isle

## Table of Contents

- [1. The Game](#1-the-game)
- [2. Character Generation](#2-character-generation)
- [3. Interaction and Moral Friction](#3-interaction-and-moral-friction)
- [4. Trait Modification — Events, Contagions, Purification](#4-trait-modification--events-contagions-purification)
- [5. Analysis and Shortcomings](#5-analysis-and-shortcomings)

## 1. The Game

- **The Shrouded Isle** — human-sacrifice cult simulator. Player is the high priest of a small island village preparing for a slumbering dark god's prophesied awakening. Core gameplay: maintain villagers' faith by investigating, manipulating, and killing sinners.
- **Design thesis** — minimal, trait-based personality generation creates flawed, believable characters whose behaviour conflicts with the player's goals, so choices become genuinely difficult.
- **Origin** — Ludum Dare 33 entry (August 2015, theme "You are the monster"). The team wanted to explore why someone chooses to become an *administrative monster*, ostensibly serving the greater good while harming their community. Full release August 2017; free *Sunken Sins* expansion December 2017.
- **Two challenges** — humanise the townspeople (not stat sheets), and give the player compelling reasons to make harsh decisions. The team picked systemic generation over scripted content so every playthrough forces fresh engagement.

## 2. Character Generation

Three layered elements: **family**, **traits**, **aesthetics**.

- **Family** — every character belongs to one of five Great Houses: **Kegnni, Iosefka, Cadwell, Efferson, Blackborn**. Each house has ~6 members (30 townspeople total), with at least one elderly male and elderly female (parents) and 2–5 younger members (children). Family relationships are implied, not explicit. No new characters arrive during the playthrough, giving the cast permanence and history.
- **House specialties** — each House is responsible for one of the cult's five values:

| House | Value | Ritual |
|---|---|---|
| Kegnni | Ignorance | Burn Books |
| Iosefka | Fervour | Build Monument |
| Cadwell | Discipline | Confiscate Goods |
| Efferson | Penitence | Flagellate Sinners |
| Blackborn | Obedience | Investigate Heresy |

  When a character's personal traits happen to align with the family specialty, they become either the favoured child or the black sheep.

- **Traits** — each character is assigned one **virtue** (improves a cult value) and one **vice** (impedes it). The generator avoids duplicates so trait pairs are usually unique.
- **Severity** — minor (±10) or major (±30). Any combination is allowed; a Minor Virtue + Major Vice character may feel unbalanced individually, but major traits are limited at the town level. Lopsided characters are *more* visible, which accentuates personality.
- **Aesthetics** — unique name + unique portrait per character. No gameplay impact, but essential: duplicate names or portraits break immersion. Players extrapolate personality from looks alone (picking advisors because they look attractive, sacrificing those who look maniacal).

## 3. Interaction and Moral Friction

Five values × five Great Houses. Seasons break into **Town**, **Work**, **Sacrifice** phases.

- **Town phase** — investigate characters to reveal traits; appoint one advisor per family.
- **Work phase** — pick 1–3 advisors to perform rituals. Their virtues/vices shift cult values alongside the ritual.
- **Sacrifice phase** — ritual-kill one advisor. The impact inverts the Work phase — worse vice = greater benefit from the sacrifice, better virtue = worse loss. Sacrificing the same family repeatedly stacks a massive opinion penalty that risks revolt.
- **Trait reveal states** — unrevealed, partially revealed, fully revealed. The actual effect on the town is identical regardless; what changes is the player's *trust*. Players assume hidden vices are benign; when a Major Vice surfaces, they react with a sense of betrayal as if the character chose to sabotage them.
- **Random Work-phase outcomes** — 15 % Great (1.5×) / 70 % Average (1×) / 15 % Poor (0.5×). The high frequency creates extrapolation gameplay (players overuse "pet advisors" who are merely lucky, sacrifice underperformers in anger). Not punishing enough early to end a run, but in the late game a Poor outcome can drop a value below its critical threshold and cascade.
- **Family opinions system** — using an advisor improves the family's opinion; ignoring them lowers it. Only three of five families can be used each month, so two or more are always scorned. Players are forced to use each family at least once per season even if the advisors' traits are detrimental — ensuring deeply flawed characters get screen time.
- **Sacrifice opinion penalty** — families react badly to members being killed. Inquiries mitigate the penalty; repeated targeting of the same family doesn't. Skilled players may sacrifice a Minor Vice (or even a Major Virtue) for political stability.

## 4. Trait Modification — Events, Contagions, Purification

Players expected some dynamism beyond the virtue/vice static pair.

- **Random events (original release)** — letters or visits with political/moral choices. Some choices replaced a trait with another, enabling arcs (a sceptical scholar regaining faith, someone overcoming the sacrifice of a loved one to become more resilient). Event *chains* were fragile (any character death broke them), so single events were the workhorse.
- **Contagions (Sunken Sins expansion)** — in the first autumn, one character becomes the carrier of a **spiritual contagion** that replaces their virtue with a partially-discovered trait reducing a cult value. Every following season it spreads within the family or a new contagion spawns elsewhere. Players blame the "patient zero" just as they blame underperforming Work-phase advisors.
- **Purification Tower** — confines up to three characters per Town phase for a full-season purification in seawater. Cure rate depends on how much the player has inquired about the contagion (100 % if fully revealed). Failure drowns the character, angering the family.
  - **Afflicted cure table** — fully revealed: 100 % cure. Partially revealed or unrevealed: 40 % cure / 40 % vice worsening / 20 % death.
  - **Unafflicted unintended use** — random virtue/vice upgrade (40 %/40 %/20 % drown for Minor Virtues), creating more surprise opportunities.
  - **Major Virtues → Awoken** — 100 % transformation into mute mushroom-like mutants blessed by Chernobog. Portrait swaps, virtue replaced with *Awoken* (stat-less). To unlock the Sunken Sins secret ending, every surviving townsperson must become Awoken. Narratively: loss of personality via forced conformity. Mechanically similar to victory-point cards in *Dominion* — necessary for an ending, but early collection constrains gameplay.

## 5. Analysis and Shortcomings

- **Moral quandaries decayed quickly** — players embraced the tyrant role within one or two seasons. Letting players skip a Sacrifice proved anticlimactic and hard to balance thematically (punishment had to come from cult values or family opinions, which are worldly, not divine). Cut in favour of forcing the *who* of the sacrifice rather than *whether*.
- **Choice paralysis at the start** — 30 characters is too many to connect with in the first seasons. A gradual arrival system was rejected because it would raise awkward worldbuilding questions (*"Do other communities exist?"*, *"Why didn't I know about these children?"*). The shrinking demographic contributes the apocalyptic feel, which is worth the cost in this setting.
- **What worked** — families give social context; unique virtue/vice pairs give distinct personalities; unique name + portrait give aesthetic identity. Random Work outcomes and hidden traits let characters surprise or betray expectations. The family-opinions system forces engagement with flawed characters; the Sacrifice phase makes you re-examine each one through both personal and political lenses. Combined, these systems successfully turn the player into an administrative monster through their own generated circumstances.
