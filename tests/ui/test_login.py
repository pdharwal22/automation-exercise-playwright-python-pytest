import pytest
from playwright.sync_api import Page
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.account_page import AccountPage


@pytest.mark.ui
@pytest.mark.smoke
def test_valid_login(page: Page, config: dict, test_user: dict):
    home_page = HomePage(page)
    login_page = LoginPage(page)
    account_page = AccountPage(page)

    home_page.open(config["environment_config"]["base_url"])

    login_page.open_login_page()
    login_page.login(email=test_user["email"], password=test_user["password"])
    assert account_page.is_user_logged_in(test_user["name"])

