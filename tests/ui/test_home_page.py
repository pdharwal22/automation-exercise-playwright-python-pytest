import pytest
from playwright.sync_api import Page


@pytest.mark.ui
@pytest.mark.smoke
def test_home_page_title(page: Page, config: dict):
    page.goto(config["environment_config"]["base_url"])
    assert page.title() == "Automation Exercise"

