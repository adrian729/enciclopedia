---
name: md-standards
description: Markdown Standards & TOC
globs: 
  - "**/*.md"
  - "!README.md"
alwaysApply: false
---

# Markdown Standards

## Headers & TOC
- **H1:** Title only. **No** numbering. **No** TOC.
- **H2-H4:** Hierarchical numbering (`1.` → `1.1.` → `1.1.1.`).
- **H5+:** Bold text or simple header. **No** numbering. **No** TOC.
- **TOC:** Insert `## Table of Contents` after H1. **self-exclude**.

## Example (Strict)
`### 1.1. My Title` → TOC: `[1.1. My Title](#11-my-title)`