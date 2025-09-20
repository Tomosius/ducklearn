# src/backend/main_dev.py  (DEV only)
import argparse

import webview

from backend import app


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=5173)
    args = p.parse_args()

    dev_url = f"http://127.0.0.1:{args.port}"
    webview.create_window(
        title="DuckLearn (dev)",
        url=dev_url,  # always point to vite server
        js_api=app.Api(),
        width=1200,
        height=800,
        resizable=True,
    )
    webview.start(debug=False)


if __name__ == "__main__":
    main()
