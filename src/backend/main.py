# src/backend/main.py  (PROD only)
from pathlib import Path

import webview

from backend import app


def main():
    build_dir = Path(__file__).resolve().parents[1] / "frontend" / "build"
    webview.create_window(
        title="DuckLearn",
        url=str(build_dir),  # serve built static dir
        js_api=app.Api(),
        width=1200,
        height=800,
        resizable=True,
    )
    webview.start(debug=False, http_server=True)


if __name__ == "__main__":
    main()
