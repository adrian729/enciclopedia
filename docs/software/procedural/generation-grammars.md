# Grammars & Systems: L-systems, CA, Sampling

> *Generation throughline.* Where [noise](software/procedural/generation-noise.md) generates *continuous fields*, this page generates *structure* by applying **local rules** repeatedly: rewriting grammars (L-systems) for recursive forms like plants, cellular automata for organic grids like caves, and sampling for natural scatter. All are still pure functions of a seed. This is a primer; for design-level treatment see [Procedural Generation in Game Design](software/books/procedural-generation-in-game-design/book_summary.md). Examples use Bevy `0.18`.

## Table of Contents

- [1. Generation by Rules, Not Fields](#1-generation-by-rules-not-fields)
- [2. L-systems](#2-l-systems)
  - [2.1. Axiom, Rules, Iteration](#21-axiom-rules-iteration)
  - [2.2. Turtle Interpretation](#22-turtle-interpretation)
  - [2.3. Worked Example: An L-system Plant](#23-worked-example-an-l-system-plant)
- [3. Cellular Automata](#3-cellular-automata)
  - [3.1. The Cave Rule](#31-the-cave-rule)
  - [3.2. Worked Example: A CA Cave](#32-worked-example-a-ca-cave)
- [4. Poisson-Disk Sampling](#4-poisson-disk-sampling)
- [5. Wave Function Collapse](#5-wave-function-collapse)
- [Sources](#sources)

## 1. Generation by Rules, Not Fields

Noise answers "what is the value *at this point*?". Rule-based generation answers "what happens when I apply *this local rule* everywhere, repeatedly?". The structure emerges from iteration: a grammar rewrites symbols into longer strings, a cellular automaton rewrites cells from their neighbours, a sampler places points subject to a spacing rule. These produce the *recursive* and *organic-but-structured* content noise cannot.

## 2. L-systems

A **Lindenmayer system** models growth by string rewriting. It is the canonical way to generate plants, trees, and other recursive, self-similar forms.

### 2.1. Axiom, Rules, Iteration

Three ingredients:

- **Axiom** — the starting string, e.g. `"F"`.
- **Production rules** — replacements applied to *every* matching symbol simultaneously, e.g. `F → "FF+[+F-F-F]-[-F+F+F]"`.
- **Iterations** — how many times to apply the rules. Each pass replaces every symbol, so the string grows exponentially; 3-5 iterations is usually enough.

```rust
/// Apply the production rules to every symbol, `iterations` times.
fn expand(axiom: &str, rules: &[(char, &str)], iterations: usize) -> String {
    let mut s = axiom.to_string();
    for _ in 0..iterations {
        let mut next = String::with_capacity(s.len() * 2);
        for c in s.chars() {
            match rules.iter().find(|(sym, _)| *sym == c) {
                Some((_, replacement)) => next.push_str(replacement),
                None => next.push(c), // symbols with no rule pass through
            }
        }
        s = next;
    }
    s
}
```

### 2.2. Turtle Interpretation

The expanded string is drawn by a **turtle** — a pen with a position and a heading that obeys each symbol:

| Symbol | Action |
|---|---|
| `F` | Move forward one step, drawing a segment |
| `+` | Turn left by a fixed angle |
| `-` | Turn right by a fixed angle |
| `[` | Push (save) the current position and heading |
| `]` | Pop (restore) the saved position and heading |

The `[` / `]` brackets are what make *branches*: push before a branch, draw it, pop back to the trunk to draw the next. They form a stack — exactly the call stack of a recursive tree.

### 2.3. Worked Example: An L-system Plant

A complete Bevy `0.18` program. It expands a classic bushy-plant grammar and draws it with gizmos.

```rust
use bevy::prelude::*;
use std::f32::consts::FRAC_PI_2;

#[derive(Resource)]
struct Plant(Vec<(Vec2, Vec2)>); // line segments

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .add_systems(Startup, setup)
        .add_systems(Update, draw)
        .run();
}

fn setup(mut commands: Commands) {
    commands.spawn(Camera2d);
    let s = expand("F", &[('F', "FF+[+F-F-F]-[-F+F+F]")], 3);
    let segments = interpret(&s, 6.0, 0.45); // step length, turn angle (radians)
    commands.insert_resource(Plant(segments));
}

/// Walk the string with a turtle, emitting one segment per `F`.
fn interpret(s: &str, step: f32, angle: f32) -> Vec<(Vec2, Vec2)> {
    let mut pos = Vec2::new(0.0, -300.0); // start near the bottom
    let mut heading = FRAC_PI_2;          // pointing up
    let mut stack: Vec<(Vec2, f32)> = Vec::new();
    let mut segments = Vec::new();
    for c in s.chars() {
        match c {
            'F' => {
                let next = pos + Vec2::from_angle(heading) * step;
                segments.push((pos, next));
                pos = next;
            }
            '+' => heading += angle,
            '-' => heading -= angle,
            '[' => stack.push((pos, heading)),
            ']' => {
                if let Some((p, h)) = stack.pop() {
                    pos = p;
                    heading = h;
                }
            }
            _ => {}
        }
    }
    segments
}

fn draw(mut gizmos: Gizmos, plant: Res<Plant>) {
    let green = Color::srgb(0.3, 0.6, 0.25);
    for &(a, b) in &plant.0 {
        gizmos.line_2d(a, b, green);
    }
}
```

The plant is fully determined by the grammar, the angle, and the step — change `0.45` radians to `0.6` and the plant fans wider; add a fourth iteration for denser foliage (at exponential cost). Real plant generators add randomness per rule (*stochastic* L-systems) so every plant differs while sharing a species' grammar.

## 3. Cellular Automata

A **cellular automaton** evolves a grid: every cell's next state is a function of its current neighbourhood, applied to all cells at once. A handful of iterations of one simple rule turns random noise into coherent, cave-like caverns.

### 3.1. The Cave Rule

Start with each cell randomly a wall (≈ 45% chance) or floor. Then repeatedly apply the **"4-5 rule"**: a wall stays a wall if **4 or more** of its 8 neighbours are walls, and a floor becomes one at **5 or more**. The two cases collapse into a single test — a cell is a wall next step iff its 3×3 block, **itself included**, holds 5 or more walls (off-grid counts as wall, so the map stays enclosed):

\[ c'_{x,y} = \big[\, \#\{\text{walls in the } 3 \times 3 \text{ block at } (x,y)\} \ge 5 \,\big] \]

Each pass erodes lonely walls and fills isolated holes; after 4-6 passes the noise has organised into smooth, connected caverns. It is the same "project toward a local rule, iterate" pattern as the relaxation loops in the animation pages — here on a discrete grid.

### 3.2. Worked Example: A CA Cave

A complete program. It generates the grid deterministically (seeded `ChaCha8Rng`), bakes wall/floor to an `Image`, and shows it scaled up as a sprite. Add `rand = "0.9"` and `rand_chacha = "0.9"` to `Cargo.toml`.

```rust
use bevy::asset::RenderAssetUsages;
use bevy::image::Image;
use bevy::prelude::*;
use bevy::render::render_resource::{Extent3d, TextureDimension, TextureFormat};
use rand::{Rng, SeedableRng};
use rand_chacha::ChaCha8Rng;

const W: usize = 120;
const H: usize = 80;

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .add_systems(Startup, setup)
        .run();
}

fn setup(mut commands: Commands, mut images: ResMut<Assets<Image>>) {
    commands.spawn(Camera2d);

    let cells = generate_cave(7, 5); // seed, smoothing passes
    let mut data = vec![0u8; W * H * 4];
    for (i, &wall) in cells.iter().enumerate() {
        let rgba = if wall { [30, 30, 40, 255] } else { [182, 170, 150, 255] };
        data[i * 4..i * 4 + 4].copy_from_slice(&rgba);
    }

    let image = Image::new(
        Extent3d { width: W as u32, height: H as u32, depth_or_array_layers: 1 },
        TextureDimension::D2,
        data,
        TextureFormat::Rgba8UnormSrgb,
        RenderAssetUsages::RENDER_WORLD,
    );
    commands.spawn((
        Sprite::from_image(images.add(image)),
        Transform::from_scale(Vec3::splat(8.0)),
    ));
}

fn generate_cave(seed: u64, steps: usize) -> Vec<bool> {
    let mut rng = ChaCha8Rng::seed_from_u64(seed);
    let mut cells: Vec<bool> = (0..W * H).map(|_| rng.random_bool(0.45)).collect();
    for _ in 0..steps {
        let prev = cells.clone();
        for y in 0..H {
            for x in 0..W {
                cells[y * W + x] = walls_3x3(&prev, x, y) >= 5;
            }
        }
    }
    cells
}

/// Walls in the 3x3 block centred on (x, y) — the cell itself included.
fn walls_3x3(cells: &[bool], x: usize, y: usize) -> usize {
    let mut count = 0;
    for dy in -1i32..=1 {
        for dx in -1i32..=1 {
            let (nx, ny) = (x as i32 + dx, y as i32 + dy);
            // Off-grid counts as wall, so the cavern stays sealed.
            let is_wall = nx < 0
                || ny < 0
                || nx >= W as i32
                || ny >= H as i32
                || cells[ny as usize * W + nx as usize];
            count += is_wall as usize;
        }
    }
    count
}
```

Reseed for a new cave; raise the fill probability for denser rock; raise the pass count for smoother walls. A common follow-up is a flood fill to keep only the largest connected cavern (discarding sealed pockets).

## 4. Poisson-Disk Sampling

To scatter trees, rocks, or stars so they look *natural* — random but never clumped or gridded — you want points with a guaranteed **minimum spacing** \( r \). White noise clumps; a grid looks artificial. **Bridson's algorithm** produces such "blue-noise" sampling in linear time using a background grid:

1. Grid cells of side \( r/\sqrt{2} \), so each cell holds at most one sample (fast neighbour lookup).
2. Place a random first point; put it on an *active list*.
3. While the active list is non-empty: pick a random active point and try up to \( k \approx 30 \) candidate points in the annulus \( [r, 2r] \) around it. Accept the first candidate that is at least \( r \) from all existing samples (checked against the few nearby grid cells). If none of the \( k \) candidates qualify, remove the point from the active list.

```text
grid[cell] = sample index;  active = [first point]
while active not empty:
    p = random point from active
    for _ in 0..k:
        c = p + random vector in annulus [r, 2r]
        if c in bounds and no sample within r (check neighbouring grid cells):
            add c to samples, grid, and active;  break
    else:
        remove p from active        // no room left around p
```

The result fills space evenly with organic, grid-free spacing — the standard tool for object placement.

## 5. Wave Function Collapse

**Wave Function Collapse (WFC)** generates tile-based content (dungeon layouts, textures, towns) that locally resembles a small example. Each grid cell starts in a *superposition* of all possible tiles; the algorithm repeatedly **collapses** the lowest-entropy cell (fewest remaining options) to a single tile chosen at random, then **propagates** the adjacency constraints (which tiles may sit next to which) to its neighbours, shrinking their option sets. Repeat until every cell is collapsed.

It produces strikingly coherent results from a single example tileset, but it is heavier than the techniques above and can paint itself into a contradiction (a cell with zero valid options), requiring restart or backtracking. Treat it as a powerful specialist tool — reach for an existing crate or the reference implementations rather than writing it from scratch on a first pass.

## Sources

- Przemysław Prusinkiewicz & Aristid Lindenmayer — *The Algorithmic Beauty of Plants* (L-systems and turtle interpretation).
- Robert Bridson — *Fast Poisson Disk Sampling in Arbitrary Dimensions*.
- Maxim Gumin — *Wave Function Collapse* (the original algorithm and tilesets).
- [Procedural Generation in Game Design](software/books/procedural-generation-in-game-design/book_summary.md) and [Procedural Storytelling in Game Design](software/books/procedural-storytelling-in-game-design/book_summary.md).
- Next: [Synthesis & Reference](software/procedural/synthesis.md) ties both pillars together with the porting cheat-sheet.
