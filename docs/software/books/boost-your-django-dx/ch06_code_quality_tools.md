# Ch 6: Code Quality Tools

## Table of Contents

- [1. EditorConfig: normalize text formatting](#1-editorconfig-normalize-text-formatting)
- [2. pre-commit: a code quality framework](#2-pre-commit-a-code-quality-framework)
  - [2.1. What it is and basic setup](#21-what-it-is-and-basic-setup)
  - [2.2. Configuration file structure](#22-configuration-file-structure)
  - [2.3. Running hooks](#23-running-hooks)
  - [2.4. Maintenance and CI](#24-maintenance-and-ci)
- [3. Black: formatting](#3-black-formatting)
- [4. isort: import sorting](#4-isort-import-sorting)
- [5. Flake8: linting](#5-flake8-linting)

## 1. EditorConfig: normalize text formatting

- **EditorConfig** — a cross-editor standard for sharing text formatting rules (encoding, line endings, indentation) so team members produce consistent files. Built into PyCharm and GitHub's web editor; small plugins exist for nearly every other editor.
- **`.editorconfig` at repo root** — INI-syntax file (parsed by Python's `configparser`) with `root = true` to stop merging from parent directories. Sections like `[*]` set defaults, `[*.py]` overrides per file glob.
- **Recommended baseline for Django** — `charset = utf-8`, `end_of_line = lf` (LF even on Windows for compatibility), `indent_style = space`, `indent_size = 2`, `trim_trailing_whitespace = true`, `insert_final_newline = true`, plus `[*.py]` overriding `indent_size = 4` per PEP 8.
- **Trailing whitespace and final newline matter** — trailing whitespace creates "diff noise" (edits that look like they touched unrelated lines); missing final newlines violate POSIX and break some tools, including silent "skip last line" failures. Git warns `\ No newline at end of file`.
- **No bulk reformatter for existing files** — EditorConfig only nudges the editor going forward. The pre-commit hooks `trailing-whitespace` and `end-of-file-fixer` enforce two of its rules retroactively.

## 2. pre-commit: a code quality framework

### 2.1. What it is and basic setup

- **pre-commit** — a framework that installs itself as Git's `pre-commit` hook and runs configured tools against staged files before each commit. Solves Git's hook problems: hooks live outside `.git/` (so they're shared via the repo), tool installation/versioning is automated, and multiple tools can run in order. Created by Anthony Sottile in 2014; used by Django (since 2020) and CPython (since 2023).
- **Install once globally** — `brew install pre-commit` or `pip install pre-commit` (system Python, not venv). Per-repo activation: `pre-commit install` writes the hook to `.git/hooks/pre-commit`. Every team member runs this when cloning.
- **`pre-commit sample-config`** — outputs a starter `.pre-commit-config.yaml` with four utility hooks from the `pre-commit-hooks` repo: `trailing-whitespace`, `end-of-file-fixer`, `check-yaml`, `check-added-large-files` (default 500kB cutoff; Git LFS handles large files better long-term).
- **Bootstrap workflow on adoption** — before committing the config, run `pre-commit run --all-files` so existing files get fixed in one pass; review automated edits with `git diff` (hooks are software and not bug-free); then stage and commit.

### 2.2. Configuration file structure

- **`repos` is the only required top-level key** — a list of Git repositories (the "lowest common denominator" distribution format). Each entry needs `repo` (URL), `rev` (Git tag), and `hooks` (list of selected hook IDs from that repo's `.pre-commit-hooks.yaml`). pre-commit clones into `~/.cache/pre-commit`.
- **`default_language_version`** — pin interpreter versions to avoid behaviour drift across team members. Black and Mypy notably change output by Python version; Prettier needs a precise Node version since pre-commit downloads its own Node copy.

  ```yaml
  default_language_version:
    python: python3.12
    node: 20.11.0
  ```

### 2.3. Running hooks

| Command | Purpose |
|---------|---------|
| `git commit` | Runs hooks against staged files (default flow) |
| `git commit -n` (`--no-verify`) | Skip pre-commit entirely (commit broken code on a feature branch) |
| `SKIP=hook1,hook2 git commit` | Skip selected hooks via env var |
| `pre-commit run` | Run all hooks against staged files without committing |
| `pre-commit run <id>` | Run one hook against staged files |
| `pre-commit run --all-files` (`-a`) | Run all hooks against the entire repo (the CI command) |
| `pre-commit run --files <paths>` | Run against arbitrary files, even untracked ones |
| `pre-commit run --from main --to HEAD` | Check files changed on the current branch |
| `git ls-files -z -- '*.py' \| xargs -0 pre-commit run --files` | Run against many globbed files without hitting argv limits |

- **Hook fixes outrank stashed changes** — if a stashed change conflicts with a hook fix, pre-commit discards the fix. Hand-authored work is treated as more valuable than automated edits.

### 2.4. Maintenance and CI

- **`pre-commit autoupdate`** — bumps every hook's `rev` to the latest tag and rewrites `.pre-commit-config.yaml`. Does not touch `additional_dependencies` — update those manually.
- **pre-commit ci** — hosted CI service (also by Anthony Sottile), GitHub-only, free for open-source. Runs pre-commit on every commit/PR, auto-commits hook fixes back to the PR, runs `autoupdate` weekly (configurable to monthly/quarterly) opening a PR with bumped versions. Reuses pre-commit's hook-environment cache shared across users, so it's much faster than running pre-commit on Circle CI / GitHub Actions / Travis. A free "lite" version runs in GitHub Actions but is slower and skips `autoupdate`.
- **Always run `pre-commit run --all-files` in CI** — because devs can `git commit -n` past hooks locally, CI is the only enforced checkpoint.
- **Introduce hooks incrementally with `files`** — add a regex (verbose mode `(?x)` recommended for readability) to scope a new hook to one directory at a time, expanding the alternation group `(static/.* |templates/includes/.*)` until the whole repo passes, then drop the `files` key.

## 3. Black: formatting

- **Black** — the dominant Python code formatter. Reformats to a single style based on PEP 8 with no configuration options (the name nods to Henry Ford's Model T quip — "any color so long as it is black"). Created by Łukasz Langa in 2018; lives under the PSF; stable since 2022; adopted by Django via DEP 8.
- **Style summary** — 88-character line wrap, 4-space indentation, double quotes (perhaps the most controversial choice), call-chain split with one method per line and dots at line start (great for Django ORM), optional parens removed, `\` line continuations replaced with parens. Style changes only release "stable" once per year; opt-in early via `--preview`.
- **The "magic trailing comma"** — the only style lever. A trailing comma after the last collection item signals "expect this to grow", forcing one-item-per-line layout to keep future diffs minimal. Without it, Black collapses short collections onto one line. Add the comma when growth is likely; omit otherwise.
- **Pin `target-version` in `pyproject.toml`** — `[tool.black] target-version = ['py312']` prevents per-file syntax detection from triggering reformatting when new syntax is introduced. Adjust to your Python version.
- **Adopt in one big commit** — separates formatting churn from logic changes. To preserve `git blame` history, configure Git's "ignore commits in blame" mechanism (Black documents the setup).
- **blacken-docs** — Black for code snippets inside reStructuredText, Markdown, LaTeX, and `.py` docstrings. Side benefit: Black fails on syntax errors, so blacken-docs catches broken example code. Pin Black explicitly via `additional_dependencies` since blacken-docs vendors its own copy.

## 4. isort: import sorting

- **isort** — sorts and groups Python `import` statements so a reader can skim and locate where a name comes from. Created by Timothy Crosley in 2013; lives under PyCQA; used by Django since 2015.
- **What it does** — hoists imports to top of scope; groups by source in fixed order: future, standard library, third party, first party, local folder (relative); sorts `import` before `from`; alphabetizes statements and imported names.
- **Use the `black` profile** — `[tool.isort] profile = "black"` in `pyproject.toml` makes isort's output Black-compatible (no further bikeshedding needed). The legacy `django` profile is now historical — Django itself moved to `black` in 2022.
- **Order Black before isort** — both make compatible edits, so order matters little, but the author runs Black first.
- **`add_imports` / `remove_imports`** — secondary feature that injects or strips an import in every file. Useful for `from __future__ import annotations` (postponed evaluation of type hints, Python 3.7+): set `add_imports` to add it everywhere, then later flip to `remove_imports` once the future feature becomes default. Keep `remove_imports` configured for a while to clean up accidental re-additions.

## 5. Flake8: linting

- **Flake8** — extensible Python linter. Frameworks rather than implements: by default pulls checks from pyflakes, pycodestyle, and mccabe; rich plugin ecosystem on top. Created by Tarek Ziadé in 2010; now maintained by Anthony Sottile under PyCQA. Used by Django.
- **Linters catch what formatters can't** — name says it: lint catchers in dryers stop small fibres from causing fires. Flake8 reports localized issues that need human judgement to fix (e.g., undefined names, unused imports, possible bugs).
- **Black-compatible config** — in `setup.cfg` set `max-line-length = 88` (matches Black) and `extend-ignore = E203` (Black's slice spacing). Without these, Flake8 fights Black on formatting.
- **Place Flake8 after formatters** — pyupgrade, Black, isort run first; Flake8 last avoids reporting issues the formatters would auto-fix.
- **Ignore in-line with `# noqa: <code>`** — sparingly. For incremental rollout, list error codes under `extend-ignore` one per line and remove them gradually.
- **Plugins install by adding the package** — Flake8 auto-discovers any plugin in its environment (declare via `additional_dependencies` in the pre-commit hook). If using `select`, also add the plugin's error code prefix.
- **flake8-bugbear** — extra checks for common bugs (PyCQA-hosted). Example: B002 catches `++var`, which in Python is valid but means `+(+(var))` — useful for programmers coming from C who expect increment.
- **flake8-no-pep420** — bans implicit namespace packages (directories of `.py` files without `__init__.py`, valid since PEP 420). Such packages are silently skipped by unittest discovery (and Django's test runner), Coverage.py (unless `report.include_namespace_packages`), and pytest — leading to a false sense of security where tests don't run and coverage looks fine. Fix by adding `__init__.py`; exclude `manage.py` via `per-file-ignores = manage.py:INP001`.

| Plugin | Catches |
|--------|---------|
| **flake8-2020** | Misuse of `sys.version` / `sys.version_info` (e.g., `3.10` vs `3.1` confusion) |
| **flake8-breakpoint** | Committed `breakpoint()` or `import pdb` |
| **flake8-comprehensions** | Improvements to list/set/dict comprehensions and generators |
| **flake8-docstrings** | Docstring style via `pydocstyle` |
| **flake8-logging** | Misuse of stdlib `logging` (some prevent log messages from being sent) |
| **flake8-print** | Stray `print()` calls in projects that use logging |
| **flake8-tidy-imports** | Banned imports (deprecation), discouraged relative imports |
| **flake8-typing-imports** | `typing` imports incompatible with target Python versions |
