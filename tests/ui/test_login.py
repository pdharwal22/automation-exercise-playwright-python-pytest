import allure
import pytest
from playwright.sync_api import Page
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.account_page import AccountPage
from utils.test_data_generator import generate_unique_email


@allure.feature("Authentication")
@allure.story("Valid Login")
@allure.title("Verify user can login with valid credentials")
@allure.description("Verify that a registered user can successfully log in using valid email and password and is redirected to the authenticated page.")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.ui
@pytest.mark.smoke
def test_valid_login(page: Page, config: dict, test_user: dict):
    home_page = HomePage(page)
    login_page = LoginPage(page)
    account_page = AccountPage(page)

    base_url = config["environment_config"]["base_url"]

    with allure.step("Open the application"):
        home_page.open(base_url=base_url)

    with allure.step("Navigate to Login Page"):
        login_page.open_login_page(base_url=base_url)

    with allure.step("Login with valid credentials"):
        login_page.login(email=test_user["email"], password=test_user["password"])

    with allure.step("Verify user is logged in successfully"):
        assert account_page.is_user_logged_in(test_user["name"])


@allure.feature("Authentication")
@allure.story("Login with invalid email")
@allure.title("Verify login fails with invalid email")
@allure.description("Verify that the application displays an error message when a user attempts to log in using an invalid email address.")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.ui
@pytest.mark.regression
def test_login_with_invalid_email(page: Page, config: dict):
    home_page = HomePage(page)
    login_page = LoginPage(page)

    base_url = config["environment_config"]["base_url"]
    email = "demouser@example.com"
    password = "Test@12345"

    with allure.step("Open the application"):
        home_page.open(base_url=base_url)

    with allure.step("Navigate to Login Page"):
        login_page.open_login_page(base_url=base_url)

    with allure.step("Login using invalid email"):
        login_page.login(email=email, password=password)

    with allure.step("Verify login error message is displayed"):
        assert login_page.is_login_error_displayed()


@allure.feature("Authentication")
@allure.story("Login with invalid password")
@allure.title("Verify login fails with invalid password")
@allure.description("Verify that the application displays an error message when a user attempts to log in using an incorrect password.")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.ui
@pytest.mark.regression
def test_login_with_invalid_password(page: Page, config: dict):
    home_page = HomePage(page)
    login_page = LoginPage(page)

    base_url = config["environment_config"]["base_url"]

    with allure.step("Open the application"):
        home_page.open(base_url=base_url)

    with allure.step("Navigate to Login Page"):
        login_page.open_login_page(base_url=base_url)

    with allure.step("Login using invalid password"):
        email = generate_unique_email()
        password = "WrongPassword@123"
        login_page.login(email=email, password=password)

    with allure.step("Verify login error message is displayed"):
        assert login_page.is_login_error_displayed()


@allure.feature("Authentication")
@allure.story("Logout")
@allure.title("Verify logged-in user can logout successfully")
@allure.description("Verify that a logged-in user can successfully logout from the application and is redirected to the login page.")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.ui
@pytest.mark.regression
def test_logout(page: Page, config: dict, test_user: dict):
    home_page = HomePage(page)
    login_page = LoginPage(page)
    account_page = AccountPage(page)

    base_url = config["environment_config"]["base_url"]

    with allure.step("Open the application"):
        home_page.open(base_url=base_url)

    with allure.step("Naviagte to Login Page"):
        login_page.open_login_page(base_url=base_url)

    with allure.step("Login with valid credentials"):
        login_page.login(email=test_user["email"], password=test_user["password"])

    with allure.step("Verify user logged in successfully"):
        assert account_page.is_user_logged_in(test_user["name"])

    with allure.step("Logout from application"):
        account_page.logout()

    with allure.step("Verify Login page is displayed after logout"):
        assert login_page.is_login_page_displayed()

