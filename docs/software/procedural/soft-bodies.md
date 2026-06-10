# Soft Bodies: The Blob

> *Animation throughline.* A soft body is a closed **ring of Verlet points** held together by two constraints: neighbours stay a fixed distance apart, and the enclosed **area** stays near a target. It reuses every primitive from [Foundations](software/procedural/foundations.md) at full strength — and is the one place you *must* use Jacobi relaxation. The worked example is argonautcode's Blob. Examples use Bevy `0.18`.

## Table of Contents

- [1. A Soft Body Is a Ring of Constrained Points](#1-a-soft-body-is-a-ring-of-constrained-points)
- [2. Geometry and Targets](#2-geometry-and-targets)
  - [2.1. Target Area and Puffiness](#21-target-area-and-puffiness)
  - [2.2. The Shoelace Formula](#22-the-shoelace-formula)
- [3. The Per-Frame Solve](#3-the-per-frame-solve)
  - [3.1. Integrate](#31-integrate)
  - [3.2. Neighbour Distance Constraint](#32-neighbour-distance-constraint)
  - [3.3. Area Preservation](#33-area-preservation)
  - [3.4. Apply, Bounds, Collision](#34-apply-bounds-collision)
- [4. Why Area Preservation, Not Pressure Springs](#4-why-area-preservation-not-pressure-springs)
- [5. Why Jacobi Is Mandatory Here](#5-why-jacobi-is-mandatory-here)
- [6. Worked Example: The Blob](#6-worked-example-the-blob)
- [7. The Frog: Blob and Limbs](#7-the-frog-blob-and-limbs)
- [Sources](#sources)

## 1. A Soft Body Is a Ring of Constrained Points

Arrange \( N \) Verlet points in a circle and connect each to its two neighbours. Two rules give it life:

1. **Neighbour distance** — adjacent points stay roughly a chord-length apart (the skin doesn't tear).
2. **Area preservation** — the enclosed area stays near a target (the body has "volume" and resists being squashed flat).

That second constraint is what separates a soft body from a floppy closed rope. Both are projections, solved by the same relaxation loop as everything else.

## 2. Geometry and Targets

### 2.1. Target Area and Puffiness

From a rest radius \( r \), a point count \( N \), and a `puffiness` multiplier:

\[ A_\text{target} = r^2\,\pi\,\cdot\,\text{puffiness}, \qquad C = 2\pi r, \qquad \ell = \frac{C}{N} \]

\( A_\text{target} \) is the area the body wants to enclose, \( C \) its rest circumference, and \( \ell \) the rest chord between neighbours. `puffiness > 1` makes the body want *more* area than its perimeter naturally encloses, so it bulges taut like a balloon; `puffiness ≈ 1` gives a relaxed, droopy blob.

### 2.2. The Shoelace Formula

The signed area of a polygon from its vertices:

\[ A = \tfrac{1}{2}\sum_{i} (x_i - x_{i+1})(y_i + y_{i+1}) \]

(indices wrap; this trapezoidal form is algebraically identical to the more familiar \( \tfrac12\sum (x_i y_{i+1} - x_{i+1} y_i) \)). It is **signed**: positive for a counter-clockwise winding, negative for clockwise. That sign matters in the next step — see the warning in [§3.3](#33-area-preservation).

## 3. The Per-Frame Solve

Each frame: integrate once, then run \~10 relaxation iterations of (neighbour constraint → area constraint → apply → bounds/collision).

### 3.1. Integrate

Exactly the Verlet step from Foundations, applied to every ring point, with gravity pointing **down** in y-up: `pos += Vec2::NEG_Y * g`.

### 3.2. Neighbour Distance Constraint

This is the free-free distance constraint, but **one-sided**: only pull neighbours together when they have stretched *beyond* the chord length — they may come closer freely (that is what lets the body squish). For each edge \( (i, i{+}1) \) with separation \( d > \ell \): each point moves \( \tfrac{d - \ell}{2} \) toward the other. The corrections are **accumulated**, not applied immediately (see [§5](#5-why-jacobi-is-mandatory-here)).

### 3.3. Area Preservation

Once per iteration, measure the current area \( A \) and compute a uniform outward push:

\[ \text{offset} = \frac{A_\text{target} - A}{C} \]

Then push every point along its **outward normal** by `offset`. The outward normal at point \( i \) is the perpendicular of the *secant* through its neighbours, \( \mathbf{s}_i = \mathbf{p}_{i+1} - \mathbf{p}_{i-1} \):

\[ \mathbf{n}_i = \widehat{\mathrm{rot}_{-90°}(\mathbf{s}_i)}\;\cdot\;\text{offset}, \qquad \mathrm{rot}_{-90°}(x, y) = (y, -x) \]

If the body is too small (\( A < A_\text{target} \)) then `offset > 0` and the points push outward, inflating it; too large and they pull inward. Because the push is shared along the whole perimeter, the total restored area is \( \approx \text{offset}\cdot C = A_\text{target} - A \) — the constraint nudges the area straight back toward target.

> **The highest-risk port in this section.** The outward-normal direction is *coupled* to the ring's winding. Here the ring is built with **increasing angle**, so the shoelace area is **positive** and the outward normal is \( \mathrm{rot}_{-90°}(\mathbf{s}) = (s_y, -s_x) \) — which is glam's `-secant.perp()`, **not** `secant.perp()`. The Processing source's `rotate(-HALF_PI)` is the *same* \( (s_y, -s_x) \): the formula ports **literally**, because both versions build the ring with increasing angle and the algebra never sees the screen. The two ways to get it wrong: translating "rotate by −90°" *idiomatically* as `.perp()` (that is +90°), or building the ring with the opposite winding — either points the normal *inward* and the blob implodes. The shoelace sign and the normal direction must agree: if your blob collapses instead of inflating, flip this sign.

### 3.4. Apply, Bounds, Collision

After both constraints have *accumulated* their suggestions, **apply** them Jacobi-style: each point adds the *average* of its accumulated corrections, then resets its accumulator. Finally clamp points inside the play area and resolve mouse/obstacle collisions by projecting any intruding point back out to the collider's surface (another distance constraint).

## 4. Why Area Preservation, Not Pressure Springs

An alternative way to give a soft body volume is an internal **pressure** model: treat the enclosed gas as pushing outward on each edge with a force proportional to \( 1/\text{area} \). It works, but for a PBD solver area preservation is the better fit:

- It is a **single global geometric constraint** — one area target — rather than a per-edge force with its own stiffness coefficient to tune.
- It is **position-based and exact**: project the perimeter so the area equals the target. A pressure *force* must be integrated, and forces integrate poorly inside a position solver (the very problem PBD exists to avoid, per [Foundations §1.2](software/procedural/foundations.md#12-position-based-vs-force-based)).
- It composes cleanly with the neighbour constraints in the same relaxation loop.

## 5. Why Jacobi Is Mandatory Here

In [Foundations §4.2](software/procedural/foundations.md#42-gauss-seidel-vs-jacobi) we used Gauss-Seidel (apply each correction in place) for a rope. The Blob cannot: the **area constraint touches every point in the same iteration**. The push *magnitude* is computed once from a shared area measurement, but each point's *direction* is the outward normal of the secant through its **neighbours** — applied in place, point \( i \)'s normal would be computed from an already-moved point \( i-1 \), skewing the directions progressively around the ring and biasing the shape by vertex index — the blob would warp toward wherever the loop started. (Each point also collects suggestions from *two* constraints, its edges and the area push, which should be blended rather than applied in whatever order the code runs.) **Jacobi** — accumulate every point's suggestions, then average and apply together — removes that order dependence, at the cost of slightly slower convergence (hence \~10 iterations). Each point therefore carries an accumulator:

```rust
#[derive(Clone, Copy)]
struct BlobPoint {
    pos: Vec2,
    prev: Vec2,
    disp: Vec2, // accumulated correction this iteration (Jacobi)
    weight: u32,
}
```

## 6. Worked Example: The Blob

A complete Bevy `0.18` program. Build with `bevy = "0.18"`. Hold the left mouse button to poke it.

```rust
use bevy::prelude::*;
use std::f32::consts::TAU;

const N: usize = 16;
const RADIUS: f32 = 120.0;
const PUFFINESS: f32 = 1.5;
const GRAVITY: f32 = 1.0;
const DAMPING: f32 = 0.99;
const ITERATIONS: usize = 10;
const HALF_W: f32 = 620.0;
const HALF_H: f32 = 340.0;
const MOUSE_R: f32 = 100.0;

#[derive(Clone, Copy)]
struct BlobPoint {
    pos: Vec2,
    prev: Vec2,
    disp: Vec2,
    weight: u32,
}

#[derive(Component)]
struct Blob {
    points: Vec<BlobPoint>,
    target_area: f32,
    chord: f32,
    circumference: f32,
}

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .add_systems(Startup, setup)
        .add_systems(FixedUpdate, (integrate, solve).chain())
        .add_systems(Update, draw)
        .run();
}

fn setup(mut commands: Commands) {
    commands.spawn(Camera2d);

    let circumference = TAU * RADIUS;
    let points = (0..N)
        .map(|i| {
            // Counter-clockwise ring (angle increasing) -> positive shoelace area.
            let a = TAU * i as f32 / N as f32;
            let pos = Vec2::new(a.cos(), a.sin()) * RADIUS + Vec2::Y * 150.0;
            BlobPoint { pos, prev: pos, disp: Vec2::ZERO, weight: 0 }
        })
        .collect();

    commands.spawn(Blob {
        points,
        target_area: RADIUS * RADIUS * std::f32::consts::PI * PUFFINESS,
        chord: circumference / N as f32,
        circumference,
    });
}

fn integrate(mut blobs: Query<&mut Blob>) {
    for mut blob in &mut blobs {
        for p in &mut blob.points {
            let prev = p.pos;
            let velocity = (p.pos - p.prev) * DAMPING;
            p.pos += velocity + Vec2::NEG_Y * GRAVITY;
            p.prev = prev;
        }
    }
}

/// Signed polygon area (positive for counter-clockwise winding).
fn signed_area(points: &[BlobPoint]) -> f32 {
    let n = points.len();
    let mut a = 0.0;
    for i in 0..n {
        let cur = points[i].pos;
        let next = points[(i + 1) % n].pos;
        a += (cur.x - next.x) * (cur.y + next.y);
    }
    a * 0.5
}

fn solve(
    mut blobs: Query<&mut Blob>,
    buttons: Res<ButtonInput<MouseButton>>,
    windows: Query<&Window>,
    cameras: Query<(&Camera, &GlobalTransform)>,
) {
    let mouse = pressed_cursor_world(&buttons, &windows, &cameras);
    for mut blob in &mut blobs {
        let n = blob.points.len();
        let (chord, target_area, circumference) =
            (blob.chord, blob.target_area, blob.circumference);

        for _ in 0..ITERATIONS {
            // 1. Neighbour distance — one-sided: only pull together when stretched.
            for i in 0..n {
                let j = (i + 1) % n;
                let delta = blob.points[j].pos - blob.points[i].pos;
                let dist = delta.length();
                if dist > chord {
                    let off = delta.normalize_or_zero() * ((dist - chord) * 0.5);
                    accumulate(&mut blob.points[i], off);
                    accumulate(&mut blob.points[j], -off);
                }
            }

            // 2. Area preservation — uniform outward push (Jacobi).
            let offset = (target_area - signed_area(&blob.points)) / circumference;
            for i in 0..n {
                let prev = blob.points[(i + n - 1) % n].pos;
                let next = blob.points[(i + 1) % n].pos;
                let secant = next - prev;
                // CCW ring => outward normal = rot(-90°)(secant) = (s.y, -s.x) = -secant.perp().
                let outward = Vec2::new(secant.y, -secant.x).normalize_or_zero();
                accumulate(&mut blob.points[i], outward * offset);
            }

            // 3. Apply the averaged corrections, then collide.
            for p in &mut blob.points {
                if p.weight > 0 {
                    p.pos += p.disp / p.weight as f32;
                    p.disp = Vec2::ZERO;
                    p.weight = 0;
                }
                p.pos.x = p.pos.x.clamp(-HALF_W, HALF_W);
                p.pos.y = p.pos.y.clamp(-HALF_H, HALF_H);
                if let Some(m) = mouse {
                    if p.pos.distance(m) < MOUSE_R {
                        p.pos = m + (p.pos - m).normalize_or_zero() * MOUSE_R;
                    }
                }
            }
        }
    }
}

fn accumulate(p: &mut BlobPoint, offset: Vec2) {
    p.disp += offset;
    p.weight += 1;
}

fn pressed_cursor_world(
    buttons: &Res<ButtonInput<MouseButton>>,
    windows: &Query<&Window>,
    cameras: &Query<(&Camera, &GlobalTransform)>,
) -> Option<Vec2> {
    if !buttons.pressed(MouseButton::Left) {
        return None;
    }
    let cursor = windows.single().ok()?.cursor_position()?;
    let (camera, transform) = cameras.single().ok()?;
    camera.viewport_to_world_2d(transform, cursor).ok()
}

fn draw(mut gizmos: Gizmos, blobs: Query<&Blob>) {
    let skin = Color::srgb(0.16, 0.17, 0.21);
    for blob in &blobs {
        let mut loop_pts: Vec<Vec2> = blob.points.iter().map(|p| p.pos).collect();
        if let Some(&first) = loop_pts.first() {
            loop_pts.push(first);
        }
        gizmos.linestrip_2d(loop_pts, Color::WHITE);
        for p in &blob.points {
            gizmos.circle_2d(p.pos, 6.0, skin);
        }
    }
}
```

Every primitive from earlier is here: Verlet integration ([Foundations §2](software/procedural/foundations.md#2-verlet-integration)), the distance constraint ([§3.2](#32-neighbour-distance-constraint)), Jacobi accumulation ([§5](#5-why-jacobi-is-mandatory-here)), and one new constraint — area. Raise `PUFFINESS` for a tauter balloon; raise `ITERATIONS` for a stiffer body; drop `GRAVITY` to zero and poke it to watch it wobble back to a circle.

## 7. The Frog: Blob and Limbs

argonautcode's frog pairs a **soft-body blob torso** with simple two-point **limbs**: each is a gravity-affected Verlet pair (elbow, foot) solved with the angle-constrained distance constraint from [Chains & IK §2](software/procedural/chains-and-ik.md#2-angle-constraints), anchored to specific ring points — the feet *dangle* rather than step. To make such a creature walk, nothing new is needed: pick ring indices as hip/shoulder anchors, attach a [FABRIK](software/procedural/chains-and-ik.md#4-fabrik) chain to each, and reuse the lizard's [threshold-and-lerp gait](software/procedural/creature-rigging.md#4-the-walk-cycle), with desired feet offset from the (now squishy) body. The throughline holds: integrate points, project onto constraints, render.

## Sources

- argonautcode — [soft-body-proc-anim](https://github.com/argonautcode/soft-body-proc-anim) (`Blob`, `BlobPoint`: Verlet ring, accumulated displacement, area preservation) and its [video](https://www.youtube.com/watch?v=GXh0Vxg7AnQ).
- zalo — [*Constraints*](https://zalo.github.io/blog/constraints/) (volume-preserving constraint, Jacobi vs Gauss-Seidel).
- Next: the generation pillar begins with [Noise, fBm & Heightmaps](software/procedural/generation-noise.md).
