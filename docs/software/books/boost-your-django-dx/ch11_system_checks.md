# Ch 11: System Checks

## Table of Contents

- [1. How the framework works](#1-how-the-framework-works)
- [2. Writing custom check functions](#2-writing-custom-check-functions)
  - [2.1. Anatomy of a check](#21-anatomy-of-a-check)
  - [2.2. Registering checks](#22-registering-checks)
  - [2.3. Two example checks](#23-two-example-checks)
- [3. Testing custom checks](#3-testing-custom-checks)
- [4. Checks on Django classes](#4-checks-on-django-classes)
- [5. `django-version-checks`](#5-django-version-checks)

## 1. How the framework works

- **System checks framework** — Django's mechanism for collecting validation functions that each return a list of `CheckMessage`s; the framework runs them all, displays the messages, and aborts the current command if any are errors. Built-in checks cover incompatibilities, security, and uninstalled app dependencies; third-party packages plug in to validate their own configuration.
- **When checks run** — at the start of most management commands, on every `runserver` reload, and explicitly via `./manage.py check`. Misconfiguring `CACHES` produces, e.g., `(caches.E001) You must define a 'default' cache in your CACHES setting.`
- **Run `manage.py check --deploy` *before* `migrate` in deploys** — the `--deploy` flag enables an extended set of checks targeted at production environments, per Django's deployment checklist. Running it before `migrate` exits early on misconfiguration.
- **Silence via `SILENCED_SYSTEM_CHECKS`** — list check IDs (e.g., `"models.E034"` for the 30-character index name limit, only relevant on Oracle) to suppress their messages while still running them. Add an explanatory comment when silencing — it removes a safety feature. The `check` command reports the silenced count: `(1 silenced)`.
- **Why checks beat ad-hoc validation** — they run in batch (one pass surfaces every issue, vs. one-exception-at-a-time); they fire early in dev workflows; and because they execute as Python they can inspect live runtime objects, finding issues linters can't reach reliably.
- **The trade-off: checks must be fast** — milliseconds, not seconds. No file reads, DB queries, or source parsing — those belong in linters and code-quality tools.

## 2. Writing custom check functions

### 2.1. Anatomy of a check

- **Signature** — `def my_check(*, app_configs, databases, **kwargs)` returning a list of `CheckMessage`s. Always accept `**kwargs` for forward compatibility. `app_configs=None` means "check all apps"; `databases=None` means "no databases".
- **Five severity subclasses** — `Debug`, `Info`, `Warning`, `Error`, `Critical`. In practice almost all custom checks use `Error` (fails the run) or `Warning` (displayed but doesn't fail).
- **Four `CheckMessage` arguments** — `msg` (required, short user-facing string), `hint` (optional longer fix advice), `obj` (optional associated object — model class, view, etc.), `id` (optional stable identifier).
- **Recommended `id` format** — `{category}.{letter}{number}`, where `letter` is `E` for errors and `W` for warnings (e.g., `example.W001`). `id` is what `SILENCED_SYSTEM_CHECKS` references, so always provide one even though only `msg` is required.

### 2.2. Registering checks

- **Convention: `<app>/checks.py`** — Django doesn't auto-discover; you must register every check explicitly.
- **Prefer explicit registration in `AppConfig.ready()`** — `from example import checks; register(checks.example_check)`. The decorator form (`@register` on the function) works but relies on the checks module being imported as a side effect, which linters may flag as unused — silently disabling your checks if removed.
- **`register()` extras** — accepts tag arguments and a `deploy=True` flag to run only under `--deploy`. Most custom checks should always run, so these can be ignored.

### 2.3. Two example checks

- **Check 1: Python development mode active when `DEBUG=True`** — warns when `settings.DEBUG and not sys.flags.dev_mode`. Returns `CheckWarning(...)` (imported as `from django.core.checks import Warning as CheckWarning` to avoid shadowing Python's builtin `Warning`) with id `example.W001` and a hint to set `PYTHONDEVMODE=1` or run `python -X dev`. Warnings are displayed but don't block execution, leaving the developer free to ignore.
- **Check 2: Model class names must be singular** — loops over `apps.get_app_configs()` (when `app_configs is None`), filters out non-project apps by import-path prefix (`example`), iterates `app_config.get_models()`, and emits an `Error` (id `example.E001`) for any class whose `__name__` ends with `"s"` and isn't in a `SAFE_MODEL_NAMES = {"PrintingPress"}` allow-list. Singular names (`Book` not `Books`) read better with the ORM (`Book.objects.all()`).
- **Why a local allow-list?** — `SILENCED_SYSTEM_CHECKS` silences a check ID *globally* across every instance. Until Django ticket #26472 lands a per-instance silence mechanism, custom mechanisms like `SAFE_MODEL_NAMES` are needed for model-by-model exemption.

## 3. Testing custom checks

Custom checks return no errors in normal conditions, so without tests you can't be sure they still detect their target.

- **`SimpleTestCase` for check tests** — prevents DB access and runs faster; appropriate because checks shouldn't touch the DB unless explicitly tagged `database`.
- **Mock read-only attrs via `SimpleNamespace`** — `sys.flags.dev_mode` is read-only, so `mock.patch.object(sys, "flags", SimpleNamespace(dev_mode=True))` replaces the whole `sys.flags` object with one that has the attribute you need.
- **Combine `override_settings` with the mock** — `with override_settings(DEBUG=True), mock_dev_mode(False): ...`. Asserting on `result[0].id == "example.W001"` is usually enough; comparing whole `CheckMessage` instances (per Django's docs) is verbose without much added safety.
- **`isolate_apps` for model-name-style checks** — `@isolate_apps("example", attr_name="apps")` decorates a `SimpleTestCase` to give it a temporary, standalone app registry containing only the named app. Inside test methods you can declare local `class Sample(models.Model): pass` definitions that won't pollute the real registry — otherwise the check would fail outside the test. Pass `app_configs=self.apps.get_app_configs()` into the check.
- **Patching the allow-list** — `mock.patch("example.checks.SAFE_MODEL_NAMES", new={"Plurals"})` lets you verify the bypass branch without editing the real set.

## 4. Checks on Django classes

- **`check()` methods on framework classes** — Django piggybacks the check registration mechanism: `Model` (classmethod), `Field` (instance), `Manager` (instance), `ModelAdmin` (via `checks_class`), and database backend `DatabaseValidation` (instance) all support `check()` overrides that the framework auto-discovers.
- **Model class checks** — define `@classmethod def check(cls, **kwargs):`, call `super().check(**kwargs)` to inherit the built-in errors, then append your own. Putting the singular-name check on an abstract `NameCheckedModel` (id `example.E002`) limits enforcement to its subclasses, simplifying staged rollout in larger projects compared to a project-wide registered function.
- **Django's own pattern: `_check_*` helpers** — `Model.check()` itself composes results from `_check_swappable()`, `_check_model()`, `_check_managers()`, `_check_fields()`, `_check_m2m_through_same_relationship()`, `_check_long_column_names()`, etc. Worth adopting once you accumulate several model-level checks.
- **Field checks use instance methods** — same shape as model checks but `def check(self, **kwargs)` since fields are instances on the model class.

## 5. `django-version-checks`

- **The problem** — every environment (dev laptops, CI, staging, production) should run identical Python and database server versions; mismatches cause hard-to-debug bugs and risk data loss. Coordinating versions is fiddly because each environment uses different config systems and every developer has their own machine.
- **`django-version-checks`** — a package by the author that provides system checks comparing actual runtime versions against expected ranges; out-of-range versions produce check errors that block running the project. Supports Python and the major databases (MySQL/MariaDB, PostgreSQL, SQLite).
- **Why a system check fits here** — version checks are fast and should run before any other code; running through Django's check framework means identical behaviour across OSes and environments.
- **`VERSION_CHECKS` setting** — a dict from name to PEP 440 version specifier (the same format Pip accepts). `~=3.10.1` is shorthand for `>=3.10.1,<3.11`, allowing patch upgrades but not minor jumps. Example:

  ```python
  VERSION_CHECKS = {
      "postgresql": "~=14.0",
      "python": "~=3.10.1",
  }
  ```

  A non-compliant environment errors as `(dvc.E003) The current version of Python (3.9.9) does not match the specified range (~=3.10.1).`
- **Three-step upgrade workflow** — (1) widen the range to admit both old and new versions, (2) upgrade environments, (3) narrow the range to only the new version. E.g., `~=3.11.0` → `>=3.11.6, < 3.13` → `~=3.12.0`.
- **Phased rollouts via `DEBUG`** — branch the setting on `if DEBUG:` to require the new version in development first while staging/production stay on the old one, giving developers time to flush out incompatibilities before the wider rollout.
