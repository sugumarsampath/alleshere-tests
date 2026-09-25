"""Shared pytest fixtures for the AllesHere UI test suite."""
import os

import pytest


@pytest.fixture(scope="session")
def base_url():
    """The site under test.

    Defaults to the live site. To run against your local Django dev server:
        PowerShell:  $env:BASE_URL="http://127.0.0.1:8000"; pytest
        Bash:        BASE_URL=http://127.0.0.1:8000 pytest
    """
    return os.environ.get("BASE_URL", "https://www.alleshere.de").rstrip("/")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Give every test a sensible desktop viewport."""
    return {**browser_context_args, "viewport": {"width": 1280, "height": 900}}
