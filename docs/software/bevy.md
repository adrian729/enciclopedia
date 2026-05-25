# Bevy

A topic-organised guide to Rust and the Bevy game engine. Each section covers a concept once and applies to any game built on Bevy. Snippets use Bevy `0.18`.

## Table of Contents

- [1. Setup](#1-setup)
  - [1.1. Toolchain](#11-toolchain)
  - [1.2. Creating a Project](#12-creating-a-project)
  - [1.3. Cargo.toml (Recommended Profile)](#13-cargotoml-recommended-profile)
  - [1.4. Project Layout](#14-project-layout)
  - [1.5. Asset Path and Renderer Configuration](#15-asset-path-and-renderer-configuration)
- [2. Rust Essentials for Bevy](#2-rust-essentials-for-bevy)
  - [2.1. Type System and Memory Layout](#21-type-system-and-memory-layout)
  - [2.2. Mutability, Ownership, Borrowing](#22-mutability-ownership-borrowing)
  - [2.3. Lifetimes and Strings](#23-lifetimes-and-strings)
  - [2.4. Structs and Enums](#24-structs-and-enums)
  - [2.5. Expressions and Returns](#25-expressions-and-returns)
  - [2.6. Derive Macros](#26-derive-macros)
  - [2.7. Modules and Visibility](#27-modules-and-visibility)
  - [2.8. Traits](#28-traits)
  - [2.9. Generics and Trait Bounds](#29-generics-and-trait-bounds)
  - [2.10. Closures and Function Pointers](#210-closures-and-function-pointers)
  - [2.11. Pattern Matching with Result and Option](#211-pattern-matching-with-result-and-option)
- [3. Bevy Architecture](#3-bevy-architecture)
  - [3.1. The ECS Model](#31-the-ecs-model)
  - [3.2. App and Main Loop](#32-app-and-main-loop)
  - [3.3. Schedules](#33-schedules)
  - [3.4. Plugins](#34-plugins)
  - [3.5. Resources vs Components](#35-resources-vs-components)
  - [3.6. The Prelude](#36-the-prelude)
- [4. Systems and Data Access](#4-systems-and-data-access)
  - [4.1. Systems as Functions](#41-systems-as-functions)
  - [4.2. System Parameters (Dependency Injection)](#42-system-parameters-dependency-injection)
  - [4.3. Commands](#43-commands)
  - [4.4. Queries and Filters](#44-queries-and-filters)
  - [4.5. Bundles](#45-bundles)
- [5. Common APIs and Types](#5-common-apis-and-types)
  - [5.1. Transform](#51-transform)
  - [5.2. Time and Frame-Rate Independence](#52-time-and-frame-rate-independence)
  - [5.3. Input](#53-input)
  - [5.4. Timers](#54-timers)
  - [5.5. Math Types](#55-math-types)
  - [5.6. Color and ClearColor](#56-color-and-clearcolor)
  - [5.7. Cameras](#57-cameras)
  - [5.8. Sprites and Texture Atlases](#58-sprites-and-texture-atlases)
  - [5.9. 2D Text](#59-2d-text)
  - [5.10. AssetServer and Handles](#510-assetserver-and-handles)
  - [5.11. Window and Pixel-Art Configuration](#511-window-and-pixel-art-configuration)
- [6. Patterns and Idioms](#6-patterns-and-idioms)
  - [6.1. Marker Components](#61-marker-components)
  - [6.2. Setup + Update Pattern](#62-setup--update-pattern)
  - [6.3. Plugin-First Organization](#63-plugin-first-organization)
  - [6.4. Component Composition](#64-component-composition)
  - [6.5. Constants over Magic Numbers](#65-constants-over-magic-numbers)
  - [6.6. Early-Return Error Handling in Systems](#66-early-return-error-handling-in-systems)
  - [6.7. Y-Sorted Z-Ordering for 2D Top-Down](#67-y-sorted-z-ordering-for-2d-top-down)

## 1. Setup

### 1.1. Toolchain

Install Rust through `rustup`; it manages compiler versions and `cargo`, the package manager and build tool.

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

### 1.2. Creating a Project

```bash
cargo new my_game
cd my_game
```

`cargo new` scaffolds `Cargo.toml` and `src/main.rs`. `cargo run` compiles and runs; `cargo build --release` produces an optimised binary.

### 1.3. Cargo.toml (Recommended Profile)

```toml
[package]
name = "my_game"
version = "0.1.0"
edition = "2024"

[dependencies]
bevy = { version = "0.18.1", features = ["dynamic_linking"] }
log = { version = "*", features = ["max_level_debug", "release_max_level_warn"] }

[profile.dev]
opt-level = 1

[profile.dev.package."*"]
opt-level = 3

# Remove expensive debug assertions due to <https://github.com/bevyengine/bevy/issues/14291>
[profile.dev.package.wgpu-types]
debug-assertions = false

[profile.release]
codegen-units = 1 # Compile the entire crate as one unit. Marginal improvements.
lto = "thin" # Second optimization pass. Marginal improvements.
```

What each tweak does:

- **`bevy` feature `dynamic_linking`** — links Bevy as a dynamic library so iterative dev rebuilds are dramatically faster. Drop it for release builds.
- **`log` `max_level_debug` / `release_max_level_warn`** — keep `debug!`/`info!` calls in dev, compile out anything below `warn` in release (zero runtime cost for stripped logs).
- **`[profile.dev]` `opt-level = 1`** — light optimisation of your own crate so the dev binary is fast enough to actually play.
- **`[profile.dev.package."*"]` `opt-level = 3`** — fully optimise every dependency. They're compiled once and reused, so the cost is paid once.
- **`[profile.dev.package.wgpu-types]` `debug-assertions = false`** — workaround for [bevy#14291](https://github.com/bevyengine/bevy/issues/14291); `wgpu-types` has expensive debug assertions that tank dev framerates.
- **`[profile.release]` `codegen-units = 1` + `lto = "thin"`** — single-unit codegen and link-time optimisation. Marginal release-mode perf gains at the cost of longer link times.

### 1.4. Project Layout

```
my_game/
├── Cargo.toml
└── src/
    ├── main.rs       # App wiring, plugin list
    ├── player.rs     # One module per feature
    ├── world.rs
    └── assets/       # PNGs, fonts, audio
```

Split features into modules early. A `main.rs` that imports a handful of feature plugins reads far better than one with hundreds of systems. For a feature large enough to warrant several files, promote it to a directory with a `mod.rs` that re-exports its sub-modules:

```
src/world/
├── mod.rs        # `pub mod tiles; pub mod spawn; …`
├── tiles.rs
└── spawn.rs
```

`mod.rs` acts as a table of contents for the directory; consumers still write `use crate::world::spawn::*`.

### 1.5. Asset Path and Renderer Configuration

By default Bevy loads from `assets/` at the crate root. Override Bevy's default plugins via `.set(<Plugin>)`, which replaces a single plugin in the stack without rebuilding it:

```rust
.add_plugins(
    DefaultPlugins
        .set(AssetPlugin {
            file_path: "src/assets".into(),
            ..default()
        })
        .set(ImagePlugin::default_nearest()),
)
```

- **`AssetPlugin.file_path`** — points the asset server at any directory you like.
- **`ImagePlugin::default_nearest()`** — switches the default sampler to nearest-neighbour filtering. Use this for pixel art so textures aren't smoothed when scaled.

`..default()` fills any unspecified fields from the type's `Default` impl — idiomatic for partially overriding Bevy config structs.

## 2. Rust Essentials for Bevy

### 2.1. Type System and Memory Layout

Rust is statically typed. Every value has a known size at compile time, packed without runtime metadata. A `Vec2` of two `f32`s occupies exactly 8 bytes — no hidden header, no boxing — which is what makes ECS storage cache-friendly.

### 2.2. Mutability, Ownership, Borrowing

- Variables are immutable by default; `mut` opts in. Function parameters follow the same rule: `mut commands: Commands` signals the system mutates it.
- Each value has one owner. Assignment **moves** ownership; the source becomes unusable unless the type implements `Copy` (cheap-to-duplicate types like primitives and `Vec2`).
- Borrows let other code read (`&T`) or mutate (`&mut T`) without taking ownership. The compiler enforces that you have either one mutable borrow or any number of shared borrows — never both. Bevy's system scheduler uses this to run non-conflicting systems in parallel.

### 2.3. Lifetimes and Strings

A **lifetime** is Rust's way of tracking how long borrowed data stays valid. The compiler refuses to let a reference outlive what it points to. Most lifetimes are inferred; the one you write by hand most often is `'static` — "lives for the entire program."

The canonical `'static` value is a string literal: it's baked into the executable, so a reference to it is valid forever.

```rust
const SPRITE_KEY: &'static str = "hero_idle";  // baked into the binary
```

Three string types you'll meet:

| Type | Owned? | Mutable? | Notes |
|---|---|---|---|
| `&str` | No (borrowed slice) | No | A view into UTF-8 bytes owned by something else |
| `&'static str` | No | No | A `&str` that lives forever — typically a string literal |
| `String` | Yes (heap) | Yes | Grow-able owned text |

Rule of thumb: use `&'static str` for compile-time-known names (asset keys, tags, marker labels); use `String` when text is built or read at runtime; accept `&str` in function parameters that don't need ownership.

### 2.4. Structs and Enums

Use a **struct** when you need several fields:

```rust
struct Position { x: f32, y: f32 }
```

Use an **enum** when a value is one of a fixed set of variants:

```rust
enum Facing { Up, Down, Left, Right }
```

Enums replace constellations of booleans (`is_up`, `is_down`, …) with a type-checked single choice that pattern matching forces you to handle exhaustively.

### 2.5. Expressions and Returns

Rust is expression-oriented: nearly everything produces a value, and the final expression of a block is its value. A function returns whatever its last expression evaluates to — no `return` keyword and no trailing semicolon.

```rust
fn double(x: i32) -> i32 {
    x * 2  // last expression, no semicolon — this is the return value
}
```

The same shape works for constructors:

```rust
impl Bullet {
    pub fn new(damage: f32) -> Self {
        Self { damage, lifetime: 0.0 }
    }
}
```

`Self` is a type alias for "the type this `impl` block is for." It saves repeating the name and keeps the constructor stable if the type is renamed. Use an explicit `return` only to short-circuit out of the middle of a function.

### 2.6. Derive Macros

`#[derive(...)]` auto-generates boilerplate implementations. Common ones in Bevy code:

| Macro | Purpose |
|---|---|
| `Component` | Marks the type as attachable to entities. |
| `Resource` | Marks the type as a global, singleton-style resource. |
| `Debug` | Enables `{:?}` formatting for logs. |
| `Clone`, `Copy` | Cheap duplication; `Copy` makes moves implicit copies. |
| `PartialEq`, `Eq` | Enables `==` comparison. |
| `Default` | Provides `Type::default()` and lets `..default()` work. |
| `Deref`, `DerefMut` | Newtype wrapper transparently exposes its inner type's methods. |

### 2.7. Modules and Visibility

Each `.rs` file is a module. Declare it in the parent with `mod`, expose items with `pub`:

```rust
// main.rs
mod player;
use player::PlayerPlugin;

// player.rs
pub struct PlayerPlugin;
pub fn spawn_player(/* ... */) { /* ... */ }
```

Without `pub`, an item is crate-private. For a directory module, `mod.rs` is the entry point and re-exports child modules:

```rust
// src/world/mod.rs
pub mod tiles;
pub mod spawn;
```

Consumers then write `use crate::world::spawn::SpawnPoint`. Use module boundaries to enforce a public surface and keep internals private.

### 2.8. Traits

Traits are interface contracts. The most important one for Bevy is `Plugin`:

```rust
pub trait Plugin {
    fn build(&self, app: &mut App);
}
```

Anything implementing `Plugin` can be added to the app. The trait system also underlies `IntoSystem`, `Bundle`, `Component`, and many other Bevy concepts — they all boil down to "this type implements trait X, so Bevy knows how to handle it".

### 2.9. Generics and Trait Bounds

Generics let one type or function work across many types without giving up compile-time safety. They are everywhere in Bevy:

| Generic | What it parameterizes |
|---|---|
| `Query<D, F>` | The component shape to fetch and the filter |
| `Handle<T>` | The asset type the handle points to |
| `Res<T>` / `ResMut<T>` | The resource type |
| `Assets<T>` | The asset type in storage |
| `EventReader<E>` / `EventWriter<E>` | The event type |

**Trait bounds** restrict what a generic type can be. A `where` clause keeps the signature readable when bounds get involved:

```rust
fn add_to_world<B>(commands: &mut Commands, bundle: B)
where
    B: Bundle,
{
    commands.spawn(bundle);
}
```

`Into<T>` is a particularly common bound — it lets callers pass anything that can be converted into the expected type, sparing them an explicit conversion:

```rust
fn tint<C: Into<Color>>(c: C) -> Sprite { /* … */ }
tint(Color::WHITE);                            // Color: Into<Color>
tint(LinearRgba::new(1.0, 0.5, 0.0, 1.0));     // LinearRgba: Into<Color>
```

The same shape generalises to "accept anything convertible into my domain type" — useful for ergonomic constructors and builder methods.

### 2.10. Closures and Function Pointers

A **closure** is an inline anonymous function that can capture variables from its surrounding scope. Bevy uses them for one-off callbacks, builder hooks, and observer logic.

```rust
let speed = 50.0;
let stride = |dt: f32| dt * speed;   // captures `speed`
let do_nothing = |_| {};             // ignores its argument
```

A **function pointer** is the type `fn(...) -> ...` — a non-capturing function passed as a value. Use it where the callback must be plain data, e.g. a `const` lookup table of per-variant behaviour:

```rust
struct ScoreRule {
    apply: fn(&mut u32, u32),
}

const DOUBLE_BONUS: ScoreRule = ScoreRule {
    apply: |total, points| { *total += points * 2; },
};
```

Rules of thumb: reach for a closure when you need to capture local state; reach for `fn(...)` when the callback must be `Copy` and storable in a `const` or `static`.

### 2.11. Pattern Matching with Result and Option

Bevy APIs return `Result` or `Option` when an operation may legitimately fail (e.g. a query that should yield exactly one entity). Use `let … else` to bind on success and short-circuit on failure:

```rust
let Ok((mut transform, mut anim)) = query.single_mut() else { return; };
let Some(handle) = assets.get(&key) else { return; };
```

For exhaustive branching, use `match`:

```rust
match facing {
    Facing::Up => /* … */,
    Facing::Down => /* … */,
    Facing::Left => /* … */,
    Facing::Right => /* … */,
}
```

The compiler refuses to compile a non-exhaustive `match` over an enum, so adding a variant flushes out every site that must update.

## 3. Bevy Architecture

### 3.1. The ECS Model

Bevy is an **Entity Component System**:

- **Entity** — a bare ID. Conceptually a row key.
- **Component** — a piece of data attached to an entity (`Transform`, `Velocity`, `Health`, a custom marker). Conceptually a column.
- **System** — a function that queries entities by their component shape and operates on them.

Behaviour lives in systems; data lives in components; there is no class hierarchy. Composition beats inheritance — give an entity exactly the components it needs.

### 3.2. App and Main Loop

`App` wires everything together. A minimal entry point:

```rust
use bevy::prelude::*;

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .add_systems(Startup, setup)
        .add_systems(Update, tick)
        .run();
}
```

- `DefaultPlugins` registers rendering, windowing, input, audio, asset loading, logging — the standard stack.
- `add_systems(<schedule>, <system>)` registers a function to run on that schedule. Pass a tuple to register several at once: `add_systems(Startup, (setup_camera, setup_world))`.
- `run()` hands control to Bevy: it opens a window, then enters the loop (poll input → run schedules → render).

### 3.3. Schedules

Schedules are named points in the frame at which a set of systems runs. Two are universal:

- **`Startup`** — runs once before the first frame. Spawn the camera, load static assets, configure resources.
- **`Update`** — runs every frame. Read input, advance simulation, update transforms.

Bevy ships more schedules (`PreUpdate`, `PostUpdate`, `FixedUpdate`, …); each lets you place a system precisely in the frame pipeline.

### 3.4. Plugins

A plugin bundles related systems, resources, and setup behind a single `add_plugins` call. Define one per feature:

```rust
pub struct PlayerPlugin;

impl Plugin for PlayerPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Startup, spawn_player)
            .add_systems(Update, (handle_input, animate));
    }
}

// main.rs
App::new()
    .add_plugins((DefaultPlugins, PlayerPlugin, WorldPlugin, UiPlugin))
    .run();
```

`main.rs` stays a one-screen overview of the game's modules.

Plugins can themselves be generic. Library plugins frequently parameterize over coordinate spaces or data shapes:

```rust
.add_plugins(MyLibPlugin::<GridSpace, Sprite>::default())
```

The turbofish (`::<...>`) supplies the generic arguments; default plugin configuration usually comes from `Default`.

### 3.5. Resources vs Components

| | Components | Resources |
|---|---|---|
| Scope | Attached to specific entities | One global instance per type |
| Access | `Query<&T>` / `Query<&mut T>` | `Res<T>` / `ResMut<T>` |
| Examples | `Transform`, `Health`, `Velocity` | `Time`, `ButtonInput<KeyCode>`, `ClearColor` |

Use a resource for "the world has one of these" data (score, current level, settings). Use components for "many things each have one of these" data (positions, hitboxes).

### 3.6. The Prelude

```rust
use bevy::prelude::*;
```

Re-exports the types you reach for constantly: `App`, `Commands`, `Query`, `Res`, `ResMut`, `Transform`, `Vec2`, `Vec3`, common components and bundles, the `default()` helper, etc. Subsystem-specific items still need explicit imports.

## 4. Systems and Data Access

### 4.1. Systems as Functions

A system is a plain function. Bevy inspects its parameter list to wire up the right data:

```rust
fn move_things(time: Res<Time>, mut q: Query<&mut Transform, With<Mover>>) {
    for mut t in &mut q {
        t.translation.x += time.delta_secs() * 50.0;
    }
}
```

Return type is typically `()`. Each parameter declares what the system reads or mutates — that declaration is what lets the scheduler run independent systems in parallel.

### 4.2. System Parameters (Dependency Injection)

| Parameter | What it gives you |
|---|---|
| `Res<T>` | Shared read of a resource. |
| `ResMut<T>` | Exclusive write of a resource. |
| `Query<D, F>` | Iterate entities matching the component shape `D` and filters `F`. |
| `Commands` | Defer entity spawn/despawn and component insert/remove. |
| `EventReader<E>` / `EventWriter<E>` | Read/emit frame-buffered events. |
| `Local<T>` | Per-system persistent state. |

You can add as many parameters as you need; Bevy resolves them by type.

### 4.3. Commands

`Commands` queues structural changes (spawn, despawn, insert, remove). They apply at the next sync point, which is why they're cheap to issue from any system:

```rust
fn spawn_player(mut commands: Commands, asset_server: Res<AssetServer>) {
    commands.spawn((
        Player,
        Transform::from_translation(Vec3::ZERO),
        Sprite::from_image(asset_server.load("sprites/player.png")),
    ));
}
```

### 4.4. Queries and Filters

A query has two type parameters: **what to fetch** and **how to filter**.

```rust
// Fetch: mutable Transform + read-only AnimationState
// Filter: only entities tagged with Player
fn animate_player(
    mut q: Query<(&mut Transform, &AnimationState), With<Player>>,
) {
    for (mut tf, anim) in &mut q { /* … */ }
}
```

Common filters: `With<T>`, `Without<T>`, `Added<T>`, `Changed<T>`. When you expect exactly one match, use `single()` / `single_mut()` — they return a `Result` so you can short-circuit with `let Ok(...) else { return; }`.

### 4.5. Bundles

A bundle is a tuple (or named struct) of components inserted together. The shorthand `commands.spawn((A, B, C))` inserts components `A`, `B`, `C` on a new entity. Bevy ships ready-made bundles for common archetypes (sprites, cameras, text) so you don't list every required component by hand.

## 5. Common APIs and Types

### 5.1. Transform

`Transform` is the universal position/rotation/scale component.

```rust
Transform::from_translation(Vec3::new(10.0, 0.0, 0.0))
Transform::from_xyz(10.0, 0.0, 0.0)
// uniform scale via splat
Transform::from_xyz(0.0, 0.0, 0.0).with_scale(Vec3::splat(0.8))
// inside a system:
transform.translation.x += 1.0;
transform.rotate_z(angle);
```

### 5.2. Time and Frame-Rate Independence

`Res<Time>` exposes per-frame timing. Multiply velocities by `time.delta_secs()` so motion is frame-rate independent:

```rust
fn move_player(time: Res<Time>, mut q: Query<&mut Transform, With<Player>>) {
    let Ok(mut tf) = q.single_mut() else { return; };
    tf.translation.x += SPEED * time.delta_secs();
}
```

### 5.3. Input

`Res<ButtonInput<KeyCode>>` (and the equivalent for mouse buttons / gamepad buttons) exposes the current frame's button state:

```rust
if input.pressed(KeyCode::ArrowLeft)  { /* held */ }
if input.just_pressed(KeyCode::Space) { /* pressed this frame */ }
if input.just_released(KeyCode::KeyE) { /* released this frame */ }
```

Mouse buttons use `Res<ButtonInput<MouseButton>>`; cursor motion comes from `EventReader<CursorMoved>` and scroll from `EventReader<MouseWheel>`.

### 5.4. Timers

`Timer` advances by a duration each tick and can fire once or repeatedly. Wrap one in a component (or resource) and tick it from a system:

```rust
#[derive(Component)]
struct AnimationTimer(Timer);

fn tick_animation(time: Res<Time>, mut q: Query<&mut AnimationTimer>) {
    for mut anim in &mut q {
        anim.0.tick(time.delta());
        if anim.0.just_finished() {
            /* advance animation frame, fire projectile, etc. */
        }
    }
}

// At spawn:
commands.spawn(AnimationTimer(Timer::from_seconds(0.1, TimerMode::Repeating)));
```

`TimerMode::Once` fires once and stops; `TimerMode::Repeating` resets after each fire.

### 5.5. Math Types

`Vec2`, `Vec3`, `Vec4`, `Quat`, `Mat3`, `Mat4` are re-exported from `glam`. Bevy also ships unsigned/integer variants used for pixel coordinates and image regions:

| Type | Purpose |
|---|---|
| `Vec2` / `Vec3` / `Vec4` | World-space floats. |
| `UVec2` / `IVec2` | Pixel and grid coordinates (unsigned / signed). |
| `URect` / `IRect` / `Rect` | Rectangular regions — used for atlas slicing, UI nodes, picking. |
| `Quat` | Rotations. Combine via multiplication; convert to/from axis-angle. |

Common operations:

```rust
Vec2::ZERO;          Vec3::ZERO;          Vec3::ONE;
Vec3::splat(0.8);    // (0.8, 0.8, 0.8) — uniform scale shorthand
v.normalize();       // length 1 (panics on zero vector — use normalize_or_zero)
v.length();          v.length_squared();
v.dot(other);        v.x.abs();

let region = URect::from_corners(UVec2::new(0, 0), UVec2::new(32, 32));
```

### 5.6. Color and ClearColor

`Color` constructors: `Color::WHITE`, `Color::srgb(r, g, b)`, `Color::srgba(r, g, b, a)`. The window's background is the `ClearColor` resource:

```rust
.insert_resource(ClearColor(Color::srgb(0.1, 0.1, 0.15)))
```

### 5.7. Cameras

For 2D, spawn a `Camera2d` once at startup. For 3D, `Camera3d` plus a `Transform` positioning it. Rendering happens only if a camera exists.

```rust
commands.spawn(Camera2d);
```

### 5.8. Sprites and Texture Atlases

A `Sprite` displays an image; a `TextureAtlas` packs many frames into one image and an index selects the current frame.

**Uniform grid atlas** — use `from_grid` when frames are the same size laid out in rows and columns:

```rust
let texture = asset_server.load("sprites/hero.png");
let layout = TextureAtlasLayout::from_grid(UVec2::splat(64), 9, 4, None, None);
let layout_handle = atlases.add(layout);

commands.spawn(Sprite::from_atlas_image(
    texture,
    TextureAtlas { layout: layout_handle, index: 0 },
));
```

Index math for a row-major grid: `index = row * columns + column`. To change rows (e.g. a walking direction change), reset the column to `0` of the new row.

**Non-uniform / hand-packed atlas** — when sprites differ in size or aren't laid out as a strict grid, build the layout by registering each rectangle:

```rust
let mut layout = TextureAtlasLayout::new_empty(atlas_size);
for region in &regions {
    layout.add_texture(URect::from_corners(region.min, region.min + region.size));
}
let layout_handle = atlases.add(layout);
```

Either approach yields a `Handle<TextureAtlasLayout>` that any number of `Sprite`s can reference by index.

A reusable wrapper that bundles the image handle and the layout handle keeps spawning concise:

```rust
struct AtlasHandles {
    image: Handle<Image>,
    layout: Handle<TextureAtlasLayout>,
}

impl AtlasHandles {
    fn sprite(&self, index: usize) -> Sprite {
        Sprite::from_atlas_image(
            self.image.clone(),
            TextureAtlas::from(self.layout.clone()).with_index(index),
        )
    }
}
```

`Handle` is cheap to clone — it's a reference-counted asset ID, not the asset data.

### 5.9. 2D Text

```rust
commands.spawn((
    Text2d::new("Hello"),
    TextFont { font: asset_server.load("fonts/main.ttf"), font_size: 32.0, ..default() },
    TextColor(Color::WHITE),
    Transform::from_xyz(0.0, 100.0, 0.0),
));
```

UI text (anchored to the screen, not the world) uses the `Text`/`Node` family from `bevy_ui` instead.

### 5.10. AssetServer and Handles

`Res<AssetServer>` loads files into asset storage. `load(path)` is non-blocking and returns a `Handle<T>` immediately; the actual load happens in the background and is deduplicated by path.

```rust
let icon: Handle<Image> = asset_server.load("ui/icon.png");
```

A `Handle<T>` is a typed reference to an asset, not the asset data itself. Properties:

- **Cheap to clone** — internally a small reference-counted ID.
- **Loaded lazily** — the asset may not be ready the frame you create the handle. Systems should treat "asset not yet present" as a normal state (see [6.6](#66-early-return-error-handling-in-systems)).
- **Deduplicated** — two `load("foo.png")` calls return handles to the same asset.
- **Reference-counted** — when the last handle is dropped, Bevy may unload the asset.

Hand the handle to components that reference the asset. The asset itself lives in `Assets<T>` (a resource), which you query with `Res<Assets<T>>` / `ResMut<Assets<T>>` and look up by handle.

A common pattern is to gather related handles into a single resource so any system can pull them out by type:

```rust
#[derive(Resource)]
struct SpriteHandles {
    image: Handle<Image>,
    layout: Handle<TextureAtlasLayout>,
}
```

### 5.11. Window and Pixel-Art Configuration

The primary window is configured by overriding `WindowPlugin` in the default plugin stack:

```rust
.add_plugins(
    DefaultPlugins
        .set(WindowPlugin {
            primary_window: Some(Window {
                resolution: WindowResolution::new(width, height),
                resizable: false,
                ..default()
            }),
            ..default()
        })
        .set(ImagePlugin::default_nearest()),
)
```

- **`Window.resolution`** — initial window size. Combine with a fixed camera scale for a known logical resolution.
- **`Window.resizable`** — disable when the rendering pipeline assumes a fixed size (e.g. tile-based games).
- **`ImagePlugin::default_nearest()`** — use nearest-neighbour filtering as the default sampler. Required for crisp pixel art; without it, scaled sprites get blurred by linear filtering.

You can chain as many `.set(...)` calls as needed; each one replaces a single plugin in the default stack.

## 6. Patterns and Idioms

### 6.1. Marker Components

Empty structs make tagging entities cheap and self-documenting:

```rust
#[derive(Component)] struct Player;
#[derive(Component)] struct Enemy;
#[derive(Component)] struct MainCamera;
```

Filter on them with `With<Player>` / `Without<Enemy>`. Far clearer than boolean flags on a fat component.

### 6.2. Setup + Update Pattern

Every feature tends to follow the same shape: one `Startup` system to create entities and one or more `Update` systems to evolve them. Plugins compose these two halves per feature.

### 6.3. Plugin-First Organization

Default to writing a `Plugin` for every feature. The cost is a four-line struct; the payoff is that `main.rs` stays a table of contents and features are trivial to swap, gate, or extract into a crate.

### 6.4. Component Composition

Prefer many small components over one large one. A `Bullet` entity might carry `Transform + Velocity + Damage + Lifetime + Sprite`. Systems that care about only `Velocity + Transform` (like the generic mover) automatically handle bullets, players, and everything else that opts in.

### 6.5. Constants over Magic Numbers

Name tuning values at the top of the file:

```rust
const MOVE_SPEED: f32 = 140.0;
const ANIM_INTERVAL: f32 = 0.1;
const TILE_SIZE: f32 = 64.0;
```

You'll iterate on them constantly. Centralising them keeps balancing painless. The same goes for layering: dedicate named constants to Z-axis bands (`const PLAYER_Z: f32 = 20.0;`) so render order never depends on a literal scattered across the codebase.

### 6.6. Early-Return Error Handling in Systems

Systems run every frame, so a missing entity or unready asset is normal — not an error. Use `let … else { return; }` rather than `unwrap` to avoid panics in the game loop:

```rust
fn drive_player(mut q: Query<&mut Transform, With<Player>>) {
    let Ok(mut tf) = q.single_mut() else { return; };
    // …
}
```

`unwrap` is acceptable in `Startup` for things that genuinely cannot fail (compile-time-known asset layouts, builder finalisation), since a panic at startup is easy to spot and fix; never use it in `Update`.

### 6.7. Y-Sorted Z-Ordering for 2D Top-Down

In 2D top-down games, entities lower on the screen should render in front of entities higher up — that's what makes a character feel like they're walking past a tree rather than through it. Bevy expresses depth via the `Z` axis of `Transform.translation`, so the trick is to derive `Z` from `Y`:

```rust
// In an update system, after positions change:
tf.translation.z = BASE_Z - tf.translation.y * Y_SORT_SCALE;
```

Many sprite/tilemap helpers offer a "Z from Y" toggle that does this for you per node. Reserve dedicated Z bands (via constants) for things that should always sit on top regardless of position — UI, projectiles, the player above all terrain:

```rust
const TERRAIN_Z_BASE: f32 = 0.0;
const PLAYER_Z: f32       = 20.0;
const PROJECTILE_Z: f32   = 30.0;
```

Y-sort within each band, but never let one band leak into another.
