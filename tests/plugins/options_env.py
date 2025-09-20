# tests/plugins/options_env.py
from __future__ import annotations

import os
import platform
import subprocess
import sys
from datetime import UTC, datetime

from rich.console import Console


def _git(cmd: list[str]) -> str:
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return out.stdout.strip()
    except Exception:
        return ""


def _git_info() -> dict[str, str]:
    commit = _git(["git", "rev-parse", "--short", "HEAD"])
    branch = _git(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    dirty = "yes" if _git(["git", "status", "--porcelain"]) else "no"
    return {"commit": commit, "branch": branch, "dirty": dirty}


def pytest_addoption(parser):
    group = parser.getgroup("rich-table-report")
    group.addoption(
        "--test-report",
        choices=["summary", "full"],
        default="summary",
        help="Colored table at end: 'summary' (per file) or 'full' (per test).",
    )
    group.addoption(
        "--term-width",
        type=int,
        default=None,
        help="Force terminal width (columns) for pytest/coverage output.",
    )
    group.addoption(
        "--repo-url-base",
        default="",
        help="Base URL for source links, e.g. https://github.com/USER/REPO/blob/main",
    )
    group.addoption(
        "--open-html",
        action="store_true",
        default=False,
        help="Open the generated pytest-html report after run.",
    )


def pytest_configure(config):
    # clamp terminal width
    tw = config.getoption("--term-width")
    if tw is None:
        try:
            tw = Console().size.width
        except Exception:
            tw = None
    if tw:
        os.environ["COLUMNS"] = str(tw)

    # environment metadata for pytest-html / metadata
    md = getattr(config, "_metadata", None)
    if md is None:
        try:
            config._metadata = {}
            md = config._metadata
        except Exception:
            md = {}
    gi = _git_info()
    md["Commit"] = gi.get("commit") or "N/A"
    md["Branch"] = gi.get("branch") or "N/A"
    md["Dirty"] = gi.get("dirty", "no")
    md["Run at"] = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S %Z")
    md["Python"] = sys.version.split()[0]
    md["Platform"] = platform.platform()
    md["Executable"] = sys.executable
