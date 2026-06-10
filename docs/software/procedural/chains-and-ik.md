# Kinematic Chains & Inverse Kinematics

> *Animation throughline.* A chain is just the distance constraint from [Foundations](software/procedural/foundations.md) repeated along a row of joints, optionally with **angle constraints** added. Two solvers cover most needs: a **forward "follow-the-leader" pass** for a spine that trails a moving head, and **FABRIK** for a limb that must reach a target from a fixed root. We finish with a comparison of all the common IK methods so you can pick the right one. Examples use Bevy `0.18`.

## Table of Contents

- [1. A Chain Is a Sequence of Constraints](#1-a-chain-is-a-sequence-of-constraints)
- [2. Angle Constraints](#2-angle-constraints)
  - [2.1. Representing and Wrapping Angles](#21-representing-and-wrapping-angles)
  - [2.2. Constraining an Angle to a Cone](#22-constraining-an-angle-to-a-cone)
  - [2.3. In Bevy](#23-in-bevy)
- [3. The Forward Chain (Follow-the-Leader)](#3-the-forward-chain-follow-the-leader)
  - [3.1. The Algorithm](#31-the-algorithm)
  - [3.2. Why This for a Spine](#32-why-this-for-a-spine)
  - [3.3. Worked Example: A Chain That Follows the Cursor](#33-worked-example-a-chain-that-follows-the-cursor)
- [4. FABRIK](#4-fabrik)
  - [4.1. The Two Passes](#41-the-two-passes)
  - [4.2. Why This for Limbs](#42-why-this-for-limbs)
  - [4.3. Worked Example: A FABRIK Arm](#43-worked-example-a-fabrik-arm)
- [5. Choosing an IK Method](#5-choosing-an-ik-method)
  - [5.1. FABRIK](#51-fabrik)
  - [5.2. CCD and CCDIK](#52-ccd-and-ccdik)
  - [5.3. Jacobian Transpose](#53-jacobian-transpose)
  - [5.4. Analytic (Two-Bone)](#54-analytic-two-bone)
  - [5.5. Autodiff and Gradient Descent](#55-autodiff-and-gradient-descent)
  - [5.6. Comparison Table](#56-comparison-table)
- [Sources](#sources)

## 1. A Chain Is a Sequence of Constraints

Take \( n \) joints in a row. The link-length rule — "joint \( i \) is exactly \( L \) from joint \( i-1 \)" — is the [distance constraint](software/procedural/foundations.md#32-the-distance-constraint) applied \( n-1 \) times. That alone gives a floppy rope. To get a *creature's* spine or a robot arm you add a second rule: each joint may only bend so far relative to the one before it — an **angle constraint**. The two solvers below differ in how they combine these.

## 2. Angle Constraints

### 2.1. Representing and Wrapping Angles

Angles live on a circle, so \( 0 \) and \( 2\pi \) are the same heading and naive subtraction misbehaves near the wrap. Normalise into \( [0, 2\pi) \):

\[ \mathrm{simplify}(\theta) = \theta \bmod 2\pi \]

Then the **signed** rotation needed to turn a heading \( \theta \) onto an anchor heading \( \alpha \) — chosen to take the short way round, landing in \( (-\pi, \pi] \) — is:

\[ \mathrm{relDiff}(\theta, \alpha) = \pi - \mathrm{simplify}(\theta + \pi - \alpha) \]

This particular sign convention is load-bearing: it reduces to \( \mathrm{relDiff} = \alpha - \theta \), and the clamp below depends on it. The negated form \( \mathrm{simplify}(\theta - \alpha + \pi) - \pi \) looks equivalent but flips the sign, which would clamp a joint to the *wrong* limit.

### 2.2. Constraining an Angle to a Cone

To keep \( \theta \) within \( \pm c \) of the anchor \( \alpha \):

\[ \mathrm{constrain}(\theta, \alpha, c) = \begin{cases} \mathrm{simplify}(\theta) & |\mathrm{relDiff}(\theta,\alpha)| \le c \\ \mathrm{simplify}(\alpha - c) & \mathrm{relDiff}(\theta,\alpha) > c \\ \mathrm{simplify}(\alpha + c) & \text{otherwise} \end{cases} \]

In words: if the joint is already within the allowed cone, leave it; otherwise snap it to the nearer cone edge.

### 2.3. In Bevy

The Processing `PVector.heading()` maps to glam's `Vec2::to_angle()` (both are `atan2(y, x)`), and `PVector.fromAngle(a)` maps to `Vec2::from_angle(a)` (both are \( (\cos a, \sin a) \)). The wrap is `f32::rem_euclid`.

```rust
use bevy::prelude::*;
use std::f32::consts::{PI, TAU};

/// Wrap into [0, 2π).
fn simplify_angle(a: f32) -> f32 {
    a.rem_euclid(TAU)
}

/// Signed rotation that turns `angle` onto `anchor`, in (−π, π]. Sign matters — see §2.1.
fn relative_angle_diff(angle: f32, anchor: f32) -> f32 {
    PI - simplify_angle(angle + PI - anchor)
}

/// Clamp `angle` to within ±`constraint` of `anchor`.
fn constrain_angle(angle: f32, anchor: f32, constraint: f32) -> f32 {
    let diff = relative_angle_diff(angle, anchor);
    if diff.abs() <= constraint {
        simplify_angle(angle)
    } else if diff > constraint {
        simplify_angle(anchor - constraint)
    } else {
        simplify_angle(anchor + constraint)
    }
}
```

## 3. The Forward Chain (Follow-the-Leader)

### 3.1. The Algorithm

This is the resolver behind every creature spine in [Creature Rigging](software/procedural/creature-rigging.md). Joint 0 (the head) jumps straight to the target; every other joint trails its parent at a *constrained* angle and a fixed distance:

1. Set the head's heading to point at the target, then move the head to the target.
2. For each following joint \( i \): measure the heading from joint \( i \) toward its parent \( i-1 \); clamp that heading to within \( \pm c \) of the parent's heading; then place joint \( i \) one link-length back along the clamped heading:

\[ \theta_i = \mathrm{constrain}\big(\angle(\mathbf{j}_{i-1} - \mathbf{j}_i),\; \theta_{i-1},\; c\big), \qquad \mathbf{j}_i = \mathbf{j}_{i-1} - \hat{u}(\theta_i)\,L \]

where \( \hat u(\theta) = (\cos\theta, \sin\theta) \) and \( \angle(\cdot) \) is `to_angle`.

```rust
#[derive(Component)]
struct Chain {
    joints: Vec<Vec2>,
    angles: Vec<f32>,
    link_len: f32,
    angle_constraint: f32,
}

impl Chain {
    fn new(origin: Vec2, count: usize, link_len: f32, angle_constraint: f32) -> Self {
        let joints = (0..count)
            .map(|i| origin + Vec2::Y * (i as f32 * link_len))
            .collect();
        Self { joints, angles: vec![0.0; count], link_len, angle_constraint }
    }

    /// Head jumps to `target`; the body trails behind at constrained angles.
    fn resolve(&mut self, target: Vec2) {
        self.angles[0] = (target - self.joints[0]).to_angle();
        self.joints[0] = target;
        for i in 1..self.joints.len() {
            let cur = (self.joints[i - 1] - self.joints[i]).to_angle();
            self.angles[i] = constrain_angle(cur, self.angles[i - 1], self.angle_constraint);
            self.joints[i] = self.joints[i - 1] - Vec2::from_angle(self.angles[i]) * self.link_len;
        }
    }
}
```

The `angles` array is kept because the next page renders the body *perpendicular* to each joint's heading — the headings are a by-product worth storing.

### 3.2. Why This for a Spine

A spine has **no fixed root** — the head leads and the tail simply follows, lagging naturally like a fish. The forward pass models exactly that: one sweep, head to tail, with per-joint angle limits that prevent kinking (a real spine cannot fold back on itself). There is no second target to satisfy, so the two-ended FABRIK below would be overkill. The angle clamp is what makes it read as a *body* and not a wet noodle.

### 3.3. Worked Example: A Chain That Follows the Cursor

A complete program: a 12-joint chain whose head chases the mouse, each joint limited to \( \pm\pi/8 \) of bend. This also introduces **cursor→world conversion**, which `Camera::viewport_to_world_2d` provides (note it returns a `Result` in Bevy `0.18`).

```rust
use bevy::prelude::*;
use std::f32::consts::{PI, TAU};

// ... simplify_angle / relative_angle_diff / constrain_angle from §2.3 ...
// ... the Chain struct + impl from §3.1 ...

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .add_systems(Startup, setup)
        .add_systems(Update, (follow_cursor, draw).chain())
        .run();
}

fn setup(mut commands: Commands) {
    commands.spawn(Camera2d);
    commands.spawn(Chain::new(Vec2::ZERO, 12, 32.0, PI / 8.0));
}

/// Read the cursor in world space, or `None` if it is off-window.
fn cursor_world(
    windows: &Query<&Window>,
    cameras: &Query<(&Camera, &GlobalTransform)>,
) -> Option<Vec2> {
    let cursor = windows.single().ok()?.cursor_position()?;
    let (camera, transform) = cameras.single().ok()?;
    camera.viewport_to_world_2d(transform, cursor).ok()
}

fn follow_cursor(
    mut chains: Query<&mut Chain>,
    windows: Query<&Window>,
    cameras: Query<(&Camera, &GlobalTransform)>,
) {
    let Some(target) = cursor_world(&windows, &cameras) else {
        return;
    };
    for mut chain in &mut chains {
        chain.resolve(target);
    }
}

fn draw(mut gizmos: Gizmos, chains: Query<&Chain>) {
    for chain in &chains {
        for pair in chain.joints.windows(2) {
            gizmos.line_2d(pair[0], pair[1], Color::WHITE);
        }
        for &j in &chain.joints {
            gizmos.circle_2d(j, 6.0, Color::srgb(0.5, 0.8, 0.9));
        }
    }
}
```

Because there is no integrator here — the chain is purely *kinematic*, recomputed each frame from the cursor — it can run in `Update`. Lower the `PI / 8.0` constraint toward `0.0` and the chain stiffens into a near-rigid rod; raise it to `PI` and the clamp never engages — the chain coils freely.

## 4. FABRIK

**FABRIK** — Forward And Backward Reaching Inverse Kinematics — bends a chain so its tip reaches a target *while* its root stays anchored. It is nothing but the distance constraint again, swept in two directions.

### 4.1. The Two Passes

Per iteration:

- **Forward reach** — move the tip onto the target, then walk down the chain projecting each joint to be exactly \( L \) from the one just moved. The tip now hits the target but the root has drifted.
- **Backward reach** — move the root back onto its anchor, then walk back up projecting each joint to be \( L \) from the one just moved. The root is restored; the tip drifts slightly.

Each pass trades one error for a smaller one; repeating converges on a pose that satisfies both ends.

```rust
/// Reach `target` from a fixed `anchor`, preserving link length. `joints[0]`
/// is the tip (pulled to the target); `joints[last]` is the root (pinned to
/// the anchor). Reuses `constrain_distance` from Foundations §3.3.
fn fabrik_resolve(
    joints: &mut [Vec2],
    link_len: f32,
    target: Vec2,
    anchor: Vec2,
    iterations: usize,
) {
    let n = joints.len();
    for _ in 0..iterations {
        joints[0] = target;                                   // forward pass
        for i in 1..n {
            joints[i] = constrain_distance(joints[i], joints[i - 1], link_len);
        }
        joints[n - 1] = anchor;                               // backward pass
        for i in (0..n - 1).rev() {
            joints[i] = constrain_distance(joints[i], joints[i + 1], link_len);
        }
    }
}
```

The original source runs a **single** forward+backward pass per frame and lets continuous re-solving converge over frames (fine when the target moves slowly). For a static reach, loop `iterations` times (≈ 10 is plenty) to converge within one frame.

### 4.2. Why This for Limbs

A leg differs from a spine in one decisive way: it has **two fixed ends**. The foot wants to reach a planted target *and* the hip stays attached to the body. FABRIK satisfies both simultaneously, needs no trigonometry, handles many bones, and when the target is out of reach it degrades gracefully to a straight, fully-extended limb. The forward chain of [§3](#3-the-forward-chain-follow-the-leader) cannot do this — it has only one controlled end. (In [Creature Rigging](software/procedural/creature-rigging.md) each lizard leg is a three-joint FABRIK chain whose anchor is recomputed every frame from the moving spine.)

### 4.3. Worked Example: A FABRIK Arm

Reusing the scaffold from [§3.3](#33-worked-example-a-chain-that-follows-the-cursor) (`cursor_world`, `DefaultPlugins`), the differences are: store the joints in a component, anchor the root at a fixed point below centre, and drive the tip to the cursor. `setup_arm` *replaces* §3.3's `setup` — keep exactly one camera, or `cameras.single()` errors and the arm never moves.

```rust
#[derive(Component)]
struct Arm {
    joints: Vec<Vec2>, // joints[0] = hand (reaches), joints[last] = shoulder (anchored)
    link_len: f32,
    anchor: Vec2,
}

fn setup_arm(mut commands: Commands) {
    commands.spawn(Camera2d);
    let anchor = Vec2::new(0.0, -100.0);
    let link_len = 60.0;
    let joints = (0..4).map(|i| anchor + Vec2::Y * (i as f32 * link_len)).collect();
    commands.spawn(Arm { joints, link_len, anchor });
}

fn reach_cursor(
    mut arms: Query<&mut Arm>,
    windows: Query<&Window>,
    cameras: Query<(&Camera, &GlobalTransform)>,
) {
    let Some(target) = cursor_world(&windows, &cameras) else {
        return;
    };
    for mut arm in &mut arms {
        let (link, anchor) = (arm.link_len, arm.anchor);
        fabrik_resolve(&mut arm.joints, link, target, anchor, 10);
    }
}
```

Drive the shoulder from a moving body instead of a fixed point and you have a limb; that is precisely the next page.

## 5. Choosing an IK Method

FABRIK is one of several ways to solve inverse kinematics. Knowing the alternatives lets you pick deliberately.

### 5.1. FABRIK

Position-based, heuristic, iterative. Fast, trig-free, scales to long chains, and joint limits drop in by clamping each projected joint. Downsides: it can look "rubbery", and it controls joint *positions*, not end-effector *orientation*. The default for game creatures and tentacles.

### 5.2. CCD and CCDIK

**Cyclic Coordinate Descent** sweeps from the tip's neighbour down to the root; at each joint it rotates the entire sub-chain so the end-effector points at the goal:

```text
for joint in (tip-1 ..= root):          // base-ward sweep
    to_end  = end_effector - joint.pos
    to_goal = goal         - joint.pos
    rotate the sub-chain past `joint` by  angle(to_goal) - angle(to_end)
    clamp joint to its angle limits
```

CCDIK shines when joints have **hard limits** (hinges, euler clamps) — zalo's post applies it in 3D with quaternion `rotateFromTo` and per-joint euler clamping. Plain CCD without limits tends to over-bend the joints nearest the tip, giving a characteristic curl.

### 5.3. Jacobian Transpose

A force-based gradient method: build the Jacobian relating joint-angle changes to end-effector motion, then step the joints along its transpose toward the goal. Smooth and able to juggle multiple goals or redundant joints, but slow, sensitive to its step size, and prone to stalling near singularities (a fully-extended limb). Used more in robotics than games.

### 5.4. Analytic (Two-Bone)

For exactly two bones (the common arm/leg case) the answer is **closed-form** — no iteration. The interior knee angle comes straight from the law of cosines, with \( d \) the root-to-target distance:

\[ \cos\gamma = \frac{l_1^2 + l_2^2 - d^2}{2\,l_1 l_2} \]

valid when the target is reachable, \( |l_1 - l_2| \le d \le l_1 + l_2 \) (clamp \( d \) into that range otherwise). Exact, instant, and stable — the right tool for a humanoid limb where you also want to control which way the knee points.

### 5.5. Autodiff and Gradient Descent

Define a loss (squared distance to the goal plus penalties for exceeding joint limits) and let automatic differentiation minimise it. The most flexible — arbitrary objectives, soft constraints, any number of goals — but the heaviest, and overkill for the simple reaches games usually need.

### 5.6. Comparison Table

| Method | Type | Joint limits | Speed | Behaviour | Orientation control | Best for |
|---|---|---|---|---|---|---|
| **FABRIK** | Position, iterative | Easy (clamp each joint) | Fast | Can look rubbery | No (positions only) | Game creatures, long chains |
| **CCD / CCDIK** | Angle, iterative | Easy & natural (hinges) | Fast | Curls near the tip | Partial | Hard-limited joints, robot arms |
| **Jacobian transpose** | Force, iterative | Via penalties | Slow | Smooth | Yes | Redundant chains, multi-goal |
| **Analytic (2-bone)** | Closed form | Built into the geometry | Instant | Exact | Yes (pole vector) | Humanoid arms/legs (≤ 2 bones) |
| **Autodiff / gradient** | Optimisation | Soft (loss penalties) | Slowest | Whatever you optimise | Yes | Research, arbitrary objectives |

## Sources

- zalo — [*Inverse Kinematics*](https://zalo.github.io/blog/inverse-kinematics/) (CCDIK, the method comparison) and [*Constraints*](https://zalo.github.io/blog/constraints/) (FABRIK as iterated distance constraints).
- argonautcode — [animal-proc-anim](https://github.com/argonautcode/animal-proc-anim) (`Chain.resolve`, `fabrikResolve`, the angle helpers).
- Next: [Creature Rigging](software/procedural/creature-rigging.md) puts a body on the spine and a gait on the legs.
