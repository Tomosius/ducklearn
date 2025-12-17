## DuckLearn Code Style Guide

### Introduction

DuckLearn follows strict, professional, and explicit coding rules to
ensure maintainability, readability, and reliability across the entire
project. This guide applies to **Python**, **SQL**, **SQLGlot**,
**Markdown**, and **YAML**. It fully aligns with the tooling configured
in `pyproject.toml`: ruff, mypy, pylint, pyright, vulture, and pytest.

---

## 1. Python Coding Standards

### 1.1 Line Length

- Maximum: **79 characters**
- Applies to code, docstrings, comments, examples

### 1.2 Naming Conventions

- Use full, descriptive names everywhere.
- Only scikit-learn compatibility methods may use short names:
    - `fit`, `transform`, `fit_transform`
    - `get_params`, `set_params`

Examples:

| Avoid    | Prefer                        |
|----------|-------------------------------|
| df       | input_dataframe               |
| vals     | transformed_values            |
| sql_expr | sql_transformation_expression |

### 1.3 Docstrings

- Required for all public modules, classes, methods, functions.
- Google or NumPy style acceptable.
- Must document: Purpose, Args, Returns, Raises, Examples.

### 1.4 Inline Comments

- Required for non-obvious logic.
- Must be complete sentences.
- Avoid explaining the obvious.

### 1.5 Imports

- Order:
    1. Standard library
    2. Third‑party
    3. Local modules
- Alphabetical within each group.

### 1.6 Typing Rules

- Full type annotations required.
- Mypy strict mode enforced:
    - No untyped definitions
    - No incomplete types
    - No unnecessary ignores
    - Warn on unreachable code

---

## 2. SQL Coding Standards

### 2.1 Line Length

- Soft max: 90 characters
- Prefer readable multi-line formatting

### 2.2 Naming

- Raw SQL: UPPERCASE keywords
- SQLGlot: lowercase keywords (tooling requirement)
- Identifiers: snake_case

### 2.3 Query Style

- Use explicit JOIN
- Always alias tables
- Avoid SELECT *

---

## 3. SQLGlot Conventions

### 3.1 AST Construction

- Prefer programmatic AST building
- Avoid raw SQL strings unless necessary

### 3.2 Naming

- Use fully descriptive variable names

---

## 4. Markdown Conventions

### 4.1 Structure

- Only one H1 per file
- Proper hierarchy: H1 → H2 → H3

### 4.2 Line Length

- Aim for ≤ 80 characters (text only)

### 4.3 Lists

- Unordered lists for unordered concepts
- Ordered lists when order matters

---

## 5. YAML Conventions

### 5.1 Formatting

- 2-space indentation
- Snake_case keys
- Maximum line length: 79 characters

### 5.2 Comments

- Clarify configuration intent
- Avoid long inline comments

---

## 6. General Engineering Principles

#### 6.1 Explicit > Implicit

No magic behavior.

#### 6.2 One Responsibility per Function

Functions should stay small and clear.

#### 6.3 DRY (but not too DRY)

Avoid unnecessary abstraction.

#### 6.4 Fail Loudly

Raise informative exceptions early.

#### 6.5 Avoid Side Effects

Ensure predictable, deterministic behavior.

---

## 7. Compatibility Rules

### 7.1 Scikit-Learn API

The following methods must always exist on DuckLearn transformers:

- fit
- transform
- fit_transform
- get_params
- set_params

### 7.2 Linter/Formatter Compatibility

All code must pass:

- ruff (lint + format)
- pylint
- mypy
- pyright
- docformatter
- vulture
- pytest

---

## 8. Summary

This guide ensures:

- Clean, consistent, maintainable code
- Fully typed, fully linted, fully documented implementations
- SQL and SQLGlot consistency
- Predictable API behavior
- Easy onboarding for contributors

Always follow this guide before committing or reviewing code.
