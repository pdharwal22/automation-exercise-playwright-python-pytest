from playwright.sync_api import Page, TimeoutError
from pages.base_page import BasePage

class ProductPage(BasePage):
    """
    Page Object for the Automation Exercise Products page.
    """

    def __init__(self, page: Page):
        super().__init__(page)

        self.products_link = page.get_by_text("Products")
        self.search_input = page.locator("#search_product")
        self.search_button = page.locator("#submit_search")
        self.searched_products_heading = page.get_by_text("Searched Products")
        self.product_cards = page.locator(".productinfo")
        self.product_detail = page.locator(".product-information")
        self.product_detail_name = self.product_detail.locator("h2")
        self.product_detail_category = self.product_detail.locator("p").filter(has_text="Category:").first
        self.product_detail_price = self.product_detail.locator("span span").first
        self.product_detail_availability = self.product_detail.locator("p").filter(has_text="Availability:")
        self.product_detail_condition = self.product_detail.locator("p").filter(has_text="Condition:")
        self.product_detail_brand = self.product_detail.locator("p").filter(has_text="Brand:")
        self.added_modal = page.get_by_text("Added!", exact=True)
        self.product_added_message = page.get_by_text("Your product has been added to cart.", exact=True)
        self.view_cart_link = page.get_by_text("View Cart")
        self.continue_shopping_button = page.get_by_text("Continue Shopping")
        self.product_quantity = page.locator("#quantity")
        self.add_to_cart_button = page.locator("button.cart")


    def open_products_page(self):
        self.products_link.click()


    def search_product(self, product_name: str):
        self.search_input.fill(product_name)
        self.search_button.click()


    def is_searched_products_displayed(self) -> bool:
        return self.searched_products_heading.is_visible()


    def is_product_displayed(self, product_name: str) -> bool:
        product = self.product_cards.filter(has_text=product_name)
        return product.is_visible()


    def open_product(self, product_name: str, base_url: str):
        product = self.product_cards.filter(has_text=product_name)
        product_id = product.locator("[data-product-id]").get_attribute("data-product-id")
        if not product_id:
            raise AssertionError(f"Product ID not found for product: {product_name}")

        self.navigate(f"{base_url}/product_details/{product_id}")


    def is_product_detail_displayed(self, detail: str) -> bool:
            return self.product_detail_condition.get_by_text(detail, exact=False).is_visible()


    def get_product_detail_name(self) -> str:
        return " ".join(self.product_detail_name.inner_text().replace("\xa0"," ").split())


    def get_product_detail_price(self) -> str:
        return self.product_detail_price.inner_text()


    def get_product_detail_category(self) -> str:
        return " ".join(self.product_detail_category.inner_text().replace("\xa0", " ").split())


    def get_product_detail_availability(self) -> str:
        return self.product_detail_availability.inner_text()


    def get_product_detail_condition(self) -> str:
        return self.product_detail_condition.inner_text()


    def get_product_detail_brand(self) -> str:
        return " ".join(self.product_detail_brand.inner_text().replace("\xa0", " ").split())


    def add_product_to_cart(self, product_name: str):
        product = self.product_cards.filter(has_text=product_name).first
        product.get_by_text("Add to cart").click()


    def is_product_added_message_displayed(self) -> bool:
        try:
            self.product_added_message.wait_for(state="visible", timeout=5000)
            return True
        except TimeoutError:
            return False


    def view_cart(self):
        self.view_cart_link.click()


    def continue_shopping(self):
        self.continue_shopping_button.click()


    def set_product_quantity(self, quantity: int):
        self.product_quantity.fill(str(quantity))


    def add_product_from_details(self):
        self.add_to_cart_button.click()

