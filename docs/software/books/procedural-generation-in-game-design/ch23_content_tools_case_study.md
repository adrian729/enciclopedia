# Ch 23: Content Tools Case Study

## Table of Contents

- [1. Context and Goals](#1-context-and-goals)
- [2. System Overview](#2-system-overview)
- [3. Example Room Walkthrough](#3-example-room-walkthrough)

## 1. Context and Goals

- **Setting** — Rocketcat Games' room-editing tools for **Wayward Souls**, inspired by **Dungeon Crawl: Stone Soup** and **Spelunky**. The case is 2D but the patterns transfer to 3D.
- **Problem the tools solve** — supporting handcrafted moments that play nicely with a generator without becoming repetitive themselves. A previous web-based tile editor was too cumbersome once Wayward Souls accumulated many tile types, decorations, monsters, and entities.
- **Tooling goals**:
  - **Easy visualization** — anyone on the team can use the editor; a designer roughs in combat/exploration geometry, an artist reopens it for a visual pass. Far less cumbersome than typing tiles in ASCII text files.
  - **Conditional elements** — modifications can depend on other modifications. Nested random chances (e.g., 50% pillar, then a further chance for decorations and a torch on its front) build modular combinatorial possibilities.
  - **Additive and subtractive geometry** — random or conditional changes can both add features (doors, passageways) and remove them (cut chunks from walls), so a single room reads differently across visits.
  - **Easy further scripting** — dialogue triggers, doors that open or close on entry, ambush encounters, cut scenes.
  - **Easy to learn** — layered image files plus a parser are quicker for new designers to pick up than complex text formats.
- **Final shipping pattern** — Wayward Souls used handcrafted rooms with procedural short hallways. The follow-up game attaches the same modular rooms to more purely code-generated areas, mixing freeform generated space with varied handcrafted set pieces.

## 2. System Overview

- **Image-as-map representation** — every pixel of a map image is a tile; every color is a tile type; a separate **palette file** maps colors to specific tiles. Authoring tool: Photoshop or GIMP.
- **PSD pipeline** — a layered PSD is run through a web-based parser that converts each graphic layer into tile data, stored in an SQLite database on the server. The data is then instantly accessible in test builds for all developers and testers.
- **Layer names as scripting** — each layer's name encodes the conditionals that control whether and how its pixels are drawn into the map. Multiple compatible directives can live on one layer:
  - Mark layer pixels as **entities** rather than tiles — a specific monster, breakable furniture, torch, door, or large art asset.
  - Set the layer's **percentage chance** to spawn.
  - Group layers by a shared **pick-from-one** name; the game picks exactly one layer from the group. Multiple group names allow one pick per group.
  - **Associate** a layer with another so it only rolls if the parent rolled (e.g., 50% torch only on a wall that itself spawned at 50%).
  - Set pixels as **invisible triggers** that call a scripted function when the player steps on them — close all doors, spawn enemy waves until cleared, etc.

## 3. Example Room Walkthrough

- **Step 1 — Geometry** — a plain square base layer drawn under everything. Light center pixels mark possible item spawns; corner pixels mark larger breakable decorations; darker pixels mark walkable, breakable-in-combat objects.
- **Step 2 — Entry** — a conditional layer that fires only if a hallway connects from the east; it draws a door, decoration spawns, indents part of the wall, and creates a shallow alcove in the top right.
- **Step 3a — Random elements (variant A)** — the game evaluates a pick-from-one group that may add pillars; the chosen branch drops three large pillars into the room.
- **Step 3b — Random elements (variant B)** — the same room with a different pick-from-one branch chosen: different decorations spawn and a new west door spawn appears above the previous one.
- **Step 4 — AI** — monsters are added by the game from parameters tied to dungeon area and floor; a second roll of conditionals on the same room produces a different layout. The same authored room can recur across a level and still play differently. To strictly avoid duplicates, push the rolled conditional layers onto a stack so the same combination is not used twice.
- **Generalization** — the same layer-driven, conditional, pick-from-one pipeline can decorate any code-generated area with anything the game supports, letting designers add a large variety of interesting set pieces to otherwise procedural levels.
