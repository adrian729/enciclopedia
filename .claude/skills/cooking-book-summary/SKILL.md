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
├── README.md                              # Cooking landing page
├── ingredients-info.md                    # Alphabetical ingredient → nutrient lookup
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
├── books/
│   ├── README.md                          # Alphabetical list of every book summarized
│   └── fast-easy-cheap-vegan.md
├── macronutrients/                        # ingredient-derived facet
│   ├── README.md                          # canonical table (Category cells link to row pages)
│   ├── complex-carbs.md
│   ├── healthy-fats.md
│   └── protein.md
├── minerals/                              # ingredient-derived facet
│   ├── README.md                          # canonical table (Category cells link to row pages)
│   ├── calcium.md
│   ├── iodine.md
│   ├── iron.md
│   ├── magnesium.md
│   ├── potassium.md
│   ├── selenium.md
│   └── zinc.md
├── vitamins/                              # ingredient-derived facet
│   ├── README.md                          # canonical table (Category cells link to row pages)
│   ├── vitamin-a.md
│   ├── vitamin-b1.md
│   ├── vitamin-b2.md
│   ├── vitamin-b3.md
│   ├── vitamin-b5.md
│   ├── vitamin-b6.md
│   ├── vitamin-b7.md
│   ├── vitamin-b9.md
│   ├── vitamin-b12.md
│   ├── vitamin-c.md
│   ├── vitamin-d.md
│   ├── vitamin-e.md
│   └── vitamin-k.md
└── soft-essentials/                       # ingredient-derived facet
    ├── README.md                          # canonical table (Category cells link to row pages)
    ├── dietary-fiber.md
    ├── omega-3.md
    ├── phytochemicals.md
    └── probiotics.md
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

### Link path convention

All Markdown links inside `docs/cooking/**` MUST be **absolute from the docs root**, i.e. start with `cooking/...`. This project uses Docsify with the default `relativePath: false`, which resolves every link as if it were rooted at `docs/`. Relative paths like `apple-chickpea-salad.md`, `../recipes/foo.md`, `README.md`, or `../README.md` resolve to wrong URLs (e.g. `/#/apple-chickpea-salad` instead of `/#/cooking/recipes/apple-chickpea-salad`) and break every recipe link.

Required form for every link target under `docs/cooking/**`:

| From → To | Correct link |
|---|---|
| any cooking page → cooking landing | `cooking/README.md` |
| any cooking page → recipes index | `cooking/recipes/README.md` |
| any cooking page → categories index | `cooking/categories/README.md` |
| any cooking page → traits index | `cooking/traits/README.md` |
| any cooking page → books index | `cooking/books/README.md` |
| any cooking page → a recipe | `cooking/recipes/<slug>.md` |
| any cooking page → a category | `cooking/categories/<slug>.md` |
| any cooking page → a trait | `cooking/traits/<slug>.md` |
| any cooking page → a book | `cooking/books/<slug>.md` |
| any cooking page → macronutrients index | `cooking/macronutrients/README.md` |
| any cooking page → minerals index | `cooking/minerals/README.md` |
| any cooking page → vitamins index | `cooking/vitamins/README.md` |
| any cooking page → soft-essentials index | `cooking/soft-essentials/README.md` |
| any cooking page → a macronutrient | `cooking/macronutrients/<slug>.md` |
| any cooking page → a mineral | `cooking/minerals/<slug>.md` |
| any cooking page → a vitamin | `cooking/vitamins/<slug>.md` |
| any cooking page → a soft-essential | `cooking/soft-essentials/<slug>.md` |
| any cooking page → ingredients info | `cooking/ingredients-info.md` |

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

### Nutrient-section omission rule

`## Macronutrients`, `## Minerals`, `## Vitamins`, and `## Soft Essentials` are omitted from a recipe page when their derived list is empty (same omission rule as `## Traits`). The four sections always appear in this fixed order, after `## Books`. Bullets within each section are alphabetical by display name, case-insensitive, with B-vitamins ordered by numeric value (`Vitamin B1` … `Vitamin B12`, NOT ASCII).

Within each section, drop any **quantitative** bullet whose computed per-recipe **unrounded** total is below the per-nutrient **recipe drop threshold** in `### Canonical units and inclusion thresholds per nutrient`. The recipe drop threshold is the single arbiter — there is NO separate "rounds to 0" rule and no separate macro/fiber floor test (the macros and fiber recipe drop thresholds are simply `1g`, applied via the same threshold check as every other quantitative slug). **Qualitative** bullets (`Phytochemicals`, `Probiotics`) have no quantitative total and are NEVER subject to this rule; they appear whenever ≥1 ingredient lists them in `ingredients-info.md` and are removed only if no ingredient lists them at all. If dropping below-threshold quantitative bullets (and the absence of any qualifying qualitative entries) leaves the section empty, omit the section entirely.

### Frozen-table rule

The canonical tables in `docs/cooking/macronutrients/README.md`, `minerals/README.md`, `vitamins/README.md`, and `soft-essentials/README.md` are **byte-for-byte canonical**. They duplicate the tables in this SKILL's `## Nutrient lexicons` section (4 columns: `Category | Requirement | Function | Example Sources`; the `Category` cell of each row contains a Markdown link of the form `[Display Name](cooking/<group>/<slug>.md)` — never bare display text and never a slug; rows alphabetical by display name, with B-vitamins ordered by numeric value — `Vitamin B1` … `Vitamin B12` — NOT ASCII; `—` for empty cells, `†` for AIs). Audit and formatting passes MUST NOT modify them. Any drift between the SKILL copy and the README copy is a defect — restore from this SKILL. Reformatting attempts (renaming columns back to `Top Sources`/`Best Sources`, adding columns like `Type`, splitting cells into multiple rows, re-sorting B-vitamins as ASCII strings, unlinking the Category cells, splitting the link across lines, etc.) explicitly violate this rule.

### Ingredient-info append-only rule

`docs/cooking/ingredients-info.md` grows monotonically. Existing rows are never deleted by agents; they may be corrected only on explicit user instruction. New rows are inserted in alphabetical position. Cells use display names from `## Nutrient lexicons` with per-100g amount estimates (see "Cell content rules" in `## Ingredient → nutrient mapping`); entries are sorted alphabetically inside each cell — never reorder them into "frequency" or "priority" order. Empty cells are a single en-dash (`—`), never blank, never `none`, never `N/A`.

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

```
| Category | Requirement | Function | Example Sources |
```

No table uses a different column name (`Top Sources`, `Best Bioavailable Sources`, `Why You Can't Skip It`, `Main Focus`, `Mineral`, `Type`, etc.). Empty cells are a single en-dash (`—`). Rows are alphabetized within each table per the alphabetical sort key.

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

Cells in the `Example Sources` column contain edible foods only. No supplements (D3 capsules, algae oil softgels, B12 pills), no non-foods (sunlight). Water is the only acceptable "intake by default" non-recipe item but is not actually present in any cell. The tables map to recipes; supplements and sunlight do not appear in any recipe ingredient list and would create dead leads in `ingredients-info.md`.

Examples are also restricted to **vegetarian + fish/shellfish** sources. "Vegetarian" here is broad: plants, grains, legumes, nuts, seeds, fungi, eggs, dairy, honey, and any other vegetarian-friendly products are all allowed. Fish and shellfish (clams, oysters, mussels) are also allowed. The only exclusion is land-animal flesh — no beef, pork, lamb, chicken, turkey, liver, or other meat / poultry / organ meats. When a row's most concentrated source is land meat (e.g., liver for retinol, beef for B12), substitute the next-best vegetarian or pescatarian source (egg yolks, dairy, fatty fish, sardines) rather than reintroducing meat.

## Ingredient → nutrient mapping

Recipe nutrient sections are *derived*, not hand-picked. The single authoritative lookup is `docs/cooking/ingredients-info.md`. This section defines its schema and the protocol agents follow when writing or auditing a recipe's nutrient sections.

### Canonical units and inclusion thresholds per nutrient

**Each of the 25 quantitative v1 nutrient slugs has exactly one canonical unit AND two thresholds — one for ingredient-cell inclusion (looser) and one for recipe-page rendering (stricter).** The unit is fixed: every `ingredients-info.md` cell for that nutrient MUST use this unit, and every recipe-page bullet for that nutrient MUST display the summed total in this unit. **Do NOT mix units within a nutrient** — `spinach` writing `Vitamin A (470µg/100g)` and another row writing `Vitamin A (0.5mg/100g)` is a defect: the agent would sum `470 + 0.5 = 470.5` and emit a wrong value (the correct sum is `470 + 500 = 970µg`). The single-unit rule below makes summation a straight numeric add with no conversion step.

**Why two thresholds (and not one).** A recipe can use anywhere from a teaspoon to a kilogram of any single ingredient — we cannot know in advance which. If the ingredient-cell rule used the same threshold as the recipe-page rule, we would silently drop nutrients whose per-100g content is small but whose contribution to a large-quantity recipe would be meaningful (e.g., apple Vitamin C at 4.6mg/100g, recipe drop threshold 5mg — pre-filtering at ingredient level would mean a 1kg apple pie loses Vitamin C from the lookup, even though the per-recipe sum would be ~46mg, well above the recipe threshold). The two-tier design fixes this: the **ingredient inclusion threshold** is calibrated to ~1% of the adult RDA / AI per 100g (a low floor that filters only true-trace amounts) and is set to **the recipe drop threshold ÷ 5**. The **recipe drop threshold** stays at ~5% of the adult RDA / AI and decides whether the per-recipe summed total surfaces as a bullet.

The two thresholds are used at two distinct stages:

1. **`ingredients-info.md` cell inclusion (per-100g content):** include a nutrient on the row whenever the ingredient's per-100g content is **at or above the inclusion threshold**. Omit when below the inclusion threshold (true-trace contamination — e.g., a vegan food with traceable B12 from soil microbes that is not a meaningful source). Do NOT preemptively apply the recipe drop threshold here — we don't know in advance how much of the ingredient any recipe will use, so a low per-100g content can still produce a meaningful per-recipe sum at high ingredient quantities.
2. **Recipe-page rendering (per-recipe sum):** drop the bullet whenever the summed recipe-level total is **below the recipe drop threshold**. Render the rounded amount when at or above. Recipe-level filtering is the gate that surfaces only meaningful contributions to the reader.

This makes the threshold table the single source of truth for "what counts" at each stage. Agents do NOT make ad-hoc calls about trace amounts; they consult the table.

| Slug | Display name | Canonical unit | Inclusion threshold (per 100g) | Recipe drop threshold (per recipe) | Notes |
|---|---|---|---|---|---|
| `complex-carbs` | `Complex Carbs` | `g` | `0.2g` | `1g` | Macros — always `g`. |
| `healthy-fats` | `Healthy Fats` | `g` | `0.2g` | `1g` | Always `g`. **Strict policy: only UNSATURATED fats count** (lexicon Example Sources are extra-virgin olive oil, walnuts, avocado, fatty fish — all unsaturated). Coconut oil / coconut milk / coconut cream / palm oil / butter / lard / dairy fat / deep-frying fat / hydrogenated shortening are saturated and DO NOT contribute to `Healthy Fats`. Saturated fat is not tracked anywhere in v1. |
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

**Why this matters for summation.** The lookup-extend protocol computes `contribution = X × mass_g / 100` for each ingredient and sums per nutrient. Because every cell for a given nutrient uses the same unit, the sum is a straight numeric add — no µg-to-mg conversion ever appears in the agent's workflow. If an audit ever finds a cell using a non-canonical unit (e.g., `Vitamin A (0.47mg/100g)` instead of `Vitamin A (470µg/100g)`), it is a defect to be fixed by re-rendering the cell in the canonical unit before any summation runs.

**Adding a new ingredient.** When step 4 of the lookup-extend protocol adds a new row to `ingredients-info.md`, the per-100g amount for each nutrient MUST be expressed in the canonical unit above. Do NOT pick a unit based on what feels readable for that ingredient — readability is fixed at the slug level, not the row level. The agent fills a nutrient cell entry whenever the ingredient's per-100g content is **at or above the inclusion threshold above** (the looser, ingredient-level threshold) — and omits it when below. The recipe drop threshold is NOT applied at this stage. Example: apple Vitamin C is ~4.6mg/100g — above the 1mg inclusion threshold, so the row lists `Vitamin C (4.6mg/100g)`, even though a recipe using only ~50g of apple would yield ~2mg (below the 5mg recipe drop threshold and would NOT render a bullet at the recipe stage). A recipe using ~1kg of apple yields ~46mg (above the recipe threshold and DOES render). The two-tier design preserves this signal at the lookup level so the recipe-stage filter has the data it needs.

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

- Comma-separated list of entries from the relevant group's lexicon. Each entry uses the EXACT `Category` column display name from `## Nutrient lexicons` (e.g., `Complex Carbs`, `Healthy Fats`, `Vitamin B12`, `Omega-3 (EPA/DHA)`, `Dietary Fiber`) — never the slug form, never a plural, never a free-text variant.
- Each entry is followed by an approximate per-100g amount in parentheses, rounded to a natural value, **using the canonical unit for that nutrient from `### Canonical units and inclusion thresholds per nutrient` above** (do NOT pick the unit row-by-row). Format: `<Display Name> (<value><unit>/100g)`. Do NOT prefix the amount with `~` — Docsify's bundled marked@1.x parser treats single tildes as strikethrough delimiters, so `(~50g/100g), Protein (~21g/100g)` would render with a strikethrough span across `50g/100g), Protein (`. Examples:
  - Macronutrients (always `g`): `Healthy Fats (50g/100g)`, `Protein (21g/100g)`, `Complex Carbs (66g/100g)`.
  - Minerals (per the canonical-unit table — Calcium / Iron / Magnesium / Potassium / Zinc in `mg`; Iodine / Selenium in `µg`): `Calcium (270mg/100g)`, `Selenium (30µg/100g)`.
  - Vitamins (per the canonical-unit table): `Vitamin C (28mg/100g)`, `Vitamin B12 (0.9µg/100g)`, `Vitamin A (470µg/100g)`. Never write `Vitamin A (0.47mg/100g)` — that's a different (non-canonical) unit and would corrupt summation.
  - Soft Essentials: `Dietary Fiber (12g/100g)`, `Omega-3 (EPA/DHA) (2400mg/100g)` use a per-100g amount; `Phytochemicals` and `Probiotics` are qualitative — write the bare display name with no amount.
- Within-cell sort: alphabetical by display name, case-insensitive. Vitamins ending in a digit sort by **numeric value** of the digit, NOT ASCII: `Vitamin B1, Vitamin B2, Vitamin B3, Vitamin B5, Vitamin B6, Vitamin B7, Vitamin B9, Vitamin B12`.
- Empty cells written as a single en-dash (`—`) — never blank, never `none`, never `N/A`.
- **Inclusion criterion (per-100g `inclusion threshold`, NOT the stricter recipe drop threshold):** a nutrient is listed in the row whenever the ingredient's per-100g content is **at or above the inclusion threshold** for that nutrient (see `### Canonical units and inclusion thresholds per nutrient` — the `Inclusion threshold (per 100g)` column, which is roughly the recipe drop threshold ÷ 5). It is **omitted** when below the inclusion threshold. **Do NOT apply the recipe drop threshold here** — at the ingredient level we do not know how much of the ingredient any particular recipe will use, and a small per-100g content can still produce a meaningful recipe-level sum at high ingredient quantities (e.g., apple Vitamin C at 4.6mg/100g is below the 5mg recipe drop threshold but well above the 1mg inclusion threshold, and a 1kg apple-pie filling delivers ~46mg, which the recipe stage would surface). The agent's job at the ingredient level is to write what's actually in the food, filtered only against the looser inclusion threshold; the recipe-level filter decides whether to surface a nutrient on any particular recipe page.
- For qualitative entries (`Phytochemicals`, `Probiotics`), include whenever the ingredient is a recognized source (lycopene, capsaicin, anthocyanins, sulforaphane, etc. for Phytochemicals; live-culture fermented items for Probiotics) — there is no quantitative threshold.

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

> Note on `Omega-3 (EPA/DHA)`: the slug drops the `(EPA/DHA)` parenthetical per the standard slug-derivation rule (lowercase, kebab-case, parentheticals dropped). The slug is `omega-3`, the file is `cooking/soft-essentials/omega-3.md`, and the recipe-page bullet link text is `Omega-3` (humanized slug, parenthetical absent) — see `### Recipe-page rendering` for the bullet-link-text rule.

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

- **Eggs default to `large` = 50g.** This matches North American recipe convention (USDA "large" is the standard cookbook default). So `2 eggs` → 100g, even though the table also lists smaller variants.
- **Mushrooms (whole-item count, cultivar omitted) default to white/button = 18g** — e.g., `1 mushroom`, `2 mushrooms`. When the source names a cultivar (`1 cremini`, `1 portobello cap`, `2 shiitake`), use the cultivar's row. **Volume measurements** (`½ cup chopped mushrooms`, `1 cup sliced mushrooms`) follow the **whole-item-vs-volume precedence** rule and go to the volume table above — specifically the row labeled `Mushrooms (sliced / chopped, raw)` (70g per cup) — NOT to this whole-item fallback.
- **All other current items** (every entry besides eggs and mushrooms — `1 medium onion`, `1 medium carrot`, `1 stalk celery`, `1 clove garlic`, `1 slice bread`, `1 cherry tomato`, etc.) have only one row in the table and therefore fall through to the **Single-variant items** rule below. There is no choice to make.
- **Forward-compatibility:** if a future revision adds multiple non-egg, non-mushroom size rows for some item, those default to the `medium` entry. (No such item exists in the current table.)

**Single-variant items.** When the table lists only one row for an item (whether tagged `medium` or untagged — e.g., `1 medium onion`, `1 stalk celery`, `1 clove garlic`, `1 slice bread`), the single listed weight applies **regardless of any size qualifier in the source**. The skill deliberately avoids size-scaling for single-row items because it would require per-ingredient density judgments that drift across runs. If a recipe truly hinges on a non-default size (`1 large butternut squash` ≈ 1500g vs. medium ≈ 1000g), the agent estimates from established culinary knowledge per the "ingredients/forms not in either table" rule below — but this is the exception, not the default behavior.

For ingredients/forms not in either table (`1 medium butternut squash` ≈ 1000g, `1 small head of broccoli` ≈ 400g, `1 head of garlic` ≈ 50g), estimate from established culinary knowledge. For canned/jarred items: prefer the drained weight when "drained" is mentioned (typically ~60% of the can's gross weight); otherwise use the source's stated total weight.

### Lookup-extend protocol

The writing process for the four nutrient sections of any recipe page:

1. For each row in the recipe's `## Ingredients` table, compute (a) the canonical ingredient name per the normalization rules above, and (b) the ingredient mass in grams via `### Quantity → grams conversion`. Skip ingredients with 0g mass.
2. Search `ingredients-info.md` for that canonical name. (`grep -i "^| <name> |" docs/cooking/ingredients-info.md` is fine; `Read` followed by visual scan is fine. **Do not invent or fuzzy-match** — exact canonical match only.) **Sub-recipe rows** use a Markdown link in the Ingredient column (`| [Maple Dijon Dressing](cooking/recipes/maple-dijon-dressing.md) | … |`); for those, match against the link text only, ignoring `[...](...)` syntax. After matching, the four cells provide the sub-recipe's per-100g profile and the standard `(value × grams / 100)` math applies — sub-recipes are otherwise treated identically to raw ingredients during lookup.
3. **If found:** read the four nutrient cells. For each entry of the form `<Display Name> (<X><unit>/100g)`:
   - Compute the contribution: `contribution = X × mass_g / 100` (in the same unit).
   - Add the contribution to the recipe-level running total for that display name (per group).
   - For qualitative entries (`Phytochemicals`, `Probiotics`), no amount is summed — just record presence.
4. **If not found:**
   1. Determine the ingredient's nutrient profile from established nutritional knowledge — both which nutrients are present meaningfully and the per-100g amount of each.
   2. Add a new row to `ingredients-info.md` in the correct alphabetical position with the four cells filled per the **Cell content rules** above (display names + `(Xunit/100g)` amounts, or a single `—` if none).
   3. Then read the cells back and apply step 3 to compute contributions.
5. After processing every recipe ingredient:
   - **Quantitative entries (all 25 quantitative slugs — macros, fiber, minerals, vitamins, Omega-3):** for each, compare the summed **unrounded** total against the per-nutrient **recipe drop threshold** in `### Canonical units and inclusion thresholds per nutrient`. If the total is **below** the recipe drop threshold, drop the bullet (no meaningful contribution to surface). If at or above, round per `### Recipe-page rendering` and render. The recipe drop threshold is the single arbiter — there is no separate "rounds to 0" rule. (Note: the *inclusion* threshold is looser and applies to `ingredients-info.md` cells, not to recipe pages.)
   - **Qualitative entries** (`Phytochemicals`, `Probiotics`): keep them whenever ≥1 ingredient listed them in step 3. They have no summed total and no threshold; presence is the only test.
   - Convert each remaining display name to its slug via the **Display name → slug mapping**.
   - Write the four nutrient sections on the recipe page using deduped, alphabetically-sorted bullets per `### Recipe-page rendering`. Omit any section whose set is empty (every quantitative entry below threshold AND no qualifying qualitative entries).

**Dedup + sort.** Within a recipe's `## Macronutrients` (and the other three sections), each slug appears at most once and the bullet list is alphabetical by display name, case-insensitive, with B-vitamins by numeric value (`Vitamin B1` … `Vitamin B12`). Bullets link to the slug's canonical row file (e.g., `cooking/minerals/iron.md`).

**Critical guard.** The agent **MUST NOT** invent slugs not present in the v1 lexicons. If the agent believes an ingredient provides a nutrient that has no slug (e.g., a hypothetical "iron-bound copper"), it surfaces this to the user — it does not silently add a new row to any lexicon table or to `ingredients-info.md`.

### Sub-recipe ingredients

Some recipes use other recipes as ingredients (e.g., `apple-chickpea-salad` calls for "1 batch Maple Dijon Dressing"; `breakfast-sandwiches` uses "1 tbsp Tofu Scramble Seasoning"). These sub-recipe ingredients need a row in `ingredients-info.md` so their nutrients propagate to the parent — but the row is built differently from a raw-ingredient row.

**Convention.** A sub-recipe gets a row in `ingredients-info.md` like any other ingredient, with two differences:

1. **Ingredient column is a Markdown link** to the recipe page:

   ```
   | [Maple Dijon Dressing](cooking/recipes/maple-dijon-dressing.md) | Healthy Fats (60g/100g) | Calcium (40mg/100g), Potassium (110mg/100g) | Vitamin C (8mg/100g), Vitamin E (2.4mg/100g), Vitamin K (11µg/100g) | — |
   ```

   The visible link text is the recipe's H1 (Title Case). This signals "this row is a sub-recipe; click for the underlying recipe."

2. **Nutrient cells contain a per-100g profile computed by aggregating the sub-recipe's own `## Ingredients` table.** The procedure:
   a. For each ingredient row in the sub-recipe, compute canonical name → grams (per `### Quantity → grams conversion`).
   b. Sum those masses → the sub-recipe's **batch mass** (the total grams of the produced output; for sauces, seasonings, dressings, dips, and assemblies this equals the sum of ingredient masses; for mass-loss recipes see below).
   c. For each nutrient slug, sum `(per_100g_value × ingredient_grams / 100)` across the sub-recipe's ingredients = total of that nutrient in one batch.
   d. Per-100g of the sub-recipe = `(total_in_batch × 100) / batch_mass`.
   e. Apply the same per-100g **inclusion thresholds** that gate any ingredient cell (see `### Canonical units and inclusion thresholds per nutrient`); only include nutrients above their inclusion threshold; round per the cell content rules in `### `ingredients-info.md` schema`.

**Sort key.** The row's alphabetical position is determined by the link text in lowercase, ignoring `[...](...)` punctuation. `[Maple Dijon Dressing](...)` sorts at `maple dijon dressing`.

**Lookup matching.** When a parent-recipe agent encounters a sub-recipe ingredient, it computes the canonical name (e.g., `maple dijon dressing`) and matches against the link text in `ingredients-info.md`'s Ingredient column (case-insensitive, ignoring Markdown link syntax). Once matched, the four cells provide the per-100g profile, and the standard `(value × grams / 100)` math propagates the sub-recipe's nutrients to the parent. **No special-casing beyond the link-text match** — at consumption time, a sub-recipe is just another ingredient with a per-100g profile.

**Mass conversion when a parent recipe uses a sub-recipe:**

- "1 batch &lt;Sub-recipe Title&gt;" → grams = the sub-recipe's batch mass (computed in step b above). Consult the sub-recipe page's metadata blockquote `Yield:` field if it states a finished mass; otherwise sum the ingredient masses directly.
- "1 tbsp / 1 tsp / 1 cup &lt;Sub-recipe Title&gt;" → standard `### Quantity → grams conversion` using the sub-recipe's bulk-density family (dressings/sauces ~15g/tbsp · 240g/cup; dry seasoning blends ~6g/tbsp · 80g/cup; dips/spreads ~15g/tbsp · 240g/cup; granola ~30g per ¼ cup; ice cream ~130g/cup). When ambiguous, prefer the closest culinary analogue and note the assumption in the sub-recipe's `## Notes`.
- "to taste" or "—" quantity → 0g contribution, exactly as for raw ingredients.

**Recursion (sub-recipes that use sub-recipes).** Sub-recipes can reference further sub-recipes (e.g., a dressing that calls for hummus). Process **leaf sub-recipes first** so the inner sub-recipe's row is populated before the outer one is computed. Two-level recursion is the practical limit observed in v1; deeper chains require explicit user surfacing.

**Mass-loss sub-recipes.** For sub-recipes where the produced batch mass differs materially from the raw-ingredient sum (typically baked goods that lose 15–25% to evaporation, or reductions/concentrates), use the **finished batch mass** in step (b), not the raw ingredient sum. State the assumed finished mass in the sub-recipe's own `## Notes` so future runs can verify. For sauces, seasonings, dressings, dips, granola, and most assemblies, the raw-sum mass is fine.

**Updating sub-recipe rows.** When a sub-recipe's `## Ingredients` table changes, its row in `ingredients-info.md` must be recomputed and the per-100g profile updated. Then every parent recipe that uses it must be re-derived. The audit subsection `### 5.15 Sub-recipe profile validity` exists to catch drift.

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

- Bullet shape: `- [<Bullet Link Text>](cooking/<group>/<slug>.md) — <amount><unit>`.
- Separator: ` — ` (single space, em-dash U+2014, single space). Not a hyphen-minus, not an en-dash.
- **Bullet link text is the humanized slug** (Title Case, hyphens → spaces, B-vitamins keep their digit, **`omega-3` carve-out: hyphen-digit suffix RETAINED — `Omega-3`, NOT `Omega 3`**) — NOT necessarily the full lexicon `Category` display name. For 26 of the 27 v1 entries the two are identical (e.g., `Vitamin B12`, `Healthy Fats`, `Iron`). The one exception is **Omega-3**: the lexicon Category is `Omega-3 (EPA/DHA)` and `ingredients-info.md` cells use that full form (`Omega-3 (EPA/DHA) (200mg/100g)`), but the recipe-page bullet drops the parenthetical so the link text matches the slug's H1: `- [Omega-3](cooking/soft-essentials/omega-3.md) — 200mg`. Slug derivation always strips parentheticals; this rule keeps the bullet text aligned with the slug page's H1.
- No space between number and unit: `28g`, not `28 g`. This matches the convention used in `ingredients-info.md` cell amounts.
- Amount unit is the canonical unit for that nutrient from `### Canonical units and inclusion thresholds per nutrient` (the same unit used in every `ingredients-info.md` cell for that nutrient). Summation across ingredients is therefore a straight numeric add — no unit conversion ever appears in the agent's workflow. Quick reference: `g` for macros and Dietary Fiber; `mg` or `µg` for minerals and vitamins per the canonical-unit table; `mg` for Omega-3.
- **Threshold drop FIRST, then rounding.** Compute the unrounded recipe-level sum for each nutrient. If the sum is **below the per-nutrient recipe drop threshold** in `### Canonical units and inclusion thresholds per nutrient` (the `Recipe drop threshold` column — NOT the looser `Inclusion threshold` that gates `ingredients-info.md` cells), drop the bullet entirely — do not render. If the sum is at or above the recipe drop threshold, apply the rounding rules below to the sum and render the rounded value. The recipe drop threshold is the single arbiter of "is this enough to list on a recipe page"; the rounding rules only apply to values that already passed it.
- **Rounding** (apply by magnitude band of the *value*, regardless of unit; bands are half-open at the upper end so a value of exactly 10 falls into `[10, 100)`, not `[1, 10)`):
  - `[0, 1)` (e.g., `0.7µg`): one decimal place. (A value here only renders if its threshold is sub-1; e.g., Vitamin B12 threshold `0.1µg` → `0.7µg` renders.)
  - `[1, 10)` (e.g., `1.8mg`, `1.4µg`, `3µg`): one decimal place; drop a trailing `.0` (so `3.0µg` → `3µg`, but `1.4µg` stays `1.4µg`).
  - `[10, 100)` (e.g., `45µg`, `28mg`): integer.
  - `[100, 1000)` (e.g., `270mg`, `370µg`, `480µg`): nearest 10.
  - `[1000, 5000)` (e.g., `2400mg`): nearest 50.
  - `[5000, ∞)`: nearest 100.
  - **Macros and Dietary Fiber override:** always reported in `g`, always integer (round half-up at every magnitude — no band rounding). So `1.4g` → `1g`, `19.6g` → `20g`, `28.3g` → `28g`, `245.4g` → `245g` (NOT `250g`). The recipe drop threshold for these four (`Complex Carbs`, `Healthy Fats`, `Protein`, `Dietary Fiber`) is `1g`, so any unrounded sum `< 1g` is dropped at the threshold step above before rounding ever runs.
  - Vitamin B12 typical amounts are sub-µg to a few µg — threshold is `0.1µg`, so any sum at or above `0.1µg` renders. Render with one decimal place per the band rule. For values in `[1, 10)`, drop a trailing `.0` (so `2.0µg → 2µg`). For values in `[0, 1)`, the leading `0.` is kept (so `0.7µg`, NOT `7µg`).
  - Vitamin D is always reported in `µg` (the unit used in `## Nutrient lexicons`), never `IU`. The IU form shown in the lexicon's Requirement column is informational only; recipe-page bullets and `ingredients-info.md` cells use `µg`.
- **Qualitative entries** (`Phytochemicals`, `Probiotics`) carry NO amount and NO ` — ` separator: `- [Phytochemicals](cooking/soft-essentials/phytochemicals.md)`. They are present on the recipe page whenever **at least one** ingredient lists them in its `ingredients-info.md` cell — there is no per-recipe "amount" to compare, so the threshold rule below does NOT apply to qualitative entries.
- **Bullet inclusion threshold (quantitative entries only):** drop any bullet whose **unrounded** recipe-level total is below the per-nutrient **recipe drop threshold** in `### Canonical units and inclusion thresholds per nutrient` (the stricter of the two thresholds — the looser inclusion threshold gates ingredient-cell content, not recipe-page bullets). The recipe drop threshold is the single arbiter; "rounds to 0" is no longer used as a separate trigger. Examples: Vitamin C recipe drop threshold `5mg` — a recipe with summed `3mg` Vitamin C drops the bullet; with summed `7mg` renders `7mg`. Calcium recipe drop threshold `50mg` — `40mg` drops, `60mg` renders. Macros and fiber recipe drop threshold `1g` — `0.7g` of Protein drops (not rendered as `1g`); `1.4g` renders as `1g`. This rule applies ONLY to quantitative nutrients; qualitative entries (Phytochemicals, Probiotics) are governed by the rule above. If no bullets remain in a group after applying both rules, omit the section heading entirely.
- **Within-section sort:** alphabetical by display name, case-insensitive, with B-vitamins by numeric value.

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

- [Banana Bread](cooking/recipes/banana-bread.md)
- [Classic French Omelette](cooking/recipes/classic-french-omelette.md)
...
```

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

Each nutrient bullet shows the recipe-level rounded total amount in the format `- [<Display Name>](cooking/<group>/<slug>.md) — <amount><unit>` (see `### Recipe-page rendering` for full format and rounding rules). Qualitative entries (`Phytochemicals`, `Probiotics`) carry no ` — <amount>` suffix.

Section order is fixed: `Ingredients` → `Preparation` → `Notes` → `Categories` → `Traits` → `Books` → `Macronutrients` → `Minerals` → `Vitamins` → `Soft Essentials`. Sections that are empty:

- `## Notes` — omit if no notes are available.
- `## Traits` — omit entirely if the recipe has zero traits.
- `## Macronutrients`, `## Minerals`, `## Vitamins`, `## Soft Essentials` — each section is omitted entirely (heading + bullet list both gone) when its derived list is empty. The four sections are *ingredient-derived* via the lookup-extend protocol in `## Ingredient → nutrient mapping`; in practice macronutrients/minerals/vitamins almost always have ≥1 entry; soft-essentials often won't.
- `## Categories` and `## Books` are always present (every recipe has ≥1 of each).

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

- [Banana Bread](cooking/recipes/banana-bread.md)
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

The body shape: H1 → back-link → the **verbatim canonical table** copied byte-for-byte from `## Nutrient lexicons` (4 columns, alphabetical rows, `Category` cells are Markdown links of the form `[Display Name](cooking/<group>/<slug>.md)`, `—` for empty cells, `†` for AIs) → the source-note blockquote (also copied verbatim from `## Nutrient lexicons`). The table itself is frozen (see "Frozen-table rule" under `## Anti-drift rules`). **No bullet list follows the table** — the linked Category cells are the only navigation path to the individual row pages.

### `docs/cooking/minerals/README.md`, `docs/cooking/vitamins/README.md`, `docs/cooking/soft-essentials/README.md`

Structurally identical to `macronutrients/README.md` — H1 (`# Minerals` / `# Vitamins` / `# Soft Essentials`), back-link to Cooking, and the verbatim canonical table for that group from `## Nutrient lexicons` (with linked Category cells), followed by the source-note blockquote. For v1 the tables contain exactly 7 / 13 / 4 rows respectively.

### `docs/cooking/macronutrients/<slug>.md` (and analogous for minerals, vitamins, soft-essentials)

```markdown
# Protein

Back to [Macronutrients](cooking/macronutrients/README.md)

- [Apple Chickpea Salad](cooking/recipes/apple-chickpea-salad.md)
- [Classic French Omelette](cooking/recipes/classic-french-omelette.md)
...
```

H1 is humanized from the slug (Title Case, hyphens → spaces, with one carve-out for `omega-3`). Worked examples covering all 27 v1 slugs:

- Macronutrients: `complex-carbs` → `Complex Carbs`, `healthy-fats` → `Healthy Fats`, `protein` → `Protein`.
- Minerals: `calcium` → `Calcium`, `iodine` → `Iodine`, `iron` → `Iron`, `magnesium` → `Magnesium`, `potassium` → `Potassium`, `selenium` → `Selenium`, `zinc` → `Zinc`.
- Vitamins: `vitamin-a` → `Vitamin A`, `vitamin-b1` → `Vitamin B1`, … `vitamin-b12` → `Vitamin B12` (hyphen between `vitamin` and `b12` becomes a space, B-vitamin digit kept), `vitamin-c` → `Vitamin C`, …, `vitamin-k` → `Vitamin K`.
- Soft Essentials: `dietary-fiber` → `Dietary Fiber`, `phytochemicals` → `Phytochemicals`, `probiotics` → `Probiotics`, **`omega-3` → `Omega-3` (carve-out — the hyphen-digit suffix is RETAINED, not converted to a space; `Omega 3` is wrong).** This matches the conventional written form of the term and aligns with the recipe-page bullet link text rule under `### Recipe-page rendering`.

Back-link points to the parent group's README. Bullet list is every recipe whose `## Macronutrients` (or `## Minerals` / `## Vitamins` / `## Soft Essentials`) section contains this slug, alphabetical. Empty list when no recipes yet reference the slug — the file still exists with just the H1 and back-link.

### `docs/cooking/ingredients-info.md`

```markdown
# Ingredients Info

Back to [Cooking](cooking/README.md)

Authoritative ingredient → nutrient lookup. Alphabetical by ingredient (canonical name; see `## Ingredient → nutrient mapping` for the normalization rules). Cells contain entries from `## Nutrient lexicons` using the EXACT `Category` column display name, each followed by a per-100g amount estimate in parentheses (`Display Name (Xunit/100g)`). `Phytochemicals` and `Probiotics` are qualitative — bare display name with no amount. An en-dash (`—`) marks an empty cell. New ingredients are appended in alphabetical position; existing rows are not deleted.

| Ingredient | Macronutrients | Minerals | Vitamins | Soft Essentials |
|---|---|---|---|---|
| almonds | Healthy Fats (50g/100g), Protein (21g/100g) | Calcium (270mg/100g), Magnesium (270mg/100g) | Vitamin E (26mg/100g) | Dietary Fiber (12g/100g) |
| olive oil | Healthy Fats (100g/100g) | — | Vitamin E (14mg/100g), Vitamin K (60µg/100g) | — |
| spinach | — | Iron (2.7mg/100g), Magnesium (80mg/100g), Potassium (560mg/100g) | Vitamin A (470µg/100g), Vitamin B9 (190µg/100g), Vitamin C (28mg/100g), Vitamin K (480µg/100g) | Dietary Fiber (2g/100g), Phytochemicals |
```

Five columns, exactly. Cells use the canonical display name from `## Nutrient lexicons` (NOT the slug, NOT a plural, NOT a free-text variant) plus a per-100g amount in parentheses. Entries sorted alphabetically inside each cell (B-vitamins by numeric value: `Vitamin B1, Vitamin B2, …, Vitamin B9, Vitamin B12`). The file is append-only (see "Ingredient-info append-only rule" under `## Anti-drift rules`).

## Sidebar shape

Add the following block to `docs/_sidebar.md` under a top-level `**Cooking**` group. The sidebar uses two enumerated subgroups (`**Recipes**` and `**Books**`) — every recipe and every book is a direct sidebar link. Categories, traits, and the four nutrient axes are NOT enumerated; their index pages serve as the entry points.

```markdown
- **Cooking**
  - **Recipes**
    - [All Recipes](cooking/recipes/README.md)
    - [<Recipe Name>](cooking/recipes/<recipe-slug>.md)
    - [<Recipe Name>](cooking/recipes/<recipe-slug>.md)
    - ... (every recipe, alphabetical by display name per the standard sort key)
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

- **In-corpus**: `[<Recipe Name>](cooking/recipes/<slug>.md)` — absolute path from the docs root, per the link path convention.
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

1. For each ingredient, compute (a) the canonical name per the normalization rules and (b) the mass in grams via `### Quantity → grams conversion`. Skip 0g entries.
2. Look up the canonical name in `docs/cooking/ingredients-info.md`. If absent, append a new alphabetical row with the four nutrient cells filled from established nutritional knowledge.
3. For each entry in the ingredient's four cells, multiply the per-100g amount by `mass_g / 100` and add to the recipe-level running total for that display name (per group). Qualitative entries (`Phytochemicals`, `Probiotics`) are recorded as presence with no amount.
4. After all ingredients are processed:
   - **Quantitative entries (all 25 quantitative slugs — macros, fiber, minerals, vitamins, Omega-3):** for each, compare the summed **unrounded** total against the per-nutrient **recipe drop threshold** in `### Canonical units and inclusion thresholds per nutrient`. If below the recipe drop threshold, drop the bullet. If at or above, round per `### Recipe-page rendering` and render. The recipe drop threshold is the single arbiter — there is no separate "rounds to 0" rule and no separate macro/fiber floor test (macros and fiber recipe drop thresholds are `1g`, applied via the same threshold check as every other slug). The looser inclusion threshold (per-100g ingredient gate) does NOT apply at this stage.
   - **Qualitative entries** (`Phytochemicals`, `Probiotics`): keep them whenever ≥1 ingredient listed them. They have no summed total and the threshold rule does NOT apply to them.
   - Convert each remaining display name to its slug via the **Display name → slug mapping** (used both for the tracker and for the bullet links).
   - Alphabetize within each group (B-vitamins by numeric value).

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
6. **`macronutrients/<slug>.md`** — for each macronutrient slug referenced by any new recipe, insert the recipe link (just `[<Recipe Name>](cooking/recipes/<slug>.md)`, no per-recipe amount) in alphabetical position. The 27 nutrient row files (`<group>/<slug>.md`) were created during the v1 setup of the cooking section and pre-exist on every cookbook run; agents normally only append to the bullet list of recipes that reference each slug. **Create-if-missing fallback:** if a v1 row file is somehow absent (e.g., partial setup, accidental deletion), recreate it from the row-page template under `## Page templates` (H1 = humanized slug, back-link to the group README, then the recipe bullet). Humanization is Title Case with hyphens → spaces, **except** `omega-3` → `Omega-3` (hyphen-digit suffix retained, NOT `Omega 3`). Other examples: `complex-carbs` → `Complex Carbs`, `vitamin-b12` → `Vitamin B12`, `dietary-fiber` → `Dietary Fiber`, `iron` → `Iron`. The full slug-to-H1 list is given under `### docs/cooking/macronutrients/<slug>.md (and analogous for minerals, vitamins, soft-essentials)` in `## Page templates`. Do NOT add a canonical table to the row file — the frozen canonical tables live exclusively in the four group `<group>/README.md` files (see the "Frozen-table rule" under `## Anti-drift rules`).
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

Concrete check: for each recipe `R` and each category `C` listed on it, `grep "cooking/recipes/R.md" docs/cooking/categories/C.md` must succeed.

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

# Index entries with no backing file (links are absolute from docs/, e.g. cooking/recipes/foo.md)
for d in docs/cooking/recipes docs/cooking/categories docs/cooking/traits docs/cooking/books; do
  rg -o '\[[^]]+\]\(([^)]+\.md)\)' $d/README.md -r '$1' | while read link; do
    [ -f "docs/$link" ] || echo "DEAD link in $d/README.md: $link"
  done
done
```

### 5.6 Link resolution

Every Markdown link inside `docs/cooking/**` resolves to an existing file. Links must be absolute from the docs root (start with `cooking/`). Per the link path convention, any link target containing `../`, starting with `./`, or being a bare filename is a defect — flag it.

```bash
# Find any link that violates the absolute-from-docs-root rule
rg -n '\]\((?:\.\./|\./|[a-z][^/)]*\.md\))' docs/cooking/ && echo "FOUND non-absolute link(s)"

# Verify every link target resolves
rg -o '\]\((cooking/[^)]+\.md)\)' docs/cooking/ -r '$1' --no-filename | sort -u | while read link; do
  [ -f "docs/$link" ] || echo "DEAD link target: $link"
done
```

Agents do this per-file: for each recipe / category / trait / book page, enumerate every link target and `test -f docs/$target` the resolved path.

### 5.7 Alphabetical order

Every list that should be alphabetical is alphabetical per the sort key in "Anti-drift rules". Includes: every `README.md`'s bullet list, every category/trait/book page's recipe list, and every recipe page's `## Categories`, `## Traits`, `## Books` sections.

### 5.8 Back-link presence

Every page under `docs/cooking/**` carries a "Back to ..." line with the exact prescribed wording from the back-link table, immediately under the H1, blank-line separated above and below. Recipe pages back-link to `[All Recipes](cooking/recipes/README.md)` (the back-link line sits between the H1 and the metadata blockquote, with one blank line on each side).

### 5.9 Metadata / template conformance

Every recipe page:

- Has H1 followed by a blank line.
- Has the metadata blockquote in the canonical field order using ` · ` separators. The blockquote is required whenever the source provides ≥1 of the canonical fields (Prep, Cook, Total, Yield, Cost, Equipment); when the source provides none, the blockquote may be omitted entirely (rare — most cookbook recipes provide at least Yield).
- Has section headers in the canonical order: `Ingredients`, `Preparation`, optional `Notes`, `Categories`, optional `Traits`, `Books`, optional `Macronutrients`, optional `Minerals`, optional `Vitamins`, optional `Soft Essentials`. The four nutrient sections, when present, appear in that fixed order after `Books`.
- Has a two-column ingredient table — never three columns.
- Uses Unicode fractions in the Quantity column, not ASCII (`½` not `1/2`) — match existing files.

### 5.10 Frozen-table integrity

The four group `README.md` tables (`macronutrients/README.md`, `minerals/README.md`, `vitamins/README.md`, `soft-essentials/README.md`) are byte-identical to the canonical copies in this SKILL's `## Nutrient lexicons` (modulo whitespace within a cell). The `Category` cells are Markdown links of the form `[Display Name](cooking/<group>/<slug>.md)`; an unlinked Category cell is a drift defect and fails the audit. Any drift must be restored from this SKILL — agents do not touch the table content, column order, or the link target.

### 5.11 Nutrient bidirectional integrity

For every entry in a recipe's `## Macronutrients`, the recipe link appears in `cooking/macronutrients/<slug>.md`. Same for minerals, vitamins, soft-essentials. And vice-versa: every recipe link in a nutrient row file corresponds to an entry on that recipe's nutrient section.

Concrete check for each recipe `R` and each nutrient slug `N` listed on it: `grep "cooking/recipes/R.md" docs/cooking/<group>/N.md` must succeed.

### 5.12 Ingredient-info coverage

Every ingredient in every recipe under `docs/cooking/recipes/` appears as a row in `docs/cooking/ingredients-info.md` under its canonical name. Surface unmatched ingredients; do not silently fix — the agent must add the row with a real nutrient profile (per the lookup-extend protocol). New rows go in alphabetical position; existing rows are not deleted.

### 5.13 Nutrient-derivation correctness

For each recipe, recompute the four nutrient sets and their per-recipe totals: walk its `## Ingredients`, convert each quantity to grams via `### Quantity → grams conversion` (skip 0g-mass entries — `to taste`, `for serving`, etc., per the Special quantities list), look each remaining ingredient up in `ingredients-info.md`, multiply each per-100g amount by `mass_g / 100`, and sum per nutrient. Then confirm:

- The recipe page's `## Macronutrients` / `## Minerals` / `## Vitamins` / `## Soft Essentials` sections list the same quantitative nutrients (deduped, alphabetical, B-vitamins by numeric value, with empty sections and below-threshold quantitative bullets omitted). **Qualitative entries** (`Phytochemicals`, `Probiotics`) are governed by presence, NOT by any threshold: a qualitative bullet is correct iff ≥1 ingredient lists it in `ingredients-info.md`.
- **Threshold check (HARD CLIFF — applies BEFORE the tolerance check):** for every quantitative slug, compare the recomputed **unrounded** total against the per-nutrient **recipe drop threshold** in `### Canonical units and inclusion thresholds per nutrient`. If the recipe page DROPPED a quantitative bullet, the recomputed unrounded total must be **below** the recipe drop threshold. If the recipe page RENDERS a quantitative bullet, the recomputed unrounded total must be **at or above** the recipe drop threshold. The recipe drop threshold is a hard boundary that wins over the ±20% / ±1-step tolerance: a printed `Vitamin C — 6mg` bullet for a recomputed unrounded `4.5mg` (recipe drop threshold 5mg) is a defect even though `4.5mg` is within ±20% of `6mg`; a dropped Vitamin C bullet for a recomputed unrounded `5.5mg` is also a defect. The same applies to macros (printed `1g` Protein for recomputed `0.95g` is a defect — recipe drop threshold is 1g) and to every other slug. The two thresholds work in series: the (looser) inclusion threshold gates `ingredients-info.md` cell entries (audited under 5.14), and the (stricter) recipe drop threshold gates recipe-page bullets (audited here under 5.13).
- **Tolerance check (applies only to bullets that pass the threshold check):** each rendered bullet's printed amount matches the recomputed total within **±20% or ±1 step of the rounding granularity, whichever is greater**. "Rounding granularity" means the rounding step from the band that applies in `### Recipe-page rendering` — e.g., for a value in `[100, 1000)` rounded to the nearest 10, the granularity is 10, so `370µg` is acceptable for a recomputed `360µg` or `380µg`. **For macros and Dietary Fiber the granularity is `1g` (plain-integer rendering, no band)**, and the ±20% rule typically dominates: `28g` is acceptable for a recomputed range of `~22g–~34g`.
- Larger discrepancies and gross errors (wrong unit, missing factor of 10, qualitative-vs-quantitative confusion) still fail.
- Qualitative bullets (`Phytochemicals`, `Probiotics`) carry NO ` — <amount>` suffix; including one is a defect.

Discrepancies fail the audit.

### 5.14 Slug / display-name / amount-format validity

Every slug appearing in any recipe nutrient section bullet link, or in any nutrient row file, exists in the v1 lexicon (the 27 slugs listed in `## Nutrient lexicons`). No invented slugs, no `b-complex`, no aliases, no plurals.

For `ingredients-info.md` cells specifically: every entry uses the EXACT `Category` column display name from `## Nutrient lexicons` (e.g., `Vitamin B12`, `Omega-3 (EPA/DHA)`), followed by `(Xunit/100g)` for quantifiable nutrients or no amount for `Phytochemicals` / `Probiotics`. Slug-form entries (`vitamin-b12`, `omega-3`) inside a cell are a defect — they must be re-rendered as the display name with the amount appended.

**Canonical-unit consistency**: every `(<value><unit>/100g)` cell amount uses the canonical unit for that nutrient from `### Canonical units and inclusion thresholds per nutrient`. Defects: `Vitamin A (0.47mg/100g)` (canonical unit is `µg` — must be `Vitamin A (470µg/100g)`); `Iron (2700µg/100g)` (canonical unit is `mg` — must be `Iron (2.7mg/100g)`); `Vitamin D (200 IU/100g)` (must be `µg`). Fix by re-expressing the amount in the canonical unit before any summation runs. The same canonical unit also applies to recipe-page bullet amounts — a recipe-page bullet rendering `Vitamin A — 0.5mg` instead of `Vitamin A — 500µg` is the same defect class.

**Per-100g `inclusion threshold` compliance for `ingredients-info.md` cells:** the audit uses the **inclusion threshold** column (the looser of the two — roughly 1% of RDA per 100g, or recipe drop threshold ÷ 5), NOT the recipe drop threshold. For every `(<value><unit>/100g)` cell entry, the value MUST be at or above the inclusion threshold. Defects:

- **Below-inclusion-threshold entry present:** e.g., a row listing `Vitamin C (0.5mg/100g)` (inclusion threshold `1mg`) — true-trace level, must be REMOVED (no plausible recipe quantity would surface it). Fix by deleting the entry from the cell.
- **Above-inclusion-threshold nutrient absent:** if established USDA per-100g data shows an ingredient has a nutrient at or above the inclusion threshold, the row MUST list it. Concrete cases the previous (single-threshold) audit incorrectly trimmed and that the inclusion-threshold audit MUST restore: `apple` Vitamin C ~4.6mg/100g (above 1mg inclusion threshold), `pear` Vitamin C ~4.3mg/100g, `sweet potato` Vitamin C ~2.4mg/100g, `peach` Vitamin A ~16µg/100g (above 10µg inclusion threshold), `pumpkin` Dietary Fiber ~0.5g/100g (above 0.2g inclusion threshold). Missing entries — even when the agent considered the per-recipe contribution unlikely to surface — are defects under the no-preemptive-recipe-quantity-assumption rule. Fix by adding the entry.

**Important: do NOT apply the recipe drop threshold here.** A common defect class is to filter ingredient cells against the recipe drop threshold (e.g., dropping `apple Vitamin C (4.6mg/100g)` because it is below the 5mg recipe drop threshold). This is wrong: the recipe drop threshold gates the per-recipe SUM (apple at 1kg in a recipe yields ~46mg → above 5mg → renders), not the per-100g entry. Use the inclusion threshold column for ingredient-cell decisions.

The audit cross-checks each ingredient row against established USDA per-100g profiles and the inclusion-threshold column to flag both kinds of defect. Agents do NOT make ad-hoc trace-amount decisions.

**Per-recipe threshold compliance for recipe-page bullets:** see `### 5.13 Nutrient-derivation correctness` — recipe-page bullets that fall below the **recipe drop threshold** (or are dropped while above it) are flagged there, since the check requires recomputing the per-recipe sum.

### 5.15 Sub-recipe profile validity

For every sub-recipe used as an ingredient anywhere in `docs/cooking/recipes/`, confirm:

- A row exists in `docs/cooking/ingredients-info.md` whose Ingredient column is a Markdown link to the sub-recipe's recipe page (`| [<Title>](cooking/recipes/<slug>.md) | … |`) — not a plain canonical-name string.
- The four nutrient cells follow the per-100g convention defined in `### Sub-recipe ingredients`. Recompute the per-100g profile from the sub-recipe's `## Ingredients` table (steps a–d in that section) and verify each surfaced display name's amount matches within ~10% rounding tolerance. Missing nutrients above the inclusion threshold or surfaced nutrients below it are defects.
- Cross-check by walking parent recipes that use the sub-recipe: their derived nutrient sections must include the sub-recipe's per-100g contribution. A parent recipe whose sums silently exclude a sub-recipe's nutrients is the canonical pre-v1 defect this audit is designed to catch.

To enumerate sub-recipes used as ingredients, scan every recipe's `## Ingredients` table for substrings matching another recipe's H1 title (case-insensitive). The set is closed: a recipe is a sub-recipe iff at least one other recipe lists it as an ingredient. Build-your-own / template recipes (e.g., `guzinta-bowl-guide`, `toast-is-the-most`) reference sub-recipes only inside `—`-quantity rows, so those parents contribute no real consumption — sub-recipe rows still exist, but parent re-derivation is a no-op there.

Discrepancies fail the audit. Restore by recomputing the sub-recipe's per-100g profile, updating its row, and re-deriving every parent recipe that uses it.

For recipe-page nutrient bullets specifically: every bullet matches `- [<Display Name>](cooking/<group>/<slug>.md) — <amount><unit>` for quantitative nutrients, or `- [<Display Name>](cooking/<group>/<slug>.md)` for qualitative `Phytochemicals` / `Probiotics`. Defects:

- Missing the ` — <amount><unit>` suffix on a quantitative bullet.
- Including ` — <amount>` on `Phytochemicals` or `Probiotics`.
- Using a hyphen-minus or en-dash instead of em-dash (` — ` is `space U+2014 space`).
- Adding a space between the number and the unit (`28 g` is wrong; `28g` is correct).
- Display name in slug form (`vitamin-b12` instead of `Vitamin B12`) or in plural / free-text variant.

### Audit reports

Audit agents report under 50 words, one line per recipe:

- `<slug>: CLEAN`
- `<slug>: N fixes — <terse phrase per fix>` (e.g., `chocolate-pots: 2 fixes — renamed (3-ingredient stripped), added breakfast category`)

No recaps, no diffs. The fix is in the file; the report is the ledger.

### Convergence

Repeat audit rounds until every recipe reports clean on first iteration of a round, or max 5 outer rounds. At max iterations with remaining issues, stop and surface to the user — do not silently accept flawed output.

**Compact checkpoint**: after Phase 5 converges, proactively `/compact` before Phase 6.

## Phase 6: Finalize

1. Update `docs/_sidebar.md` per the Sidebar shape section. If the `**Cooking**` block already exists: (a) insert each new recipe into the `**Recipes**` subgroup in alphabetical position (preserving the leading `[All Recipes]` entry), (b) ensure all four nutrient indexes and `[Ingredients Info]` are listed, and (c) add the new book to `**Books**` in alphabetical position.
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
- **Lexicon expansion without explicit user approval.** The four nutrient lexicons (3 macronutrients, 7 minerals, 13 vitamins, 4 soft-essentials = 27 slugs) are **closed at v1**, mirroring the trait lexicon's closed status. The standard "lexicon-first rule" applies: agents do not invent rows, do not add columns, do not rename slugs, and do not silently fix table content. Unmapped concepts are surfaced to the user in the Phase 2.8 / Phase 6 completion report.
