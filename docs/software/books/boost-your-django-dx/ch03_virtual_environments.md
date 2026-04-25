# Ch 3: Virtual Environments and Dependencies

## Table of Contents

- [1. Tool philosophy](#1-tool-philosophy)
- [2. Creating and activating environments](#2-creating-and-activating-environments)
  - [2.1. venv](#21-venv)
  - [2.2. virtualenv](#22-virtualenv)
- [3. Pinning dependencies with pip-compile](#3-pinning-dependencies-with-pip-compile)
- [4. Keeping environments in sync with pip-lock](#4-keeping-environments-in-sync-with-pip-lock)
- [5. Dependency management practices](#5-dependency-management-practices)
- [6. Python's development mode](#6-pythons-development-mode)

## 1. Tool philosophy

- **Stick to default tools** — the author prefers venv + Pip over Conda, Poetry, or Pipenv because every Python developer already knows them, Pip covers more edge cases as the universal installer, and fewer layers means fewer things to debug when an environment breaks.
- **Always invoke Pip via `python -m pip`** — bare `pip` can resolve to a different Python than the active one, silently installing packages into the wrong environment. `python -m pip` always targets the active interpreter. Make permanent with `alias pip='python -m pip'` in `~/.bashrc` / `~/.zshrc`.

## 2. Creating and activating environments

### 2.1. venv

- **Snazzy create command** — `python -m venv --prompt . --upgrade-deps .venv`. `--prompt .` sets the shell prompt label to the current directory name; `--upgrade-deps` upgrades Pip inside the env so commands stop nagging about new releases; `.venv` is the conventional hidden directory name (auto-detected by VS Code and PyCharm).
- **Don't commit virtual environments** — they aren't source you control, aren't portable across machines, and bloat the repo. Add `/.venv/` to `.gitignore`. From Python 3.13 onward, venv writes a `.gitignore` inside the env automatically (copied from virtualenv via CPython issue #108125).
- **Remove an accidentally committed venv** — `git rm -r --cached .venv` after adding the gitignore rule; files stay on disk but Git stops tracking them.
- **Activation prepends `bin/` to `PATH`** — running `source .venv/bin/activate` (or the shorter `. .venv/bin/activate`) makes `python` and installed tools resolve inside the env. `deactivate` reverses it. The author rarely deactivates — opens a new terminal tab per project instead, isolating env vars too.

| Platform | Shell | Activate command |
|----------|-------|------------------|
| POSIX | Bash/Zsh | `. .venv/bin/activate` |
| POSIX | fish | `source .venv/bin/activate.fish` |
| POSIX | csh/tcsh | `source .venv/bin/activate.csh` |
| POSIX | PowerShell Core | `.venv/bin/activate.ps1` |
| Windows | cmd.exe | `.venv\Scripts\activate.bat` |
| Windows | PowerShell | `.venv\Scripts\Activate.ps1` |

### 2.2. virtualenv

- **virtualenv vs. venv** — virtualenv is the original third-party tool that was copied into the stdlib as venv in Python 3.3 (PEP 405). venv has stagnated; virtualenv kept evolving. Roughly 10x faster (~0.3s vs. ~3s), seeds the env with a recent cached Pip, and writes its own `.gitignore`. Worth installing if you create envs frequently: `python -m pip install virtualenv` then `python -m virtualenv --prompt . .venv`. Activate exactly like venv.

## 3. Pinning dependencies with pip-compile

- **Why `pip freeze > requirements.txt` is risky** — the freeze output mixes top-level and transitive dependencies with no way to tell which is which; new direct deps don't auto-pin their transitives; editing a version doesn't recompute transitives. Result: silent breakage from drifted transitive versions.
- **Two-file pattern** — keep `requirements.in` (your direct deps, mostly unconstrained) and generate `requirements.txt` (every package pinned, with `# via` annotations explaining each). Same idea npm and Cargo use. Commit both.
- **`pip-compile`** — ships in the `pip-tools` package (`python -m pip install pip-tools`). Reads `requirements.in`, resolves the full dependency graph, writes a fully pinned `requirements.txt` with a header comment and `# via` annotations showing why each package is included.
- **Version constraints in `requirements.in`** — leave most packages unconstrained; add ranges (e.g., `django>=5.0,<5.1`) only for large/hard-to-upgrade packages.
- **Add a dependency** — append to `requirements.in`, run `pip-compile`, then `python -m pip install -r requirements.txt`. Don't edit `requirements.txt` by hand on pip-compile projects.
- **Remove a dependency** — delete from `requirements.in`, run `pip-compile`, then `python -m pip uninstall <pkg>`. For bulk cleanup use `pip-sync --ask`, which adds, upgrades, and removes packages to exactly match `requirements.txt` (warning: it uninstalls anything not listed, including dev extras).
- **Upgrade flags** — `pip-compile -P <pkg>` (`--upgrade-package`) bumps one package; `-P 'asgiref<3.8'` adds an extra constraint; `pip-compile -U` (`--upgrade`) bumps everything compatible with `requirements.in` constraints. Even when not upgrading wholesale, `-U` is useful for splitting upgrades into chunks via `git add --patch`.
- **Converting an existing `requirements.txt`** — back up as `requirements.txt.orig`, write your guess of top-level deps into `requirements.in`, copy the backup back over `requirements.txt` (so pip-compile reuses pinned versions instead of upgrading), run `pip-compile --no-header --no-annotate` for a diffable output, compare against the backup, loop until everything important is accounted for, then re-run plain `pip-compile` for the final annotated file.

## 4. Keeping environments in sync with pip-lock

- **The drift problem** — every `requirements.txt` change risks silent `ModuleNotFoundError`s on teammates' machines until they reinstall. Wasted debugging time multiplied by team size.
- **`pip-lock`** — a universal package providing `check_requirements()`, which compares the current env against `requirements.txt` and exits with a clear "run `python -m pip install -r requirements.txt`" message if they differ. Wire it into `manage.py` so every Django command checks first.

## 5. Dependency management practices

- **One requirements file is usually enough** — splitting into base + dev requirements adds overhead, risks version mismatch between environments, and rarely pays off. Pre-commit (covered later) already isolates lint/format tools, and "dev-only" tools like profilers occasionally help in production. `pip-compile-multi` exists if you genuinely need multiple files.
- **Well Maintained Test** — twelve yes/no questions the author uses to gauge whether a package is safe to depend on: production-ready claim, sufficient docs, a changelog, responsive bug reports, sufficient tests, tests on the latest language version, tests on the latest integration version, CI configured, CI passing, well used, commit in last year, release in last year. No hard pass/fail — a guide for judgment, and each "no" is a contribution opportunity.
- **Schedule regular upgrades** — author's analogy: dependency upgrades are like washing dishes — defer too long and they consume all your time. Suggested cadence: every 2–4 weeks on medium teams; relaxed on small teams; continuous on the largest. Calendar the big ones: Python releases yearly in October, Django every 8 months (every third is LTS, version ending `.2`), PostgreSQL yearly around October.
- **Don't bother sticking to Django LTS** — non-LTS feature releases are equally stable, just shorter-supported. Upgrading each feature release keeps the upgrade muscle warm and avoids one giant risky jump.

## 6. Python's development mode

- **Development mode (Python 3.7+)** — opt-in mode that surfaces classes of bugs Python normally hides during dev, at a small runtime cost. Enables `DeprecationWarning` / `PendingDeprecationWarning` (catches use of soon-to-be-removed Django/library APIs), `ImportWarning` (likely import mistakes), `ResourceWarning` (leaked files/sockets), the `faulthandler` module (dumps tracebacks on segfaults), C-level debug hooks for extensions, and `asyncio` debug mode (must-have for async views and Channels — flags missing `await`s).
- **Two ways to enable** — `python -X dev manage.py runserver` for one-off use (alias as `pydev='python -X dev'`), or set `PYTHONDEVMODE=1` in the shell or `~/.bashrc` / `~/.zshrc` for permanent use. `.env` files generally don't work because Django loads them after Python has started, and dev mode can't be enabled retroactively.
- **Verify** — `python -c 'import sys; print(sys.flags.dev_mode)'` reads the underlying `sys.flags` and prints `True` when active.
- **Where to use it** — at minimum, enable on CI for the bug-catching benefit; locally it's usually worth the noise, though warnings from third-party tools you can't fix may be distracting. A later chapter shows a Django system check to enforce it.
