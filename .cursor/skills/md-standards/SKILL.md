---
name: md-standards
description: Global standards for Markdown files (Structure, TOC, and Numbering)
globs: **/*.md
---

# Markdown Structure Standards

## Headers Structure & Table of Contents (TOC)

- **The Title (H1):**
  - Level 1 (`#`) is the document title. 
  - **Exclude** from numbering and the Table of Contents.
- **Numbered Chapters (H2, H3, H4):**
  - These three levels must be hierarchical and indexed in the TOC.
  - **H2:** Primary level (e.g., `1.`, `2.`)
  - **H3:** Secondary level (e.g., `1.1.`, `1.2.`)
  - **H4:** Tertiary level (e.g., `1.1.1.`, `1.1.2.`)
- **Unnumbered Deep Nesting (H5 and below):**
  - Level 5 (`#####`) and deeper must **never** be numbered and **never** appear in the TOC.
- **TOC Requirements:**
  - Place `## Table of Contents` immediately after the H1 Title.
  - **Exclude the "Table of Contents" header itself from the list.**
  - Ensure all H2, H3, and H4 headers are linked **using standard internal anchors: `[Text](#text-slug)`.**