import pytest
from utils.config_manager import ConfigManager
from collections.abc import Generator
from playwright.sync_api import (Browser, BrowserContext, Page, Playwright)


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
    return browser_type.launch(headless=config["browser"]["headless"], slow_mo=config["browser"]["slow_mo"])


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

    yield page

    page.close()

