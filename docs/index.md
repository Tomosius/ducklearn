
---
title: DuckLearn111
hide:
  - title
---

# DuckLearn

DuckLearn is a **SQL-first machine learning toolkit powered by DuckDB**.

It’s designed for people who like:

- writing **clean SQL** instead of opaque black-box pipelines  
- keeping data **inside DuckDB** instead of constantly round-tripping through pandas  
- having an API that still *feels* like scikit-learn (estimators, pipelines, fit/transform)

---

## What DuckLearn gives you

- 🚀 **Fast analytics with DuckDB**  
  Push as much work as possible down into DuckDB’s query engine.

- 🧠 **SQL-driven estimators**  
  Write estimators in pure SQL using a tiny base class (`SQLDuckEstimator`) and a simple convention:
  - `fit_sql(...)` → SQL that learns parameters (e.g. mean, std, categories)
  - `transform_sql(...)` → SQL that applies the learned parameters
  - `predict_sql(...)` → SQL that produces predictions

- 🔗 **Pipeline-style composition**  
  Chain multiple SQL transformers/estimators together, just like scikit-learn pipelines, but the “glue” between steps is SQL instead of in-memory pandas operations.

- 🧪 **Friendly with pandas / numpy / sklearn**  
  DuckLearn is meant to complement the existing Python ML stack, not replace it. Use DuckDB + SQL where it’s fast and convenient, fall back to pandas/numpy/sklearn where it makes sense.

- 🧬 **Type-annotated, minimal, and extensible**  
  The codebase is intentionally small and strongly typed, so you can:
  - read the source,
  - copy patterns,
  - and easily build your own custom SQL transformers.

---

## Core ideas

### 1. SQL-first estimators

Every SQL estimator inherits from `SQLDuckEstimator` and implements:

- `fit_sql(self, sql: str, cte: str | None = None) -> str | None`
- `transform_sql(self, sql: str, cte: str | None = None) -> str`
- `predict_sql(self, sql: str) -> str`

Inside these methods you use a special placeholder:

```sql
SELECT ...
FROM (__input__)
```

`(__input__)` is replaced by DuckLearn with the upstream step’s SQL, wrapped as a subquery. That’s how multiple steps chain together.

Learned parameters can be defined via **SQLExpr**:

```python
from ducklearn.base import SQLDuckEstimator, SQLExpr

class MeanStdScalerSQL(SQLDuckEstimator):
    def __init__(self, column: str = "x") -> None:
        super().__init__()
        self.column = column
        self.mean: float | None = None
        self.std: float | None = None

    def fit_sql(self, sql: str, cte: str | None = None) -> str:
        col = self.column

        # describe how to compute fit parameters in SQL
        self.mean = SQLExpr(f"SELECT AVG({col}) AS mean FROM (__input__)")
        self.std = SQLExpr(f"SELECT STDDEV_POP({col}) AS std FROM (__input__)")

        # return one representative SQL template (for inspection / translation)
        return self.mean.sql

    def transform_sql(self, sql: str, cte: str | None = None) -> str:
        col = self.column
        return f"""
        SELECT
            *,
            ({col} - {self.mean}) / NULLIF({self.std}, 0) AS {col}_scaled
        FROM (__input__)
        """.strip()

    def predict_sql(self, sql: str) -> str:
        return self.transform_sql(sql)
```

DuckLearn will:

- collect `SQLExpr` objects assigned during `fit_sql`,
- execute the corresponding SQL against DuckDB,
- store back the **Python** values (e.g. `self.mean = 4.2`),
- and keep the original SQL templates for translation / debugging.

For purely constant parameters (e.g. “always fill with 10”), you can skip `fit_sql` entirely and just set them in `__init__`.

---

### 2. Static vs dynamic fits

Some fit queries are **static** (global aggregates like `AVG(col)` returning one row), and some are **dynamic** (e.g. `SELECT DISTINCT col` whose output size depends on the data).

DuckLearn includes an **inspector** that looks at the SQL AST (via `sqlglot`) and classifies fit queries as static or dynamic. This helps the pipeline decide:

- which fits can be pre-computed and reused safely, and  
- which fits depend heavily on the input data and should be treated dynamically.

You don’t have to think about that most of the time, but it’s there under the hood.

---

### 3. Extending DuckLearn

You can create your own transformers/estimators in two ways:

1. **Parameter-only (no fit SQL)**  
   Just store values in `__init__` and use them in `transform_sql`:

   ```python
   class ConstantImputerSQL(SQLDuckEstimator):
       def __init__(self, column: str, fill_value: float | int = 0) -> None:
           super().__init__()
           self.column = column
           self.fill_value = fill_value

       def transform_sql(self, sql: str, cte: str | None = None) -> str:
           col = self.column
           val = self.fill_value
           return f"""
           SELECT
               *,
               COALESCE({col}, {val}) AS {col}
           FROM (__input__)
           """.strip()

       def predict_sql(self, sql: str) -> str:
           return self.transform_sql(sql)
   ```

2. **Learned-from-data (with fit SQL)**  
   Use `SQLExpr` in `fit_sql` to compute parameters from the data, then use them in `transform_sql`, like the `MeanStdScalerSQL` above.

A more detailed “How to write custom transformers” guide will live on its own page.

---

## Installation

```bash
pip install ducklearn
```

(For DuckDB itself, you can either use the `duckdb` Python package directly or let DuckLearn work with an existing DuckDB connection in your project.)

---

More docs are coming: end-to-end examples, pipelines, and recipes for common transformers (imputers, scalers, encoders, etc.). In the meantime, the codebase is small enough that reading it is encouraged. 😄
