---
name: playwright-best-practices
description: Playwright + pytest (Python) UI test standards for the AllesHere suite — locator strategy, assertion patterns, test structure, Page Object Model, prod-safe vs local-only tests, route mocking, wait strategies, and anti-patterns. Use when writing, reviewing, or debugging any test in this repo.
user-invocable: false
---

# Playwright Best Practices — AllesHere (Python + pytest)

Standards for every test in this repo. Adapted from the EventHub skill for
**Python `pytest-playwright`** and the **AllesHere Django site**
(https://www.alleshere.de/).

---

## 1. Project setup

- **Runner**: `pytest` + `pytest-playwright` (sync API: `from playwright.sync_api import Page, expect`)
- **Test dir**: `tests/` (see `pytest.ini`)
- **Base URL**: `base_url` fixture in `conftest.py` — defaults to production
  `https://www.alleshere.de`, override with `BASE_URL` env var
  (`$env:BASE_URL="http://127.0.0.1:8000"; pytest`)
- **Browser**: Chromium by default (`--browser chromium` in `pytest.ini`)
- **Viewport**: 1280×900 via `browser_context_args`
- **Debug artefacts**: `pytest --tracing=retain-on-failure --screenshot=only-on-failure --video=retain-on-failure`

Never hardcode the host in a test — always build URLs from `base_url`.

### File naming
- `tests/test_<feature>.py` — e.g. `test_accommodation.py`, `test_auth.py`, `test_directory.py`
- Test functions: `test_<what_is_verified>` — the name should read as the behaviour checked
- Group related tests in one file; use a class (`class TestRoomFilters:`) only when it adds clarity

---

## 2. Prod-safe vs local-only tests (AllesHere-specific)

Default target is the **live site**, so tests are split:

| Kind | Examples | Where it may run |
|---|---|---|
| **Read-only** | page loads, headings, navbar/footer links, filters, search | Production + local |
| **Mutating** | register, login, post/edit listing, send message, contact form (sends a real email) | **Local dev server only** |

Mark mutating tests with the `local_only` marker (registered in `pytest.ini`;
`--strict-markers` makes typos fail):

```python
import pytest

@pytest.mark.local_only
def test_post_listing(page: Page, base_url):
    ...
```

`conftest.py` (`pytest_collection_modifyitems`) skips every `local_only` test
unless `BASE_URL`'s host is `localhost`, `127.0.0.1`, `::1`, `*.localhost` or
`*.test` — so a forgotten `BASE_URL` fails safe (skipped, not run on prod).
Apply to a whole file with `pytestmark = pytest.mark.local_only`.

**Never** submit forms, post listings, or send messages against production.

---

## 3. Locator strategy (priority order)

### 1. Role + accessible name (preferred for this Django/Tailwind site)
```python
page.get_by_role("link", name="Accommodation")
page.get_by_role("button", name="Send Message")
page.get_by_role("heading", name="Accommodation in Berlin")
```

### 2. Label / placeholder (forms)
```python
page.get_by_label("Email ID")
page.get_by_label("Password")
page.get_by_placeholder("Search restaurants")
```

### 3. `data-testid` (add to templates when 1–2 are ambiguous)
```python
page.get_by_test_id("listing-card")
```
When a stable hook is needed, add `data-testid="..."` to the Django template in
the `DreamProject` repo rather than reaching for CSS.

### 4. Element IDs
```python
page.locator("#id_email")   # Django form fields render as id_<field_name>
```

### 5. CSS classes — last resort
Tailwind utility classes (`.bg-orange-500`, `.rounded-xl`) change with styling —
**never** use them as locators.

### Never
- XPath
- Deep CSS chains (`div > div:nth-child(3) > span`)
- Bare `.nth(i)` / `.first` without a filter, unless the order *is* the behaviour
  being tested (e.g. navbar duplicate links on mobile → `.first` is acceptable with a comment)

---

## 4. Filtering and scoping

```python
cards = page.get_by_test_id("listing-card")
card = cards.filter(has_text=listing_title).first
card.get_by_role("link", name="View More").click()

# Filter by a nested element
card = cards.filter(has=page.get_by_text("Friedrichshain"))
```

Scope actions to a parent (navbar, footer, card) instead of searching the whole page:

```python
footer = page.locator("footer")
footer.get_by_role("link", name="Contact us").click()
```

---

## 5. Assertions — always web-first `expect`

```python
expect(page).to_have_title(re.compile("AllesHere"))
expect(page).to_have_url(re.compile(r"/listings/\d+/$"))
expect(page.get_by_text("Your listing is now live!")).to_be_visible()
expect(card).to_contain_text("€")
expect(cards).to_have_count(6)
expect(banner).not_to_be_visible()
```

Custom timeout only for genuinely slow things:
```python
expect(page.get_by_test_id("listing-card").first).to_be_visible(timeout=10_000)
```

Avoid non-retrying checks like `assert page.locator(...).count() == 6` or
`assert x.is_visible()` — they don't auto-wait and cause flakes. Plain `assert`
is fine for values you've already read (e.g. comparing two numbers).

---

## 6. Test structure

```python
import re
from playwright.sync_api import Page, expect


def test_room_type_chip_filters_listings(page: Page, base_url):
    # -- Step 1: Open accommodation page --
    page.goto(f"{base_url}/rooms/")

    # -- Step 2: Pick the "Shared" chip --
    page.get_by_role("link", name="Shared").click()

    # -- Step 3: URL and results reflect the filter --
    expect(page).to_have_url(re.compile(r"room_type=shared_room"))
```

- Arrange → Act → Assert; mark multi-step flows with `# -- Step N: ... --`
- Every test ends with at least one assertion
- Shared setup goes in **fixtures** (`conftest.py`), not copy-pasted helpers

### Page Object Model

For flows used by more than one test, put page classes in `tests/pages/`:

```python
# tests/pages/login_page.py
from playwright.sync_api import Page


class LoginPage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url
        self.email = page.get_by_label("Email ID")
        self.password = page.get_by_label("Password")
        self.submit = page.get_by_role("button", name="Log in")

    def goto(self):
        self.page.goto(f"{self.base_url}/accounts/login/")

    def login(self, email: str, password: str):
        self.email.fill(email)
        self.password.fill(password)
        self.submit.click()
```

POM rules:
- One class per page / major component
- Locators as attributes set in `__init__`
- Methods = user actions (`login`, `post_listing`), not low-level clicks
- **Assertions stay in tests**, not in page objects
- Expose page objects via fixtures (`def login_page(page, base_url): return LoginPage(page, base_url)`)

---

## 7. Test users and secrets

- Test accounts exist **only on the local dev DB**; never use real or production credentials.
- Read credentials from env vars (`TEST_USER_EMAIL`, `TEST_USER_PASSWORD`) or a
  git-ignored `.env` — **never hardcode passwords in test files**.
- Passwords must satisfy AllesHere's rules: 7–16 chars, ≥1 capital, ≥1 number.
- Prefer creating a fresh user inside the test (via the register page or a fixture)
  over depending on a pre-existing one.

---

## 8. Dynamic data

Generate unique data to avoid collisions between runs:

```python
import time
title = f"Test listing {time.time_ns()}"
email = f"qa+{time.time_ns()}@example.com"
```

Don't hardcode listing/restaurant IDs — find records by content instead.
Production content changes; assert on structure ("at least one card", headings,
links), not on specific listings.

---

## 9. Wait strategies

- **DO** rely on auto-waiting: `click()`, `fill()`, and `expect(...)` all wait.
- **HTMX live filtering** (`/rooms/`): after changing a filter, assert on the
  updated grid/URL with `expect` — don't sleep.
  ```python
  with page.expect_response(re.compile(r"/rooms/")):
      page.get_by_label("District").select_option("Neukölln")
  expect(page.get_by_test_id("listing-card").first).to_contain_text("Neukölln")
  ```
- **DON'T** use `page.wait_for_timeout(...)` / `time.sleep(...)`.
- **Avoid** `wait_until="networkidle"` — the site loads analytics, Google
  Translate and a banner carousel, so the network rarely goes idle. Wait for a
  specific element instead.
- Exception: testing timed UI (e.g. carousel auto-advance every 5s) — assert
  with an explicit `timeout=` on `expect`, still no sleeps.

---

## 10. Route mocking

Use `page.route` to isolate UI states that are hard to reproduce on real data
(empty results, failing third-party assets):

```python
page.route("**/*google-analytics*", lambda route: route.abort())
```

Use sparingly — this is mostly a server-rendered Django site, so most tests
should exercise the real HTML.

---

## 11. Running and debugging

```powershell
pytest                                   # all, headless, prod
pytest tests/test_smoke.py -k navbar     # one test
pytest --headed --slowmo 300             # watch it
pytest --tracing=retain-on-failure       # then: playwright show-trace test-results\...\trace.zip
playwright codegen https://www.alleshere.de   # record locators by clicking
$env:PWDEBUG=1; pytest -k contact        # Playwright Inspector
```

---

## 12. Anti-patterns

| Anti-pattern | Why it's bad | Do instead |
|---|---|---|
| `page.wait_for_timeout(n)` / `time.sleep` | Flaky, slow | `expect(...).to_be_visible()` |
| Tailwind-class or nth-child CSS locators | Break on restyle | Role / label / `data-testid` |
| Hardcoded host in `goto` | Can't switch prod/local | `f"{base_url}/..."` |
| Mutating test without `local_only` | Pollutes production, sends real email | Mark `@pytest.mark.local_only` |
| Hardcoded IDs / specific prod listings | Break when data changes | Find by content, assert structure |
| Passwords in test files | Leak via git | Env vars / `.env` |
| `.only`-style focus left in (`-k` in `pytest.ini`) | Silently skips tests in CI | Keep `addopts` clean |
| No assertion after an action | Proves nothing | Always assert the outcome |
| Tests depending on each other's state | Order-dependent failures | Self-contained tests + fixtures |
| Asserting implementation details | Break on refactor | Assert user-visible behaviour |
