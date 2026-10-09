"""Page object for the Insightboard QE Challenge dashboard (single static HTML page)."""
import os
from pathlib import Path

from playwright.sync_api import Locator, Page

# Local copy of the page under test, kept in the repo so the test runs the same
# everywhere (local + CI). Override with INSIGHTBOARD_HTML to point elsewhere.
DEFAULT_HTML = Path(__file__).resolve().parent.parent / "data" / "insightboard" / "dashboard.html"


class InsightboardDashboardPage:
    def __init__(self, page: Page):
        self.page = page
        self.html_path = Path(os.environ.get("INSIGHTBOARD_HTML", DEFAULT_HTML)).resolve()

        # Locators — data-testid first, then role/label, scoped to their region.
        self.sidebar: Locator = page.get_by_role("complementary", name="Primary navigation")
        self.brand: Locator = self.sidebar.get_by_text("Insightboard")
        self.page_title: Locator = page.get_by_role("heading", level=1)
        self.client_dropdown: Locator = page.get_by_test_id("client-dropdown")
        self.nps_tile: Locator = page.get_by_test_id("tile-nps")
        # The KPI value has no testid; it's the tile's #kpi-nps child.
        self.nps_value: Locator = self.nps_tile.locator("#kpi-nps")

    def goto(self) -> None:
        self.page.goto(self.html_path.as_uri())

    def select_client(self, client_name: str) -> None:
        """Choose a client by its visible label, e.g. "Test Client 3"."""
        self.client_dropdown.select_option(label=client_name)
