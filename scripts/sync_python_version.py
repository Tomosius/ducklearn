#!/usr/bin/env python3

import re
import sys
from pathlib import Path

# ----------------------------------------------------
# Detect current Python major.minor in this environment
# ----------------------------------------------------
major = sys.version_info.major
minor = sys.version_info.minor
py = f"{major}.{minor}"  # e.g. "3.12"
py_req = f">={py}"
py_ruff = "py" + py.replace(".", "")
classifier_line = f'"Programming Language :: Python :: {py}"'

path = Path("pyproject.toml")
text = path.read_text(encoding="utf-8")

# ----------------------------------------------------
# Update requires-python
# ----------------------------------------------------
text = re.sub(
    r'requires-python\s*=\s*".*?"',
    f'requires-python = "{py_req}"',
    text,
)

# ----------------------------------------------------
# Update ruff target-version
# ----------------------------------------------------
text = re.sub(
    r'target-version\s*=\s*"py[0-9]+"',
    f'target-version = "{py_ruff}"',
    text,
)

# ----------------------------------------------------
# Update mypy python_version
# ----------------------------------------------------
text = re.sub(
    r'python_version\s*=\s*".*?"',
    f'python_version = "{py}"',
    text,
)

# ----------------------------------------------------
# Update pyright pythonVersion
# ----------------------------------------------------
text = re.sub(
    r'pythonVersion\s*=\s*".*?"',
    f'pythonVersion = "{py}"',
    text,
)

# ----------------------------------------------------
# Clean & reinsert Python classifier
# ----------------------------------------------------

# Remove all old Python-version classifiers
text = re.sub(
    r'"Programming Language :: Python :: [0-9]+\.[0-9]+"',
    "",
    text,
)

# Insert correct one after the classifiers=[ line
text = re.sub(
    r"classifiers\s*=\s*\[",
    f"classifiers = [\n    {classifier_line},",
    text,
)

# Clean double commas, blank lines
text = re.sub(r",\s*,", ",", text)
text = re.sub(r"\n\s*\n", "\n", text)

path.write_text(text, encoding="utf-8")

print(f"Updated pyproject.toml → Python {py}")
