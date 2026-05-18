#!/usr/bin/env python3
r"""
export_recipes_bincode.py
=========================

Serialize `docs/cooking/recipes/README.md` (the 30-column recipes table) into a
single binary file that a Rust program can decode with the `bincode` crate.

The wire format is byte-identical to:

    * `bincode` 1.3.x with default `bincode::config()` (i.e. `DefaultOptions`
      with `.with_fixint_encoding()` left at its default), OR
    * `bincode` 2.x with `bincode::config::legacy()`.

Both configurations produce: little-endian, fixed-width integers (no varint),
u64 length prefixes on every collection/string, u32 enum discriminant.

----------------------------------------------------------------------------
INTENDED CONSUMER
----------------------------------------------------------------------------

A Rust program in a separate repository that depends only on the `bincode`
crate. The Rust agent receives **only this script**; the docstring below
specifies the full schema, the wire format, and provides a copy-pasteable
Rust definition. The agent should be able to write a working decoder without
reading any other file.

----------------------------------------------------------------------------
DATA MODEL (paste into the Rust consumer)
----------------------------------------------------------------------------

```rust
use bincode::{Decode, Encode};

/// Top-level container.
#[derive(Encode, Decode, Debug)]
pub struct RecipesDb {
    /// Format version. Currently `1`. Bump on any breaking schema change.
    pub version: u32,
    /// Redundant recipe count (also `recipes.len()`). Decoder MUST assert
    /// `count as usize == recipes.len()` and reject mismatches.
    pub count: u64,
    /// The 27 nutrient slugs in canonical column order (3 macros, 7 minerals,
    /// 13 vitamins, 4 soft-essentials). Index `i` here aligns with index `i`
    /// inside each `Recipe::nutrients`. Provided once at the top of the file
    /// so the per-recipe vector can be index-aligned without duplicating slug
    /// strings on every recipe. Decoder MUST assert `nutrient_slugs.len() ==
    /// 27` and SHOULD assert the slugs match `NUTRIENT_SLUGS` below.
    pub nutrient_slugs: Vec<String>,
    /// One entry per recipe, sorted alphabetically by the cooking SKILL sort
    /// key (case-insensitive, strip leading articles `the`/`a`/`an`, numeric
    /// tokens by integer value).
    pub recipes: Vec<Recipe>,
}

#[derive(Encode, Decode, Debug)]
pub struct Recipe {
    /// H1 title, Title Case. Example: `"Apple Chickpea Salad"`.
    pub title: String,
    /// Filename without extension. The recipe page is at
    /// `docs/cooking/recipes/<slug>.md`. Example: `"apple-chickpea-salad"`.
    pub slug: String,
    /// Category slugs in alphabetical order. Every recipe has 1 or 2.
    /// Example: `vec!["breakfast", "main"]`.
    pub categories: Vec<String>,
    /// Trait slugs in alphabetical order. May be empty.
    /// Example: `vec!["fast", "make-ahead", "no-cook"]`.
    pub traits: Vec<String>,
    /// Exactly 27 entries, index-aligned with `RecipesDb::nutrient_slugs`.
    /// `None` = nutrient absent on this recipe (table cell was `—`).
    /// `Some(...)` = present.
    pub nutrients: Vec<Option<NutrientValue>>,
}

#[derive(Encode, Decode, Debug)]
pub enum NutrientValue {
    /// 25 of the 27 slugs are quantitative. The amount is the value printed
    /// in the recipes table (already threshold-filtered and rounded per the
    /// cooking SKILL). Unit is the canonical unit for the slug.
    Quantitative { amount: f64, unit: Unit },
    /// Only `phytochemicals` and `probiotics` are qualitative; the cell
    /// reads `yes` for present and carries no amount.
    Qualitative,
}

#[derive(Encode, Decode, Debug)]
pub enum Unit {
    /// `g` — Complex Carbs, Healthy Fats, Protein, Dietary Fiber.
    Grams,
    /// `mg` — Calcium, Iron, Magnesium, Potassium, Zinc, Vitamin B1, B2, B3,
    /// B5, B6, C, E, Omega-3.
    Milligrams,
    /// `µg` (U+00B5) — Iodine, Selenium, Vitamin A, B7, B9, B12, D, K.
    Micrograms,
}

/// The 27 canonical nutrient slugs in column order. Use as a compile-time
/// cross-check against the `RecipesDb::nutrient_slugs` field decoded from
/// the file.
pub const NUTRIENT_SLUGS: [&str; 27] = [
    // 3 macronutrients
    "complex-carbs", "healthy-fats", "protein",
    // 7 minerals
    "calcium", "iodine", "iron", "magnesium", "potassium", "selenium", "zinc",
    // 13 vitamins
    "vitamin-a", "vitamin-b1", "vitamin-b2", "vitamin-b3", "vitamin-b5",
    "vitamin-b6", "vitamin-b7", "vitamin-b9", "vitamin-b12",
    "vitamin-c", "vitamin-d", "vitamin-e", "vitamin-k",
    // 4 soft-essentials
    "dietary-fiber", "omega-3", "phytochemicals", "probiotics",
];
```

----------------------------------------------------------------------------
WIRE FORMAT (byte-for-byte specification)
----------------------------------------------------------------------------

All multi-byte integers are **little-endian**. There is no padding, no
framing, no separators, and no trailing bytes after the last recipe.

| Rust type           | Wire bytes                                             |
|---------------------|--------------------------------------------------------|
| `u32` / `i32`       | 4 bytes LE                                             |
| `u64` / `i64`       | 8 bytes LE                                             |
| `f64`               | 8 bytes LE IEEE 754 binary64                           |
| `bool`              | 1 byte: `0x00` = false, `0x01` = true                  |
| `String`            | `u64` LE byte length, then UTF-8 bytes (no NUL)        |
| `Vec<T>`            | `u64` LE element count, then T elements back-to-back   |
| `Option<T>`         | 1-byte tag: `0x00` = None (no payload), `0x01` = Some  |
| `enum`              | `u32` LE variant discriminant, then variant fields     |
| `struct`            | fields concatenated in declaration order (no padding)  |

Variant discriminants used in this schema:

* `NutrientValue::Quantitative` = `0`
* `NutrientValue::Qualitative`  = `1`
* `Unit::Grams`                 = `0`
* `Unit::Milligrams`            = `1`
* `Unit::Micrograms`            = `2`

Discriminant order MUST match the Rust enum declaration order shown above.

----------------------------------------------------------------------------
SAMPLE DECODE
----------------------------------------------------------------------------

Cargo.toml:

```toml
[dependencies]
bincode = "2.0"
```

main.rs (bincode 2.x):

```rust
use std::fs;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let bytes = fs::read("recipes.bincode")?;
    let config = bincode::config::legacy();
    let (db, consumed): (RecipesDb, usize) =
        bincode::decode_from_slice(&bytes, config)?;
    assert_eq!(consumed, bytes.len(), "trailing bytes");
    assert_eq!(db.version, 1, "unsupported version");
    assert_eq!(db.count as usize, db.recipes.len(), "count mismatch");
    assert_eq!(db.nutrient_slugs.len(), 27);
    for r in &db.recipes {
        assert_eq!(r.nutrients.len(), 27);
    }
    println!("loaded {} recipes", db.recipes.len());
    Ok(())
}
```

Equivalent with bincode 1.x:

```rust
let db: RecipesDb = bincode::deserialize(&bytes)?;
```

----------------------------------------------------------------------------
PER-CELL PARSING RULES (used by this script)
----------------------------------------------------------------------------

* **Recipe cell** matches `\[(.+?)\]\(cooking/recipes/([a-z0-9-]+)\.md\)` →
  `(title, slug)`.
* **Categories / Traits cells** are comma-separated slugs. The single
  character `—` (U+2014 EM DASH) encodes an empty vector.
* **Quantitative nutrient cells** are `<number><unit>` with no space.
  - `<number>` is integer or single-decimal-place float.
  - `<unit>` is exactly one of `g`, `mg`, or `µg` (U+00B5 MICRO SIGN).
  - The unit MUST equal the canonical unit for that nutrient slug — see the
    `UNIT_MAP` table inside this script. The recipes README is regenerated
    by the cooking SKILL's `build_recipes_table.py`, which enforces unit
    consistency, so a unit mismatch here indicates corpus corruption and
    aborts the script.
* **Qualitative cells** (only `phytochemicals` and `probiotics`) are either
  `yes` (Some(Qualitative)) or `—` (None). Any other value aborts.

----------------------------------------------------------------------------
USAGE
----------------------------------------------------------------------------

From the repo root:

```bash
python3 scripts/export_recipes_bincode.py
# writes ./recipes.bincode

python3 scripts/export_recipes_bincode.py \
    --input docs/cooking/recipes/README.md \
    --output dist/recipes.bincode

python3 scripts/export_recipes_bincode.py --check
# parses + summarizes; does not write
```

The script is read-only over the input markdown; it never mutates the corpus.
"""

from __future__ import annotations

import argparse
import re
import struct
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Schema constants — keep these in sync with the docstring above.
# ---------------------------------------------------------------------------

SCHEMA_VERSION = 1

# Canonical nutrient column order (must match the README header order
# byte-for-byte and the SKILL's `## Nutrient lexicons` ordering).
NUTRIENT_SLUGS: list[str] = [
    # 3 macronutrients
    "complex-carbs", "healthy-fats", "protein",
    # 7 minerals
    "calcium", "iodine", "iron", "magnesium", "potassium", "selenium", "zinc",
    # 13 vitamins
    "vitamin-a", "vitamin-b1", "vitamin-b2", "vitamin-b3", "vitamin-b5",
    "vitamin-b6", "vitamin-b7", "vitamin-b9", "vitamin-b12",
    "vitamin-c", "vitamin-d", "vitamin-e", "vitamin-k",
    # 4 soft-essentials
    "dietary-fiber", "omega-3", "phytochemicals", "probiotics",
]

# Display-name column headers in the README, in the same order as
# NUTRIENT_SLUGS. Used to validate the header row.
COLUMN_HEADERS: list[str] = [
    "Complex Carbs", "Healthy Fats", "Protein",
    "Calcium", "Iodine", "Iron", "Magnesium", "Potassium", "Selenium", "Zinc",
    "Vitamin A", "Vitamin B1", "Vitamin B2", "Vitamin B3", "Vitamin B5",
    "Vitamin B6", "Vitamin B7", "Vitamin B9", "Vitamin B12",
    "Vitamin C", "Vitamin D", "Vitamin E", "Vitamin K",
    "Dietary Fiber", "Omega-3", "Phytochemicals", "Probiotics",
]

# Qualitative slugs are presence-only ("yes" or "—" in the cell).
QUALITATIVE_SLUGS: set[str] = {"phytochemicals", "probiotics"}

# Canonical unit per slug. Three valid units: "g", "mg", "µg" (U+00B5).
MICRO = "µ"
UNIT_MAP: dict[str, str] = {
    "complex-carbs":   "g",
    "healthy-fats":    "g",
    "protein":         "g",
    "calcium":         "mg",
    "iodine":          MICRO + "g",
    "iron":            "mg",
    "magnesium":       "mg",
    "potassium":       "mg",
    "selenium":        MICRO + "g",
    "zinc":            "mg",
    "vitamin-a":       MICRO + "g",
    "vitamin-b1":      "mg",
    "vitamin-b2":      "mg",
    "vitamin-b3":      "mg",
    "vitamin-b5":      "mg",
    "vitamin-b6":      "mg",
    "vitamin-b7":      MICRO + "g",
    "vitamin-b9":      MICRO + "g",
    "vitamin-b12":     MICRO + "g",
    "vitamin-c":       "mg",
    "vitamin-d":       MICRO + "g",
    "vitamin-e":       "mg",
    "vitamin-k":       MICRO + "g",
    "dietary-fiber":   "g",
    "omega-3":         "mg",
}

# Enum discriminants (MUST match the Rust enum declaration order).
DISCRIMINANT_QUANTITATIVE = 0
DISCRIMINANT_QUALITATIVE  = 1
DISCRIMINANT_GRAMS        = 0
DISCRIMINANT_MILLIGRAMS   = 1
DISCRIMINANT_MICROGRAMS   = 2

EM_DASH = "—"


# ---------------------------------------------------------------------------
# bincode primitive encoders.
# ---------------------------------------------------------------------------

def enc_u32(n: int) -> bytes:
    return struct.pack("<I", n)


def enc_u64(n: int) -> bytes:
    return struct.pack("<Q", n)


def enc_f64(x: float) -> bytes:
    return struct.pack("<d", x)


def enc_string(s: str) -> bytes:
    payload = s.encode("utf-8")
    return enc_u64(len(payload)) + payload


def enc_vec_strings(items: list[str]) -> bytes:
    out = enc_u64(len(items))
    for s in items:
        out += enc_string(s)
    return out


# ---------------------------------------------------------------------------
# README parser.
# ---------------------------------------------------------------------------

RECIPE_LINK_RE = re.compile(
    r"\[(?P<title>.+?)\]\(cooking/recipes/(?P<slug>[a-z0-9-]+)\.md\)"
)
QUANTITY_RE = re.compile(
    r"^(?P<amount>\d+(?:\.\d+)?)(?P<unit>g|mg|" + MICRO + r"g)$"
)


class ParseError(RuntimeError):
    pass


def split_row(row: str) -> list[str]:
    """Split a Markdown table row by `|`, stripping outer pipes and whitespace."""
    parts = row.strip().strip("|").split("|")
    return [p.strip() for p in parts]


def parse_csv_slugs(cell: str) -> list[str]:
    if cell == EM_DASH or cell == "":
        return []
    return [token.strip() for token in cell.split(",") if token.strip()]


def parse_quantitative(slug: str, cell: str) -> tuple[float, str] | None:
    """Return `(amount, unit)` or `None` for an em-dash cell."""
    if cell == EM_DASH or cell == "":
        return None
    match = QUANTITY_RE.match(cell)
    if not match:
        raise ParseError(
            f"unparseable quantitative cell for slug {slug!r}: {cell!r}"
        )
    amount = float(match["amount"])
    unit = match["unit"]
    expected = UNIT_MAP[slug]
    if unit != expected:
        raise ParseError(
            f"wrong unit on slug {slug!r}: cell uses {unit!r}, "
            f"canonical is {expected!r}"
        )
    return (amount, unit)


def parse_qualitative(slug: str, cell: str) -> bool:
    """Return `True` for `yes`, `False` for `—`. Anything else aborts."""
    if cell == EM_DASH or cell == "":
        return False
    if cell == "yes":
        return True
    raise ParseError(
        f"qualitative cell for slug {slug!r} must be 'yes' or '{EM_DASH}', "
        f"got {cell!r}"
    )


def parse_readme(path: Path) -> list[dict]:
    """Parse the recipes README table and return a list of recipe dicts.

    Each dict has keys: title (str), slug (str), categories (list[str]),
    traits (list[str]), nutrients (list of entries). A nutrient entry is one
    of:
        None                            -> Option::None
        ("qualitative", True)           -> Option::Some(NutrientValue::Qualitative)
        ("quantitative", amount, unit)  -> Option::Some(NutrientValue::Quantitative {...})

    A `("qualitative", False)` entry collapses to `None` in the encoder.
    """
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    header_idx = None
    for idx, line in enumerate(lines):
        if line.startswith("| Recipe |"):
            header_idx = idx
            break
    if header_idx is None:
        raise ParseError(f"no `| Recipe |` header row found in {path}")

    headers = split_row(lines[header_idx])
    expected_headers = ["Recipe", "Categories", "Traits"] + COLUMN_HEADERS
    if headers != expected_headers:
        raise ParseError(
            f"unexpected table header. Got:\n  {headers}\n"
            f"Expected:\n  {expected_headers}"
        )
    if header_idx + 1 >= len(lines) or not lines[header_idx + 1].lstrip().startswith("| ---"):
        raise ParseError("expected `| --- |` separator row directly after header")

    recipes: list[dict] = []
    for ln_no in range(header_idx + 2, len(lines)):
        line = lines[ln_no]
        if not line.startswith("|"):
            break  # table ended

        cells = split_row(line)
        if len(cells) != 30:
            raise ParseError(
                f"line {ln_no + 1}: expected 30 cells, got {len(cells)}: "
                f"{line[:120]}..."
            )

        link_match = RECIPE_LINK_RE.match(cells[0])
        if not link_match:
            raise ParseError(
                f"line {ln_no + 1}: unparseable Recipe cell: {cells[0]!r}"
            )

        categories = parse_csv_slugs(cells[1])
        traits = parse_csv_slugs(cells[2])

        if not categories:
            raise ParseError(
                f"line {ln_no + 1}: recipe {link_match['slug']!r} has no "
                f"categories — SKILL requires 1 or 2"
            )

        nutrients: list = []
        for col_offset, slug in enumerate(NUTRIENT_SLUGS):
            cell = cells[3 + col_offset]
            if slug in QUALITATIVE_SLUGS:
                present = parse_qualitative(slug, cell)
                if present:
                    nutrients.append(("qualitative", True))
                else:
                    nutrients.append(None)
            else:
                parsed = parse_quantitative(slug, cell)
                if parsed is None:
                    nutrients.append(None)
                else:
                    amount, unit = parsed
                    nutrients.append(("quantitative", amount, unit))

        recipes.append({
            "title": link_match["title"],
            "slug": link_match["slug"],
            "categories": categories,
            "traits": traits,
            "nutrients": nutrients,
        })

    if not recipes:
        raise ParseError(f"no data rows found in {path}")
    return recipes


# ---------------------------------------------------------------------------
# bincode encoders for the schema.
# ---------------------------------------------------------------------------

def encode_unit(unit: str) -> bytes:
    if unit == "g":
        return enc_u32(DISCRIMINANT_GRAMS)
    if unit == "mg":
        return enc_u32(DISCRIMINANT_MILLIGRAMS)
    if unit == MICRO + "g":
        return enc_u32(DISCRIMINANT_MICROGRAMS)
    raise ParseError(f"unknown unit string passed to encode_unit: {unit!r}")


def encode_nutrient(entry) -> bytes:
    """Encode one element of `Recipe::nutrients` (an `Option<NutrientValue>`)."""
    if entry is None:
        return b"\x00"  # Option::None
    kind = entry[0]
    if kind == "qualitative":
        # Option::Some(NutrientValue::Qualitative) — discriminant 1, no fields.
        return b"\x01" + enc_u32(DISCRIMINANT_QUALITATIVE)
    if kind == "quantitative":
        _, amount, unit = entry
        # Option::Some(NutrientValue::Quantitative { amount, unit }).
        return (
            b"\x01"
            + enc_u32(DISCRIMINANT_QUANTITATIVE)
            + enc_f64(amount)
            + encode_unit(unit)
        )
    raise ParseError(f"unknown nutrient entry kind: {entry!r}")


def encode_recipe(recipe: dict) -> bytes:
    out = b""
    out += enc_string(recipe["title"])
    out += enc_string(recipe["slug"])
    out += enc_u64(len(recipe["categories"]))
    for slug in recipe["categories"]:
        out += enc_string(slug)
    out += enc_u64(len(recipe["traits"]))
    for slug in recipe["traits"]:
        out += enc_string(slug)
    out += enc_u64(len(recipe["nutrients"]))
    for entry in recipe["nutrients"]:
        out += encode_nutrient(entry)
    return out


def encode_db(recipes: list[dict]) -> bytes:
    """Encode the top-level `RecipesDb` struct."""
    out = b""
    out += enc_u32(SCHEMA_VERSION)               # version: u32
    out += enc_u64(len(recipes))                 # count: u64
    out += enc_vec_strings(NUTRIENT_SLUGS)       # nutrient_slugs: Vec<String>
    out += enc_u64(len(recipes))                 # recipes Vec length
    for recipe in recipes:
        out += encode_recipe(recipe)
    return out


# ---------------------------------------------------------------------------
# CLI.
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Export docs/cooking/recipes/README.md to a bincode binary. "
            "See the module docstring for the wire format and Rust schema."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("docs/cooking/recipes/README.md"),
        help="path to the recipes README table (default: %(default)s)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("recipes.bincode"),
        help="path to write the bincode binary (default: %(default)s)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="parse + summarize without writing the binary",
    )
    args = parser.parse_args()

    if not args.input.exists():
        print(f"error: input not found: {args.input}", file=sys.stderr)
        return 1

    try:
        recipes = parse_readme(args.input)
    except ParseError as exc:
        print(f"parse error: {exc}", file=sys.stderr)
        return 2

    blob = encode_db(recipes)

    print(f"parsed {len(recipes)} recipes from {args.input}", file=sys.stderr)
    print(f"encoded {len(blob)} bytes (schema v{SCHEMA_VERSION})", file=sys.stderr)

    if args.check:
        preview = blob[:96]
        hex_str = " ".join(f"{b:02x}" for b in preview)
        print(f"first {len(preview)} bytes (hex):", file=sys.stderr)
        print(hex_str, file=sys.stderr)
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(blob)
    print(f"wrote {args.output} ({len(blob)} bytes)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
