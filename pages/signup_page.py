from playwright.sync_api import Page
from pages.base_page import BasePage

class SignupPage(BasePage):
    """
    Page Object for the Automation Exercise Signup Page.
    """

    def __init__(self, page: Page):
        super().__init__(page)

        self.signup_login_link = page.get_by_text("Signup / Login")

        # Initial signup form
        self.signup_name = page.get_by_placeholder("Name")
        self.signup_email = page.locator("input[data-qa='signup-email']")
        self.signup_button = page.get_by_role("button", name="Signup")

        # Account information form
        self.title_mr = page.locator("#id_gender1")
        self.password = page.locator("#password")

        self.days = page.locator("#days")
        self.months = page.locator("#months")
        self.years = page.locator("#years")

        self.first_name = page.locator("#first_name")
        self.last_name = page.locator("#last_name")
        self.company = page.locator("#company")
        self.address = page.locator("#address1")
        self.country = page.locator("#country")
        self.state = page.locator("#state")
        self.city = page.locator("#city")
        self.zipcode = page.locator("#zipcode")
        self.mobile_number = page.locator("#mobile_number")

        self.create_account_button = page.get_by_role("button", name="Create Account")


    def open_signup_page(self):
            self.signup_login_link.click()


    def start_signup(self, name: str, email: str):
        self.signup_name.fill(name)
        self.signup_email.fill(email)
        self.signup_button.click()


    def fill_account_information(self, password: str, first_name: str, last_name: str, address: str, state: str, city: str, zipcode: str, mobile_number: str):
        self.title_mr.check()
        self.password.fill(password)

        self.days.select_option("1")
        self.months.select_option("1")
        self.years.select_option("2000")

        self.first_name.fill(first_name)
        self.last_name.fill(last_name)
        self.address.fill(address)

        self.country.select_option("India")

        self.state.fill(state)
        self.city.fill(city)
        self.zipcode.fill(zipcode)
        self.mobile_number.fill(mobile_number)


    def create_account(self):
        self.create_account_button.click()


    def is_account_created(self) -> bool:
        return self.page.get_by_text("Account Created!").is_visible()


    def register_user(self, user: dict):
        self.start_signup(name=user["name"], email=user["email"])
        self.fill_account_information(
            password=user["password"],
            first_name = user["first_name"],
            last_name = user["last_name"],
            address = user["address"],
            state = user["state"],
            city = user["city"],
            zipcode = user["zipcode"],
            mobile_number=user["mobile_number"]
        )
        self.create_account()

