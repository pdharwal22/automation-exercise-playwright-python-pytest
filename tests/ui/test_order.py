import allure
import pytest
from playwright.sync_api import Page
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.payment_page import PaymentPage
from pages.order_page import OrderPage
from utils.test_data_loader import TestDataLoader


@allure.feature("Order")
@allure.story("Place Order")
@allure.title("Verify user can place an order successfully")
@allure.description("Verify that a registered user can successfully place an order by adding product to the cart, completing checkout, making paymentm and receiving the order confirmation message.")
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.ui
@pytest.mark.regression
def test_order_placed_successfully(page: Page, config: dict, test_user: dict):
    home_page = HomePage(page)
    login_page = LoginPage(page)
    product_page = ProductPage(page)
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)
    payment_page = PaymentPage(page)
    order_page = OrderPage(page)

    base_url = config["environment_config"]["base_url"]

    product_name = next(iter(TestDataLoader.load_products()))
    payment = TestDataLoader.get_payment("default")
    order = TestDataLoader.get_order()

    allure.dynamic.parameter("Product", product_name)
    allure.dynamic.parameter("Payment Profile", "default")

    with allure.step("Open the application"):
        home_page.open(base_url=base_url)

    with allure.step("Login with registered user"):
        login_page.open_login_page(base_url=base_url)
        login_page.login(email=test_user["email"], password=test_user["password"])

    with allure.step(f"Search product '{product_name}'"):
        product_page.open_products_page()
        product_page.search_product(product_name=product_name)

    with allure.step("Add product to cart"):
        product_page.add_product_to_cart(product_name=product_name)
        assert product_page.is_product_added_message_displayed()

    with allure.step("Open shopping cart"):
        product_page.view_cart()

    with allure.step("Proceed to checkout"):
        cart_page.proceed_to_checkout()
        assert checkout_page.is_checkout_page_displayed()

    with allure.step("Place order from checkout page"):
        checkout_page.place_order()

    with allure.step("Enter payment details"):
        payment_page.enter_payment_details(
            name_on_card=payment["name_on_card"],
            card_number=payment["card_number"],
            cvc=payment["cvc"],
            expiry_month=payment["expiry_month"],
            expiry_year=payment["expiry_year"]
        )

    with allure.step("Confirm payment"):
        payment_page.confirm_payment()

    with allure.step("Verify order confirmation"):
        assert order_page.is_order_successful()
        assert order_page.get_success_message() == order["success_message"]

