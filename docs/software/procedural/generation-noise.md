# Noise, fBm & Heightmaps

> *Generation throughline.* Procedural *generation* shares no physics with the animation pages — its unifying idea is that content is a **deterministic function of a seed**. This page covers the workhorse of that idea: **noise**, a smooth pseudo-random function of space, and **fBm**, the trick that turns one octave of noise into natural-looking detail. The worked example generates a terrain heightmap. Examples use Bevy `0.18` and the [`noise`](https://docs.rs/noise) crate. This is a primer — for design-level depth see [Procedural Generation in Game Design](software/books/procedural-generation-in-game-design/book_summary.md).

## Table of Contents

- [1. Procedural Generation: Determinism from a Seed](#1-procedural-generation-determinism-from-a-seed)
  - [1.1. Why Seeds](#11-why-seeds)
  - [1.2. Seeded RNG in Bevy](#12-seeded-rng-in-bevy)
- [2. Noise: A Smooth Function of Space](#2-noise-a-smooth-function-of-space)
  - [2.1. Value Noise](#21-value-noise)
  - [2.2. Gradient (Perlin) Noise](#22-gradient-perlin-noise)
  - [2.3. Simplex Noise](#23-simplex-noise)
  - [2.4. The Interpolation Curve](#24-the-interpolation-curve)
- [3. Fractal Brownian Motion (Octaves)](#3-fractal-brownian-motion-octaves)
- [4. Domain Warping](#4-domain-warping)
- [5. Worked Example: A Terrain Heightmap](#5-worked-example-a-terrain-heightmap)
- [Sources](#sources)

## 1. Procedural Generation: Determinism from a Seed

### 1.1. Why Seeds

The defining property of procedural generation is **determinism**: the same seed always produces the same content. This is what lets a game ship a whole galaxy as a single integer — you store the *seed*, not the terabytes, and regenerate on demand. It also makes worlds shareable ("try seed 1337") and bugs reproducible. Every generator on this page and the [next](software/procedural/generation-grammars.md) is a pure function from a seed (and a coordinate) to content.

### 1.2. Seeded RNG in Bevy

The enemy of determinism is a randomly-seeded global generator. **Never** use `rand::rng()` (the OS-seeded global generator; `thread_rng()` before rand 0.9) for world content — it differs every run. Instead seed an explicit generator:

```rust
use rand::{Rng, SeedableRng};
use rand_chacha::ChaCha8Rng;

let mut rng = ChaCha8Rng::seed_from_u64(seed);
let x: f32 = rng.random(); // reproducible for a given seed
```

`ChaCha8Rng` is portable and reproducible across platforms. In an ECS app, the [`bevy_rand`](https://github.com/bluefinger/bevy_rand) crate (use **v0.14** with Bevy 0.18) wraps this in a resource/component so each entity can carry its own deterministic stream — note `bevy_rand` tracks the `rand` 0.10 line, distinct from Bevy's internal `rand`. For continuous fields, though, you usually want *noise* rather than raw RNG.

## 2. Noise: A Smooth Function of Space

Raw RNG is white noise — each sample independent, no spatial structure. Terrain, clouds, and textures need a function that is random *but smooth*: nearby points have nearby values. That is **coherent noise**. A noise function maps a coordinate to a value, conventionally in \( [-1, 1] \):

\[ \mathrm{noise}: \mathbb{R}^n \rightarrow [-1, 1] \]

It is deterministic (same point → same value) and continuous. Three common kinds:

### 2.1. Value Noise

Assign a random value to each integer lattice point, then **interpolate** between them for points in between. Cheap and simple, but it tends to look blocky and axis-aligned because the extrema are pinned to the grid.

### 2.2. Gradient (Perlin) Noise

Ken Perlin's improvement: assign a random *gradient vector* (not a value) to each lattice point. The noise at a point is the interpolation of the dot products between each corner's gradient and the offset from that corner to the point. Because the values are zero *at* the lattice points and shaped by gradients between them, the result has no grid-aligned blockiness — the smooth, organic look everyone recognises. This is the default choice.

### 2.3. Simplex Noise

Perlin's later design replaces the square grid with a **simplex** (triangles in 2D, tetrahedra in 3D). It has fewer directional artifacts, is cheaper in high dimensions (the cost of grid noise grows as \( 2^n \) corners; simplex grows as \( n{+}1 \) vertices), and has well-defined gradients. Prefer it for 3D/4D noise (e.g. animated 3D noise where the third axis is time).

### 2.4. The Interpolation Curve

The *quality* of gradient noise lives in the interpolation curve. Linear interpolation,

\[ \mathrm{lerp}(a, b, t) = a + (b - a)\,t, \]

leaves visible creases because its slope is discontinuous at the lattice lines. Smoothstep fixes the first derivative:

\[ s(t) = 3t^2 - 2t^3 \qquad (s'(0) = s'(1) = 0) \]

Perlin's improved noise goes further with the **quintic fade**, whose first *and second* derivatives vanish at the endpoints — eliminating the subtle second-order discontinuities that smoothstep still shows under lighting:

\[ f(t) = 6t^5 - 15t^4 + 10t^3 = t^3\,(6t^2 - 15t + 10) \]

You rarely write these by hand — the `noise` crate bakes them in — but knowing why the curve matters explains why early Perlin noise looked subtly grid-like and the improved version does not.

## 3. Fractal Brownian Motion (Octaves)

A single octave of noise is too smooth to be interesting — it has one feature size. Real terrain has detail at every scale: mountains, hills on the mountains, bumps on the hills. **Fractal Brownian Motion (fBm)** sums several octaves, each at higher frequency and lower amplitude:

\[ \mathrm{fBm}(\mathbf{p}) = \sum_{k=0}^{O-1} a^{\,k}\;\mathrm{noise}\!\left(f^{\,k}\,\mathbf{p}\right) \]

with three dials:

- **Octaves** \( O \) — how many layers (more = finer detail, more cost). 4-8 is typical.
- **Persistence** \( a \) — how fast amplitude falls per octave (≈ 0.5; lower = smoother, higher = rougher/noisier).
- **Lacunarity** \( f \) — how fast frequency grows per octave (≈ 2.0, i.e. each octave has twice the detail).

The `noise` crate's `Fbm` defaults sit here too: 6 octaves, persistence 0.5 — though its default lacunarity is \( 2\pi/3 \approx 2.09 \), not exactly 2. Tuning \( a \) and \( f \) is most of the art of "what kind of terrain is this".

## 4. Domain Warping

A cheap trick for organic, swirly results: instead of sampling noise at \( \mathbf{p} \), sample it at a position that has itself been *displaced by noise*:

\[ \mathrm{warp}(\mathbf{p}) = \mathrm{noise}\big(\mathbf{p} + \mathbf{q}(\mathbf{p})\big) \]

where \( \mathbf{q}(\mathbf{p}) \) is a small vector field built from more noise. One level gives flowing, marbled terrain; nesting it twice gives the wispy, cloud-like fields you see in high-end procedural art. It costs only extra noise lookups.

## 5. Worked Example: A Terrain Heightmap

A complete Bevy `0.18` program: sample `Fbm<Perlin>` over a grid, map height bands to terrain colours, bake the result into an `Image`, and display it as a sprite. Add `noise = "0.9"` to `Cargo.toml`.

```rust
use bevy::asset::RenderAssetUsages;
use bevy::image::Image;
use bevy::prelude::*;
use bevy::render::render_resource::{Extent3d, TextureDimension, TextureFormat};
use noise::{Fbm, NoiseFn, Perlin};

const W: u32 = 512;
const H: u32 = 512;
const FEATURES: f64 = 3.0; // how many large features span the image

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .add_systems(Startup, setup)
        .run();
}

fn setup(mut commands: Commands, mut images: ResMut<Assets<Image>>) {
    commands.spawn(Camera2d);

    let fbm = Fbm::<Perlin>::new(42); // seed -> reproducible terrain
    let mut data = vec![0u8; (W * H * 4) as usize];

    for y in 0..H {
        for x in 0..W {
            let p = [
                x as f64 / W as f64 * FEATURES,
                y as f64 / H as f64 * FEATURES,
            ];
            let n = fbm.get(p);                          // ≈ [-1, 1]
            let height = ((n + 1.0) * 0.5).clamp(0.0, 1.0) as f32; // -> [0, 1]
            let [r, g, b] = terrain_color(height);
            let i = ((y * W + x) * 4) as usize;
            data[i] = (r * 255.0) as u8;
            data[i + 1] = (g * 255.0) as u8;
            data[i + 2] = (b * 255.0) as u8;
            data[i + 3] = 255;
        }
    }

    let image = Image::new(
        Extent3d { width: W, height: H, depth_or_array_layers: 1 },
        TextureDimension::D2,
        data,
        TextureFormat::Rgba8UnormSrgb,
        RenderAssetUsages::RENDER_WORLD, // static texture; never mutated
    );
    commands.spawn(Sprite::from_image(images.add(image)));
}

/// Classic height bands: water → sand → grass → rock → snow.
fn terrain_color(h: f32) -> [f32; 3] {
    match h {
        _ if h < 0.40 => [0.10, 0.30, 0.60],
        _ if h < 0.50 => [0.80, 0.72, 0.50],
        _ if h < 0.75 => [0.20, 0.55, 0.30],
        _ if h < 0.90 => [0.40, 0.32, 0.24],
        _ => [0.95, 0.95, 0.97],
    }
}
```

Change the `42` seed and you get an entirely different — but always reproducible — continent. To add detail, configure the `Fbm` via the `noise::MultiFractal` trait (`.set_octaves(...)`, `.set_persistence(...)`, `.set_lacunarity(...)`); to make coastlines wind and curl, [domain-warp](#4-domain-warping) the input coordinates with a second noise.

## Sources

- Ken Perlin — *Improving Noise* (the quintic fade and gradient noise); the [`noise`](https://docs.rs/noise) crate documentation (Perlin, Simplex, `Fbm`, `MultiFractal`).
- [Procedural Generation in Game Design](software/books/procedural-generation-in-game-design/book_summary.md) (design-level treatment of noise-driven content).
- Next: [Grammars & Systems](software/procedural/generation-grammars.md) — generation by *rules* rather than fields.
