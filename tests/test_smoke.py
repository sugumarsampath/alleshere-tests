"""Smoke tests: the key public pages load and show their headline content.

These run against whatever BASE_URL points at (production by default). They are
read-only — they don't post listings or submit forms — so they're safe to run
against the live site.
"""
import re

from playwright.sync_api import Page, expect


def test_homepage_loads(page: Page, base_url):
    page.goto(base_url)
    expect(page).to_have_title(re.compile("AllesHere"))


def test_navbar_has_core_links(page: Page, base_url):
    page.goto(base_url)
    # The navbar exposes the live categories.
    expect(page.get_by_role("link", name="Accommodation").first).to_be_visible()
    expect(page.get_by_role("link", name="Restaurants").first).to_be_visible()


def test_accommodation_page(page: Page, base_url):
    page.goto(f"{base_url}/rooms/")
    expect(
        page.get_by_role("heading", name="Accommodation in Berlin")
    ).to_be_visible()


def test_marathon_guide_reachable(page: Page, base_url):
    page.goto(f"{base_url}/berlin-marathon/")
    expect(
        page.get_by_role("heading", name="Berlin Marathon").first
    ).to_be_visible()


def test_contact_page_has_form(page: Page, base_url):
    page.goto(f"{base_url}/contact/")
    # The contact form asks for an email address.
    expect(page.get_by_role("textbox").first).to_be_visible()
