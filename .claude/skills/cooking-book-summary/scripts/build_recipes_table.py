#!/usr/bin/env python3
"""Build the recipes overview table for docs/cooking/recipes/README.md.

Sole writer of docs/cooking/recipes/README.md. Invoke from the repo root:

    python3 .claude/skills/cooking-book-summary/scripts/build_recipes_table.py \\
        > docs/cooking/recipes/README.md

Behavior, cell formats, sort key, and warning emissions are defined by the
cooking-book-summary SKILL.md — see the `### `docs/cooking/recipes/README.md``
template under `## Page templates`, the `### Recipe-page rendering` section
for cell-amount source-of-truth, and `### 5.16` for the byte-identical audit.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

RECIPES_DIR = Path("docs/cooking/recipes")

# Column order matches the canonical lexicon ordering in the cooking skill:
# macronutrients → minerals → vitamins → soft-essentials, alphabetical within
# each group, B-vitamins by numeric value.
NUTRIENT_COLUMNS: list[tuple[str, str, str]] = [
    ("Complex Carbs", "complex-carbs", "quant"),
    ("Healthy Fats", "healthy-fats", "quant"),
    ("Protein", "protein", "quant"),
    ("Calcium", "calcium", "quant"),
    ("Iodine", "iodine", "quant"),
    ("Iron", "iron", "quant"),
    ("Magnesium", "magnesium", "quant"),
    ("Potassium", "potassium", "quant"),
    ("Selenium", "selenium", "quant"),
    ("Zinc", "zinc", "quant"),
    ("Vitamin A", "vitamin-a", "quant"),
    ("Vitamin B1", "vitamin-b1", "quant"),
    ("Vitamin B2", "vitamin-b2", "quant"),
    ("Vitamin B3", "vitamin-b3", "quant"),
    ("Vitamin B5", "vitamin-b5", "quant"),
    ("Vitamin B6", "vitamin-b6", "quant"),
    ("Vitamin B7", "vitamin-b7", "quant"),
    ("Vitamin B9", "vitamin-b9", "quant"),
    ("Vitamin B12", "vitamin-b12", "quant"),
    ("Vitamin C", "vitamin-c", "quant"),
    ("Vitamin D", "vitamin-d", "quant"),
    ("Vitamin E", "vitamin-e", "quant"),
    ("Vitamin K", "vitamin-k", "quant"),
    ("Dietary Fiber", "dietary-fiber", "quant"),
    ("Omega-3", "omega-3", "quant"),
    ("Phytochemicals", "phytochemicals", "qual"),
    ("Probiotics", "probiotics", "qual"),
]

EMPTY = "—"  # em-dash U+2014

# Bullet line variants accepted in a nutrient section:
#   `- [Display Name](cooking/<group>/<slug>.md) — <amount><unit>` (quantitative)
#   `- [Display Name](cooking/<group>/<slug>.md)`                  (qualitative)
BULLET_RE = re.compile(
    r"^-\s+\[(?P<name>[^\]]+)\]\(cooking/(?P<group>[^/]+)/(?P<slug>[^)]+)\.md\)"
    r"(?:\s+—\s+(?P<amount>\S+))?\s*$"
)

# Bullet line in Categories / Traits sections — no amount suffix allowed.
LIST_BULLET_RE = re.compile(
    r"^-\s+\[(?P<name>[^\]]+)\]\(cooking/(?P<group>[^/]+)/(?P<slug>[^)]+)\.md\)\s*$"
)


QUALITATIVE_SLUGS = {"phytochemicals", "probiotics"}


def sort_key(title: str) -> tuple:
    """Canonical alphabetical sort key.

    Matches the cooking SKILL's anti-drift rule:
    - case-insensitive
    - strip leading article (`the `, `a `, `an `)
    - digit runs compared by integer value (so `5-bean` < `10-bean`)

    Returns a tuple of `(0, int)` for digit runs and `(1, str)` for text runs
    so a tuple-wise compare never mixes int and str at the same position.
    """
    t = title.lower()
    for article in ("the ", "a ", "an "):
        if t.startswith(article):
            t = t[len(article):]
            break
    parts = re.split(r"(\d+)", t)
    return tuple((0, int(p)) if p.isdigit() else (1, p) for p in parts)


def parse_recipe(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    title = None
    for line in lines:
        if line.startswith("# "):
            title = line[2:].strip()
            break
    if title is None:
        raise ValueError(f"No H1 in {path}")

    sections: dict[str, list[str]] = {}
    current = None
    for line in lines:
        if line.startswith("## "):
            current = line[3:].strip()
            sections[current] = []
        elif current is not None:
            sections[current].append(line)

    def collect_slugs(section_name: str, expected_group: str) -> list[str]:
        body = sections.get(section_name, [])
        slugs: list[str] = []
        for line in body:
            m = LIST_BULLET_RE.match(line)
            if m and m.group("group") == expected_group:
                slugs.append(m.group("slug"))
        return slugs

    categories = sorted(collect_slugs("Categories", "categories"), key=sort_key)
    traits = sorted(collect_slugs("Traits", "traits"), key=sort_key)

    nutrient_amounts: dict[str, str] = {}
    nutrient_present: set[str] = set()
    for section_name, expected_group in [
        ("Macronutrients", "macronutrients"),
        ("Minerals", "minerals"),
        ("Vitamins", "vitamins"),
        ("Soft Essentials", "soft-essentials"),
    ]:
        for line in sections.get(section_name, []):
            if not line.strip().startswith("- "):
                continue
            m = BULLET_RE.match(line)
            if not m or m.group("group") != expected_group:
                # Bullet-shaped line that didn't pass the strict regex —
                # likely malformed (e.g. `28 g` instead of `28g`, wrong dash,
                # mismatched group). Surface it; recipe-page audits (5.13/5.14)
                # are the right place to fix.
                print(f"[WARN] {path.name}: unparseable bullet → {line!r}",
                      file=sys.stderr)
                continue
            slug = m.group("slug")
            amount = m.group("amount")
            if slug in QUALITATIVE_SLUGS and amount is not None:
                print(f"[WARN] {path.name}: qualitative bullet for {slug!r} "
                      f"carries an amount ({amount!r}) — recipe-page defect",
                      file=sys.stderr)
            elif slug not in QUALITATIVE_SLUGS and amount is None:
                print(f"[WARN] {path.name}: quantitative bullet for {slug!r} "
                      "missing ` — <amount><unit>` suffix — recipe-page defect",
                      file=sys.stderr)
            nutrient_present.add(slug)
            if amount is not None:
                nutrient_amounts[slug] = amount

    return {
        "title": title,
        "slug": path.stem,
        "categories": categories,
        "traits": traits,
        "amounts": nutrient_amounts,
        "present": nutrient_present,
    }


def build_row(recipe: dict) -> str:
    name_cell = f"[{recipe['title']}](cooking/recipes/{recipe['slug']}.md)"
    cats_cell = ", ".join(recipe["categories"]) if recipe["categories"] else EMPTY
    traits_cell = ", ".join(recipe["traits"]) if recipe["traits"] else EMPTY

    cells = [name_cell, cats_cell, traits_cell]
    for _display, slug, kind in NUTRIENT_COLUMNS:
        if kind == "quant":
            cells.append(recipe["amounts"].get(slug, EMPTY))
        else:
            cells.append("yes" if slug in recipe["present"] else EMPTY)
    return "| " + " | ".join(cells) + " |"


def build_table(recipes: list[dict]) -> str:
    headers = ["Recipe", "Categories", "Traits"] + [d for d, _s, _k in NUTRIENT_COLUMNS]
    out = ["| " + " | ".join(headers) + " |",
           "| " + " | ".join(["---"] * len(headers)) + " |"]
    for r in sorted(recipes, key=lambda r: sort_key(r["title"])):
        out.append(build_row(r))
    return "\n".join(out)


def main() -> int:
    recipe_paths = sorted(p for p in RECIPES_DIR.glob("*.md") if p.name != "README.md")
    recipes = [parse_recipe(p) for p in recipe_paths]
    print("# Recipes")
    print()
    print("Back to [Cooking](cooking/README.md)")
    print()
    print(build_table(recipes))
    print(f"\n[INFO] {len(recipes)} recipes parsed.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
