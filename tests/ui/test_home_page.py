import allure
import pytest
from playwright.sync_api import Page
from pages.home_page import HomePage


@allure.feature("Home Page")
@allure.story("Verify Home Page")
@allure.title("Verify that the Home Page loads successfully")
@allure.description("Verify that the Home Page loads successfully and all primary page elements are displayed.")
@pytest.mark.ui
@pytest.mark.smoke
def test_home_page(page: Page, config: dict):
    home_page = HomePage(page)

    with allure.step("Open the Home Page"):
        home_page.open(config["environment_config"]["base_url"])

    with allure.step("Verify the Home Page is displayed successfully"):
        assert home_page.verify_home_page()

