#!/usr/bin/env python3
"""Assemble the Rust code blocks from docs/software/procedural/ into a scratch
cargo project — one bin per worked example — to verify the docs' "complete
program" claims against the real crates (bevy 0.18, noise 0.9, rand 0.9).

"Complete program" blocks are used verbatim; cross-page examples (FABRIK arm,
lizard) are concatenated exactly per each page's stated reuse list, with `use`
lines deduplicated and a trivial `main` added only where a page explicitly
leaves the wiring to the reader.

Blocks are located by a marker string they must contain (not by index), so
reordering blocks within a page is safe. Renaming a marked item (e.g.
`struct Chain`, `fn fabrik_resolve`) requires updating the recipes below.

Usage:
    python3 scripts/assemble_procedural_bins.py            # write project to /tmp/proc-compile-test
    python3 scripts/assemble_procedural_bins.py --check    # ...then run `cargo check --bins` (cold ~10 min)
    python3 scripts/assemble_procedural_bins.py --out DIR
"""
import re
import subprocess
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs" / "software" / "procedural"

CARGO_TOML = """\
[package]
name = "proc-compile-test"
version = "0.1.0"
edition = "2021"

[dependencies]
bevy = "0.18"
noise = "0.9"
rand = "0.9"
rand_chacha = "0.9"
"""


def blocks(name):
    text = (DOCS / name).read_text(encoding="utf-8")
    return re.findall(r"```rust\n(.*?)```", text, re.S)


def find(blocks_list, marker, name):
    matches = [b for b in blocks_list if marker in b]
    if len(matches) != 1:
        raise SystemExit(f"{name}: expected exactly 1 rust block containing {marker!r}, found {len(matches)}")
    return matches[0]


def split_uses(code):
    uses, body = [], []
    for line in code.split("\n"):
        (uses if line.startswith("use ") else body).append(line)
    return uses, "\n".join(body).strip("\n")


def extract_fn(code, fn_name):
    """Extract `fn fn_name` plus its preceding ///-comments, by brace counting."""
    lines = code.split("\n")
    start = next(i for i, l in enumerate(lines) if re.match(rf"\s*(pub )?fn {fn_name}\b", l))
    while start > 0 and lines[start - 1].lstrip().startswith("///"):
        start -= 1
    depth = 0
    seen_open = False
    for j in range(start, len(lines)):
        depth += lines[j].count("{") - lines[j].count("}")
        if "{" in lines[j]:
            seen_open = True
        if seen_open and depth == 0:
            return "\n".join(lines[start: j + 1])
    raise SystemExit(f"unterminated fn {fn_name}")


def assemble(parts, extra_uses=(), glue=""):
    all_uses = list(extra_uses)
    bodies = []
    for p in parts:
        uses, body = split_uses(p)
        all_uses.extend(uses)
        bodies.append(body)
    # dedupe `use` lines; drop a bare PI import when a grouped {PI, ...} import exists
    seen, uses = set(), []
    grouped_pi = any("{" in u and "PI" in u for u in all_uses)
    for u in all_uses:
        if u in seen or (grouped_pi and u.strip() == "use std::f32::consts::PI;"):
            continue
        seen.add(u)
        uses.append(u)
    out = "\n".join(uses) + "\n\n" + "\n\n".join(b for b in bodies if b)
    if glue:
        out += "\n\n" + glue
    return out + "\n"


def wrap_statements(block, prelude, suffix):
    """Wrap a statements-only snippet (its `use` lines hoisted) in fn main."""
    uses, body = split_uses(block)
    stmts = "\n".join(f"    {l}" if l.strip() else l for l in body.split("\n"))
    return "\n".join(uses) + "\n\nfn main() {\n" + prelude + stmts + "\n" + suffix + "}\n"


def main():
    out = Path("/tmp/proc-compile-test")
    check = False
    args = sys.argv[1:]
    while args:
        a = args.pop(0)
        if a == "--check":
            check = True
        elif a == "--out":
            out = Path(args.pop(0))
        else:
            raise SystemExit(f"unknown arg: {a}")

    found = blocks("foundations.md")
    chains = blocks("chains-and-ik.md")
    creature = blocks("creature-rigging.md")
    soft = blocks("soft-bodies.md")
    noisemd = blocks("generation-noise.md")
    grammars = blocks("generation-grammars.md")

    constrain_distance = find(found, "fn constrain_distance", "foundations.md")
    rope = find(found, "fn main", "foundations.md")
    angle_fns = find(chains, "fn simplify_angle", "chains-and-ik.md")
    chain = find(chains, "struct Chain", "chains-and-ik.md")
    cursor_prog = find(chains, "fn cursor_world", "chains-and-ik.md")
    fabrik = find(chains, "fn fabrik_resolve", "chains-and-ik.md")
    arm = find(chains, "struct Arm", "chains-and-ik.md")
    outline_mesh = find(creature, "fn outline_mesh", "creature-rigging.md")
    lizard = find(creature, "struct Lizard", "creature-rigging.md")
    blob = find(soft, "fn main", "soft-bodies.md")
    rng_snippet = find(noisemd, "ChaCha8Rng::seed_from_u64", "generation-noise.md")
    terrain = find(noisemd, "fn main", "generation-noise.md")
    expand = find(grammars, "fn expand", "generation-grammars.md")
    plant = find(grammars, "struct Plant", "generation-grammars.md")
    cave = find(grammars, "fn generate_cave", "generation-grammars.md")

    cursor_world = extract_fn(cursor_prog, "cursor_world")

    bins = {
        # complete programs, verbatim
        "rope.rs": assemble([rope]),
        "blob.rs": assemble([blob]),
        "terrain.rs": assemble([terrain]),
        "cave.rs": assemble([cave]),
        # programs the pages assemble from their earlier snippets
        "chain_cursor.rs": assemble([angle_fns, chain, cursor_prog]),
        "plant.rs": assemble([expand, plant]),
        "fabrik_arm.rs": assemble(
            [constrain_distance, fabrik, arm, cursor_world],
            extra_uses=["use bevy::prelude::*;"],
            glue=(
                "fn main() {\n"
                "    App::new()\n"
                "        .add_plugins(DefaultPlugins)\n"
                "        .add_systems(Startup, setup_arm)\n"
                "        .add_systems(Update, reach_cursor)\n"
                "        .run();\n"
                "}"
            ),
        ),
        "lizard.rs": assemble(
            [angle_fns, chain, constrain_distance, fabrik, cursor_world, lizard],
        ),
        # standalone snippets
        "mesh_snippet.rs": assemble(
            [outline_mesh],
            extra_uses=["use bevy::prelude::*;"],
            glue="fn main() {}  // outline_mesh is intentionally unused here",
        ),
        "rng_snippet.rs": wrap_statements(
            rng_snippet, "    let seed = 42u64;\n", "    let _ = x;\n"
        ),
    }

    (out / "src" / "bin").mkdir(parents=True, exist_ok=True)
    (out / "Cargo.toml").write_text(CARGO_TOML, encoding="utf-8")
    for fname, content in bins.items():
        (out / "src" / "bin" / fname).write_text(content, encoding="utf-8")
        print(f"wrote {fname}: {len(content.splitlines())} lines")
    print(f"\nproject at {out}")

    if check:
        print("running cargo check --bins ...")
        sys.exit(subprocess.run(["cargo", "check", "--bins"], cwd=out).returncode)
    print(f"verify with: cargo check --bins  (in {out})")


if __name__ == "__main__":
    main()
