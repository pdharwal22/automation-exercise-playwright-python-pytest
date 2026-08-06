from playwright.sync_api import Page
from pages.base_page import BasePage

class PaymentPage(BasePage):
    """
    Page Object for Automation Exercise Payment page.
    """
    def __init__(self, page: Page):
        super().__init__(page)

        self.name_on_card = page.locator("input[data-qa='name-on-card']")
        self.card_number = page.locator("input[data-qa='card-number']")
        self.cvc = page.locator("input[data-qa='cvc']")
        self.expiry_month = page.locator("input[data-qa='expiry-month']")
        self.expiry_year = page.locator("input[data-qa='expiry-year']")
        self.pay_button = page.get_by_role("button", name="Pay and Confirm Order")


    def enter_payment_details(self, name_on_card: str, card_number: str, cvc: str, expiry_month: str, expiry_year: str):
        self.name_on_card.fill(name_on_card)
        self.card_number.fill(card_number)
        self.cvc.fill(cvc)
        self.expiry_month.fill(expiry_month)
        self.expiry_year.fill(expiry_year)


    def confirm_payment(self):
        self.pay_button.click()

