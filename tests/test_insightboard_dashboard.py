"""Insightboard dashboard: client selection drives the KPI tiles.

Read-only test against a local static HTML page — no AllesHere data involved,
so it is safe to run in any environment.
"""
import re

import pytest
from playwright.sync_api import Page, expect

from tests.pages.insightboard_dashboard_page import InsightboardDashboardPage

BRAND_NAME = "Insightboard"
CLIENT = "Test Client 3"
CLIENT_VALUE = "3"
EXPECTED_NPS = "51"  # client data is seeded per client id, so this is stable


@pytest.fixture
def dashboard(page: Page) -> InsightboardDashboardPage:
    dashboard = InsightboardDashboardPage(page)
    dashboard.goto()
    return dashboard


class TestInsightboardDashboard:
    def test_selecting_test_client_3_shows_nps_51(self, dashboard: InsightboardDashboardPage):
        # -- Step 1: Home page loaded with the Insightboard brand --
        expect(dashboard.page).to_have_title(re.compile(rf"^{BRAND_NAME}"))
        expect(dashboard.brand).to_be_visible()
        expect(dashboard.brand).to_contain_text(BRAND_NAME)
        expect(dashboard.page_title).to_have_text("Teams Overview")

        # -- Step 2: Select Test Client 3 --
        dashboard.select_client(CLIENT)
        expect(dashboard.client_dropdown).to_have_value(CLIENT_VALUE)

        # -- Step 3: Net Promoter Score tile shows 51 --
        expect(dashboard.nps_tile).to_contain_text("Net Promoter Score")
        expect(dashboard.nps_value).to_have_text(EXPECTED_NPS)
