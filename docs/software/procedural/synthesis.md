# Synthesis, Tradeoffs & Bevy Reference

> The page to keep open while implementing. It restates the two throughlines as one table, indexes every "why this and not that" decision argued across the section, and collects the Processing→Bevy porting cheat-sheet and the correctness gotchas that bite during a port.

## Table of Contents

- [1. The Two Throughlines, Restated](#1-the-two-throughlines-restated)
- [2. Reasoning Index](#2-reasoning-index)
- [3. Bevy and Rust Port Cheat-Sheet](#3-bevy-and-rust-port-cheat-sheet)
  - [3.1. Processing to glam API Map](#31-processing-to-glam-api-map)
  - [3.2. The y-down to y-up Checklist](#32-the-y-down-to-y-up-checklist)
  - [3.3. Correctness Gotchas](#33-correctness-gotchas)
- [Sources](#sources)

## 1. The Two Throughlines, Restated

Every technique in this section is one row of this table. Animation is **integrate → project → render**; generation is **seed → function → content**.

| Technique | Pillar | Core operation | Constraint / generator | Renderer |
|---|---|---|---|---|
| Rope / cloth | Animation | Verlet + relax | Distance constraints | Gizmo lines |
| Spine / tentacle | Animation | Forward chain | Distance + angle constraints | Mesh / gizmos |
| Limb reach | Animation | FABRIK | Iterated distance constraints (two ends) | Gizmo / bezier |
| Creature body | Animation | Spine + outline + gait | Chains + per-vertebra widths + step rule | Triangle-strip mesh |
| Soft body | Animation | Verlet ring + Jacobi | Distance + area-preservation | Gizmo loop / triangulated mesh |
| Terrain / clouds | Generation | Sample a field | Perlin/simplex noise + fBm | Texture / heightmesh |
| Plants / trees | Generation | Rewrite a string | L-system grammar + turtle | Gizmo lines |
| Caves | Generation | Iterate a grid rule | Cellular automaton | Texture / tilemap |
| Scatter | Generation | Sample with spacing | Poisson-disk | Sprites / instances |
| Tile worlds | Generation | Collapse + propagate | Adjacency constraints from an example (WFC) | Tilemap |

## 2. Reasoning Index

The deliberate "why this, not that" choices, each argued where it first matters:

| Decision | Chose | Over | Because | Argued in |
|---|---|---|---|---|
| Integration model | Position-based (PBD) | Force-based | Stable however stiff; positions are what you author | [Foundations §1.2](software/procedural/foundations.md#12-position-based-vs-force-based) |
| Integrator | Verlet | Explicit Euler | No stored velocity to desync when the solver moves a point | [Foundations §2.3](software/procedural/foundations.md#23-verlet-vs-explicit-euler) |
| Schedule | `FixedUpdate` | `Update` | Verlet needs a constant Δt or it jitters/explodes | [Foundations §2.4](software/procedural/foundations.md#24-in-bevy-why-fixedupdate) |
| Rope/chain relaxation | Gauss-Seidel | Jacobi | Faster convergence; order bias is invisible on a chain | [Foundations §4.2](software/procedural/foundations.md#42-gauss-seidel-vs-jacobi) |
| Soft-body relaxation | Jacobi | Gauss-Seidel | Area constraint touches all points at once; in-place biases by index | [Soft Bodies §5](software/procedural/soft-bodies.md#5-why-jacobi-is-mandatory-here) |
| Spine solver | Forward chain | FABRIK | Head leads, no anchored second end; angle limits prevent kinks | [Chains & IK §3.2](software/procedural/chains-and-ik.md#32-why-this-for-a-spine) |
| Limb solver | FABRIK (game default) | CCD / Jacobian / analytic / autodiff | Fast, trig-free, two-ended, easy joint limits | [Chains & IK §5](software/procedural/chains-and-ik.md#5-choosing-an-ik-method) |
| Gait | Step threshold + lerp | Continuous foot tracking | Plants feet (no skating) then swings smoothly | [Creature Rigging §4.2](software/procedural/creature-rigging.md#42-why-a-threshold-and-a-lerp) |
| Soft-body volume | Area preservation | Internal pressure springs | One global geometric constraint, PBD-native, no force integration | [Soft Bodies §4](software/procedural/soft-bodies.md#4-why-area-preservation-not-pressure-springs) |
| Debug drawing | Gizmos | Mesh | Zero setup, redrawn each frame; mesh only for the final fill | [Creature Rigging §2.3](software/procedural/creature-rigging.md#23-gizmos-vs-mesh) |
| Chain storage | One entity, `Vec` of joints | Entity-per-joint | Solve is a sequential ordered pass; `Vec` is cache-friendly | [Foundations §2.4](software/procedural/foundations.md#24-in-bevy-why-fixedupdate) |
| Generation RNG | Seeded `ChaCha8Rng` | `rand::rng()` | Reproducible, shareable, debuggable worlds | [Noise §1.2](software/procedural/generation-noise.md#12-seeded-rng-in-bevy) |

## 3. Bevy and Rust Port Cheat-Sheet

### 3.1. Processing to glam API Map

The source repos are Processing (`PVector`); these are the Bevy/glam equivalents.

| Processing `PVector` | Bevy / glam | Note |
|---|---|---|
| `v.heading()` | `v.to_angle()` | both are `atan2(y, x)` |
| `PVector.fromAngle(a)` | `Vec2::from_angle(a)` | both are `(cos a, sin a)` |
| `v.setMag(m)` | `v.normalize_or_zero() * m` | **never** `normalize()` — on the zero vector it yields NaN and silently corrupts everything downstream |
| `v.mag()` / `v.magSq()` | `v.length()` / `v.length_squared()` | |
| `PVector.dist(a, b)` | `a.distance(b)` | |
| `v.rotate(-PI/2)` | `Vec2::new(v.y, -v.x)` (= `-v.perp()`) | `perp()` is `+90°` = `(-y, x)`; the source's `-90°` is its negation — verify the sign on screen |
| `PVector.lerp(a, b, t)` | `a.lerp(b, t)` | |
| `PI`, `TWO_PI`, `HALF_PI` | `std::f32::consts::{PI, TAU, FRAC_PI_2}` | use the consts, not literals |
| angle wrap to `[0, 2π)` | `theta.rem_euclid(TAU)` | the `simplifyAngle` helper |
| `mouseX, mouseY` | `Camera::viewport_to_world_2d(&GlobalTransform, cursor)` | returns `Result` in 0.18 — handle with `let Ok(..) = .. else { return }` |

### 3.2. The y-down to y-up Checklist

Processing's screen is y-**down**; Bevy is y-**up**. Run this checklist on any port:

- **Gravity** points `Vec2::NEG_Y * g` (down = negative y), not `+y`.
- **Body outline sides** at `±π/2` swap left/right on screen — the formula is unchanged; verify the silhouette visually.
- **Soft-body area normal** does *not* flip — the source's `rotate(-HALF_PI)` ports literally to `Vec2::new(s.y, -s.x)` (= `-secant.perp()`) because the ring keeps its increasing-angle winding. The trap is "fixing" it to `secant.perp()` (a +90° rotation) or reversing the winding. If the blob implodes, normal and winding disagree.
- **Rotations**: Processing's `rotate(-PI/2)` is `(y, -x)` — the *negation* of glam's `perp()` (+90°), not `perp()` itself. Port the algebra literally rather than by visual intuition, then verify which on-screen side you got.

### 3.3. Correctness Gotchas

The bugs most likely to survive a port because the code still *runs*:

1. **`relative_angle_diff` sign.** Must be `PI - simplify_angle(angle + PI - anchor)`. The mirror form `simplify(angle - anchor + PI) - PI` is its negation and clamps joints to the *wrong* cone edge.
2. **`heading` subtraction order.** The forward chain measures `(joints[i-1] - joints[i]).to_angle()` (child → parent). Reverse it and the measured heading shifts by π, so every joint slams to a cone edge and the spine coils at maximum bend instead of trailing. (An actually *mirrored* creature points to an angle negation — gotcha 1 — or a flipped ±π/2 side, not to this.)
3. **`normalize_or_zero` everywhere.** Any delta between two points can be zero (coincident joints, target on a joint); `normalize` yields NaN there (it panics only under the opt-in `glam_assert` feature) and the NaN spreads silently through every later position. `normalize_or_zero` is safe.
4. **Shoelace winding vs area-normal direction.** They are coupled (see [§3.2](#32-the-y-down-to-y-up-checklist)); a positive (CCW) area needs the `(s.y, -s.x)` outward normal. Mismatch ⇒ the soft body collapses.
5. **FABRIK anchor/target order.** Forward end = the reaching target, backward end = the fixed anchor. The leg's anchor (shoulder) is recomputed every frame from the moving spine.
6. **Δt² convention.** The source uses an implicit unit timestep, so gravity is a per-tick constant. Under `FixedUpdate` keep that form and tune `g`; don't fold `time.delta_secs()` into the `(pos - prev)` inertia term while leaving gravity unit-treated — the two terms then scale inconsistently and the body drifts.
7. **Jacobi accumulator reset.** Zero `disp`/`weight` after applying each iteration; `apply` divides by the count. Forget the reset and corrections compound until the body explodes.
8. **Runtime-mutated meshes.** Import `RenderAssetUsages` from `bevy::asset` (not `bevy::render` — re-export dropped in 0.17) and build with `RenderAssetUsages::default()`; `RENDER_WORLD`-only drops the CPU copy and per-frame `meshes.get_mut` updates stall. `gizmos.circle_2d` takes an `Isometry2d` (a `Vec2` coerces via `Into`); `Camera2dBundle` was removed in 0.16 — spawn the `Camera2d` component.

## Sources

- argonautcode — [animal-proc-anim](https://github.com/argonautcode/animal-proc-anim) and [soft-body-proc-anim](https://github.com/argonautcode/soft-body-proc-anim), with the videos [*A simple procedural animation technique*](https://www.youtube.com/watch?v=qlfh_rv6khY) and [*Simulating soft body animals*](https://www.youtube.com/watch?v=GXh0Vxg7AnQ).
- zalo — [*Constraints*](https://zalo.github.io/blog/constraints/) and [*Inverse Kinematics*](https://zalo.github.io/blog/inverse-kinematics/).
- Ken Perlin (*Improving Noise*), Robert Bridson (*Fast Poisson Disk Sampling*), Prusinkiewicz & Lindenmayer (*The Algorithmic Beauty of Plants*), Maxim Gumin (*Wave Function Collapse*).
- In this knowledge base: the [Bevy](software/bevy.md) guide, [Procedural Generation in Game Design](software/books/procedural-generation-in-game-design/book_summary.md), [Procedural Storytelling in Game Design](software/books/procedural-storytelling-in-game-design/book_summary.md).
- Back to the [Overview](software/procedural/README.md).
