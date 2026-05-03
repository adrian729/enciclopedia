---
name: book-summary
description: End-to-end process for summarizing a book into the Docsify knowledge base. Use when the user provides a book file (.epub, .pdf, .txt, .md) and wants chapter-by-chapter summaries.
---

# Book Summary Skill

Turn a book into concise, verified summaries in the Docsify knowledge base.

If the source is a cookbook (recipe-organized rather than chapter-organized), use the `cooking-book-summary` skill instead.

## Prerequisites

Load `docsify` and `md-standards` skills before starting. Follow them throughout.

## Mode selection

Before Phase 1, ask the user once:

> Do you want to guide this run (review structure, give calibration feedback) or run it autonomously end-to-end?

- **Guided mode**: stop at the normal checkpoints — Phase 2.4 (structure approval) and Phase 3.5 (calibration feedback).
- **Autonomous mode**: skip every feedback checkpoint until Phase 6. Make sensible default choices (pick the closest existing category, keep the obvious chapter list, skip prefaces/indexes/acknowledgements by default) and proceed straight through. Only interrupt for genuine blockers that cannot be resolved without the user: source file not found in the library, DRM-protected file that fails extraction, or Phase 4 non-convergence at max iterations.

Record the chosen mode and honor it for the rest of the run. In autonomous mode, do not ask the user *anything* — including the structure confirmation in 2.4 and the calibration review in 3.5 — until Phase 6 reports completion.

## Context discipline

A full book run dispatches many agents and touches many files. Without discipline, the main conversation balloons past 40% context and forces compaction mid-run. Follow these rules across every phase:

- **Never read source chapter files (HTML/TXT under `tmp/`) in the main thread.** Source reading belongs inside agents. The only main-thread reads on source are (a) one sample file in Phase 1 to confirm extraction worked, and (b) the TOC/nav file in Phase 2.
- **Never re-read a completed summary file in the main thread to spot-check an agent's fix.** If you need verification, send another agent. Main-thread `Read` on `docs/<category>/books/<book-slug>/*.md` is reserved for: the reference chapter during Phase 3.5 calibration, and the narrative `book_summary.md` while authoring it in Phase 5.
- **Cap every agent report.** Include `Report in under 100 words.` (or under 50 for audit agents) in every Agent prompt. Audit agents report only `CLEAN` or a terse fix list — no recaps of what the summary says, no explanations of why a fix was needed beyond a phrase.
- **Compact at phase boundaries.** After Phase 3 completes, after Phase 4 converges, and after Phase 5 audit is clean, the prior phase's detail stops being load-bearing. Proactively `/compact` at these seams rather than waiting for auto-compact.
- **Keep agent prompts self-contained but terse.** Point agents at the skill file and the reference chapter; don't inline long style recaps.
- **Don't dump tool output into the thread.** When listing files or checking progress, prefer `wc -l`, `ls | head`, or counts over full listings.

Tradeoff: less visibility into each agent's reasoning. Mitigation: the audit loop in Phase 4 is the safety net — trust it to catch silent misbehavior rather than paying context to watch every agent.

## Phase 1: Extract

### Locating the source file

Before extracting, find the book file. Check in this order:

1. **Explicit path** — if the user provided a file path, use it.
2. **`~/projects/resources/books/`** — the local book library. Filenames are inconsistent (may include ISBNs, authors, publishers, scan codes), so match by keywords from the title or author: `ls ~/projects/resources/books/ | grep -i <keyword>`.
3. **Ask the user** — only if the library has no match. Don't guess or download.

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

Create `docs/<category>/books/<book-slug>/` (e.g., `docs/software/books/philosophy-of-software-design/`).

Books always live in a `books/` subfolder so they're visually distinguished from non-book topical pages in the sidebar. The `books/` segment immediately precedes the book slug.

Match `<category>` to existing top-level folders under `docs/`. If none fits, ask the user.

**Subcategories are allowed.** When a book genuinely belongs under an existing sub-topic, place it under that subcategory's own `books/` folder — e.g., `docs/life/parenting/books/<book-slug>/`. Use a subcategory only if one already exists or the user requests it; do not invent new subcategory layers.

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

**Autonomous mode**: skip this step. Pick the closest category, keep all main chapters, skip prefaces / forewords / acknowledgements / indexes by default, and proceed.

### 2.5 Sidebar

After approval, add entries to `docs/_sidebar.md` per docsify skill. Books always live under a `**Books**` subheader inside their category (matching the `<category>/books/` folder layout from 2.1). Mirror the folder structure exactly: every path segment between the top-level category and the book slug appears as a nested bold header in the sidebar.

- For a book at `docs/<category>/books/<slug>/`: nest under `**<Category>**` → `**Books**` → book entry.
- For a book at `docs/<category>/<subcategory>/books/<slug>/`: nest under `**<Category>**` → `**<Subcategory>**` → `**Books**` → book entry.

If the `**Books**` header (or an intermediate subcategory header) doesn't already exist in the sidebar for that category, create it. Place the `**Books**` group after non-book topical entries in the same category so books visually trail topical pages.

Initial structure: the book-title link points to `ch01`, chapter links nested under it. Phase 5.4 will finalize the structure once `book_summary.md` exists.

Example shape (single category):

```markdown
- **<Category>**
  - [Topical Page](<category>/topical.md)
  - **Books**
    - [<Book Title>](<category>/books/<book-slug>/ch01_*.md)
      - [Ch 1: ...](<category>/books/<book-slug>/ch01_*.md)
      - [Ch 2: ...](<category>/books/<book-slug>/ch02_*.md)
```

Example shape (subcategory):

```markdown
- **<Category>**
  - **<Subcategory>**
    - **Books**
      - [<Book Title>](<category>/<subcategory>/books/<book-slug>/ch01_*.md)
        - [Ch 1: ...](<category>/<subcategory>/books/<book-slug>/ch01_*.md)
```

## Phase 3: Write Summaries

### 3.1 Section organization

Do NOT mirror the book's section numbers. Reorganize into logical thematic groups. Name sections by core concept.

### 3.2 Markdown format

Follow `md-standards` for headings, numbering, TOC, anchors. The H1 (`# Ch N: Chapter Title`) from Phase 2.2 is fixed — do not change it.

### 3.3 Writing style

- **Concise bullet points**, not paragraphs. Strip all filler.
- Lead with **key concept/keyword in bold**, then short dash (`—`) and brief explanation.
- **Concise ≠ context-free.** Each bullet must carry enough meaning for a reader who hasn't read the book to understand *why* the concept matters. If a bare definition leaves someone thinking "so what?", add the implication or a concrete example.
- **Definitions must be clear and complete.** When introducing a coined term or named concept, the explanation should actually define it — what it is, what distinguishes it — not just restate the label. "Deep modules — modules with simple interfaces and complex implementations" beats "Deep modules — a key idea Ousterhout emphasizes." Cross-references to terms defined elsewhere *in this same summary* are fine; assume the reader is reading top-to-bottom.
- **Prefer concrete over abstract.** When the author gives a concrete example, name or reference it; don't reduce a vivid illustration to a generic phrase. A concept paired with one short example beats two abstract restatements.
- **First-pass test:** before moving on, re-read each bullet. If the explanation could apply to almost any concept ("X is important", "Y matters", "use X carefully"), it isn't a definition — rewrite it to say what the concept actually *is* or *does*.
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

Write the first 1–2 chapters manually (not via agents). Before showing them to the user:

1. **Self-audit pass.** Run a single audit on the calibration chapter(s) using the same checks as Phase 4.1 (accuracy against source, no fabrications, terminology preserved, formal callouts only when explicitly labeled) **plus the Phase 3.3 clarity bar** (definitions actually define, no label-only bullets, concrete examples preserved). Fix any issues found.
2. **Then ask the user** for feedback on style, density, tone, and clarity.

This establishes the reference standard for agents. Catching accuracy and clarity issues before the user reviews keeps their feedback focused on style/tone rather than correctness.

**Autonomous mode**: still write 1–2 chapters manually and run the self-audit pass — they remain the reference for the parallel agents in 3.6 — but skip step 2 and proceed directly to Phase 3.6 once the self-audit is clean.

### 3.6 Parallelization

Once a reference chapter is approved, split remaining chapters across agents (~2–4 chapters each). Each agent:

1. Reads this skill (or instructions file if one exists)
2. Reads a completed reference chapter as style example
3. Reads assigned source files
4. Writes each summary
5. Does NOT update progress tracker or sidebar (do centrally to avoid conflicts)
6. **Reports in under 100 words**: just the list of files written, one line each. No recap of contents.

After all agents complete, bulk-update the progress tracker from the file list alone — do not Read the summaries to verify them; Phase 4 is where verification happens.

**Compact checkpoint**: after Phase 3 finishes, proactively `/compact` before starting Phase 4. The per-chapter drafting detail is no longer needed.

## Phase 4: Audit

Audit every summary against source material for inaccuracies, fabrications, and misattributed terminology.

Source files in `tmp/` must still be available. If deleted (e.g., across sessions), re-extract before auditing.

### 4.1 Audit-fix loop (inner)

Each audit agent:
1. Reads source material for assigned chapters
2. Reads corresponding summary
3. Cross-references **every claim** against source
4. Checks: accuracy, no fabrications, terminology preserved, formal callouts correctly labeled
5. Issues found → fix immediately in the file, re-audit (max 5 iterations)
6. Clean → report "CLEAN", stop

**Report format — strict cap, under 50 words total.** One line per chapter:
- `chNN: CLEAN` if no fixes were needed
- `chNN: N fixes — <terse phrase per fix>` (e.g., `ch05_03: 2 fixes — DB taxonomy, removed fabricated IDs bullet`)

No recaps of what the summary covers, no explanations of why fixes were correct, no diffs. The fix is in the file; the report is just the ledger.

### 4.2 Convergence loop (outer)

Any round with fixes requires another round to confirm. Repeat until **every chapter reports clean on first iteration in the same round** (max 5 outer iterations).

1. Spawn audit-fix agents (~2–3 chapters each) in parallel
2. Did every agent report clean on first iteration?
3. YES → done
4. NO → run another round on chapters that had fixes
5. Repeat until all clean on first iteration, or max 5 outer iterations

**Early graduation**: chapter clean for 2 consecutive rounds → exclude from further rounds.

**Non-convergence**: at max iterations with remaining issues → stop, flag problematic chapters to user with details. Do not silently accept flawed summaries.

**Compact checkpoint**: after Phase 4 converges, proactively `/compact` before starting Phase 5. The audit round-by-round fix ledger is no longer needed.

### 4.3 Checks

- Every bullet supported by source text
- No fabricated content (concepts, examples, numbers not in source)
- Author's terminology preserved exactly
- Formal callouts only when author explicitly labels them
- No misattributed claims between chapters

## Phase 5: Narrative Summary

Produce a single readable whole-book summary at `docs/<category>/books/<book-slug>/book_summary.md`. Target: 15–30 minute read (≈3,000–6,000 words). Reader is someone who will not read the book itself and wants the core ideas in one sitting.

### 5.1 Scope and position

Written only after Phase 4 converges (all chapter summaries clean). Uses the audited chapter summaries as scaffolding and the source material in `tmp/` as ground truth. If `tmp/` was cleared between sessions, re-extract per Phase 1 before starting.

### 5.2 File format

- H1: `# <Book Title>: Summary` (e.g., `# A Philosophy of Software Design: Summary`)
- **Standard intro blockquote** immediately after H1, verbatim across every book:

  ```markdown
  > **Read time: ~15–30 minutes.** This page is a single-sitting narrative summary of the book's key ideas. For a detailed chapter-by-chapter reference with the author's definitions and concrete examples, see the chapter entries in the sidebar.
  ```
- `## Table of Contents` after the intro (follow `md-standards`)
- H2–H4 numbered per `md-standards`
- Organize by **theme/argument**, not by chapter order. The narrative should flow as an essay, weaving related chapters together under shared headings. Chapter numbers are an implementation detail of the source, not of the summary.

### 5.3 Writing style

- **Prose-first.** Full sentences and paragraphs are the default. A reader should be able to read it top-to-bottom without losing the thread.
- **Bullets only for genuine enumerations** — a list of principles, a list of steps, a side-by-side comparison. Never as a substitute for an explanation.
- **Preserve author's terminology exactly** (same rule as chapter summaries). When introducing a coined term for the first time, bold it.
- **Explain, don't just name-drop.** Each key concept gets a sentence or two of context: what it means, why it matters, a concrete example when the author provides one.
- **No opinions, no commentary, no comparisons to other books.** The narrative should read as a faithful condensation of the author's own argument.
- **Voice:** third-person, neutral ("Ousterhout argues…", "The book distinguishes…"). Don't address the reader as "you".
- **Open with the book's thesis** in 2–4 sentences — what problem it's solving and the author's core claim.
- **Close with a short "Key takeaways" section** (5–10 bullets) restating the most important ideas for recall.

### 5.4 Sidebar entry

Finalize the book's sidebar block so readers land on the narrative summary by default and can drill into chapters from there:

1. **Change the book title link** from `ch01_*.md` to `book_summary.md` — clicking the book name in the sidebar opens the narrative summary.
2. **Add Book Summary as the FIRST nested entry**, above all chapter links. Any topical summary files (e.g., `summary_design_principles.md`) stay at the bottom of the block.

Final shape (the book entry lives inside the `**Books**` group established in Phase 2.5; indentation reflects that nesting — the book title sits one level below `**Books**`, chapters two levels below):

```markdown
  - **Books**
    - [<Book Title>](<category>/books/<book-slug>/book_summary.md)
      - [Book Summary](<category>/books/<book-slug>/book_summary.md)
      - [Ch 1: ...](<category>/books/<book-slug>/ch01_*.md)
      - [Ch 2: ...](<category>/books/<book-slug>/ch02_*.md)
      ...
      - [Ch N: ...](<category>/books/<book-slug>/chNN_*.md)
      - [<Topical Summary>](<category>/books/<book-slug>/summary_*.md)   # if any
```

If the book lives under a subcategory, the `**Books**` group sits one level deeper (under the subcategory header) and every entry below it is indented an extra two spaces accordingly.

### 5.5 Authoring

Write this phase **centrally**, not via parallel agents. The narrative requires a single coherent voice; splitting it across agents produces stitched-together sections that don't flow. Input: all chapter summaries + the source material for any section where the chapter summary is too condensed to write prose from.

### 5.6 Audit

Run the narrative summary through the same audit loop as Phase 4:

- Spawn an audit agent that reads `book_summary.md` alongside the source material
- Cross-reference every factual claim, every named concept, every example against source
- Check: accuracy, no fabrications, author's terminology preserved, no smuggled opinions or cross-book references
- Fix-and-reaudit loop, max 5 iterations
- Must reach CLEAN on first iteration of a round before proceeding to Phase 6
- Agent reports under 50 words, same format as Phase 4.1 (`CLEAN` or terse fix list). Do not re-read `book_summary.md` in the main thread to verify — trust the audit agent and send another if in doubt.

Because this is a single file, parallelization doesn't apply — one audit agent covers the whole document.

**Compact checkpoint**: after Phase 5 audit reaches CLEAN, proactively `/compact` before Phase 6. Only the final sidebar edit and progress-tracker update remain.

## Phase 6: Finalize

1. Mark all chapters `done` in progress tracker
2. Verify `book_summary.md` is present and audited clean
3. Verify sidebar renders correctly (`docsify serve docs`)
4. Confirm collapsible sections work for new book's chapters and the Book Summary link appears last
5. Report completion to user

## Key files

| What | Where | Git? |
|------|-------|------|
| Summaries | `docs/<category>/books/<book-slug>/chNN_*.md` | Yes |
| Narrative summary | `docs/<category>/books/<book-slug>/book_summary.md` | Yes |
| Sidebar | `docs/_sidebar.md` | Yes |
| Source | `tmp/<book-slug>/` | No |
| Progress | `tmp/<book-slug>-progress.md` | No |
