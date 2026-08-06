import allure
import pytest
from playwright.sync_api import Page
from pages.home_page import HomePage
from pages.signup_page import SignupPage
from pages.account_page import AccountPage
from utils.test_data_generator import generate_unique_email


@allure.feature("Registration")
@allure.story("User Registration")
@allure.title("Verify new user registration")
@allure.description("Verify that a new user can successfully register an account, login automatically after registration, and delete the account.")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.ui
@pytest.mark.regression
def test_user_registration(page: Page, config: dict):
    home_page = HomePage(page)
    signup_page = SignupPage(page)
    account_page = AccountPage(page)

    base_url = config["environment_config"]["base_url"]
    username = "Automation User"
    email = generate_unique_email()
    allure.dynamic.parameter("Username", username)
    allure.dynamic.parameter("Email", email)

    with allure.step("Open the application"):
        home_page.open(base_url=base_url)

    with allure.step("Navigate to Signup page"):
        signup_page.open_signup_page()

    with allure.step("Start user registration"):
        signup_page.start_signup(name=username, email=email)

    with allure.step("Fill account information"):
        signup_page.fill_account_information(
            password="Test@12345",
            first_name="Automation",
            last_name="User",
            address="Automation Street",
            state="Punjab",
            city="Ludhiana",
            zipcode="141001",
            mobile_number="9999999999"
        )

    with allure.step("Create user account"):
        signup_page.create_account()
        assert signup_page.is_account_created()

    with allure.step("Continue after successful registration"):
        account_page.continue_after_registration()

    with allure.step("Verify user is logged in"):
        assert account_page.is_user_logged_in(username=username)

    with allure.step("Delete user account"):
        account_page.delete_account()

    with allure.step("Verify account is deleted successfully"):
        assert account_page.is_account_deleted()

