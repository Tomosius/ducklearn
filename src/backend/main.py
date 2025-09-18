# src/backend/app.py
import webview

def main():
    # Point pywebview to the running Svelte dev server
    window = webview.create_window(
        title="My App (Dev)",
        url="http://localhost:5173",
        width=1200,
        height=800
    )
    webview.start()

if __name__ == "__main__":
    main()
