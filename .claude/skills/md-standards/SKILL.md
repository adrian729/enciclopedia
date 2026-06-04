---
name: md-standards
description: Markdown standards and TOC rules. Use with .md files (exclude README.md).
---

# Markdown Standards

## Headers & TOC

- **H1:** Title only. No numbering/TOC.
- **H2-H4:** Numbered (`1.` → `1.1.` → `1.1.1.`).
- **H5+:** `#####` header or inline **bold**. No numbering/TOC.
- **Nesting:** Never skip levels (H3 → H5 ✗, H3 → H4 ✓).
- **TOC:** `## Table of Contents` after H1. Self-exclude. IDs: dot-stripped number + slug (`111-deep-dive`).

See `examples.md` for anchor/TOC formatting details.

## Tildes

Docsify's marked renders a PAIR of single tildes as strikethrough (`del: /^(~~?)(?=[^\s~])([\s\S]*?[^\s~])\1(?=[^~]|$)/`), so `(~0.2%) vs (~0.3%)` strikes through everything between the tildes. GitHub renders the same way.

- **Bare `~` in prose is forbidden** — always escape: `\~30%` (renders as a literal `~`). A lone `~` is safe today but becomes a strikethrough bug when a second one lands in the same paragraph.
- `~~text~~` for intentional strikethrough and `~` inside code spans/fences are fine.
- Exception: `docs/cooking/macronutrients/README.md` keeps bare `~` (frozen table, see `cooking-book-summary`; safe — one `~` per cell can't pair).
- **Verify:** `python3 scripts/check_tildes.py` must exit clean (`--fix` auto-escapes).
