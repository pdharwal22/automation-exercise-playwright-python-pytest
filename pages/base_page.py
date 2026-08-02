from playwright.sync_api import Page

class BasePage:
    """
    Base class containing common page-level operations.
    """

    def __init__(self, page: Page):
        self.page = page


    def navigate(self, url: str):
        self.page.goto(url, wait_until="domcontentloaded")


    def get_title(self) -> str:
        return self.page.title()


    def get_current_url(self) -> str:
        return self.page.url

