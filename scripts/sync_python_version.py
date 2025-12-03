#!/usr/bin/env python3
"""
Synchronize Python version markers inside `pyproject.toml`.

This script extracts the current Python version from the running interpreter
(e.g., "3.12") and updates the following fields in `pyproject.toml`:

- `requires-python = ">=X.Y"`
- `tool.ruff.target-version = "pyXY"`
- `tool.mypy.python_version = "X.Y"`
- `tool.pyright.pythonVersion = "X.Y"`
- Python version classifier inside the `classifiers` list.

The script performs safe, regex-based replacements and ensures that old Python
version classifiers are removed before inserting the new one.

Usage:
    $ python scripts/sync_python_version.py

This script is intended to be run inside the project's conda environment,
typically through `make sync`.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Final


def get_python_version() -> tuple[str, str, str]:
    """
    Return the current Python version parts.

    Returns:
        A tuple of:
            - py: full "major.minor" string, e.g. "3.12"
            - py_req: version requirement string, e.g. ">=3.12"
            - py_ruff: ruff-style version string, e.g. "py312"
    """
    major: int = sys.version_info.major
    minor: int = sys.version_info.minor

    py: str = f"{major}.{minor}"
    py_req: str = f">={py}"
    py_ruff: str = f"py{major}{minor}"

    return py, py_req, py_ruff


def update_pyproject(text: str, py: str, py_req: str, py_ruff: str) -> str:
    """
    Apply all required regex substitutions to pyproject.toml.

    Args:
        text: The original contents of pyproject.toml.
        py: Python version "X.Y".
        py_req: Version requirement ">=X.Y".
        py_ruff: Ruff compatibility version "pyXY".

    Returns:
        The updated pyproject.toml text.
    """
    classifier_line: str = f'"Programming Language :: Python :: {py}"'

    # ---- Update requires-python ----
    text = re.sub(
        r'requires-python\s*=\s*".*?"',
        f'requires-python = "{py_req}"',
        text,
    )

    # ---- Update Ruff target-version ----
    text = re.sub(
        r'target-version\s*=\s*"py[0-9]+"',
        f'target-version = "{py_ruff}"',
        text,
    )

    # ---- Update Mypy python_version ----
    text = re.sub(
        r'python_version\s*=\s*".*?"',
        f'python_version = "{py}"',
        text,
    )

    # ---- Update Pyright pythonVersion ----
    text = re.sub(
        r'pythonVersion\s*=\s*".*?"',
        f'pythonVersion = "{py}"',
        text,
    )

    # ---- Remove old Python classifiers ----
    text = re.sub(
        r'"Programming Language :: Python :: [0-9]+\.[0-9]+"',
        "",
        text,
    )

    # ---- Insert new classifier ----
    text = re.sub(
        r"classifiers\s*=\s*\[",
        f"classifiers = [\n    {classifier_line},",
        text,
    )

    # ---- Cleanup accidental duplicates / blank lines ----
    text = re.sub(r",\s*,", ",", text)
    text = re.sub(r"\n\s*\n", "\n", text)

    return text


def main() -> None:
    """Main entry point for script."""
    pyproject_path: Final[Path] = Path("pyproject.toml")

    if not pyproject_path.exists():
        raise FileNotFoundError("pyproject.toml not found in project root.")

    py, py_req, py_ruff = get_python_version()
    original_text: str = pyproject_path.read_text(encoding="utf-8")

    updated_text: str = update_pyproject(original_text, py, py_req, py_ruff)
    pyproject_path.write_text(updated_text, encoding="utf-8")

    print(f"Updated pyproject.toml → Python {py}")


if __name__ == "__main__":
    main()
