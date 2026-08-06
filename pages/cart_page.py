from playwright.sync_api import Page
from pages.base_page import BasePage

class CartPage(BasePage):
    """
    Page Object for the Automation Exercise Cart Page.
    """
    def __init__(self, page: Page):
        super().__init__(page)

        self.cart_link = page.get_by_text("Cart")
        self.cart_items = page.locator("#cart_info_table tbody tr")
        self.empty_cart_message = page.get_by_text("Cart is empty!")
        self.proceed_to_checkout_button = page.get_by_text("Proceed To Checkout")
        self.checkout_modal = page.get_by_role("heading", name="Checkout")
        self.register_login_link = page.get_by_role("link", name="Register / Login")
        self.continue_on_cart_button = page.get_by_text("Continue On Cart")


    def open_cart(self):
        self.cart_link.click()


    def get_product(self, product_name: str):
        return self.cart_items.filter(has_text=product_name)


    def is_product_in_cart(self, product_name: str) -> bool:
        return self.get_product(product_name).is_visible()


    def get_product_price(self, product_name: str) -> str:
        product = self.get_product(product_name)
        return product.locator(".cart_price p").inner_text()


    def get_product_quantity(self, product_name: str) -> str:
        product = self.get_product(product_name)
        return product.locator(".cart_quantity button").inner_text()


    def get_product_total(self, product_name: str) -> str:
        product = self.get_product(product_name)
        return product.locator(".cart_total_price").inner_text()


    def remove_product(self, product_name: str):
        product = self.get_product(product_name)
        product.locator(".cart_quantity_delete").click()


    def is_cart_empty(self) -> bool:
        return self.empty_cart_message.is_visible()


    def proceed_to_checkout(self):
        self.proceed_to_checkout_button.click()


    def is_login_required_for_checkout(self) -> bool:
        return (self.checkout_modal.is_visible() and self.register_login_link.is_visible())

