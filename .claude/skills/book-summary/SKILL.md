---
name: book-summary
description: End-to-end process for summarizing a book into the Docsify knowledge base. Use when the user provides a book file (.epub, .pdf, .txt, .md) and wants chapter-by-chapter summaries.
---

# Book Summary Skill

Complete process for turning a book into concise, verified chapter summaries in the Docsify knowledge base.

## Prerequisites

Load the `docsify` and `md-standards` skills before starting. Follow them throughout.

## Phase 1: Extract the Book

Accept a book in any format. Extract to readable text under `tmp/<book-slug>/`.

| Format | Extraction method |
|--------|-------------------|
| `.epub` | `unzip -o <file> -d tmp/<book-slug>/` — produces HTML files in `text/` |
| `.pdf` | Install poppler (`brew install poppler`), then `pdftotext <file> tmp/<book-slug>/book.txt` for text extraction. For scanned or image-heavy PDFs where `pdftotext` produces garbage, fall back to `pdftoppm -png -r 200 <file> tmp/<book-slug>/pages/page` to get PNG page images |
| `.txt` / `.md` | Copy directly to `tmp/<book-slug>/` |

Read the table of contents or navigation file (e.g., `toc.ncx` for epub) to map chapters to source files.

**Post-extraction check**: Read a sample page/chapter to confirm the extraction produced readable content. If the output is garbled, empty, or unreadable, try the fallback method or flag the issue to the user.

**Note**: DRM-protected files will fail extraction. If this happens, inform the user — the file must be DRM-free.

**Note**: `tmp/` is gitignored. Extracted files are ephemeral working copies — the final summaries in `docs/` are what persist.

## Phase 2: Set Up the Structure

### 2.1. Create the output folder

Create `docs/<category>/<book-slug>/` (e.g., `docs/software/philosophy-of-software-design/`).

Choose `<category>` by matching existing top-level folders under `docs/`. If no existing category fits, ask the user what category to use.

### 2.2. Create chapter files

Create one `.md` file per chapter with only the H1 title:

```markdown
# Ch N: Chapter Title
```

**File naming**: `chNN_short_snake_case_name.md` (e.g., `ch01_introduction.md`, `ch10_define_errors.md`).

### 2.3. Create a progress tracker

Create `tmp/<book-slug>-progress.md` with a table mapping chapters to source files and status:

```markdown
| # | Chapter | Source | Status |
|---|---------|--------|--------|
| 1 | Introduction | part0004.html | pending |
| 2 | ... | ... | pending |
```

### 2.4. Get user approval

Show the structure to the user before writing any summaries. Confirm chapter list, file names, category, and any chapters to skip (e.g., preface, index).

### 2.5. Update the sidebar

After the user approves the structure, add entries to `docs/_sidebar.md` following the docsify skill conventions. All chapter links should be nested under the book title.

## Phase 3: Write Summaries

### 3.1. Section organization

- **Do NOT mirror the book's own section numbers 1:1.** Reorganize content into logical thematic groups that best convey the chapter's ideas.
- Name sections based on the core concept they cover.

### 3.2. Markdown format

Follow `md-standards` for all heading, numbering, TOC, and anchor rules. The H1 title (`# Ch N: Chapter Title`) was created in Phase 2.2 — do not change it.

### 3.3. Writing style

- **Concise bullet points**, not paragraphs. Strip all filler.
- Lead with the **key concept or keyword in bold**, then a short dash (`—`) and a brief explanation.
- **Concise does NOT mean stripped of context.** Each bullet should carry enough meaning that a reader who hasn't read the book understands *why* the concept matters, not just *that* it exists. If a bare definition would leave someone thinking "so what?", add a short clause with the implication or a concrete example.
- Use sub-bullets only when genuinely needed (e.g., listing examples under a concept).
- Prefer **tables** for comparisons or paired/grouped items.
- **No opinions, no commentary** — just the book's content distilled.
- **Preserve the author's terminology exactly.** Do not paraphrase the author's coined terms.
- Target: someone reviewing this should grasp the chapter's core ideas in **under 2 minutes**.
- Aim for roughly **10–20 bullets per chapter** as a baseline. Shorter chapters may need fewer; dense chapters may need more — but this range keeps summaries consistent.

### 3.4. Formal callouts (red flags, design principles, etc.)

Only use blockquote callouts when the **author explicitly labels** something as a formal concept (e.g., a named "Red Flag" box, a numbered "Design Principle"). Do not elevate informal observations into formal callouts.

```markdown
> **Red Flag: Name** — description

> **Design Principle: Name** — description
```

### 3.5. Calibration

Write the first 1–2 chapters manually (not via agents) and get user feedback on style, density, and tone before batching the rest. This establishes the reference standard that agents will follow.

### 3.6. Parallelization

Once a reference chapter is approved, split remaining chapters across multiple agents (~2–4 chapters per agent) to avoid context overload. Each agent should:

1. Read this skill (or the instructions file if one exists)
2. Read a completed reference chapter as a style example
3. Read its assigned source files
4. Write each summary
5. NOT update the progress tracker or sidebar (do that centrally to avoid conflicts)

After all agents complete, bulk-update the progress tracker.

## Phase 4: Audit

Audit every summary against its source material to catch inaccuracies, fabrications, and misattributed terminology.

**Important**: Source files in `tmp/` must still be available for this phase. If they've been deleted (e.g., across sessions), re-extract them before auditing.

### 4.1. Audit-fix loop (inner loop)

Each audit agent:
1. Reads the source material for its assigned chapters
2. Reads the corresponding summary
3. Cross-references **every claim** against the source
4. Checks: accuracy, no fabrications, author's terminology preserved, formal callouts correctly labeled
5. If issues found: fixes immediately, reports what was wrong, re-audits (max 5 iterations)
6. If clean: reports "CLEAN" and stops

### 4.2. Convergence loop (outer loop)

Any round that produces fixes requires another round to confirm those fixes are clean. Repeat until **every chapter reports clean on its first iteration in the same round** (max 5 outer loop iterations).

**Process:**
1. Spawn audit-fix agents (split ~2–3 chapters each) — all run in parallel
2. Collect results: did every agent report clean on its first iteration?
3. If YES → done
4. If NO → run another round on the chapters that had fixes (to verify the fixes didn't introduce new issues)
5. Repeat until all come back clean on first iteration in the same round, or max 5 outer iterations

**Early graduation:** if a chapter has been clean for 2 consecutive rounds, exclude it from further rounds — it has converged and does not need re-auditing.

**Non-convergence:** if max iterations are reached and some chapters still have issues, stop and flag the problematic chapters to the user with details on what's not converging. Do not silently accept flawed summaries.

### 4.3. What to check

- Every bullet point is supported by the source text
- No fabricated content (concepts, examples, numbers not in the source)
- Author's terminology preserved exactly
- Formal callouts (red flags, design principles) only used when the author explicitly labels them
- No misattributed claims between chapters

## Phase 5: Finalize

1. Mark all chapters as `done` in the progress tracker
2. Verify the sidebar renders correctly (`docsify serve docs`)
3. Confirm collapsible sections work for the new book's chapters
4. Report completion to the user

## Summary of key files

| What | Where | Persists in git? |
|------|-------|------------------|
| Chapter summaries | `docs/<category>/<book-slug>/chNN_*.md` | Yes |
| Sidebar | `docs/_sidebar.md` | Yes |
| Extracted source | `tmp/<book-slug>/` | No (gitignored) |
| Progress tracker | `tmp/<book-slug>-progress.md` | No (gitignored) |
