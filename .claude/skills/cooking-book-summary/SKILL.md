---
name: cooking-book-summary
description: Use INSTEAD of book-summary for cookbooks, cooking books, recipes, recipe books, baking, pastry, culinary, food, kitchen, gastronomy.
---

# Cooking Book Summary Skill

Turn a cookbook into distilled, verifiable recipe pages in the Docsify knowledge base.

If you are summarizing a standard chapter-based book, use `book-summary` instead.

## Prerequisites

Load `docsify` and `md-standards` skills before starting.

## Mode selection

**Autonomous mode is the default.** Do not ask the user before starting. Run end-to-end without human interaction, making sensible defaults (keeping all valid recipes, preserving all categories). 

**Guided mode** is only used if the user explicitly asks for it before the run begins.

## Context discipline

Follow the same rules as `book-summary`:
- Never read source files (HTML/TXT under `tmp/`) in the main thread.
- Never re-read completed files in the main thread.
- Cap every agent report.
- Compact at phase boundaries.
- Keep agent prompts self-contained but terse.

## Phase 1: Extract

Uses the exact same extraction mechanics as `book-summary` Phase 1 (locating source, extraction by format).

**Detection heuristics:** If this skill was loaded automatically, verify we actually have a cookbook post-extraction by checking for:
- Filename keywords (recipe, cookbook, etc.).
- TOC scan (entries that look like recipe categories rather than "Chapter N").
- Sample-page shape (an Ingredients heading + a quantity-prefixed list + numbered steps).

If the source is NOT a cookbook, switch to `book-summary` and inform the user.

## Phase 2: Structure

### 2.1 Folder layout

Top-level category is always `docs/cooking/`.
Per book: `docs/cooking/books/<book-slug>/<category>/<recipe-slug>.md`

- `<category>`: Categories as **subfolders**. Discovered from the book itself. Kebab-case, ASCII transliterations (e.g., `main-courses`, `postres`).
- `<recipe-slug>`: kebab-case, ASCII transliteration of the recipe name. Must be descriptive enough to identify the recipe.

### 2.2 Book-root landing page

Create `docs/cooking/books/<book-slug>/README.md`:
- H1 with the book title.
- (Optional) Short context paragraph if the book has a useful introduction.
- `## Categories` list linking to each category folder.
- **Follows `md-standards`** strictly.

### 2.3 Recipe scaffolds

Create one `.md` per recipe containing only the H1:
```markdown
# Recipe Name
```

### 2.4 Progress tracker

Create `tmp/<book-slug>-progress.md` using this exact schema:

```markdown
| Category | Recipe | Slug | Source | Status |
|----------|--------|------|--------|--------|
```
*Categories and recipes come from the source.* The `Slug` column doubles as a lookup table for cross-references during writing.

### 2.5 Sidebar block

Add to `docs/_sidebar.md` under `**Cooking**`.

Example shape:
```markdown
- **Cooking**
  - **Books**
    - [<Book Title>](cooking/books/<book-slug>/README.md)
      - **<Cat A>**
        - [<Recipe 1>](cooking/books/<book-slug>/<cat-a>/<recipe-1-slug>.md)
        - [<Recipe 2>](cooking/books/<book-slug>/<cat-a>/<recipe-2-slug>.md)
      - **<Cat B>**
        - [<Recipe 3>](cooking/books/<book-slug>/<cat-b>/<recipe-3-slug>.md)
```
- The book-title link points to `README.md`. 
- Categories are bold sub-headers. 
- Recipes are alphabetical within each category.

## Phase 3: Write Recipes

### 3.1 Recipe page format

Recipes do NOT strictly follow `md-standards`. **Drop H2/H3 numbering and the Table of Contents.**

1. **H1:** Recipe name only.
2. **Metadata block:** Immediately below H1. Anything a cook needs to plan/execute (prep time, cook time, yield, oven temp). Render as a single blockquote line with `·` separators or a small list. Keep ONLY what the source provides.
3. **`## Ingredients`:** Un-numbered. A two-column Markdown table (`Quantity` | `Ingredient`). Every ingredient must have a quantity exactly as given.
4. **`## Preparation`:** Un-numbered. Numbered list of steps. Use sub-headings if the source splits phases (e.g., "### Dough", "### Filling").
5. **Optional sections:** (e.g., `## Notes`) for less-relevant metadata or variations.

### 3.2 Writing style: Distilled Procedure

The page must contain everything a cook needs to follow the recipe end-to-end, and nothing else. 

- **Keep exactly:** every ingredient, quantity, unit, step, time, temperature, visual cue ("until amber"), rest/proof duration, and equipment requirement.
- **Strip:** author anecdotes, personal stories, philosophy, opinions.
- **Phrasing:** Rewrite prose paragraphs into tight numbered steps. Imperative and concise.
- **Preserve:** Units exactly (no conversions). Ingredient names verbatim (with accents/original spelling).
- **Never invent** an ingredient, quantity, step, time, or temp.
- **No commentary or substitution.**

### 3.3 Cross-recipe references

Any recipe can reference any other recipe.
- **Syntax:** Relative path including category folder: `[<recipe name>](../<category>/<recipe-slug>.md)`
- **Out-of-book references:** Leave as plain text with `<!-- TODO: not in this book -->`. Do not fabricate links.
- Look up target slugs using the progress tracker.

### 3.4 Parallelization

Follow the same parallelization and calibrate-then-parallelize loop as `book-summary`, but skip human calibration feedback unless in guided mode.

## Phase 4: Audit

Audit every recipe. The audit is two-directional:

1. **Nothing fabricated:** No ingredient, quantity, step, time, or temperature in the page that isn't in the source.
2. **Nothing essential dropped:** Every ingredient, quantity, unit, step, time, temperature, visual cue, rest/proof duration, and equipment requirement from the source MUST be in the page. (Missing author anecdotes is correct; missing cooking instructions is a failure).
3. **Checks:** Cross-recipe links resolve, ingredient names spelled as in source, units not silently converted.

Use the same Audit-fix loop and Convergence loop as `book-summary`.

## Phase 5: Narrative

**DROPPED.** Do not write a whole-book narrative summary for cookbooks.

## Phase 6: Finalize

1. Mark all recipes `done` in progress tracker.
2. Verify `README.md` lists every category that exists on disk.
3. Link-check every cross-recipe reference.
4. Verify sidebar renders correctly (`docsify serve docs`).
5. Report completion to user.

## Example (Format illustration only)

```markdown
# Classic French Omelette

> Prep: 5 mins · Cook: 5 mins · Yield: 1 serving

## Ingredients

| Quantity | Ingredient |
|---|---|
| 3 | large eggs |
| 1 tbsp | unsalted butter |
| to taste | fine sea salt |

## Preparation

1. Crack the eggs into a bowl. Season with salt and beat vigorously with a fork until perfectly uniform.
2. Heat a non-stick skillet over medium-high heat. Add butter and swirl until melted and foaming.
3. Pour the eggs into the pan. Immediately shake the pan back and forth while stirring rapidly with a fork.
4. Once the eggs are mostly set but still slightly runny on top, push them to one side of the pan and roll into a cylinder.
5. Invert onto a warm plate and serve immediately.
```