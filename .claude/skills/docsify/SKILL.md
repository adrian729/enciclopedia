---
name: docsify
description: Docsify conventions for this project. Use when editing docs/ files (index.html, _sidebar.md) or adding/linking pages.
---

# Docsify

## Project setup

- Docs root: `docs/`
- Entry: `docs/index.html` (Docsify v4, `vue.css` theme)
- Homepage: `docs/README.md`
- Sidebar: `docs/_sidebar.md` (manual, `loadSidebar: true`)
- `.nojekyll` required for GitHub Pages (files starting with `_`)
- Live config: `loadSidebar: true`, `auto2top: true`, `subMaxLevel: 0`, `sidebarDisplayLevel: 1`, two custom inline plugins (`fixHeadingIds`, `katexMath`). No navbar, no coverpage.

## Routing

Hash-based (`/#/`). File mapping:

```
docs/README.md       => /#/
docs/guide.md        => /#/guide
docs/sub/README.md   => /#/sub/
docs/sub/page.md     => /#/sub/page
```

## Links

- Every `.md` link target is **root-relative to `docs/`**: `[text](software/procedural/foundations.md)`, `[text](cooking/recipes/banana-bread.md)` — even when the target is a sibling of the current page.
- The project keeps Docsify's default `relativePath: false`, so targets resolve from the docs root regardless of which page contains the link. `./`, `../`, and bare sibling filenames inside subdirectories are defects.
- Cross-page anchors use the docsify slug with the `_` digit-prefix stripped (see fixHeadingIds below): `page.md#11-my-title`.
- Verify: `python3 scripts/check_docs.py <paths>` confirms every link target and anchor resolves.

## Sidebar (`_sidebar.md`)

- Markdown list of links. Nesting via indentation.
- Section headers: bold unlinked items.
- Format:

```markdown
- **Section Name**
  - [Page Title](filename.md)
  - [Sub Section](sub/page.md)

- **Another Section**
  - [Topic](topic.md)
```

- Links relative to `docs/`.
- `subMaxLevel: 0` — auto-TOC disabled; all navigation is manual.
- `sidebarDisplayLevel: 1` — nested items collapsed by default (click to expand). Uses `docsify-sidebar-collapse` plugin.
- Nested sidebars: `_sidebar.md` in a subdirectory overrides root for that path. Falls back to parent if absent.

## Adding pages

1. Create `docs/page_name.md`.
2. Add entry to `docs/_sidebar.md`.
3. Link between pages with paths root-relative to `docs/` (see Links above).

## Plugins

- **search** — full-text search, loaded via `<script>` tag.
- **docsify-sidebar-collapse** — collapses nested sidebar items by default. Controlled by `sidebarDisplayLevel`. External CSS + JS from CDN.
- **fixHeadingIds** — custom inline plugin; strips the `_` prefix docsify adds to heading IDs starting with a digit, patches sidebar links to match, and fixes click/load scrolling for digit-leading IDs (`querySelector('#1-xxx')` is invalid CSS). Needed because the project uses numbered headings with digit-prefixed IDs. See `md-standards` for heading ID convention.
- **katexMath** — custom inline plugin; extracts `\( \)` (inline) and `\[ \]` (display) math from the RAW markdown in `beforeEach` — before marked can eat backslashes or mangle underscores — and injects `katex.renderToString` output in `afterEach`. KaTeX CSS + JS pinned at `0.16.11` from CDN. Consequences: math MUST use `\( \)` / `\[ \]`, never `$` (many docs lines use `$` as currency), and `\(`/`\[` must never appear inside code fences (extraction sees raw markdown, fences included). Verify with `node scripts/check_katex.mjs` — it renders every snippet with the index.html-pinned KaTeX version.

## Configuration (`window.$docsify`)

| Option | Type | Default | Purpose |
|---|---|---|---|
| `name` | String | - | Site name in sidebar |
| `loadSidebar` | Bool/String | `false` | Load `_sidebar.md` |
| `loadNavbar` | Bool/String | `false` | Load `_navbar.md` |
| `subMaxLevel` | Number | `0` | Auto-TOC depth from headings |
| `maxLevel` | Number | `6` | Max heading level in auto sidebar |
| `coverpage` | Bool/String | `false` | Load `_coverpage.md` |
| `auto2top` | Boolean | `false` | Scroll to top on navigation |
| `homepage` | String | `README.md` | Landing page file |
| `relativePath` | Boolean | `false` | Resolve links relative to current file |
| `search` | Object | - | Full-text search plugin config |
| `repo` | String | - | GitHub corner widget |
| `routerMode` | String | `hash` | `hash` or `history` |
| `alias` | Object | - | Route aliases (regex supported) |
| `notFoundPage` | Bool/String | `false` | Custom 404 page |
| `sidebarDisplayLevel` | Number | — | Initial sidebar nesting depth (collapse plugin option; this project sets `1`) |
| `plugins` | Array | - | Inline plugin functions |
