# Ch 10: Models and Migrations

## Table of Contents

- [1. Seeding the database](#1-seeding-the-database)
  - [1.1. Choosing a sample-data source](#11-choosing-a-sample-data-source)
  - [1.2. The `seed_database` command](#12-the-seed_database-command)
  - [1.3. Testing the command](#13-testing-the-command)
- [2. Factory Boy for data generation](#2-factory-boy-for-data-generation)
- [3. Migration safeguards](#3-migration-safeguards)
  - [3.1. Detecting pending migrations](#31-detecting-pending-migrations)
  - [3.2. `django-linear-migrations`](#32-django-linear-migrations)

## 1. Seeding the database

### 1.1. Choosing a sample-data source

- **Two possible sources** — production data (or a near-production copy) or generated data. Production data risks leaking sensitive customer info even after pseudonymization (correlations can re-identify users) and may be illegal under GDPR when an alternative exists.
- **Three formats for generated data** — SQL backups load fast but are tedious to update; Django **fixture files** are cross-database backups, easier to edit than SQL but still hard to maintain; **data generation code** via the ORM is flexible, adaptable, and easy to test, which makes it the recommended approach.

### 1.2. The `seed_database` command

- **Put the seeding code in a management command named `seed_database`** — sets up a fresh local DB in two steps: `./manage.py migrate` then `./manage.py seed_database`. Lives at `<app>/management/commands/seed_database.py` per Django's custom-management-command tutorial.
- **Wrap `handle()` in `@transaction.atomic`** — ensures a partial run leaves no rows behind if the command crashes, and lets the database batch writes for speed.
- **Guard against accidental production runs** — early in `handle()`, check `if Author.objects.exists()` (or any model that should be empty) and raise `CommandError` with an explanatory message. Django prints `CommandError` in red and exits non-zero, the idiomatic way to fail a management command.
- **Use `bulk_create()` for related batches** — wrapping `Book.objects.bulk_create([...])` in a small inner helper like `make_books(author, titles)` shortens the code and inserts many rows in a single query.
- **Update `Site` for the sites framework inside the command** — the framework's migration creates a default `Site`, so `seed_database` can update it (e.g., to `localhost:8000`) instead of using a separate data migration; safe because seeding only runs locally.

### 1.3. Testing the command

- **Wrap calls in a `call_command()` helper** — capture `stdout` and `stderr` via `StringIO` and return them for assertion. Use `assertRaisesMessage(CommandError, msg)` to verify the production-guard path.
- **Auto-detect missing models with `apps.get_app_configs()`** — loop over every project app's configs (filtered by name prefix to skip third-party/contrib apps), then loop over each `AppConfig.get_models()` and assert `model.objects.exists()`. Wrap each assertion in `subTest()` so one missing model doesn't mask others.
- **Maintain an `exempt_models` set** — listed as `(app_name, model_name)` tuples for models intentionally not seeded (e.g., `BookImport`, populated only by the real import pipeline). The error message names the offending model and points at this set, so adding a new model and forgetting to seed it produces a clear failure.

## 2. Factory Boy for data generation

- **Factories solve the tedium of populating many fields** — manually filling each model's fields scales poorly. A **factory** class fills fields with sensible defaults so you specify only the values that matter for the current call.
- **Two popular packages** — **Model Bakery** (Django-specific) and **Factory Boy** (general-purpose, with built-in Django support and **Faker** integration for plausible random strings). Factory Boy has more tools and is the author's recommendation despite a steeper setup.
- **Factory class shape mirrors a Django model** — subclass `DjangoModelFactory`, set the target model in inner `class Meta`, and declare each field. Place factories next to `models.py` as `<app>/factories.py` by convention. Example:

  ```python
  class AuthorFactory(DjangoModelFactory):
      class Meta:
          model = Author
      name = Faker("name")

  class BookFactory(DjangoModelFactory):
      class Meta:
          model = Book
      author = SubFactory(AuthorFactory)
      title = Faker("sentence")
  ```

- **`Faker("name")`, `Faker("sentence")`** — Factory Boy's `Faker` wraps Faker's locale-aware provider functions to generate plausible random strings; parameters can customize length etc.
- **`SubFactory` for foreign keys** — calling `BookFactory()` invokes `AuthorFactory` automatically, so the `Book` and its `Author` come together. Override sub-fields with Django-style double-underscore syntax: `BookFactory(author__name="Bruce Wayne")`.
- **Calling vs building** — `BookFactory()` returns a saved model instance (not a factory instance); `BookFactory.create_batch(5)` makes five at once; `BookFactory.build()` returns an unsaved instance with `id is None`, useful for tests that don't touch the database. `build_batch()` mirrors this.
- **In tests, factories collapse setup** — `BookFactory()` replaces a four-line `Author.objects.create(...)` + `Book.objects.create(...)` setup, dropping irrelevant field values. Pairs well with `setUpTestData()` for shared fixtures.
- **In `seed_database`, factories shrink the command** — `AuthorFactory.create_batch(2)` and `BookFactory.create_batch(5, author=author2)` replace the hand-written author/title lists; override fields when you want realistic values.
- **More features for advanced cases** — `SelfAttribute` for fields that reference each other, `RelatedFactory` for many-to-many, `Sequence` for counter-based fields, `django_get_or_create` to reuse existing rows.

## 3. Migration safeguards

### 3.1. Detecting pending migrations

- **Why this matters** — Django requires migrations for every model field and `Meta` change, even non-DB ones like `Field.choices`. Forgetting a migration can ship code that crashes on deploy.
- **`makemigrations --dry-run --check`** — `--dry-run` skips writing files; `--check` exits non-zero if any migration would be generated. Together they succeed when migrations are up-to-date and fail with a report when they aren't.
- **Run it as a unit test, not just CI** — a `PendingMigrationsTests.test_no_pending_migrations` test calls `call_command("makemigrations", "--dry-run", "--check", ...)`, catches the `SystemExit` raised on failure, and re-raises it as `AssertionError("Pending migrations:\n" + out.getvalue())` (with `from None` to hide the noise). Captures `stdout`/`stderr` via `StringIO` so successful runs stay quiet. Copy-paste-ready into any project.

### 3.2. `django-linear-migrations`

- **Merge migrations are Django's fix for branched histories** — when two branches each add a `0002_*` migration to the same app, `migrate` fails with `Conflicting migrations detected; multiple leaf nodes...`, and `makemigrations --merge` creates a `0003_merge` that depends on both leaves.
- **Three problems with merge migrations:**
  1. *Reactive, not preventive.* You only learn about the conflict after merging to main and breaking CI; team progress stalls until someone commits the merge migration. In an active small team, this can fire several times per week.
  2. *Inconsistent execution order across environments.* Staging may run the migrations in commit order while production runs them in the merge migration's declared order — particularly dangerous with `RunSQL` / `RunPython` operations, and erodes staging's value as a production proxy.
  3. *Harder rollbacks.* Reverse-migrating may need per-environment inspection because the order isn't uniform.
- **`django-linear-migrations` enforces a linear history** — written by the author after seeing many in-house versions of the same idea. Every app keeps a `max_migration.txt` file (auto-updated by `makemigrations`) holding the name of its latest migration. When two branches each touch it, Git produces a **merge conflict** on `max_migration.txt`, forcing the developer to reorder migrations linearly *before* merging. Compatible with apps that already contain historical merge migrations — it enforces linearity from install onwards.
- **`rebase_migration` command** — ships with the package; for simple cases, automates editing the new migration's `dependencies` and `max_migration.txt` to make the history linear again.
