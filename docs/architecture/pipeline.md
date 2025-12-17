# DuckLearn Pipeline Design

## Overview

DuckLearn pipelines define a deterministic, SQL-native sequence of
transformations that operate entirely within a relational engine such as
DuckDB. Unlike scikit-learn pipelines, DuckLearn pipelines do not operate
on NumPy arrays but instead construct a **CTE-based SQL graph**.

A pipeline is:

- Lazy (builds SQL, does not execute)
- Immutable (each step produces a new SQL AST)
- Fully traceable (debuggable SQL)
- Engine-agnostic (SQLGlot translation layer)

---

# 1. Pipeline Philosophy

DuckLearn pipelines follow three principles:

### 1. Predictability

Every pipeline step must produce a reproducible SQL transformation.

### 2. Transparency

Users can inspect or print SQL at any stage.

### 3. Compatibility

Pipelines respect scikit-learn conventions but extend them into SQL.

---

# 2. Pipeline Structure

A pipeline is composed of **ordered named steps**, for example:

```python
Pipeline(
    [
        ("selector", ColumnSelector(columns=["a", "b"])),
        ("scale", StandardScaler()),
        ("encode", OneHotEncoder())
        ]
    )
```

Each step implements:

- `fit()`
- `transform()`

And returns SQL AST nodes.

---

# 3. Execution Model

Internally:

1. Each step receives a SQLGlot expression representing the current table.
2. It produces a new SQLGlot expression.
3. The pipeline assembles these expressions into a **CTE graph**.
4. Execution occurs only at:
    - `execute()`
    - `to_dataframe()`
    - `to_arrow()`

---

## 3.1 Example CTE Graph

```
WITH
    step_00 AS (SELECT * FROM raw_input),
    step_01 AS (SELECT col1, col2_normalized AS col2 FROM step_00),
    step_02 AS (... FROM step_01),
    step_03 AS (... FROM step_02)
SELECT * FROM step_03;
```

Each pipeline step maps to exactly one CTE.

---

# 4. Fit / Transform Behavior

### `fit()`

- Computes metadata (e.g., min/max, categories)
- Does **not** modify SQL

### `transform()`

- Emits SQLGlot expressions using learned metadata

### `fit_transform()`

- Equivalent to scikit-learn semantics

---

# 5. Partial Pipelines

DuckLearn supports:

- Returning SQL for an intermediate step
- Inspecting AST of any step
- Debugging individual transformers

Example:

```python
pipeline.get_step_sql("scale")
```

---

# 6. Validation Rules

Pipeline construction enforces:

- Unique step names
- Each step must be a TransformerMixin subclass
- Order preserved
- Learned attributes must end in `_`
- Transformers must not mutate the incoming expression

---

# 7. Error Handling

The pipeline raises explicit errors:

| Error Type           | Condition                                |
|----------------------|------------------------------------------|
| MissingColumnError   | transform references nonexistent columns |
| InvalidStepError     | step is not a transformer                |
| FitRequiredError     | transform before fit                     |
| EngineExecutionError | SQL engine rejects generated SQL         |

---

# 8. Future Enhancements

- Branching pipelines (DAG, not just linear)
- Hyperparameter search integration
- Optimized SQL fusion (combine compatible CTEs)
- Visual pipeline graph export

---

# Summary

DuckLearn pipelines:

- Build SQL lazily
- Represent transformations as a CTE graph
- Maintain strict sklearn-compatible behavior
- Provide full introspection and debuggability
- Serve as the backbone of the DuckLearn execution model

This file defines how pipelines should be implemented and extended across
the DuckLearn project.
