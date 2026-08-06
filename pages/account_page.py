from playwright.sync_api import Page
from pages.base_page import BasePage

class AccountPage(BasePage):
    """
    Page Object for Automation Exercise account-related actions.
    """

    def __init__(self, page: Page):
        super().__init__(page)

        self.continue_button = page.get_by_text("Continue")
        self.delete_account_link = page.get_by_text("Delete Account")
        self.logout_link = page.get_by_text("Logout")

        self.account_created_message = page.get_by_text("Account Created!")
        self.account_deleted_message = page.get_by_text("Account Deleted!")


    def continue_after_registration(self):
        self.continue_button.click()


    def is_user_logged_in(self, username: str) -> bool:
        return self.page.get_by_text(f"Logged in as {username}").is_visible()


    def delete_account(self):
        self.delete_account_link.click()


    def is_account_deleted(self) -> bool:
        return self.account_deleted_message.is_visible()


    def logout(self):
        self.logout_link.click()

