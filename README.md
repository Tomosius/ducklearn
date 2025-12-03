# DuckLearn

A lightweight, fast, SQL-powered machine learning toolkit built on top of **DuckDB**, **pandas**, **NumPy**, and **scikit-learn**.

DuckLearn is designed for:

- 🔥 High-performance data processing (backed by DuckDB)
- 🧠 ML workflows that stay close to SQL and dataframe principles
- 🧪 Fast experimentation & interactive notebooks
- 📦 A clean, typed API with automatic documentation
- 🧰 Modern development tooling (Pixi, Ruff, Mypy, Commitizen, MkDocs)

---

## 🚀 Features

- **DuckDB-accelerated ML pipelines**
- **Pandas-first API**, compatible with scikit-learn
- Automatic documentation powered by **MkDocs Material**
- Full CI-quality static analysis locally via Pixi
- Strict typing (Pyright + Mypy)
- Excellent developer experience (Pixi tasks, Commitizen, precommit tools)

---

## 🛠 Installation

### 1. Install DuckLearn

```bash
pip install ducklearn
```

### 2. Development Setup (Recommended — uses Pixi)

Install Pixi:

```bash
curl -fsSL https://pixi.sh/install.sh | bash
```

Clone repository:

```bash
git clone https://github.com/Tomosius/ducklearn
cd ducklearn
```

Create environment:

```bash
pixi install
pixi shell
```

---

# 🧠 IDE Support

## PyCharm Integration

Detailed instructions:
<https://pixi.sh/v0.22.0/ide_integration/pycharm/>

Summary:

1. Install the **Pixi plugin** in PyCharm
2. Open **Settings → Project → Python Interpreter**
3. Select **Pixi Environment**
4. Choose the `ducklearn` environment

---

# 📚 Documentation

DuckLearn uses **MkDocs Material**.

Serve docs locally:

```bash
pixi run docs-serve
```

Build docs:

```bash
pixi run docs-build
```

Deploy docs (GitHub Pages):

```bash
pixi run docs-deploy
```

---

# 🧪 Tests

```bash
pixi run test
```

---

# 🧹 Code Quality

Run all static analysis tools:

```bash
pixi run fullcheck
```

Includes:

- Ruff (lint + format)
- Pyright (type check)
- Mypy (strict)
- Pylint
- SQL validator
- pip-audit
- Bandit
- Vulture

---

# 📝 Conventional Commits

DuckLearn uses Commitizen.

```bash
pixi run commit
```

Version bump:

```bash
pixi run bump
```

Changelog:

```bash
pixi run changelog
```

---

# 📦 License

MIT License © Tomas Pecukevicius