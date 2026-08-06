import pytest
from playwright.sync_api import Page
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.payment_page import PaymentPage
from pages.order_confirmation_page import OrderConfirmationPage
from utils.test_data_loader import TestDataLoader


@pytest.mark.ui
@pytest.mark.regression
def test_successful_payment(page: Page, config: dict, test_user: dict):
    home_page = HomePage(page)
    login_page = LoginPage(page)
    product_page = ProductPage(page)
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)
    payment_page = PaymentPage(page)
    order_confirmation_page = OrderConfirmationPage(page)

    base_url = config["environment_config"]["base_url"]

    product_name = next(iter(TestDataLoader.load_products()))
    payment = TestDataLoader.get_payment("default")

    # Login
    home_page.open(base_url=base_url)

    login_page.open_login_page(base_url=base_url)
    login_page.login(email=test_user["email"], password=test_user["password"])

    # Add Product
    product_page.open_products_page()
    product_page.search_product(product_name=product_name)
    product_page.add_product_to_cart(product_name=product_name)

    product_page.view_cart()

    # Checkout
    cart_page.proceed_to_checkout()
    assert checkout_page.is_checkout_page_displayed()
    checkout_page.place_order()

    # Payment
    payment_page.enter_payment_details(
        name_on_card=payment["name_on_card"],
        card_number=payment["card_number"],
        cvc=payment["cvc"],
        expiry_month=payment["expiry_month"],
        expiry_year=payment["expiry_year"]
    )
    payment_page.confirm_payment()

    # Validation
    assert order_confirmation_page.is_order_confirmed()

