import pytest
from playwright.sync_api import Page
from pages.home_page import HomePage
from pages.signup_page import SignupPage
from pages.account_page import AccountPage
from utils.test_data_generator import generate_unique_email


@pytest.mark.ui
@pytest.mark.regression
def test_user_registration(page: Page, config: dict):
    home_page = HomePage(page)
    signup_page = SignupPage(page)
    account_page = AccountPage(page)

    home_page.open(config["environment_config"]["base_url"])

    signup_page.open_signup_page()

    username = "Automation User"
    email = generate_unique_email()
    signup_page.start_signup(name=username, email=email)
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
    signup_page.create_account()
    assert signup_page.is_account_created()

    account_page.continue_after_registration()
    assert account_page.is_user_logged_in(username=username)

    account_page.delete_account()
    assert account_page.is_account_deleted()

