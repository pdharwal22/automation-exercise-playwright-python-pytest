from playwright.sync_api import Page
from pages.base_page import BasePage

class OrderPage(BasePage):
    """
    Page Object for the Automation Exercise order confirmation page.
    """
    def __init__(self, page: Page):
        super().__init__(page)

        self.order_heading = page.get_by_role("heading", name="Order Placed!")
        self.success_message = page.locator("#form p")
        self.download_invoice_button = page.get_by_role("link", name="Download Invoice")
        self.continue_button = page.get_by_role("link", name="Continue")


    def is_order_successful(self) -> bool:
        return self.order_heading.is_visible()


    def get_success_message(self) -> str:
        return self.success_message.inner_text().strip()


    def download_invoice(self):
        self.download_invoice_button.click()


    def continue_shopping(self):
        return self.continue_button.click()

