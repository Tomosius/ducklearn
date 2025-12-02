import re
import sys

py = sys.argv[1]
py_req = f">={py}"
py_ruff = "py" + py.replace(".", "")

# -------- Update pyproject.toml --------
with open("pyproject.toml") as f:
    text = f.read()

text = re.sub(r'requires-python = ".*"', f'requires-python = "{py_req}"', text)
text = re.sub(
    r'target-version = "py.*"', f'target-version = "{py_ruff}"', text
)
text = re.sub(r'python_version = ".*"', f'python_version = "{py}"', text)
text = re.sub(r'pythonVersion = ".*"', f'pythonVersion = "{py}"', text)

with open("pyproject.toml", "w") as f:
    f.write(text)

print(f"Updated pyproject.toml → Python {py}")
