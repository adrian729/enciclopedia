# Creature Rigging: Outlines & Walk Cycles

> *Animation throughline.* A spine [chain](software/procedural/chains-and-ik.md) is an invisible skeleton. This page turns it into a creature: a **body outline** wrapped around the spine, and a **procedural walk cycle** for legs that are [FABRIK](software/procedural/chains-and-ik.md#4-fabrik) chains. The worked example is argonautcode's lizard. Examples use Bevy `0.18`.

## Table of Contents

- [1. From Skeleton to Silhouette](#1-from-skeleton-to-silhouette)
  - [1.1. The Outline Formula](#11-the-outline-formula)
  - [1.2. Per-Vertebra Width Arrays](#12-per-vertebra-width-arrays)
  - [1.3. The Handedness Gotcha](#13-the-handedness-gotcha)
- [2. Drawing Without Assets](#2-drawing-without-assets)
  - [2.1. Gizmos for the Skeleton and Outline](#21-gizmos-for-the-skeleton-and-outline)
  - [2.2. Meshes for the Filled Body](#22-meshes-for-the-filled-body)
  - [2.3. Gizmos vs Mesh](#23-gizmos-vs-mesh)
- [3. The Lizard](#3-the-lizard)
  - [3.1. Spine](#31-spine)
  - [3.2. Legs](#32-legs)
- [4. The Walk Cycle](#4-the-walk-cycle)
  - [4.1. Step Commitment](#41-step-commitment)
  - [4.2. Why a Threshold and a Lerp](#42-why-a-threshold-and-a-lerp)
- [5. Worked Example: The Lizard](#5-worked-example-the-lizard)
- [Sources](#sources)

## 1. From Skeleton to Silhouette

### 1.1. The Outline Formula

The spine gives a position \( \mathbf{j}_i \) and a heading \( \theta_i \) at each vertebra. To draw a body, step **sideways** from each vertebra — perpendicular to the heading — by the creature's half-width there:

\[ \mathbf{o}_i = \mathbf{j}_i + \hat u(\theta_i + \phi)\,(w_i + \delta), \qquad \phi = \pm\tfrac{\pi}{2} \]

where \( \hat u(\theta) = (\cos\theta, \sin\theta) \), \( w_i \) is the half-width at vertebra \( i \), and \( \delta \) is an optional bias (negative to tuck the head, positive to flare a fin). The two values \( \phi = +\tfrac{\pi}{2} \) and \( \phi = -\tfrac{\pi}{2} \) give the left and right outlines. Walking \( i \) down one side and back up the other traces a closed silhouette.

A useful identity: \( \hat u(\theta + \tfrac{\pi}{2}) \) is exactly the **perpendicular** of \( \hat u(\theta) \). In glam, `Vec2::perp()` computes \( (x, y) \mapsto (-y, x) \), so `Vec2::from_angle(theta).perp()` equals `Vec2::from_angle(theta + PI/2)` — handy for the two sides.

### 1.2. Per-Vertebra Width Arrays

\( w_i \) is not a formula but a hand-tuned **array**, one entry per vertebra — that is what gives each creature its character. argonautcode's lizard uses 14 widths:

```rust
let widths = [52.0, 58.0, 40.0, 60.0, 68.0, 71.0, 65.0, 50.0, 28.0, 15.0, 11.0, 9.0, 7.0, 7.0];
```

The bulge at indices 4-6 is the ribcage; the long taper is the tail. An array (not a smooth function) lets the artist place a head, shoulders, and hips exactly where they want them.

### 1.3. The Handedness Gotcha

The Processing source is y-**down**; Bevy is y-**up**. Under that flip, a \( +\tfrac{\pi}{2} \) rotation that pointed "right" on a Processing screen points the *other* way in Bevy, so **left and right outlines swap**. The formula is identical; only the on-screen labelling flips. When you port a creature and it renders inside-out or mirrored, this is why — verify the two sides visually rather than trusting the sign. (See the [Synthesis](software/procedural/synthesis.md) gotcha list.)

## 2. Drawing Without Assets

### 2.1. Gizmos for the Skeleton and Outline

Bevy **gizmos** are immediate-mode debug drawing: `gizmos.line_2d`, `gizmos.circle_2d`, `gizmos.linestrip_2d`. They allocate no entities and are recomputed every frame — ideal for the skeleton, the leg chains, and even the unfilled silhouette (a closed `linestrip_2d` through the outline points). They cannot be filled or textured.

### 2.2. Meshes for the Filled Body

For a *filled* body, generate a `Mesh` at runtime from the outline. Interleave the left/right outline points and draw them as a triangle strip:

```rust
use bevy::asset::RenderAssetUsages;
use bevy::render::render_resource::PrimitiveTopology;

/// `strip` is interleaved [left_0, right_0, left_1, right_1, …] along the spine.
fn outline_mesh(strip: &[Vec2]) -> Mesh {
    let positions: Vec<[f32; 3]> = strip.iter().map(|p| [p.x, p.y, 0.0]).collect();
    Mesh::new(PrimitiveTopology::TriangleStrip, RenderAssetUsages::default())
        .with_inserted_attribute(Mesh::ATTRIBUTE_POSITION, positions)
}
```

Two non-obvious points, both port-killers:

- **Import `RenderAssetUsages` from `bevy::asset`** (its `bevy::render` re-export was dropped in 0.17) and build with `RenderAssetUsages::default()` (= `MAIN_WORLD | RENDER_WORLD`). With `RENDER_WORLD` only, the CPU copy is discarded and your per-frame `meshes.get_mut(&handle)` updates silently stall.
- Spawn it once with `Mesh2d(handle)` + `MeshMaterial2d(materials.add(Color::srgb(...)))`, then each frame fetch `meshes.get_mut(&handle)` and overwrite `ATTRIBUTE_POSITION` with the new outline. The handle persists; only the vertices move.

### 2.3. Gizmos vs Mesh

| | Gizmos | Mesh |
|---|---|---|
| Setup | None | Spawn entity + handle + material |
| Fill | Outline only | Filled, textured, lit |
| Lifetime | Redrawn every frame | Persists; mutate in place |
| Use it for | Skeletons, debug, prototyping | The final rendered creature |

Rule of thumb: draw the skeleton with gizmos *always* (free debugging), and reach for a mesh only when you want the body actually filled. The example below uses gizmos throughout so it stays a single file.

## 3. The Lizard

### 3.1. Spine

A 14-joint chain with a \( \pi/8 \) bend limit, head chasing a target:

```rust
let spine = Chain::new(origin, 14, 64.0, PI / 8.0); // from chains-and-ik.md §3.1
```

### 3.2. Legs

Four legs, each a **three-joint FABRIK chain**. Per leg, three numbers place it:

- `side` = \( +1 \) or \( -1 \) — which side of the body.
- `body_index` — which vertebra it hangs from: **3** for the front pair, **7** for the rear pair.
- `spread` — the resting angle off the spine: \( \pi/4 \) front, \( \pi/3 \) rear.

Front legs use a longer link (52) than the rear (36). Each leg's **shoulder** (the FABRIK anchor) is a body point tucked slightly *inside* the silhouette, and its **desired foot** is a body point thrown well *outside* it:

```rust
fn body_point(spine: &Chain, i: usize, angle_off: f32, len_off: f32, widths: &[f32]) -> Vec2 {
    spine.joints[i] + Vec2::from_angle(spine.angles[i] + angle_off) * (widths[i] + len_off)
}
// shoulder (anchor): body_point(spine, body_index, side * PI/2, -20.0, widths)
// desired foot:      body_point(spine, body_index, side * spread, 80.0, widths)
```

## 4. The Walk Cycle

### 4.1. Step Commitment

The trick that makes legs *walk* instead of *skate*: the foot does not track its ideal position continuously. Instead each leg remembers a **committed** target \( \mathbf{c}_i \) (where the foot is planted). Every frame it computes the *desired* position \( \mathbf{d}_i \) from the moving body; only when the desired has drifted more than a threshold \( \tau \) from the committed does the foot **take a step** — committing to the new spot — and even then the foot eases toward it:

\[ \text{if } \lVert \mathbf{d}_i - \mathbf{c}_i \rVert > \tau:\quad \mathbf{c}_i \leftarrow \mathbf{d}_i; \qquad\qquad \mathbf{f}_i \leftarrow \mathrm{lerp}(\mathbf{f}_i,\, \mathbf{c}_i,\, 0.4) \]

Then FABRIK solves the leg so the foot reaches \( \mathbf{f}_i \) while the shoulder stays anchored to the body.

### 4.2. Why a Threshold and a Lerp

Two mechanisms, two jobs:

- **The threshold** \( \tau \) creates *foot-planting*: the foot stays put while the body moves over it, then snaps to a new plant once the body has moved far enough. A foot that tracked the body every frame would slide along the ground — the dreaded "ice-skating" look.
- **The lerp** (factor 0.4) makes the *swing* smooth: instead of teleporting to the new plant, the foot eases there over a few frames, reading as a quick step.

Together they are a complete gait with no animation data — the legs step because the geometry forces them to.

## 5. Worked Example: The Lizard

A complete program. It reuses `Chain` + `constrain_angle` (from [Chains & IK §2-3](software/procedural/chains-and-ik.md#23-in-bevy)), `fabrik_resolve` + `constrain_distance` (from [Chains & IK §4](software/procedural/chains-and-ik.md#4-fabrik) and [Foundations §3.3](software/procedural/foundations.md#33-in-bevy)), and `cursor_world` (from [Chains & IK §3.3](software/procedural/chains-and-ik.md#33-worked-example-a-chain-that-follows-the-cursor)). The silhouette and legs are drawn with gizmos.

```rust
use bevy::prelude::*;
use std::f32::consts::PI;

const STEP_THRESHOLD: f32 = 200.0;

struct Leg {
    chain: Vec<Vec2>, // 3 joints: [0] = foot (reaches), [2] = shoulder (anchor)
    link_len: f32,
    side: f32,        // +1 / -1
    body_index: usize,
    spread: f32,
    committed: Vec2,  // planted foot target
}

#[derive(Component)]
struct Lizard {
    spine: Chain,
    legs: Vec<Leg>,
    widths: Vec<f32>,
}

fn body_point(spine: &Chain, i: usize, angle_off: f32, len_off: f32, widths: &[f32]) -> Vec2 {
    spine.joints[i] + Vec2::from_angle(spine.angles[i] + angle_off) * (widths[i] + len_off)
}

fn setup(mut commands: Commands) {
    commands.spawn(Camera2d);

    let origin = Vec2::ZERO;
    let spine = Chain::new(origin, 14, 64.0, PI / 8.0);
    let widths = vec![52.0, 58.0, 40.0, 60.0, 68.0, 71.0, 65.0, 50.0, 28.0, 15.0, 11.0, 9.0, 7.0, 7.0];

    // (side, body_index, spread, link_len) for front-left, front-right, rear-left, rear-right.
    let specs = [
        (1.0, 3usize, PI / 4.0, 52.0),
        (-1.0, 3, PI / 4.0, 52.0),
        (1.0, 7, PI / 3.0, 36.0),
        (-1.0, 7, PI / 3.0, 36.0),
    ];
    let legs = specs
        .iter()
        .map(|&(side, body_index, spread, link_len)| {
            let foot = body_point(&spine, body_index, side * spread, 80.0, &widths);
            Leg { chain: vec![foot; 3], link_len, side, body_index, spread, committed: foot }
        })
        .collect();

    commands.spawn(Lizard { spine, legs, widths });
}

fn resolve(
    mut lizards: Query<&mut Lizard>,
    windows: Query<&Window>,
    cameras: Query<(&Camera, &GlobalTransform)>,
) {
    let Some(cursor) = cursor_world(&windows, &cameras) else {
        return;
    };
    for mut lizard in &mut lizards {
        // Step the head ≤12 px toward the cursor, not onto it. (The source steps a
        // constant 12 px via setMag; clamping also stops dead-on once the cursor is near.)
        let head = lizard.spine.joints[0];
        let target = head + (cursor - head).clamp_length_max(12.0);
        lizard.spine.resolve(target);

        // Borrow the spine + widths immutably while mutating legs: pull them apart.
        let Lizard { spine, legs, widths } = &mut *lizard;
        for leg in legs.iter_mut() {
            let desired = body_point(spine, leg.body_index, leg.side * leg.spread, 80.0, widths);
            if desired.distance(leg.committed) > STEP_THRESHOLD {
                leg.committed = desired;
            }
            let target = leg.chain[0].lerp(leg.committed, 0.4);
            let anchor = body_point(spine, leg.body_index, leg.side * PI / 2.0, -20.0, widths);
            fabrik_resolve(&mut leg.chain, leg.link_len, target, anchor, 10);
        }
    }
}

fn draw(mut gizmos: Gizmos, lizards: Query<&Lizard>) {
    let body = Color::srgb(0.32, 0.47, 0.43);
    for lizard in &lizards {
        let n = lizard.spine.joints.len();
        // Closed silhouette: one side head→tail (+π/2), back along the other (−π/2).
        let mut outline: Vec<Vec2> = (0..n)
            .map(|i| body_point(&lizard.spine, i, PI / 2.0, 0.0, &lizard.widths))
            .collect();
        outline.extend(
            (0..n)
                .rev()
                .map(|i| body_point(&lizard.spine, i, -PI / 2.0, 0.0, &lizard.widths)),
        );
        if let Some(&first) = outline.first() {
            outline.push(first); // close the loop
        }
        gizmos.linestrip_2d(outline, body);

        // Legs: shoulder → elbow → foot.
        for leg in &lizard.legs {
            gizmos.linestrip_2d(leg.chain.iter().rev().copied(), Color::WHITE);
            gizmos.circle_2d(leg.chain[0], 5.0, Color::WHITE); // foot
        }
    }
}

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .add_systems(Startup, setup)
        .add_systems(Update, (resolve, draw).chain())
        .run();
}
```

Notice the **destructuring borrow** `let Lizard { spine, legs, widths } = &mut *lizard;` — Rust will not let you call `body_point(&self.spine, …)` (immutable) while iterating `self.legs` mutably through the same `&mut Lizard`, so we split the struct into disjoint field borrows. This is the idiomatic Rust answer to a pattern that is implicit in the garbage-collected Processing original. Everything else is a faithful port: the spine resolves first, then each leg computes its desired foot, steps if it has drifted past `STEP_THRESHOLD`, eases the foot with a `lerp`, and FABRIK-solves against a freshly-recomputed shoulder anchor.

One deliberate looseness to know about: the 12 px head step is per `Update` *frame*, so locomotion speed scales with the refresh rate (the Processing source is locked to 60 fps). Scale the step by `time.delta_secs()` — or move `resolve` into `FixedUpdate` — if you need rate-independent movement.

## Sources

- argonautcode — [animal-proc-anim](https://github.com/argonautcode/animal-proc-anim) (`Lizard`, `Fish`: `getPosX`/`getPosY`, body widths, the step cycle) and its [video](https://www.youtube.com/watch?v=qlfh_rv6khY).
- Next: [Soft Bodies](software/procedural/soft-bodies.md) reuses the same Verlet + relaxation machinery for a deformable, volume-preserving body.
