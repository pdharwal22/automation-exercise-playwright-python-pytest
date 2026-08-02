import pytest
from playwright.sync_api import Page
from pages.home_page import HomePage


@pytest.mark.ui
@pytest.mark.smoke
def test_home_page(page: Page, config: dict):
    home_page = HomePage(page)

    home_page.open(config["environment_config"]["base_url"])
    assert home_page.verify_home_page()

