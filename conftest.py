import os
import pytest
from utils.config_manager import ConfigManager
from collections.abc import Generator
from playwright.sync_api import (Browser, BrowserContext, Page, Playwright)
from utils.test_data_generator import generate_unique_email
from pages.home_page import HomePage
from pages.signup_page import SignupPage
from pages.account_page import AccountPage
from pages.login_page import LoginPage


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="qa", help="Environment to execute tests against")


@pytest.fixture(scope="session")
def config(request):
    environment = request.config.getoption("--env")
    config_manager = ConfigManager()
    return {
        "environment": environment,
        "environment_config": config_manager.get_environment(environment),
        "browser": config_manager.get_browser_config(),
        "timeouts": config_manager.get_timeout_config()
    }


@pytest.fixture(scope="session")
def browser(playwright: Playwright, config: dict) -> Browser:
    browser_name = config["browser"]["name"]
    browser_type = getattr(playwright, browser_name)
    if os.getenv("CI", "").lower() == "true":
        headless=True
        slow_mo=0
    else:
        headless=config["browser"]["headless"]
        slow_mo =config["browser"]["slow_mo"]

    return browser_type.launch(headless=headless, slow_mo=slow_mo)


@pytest.fixture
# Generator[YieldType, SendType, ReturnType]
def context(browser: Browser, config: dict) -> Generator[BrowserContext, None, None]:
    context = browser.new_context(viewport={"width":1440, "height": 900})
    context.set_default_timeout(config["timeouts"]["default"])
    context.set_default_navigation_timeout(config["timeouts"]["navigation"])

    yield context

    context.close()


@pytest.fixture
def page(context: BrowserContext) -> Generator[Page, None, None]:
    page = context.new_page()

    if os.getenv("CI", "").lower() == "true":
        page.on("console", lambda msg: print(f"[PROWSER CONSOLE] {msg.type}: {msg.tex}"))
        page.on("pageerror", lambda exc: print(f"PAGE ERROR {exc}"))

    yield page

    if os.getenv("CI", "").lower() == "true":
        page.screenshot(path="test-results/final-page.png", full_page=True)

    page.close()


# Setup → Logout → Test Login → Shop → Checkout → Logout → Teardown Login → Delete
@pytest.fixture
def test_user(page: Page, config: dict):
    user = {
        "name": "Automation User",
        "email": generate_unique_email(),
        "password": "Test@12345",
        "first_name": "Automation",
        "last_name": "User",
        "address": "Automation Street",
        "state": "Punjab",
        "city": "Ludhiana",
        "zipcode": "141001",
        "mobile_number": "9999999999"
    }

    home_page = HomePage(page)
    signup_page = SignupPage(page)
    account_page = AccountPage(page)

    home_page.open(config["environment_config"]["base_url"])

    signup_page.open_signup_page()
    signup_page.register_user(user)
    assert signup_page.is_account_created()

    account_page.continue_after_registration()
    assert account_page.is_user_logged_in(user["name"])
    account_page.logout()

    yield user

    # Ensure the user is logged out before cleanup
    account_page = AccountPage(page)
    if account_page.is_user_logged_in(user["name"]):
        account_page.logout()

    # Navigate directly to the login page
    login_page = LoginPage(page)
    login_page.open_login_page(config["environment_config"]["base_url"])
    login_page.login(email=user["email"], password=user["password"])
    assert account_page.is_user_logged_in(user["name"])

    account_page.delete_account()
    assert account_page.is_account_deleted()

