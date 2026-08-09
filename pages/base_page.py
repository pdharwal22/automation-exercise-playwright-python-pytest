from playwright.sync_api import Page

class BasePage:
    """
    Base class containing common page-level operations.
    """

    def __init__(self, page: Page):
        self.page = page


    def navigate(self, url: str):
        response = self.page.goto(url, wait_until="domcontentloaded")
        print(f"[PAGE URL] {self.page.url}")
        print(f"[PAGE TITLE] {self.page.title()}")
        if response:
            print(f"[HTTP STATUS] {response.status}")

        print(f"[PAGE CONTENT LENGTH] {len(self.page.content())}")


    def get_title(self) -> str:
        return self.page.title()


    def get_current_url(self) -> str:
        return self.page.url

