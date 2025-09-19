# src/backend/main.py
from __future__ import annotations

from pathlib import Path

import webview


class Api:
    def hello(self, name: str) -> str:
        return f"Hello {name}"


def main() -> None:
    here = Path(__file__).resolve()

    project_root = here.parents[1]  # .../ducklearn

    build_dir = project_root / "frontend" / "build"

    index_html = build_dir / "index.html"

    # Pass directory (not file) so pywebview's built-in server resolves index.html
    webview.create_window(
        title="DuckLearn",
        url=str(index_html),
        js_api=Api(),
        width=1200,
        height=800,
        resizable=True,
    )

    webview.start(debug=False)


if __name__ == "__main__":
    main()
