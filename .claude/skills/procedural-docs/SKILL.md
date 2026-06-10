---
name: procedural-docs
description: Conventions and verification for docs/software/procedural/ (procedural animation & generation, Rust + Bevy). Load when editing ANY file under docs/software/procedural/ for any reason — content, code snippets, formatting, sidebar updates, audits — not only new pages.
---

# Procedural Docs: Conventions & Verification

The section is a from-scratch Rust + Bevy reference (animation: Verlet/PBD, chains, IK, creatures, soft bodies; generation: noise, grammars). Its load-bearing promise: **every worked example is a compilable program** and every constant/claim traces to a verified primary source.

## Invariants

- **Pinned versions:** `bevy = "0.18"`, `noise = "0.9"`, `rand`/`rand_chacha = "0.9"`. Bump all page mentions and `scripts/assemble_procedural_bins.py`'s Cargo.toml together, then re-run the compile check.
- **Compilability:** "complete program" blocks contain `fn main` and compile verbatim. Cross-page examples (FABRIK arm, lizard) must compile when assembled per the page's stated reuse list — `scripts/assemble_procedural_bins.py` encodes those recipes, locating blocks by marker strings (`struct Chain`, `fn fabrik_resolve`, `fn cursor_world`, …). Renaming a marked item ⇒ update the recipes there.
- **Source fidelity:** deliberate deviations from the argonautcode sources are annotated in-text (pattern: the lizard's `clamp_length_max(12.0)` vs the source's constant `setMag(12)` step). Don't deviate silently.
- **Math:** KaTeX `\( \)` / `\[ \]` only — never `$`; never `\(`/`\[` inside code fences (the `katexMath` plugin in `docs/index.html` extracts delimiters from RAW markdown, fences included).
- **md-standards apply:** H2–H4 numbered; `## Table of Contents` and `## Sources` are the only unnumbered H2s; links root-relative to `docs/`.

## Verify after editing

| You changed | Run (all must exit 0) |
|---|---|
| any `.md` | `python3 scripts/check_docs.py` and `python3 scripts/check_tildes.py` |
| any math | `node scripts/check_katex.mjs` (renders via the index.html-pinned KaTeX; downloads it once per version) |
| any Rust block | `python3 scripts/assemble_procedural_bins.py --check` (cold build ≈ 10 min) |

## Adjudicated facts — do not "fix" these

Verified against primary sources (argonautcode repos line-by-line, zalo's posts, Bevy/crates docs) in June 2026. Re-verify only if upstream changes; do not "correct" the docs back to the plausible-but-wrong versions:

- The soft-body outward normal `Vec2::new(s.y, -s.x)` is the **literal** port of the source's `rotate(-HALF_PI)` — nothing flips under y-up; the traps are translating idiomatically to `.perp()` (that's +90°) or reversing the ring winding.
- The cave **"4-5 rule" counts the cell itself**: wall iff ≥ 5 walls in the 3×3 block *including* the centre (wall survives at ≥ 4/8 neighbours, floor converts at ≥ 5/8).
- glam `normalize()` on a zero vector returns **NaN** in default builds; it panics only under the opt-in `glam_assert` feature.
- `Camera2dBundle` was removed in Bevy **0.16**; `RenderAssetUsages` imports from `bevy::asset` (its `bevy::render` re-export was dropped in **0.17**); `RenderAssetUsages::default()` = `MAIN_WORLD | RENDER_WORLD`; `FixedUpdate` defaults to 64 Hz; `Query::single()` and `viewport_to_world_2d` return `Result`.
- `noise` crate `Fbm` defaults: 6 octaves, frequency 1.0, persistence 0.5, lacunarity **2π/3 ≈ 2.094** (not 2.0).
- rand 0.9 renames: `gen`→`random`, `gen_bool`→`random_bool`, `thread_rng()`→`rng()`; `bevy_rand` v0.14 pairs with Bevy 0.18 and tracks rand 0.10.
- animal-proc-anim constants are exact: widths `{52,58,40,60,68,71,65,50,28,15,11,9,7,7}`; legs at vertebrae 3/7; spreads π/4 front, π/3 rear; links 52/36; shoulder offset −20, foot offset +80 (both added to `bodyWidth[i]`); step threshold 200; foot lerp 0.4; spine 14 joints, link 64, clamp π/8; head steps a constant 12 px (`setMag(12)`).
- soft-body-proc-anim's **frog has dangling two-point Verlet limbs** (angle-constrained distance constraints) — no FABRIK, no step gait; the walking recipe in soft-bodies §7 is this doc's extension and must stay phrased as such.
- zalo, verbatim: *"The essence of constraint is projection. Find the minimum movement that satisfies the constraint."*
- Video titles: *A simple procedural animation technique* (`qlfh_rv6khY`), *Simulating soft body animals* (`GXh0Vxg7AnQ`). Book authors: **Prusinkiewicz & Lindenmayer** (that order).
