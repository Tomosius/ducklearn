import re
import sys

py = sys.argv[1]  # e.g. "3.12"
py_req = f">={py}"
py_ruff = "py" + py.replace(".", "")
classifier_line = f'"Programming Language :: Python :: {py}"'

with open("pyproject.toml", encoding="utf-8") as f:
    text = f.read()

# -----------------------------
# Update requires-python
# -----------------------------
text = re.sub(
    r'requires-python\s*=\s*".*?"',
    f'requires-python = "{py_req}"',
    text,
)

# -----------------------------
# Update ruff target-version
# -----------------------------
text = re.sub(
    r'target-version\s*=\s*"py[0-9]+"',
    f'target-version = "{py_ruff}"',
    text,
)

# -----------------------------
# Update mypy python_version
# -----------------------------
text = re.sub(
    r'python_version\s*=\s*".*?"',
    f'python_version = "{py}"',
    text,
)

# -----------------------------
# Update pyright pythonVersion
# -----------------------------
text = re.sub(
    r'pythonVersion\s*=\s*".*?"',
    f'pythonVersion = "{py}"',
    text,
)

# -----------------------------
# Update classifiers (safe)
# -----------------------------

# 1. Remove all Python-version classifiers
text = re.sub(
    r'"Programming Language :: Python :: [0-9]+\.[0-9]+"',
    "",
    text,
)

# 2. Insert correct version ONE time
text = re.sub(
    r"classifiers = \[",
    f"classifiers = [\n    {classifier_line},",
    text,
)

# 3. Cleanup accidental double commas / blank lines
text = re.sub(r",\s*,", ",", text)
text = re.sub(r"\n\s*\n", "\n", text)

# Save file
with open("pyproject.toml", "w", encoding="utf-8") as f:
    f.write(text)

print(f"Updated pyproject.toml → Python {py}")
