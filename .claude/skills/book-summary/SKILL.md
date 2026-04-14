---
name: book-summary
description: End-to-end process for summarizing a book into the Docsify knowledge base. Use when the user provides a book file (.epub, .pdf, .txt, .md) and wants chapter-by-chapter summaries.
---

# Book Summary Skill

Turn a book into concise, verified chapter summaries in the Docsify knowledge base.

## Prerequisites

Load `docsify` and `md-standards` skills before starting. Follow them throughout.

## Phase 1: Extract

Accept any format. Extract to readable text under `tmp/<book-slug>/`.

| Format | Method |
|--------|--------|
| `.epub` | `unzip -o <file> -d tmp/<book-slug>/` → HTML in `text/` |
| `.pdf` | Install poppler (`brew install poppler`), `pdftotext <file> tmp/<book-slug>/book.txt`. For scanned/image-heavy PDFs where pdftotext produces garbage, fall back to `pdftoppm -png -r 200 <file> tmp/<book-slug>/pages/page` for PNG page images |
| `.txt`/`.md` | Copy directly to `tmp/<book-slug>/` |

Read the TOC/navigation file (e.g., `toc.ncx` for epub) to map chapters to source files.

**Post-extraction**: Read a sample page/chapter to confirm readable output. If garbled or empty, try the fallback or flag to user.

DRM-protected files will fail extraction — inform the user the file must be DRM-free.

`tmp/` is gitignored. Extracted files are ephemeral working copies; final summaries in `docs/` persist.

## Phase 2: Structure

### 2.1 Output folder

Create `docs/<category>/<book-slug>/` (e.g., `docs/software/philosophy-of-software-design/`).

Match `<category>` to existing top-level folders under `docs/`. If none fits, ask the user.

### 2.2 Chapter files

One `.md` per chapter with only the H1:

```markdown
# Ch N: Chapter Title
```

Naming: `chNN_short_snake_case_name.md` (e.g., `ch01_introduction.md`, `ch10_define_errors.md`).

### 2.3 Progress tracker

Create `tmp/<book-slug>-progress.md`:

```markdown
| # | Chapter | Source | Status |
|---|---------|--------|--------|
| 1 | Introduction | part0004.html | pending |
```

### 2.4 User approval

Show structure before writing summaries. Confirm: chapter list, file names, category, chapters to skip (e.g., preface, index).

### 2.5 Sidebar

After approval, add entries to `docs/_sidebar.md` per docsify skill. All chapter links nested under book title.

## Phase 3: Write Summaries

### 3.1 Section organization

Do NOT mirror the book's section numbers. Reorganize into logical thematic groups. Name sections by core concept.

### 3.2 Markdown format

Follow `md-standards` for headings, numbering, TOC, anchors. The H1 (`# Ch N: Chapter Title`) from Phase 2.2 is fixed — do not change it.

### 3.3 Writing style

- **Concise bullet points**, not paragraphs. Strip all filler.
- Lead with **key concept/keyword in bold**, then short dash (`—`) and brief explanation.
- **Concise ≠ context-free.** Each bullet must carry enough meaning for a reader who hasn't read the book to understand *why* the concept matters. If a bare definition leaves someone thinking "so what?", add the implication or a concrete example.
- Sub-bullets only when genuinely needed (e.g., listing examples under a concept).
- Prefer **tables** for comparisons or paired/grouped items.
- **No opinions, no commentary** — just the book's content distilled.
- **Preserve author's terminology exactly.** Do not paraphrase coined terms.
- Target: grasp chapter's core ideas in **under 2 minutes**.
- Aim for **10–20 bullets per chapter** for consistency. Shorter chapters fewer; dense chapters more.

### 3.4 Formal callouts

Only use blockquote callouts when the **author explicitly labels** something as a formal concept (e.g., named "Red Flag" box, numbered "Design Principle"). Do not elevate informal observations.

```markdown
> **Red Flag: Name** — description

> **Design Principle: Name** — description
```

### 3.5 Calibration

Write the first 1–2 chapters manually (not via agents). Get user feedback on style, density, and tone before batching the rest. This establishes the reference standard for agents.

### 3.6 Parallelization

Once a reference chapter is approved, split remaining chapters across agents (~2–4 chapters each). Each agent:

1. Reads this skill (or instructions file if one exists)
2. Reads a completed reference chapter as style example
3. Reads assigned source files
4. Writes each summary
5. Does NOT update progress tracker or sidebar (do centrally to avoid conflicts)

After all agents complete, bulk-update the progress tracker.

## Phase 4: Audit

Audit every summary against source material for inaccuracies, fabrications, and misattributed terminology.

Source files in `tmp/` must still be available. If deleted (e.g., across sessions), re-extract before auditing.

### 4.1 Audit-fix loop (inner)

Each audit agent:
1. Reads source material for assigned chapters
2. Reads corresponding summary
3. Cross-references **every claim** against source
4. Checks: accuracy, no fabrications, terminology preserved, formal callouts correctly labeled
5. Issues found → fix immediately, report what was wrong, re-audit (max 5 iterations)
6. Clean → report "CLEAN", stop

### 4.2 Convergence loop (outer)

Any round with fixes requires another round to confirm. Repeat until **every chapter reports clean on first iteration in the same round** (max 5 outer iterations).

1. Spawn audit-fix agents (~2–3 chapters each) in parallel
2. Did every agent report clean on first iteration?
3. YES → done
4. NO → run another round on chapters that had fixes
5. Repeat until all clean on first iteration, or max 5 outer iterations

**Early graduation**: chapter clean for 2 consecutive rounds → exclude from further rounds.

**Non-convergence**: at max iterations with remaining issues → stop, flag problematic chapters to user with details. Do not silently accept flawed summaries.

### 4.3 Checks

- Every bullet supported by source text
- No fabricated content (concepts, examples, numbers not in source)
- Author's terminology preserved exactly
- Formal callouts only when author explicitly labels them
- No misattributed claims between chapters

## Phase 5: Finalize

1. Mark all chapters `done` in progress tracker
2. Verify sidebar renders correctly (`docsify serve docs`)
3. Confirm collapsible sections work for new book's chapters
4. Report completion to user

## Key files

| What | Where | Git? |
|------|-------|------|
| Summaries | `docs/<category>/<book-slug>/chNN_*.md` | Yes |
| Sidebar | `docs/_sidebar.md` | Yes |
| Source | `tmp/<book-slug>/` | No |
| Progress | `tmp/<book-slug>-progress.md` | No |
