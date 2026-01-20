---
name: md-standards
description: Markdown Standards & TOC
globs: 
  - "**/*.md"
  - "!README.md"
alwaysApply: false
---

# Markdown Standards

## 1. Headers & TOC
- **H1 (Title):** No numbering. Exclude from TOC.
- **H2-H4 (Numbered):** Required in TOC. Use hierarchical numbering:
  - `##` → `1.`
  - `###` → `1.1.`
  - `####` → `1.1.1.`
- **H5+ (Details):** No numbering. Exclude from TOC.
- **TOC Specs:**
  - Section: `## Table of Contents` (self-exclude) directly after H1.
  - Links: Use `[Number. Title](#slug)` format (e.g., `[1.1. Title](#11-title)`).
  