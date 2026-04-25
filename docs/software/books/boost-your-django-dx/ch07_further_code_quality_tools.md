# Ch 7: Further Code Quality Tools

## Table of Contents

- [1. Syntax modernizers](#1-syntax-modernizers)
- [2. Extra pre-commit-hooks utilities](#2-extra-pre-commit-hooks-utilities)
- [3. reorder-python-imports: alternative import sorter](#3-reorder-python-imports-alternative-import-sorter)
- [4. DjHTML: template indentation](#4-djhtml-template-indentation)
- [5. Mypy: static type checking](#5-mypy-static-type-checking)
- [6. Prettier: format CSS, JavaScript, and more](#6-prettier-format-css-javascript-and-more)
- [7. ESLint: JavaScript linting](#7-eslint-javascript-linting)
- [8. ShellCheck: shell script linting](#8-shellcheck-shell-script-linting)

## 1. Syntax modernizers

- **pyupgrade** — rewrites old Python syntax into the current preferred form, normalizing code so muscle memory for the old style doesn't matter. Created by Anthony Sottile in 2017; used by Django. Pass `--py312-plus` (or your version) to enable rewrites up to that Python; add the flag to your "upgrade checklist" so it gets bumped after Python upgrades. Examples: `'{foo}'.format(foo=foo)` → f-string; `super(C, self).f()` → `super().f()`; `if x is 5` → `if x == 5`.
- **django-upgrade** — same idea for Django: rewrites code to avoid deprecation warnings on a target Django version. Created by the book's author Adam Johnson in 2021, building on Bruno Alla's django-codemod. Configure with `args: [--target-version, "4.0"]`. Examples: `django.conf.urls.url(r'^$', ...)` → `django.urls.path('', ...)`; `request.META['HTTP_ACCEPT_ENCODING']` → `request.headers['Accept-Encoding']`; `django.contrib.postgres.fields.JSONField` → `django.db.models.JSONField`.
- **Order modernizers before formatters and linters** — pyupgrade and django-upgrade emit code that may need cleanup by Black, and shouldn't trip Flake8 along the way.

## 2. Extra pre-commit-hooks utilities

The default `pre-commit-hooks` repo ships more cheap checks worth adding:

| Hook | Catches |
|------|---------|
| `check-case-conflict` | Files differing only by case (`Example.py` vs `example.py`) — broken on macOS HFS and Windows FAT |
| `check-json` / `check-toml` / `check-xml` | Invalid JSON / TOML / XML files |
| `check-merge-conflict` | Leftover Git merge markers (`<<<<<<< HEAD` etc.) |

## 3. reorder-python-imports: alternative import sorter

- **reorder-python-imports** — alternative to isort, also by Anthony Sottile. Same grouping/sorting concept but always **one `from` import per line**, never combined. The single-line layout dramatically reduces merge conflicts: concurrent edits adding/removing imports from the same module no longer touch the same line.
- **Built-in stdlib rewrites** — pass `--py312-plus` (and similar) to apply rewrites between Python versions. Example: `from mock import patch` → `from unittest.mock import patch` (Python 3.3 absorbed `mock` into `unittest.mock`).
- **`--replace-import <old>=<new>`** — refactor aid for renaming modules across the codebase. Worth knowing even if you stay on isort: use temporarily during a rename, then return to your usual sorter.
- **isort can mimic the single-line style** — set `force_single_line = true` in `[tool.isort]` to get the merge-conflict reduction without switching tools.

## 4. DjHTML: template indentation

- **DjHTML** — formatter for Django templates that *only* corrects indentation. Conservative scope avoids more aggressive changes that might break templates. Created by Jaap Joris in 2021. Indents one level per Django tag and HTML tag; also indents inline CSS/JS inside `<style>` and `<script>`.
- **`--tabwidth=2`** — DjHTML defaults to 4-space indents; override to 2 to match the de facto HTML/CSS/JS standard (and the EditorConfig baseline from Ch 6).
- **Verify whitespace-only changes** — run `git diff --ignore-all-space` after; for most tags, whitespace shifts preserve meaning, but elements like `<pre>` (special-cased) and anything with `white-space: pre` in CSS are sensitive. Automated changes always remain the developer's responsibility.

## 5. Mypy: static type checking

- **Mypy** — the most popular Python static type checker. Catches mismatched types via Python's annotation syntax (`def greet(name: str) -> None:`), spotting bugs that linters can't because Mypy understands code structure more deeply. Example: `greet(["World"])` reports `Argument 1 to "greet" has incompatible type "List[str]"; expected "str"`.
- **django-stubs** — adds Django-aware type hints; lets Mypy verify e.g. that callers handle `None` from nullable model fields.
- **Use `mirrors-mypy` with pre-commit** — but be aware Mypy runs in pre-commit's separate virtualenv; if that breaks, fall back to a `system` hook that runs Mypy in your project's venv.
- **The book defers depth** — type-checking is a whole topic on its own; the chapter points to Mypy's getting-started guide, the author's blog tag, and the awesome-python-typing articles list.

## 6. Prettier: format CSS, JavaScript, and more

- **Prettier** — multi-language code formatter ("Black for JavaScript"). Created in 2017 by James Long and Christopher Chedeau. Like Black, applies a single style with minimal options. Out-of-the-box support: JavaScript (incl. JSX, experimental features), Angular, Vue, Flow, TypeScript, CSS/Less/SCSS, HTML, JSON, GraphQL, Markdown, YAML.
- **Cannot format Django HTML templates** — template syntax isn't valid HTML. Use `types_or` in the pre-commit hook to scope Prettier to safe types (`css`, `js`, etc.) rather than all text files.
- **Use `mirrors-prettier`** — official pre-commit repo mirroring Prettier releases.
- **Plugins extend coverage** — set `additional_dependencies` in the pre-commit hook *and re-declare prettier itself there* (because the mirror repo isn't Prettier; `additional_dependencies` replaces the mirror's declaration). Example: `prettier@3.0.3` plus `'@prettier/plugin-xml@3.2.1'`. Caveat: `pre-commit autoupdate` doesn't touch `additional_dependencies` — bump versions manually.

## 7. ESLint: JavaScript linting

- **ESLint** — most widely used JavaScript linter. Name from ECMAScript. Created in 2013 by Nicholas C. Zakas. Many rules, some auto-fixable via `--fix`.
- **Recommended ruleset is the starting point** — enable `js.configs.recommended` from `@eslint/js`; without it ESLint runs no rules. Examples of rules it covers: `no-const-assign` (catches reassignment of `const` variables, which raises `TypeError` at runtime); `no-sparse-arrays` (catches `["blue",, "purple"]` where a stray comma creates an `undefined` hole — almost always a typo).
- **`eslint.config.js` ("flat config")** — the new format from ESLint 9, replacing `.eslintrc` / `package.json`-embedded configs. Exports an array of config objects. Also configure `globals.browser` so `console`/`window`/etc. aren't flagged.
- **Pre-commit setup uses `repo: local`** — defines the hook in your repo (the older `mirrors-eslint` only installs base ESLint and doesn't fit flat config). Required `additional_dependencies`: `eslint`, `@eslint/js`, `globals`. Run with `--fix`.
- **Place ESLint after Prettier** — otherwise ESLint flags formatting issues that Prettier would have fixed.
- **eslint-config-prettier** — disables ESLint rules that conflict with Prettier's formatting choices. Add to `additional_dependencies` and import into the flat config (`eslintConfigPrettier`) when running both tools.
- **Run ESLint twice on first install** — first pass auto-fixes, second pass reports what still needs human attention. Also bump versions when copying configs because ESLint moves fast.

## 8. ShellCheck: shell script linting

- **ShellCheck** — linter for shell scripts (POSIX sh, Bash, dash, ksh). Catches the many sharp edges in shell syntax that bite even experienced authors. (The author also suggests rewriting some scripts in Python.)
- **Example findings on a backup script** — SC2045 (iterating `$(ls ./*.py)` is fragile, use globs), SC2086 (unquoted `$file` allows globbing/word-splitting, use `"$file"`), SC2016 (single quotes don't expand `$file`, use double). Linked wiki pages explain *why* each pattern is risky.
- **shellcheck-py for pre-commit** — ShellCheck is written in Haskell and tricky to install cross-platform; the `shellcheck-py` package wraps it as a pip-installable Python distribution, sidestepping pre-commit's environment management. Configuration usually unnecessary; `.shellcheckrc` covers global tweaks.
