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

