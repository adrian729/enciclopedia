# Ch 9: Settings

## Table of Contents

- [1. Organizing the settings file](#1-organizing-the-settings-file)
  - [1.1. Single file with environment variables](#11-single-file-with-environment-variables)
  - [1.2. Grouping and ordering](#12-grouping-and-ordering)
  - [1.3. `BASE_DIR` with `pathlib`](#13-base_dir-with-pathlib)
- [2. Settings in tests](#2-settings-in-tests)
- [3. Anti-patterns to avoid](#3-anti-patterns-to-avoid)
- [4. Testing the settings file](#4-testing-the-settings-file)

## 1. Organizing the settings file

### 1.1. Single file with environment variables

- **Single settings file over per-environment files** — one file reading external values is more straightforward than maintaining a `settings/dev.py`, `settings/prod.py` split, and keeps configuration separate from code so a deploy can be reconfigured without a code change.
- **Environment variables as the config channel** — universal across OSes, languages, and platforms; popularized by Heroku's "Twelve-Factor App". Read with `os.environ`; values are always strings, so parse as needed.
- **`.env` file for local dev** — a `KEY=value` text file loaded into `os.environ` at the top of settings via `python-dotenv` (`dotenv.load_dotenv(...)`); doesn't error if missing and won't override existing env vars, so command-line overrides still work. `environs` adds parsing helpers on top.
- **Never commit `.env`** — it holds secrets like API passwords; add `/.env` to `.gitignore` and ship a tracked `.env-example` template with example values and comments so new developers can copy it.

### 1.2. Grouping and ordering

- **Five-section settings layout** — head each group with a comment so a reader can jump straight to the relevant section:

  | # | Group | Contents |
  |---|-------|----------|
  | 0 | Setup | Imports and `.env` loading |
  | 1 | Django Core Settings | Settings from Django's "Core Settings" reference |
  | 2 | Django Contrib Settings | One sub-section per `django.contrib.*` app, alphabetized |
  | 3 | Third Party Settings | One sub-section per installed package, alphabetized |
  | 4 | Project Settings | Custom settings, grouped per app if multiple |

- **Alphabetize within each group** — co-locates related settings; hoist dependencies like `BASE_DIR` to the top of their section when other settings reference them.
- **Order `INSTALLED_APPS` First Party → Third Party → Contrib** — Django resolves ties (templates, static files, management commands, translations) by first listing wins, so put apps you might want to override last. Alphabetize within each group unless an override demands otherwise.

### 1.3. `BASE_DIR` with `pathlib`

- **`BASE_DIR` is a pseudo-setting** — Django itself doesn't read it, but the default `settings.py` defines it, the docs reference it, and some third-party packages use it for path-based configuration.
- **Modern form uses `pathlib`** — since Django 3.1: `BASE_DIR = Path(__file__).resolve().parent.parent`. Replaces the older nested `os.path.dirname(os.path.dirname(os.path.abspath(__file__)))` and lets you build paths with the `/` operator (`BASE_DIR / "static"`) instead of `os.path.join`.
- **Some settings reject `Path` objects** — wrap in `str()` (e.g., `str(BASE_DIR / "static")`) when targeting older Django versions that expect strings.

## 2. Settings in tests

Tests pose two problems: a stray `.env` file could leak local config (worst case, hit a real remote API), and some settings need to differ during tests for speed or isolation.

- **Skip `.env` loading during tests** — guard `load_dotenv()` so it doesn't run under the test command. With Django's test framework, check `sys.argv[1] != "test"`; with pytest, check `"pytest" not in sys.modules` (the documented pytest pattern fails because pytest-django imports settings too early).
- **Override settings via a test runner (Django)** — set `TEST_RUNNER = "example.test.TestRunner"` to a `DiscoverRunner` subclass that wraps `run_tests()` in `override_settings(**TEST_SETTINGS)`. Place test-only values in a `TEST_SETTINGS` dict.
- **Override settings via a session fixture (pytest)** — an `autouse=True`, `scope="session"` fixture in top-level `conftest.py` that yields inside `override_settings(**TEST_SETTINGS)`. Same `TEST_SETTINGS` dict pattern.

## 3. Anti-patterns to avoid

- **Don't read settings at import time** — `page_size = settings.PAGE_SIZE` at module level captures the value once, so `override_settings` in tests won't take effect. Read inside the function/method (e.g., pass `settings.PAGE_SIZE` to `Paginator` per-call, or implement `get_paginate_by()` on a CBV instead of setting `paginate_by` as a class attribute).
- **Don't mutate `settings.X = ...` directly** — bypasses the `setting_changed` signal, so receivers (cache rebuilds, etc.) aren't notified. Always use `override_settings` (decorator or context manager). pytest-django's `settings` fixture is a special case — it uses `override_settings` internally.
- **Don't import the project's settings module** — `from example import settings` bypasses Django's settings machinery, so `override_settings` and alternate settings modules don't apply. Always `from django.conf import settings`. Enforce with the `flake8-tidy-imports` `banned-modules` option. The one legitimate exception: tests for the settings module itself.
- **Don't promote constants to settings** — if a value can't actually change (e.g., `EXAMPLE_API_BASE_URL = "https://api.example.com"`), it's a constant. Define it in the module that uses it instead of cluttering the settings file.
- **Don't define dynamic constants outside settings** — putting `os.environ.get(...)` reads in random modules makes the project's environment variables undiscoverable, makes timing unpredictable (the module may import before `.env` loads), and `override_settings` can't reach them. Centralize all env-var reads in the settings file.
- **Name custom settings verbosely** — settings share a single flat namespace, so abbreviations bite. `EA_TO` raises questions ("EA"? "TO"? what units?); `EXAMPLE_API_TIMEOUT_SECONDS` answers them. Match the env-var name to the setting name.
- **Override complex settings by copying, not replacing** — `override_settings(EXAMPLE={"PAGE_SIZE": 2})` erases sibling keys like `VERSIONING`. Use `settings.EXAMPLE | {"PAGE_SIZE": 2}` (Python 3.9+ merge operator) or `dict(settings.EXAMPLE, PAGE_SIZE=2)` to preserve the rest.

## 4. Testing the settings file

- **It's fine to put logic and helper functions in settings** — if a function is only used there, defining it inline beats inventing a new module. Test that logic like any other code.
- **Test settings functions directly** — import the settings module (one of the few times bypassing `django.conf.settings` is okay, because settings only exposes uppercase names). Use `RequestFactory` for callable settings like django-debug-toolbar's `SHOW_TOOLBAR_CALLBACK`, and `@override_settings(DEBUG=True)` since the test runner sets `DEBUG=False`.
- **Test module-level logic by re-importing** — module-level code runs once at import time, so to exercise branches like `if os.environ.get("HTTPS") == "1": ...` you need a fresh import. Copy `import_fresh_module()` from Python's `test.support` (it has no public-API guarantees, so vendoring is safer than depending on it). Combine with `mock.patch.dict(os.environ, {...})` to simulate different env vars; pass dependent settings modules via the `fresh` parameter when re-importing a layered settings file.
