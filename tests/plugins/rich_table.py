# tests/plugins/rich_table.py
from __future__ import annotations

STATUS_COLUMNS = ["passed", "failed", "error", "skipped", "xfail", "xpass"]
NUM_W = 5
SUBTOTAL_W = 8
COLOR = {
    "header": "bold",
    "filepath": "cyan",
    "func": "bright_cyan",
    "passed": "green",
    "failed": "red",
    "error": "red",
    "skipped": "yellow",
    "xfail": "yellow",
    "xpass": "yellow",
    "subtotal": "magenta",
    "total": "bold",
}
_records: list[tuple[str, str, str]] = []

# ⬇️ paste your helper functions here (split_nodeid, status, shorten, widths, labels, caption)

# ⬇️ paste pytest_runtest_logreport unchanged

# ⬇️ paste _make_summary_table and _make_full_table unchanged

# ⬇️ paste pytest_terminal_summary unchanged
