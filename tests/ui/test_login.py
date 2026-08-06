import pytest
from playwright.sync_api import Page
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.account_page import AccountPage
from utils.test_data_generator import generate_unique_email


@pytest.mark.ui
@pytest.mark.smoke
def test_valid_login(page: Page, config: dict, test_user: dict):
    home_page = HomePage(page)
    login_page = LoginPage(page)
    account_page = AccountPage(page)

    home_page.open(config["environment_config"]["base_url"])

    login_page.open_login_page(config["environment_config"]["base_url"])
    login_page.login(email=test_user["email"], password=test_user["password"])
    assert account_page.is_user_logged_in(test_user["name"])


@pytest.mark.ui
@pytest.mark.regression
def test_login_with_invalid_email(page: Page, config: dict):
    home_page = HomePage(page)
    login_page = LoginPage(page)

    home_page.open(config["environment_config"]["base_url"])
    login_page.open_login_page(config["environment_config"]["base_url"])
    email = "demouser@example.com"
    password = "Test@12345"
    login_page.login(email=email, password=password)
    assert login_page.is_login_error_displayed()


@pytest.mark.ui
@pytest.mark.regression
def test_login_with_invalid_password(page: Page, config: dict):
    home_page = HomePage(page)
    login_page = LoginPage(page)

    home_page.open(config["environment_config"]["base_url"])
    login_page.open_login_page(config["environment_config"]["base_url"])
    email = generate_unique_email()
    password = "WrongPassword@123"
    login_page.login(email=email, password=password)
    assert login_page.is_login_error_displayed()


@pytest.mark.ui
@pytest.mark.regression
def test_logout(page: Page, config: dict, test_user: dict):
    home_page = HomePage(page)
    login_page = LoginPage(page)
    account_page = AccountPage(page)

    home_page.open(config["environment_config"]["base_url"])

    login_page.open_login_page(config["environment_config"]["base_url"])
    login_page.login(email=test_user["email"], password=test_user["password"])
    assert account_page.is_user_logged_in(test_user["name"])

    account_page.logout()
    assert login_page.is_login_page_displayed()

