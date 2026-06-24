---
name: cooking-book-summary
description: Use INSTEAD of book-summary for cookbooks, cooking books, recipes, recipe books, baking, pastry, culinary, food, kitchen, gastronomy. Also load whenever editing any file under docs/cooking/ for any reason (formatting, audits, fixes, sidebar updates, refactors), not only when summarizing a new book.
---

# Cooking Book Summary Skill

Turn a cookbook into a deterministic set of recipe, category, trait, and book pages in the Docsify knowledge base. The output is faithful to the source, navigable in every direction, and identical across runs.

If you are summarizing a standard chapter-based book, use `book-summary` instead.

## Scope

This skill governs ALL edits to `docs/cooking/**`, not only initial cookbook summarization. Any task that creates, modifies, formats, audits, or reorganizes a file under `docs/cooking/` MUST follow the page templates, anti-drift rules, and audit checks in this skill.

- The **page templates**, **anti-drift rules**, and **Phase 5 audit checks** apply to every edit, even one-off fixes (typo corrections, link fixes, lexicon updates, formatting passes).
- The **Phase 1–4 and Phase 6 pipeline** applies only to fresh cookbook summarization runs. For maintenance tasks, skip the pipeline and apply the relevant rules directly.

**Authority over conflicting skills:** Inside `docs/cooking/**`, this skill wins. If `md-standards`, `docsify`, or any future generic skill would apply rules that contradict the templates or anti-drift rules here (e.g., adding `## Table of Contents`, renumbering `## Ingredients` to `## 1. Ingredients`, restructuring the sidebar), follow this skill and ignore the conflicting rule. Outside `docs/cooking/**`, those skills apply normally.

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
├── README.md                       # Cooking landing page
├── ingredients-info.md             # Alphabetical ingredient → nutrient lookup
├── recipes/
│   ├── README.md                   # Alphabetical table of every recipe
│   └── <slug>.md                   # one per recipe (`<slug>--<book>.md` on collision)
├── categories/
│   ├── README.md                   # Alphabetical list of every category in use
│   └── <slug>.md                   # one per category in use
├── traits/
│   ├── README.md                   # Alphabetical list of every trait in use
│   └── <slug>.md                   # one per trait in use
├── books/
│   ├── README.md                   # Alphabetical list of every book summarized
│   └── <book-slug>.md              # one per summarized book
├── macronutrients/                 # ingredient-derived facet
│   ├── README.md                   # one canonical table per group (Category cells link to row pages)
│   └── <slug>.md                   # one per row in the group's README
├── minerals/                       # one <slug>.md per row in minerals/README.md
│   ├── README.md
│   └── <slug>.md
├── vitamins/                       # one <slug>.md per row in vitamins/README.md
│   ├── README.md
│   └── <slug>.md
└── soft-essentials/                # one <slug>.md per row in soft-essentials/README.md
    ├── README.md
    └── <slug>.md
```

**Why flat instead of per-book folders:** every recipe is a globally addressable page that can belong to many categories and many traits and appear in multiple books. A nested per-book layout breaks that fan-in.

**Categories/traits vs. nutrient facets:** categories and traits are *agent-chosen* per recipe (from the canonical lexicons below). Macronutrients, minerals, vitamins, and soft-essentials are *ingredient-derived* — they are not chosen, they are computed from each recipe's `## Ingredients` table via the lookup in `ingredients-info.md`. See `## Nutrient lexicons` and `## Ingredient → nutrient mapping` below.

## Anti-drift rules

These rules apply to every slug, label, and template field. They are what make repeated runs converge to the same output. Agents do not re-decide these — they apply them.

### Slug normalization

Applies to every slug (recipes, categories, traits, books):

- Lowercase ASCII only. Transliterate accents: `crème` → `creme`, `piña` → `pina`, `jalapeño` → `jalapeno`.
- Words separated by single `-`. No underscores, no spaces, no double dashes (`--` is reserved for the collision suffix).
- Numbers as digits, not words: `30-min`, not `thirty-min`.
- No trailing punctuation, no parentheses, no apostrophes (drop them: `devil's-food` → `devils-food`).
- No leading numbers unless they are part of the dish identity (see `### Recipe-name strip-list`).

### Singular by default

Category and trait slugs are singular forms unless the term is naturally plural in English. The lexicons below already encode the chosen form; agents do not re-decide. All current canonical slugs are singular (`dessert`, `soup`, `main`, `salad`, `snack`, `mix`, …); plural source terms (`mixes`, `noodles`, `sweets`, `mains`, `snacks`) appear only in alias lists and collapse to their singular canonical (`mix`, `pasta`, `dessert`, `main`, `snack`).

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

```markdown
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
- Numeric tokens sort by integer value, not ASCII (so `5-bean` < `7-layer` < `10-bean`). The most common case is a leading-digit token, but any embedded digit run is compared numerically.

This sort key applies to: the recipes-index **table rows** (sorted by the `Recipe` cell title) and the comma-separated entries inside each `Categories` / `Traits` cell of that table; the categories/traits/books-index bullet lists; the recipe links inside any category/trait/book page; and the `## Categories`, `## Traits`, `## Books` sections of every recipe page.

### Link path convention

All Markdown links inside `docs/cooking/**` MUST be **absolute from the docs root**, i.e. start with `cooking/...`. This project uses Docsify with the default `relativePath: false`. Relative paths resolve to wrong URLs and break every recipe link.

Examples:

- Index target: `cooking/recipes/README.md`
- Recipe target: `cooking/recipes/banana-bread.md`
- Nutrient row target: `cooking/vitamins/vitamin-b12.md`

Never use `./`, `../`, or bare filenames (e.g. `salad.md`, `README.md`) as the link target. If a sibling page is the target, still write the full `cooking/...` path.

### Back-link wording

Fixed wording per page kind. The line lives directly under the H1, separated from the H1 and from the next section by one blank line each side.

| Page kind | Back link |
|---|---|
| `recipes/README.md` | `Back to [Cooking](cooking/README.md)` |
| `categories/README.md` | `Back to [Cooking](cooking/README.md)` |
| `traits/README.md` | `Back to [Cooking](cooking/README.md)` |
| `books/README.md` | `Back to [Cooking](cooking/README.md)` |
| `categories/<slug>.md` | `Back to [Categories](cooking/categories/README.md)` |
| `traits/<slug>.md` | `Back to [Traits](cooking/traits/README.md)` |
| `books/<slug>.md` | `Back to [Books](cooking/books/README.md)` |
| `macronutrients/README.md` | `Back to [Cooking](cooking/README.md)` |
| `minerals/README.md` | `Back to [Cooking](cooking/README.md)` |
| `vitamins/README.md` | `Back to [Cooking](cooking/README.md)` |
| `soft-essentials/README.md` | `Back to [Cooking](cooking/README.md)` |
| `macronutrients/<slug>.md` | `Back to [Macronutrients](cooking/macronutrients/README.md)` |
| `minerals/<slug>.md` | `Back to [Minerals](cooking/minerals/README.md)` |
| `vitamins/<slug>.md` | `Back to [Vitamins](cooking/vitamins/README.md)` |
| `soft-essentials/<slug>.md` | `Back to [Soft Essentials](cooking/soft-essentials/README.md)` |
| `ingredients-info.md` | `Back to [Cooking](cooking/README.md)` |
| `recipes/<slug>.md` | `Back to [All Recipes](cooking/recipes/README.md)` |

Recipe pages back-link to the recipes index for direct return navigation. The link sits on the standard line under the H1, separated by one blank line above and below, before the metadata blockquote.

### Section-omission rule

A recipe-page section is omitted (heading and body both) when it would be empty:

- `## Notes` — omit if the recipe has no notes.
- `## Traits` — omit if the recipe has zero traits.
- `## Macronutrients`, `## Minerals`, `## Vitamins`, `## Soft Essentials` — omit when the derived list is empty after applying the threshold drop (see `### Threshold model`).

The four nutrient sections always appear in fixed order after `## Books`. Bullets within each section are alphabetical by display name, case-insensitive, B-vitamins by numeric value.

### Frozen-table rule

The canonical tables in `docs/cooking/macronutrients/README.md`, `minerals/README.md`, `vitamins/README.md`, and `soft-essentials/README.md` are **byte-for-byte canonical**. They duplicate the tables in this SKILL's `## Nutrient lexicons` section (4 columns: `Category | Requirement | Function | Example Sources`; the `Category` cell of each row contains a Markdown link of the form `[Display Name](cooking/<group>/<slug>.md)` — never bare display text and never a slug; rows alphabetical by display name, with B-vitamins ordered by numeric value — `Vitamin B1` … `Vitamin B12` — NOT ASCII; `—` for empty cells, `†` for AIs). Audit and formatting passes MUST NOT modify them. Any drift between the SKILL copy and the README copy is a defect — restore from this SKILL. Reformatting attempts (renaming columns back to `Top Sources`/`Best Sources`, adding columns like `Type`, splitting cells into multiple rows, re-sorting B-vitamins as ASCII strings, unlinking the Category cells, splitting the link across lines, etc.) explicitly violate this rule.

### Ingredient-info append-only rule

`docs/cooking/ingredients-info.md` grows monotonically. Existing rows are never deleted by agents; they may be corrected only on explicit user instruction. New rows are inserted in alphabetical position. Cells use display names from `## Nutrient lexicons` with per-100g amount estimates (see the cell content rules in `## Ingredient → nutrient mapping`); entries are sorted alphabetically inside each cell — never reorder them into "frequency" or "priority" order. Empty cells are a single em-dash (`—`, U+2014), never blank, never `none`, never `N/A`.

### Formatting conventions

File-wide style rules. Apply uniformly so audit greps work and diffs stay readable.

- **Slugs in backticks**: `` `breakfast` ``, `` `vitamin-b12` ``. Bold + backticks only inside lexicon definitions where the slug is the bullet anchor.
- **Display names plain** in prose: `Vitamin B12`, `Healthy Fats`. Use backticks only when quoting a literal cell string (e.g., `` `Vitamin B12 (0.9µg/100g)` ``).
- **Cross-section references** use the backticked-heading form: `` `### Threshold model` ``, `` `### 5.13` ``. Never bare prose ("under Anti-drift rules") or double-quoted names.
- **Cross-reference verb**: "see" everywhere. Never "per", "as defined in", "reference".
- **Hard imperative**: **MUST** / **MUST NOT** in caps for load-bearing rules; lowercase "must" only inside example prose. This keeps the file greppable for audits.
- **"Do not" callouts**: inline `**Do NOT** …` at paragraph start. Never as a blockquote.
- **Code-fence languages**: `` ```markdown `` for every markdown example block; `` ```bash `` for shell; `` ```python `` for Python. No bare `` ``` ``.
- **Em-dash** U+2014 `—` for empty cells; separator ` — ` is `space U+2014 space`. Never blank, never `none`, never `N/A`, never hyphen-minus, never en-dash.
- **No space between value and unit**: `28g`, `1.4µg`, `470µg`. Never `28 g`.
- **Humanization** (slug → display name): Title Case, hyphens → spaces. **Omega-3 carve-out: the `omega-3` slug's humanized form RETAINS the hyphen-digit suffix — `Omega-3`, NOT `Omega 3`.** This is the only such carve-out among the 27 v1 slugs. (The lexicon Category column also encodes it as `Omega-3 (EPA/DHA)`; `ingredients-info.md` cells use that full form, recipe-page bullets drop the parenthetical to `Omega-3`. The hyphen-digit retention is identical in both forms.) Distinct from the nutrition rule "marine EPA/DHA only" that gates which sources count — see the `omega-3` Notes cell in `### Canonical units and inclusion thresholds per nutrient`.
- **B-vitamin ordering** is by **numeric value, not ASCII**: `Vitamin B1, Vitamin B2, Vitamin B3, Vitamin B5, Vitamin B6, Vitamin B7, Vitamin B9, Vitamin B12`. Applies to every list of nutrients in this file and every list of nutrients agents emit (recipes-index columns, recipe-page bullets, `ingredients-info.md` cell-internal sort, threshold table, slug-mapping table, group READMEs).

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

## Nutrient lexicons

> **CANONICAL REFERENCE DATA — DO NOT MODIFY.** The four tables below (rows, columns, cell text, ordering) MUST NOT be changed by any agent, audit pass, formatting pass, or lexicon-conformance fix. Adding a row, renaming a row, or changing a cell requires explicit user approval. The same rule applies to the duplicated copy of each table inside `<group>/README.md` — this SKILL is the source; the README copy must remain byte-identical.

The four nutrient axes — macronutrients, minerals, vitamins, soft-essentials — are *ingredient-derived* facets. Each row of each table maps to a `<slug>.md` page under the corresponding directory; each recipe's `## Macronutrients` / `## Minerals` / `## Vitamins` / `## Soft Essentials` sections list the slugs derived from its ingredients via `## Ingredient → nutrient mapping` (next section).

**Uniform schema.** All four tables use the same four columns in the same order:

```markdown
| Category | Requirement | Function | Example Sources |
```

No table uses a different column name (`Top Sources`, `Best Bioavailable Sources`, `Why You Can't Skip It`, `Main Focus`, `Mineral`, `Type`, etc.). Empty cells are a single em-dash (`—`, U+2014). Rows are alphabetized within each table (see `### Alphabetical sort key`).

**The `Example Sources` column is examples only, NOT an exhaustive list.** This is repeated in the column-name itself (`Example Sources`, not `Top Sources` or `Best Sources`) so the framing survives at every glance. An ingredient not appearing in any cell may still be a meaningful source of the nutrient. Use the column as orientation; derive each ingredient's actual nutrient profile from established nutritional knowledge.

**The closed-lexicon rule.** The 27 row slugs (3 macronutrients + 7 minerals + 13 vitamins + 4 soft-essentials) are frozen at v1. New rows require explicit user approval, identical to the rule already in place for traits. Agents do not invent slugs; unmapped concepts are surfaced to the user.

**Slug derivation from the `Category` column.** Lowercase ASCII, kebab-case, accents stripped, parentheticals dropped. Specifically: `Complex Carbs` → `complex-carbs`, `Healthy Fats` → `healthy-fats`, `Omega-3 (EPA/DHA)` → `omega-3` (parenthetical dropped), `Vitamin A` → `vitamin-a`, `Vitamin B1` → `vitamin-b1`, `Vitamin B12` → `vitamin-b12`. The 27 slugs below are the only valid values; `b-complex` is **not** a valid slug (the source's lumped B-Complex row is split into seven individual B-vitamin rows).

### Macronutrients

| Category                                                 | Requirement                                                       | Function                                                | Example Sources                                                                  |
|----------------------------------------------------------|-------------------------------------------------------------------|---------------------------------------------------------|----------------------------------------------------------------------------------|
| [Complex Carbs](cooking/macronutrients/complex-carbs.md) | ~3–5 g/kg body weight per day; 45–65% of total daily calories     | Glucose for the brain, glycogen for muscles.            | Quinoa, oats, berries, legumes, sprouted grains.                                 |
| [Healthy Fats](cooking/macronutrients/healthy-fats.md)   | ~0.8–1.2 g/kg body weight per day; 20–35% of total daily calories | Hormone production, brain structure, vitamin absorption.| Extra virgin olive oil, walnuts (Omega-3), avocado, fatty fish.                  |
| [Protein](cooking/macronutrients/protein.md)             | 0.8–1.5 g/kg body weight per day; 10–35% of total daily calories  | Muscle repair, neurotransmitters, enzymes.              | Eggs (gold standard), fish, Greek yogurt, soy, lentils.                          |

### Minerals

| Category                                  | Requirement                       | Function                                            | Example Sources                                              |
|-------------------------------------------|-----------------------------------|-----------------------------------------------------|--------------------------------------------------------------|
| [Calcium](cooking/minerals/calcium.md)    | 1000 mg/day                       | Muscle contraction and bone integrity.              | Sardines (with bones), dairy, fortified milks, almonds.      |
| [Iodine](cooking/minerals/iodine.md)      | 150 µg/day                        | Crucial for thyroid function (metabolism).          | Seaweed (nori/kelp), iodized salt, white fish.               |
| [Iron](cooking/minerals/iron.md)          | 8 mg/day (M) / 18 mg/day (F)      | Prevents anemia; carries oxygen to cells.           | Clams, spinach (eat with Vitamin C), lentils, tofu.          |
| [Magnesium](cooking/minerals/magnesium.md)| 400 mg/day (M) / 310 mg/day (F)   | 300+ reactions (energy, sleep, DNA repair).         | Pumpkin seeds, dark chocolate (85%+), spinach.               |
| [Potassium](cooking/minerals/potassium.md)| 3400 mg/day (M) / 2600 mg/day (F) † | Regulates blood pressure and heartbeat.           | Bananas, potatoes (with skin), coconut water, beans.         |
| [Selenium](cooking/minerals/selenium.md)  | 55 µg/day                         | Antioxidant defense and thyroid health.             | Brazil nuts, eggs.                                           |
| [Zinc](cooking/minerals/zinc.md)          | 11 mg/day (M) / 8 mg/day (F)      | DNA synthesis and immune response.                  | Oysters, pumpkin seeds, chickpeas, cashews.                  |

### Vitamins

| Category                                    | Requirement                        | Function                                                                                       | Example Sources                                                                 |
|---------------------------------------------|------------------------------------|------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| [Vitamin A](cooking/vitamins/vitamin-a.md)  | 900 µg/day (M) / 700 µg/day (F)    | Fat-soluble. Eye health and skin integrity.                                                    | Egg yolks, dairy, carrots, sweet potatoes (as Beta-Carotene).                   |
| [Vitamin B1](cooking/vitamins/vitamin-b1.md)| 1.2 mg/day (M) / 1.1 mg/day (F)    | Water-soluble. Carbohydrate metabolism and nerve function. Also called thiamin.                | Trout, sunflower seeds, whole grains, legumes, fortified grains.                |
| [Vitamin B2](cooking/vitamins/vitamin-b2.md)| 1.3 mg/day (M) / 1.1 mg/day (F)    | Water-soluble. Energy metabolism and antioxidant function. Also called riboflavin.             | Dairy, eggs, salmon, almonds, leafy greens.                                     |
| [Vitamin B3](cooking/vitamins/vitamin-b3.md)| 16 mg/day (M) / 14 mg/day (F)      | Water-soluble. Energy metabolism and DNA repair. Also called niacin.                           | Tuna, salmon, sardines, peanuts, fortified grains.                              |
| [Vitamin B5](cooking/vitamins/vitamin-b5.md)| 5 mg/day †                         | Water-soluble. Coenzyme A synthesis and fatty acid metabolism. Also called pantothenic acid.   | Avocado, mushrooms, sunflower seeds, salmon, eggs.                              |
| [Vitamin B6](cooking/vitamins/vitamin-b6.md)| 1.3 mg/day                         | Water-soluble. Amino acid metabolism and neurotransmitter synthesis. Also called pyridoxine.   | Chickpeas, salmon, potatoes, bananas, tuna.                                     |
| [Vitamin B7](cooking/vitamins/vitamin-b7.md)| 30 µg/day †                        | Water-soluble. Fatty acid synthesis and glucose metabolism. Also called biotin.                | Egg yolks, salmon, almonds, sweet potatoes, sunflower seeds.                    |
| [Vitamin B9](cooking/vitamins/vitamin-b9.md)| 400 µg/day                         | Water-soluble. DNA/RNA synthesis and cell division (critical in pregnancy). Also called folate.| Leafy greens, lentils, asparagus, beans, fortified grains.                      |
| [Vitamin B12](cooking/vitamins/vitamin-b12.md)| 2.4 µg/day                       | Water-soluble. Nervous system and DNA. Crucial for vegans to supplement.                       | Clams, sardines, eggs, dairy, fortified cereals, nutritional yeast.             |
| [Vitamin C](cooking/vitamins/vitamin-c.md)  | 90 mg/day (M) / 75 mg/day (F)      | Water-soluble. Collagen and immune function.                                                   | Bell peppers (higher than oranges), kiwi, citrus.                               |
| [Vitamin D](cooking/vitamins/vitamin-d.md)  | 600 IU/day (15 µg/day)             | Fat-soluble. Immune system and bone health.                                                    | Fatty fish (salmon, mackerel), egg yolks, fortified milk, UV-exposed mushrooms. |
| [Vitamin E](cooking/vitamins/vitamin-e.md)  | 15 mg/day                          | Fat-soluble. Protecting cells from oxidative stress.                                           | Sunflower seeds, almonds, wheat germ oil.                                       |
| [Vitamin K](cooking/vitamins/vitamin-k.md)  | 120 µg/day (M) / 90 µg/day (F) †   | Fat-soluble. Blood clotting and bone mineralization.                                           | Kale, spinach, fermented foods (K2).                                            |

### Soft Essentials

| Category                                                      | Requirement                    | Function                                            | Example Sources                                              |
|---------------------------------------------------------------|--------------------------------|-----------------------------------------------------|--------------------------------------------------------------|
| [Dietary Fiber](cooking/soft-essentials/dietary-fiber.md)     | 25 g/day (F) / 38 g/day (M)    | Gut motility, feeding good bacteria.                | Chia seeds, beans, raspberries, broccoli.                    |
| [Omega-3 (EPA/DHA)](cooking/soft-essentials/omega-3.md)       | 250–500 mg/day                 | Reducing systemic inflammation.                     | Wild salmon, sardines, mackerel, anchovies, oysters.         |
| [Phytochemicals](cooking/soft-essentials/phytochemicals.md)   | Diverse intake daily           | Anti-aging and disease prevention.                  | "Eat the rainbow": purple cabbage, blueberries, turmeric.    |
| [Probiotics](cooking/soft-essentials/probiotics.md)           | Periodic intake (daily/weekly) | Maintaining a healthy "army" of gut bacteria.       | Kimchi, kefir, sauerkraut, miso.                             |

### Requirement-source note

> **All Requirement values are daily intake targets** (the amount expected to be consumed across a 24-hour day, summed across all meals and snacks combined). Values shown are for adults 19–50, single value where male/female intake is the same. `(M)` and `(F)` distinguish the two when they differ. `†` marks an Adequate Intake (AI) rather than a Recommended Dietary Allowance (RDA) — used by the NIH Office of Dietary Supplements when evidence is insufficient to set a true RDA. Macronutrient `g/kg body weight per day` values scale with body weight (e.g., 0.8 g/kg/day protein for a 70 kg adult ≈ 56 g/day total); the `% of total daily calories` ranges are AMDRs from the U.S. Dietary Reference Intakes. Sources: NIH ODS Fact Sheets ([ods.od.nih.gov/factsheets](https://ods.od.nih.gov/factsheets/list-all/)) for RDAs/AIs; U.S. DRIs for macronutrient AMDRs.
>
> **Recipe-page totals are NOT daily intakes.** A recipe-page bullet shows the total contained in the entire dish as written (the yield in the metadata blockquote). To compare against a daily Requirement value, the reader divides by servings (or multiplies by how much they eat) and compares with their own day's total. The SKILL does NOT do this comparison automatically.

### Edible-only rule for `Example Sources`

Cells contain edible foods only — no supplements (D3 capsules, B12 pills), no non-foods (sunlight). **Reason:** the tables map to recipes; supplements / sunlight don't appear in any recipe ingredient list and would create dead leads in `ingredients-info.md`.

Examples are restricted to **vegetarian + fish/shellfish** sources. "Vegetarian" is broad: plants, grains, legumes, nuts, seeds, fungi, eggs, dairy, honey. Fish and shellfish (clams, oysters, mussels) are allowed. **The only exclusion is land-animal flesh** — no beef, pork, lamb, chicken, turkey, liver, or other meat / poultry / organ meats. When a row's most concentrated source is land meat (e.g., liver for retinol, beef for B12), substitute the next-best vegetarian or pescatarian source (egg yolks, dairy, fatty fish, sardines).

## Ingredient → nutrient mapping

Recipe nutrient sections are *derived*, not hand-picked. The single authoritative lookup is `docs/cooking/ingredients-info.md`. This section defines its schema and the protocol agents follow when writing or auditing a recipe's nutrient sections.

### Threshold model

Two thresholds, used at two distinct stages. The full per-nutrient values live in `### Canonical units and inclusion thresholds per nutrient`; the model below states the rules.

- **Inclusion threshold (per-100g)** gates `ingredients-info.md` cells. Roughly 1% of the adult RDA / AI per 100g; set to **recipe drop threshold ÷ 5**. **Do NOT preemptively apply the recipe drop threshold here** — at the ingredient level we do not know how much of the ingredient any recipe will use, and a small per-100g content can still produce a meaningful per-recipe sum at high ingredient quantities.
- **Recipe drop threshold (per-recipe sum)** gates recipe-page bullets and recipes-index table cells. The single arbiter of "is this enough to render": **no separate "rounds to 0" rule and no separate macro/fiber floor test** (macros and fiber recipe drop thresholds are simply `1g`, applied via the same threshold check as every other quantitative slug). Threshold drop runs BEFORE rounding.
- **HARD CLIFF**: when an audit recomputes a recipe's sums, the recipe drop threshold wins over the ±20% / ±1-step tolerance — see `### 5.13`.
- **Qualitative entries** (`Phytochemicals`, `Probiotics`): no unit, no amount, no quantitative threshold, no ` — <amount>` suffix on bullets. Presence-based: listed in an `ingredients-info.md` cell whenever the ingredient is a recognized source; listed on a recipe whenever ≥1 ingredient lists them. **State once here; every other site references this rule.**

**Reason for two tiers (one sentence).** A low per-100g content can still produce a meaningful per-recipe sum at high ingredient quantities (e.g., apple Vitamin C at 4.6mg/100g, recipe drop threshold 5mg — pre-filtering at the ingredient level would lose Vitamin C from a 1kg apple-pie filling, whose per-recipe sum is ~46mg).

### Canonical units and inclusion thresholds per nutrient

Each of the 25 quantitative v1 nutrient slugs has exactly one canonical unit AND two thresholds — one for ingredient-cell inclusion (looser) and one for recipe-page rendering (stricter). The unit is fixed: every `ingredients-info.md` cell for that nutrient MUST use this unit, and every recipe-page bullet for that nutrient MUST display the summed total in this unit. **Reason:** mixing units within a nutrient corrupts summation — e.g., `Vitamin A (470µg/100g)` + `Vitamin A (0.5mg/100g)` summed as `470 + 0.5 = 470.5` is wrong (the correct sum is `970µg`).

For the two-stage threshold rule itself, see `### Threshold model` above.

| Slug | Display name | Canonical unit | Inclusion threshold (per 100g) | Recipe drop threshold (per recipe) | Notes |
|---|---|---|---|---|---|
| `complex-carbs` | `Complex Carbs` | `g` | `0.2g` | `1g` | Macros — always `g`. |
| `healthy-fats` | `Healthy Fats` | `g` | `0.2g` | `1g` | Always `g`. **Strict policy: only UNSATURATED fats count** (lexicon Example Sources are extra-virgin olive oil, walnuts, avocado, fatty fish — all unsaturated). Saturated fats — coconut oil / coconut milk / coconut cream / palm oil / butter / lard / dairy fat / deep-frying fat / hydrogenated shortening — do NOT contribute to `Healthy Fats`. Saturated fat is not tracked anywhere in v1. |
| `protein` | `Protein` | `g` | `0.2g` | `1g` | Macros — always `g`. |
| `calcium` | `Calcium` | `mg` | `10mg` | `50mg` | |
| `iodine` | `Iodine` | `µg` | `2µg` | `10µg` | |
| `iron` | `Iron` | `mg` | `0.1mg` | `0.5mg` | |
| `magnesium` | `Magnesium` | `mg` | `4mg` | `20mg` | |
| `potassium` | `Potassium` | `mg` | `30mg` | `150mg` | |
| `selenium` | `Selenium` | `µg` | `1µg` | `5µg` | |
| `zinc` | `Zinc` | `mg` | `0.1mg` | `0.5mg` | |
| `vitamin-a` | `Vitamin A` | `µg` | `10µg` | `50µg` | RAE; not IU. |
| `vitamin-b1` | `Vitamin B1` | `mg` | `0.02mg` | `0.1mg` | Thiamin. |
| `vitamin-b2` | `Vitamin B2` | `mg` | `0.02mg` | `0.1mg` | Riboflavin. |
| `vitamin-b3` | `Vitamin B3` | `mg` | `0.2mg` | `1mg` | Niacin. |
| `vitamin-b5` | `Vitamin B5` | `mg` | `0.1mg` | `0.5mg` | Pantothenic acid. |
| `vitamin-b6` | `Vitamin B6` | `mg` | `0.02mg` | `0.1mg` | Pyridoxine. |
| `vitamin-b7` | `Vitamin B7` | `µg` | `0.4µg` | `2µg` | Biotin. |
| `vitamin-b9` | `Vitamin B9` | `µg` | `4µg` | `20µg` | Folate. |
| `vitamin-b12` | `Vitamin B12` | `µg` | `0.05µg` | `0.1µg` | Inclusion threshold floored at `0.05µg` to filter true-trace soil-microbe levels in plant foods. |
| `vitamin-c` | `Vitamin C` | `mg` | `1mg` | `5mg` | |
| `vitamin-d` | `Vitamin D` | `µg` | `0.2µg` | `1µg` | Not IU — IU appears only in the lexicon's Requirement column for reference. |
| `vitamin-e` | `Vitamin E` | `mg` | `0.2mg` | `1mg` | |
| `vitamin-k` | `Vitamin K` | `µg` | `1µg` | `5µg` | |
| `dietary-fiber` | `Dietary Fiber` | `g` | `0.2g` | `1g` | |
| `omega-3` | `Omega-3 (EPA/DHA)` | `mg` | `10mg` | `50mg` | Marine EPA/DHA only — plant ALA (chia, flax, walnuts) is NOT EPA/DHA and does not count for v1. |
| `phytochemicals` | `Phytochemicals` | — | presence | presence | Qualitative — no unit, no amount, no quantitative threshold. Listed in an ingredient cell whenever the ingredient is a recognized source; listed on a recipe whenever ≥1 ingredient lists it. |
| `probiotics` | `Probiotics` | — | presence | presence | Qualitative — no unit, no amount, no quantitative threshold. Listed in an ingredient cell only for live-culture fermented foods; listed on a recipe whenever ≥1 ingredient lists it. |

Summation: `contribution = X × mass_g / 100` per ingredient, summed per nutrient. Single-unit-per-nutrient means the sum is a straight numeric add — no conversion step. A non-canonical-unit cell (e.g., `Vitamin A (0.47mg/100g)` instead of `Vitamin A (470µg/100g)`) is a defect: fix by re-expressing the cell in the canonical unit before any summation runs (see `### 5.14`).

When step 4 of the lookup-extend protocol adds a new row, fill each nutrient cell whenever per-100g content is at or above the **inclusion threshold** above (the looser threshold). **Do NOT preemptively apply the recipe drop threshold here** — see `### Threshold model`.

### `ingredients-info.md` schema

The file shape:

- One H1: `# Ingredients Info`.
- One back-link line: `Back to [Cooking](cooking/README.md)`.
- One short paragraph reminding agents that the table is alphabetical and the cells contain *display names from the `Category` column of `## Nutrient lexicons`* with a per-100g amount estimate appended in parentheses.
- A single five-column table:

  ```
  | Ingredient | Macronutrients | Minerals | Vitamins | Soft Essentials |
  |---|---|---|---|---|
  ```

**Ingredient column rules** (canonical name normalization):

- Lowercase. Canonical generic name (e.g., `olive oil`, not `extra virgin olive oil`; `yogurt` covers brand/style variants unless nutrition meaningfully differs — `greek yogurt` is a distinct row because protein density differs materially).
- Strip preparation modifiers (`chopped`, `diced`, `sliced`, `minced`, `grated`, `crushed`, `ground`, `melted`, `softened`, etc.).
- Strip size modifiers (`small`, `medium`, `large`, `extra-large`, `jumbo`, `baby`, `mini`, `giant`, and similar) for the canonical lookup name — list non-exhaustive; if a modifier is clearly a size, strip it. The size IS retained for the mass calculation via the whole-item table — e.g., a recipe row `| 3 | large eggs |` looks up canonical `egg` in `ingredients-info.md` AND uses `1 large egg = 50g` from the whole-item table to compute mass = 150g.
- **Cultivar / variety carve-out (NOT stripped).** A modifier is a *cultivar* (kept as part of the canonical name, distinct row in `ingredients-info.md`) when it designates a different plant variety with materially different nutrition density or culinary use. A modifier is a *size* (stripped) when it just means "a smaller/larger specimen of the same plant".
  - **Cultivars (KEEP):** `cherry tomato`, `grape tomato`, `roma tomato`, `pearl onion`, `baby corn`, `baby bok choy`, `baby kale`, `kabocha squash`, `delicata squash`, `cremini mushroom`, `shiitake mushroom`, `portobello mushroom`. These get their own canonical row.
  - **Sizes (STRIP):** `large onion`, `medium tomato`, `small potato`, `baby carrot` (just a peeled small carrot — same density), `baby spinach` (young leaves of regular spinach — same density), `mini bell pepper` (smaller specimen), `large egg` (size only), `white mushroom` / `button mushroom` (the default `mushroom` referent — these strip to canonical `mushroom`, NOT a separate cultivar).
  - When in doubt: if a USDA / standard nutrition-database row exists separately for the modified form (e.g., "tomato, cherry, raw" is its own row), treat it as a cultivar. Otherwise it's a size.
- Strip quantity, parentheticals, and packaging notes.
- Use the singular form unless the ingredient is naturally plural (`oats`, `lentils`, `chickpeas`).
- **Sub-recipe ingredients** (a recipe used as an ingredient by another recipe — e.g., `[Maple Dijon Dressing](cooking/recipes/maple-dijon-dressing.md)` used inside `apple-chickpea-salad`) use a Markdown link as the canonical name: `[<Title>](cooking/recipes/<slug>.md)`. The visible link text is the recipe's H1 (Title Case). The alphabetical sort key is the link text in lowercase, ignoring `[...](...)` syntax. Lookup matches the link text, not the URL. See `### Sub-recipe ingredients` below for how their cells are computed.
- Sort the table by the canonical ingredient name, case-insensitive, with the same alphabetical sort key used elsewhere in this skill (strip leading articles `the`/`a`/`an`; numeric tokens by value; for sub-recipe rows, use the link text only).

**Cell content rules:**

- Comma-separated entries from the relevant group's lexicon. Each entry uses the EXACT `Category` column display name from `## Nutrient lexicons` (e.g., `Complex Carbs`, `Vitamin B12`, `Omega-3 (EPA/DHA)`) — never the slug, never a plural, never a free-text variant.
- Format: `<Display Name> (<value><unit>/100g)`. Unit is the canonical unit (see `### Canonical units and inclusion thresholds per nutrient`); do NOT pick the unit row-by-row. **Do NOT** prefix the amount with `~` — **Reason:** marked@1.x renders `~text~` as strikethrough, so `(~50g/100g), Protein (~21g/100g)` would render struck-through across `50g/100g), Protein (`.
- Examples: `Healthy Fats (50g/100g)`, `Vitamin B12 (0.9µg/100g)`, `Vitamin A (470µg/100g)` (never `Vitamin A (0.47mg/100g)` — wrong unit), `Omega-3 (EPA/DHA) (2400mg/100g)`. `Phytochemicals` and `Probiotics` are qualitative — bare display name, no amount.
- Within-cell sort: alphabetical by display name, B-vitamins by numeric value (see `### Formatting conventions`).
- Empty cells: single em-dash (`—`).
- **Inclusion criterion**: per-100g `inclusion threshold` (looser column), NOT the recipe drop threshold. See `### Threshold model`.
- **Qualitative entries** (`Phytochemicals`, `Probiotics`): include whenever the ingredient is a recognized source (lycopene, capsaicin, anthocyanins, sulforaphane for Phytochemicals; live-culture fermented items for Probiotics). See `### Threshold model`.

**Display name → slug mapping** (used when deriving recipe page bullet links from cell content). The 27 v1 entries map cleanly via the standard slug-derivation rule (lowercase, kebab-case, parentheticals dropped):

| Display name | Slug |
|---|---|
| `Complex Carbs` | `complex-carbs` |
| `Healthy Fats` | `healthy-fats` |
| `Protein` | `protein` |
| `Calcium` | `calcium` |
| `Iodine` | `iodine` |
| `Iron` | `iron` |
| `Magnesium` | `magnesium` |
| `Potassium` | `potassium` |
| `Selenium` | `selenium` |
| `Zinc` | `zinc` |
| `Vitamin A` | `vitamin-a` |
| `Vitamin B1` | `vitamin-b1` |
| `Vitamin B2` | `vitamin-b2` |
| `Vitamin B3` | `vitamin-b3` |
| `Vitamin B5` | `vitamin-b5` |
| `Vitamin B6` | `vitamin-b6` |
| `Vitamin B7` | `vitamin-b7` |
| `Vitamin B9` | `vitamin-b9` |
| `Vitamin B12` | `vitamin-b12` |
| `Vitamin C` | `vitamin-c` |
| `Vitamin D` | `vitamin-d` |
| `Vitamin E` | `vitamin-e` |
| `Vitamin K` | `vitamin-k` |
| `Dietary Fiber` | `dietary-fiber` |
| `Omega-3 (EPA/DHA)` | `omega-3` |
| `Phytochemicals` | `phytochemicals` |
| `Probiotics` | `probiotics` |

### Quantity → grams conversion

To compute per-recipe nutrient totals, each `## Ingredients` row's quantity must be expressed in grams. Apply these canonical conversions; for items not covered, estimate from established culinary knowledge.

**Volume → weight (most common ingredient families):**

| Family | 1 cup | 1 tbsp | 1 tsp |
|---|---|---|---|
| Water-like liquid (water, broth, milk, plant milk, juice, vinegar, soy sauce) | 240g | 15g | 5g |
| Oils (olive, vegetable, avocado, coconut melted) | 215g | 13g | 4g |
| Honey, maple syrup, molasses, agave | 340g | 21g | 7g |
| Yogurt, sour cream, kefir, applesauce | 240g | 15g | 5g |
| Butter, ghee | 227g | 14g | 5g |
| Nut butter (peanut, almond, tahini) | 250g | 16g | 5g |
| All-purpose flour | 120g | 8g | — |
| Whole-wheat / rye / oat flour | 130g | 8g | — |
| Cornstarch, arrowroot, tapioca starch | 120g | 8g | — |
| Granulated sugar | 200g | 12g | 4g |
| Brown sugar (packed) | 220g | 14g | 4.5g |
| Powdered / icing sugar | 120g | 8g | 2.5g |
| Cocoa powder | 100g | 6g | 2g |
| Rolled oats | 90g | 6g | — |
| Cooked rice / quinoa / pasta | 180g | — | — |
| Dry rice / quinoa | 190g | — | — |
| Dry pasta | 90g | — | — |
| Dry lentils / beans / chickpeas | 200g | — | — |
| Cooked / canned beans (drained) | 175g | — | — |
| Whole nuts (almonds, cashews, walnuts, peanuts) | 140g | — | — |
| Pumpkin / sunflower / sesame seeds | 130g | — | — |
| Chia / flax seeds | 170g | 10g | 3g |
| Shredded / crumbled cheese | 100g | — | — |
| Grated hard cheese (parmesan, pecorino) | 90g | 5g | — |
| Berries / diced fruit | 150g | — | — |
| Diced vegetables (onion, pepper, tomato, etc.) | 150g | — | — |
| Mushrooms (sliced / chopped, raw) | 70g | — | — |
| Leafy greens (chopped, packed) | 30g (spinach), 60g (kale, chard, collard) | — | — |
| Salt | — | 18g | 6g |
| Baking powder, baking soda, yeast | — | 12g | 4g |
| Dried herbs / spices (ground) | — | 6g | 2g |
| Fresh herbs (chopped, loose-packed) | 25g | 2g | — |
| Coconut (shredded, unsweetened) | 80g | 5g | — |
| Raisins / dried cranberries / chopped dates | 150g | 10g | — |

**Whole-item weights (most common):**

| Item | g |
|---|---|
| 1 large egg | 50 (white 30, yolk 20) |
| 1 medium egg | 44 |
| 1 small egg | 38 |
| 1 extra-large egg | 56 |
| 1 jumbo egg | 63 |
| 1 medium onion | 150 |
| 1 clove garlic | 3 |
| 1 medium tomato | 120 |
| 1 cherry tomato | 15 |
| 1 medium carrot | 60 |
| 1 stalk celery | 40 |
| 1 medium bell pepper | 150 |
| 1 jalapeño | 14 |
| 1 medium cucumber | 200 |
| 1 medium potato | 200 |
| 1 medium sweet potato | 150 |
| 1 medium banana | 120 |
| 1 medium apple | 180 |
| 1 medium pear | 180 |
| 1 medium avocado | 200 (flesh ~150) |
| 1 medium lemon | 60 (juice ~45) |
| 1 medium lime | 50 (juice ~30) |
| 1 medium orange | 130 |
| 1 medium peach | 150 |
| 1 medium zucchini | 200 |
| 1 mushroom (default — white / button, any size unstated) | 18 |
| 1 cremini mushroom | 18 |
| 1 shiitake mushroom (fresh, cap) | 18 |
| 1 portobello mushroom (whole, cap + stem) | 120 |
| 1 portobello mushroom cap (stem removed) | 85 |
| 1 slice bread | 30 |
| 1 medium tortilla | 50 |
| 1 inch piece ginger | 7 |

**Mass / volume conversions (when the source already gives a precise weight or volume):**

- `1 oz` = 28g; `1 lb` = 454g.
- `1 mL` water-like liquid = 1g; oil = 0.92g; honey/syrup = 1.4g.
- Fluid `1 fl oz` = 30 mL.
- A quantity already in grams (`200 g flour`) is used directly — no conversion.

**Special quantities (treat as 0g contribution):**

- `to taste`, `for taste`, `to season`
- `for serving`, `for garnish`, `for topping`, `to serve`, `to drizzle`, `drizzle of`
- `as needed`
- `optional` when no explicit amount is given (if an amount IS given, use it)
- `pinch`, `dash`, `splash`, `splash of`, `squeeze of`, `few drops`

**Whole-item vs volume precedence.** When the source quantity uses an item count (`1 apple`, `2 medium onions`, `3 large eggs`), use the whole-item table. When the source uses a volume (`1 cup diced apple`, `½ cup chopped onion`), use the volume table. When the source gives a weight directly (`200g flour`, `1 lb chicken`), use that weight as-is. If the source mixes both ("1 large apple, diced (1 cup)"), use the whole-item count.

**Unspecified-size fallback.** When the source omits a size qualifier (`1 onion`, `1 tomato`, `2 eggs`):

- **Eggs default to large = 50g.** This matches North American recipe convention (USDA "large" is the standard cookbook default). So `2 eggs` → 100g, even though the table also lists smaller variants.
- **Mushrooms (whole-item count, cultivar omitted) default to white/button = 18g** — e.g., `1 mushroom`, `2 mushrooms`. When the source names a cultivar (`1 cremini`, `1 portobello cap`, `2 shiitake`), use the cultivar's row. **Volume measurements** (`½ cup chopped mushrooms`, `1 cup sliced mushrooms`) follow the **whole-item-vs-volume precedence** rule and go to the volume table above — specifically the row labeled `Mushrooms (sliced / chopped, raw)` (70g per cup) — NOT to this whole-item fallback.
- **All other current items** (every entry besides eggs and mushrooms — `1 medium onion`, `1 medium carrot`, `1 stalk celery`, `1 clove garlic`, `1 slice bread`, `1 cherry tomato`, etc.) have only one row in the table and therefore fall through to the **Single-variant items** rule below. There is no choice to make.
- **Forward-compatibility:** if a future revision adds multiple non-egg, non-mushroom size rows for some item, those default to the `medium` entry. (No such item exists in the current table.)

**Single-variant items.** When the table lists only one row for an item (whether tagged `medium` or untagged — e.g., `1 medium onion`, `1 stalk celery`, `1 clove garlic`, `1 slice bread`), the single listed weight applies **regardless of any size qualifier in the source**. The skill deliberately avoids size-scaling for single-row items because it would require per-ingredient density judgments that drift across runs. If a recipe truly hinges on a non-default size (`1 large butternut squash` ≈ 1500g vs. medium ≈ 1000g), the agent estimates from established culinary knowledge (see the fallback rule for ingredients/forms not in either table, below) — but this is the exception, not the default behavior.

For ingredients/forms not in either table (`1 medium butternut squash` ≈ 1000g, `1 small head of broccoli` ≈ 400g, `1 head of garlic` ≈ 50g), estimate from established culinary knowledge. For canned/jarred items: prefer the drained weight when "drained" is mentioned (typically ~60% of the can's gross weight); otherwise use the source's stated total weight.

### Lookup-extend protocol

Writing the four nutrient sections of any recipe page:

1. For each `## Ingredients` row, compute canonical name + mass in grams (see `### Quantity → grams conversion`). Skip 0g entries.
2. Look up the canonical name in `ingredients-info.md`. **Exact canonical match only — do not invent or fuzzy-match.** Sub-recipe rows match against the link text only, ignoring `[...](...)` syntax.
3. **If found:** for each cell entry `<Display Name> (<X><unit>/100g)`, compute `contribution = X × mass_g / 100` and add to the recipe-level running total. Qualitative entries record presence only.
4. **If not found:** determine the per-100g profile from established nutritional knowledge, append a new alphabetical row with the four cells filled (see the cell content rules above), then apply step 3.
5. After all ingredients: apply the recipe drop threshold to each quantitative sum and presence to qualitative entries (see `### Threshold model`). Convert surviving display names to slugs via the **Display name → slug mapping**. Write per `### Recipe-page rendering`; omit empty sections (see `### Section-omission rule`).

**Dedup + sort:** within each section, each slug appears at most once; sort as in `### Recipe-page rendering`. Bullets link to the slug's canonical row file (e.g., `cooking/minerals/iron.md`).

**Critical guard:** the agent **MUST NOT** invent slugs outside the v1 lexicons. Surface unmapped concepts to the user — do not silently add rows (see `### Lexicon-first rule`).

### Sub-recipe ingredients

Some recipes use other recipes as ingredients (e.g., `apple-chickpea-salad` uses "1 batch Maple Dijon Dressing"). Sub-recipes need a row in `ingredients-info.md` so their nutrients propagate to the parent.

**Row convention.** Two differences from a raw-ingredient row:

1. **Ingredient column is a Markdown link** to the recipe page (signals "this row is a sub-recipe"):

   ```markdown
   | [Maple Dijon Dressing](cooking/recipes/maple-dijon-dressing.md) | Healthy Fats (60g/100g) | Calcium (40mg/100g), Potassium (110mg/100g) | Vitamin C (8mg/100g), Vitamin E (2.4mg/100g), Vitamin K (11µg/100g) | — |
   ```

2. **Nutrient cells contain a per-100g profile** aggregated from the sub-recipe's own `## Ingredients` table:
   a. For each ingredient row, compute canonical name → grams (see `### Quantity → grams conversion`).
   b. Sum masses → **batch mass** (for sauces / seasonings / dressings / dips / assemblies this equals the raw-ingredient sum; for mass-loss recipes see below).
   c. For each nutrient slug, sum `(per_100g_value × ingredient_grams / 100)` = total in one batch.
   d. Per-100g of the sub-recipe = `(total_in_batch × 100) / batch_mass`.
   e. Apply per-100g **inclusion thresholds** as for any ingredient cell (see `### Threshold model`); round per cell content rules.

**Sort key and lookup matching.** Row sorts by the link text in lowercase, ignoring `[...](...)` syntax: `[Maple Dijon Dressing](...)` sorts at `maple dijon dressing`. A parent-recipe agent computes the canonical name (e.g., `maple dijon dressing`) and matches against the link text in `ingredients-info.md`'s Ingredient column (case-insensitive, ignoring Markdown link syntax). Once matched, the four cells provide the per-100g profile; the standard `(value × grams / 100)` math propagates nutrients to the parent. No special-casing beyond the link-text match.

**Mass conversion when a parent uses a sub-recipe:**

- "1 batch &lt;Title&gt;" → batch mass (step b above; consult the sub-recipe page's `Yield:` if it states a finished mass).
- "1 tbsp / 1 tsp / 1 cup &lt;Title&gt;" → standard `### Quantity → grams conversion` using the sub-recipe's bulk-density family (dressings/sauces ~15g/tbsp · 240g/cup; dry seasoning blends ~6g/tbsp · 80g/cup; dips/spreads ~15g/tbsp · 240g/cup; granola ~30g per ¼ cup; ice cream ~130g/cup). When ambiguous, note the assumption in the sub-recipe's `## Notes`.
- "to taste" or "—" → 0g contribution.

**Recursion.** Process leaf sub-recipes first so inner rows are populated before outer ones. **Two-level recursion is the practical limit in v1**; deeper chains require explicit user surfacing.

**Mass-loss sub-recipes.** Where the produced batch mass differs materially from the raw-ingredient sum (typically baked goods losing 15–25% to evaporation, or reductions/concentrates), use the **finished batch mass** in step (b), not the raw sum. State the assumed finished mass in the sub-recipe's own `## Notes`.

**Updating.** When a sub-recipe's `## Ingredients` table changes, recompute its row in `ingredients-info.md` and re-derive every parent recipe that uses it. `### 5.15` catches drift.

### Recipe-page rendering

A recipe page's nutrient sections list each derived nutrient as a bullet with its rounded recipe-level total amount. The total reflects the **entire dish as written** (the yield stated in the metadata blockquote) — it is NOT divided by yield to give per-serving amounts.

Bullet format:

```markdown
## Vitamins

- [Vitamin A](cooking/vitamins/vitamin-a.md) — 470µg
- [Vitamin B12](cooking/vitamins/vitamin-b12.md) — 1.2µg
- [Vitamin D](cooking/vitamins/vitamin-d.md) — 6µg
```

Format rules:

- Bullet shape: `- [<Bullet Link Text>](cooking/<group>/<slug>.md) — <amount><unit>`. Separator ` — `, no space between number and unit (see `### Formatting conventions`).
- **Bullet link text is the humanized slug** (Title Case, hyphens → spaces, B-vitamins keep their digit; `omega-3` carve-out — `Omega-3`, hyphen-digit retained — see `### Formatting conventions`). For 26 of 27 v1 entries this equals the lexicon `Category` display name. The one exception is `Omega-3`: lexicon Category `Omega-3 (EPA/DHA)` and `ingredients-info.md` cells use the full form (`Omega-3 (EPA/DHA) (200mg/100g)`), but the recipe-page bullet drops the parenthetical so the link text matches the slug's H1: `- [Omega-3](cooking/soft-essentials/omega-3.md) — 200mg`.
- Amount unit is the canonical unit (see `### Canonical units and inclusion thresholds per nutrient`; same as `ingredients-info.md`). Quick reference: `g` for macros and Dietary Fiber; `mg` or `µg` as that table assigns; `mg` for Omega-3.
- **Vitamin D is always reported in `µg`, never IU.** The IU form in the lexicon's Requirement column is informational only; recipe-page bullets AND `ingredients-info.md` cells use `µg`.
- **Threshold drop FIRST, then rounding.** Drop any quantitative bullet whose **unrounded** recipe-level sum is below the per-nutrient **recipe drop threshold** (see `### Threshold model`). Apply rounding only to values that passed.
- **Rounding** (apply by magnitude band of the *value*, regardless of unit; bands are half-open at the upper end so a value of exactly 10 falls into `[10, 100)`, not `[1, 10)`):
  - `[0, 1)` (e.g., `0.7µg`): one decimal place.
  - `[1, 10)` (e.g., `1.8mg`, `1.4µg`, `3µg`): one decimal place; drop a trailing `.0` (so `3.0µg` → `3µg`, `1.4µg` stays).
  - `[10, 100)` (e.g., `45µg`, `28mg`): integer.
  - `[100, 1000)` (e.g., `270mg`, `370µg`): nearest 10.
  - `[1000, 5000)` (e.g., `2400mg`): nearest 50.
  - `[5000, ∞)`: nearest 100.
  - **Macros and Dietary Fiber override:** always `g`, always integer (round half-up; no band rounding). `1.4g` → `1g`, `19.6g` → `20g`, `28.3g` → `28g`, `245.4g` → `245g`. (Sums `< 1g` are dropped at the threshold step before rounding runs.)
- **Qualitative entries** (`Phytochemicals`, `Probiotics`): no amount, no ` — ` separator. See `### Threshold model`.
- **Within-section sort:** alphabetical by display name, case-insensitive, B-vitamins by numeric value.
- If no bullets remain in a group after the threshold check, omit the section (see `### Section-omission rule`).

## Page templates

Every page kind under `docs/cooking/` has a fixed shape. Agents emit these verbatim.

### `docs/cooking/README.md`

```markdown
# Cooking

- [Recipes](cooking/recipes/README.md)
- [Categories](cooking/categories/README.md)
- [Traits](cooking/traits/README.md)
- [Books](cooking/books/README.md)
- [Macronutrients](cooking/macronutrients/README.md)
- [Minerals](cooking/minerals/README.md)
- [Vitamins](cooking/vitamins/README.md)
- [Soft Essentials](cooking/soft-essentials/README.md)
- [Ingredients Info](cooking/ingredients-info.md)
```

### `docs/cooking/recipes/README.md`

```markdown
# Recipes

Back to [Cooking](cooking/README.md)

| Recipe | Categories | Traits | Complex Carbs | Healthy Fats | Protein | Calcium | Iodine | Iron | Magnesium | Potassium | Selenium | Zinc | Vitamin A | Vitamin B1 | Vitamin B2 | Vitamin B3 | Vitamin B5 | Vitamin B6 | Vitamin B7 | Vitamin B9 | Vitamin B12 | Vitamin C | Vitamin D | Vitamin E | Vitamin K | Dietary Fiber | Omega-3 | Phytochemicals | Probiotics |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Banana Bread](cooking/recipes/banana-bread.md) | dessert | easy | 245g | 22g | 16g | 120mg | — | 4mg | 60mg | 580mg | — | 1.2mg | 90µg | 0.2mg | 0.3mg | 4mg | 1mg | 0.4mg | — | 90µg | — | 8mg | — | 3.5mg | 7µg | 7g | — | yes | — |
| [Classic French Omelette](cooking/recipes/classic-french-omelette.md) | breakfast, main | easy, fast | — | 28g | 19g | — | — | 1.8mg | — | — | 45µg | — | 370µg | — | — | — | — | — | — | — | 1.4µg | — | 3µg | — | — | — | — | — | — |
...
```

**Schema (the contract for every row).** The script `scripts/build_recipes_table.py` (next to this SKILL) regenerates this file in one pass from the current `docs/cooking/recipes/*.md` set. Maintenance runs MUST regenerate it from the script rather than hand-editing rows, so the rules below stay enforced by construction:

- **30 columns, fixed order**: `Recipe | Categories | Traits | <macronutrients> | <minerals> | <vitamins> | <soft-essentials>`. Within each nutrient group the columns are alphabetical (B-vitamins by numeric value: `B1 … B12`). The 27 nutrient columns are the 27 v1 slugs from `## Nutrient lexicons`. The header label is the canonical lexicon display name **except** `Omega-3` (parenthetical dropped — matches the recipe-page bullet link text rule).
- **Rows sorted alphabetically by recipe display name** using the standard sort key (case-insensitive, strip leading `the`/`a`/`an`, numeric tokens by value).
- **`Recipe` cell**: `[<H1 title>](cooking/recipes/<slug>.md)` — absolute path (see `### Link path convention`).
- **`Categories` cell**: comma-separated category **slugs** (not display names), alphabetical, e.g. `breakfast, main`. `—` when empty (won't happen in practice — every recipe has ≥1 category, but the empty form is defined for completeness).
- **`Traits` cell**: comma-separated trait **slugs**, alphabetical, e.g. `easy, fast, vegan`. `—` when the recipe has zero traits.
- **Quantitative nutrient cells**: the **exact `<amount><unit>` printed in the recipe page bullet** (e.g. `158g`, `1.4µg`, `370µg`). No space between number and unit. No rounding here — the recipe page is the source of truth and this cell mirrors it byte-for-byte. `—` when the bullet is absent from that recipe (i.e. the nutrient was below its recipe drop threshold or the section was omitted).
- **Qualitative nutrient cells** (`Phytochemicals`, `Probiotics`): `yes` when the recipe page lists the bullet, `—` when it does not. No amount.

The slug-form encoding for `Categories` / `Traits` is deliberate: it gives a parser a single canonical key per cell entry, mapping directly to `cooking/categories/<slug>.md` / `cooking/traits/<slug>.md` and to the corresponding lexicon entry. Display-name encoding would require a slugify step before any lookup.

### `docs/cooking/recipes/<slug>.md`

```markdown
# <Recipe Name>

Back to [All Recipes](cooking/recipes/README.md)

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

- [Breakfast](cooking/categories/breakfast.md)
- [Main](cooking/categories/main.md)

## Traits

- [Easy](cooking/traits/easy.md)
- [Fast](cooking/traits/fast.md)

## Books

- [Salt Fat Acid Heat](cooking/books/salt-fat-acid-heat.md)

## Macronutrients

- [Healthy Fats](cooking/macronutrients/healthy-fats.md) — 28g
- [Protein](cooking/macronutrients/protein.md) — 19g

## Minerals

- [Iron](cooking/minerals/iron.md) — 1.8mg
- [Selenium](cooking/minerals/selenium.md) — 45µg

## Vitamins

- [Vitamin A](cooking/vitamins/vitamin-a.md) — 370µg
- [Vitamin B12](cooking/vitamins/vitamin-b12.md) — 1.4µg
- [Vitamin D](cooking/vitamins/vitamin-d.md) — 3µg
```

Each nutrient bullet shows the recipe-level rounded total amount (see `### Recipe-page rendering`). Qualitative entries carry no ` — <amount>` suffix.

Section order is fixed: `Ingredients` → `Preparation` → `Notes` → `Categories` → `Traits` → `Books` → `Macronutrients` → `Minerals` → `Vitamins` → `Soft Essentials`. `## Categories` and `## Books` are always present (every recipe has ≥1 of each); other optional sections are omitted when empty (see `### Section-omission rule`). The four nutrient sections are *ingredient-derived* via `### Lookup-extend protocol`.

### `docs/cooking/categories/README.md`

```markdown
# Categories

Back to [Cooking](cooking/README.md)

- [Appetizer](cooking/categories/appetizer.md)
- [Breakfast](cooking/categories/breakfast.md)
- [Dessert](cooking/categories/dessert.md)
...
```

Lists every category currently in use under `categories/`. New entries appear here only when a corresponding `<slug>.md` file is created.

### `docs/cooking/categories/<slug>.md`

```markdown
# Breakfast

Back to [Categories](cooking/categories/README.md)

- [Breakfast Sandwiches](cooking/recipes/breakfast-sandwiches.md)
- [Classic French Omelette](cooking/recipes/classic-french-omelette.md)
...
```

H1 is the humanized form (Title Case, single word for single-word slugs; replace `-` with space for multi-word slugs).

### `docs/cooking/traits/README.md`

```markdown
# Traits

Back to [Cooking](cooking/README.md)

- [Cheap](cooking/traits/cheap.md)
- [Easy](cooking/traits/easy.md)
- [Fast](cooking/traits/fast.md)
...
```

### `docs/cooking/traits/<slug>.md`

```markdown
# Fast

Back to [Traits](cooking/traits/README.md)

- [Classic French Omelette](cooking/recipes/classic-french-omelette.md)
...
```

### `docs/cooking/books/README.md`

```markdown
# Books

Back to [Cooking](cooking/README.md)

- [Fast Easy Cheap Vegan](cooking/books/fast-easy-cheap-vegan.md)
- [Salt Fat Acid Heat](cooking/books/salt-fat-acid-heat.md)
...
```

### `docs/cooking/books/<slug>.md`

```markdown
# <Book Title>

Back to [Books](cooking/books/README.md)

<optional 1–2-sentence intro from the source — only if the book's own introduction provides one>

- [Banana Bread](cooking/recipes/banana-bread.md)
- [Classic French Omelette](cooking/recipes/classic-french-omelette.md)
...
```

The bullet list contains every recipe from this book, alphabetical, linking to the recipe's own page (which itself lists the book under `## Books`).

### `docs/cooking/macronutrients/README.md`

```markdown
# Macronutrients

Back to [Cooking](cooking/README.md)

| Category                                                 | Requirement                                                       | Function                                                | Example Sources                                                                  |
|----------------------------------------------------------|-------------------------------------------------------------------|---------------------------------------------------------|----------------------------------------------------------------------------------|
| [Complex Carbs](cooking/macronutrients/complex-carbs.md) | ~3–5 g/kg body weight per day; 45–65% of total daily calories     | Glucose for the brain, glycogen for muscles.            | Quinoa, oats, berries, legumes, sprouted grains.                                 |
| [Healthy Fats](cooking/macronutrients/healthy-fats.md)   | ~0.8–1.2 g/kg body weight per day; 20–35% of total daily calories | Hormone production, brain structure, vitamin absorption.| Extra virgin olive oil, walnuts (Omega-3), avocado, fatty fish.                  |
| [Protein](cooking/macronutrients/protein.md)             | 0.8–1.5 g/kg body weight per day; 10–35% of total daily calories  | Muscle repair, neurotransmitters, enzymes.              | Eggs (gold standard), fish, Greek yogurt, soy, lentils.                          |

> All Requirement values are daily intake targets (24-hour total, summed across all meals). Values shown are for adults 19–50; `(M)` and `(F)` distinguish male/female when they differ; `†` marks an Adequate Intake (AI) rather than RDA. Macronutrient `g/kg/day` values scale with body weight; `% of total daily calories` are AMDRs from the U.S. DRIs. Source: NIH ODS Fact Sheets ([ods.od.nih.gov/factsheets](https://ods.od.nih.gov/factsheets/list-all/)).
```

Body shape: H1 → back-link → verbatim canonical table from `## Nutrient lexicons` (4 columns, alphabetical rows, `Category` cells are Markdown links `[Display Name](cooking/<group>/<slug>.md)`, `—` for empty cells, `†` for AIs) → the source-note blockquote from `## Nutrient lexicons` (see `### Requirement-source note`). Table is frozen — see `### Frozen-table rule`. **No bullet list follows the table** — the linked Category cells are the only navigation path to the individual row pages.

### `docs/cooking/minerals/README.md`, `docs/cooking/vitamins/README.md`, `docs/cooking/soft-essentials/README.md`

Structurally identical to `macronutrients/README.md`: H1 (`# Minerals` / `# Vitamins` / `# Soft Essentials`), back-link to Cooking, verbatim canonical table from `## Nutrient lexicons`, then the source-note blockquote. For v1 the tables contain exactly 7 / 13 / 4 rows respectively.

### `docs/cooking/macronutrients/<slug>.md` (and analogous for minerals, vitamins, soft-essentials)

```markdown
# Protein

Back to [Macronutrients](cooking/macronutrients/README.md)

- [Apple Chickpea Salad](cooking/recipes/apple-chickpea-salad.md)
- [Classic French Omelette](cooking/recipes/classic-french-omelette.md)
...
```

H1 is the humanized slug (see `### Formatting conventions` for the rule, including the `omega-3` → `Omega-3` carve-out). Back-link points to the parent group's README. Bullet list is every recipe whose `## Macronutrients` / `## Minerals` / `## Vitamins` / `## Soft Essentials` section contains this slug, alphabetical. Empty list when no recipes yet reference the slug — the file still exists with just the H1 and back-link.

### `docs/cooking/ingredients-info.md`

```markdown
# Ingredients Info

Back to [Cooking](cooking/README.md)

Authoritative ingredient → nutrient lookup. Alphabetical by ingredient (canonical name; see `## Ingredient → nutrient mapping` for the normalization rules). Cells contain entries from `## Nutrient lexicons` using the EXACT `Category` column display name, each followed by a per-100g amount estimate in parentheses (`Display Name (Xunit/100g)`). `Phytochemicals` and `Probiotics` are qualitative — bare display name with no amount. An em-dash (`—`, U+2014) marks an empty cell. New ingredients are appended in alphabetical position; existing rows are not deleted.

| Ingredient | Macronutrients | Minerals | Vitamins | Soft Essentials |
|---|---|---|---|---|
| almonds | Healthy Fats (50g/100g), Protein (21g/100g) | Calcium (270mg/100g), Magnesium (270mg/100g) | Vitamin E (26mg/100g) | Dietary Fiber (12g/100g) |
| olive oil | Healthy Fats (100g/100g) | — | Vitamin E (14mg/100g), Vitamin K (60µg/100g) | — |
| spinach | — | Iron (2.7mg/100g), Magnesium (80mg/100g), Potassium (560mg/100g) | Vitamin A (470µg/100g), Vitamin B9 (190µg/100g), Vitamin C (28mg/100g), Vitamin K (480µg/100g) | Dietary Fiber (2g/100g), Phytochemicals |
```

Five columns, exactly. Cells use the canonical display name from `## Nutrient lexicons` (NOT the slug, NOT a plural, NOT a free-text variant) plus a per-100g amount in parentheses. Entries sorted alphabetically inside each cell (B-vitamins by numeric value: `Vitamin B1, Vitamin B2, …, Vitamin B9, Vitamin B12`). The file is append-only (see `### Ingredient-info append-only rule`).

## Sidebar shape

Add the following block to `docs/_sidebar.md` under a top-level `**Cooking**` group. The sidebar uses two enumerated subgroups (`**Recipes**` and `**Books**`) — every recipe and every book is a direct sidebar link. Categories, traits, and the four nutrient axes are NOT enumerated; their index pages serve as the entry points.

```markdown
- **Cooking**
  - **Recipes**
    - [All Recipes](cooking/recipes/README.md)
    - [<Recipe Name>](cooking/recipes/<recipe-slug>.md)
    - [<Recipe Name>](cooking/recipes/<recipe-slug>.md)
    - ... (every recipe, alphabetical by display name — see `### Alphabetical sort key`)
  - [Categories](cooking/categories/README.md)
  - [Traits](cooking/traits/README.md)
  - [Macronutrients](cooking/macronutrients/README.md)
  - [Minerals](cooking/minerals/README.md)
  - [Vitamins](cooking/vitamins/README.md)
  - [Soft Essentials](cooking/soft-essentials/README.md)
  - [Ingredients Info](cooking/ingredients-info.md)
  - **Books**
    - [<Book Title>](cooking/books/<book-slug>.md)
    - [<Book Title>](cooking/books/<book-slug>.md)
```

The `**Recipes**` subgroup begins with `[All Recipes]` (the index) and then lists every recipe alphabetically. The `**Books**` subgroup lists each summarized book, alphabetical. Both rely on Docsify's `docsify-sidebar-collapse` plugin (configured in `docs/index.html`) to keep the sidebar tidy when collapsed.

## Cross-recipe references

A recipe's body (typically the `## Notes` section, occasionally a `## Preparation` step) may reference another recipe.

- **In-corpus**: `[<Recipe Name>](cooking/recipes/<slug>.md)` — absolute path from the docs root (see `### Link path convention`).
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
- `docs/cooking/ingredients-info.md` is NOT bulk-read here — it is consulted on-demand per ingredient during Phase 2.4b (lookup-extend protocol). Loading the full file in Phase 2.1 would bloat context for no benefit.

### 2.2 Enumerate recipes

Walk the source TOC and produce a list of `(book-section-name, recipe-source-title, source-file)` tuples. Skip non-recipe content (front matter, indexes, acknowledgements, glossaries) unless the user requested otherwise in guided mode.

### 2.3 Map source sections to canonical categories

For each source section name (e.g., "Mains", "Soups", "Wraps & Sandwiches"), resolve to the canonical category slug using the lexicon's aliases. If a section name has no mapping (extremely rare with the alias list above), surface to the user — do NOT silently invent a new category.

### 2.4 Per-recipe category and trait assignment

For each recipe:

1. **Categories** (1–2): start with the section's mapped category. Read the recipe's source content to detect a second category if the boundary rules call for it (sweet breakfast, side-vs-main, etc.).
2. **Traits** (0+): scan the recipe's source content for triggers: time claims, "easy" wording, single-vessel preparation, no-cook / no-bake claims, freezer notes, make-ahead notes, source cost claims, dietary deviations from the book baseline, kid-friendly callouts.
3. Apply alias collapse and lexicon-first rules. Never invent.

### 2.4b Per-recipe nutrient derivation

For each recipe, walk its `## Ingredients` and apply the **lookup-extend protocol** from `## Ingredient → nutrient mapping`. Specifically:

1. For each ingredient, compute (a) the canonical name (see the normalization rules in `## Ingredient → nutrient mapping`) and (b) the mass in grams via `### Quantity → grams conversion`. Skip 0g entries.
2. Look up the canonical name in `docs/cooking/ingredients-info.md`. If absent, append a new alphabetical row with the four nutrient cells filled from established nutritional knowledge.
3. For each entry in the ingredient's four cells, multiply the per-100g amount by `mass_g / 100` and add to the recipe-level running total for that display name (per group). Qualitative entries (`Phytochemicals`, `Probiotics`) are recorded as presence with no amount.
4. After all ingredients are processed: apply the recipe drop threshold to each quantitative sum and presence to qualitative entries (see `### Threshold model`). Convert surviving display names to slugs via the **Display name → slug mapping**. Alphabetize within each group (B-vitamins by numeric value).

Record the four resulting **slug** sets on the progress tracker (four new columns: `Macronutrients`, `Minerals`, `Vitamins`, `Soft Essentials`). Per-bullet amounts are NOT stored in the tracker — they are rendered when the recipe page is written in Phase 3 (or recomputed during Phase 5.13 audit). Empty sets stay as `—` in the tracker. The agent does NOT invent slugs outside the v1 lexicon — see the critical guard in `## Ingredient → nutrient mapping`.

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
| Recipe | Slug | Categories | Traits | Macronutrients | Minerals | Vitamins | Soft Essentials | Source | Status |
|--------|------|------------|--------|----------------|----------|----------|-----------------|--------|--------|
| Classic French Omelette | classic-french-omelette | breakfast, main | easy, fast | healthy-fats, protein | iron, selenium | vitamin-a, vitamin-b12, vitamin-d | — | text/part0042.html | pending |
```

The tracker doubles as a lookup table during Phase 4. The four nutrient columns are populated in Phase 2.4b; empty sets are written as `—`.

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

Split the remaining recipes across agents (6–10 each). Each agent:

1. Reads this skill.
2. Reads the calibration recipe(s) as a style reference.
3. Reads its assigned source files.
4. For each assigned recipe, writes `docs/cooking/recipes/<slug>.md` matching the template (see `## Page templates`), using the slug / categories / traits already decided in Phase 2 (read from the progress tracker).
5. Does NOT update the progress tracker, indexes, or category/trait/book pages.
6. **Reports under 100 words**: a list of files written, one per line. No recap.

Bulk-update the progress tracker centrally from the file list.

**Compact checkpoint**: after Phase 3, proactively `/compact` before Phase 4.

## Phase 4: Update indexes & cross-references

Centralized phase. Single agent (or main thread) writes the index and category/trait/book files so all writes serialize on the same actor and no two agents fight over `categories/dessert.md`.

Steps, in this order:

1. **`recipes/README.md`** — regenerate the table in one pass by running the script bundled with this skill from the repo root:

   ```bash
   python3 .claude/skills/cooking-book-summary/scripts/build_recipes_table.py \
       > docs/cooking/recipes/README.md
   ```

   The script walks every `docs/cooking/recipes/<slug>.md` file, extracts H1 / categories / traits / nutrient sections, sorts by the standard sort key, and emits the H1 + back-link + table in the canonical 30-column format (see the recipes-index template in `## Page templates`). Never hand-edit rows — the script is the only writer, and hand-edits drift from recipe-page truth. The script is idempotent; running it twice in a row produces no diff.
2. **`categories/<slug>.md`** — for each category referenced by any new recipe:
   1. Create the file from the template if it doesn't exist.
   2. Insert each new recipe link in alphabetical position.
3. **`categories/README.md`** — append any newly-created categories in alphabetical position.
4. **`traits/<slug>.md`** — same as 2 but for traits.
5. **`traits/README.md`** — same as 3 but for traits.
6. **`macronutrients/<slug>.md`** — for each macronutrient slug referenced by any new recipe, insert the recipe link (`[<Recipe Name>](cooking/recipes/<slug>.md)`, no per-recipe amount) in alphabetical position. The 27 nutrient row files pre-exist from v1 setup; agents normally only append. **Create-if-missing fallback:** if a v1 row file is somehow absent, recreate it from the row-page template in `## Page templates` (H1 = humanized slug, see `### Formatting conventions`; back-link to the group README; then the recipe bullet). **Do NOT** add a canonical table to the row file — see `### Frozen-table rule`.
7. **`minerals/<slug>.md`** — same as 6 but for minerals.
8. **`vitamins/<slug>.md`** — same as 6 but for vitamins.
9. **`soft-essentials/<slug>.md`** — same as 6 but for soft-essentials.
10. **`books/<book-slug>.md`** — create from template; list every recipe in this book, alphabetical.
11. **`books/README.md`** — insert the new book in alphabetical position. Create the file if it didn't exist.
12. **`docs/cooking/README.md`** — create from template if it doesn't already exist. (Created once and never modified after.)

The four group `README.md` files (`macronutrients/README.md`, `minerals/README.md`, `vitamins/README.md`, `soft-essentials/README.md`) do **not** need modification during a normal run — their canonical tables are frozen at v1 (and they no longer contain a separate slug list; the Category column links replace it). The only legitimate edit is when the user explicitly approves a new lexicon row.

`docs/cooking/ingredients-info.md` is updated **inline during Phase 2.4b** (recipe-level lookup-extend). By Phase 4 it is already current.

## Phase 5: Audit

The audit is the hard bar that catches drift, fabrication, and missed cross-references. Use the same audit-fix-converge loop as `book-summary` Phase 4 (max 5 inner iterations per agent, max 5 outer rounds, early graduation after 2 consecutive clean rounds).

### 5.1 Source fidelity (per recipe)

Read each source against each recipe page. Verify every ingredient / quantity / unit / step / time / temperature / visual cue / equipment requirement is present and not fabricated. Anecdotes and philosophy correctly stripped. Units not silently converted. Names spelled as in source.

### 5.2 Recipe-name purity

H1 and slug carry no stripped descriptors (see `### Recipe-name strip-list` for the list and identity exceptions). Violations require renaming the file AND every link to it.

### 5.3 Lexicon conformance

Every category / trait used exists in `categories/README.md` / `traits/README.md` (or the v1 canonical lexicon on first run). No alias slipped through as a new file. No `desserts.md` next to `dessert.md`.

### 5.4 Bidirectional integrity

For every recipe `R` and each category `C` / trait `T` / book `B` listed on it, `grep "cooking/recipes/R.md" docs/cooking/categories/C.md` (and the trait / book analogues) must succeed — and vice-versa (entries in `categories/<slug>.md` are listed on the recipe). Apply the same two-way check for `## Traits` ↔ `traits/<slug>.md` and `## Books` ↔ `books/<slug>.md`.

### 5.5 Index completeness

Every file under `recipes/`, `categories/`, `traits/`, and `books/` (excluding `README.md`) is referenced from that directory's `README.md`; every link target in any `README.md` has a backing file. `recipes/README.md` is a table (see `### 5.16`); the others are bullet lists. Run:

```bash
# Files that exist but aren't indexed
for d in docs/cooking/recipes docs/cooking/categories docs/cooking/traits docs/cooking/books; do
  for f in $d/*.md; do
    [ "$(basename $f)" = "README.md" ] && continue
    grep -qF "$(basename $f)" $d/README.md || echo "MISSING in index: $f"
  done
done

# Index entries with no backing file (links are absolute from docs/, e.g. cooking/recipes/foo.md)
for d in docs/cooking/recipes docs/cooking/categories docs/cooking/traits docs/cooking/books; do
  rg -o '\[[^]]+\]\(([^)]+\.md)\)' $d/README.md -r '$1' | while read link; do
    [ -f "docs/$link" ] || echo "DEAD link in $d/README.md: $link"
  done
done
```

### 5.6 Link resolution

Every Markdown link inside `docs/cooking/**` resolves to an existing file and is absolute from the docs root. Per `### Link path convention`, any link target containing `../`, starting with `./`, or being a bare filename is a defect.

```bash
# Find any link that violates the absolute-from-docs-root rule
# (bare filename = any .md target with no '/', e.g. `salad.md`, `README.md`, `7-layer-dip.md`)
rg -n '\]\((?:\.\./|\./|[^/)]+\.md[)#])' docs/cooking/ && echo "FOUND non-absolute link(s)"

# Verify every link target resolves
rg -o '\]\((cooking/[^)]+\.md)\)' docs/cooking/ -r '$1' --no-filename | sort -u | while read link; do
  [ -f "docs/$link" ] || echo "DEAD link target: $link"
done
```

### 5.7 Alphabetical order

Every list that should be alphabetical is alphabetical (see `### Alphabetical sort key`). Covers: `categories/README.md`, `traits/README.md`, `books/README.md` bullet lists; every category / trait / book page's recipe list; every recipe page's `## Categories` / `## Traits` / `## Books` sections; and the comma-separated entries inside each `Categories` / `Traits` cell of the recipes-index table. The recipes-index table row order is covered byte-for-byte by `### 5.16`.

### 5.8 Back-link presence

Every page under `docs/cooking/**` carries the exact prescribed back-link line from `### Back-link wording`, immediately under the H1, blank-line separated above and below.

### 5.9 Metadata / template conformance

Every recipe page: H1 followed by blank line; metadata blockquote in canonical field order with ` · ` separators (omit only when the source provides zero canonical fields); section headers in canonical order (`Ingredients`, `Preparation`, optional `Notes`, `Categories`, optional `Traits`, `Books`, then optional `Macronutrients` / `Minerals` / `Vitamins` / `Soft Essentials`); two-column ingredient table; Unicode fractions in the Quantity column. See `### Section-omission rule` for which sections may be omitted.

### 5.10 Frozen-table integrity

The four group `README.md` tables are byte-identical to `## Nutrient lexicons` (modulo whitespace within a cell). `Category` cells MUST be Markdown links `[Display Name](cooking/<group>/<slug>.md)`. See `### Frozen-table rule`.

### 5.11 Nutrient bidirectional integrity

For each recipe `R` and each nutrient slug `N` listed on it: `grep "cooking/recipes/R.md" docs/cooking/<group>/N.md` must succeed; and every recipe link in a nutrient row file corresponds to an entry in that recipe's nutrient section.

### 5.12 Ingredient-info coverage

Every ingredient in every recipe under `docs/cooking/recipes/` appears as a row in `docs/cooking/ingredients-info.md` under its canonical name. Surface unmatched ingredients; do not silently fix — add the row with a real nutrient profile (see `### Lookup-extend protocol`). New rows go in alphabetical position; existing rows are not deleted (see `### Ingredient-info append-only rule`).

### 5.13 Nutrient-derivation correctness

Recompute each recipe's four nutrient sets and per-recipe totals: walk its `## Ingredients`, convert each quantity via `### Quantity → grams conversion` (skip 0g entries), look up each canonical name in `ingredients-info.md`, multiply each per-100g amount by `mass_g / 100`, sum per nutrient. Confirm:

- The four nutrient sections list the same quantitative nutrients (deduped, alphabetical, B-vitamins by numeric value, empty sections and below-threshold bullets omitted). **Qualitative entries** (`Phytochemicals`, `Probiotics`) are governed by presence — see `### Threshold model`.
- **Threshold check (HARD CLIFF — applies BEFORE the tolerance check):** for every quantitative slug, compare the recomputed **unrounded** total against the per-nutrient **recipe drop threshold**. If the recipe page DROPPED a bullet, the recomputed unrounded total MUST be **below** the recipe drop threshold; if the page RENDERS, MUST be **at or above**. The recipe drop threshold is a hard boundary that wins over the ±20% / ±1-step tolerance: a printed `Vitamin C — 6mg` bullet for a recomputed unrounded `4.5mg` (recipe drop threshold 5mg) is a defect even though `4.5mg` is within ±20% of `6mg`; a dropped Vitamin C bullet for a recomputed unrounded `5.5mg` is also a defect. Same applies to macros (printed `1g` Protein for recomputed `0.95g` is a defect — threshold 1g) and every other slug. The looser inclusion threshold gates `ingredients-info.md` cells (see `### 5.14`); the stricter recipe drop threshold gates recipe-page bullets (here).
- **Tolerance check (applies only to bullets that pass the threshold check):** each rendered bullet's printed amount matches the recomputed total within **±20% or ±1 step of the rounding granularity, whichever is greater**. "Rounding granularity" means the rounding step from the applicable band in `### Recipe-page rendering` — e.g., for `[100, 1000)` rounded to the nearest 10, granularity is 10, so `370µg` is acceptable for a recomputed `360µg` or `380µg`. **For macros and Dietary Fiber, granularity is `1g` (plain integer)**, and the ±20% rule typically dominates: `28g` is acceptable for a recomputed range of `~22g–~34g`.
- Gross errors (wrong unit, missing factor of 10, qualitative-vs-quantitative confusion) fail.
- Qualitative bullets (`Phytochemicals`, `Probiotics`) carry NO ` — <amount>` suffix; including one is a defect.

Discrepancies fail the audit.

### 5.14 Slug / display-name / amount-format validity

Every slug in any recipe nutrient section or any nutrient row file exists in the v1 lexicon (27 slugs in `## Nutrient lexicons`). No invented slugs, no `b-complex`, no aliases, no plurals.

`ingredients-info.md` cell entries use the EXACT `Category` column display name (e.g., `Vitamin B12`, `Omega-3 (EPA/DHA)`), followed by `(Xunit/100g)` for quantifiable nutrients or no amount for `Phytochemicals` / `Probiotics`. Slug-form entries (`vitamin-b12`, `omega-3`) inside a cell are a defect.

**Canonical-unit consistency**: every `(<value><unit>/100g)` cell amount uses the canonical unit (see `### Canonical units and inclusion thresholds per nutrient`). Defects: `Vitamin A (0.47mg/100g)` (canonical unit is `µg` — must be `Vitamin A (470µg/100g)`); `Iron (2700µg/100g)` (canonical unit is `mg` — must be `Iron (2.7mg/100g)`); `Vitamin D (200 IU/100g)` (must be `µg`). Same defect class applies to recipe-page bullet amounts — `Vitamin A — 0.5mg` instead of `Vitamin A — 500µg`. Fix by re-expressing in the canonical unit before any summation runs.

**Per-100g `inclusion threshold` compliance for `ingredients-info.md` cells:** audit uses the **inclusion threshold** column (the looser — recipe drop threshold ÷ 5), NOT the recipe drop threshold. See `### Threshold model`. Defects:

- **Below-inclusion-threshold entry present:** e.g., `Vitamin C (0.5mg/100g)` (inclusion threshold `1mg`) — true-trace level, must be REMOVED.
- **Above-inclusion-threshold nutrient absent:** if established USDA per-100g data shows the ingredient has a nutrient at or above the inclusion threshold, the row MUST list it. Concrete cases the previous (single-threshold) audit incorrectly trimmed and that the inclusion-threshold audit MUST restore: apple Vitamin C ~4.6mg/100g (above 1mg inclusion threshold), pear Vitamin C ~4.3mg/100g, sweet potato Vitamin C ~2.4mg/100g, peach Vitamin A ~16µg/100g (above 10µg inclusion threshold), pumpkin Dietary Fiber ~0.5g/100g (above 0.2g inclusion threshold). Missing entries — even when the agent considered the per-recipe contribution unlikely to surface — are defects under the no-preemptive-recipe-quantity-assumption rule.

**Important: do NOT preemptively apply the recipe drop threshold here.** Filtering ingredient cells against the recipe drop threshold (e.g., dropping `apple Vitamin C (4.6mg/100g)` because it's below the 5mg recipe drop threshold) is wrong: the recipe drop threshold gates the per-recipe SUM (apple at 1kg yields ~46mg → above 5mg → renders), not the per-100g entry. Worked example: apple Vitamin C ~4.6mg/100g × 1kg = 46mg, which is above the 5mg recipe drop threshold → renders. Use the inclusion threshold column for ingredient-cell decisions.

Per-recipe threshold compliance for recipe-page bullets is checked by `### 5.13`.

**Recipe-page nutrient bullet format**: `- [<Display Name>](cooking/<group>/<slug>.md) — <amount><unit>` for quantitative; `- [<Display Name>](cooking/<group>/<slug>.md)` for qualitative `Phytochemicals` / `Probiotics`. Defects:

- Missing ` — <amount><unit>` suffix on a quantitative bullet.
- Including ` — <amount>` on `Phytochemicals` or `Probiotics`.
- Hyphen-minus or en-dash instead of em-dash (` — ` is `space U+2014 space`).
- Space between number and unit (`28 g` wrong; `28g` correct).
- Display name in slug form (`vitamin-b12` instead of `Vitamin B12`) or in plural / free-text variant.

### 5.15 Sub-recipe profile validity

For every sub-recipe used as an ingredient anywhere under `docs/cooking/recipes/`:

- A row exists in `ingredients-info.md` whose Ingredient column is a Markdown link to the sub-recipe's recipe page (`| [<Title>](cooking/recipes/<slug>.md) | … |`) — never a plain canonical-name string.
- The four nutrient cells follow the per-100g convention from `### Sub-recipe ingredients`. Recompute the per-100g profile (steps a–d in that section); each surfaced display-name amount matches within ~10% rounding tolerance. Missing nutrients above the inclusion threshold, or surfaced nutrients below it, are defects.
- **Recursion invariant:** parent recipes that use a sub-recipe MUST include its per-100g contribution in their derived nutrient sums. A parent recipe whose sums silently exclude a sub-recipe's nutrients is the canonical pre-v1 defect this audit catches.

Enumerate sub-recipes by scanning every recipe's `## Ingredients` table for substrings matching another recipe's H1 (case-insensitive). The set is closed: a recipe is a sub-recipe iff at least one other recipe lists it as an ingredient. Build-your-own / template recipes (e.g., `guzinta-bowl-guide`, `toast-is-the-most`) reference sub-recipes only inside `—`-quantity rows, so those parents contribute no real consumption — sub-recipe rows still exist, but parent re-derivation is a no-op there.

Discrepancies fail the audit. Restore by recomputing the sub-recipe's per-100g profile, updating its row, and re-deriving every parent.

### 5.16 Recipes-index table integrity

`docs/cooking/recipes/README.md` MUST be byte-identical to the output of the bundled script:

```bash
python3 .claude/skills/cooking-book-summary/scripts/build_recipes_table.py | diff - docs/cooking/recipes/README.md
```

Any diff is a defect — restore by re-running the script with output redirected to the file (see Phase 4 step 1). The script is the only sanctioned writer.

Named invariants (a failure will surface as a diff; stating them aids debugging):

- **Row count = recipe-page count.** Every `docs/cooking/recipes/*.md` (excluding `README.md`) is exactly one row; every row corresponds to a file.
- **Recipe cell link target exists.** Each `Recipe` cell links to `cooking/recipes/<slug>.md`; the target file must exist.
- **Categories / Traits cells = slugs only**, comma-separated, alphabetical; `—` only when the section is absent (Traits) or impossible (Categories, never empty). **Display names in these cells are a defect — slugs only.**
- **Quantitative nutrient cells match the recipe-page bullets byte-for-byte.** `158g` on the recipe page → `158g` in the cell; `—` ↔ bullet absent. Discrepancies are defects — fix the recipe page (source of truth) and regenerate.
- **Qualitative nutrient cells**: `yes` ↔ recipe-page bullet present; `—` ↔ bullet absent. Anything else (`y`, `Y`, `✓`, `true`, blank) is a defect. 5.16 checks only the cell value form; bullet-format defects (malformed qualitative bullet with illegal suffix, slug-form display name) are caught by `### 5.13` / `### 5.14`. The script emits `[WARN]` to stderr for the structural subset it can detect (unparseable bullet, qualitative bullet with an amount, quantitative bullet missing its amount).
- **Alphabetical row order** (see `### Alphabetical sort key`).

**Auditors fix the recipe page, not cells in the README.** (Or the script's column list, on user-approved addition of a new v1 lexicon row — see the lexicon-expansion bullet in `## What is dropped` for the full file list.) Then rerun the script.

### Audit reports

Audit agents report under 50 words, one line per recipe:

- `<slug>: CLEAN`
- `<slug>: N fixes — <terse phrase per fix>` (e.g., `chocolate-pots: 2 fixes — renamed (3-ingredient stripped), added breakfast category`)

No recaps, no diffs. The fix is in the file; the report is the ledger.

### Convergence

Repeat audit rounds until every recipe reports clean on first iteration of a round, or max 5 outer rounds. At max iterations with remaining issues, stop and surface to the user — do not silently accept flawed output.

**Compact checkpoint**: after Phase 5 converges, proactively `/compact` before Phase 6.

## Phase 6: Finalize

1. Update `docs/_sidebar.md` (see `## Sidebar shape`). If the `**Cooking**` block already exists: (a) insert each new recipe into the `**Recipes**` subgroup in alphabetical position (preserving the leading `[All Recipes]` entry), (b) ensure all four nutrient indexes and `[Ingredients Info]` are listed, and (c) add the new book to `**Books**` in alphabetical position.
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
| Macronutrient pages | `docs/cooking/macronutrients/<slug>.md` | Yes |
| Mineral pages | `docs/cooking/minerals/<slug>.md` | Yes |
| Vitamin pages | `docs/cooking/vitamins/<slug>.md` | Yes |
| Soft-essential pages | `docs/cooking/soft-essentials/<slug>.md` | Yes |
| Ingredient lookup | `docs/cooking/ingredients-info.md` | Yes |
| Cooking landing | `docs/cooking/README.md` | Yes |
| Sidebar | `docs/_sidebar.md` | Yes |
| Source extraction | `tmp/<book-slug>/` | No |
| Progress tracker | `tmp/<book-slug>-progress.md` | No |

## What is dropped

- **Phase 5 "Narrative"** from `book-summary` does not apply. Cookbooks don't get a whole-book narrative summary.
- **Per-book folders** under `docs/cooking/books/<book-slug>/<category>/<recipe>.md`. Recipes are global; books are flat reference pages.
- **`md-standards` H2 numbering and TOC.** The cooking templates above are the authoritative shape.
- **Lexicon expansion without explicit user approval.** The four nutrient lexicons (3 macronutrients, 7 minerals, 13 vitamins, 4 soft-essentials = 27 slugs) are **closed at v1**, mirroring the trait lexicon's closed status. The standard "lexicon-first rule" applies: agents do not invent rows, do not add columns, do not rename slugs, and do not silently fix table content. Unmapped concepts are surfaced to the user in the Phase 2.8 / Phase 6 completion report. A user-approved addition MUST also update the hardcoded slug lists in `.claude/skills/cooking-book-summary/scripts/build_recipes_table.py` (`NUTRIENT_COLUMNS`) and `scripts/export_recipes_bincode.py` (`NUTRIENT_SLUGS`, which validates against the README header row), then regenerate `recipes/README.md`.
