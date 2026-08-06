from playwright.sync_api import Page
from pages.base_page import BasePage

class LoginPage(BasePage):
    """
    Page Object for the Automation Exercise Login Page.
    """

    def __init__(self, page: Page):
        super().__init__(page)

        # self.login_link = page.get_by_text("Signup / Login")
        self.login_email = page.locator("input[data-qa='login-email']")
        self.login_password = page.locator("input[data-qa='login-password']")
        self.login_button = page.get_by_role("button", name="Login")
        self.login_error_message = page.get_by_text("Your email or password is incorrect!")


    def open_login_page(self, base_url: str):
        self.navigate(f"{base_url}/login")


    def login(self, email: str, password: str):
        self.login_email.fill(email)
        self.login_password.fill(password)
        self.login_button.click()


    def is_login_error_displayed(self) -> bool:
        return self.login_error_message.is_visible()


    def is_login_page_displayed(self) -> bool:
        return self.login_email.is_visible()

