# Foundations: Verlet & Constraint Projection

> *Animation throughline.* This page builds the three primitives every later animation page reuses: a **Verlet integrator** that moves points by inertia, a **constraint** that projects points back onto a rule, and a **relaxation loop** that applies many constraints until they agree. The worked example is a hanging rope — the smallest program that exercises all three. Examples use Bevy `0.18`; for ECS basics (components, systems, schedules) see the [Bevy](software/bevy.md) guide.

## Table of Contents

- [1. Position-Based Dynamics](#1-position-based-dynamics)
  - [1.1. The Throughline](#11-the-throughline)
  - [1.2. Position-Based vs Force-Based](#12-position-based-vs-force-based)
- [2. Verlet Integration](#2-verlet-integration)
  - [2.1. The Update Rule](#21-the-update-rule)
  - [2.2. Damping](#22-damping)
  - [2.3. Verlet vs Explicit Euler](#23-verlet-vs-explicit-euler)
  - [2.4. In Bevy: Why FixedUpdate](#24-in-bevy-why-fixedupdate)
- [3. Constraint Projection](#3-constraint-projection)
  - [3.1. A Constraint Is a Projection](#31-a-constraint-is-a-projection)
  - [3.2. The Distance Constraint](#32-the-distance-constraint)
  - [3.3. In Bevy](#33-in-bevy)
- [4. Relaxation](#4-relaxation)
  - [4.1. Why Iterate](#41-why-iterate)
  - [4.2. Gauss-Seidel vs Jacobi](#42-gauss-seidel-vs-jacobi)
- [5. Worked Example: A Hanging Rope](#5-worked-example-a-hanging-rope)
- [Sources](#sources)

## 1. Position-Based Dynamics

### 1.1. The Throughline

A physics simulation traditionally tracks position, velocity, and the forces acting on a body, then integrates forces into velocities and velocities into positions. **Position-Based Dynamics (PBD)** throws out the middle layer. It keeps only positions, derives velocity *implicitly* from how far a point moved last step, and enforces every rule by directly **moving points**. The whole loop is:

\[ \text{integrate (move by inertia + gravity)} \;\rightarrow\; \big(\text{project points onto constraints}\big) \times N \;\rightarrow\; \text{render} \]

This is the engine behind ropes, cloth, inverse kinematics, and soft bodies alike — they differ only in *which* constraints they project onto. Master this loop once and the rest of the section is variations on a theme.

### 1.2. Position-Based vs Force-Based

Why move positions directly instead of applying forces?

- **Stability.** A stiff spring (force-based) needs tiny timesteps or it overshoots and explodes. A distance *constraint* (position-based) simply teleports the point to the correct distance — it cannot overshoot, so it is unconditionally stable however stiff the material.
- **Directness.** "This bone is 30 units long" is awkward to express as a force but trivial as a projection: move the endpoint until it is 30 units away.
- **Control.** Designers think in positions and lengths, not spring coefficients. PBD lets you author the rules you actually care about.

The price is that PBD is not physically exact — it is *plausible*, which is exactly what animation wants.

## 2. Verlet Integration

### 2.1. The Update Rule

Verlet integration stores each point's **current** and **previous** position. Velocity is never stored; it is implied by the gap between them. One step is:

\[ \mathbf{x}_{t+1} = \mathbf{x}_t + \underbrace{(\mathbf{x}_t - \mathbf{x}_{t-1})\, d}_{\text{inertia (implicit velocity)}} + \underbrace{\mathbf{a}\,\Delta t^{2}}_{\text{acceleration}} \]

where \( \mathbf{a} \) is acceleration (gravity), \( d \) is a damping factor, and \( \Delta t \) is the timestep. The implicit velocity term \( (\mathbf{x}_t - \mathbf{x}_{t-1}) \) is the magic: if a constraint *yanks* a point to a new position during the solve, the next frame automatically sees the change in implied velocity — momentum is conserved for free, with no velocity bookkeeping.

The source code uses a **unit timestep** (\( \Delta t = 1 \)), so \( \mathbf{a}\,\Delta t^{2} \) collapses to just \( \mathbf{a} \), with the gravity constant absorbing the units. We keep that form (see [§2.4](#24-in-bevy-why-fixedupdate) for why it is safe).

### 2.2. Damping

The factor \( d \) (typically \( 0.99 \)) multiplies only the inertia term. It bleeds off a little velocity each step, modelling air drag and keeping the simulation from accumulating numerical energy. Set \( d = 1 \) for frictionless motion; lower it for a sluggish, underwater feel.

### 2.3. Verlet vs Explicit Euler

Explicit (forward) Euler stores velocity and updates `pos += vel * dt; vel += accel * dt`. Under PBD it is a poor fit:

- When the constraint solver **moves a position**, explicit Euler's stored velocity is now a lie — it no longer matches where the point actually is, so energy is injected or lost and the system jitters or blows up. Verlet has no stored velocity to desync; projecting the position *is* the velocity update.
- Verlet is time-reversible and (with a constant step) conserves energy far better, so chains settle instead of buzzing.

That is why every PBD system in this section integrates with Verlet.

### 2.4. In Bevy: Why FixedUpdate

Run the integrate + solve systems in the **`FixedUpdate`** schedule, not `Update`. Verlet's stability hinges on a **constant \( \Delta t \)**: the inertia term \( (\mathbf{x}_t - \mathbf{x}_{t-1}) \) already bakes in the *previous* step's duration, so if this step's duration differs (which it does, frame to frame, in `Update`), the implied velocity is silently rescaled — ropes jitter, stretch, or detonate. `FixedUpdate` ticks at a fixed rate (64 Hz by default), giving every step the same \( \Delta t \). Because that \( \Delta t \) is constant we keep the unit-timestep form and simply tune the gravity constant — **do not** fold `time.delta_secs()` into the inertia term while leaving gravity unit-treated, or the two terms scale inconsistently and the rope drifts. Rendering (gizmos) stays in `Update`.

A point is modelled as its two positions plus whether it is pinned (an anchor that the integrator skips):

```rust
struct VerletPoint {
    pos: Vec2,
    prev: Vec2,
    pinned: bool,
}
```

We store the points inline in a `Vec` on a single entity rather than one entity per point: the solve is an inherently *sequential* pass over an ordered array, and a `Vec` keeps it cache-friendly and simple to index.

## 3. Constraint Projection

### 3.1. A Constraint Is a Projection

> The essence of constraint is projection. **Find the minimum movement that satisfies the constraint.**

A constraint is a rule the configuration must obey ("these two points are exactly \( L \) apart"). To *solve* it you move the offending point(s) the shortest distance that makes the rule true again. Minimum movement matters: it disturbs the rest of the system as little as possible, so many constraints can coexist and be solved by repetition ([§4](#4-relaxation)).

### 3.2. The Distance Constraint

The atom of PBD. Keep a point \( \mathbf{p} \) at distance \( L \) from an anchor \( \mathbf{a} \) by projecting it onto the circle of radius \( L \):

\[ \mathbf{p}' = \mathbf{a} + (\mathbf{p} - \mathbf{a})\,\frac{L}{\lVert \mathbf{p} - \mathbf{a} \rVert} \]

That is the **pinned** form (one end fixed). When *both* points are free, split the error so each moves half — momentum stays centred:

\[ e = \lVert \mathbf{b} - \mathbf{a} \rVert - L, \qquad \hat{\mathbf{d}} = \frac{\mathbf{b} - \mathbf{a}}{\lVert \mathbf{b} - \mathbf{a} \rVert}, \qquad \mathbf{a} \leftarrow \mathbf{a} + \tfrac{e}{2}\,\hat{\mathbf{d}}, \quad \mathbf{b} \leftarrow \mathbf{b} - \tfrac{e}{2}\,\hat{\mathbf{d}} \]

A rope is just a row of these constraints, one per link.

### 3.3. In Bevy

```rust
/// Pinned form: project `p` onto the circle of radius `len` around `anchor`.
fn constrain_distance(p: Vec2, anchor: Vec2, len: f32) -> Vec2 {
    anchor + (p - anchor).normalize_or_zero() * len
}
```

Use `normalize_or_zero`, never `normalize`: if the two points ever coincide, `normalize` returns NaN components on the zero vector (it only *panics* under glam's opt-in `glam_assert` feature, which Bevy does not enable by default) — and one NaN silently poisons every position it touches. `normalize_or_zero` yields `Vec2::ZERO`, so the (zero-magnitude) correction is harmlessly skipped.

## 4. Relaxation

### 4.1. Why Iterate

A single pass over a rope only locally satisfies each link: fixing link \( i \) nudges the shared point and *breaks* link \( i-1 \) that you just fixed. Error propagates one link per pass, so a chain of \( n \) links needs on the order of \( n \) passes to fully "tighten". You therefore run the constraint pass several times per frame — **relaxation**. More iterations means a stiffer, less stretchy result; fewer means a softer, springier one. Iteration count is a tuning dial, not a correctness requirement.

### 4.2. Gauss-Seidel vs Jacobi

Two ways to apply the corrections within a pass:

- **Gauss-Seidel** — update each point **in place**, so later constraints in the pass already see the moved point. Converges fastest and is the simplest to write. It is *order-dependent* (solving links front-to-back differs from back-to-front) and "not technically correct", but for a rope that bias is invisible.
- **Jacobi** — **accumulate** every constraint's suggested correction without applying any, then at the end of the pass average the suggestions per point and apply once. Order-independent and more stable, but "squishier": it converges more slowly because no constraint benefits from another's work within the pass.

Use **Gauss-Seidel** for chains and ropes (fast, order bias harmless). You **must** switch to **Jacobi** when a constraint touches every point at once — the soft-body area constraint in [Soft Bodies](software/procedural/soft-bodies.md) — because in-place updates would bias the shape by vertex index. The rope below uses Gauss-Seidel.

## 5. Worked Example: A Hanging Rope

A complete Bevy `0.18` program: 20 Verlet points in a column, the top one pinned, gravity pulling the rest, distance constraints holding the links, solved Gauss-Seidel in `FixedUpdate` and drawn with gizmos in `Update`. Drop it into `main.rs` with `bevy = "0.18"` in `Cargo.toml`.

```rust
use bevy::prelude::*;

#[derive(Clone, Copy)]
struct VerletPoint {
    pos: Vec2,
    prev: Vec2,
    pinned: bool,
}

#[derive(Component)]
struct Rope {
    points: Vec<VerletPoint>,
    link_len: f32,
}

#[derive(Resource)]
struct Sim {
    gravity: Vec2,
    damping: f32,
    iterations: usize,
}

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .insert_resource(Sim {
            gravity: Vec2::new(0.0, -0.5), // y-up: gravity points DOWN (negative y)
            damping: 0.99,
            iterations: 20,
        })
        .add_systems(Startup, setup)
        .add_systems(FixedUpdate, (integrate, solve).chain())
        .add_systems(Update, draw)
        .run();
}

fn setup(mut commands: Commands) {
    commands.spawn(Camera2d);

    let n = 20;
    let link_len = 18.0;
    let top = Vec2::new(0.0, 250.0);
    let points = (0..n)
        .map(|i| {
            let pos = top - Vec2::Y * (i as f32 * link_len);
            VerletPoint { pos, prev: pos, pinned: i == 0 }
        })
        .collect();

    commands.spawn(Rope { points, link_len });
}

/// Move every free point by inertia + gravity. Unit timestep (constant under FixedUpdate).
fn integrate(mut ropes: Query<&mut Rope>, sim: Res<Sim>) {
    for mut rope in &mut ropes {
        for p in &mut rope.points {
            if p.pinned {
                continue;
            }
            let prev = p.pos;
            let velocity = (p.pos - p.prev) * sim.damping;
            p.pos += velocity + sim.gravity;
            p.prev = prev;
        }
    }
}

/// Relax the link constraints. Gauss-Seidel: corrections applied in place.
fn solve(mut ropes: Query<&mut Rope>, sim: Res<Sim>) {
    for mut rope in &mut ropes {
        let n = rope.points.len();
        let link = rope.link_len;
        for _ in 0..sim.iterations {
            for i in 0..n - 1 {
                let a = rope.points[i];
                let b = rope.points[i + 1];
                let delta = b.pos - a.pos;
                let err = delta.length() - link;
                let dir = delta.normalize_or_zero();
                match (a.pinned, b.pinned) {
                    (true, true) => {}
                    (true, false) => rope.points[i + 1].pos -= dir * err,
                    (false, true) => rope.points[i].pos += dir * err,
                    (false, false) => {
                        rope.points[i].pos += dir * (err * 0.5);
                        rope.points[i + 1].pos -= dir * (err * 0.5);
                    }
                }
            }
        }
    }
}

fn draw(mut gizmos: Gizmos, ropes: Query<&Rope>) {
    for rope in &ropes {
        for pair in rope.points.windows(2) {
            gizmos.line_2d(pair[0].pos, pair[1].pos, Color::WHITE);
        }
        for p in &rope.points {
            gizmos.circle_2d(p.pos, 4.0, Color::srgb(0.16, 0.17, 0.21));
        }
    }
}
```

Things to notice, each tying back to the theory:

- **Gravity is `Vec2::new(0.0, -0.5)`** — negative `y`, because Bevy is y-**up** while the Processing source is y-**down**. This sign flip recurs throughout the section.
- **`integrate` and `solve` are `.chain()`-ed in `FixedUpdate`** — constant \( \Delta t \) ([§2.4](#24-in-bevy-why-fixedupdate)); `draw` is in `Update`.
- **The pinned check** in both `integrate` and `solve` is how an anchor works: an immovable point the simulation flows from. Point a free end to the mouse instead, and you have the chains of the next page.
- **`iterations: 20`** is the stiffness dial ([§4.1](#41-why-iterate)). Drop it to 2 and the rope visibly sags and stretches.

## Sources

- zalo — [*Constraints*](https://zalo.github.io/blog/constraints/) (Verlet integration, the projection principle, Gauss-Seidel vs Jacobi).
- argonautcode — [soft-body-proc-anim](https://github.com/argonautcode/soft-body-proc-anim) (the Verlet point / accumulated-displacement pattern).
- Next: [Kinematic Chains & IK](software/procedural/chains-and-ik.md) composes these primitives into chains and inverse kinematics.
