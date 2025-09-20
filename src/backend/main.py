# src/backend/main.py
from __future__ import annotations

import argparse
import os
from pathlib import Path

import webview

import backend as backend_pkg  # <-- use package __file__ to get an on-disk Path


class Api:
    def hello(self, name: str) -> str:
        return f"Hello {name}"


def repo_build_dir() -> Path | None:
    """<repo>/src/frontend/build if it exists (editable dev installs)."""
    here = Path(__file__).resolve()
    p = here.parents[1] / "frontend" / "build"  # .../src/frontend/build
    return p if (p / "index.html").exists() else None


def package_build_dir() -> Path | None:
    """
    Locate bundled assets in an installed wheel.
    Supports either:
      - backend/frontend_build   (recommended)
      - src/frontend/build       (if you force-included with that path)
    """
    pkg_dir = Path(backend_pkg.__file__).resolve().parent  # .../site-packages/backend

    # Recommended layout: put assets under the backend package
    p1 = pkg_dir / "frontend_build"
    if (p1 / "index.html").exists():
        return p1

    # If you force-included to "src/frontend/build" at wheel root:
    p2 = pkg_dir.parent / "src" / "frontend" / "build"  # .../site-packages/src/frontend/build
    if (p2 / "index.html").exists():
        return p2

    return None


def find_build_dir() -> Path:
    for candidate in (repo_build_dir(), package_build_dir()):
        if candidate:
            return candidate
    raise FileNotFoundError(
        "Could not find built frontend.\n"
        "Build it with: npm --prefix src/frontend run build\n"
        "Or ensure the wheel includes the assets."
    )


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="DuckLearn launcher")
    p.add_argument("--dev", action="store_true", help="Use a running dev server")
    p.add_argument("--url", help="Dev server URL (overrides --port), e.g. http://127.0.0.1:5173")
    p.add_argument("--port", type=int, default=5173, help="Dev server port if --url not given")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    dev_mode = args.dev or os.environ.get("DUCKLEARN_DEV") == "1"

    if dev_mode:
        dev_url = args.url or f"http://127.0.0.1:{args.port}"
        webview.create_window(
            title="DuckLearn (dev)",
            url=dev_url,
            js_api=Api(),
            width=1200,
            height=800,
            resizable=True,
        )
        webview.start(debug=False)
        return

    # Built mode: serve the *directory* so absolute `/_app/...` works
    build_dir = find_build_dir()
    webview.create_window(
        title="DuckLearn",
        url=str(build_dir),  # directory, not file
        js_api=Api(),
        width=1200,
        height=800,
        resizable=True,
    )
    webview.start(debug=False, http_server=True)


if __name__ == "__main__":
    main()
