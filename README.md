# AllesHere — UI test automation (Playwright + Python)

End-to-end / smoke tests for **[www.alleshere.de](https://www.alleshere.de)**,
kept in their own repo so they stay independent of the Django app.

## Setup

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install
```

## Run

```powershell
pytest                         # headless, against production (default)
```

Run against your local Django dev server instead:

```powershell
$env:BASE_URL="http://127.0.0.1:8000"; pytest
```

Useful flags:

```powershell
pytest --headed                # watch the browser as it runs
pytest -k marathon             # only tests matching "marathon"
pytest --tracing=on            # record a Playwright trace on failure
```

## Record a test by clicking

Playwright can watch you click through the site and write the Python for you:

```powershell
playwright codegen https://www.alleshere.de
```

Copy the generated code into a new file under `tests/`.

## Layout

| Path | What |
|---|---|
| `tests/` | test files (`test_*.py`) |
| `conftest.py` | shared fixtures — `base_url`, viewport; skips `local_only` tests off-localhost |
| `pytest.ini` | default options (headless Chromium) + `local_only` marker |
| `.github/workflows/ci.yml` | runs the suite headless on every push/PR |

## Notes

- The smoke tests are **read-only** (no posting / form submission), so they're
  safe to run against the live site.
- Tests that create or change data (register, post a listing, messaging,
  contact form) must be marked `@pytest.mark.local_only`. They are **skipped
  automatically** unless `BASE_URL` points at a local server, so they can
  never run against production:

  ```powershell
  $env:BASE_URL="http://127.0.0.1:8000"; pytest     # runs everything
  pytest                                            # prod: local_only tests skipped
  ```
