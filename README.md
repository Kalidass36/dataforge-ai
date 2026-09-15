DataForge
=========

Development
-----------

Install editable package and run tests:

```bash
python -m venv .venv
source .venv/bin/activate    # On Windows: .\.venv\Scripts\Activate.ps1 or activate.bat
pip install -e .
pip install -r requirements.txt
pytest
```

CI tips
-------

- On CI, either `pip install -e .` or set `PYTHONPATH` to the repository root before running tests.
- Example GitHub Actions step to install editable package:

```yaml
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install -e .
    pip install -r requirements.txt
```

End-to-end (E2E) smoke tests
---------------------------

An optional Playwright-based E2E smoke test is provided at `tests/e2e/test_streamlit_smoke.py`.

To run E2E tests locally:

```bash
# Install dev requirements and Playwright browsers
pip install -r requirements-dev.txt
playwright install chromium

# Start tests (the test will start Streamlit automatically)
pytest tests/e2e -q
```

Notes:
- The E2E test requires a headless browser environment (Playwright) and may need extra setup on CI.
- On CI, install the `requirements-dev.txt` and run `playwright install chromium` before running the E2E tests.

