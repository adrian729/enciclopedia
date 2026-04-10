---
name: docsify
description: Docsify conventions for this project. Use when editing docs/ files (index.html, _sidebar.md, _coverpage.md, _navbar.md) or adding new pages.
---

# Docsify

## Project setup

- Docs root: `docs/`
- Entry: `docs/index.html` (Docsify v4, `vue.css` theme)
- Homepage: `docs/README.md`
- Sidebar: `docs/_sidebar.md` (manual, `loadSidebar: true`)
- `.nojekyll` required for GitHub Pages (files starting with `_`)

## Routing

Hash-based (`/#/`). File mapping:

```
docs/README.md       => /#/
docs/guide.md        => /#/guide
docs/sub/README.md   => /#/sub/
docs/sub/page.md     => /#/sub/page
```

## Sidebar (`_sidebar.md`)

- Markdown list of links. Nesting via indentation.
- Section headers are bold unlinked items.
- Format:

```markdown
- **Section Name**
  - [Page Title](filename.md)
  - [Sub Section](sub/page.md)

- **Another Section**
  - [Topic](topic.md)
```

- Links are relative to `docs/`.
- `subMaxLevel: 0` — sidebar auto-TOC is disabled; all sidebar navigation is manual.
- Nested sidebars: a `_sidebar.md` in a subdirectory overrides the root one for that path. Falls back to parent if absent.

## Adding pages

1. Create `docs/page_name.md`.
2. Add entry to `docs/_sidebar.md`.
3. Link between pages with relative paths: `[text](other_page.md)`.

## Plugins

- **search** — full-text search, loaded via separate `<script>` tag.
- **fixHeadingIds** — custom inline plugin that strips the `_` prefix docsify adds to heading IDs starting with a digit (e.g. `_1-section` → `1-section`), and patches sidebar links to match.

## Configuration reference (`window.$docsify`)

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
| `plugins` | Array | - | Inline plugin functions |
