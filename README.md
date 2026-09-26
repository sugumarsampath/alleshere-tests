# AllesHere — AI-powered UI test automation (Playwright + Python)

[![UI tests](https://github.com/sugumarsampath/alleshere-tests/actions/workflows/ci.yml/badge.svg)](https://github.com/sugumarsampath/alleshere-tests/actions/workflows/ci.yml)

End-to-end tests for **[AllesHere](https://www.alleshere.de/)**, a live
Berlin community platform (Django, HTMX, PostgreSQL). The tests are kept in
their own repo, separate from the (private) app code.

## How it works: AI-assisted QA workflow

The suite is built with **Claude Code** agents driven by project-specific
skills in [`.claude/skills/`](.claude/skills/):

| Step | Skill | What it produces |
|---|---|---|
| 1. Know the product | `alleshere-domain` | Business rules (numbered `BR-…`), URL map, user flows, verified UI selectors |
| 2. Design scenarios | `/create-scenarios` | `docs/test-scenarios.md`, covering happy path, business rules, security, negative, edge and UI-state cases |
| 3. Pick test layers | `/test-strategy` | `docs/test-strategy.md` (test pyramid: unit / Django view test / E2E) |
| 4. Write & self-heal | `/generate-tests` | Playwright tests, checked in a real browser and re-run until green |
| 5. Review | `/review-tests` | Scored review against the `playwright-best-practices` standard |

Every test traces back to a business rule, and a human reviews the output.

## Safety by design

- **Production smoke tests are read-only.** They run on every push via GitHub Actions.
- **Tests that create or change data are marked `@pytest.mark.local_only`** and
  are skipped automatically unless `BASE_URL` points at a local server, so they
  can never touch the live site.

## Tech

Python 3.13 · Playwright · pytest / pytest-playwright · GitHub Actions · Claude Code

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
