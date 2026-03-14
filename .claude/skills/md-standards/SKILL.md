---
name: md-standards
description: Markdown standards and TOC rules. Use with .md files (exclude README.md).
---

# Markdown Standards

## Headers & TOC

- **H1:** Title only. No numbering/TOC.
- **H2-H4:** Numbered (`1.` → `1.1.` → `1.1.1.`).
- **Anchors:** `<a id="">` own line above H2-H4, blank line between. ID: dot-stripped number + slug (`111-deep-dive`).
- **H5+:** `#####` header or inline **bold**. No numbering/TOC.
- **Nesting:** Never skip levels (H3 → H5 ✗, H3 → H4 ✓).
- **TOC:** `## Table of Contents` after H1. Self-exclude.

See `examples.md` for anchor/TOC formatting details.
