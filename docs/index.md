# DuckLearn

DuckLearn is a lightweight, fast, **SQL-powered** machine learning toolkit built
on top of **DuckDB**, with APIs designed to feel familiar to users of
**pandas**, **NumPy**, and the **scikit-learn** ecosystem.

The project is intentionally developer-friendly:

- Fast, reproducible environments via **uv**
- One-command quality gates via **pre-commit**
- Strict typing via **Mypy** and **Pyright**
- Consistent formatting and linting via **Ruff**
- Documentation via **MkDocs Material**
- Conventional commits and versioning via **Commitizen**

> Status: pre-alpha — APIs will change.

---

## Quick start

### Install (runtime)

```bash
pip install ducklearn
```

### Clone and set up for development

```bash
git clone https://github.com/Tomosius/ducklearn
cd ducklearn

# Install all dependency groups (quality + tests + docs + workflow + release)
make dev
```

Run the full local quality gate (same as pre-commit):

```bash
make check
```

Run tests:

```bash
make test
```

Serve docs:

```bash
make docs-serve
```

---

## Requirements

- Python: **3.12–3.14** (matches `requires-python = ">=3.12,<3.15"`)
- `uv` installed (recommended): https://docs.astral.sh/uv/
- Git (for pre-commit hooks)

---

## Project layout

This repository uses the `src/` layout:

```text
src/
  ducklearn/
    __init__.py
tests/
pyproject.toml
uv.lock
Makefile
.pre-commit-config.yaml
mkdocs.yml
```

---

## Dependency groups (PEP 735)

Dependencies are organized into groups in `pyproject.toml`:

- `quality`: linters, type checkers, doc quality tools
- `tests`: pytest, coverage, hypothesis, etc.
- `docs`: mkdocs + plugins
- `workflow`: pre-commit, commitizen
- `release`: build/wheel tooling for packaging

In development, the recommended setup is installing all groups:

```bash
uv sync --all-groups
```

---

## The Makefile

The Makefile is the “front door” for day-to-day workflows. It is **uv-driven**
and intentionally mirrors what CI would do.

### Why this matters

- You run the same toolchain locally as CI.
- Everything is pinned via `uv.lock`.
- Pre-commit is the single orchestration layer for checks (consistent results).

### Targets

#### `make install`

Installs the **runtime environment** (default dependency set):

```bash
make install
```

Equivalent to:

```bash
uv sync
```

Use this if you only want to use DuckLearn (not develop it).

---

#### `make dev`

Installs the **full development environment** (all dependency groups) and
installs git hooks for pre-commit:

```bash
make dev
```

Equivalent to:

```bash
uv sync --all-groups
uv run pre-commit install
```

---

#### `make check`

Runs the **full pre-commit suite** across the entire repository:

```bash
make check
```

This is the canonical local “quality gate”. It runs:

- formatting/linting (Ruff)
- type checks (Mypy, Pyright)
- docstring coverage gate (Interrogate)
- and any other hooks configured in `.pre-commit-config.yaml`

If pre-commit modifies files (e.g., formatting), re-run `make check` until clean.

---

#### `make check-fast`

Runs pre-commit only on **currently staged files**:

```bash
make check-fast
```

This is the fastest loop when you are iterating on a small change.

---

#### `make fix`

Runs pre-commit across the repo, but **does not fail the Make target** (useful
for applying autofixes quickly):

```bash
make fix
```

This is a convenience “apply fixes then re-check” helper.

---

#### `make test`

Runs the test suite:

```bash
make test
```

Equivalent to:

```bash
uv run pytest
```

---

#### `make test-cov`

Runs tests with coverage output:

```bash
make test-cov
```

---

#### `make docs-serve`

Serves documentation locally with live reload:

```bash
make docs-serve
```

---

#### `make docs-build`

Builds the documentation site:

```bash
make docs-build
```

---

#### `make docs-deploy`

Deploys docs to GitHub Pages (requires appropriate repo permissions):

```bash
make docs-deploy
```

---

#### `make prerelease`

Runs a **multi-Python** matrix for pre-release confidence. This creates separate
environments per Python minor and runs checks + tests in each:

```bash
make prerelease
```

Internally it uses:

- `.venv-py3.12`
- `.venv-py3.13`
- `.venv-py3.14`

and runs:

- `pre-commit run --all-files`
- `pytest`

This is especially useful before tagging / publishing.

> Note: this does not replace CI, but it makes local validation very strong.

---

## Pre-commit (what runs in `make check`)

Pre-commit is configured in `.pre-commit-config.yaml`.

You can always run it directly:

```bash
uv run pre-commit run --all-files --show-diff-on-failure
```

Install hooks (done by `make dev`):

```bash
uv run pre-commit install
```

---

## Typing and style

DuckLearn aims for:

- Ruff formatting + lint rules
- Mypy strict typing
- Pyright strict mode
- Docstring coverage gate via Interrogate

If you see a failure, prefer fixing the underlying issue rather than weakening
the checks. If a rule is too strict for a valid reason, document the exception
and scope it narrowly (per-file ignore, or targeted config).

---

## Versioning and changelog (Commitizen)

Commitizen helps enforce conventional commits and can manage version bumps.

Typical flows:

Create an interactive conventional commit:

```bash
uv run cz commit
```

Bump version (updates project version + changelog if configured):

```bash
uv run cz bump
```

> Your exact Commitizen behavior is configured under `[tool.commitizen]` in
> `pyproject.toml`.

---

## Packaging and release

To build distribution artifacts (wheel + sdist):

```bash
uv run python -m build
```

### Do you need Twine?

Twine is typically used to **upload** built artifacts to PyPI:

```bash
uv run twine upload dist/*
```

If you publish via GitHub Actions / trusted publishing, you may not need Twine
locally. Keep it in `release` only if you actually upload from your machine.

---

## Git staging tips

To stage only **modified/deleted tracked files** (not new files), use:

```bash
git add -u
```

To stage specific files:

```bash
git add path/to/file1 path/to/file2
```

Avoid `git add -A` if you don’t want to add newly created files.

---

## License

DuckLearn is licensed under the **Apache License 2.0**.

See the `LICENSE` file for full text.

---

## Support / roadmap

If you spot gaps, rough edges, or want to propose a feature:

- open an issue on GitHub
- include a minimal reproducible example when reporting bugs
- include target audience and motivation for feature requests
