import os
import subprocess
import time
import pytest

try:
    from playwright.sync_api import sync_playwright
except Exception:  # pragma: no cover - skip when playwright isn't installed
    pytest.skip("playwright not installed, skipping e2e tests", allow_module_level=True)


def wait_for_url(url, timeout=30):
    import time
    import requests

    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(url, timeout=1)
            if r.status_code == 200:
                return True
        except Exception:
            pass
        time.sleep(0.5)
    return False


def test_streamlit_smoke():
    """Start the Streamlit app and check the homepage loads using Playwright."""

    port = int(os.getenv("STREAMLIT_PORT", "8501"))
    url = f"http://127.0.0.1:{port}"

    # Start Streamlit in a subprocess
    cmd = [
        "python",
        "-m",
        "streamlit",
        "run",
        "app/ui/dashboard.py",
        "--server.port",
        str(port),
        "--server.headless",
        "true",
    ]

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        assert wait_for_url(url, timeout=30), "Streamlit did not start in time"

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url, timeout=15000)

            # Basic smoke checks
            title = page.title()
            body_text = page.inner_text("body")[:200]

            assert "DataForge" in title or "DataForge" in body_text

            browser.close()

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            proc.kill()
