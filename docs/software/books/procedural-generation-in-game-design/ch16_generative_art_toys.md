# Ch 16: Generative Art Toys

## Table of Contents

- [1. Why Art Toys](#1-why-art-toys)
- [2. Experience and Modes of Operation](#2-experience-and-modes-of-operation)
- [3. Trading Control for Power](#3-trading-control-for-power)
- [4. Kasparov's Centaur](#4-kasparovs-centaur)
- [5. Design Pattern: Inputs, Transformations, Rendering](#5-design-pattern-inputs-transformations-rendering)
- [6. Beyond the Generator: Judgment, Sharing, Curation](#6-beyond-the-generator-judgment-sharing-curation)

## 1. Why Art Toys

- **Generative art toys** — digital descendants of pottery wheels, Spirographs, Mad Libs, spin art, paper marbling, and tie-dye: tools that let everyday people make interesting artworks via surprising and emergent results from simple choices.
- **Why in a PCG book** — art toys reuse PCG techniques but lack gameplay restrictions, giving more freedom and less worry about gameplay issues. They are also a sandbox for trying generative methods (L-systems for surreal flowers, particle techniques from Spore, context-free grammars for music/poetry, flocking for choreography).
- **Generator as the star** — in games, PCG is invisible (AI movement) or background (skies, trees) and serves the gameplay. In an art toy, the user interacts directly with the generator, controlling, curating, or exploring it; the generator becomes the center of attention.

## 2. Experience and Modes of Operation

- **Autotelic activity** — creativity practiced as an end in itself (vs. external goals). Wellbeing benefits aren't correlated to skill, only engagement, so art toys must engage the user regardless of talent.
- **Three modes of independence** — an art toy can feel like:

| Mode | Role of the toy |
|---|---|
| **Tool** | Magnifies or constrains user input so the output is bigger, more complex, better made than their actual skill |
| **Collaborator** | Provides inspiration, suggests directions and modifications, encourages the uninspired user |
| **Artist** | Generates content on its own; the user becomes guide and curator, exploring the possibility space and sharing favorites |

- **Chaotic surfing** — sometimes users abandon control entirely for the fun of riding a generative wave (e.g., Brough and McClure's *Become a Great Artist in Just 10 Seconds*).
- **Ownership matters** — users should feel they personally own the artifacts, whether through skill (with the generator's help) or taste (in selecting from output).
- **Minecraft effect** — when users feel creative and powerful they share their work, symbiotically promoting the app; "I'm really good at this" beats "this generator is good at this."

## 3. Trading Control for Power

- **Trading control for power** — the central idea of an art toy: the user gives up some control and gains capability they couldn't otherwise reach.
- **Pro tools (Photoshop, Maya) require total control** — they assume professional users with a specific output in mind; automated generators aren't customizable enough for that workflow.
- **Autotelic users will cede control** — as long as the generator magnifies or streamlines their creative activity, casual creators are happy to trade away control.
- **Pen vs. Spirograph** — a pen offers complete control over a huge possibility space mostly full of ugly scribbles; the Spirograph constrains motion to spiraling loops via gear sockets, shrinking the space but filling it with universally satisfying mandala geometry. Pottery wheels do the same in 3D, automating one rotational dimension to leave in–out and up–down.

## 4. Kasparov's Centaur

- **Centaur chess (Isaac Karth sidebar)** — after losing to Deep Blue, Kasparov played the first "advanced chess" match (1998, vs. Topalov) where each player was paired with a computer. Human–machine teams outperformed either alone; rote work is automated, freeing the human to express themselves.
- **Strangethink's Joy Exhibition** — a VR gallery whose only painting tool is a collection of billions of procedurally generated paint guns, each with a distinct weird pattern: a microcosm of PCG and centaur art.
- **Photography parallel** — generative tools echo early photography's effect on painting, which embraced Impressionism for what cameras couldn't capture; loose impressionist brushstrokes happen to work especially well for neural style transfer.

## 5. Design Pattern: Inputs, Transformations, Rendering

Art toys lack established genres, but most fit a modular pattern of **inputs**, **transformations**, **rendering**, plus optional **social/sharing** mechanics — Lego bricks that snap together into different toys.

### 5.1. Inputs

- **Pipeline width** — keyboard yields sparse binary events; mouse yields continuous (X, Y) per frame; a Leap Motion hand tracker produces 50–100 data points per sample (joints × rotations).
- **High-DOF input needs continuous feedback** — Chris Milk's *Treachery of Sanctuary* uses the user's full continuous shadow as input; raising arms extends feathered wings, fingers fan in and out at the same rate. Children grasp it instantly.
- **Pose-detection apps fail** — apps that compress rich tracking data into discrete pose events discard ~99.99% of the input and end up with the same expressiveness as a keyboard.

### 5.2. Transformations

Multiple ways to interpret hand-tracking data without discarding information:

| Layer | What it captures | Example use |
|---|---|---|
| **Points and rotations** | Joint locations + 3D pointing vectors per finger | Build geometry aligned along bones, extending outward (*Treachery of Sanctuary*) |
| **Connectivity and meshes** | Edges between joints; transient edges between fingertips; cross-hand Voronoi map | A procedurally generated cat's cradle of edges |
| **Gestural curves** | Animation curves of joint motion through space | Google's *Tilt Brush* records strokes as curves and reskins them |
| **Forces and acceleration** | Velocity vectors → acceleration → implicit force; flex/stretch as stress | Direction paint falls from a hand; force applied to particles, agents, or pixel buffers |

### 5.3. Rendering

- **Canvas and mark** — the canvas is whatever records what will render (pixel buffer, scene graph, list of shapes). A *mark* is a semipermanent element or action that's added to the canvas and may morph, flow, or be deleted.
- **Additive vs. parametric rendering** — additive: each frame builds on the previous buffer (`final = ƒe(ƒd(ƒc(ƒb(ƒa(buffer)))))`). Parametric: every frame re-renders from scratch (`final = ƒ(a, b, c, d, e, …, initial buffer)`). The boundary is flexible: a parametric engine that doesn't clear its buffer leaves trails (Windows Solitaire win, 3D Pipes screensaver); a partially transparent overdraw rectangle yields attractively veiled fading trails.
- **Medium vs. Tilt Brush** — same input (gestural curves), different rendering models. *Oculus Medium* uses voxels (3D pixel buffer) — additive, can overwrite but not edit prior marks. *Tilt Brush* stores each stroke as a vector and renders parametrically — earlier strokes can be modified, animated, or rendered as particles or patterned ribbons.
- **DNA-string rendering** — a parametric pattern: an array of numbers (e.g., 30 floats) drives an L-system for flowers. Continuous parameter space supports evolutionary algorithms responding to user picks, lerping for animation, mapping music analyzers, or hooking a Leap Motion so each hand position generates a different flower.
- **Time as parameter** — using time as an input parameter for any continuous parametric function produces smooth animation. *Panoramical* gives the user nine 2D sliders (18 parameters) plus time (the 19th), each level a different parametric interpretation into music and 3D scene.
- **Indirect rendering** — toys aimed at casual users can sacrifice a direct input→output mapping for generativity and power. Models can also feed simulations: any graph or point set yields a Voronoi or Delaunay triangulation; *Text Rain* (Utterback and Achituv, 1999) drops projected text that puddles on user shadows.

## 6. Beyond the Generator: Judgment, Sharing, Curation

- **Judgment latency varies** — a Spore creature is judged at a glance; music, stories, or games take seconds to hours. Toys can play with judgment: *Become a Great Artist in Just 10 Seconds* asks the user to match a still life using only glitch-art keyboard filters, making automated judgment a silly metric.
- **Curation as creation** — *Picbreeder* lets users only click favorites among neural-network-generated images to "breed" new ones. Users still take pride in finding unusual artifacts and showing them off.
- **Aesthetic spectrum** — art toys range from frustrating/opaque (*Become a Great Artist*) to welcoming (*Spore Creature Creator*), intensive/controllable (*Medium*, *Tilt Brush*), uncontrolled/automated (*Picbreeder*), or meditative (*Text Rain*, *The Treachery of Sanctuary*).
