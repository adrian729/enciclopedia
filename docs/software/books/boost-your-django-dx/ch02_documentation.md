# Ch 2: Documentation

## Table of Contents

- [1. Searching docs faster](#1-searching-docs-faster)
  - [1.1. DevDocs](#11-devdocs)
  - [1.2. DuckDuckGo](#12-duckduckgo)
- [2. Curated Django reference sites](#2-curated-django-reference-sites)
- [3. Offline docs with Wget](#3-offline-docs-with-wget)
- [4. Per-source navigation tips](#4-per-source-navigation-tips)
  - [4.1. Python documentation](#41-python-documentation)
  - [4.2. Django documentation](#42-django-documentation)
  - [4.3. Read the Docs](#43-read-the-docs)
  - [4.4. Sphinx](#44-sphinx)

## 1. Searching docs faster

### 1.1. DevDocs

- **DevDocs** — free browser-based rapid documentation reference combining many sources (Python, Django, HTML, JS, etc.). Works offline, much faster than vanilla docs sites.
- **Browser-based alternative to Dash** — Dash is the original macOS-only paid offline docs tool; **Zeal** is its open-source clone for Windows/Linux. DevDocs is universal and free.
- **Setup is a one-time browser action** — DevDocs stores config in browser local storage; enable Django docs from the disabled list on the left.
- **Fuzzy search with `/`** — press `/` to focus the search box, type a partial term (e.g., `integf` matches `IntegerField`), navigate results with up/down arrows, enter to open.
- **Restrict search to one source** — type the docset prefix (e.g., `dj`) then `tab` to limit results to that source, avoiding cross-context jumble.
- **Reset with `escape`** — first press clears the search term, second press clears the source restriction.
- **Open original docs page** — `alt+o` opens the highlighted result on the original documentation site in a new tab.
- **Offline data via the kebab menu** — "Install all" downloads every enabled docset; useful on transport or when internet fails. Uncheck "Install updates automatically" to limit bandwidth surprises.
- **Recommended docsets for Django dev** — CSS, Django, Django REST Framework, DOM, Git, HTML, HTTP, JavaScript, Jinja, MariaDB, PostgreSQL, Python, SQLite (CSS, DOM, HTML, HTTP, and JavaScript come from MDN).

### 1.2. DuckDuckGo

- **DuckDuckGo** — privacy-first search engine with developer-centric features (keyboard shortcuts, bangs, instant answers). The author finds its results nearly always good enough for development and about 95% of the time for general queries; for the remaining ~5% the `!g` bang re-runs the query on Google.
- **Keyboard navigation** — `/` or `h` focuses the search box; `j`/`k` (or arrows) move between results; `enter`/`l`/`o` opens the selected result; `ctrl+enter` (or `command+enter`) opens it in a background tab. Google by contrast offers no shortcuts beyond focusing the search bar, and has even removed shortcuts over time.
- **Bangs** — exclamation-mark prefixes that redirect a query to another search engine without an intermediate page (e.g., `!py sorted` jumps directly to Python docs search).

| Bang | Target |
|------|--------|
| `!py` / `!python` | Python docs (latest stable) |
| `!pip` | PyPI package search |
| `!pep` | Python Enhancement Proposals (requires PEP number) |
| `!dj` / `!django` | Django docs (latest stable) |
| `!djpackages` | Django Packages |
| `!djticket` | Django ticket tracker (requires ticket number) |
| `!drf` | Django REST Framework docs |
| `!mdn` | Mozilla Developer Network |
| `!gh` / `!github` | GitHub general search |
| `!ghc` | GitHub code search |
| `!mariadb` / `!mysql` / `!postgres` / `!sqlite` | Database docs |
| `!g` | Google fallback |

- **Instant Answers** — for matching queries, DuckDuckGo shows extracted Python doc descriptions (e.g., `sorted()` signature) or top StackOverflow answers (e.g., Django's `truncatechars` filter) beside results.

## 2. Curated Django reference sites

Community-built cheat sheets that complement the official docs.

| Site | Purpose |
|------|---------|
| **Classy Class-Based Views (ccbv.co.uk)** | Class explorer for Django CBV hierarchy — shows where attributes/methods are defined. By Charles Denton and Marc Tamlyn. |
| **Classy Django Forms (cdf.9vo.lt)** | Same explorer pattern for Django forms and form fields. By Ana Balica, based on Classy Class-Based Views. |
| **Template Tags and Filters (djangotemplatetagsandfilters.com)** | Cheat sheet for Django's template language. By Nat Dunn. |
| **Classy Django REST Framework (cdrf.co)** | Class explorer for several types of classes in DRF. By André Ericson, also based on Classy Class-Based Views. |
| **Awesome Django (awesomedjango.org)** | Vetted index of Django resources, maintained by Jeff Triplett and Will Vincent. |

## 3. Offline docs with Wget

- **Wget** — command-line tool ("web get") that downloads a website and converts it for offline browsing. Use when a docs site has no download option and isn't on DevDocs.
- **Install** — `brew install wget` (macOS), `choco install wget` (Windows), pre-installed on most Linux distros.
- **One command to mirror a site**:

  ```console
  $ wget --mirror --convert-links --adjust-extension --page-requisites --no-parent <website>
  ```

  Output is stored in a directory named after the site's domain.
- **Flag breakdown**:

  | Flag | Purpose |
  |------|---------|
  | `--mirror` | Activates whole-site mirroring behaviours |
  | `--convert-links` | Rewrites HTML/CSS links to relative offline paths |
  | `--adjust-extension` | Adds correct file extensions where missing |
  | `--page-requisites` | Pulls CSS, images, and other included resources |
  | `--no-parent` | Stops recursion to parent paths (still allows resources from parent) |
  | `--wait <n>` | Optional — adds `n`-second delay between requests to limit bandwidth |

- **Some offline copies need a local web server** — sites that use AJAX or other JS navigation are blocked under `file://` URLs by browser security. Serve them via `python -m http.server 8001` (port 8001 avoids colliding with Django's `runserver` on 8000).

## 4. Per-source navigation tips

### 4.1. Python documentation

- **Three URL specificity levels** — stable (`/3/`), minor version (`/3.10/`), patch version (`/release/3.10.0/`). Read the *minor* version when browsing; patch pages are redundant.
- **Use stable URLs in links and comments** — `/3/` URLs are evergreen and survive Python upgrades. Convert `/3.10/...` to `/3/...` when sharing.
- **Lesser-known pages worth knowing** — the FAQ section (especially the Programming FAQ), the Glossary (e.g., distinguishes *annotations* from *type hints*, defines *EAFP*/*LBYL*), and the HOWTOs (Sorting, Unicode, Logging, Argparse, Regex) are useful complements to the reference.
- **Downloadable in PDF, HTML, plain text, and ePub** — useful as offline backup, but DevDocs is better for search.

### 4.2. Django documentation

- **Hidden `stable` URL specifier** — `https://docs.djangoproject.com/en/stable/...` redirects to the latest stable version, even though it isn't shown in the version switcher. Use it for evergreen links in code comments and docs.
- **Search shortcut `ctrl+k`** — focuses the docs search box from any page (also `command+enter` on macOS). Many other docs sites (MDN, Bootstrap CSS, Tailwind CSS) use the same convention; `/` is another common shortcut.
- **Read the Docs mirror** — `https://django.readthedocs.io/` hosts Django docs in the classic theme, including obsolete versions back to 1.4. Useful when `docs.djangoproject.com` is down.
- **Downloads in PDF, HTML, ePub** — links live in the docs sidebar.

### 4.3. Read the Docs

- **Project pages** — accessible via the floating switcher at the bottom right of any docs page. Provide downloads, version links, GitHub links, and an alternate search box.
- **Cross-version, type-narrowing search** — Read the Docs' search engine searches across versions and lets you narrow by *Code API Type* (function, class, exception, etc.), e.g., filtering attrs's `define` to `py:function` returns just the function entry.
- **`<project>.rtfd.io` shortcut** — redirects to `<project>.readthedocs.io` (RTFD = "Read The Friendly Docs"). Works for projects with custom domains too — `attrs.rtfd.io` redirects to `https://www.attrs.org/en/stable/`.

### 4.4. Sphinx

- **Sphinx is the de facto Python docs builder** — used by Python itself, Django, and most Read the Docs projects.
- **Find import paths via header anchors** — hover a function/class definition until the pilcrow (¶) appears, click it, and read the URL fragment after `#`. The fragment *is* the import path (e.g., `html.parser.HTMLParser`).
- **Strip search highlighting via the URL** — Sphinx adds `?highlight=...` after a search, which highlights every matched word on the destination page. Delete the query string to clean up the URL before sharing.
