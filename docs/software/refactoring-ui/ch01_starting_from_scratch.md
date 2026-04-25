# Ch 1: Starting from Scratch

## Table of Contents

- [1. Start with a feature, not a layout](#1-start-with-a-feature-not-a-layout)
- [2. Work in cycles, not all at once](#2-work-in-cycles-not-all-at-once)
- [3. Hold the color; defer the details](#3-hold-the-color-defer-the-details)
- [4. Choose a personality](#4-choose-a-personality)
- [5. Limit your choices with systems](#5-limit-your-choices-with-systems)

## 1. Start with a feature, not a layout

- **Apps are collections of features** — "designing the app" (nav bar, sidebar, logo placement) is designing the shell, and you can't make good shell decisions before you've designed some real features.
- **Pick one piece of functionality and start there** — e.g., for a flight-booking service, start with "searching for a flight": fields for departure/destination/dates and a search button. Build the shell around features later, once you actually know what it has to hold.

## 2. Work in cycles, not all at once

- **Don't design every feature up front** — trying to resolve every edge case in the abstract (2000 contacts, overlapping calendar events, form error placements) leads to frustration. You lack the information to decide in advance.
- **Short design → build cycles** — design a simple version of the next feature, make it real, iterate on the working thing, then move on. Real interfaces expose problems imagination can't.
- **Be a pessimist about scope** — don't imply functionality you aren't ready to build. A comment system without attachments ships; a comment system blocked on attachments doesn't. Design the smallest useful version first and treat "nice-to-haves" as later work.

## 3. Hold the color; defer the details

- **Low fidelity first** — in early stages, don't get hung up on typefaces, shadows, or icons. Jason Fried of Basecamp sketches on paper with a thick Sharpie because the tool itself makes obsessing over detail impossible.
- **Design in grayscale** — resist introducing color right away. Without color, you're forced to use **spacing, contrast, and size** to carry the hierarchy, which produces a stronger interface that's easier to enhance with color later.
- **Don't over-invest in sketches** — wireframes and sketches are disposable. Users can't do anything with static mockups; use them to explore, then leave them behind.

## 4. Choose a personality

Every design communicates a personality (secure/professional, fun/playful, elegant, etc.). Personality feels abstract but is driven by concrete, controllable factors:

| Factor | How it shapes personality |
|---|---|
| **Font choice** | Serif → elegant/classic; rounded sans serif → playful; neutral sans serif → plain or neutral base for other elements to carry the feel |
| **Color** | Blue reads safe and familiar; gold reads expensive/sophisticated; pink reads fun, less serious. Skip pure color psychology — go with what looks right for the product |
| **Border radius** | Small radius is neutral; large radius feels playful; no radius feels serious/formal. Stay consistent — mixing square and rounded corners almost always looks worse than picking one |
| **Language** | Words are everywhere in a UI. A formal tone feels official; casual, friendlier copy feels friendlier. Word choice matters as much as color or type |

- **How to decide the personality** — usually gut feel. If stuck, look at other sites your target users already use and match the register (serious vs. playful). Don't copy direct competitors; you don't want to look like a second-rate version of them.

## 5. Limit your choices with systems

- **Unlimited options = paralysis** — 12px vs. 13px, 10% vs. 15% shadow opacity, 24px vs. 25px avatar. With no constraints there's always more than one right answer, so decisions are torture.
- **Define systems in advance** — instead of hand-picking from a limitless pool each time, choose from a predefined set (e.g., 8–10 blue shades, a restrictive type scale). Do the hard work once up front, not every time you build UI.
- **Process-of-elimination picking** — when your options are constrained (say icon sizes of 12/16/24/32px), pick a guess and compare to the values on either side. Two will look obviously wrong; keep sliding until the middle option is clearly best.
- **Systematize everything** — font size, font weight, line height, color, margin, padding, width, height, box shadow, border radius, border width, opacity. You don't have to define them all up front — just work with a system-focused mindset and avoid making the same minor decision twice.
