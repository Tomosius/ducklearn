# tests/plugins/html_report.py
from __future__ import annotations

try:
    from py.xml import html as _HTML
except Exception:
    _HTML = None

# ⬇️ paste _git, _git_info, _guess_location from your file

# ⬇️ paste pytest_html_report_title unchanged
# ⬇️ paste pytest_html_results_summary unchanged
# ⬇️ paste pytest_html_results_table_header unchanged
# ⬇️ paste pytest_html_results_table_row unchanged
# ⬇️ paste pytest_runtest_makereport unchanged
# ⬇️ paste pytest_sessionfinish unchanged
