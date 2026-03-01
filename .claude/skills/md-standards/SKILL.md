---
name: md-standards
description: Markdown standards and TOC rules for .md files (exclude README.md).
---

# Markdown Standards

## Headers & TOC
- **H1:** Title only. **No** numbering. **No** TOC.
- **H2-H4:** Hierarchical numbering (`1.` → `1.1.` → `1.1.1.`).
- **Anchors:** Place explicit HTML anchors on their own line **above** every H2-H4 header, separated by a blank line.
- **H5+:** Bold text or simple header. **No** numbering. **No** TOC.
- **TOC:** Insert `## Table of Contents` after H1. **self-exclude**.

**Note:** For strict formatting of hierarchical anchors and TOC links, read `examples.md`.