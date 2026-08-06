from playwright.sync_api import Page
from pages.base_page import BasePage

class CheckoutPage(BasePage):
    """
    Page Object for the Automation Exercise Checkout page.
    """
    def __init__(self, page: Page):
        super().__init__(page)

        self.checkout_heading = page.get_by_text("Address Details")
        self.delivery_address = page.locator("#address_delivery")
        self.billing_address = page.locator("#address_invoice")
        self.order_summary = page.locator("#cart_info")
        self.order_items = page.locator("#cart_info tbody tr")
        self.order_comment = page.locator("textarea[name='message']")
        self.place_order_button = page.get_by_text("Place Order")
        self.total_amount = page.locator(".cart_total_price")


    def is_checkout_page_displayed(self) -> bool:
        return self.checkout_heading.is_visible()


    def get_delivery_address(self) -> str:
        return self.delivery_address.inner_text()


    def get_billing_address(self) -> str:
        return self.billing_address.inner_text()


    def get_order_product(self, product_name: str):
        return self.order_items.filter(has_text=product_name)


    def is_product_in_order(self, product_name: str) -> bool:
        return self.get_order_product(product_name).is_visible()


    def get_product_price(self, product_name: str) -> str:
        product = self.get_order_product(product_name)
        return product.locator(".cart_price p").inner_text()


    def get_product_quantity(self, product_name: str) -> str:
        product = self.get_order_product(product_name)
        return product.locator(".cart_quantity button").inner_text()


    def get_product_total(self, product_name: str) -> str:
        product = self.get_order_product(product_name)
        return product.locator(".cart_total_price").inner_text()


    def get_total_amount(self) -> str:
        return self.total_amount.last.inner_text()


    def enter_order_comment(self, comment: str):
        self.order_comment.fill(comment)


    def place_order(self):
        self.place_order_button.click()

