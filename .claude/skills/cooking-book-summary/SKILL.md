---
name: cooking-book-summary
description: Use INSTEAD of book-summary for cookbooks, cooking books, recipes, recipe books, baking, pastry, culinary, food, kitchen, gastronomy.
---

# Cooking Book Summary Skill

Turn a cookbook into a deterministic set of recipe, category, trait, and book pages in the Docsify knowledge base. The output is faithful to the source, navigable in every direction, and identical across runs.

If you are summarizing a standard chapter-based book, use `book-summary` instead.

## Prerequisites

Load `docsify` and `md-standards` skills before starting.

`md-standards` H2 numbering and table-of-contents do NOT apply under `docs/cooking/**`. The page templates in this skill are the authoritative shape; do not add numbering or a TOC to any cooking page.

## Mode selection

**Autonomous mode is the default.** Do not ask the user before starting. Run end-to-end without human interaction, using sensible defaults (keep all source recipes, map to the closest canonical category/trait, keep all source-provided metadata).

**Guided mode** is only used if the user explicitly asks for it before the run begins.

## Context discipline

A cookbook run dispatches many agents and writes many small files. Without discipline the main thread balloons and forces compaction mid-run. Follow these rules across every phase:

- **Never read source files (HTML/TXT/PDF under `tmp/`) in the main thread.** Source reading belongs inside agents. The only main-thread reads on source are (a) one sample after extraction to confirm readable output, and (b) the TOC/nav file in Phase 2.
- **Never re-read a completed recipe page in the main thread to spot-check an agent's fix.** If you need verification, send another audit agent.
- **Cap every agent report.** Include `Report in under 100 words.` (or under 50 for audit agents) in every Agent prompt.
- **Compact at phase boundaries.** Proactively `/compact` after Phase 3, after Phase 5 converges, and before Phase 6.
- **Keep agent prompts self-contained but terse.** Point agents at this skill; do not inline long style recaps.

## Folder structure

The cooking section uses a flat four-section layout. Recipes live in one global folder; categories, traits, and books are separate global indexes that all reference recipes.

```
docs/cooking/
├── README.md                              # Cooking landing page
├── recipes/
│   ├── README.md                          # Alphabetical list of every recipe
│   ├── classic-french-omelette.md
│   ├── banana-bread.md
│   └── banana-bread--joy-of-cooking.md   # only on slug collision
├── categories/
│   ├── README.md                          # Alphabetical list of every category in use
│   ├── breakfast.md
│   ├── dessert.md
│   └── soup.md
├── traits/
│   ├── README.md                          # Alphabetical list of every trait in use
│   ├── easy.md
│   ├── fast.md
│   └── one-pot.md
└── books/
    ├── README.md                          # Alphabetical list of every book summarized
    └── fast-easy-cheap-vegan.md
```

**Why flat instead of per-book folders:** every recipe is a globally addressable page that can belong to many categories and many traits and appear in multiple books. A nested per-book layout breaks that fan-in.

## Anti-drift rules

These rules apply to every slug, label, and template field. They are what make repeated runs converge to the same output. Agents do not re-decide these — they apply them.

### Slug normalization

Applies to every slug (recipes, categories, traits, books):

- Lowercase ASCII only. Transliterate accents: `crème` → `creme`, `piña` → `pina`, `jalapeño` → `jalapeno`.
- Words separated by single `-`. No underscores, no spaces, no double dashes (`--` is reserved for the collision suffix).
- Numbers as digits, not words: `30-min`, not `thirty-min`.
- No trailing punctuation, no parentheses, no apostrophes (drop them: `devil's-food` → `devils-food`).
- No leading numbers unless they are part of the dish identity (see "Recipe-name strip-list" below).

### Singular by default

Category and trait slugs are singular forms unless the term is naturally plural in English. The lexicons below already encode the chosen form; agents do not re-decide. Plural exceptions present in the lexicons: `mixes`, `noodles` (collapsed into `pasta`), `greens`. Singular: `dessert`, `soup`, `main`, `salad`, `snack`.

### Lexicon-first rule

Before creating any new `categories/<slug>.md` or `traits/<slug>.md` file, the agent MUST read the corresponding `README.md` (the live lexicon) AND consult the canonical lexicons in this skill. If any existing entry semantically fits — including via its alias list — that existing entry is reused. Creating a new lexicon entry requires explicit user approval; in autonomous mode, surface the unmapped term to the user instead of silently inventing a new file.

### Alias collapse

Each lexicon entry below has an explicit "Aliases" line. Source terms matching any alias map to the canonical slug. Do not create per-alias files.

### Recipe-name strip-list

The following descriptors are removed from recipe titles unless they are part of the dish identity. They typically resurface as traits, or are dropped silently.

- **Time prefixes**: `5-minute`, `10-minute`, `15-minute`, `20-minute`, `25-minute`, `30-minute`, `45-minute`, `60-minute`, `quick`, `fast`, `speedy`, `lickety-split`, `asap`, `instant`, `no-sweat`. → If source claims it, add the `fast` trait when total time ≤ 30 min.
- **Effort prefixes**: `easy`, `easy-as`, `easy-peasy`, `simple`, `no-fuss`, `lazy`, `get-er-done`, `low-maintenance`, `cheater`, `personalized`, `presto`, `grab-blend`, `grab-and-go`. → If source explicitly markets it as easy, add the `easy` trait.
- **Marketing prefixes**: `better`, `best-ever`, `ultimate`, `gorgeous`, `homemade`, `diy` (only when not part of dish identity), `loaded` (when redundant), `mix-n-match`. → Drop silently.
- **Ingredient-count prefixes**: `3-ingredient`, `4-ingredient`, `5-ingredient`, `10-ingredient`. → Drop silently unless the count IS the dish identity.

**Identity exceptions kept:** `7-layer dip`, `three-cheese pizza`, `5-bean chili`, `s'mores`, `5-spice`. When the count or qualifier IS the dish, leave it.

### Book slug format

Kebab-case of the book's main title. Drop subtitle, edition, author, publisher, and ISBN. Examples:

- "Fast Easy Cheap Vegan" → `fast-easy-cheap-vegan`
- "The Joy of Cooking, 2019 Edition" → `joy-of-cooking` (drop article, drop edition)
- "Salt, Fat, Acid, Heat: Mastering the Elements of Good Cooking" → `salt-fat-acid-heat`

### Recipe slug collision

If `<recipe-slug>.md` already exists in `docs/cooking/recipes/` for a different recipe, the new recipe is written as `<recipe-slug>--<book-slug>.md`. The earlier recipe keeps its bare slug. Two `--` characters separate the parts; this is the only place double-dash appears.

### Metadata blockquote format

Recipe pages start with a single-line blockquote immediately under the H1. Fields appear in this fixed order, separated by ` · `, and are included only when the source provides them:

```
> Prep: 5 mins · Cook: 5 mins · Total: 10 mins · Yield: 1 serving · Cost: under $5 · Equipment: blender
```

- Time format: `5 mins`, `1 hr`, `1 hr 15 mins`. Always abbreviated, lowercase, one canonical form.
- Yield format: `1 serving` / `4 servings` (singular vs plural by count), or use the source's natural unit: `1 loaf`, `12 cookies`, `4 cups`.
- Cost: include only when source explicitly states it.
- Equipment: include only when a non-standard piece is required (blender, pressure cooker, mandoline, etc.). Standard pots/pans/bowls do not warrant a mention.

### Ingredient table format

Two columns exactly:

| Quantity | Ingredient |
|---|---|

- Quantity column preserves the source verbatim, including parentheticals (`½ cup (3.5 ounces)`). Use Unicode fractions (`½`, `¼`, `¾`, `⅓`, `⅔`, `⅛`) to match existing files. Never silently convert units.
- "to taste", "as needed", "for serving", "optional" are valid quantities.
- Ingredient names verbatim, including accents and original spelling.
- No third column. Variations or substitutions go to `## Notes`.

### Alphabetical sort key

Every list that is supposed to be alphabetical uses this sort key:

- Case-insensitive.
- Strip leading articles `the`, `a`, `an` before comparing.
- Numbers sort by numeric value when the leading token is a digit (`5-bean` < `7-layer`).

Lists this applies to: recipes index, categories index, traits index, books index, recipe links inside any category/trait/book page, and the `## Categories`, `## Traits`, `## Books` sections of every recipe page.

### Back-link wording

Fixed wording per page kind. The line lives directly under the H1, separated from the H1 and from the next section by one blank line each side.

| Page kind | Back link text | Target |
|---|---|---|
| `recipes/README.md` | `Back to [Cooking](../README.md)` | `../README.md` |
| `categories/README.md` | `Back to [Cooking](../README.md)` | `../README.md` |
| `traits/README.md` | `Back to [Cooking](../README.md)` | `../README.md` |
| `books/README.md` | `Back to [Cooking](../README.md)` | `../README.md` |
| `categories/<slug>.md` | `Back to [Categories](README.md)` | sibling `README.md` |
| `traits/<slug>.md` | `Back to [Traits](README.md)` | sibling `README.md` |
| `books/<slug>.md` | `Back to [Books](README.md)` | sibling `README.md` |
| `recipes/<slug>.md` | *no back-link line* | — |

Recipe pages omit the back-link because the sidebar handles navigation and the recipe is the deep page; cluttering it with chrome is undesirable.

## Canonical category lexicon

The *type* of dish. Each recipe MUST have at least one and at most two categories. The list below is the v1 lexicon — it is the source of truth when bootstrapping `docs/cooking/categories/README.md` for the first time. After bootstrap, the live `categories/README.md` is authoritative for the current corpus state, but it can grow only via explicit user approval.

- **`appetizer`** — starters, hors d'oeuvres, small plates served before a main meal. *Aliases:* starter, hors-d-oeuvre, small-plate, finger-food.
- **`breakfast`** — morning meals: oatmeals, pancakes, breakfast sandwiches, granola, breakfast bakes, breakfast cookies. *Aliases:* brunch, morning.
- **`bread`** — savory and neutral baked goods: loaves, biscuits, scones, rolls, focaccia (without toppings — with toppings goes to `pizza`), savory muffins. *Aliases:* loaf, scone, biscuit, roll.
- **`dessert`** — sweet finishers: cakes, cookies, pies, ice cream, puddings, sweet bars, sweetened muffins served as treats. *Aliases:* sweets, pastry (when sweet), pudding, candy.
- **`drink`** — beverages: smoothies, hot chocolates, cocktails, teas, lemonades, infusions. *Aliases:* beverage, cocktail, smoothie, tea.
- **`main`** — entrees that don't fit a more specific category: stir-fries, curries, casseroles, grain bowls, stuffed vegetables, meatless mains. The default for "this is the substantial dish at the table". *Aliases:* mains, entree, main-course, bowl, stir-fry, curry, casserole.
- **`mix`** — dry blends and pantry staples: spice mixes, baking mixes, seasoning blends, instant-style packets, hot-chocolate mix powders. *Aliases:* mixes, seasoning, blend, pantry-mix, spice.
- **`pasta`** — pasta and noodle dishes (Italian, Asian, gnocchi, etc.). One bucket — regional style is captured in the recipe name and metadata, not as a separate category. *Aliases:* noodle, noodles, gnocchi, lo-mein, udon.
- **`pizza`** — pizzas and topped flatbreads. *Aliases:* flatbread, focaccia (when topped).
- **`preserve`** — jams, pickles, ferments, chutneys, cured items. *Aliases:* pickle, jam, ferment, chutney, cured.
- **`salad`** — composed cold dishes (leaves, grains, beans, fruit). *Aliases:* slaw.
- **`sandwich`** — fillings between bread or wrappers eaten as a substantial item: classic sandwiches, wraps, burritos, quesadillas, tacos, pinwheels, lettuce wraps. *Aliases:* wrap, burrito, quesadilla, taco, lettuce-wrap, pinwheel.
- **`sauce`** — sauces, dressings, condiments, dips, spreads, gravies, salsas, hummus, pestos. *Aliases:* dressing, dip, condiment, spread, gravy, salsa, pesto, hummus.
- **`side`** — accompaniments served alongside a main: roasted vegetables, grain sides, bean sides. *Aliases:* side-dish, accompaniment.
- **`snack`** — between-meal items: popcorn, chips, energy bars, trail mix, crackers, dip-and-cracker pairings. *Aliases:* snacks, nibble, popcorn.
- **`soup`** — soups, stews, chowders, bisques, brothy bowls. *Aliases:* stew, chowder, bisque, broth.

### Category boundary rules

When a recipe could fit two categories, apply these rules in order:

1. **Wrapper test**: a substantial dish served in a wrapper (burrito, lettuce wrap, taco, quesadilla, pinwheel) is `sandwich`, not `main`. A composed bowl is `main`.
2. **Sweet-breakfast test**: a sweet pastry served as breakfast (cinnamon rolls, sweet breakfast cookies) gets BOTH `breakfast` and `dessert`. The two-category cap covers this.
3. **Soup-stew test**: a soup-stew hybrid gets `soup` only. Single category preferred when it clearly fits.
4. **Bread-vs-dessert test**: banana bread, zucchini bread, and similar quick breads marketed as treats with substantial sweetener go to `dessert`. Plain or savory loaves go to `bread`.
5. **Mix-vs-sauce test**: dry mixes (no liquid) → `mix`. Wet preparations → `sauce`.
6. **Side-vs-main test**: if the source explicitly names it a side, it's `side`. If it could be a meal on its own, it's `main`.

### Recipe → categories mapping examples

(Brief illustrations the agent can pattern-match against. These are how the lexicon resolves real cookbook section names.)

- Source section "Mains" or "Entrees" → `main`.
- Source section "Noodles" → `pasta`.
- Source section "Wraps & Sandwiches" → individual recipes get `sandwich`.
- Source section "Dressings & Sauces" → individual recipes get `sauce`.
- Source recipe "Loaded Queso Dip" → `sauce` (it's a dip).
- Source recipe "White Bean Pinwheels" → `sandwich` (wrapped).

## Canonical trait lexicon

Recipe characteristics. Zero or more per recipe; section is omitted entirely from the recipe page if the recipe has no traits. Only tag a trait when it's recipe-level — do not tag traits that are universally true at the book level (a vegan cookbook does not tag every recipe with `vegan`; the book's intro carries that). Diet traits get tagged only on recipes that *deviate* from or specifically opt into the property within the book's universe.

This v1 list is closed. Adding a new trait requires explicit user approval.

### Time / effort

- **`fast`** — total time ≤ 30 minutes per source. Subsumes "quick", "speedy", "ASAP", "10-minute", "15-minute", "20-minute", "30-minute". Exact time stays in the metadata blockquote.
- **`easy`** — source explicitly markets it as easy / simple, or technique requires no specialized skill. Subsumes "simple", "no-fuss", "lazy", "lickety-split", "get-er-done", "easy-peasy".
- **`one-pot`** — single vessel cooking. Subsumes "one-pan", "sheet-pan", "skillet-only".
- **`no-cook`** — no heat applied at all (assemble-only).
- **`no-bake`** — no oven required (microwave / stovetop / chill OK).
- **`microwave`** — primary cooking is microwave-only.
- **`pantry`** — uses only shelf-stable ingredients per source.

### Planning

- **`make-ahead`** — source explicitly notes it can be prepped in advance and held.
- **`freezer-friendly`** — source explicitly notes it freezes well.

### Cost

- **`cheap`** — source explicitly markets / labels it as low-cost. Subsumes "budget", "affordable".

### Diet (recipe-level deviations only)

- **`gluten-free`**
- **`dairy-free`**
- **`nut-free`**
- **`vegan`**
- **`vegetarian`**

### Audience

- **`kid-friendly`** — source explicitly calls out kid appeal. Subsumes "kids", "family-friendly".

## Page templates

Every page kind under `docs/cooking/` has a fixed shape. Agents emit these verbatim.

### `docs/cooking/README.md`

```markdown
# Cooking

- [Recipes](recipes/README.md)
- [Categories](categories/README.md)
- [Traits](traits/README.md)
- [Books](books/README.md)
```

### `docs/cooking/recipes/README.md`

```markdown
# Recipes

Back to [Cooking](../README.md)

- [Banana Bread](banana-bread.md)
- [Classic French Omelette](classic-french-omelette.md)
...
```

### `docs/cooking/recipes/<slug>.md`

```markdown
# <Recipe Name>

> Prep: 5 mins · Cook: 5 mins · Yield: 1 serving

## Ingredients

| Quantity | Ingredient |
|---|---|
| 3 | large eggs |
| 1 tbsp | unsalted butter |
| to taste | fine sea salt |

## Preparation

1. Crack the eggs into a bowl. Season with salt and beat with a fork until uniform.
2. Heat a non-stick skillet over medium-high heat. Add butter and swirl until foaming.
3. Pour in the eggs. Shake the pan and stir rapidly with a fork.
4. When mostly set but slightly runny on top, push the eggs to one side and roll into a cylinder.
5. Invert onto a warm plate and serve immediately.

## Notes

- Best eaten immediately; an omelette does not hold.

## Categories

- [Breakfast](../categories/breakfast.md)
- [Main](../categories/main.md)

## Traits

- [Easy](../traits/easy.md)
- [Fast](../traits/fast.md)

## Books

- [Salt Fat Acid Heat](../books/salt-fat-acid-heat.md)
```

Section order is fixed. Sections that are empty:

- `## Notes` — omit if no notes are available.
- `## Traits` — omit entirely if the recipe has zero traits.
- `## Categories` and `## Books` are always present (every recipe has ≥1 of each).

### `docs/cooking/categories/README.md`

```markdown
# Categories

Back to [Cooking](../README.md)

- [Appetizer](appetizer.md)
- [Breakfast](breakfast.md)
- [Dessert](dessert.md)
...
```

Lists every category currently in use under `categories/`. New entries appear here only when a corresponding `<slug>.md` file is created.

### `docs/cooking/categories/<slug>.md`

```markdown
# Breakfast

Back to [Categories](README.md)

- [Banana Bread](../recipes/banana-bread.md)
- [Classic French Omelette](../recipes/classic-french-omelette.md)
...
```

H1 is the humanized form (Title Case, single word for single-word slugs; replace `-` with space for multi-word slugs).

### `docs/cooking/traits/README.md`

```markdown
# Traits

Back to [Cooking](../README.md)

- [Cheap](cheap.md)
- [Easy](easy.md)
- [Fast](fast.md)
...
```

### `docs/cooking/traits/<slug>.md`

```markdown
# Fast

Back to [Traits](README.md)

- [Classic French Omelette](../recipes/classic-french-omelette.md)
...
```

### `docs/cooking/books/README.md`

```markdown
# Books

Back to [Cooking](../README.md)

- [Fast Easy Cheap Vegan](fast-easy-cheap-vegan.md)
- [Salt Fat Acid Heat](salt-fat-acid-heat.md)
...
```

### `docs/cooking/books/<slug>.md`

```markdown
# <Book Title>

Back to [Books](README.md)

<optional 1–2-sentence intro from the source — only if the book's own introduction provides one>

- [Banana Bread](../recipes/banana-bread.md)
- [Classic French Omelette](../recipes/classic-french-omelette.md)
...
```

The bullet list contains every recipe from this book, alphabetical, linking to the recipe's own page (which itself lists the book under `## Books`).

## Sidebar shape

Add the following block to `docs/_sidebar.md` under a top-level `**Cooking**` group. The sidebar deliberately does NOT enumerate every recipe, category, or trait — index pages handle that.

```markdown
- **Cooking**
  - [All Recipes](cooking/recipes/README.md)
  - [Categories](cooking/categories/README.md)
  - [Traits](cooking/traits/README.md)
  - **Books**
    - [<Book Title>](cooking/books/<book-slug>.md)
    - [<Book Title>](cooking/books/<book-slug>.md)
```

The `**Books**` subgroup lists each summarized book, alphabetical, linking to the book's own page.

## Cross-recipe references

A recipe's body (typically the `## Notes` section, occasionally a `## Preparation` step) may reference another recipe.

- **In-corpus**: `[<Recipe Name>](../recipes/<slug>.md)` — relative path, always `../recipes/` since recipe pages live in `recipes/`.
- **Out-of-corpus** (recipe not in any summarized book): leave as plain text and append `<!-- TODO: not in corpus -->`. Do not fabricate links.
- Look up target slugs from the in-flight progress tracker or by listing `docs/cooking/recipes/`.

## Phase 1: Extract

Same mechanics as `book-summary` Phase 1.

1. **Locate the source.** Check explicit user path → `~/projects/resources/books/` (match by keyword via `ls | grep -i`) → ask the user only if no match. Don't guess or download.
2. **Extract** to readable text under `tmp/<book-slug>/`:

   | Format | Method |
   |---|---|
   | `.epub` | `unzip -o <file> -d tmp/<book-slug>/` |
   | `.pdf` | `pdftotext <file> tmp/<book-slug>/book.txt`; fallback `pdftoppm -png -r 200 ...` for image-heavy PDFs |
   | `.txt`/`.md` | copy directly |

3. **Confirm extraction worked** by reading one sample page in the main thread. If garbled or empty, fall back or flag.
4. **Cookbook detection** (since this skill auto-loads on cookbook keywords). Verify the extracted text is actually a cookbook by checking:
   - Filename keywords (recipe, cookbook, cooking, baking, etc.).
   - TOC entries that look like recipe categories (`Mains`, `Desserts`, `Soups`) rather than `Chapter N`.
   - Sample-page shape: an `Ingredients` heading, a quantity-prefixed list, and numbered steps.

   If the source is NOT a cookbook, switch to `book-summary` and inform the user.

DRM-protected files will fail extraction — inform the user the file must be DRM-free.

## Phase 2: Plan

The planning phase is centralized (single agent or main-thread). It produces the slug map and category/trait assignments before any recipe page is written, so writing in Phase 3 is purely mechanical.

### 2.1 Read existing state

- Read `docs/cooking/categories/README.md` and `docs/cooking/traits/README.md` (if they exist) to get the current live lexicons. If these files don't exist yet (first cookbook ever), the v1 canonical lexicons in this skill are the starting point.
- Read `docs/cooking/recipes/README.md` (if it exists) to know which recipe slugs are already taken (for collision detection).
- Read `docs/cooking/books/README.md` (if it exists) to confirm the new book isn't a duplicate.

### 2.2 Enumerate recipes

Walk the source TOC and produce a list of `(book-section-name, recipe-source-title, source-file)` tuples. Skip non-recipe content (front matter, indexes, acknowledgements, glossaries) unless the user requested otherwise in guided mode.

### 2.3 Map source sections to canonical categories

For each source section name (e.g., "Mains", "Soups", "Wraps & Sandwiches"), resolve to the canonical category slug using the lexicon's aliases. If a section name has no mapping (extremely rare with the alias list above), surface to the user — do NOT silently invent a new category.

### 2.4 Per-recipe category and trait assignment

For each recipe:

1. **Categories** (1–2): start with the section's mapped category. Read the recipe's source content to detect a second category if the boundary rules call for it (sweet breakfast, side-vs-main, etc.).
2. **Traits** (0+): scan the recipe's source content for triggers: time claims, "easy" wording, single-vessel preparation, no-cook / no-bake claims, freezer notes, make-ahead notes, source cost claims, dietary deviations from the book baseline, kid-friendly callouts.
3. Apply alias collapse and lexicon-first rules. Never invent.

### 2.5 Apply the recipe-name strip-list

Convert each source recipe title into a clean recipe name by applying the strip-list. Examples:

- "10-Minute Chickpea Lettuce Wraps" → name `Chickpea Lettuce Wraps`, slug `chickpea-lettuce-wraps`, traits include `fast`.
- "3-Ingredient Chocolate Pots" → name `Chocolate Pots`, slug `chocolate-pots`. (3-ingredient is a marketing claim, not the dish identity.)
- "Easy-Peasy Peanut Butter Squares" → name `Peanut Butter Squares`, slug `peanut-butter-squares`, traits include `easy`.
- "7-Layer Dip" → name kept, slug `7-layer-dip` (count IS the identity).

### 2.6 Resolve slug collisions

For each candidate recipe slug, check if `docs/cooking/recipes/<slug>.md` already exists. If yes (and it's a different recipe), use `<slug>--<book-slug>.md`.

### 2.7 Build the progress tracker

Create `tmp/<book-slug>-progress.md`:

```markdown
| Recipe | Slug | Categories | Traits | Source | Status |
|--------|------|------------|--------|--------|--------|
| Classic French Omelette | classic-french-omelette | breakfast, main | easy, fast | text/part0042.html | pending |
```

The tracker doubles as a lookup table during Phase 4.

### 2.8 Surface decisions in autonomous mode

Autonomous mode does NOT pause for approval, but it MUST surface in the final completion report:

- Any source section name that did not map cleanly to a canonical category and the closest fit chosen.
- Any candidate trait that didn't match the lexicon and was therefore dropped.
- Any slug collision and the suffix applied.

The user can then react in a follow-up turn.

## Phase 3: Write recipes

Parallel agents write `docs/cooking/recipes/<slug>.md` files. This phase touches recipe pages only; indexes and the categories/traits/books pages are updated centrally in Phase 4 to avoid write conflicts.

### 3.1 Calibration

Write the first 1–2 recipes manually (not via agents) to establish the reference. Run a quick self-audit against the source for those recipes (Phase 5.1 checks plus template conformance). In autonomous mode, proceed once self-audit is clean.

### 3.2 Parallelization

Split the remaining recipes across agents (~6–10 each). Each agent:

1. Reads this skill.
2. Reads the calibration recipe(s) as a style reference.
3. Reads its assigned source files.
4. For each assigned recipe, writes `docs/cooking/recipes/<slug>.md` per the template, using the slug / categories / traits already decided in Phase 2 (read from the progress tracker).
5. Does NOT update the progress tracker, indexes, or category/trait/book pages.
6. **Reports under 100 words**: a list of files written, one per line. No recap.

Bulk-update the progress tracker centrally from the file list.

**Compact checkpoint**: after Phase 3, proactively `/compact` before Phase 4.

## Phase 4: Update indexes & cross-references

Centralized phase. Single agent (or main thread) writes the index and category/trait/book files so all writes serialize on the same actor and no two agents fight over `categories/dessert.md`.

Steps, in this order:

1. **`recipes/README.md`** — for each new recipe, insert in alphabetical position. Create the file if it didn't exist.
2. **`categories/<slug>.md`** — for each category referenced by any new recipe:
   1. Create the file from the template if it doesn't exist.
   2. Insert each new recipe link in alphabetical position.
3. **`categories/README.md`** — append any newly-created categories in alphabetical position.
4. **`traits/<slug>.md`** — same as 2 but for traits.
5. **`traits/README.md`** — same as 3 but for traits.
6. **`books/<book-slug>.md`** — create from template; list every recipe in this book, alphabetical.
7. **`books/README.md`** — insert the new book in alphabetical position. Create the file if it didn't exist.
8. **`docs/cooking/README.md`** — create from template if it doesn't already exist. (Created once and never modified after.)

## Phase 5: Audit

The audit is the hard bar that catches drift, fabrication, and missed cross-references. Use the same audit-fix-converge loop as `book-summary` Phase 4 (max 5 inner iterations per agent, max 5 outer rounds, early graduation after 2 consecutive clean rounds).

### 5.1 Source fidelity (per recipe)

For each recipe page, read the corresponding source and verify:

- Every ingredient, quantity, and unit matches the source.
- Every step's time, temperature, visual cue, rest/proof duration, and equipment requirement is present.
- Nothing fabricated: no ingredient/step/time/temp on the page that isn't in the source.
- Nothing essential dropped: no source ingredient or step missing from the page.
- Author anecdotes / philosophy / personal stories are correctly stripped.
- Units not silently converted; ingredient names spelled as in source.

### 5.2 Recipe-name purity

The H1 and slug of every recipe page do not contain stripped descriptors unless they're identity exceptions. Violations require renaming the file AND updating every link to it (in `recipes/README.md`, in every category file, every trait file, the book file, and any cross-recipe reference).

### 5.3 Lexicon conformance

Every category and trait used by any recipe exists in the live `categories/README.md` / `traits/README.md` (or the v1 canonical lexicon for first run). No alias slipped through as a new file. No accidental `desserts.md` next to `dessert.md`.

### 5.4 Bidirectional integrity

The most error-prone area. For every cross-reference, both directions must agree.

- For every entry in a recipe's `## Categories`, that recipe link is present in `categories/<slug>.md`.
- For every recipe link in `categories/<slug>.md`, that category is in the recipe's `## Categories`.
- Same two-way check for `## Traits` ↔ `traits/<slug>.md`.
- Same two-way check for `## Books` ↔ `books/<slug>.md`.

Concrete check: for each recipe `R` and each category `C` listed on it, `grep "../recipes/R.md" categories/C.md` must succeed.

### 5.5 Index completeness

Every file under `recipes/`, `categories/`, `traits/`, and `books/` (excluding the directory's own `README.md`) is listed in that directory's `README.md`. Conversely, every entry in any `README.md` has a backing file. Run:

```bash
# Files that exist but aren't indexed
for d in docs/cooking/recipes docs/cooking/categories docs/cooking/traits docs/cooking/books; do
  for f in $d/*.md; do
    [ "$(basename $f)" = "README.md" ] && continue
    grep -q "$(basename $f)" $d/README.md || echo "MISSING in index: $f"
  done
done

# Index entries with no backing file
for d in docs/cooking/recipes docs/cooking/categories docs/cooking/traits docs/cooking/books; do
  rg -o '\[[^\]]+\]\(([^)]+)\)' $d/README.md -r '$1' | while read link; do
    [ -f "$d/$link" ] || echo "DEAD link in $d/README.md: $link"
  done
done
```

### 5.6 Link resolution

Every Markdown link inside `docs/cooking/**` resolves to an existing file:

```bash
rg -o '\[[^\]]+\]\(([^)]+\.md)\)' docs/cooking/ -r '$1' --no-filename | sort -u | while read link; do
  : # cross-check each link with its source file location; agent does this per-file
done
```

Agents do this per-file: for each recipe / category / trait / book page, enumerate every link target and `test -f` the resolved path.

### 5.7 Alphabetical order

Every list that should be alphabetical is alphabetical per the sort key in "Anti-drift rules". Includes: every `README.md`'s bullet list, every category/trait/book page's recipe list, and every recipe page's `## Categories`, `## Traits`, `## Books` sections.

### 5.8 Back-link presence

Every page that should carry a "Back to ..." line has it, with the prescribed wording, immediately under the H1, blank-line separated. Recipe pages do NOT have a back-link line.

### 5.9 Metadata / template conformance

Every recipe page:

- Has H1 followed by a blank line.
- Has the metadata blockquote in the canonical field order using ` · ` separators.
- Has section headers in the canonical order: `Ingredients`, `Preparation`, optional `Notes`, `Categories`, optional `Traits`, `Books`.
- Has a two-column ingredient table — never three columns.
- Uses Unicode fractions in the Quantity column, not ASCII (`½` not `1/2`) — match existing files.

### Audit reports

Audit agents report under 50 words, one line per recipe:

- `<slug>: CLEAN`
- `<slug>: N fixes — <terse phrase per fix>` (e.g., `chocolate-pots: 2 fixes — renamed (3-ingredient stripped), added breakfast category`)

No recaps, no diffs. The fix is in the file; the report is the ledger.

### Convergence

Repeat audit rounds until every recipe reports clean on first iteration of a round, or max 5 outer rounds. At max iterations with remaining issues, stop and surface to the user — do not silently accept flawed output.

**Compact checkpoint**: after Phase 5 converges, proactively `/compact` before Phase 6.

## Phase 6: Finalize

1. Update `docs/_sidebar.md` per the Sidebar shape section. If the `**Cooking**` block already exists, ensure all four indexes are listed and the new book is added to `**Books**` in alphabetical position.
2. Mark every recipe `done` in the progress tracker.
3. Run `docsify serve docs` and spot-check (a) the cooking landing page, (b) a recipe, (c) a category page, (d) a trait page, (e) a book page. Confirm sidebar collapsibles work.
4. Report completion to the user, surfacing any decisions called out in Phase 2.8 (unmapped section names, dropped traits, slug collisions).

## Key files

| What | Where | Git? |
|---|---|---|
| Recipe pages | `docs/cooking/recipes/<slug>.md` | Yes |
| Category pages | `docs/cooking/categories/<slug>.md` | Yes |
| Trait pages | `docs/cooking/traits/<slug>.md` | Yes |
| Book pages | `docs/cooking/books/<slug>.md` | Yes |
| Cooking landing | `docs/cooking/README.md` | Yes |
| Sidebar | `docs/_sidebar.md` | Yes |
| Source extraction | `tmp/<book-slug>/` | No |
| Progress tracker | `tmp/<book-slug>-progress.md` | No |

## What is dropped

- **Phase 5 "Narrative"** from `book-summary` does not apply. Cookbooks don't get a whole-book narrative summary.
- **Per-book folders** under `docs/cooking/books/<book-slug>/<category>/<recipe>.md`. Recipes are global; books are flat reference pages.
- **`md-standards` H2 numbering and TOC.** The cooking templates above are the authoritative shape.
