# Ch 4: Python Shell

## Table of Contents

- [1. Django's `shell` command](#1-djangos-shell-command)
- [2. IPython basics](#2-ipython-basics)
  - [2.1. Help and autocomplete](#21-help-and-autocomplete)
  - [2.2. Input and output history](#22-input-and-output-history)
  - [2.3. Pasting code](#23-pasting-code)
- [3. Iterative development with autoreload](#3-iterative-development-with-autoreload)
- [4. Embedding and debugging](#4-embedding-and-debugging)
- [5. Benchmarking with `%timeit`](#5-benchmarking-with-timeit)
- [6. Production safety with django-read-only](#6-production-safety-with-django-read-only)

## 1. Django's `shell` command

- **`./manage.py shell`** — starts a Python REPL pre-configured with your Django project, so models, caches, and settings are reachable. Defaults to the stdlib shell (`>>>`); auto-upgrades to IPython or bpython if installed (preferring IPython).
- **`-c '<code>'`** — runs a code string and exits without launching the interactive prompt. Strings can span multiple lines on Bash/Zsh; otherwise use `;` separators. Useful inside shell scripts.
- **`-c 'import t'` pattern** — when inline `-c` code grows unwieldy, save it as `t.py` ("test"/"temporary") and run `./manage.py shell -c 'import t'`. Module-level code executes on import. Tracebacks show the file and line; piping with `< t.py` works but obscures source location in stack traces (fixed in Python 3.13).

## 2. IPython basics

- **IPython** — enhanced Python REPL with syntax highlighting, advanced autocomplete, and **magic commands** (lines starting with `%`). Spawned the Jupyter Notebook project, where it powers the Python kernel. Install it (`python -m pip install ipython`) and Django's `shell` picks it up automatically. Prompt changes from `>>>` to `In [1]:`.

### 2.1. Help and autocomplete

- **`?` and `??`** — typing `name?` shows type, signature, and docstring (an upgraded `help()`); `name??` adds the source code. Bare `?` opens the IPython help page in your pager (usually `less`); `%quickref` prints a cheat sheet.
- **Tab autocomplete** — completes attribute names after `.`, hides underscore-prefixed names unless you type `_` first. Filters by characters typed so far, inserts the longest common prefix when ambiguous, and inspects sub-expression types — including completing dictionary keys, e.g., `d["us<tab>` expands to `d["user_count`.

### 2.2. Input and output history

- **`Out` dictionary** — IPython caches every result by line number, so `Out[1]` retrieves any earlier value (the stdlib shell only keeps the last in `_`). Shortcut form `_<n>` (e.g., `_1`) is equivalent. Saves copy-pasting between cells.
- **`In` dictionary** — caches the source strings of past inputs, accessed as `In[1]` or `_i1`. Less directly useful, but it's the data magic commands read.
- **`%hist` / `%history`** — prints prior input lines without prompts, ideal for copying a session into a file.
- **`%rerun <n1> <n2> ...`** — re-executes specific past lines in the order given.

### 2.3. Pasting code

- **Multi-line paste detection** — IPython treats a paste as one block, so blank lines inside a function don't terminate it (the stdlib shell raises `IndentationError` in that situation).
- **`%cpaste`** — opens a paste prompt that ends when you type `--` on its own line (or Ctrl-D). Useful for very large code blocks, especially when SSH'd into a remote `manage.py shell` — edit locally, paste remotely.

## 3. Iterative development with autoreload

- **`%load_ext autoreload` + `%autoreload 2`** — IPython extension that re-imports your modules before every prompt, so edits take effect without restarting the shell. Works for both `import eggs` and `from eggs import x`. Massive time-saver during incremental coding.
- **`%autoreload 1`** — stricter mode: only modules explicitly marked with `%aimport <module>` get reloaded. Use this when level 2 misbehaves.
- **Reloading caveats** — Python module reloads have side effects.
  - **Registry patterns** — modules that register callbacks at import time (e.g., Django admin classes, `atexit` handlers) re-register on each reload, which can fire callbacks repeatedly.
  - **Model classes** — Django stores models in a registry at definition time; reloading a models module triggers `RuntimeWarning: Model 'example.author' was already registered. Reloading models is not advised...`. Fine for one model in one module; risky when iterating across many models.

## 4. Embedding and debugging

- **`import IPython; IPython.embed()`** — drops an IPython prompt at any point in your code, with full access to local variables. Great inside a view or management command for ad-hoc exploration; `exit` resumes the original code. Useful when autoreload doesn't fit your workflow. Save as an editor macro.
- **`runserver` interaction** — embedded shells can collide with `runserver`'s threading and autoreloading. When using `IPython.embed()` inside a view, run `./manage.py runserver --nothreading --noreload` to avoid concurrent re-entry and file-change restarts mid-session.
- **`%debug`** — IPython magic that opens IPython's pdb-extended debugger at the line where the last exception was raised. Adds syntax highlighting and autocomplete on top of standard `pdb`.
- **`ipdb` outside IPython** — install the `ipdb` package and set `PYTHONBREAKPOINT=ipdb.set_trace` so plain `breakpoint()` calls anywhere in the project open IPython's debugger instead of `pdb`. Wire it via `os.environ.setdefault("PYTHONBREAKPOINT", "ipdb.set_trace")` in `manage.py`.
- **`--pdb` integration** — Django's test runner `--pdb` flag auto-uses `ipdb` when installed. For pytest, set `addopts = --pdbcls=IPython.terminal.debugger:TerminalPdb` in `pytest.ini`.
- **pdb++** — third-party `pdbpp` package, an even more featureful drop-in for pdb that some prefer over IPython's debugger.

## 5. Benchmarking with `%timeit`

- **`%timeit <expr>`** — IPython magic that auto-determines a sensible loop count and reports mean ± std. dev. with units (e.g., `36.5 ns ± 0.0944 ns per loop`). Cleaner than the stdlib `timeit.timeit("...", number=...)` which forces a guessed count and outputs raw seconds.
- **Concrete finding** — `%timeit dict()` ≈ 36.5 ns vs. `%timeit {}` ≈ 16.7 ns; `{}` skips the name lookup `dict()` requires (since `dict` could be locally rebound).

## 6. Production safety with django-read-only

- **The risk** — running `manage.py shell` in production accelerates feature work, migrations, and backfills, but it's easy to mix up terminal sessions and run a destructive command meant for dev. Multiplied across team and time, accidents become near-inevitable.
- **django-read-only** — package providing a read-only DB mode. Add `"django_read_only"` to `INSTALLED_APPS`, then either set `DJANGO_READ_ONLY = True` in settings or export the `DJANGO_READ_ONLY` env var. Writes raise `DjangoReadOnlyError: Write queries are currently disabled. Enable with django_read_only.enable_writes().`
- **Escape hatches** — `django_read_only.enable_writes()` / `disable_writes()` toggle interactively, and the `temp_writes()` context manager re-enables writes only for a `with` block. Recommended setup: export `DJANGO_READ_ONLY=1` in the production shell's `.bashrc` / `.zshrc` so the protection is on by default.
