# Ch 5: Development Server

## Table of Contents

- [1. django-debug-toolbar](#1-django-debug-toolbar)
  - [1.1. Key panels](#11-key-panels)
  - [1.2. Diagnosing slow queries](#12-diagnosing-slow-queries)
  - [1.3. Non-HTML requests via the History panel](#13-non-html-requests-via-the-history-panel)
- [2. django-browser-reload](#2-django-browser-reload)
- [3. Rich terminal output](#3-rich-terminal-output)
  - [3.1. Server logs via `RichHandler`](#31-server-logs-via-richhandler)
  - [3.2. Management commands with django-rich](#32-management-commands-with-django-rich)

## 1. django-debug-toolbar

- **django-debug-toolbar** — development package that injects a floating "DjDT" tab into every HTML response (before `</body>`), opening a panel that exposes per-request data Django would otherwise hide. Created by Rob Hudson in 2008, now maintained by Jazzband. Third-most-mentioned package in the 2022 Django survey; clones exist for Flask and FastAPI. Author rates it a "must-have".
- **Installation** — `pip-install` the package, then add the app, URLs, and middleware per its docs. Requires `DEBUG=1` to be active. Drag the tab vertically to keep it from covering content; click "Hide »" to close once open.
- **Customizable panels** — each panel collects data during request processing. Toggle individual panels off via checkboxes for performance — especially useful for the heavier "Profiling" panel.

### 1.1. Key panels

| Panel | Shows |
|-------|-------|
| **Versions** | Django, Python, and third-party package versions — basic but handy for environment bugs. |
| **Time** | Two tables: in-Django CPU time (User CPU = Python time, System CPU = system calls like DB I/O) and browser-side timings (DOM events, etc., per MDN's Navigation and resource timings). |
| **SQL** | Every query in order, with timeline blocks colour-coded slowest-red to fastest-green. `+` expands to full SQL; `Sel` re-runs a SELECT and shows results; `Expl` runs the database's `EXPLAIN` for the query plan. |
| **Templates** | All templates rendered including those pulled in via `{% extends %}` and `{% include %}`. "Toggle context" reveals the chained dictionaries (engine, context processors, view-passed); the explicit context is last and usually what you want. |
| **History** | Past requests, switchable via the "Switch" button to inspect non-HTML responses. |

### 1.2. Diagnosing slow queries

- **`Books` page case study** — page takes ~1.5s; SQL panel shows "96 queries including 95 similar and 95 duplicates". *Similar* = repeated SQL with possibly different parameters; *duplicate* = same SQL with same parameters. The slowest query (red) is the initial `SELECT ... FROM core_book`; the second query, `SELECT ... FROM core_author WHERE ...`, repeats 95 times.
- **N + 1 Queries Problem** — outer template loop `{% for book in books %}` runs one query for books; inner `{{ book.author.name }}` triggers one query per book to fetch its author. Total: *N + 1* queries. Traceback in the SQL panel pinpoints the responsible template line.
- **Fix with `prefetch_related()`** — change `Book.objects.all()` to `Book.objects.prefetch_related("author")`. Page now issues 2 queries (one for books, one batched `WHERE "core_author"."id" IN (...)`) and loads ~10x faster.

### 1.3. Non-HTML requests via the History panel

- **JSON / API endpoints** — toolbar can't inject into non-HTML responses. Open the endpoint in a new tab, then back on a toolbar-bearing page open the **History** panel, click "Refresh" to update, and "Switch" on the API request — all panels (SQL, Templates, etc.) re-bind to that captured request. Same N+1 fix (`prefetch_related("author")`) applies to JSON views.

## 2. django-browser-reload

- **Why** — the manual edit-save-refresh loop wastes hours per developer per year. Existing JS-based reloaders typically need Node.js or extra processes.
- **django-browser-reload** — author-built package that uses Django's existing change detection plus a small JS shim to reload the browser automatically. Written during this book ("Book Driven Development"). Designed as the simplest thing that works for typical projects; complex SPA stacks may want something else.
- **Triggers reloads on** — template changes (Django's engine and Jinja, fires within milliseconds of save), static asset changes (e.g., editing CSS), and Python code changes — for code edits, the JS waits for `runserver` to finish restarting before reloading, avoiding the "unable to connect" error from refreshing too soon.
- **Scope** — always reloads the most recently loaded tab; doesn't try to track which file affects which page (too unreliable).
- **Production-safe** — only operates when `DEBUG = True`, so it can stay installed in production deployments.

## 3. Rich terminal output

- **Rich** — library for richly formatted terminal output: colour, tables, syntax highlighting, hyperlinks. Cross-platform and degrades gracefully when features are absent. Used by Pip itself. Two Django use cases: `runserver` logs and management commands.

### 3.1. Server logs via `RichHandler`

- **Wire-up** — copy Django's `DEFAULT_LOGGING` from `django/utils/log.py` into your settings as `LOGGING`, then point the `console` handler's `class` to `rich.logging.RichHandler`. Pass `rich_tracebacks=True` and `tracebacks_show_locals=True` to enable Rich's traceback rendering, and gate with the `require_debug_true` filter so Rich never runs in production.
- **`%X` datefmt** — the project uses a `rich` formatter with `datefmt: "[%X]"`, the locale's time-only representation per `time.strftime()`. Good for short-lived dev servers; not for production where you want full datestamps and persisted logs.
- **Visual improvements** — Rich skips repeating the time within the same second (easy left-column skim), colours log levels by severity (INFO dark blue, WARNING red), and parses Django's request log format to colour Method, URL, HTTP version, status, and response size separately. Right-side filename and line number are clickable hyperlinks on capable terminals (e.g., command-click in iTerm2 on macOS).
- **Rich tracebacks** — when an exception is logged, Rich shows for each frame a clickable file:line link, a syntax-highlighted source extract, and (with `tracebacks_show_locals`) a table of local variables. Like Django's debug error page, but in the terminal — and works for exceptions outside HTTP requests, e.g., in management commands.

### 3.2. Management commands with django-rich

- **django-rich** — separate package providing a `RichCommand` base class. Subclassing it gives `self.console`, a properly configured Rich `Console` instance.
- **Example: `top_books` command** — fetches the top 5 `Book`s by likes (`prefetch_related("author").order_by("-likes")[:5]`), builds a `rich.table.Table` with columns Title, Author, Number of Likes (right-justified, `style="bold blue"`), adds a row per book, and prints with `self.console.print(table)`.
- **Other Rich tools worth checking out**:
  - **Progress Display** — animated progress bars for long-running tasks like data backfills.
  - **Live Display** — live-updating UIs, useful for monitoring commands.
  - **Console Protocol** — let your model classes define their own Rich rendering so they're readable when printed during debugging.
