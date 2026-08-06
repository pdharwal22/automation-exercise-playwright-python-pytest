from playwright.sync_api import Page
from pages.base_page import BasePage

class HomePage(BasePage):
    """
    Page Object for the Automation Exercise home page.
    """

    def __init__(self, page: Page):
        super().__init__(page)


    def open(self, base_url: str):
        self.navigate(base_url)


    def verify_home_page(self) -> bool:
        return self.get_title() == "Automation Exercise"

