"""Shared pytest fixtures for the AllesHere UI test suite."""
import os
from urllib.parse import urlparse

import pytest

BASE_URL = os.environ.get("BASE_URL", "https://www.alleshere.de").rstrip("/")

# Hosts where tests may create/change data. Anything else (i.e. production)
# only runs the read-only tests.
LOCAL_HOSTS = {"localhost", "127.0.0.1", "::1"}


def is_local(url: str) -> bool:
    host = urlparse(url).hostname or ""
    return host in LOCAL_HOSTS or host.endswith((".localhost", ".test"))


def pytest_collection_modifyitems(config, items):
    """Skip @pytest.mark.local_only tests unless BASE_URL is a local server.

    Mutating tests (register, post a listing, messaging, contact form) must
    never run against the live site.
    """
    if is_local(BASE_URL):
        return
    skip = pytest.mark.skip(
        reason=f"local_only: mutates data — skipped against {BASE_URL}"
    )
    for item in items:
        if "local_only" in item.keywords:
            item.add_marker(skip)


@pytest.fixture(scope="session")
def base_url():
    """The site under test.

    Defaults to the live site. To run against your local Django dev server:
        PowerShell:  $env:BASE_URL="http://127.0.0.1:8000"; pytest
        Bash:        BASE_URL=http://127.0.0.1:8000 pytest
    """
    return BASE_URL


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Give every test a sensible desktop viewport."""
    return {**browser_context_args, "viewport": {"width": 1280, "height": 900}}
