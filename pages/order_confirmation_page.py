from playwright.sync_api import Page
from pages.base_page import BasePage

class OrderConfirmationPage(BasePage):
    """
    Page Object for Automation Exercise order confirmation page.
    """
    def __init__(self, page: Page):
        super().__init__(page)

        self.success_message = page.get_by_text("Congratulations! Your order has been confirmed!")


    def is_order_confirmed(self) -> bool:
        return self.success_message.is_visible()

